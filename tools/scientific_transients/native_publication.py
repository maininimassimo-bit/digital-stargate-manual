"""Parent-only W7 byte-bundle publication. No launch, image decode or close authority."""
import datetime as dt
import hashlib
import json
import math
import os
import re
import stat

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, require
from tools.scientific_transients.local_registry import safe_path, signature
from tools.scientific_transients.native_retention import retain_opaque_product, _hash_bounded

MIB = 1024 * 1024
REQUIRED = frozenset({"started-native.json", "native.log", "result.json", "native-evidence.json",
    "checkpoint.xisf", "source-initial.js", "source-before.js", "source-after.js",
    "checkpoint-initial.js", "checkpoint-current.js", "closing-source.js", "closing-checkpoint.js"})
ERROR_VIEWS = frozenset({"error-owned-1.xisf", "error-owned-2.xisf"})
CONTROL = frozenset({"terminal.json", "terminal-ready.json"})
ALLOWED = REQUIRED | ERROR_VIEWS | CONTROL
STATES = {"COMPLETED_CONDITIONAL_COMPUTATION", "FAILED_RETAINED", "CANCELLED_RETAINED", "UNCERTAIN_RETENTION"}
TERMINAL_FIELDS = {"protocol", "operationRef", "state", "errorCode", "retentionErrorCode", "products",
    "unclosedOwnedViews", "cooperativeDeadlineExceeded", "fullPhysicalVariance", "significance",
    "scientificValidation", "qualifiedControls", "provenanceVerified", "physicalApplicabilityVerified"}
INTENT_FIELDS = {"protocol", "operationRef", "createdUTC", "nativeWorkCanonicalPath",
    "nativeWorkDirectoryIdentity", "retainedCanonicalPath", "retainedDirectoryIdentity",
    "supervisionCanonicalPath", "supervisionDirectoryIdentity", "sealSha256", "grantSha256"}


class PublicationFailure(ProtocolError):
    """All copies/markers remain. The caller retains supervision and blocks new starts."""
    def __init__(self, code, uncertain_marker_written):
        super().__init__(code)
        self.uncertain_marker_written = uncertain_marker_written


def _fields(value, names):
    require(type(value) is dict and set(value) == set(names), "PUBLICATION_FIELDS")


def _sha(value):
    return type(value) is str and re.fullmatch("[a-f0-9]{64}", value) is not None


def _directory(path):
    path = safe_path(path)
    info = path.lstat()
    require(stat.S_ISDIR(info.st_mode) and info.st_ino != 0, "PUBLICATION_DIRECTORY")
    return path, [info.st_dev, info.st_ino]


def _control_tree(value, depth=1):
    require(depth <= 8, "PUBLICATION_JSON_DEPTH")
    if value is None or type(value) is bool: return
    if type(value) is int:
        # Private Python parent metadata includes OS volume/file identities up to 128 bits.
        require(abs(value) <= 2**128 - 1, "PUBLICATION_JSON_INTEGER")
    elif type(value) is str:
        require(len(value) <= 192 and value.isascii(), "PUBLICATION_JSON_STRING")
    elif type(value) is list:
        require(len(value) <= 20, "PUBLICATION_JSON_ARRAY")
        for item in value: _control_tree(item, depth + 1)
    elif type(value) is dict:
        require(len(value) <= 32, "PUBLICATION_JSON_MEMBERS")
        for key, item in value.items():
            require(key not in {"__proto__", "prototype", "constructor"}, "PUBLICATION_JSON_KEY")
            _control_tree(key, depth + 1); _control_tree(item, depth + 1)
    else: raise ProtocolError("PUBLICATION_JSON_TYPE")


def _read_control(path):
    path = safe_path(path)
    raw = bytearray()
    with path.open("rb") as stream:
        before = os.fstat(stream.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                and 0 < before.st_size <= MIB, "PUBLICATION_CONTROL_SIZE")
        while chunk := stream.read(min(65536, MIB - len(raw) + 1)):
            raw.extend(chunk)
            require(len(raw) <= MIB, "PUBLICATION_CONTROL_SIZE")
        after = os.fstat(stream.fileno())
    require(len(raw) == before.st_size and signature(before) == signature(after)
            and signature(after)[:4] == signature(path.lstat())[:4], "PUBLICATION_CONTROL_CHANGED")
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "PUBLICATION_JSON_DUPLICATE")
            value[key] = item
        return value
    def integer(token):
        require(len(token) <= 40, "PUBLICATION_JSON_INTEGER")
        return int(token)
    def invalid(_): raise ProtocolError("PUBLICATION_JSON_NUMBER")
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                           parse_int=integer, parse_float=invalid, parse_constant=invalid)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ProtocolError("PUBLICATION_JSON_INVALID") from exc
    _control_tree(value)
    return value, {"role": path.name, "name": path.name,
                   "sha256": hashlib.sha256(raw).hexdigest(), "byteLength": len(raw)}, before


def _write_control(path, value):
    _control_tree(value)
    raw = encode(value)
    require(len(raw) <= MIB, "PUBLICATION_CONTROL_SIZE")
    safe_path(path.parent)
    with path.open("xb") as stream:
        require(stream.write(raw) == len(raw), "PUBLICATION_SHORT_WRITE")
        stream.flush(); os.fsync(stream.fileno())
        before = os.fstat(stream.fileno())
    observed, record, after = _read_control(path)
    require(signature(before) == signature(after) and observed == value
            and record["sha256"] == hashlib.sha256(raw).hexdigest(), "PUBLICATION_MARKER_READBACK")
    return record["sha256"], after


def _limit(name):
    if name.endswith(".xisf"): return 192 * MIB
    if name.endswith(".js"): return 4 * MIB
    if name == "native.log": return 32 * MIB
    if name == "result.json": return 8 * MIB
    return MIB


def _terminal(value, operation):
    _fields(value, TERMINAL_FIELDS)
    require(value["protocol"] == "DSG_NATIVE_LINEAR_TERMINAL_V1"
            and value["operationRef"] == operation and value["state"] in STATES,
            "PUBLICATION_TERMINAL_IDENTITY")
    require(type(value["unclosedOwnedViews"]) is int and 0 <= value["unclosedOwnedViews"] <= 2
            and type(value["cooperativeDeadlineExceeded"]) is bool, "PUBLICATION_TERMINAL_LIFECYCLE")
    require(value["fullPhysicalVariance"] is None and value["significance"] is None
            and value["scientificValidation"] == "NOT_VALIDATED"
            and type(value["qualifiedControls"]) is int and value["qualifiedControls"] == 0
            and value["provenanceVerified"] is False and value["physicalApplicabilityVerified"] is False,
            "PUBLICATION_SCIENCE_FLAGS")
    for key in ["errorCode", "retentionErrorCode"]:
        require(value[key] is None or (type(value[key]) is str
                and re.fullmatch("[A-Z0-9_]{1,96}", value[key]) is not None), "PUBLICATION_ERROR_CODE")
    require(type(value["products"]) is list and len(value["products"]) <= 18, "PUBLICATION_PRODUCTS")
    names, records = set(), []
    for record in value["products"]:
        _fields(record, {"role", "name", "sha256", "byteLength"})
        name = record["name"]
        require(type(name) is str and name in ALLOWED - CONTROL and name not in names
                and record["role"] == name and _sha(record["sha256"])
                and type(record["byteLength"]) is int and 0 <= record["byteLength"] <= _limit(name),
                "PUBLICATION_PRODUCT_ROLE")
        names.add(name); records.append(dict(record))
    if value["state"] == "COMPLETED_CONDITIONAL_COMPUTATION":
        require(names == REQUIRED and value["unclosedOwnedViews"] == 0
                and value["cooperativeDeadlineExceeded"] is False
                and value["errorCode"] is None and value["retentionErrorCode"] is None,
                "PUBLICATION_INCOMPLETE_SUCCESS")
    else: require(value["errorCode"] is not None, "PUBLICATION_FAILURE_CODE_REQUIRED")
    return records


def _snapshot(path, expected):
    with safe_path(path).open("rb") as stream:
        info = os.fstat(stream.fileno())
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1
                and info.st_size == expected["byteLength"], "PUBLICATION_PRODUCT_SIZE")
    return info


def publish_native_bundle(native_work, retained, supervision, binding, *, clock, deadline):
    """One publication attempt; caller already owns and supervises the sole launch.

    Return is a byte-retention receipt, never permission to close/restart a process.
    Live trusted parent clock/deadline cover the original whole attempt, not this call.
    """
    _fields(binding, {"operationRef", "parentIntentSha256", "sealSha256", "grantSha256"})
    binding = dict(binding)
    operation = binding["operationRef"]
    require(type(operation) is str and re.fullmatch("[a-f0-9]{32}", operation) is not None
            and all(_sha(binding[k]) for k in binding if k != "operationRef"), "PUBLICATION_BINDING")
    require(callable(clock) and type(deadline) in {int, float} and math.isfinite(deadline), "PUBLICATION_CLOCK")
    roots = [_directory(path) for path in [native_work, retained, supervision]]
    work, archive, journal = [row[0] for row in roots]
    require(all(path.name == operation for path in [work, archive, journal])
            and [path.parent.name for path in [work, archive, journal]] ==
                ["native-work", "native-retained", "native-supervision"]
            and work.parent.parent == archive.parent.parent == journal.parent.parent,
            "PUBLICATION_ROOT_LAYOUT")
    def roots_unchanged():
        require([_directory(path) for path in [work, archive, journal]] == roots, "PUBLICATION_ROOT_CHANGED")
    last_clock = None
    def exceeded():
        nonlocal last_clock
        now = clock()
        require(type(now) in {int, float} and math.isfinite(now)
                and (last_clock is None or now >= last_clock), "PUBLICATION_CLOCK_CHANGED")
        last_clock = now
        return now >= deadline
    failed_role = None
    try:
        require(not os.path.lexists(journal / "publication-uncertain.json"), "PUBLICATION_PRIOR_UNCERTAINTY")
        # Reserve even if the subsequent intent/control validation fails. No repair/retry.
        publication_intent = {
            "protocol": "DSG_NATIVE_LINEAR_PUBLICATION_INTENT_V1", "operationRef": operation,
            "parentIntentSha256": binding["parentIntentSha256"], "newNativeStartAllowed": False}
        publication_sha, publication_stat = _write_control(journal / "publication-intent.json", publication_intent)
        intent, intent_record, intent_stat = _read_control(journal / "parent-intent.json")
        _fields(intent, INTENT_FIELDS)
        require(intent_record["sha256"] == binding["parentIntentSha256"]
                and intent["protocol"] == "DSG_NATIVE_LINEAR_PARENT_INTENT_V1"
                and intent["operationRef"] == operation
                and intent["sealSha256"] == binding["sealSha256"]
                and intent["grantSha256"] == binding["grantSha256"], "PUBLICATION_INTENT_BINDING")
        require(type(intent["createdUTC"]) is str
                and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", intent["createdUTC"]) is not None,
                "PUBLICATION_INTENT_TIME")
        dt.datetime.strptime(intent["createdUTC"], "%Y-%m-%dT%H:%M:%SZ")
        for prefix, (path, identity) in zip(["nativeWork", "retained", "supervision"], roots):
            require(intent[prefix + "CanonicalPath"] == path.as_posix()
                    and type(intent[prefix + "DirectoryIdentity"]) is list
                    and all(type(n) is int for n in intent[prefix + "DirectoryIdentity"])
                    and intent[prefix + "DirectoryIdentity"] == identity, "PUBLICATION_INTENT_ROOT")
        require(not list(archive.iterdir()), "PUBLICATION_RETAINED_COLLISION")
        pins = [(journal / "parent-intent.json", intent_record, intent_stat),
                (journal / "publication-intent.json", {"sha256": publication_sha,
                 "byteLength": publication_stat.st_size}, publication_stat)]
        for name, expected_sha in [("launch-seal.json", binding["sealSha256"]),
                                   ("launch-grant.json", binding["grantSha256"])]:
            path = work / name
            with safe_path(path).open("rb") as stream: info = os.fstat(stream.fileno())
            require(0 < info.st_size <= MIB and stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                    "PUBLICATION_LAUNCH_PIN_SIZE")
            record = {"sha256": expected_sha, "byteLength": info.st_size}
            require(_hash_bounded(path, info.st_size, info) == expected_sha, "PUBLICATION_LAUNCH_PIN")
            pins.append((path, record, info))
        ready, ready_record, ready_stat = _read_control(work / "terminal-ready.json")
        _fields(ready, {"protocol", "operationRef", "terminalSha256"})
        require(ready["protocol"] == "DSG_NATIVE_LINEAR_TERMINAL_READY_V1"
                and ready["operationRef"] == operation and _sha(ready["terminalSha256"]), "PUBLICATION_READY")
        terminal, terminal_record, terminal_stat = _read_control(work / "terminal.json")
        require(ready["terminalSha256"] == terminal_record["sha256"], "PUBLICATION_TERMINAL_HASH")
        records = _terminal(terminal, operation) + [terminal_record, ready_record]
        require(len(records) <= 20 and sum(row["byteLength"] for row in records) <= 192 * MIB,
                "PUBLICATION_AGGREGATE")
        require({path.name for path in work.iterdir()} & ALLOWED == {row["name"] for row in records},
                "PUBLICATION_UNLISTED_PRODUCT")
        source_stats = {row["name"]: _snapshot(work / row["name"], row) for row in records}
        # Bind the control parsing descriptors to the sources that are about to be copied.
        require(signature(source_stats["terminal.json"]) == signature(terminal_stat)
                and signature(source_stats["terminal-ready.json"]) == signature(ready_stat),
                "PUBLICATION_CONTROL_CHANGED")
        retained_stats = {}
        for record in records:
            failed_role = record["role"]
            roots_unchanged()
            retain_opaque_product(work, archive, record["name"],
                                  {k: record[k] for k in ["sha256", "byteLength"]})
            retained_stats[record["name"]] = _snapshot(archive / record["name"], record)
        def verify_bundle(marker_pin=None):
            require(not os.path.lexists(journal / "publication-uncertain.json"), "PUBLICATION_PRIOR_UNCERTAINTY")
            for record in records:
                name, size = record["name"], record["byteLength"]
                require(_hash_bounded(work / name, size, source_stats[name]) == record["sha256"]
                        and _hash_bounded(archive / name, size, retained_stats[name]) == record["sha256"],
                        "PUBLICATION_FINAL_PRODUCT_CHANGED")
            for path, record, info in pins:
                require(_hash_bounded(path, record["byteLength"], info) == record["sha256"],
                        "PUBLICATION_PARENT_PIN_CHANGED")
            expected_names = {row["name"] for row in records}
            archive_names = expected_names | ({"retained-native-terminal.json"} if marker_pin else set())
            require({path.name for path in work.iterdir()} & ALLOWED == expected_names
                    and {path.name for path in archive.iterdir()} == archive_names,
                    "PUBLICATION_FINAL_INVENTORY_CHANGED")
            if marker_pin:
                expected_sha, info = marker_pin
                require(_hash_bounded(archive / "retained-native-terminal.json", info.st_size, info)
                        == expected_sha, "PUBLICATION_FINAL_MARKER_CHANGED")
            roots_unchanged()
        verify_bundle()
        overrun = exceeded()
        marker = {"protocol": "DSG_NATIVE_LINEAR_RETAINED_TERMINAL_V1", **binding,
            "nativeTerminalSha256": terminal_record["sha256"], "nativeReadySha256": ready_record["sha256"],
            "nativeState": terminal["state"], "products": records, "allProductsRetained": True,
            "unclosedOwnedViews": terminal["unclosedOwnedViews"],
            "parentMonotonicDeadlineExceeded": overrun, "measurementAccepted": False,
            "scientificValidation": "NOT_VALIDATED", "qualifiedControls": 0}
        failed_role = None
        marker_sha, marker_stat = _write_control(archive / "retained-native-terminal.json", marker)
        # Last IO phase is part of publication: a marker is not acceptance by itself.
        verify_bundle((marker_sha, marker_stat))
        require(exceeded() == overrun, "PUBLICATION_DEADLINE_CROSSED_DURING_MARKER")
        roots_unchanged()
        return {"marker": marker, "markerSha256": marker_sha, "processClosureAuthorized": False,
                "newNativeStartAllowed": False}
    except Exception as exc:
        code = str(exc) if isinstance(exc, ProtocolError) else "PUBLICATION_IO_OR_JSON_FAILURE"
        if re.fullmatch("[A-Z0-9_]{1,96}", code) is None: code = "PUBLICATION_FAILURE"
        marker_written = False
        try:
            roots_unchanged()
            partial = []
            for name in sorted(ALLOWED):
                path = archive / name
                if path.exists():
                    info = safe_path(path).lstat()
                    partial.append({"role": name, "name": name, "byteLength": info.st_size})
            _write_control(journal / "publication-uncertain.json", {
                "protocol": "DSG_NATIVE_LINEAR_PUBLICATION_UNCERTAIN_V1", "operationRef": operation,
                "parentIntentSha256": binding["parentIntentSha256"], "failedRole": failed_role,
                "errorCode": code, "partialProducts": partial, "newNativeStartAllowed": False})
            marker_written = True
        except Exception: pass  # The original error and all files survive even if uncertainty IO fails.
        raise PublicationFailure(code, marker_written) from exc
