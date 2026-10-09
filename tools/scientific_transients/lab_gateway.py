"""Isolated test-only two-executor gateway; never the P6 deployment entry point."""
import contextlib
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import re
import threading
import time
import urllib.parse

from tools.pixinsight.local_pilot.broker import Broker, decode, encode, require
from tools.pixinsight.local_pilot.transport_http import AuthError, handler_for
from tools.scientific_registry.ingestion_storage import BackedUpStore, Conflict
from tools.scientific_transients.isolated_concurrency import Rendezvous
from tools.scientific_transients.queue import STATE_KEY, TransientQueue

ROOT_PREFIX = "/v1/transient-analysis"
ROUTES = {("POST", ROOT_PREFIX + "/worker/register"),
          ("POST", ROOT_PREFIX + "/jobs"),
          ("GET", ROOT_PREFIX + "/jobs"),
          ("GET", ROOT_PREFIX + "/options")}


class RequestBudget:
    """Shared transport ceiling, with a reserve for final verification."""
    def __init__(self, maximum=200, reserve=40, deadline=None):
        require(type(maximum) is int and type(reserve) is int and 0 < reserve < maximum <= 200,
                "LAB_PROVIDER_BUDGET")
        self.maximum, self.reserve, self.deadline = maximum, reserve, deadline
        self.lock = threading.Lock()
        self.rows = []
        self.context = threading.local()

    @contextlib.contextmanager
    def stage(self, executor, phase):
        old = getattr(self.context, "stage", (None, "STARTUP"))
        self.context.stage = executor, phase
        try:
            yield
        finally:
            self.context.stage = old

    def before(self, kind, method):
        executor, phase = getattr(self.context, "stage", (None, "STARTUP"))
        with self.lock:
            limit = self.maximum if phase == "FINAL" else self.maximum - self.reserve
            if len(self.rows) >= limit:
                raise RuntimeError("LAB_PROVIDER_BUDGET_EXHAUSTED")
            if self.deadline is not None:
                expiry = self.deadline + 600 if phase == "FINAL" else self.deadline
                if time.time() >= expiry:
                    raise RuntimeError("LAB_EXPERIMENT_DEADLINE")
            index = len(self.rows)
            self.rows.append({"sequence": index, "kind": kind, "method": method,
                              "executor": executor, "phase": phase, "status": None})
            return index

    def after(self, index, status):
        with self.lock:
            self.rows[index]["status"] = int(status)

    def snapshot(self):
        with self.lock:
            return [dict(row) for row in self.rows]


class LabState:
    def __init__(self, stores, session_ref, worker_id, worker_digest, legacy_digest,
                 owner_callback, origin, deadline, provider_budget, storage_mode,
                 source_revision="0" * 40):
        require(set(stores) == {"A", "B"}, "LAB_TWO_EXECUTORS")
        require(re.fullmatch(r"[a-f0-9]{32}", session_ref or "") is not None, "LAB_SESSION")
        require(storage_mode in {"SYNTHETIC", "GCS_ADC"}, "LAB_STORAGE_MODE")
        parsed_origin = urllib.parse.urlsplit(origin)
        require(parsed_origin.hostname and parsed_origin.path in ("", "/") and not parsed_origin.query and not parsed_origin.fragment
                and not parsed_origin.username and not parsed_origin.password
                and (parsed_origin.scheme == "https" or storage_mode == "SYNTHETIC"
                     and parsed_origin.scheme == "http" and parsed_origin.hostname in {"127.0.0.1", "localhost"}),
                "LAB_ORIGIN")
        require(re.fullmatch(r"[a-f0-9]{40}", source_revision or "") is not None, "LAB_SOURCE_REVISION")
        require(type(deadline) in (int, float) and time.time() < deadline <= time.time() + 1800,
                "LAB_DEADLINE")
        self.session_ref, self.worker_id = session_ref, worker_id
        self.worker_digest, self.legacy_digest = worker_digest, legacy_digest
        self.owner_callback, self.origin = owner_callback, origin.rstrip("/")
        self.deadline, self.budget, self.storage_mode = deadline, provider_budget, storage_mode
        self.source_revision = source_revision
        self.stores, self.servers, self.threads = stores, {}, []
        self.rendezvous = Rendezvous(timeout=10)
        self.phase, self.finished = None, []
        self.lock = threading.Lock()
        self.audit_lock = threading.Lock()
        self.attempts, self.http_count = [], 0
        self.stopped = False
        self.submitted = {}

    def admitted(self, final=False):
        with self.lock:
            limit = 80 if final else 60
            require(self.http_count < limit, "LAB_HTTP_BUDGET")
            if not final:
                require(not self.stopped and time.time() < self.deadline, "LAB_STOPPED")
            else:
                require(time.time() < self.deadline + 600, "LAB_FINAL_DEADLINE")
            self.http_count += 1

    def arm(self, phase):
        with self.lock:
            expected = "REGISTER" if self.finished == [] else "CREATE" if self.finished == ["REGISTER"] else None
            require(phase == expected and self.phase is None and not self.stopped, "LAB_PHASE_ORDER")
            self.rendezvous.arm(phase)
            self.phase = phase

    def finish(self):
        with self.lock:
            require(self.phase is not None, "LAB_NO_PHASE")
            with self.audit_lock:
                writes = [row for row in self.attempts if row["phase"] == self.phase]
            require(len(writes) == 3 and sum(row.get("committed", False) for row in writes) == 2,
                    "LAB_PHASE_WRITES_NOT_CONFIRMED")
            self.rendezvous.finish()
            self.finished.append(self.phase)
            self.phase = None

    def authenticate_worker(self, headers):
        values = headers.get_all("Authorization", [])
        require(len(values) == 1 and not headers.get_all("Origin", []), "LAB_WORKER_AUTH")
        token = values[0].removeprefix("Bearer ")
        require(values[0].startswith("Bearer ") and re.fullmatch(r"[a-f0-9]{64}", token or "") is not None,
                "LAB_WORKER_AUTH")
        import secrets
        require(secrets.compare_digest(hashlib.sha256(token.encode()).hexdigest(), self.worker_digest),
                "LAB_WORKER_AUTH")

    def authenticate_owner(self, headers):
        values = headers.get_all("Authorization", [])
        origins = headers.get_all("Origin", [])
        require(len(values) == 1 and origins == [self.origin] and values[0].startswith("Bearer "),
                "LAB_OWNER_AUTH")
        token = values[0][7:]
        require(0 < len(token) <= 8192, "LAB_OWNER_AUTH")
        self.owner_callback(token)

    def audit(self):
        # Only synthetic queue state; no native/image/provider-submission paths exist.
        with self.budget.stage(None, "FINAL"):
            primary, backup = self.stores["A"]
            raw, generation = primary.get(STATE_KEY)
            state = None if raw is None else decode(raw)
            with self.audit_lock:
                attempts = [dict(row) for row in self.attempts]
            prefix = "recovery/" + hashlib.sha256(STATE_KEY.encode()).hexdigest() + "/"
            copies = []
            for digest in sorted({row["sha256"] for row in attempts}):
                value, _ = backup.get(prefix + digest)
                copies.append({"sha256": digest, "verified": value is not None and hashlib.sha256(value).hexdigest() == digest})
            require(all(row["verified"] for row in copies), "LAB_BACKUP_AUDIT_FAILED")
        network = self.budget.snapshot()
        return {"protocol": "DSG_S4_LAB_AUDIT_V1", "sessionRef": self.session_ref,
                "sourceRevision": self.source_revision,
                "storageMode": self.storage_mode, "scientificValidation": "NOT_VALIDATED",
                "milestoneClosed": False, "sourceOfEvidence": "TEST_HARNESS_REPORTED",
                "phase": self.phase, "finishedPhases": list(self.finished), "httpRequests": self.http_count,
                "reads": list(self.rendezvous.observed), "attempts": attempts, "copies": copies,
                "providerRequests": network,
                "observedUpload412": sum(row["kind"] == "GCS_UPLOAD" and row["status"] == 412 for row in network),
                "generation": generation, "sha256": None if raw is None else hashlib.sha256(raw).hexdigest(),
                "bindings": [] if state is None else state["bindings"],
                "jobs": [] if state is None else [{"jobId": job["jobId"], "request": job["request"],
                                                    "state": job["state"]} for job in state["jobs"]]}

    def __enter__(self):
        try:
            for executor in ("A", "B"):
                primary, backup = self.stores[executor]
                store = PhaseStore(BackedUpStore(primary, backup), self, executor)
                base = handler_for(Broker(store, "f" * 32), self.owner_callback, self.origin,
                                   self.legacy_digest, transient=TransientQueue(store, self.worker_id),
                                   transient_worker_digest=self.worker_digest)
                # Exact handler implementation retained; only route context is instrumented.
                def bound_handler(parent, bound_store):
                    class Bound(parent):
                        def dispatch(self):
                            phase = "REGISTER" if self.command == "POST" and self.path == ROOT_PREFIX + "/worker/register" else "CREATE" if self.command == "POST" and self.path == ROOT_PREFIX + "/jobs" else None
                            with bound_store.context(phase):
                                return super().dispatch()
                    return Bound
                server = HTTPServer(("127.0.0.1", 0), bound_handler(base, store))
                self.servers[executor] = server
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start(); self.threads.append(thread)
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *_):
        self.stopped = True
        for server in self.servers.values():
            server.shutdown(); server.server_close()
        for thread in self.threads:
            thread.join(timeout=12)
            require(not thread.is_alive(), "LAB_EXECUTOR_NOT_STOPPED")


class PhaseStore:
    def __init__(self, store, lab, executor):
        self.store, self.lab, self.executor = store, lab, executor
        self.local = threading.local()

    @contextlib.contextmanager
    def context(self, phase):
        self.local.phase = phase
        with self.lab.budget.stage(self.executor, phase or "READ"):
            try:yield
            finally:self.local.phase = None

    def get(self, key):
        result = self.store.get(key)
        if key == STATE_KEY and getattr(self.local, "phase", None) == self.lab.phase and self.lab.phase is not None:
            self.lab.rendezvous.read(self.executor, result[1])
        return result

    def put(self, key, raw, generation=0):
        row = {"executor": self.executor, "phase": getattr(self.local, "phase", None),
               "expectedGeneration": generation, "sha256": hashlib.sha256(raw).hexdigest()}
        try:
            value = self.store.put(key, raw, generation)
            row.update(committed=True, generation=value)
            return value
        except Conflict:
            row["committed"] = False
            raise
        finally:
            with self.lab.audit_lock:self.lab.attempts.append(row)

    def exists(self, key):return self.store.exists(key)


def gateway_for(lab):
    class Gateway(BaseHTTPRequestHandler):
        def log_message(self, *_):pass

        def send(self, status, value):
            raw = encode(value)
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if self.headers.get_all("Origin", []) == [lab.origin]:
                self.send_header("Access-Control-Allow-Origin", lab.origin)
                self.send_header("Vary", "Origin")
            self.end_headers(); self.wfile.write(raw)
            self.close_connection = True

        def body(self):
            values = self.headers.get_all("Content-Length", [])
            require(len(values) == 1 and values[0].isdigit() and not self.headers.get_all("Transfer-Encoding", []), "LAB_BODY_LENGTH")
            length = int(values[0]);require(0 < length <= 16384, "LAB_BODY_LIMIT")
            require(self.headers.get_all("Content-Type", []) == ["application/json"], "LAB_BODY_TYPE")
            self.connection.settimeout(10)
            raw = self.rfile.read(length);require(len(raw) == length, "LAB_BODY_TRUNCATED")
            decode(raw)
            return raw

        def do_OPTIONS(self):
            try:
                require(self.headers.get_all("Origin", []) == [lab.origin], "LAB_ORIGIN")
                lab.admitted()
            except ValueError:
                return self.send(403, {"error": "ACCESS_DENIED"})
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", lab.origin)
            self.send_header("Access-Control-Allow-Headers", "Authorization,Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
            self.send_header("Content-Length", "0")
            self.send_header("Vary", "Origin")
            self.end_headers();self.close_connection = True

        def dispatch(self):
            require(not urllib.parse.urlsplit(self.path).query and "%" not in self.path, "LAB_EXACT_PATH")
            final = self.path in ("/lab/audit", "/lab/stop")
            lab.admitted(final=final)
            if self.command == "GET" and self.path == "/health":
                return self.send(200, {"protocol": "DSG_S4_LAB_V1", "sessionRef": lab.session_ref,
                                      "sourceRevision": lab.source_revision,
                                      "storageMode": lab.storage_mode, "scientificValidation": "NOT_VALIDATED"})
            if self.path in ("/lab/arm", "/lab/finish", "/lab/audit", "/lab/stop"):
                if self.headers.get_all("Origin", []):
                    with lab.budget.stage(None, "FINAL" if final else "OWNER_CONTROL"):
                        lab.authenticate_owner(self.headers)
                else:lab.authenticate_worker(self.headers)
                if self.command == "GET" and self.path == "/lab/audit":return self.send(200, lab.audit())
                require(self.command == "POST", "LAB_METHOD")
                body = decode(self.body())
                if self.path == "/lab/arm":
                    require(type(body) is dict and set(body) == {"sessionRef", "phase"} and body["sessionRef"] == lab.session_ref, "LAB_ARM_FIELDS")
                    lab.arm(body["phase"])
                else:
                    require(body == {"sessionRef": lab.session_ref}, "LAB_SESSION_FIELDS")
                    if self.path == "/lab/finish":lab.finish()
                    elif self.path == "/lab/stop":lab.stopped = True
                return self.send(200, {"sessionRef": lab.session_ref, "phase": lab.phase, "stopped": lab.stopped})
            match = re.fullmatch(r"/e/([AB])(/v1/transient-analysis(?:/.*)?)", self.path)
            require(match is not None, "LAB_ROUTE_BLOCKED")
            executor, path = match.groups()
            require((self.command, path) in ROUTES, "LAB_ROUTE_BLOCKED")
            require(len(self.headers.get_all("Authorization", [])) == 1 and len(self.headers.get_all("Origin", [])) <= 1, "LAB_AUTH_HEADERS")
            if self.command == "POST":
                phase = "REGISTER" if path.endswith("/worker/register") else "CREATE"
                require(lab.phase == phase or phase == "CREATE" and lab.finished == ["REGISTER", "CREATE"], "LAB_PHASE_REQUIRED")
            body = self.body() if self.command == "POST" else None
            if body is not None:
                if phase == "REGISTER":lab.authenticate_worker(self.headers)
                else:
                    with lab.budget.stage(executor, "OWNER_AUTH"):
                        lab.authenticate_owner(self.headers)
                with lab.lock:
                    previous = lab.submitted.get((phase, executor))
                    if lab.phase == phase:
                        require(previous is None, "LAB_SINGLE_SUBMISSION")
                        lab.submitted[phase, executor] = body
                    else:
                        require(previous == body, "LAB_CONFIRMED_REQUEST_ONLY")
            headers = {"Authorization": self.headers["Authorization"]}
            if "Origin" in self.headers:headers["Origin"] = self.headers["Origin"]
            if body is not None:headers["Content-Type"] = "application/json"
            connection = http.client.HTTPConnection("127.0.0.1", lab.servers[executor].server_port, timeout=25)
            try:
                connection.request(self.command, path, body=body, headers=headers)
                response = connection.getresponse();raw = response.read(65537)
                require(len(raw) <= 65536, "LAB_REPLY_LIMIT")
                return self.send(response.status, decode(raw))
            finally:connection.close()

        def handle_request(self):
            try:self.dispatch()
            except (AuthError, ValueError):self.send(403, {"error": "LAB_ACCESS_OR_CONTRACT_DENIED"})
            except Exception:self.send(503, {"error": "LAB_UNCERTAIN_STOP_NO_REPLAY"})
        do_GET = do_POST = handle_request
    return Gateway


class GatewayServer(ThreadingHTTPServer):
    daemon_threads = True
