"""Bounded private P4 queue. No script, image, path or provider dispatch."""
from __future__ import annotations

import copy
import datetime as dt
import json
import re
import secrets

from tools.scientific_registry.ingestion_storage import Conflict
from tools.pixinsight.local_pilot.worker import RECIPE, NONLINEAR_RECIPE, NONLINEAR_RECIPES, actions, expected_outputs

STATE_KEY = "control/piai-state.json"
LIMIT = 1024 * 1024
TERMINAL = {"COMPLETED", "FAILED", "CANCELLED", "RECOVERY_REQUIRED"}
STAGES = {"RESERVED", "PREPARING", "PREPARED", "AWAITING_NATIVE", "RUNNING"} | TERMINAL


class ProtocolError(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise ProtocolError(code)


def opaque(value):
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{32}", value) is not None


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def decode(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "DUPLICATE_FIELD")
            value[key] = item
        return value
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ProtocolError("JSON_INVALID")))
    except (ValueError, UnicodeError, RecursionError):
        raise ProtocolError("JSON_INVALID") from None


class Broker:
    def __init__(self, store, worker_id, clock=None):
        require(opaque(worker_id), "WORKER_ID_INVALID")
        self.store, self.worker_id = store, worker_id
        self.clock = clock or (lambda: dt.datetime.now(dt.timezone.utc))

    def _state(self):
        raw, generation = self.store.get(STATE_KEY)
        if raw is None:
            return {"schemaVersion": "1.0", "workerId": self.worker_id, "rootId": None, "lastSeen": None, "jobs": []}, generation
        require(len(raw) <= LIMIT, "STATE_LIMIT")
        state = decode(raw)
        require(state["schemaVersion"] == "1.0" and state["workerId"] == self.worker_id, "STATE_IDENTITY")
        return state, generation

    def _mutate(self, operation):
        now = self.clock().isoformat()
        for _ in range(8):
            state, generation = self._state()
            result = operation(state, now)
            raw = encode(state)
            require(len(raw) <= LIMIT, "STATE_LIMIT")
            try:
                self.store.put(STATE_KEY, raw, generation)
                return result
            except Conflict:
                continue
        raise Conflict("QUEUE_CONFLICT")

    @staticmethod
    def _job(state, job_id):
        require(isinstance(job_id, str) and re.fullmatch(r"PIAI_[a-f0-9]{32}", job_id), "JOB_ID_INVALID")
        matches = [item for item in state["jobs"] if item["jobId"] == job_id]
        require(len(matches) == 1, "JOB_NOT_FOUND")
        return matches[0]

    @staticmethod
    def _view(item, worker=False):
        value = copy.deepcopy(item)
        if not worker:
            value.pop("leaseToken", None)
            if value.get("report"):
                value["report"].pop("leaseToken", None)
        return value

    def create(self, request, scientific_context_sha=None):
        require(isinstance(request, dict) and set(request) == {"schemaVersion", "requestId", "inputRef", "recipe", "aiMode"}, "REQUEST_FIELDS")
        require(request["schemaVersion"] == "1.0" and opaque(request["requestId"]) and opaque(request["inputRef"]), "REQUEST_IDENTITY")
        require(request["recipe"] in {RECIPE} | NONLINEAR_RECIPES and request["aiMode"] in
                {'SESSION_ASSISTED', 'OPENAI_API_PLANNING'}, "RECIPE_OR_AI_MODE")
        require(request['aiMode'] != 'OPENAI_API_PLANNING' or scientific_context_sha is not None, 'AI_APPROVED_CONTEXT_REQUIRED')
        def operation(state, now):
            require(request['requestId'] not in state.get('withdrawnIntakes', []), 'INTAKE_WITHDRAWN')
            for item in state["jobs"]:
                if item["request"]["requestId"] == request["requestId"]:
                    require(item["request"] == request, "IDEMPOTENCY_CONFLICT")
                    require(item.get("scientificContextSha256") == scientific_context_sha, "IDEMPOTENCY_CONTEXT_CONFLICT")
                    return self._view(item)
            require(len(state["jobs"]) < 16, "QUEUE_CAPACITY")
            item = {"jobId": "PIAI_" + request["requestId"], "request": copy.deepcopy(request),
                    "state": "QUEUED", "cancelRequested": False, "sequence": 0,
                    "report": None, "createdAt": now, "updatedAt": now}
            if scientific_context_sha is not None:
                require(isinstance(scientific_context_sha, str) and re.fullmatch(r"[a-f0-9]{64}", scientific_context_sha), "CONTEXT_DIGEST")
                item["scientificContextSha256"] = scientific_context_sha
            state["jobs"].append(item)
            return self._view(item)
        return self._mutate(operation)

    def claim(self, worker_id, root_id):
        require(worker_id == self.worker_id, "WORKER_NOT_ALLOWED")
        require(opaque(root_id), "ROOT_ID_INVALID")
        token = secrets.token_hex(32)
        def operation(state, now):
            require(state["rootId"] in {None, root_id}, "ROOT_ID_MISMATCH_RECOVERY_REQUIRED")
            state["rootId"] = root_id
            state["lastSeen"] = now
            active = [x for x in state["jobs"] if x["state"] in (STAGES - TERMINAL) | {"RECOVERY_REQUIRED"}]
            require(len(active) <= 1, "QUEUE_INVARIANT")
            if active:
                return self._view(active[0], worker=True)
            pending = next((x for x in state["jobs"] if x["state"] == "QUEUED"), None)
            if pending:
                pending.update(state="RESERVED", leaseToken=token, rootId=root_id, updatedAt=now)
                return self._view(pending, worker=True)
            return None
        return self._mutate(operation)

    def status(self, job_id):
        state, _ = self._state()
        item = self._view(self._job(state, job_id))
        seen = state["lastSeen"]
        if seen is None:
            connection = "UNKNOWN"
        else:
            age = (self.clock() - dt.datetime.fromisoformat(seen)).total_seconds()
            connection = "CLOCK_UNCERTAIN" if age < 0 else "OFFLINE" if age > 120 else "RECENT_CONTACT"
        return {"job": item, "connection": connection, "lastSeen": seen,
                "executionEvidence": "WORKER_REPORTED_NOT_ATTESTED", "publication": "NONE"}

    def cancel(self, job_id):
        def operation(state, now):
            item = self._job(state, job_id)
            if item["state"] in TERMINAL:
                return self._view(item)
            item.update(cancelRequested=True, updatedAt=now)
            if item["state"] == "QUEUED":
                item["state"] = "CANCELLED"
            return self._view(item)
        return self._mutate(operation)

    def report(self, job_id, worker_id, request):
        require(worker_id == self.worker_id, "WORKER_NOT_ALLOWED")
        require(isinstance(request, dict) and set(request) == {"leaseToken", "sequence", "stage", "processCount", "outputCount", "verified"}, "REPORT_FIELDS")
        require(isinstance(request["leaseToken"], str) and re.fullmatch(r"[a-f0-9]{64}", request["leaseToken"]), "LEASE_INVALID")
        require(type(request["sequence"]) is int and 1 <= request["sequence"] <= 128, "SEQUENCE_INVALID")
        require(request["stage"] in STAGES - {"RESERVED"} and type(request["verified"]) is bool, "REPORT_INVALID")
        for name, maximum in (("processCount", 29), ("outputCount", 15)):
            require(type(request[name]) is int and 0 <= request[name] <= maximum, "COUNTS_INVALID")
        def operation(state, now):
            item = self._job(state, job_id)
            require(secrets.compare_digest(item.get("leaseToken", ""), request["leaseToken"]), "LEASE_MISMATCH")
            if request["sequence"] == item["sequence"]:
                require(item["report"] == request, "REPORT_CONFLICT")
                state["lastSeen"] = now
                return self._view(item, worker=True)
            require(item["state"] not in TERMINAL and request["sequence"] == item["sequence"] + 1, "REPORT_ORDER")
            rank = {"RESERVED": 0, "PREPARING": 1, "PREPARED": 2, "AWAITING_NATIVE": 3, "RUNNING": 4}
            stage = request["stage"]
            require(stage in TERMINAL or rank[stage] >= rank[item["state"]], "STAGE_REGRESSION")
            previous = item["report"]
            require(previous is None or (request["processCount"] >= previous["processCount"] and request["outputCount"] >= previous["outputCount"]), "COUNT_REGRESSION")
            recipe = item['request']['recipe']
            expected = (len(actions(recipe)),len(expected_outputs(recipe)))
            require(request["processCount"] <= expected[0] and request["outputCount"] <= expected[1], "RECIPE_COUNTS")
            require(request["verified"] == (stage == "COMPLETED"), "VERIFICATION_REQUIRED")
            if stage == "COMPLETED":
                require((request["processCount"], request["outputCount"]) == expected, "COMPLETION_INCOMPLETE")
            item.update(state=stage, sequence=request["sequence"], report=copy.deepcopy(request), updatedAt=now)
            state["lastSeen"] = now
            return self._view(item, worker=True)
        return self._mutate(operation)
