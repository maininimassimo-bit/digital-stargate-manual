"""Synthetic P4 persistence and real loopback HTTP; no cloud or PixInsight OAT."""
import copy
import datetime as dt
import concurrent.futures
import hashlib
import importlib.util
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import Broker, ProtocolError, STATE_KEY, encode, decode
from tools.pixinsight.local_pilot.transport_http import handler_for, AuthError
from tools.pixinsight.local_pilot.transport import Transport, SessionWorker
from tools.pixinsight.local_pilot import worker
from tools.scientific_registry.ingestion_storage import MemoryStore, BackedUpStore, Conflict

WORKER = "a" * 32
TOKEN = "b" * 64
INPUT = "c" * 32
REQUEST = {"schemaVersion": "1.0", "requestId": "d" * 32, "inputRef": INPUT,
           "recipe": worker.RECIPE, "aiMode": "SESSION_ASSISTED"}


class BrokerTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime(2026, 10, 5, tzinfo=dt.timezone.utc)
        self.primary, self.backup = MemoryStore(), MemoryStore()
        self.broker = Broker(BackedUpStore(self.primary, self.backup), WORKER, lambda: self.now)

    def claim(self):
        self.broker.create(REQUEST)
        return self.broker.claim(WORKER)

    def report(self, claim, stage, sequence=1, processes=0, outputs=0):
        return dict(leaseToken=claim["leaseToken"], sequence=sequence, stage=stage,
                    processCount=processes, outputCount=outputs, verified=stage == "COMPLETED")

    def test_create_duplicate_restart_and_conflict(self):
        first = self.broker.create(REQUEST)
        restarted = Broker(BackedUpStore(self.primary, self.backup), WORKER, lambda: self.now)
        self.assertEqual(first, restarted.create(REQUEST))
        with self.assertRaisesRegex(ProtocolError, "IDEMPOTENCY"):
            restarted.create({**REQUEST, "inputRef": "e" * 32})
        self.assertTrue(self.backup.items)

    def test_scripts_paths_parameters_and_paid_modes_rejected(self):
        for request in ({**REQUEST, "script": "evil"}, {**REQUEST, "path": "private"},
                        {**REQUEST, "recipe": "ARBITRARY"}, {**REQUEST, "aiMode": "API"}):
            with self.assertRaises(ProtocolError):
                self.broker.create(request)
        self.assertEqual(self.primary.items, {})

    def test_single_claim_lost_response_and_no_offline_reassignment(self):
        claim = self.claim()
        self.broker.create({**REQUEST, "requestId": "e" * 32})
        self.now += dt.timedelta(days=365)
        self.assertEqual(self.broker.status(claim["jobId"])["connection"], "OFFLINE")
        self.assertEqual(claim["leaseToken"], self.broker.claim(WORKER)["leaseToken"])
        self.assertEqual(claim["jobId"], self.broker.claim(WORKER)["jobId"])
        with self.assertRaises(ProtocolError):
            self.broker.claim("f" * 32)

    def test_status_never_exposes_lease_and_clock_uncertainty(self):
        claim = self.claim()
        self.broker.report(claim["jobId"], WORKER, self.report(claim, "AWAITING_NATIVE"))
        status = self.broker.status(claim["jobId"])
        self.assertNotIn("leaseToken", encode(status).decode())
        self.assertEqual(status["executionEvidence"], "WORKER_REPORTED_NOT_ATTESTED")
        self.now -= dt.timedelta(seconds=1)
        self.assertEqual(self.broker.status(claim["jobId"])["connection"], "CLOCK_UNCERTAIN")

    def test_concurrent_claims_have_one_durable_identity(self):
        self.broker.create(REQUEST)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            claims = list(pool.map(lambda _: self.broker.claim(WORKER), range(4)))
        self.assertEqual(len({item["leaseToken"] for item in claims}), 1)
        self.assertEqual(len({item["jobId"] for item in claims}), 1)

    def test_report_duplicate_changed_content_gap_and_stale_lease(self):
        claim = self.claim()
        report = self.report(claim, "AWAITING_NATIVE")
        self.broker.report(claim["jobId"], WORKER, report)
        self.broker.report(claim["jobId"], WORKER, report)
        for bad in ({**report, "stage": "RUNNING"}, {**report, "sequence": 3}, {**report, "leaseToken": "0" * 64}):
            with self.assertRaises(ProtocolError):
                self.broker.report(claim["jobId"], WORKER, bad)

    def test_complete_requires_counts_and_verified_then_immutable(self):
        claim = self.claim()
        with self.assertRaisesRegex(ProtocolError, "COMPLETION_INCOMPLETE"):
            self.broker.report(claim["jobId"], WORKER, self.report(claim, "COMPLETED"))
        report = self.report(claim, "COMPLETED", processes=5, outputs=5)
        self.broker.report(claim["jobId"], WORKER, report)
        self.broker.report(claim["jobId"], WORKER, report)
        with self.assertRaises(ProtocolError):
            self.broker.report(claim["jobId"], WORKER, self.report(claim, "RUNNING", sequence=2))
        self.assertIsNone(self.broker.claim(WORKER))

    def test_recipe_count_and_stage_regression(self):
        claim = self.claim()
        for bad in (self.report(claim, "RUNNING", processes=6), self.report(claim, "RUNNING", outputs=6)):
            with self.assertRaises(ProtocolError):
                self.broker.report(claim["jobId"], WORKER, bad)
        self.broker.report(claim["jobId"], WORKER, self.report(claim, "RUNNING", processes=1))
        for bad in (self.report(claim, "PREPARED", sequence=2, processes=1), self.report(claim, "RUNNING", sequence=2)):
            with self.assertRaises(ProtocolError):
                self.broker.report(claim["jobId"], WORKER, bad)

    def test_cancel_queued_and_active_and_recovery_holds_queue(self):
        queued = self.broker.create(REQUEST)
        self.broker.cancel(queued["jobId"])
        self.assertIsNone(self.broker.claim(WORKER))
        self.broker.create({**REQUEST, "requestId": "e" * 32})
        claim = self.broker.claim(WORKER)
        self.broker.cancel(claim["jobId"])
        self.assertTrue(self.broker.claim(WORKER)["cancelRequested"])
        self.broker.report(claim["jobId"], WORKER, self.report(claim, "RECOVERY_REQUIRED"))
        self.broker.create({**REQUEST, "requestId": "f" * 32})
        self.assertEqual(claim["jobId"], self.broker.claim(WORKER)["jobId"])

    def test_backup_failure_and_primary_conflict(self):
        with patch.object(self.backup, "put", side_effect=RuntimeError("offline")):
            with self.assertRaises(RuntimeError):
                self.broker.create(REQUEST)
        self.assertEqual(self.primary.items, {})
        original = self.primary.put
        calls = 0
        def once(*args):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise Conflict()
            return original(*args)
        with patch.object(self.primary, "put", side_effect=once):
            self.broker.create(REQUEST)
        self.assertEqual(len(decode(self.primary.get(STATE_KEY)[0])["jobs"]), 1)

    def test_capacity_preserves_existing_jobs(self):
        for i in range(16):
            self.broker.create({**REQUEST, "requestId": f"{i:032x}"})
        before = self.primary.get(STATE_KEY)
        with self.assertRaisesRegex(ProtocolError, "CAPACITY"):
            self.broker.create(REQUEST)
        self.assertEqual(before, self.primary.get(STATE_KEY))

    def test_duplicate_json_nonfinite_and_changed_worker_rejected(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}'):
            with self.assertRaises(ProtocolError):
                decode(raw)
        self.broker.create(REQUEST)
        with self.assertRaisesRegex(ProtocolError, "STATE_IDENTITY"):
            Broker(self.primary, "f" * 32).claim("f" * 32)

    def test_deployment_startup_refuses_missing_activation_without_cloud_access(self):
        app = Path(__file__).resolve().parents[3] / "infrastructure/pixinsight-pilot/app.py"
        spec = importlib.util.spec_from_file_location("piai_candidate", app)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch.dict(os.environ, {}, clear=True), patch.object(module, "GCSStore", side_effect=AssertionError("no cloud access")):
            with self.assertRaisesRegex(ProtocolError, "ACTIVATION_REQUIRED"):
                module.main()


class HttpHarness(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.broker = Broker(self.store, WORKER)
        def authenticate(token):
            if token != "synthetic-owner":
                raise AuthError()
        self.server = HTTPServer(("127.0.0.1", 0), handler_for(self.broker, authenticate,
                              "https://portal.invalid", hashlib.sha256(TOKEN.encode()).hexdigest()))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.origin = f"http://127.0.0.1:{self.server.server_port}"
        self.client = Transport(self.origin, TOKEN, test_loopback=True)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, path, payload=None, token=None, origin=None, raw=None):
        headers = {}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        if origin is not None:
            headers["Origin"] = origin
        data = raw if raw is not None else encode(payload) if payload is not None else None
        if data:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(self.origin + path, data, headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status, decode(response.read())
        except urllib.error.HTTPError as error:
            return error.code, decode(error.read())

    def create(self):
        return self.request("/v1/jobs", REQUEST, "synthetic-owner", "https://portal.invalid")[1]


class HttpTests(HttpHarness):
    def test_roles_origins_and_anonymous_denial(self):
        for token, origin in ((None, None), (TOKEN, None), ("synthetic-owner", None), ("synthetic-owner", "https://evil.invalid")):
            self.assertEqual(self.request("/v1/jobs", REQUEST, token, origin)[0], 403)
        self.assertEqual(self.request("/v1/worker/claim", {"workerId": WORKER}, "synthetic-owner")[0], 403)
        self.assertEqual(self.request("/v1/worker/claim", {"workerId": WORKER}, TOKEN, "https://portal.invalid")[0], 403)
        self.assertEqual(self.store.items, {})

    def test_authenticated_http_roundtrip_restart_and_status_minimization(self):
        item = self.create()
        claimed = self.client.post("/v1/worker/claim", {"workerId": WORKER})["job"]
        restarted = Transport(self.origin, TOKEN, test_loopback=True)
        self.assertEqual(claimed, restarted.post("/v1/worker/claim", {"workerId": WORKER})["job"])
        report = dict(leaseToken=claimed["leaseToken"], sequence=1, stage="COMPLETED", processCount=5, outputCount=5, verified=True)
        restarted.post("/v1/worker/" + item["jobId"] + "/report", {"workerId": WORKER, "report": report})
        code, status = self.request("/v1/jobs/" + item["jobId"], token="synthetic-owner", origin="https://portal.invalid")
        self.assertEqual(code, 200)
        self.assertEqual(status["job"]["state"], "COMPLETED")
        self.assertNotIn(claimed["leaseToken"], json.dumps(status))

    def test_body_limits_duplicate_fields_and_unknown_routes(self):
        for raw in (b'{"workerId":"a","workerId":"b"}', b"x" * 16385):
            self.assertEqual(self.request("/v1/worker/claim", token=TOKEN, raw=raw)[0], 400)
        self.assertEqual(self.request("/v1/worker/unknown", {}, TOKEN)[0], 404)
        self.assertEqual(self.store.items, {})

    def test_production_refuses_http_and_nonpinned_origins(self):
        for origin in (self.origin, "https://evil.invalid", "https://dsg.run.app/?q=x", "https://u:p@dsg.run.app", "https://dsg.run.app:8443"):
            with self.assertRaises(ProtocolError):
                Transport(origin, TOKEN)
        Transport("https://dsg-pilot-123.europe-west1.run.app", TOKEN)

    def test_redirect_refused_without_forwarding_credential(self):
        received = []
        class Target(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append(self.headers.get("Authorization"))
                self.send_response(200); self.end_headers()
            def log_message(self, *_):
                pass
        target = HTTPServer(("127.0.0.1", 0), Target)
        target_thread = threading.Thread(target=target.serve_forever, daemon=True); target_thread.start()
        class Redirect(Target):
            def do_POST(self):
                self.send_response(307)
                self.send_header("Location", f"http://127.0.0.1:{target.server_port}/stolen")
                self.end_headers()
        redirect = HTTPServer(("127.0.0.1", 0), Redirect)
        redirect_thread = threading.Thread(target=redirect.serve_forever, daemon=True); redirect_thread.start()
        try:
            with self.assertRaises(ProtocolError):
                Transport(f"http://127.0.0.1:{redirect.server_port}", TOKEN, test_loopback=True).post("/v1/worker/claim", {"workerId": WORKER})
            self.assertEqual(received, [])
        finally:
            redirect.shutdown(); redirect.server_close(); redirect_thread.join()
            target.shutdown(); target.server_close(); target_thread.join()


class SessionTests(HttpHarness):
    def setUp(self):
        super().setUp()
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "worker"; self.root.mkdir()
        sources = base / "sources"; sources.mkdir()
        inputs = []
        for role in worker.ROLES:
            source = sources / (role + ".xisf"); source.write_bytes(("synthetic " + role).encode())
            inputs.append(dict(role=role, path=str(source), sha256=worker.digest(source), imageIndex=0, width=10, height=12))
        request = dict(schemaVersion="1.0", jobId="LocalSelection", recipe=worker.RECIPE, inputs=inputs,
                       background=dict(polyDegree=1, boxSize=12, boxSeparation=16))
        self.registry = {INPUT: request}
        self.session = SessionWorker(self.root, self.registry, WORKER, self.client)

    def tearDown(self):
        super().tearDown()
        self.tmp.cleanup()

    def test_prepare_once_without_launch_or_private_upload(self):
        item = self.create()
        first = self.session.cycle()
        self.assertEqual(first["state"], "AWAITING_NATIVE")
        job = self.root / item["jobId"]
        original = worker.digest(job / "manifest.json")
        restarted = SessionWorker(self.root, self.registry, WORKER, self.client)
        with patch.object(worker, "prepare", side_effect=AssertionError("must not repeat")):
            self.assertEqual(restarted.cycle()["state"], "AWAITING_NATIVE")
        self.assertEqual(original, worker.digest(job / "manifest.json"))
        self.assertFalse((job / "terminal.json").exists())
        remote = self.store.get(STATE_KEY)[0].decode()
        self.assertNotIn(str(self.root), remote)
        self.assertNotIn(self.registry[INPUT]["inputs"][0]["sha256"], remote)
        self.assertNotIn("background", remote)

    def test_lost_report_response_retries_identical_without_reprepare(self):
        self.create()
        original = self.client.post
        def lost(path, payload):
            result = original(path, payload)
            if path.endswith("/report"):
                raise ProtocolError("lost response")
            return result
        with patch.object(self.client, "post", side_effect=lost):
            with self.assertRaises(ProtocolError):
                self.session.cycle()
        with patch.object(worker, "prepare", side_effect=AssertionError("duplicate preparation")):
            self.assertEqual(self.session.cycle()["state"], "AWAITING_NATIVE")

    def test_active_cancel_uses_local_token_marker_and_keeps_reservation(self):
        item = self.create(); self.session.cycle()
        self.request("/v1/jobs/" + item["jobId"] + "/cancel", {}, "synthetic-owner", "https://portal.invalid")
        self.session.cycle()
        job = self.root / item["jobId"]
        marker = decode((job / "cancel.json").read_bytes())
        self.assertEqual(marker["token"], decode((job / "manifest.json").read_bytes())["token"])
        self.assertTrue((self.root / "active-job.json").exists())

    def test_collection_requires_explicit_native_stopped_then_closes(self):
        item = self.create(); self.session.cycle()
        job = self.root / item["jobId"]
        manifest = decode((job / "manifest.json").read_bytes())
        worker.write_new(job / "terminal.json", dict(jobId=item["jobId"], token=manifest["token"],
            runtimeSha256=manifest["runtimeSha256"], status="CANCELLED", outputs=[], processCount=0))
        with patch.object(worker, "collect", side_effect=AssertionError("must await owner")):
            self.assertEqual(self.session.cycle()["state"], "AWAITING_NATIVE")
        self.assertEqual(self.session.cycle(native_stopped=True)["state"], "CANCELLED")
        self.assertFalse((self.root / "active-job.json").exists())
        self.assertFalse((self.root / "transport/active.json").exists())
        self.assertEqual(self.session.cycle()["state"], "IDLE")

    def test_unregistered_input_and_failed_preparation_hold_queue(self):
        self.create()
        self.session.registry = {}
        self.assertEqual(self.session.cycle()["state"], "RECOVERY_REQUIRED")
        self.assertEqual(self.session.cycle()["state"], "RECOVERY_REQUIRED")
        self.assertFalse((self.root / ("PIAI_" + REQUEST["requestId"])).exists())

    def test_crash_after_terminal_ack_before_local_close_recovers(self):
        item = self.create(); self.session.cycle()
        folder = self.root / "transport" / item["jobId"]
        remote = self.broker.claim(WORKER)
        message = dict(leaseToken=remote["leaseToken"], sequence=2, stage="CANCELLED", processCount=0, outputCount=0, verified=False)
        self.broker.report(item["jobId"], WORKER, message)
        worker.write_new(folder / "ack-002.json", message)
        # Simulated crash after durable ack: no new remote claim or preparation.
        with patch.object(self.client, "post", side_effect=AssertionError("must close before claiming")):
            self.assertEqual(self.session.cycle()["state"], "ACKNOWLEDGED")
        self.assertFalse((self.root / "transport/active.json").exists())

    def test_local_busy_root_preserved_and_recovery_reported(self):
        self.create()
        worker.write_new(self.root / "active-job.json", {"jobId": "Other", "token": "private"})
        self.assertEqual(self.session.cycle()["state"], "RECOVERY_REQUIRED")
        self.assertEqual(decode((self.root / "active-job.json").read_bytes())["jobId"], "Other")

    def test_collection_failure_preserves_original_local_reservation(self):
        item = self.create(); self.session.cycle()
        job = self.root / item["jobId"]
        worker.write_new(job / "terminal.json", {"status": "COMPLETED"})
        self.assertEqual(self.session.cycle(native_stopped=True)["state"], "RECOVERY_REQUIRED")
        self.assertTrue((self.root / "active-job.json").exists())

    def test_network_failure_and_concurrent_cycle_do_not_prepare(self):
        self.create()
        with patch.object(self.client, "post", side_effect=ProtocolError("offline")):
            with self.assertRaises(ProtocolError):
                self.session.cycle()
        self.assertFalse((self.root / "active-job.json").exists())
        worker.write_new(self.root / "transport/cycle-lock.json", {"crash": True})
        with self.assertRaises(FileExistsError):
            self.session.cycle()
        self.assertFalse((self.root / "active-job.json").exists())


if __name__ == "__main__":
    unittest.main()
