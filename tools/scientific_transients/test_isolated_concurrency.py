"""Actual loopback HTTP tests; no credential lookup or external network."""
import unittest
from unittest.mock import patch

from tools.scientific_transients import isolated_concurrency as subject
from tools.scientific_transients.queue import STATE_KEY


class IsolatedConcurrencyTests(unittest.TestCase):
    def test_two_http_executors_same_generation_cas_and_backup(self):
        with subject.OfflineController() as controller:
            receipt = controller.run()
            self.assertEqual(receipt["httpExecutors"], 2)
            self.assertEqual(receipt["requests"], 6)
            self.assertEqual(len(receipt["backupVerification"]), 6)
            self.assertEqual(sum(not row["committed"] for row in receipt["primaryAttempts"]), 2)
            for phase in ("REGISTER", "CREATE"):
                rows = [row for row in receipt["observedReads"] if row["phase"] == phase]
                self.assertEqual({row["executor"] for row in rows}, {"A", "B"})
                self.assertEqual(len({row["generation"] for row in rows}), 1)
            self.assertFalse(receipt["realProvider412"])
            self.assertFalse(receipt["S4Closed"])
        self.assertTrue(all(not thread.is_alive() for thread in controller.threads))

    def test_barrier_timeout_has_no_primary_or_backup_write(self):
        with subject.OfflineController(barrier_timeout=0.1) as controller:
            controller.rendezvous.arm("UNPAIRED")
            body = {field: "1" * 32 for field in subject.BINDING_FIELDS}
            status, _ = controller.request("A", "/v1/transient-analysis/worker/register", body)
            self.assertEqual(status, 503)
            self.assertEqual(controller.primary.items, {})
            self.assertEqual(controller.backup.items, {})
            with self.assertRaisesRegex(RuntimeError, "PAIR_NOT_OBSERVED"):
                controller.rendezvous.finish()

    def test_auth_failures_do_not_write(self):
        with subject.OfflineController() as controller:
            request = {"requestId": "1" * 32, "bindingRef": "2" * 32}
            self.assertEqual(controller.request("A", "/v1/transient-analysis/jobs", request,
                                               owner=True, token="bad")[0], 403)
            self.assertEqual(controller.request("B", "/v1/transient-analysis/jobs", request,
                                               owner=True, origin="https://wrong.invalid")[0], 403)
            binding = {field: "1" * 32 for field in subject.BINDING_FIELDS}
            self.assertEqual(controller.request("A", "/v1/transient-analysis/worker/register", binding,
                                               origin=subject.ORIGIN)[0], 403)
            self.assertEqual(controller.primary.items, {})

    def test_uncertain_pair_never_automatically_replays(self):
        with subject.OfflineController() as controller:
            with patch.object(controller, "request", return_value=(503, {"error": "UNAVAILABLE"})) as request:
                with self.assertRaisesRegex(RuntimeError, "STOP_NO_REPLAY"):
                    controller.pair("FAIL", "/v1/transient-analysis/jobs", [{}, {}], owner=True)
                self.assertEqual(request.call_count, 2)
            self.assertEqual(controller.primary.items, {})

    def test_budget_rejected_before_another_http_request(self):
        with subject.OfflineController() as controller:
            controller.requests = 40
            with self.assertRaisesRegex(RuntimeError, "REQUEST_BUDGET"):
                controller.request("A", "/health")
            self.assertEqual(controller.requests, 40)
            self.assertEqual(controller.primary.get(STATE_KEY), (None, 0))

    def test_missing_backup_prevents_pass(self):
        with subject.OfflineController() as controller:
            with patch.object(controller.backup, "get", return_value=(None, 0)):
                with self.assertRaisesRegex(RuntimeError, "BACKUP_NOT_VERIFIED"):
                    controller.run()


if __name__ == "__main__":
    unittest.main()
