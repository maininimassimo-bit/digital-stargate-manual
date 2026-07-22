"""Load and validate Digital StarGate session manifests."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from session.metadata import SessionMetadata


SESSION_ID_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$"
)


class SessionMetadataError(ValueError):
    """Raised when a session manifest is missing or invalid."""


def find_session_path(path: Path) -> Path:
    """Return the nearest parent directory having a session identifier."""
    candidate = path.resolve()

    if candidate.is_file():
        candidate = candidate.parent

    for current in (candidate, *candidate.parents):
        if SESSION_ID_RE.fullmatch(current.name):
            return current

    raise SessionMetadataError(
        f"Session directory not found in path: {path}"
    )


def _require_text(
    payload: dict[str, Any],
    field_name: str,
    manifest_path: Path,
) -> str:
    value = payload.get(field_name)

    if not isinstance(value, str) or not value.strip():
        raise SessionMetadataError(
            f"Missing or invalid '{field_name}' in {manifest_path}"
        )

    return value.strip()


def parse_local_datetime(
    value: str,
    timezone_id: str,
    field_name: str = "timestamp",
) -> datetime:
    """Parse an ISO timestamp and attach the session timezone when absent."""
    normalized = value.strip()

    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise SessionMetadataError(
            f"Invalid ISO timestamp for '{field_name}': {value}"
        ) from exc

    try:
        timezone = ZoneInfo(timezone_id)
    except ZoneInfoNotFoundError as exc:
        raise SessionMetadataError(
            f"Unknown timezone_id: {timezone_id}"
        ) from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone)

    return parsed


def load_session_metadata(session_path: Path) -> SessionMetadata:
    """Load, validate and return metadata for one observing session."""
    resolved_session_path = find_session_path(session_path)
    manifest_path = resolved_session_path / "manifest.json"

    if not manifest_path.is_file():
        raise SessionMetadataError(
            f"Session manifest not found: {manifest_path}"
        )

    try:
        payload = json.loads(
            manifest_path.read_text(
                encoding="utf-8-sig",
                errors="strict",
            )
        )
    except json.JSONDecodeError as exc:
        raise SessionMetadataError(
            f"Invalid JSON manifest: {manifest_path}: {exc}"
        ) from exc
    except OSError as exc:
        raise SessionMetadataError(
            f"Unable to read manifest: {manifest_path}: {exc}"
        ) from exc

    if not isinstance(payload, dict):
        raise SessionMetadataError(
            f"Manifest root must be a JSON object: {manifest_path}"
        )

    session_id = _require_text(
        payload,
        "session_id",
        manifest_path,
    )
    timezone_id = _require_text(
        payload,
        "timezone_id",
        manifest_path,
    )
    start_value = _require_text(
        payload,
        "start_local",
        manifest_path,
    )
    end_value = _require_text(
        payload,
        "end_local",
        manifest_path,
    )

    if not SESSION_ID_RE.fullmatch(session_id):
        raise SessionMetadataError(
            f"Invalid session_id '{session_id}' in {manifest_path}"
        )

    if session_id != resolved_session_path.name:
        raise SessionMetadataError(
            "Session ID mismatch: "
            f"folder='{resolved_session_path.name}', "
            f"manifest='{session_id}'"
        )

    start_local = parse_local_datetime(
        start_value,
        timezone_id,
        "start_local",
    )
    end_local = parse_local_datetime(
        end_value,
        timezone_id,
        "end_local",
    )

    if end_local <= start_local:
        raise SessionMetadataError(
            f"Session end must be after start in {manifest_path}"
        )

    generated_at_local: datetime | None = None
    generated_value = payload.get("generated_at_local")

    if isinstance(generated_value, str) and generated_value.strip():
        generated_at_local = parse_local_datetime(
            generated_value,
            timezone_id,
            "generated_at_local",
        )

    raw_files = payload.get("files", [])
    if not isinstance(raw_files, list):
        raise SessionMetadataError(
            f"Field 'files' must be a list in {manifest_path}"
        )

    files: list[dict[str, Any]] = []
    for index, item in enumerate(raw_files):
        if not isinstance(item, dict):
            raise SessionMetadataError(
                f"Invalid files[{index}] in {manifest_path}"
            )
        files.append(dict(item))

    try:
        diagnostic_level = int(
            payload.get("diagnostic_level", 0)
        )
    except (TypeError, ValueError) as exc:
        raise SessionMetadataError(
            f"Invalid diagnostic_level in {manifest_path}"
        ) from exc

    return SessionMetadata(
        session_id=session_id,
        session_path=resolved_session_path,
        manifest_path=manifest_path,
        schema_version=str(payload.get("schema_version", "")),
        observatory=str(payload.get("observatory", "")),
        timezone_id=timezone_id,
        start_local=start_local,
        end_local=end_local,
        report_status=str(payload.get("report_status", "")),
        severity=str(payload.get("severity", "")),
        diagnostic_level=diagnostic_level,
        generated_at_local=generated_at_local,
        files=tuple(files),
    )
