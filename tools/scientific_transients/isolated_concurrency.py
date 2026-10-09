"""Offline S4 controller: two real HTTP executors, synthetic authentication/storage.

No cloud entry point, ADC, Google login, native worker, or deployment capability.
The rendezvous instruments reads; production queue and HTTP handler stay unchanged.
"""
import concurrent.futures
import datetime as dt
import hashlib
from http.server import HTTPServer
import threading
import urllib.error
import urllib.request

from tools.pixinsight.local_pilot.broker import Broker, decode, encode
from tools.pixinsight.local_pilot.transport_http import AuthError, handler_for
from tools.scientific_registry.ingestion_storage import BackedUpStore, Conflict, MemoryStore
from tools.scientific_transients.queue import BINDING_FIELDS, STATE_KEY, TransientQueue

WORKER = "a" * 32
TOKEN = "b" * 64  # Public fixture, never a credential for any deployed service.
LEGACY_TOKEN = "c" * 64
ORIGIN = "https://offline.invalid"
NOW = dt.datetime(2026, 10, 9, tzinfo=dt.timezone.utc)


class Rendezvous:
    """One read per executor per phase, after both have captured their generation."""
    def __init__(self, timeout=3):
        self.timeout = timeout
        self.lock = threading.Lock()
        self.phase = None
        self.barrier = None
        self.observed = []
        self.seen = set()

    def arm(self, phase):
        with self.lock:
            if self.phase is not None:
                raise RuntimeError("PHASE_ALREADY_ARMED")
            self.phase, self.seen = phase, set()
            self.barrier = threading.Barrier(2, timeout=self.timeout)

    def read(self, executor, generation):
        with self.lock:
            if self.phase is None or executor in self.seen:
                return
            self.seen.add(executor)
            self.observed.append({"phase": self.phase, "executor": executor,
                                  "generation": generation})
            barrier = self.barrier
        # Failure here precedes queue mutation/CAS. Never continue after timeout.
        barrier.wait()

    def finish(self):
        with self.lock:
            rows = [row for row in self.observed if row["phase"] == self.phase]
            if self.seen != {"A", "B"} or len(rows) != 2:
                raise RuntimeError("PAIR_NOT_OBSERVED")
            if rows[0]["generation"] != rows[1]["generation"]:
                raise RuntimeError("GENERATIONS_DIFFER")
            self.phase = None


class ObservedPrimary(MemoryStore):
    def __init__(self):
        super().__init__()
        self.attempts = []
        self.audit_lock = threading.Lock()

    def put(self, key, raw, generation=0):
        row = {"key": key, "expectedGeneration": generation,
               "sha256": hashlib.sha256(raw).hexdigest()}
        try:
            result = super().put(key, raw, generation)
            row.update(committed=True, generation=result)
            return result
        except Conflict:
            row.update(committed=False, conflict="SYNTHETIC_MEMORY_CAS")
            raise
        finally:
            with self.audit_lock:
                self.attempts.append(row)


class ExecutorStore:
    def __init__(self, store, rendezvous, executor):
        self.store, self.rendezvous, self.executor = store, rendezvous, executor

    def get(self, key):
        result = self.store.get(key)
        if key == STATE_KEY:
            self.rendezvous.read(self.executor, result[1])
        return result

    def put(self, key, raw, generation=0):
        return self.store.put(key, raw, generation)

    def exists(self, key):
        return self.store.exists(key)


class OfflineController:
    """Owned loopback-only servers with a fixed synthetic auth callback."""
    def __init__(self, barrier_timeout=3):
        self.primary, self.backup = ObservedPrimary(), MemoryStore()
        self.rendezvous = Rendezvous(barrier_timeout)
        self.servers, self.threads = {}, []
        self.requests = 0
        self.request_lock = threading.Lock()

    def __enter__(self):
        try:
            for name in ("A", "B"):
                store = ExecutorStore(BackedUpStore(self.primary, self.backup),
                                      self.rendezvous, name)
                def owner(token):
                    if token != "offline-owner-fixture":
                        raise AuthError()
                handler = handler_for(Broker(store, "d" * 32), owner, ORIGIN,
                                      hashlib.sha256(LEGACY_TOKEN.encode()).hexdigest(),
                                      transient=TransientQueue(store, WORKER, lambda: NOW),
                                      transient_worker_digest=hashlib.sha256(TOKEN.encode()).hexdigest())
                server = HTTPServer(("127.0.0.1", 0), handler)
                self.servers[name] = server
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                self.threads.append(thread)
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *_):
        for server in self.servers.values():
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join(timeout=5)
            if thread.is_alive():
                raise RuntimeError("OWNED_SERVER_NOT_STOPPED")

    def request(self, executor, path, body=None, owner=False, token=None, origin=None):
        with self.request_lock:
            if self.requests >= 40:
                raise RuntimeError("OFFLINE_REQUEST_BUDGET")
            self.requests += 1
        # No configurable URL/proxy or credential input from disk/environment.
        url = "http://127.0.0.1:" + str(self.servers[executor].server_port) + path
        headers = {"Authorization": "Bearer " + (token if token is not None else
                   "offline-owner-fixture" if owner else TOKEN)}
        if owner or origin is not None:
            headers["Origin"] = origin if origin is not None else ORIGIN
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=None if body is None else encode(body),
                                         headers=headers)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with opener.open(request, timeout=8) as response:
                return response.status, decode(response.read(65537))
        except urllib.error.HTTPError as error:
            return error.code, decode(error.read(65537))

    def pair(self, phase, path, bodies, owner=False):
        self.rendezvous.arm(phase)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(self.request, executor, path, body, owner)
                       for executor, body in zip(("A", "B"), bodies, strict=True)]
            replies = [future.result(timeout=10) for future in futures]
        if any(status != 200 for status, _ in replies):
            raise RuntimeError("UNCERTAIN_PAIR_STOP_NO_REPLAY")
        self.rendezvous.finish()
        return replies

    def run(self):
        bindings = [{field: format(index * 16 + offset, "032x")
                     for offset, field in enumerate(sorted(BINDING_FIELDS), 1)}
                    for index in (1, 2)]
        requests = [{"requestId": format(index, "032x"), "bindingRef": binding["bindingRef"]}
                    for index, binding in enumerate(bindings, 1)]
        self.pair("REGISTER", "/v1/transient-analysis/worker/register", bindings)
        created = self.pair("CREATE", "/v1/transient-analysis/jobs", requests, owner=True)
        before = self.primary.get(STATE_KEY)
        # Repeat only after both 200 receipts have been confirmed above.
        for executor, request, receipt in zip(("A", "B"), requests, created, strict=True):
            if self.request(executor, "/v1/transient-analysis/jobs", request, owner=True) != receipt:
                raise RuntimeError("IDEMPOTENT_RECEIPT_DIFFERENT")
        if self.primary.get(STATE_KEY) != before:
            raise RuntimeError("IDEMPOTENT_HEAD_CHANGED")
        raw, generation = before
        state = decode(raw)
        if {b["bindingRef"] for b in state["bindings"]} != {b["bindingRef"] for b in bindings}:
            raise RuntimeError("BINDING_LOST")
        if {j["request"]["requestId"] for j in state["jobs"]} != {r["requestId"] for r in requests}:
            raise RuntimeError("JOB_LOST")
        if any(j["state"] != "QUEUED" or j["result"] is not None for j in state["jobs"]):
            raise RuntimeError("UNEXPECTED_EXECUTION")
        attempts = list(self.primary.attempts)
        if len(attempts) != 6 or sum(row["committed"] for row in attempts) != 4:
            raise RuntimeError("CAS_COLLISIONS_NOT_PROVEN")
        backup_rows = []
        prefix = "recovery/" + hashlib.sha256(STATE_KEY.encode()).hexdigest() + "/"
        for row in attempts:
            copy, _ = self.backup.get(prefix + row["sha256"])
            if copy is None or hashlib.sha256(copy).hexdigest() != row["sha256"]:
                raise RuntimeError("BACKUP_NOT_VERIFIED")
            backup_rows.append({"sha256": row["sha256"], "primaryCommitted": row["committed"]})
        return {"protocol": "DSG_S4_OFFLINE_CONCURRENCY_V1", "result": "PASS",
                "authentication": "SYNTHETIC_CALLBACK", "storage": "MEMORY_ONLY",
                "realProvider412": False, "cloudActivated": False,
                "scientificValidation": "NOT_VALIDATED", "S4Closed": False,
                "httpExecutors": 2, "requests": self.requests,
                "observedReads": self.rendezvous.observed, "primaryAttempts": attempts,
                "backupVerification": backup_rows, "finalGeneration": generation,
                "finalSha256": hashlib.sha256(raw).hexdigest()}


def main():
    # Deliberately no live flag: this entry point cannot activate a cloud session.
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    with OfflineController() as controller:
        receipt = controller.run()
    print(encode(receipt).decode())


if __name__ == "__main__":
    main()
