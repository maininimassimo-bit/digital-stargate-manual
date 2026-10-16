"""Dedicated private control queue. No image, path, query, or native execution."""
import copy
import datetime as dt
import secrets
import hashlib

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode, opaque, require
from tools.scientific_registry.ingestion_storage import Conflict

STATE_KEY = "control/transient-analysis-state-v1.json"
PROTOCOL = "DSG_TRANSIENT_QUEUE_V1"
TERMINAL = {"COMPLETED", "FAILED", "CANCELLED", "RECOVERY_REQUIRED"}
LEASE_SECONDS = 900  # Operational lease only; no scientific threshold.
BINDING_FIELDS = {"bindingRef", "inputRef", "referenceRef", "algorithmRef", "contractRef"}
RECOVERY_FIELDS = {"decisionId", "attemptId", "rootId", "bindingRef", "evidenceSha256", "quiescenceConfirmed"}
LIMIT = 1024 * 1024
CAMPAIGN_PROFILE = "CANDIDATE_59X3_V1"
CAMPAIGN_LIMIT = 8 * 1024 * 1024
CAMPAIGN_CAPACITY = 512
CAMPAIGN_ORIGIN_FIELDS = {'protocol', 'namespaceSha256', 'planRef', 'planSha256', 'freezeEventSha256',
                         'contextSha256', 'intentSha256', 'witnessRef', 'witnessSha256', 'ordinal',
                         'inputSha256', 'algorithmSha256', 'contractSha256', 'bindingSha256', 'workerId', 'rootId'}


def campaign_origin(value, binding, worker_id):
    """Internal marker integrity/schema, not authorization from a JSON payload."""
    fields(value, CAMPAIGN_ORIGIN_FIELDS)
    require(value['protocol'] == 'DSG_CAMPAIGN_JOB_ORIGIN_V1'
            and all(opaque(value[k]) for k in ('planRef', 'witnessRef', 'workerId', 'rootId'))
            and value['workerId'] == worker_id and type(value['ordinal']) is int and 0 <= value['ordinal'] < 3
            and all(digest(value[k]) for k in CAMPAIGN_ORIGIN_FIELDS if k.endswith('Sha256'))
            and value['bindingSha256'] == hashlib.sha256(encode(binding)).hexdigest(),
            'TRANSIENT_CAMPAIGN_ORIGIN')


def digest(value):
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def fields(value, expected):
    require(type(value) is dict and set(value) == expected, "TRANSIENT_FIELDS")


class TransientQueue:
    def __init__(self, store, worker_id, clock=None, *, state_ref=None, capacity_profile=None):
        require(opaque(worker_id), "TRANSIENT_WORKER_ID")
        require(state_ref is None or opaque(state_ref), "TRANSIENT_STATE_REF")
        require(capacity_profile is None or
                type(capacity_profile) is str and capacity_profile == CAMPAIGN_PROFILE,
                "TRANSIENT_CAPACITY_PROFILE")
        require(capacity_profile is None or state_ref is not None,
                "TRANSIENT_CAPACITY_ISOLATED_STATE_REQUIRED")
        self.store, self.worker_id = store, worker_id
        # Trusted deployment choice only. Never inferred from an incoming job,
        # an existing oversized state or the candidate's scientific eligibility.
        self.capacity_profile = capacity_profile
        self.capacity = 32 if capacity_profile is None else CAMPAIGN_CAPACITY
        self.state_limit = LIMIT if capacity_profile is None else CAMPAIGN_LIMIT
        # An explicit deployment choice, never an automatic identity migration.
        self.state_key = (STATE_KEY if state_ref is None else
                          "control/transient-analysis/" + state_ref + "/state-v1.json")
        self.clock = clock or (lambda: dt.datetime.now(dt.timezone.utc))

    def _read(self):
        raw, generation = self.store.get(self.state_key)
        if raw is None:
            state = {"protocol": PROTOCOL, "workerId": self.worker_id, "rootId": None,
                     "bindings": [], "jobs": []}
            if self.capacity_profile is not None:
                state["capacityProfile"] = self.capacity_profile
            return state, generation
        require(len(raw) <= self.state_limit, "TRANSIENT_STATE_LIMIT")
        state = decode(raw)
        require(state["protocol"] == PROTOCOL and state["workerId"] == self.worker_id,
                "TRANSIENT_STATE_IDENTITY")
        require(state.get("capacityProfile") == self.capacity_profile
                and ("capacityProfile" in state) == (self.capacity_profile is not None),
                "TRANSIENT_CAPACITY_STATE_MISMATCH")
        require(type(state["bindings"]) is list and type(state["jobs"]) is list
                and len(state["bindings"]) <= self.capacity and len(state["jobs"]) <= self.capacity,
                "TRANSIENT_STATE_CAPACITY")
        for job in state['jobs']:
            if 'campaignOrigin' in job:
                campaign_origin(job['campaignOrigin'], job['binding'], self.worker_id)
            if 'campaignReservation' in job:
                require('campaignOrigin' in job, 'TRANSIENT_CAMPAIGN_RESERVATION_WITHOUT_ORIGIN')
                fields(job['campaignReservation'], {'admissionSha256', 'request'})
                require(digest(job['campaignReservation']['admissionSha256'])
                        and job['campaignReservation']['request'] == job.get('reservationIntent'),
                        'TRANSIENT_CAMPAIGN_RESERVATION')
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
            require(len(raw) <= self.state_limit, "TRANSIENT_STATE_LIMIT")
            try:
                if original != raw:
                    self.store.put(self.state_key, raw, generation)
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
        result.pop("reservationIntent", None)
        result.pop('campaignOrigin', None)
        result.pop('campaignReservation', None)
        if not worker:
            result.pop("leaseToken", None)
        else:
            result.pop("recoveryClosure", None)
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
            require(len(state["bindings"]) < self.capacity, "TRANSIENT_BINDING_CAPACITY")
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
                require('campaignOrigin' not in existing, 'TRANSIENT_CAMPAIGN_PROTECTED')
                require(existing["request"] == request, "TRANSIENT_IDEMPOTENCY_CONFLICT")
                return self._view(existing)
            binding = next((b for b in state["bindings"] if b["bindingRef"] == request["bindingRef"]), None)
            require(binding is not None, "TRANSIENT_BINDING_NOT_REGISTERED")
            require(len(state["jobs"]) < self.capacity, "TRANSIENT_JOB_CAPACITY")
            job = {"jobId": "TRN_" + request["requestId"], "request": copy.deepcopy(request),
                   "binding": copy.deepcopy(binding), "state": "QUEUED", "cancelRequested": False,
                   "sequence": 0, "result": None, "reviews": [],
                   "createdAt": now.isoformat(), "updatedAt": now.isoformat()}
            state["jobs"].append(job)
            return self._view(job)
        return self._mutate(operation)

    def _campaign_access(self, guard):
        # Configured in-process composition only. This is not an authentication
        # or signature API and cannot be satisfied by a caller-provided JSON.
        require(guard is not None and guard is getattr(self, '_campaign_guard', None),
                'TRANSIENT_CAMPAIGN_TRUSTED_COMPOSITION_REQUIRED')

    def _create_campaign(self, request, binding, origin, *, guard):
        self._campaign_access(guard)
        fields(request, {'requestId', 'bindingRef'}); fields(binding, BINDING_FIELDS)
        require(all(opaque(v) for v in request.values()) and all(opaque(v) for v in binding.values())
                and request['bindingRef'] == binding['bindingRef'], 'TRANSIENT_CAMPAIGN_PROJECTION')
        campaign_origin(origin, binding, self.worker_id)
        request, binding, origin = copy.deepcopy((request, binding, origin))
        def operation(state, now):
            existing = next((j for j in state['jobs'] if j['request']['requestId'] == request['requestId']), None)
            if existing:
                require(existing.get('campaignOrigin') == origin and existing['request'] == request
                        and existing['binding'] == binding, 'TRANSIENT_CAMPAIGN_PROJECTION_CONFLICT')
                return self._view(existing)  # Always lease-free, including active jobs.
            registered = next((b for b in state['bindings'] if b['bindingRef'] == binding['bindingRef']), None)
            require(registered == binding, 'TRANSIENT_CAMPAIGN_REGISTERED_BINDING')
            require(len(state['jobs']) < self.capacity, 'TRANSIENT_JOB_CAPACITY')
            job = {'jobId': 'TRN_' + request['requestId'], 'request': request, 'binding': binding,
                   'state': 'QUEUED', 'cancelRequested': False, 'sequence': 0, 'result': None,
                   'reviews': [], 'createdAt': now.isoformat(), 'updatedAt': now.isoformat(),
                   'campaignOrigin': origin}
            state['jobs'].append(job)
            return self._view(job)
        return self._mutate(operation)

    def _campaign_snapshot(self, job_id, *, guard):
        self._campaign_access(guard)
        state, _ = self._read(); job = self._job(state, job_id)
        require('campaignOrigin' in job, 'TRANSIENT_CAMPAIGN_PROTECTED_JOB_REQUIRED')
        return {key: copy.deepcopy(job[key]) for key in ('jobId', 'request', 'binding', 'campaignOrigin')}

    def _campaign_technical_snapshot(self, job_id, *, guard):
        """Private read-only metadata: never runs expiry or commits queue state."""
        self._campaign_access(guard)
        state, _ = self._read(); job = self._job(state, job_id)
        require('campaignOrigin' in job, 'TRANSIENT_CAMPAIGN_PROTECTED_JOB_REQUIRED')
        return {key: copy.deepcopy(job[key]) for key in
                ('jobId','request','binding','campaignOrigin','state','cancelRequested')} | {
                'reservationConsumed': 'attemptId' in job or 'campaignReservation' in job}

    def _campaign_fenced_snapshot(self, job_id, *, guard):
        self._campaign_access(guard)
        state, _ = self._read(); job = self._job(state, job_id)
        # Exact shape excludes every attempt, root, lease, reservation and
        # recovery field, including unexpected fields with a null value.
        fields(job, {'jobId', 'request', 'binding', 'state', 'cancelRequested', 'sequence',
                     'result', 'reviews', 'createdAt', 'updatedAt', 'campaignOrigin'})
        require(job['state'] == 'CANCELLED' and job['cancelRequested'] is True
                and type(job['sequence']) is int and job['sequence'] == 0
                and job['result'] is None and job['reviews'] == [], 'TRANSIENT_CAMPAIGN_NOT_FENCED_UNRESERVED')
        return copy.deepcopy(job)

    def _reserve_campaign_once(self, request, origin, admission_sha, *, guard):
        self._campaign_access(guard)
        fields(request, {'workerId', 'rootId', 'jobId', 'bindingRef', 'reservationRef'})
        require(request['workerId'] == self.worker_id
                and all(opaque(request[k]) for k in ('rootId', 'bindingRef', 'reservationRef'))
                and digest(admission_sha), 'TRANSIENT_CAMPAIGN_RESERVATION_ID')
        request, origin = copy.deepcopy((request, origin))
        token, attempt = secrets.token_hex(32), secrets.token_hex(16)
        def operation(state, now):
            job = self._job(state, request['jobId'])
            require(job.get('campaignOrigin') == origin and origin['rootId'] == request['rootId']
                    and job['binding']['bindingRef'] == request['bindingRef'],
                    'TRANSIENT_CAMPAIGN_RESERVATION_BINDING')
            existing = job.get('campaignReservation')
            if existing:
                require(existing == {'admissionSha256': admission_sha, 'request': request},
                        'TRANSIENT_CAMPAIGN_RESERVATION_CONFLICT')
                return {'disposition': 'RECONCILIATION_REQUIRED', 'job': None}
            require(not any(j.get('campaignReservation', {}).get('admissionSha256') == admission_sha
                            or j.get('reservationIntent', {}).get('reservationRef') == request['reservationRef']
                            for j in state['jobs']), 'TRANSIENT_CAMPAIGN_ADMISSION_OR_RESERVATION_REUSED')
            require(state['rootId'] in {None, request['rootId']}, 'TRANSIENT_ROOT_MISMATCH')
            require(job['state'] == 'QUEUED' and not job['cancelRequested'], 'TRANSIENT_RESERVATION_NOT_FRESH')
            require(not any(self._blocks_reservation(j) for j in state['jobs']), 'TRANSIENT_ATTEMPT_ACTIVE')
            state['rootId'] = request['rootId']
            job.update(state='RESERVED', rootId=request['rootId'], attemptId=attempt, leaseToken=token,
                       leaseIssuedAt=now.isoformat(), leaseExpiresAt=(now + dt.timedelta(seconds=LEASE_SECONDS)).isoformat(),
                       updatedAt=now.isoformat(), reservationIntent=request,
                       campaignReservation={'admissionSha256': admission_sha, 'request': request})
            return {'disposition': 'CREATED', 'job': self._view(job, worker=True)}
        return self._mutate(operation)

    def status(self, job_id=None):
        def operation(state, _):
            return self._view(self._job(state, job_id)) if job_id else {"jobs": [self._view(j) for j in state["jobs"]]}
        return self._mutate(operation)

    def worker_receipt(self, job_id):
        """Authenticated worker route only; no lease or Owner reviews returned."""
        def operation(state, _):
            job = self._job(state, job_id)
            require("attemptId" in job, "TRANSIENT_ATTEMPT_NOT_RESERVED")
            receipt = copy.deepcopy(job.get("lastEvent"))
            if receipt is not None:
                receipt.pop("leaseToken")
            return {key: copy.deepcopy(job[key]) for key in
                    ["jobId", "attemptId", "rootId", "binding", "state", "cancelRequested", "sequence", "result"]} | {"lastReceipt": receipt}
        return self._mutate(operation)

    @staticmethod
    def _blocks_reservation(job):
        if job["state"] in {"RESERVED", "RUNNING"}:
            return True
        if job["state"] != "RECOVERY_REQUIRED":
            return False
        if "recoveryClosure" not in job:
            return True
        closure = job["recoveryClosure"]
        fields(closure, {"request", "recordedAt", "authority"})
        request = closure["request"]; fields(request, RECOVERY_FIELDS)
        require(closure["authority"] == "OWNER_DECLARED"
                and all(opaque(request[k]) for k in ["decisionId", "attemptId", "rootId", "bindingRef"])
                and digest(request["evidenceSha256"]) and request["quiescenceConfirmed"] is True
                and request["attemptId"] == job.get("attemptId") and request["rootId"] == job.get("rootId")
                and request["bindingRef"] == job["binding"]["bindingRef"], "TRANSIENT_RECOVERY_CORRUPT")
        try:
            recorded = dt.datetime.fromisoformat(closure["recordedAt"])
            require(recorded.tzinfo is not None and recorded.utcoffset() == dt.timedelta(0)
                    and recorded >= dt.datetime.fromisoformat(job["updatedAt"]), "TRANSIENT_RECOVERY_CLOCK")
        except (ValueError, TypeError):
            raise ProtocolError("TRANSIENT_RECOVERY_CLOCK") from None
        return False

    def claim(self, request):
        fields(request, {"workerId", "rootId"})
        require(request["workerId"] == self.worker_id and opaque(request["rootId"]), "TRANSIENT_WORKER_ID")
        token, attempt = secrets.token_hex(32), secrets.token_hex(16)
        def operation(state, now):
            require(state["rootId"] in {None, request["rootId"]}, "TRANSIENT_ROOT_MISMATCH")
            state["rootId"] = request["rootId"]
            active = [j for j in state["jobs"] if self._blocks_reservation(j)]
            require(len(active) <= 1, "TRANSIENT_QUEUE_INVARIANT")
            if active:
                require('campaignOrigin' not in active[0], 'TRANSIENT_CAMPAIGN_PROTECTED')
                return {"job": self._view(active[0], worker=True)}
            job = next((j for j in state["jobs"] if j["state"] == "QUEUED"), None)
            if job:
                require('campaignOrigin' not in job, 'TRANSIENT_CAMPAIGN_PROTECTED')
                job.update(state="RESERVED", rootId=request["rootId"], attemptId=attempt, leaseToken=token,
                           leaseIssuedAt=now.isoformat(), leaseExpiresAt=(now + dt.timedelta(seconds=LEASE_SECONDS)).isoformat(),
                           updatedAt=now.isoformat())
            return {"job": self._view(job, worker=True) if job else None}
        return self._mutate(operation)

    def reserve_once(self, request):
        """Explicit selected job and durable local intent; an existing intent never returns a lease."""
        fields(request, {"workerId", "rootId", "jobId", "bindingRef", "reservationRef"})
        require(request["workerId"] == self.worker_id and all(opaque(request[k]) for k in
                ["rootId", "bindingRef", "reservationRef"]), "TRANSIENT_RESERVATION_ID")
        token, attempt = secrets.token_hex(32), secrets.token_hex(16)
        def operation(state, now):
            require(state["rootId"] in {None, request["rootId"]}, "TRANSIENT_ROOT_MISMATCH")
            target = self._job(state, request['jobId'])
            require('campaignOrigin' not in target, 'TRANSIENT_CAMPAIGN_PROTECTED')
            existing = [j for j in state["jobs"] if j.get("reservationIntent", {}).get("reservationRef")
                        == request["reservationRef"]]
            if existing:
                require(len(existing) == 1 and existing[0]["reservationIntent"] == request,
                        "TRANSIENT_RESERVATION_CONFLICT")
                return {"disposition": "RECONCILIATION_REQUIRED", "job": None}
            job = self._job(state, request["jobId"])
            require(job["binding"]["bindingRef"] == request["bindingRef"], "TRANSIENT_RESERVATION_BINDING")
            require(job["state"] == "QUEUED" and not job["cancelRequested"], "TRANSIENT_RESERVATION_NOT_FRESH")
            require(not any(self._blocks_reservation(j) for j in state["jobs"]),
                    "TRANSIENT_ATTEMPT_ACTIVE")
            state["rootId"] = request["rootId"]
            job.update(state="RESERVED", rootId=request["rootId"], attemptId=attempt, leaseToken=token,
                       leaseIssuedAt=now.isoformat(), leaseExpiresAt=(now + dt.timedelta(seconds=LEASE_SECONDS)).isoformat(),
                       updatedAt=now.isoformat(), reservationIntent=copy.deepcopy(request))
            return {"disposition": "CREATED", "job": self._view(job, worker=True)}
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
            require("recoveryClosure" not in job, "TRANSIENT_RECOVERY_CLOSED")
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

    def close_recovery(self, job_id, request):
        """Owner-declared quiescence, not process attestation or a successful terminal result."""
        fields(request, RECOVERY_FIELDS)
        require(all(opaque(request[k]) for k in ["decisionId", "attemptId", "rootId", "bindingRef"])
                and digest(request["evidenceSha256"]) and request["quiescenceConfirmed"] is True,
                "TRANSIENT_RECOVERY_DECLARATION")
        def operation(state, now):
            job = self._job(state, job_id)
            require(job["state"] == "RECOVERY_REQUIRED" and job.get("attemptId") == request["attemptId"]
                    and job.get("rootId") == request["rootId"]
                    and job["binding"]["bindingRef"] == request["bindingRef"], "TRANSIENT_RECOVERY_IDENTITY")
            require(now >= dt.datetime.fromisoformat(job["updatedAt"]), "TRANSIENT_RECOVERY_CLOCK")
            existing = job.get("recoveryClosure")
            if existing is not None:
                self._blocks_reservation(job)
                require(existing["request"] == request, "TRANSIENT_RECOVERY_CONFLICT")
                return self._view(job)
            require(not any(j.get("recoveryClosure", {}).get("request", {}).get("decisionId")
                            == request["decisionId"] for j in state["jobs"]), "TRANSIENT_RECOVERY_DECISION_REUSED")
            job["recoveryClosure"] = {"request":copy.deepcopy(request), "recordedAt":now.isoformat(),
                                       "authority":"OWNER_DECLARED"}
            return self._view(job)  # Retain state, timestamps, attempt, result, lease and prior receipt.
        return self._mutate(operation)
