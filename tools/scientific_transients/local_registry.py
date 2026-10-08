"""Private, quiescent-owner-file registry. No worker, parser, native launch or network."""
import datetime as dt
import hashlib
import os
from pathlib import Path, PurePosixPath
import stat
import uuid

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode, opaque, require
from tools.scientific_transients.queue import BINDING_FIELDS, digest, fields

ROLES = {"INPUT", "REFERENCE", "ALGORITHM", "CONTRACT", "PARAMETERS", "PROVENANCE"}
LIMIT = 1024 * 1024
MAX_FILES = 128  # Storage bound, not an independent-observation count.


def safe_path(path):
    """Reject links/reparse points in every existing ancestor; roots must already exist."""
    path = Path(path)
    require(".." not in path.parts, "LOCAL_ROOT_TRAVERSAL")
    path = Path(os.path.abspath(path))
    for part in [*reversed(path.parents), path]:
        info = part.lstat()
        require(not stat.S_ISLNK(info.st_mode)
                and not getattr(info, "st_file_attributes", 0) & 0x400,
                "LOCAL_LINK_OR_REPARSE")
    return path


def signature(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def fingerprint(path):
    path = safe_path(path)
    require(path.is_file(), "LOCAL_REGULAR_FILE_REQUIRED")
    with path.open("rb") as stream:
        before = os.fstat(stream.fileno())
        require(stat.S_ISREG(before.st_mode), "LOCAL_REGULAR_FILE_REQUIRED")
        value = hashlib.file_digest(stream, "sha256").hexdigest()
        after = os.fstat(stream.fileno())
    current = path.lstat()
    # Windows stat/fstat ctime may differ (CPython #157671); compare ctime only
    # through the same API, then bind path to descriptor by identity/size/mtime.
    require(before.st_ino != 0 and signature(before) == signature(after)
            and signature(after)[:4] == signature(current)[:4], "LOCAL_FILE_CHANGED")
    return {"sha256": value, "bytes": after.st_size}


def relative(value):
    require(type(value) is str and 0 < len(value) <= 512
            and not any(ord(c) < 32 for c in value) and "\\" not in value and ":" not in value,
            "LOCAL_RELATIVE_PATH")
    path = PurePosixPath(value)
    require(not path.is_absolute() and all(p not in {".", ".."} for p in value.split("/"))
            and str(path) == value, "LOCAL_RELATIVE_PATH")
    return path


class LocalRegistry:
    def __init__(self, artifact_root, registry_root):
        self.artifacts, self.registry = safe_path(artifact_root), safe_path(registry_root)
        require(self.artifacts.is_dir() and self.registry.is_dir(), "LOCAL_ROOT_DIRECTORY")
        require(self.artifacts != self.registry and self.artifacts not in self.registry.parents
                and self.registry not in self.artifacts.parents, "LOCAL_ROOT_OVERLAP")

    def _schema(self, value):
        fields(value, {"protocol", "binding", "files"})
        require(value["protocol"] == "DSG_TRANSIENT_LOCAL_BINDING_V1", "LOCAL_PROTOCOL")
        fields(value["binding"], BINDING_FIELDS)
        require(all(opaque(v) for v in value["binding"].values()), "LOCAL_BINDING_ID")
        require(type(value["files"]) is list and 6 <= len(value["files"]) <= MAX_FILES,
                "LOCAL_FILE_COUNT")
        paths, roles = set(), set()
        for record in value["files"]:
            fields(record, {"role", "path", "sha256", "bytes"})
            require(type(record["role"]) is str and record["role"] in ROLES, "LOCAL_ROLE")
            relative(record["path"])
            require(record["path"] not in paths, "LOCAL_DUPLICATE_PATH")
            require(digest(record["sha256"]) and type(record["bytes"]) is int
                    and 0 < record["bytes"] <= 2 ** 53 - 1, "LOCAL_FILE_IDENTITY")
            paths.add(record["path"]); roles.add(record["role"])
        require(roles == ROLES, "LOCAL_MISSING_ROLE")

    def _verify_files(self, value):
        # Point-in-time integrity only. Does not provide a future execution snapshot.
        safe_path(self.artifacts); safe_path(self.registry)
        for record in value["files"]:
            actual = fingerprint(self.artifacts / relative(record["path"]))
            require(actual == {k: record[k] for k in ("sha256", "bytes")}, "LOCAL_BYTES_MISMATCH")

    def _write_new(self, name, raw):
        safe_path(self.registry)
        path = self.registry / name
        # Exclusive create; a partial file after failure is retained and blocks retry.
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())

    def _read_manifest(self, path):
        path = safe_path(path)
        require(path.is_file(), "LOCAL_REGULAR_FILE_REQUIRED")
        with path.open("rb") as stream:
            raw = stream.read(LIMIT + 1)
        require(0 < len(raw) <= LIMIT, "LOCAL_MANIFEST_LIMIT")
        return raw

    def _receipt(self, operation, binding_ref, expected, status, reason):
        value = {"operation": operation, "bindingRef": binding_ref,
                 "manifestSha256": expected, "status": status, "reason": reason,
                 "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
                 "scientificValidation": "NOT_VALIDATED", "nativeExecution": False}
        self._write_new("verification-" + uuid.uuid4().hex + ".json", encode(value))

    def register(self, raw):
        require(type(raw) is bytes and 0 < len(raw) <= LIMIT, "LOCAL_MANIFEST_LIMIT")
        value = decode(raw); self._schema(value)
        canonical = encode(value)
        require(len(canonical) <= LIMIT, "LOCAL_MANIFEST_LIMIT")
        sha = hashlib.sha256(canonical).hexdigest()
        ref = value["binding"]["bindingRef"]
        try:
            self._verify_files(value)
            name = "binding-" + ref + ".json"
            try:
                self._write_new(name, canonical)
            except FileExistsError:
                require(self._read_manifest(self.registry / name) == canonical, "LOCAL_BINDING_CONFLICT")
            self._receipt("REGISTER", ref, sha, "BYTES_VERIFIED", "NO_SCIENTIFIC_ATTESTATION")
        except (ProtocolError, OSError) as error:
            self._receipt("REGISTER", ref, sha, "FAILED", str(error) if isinstance(error, ProtocolError) else "LOCAL_IO_ERROR")
            raise
        return {"binding": value["binding"], "manifestSha256": sha,
                "scientificValidation": "NOT_VALIDATED"}

    def verify(self, binding_ref, manifest_sha256):
        require(opaque(binding_ref) and digest(manifest_sha256), "LOCAL_EXPECTED_IDENTITY")
        try:
            raw = self._read_manifest(self.registry / ("binding-" + binding_ref + ".json"))
            require(hashlib.sha256(raw).hexdigest() == manifest_sha256, "LOCAL_MANIFEST_CHANGED")
            value = decode(raw); self._schema(value)
            require(value["binding"]["bindingRef"] == binding_ref, "LOCAL_BINDING_CONFLICT")
            self._verify_files(value)
            self._receipt("VERIFY", binding_ref, manifest_sha256, "BYTES_VERIFIED", "NO_SCIENTIFIC_ATTESTATION")
            return value
        except (ProtocolError, OSError) as error:
            self._receipt("VERIFY", binding_ref, manifest_sha256, "FAILED", str(error) if isinstance(error, ProtocolError) else "LOCAL_IO_ERROR")
            raise
