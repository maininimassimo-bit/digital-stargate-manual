#!/usr/bin/env python3
"""Generate docs/data/realtime/latest-observation.json from a completed session.

The updater intentionally separates stable metrics from best-effort astronomical
metadata. Metrics come from normalized/session-metrics.json. Target name and
coordinates are extracted from N.I.N.A. logs when recognizable; otherwise the
existing latest-observation.json values are preserved.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

TARGET_PATTERNS = (
    re.compile(r"(?:target|object|sequence)\s*(?:name)?\s*[:=]\s*['\"]?([^,;|\"']{2,80})", re.I),
    re.compile(r"starting\s+(?:advanced\s+)?sequence.*?\bfor\b\s+['\"]?([^,;|\"']{2,80})", re.I),
    re.compile(r"slew(?:ing)?\s+to\s+['\"]?([^,;|\"']{2,80})", re.I),
)

COORD_PATTERNS = (
    re.compile(
        r"(?:RA|RightAscension)\s*[:=]\s*(-?\d+(?:\.\d+)?)\D+"
        r"(?:DEC|Declination)\s*[:=]\s*(-?\d+(?:\.\d+)?)",
        re.I,
    ),
    re.compile(
        r"coordinates?.*?(-?\d+(?:\.\d+)?)\s*[,;/ ]+\s*(-?\d+(?:\.\d+)?)",
        re.I,
    ),
)


def read_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return dict(default or {})
    text = path.read_text(encoding="utf-8-sig")
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object expected in {path}")
    return value


def iter_nina_logs(session_dir: Path) -> Iterable[Path]:
    nina_dir = session_dir / "raw" / "nina"
    if not nina_dir.exists():
        return ()
    return sorted(nina_dir.glob("*.log"), key=lambda item: item.stat().st_mtime, reverse=True)


def clean_target(value: str) -> str | None:
    value = re.sub(r"\s+", " ", value).strip(" .:-_\t\r\n")
    value = re.split(r"\b(?:at|with|using|coordinates?|RA|DEC)\b", value, maxsplit=1, flags=re.I)[0].strip()
    if not value or len(value) > 80:
        return None
    ignored = {"sequence", "target", "object", "telescope", "mount", "park", "home"}
    if value.lower() in ignored:
        return None
    return value


def extract_astronomical_metadata(session_dir: Path) -> tuple[str | None, float | None, float | None]:
    target: str | None = None
    ra: float | None = None
    dec: float | None = None

    for log_path in iter_nina_logs(session_dir):
        try:
            lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue

        for line in reversed(lines):
            if ra is None or dec is None:
                for pattern in COORD_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        candidate_ra = float(match.group(1))
                        candidate_dec = float(match.group(2))
                        if -360.0 <= candidate_ra <= 360.0 and -90.0 <= candidate_dec <= 90.0:
                            ra, dec = candidate_ra, candidate_dec
                            break

            if target is None:
                for pattern in TARGET_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        target = clean_target(match.group(1))
                        if target:
                            break

            if target and ra is not None and dec is not None:
                return target, ra, dec

    return target, ra, dec


def relative_report_url(session_id: str) -> str:
    year = session_id[0:4]
    month = session_id[5:7]
    return f"./session-reports/{year}/{month}/{session_id}/report-sessione/"


def build_payload(
    session_dir: Path,
    metrics: dict[str, Any],
    existing: dict[str, Any],
) -> dict[str, Any]:
    session_id = str(metrics.get("session_id") or session_dir.name)
    old_target = existing.get("target") if isinstance(existing.get("target"), dict) else {}
    old_sky = existing.get("sky_view") if isinstance(existing.get("sky_view"), dict) else {}

    parsed_name, parsed_ra, parsed_dec = extract_astronomical_metadata(session_dir)
    name = parsed_name or old_target.get("name") or "Target non disponibile"
    ra = parsed_ra if parsed_ra is not None else old_target.get("ra_deg")
    dec = parsed_dec if parsed_dec is not None else old_target.get("dec_deg")

    coordinate_source = "nina-log" if parsed_ra is not None and parsed_dec is not None else old_target.get(
        "coordinate_source", "aladin-name-resolver"
    )

    nina = metrics.get("nina") if isinstance(metrics.get("nina"), dict) else {}
    phd2 = metrics.get("phd2") if isinstance(metrics.get("phd2"), dict) else {}
    integration_seconds = float(nina.get("integration_seconds") or 0.0)

    return {
        "schema_version": "1.0",
        "session_id": session_id,
        "target": {
            "name": name,
            "ra_deg": ra,
            "dec_deg": dec,
            "coordinate_source": coordinate_source,
        },
        "sky_view": {
            "survey": old_sky.get("survey", "P/DSS2/color"),
            "field_of_view_deg": old_sky.get("field_of_view_deg", 1.5),
            "interactive": True,
        },
        "metrics": {
            "integration_hours": round(integration_seconds / 3600.0, 2),
            "completed_frames": int(nina.get("light_completed") or 0),
            "rms_total_arcsec": phd2.get("rms_total_arcsec"),
        },
        "report_url": relative_report_url(session_id),
        "fallback_image": existing.get("fallback_image", "./assets/images/osservatorio-hero.jpg"),
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, type=Path, help="Session directory")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path")
    args = parser.parse_args()

    session_dir: Path = args.session
    metrics_path = session_dir / "normalized" / "session-metrics.json"
    if not metrics_path.exists():
        raise SystemExit(f"Metrics file not found: {metrics_path}")

    metrics = read_json(metrics_path)
    existing = read_json(args.output, default={})
    payload = build_payload(session_dir, metrics, existing)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {args.output} for session {payload['session_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
