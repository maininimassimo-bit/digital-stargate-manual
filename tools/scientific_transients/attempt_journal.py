"""Local attempt snapshots/checkpoint receipts. Does not launch/attest native work."""
import hashlib
import datetime as dt
import os

from tools.pixinsight.local_pilot.broker import decode, encode, opaque, require
from tools.scientific_transients.local_registry import safe_path, fingerprint, relative, LIMIT, ROLES
from tools.scientific_transients.queue import BINDING_FIELDS, TERMINAL, digest, fields

PROTOCOL = "DSG_TRANSIENT_ATTEMPT_V1"
MAX_EVENTS = 128


def identity(value):
    fields(value, {"jobId", "attemptId", "rootId", "binding", "manifestSha256"})
    require(type(value["jobId"]) is str and value["jobId"].startswith("TRN_")
            and opaque(value["jobId"][4:]) and opaque(value["attemptId"])
            and opaque(value["rootId"]) and digest(value["manifestSha256"]), "JOURNAL_IDENTITY")
    fields(value["binding"], BINDING_FIELDS)
    require(all(opaque(v) for v in value["binding"].values()), "JOURNAL_BINDING")


def read_json(path):
    path = safe_path(path)
    with path.open("rb") as stream: raw = stream.read(LIMIT + 1)
    require(0 < len(raw) <= LIMIT, "JOURNAL_JSON_LIMIT")
    return decode(raw), hashlib.sha256(raw).hexdigest()


def write_new(path, value):
    raw = encode(value); require(len(raw) <= LIMIT, "JOURNAL_JSON_LIMIT")
    safe_path(path.parent)
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    return hashlib.sha256(raw).hexdigest()


def copy_verified(source, destination, expected):
    source = safe_path(source); require(source.is_file(), "JOURNAL_REGULAR_FILE")
    safe_path(destination.parent)
    value, size = hashlib.sha256(), 0
    with source.open("rb") as incoming, destination.open("xb") as outgoing:
        while chunk := incoming.read(1024 * 1024):
            outgoing.write(chunk); value.update(chunk); size += len(chunk)
        outgoing.flush(); os.fsync(outgoing.fileno())
    require({"sha256": value.hexdigest(), "bytes": size} == expected
            and fingerprint(destination) == expected, "JOURNAL_COPY_MISMATCH")


class AttemptJournal:
    @classmethod
    def prepare(cls, registry, journal_root, value):
        identity(value)
        root = safe_path(journal_root); require(root.is_dir(), "JOURNAL_ROOT")
        for other in [registry.artifacts, registry.registry]:
            require(root != other and root not in other.parents and other not in root.parents,
                    "JOURNAL_ROOT_OVERLAP")
        manifest = registry.verify(value["binding"]["bindingRef"], value["manifestSha256"])
        require(manifest["binding"] == value["binding"], "JOURNAL_BINDING")
        directory = root / value["attemptId"]
        directory.mkdir()  # Partial directories remain and never restart implicitly.
        (directory / "snapshot").mkdir(); (directory / "events").mkdir()
        copies = []
        for i, record in enumerate(manifest["files"]):
            name = "snapshot/" + str(i).zfill(3) + ".dat"
            expected = {k: record[k] for k in ["sha256", "bytes"]}
            copy_verified(registry.artifacts / relative(record["path"]), directory / name, expected)
            copies.append({"path": name, "role": record["role"], **expected})
        anchor = {"protocol": PROTOCOL, "identity": value, "snapshot": copies,
                  "nativeExecution": "NOT_ATTESTED", "scienceValidation": "NOT_VALIDATED"}
        write_new(directory / "attempt.json", anchor)
        journal = cls(directory, value)
        journal._append("PREPARED", {"snapshotCount": len(copies)})
        return journal

    def __init__(self, directory, expected_identity):
        identity(expected_identity)
        self.directory = safe_path(directory)
        require(self.directory.name == expected_identity["attemptId"], "JOURNAL_DIRECTORY_IDENTITY")
        anchor, self.anchor_sha = read_json(self.directory / "attempt.json")
        fields(anchor, {"protocol", "identity", "snapshot", "nativeExecution", "scienceValidation"})
        require(anchor["protocol"] == PROTOCOL and anchor["identity"] == expected_identity
                and anchor["nativeExecution"] == "NOT_ATTESTED"
                and anchor["scienceValidation"] == "NOT_VALIDATED", "JOURNAL_ANCHOR")
        require(type(anchor["snapshot"]) is list and 6 <= len(anchor["snapshot"]) <= 128,
                "JOURNAL_SNAPSHOT")
        self.anchor = anchor
        events = self._events()
        failure_terminal = bool(events and events[-1]["kind"] in {"FAILED", "CANCELLED", "RECOVERY_REQUIRED"})
        self._snapshot(verify_bytes=not failure_terminal)
        self.reopened_active = bool(events and events[-1]["kind"] in {"RUNNING", "OPERATION_STARTED", "CHECKPOINT"})

    def _snapshot(self, verify_bytes=True):
        paths = set()
        for row in self.anchor["snapshot"]:
            fields(row, {"path", "role", "sha256", "bytes"}); relative(row["path"])
            require(row["path"].startswith("snapshot/") and row["path"] not in paths,
                    "JOURNAL_SNAPSHOT")
            require(type(row["role"]) is str and row["role"] in ROLES and digest(row["sha256"])
                    and type(row["bytes"]) is int and row["bytes"] > 0, "JOURNAL_SNAPSHOT")
            paths.add(row["path"])
            if verify_bytes:
                require(fingerprint(self.directory / row["path"]) == {k: row[k] for k in ["sha256", "bytes"]},
                        "JOURNAL_SNAPSHOT_CHANGED")

    def _events(self):
        directory = safe_path(self.directory / "events")
        paths = sorted(directory.iterdir()); require(len(paths) <= MAX_EVENTS, "JOURNAL_CAPACITY")
        events, previous, state, processes = [], self.anchor_sha, None, set()
        for i, path in enumerate(paths, 1):
            require(path.name == str(i).zfill(3) + ".json", "JOURNAL_EVENT_ORDER")
            value, sha = read_json(path)
            fields(value, {"sequence", "previousSha256", "kind", "data", "recordedAt"})
            require(value["sequence"] == i and type(value["sequence"]) is int
                    and value["previousSha256"] == previous, "JOURNAL_EVENT_CHAIN")
            self._transition(state, value["kind"], value["data"])
            require(type(value["recordedAt"]) is str and len(value["recordedAt"]) <= 40, "JOURNAL_TIME")
            try: timestamp = dt.datetime.fromisoformat(value["recordedAt"])
            except ValueError: require(False, "JOURNAL_TIME")
            require(timestamp.utcoffset() == dt.timedelta(0), "JOURNAL_TIME")
            self._relation(events[-1] if events else None, value["kind"], value["data"])
            if value["kind"] == "PREPARED":
                require(value["data"]["snapshotCount"] == len(self.anchor["snapshot"]), "JOURNAL_SNAPSHOT")
            if value["kind"] == "OPERATION_STARTED":
                require(value["data"]["processRef"] not in processes, "JOURNAL_PROCESS_REUSED")
                processes.add(value["data"]["processRef"])
            state, previous = value["kind"], sha
            events.append(value)
        self.head_sha = previous
        return events

    @staticmethod
    def _transition(state, kind, data):
        require(type(kind) is str and state not in TERMINAL, "JOURNAL_TERMINAL")
        if kind == "PREPARED":
            require(state is None, "JOURNAL_STAGE"); fields(data, {"snapshotCount"})
            require(type(data["snapshotCount"]) is int and 6 <= data["snapshotCount"] <= 128, "JOURNAL_DATA")
        elif kind == "RUNNING":
            require(state == "PREPARED", "JOURNAL_STAGE"); fields(data, set())
        elif kind == "OPERATION_STARTED":
            require(state in {"RUNNING", "CHECKPOINT"}, "JOURNAL_STAGE")
            fields(data, {"processRef", "files"})
            require(opaque(data["processRef"]) and type(data["files"]) is list and len(data["files"]) == 2,
                    "JOURNAL_DATA")
            require({r.get("role") for r in data["files"] if type(r) is dict} == {"PARAMETERS", "RUNTIME"}, "JOURNAL_DATA")
            AttemptJournal._file_rows(data["files"], "operation-")
        elif kind == "CHECKPOINT":
            require(state == "OPERATION_STARTED", "JOURNAL_STAGE")
            fields(data, {"processRef", "files"})
            require(opaque(data["processRef"]) and type(data["files"]) is list and len(data["files"]) == 3, "JOURNAL_DATA")
            require({r.get("role") for r in data["files"] if type(r) is dict} == {"CHECKPOINT", "PARAMETERS", "HISTORY"}, "JOURNAL_DATA")
            AttemptJournal._file_rows(data["files"], "checkpoint-")
        elif kind == "COMPLETED":
            require(state == "CHECKPOINT", "JOURNAL_STAGE"); fields(data, {"reportSha256"})
            require(digest(data["reportSha256"]), "JOURNAL_DATA")
        else:
            require(kind in {"FAILED", "CANCELLED", "RECOVERY_REQUIRED"} and state is not None, "JOURNAL_STAGE")
            fields(data, set())

    @staticmethod
    def _file_rows(rows, prefix):
        paths = set()
        for row in rows:
            fields(row, {"role", "path", "sha256", "bytes"}); relative(row["path"])
            require(row["path"].startswith(prefix) and row["path"] not in paths and digest(row["sha256"])
                    and type(row["bytes"]) is int and row["bytes"] > 0, "JOURNAL_DATA")
            paths.add(row["path"])

    @staticmethod
    def _relation(previous, kind, data):
        if kind == "CHECKPOINT":
            require(previous is not None and previous["kind"] == "OPERATION_STARTED"
                    and previous["data"]["processRef"] == data["processRef"], "JOURNAL_PROCESS_BINDING")
            start = next(r for r in previous["data"]["files"] if r["role"] == "PARAMETERS")
            end = next(r for r in data["files"] if r["role"] == "PARAMETERS")
            require((start["sha256"], start["bytes"]) == (end["sha256"], end["bytes"]), "JOURNAL_PARAMETERS_CHANGED")

    def _append(self, kind, data):
        events = self._events(); require(len(events) < MAX_EVENTS, "JOURNAL_CAPACITY")
        self._transition(events[-1]["kind"] if events else None, kind, data)
        self._relation(events[-1] if events else None, kind, data)
        if kind == "OPERATION_STARTED":
            require(not any(e["kind"] == kind and e["data"]["processRef"] == data["processRef"] for e in events), "JOURNAL_PROCESS_REUSED")
        event = {"sequence": len(events) + 1, "previousSha256": self.head_sha, "kind": kind, "data": data,
                 "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat()}
        write_new(self.directory / "events" / (str(len(events) + 1).zfill(3) + ".json"), event)

    def running(self):
        require(not self.reopened_active, "JOURNAL_EXPLICIT_RECOVERY_REQUIRED")
        self._snapshot(); self._append("RUNNING", {})

    def checkpoint(self, registry, process_ref, sources):
        require(not self.reopened_active, "JOURNAL_EXPLICIT_RECOVERY_REQUIRED")
        fields(sources, {"CHECKPOINT", "PARAMETERS", "HISTORY"}); require(opaque(process_ref), "JOURNAL_DATA")
        events = self._events()
        require(events[-1]["kind"] == "OPERATION_STARTED" and events[-1]["data"]["processRef"] == process_ref, "JOURNAL_PROCESS_BINDING")
        name = "checkpoint-" + str(len(events) + 1).zfill(3)
        target = self.directory / name; target.mkdir()
        files = []
        for role, path in sources.items():
            source = registry.artifacts / relative(path); expected = fingerprint(source)
            require(expected["bytes"] > 0, "JOURNAL_DATA")
            relative_name = name + "/" + role.lower() + ".dat"
            copy_verified(source, self.directory / relative_name, expected)
            files.append({"role": role, "path": relative_name, **expected})
        self._append("CHECKPOINT", {"processRef": process_ref, "files": files})

    def begin_operation(self, registry, process_ref, sources):
        require(not self.reopened_active, "JOURNAL_EXPLICIT_RECOVERY_REQUIRED")
        fields(sources, {"PARAMETERS", "RUNTIME"}); require(opaque(process_ref), "JOURNAL_DATA")
        events = self._events(); require(events[-1]["kind"] in {"RUNNING", "CHECKPOINT"}, "JOURNAL_STAGE")
        require(not any(e["kind"] == "OPERATION_STARTED" and e["data"]["processRef"] == process_ref for e in events), "JOURNAL_PROCESS_REUSED")
        name = "operation-" + str(len(events) + 1).zfill(3); (self.directory / name).mkdir()
        files = []
        for role, path in sources.items():
            source = registry.artifacts / relative(path); expected = fingerprint(source)
            require(expected["bytes"] > 0, "JOURNAL_DATA")
            relative_name = name + "/" + role.lower() + ".dat"
            copy_verified(source, self.directory / relative_name, expected)
            files.append({"role": role, "path": relative_name, **expected})
        self._append("OPERATION_STARTED", {"processRef": process_ref, "files": files})

    def terminal(self, kind):
        require(kind in {"FAILED", "CANCELLED", "RECOVERY_REQUIRED"}, "JOURNAL_STAGE")
        require(not self.reopened_active or kind == "RECOVERY_REQUIRED", "JOURNAL_EXPLICIT_RECOVERY_REQUIRED")
        self._append(kind, {})

    def complete(self, counts):
        require(not self.reopened_active, "JOURNAL_EXPLICIT_RECOVERY_REQUIRED")
        fields(counts, {"measured", "excluded", "incomplete"})
        require(all(type(v) is int and 0 <= v <= 10000000 for v in counts.values()), "JOURNAL_COUNTS")
        events = self._events(); require(events[-1]["kind"] == "CHECKPOINT", "JOURNAL_STAGE")
        self._verify_artifacts(events)
        report = {"protocol": PROTOCOL, "identity": self.anchor["identity"],
                  "journalParentSha256": self.head_sha, "qualityCounts": counts,
                  "nativeExecution": "CALLER_REPORTED_NOT_ATTESTED", "scienceValidation": "NOT_VALIDATED"}
        sha = write_new(self.directory / "report.json", report)
        self._append("COMPLETED", {"reportSha256": sha})

    def _verify_artifacts(self, events):
        self._snapshot()
        for event in events:
            if event["kind"] in {"OPERATION_STARTED", "CHECKPOINT"}:
                for row in event["data"]["files"]:
                    require(fingerprint(self.directory / row["path"]) == {k: row[k] for k in ["sha256", "bytes"]}, "JOURNAL_CHECKPOINT_CHANGED")

    def queue_receipt(self, sequence):
        require(type(sequence) is int and 1 <= sequence <= 128, "JOURNAL_SEQUENCE")
        events = self._events(); require(bool(events), "JOURNAL_STAGE")
        event = events[-1]; stage = event["kind"]
        require(not self.reopened_active or stage == "RECOVERY_REQUIRED", "JOURNAL_EXPLICIT_RECOVERY_REQUIRED")
        if stage not in {"FAILED", "CANCELLED", "RECOVERY_REQUIRED"}:
            self._verify_artifacts(events)
        require(stage != "PREPARED", "JOURNAL_STAGE")
        result = None
        if stage in {"CHECKPOINT", "OPERATION_STARTED"}: stage = "RUNNING"
        if stage == "COMPLETED":
            report, sha = read_json(self.directory / "report.json")
            require(sha == event["data"]["reportSha256"] and report["identity"] == self.anchor["identity"]
                    and report["journalParentSha256"] == event["previousSha256"], "JOURNAL_REPORT_CHANGED")
            result = {"reportSha256": sha, "bindingRef": self.anchor["identity"]["binding"]["bindingRef"],
                      "qualityCounts": report["qualityCounts"]}
        return {"attemptId": self.anchor["identity"]["attemptId"], "sequence": sequence, "stage": stage, "result": result}
