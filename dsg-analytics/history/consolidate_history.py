#!/usr/bin/env python3
"""Digital StarGate Analytics 2.0B.1 - historical consolidation and validation.

Scans session-metrics.json files, normalizes the most common field aliases,
upserts data/analytics/history/sessions.csv and writes validation reports.
Only Python standard library modules are required.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
SCHEMA_PATH = SCRIPT_DIR / "history_schema.json"
DEFAULT_CSV = REPO_ROOT / "data" / "analytics" / "history" / "sessions.csv"
DEFAULT_JSON_REPORT = REPO_ROOT / "data" / "analytics" / "history" / "validation-report.json"
DEFAULT_MD_REPORT = REPO_ROOT / "docs" / "analytics" / "history-validation.md"
METRICS_GLOB = "data/sessions/**/normalized/session-metrics.json"

ALIASES = {
    "session_id": ["session_id", "sessionId", "id", "session"],
    "session_start": ["session_start", "sessionStart", "start", "start_time", "startTime", "date_start"],
    "session_end": ["session_end", "sessionEnd", "end", "end_time", "endTime", "date_end"],
    "configuration_id": ["configuration_id", "configurationId", "config_id", "configId", "equipment_profile"],
    "telescope": ["telescope", "ota", "scope"],
    "camera": ["camera", "imaging_camera", "main_camera"],
    "guide_profile": ["guide_profile", "phd2_profile", "guiding_profile"],
    "duration_hours": ["duration_hours", "session_duration_hours", "durationHours"],
    "integration_hours": ["integration_hours", "total_integration_hours", "useful_integration_hours", "integrationHours"],
    "light_started": ["light_started", "lights_started", "light_exposures_started", "started_light_frames"],
    "light_completed": ["light_completed", "lights_completed", "light_exposures_completed", "completed_light_frames"],
    "light_failed": ["light_failed", "lights_failed", "light_exposures_failed", "failed_light_frames"],
    "completion_pct": ["completion_pct", "light_completion_pct", "completionPercent"],
    "rms_ra_arcsec": ["rms_ra_arcsec", "ra_rms_arcsec", "rms_ra", "raRms"],
    "rms_dec_arcsec": ["rms_dec_arcsec", "dec_rms_arcsec", "rms_dec", "decRms"],
    "rms_total_arcsec": ["rms_total_arcsec", "total_rms_arcsec", "rms_total", "totalRms"],
    "weather_safe_pct": ["weather_safe_pct", "safe_pct", "weatherSafePercent"],
    "autofocus_count": ["autofocus_count", "autofocus_runs", "focus_runs"],
    "autofocus_failed": ["autofocus_failed", "autofocus_failures", "focus_failures"],
    "dither_count": ["dither_count", "dithers", "dither_runs"],
    "dither_failed": ["dither_failed", "dither_failures"],
    "severity": ["severity", "status", "session_severity"]
}


def load_schema() -> Dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def flatten(data: Any, prefix: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            out[path] = value
            out.update(flatten(value, path))
    return out


def find_value(data: Dict[str, Any], aliases: Iterable[str]) -> Any:
    flat = flatten(data)
    # Exact top-level and leaf-name matches first.
    for alias in aliases:
        if alias in data and data[alias] not in (None, ""):
            return data[alias]
    lowered = {k.lower(): v for k, v in flat.items()}
    for alias in aliases:
        a = alias.lower()
        for key, value in lowered.items():
            if (key == a or key.endswith("." + a)) and value not in (None, ""):
                return value
    return None


def to_float(value: Any) -> Optional[float]:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def to_int(value: Any) -> Optional[int]:
    number = to_float(value)
    return None if number is None else int(round(number))


def to_iso(value: Any) -> str:
    if value in (None, ""):
        return ""
    text = str(value).strip()
    if text.endswith("Z"):
        return text
    # Keep already parseable ISO values; otherwise preserve input for validation.
    try:
        dt = datetime.fromisoformat(text)
        return dt.isoformat()
    except ValueError:
        return text


def derive_session_id(path: Path) -> str:
    # Expected: .../data/sessions/YYYY/MM/SESSION_ID/normalized/session-metrics.json
    try:
        normalized_index = path.parts.index("normalized")
        return path.parts[normalized_index - 1]
    except (ValueError, IndexError):
        return path.parent.parent.name


def derive_session_times(session_id: str) -> Tuple[str, str]:
    """Derive session start/end timestamps from an ID like YYYY-MM-DD_YYYY-MM-DD.

    Digital StarGate convention:
    - session start: 18:00 on the first date
    - session end:   07:00 on the second date
    """
    if not session_id:
        return "", ""

    match = re.fullmatch(
        r"(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})",
        str(session_id).strip()
    )
    if not match:
        return "", ""

    start_date, end_date = match.groups()
    return (
        f"{start_date}T18:00:00",
        f"{end_date}T07:00:00"
    )


def normalize(metrics: Dict[str, Any], path: Path, schema: Dict[str, Any]) -> Dict[str, str]:
    row: Dict[str, Any] = {column: "" for column in schema["canonical_columns"]}
    row["schema_version"] = schema["schema_version"]
    for field, aliases in ALIASES.items():
        row[field] = find_value(metrics, aliases)

    if not row["session_id"]:
        row["session_id"] = derive_session_id(path)

    # Backward compatibility for legacy metrics files that do not contain
    # explicit session_start/session_end fields. When possible, derive them
    # from the canonical session ID: YYYY-MM-DD_YYYY-MM-DD.
    if not row["session_start"] or not row["session_end"]:
        derived_start, derived_end = derive_session_times(str(row["session_id"]))
        if not row["session_start"]:
            row["session_start"] = derived_start
        if not row["session_end"]:
            row["session_end"] = derived_end

    row["session_start"] = to_iso(row["session_start"])
    row["session_end"] = to_iso(row["session_end"])

    integer_fields = {
        "light_started", "light_completed", "light_failed", "autofocus_count",
        "autofocus_failed", "dither_count", "dither_failed"
    }
    float_fields = {
        "duration_hours", "integration_hours", "completion_pct", "rms_ra_arcsec",
        "rms_dec_arcsec", "rms_total_arcsec", "weather_safe_pct"
    }
    for field in integer_fields:
        value = to_int(row[field])
        row[field] = "" if value is None else value
    for field in float_fields:
        value = to_float(row[field])
        row[field] = "" if value is None else round(value, 4)

    started = to_int(row["light_started"])
    completed = to_int(row["light_completed"])
    failed = to_int(row["light_failed"])
    if started is None and completed is not None and failed is not None:
        started = completed + failed
        row["light_started"] = started
    if row["completion_pct"] in (None, "") and started and completed is not None:
        row["completion_pct"] = round(100.0 * completed / started, 2)

    ra = to_float(row["rms_ra_arcsec"])
    dec = to_float(row["rms_dec_arcsec"])
    if row["rms_total_arcsec"] in (None, "") and ra is not None and dec is not None:
        row["rms_total_arcsec"] = round(math.sqrt(ra * ra + dec * dec), 4)

    if not row["configuration_id"]:
        pieces = [str(row.get("telescope") or "").strip(), str(row.get("camera") or "").strip()]
        row["configuration_id"] = " + ".join(p for p in pieces if p) or "UNKNOWN"

    row["source_metrics_path"] = path.relative_to(REPO_ROOT).as_posix()
    row["updated_at_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return {k: "" if v is None else str(v) for k, v in row.items()}


def parse_dt(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate(rows: List[Dict[str, str]], schema: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []
    seen: Dict[str, int] = {}

    for index, row in enumerate(rows, start=2):
        sid = row.get("session_id", "")
        for field in schema["required"]:
            if not row.get(field, "").strip():
                errors.append({"row": str(index), "session_id": sid, "field": field, "message": "Campo obbligatorio mancante"})

        if sid:
            if sid in seen:
                errors.append({"row": str(index), "session_id": sid, "field": "session_id", "message": f"Duplicato della riga {seen[sid]}"})
            else:
                seen[sid] = index

        start = parse_dt(row.get("session_start", ""))
        end = parse_dt(row.get("session_end", ""))
        if row.get("session_start") and start is None:
            errors.append({"row": str(index), "session_id": sid, "field": "session_start", "message": "Data/ora non valida"})
        if row.get("session_end") and end is None:
            errors.append({"row": str(index), "session_id": sid, "field": "session_end", "message": "Data/ora non valida"})
        if start and end and end <= start:
            errors.append({"row": str(index), "session_id": sid, "field": "session_end", "message": "La fine deve essere successiva all'inizio"})

        for field, limits in schema.get("numeric_ranges", {}).items():
            raw = row.get(field, "")
            if raw == "":
                continue
            number = to_float(raw)
            if number is None:
                errors.append({"row": str(index), "session_id": sid, "field": field, "message": "Valore numerico non valido"})
            elif not (limits[0] <= number <= limits[1]):
                errors.append({"row": str(index), "session_id": sid, "field": field, "message": f"Fuori intervallo [{limits[0]}, {limits[1]}]"})

        started = to_int(row.get("light_started"))
        completed = to_int(row.get("light_completed"))
        failed = to_int(row.get("light_failed"))
        if started is not None and completed is not None and completed > started:
            errors.append({"row": str(index), "session_id": sid, "field": "light_completed", "message": "Completate superiori alle avviate"})
        if started is not None and completed is not None and failed is not None and completed + failed > started:
            warnings.append({"row": str(index), "session_id": sid, "field": "light_failed", "message": "Completate + fallite superiori alle avviate: verificare retry/riconteggi"})

        duration = to_float(row.get("duration_hours"))
        integration = to_float(row.get("integration_hours"))
        if duration is not None and integration is not None and integration > duration * 1.05:
            warnings.append({"row": str(index), "session_id": sid, "field": "integration_hours", "message": "Integrazione superiore alla durata della sessione"})

        if row.get("configuration_id") == "UNKNOWN":
            warnings.append({"row": str(index), "session_id": sid, "field": "configuration_id", "message": "Configurazione non identificata"})

    return {
        "schema_version": schema["schema_version"],
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "row_count": len(rows),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "status": "ERROR" if errors else ("WARNING" if warnings else "OK"),
        "errors": errors,
        "warnings": warnings
    }


def read_existing(path: Path) -> List[Dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        except csv.Error:
            dialect = csv.excel
        return list(csv.DictReader(handle, dialect=dialect))


def write_csv(path: Path, rows: List[Dict[str, str]], columns: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows_sorted = sorted(rows, key=lambda r: (r.get("session_start", ""), r.get("session_id", "")))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows_sorted)


def write_reports(report: Dict[str, Any], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Validazione storico Digital StarGate",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Stato: **{report['status']}**",
        f"- Sessioni: **{report['row_count']}**",
        f"- Errori: **{report['error_count']}**",
        f"- Avvisi: **{report['warning_count']}**",
        f"- Generato: `{report['generated_at_utc']}`",
        ""
    ]
    for title, key in (("Errori", "errors"), ("Avvisi", "warnings")):
        lines.append(f"## {title}")
        lines.append("")
        items = report[key]
        if not items:
            lines.append("Nessuno.")
        else:
            lines.append("| Riga | Sessione | Campo | Messaggio |")
            lines.append("|---:|---|---|---|")
            for item in items:
                lines.append(f"| {item['row']} | `{item['session_id']}` | `{item['field']}` | {item['message']} |")
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    global REPO_ROOT, DEFAULT_CSV, DEFAULT_JSON_REPORT, DEFAULT_MD_REPORT
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--mode", choices=["update", "rebuild", "check"], default="update")
    parser.add_argument("--strict-warnings", action="store_true")
    args = parser.parse_args()

    REPO_ROOT = args.repo_root.resolve()
    DEFAULT_CSV = REPO_ROOT / "data" / "analytics" / "history" / "sessions.csv"
    DEFAULT_JSON_REPORT = REPO_ROOT / "data" / "analytics" / "history" / "validation-report.json"
    DEFAULT_MD_REPORT = REPO_ROOT / "docs" / "analytics" / "history-validation.md"

    schema = load_schema()
    existing = read_existing(DEFAULT_CSV)

    if args.mode == "check":
        rows = existing
    else:
        discovered: List[Dict[str, str]] = []
        for path in sorted(REPO_ROOT.glob(METRICS_GLOB)):
            try:
                metrics = json.loads(path.read_text(encoding="utf-8-sig"))
                discovered.append(normalize(metrics, path, schema))
            except Exception as exc:  # Continue and surface as a synthetic validation row.
                discovered.append({
                    **{column: "" for column in schema["canonical_columns"]},
                    "schema_version": schema["schema_version"],
                    "session_id": derive_session_id(path),
                    "source_metrics_path": path.relative_to(REPO_ROOT).as_posix(),
                    "severity": "PARSER_ERROR",
                    "updated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat()
                })
                print(f"ERRORE lettura {path}: {exc}", file=sys.stderr)

        if args.mode == "rebuild":
            rows = discovered
        else:
            by_id = {row.get("session_id", ""): row for row in existing if row.get("session_id")}
            for row in discovered:
                by_id[row["session_id"]] = row
            rows = list(by_id.values())
        write_csv(DEFAULT_CSV, rows, schema["canonical_columns"])

    report = validate(rows, schema)
    write_reports(report, DEFAULT_JSON_REPORT, DEFAULT_MD_REPORT)
    print(f"Storico: {DEFAULT_CSV}")
    print(f"Sessioni: {report['row_count']} | Errori: {report['error_count']} | Avvisi: {report['warning_count']} | Stato: {report['status']}")
    if report["error_count"]:
        return 2
    if args.strict_warnings and report["warning_count"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())