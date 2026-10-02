"""Private ingestion review model; no execution, storage or publication authority.

The caller supplies server-loaded catalogue bytes and server-measured file bytes.
This model does not turn the analytics catalogue into an AP-014 registry.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date

from tools.pixinsight.workflow_archive.archive import build_packet


class IngestionError(ValueError):
    """Stable diagnostics without private input values."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _text(value, maximum=160):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise IngestionError("TEXT_INVALID")
    if any(ord(c) < 32 for c in value):
        raise IngestionError("TEXT_INVALID")
    return value.strip()


def _asset(raw, role, media_type):
    if not isinstance(raw, bytes) or not raw:
        raise IngestionError("ASSET_EMPTY")
    limit = 32 * 1024 * 1024 if role == "preview" else 1024 * 1024 * 1024
    if len(raw) > limit:
        raise IngestionError("ASSET_SIZE_LIMIT")
    signatures = {
        "image/jpeg": raw.startswith(b"\xff\xd8\xff"),
        "image/png": raw.startswith(b"\x89PNG\r\n\x1a\n"),
        "application/x-xisf": raw.startswith(b"XISF0100"),
        "application/fits": raw.startswith(b"SIMPLE  =") and len(raw) % 2880 == 0,
    }
    allowed = {"image/jpeg", "image/png"} if role == "preview" else {"application/x-xisf", "application/fits"}
    if media_type not in allowed or not signatures.get(media_type):
        raise IngestionError("MEDIA_SIGNATURE_MISMATCH")
    # A matching signature is a preflight, not an image decode or malware scan.
    return {"role": role, "sha256": sha256(raw), "byteSize": len(raw),
            "mediaType": media_type, "state": "QUARANTINED",
            "securityScan": "PENDING", "previewSanitation": "PENDING" if role == "preview" else "NOT_APPLICABLE"}


def build_review(*, catalog_raw, catalog_digest, session_ids, title,
                 processing_date, original_raw, original_media_type,
                 preview_raw, preview_media_type, workflow_raw, receipt_id,
                 imported_at, preview_attested):
    """Build a reproducible private draft for an authenticated ingestion service.

    The digest must be pinned by the service, never accepted from the browser.
    No publication eligibility is granted here, including for parsed workflows.
    """
    if not isinstance(catalog_raw, bytes) or len(catalog_raw) > 16 * 1024 * 1024:
        raise IngestionError("CATALOG_SIZE_INVALID")
    if not isinstance(catalog_digest, str) or not re.fullmatch(r"[a-f0-9]{64}", catalog_digest) or sha256(catalog_raw) != catalog_digest:
        raise IngestionError("CATALOG_ANCHOR_MISMATCH")
    try:
        catalog = json.loads(catalog_raw)
        if catalog.get("schemaVersion") != "1.5" or catalog.get("catalogStatus") != "VERSIONED_ANALYTICS_PROJECTION":
            raise IngestionError("CATALOG_PROFILE_UNSUPPORTED")
        sessions = catalog["sessions"]
        if not isinstance(sessions, list) or len(sessions) > 10000:
            raise IngestionError("CATALOG_SESSIONS_INVALID")
        index = {}
        for session in sessions:
            sid = _text(session["sessionId"])
            if sid in index:
                raise IngestionError("CATALOG_SESSION_DUPLICATE")
            index[sid] = session
    except (KeyError, TypeError, ValueError, UnicodeError, RecursionError) as exc:
        if isinstance(exc, IngestionError):
            raise
        raise IngestionError("CATALOG_INVALID") from None
    if not isinstance(session_ids, list) or not 1 <= len(session_ids) <= 32 or any(not isinstance(s, str) for s in session_ids):
        raise IngestionError("SESSION_SELECTION_INVALID")
    if len(set(session_ids)) != len(session_ids) or any(s not in index for s in session_ids):
        raise IngestionError("SESSION_SELECTION_INVALID")
    selected = [index[s] for s in session_ids]
    targets = [_text(s.get("target")) for s in selected]
    if len(set(targets)) != 1:
        raise IngestionError("SESSION_TARGET_CONFLICT")
    title = _text(title)
    if not isinstance(processing_date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", processing_date):
        raise IngestionError("PROCESSING_DATE_INVALID")
    try:
        date.fromisoformat(processing_date)
    except ValueError:
        raise IngestionError("PROCESSING_DATE_INVALID") from None
    if preview_attested is not True:
        raise IngestionError("PREVIEW_ASSOCIATION_ATTESTATION_REQUIRED")
    original = _asset(original_raw, "original", original_media_type)
    preview = _asset(preview_raw, "preview", preview_media_type)
    packet = build_packet(workflow_raw, receipt_id, imported_at)
    source = [{"sessionId": s["sessionId"], "target": s["target"],
               "observationDate": s.get("observationDate"),
               "configurationId": s.get("configurationId"),
               "metadataState": s.get("metadataState")} for s in selected]
    review = {
        "schemaVersion": "1.0", "kind": "DSG_PRIVATE_PHOTO_INGESTION_REVIEW_V1",
        "title": title, "target": targets[0], "processingDate": processing_date,
        "importedAt": imported_at,
        "sessionContext": {"source": "VERSIONED_ANALYTICS_PROJECTION",
                           "catalogSha256": catalog_digest, "sessions": source,
                           "association": "OWNER_DECLARED", "registryAdmission": "NOT_ESTABLISHED"},
        "original": original, "preview": preview,
        "previewRelation": {"type": "PUBLICATION_VARIANT_OF", "evidence": "OWNER_ATTESTED",
                            "originalSha256": original["sha256"], "previewSha256": preview["sha256"]},
        "workflow": packet,
        "publicationState": "PRIVATE_NOT_APPROVED", "publicationEligible": False,
        "gaps": ["SECURITY_SCAN_PENDING", "PREVIEW_SANITATION_PENDING", "EXECUTION_NOT_ESTABLISHED"],
        "actionAuthority": "NONE",
    }
    # Idempotency depends on the exact selection and bytes, independently of receipt time.
    identity = {"catalog": catalog_digest, "sessions": session_ids, "title": title,
                "processingDate": processing_date, "original": original, "preview": preview,
                "workflowSha256": sha256(workflow_raw)}
    review["draftKey"] = sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode())
    return review
