"""Bounded private evidence packets. Never executes exports or opens embedded paths."""
import argparse
import base64
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

from .export_parser import MAX_BYTES, Unsupported, parse_export, safe_summary

VERSION = "1.0"
IMPORTER_VERSION = "1.2"
MAX_PACKET_BYTES = 32 * 1024 * 1024


class ArchiveError(ValueError):
    """Stable diagnostic only; never include private input values in errors."""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    raw = json.dumps(value, ensure_ascii=True, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    if len(raw) > MAX_PACKET_BYTES:
        raise ArchiveError("PACKET_SIZE_LIMIT")
    return raw


def checked_path(value, *, must_exist=True):
    path = Path(os.path.abspath(value))
    try:
        for component in [*reversed(path.parents), path]:
            if component == path and not must_exist and not component.exists():
                continue
            info = component.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ArchiveError("REPARSE_PATH")
    except ArchiveError:
        raise
    except (OSError, ValueError):
        raise ArchiveError("PATH_UNAVAILABLE") from None
    return path


def read_regular(value, limit):
    path = checked_path(value)
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise ArchiveError("NOT_REGULAR_FILE")
        if before.st_size > limit:
            raise ArchiveError("INPUT_SIZE_LIMIT")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        with os.fdopen(os.open(path, flags), "rb") as stream:
            opened = os.fstat(stream.fileno())
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                raise ArchiveError("SOURCE_CHANGED")
            raw = stream.read(limit + 1)
            after = os.fstat(stream.fileno())
        current = path.lstat()
        signature = lambda info: (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
        if signature(before) != signature(after) or signature(after) != signature(current):
            raise ArchiveError("SOURCE_CHANGED")
        if len(raw) > limit:
            raise ArchiveError("INPUT_SIZE_LIMIT")
        return raw
    except OSError:
        raise ArchiveError("INPUT_UNAVAILABLE") from None


def build_packet(raw, receipt_id, imported_at, *, importer_version=IMPORTER_VERSION):
    if not isinstance(importer_version, str) or importer_version not in {"1.0", "1.1", "1.2"}:
        raise ArchiveError("IMPORTER_VERSION_UNSUPPORTED")
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        raise ArchiveError("SOURCE_SIZE_LIMIT")
    if not isinstance(receipt_id, str) or not re.fullmatch(r"BKL049-[A-Za-z0-9_-]{1,80}", receipt_id):
        raise ArchiveError("RECEIPT_ID_INVALID")
    if not isinstance(imported_at, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", imported_at):
        raise ArchiveError("IMPORT_TIME_INVALID")
    try:
        datetime.strptime(imported_at, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ArchiveError("IMPORT_TIME_INVALID") from None
    result, diagnostic = None, None
    try:
        text = raw.decode("utf-8-sig")
        result = parse_export(text, profile=importer_version)
    except UnicodeError:
        diagnostic = {"code": "UTF8_INVALID", "offset": 0}
    except Unsupported as exc:
        diagnostic = {"code": exc.code, "offset": exc.offset}
    packet = {
        "schemaVersion": VERSION,
        "kind": "BKL049_PRIVATE_SOURCE_PACKET",
        "receiptId": receipt_id,
        "importedAt": imported_at,
        "importerVersion": importer_version,
        "authority": "processing_evidence",
        "actionAuthority": "NONE",
        "publicationState": "PRIVATE_NOT_APPROVED",
        "source": {"encoding": "UTF-8", "byteSize": len(raw), "sha256": digest(raw),
                   "originalBase64": base64.b64encode(raw).decode("ascii")},
        "extractionState": "PARSED_SUBSET" if result else "UNSUPPORTED",
        "diagnostic": diagnostic,
        "archive": result,
        "executionEvidence": "NOT_ESTABLISHED",
        "bindingState": "UNLINKED",
    }
    encode(packet)
    return packet


def verify_packet(raw, expected_digest):
    # The expected digest must come from an independently retained trusted receipt.
    # Matching hashes alone do not authenticate a packet or accept an image association.
    if not isinstance(expected_digest, str) or not re.fullmatch(r"[a-f0-9]{64}", expected_digest):
        raise ArchiveError("TRUST_ANCHOR_REQUIRED")
    if len(raw) > MAX_PACKET_BYTES or digest(raw) != expected_digest:
        raise ArchiveError("PACKET_INTEGRITY")
    try:
        packet = json.loads(raw)
        original = base64.b64decode(packet["source"]["originalBase64"], validate=True)
        rebuilt = build_packet(original, packet["receiptId"], packet["importedAt"],
                               importer_version=packet["importerVersion"])
        if encode(rebuilt) != raw:
            raise ArchiveError("PACKET_CONTENT_MISMATCH")
        return packet
    except (KeyError, TypeError, ValueError, UnicodeError, RecursionError):
        raise ArchiveError("PACKET_CONTENT_MISMATCH") from None


def write_packet(packet, output):
    raw = encode(packet)
    # Reject even a self-consistent caller-supplied object that the importer cannot reproduce.
    verify_packet(raw, digest(raw))
    return write_immutable(raw, output)


def write_immutable(raw, output):
    """Internal bounded byte commit; callers validate their own artifact first.

    Trusted private local filesystem required. No ACL or hostile-parent guarantee.
    """
    if not isinstance(raw, bytes) or len(raw) > MAX_PACKET_BYTES:
        raise ArchiveError("PACKET_SIZE_LIMIT")
    path = checked_path(output, must_exist=False)
    if path.exists():
        previous = read_regular(path, MAX_PACKET_BYTES)
        if previous == raw:
            return "DUPLICATE_NOOP"
        raise ArchiveError("RECEIPT_CONFLICT")
    temporary = None
    outcome = None
    cleanup_pending = False
    try:
        # A single packet keeps source and normalized result together. The hard-link
        # commit is create-if-absent, never rename-overwrite. Unsupported filesystems
        # fail closed; there is deliberately no non-atomic fallback.
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".bkl049-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
        outcome = "CREATED"
    except FileExistsError:
        previous = read_regular(path, MAX_PACKET_BYTES)
        if previous == raw:
            outcome = "DUPLICATE_NOOP"
        else:
            raise ArchiveError("RECEIPT_CONFLICT") from None
    except OSError:
        raise ArchiveError("ATOMIC_COMMIT_UNAVAILABLE") from None
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                # Do not turn a completed commit into a rejection, or mask an
                # earlier commit error. Staging residue is private and unaccepted.
                cleanup_pending = True
    return outcome + ("_CLEANUP_PENDING" if cleanup_pending else "")


def main():
    parser = argparse.ArgumentParser(description="Import a selected history export into a PRIVATE evidence packet.")
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--receipt-id", required=True)
    parser.add_argument("--imported-at", required=True, help="Explicit UTC import time; not a historical execution time.")
    args = parser.parse_args()
    try:
        raw = read_regular(args.source, MAX_BYTES)
        packet = build_packet(raw, args.receipt_id, args.imported_at)
        outcome = write_packet(packet, args.output)
        result = {"outcome": outcome, "extractionState": packet["extractionState"],
                  "publicationState": packet["publicationState"], "bindingState": "UNLINKED"}
        if packet["archive"]:
            result["summary"] = safe_summary(packet["archive"])
        else:
            result["diagnostic"] = packet["diagnostic"]
        print(json.dumps(result))
        return 0 if packet["archive"] else 2
    except ArchiveError as exc:
        print(json.dumps({"outcome": "REJECTED", "code": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
