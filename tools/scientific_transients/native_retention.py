"""Exclusive bounded opaque-byte retention for the native supervisor.

No image decoding, launch, terminal acceptance, retry, deletion or process closure.
The trusted parent owns quiescent directories; this is not a hostile-filesystem sandbox.
"""
import hashlib
import os
from pathlib import Path
import stat

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.local_registry import safe_path, signature

CHUNK_BYTES = 65536
MAX_PRODUCT_BYTES = 192 * 1024 * 1024


def _identity(path):
    info = safe_path(path).lstat()
    require(stat.S_ISDIR(info.st_mode) and info.st_ino != 0, "RETENTION_DIRECTORY")
    return info.st_dev, info.st_ino


def _same_file(before, after, path):
    current = safe_path(path).lstat()
    require(before.st_ino != 0 and signature(before) == signature(after)
            and signature(after)[:4] == signature(current)[:4], "RETENTION_FILE_CHANGED")


def _hash_bounded(path, expected_size, expected_stat):
    digest, count = hashlib.sha256(), 0
    with safe_path(path).open("rb") as stream:
        before = os.fstat(stream.fileno())
        require(signature(before) == signature(expected_stat), "RETENTION_IDENTITY_CHANGED")
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                and before.st_size == expected_size, "RETENTION_FILE_SHAPE")
        while chunk := stream.read(min(CHUNK_BYTES, expected_size - count + 1)):
            count += len(chunk)
            require(count <= expected_size, "RETENTION_SIZE_CHANGED")
            digest.update(chunk)
        _same_file(before, os.fstat(stream.fileno()), path)
    require(count == expected_size, "RETENTION_SIZE_CHANGED")
    return digest.hexdigest()


def retain_opaque_product(source_directory, retained_directory, name, expected):
    """Copy a single declared product once, retaining any partial destination.

    Caller must consume the attempt before calling and preserve uncertainty on
    *every* exception. A return proves byte retention only. No marker is repaired
    here and no exception authorizes a retry or closure of an owned native view.
    Aggregate limits, terminal/ready binding and supervision are caller duties.
    """
    require(type(name) is str and 1 <= len(name) <= 96
            and name[0].isalnum() and name.isascii()
            and all(c.isalnum() or c in "-_." for c in name)
            and name not in {".", ".."} and ".." not in name
            and not name.endswith(".")
            and name.split(".")[0].upper() not in
            {"CON", "PRN", "AUX", "NUL", *["COM" + str(i) for i in range(1, 10)],
             *["LPT" + str(i) for i in range(1, 10)]}, "RETENTION_NAME")
    require(type(expected) is dict and set(expected) == {"sha256", "byteLength"},
            "RETENTION_EXPECTED")
    sha, size = expected["sha256"], expected["byteLength"]
    require(type(sha) is str and len(sha) == 64
            and all(c in "0123456789abcdef" for c in sha)
            and type(size) is int and 0 <= size <= MAX_PRODUCT_BYTES,
            "RETENTION_EXPECTED")
    source_root, destination_root = safe_path(source_directory), safe_path(retained_directory)
    require(source_root != destination_root and source_root not in destination_root.parents
            and destination_root not in source_root.parents, "RETENTION_ROOT_OVERLAP")
    roots = _identity(source_root), _identity(destination_root)
    source, destination = source_root / name, destination_root / name
    digest, count = hashlib.sha256(), 0
    with safe_path(source).open("rb") as incoming:
        before = os.fstat(incoming.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                and before.st_size == size, "RETENTION_FILE_SHAPE")
        require(_identity(source_root) == roots[0] and _identity(destination_root) == roots[1],
                "RETENTION_ROOT_CHANGED")
        # OS exclusive creation: an existing zero-length or identical file is a collision.
        with destination.open("xb") as outgoing:
            while chunk := incoming.read(min(CHUNK_BYTES, size - count + 1)):
                count += len(chunk)
                require(count <= size, "RETENTION_SIZE_CHANGED")
                require(outgoing.write(chunk) == len(chunk), "RETENTION_SHORT_WRITE")
                digest.update(chunk)
            outgoing.flush()
            os.fsync(outgoing.fileno())
            written = os.fstat(outgoing.fileno())
            require(stat.S_ISREG(written.st_mode) and written.st_nlink == 1
                    and written.st_size == size, "RETENTION_DESTINATION_SHAPE")
        _same_file(before, os.fstat(incoming.fileno()), source)
    require(count == size and digest.hexdigest() == sha, "RETENTION_COPY_MISMATCH")
    require(_hash_bounded(destination, size, written) == sha, "RETENTION_READBACK_MISMATCH")
    # Read source again, not just metadata: a same-size mutation must not pass.
    require(_hash_bounded(source, size, before) == sha, "RETENTION_SOURCE_MISMATCH")
    with safe_path(destination).open("rb") as reopened:
        _same_file(written, os.fstat(reopened.fileno()), destination)
    require(_identity(source_root) == roots[0] and _identity(destination_root) == roots[1],
            "RETENTION_ROOT_CHANGED")
    return {"name": name, "sha256": sha, "byteLength": size,
            "retention": "OPAQUE_BYTES_VERIFIED", "scientificValidation": "NOT_VALIDATED"}
