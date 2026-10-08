"""Synthetic lifecycle and real loopback HTTP, not cloud/native scientific OAT."""
import concurrent.futures
import datetime as dt
import hashlib
import importlib.util
import os
from pathlib import Path
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from unittest.mock import patch

from tools.scientific_transients.queue import TransientQueue, STATE_KEY, LEASE_SECONDS
from tools.pixinsight.local_pilot.broker import Broker, ProtocolError, decode, encode
from tools.pixinsight.local_pilot.transport_http import handler_for, AuthError
from tools.scientific_registry.ingestion_storage import MemoryStore, BackedUpStore, Conflict

WORKER, ROOT, TOKEN = "a" * 32, "b" * 32, "c" * 64
LEGACY_WORKER, LEGACY_TOKEN = "d" * 32, "e" * 64
BINDING = dict(bindingRef="1" * 32, inputRef="2" * 32, referenceRef="3" * 32,
               algorithmRef="4" * 32, contractRef="5" * 32)
REQUEST = dict(requestId="6" * 32, bindingRef=BINDING["bindingRef"])
RESULT = dict(reportSha256="7" * 64, bindingRef=BINDING["bindingRef"],
              qualityCounts=dict(measured=10, excluded=2, incomplete=1))


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime(2026, 10, 8, tzinfo=dt.timezone.utc)
        self.primary, self.backup = MemoryStore(), MemoryStore()
        self.store = BackedUpStore(self.primary, self.backup)
        self.queue = TransientQueue(self.store, WORKER, lambda: self.now)

    def claim(self):
        self.queue.register(BINDING)
        self.queue.create(REQUEST)
        return self.queue.claim(dict(workerId=WORKER, rootId=ROOT))["job"]

    def report(self, job, stage="RUNNING", sequence=1, result=None):
        return dict(attemptId=job["attemptId"], leaseToken=job["leaseToken"],
                    sequence=sequence, stage=stage, result=result)

    def complete(self):
        job = self.claim()
        self.queue.report(job["jobId"], self.report(job))
        self.queue.report(job["jobId"], self.report(job, "COMPLETED", 2, RESULT))
        return job

    def test_immutable_binding_and_request_across_restart(self):
        self.queue.register(BINDING)
        job = self.queue.create(REQUEST)
        restarted = TransientQueue(self.store, WORKER, lambda: self.now)
        self.assertEqual(restarted.create(REQUEST), job)
        for changed in (dict(BINDING, inputRef="8" * 32), dict(BINDING, contractRef="8" * 32)):
            with self.assertRaisesRegex(ProtocolError, "BINDING_CONFLICT"):
                restarted.register(changed)
        with self.assertRaisesRegex(ProtocolError, "IDEMPOTENCY_CONFLICT"):
            restarted.create(dict(REQUEST, bindingRef="8" * 32))

    def test_unregistered_and_executable_private_fields_never_persist(self):
        for payload in (REQUEST, dict(REQUEST, path="F:/private"), dict(REQUEST, sql="SELECT")):
            with self.assertRaises(ProtocolError):
                self.queue.create(payload)
        with self.assertRaises(ProtocolError):
            self.queue.register(dict(BINDING, referenceRef="https://provider.invalid"))
        self.assertEqual(self.primary.items, {})

    def test_concurrent_claim_one_attempt_and_root_pinned(self):
        self.queue.register(BINDING)
        self.queue.create(REQUEST)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            jobs = list(pool.map(lambda _: self.queue.claim(dict(workerId=WORKER, rootId=ROOT))["job"], range(4)))
        self.assertEqual(len({j["attemptId"] for j in jobs}), 1)
        self.assertEqual(len({j["leaseToken"] for j in jobs}), 1)
        for bad in (dict(workerId=LEGACY_WORKER, rootId=ROOT), dict(workerId=WORKER, rootId="8" * 32)):
            with self.assertRaises(ProtocolError):
                self.queue.claim(bad)

    def test_expiry_commits_recovery_even_if_stale_delivery_rejected(self):
        job = self.claim()
        self.queue.report(job["jobId"], self.report(job))
        self.queue.create(dict(REQUEST, requestId="8" * 32))
        self.now += dt.timedelta(seconds=LEASE_SECONDS)
        with self.assertRaises(ProtocolError):
            self.queue.report(job["jobId"], self.report(job, "COMPLETED", 2, RESULT))
        self.assertEqual(decode(self.primary.get(STATE_KEY)[0])["jobs"][0]["state"], "RECOVERY_REQUIRED")
        self.assertEqual(self.queue.claim(dict(workerId=WORKER, rootId=ROOT))["job"]["jobId"], job["jobId"])

    def test_clock_rollback_freezes_without_reallocation(self):
        job = self.claim()
        self.now += dt.timedelta(seconds=10)
        self.queue.report(job["jobId"], self.report(job))
        self.now -= dt.timedelta(seconds=1)
        self.assertEqual(self.queue.status(job["jobId"])["state"], "RECOVERY_REQUIRED")

    def test_identical_report_retry_does_not_renew_lease(self):
        job = self.claim()
        report = self.report(job)
        first = self.queue.report(job["jobId"], report)
        self.now += dt.timedelta(seconds=10)
        self.assertEqual(self.queue.report(job["jobId"], report), first)
        with self.assertRaises(ProtocolError):
            self.queue.report(job["jobId"], dict(report, stage="FAILED"))
        renewed = self.queue.report(job["jobId"], self.report(job, sequence=2))
        self.assertNotEqual(first["leaseExpiresAt"], renewed["leaseExpiresAt"])

    def test_result_binding_sequence_and_terminal_immutability(self):
        job = self.claim()
        with self.assertRaises(ProtocolError):
            self.queue.report(job["jobId"], self.report(job, "COMPLETED", 1, RESULT))
        self.queue.report(job["jobId"], self.report(job))
        for bad in (self.report(job, "COMPLETED", 2, dict(RESULT, bindingRef="8" * 32)),
                    dict(self.report(job), leaseToken="0" * 64), self.report(job, sequence=3),
                    self.report(job, "COMPLETED", 2, dict(RESULT, pixels=[1, 2]))):
            with self.assertRaises(ProtocolError):
                self.queue.report(job["jobId"], bad)
        completed = self.report(job, "COMPLETED", 2, RESULT)
        first = self.queue.report(job["jobId"], completed)
        self.assertEqual(self.queue.report(job["jobId"], completed), first)
        with self.assertRaises(ProtocolError):
            self.queue.report(job["jobId"], self.report(job, sequence=3))
        self.assertIsNone(self.queue.claim(dict(workerId=WORKER, rootId=ROOT))["job"])

    def test_cancel_before_start_and_during_running_blocks_completion(self):
        self.queue.register(BINDING)
        job = self.queue.create(REQUEST)
        self.assertEqual(self.queue.cancel(job["jobId"])["state"], "CANCELLED")
        self.assertIsNone(self.queue.claim(dict(workerId=WORKER, rootId=ROOT))["job"])
        self.queue.create(dict(REQUEST, requestId="8" * 32))
        active = self.queue.claim(dict(workerId=WORKER, rootId=ROOT))["job"]
        self.queue.report(active["jobId"], self.report(active))
        self.queue.cancel(active["jobId"])
        with self.assertRaisesRegex(ProtocolError, "CANCEL_PENDING"):
            self.queue.report(active["jobId"], self.report(active, sequence=2))
        self.queue.report(active["jobId"], self.report(active, "CANCELLED", 2))
        with self.assertRaises(ProtocolError):
            self.queue.report(active["jobId"], self.report(active, "COMPLETED", 3, RESULT))

    def test_capacity_and_hostile_typed_fields_preserve_state(self):
        job = self.claim()
        before = self.primary.get(STATE_KEY)
        for bad in (dict(self.report(job), stage={}), dict(self.report(job), sequence=True),
                    self.report(job, "COMPLETED", 1, dict(RESULT, qualityCounts=dict(measured=True, excluded=0, incomplete=0)))):
            with self.assertRaises(ProtocolError):
                self.queue.report(job["jobId"], bad)
        self.assertEqual(before, self.primary.get(STATE_KEY))
        for i in range(31):
            self.queue.create(dict(REQUEST, requestId=f"{i:032x}"))
        before = self.primary.get(STATE_KEY)
        with self.assertRaisesRegex(ProtocolError, "CAPACITY"):
            self.queue.create(dict(REQUEST, requestId="f" * 32))
        self.assertEqual(before, self.primary.get(STATE_KEY))

    def test_review_bound_to_report_and_not_operational_acceptance(self):
        job = self.complete()
        request = dict(decisionId="8" * 32, reportSha256=RESULT["reportSha256"], decision="FOLLOW_UP")
        first = self.queue.review(job["jobId"], request)
        self.assertEqual(self.queue.review(job["jobId"], request), first)
        for bad in (dict(request, reportSha256="0" * 64), dict(request, decision="KEEP_FOR_REVIEW"),
                    dict(request, decision="ACCEPT_MILESTONE")):
            with self.assertRaises(ProtocolError):
                self.queue.review(job["jobId"], bad)
        public = self.queue.status(job["jobId"])
        self.assertNotIn(job["leaseToken"], encode(public).decode())
        self.assertEqual(public["scientificValidation"], "NOT_VALIDATED")
        self.assertEqual(public["publication"], "NONE")

    def test_backup_failure_cas_and_separate_piai_state(self):
        with patch.object(self.backup, "put", side_effect=RuntimeError("offline")):
            with self.assertRaises(RuntimeError):
                self.queue.register(BINDING)
        self.assertEqual(self.primary.items, {})
        put = self.primary.put
        calls = 0
        def conflict_once(*args):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise Conflict()
            return put(*args)
        with patch.object(self.primary, "put", side_effect=conflict_once):
            self.queue.register(BINDING)
        self.assertEqual(len(self.queue.options()["bindings"]), 1)
        self.assertIsNone(self.primary.get("control/piai-state.json")[0])


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.queue = TransientQueue(self.store, WORKER)
        def owner(token):
            if token != "synthetic-owner":
                raise AuthError()
        self.server = HTTPServer(("127.0.0.1", 0), handler_for(Broker(self.store, LEGACY_WORKER),
            owner, "https://portal.invalid", hashlib.sha256(LEGACY_TOKEN.encode()).hexdigest(),
            transient=self.queue, transient_worker_digest=hashlib.sha256(TOKEN.encode()).hexdigest()))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, path, data=None, token=None, owner=False):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        if owner:
            headers["Origin"] = "https://portal.invalid"
        request = urllib.request.Request(f"http://127.0.0.1:{self.server.server_port}" + path,
            encode(data) if data is not None else None, headers)
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, decode(response.read())
        except urllib.error.HTTPError as error:
            return error.code, decode(error.read())

    def test_new_and_old_credentials_cannot_cross_namespaces(self):
        base = "/v1/transient-analysis/worker/register"
        for token, owner in ((None, False), (LEGACY_TOKEN, False), ("synthetic-owner", True), (TOKEN, True)):
            self.assertEqual(self.request(base, BINDING, token, owner)[0], 403)
        self.assertEqual(self.request("/v1/worker/claim", dict(workerId=LEGACY_WORKER, rootId=ROOT), TOKEN)[0], 403)
        self.assertEqual(self.store.items, {})
        self.assertEqual(self.request(base, BINDING, TOKEN)[0], 200)

    def test_owner_worker_role_separation_and_private_http_flow(self):
        base = "/v1/transient-analysis"
        self.request(base + "/worker/register", BINDING, TOKEN)
        self.assertEqual(self.request(base + "/jobs", REQUEST, TOKEN)[0], 403)
        self.assertEqual(self.request(base + "/jobs", REQUEST, "non-owner", True)[0], 403)
        code, job = self.request(base + "/jobs", REQUEST, "synthetic-owner", True)
        self.assertEqual(code, 200)
        _, claim = self.request(base + "/worker/claim", dict(workerId=WORKER, rootId=ROOT), TOKEN)
        self.assertEqual(claim["job"]["jobId"], job["jobId"])
        code, status = self.request(base + "/jobs/" + job["jobId"], token="synthetic-owner", owner=True)
        self.assertEqual(code, 200)
        self.assertNotIn("leaseToken", status)
        self.assertEqual(self.request(base + "/jobs/" + job["jobId"] + "/cancel", {}, "synthetic-owner", True)[0], 200)
        self.assertEqual(self.request(base + "/worker/jobs/" + job["jobId"] + "/review", {}, TOKEN)[0], 404)

    def test_deployment_remains_disabled_and_identity_must_be_distinct(self):
        path = Path(__file__).resolve().parents[2] / "infrastructure/pixinsight-pilot/app.py"
        spec = importlib.util.spec_from_file_location("transient_candidate", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(module.transient_component(self.store, LEGACY_WORKER, "0" * 64), (None, None))
        with patch.dict(os.environ, {"DSG_TRANSIENT_ACTIVATION": "OWNER_AUTHORIZED",
                                    "DSG_TRANSIENT_WORKER_ID": LEGACY_WORKER,
                                    "DSG_TRANSIENT_WORKER_SHA256": "0" * 64}, clear=True):
            with self.assertRaisesRegex(ProtocolError, "DISTINCT_IDENTITY"):
                module.transient_component(self.store, LEGACY_WORKER, "0" * 64)


if __name__ == "__main__":
    unittest.main()
