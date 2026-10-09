"""Bounded worker-side orchestration, with injectable HTTP and no credential discovery."""
import concurrent.futures
import hashlib
import time
from urllib.parse import urlsplit
import urllib.request

from tools.pixinsight.local_pilot.broker import require, encode, decode
from tools.scientific_transients.queue import BINDING_FIELDS


def pair_inputs(session_ref):
    require(type(session_ref) is str and len(session_ref) == 32
            and all(c in "0123456789abcdef" for c in session_ref), "LAB_SESSION")
    def opaque(label):return hashlib.sha256((session_ref + ":" + label).encode()).hexdigest()[:32]
    bindings = [{field: opaque(str(index) + ":" + field) for field in sorted(BINDING_FIELDS)}
                for index in (1, 2)]
    jobs = [{"requestId": opaque(str(index) + ":request"), "bindingRef": body["bindingRef"]}
            for index, body in enumerate(bindings, 1)]
    return bindings, jobs


class WorkerController:
    def __init__(self, session_ref, source_revision, deadline, transport, storage_mode="GCS_ADC"):
        pair_inputs(session_ref)
        require(type(source_revision) is str and len(source_revision) == 40
                and all(c in "0123456789abcdef" for c in source_revision), "LAB_SOURCE")
        require(storage_mode in {"GCS_ADC", "SYNTHETIC"}, "LAB_MODE")
        require(type(deadline) in (int, float) and time.time() < deadline <= time.time() + 1800,
                "LAB_CONTROLLER_BOUNDED_DEADLINE")
        require(storage_mode == "SYNTHETIC" or source_revision != "0" * 40, "LAB_REAL_SOURCE_PIN")
        self.session, self.revision, self.deadline = session_ref, source_revision, deadline
        self.transport, self.mode = transport, storage_mode
        self.started = False

    def request(self, path, body=None, final=False):
        require(time.time() < self.deadline + (600 if final else 0), "LAB_CONTROLLER_DEADLINE")
        status, reply = self.transport(path, body)
        require(status == 200, "LAB_UNCERTAIN_STOP_NO_REPLAY")
        return reply

    def prepare_owner_pair(self):
        require(not self.started, "LAB_CONTROLLER_ALREADY_USED")
        self.started = True
        health = self.request("/health")
        require(health.get("sessionRef") == self.session and health.get("sourceRevision") == self.revision
                and health.get("storageMode") == self.mode, "LAB_ENDPOINT_IDENTITY")
        self.request("/lab/arm", {"sessionRef": self.session, "phase": "REGISTER"})
        bindings, jobs = pair_inputs(self.session)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(self.request, "/e/" + name + "/v1/transient-analysis/worker/register", body)
                       for name, body in zip(("A", "B"), bindings)]
            # Always wait for both; any exception stops without replay or CREATE.
            replies = [future.result(timeout=30) for future in futures]
        self.request("/lab/finish", {"sessionRef": self.session})
        self.request("/lab/arm", {"sessionRef": self.session, "phase": "CREATE"})
        audit = self.request("/lab/audit", final=True)
        require(audit.get("sessionRef") == self.session and audit.get("sourceRevision") == self.revision
                and audit.get("finishedPhases") == ["REGISTER"] and audit.get("phase") == "CREATE"
                and len(audit.get("bindings", [])) == 2 and audit.get("jobs") == [], "LAB_REGISTER_AUDIT")
        return {"protocol": "DSG_S4_WORKER_PREPARATION_V1", "sessionRef": self.session,
                "sourceRevision": self.revision, "jobs": jobs, "registerReceipts": replies,
                "audit": audit, "milestoneClosed": False}

    def stop(self):
        return self.request("/lab/stop", {"sessionRef": self.session}, final=True)


def https_transport(base_url, session_ref, worker_token):
    """Future caller supplies a fresh in-memory token; no environment/file lookup."""
    import re
    parsed = urlsplit(base_url)
    expected = "dsg-s4-lab-" + session_ref[:12] + "-183451329061.europe-west1.run.app"
    require(parsed.scheme == "https" and parsed.hostname == expected and parsed.path in ("", "/")
            and not parsed.port and not parsed.username and not parsed.password
            and not parsed.query and not parsed.fragment, "LAB_EXACT_NEW_ENDPOINT")
    require(re.fullmatch(r"[a-f0-9]{64}", worker_token or "") is not None, "LAB_FRESH_WORKER_TOKEN")
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *_):return None
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    def send(path, body):
        require(path in {"/health", "/lab/arm", "/lab/finish", "/lab/audit", "/lab/stop",
                "/e/A/v1/transient-analysis/worker/register", "/e/B/v1/transient-analysis/worker/register"},
                "LAB_WORKER_ROUTE")
        headers = {} if path == "/health" else {"Authorization": "Bearer " + worker_token}
        if body is not None:headers["Content-Type"] = "application/json"
        request = urllib.request.Request(base_url.rstrip("/") + path,
            data=None if body is None else encode(body), headers=headers)
        with opener.open(request, timeout=25) as response:
            raw = response.read(65537)
            require(len(raw) <= 65536, "LAB_REPLY_LIMIT")
            return response.status, decode(raw)
    return send
