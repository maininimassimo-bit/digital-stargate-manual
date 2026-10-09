"""Loopback integration tests, with no cloud credentials or external requests."""
import concurrent.futures
import hashlib
import http.client
import threading
import time
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode, decode
from tools.pixinsight.local_pilot.transport_http import AuthError
from tools.scientific_registry.ingestion_storage import MemoryStore
from tools.scientific_transients.queue import BINDING_FIELDS, STATE_KEY
from tools.scientific_transients.lab_gateway import LabState, RequestBudget, GatewayServer, gateway_for
from tools.scientific_transients.lab_cloud_transport import endpoint_kind, counted_adapter, make_cloud_stores
from tools.scientific_transients.lab_controller import WorkerController, pair_inputs, https_transport

TOKEN = "b" * 64
SESSION = "d" * 32
ORIGIN = "https://offline.invalid"


class Harness:
    def __enter__(self):
        self.primary, self.backup = MemoryStore(), MemoryStore()
        def owner(token):
            if token != "offline-owner":raise AuthError()
        self.lab = LabState({name: (self.primary, self.backup) for name in ("A", "B")},
            SESSION, "a" * 32, hashlib.sha256(TOKEN.encode()).hexdigest(), "c" * 64,
            owner, ORIGIN, time.time() + 120, RequestBudget(), "SYNTHETIC")
        self.lab.__enter__()
        self.server = GatewayServer(("127.0.0.1", 0), gateway_for(self.lab))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.server.shutdown();self.server.server_close();self.thread.join(5)
        self.lab.__exit__(*args)
        assert not self.thread.is_alive()

    def request(self, path, body=None, owner=False, token=None, origin=None):
        headers = {"Authorization": "Bearer " + (token or ("offline-owner" if owner else TOKEN))}
        if owner or origin:headers["Origin"] = origin or ORIGIN
        if body is not None:headers["Content-Type"] = "application/json"
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=15)
        try:
            connection.request("GET" if body is None else "POST", path,
                               None if body is None else encode(body), headers)
            reply = connection.getresponse()
            return reply.status, decode(reply.read())
        finally:connection.close()

    def control(self, action, phase=None):
        body = {"sessionRef": SESSION}
        if phase:body["phase"] = phase
        return self.request("/lab/" + action, body)

    def pair(self, phase, bodies):
        assert self.control("arm", phase)[0] == 200
        suffix = "/worker/register" if phase == "REGISTER" else "/jobs"
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            replies = list(pool.map(lambda item: self.request("/e/" + item[0] +
                "/v1/transient-analysis" + suffix, item[1], phase == "CREATE"), zip(("A", "B"), bodies)))
        assert [row[0] for row in replies] == [200, 200], replies
        assert self.control("finish")[0] == 200
        return replies

    def run(self):
        bindings = [{field: format(index * 16 + offset, "032x")
                     for offset, field in enumerate(sorted(BINDING_FIELDS), 1)} for index in (1, 2)]
        jobs = [{"requestId": format(index, "032x"), "bindingRef": body["bindingRef"]}
                for index, body in enumerate(bindings, 1)]
        self.pair("REGISTER", bindings)
        replies = self.pair("CREATE", jobs)
        return jobs, replies


class GatewayTests(unittest.TestCase):
    def test_worker_controller_prepares_owner_pair_and_cannot_replay(self):
        with Harness() as h:
            controller = WorkerController(SESSION, "0" * 40, h.lab.deadline, h.request, "SYNTHETIC")
            receipt = controller.prepare_owner_pair()
            self.assertEqual(receipt["jobs"], pair_inputs(SESSION)[1])
            self.assertEqual(receipt["audit"]["phase"], "CREATE")
            self.assertFalse(receipt["milestoneClosed"])
            before = h.primary.get(STATE_KEY)
            with self.assertRaisesRegex(ValueError, "ALREADY_USED"):controller.prepare_owner_pair()
            self.assertEqual(h.primary.get(STATE_KEY), before)
            self.assertEqual(controller.stop()["stopped"], True)

    def test_worker_controller_uncertain_pair_stops_before_owner_arm(self):
        calls = []
        def transport(path, body):
            calls.append(path)
            if path == "/health":return 200, {"sessionRef": SESSION, "sourceRevision": "0" * 40, "storageMode": "SYNTHETIC"}
            if path.startswith("/e/"):return 503, {}
            return 200, {}
        controller = WorkerController(SESSION, "0" * 40, time.time() + 100, transport, "SYNTHETIC")
        with self.assertRaisesRegex(ValueError, "STOP_NO_REPLAY"):controller.prepare_owner_pair()
        self.assertEqual(sum(path.startswith("/e/") for path in calls), 2)
        self.assertNotIn("/lab/finish", calls)

    def test_actual_outer_gateway_two_executors_cas_backup_and_idempotency(self):
        with Harness() as h:
            jobs, replies = h.run()
            before = h.primary.get(STATE_KEY)
            for name, job, reply in zip(("A", "B"), jobs, replies):
                self.assertEqual(h.request("/e/" + name + "/v1/transient-analysis/jobs", job, True), reply)
            self.assertEqual(h.primary.get(STATE_KEY), before)
            status, audit = h.request("/lab/audit")
            self.assertEqual(status, 200)
            self.assertEqual(audit["finishedPhases"], ["REGISTER", "CREATE"])
            self.assertEqual(len(audit["attempts"]), 6)
            self.assertEqual(sum(row["committed"] for row in audit["attempts"]), 4)
            self.assertEqual(len(audit["copies"]), 6)
            self.assertTrue(all(row["verified"] for row in audit["copies"]))
            self.assertEqual(len(audit["jobs"]), 2)
            self.assertEqual({job["state"] for job in audit["jobs"]}, {"QUEUED"})
            self.assertEqual(audit["observedUpload412"], 0)
            self.assertEqual(audit["storageMode"], "SYNTHETIC")
            self.assertFalse(audit["milestoneClosed"])
            for phase in ("REGISTER", "CREATE"):
                rows = [row for row in audit["reads"] if row["phase"] == phase]
                self.assertEqual(len(rows), 2)
                self.assertEqual(len({row["generation"] for row in rows}), 1)
        self.assertTrue(all(not thread.is_alive() for thread in h.lab.threads))

    def test_rejected_auth_and_forbidden_routes_write_nothing(self):
        with Harness() as h:
            self.assertEqual(h.control("arm", "REGISTER")[0], 200)
            binding = {field: "1" * 32 for field in BINDING_FIELDS}
            self.assertEqual(h.request("/e/A/v1/transient-analysis/worker/register", binding, token="bad")[0], 403)
            self.assertEqual(h.request("/e/A/v1/transient-analysis/worker/register", binding, origin=ORIGIN)[0], 403)
            self.assertEqual(h.request("/lab/stop", {"sessionRef": SESSION}, True, origin="https://bad.invalid")[0], 403)
            for path in ("/e/A/v1/jobs", "/e/A/v1/transient-analysis/worker/claim", "/lab/audit?token=x"):
                self.assertEqual(h.request(path)[0], 403)
            self.assertEqual(h.primary.items, {})
            self.assertEqual(h.lab.submitted, {})

    def test_read_does_not_satisfy_mutation_barrier_and_early_finish_denied(self):
        with Harness() as h:
            self.assertEqual(h.control("arm", "REGISTER")[0], 200)
            self.assertEqual(h.request("/e/A/v1/transient-analysis/options", owner=True)[0], 200)
            self.assertEqual(h.lab.rendezvous.observed, [])
            self.assertEqual(h.control("finish")[0], 403)
            self.assertEqual(h.primary.items, {})

    def test_no_new_jobs_or_registration_after_confirmed_pair(self):
        with Harness() as h:
            jobs, _ = h.run()
            before = h.primary.get(STATE_KEY)
            extra = dict(jobs[0], requestId="f" * 32)
            self.assertEqual(h.request("/e/A/v1/transient-analysis/jobs", extra, True)[0], 403)
            self.assertEqual(h.control("arm", "CREATE")[0], 403)
            self.assertEqual(h.primary.get(STATE_KEY), before)

    def test_expired_or_stopped_session_preserves_final_read_reserve(self):
        with Harness() as h:
            h.lab.deadline = time.time() - 1
            self.assertEqual(h.request("/health")[0], 403)
            self.assertEqual(h.request("/lab/audit")[0], 200)
            self.assertEqual(h.control("stop")[0], 200)
            self.assertTrue(h.lab.stopped)
            h.lab.deadline = time.time() - 601
            self.assertEqual(h.request("/lab/audit")[0], 403)

    def test_missing_backup_and_unpaired_request_cannot_finish(self):
        with Harness() as h:
            h.lab.rendezvous.timeout = 0.05
            h.control("arm", "REGISTER")
            binding = {field: "1" * 32 for field in BINDING_FIELDS}
            self.assertEqual(h.request("/e/A/v1/transient-analysis/worker/register", binding)[0], 503)
            self.assertEqual(h.primary.items, {})
            self.assertEqual(h.control("finish")[0], 403)
            self.assertEqual(h.request("/e/A/v1/transient-analysis/worker/register", binding)[0], 403)
        with Harness() as h:
            h.run()
            h.backup.items.clear()
            self.assertEqual(h.request("/lab/audit")[0], 403)


class TransportTests(unittest.TestCase):
    def test_worker_live_factory_rejects_old_p6_before_any_network(self):
        with self.assertRaisesRegex(ValueError, "EXACT_NEW_ENDPOINT"):
            https_transport("https://dsg-pixinsight-pilot-183451329061.europe-west1.run.app", SESSION, TOKEN)
    def test_count_retries_and_timeout_without_retaining_secrets(self):
        class Adapter:
            def send(self, request, **kwargs):
                self.timeout = kwargs["timeout"]
                return type("Reply", (), {"status_code": 412})()
        budget = RequestBudget(4, 1)
        adapter = counted_adapter(budget, Adapter)()
        request = type("Request", (), {"url": "https://storage.googleapis.com/upload/x?secret=PRIVATE", "method": "POST"})()
        for _ in range(3):adapter.send(request, timeout=(120, 30))
        self.assertEqual(adapter.timeout, (10, 10))
        with self.assertRaisesRegex(RuntimeError, "BUDGET_EXHAUSTED"):adapter.send(request)
        with budget.stage(None, "FINAL"):adapter.send(request)
        self.assertEqual(len(budget.snapshot()), 4)
        self.assertNotIn("PRIVATE", str(budget.snapshot()))
        self.assertEqual([row["status"] for row in budget.snapshot()], [412] * 4)

    def test_unknown_hosts_and_credential_overrides_blocked_before_sdk_lookup(self):
        for url in ("https://evil.invalid/", "https://storage.googleapis.com:444/", "https://www.googleapis.com/other"):
            with self.assertRaises(ValueError):endpoint_kind(url)
        with patch.dict("os.environ", {"GOOGLE_APPLICATION_CREDENTIALS": "do-not-read.json"}):
            with self.assertRaisesRegex(ValueError, "OVERRIDE_BLOCKED"):make_cloud_stores({}, RequestBudget())
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "METADATA_MUST_BE_DISABLED"):make_cloud_stores({}, RequestBudget())

    def test_sdk_delete_is_blocked_before_transport_and_budget_charge(self):
        class Adapter:
            def send(self, *_args, **_kwargs):raise AssertionError("TRANSPORT_MUST_NOT_RUN")
        budget = RequestBudget()
        adapter = counted_adapter(budget, Adapter)()
        request = type("Request", (), {"url": "https://storage.googleapis.com/storage/v1/x", "method": "DELETE"})()
        with self.assertRaisesRegex(ValueError, "METHOD_BLOCKED"):adapter.send(request)
        self.assertEqual(budget.snapshot(), [])

    def test_transport_deadline_final_reserve_is_finite(self):
        budget = RequestBudget(deadline=time.time() - 1)
        with self.assertRaisesRegex(RuntimeError, "DEADLINE"):budget.before("GCS_READ", "GET")
        with budget.stage(None, "FINAL"):budget.before("GCS_READ", "GET")
        budget.deadline = time.time() - 601
        with budget.stage(None, "FINAL"):
            with self.assertRaisesRegex(RuntimeError, "DEADLINE"):budget.before("GCS_READ", "GET")


if __name__ == "__main__":unittest.main()
