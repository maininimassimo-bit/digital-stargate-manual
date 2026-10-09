"""Real optional SDK API smoke tests with ADC/network patched BEFORE factory calls."""
import unittest
from unittest.mock import patch

from google.auth.compute_engine.credentials import Credentials
from google.auth.credentials import AnonymousCredentials
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests

from tools.pixinsight.local_pilot.transport_http import google_owner, AuthError
from tools.scientific_transients.lab_cloud_transport import make_cloud_stores
from tools.scientific_transients.lab_gateway import RequestBudget
from tools.scientific_registry.ingestion_storage import Conflict

IDENTITY = "dsg-s4-lab-fixture@digital-stargate-telemetry.iam.gserviceaccount.com"
OFFLINE_ENV = {"DISABLE_GCS_PYTHON_CLIENT_OTEL_BUCKET_METADATA": "true"}
CONFIG = {"primaryBucket": "fixture-primary", "backupBucket": "fixture-backup",
          "runtimeServiceAccount": IDENTITY, "project": "digital-stargate-telemetry",
          "ownerEmail": "owner@example.invalid", "googleClientId": "fixture.apps.googleusercontent.com"}


class OfflineCredentials(Credentials):
    def __init__(self, service_account_email=IDENTITY, **kwargs):
        kwargs.setdefault("universe_domain", "googleapis.com")
        super().__init__(service_account_email=service_account_email, **kwargs)

    def refresh(self, request):
        # No metadata server, token or real service identity is consulted.
        self.token = "public-offline-fixture"


class SDKChecks(unittest.TestCase):
    def test_real_gcs_sdk_synthetic_412_is_counted_and_translated_without_retry(self):
        def denied(request, **kwargs):
            response = requests.Response();response.status_code = 412
            response.url = request.url;response.request = request
            response.headers["Content-Type"] = "application/json"
            response._content = b'{"error":{"code":412,"message":"synthetic precondition"}}'
            return response
        with patch.dict("os.environ", OFFLINE_ENV, clear=True), patch("google.auth.default",
                side_effect=lambda **_: (OfflineCredentials(), "fixture")), \
                patch("socket.create_connection", side_effect=AssertionError("NETWORK_FORBIDDEN")), \
                patch.object(requests.adapters.HTTPAdapter, "send", side_effect=denied) as send:
            budget = RequestBudget();stores, _, close = make_cloud_stores(CONFIG, budget)
            try:
                with self.assertRaises(Conflict):stores["A"][0].put("control/test.json", b"{}", 0)
                rows = budget.snapshot()
                self.assertEqual(send.call_count, 1)
                self.assertEqual(send.call_count, len(rows))
                self.assertEqual([(row["kind"], row["status"]) for row in rows
                                  if row["kind"] == "GCS_UPLOAD"], [("GCS_UPLOAD", 412)])
                self.assertTrue(all(row["status"] == 412 for row in rows))
            finally:close()

    def test_real_sdk_factory_builds_four_independent_clients_without_network(self):
        with patch.dict("os.environ", OFFLINE_ENV, clear=True), patch("google.auth.default",
                side_effect=lambda **_: (OfflineCredentials(), "digital-stargate-telemetry")) as adc, \
                patch.object(requests.Session, "send", side_effect=AssertionError("NETWORK_FORBIDDEN")):
            budget = RequestBudget()
            stores, owner, close = make_cloud_stores(CONFIG, budget)
            try:
                self.assertEqual(adc.call_count, 4)
                clients = [store.bucket.client for pair in stores.values() for store in pair]
                self.assertEqual(len({id(client) for client in clients}), 4)
                self.assertEqual(len({id(client._http) for client in clients}), 4)
                self.assertEqual(budget.snapshot(), [])
                with patch.object(id_token, "verify_oauth2_token", return_value={
                        "email": "owner@example.invalid", "email_verified": True}) as verify:
                    owner("public-fixture")
                    self.assertIsInstance(verify.call_args.args[1], Request)
                    self.assertEqual(verify.call_args.args[2], CONFIG["googleClientId"])
            finally:close()

    def test_user_adc_or_wrong_service_identity_cannot_build_clients(self):
        for credentials in (AnonymousCredentials(), OfflineCredentials("old@example.invalid")):
            with self.subTest(kind=type(credentials).__name__), patch.dict("os.environ", OFFLINE_ENV, clear=True), \
                    patch("google.auth.default", return_value=(credentials, "fixture")), \
                    patch.object(requests.Session, "send", side_effect=AssertionError("NETWORK_FORBIDDEN")):
                with self.assertRaises(ValueError):make_cloud_stores(CONFIG, RequestBudget())

    def test_owner_verifier_preserves_audience_email_verified_and_failure_checks(self):
        request = object()
        for claims in ({"email": "wrong@example.invalid", "email_verified": True},
                       {"email": "owner@example.invalid", "email_verified": False}, {}):
            with patch.object(id_token, "verify_oauth2_token", return_value=claims) as verify:
                with self.assertRaises(AuthError):google_owner("fixture", "audience", "owner@example.invalid", request=request)
                self.assertEqual(verify.call_args.args, ("fixture", request, "audience"))
        with patch.object(id_token, "verify_oauth2_token", side_effect=ValueError("signature/issuer/audience rejected")):
            with self.assertRaises(AuthError):google_owner("fixture", "audience", "owner@example.invalid", request=request)


if __name__ == "__main__":unittest.main()
