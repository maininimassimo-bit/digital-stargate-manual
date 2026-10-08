"""Dedicated private control queue. No image, path, query, or native execution."""
import copy
import datetime as dt
import secrets

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode, opaque, require
from tools.scientific_registry.ingestion_storage import Conflict

STATE_KEY = "control/transient-analysis-state-v1.json"
PROTOCOL = "DSG_TRANSIENT_QUEUE_V1"
TERMINAL = {"COMPLETED", "FAILED", "CANCELLED", "RECOVERY_REQUIRED"}
LEASE_SECONDS = 900  # Operational lease only; no scientific threshold.
BINDING_FIELDS = {"bindingRef", "inputRef", "referenceRef", "algorithmRef", "contractRef"}
LIMIT = 1024 * 1024


def digest(value):
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def fields(value, expected):
    require(type(value) is dict and set(value) == expected, "TRANSIENT_FIELDS")


class TransientQueue:
    def __init__(self, store, worker_id, clock=None):
        require(opaque(worker_id), "TRANSIENT_WORKER_ID")
        self.store, self.worker_id = store, worker_id
        self.clock = clock or (lambda: dt.datetime.now(dt.timezone.utc))

    def _read(self):
        raw, generation = self.store.get(STATE_KEY)
        if raw is None:
            return {"protocol": PROTOCOL, "workerId": self.worker_id, "rootId": None,
                    "bindings": [], "jobs": []}, generation
        require(len(raw) <= LIMIT, "TRANSIENT_STATE_LIMIT")
        state = decode(raw)
        require(state["protocol"] == PROTOCOL and state["workerId"] == self.worker_id,
                "TRANSIENT_STATE_IDENTITY")
        return state, generation

    def _mutate(self, operation):
        now = self.clock()
        require(now.tzinfo is not None and now.utcoffset() == dt.timedelta(0), "TRANSIENT_CLOCK")
        for _ in range(8):
            state, generation = self._read()
            original = encode(state)
            for job in state["jobs"]:
                if job["state"] in {"RESERVED", "RUNNING"}:
                    if now < dt.datetime.fromisoformat(job["updatedAt"]) or now >= dt.datetime.fromisoformat(job["leaseExpiresAt"]):
                        job.update(state="RECOVERY_REQUIRED", updatedAt=now.isoformat())
            # Expiry is committed even when the incoming operation is rejected.
            expired = encode(state)
            result, failure = None, None
            try:
                result = operation(state, now)
            except ProtocolError as error:
                failure = error
                state = decode(expired)
            raw = encode(state)
            require(len(raw) <= LIMIT, "TRANSIENT_STATE_LIMIT")
            try:
                if original != raw:
                    self.store.put(STATE_KEY, raw, generation)
                if failure is not None:
                    raise failure
                return result
            except Conflict:
                continue
        raise Conflict("TRANSIENT_STORAGE_CONFLICT")

    @staticmethod
    def _job(state, job_id):
        require(isinstance(job_id, str) and job_id.startswith("TRN_") and opaque(job_id[4:]), "TRANSIENT_JOB_ID")
        matches = [j for j in state["jobs"] if j["jobId"] == job_id]
        require(len(matches) == 1, "TRANSIENT_JOB_NOT_FOUND")
        return matches[0]

    @staticmethod
    def _view(job, worker=False):
        result = copy.deepcopy(job)
        result.pop("lastEvent", None)
        if not worker:
            result.pop("leaseToken", None)
        result["executionEvidence"] = "WORKER_REPORTED_NOT_ATTESTED"
        result["scientificValidation"] = "NOT_VALIDATED"
        result["detailsLocation"] = "OWNER_PC"
        result["publication"] = "NONE"
        return result

    def register(self, request):
        fields(request, BINDING_FIELDS)
        require(all(opaque(v) for v in request.values()), "TRANSIENT_BINDING_ID")
        def operation(state, _):
            existing = next((b for b in state["bindings"] if b["bindingRef"] == request["bindingRef"]), None)
            if existing:
                require(existing == request, "TRANSIENT_BINDING_CONFLICT")
                return copy.deepcopy(existing)
            require(len(state["bindings"]) < 32, "TRANSIENT_BINDING_CAPACITY")
            state["bindings"].append(copy.deepcopy(request))
            return copy.deepcopy(request)
        return self._mutate(operation)

    def options(self):
        return self._mutate(lambda state, _: {"bindings": copy.deepcopy(state["bindings"])})

    def create(self, request):
        fields(request, {"requestId", "bindingRef"})
        require(all(opaque(v) for v in request.values()), "TRANSIENT_REQUEST_ID")
        def operation(state, now):
            existing = next((j for j in state["jobs"] if j["request"]["requestId"] == request["requestId"]), None)
            if existing:
                require(existing["request"] == request, "TRANSIENT_IDEMPOTENCY_CONFLICT")
                return self._view(existing)
            binding = next((b for b in state["bindings"] if b["bindingRef"] == request["bindingRef"]), None)
            require(binding is not None, "TRANSIENT_BINDING_NOT_REGISTERED")
            require(len(state["jobs"]) < 32, "TRANSIENT_JOB_CAPACITY")
            job = {"jobId": "TRN_" + request["requestId"], "request": copy.deepcopy(request),
                   "binding": copy.deepcopy(binding), "state": "QUEUED", "cancelRequested": False,
                   "sequence": 0, "result": None, "reviews": [],
                   "createdAt": now.isoformat(), "updatedAt": now.isoformat()}
            state["jobs"].append(job)
            return self._view(job)
        return self._mutate(operation)

    def status(self, job_id=None):
        def operation(state, _):
            return self._view(self._job(state, job_id)) if job_id else {"jobs": [self._view(j) for j in state["jobs"]]}
        return self._mutate(operation)

    def claim(self, request):
        fields(request, {"workerId", "rootId"})
        require(request["workerId"] == self.worker_id and opaque(request["rootId"]), "TRANSIENT_WORKER_ID")
        token, attempt = secrets.token_hex(32), secrets.token_hex(16)
        def operation(state, now):
            require(state["rootId"] in {None, request["rootId"]}, "TRANSIENT_ROOT_MISMATCH")
            state["rootId"] = request["rootId"]
            active = [j for j in state["jobs"] if j["state"] in {"RESERVED", "RUNNING", "RECOVERY_REQUIRED"}]
            require(len(active) <= 1, "TRANSIENT_QUEUE_INVARIANT")
            if active:
                return {"job": self._view(active[0], worker=True)}
            job = next((j for j in state["jobs"] if j["state"] == "QUEUED"), None)
            if job:
                job.update(state="RESERVED", rootId=request["rootId"], attemptId=attempt, leaseToken=token,
                           leaseIssuedAt=now.isoformat(), leaseExpiresAt=(now + dt.timedelta(seconds=LEASE_SECONDS)).isoformat(),
                           updatedAt=now.isoformat())
            return {"job": self._view(job, worker=True) if job else None}
        return self._mutate(operation)

    def cancel(self, job_id):
        def operation(state, now):
            job = self._job(state, job_id)
            if job["state"] not in TERMINAL:
                job.update(cancelRequested=True, updatedAt=now.isoformat())
                if job["state"] == "QUEUED":
                    job["state"] = "CANCELLED"
            return self._view(job)
        return self._mutate(operation)

    def report(self, job_id, request):
        fields(request, {"attemptId", "leaseToken", "sequence", "stage", "result"})
        require(opaque(request["attemptId"]) and digest(request["leaseToken"]), "TRANSIENT_LEASE")
        require(type(request["sequence"]) is int and 1 <= request["sequence"] <= 128, "TRANSIENT_SEQUENCE")
        require(type(request["stage"]) is str and request["stage"] in {"RUNNING", "COMPLETED", "FAILED", "CANCELLED", "RECOVERY_REQUIRED"}, "TRANSIENT_STAGE")
        if request["stage"] != "COMPLETED":
            require(request["result"] is None, "TRANSIENT_NO_RESULT")
        else:
            fields(request["result"], {"reportSha256", "bindingRef", "qualityCounts"})
            require(digest(request["result"]["reportSha256"]) and opaque(request["result"]["bindingRef"]), "TRANSIENT_RESULT_ID")
            counts = request["result"]["qualityCounts"]
            fields(counts, {"measured", "excluded", "incomplete"})
            require(all(type(v) is int and 0 <= v <= 10000000 for v in counts.values()), "TRANSIENT_COUNTS")
        def operation(state, now):
            job = self._job(state, job_id)
            require(job.get("attemptId") == request["attemptId"] and secrets.compare_digest(job.get("leaseToken", ""), request["leaseToken"]), "TRANSIENT_STALE_WORKER")
            if request["sequence"] == job["sequence"]:
                require(job.get("lastEvent") == request, "TRANSIENT_REPORT_CONFLICT")
                require(job["state"] != "RECOVERY_REQUIRED" or request["stage"] == "RECOVERY_REQUIRED", "TRANSIENT_EXPIRED")
                return self._view(job, worker=True)
            require(job["state"] not in TERMINAL and request["sequence"] == job["sequence"] + 1, "TRANSIENT_REPORT_ORDER")
            if job["cancelRequested"]:
                require(request["stage"] in {"CANCELLED", "RECOVERY_REQUIRED"}, "TRANSIENT_CANCEL_PENDING")
            if request["stage"] == "COMPLETED":
                require(job["state"] == "RUNNING" and request["result"]["bindingRef"] == job["binding"]["bindingRef"], "TRANSIENT_RESULT_BINDING")
            job.update(state=request["stage"], sequence=request["sequence"], lastEvent=copy.deepcopy(request),
                       result=copy.deepcopy(request["result"]), updatedAt=now.isoformat())
            if job["state"] == "RUNNING":
                job["leaseExpiresAt"] = (now + dt.timedelta(seconds=LEASE_SECONDS)).isoformat()
            return self._view(job, worker=True)
        return self._mutate(operation)

    def review(self, job_id, request):
        fields(request, {"decisionId", "reportSha256", "decision"})
        require(opaque(request["decisionId"]) and digest(request["reportSha256"]), "TRANSIENT_REVIEW_ID")
        require(type(request["decision"]) is str and request["decision"] in {"KEEP_FOR_REVIEW", "REJECT_CANDIDATE", "FOLLOW_UP"}, "TRANSIENT_REVIEW_DECISION")
        def operation(state, now):
            job = self._job(state, job_id)
            require(job["state"] == "COMPLETED" and job["result"]["reportSha256"] == request["reportSha256"], "TRANSIENT_REVIEW_BINDING")
            for review in job["reviews"]:
                if review["request"]["decisionId"] == request["decisionId"]:
                    require(review["request"] == request, "TRANSIENT_REVIEW_CONFLICT")
                    return copy.deepcopy(review)
            require(len(job["reviews"]) < 32, "TRANSIENT_REVIEW_CAPACITY")
            review = {"request": copy.deepcopy(request), "recordedAt": now.isoformat(), "authority": "OWNER_DECLARED"}
            job["reviews"].append(review)
            return copy.deepcopy(review)
        return self._mutate(operation)
