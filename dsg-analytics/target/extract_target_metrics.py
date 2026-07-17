#!/usr/bin/env python3
"""Digital StarGate Analytics v2.8 - Target metrics extractor.

Scans NINA log files under data/sessions and extracts target-related metadata
from saved-image filenames and exposure lines.

Outputs:
- data/analytics/history/target-exposures.csv
- data/analytics/history/target-summary.csv
- data/analytics/history/target-metrics-report.txt

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional


SAVED_IMAGE_RE = re.compile(
    r"Saved image to\s+(?P<path>.+)$",
    re.IGNORECASE,
)

SUCCESS_SAVED_RE = re.compile(
    r"Successfully saved file at\s+(?P<path>.+?)(?:\.\s+Duration Total:.*)?$",
    re.IGNORECASE,
)

EXPOSURE_RE = re.compile(
    r"Starting Exposure\s*-\s*Exposure Time:\s*(?P<seconds>[\d.]+)s;"
    r".*?Filter:\s*(?P<filter>[^;]*);"
    r".*?Gain:\s*(?P<gain>[^;]*);"
    r".*?Offset:\s*(?P<offset>[^;]*);",
    re.IGNORECASE,
)

FILTER_SWITCH_RE = re.compile(
    r"(?:SwitchFilter.*?Filter:|Filter:\s*)(?P<filter>[A-Za-z0-9+_.-]+)",
    re.IGNORECASE,
)

TIMESTAMP_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?)"
)

SESSION_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$")


@dataclass
class ExposureRecord:
    session_id: str
    log_path: str
    line_number: int
    timestamp: str
    image_path: str
    filename: str
    frame_type: str
    binning: str
    exposure_seconds: str
    gain: str
    offset: str
    target_name: str
    telescope: str
    camera_temperature_c: str
    filter_name: str
    sequence_number: str


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def find_session_id(path: Path) -> str:
    for part in reversed(path.parts):
        if SESSION_ID_RE.match(part):
            return part
    return ""


def parse_timestamp(line: str) -> str:
    match = TIMESTAMP_RE.match(line)
    return match.group("ts") if match else ""


def parse_saved_filename(image_path: str) -> Optional[dict[str, str]]:
    filename = Path(image_path.strip().strip('"')).name

    # Expected NINA structure:
    # LIGHT_1x1_600.00s_910_99_LDN 1320_Skywatcher quattro 200p__-9.90C_LPRO_0075_...
    parts = filename.split("_")
    if len(parts) < 8:
        return None

    frame_type = parts[0].strip()
    binning = parts[1].strip()
    exposure = parts[2].strip()
    gain = parts[3].strip()
    offset = parts[4].strip()

    if exposure.lower().endswith("s"):
        exposure = exposure[:-1]

    temp_index = None
    for index, part in enumerate(parts):
        if re.fullmatch(r"-?\d+(?:\.\d+)?C", part.strip(), re.IGNORECASE):
            temp_index = index
            break

    if temp_index is None or temp_index <= 5:
        return None

    middle = parts[5:temp_index]
    if not middle:
        return None

    # NINA often separates target and telescope with a single underscore,
    # while a double underscore produces an empty token before temperature.
    # Telescope identification is heuristic and deliberately conservative.
    telescope_start = None
    telescope_markers = (
        "skywatcher",
        "celestron",
        "quattro",
        "newton",
        "rc ",
        "rc",
        "c8",
        "edgehd",
        "refractor",
        "apo",
        "askar",
        "ts-optics",
        "william optics",
    )

    joined_middle = [normalize_text(item) for item in middle if item.strip()]
    for index, item in enumerate(joined_middle):
        item_lower = item.lower()
        if any(marker in item_lower for marker in telescope_markers):
            telescope_start = index
            break

    if telescope_start is None:
        target_parts = joined_middle[:1]
        telescope_parts = joined_middle[1:]
    else:
        target_parts = joined_middle[:telescope_start]
        telescope_parts = joined_middle[telescope_start:]

    target = normalize_text(" ".join(target_parts))
    telescope = normalize_text(" ".join(telescope_parts))
    temperature = parts[temp_index].strip().rstrip("C").rstrip("c")

    filter_name = ""
    sequence_number = ""

    for item in parts[temp_index + 1:]:
        value = item.strip()
        if not value:
            continue
        stem = Path(value).stem
        if not filter_name and not stem.isdigit():
            filter_name = stem
            continue
        if stem.isdigit():
            sequence_number = stem
            break

    return {
        "filename": filename,
        "frame_type": frame_type,
        "binning": binning,
        "exposure_seconds": exposure,
        "gain": gain,
        "offset": offset,
        "target_name": target,
        "telescope": telescope,
        "camera_temperature_c": temperature,
        "filter_name": filter_name,
        "sequence_number": sequence_number,
    }


def iter_log_files(root: Path) -> Iterable[Path]:
    yield from sorted(root.rglob("*.log"))


def extract_records(log_path: Path, repo_root: Path) -> list[ExposureRecord]:
    records: list[ExposureRecord] = []
    last_filter = ""
    last_exposure = ""
    last_gain = ""
    last_offset = ""

    try:
        lines = log_path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    except Exception:
        return records

    session_id = find_session_id(log_path)

    for line_number, line in enumerate(lines, start=1):
        exposure_match = EXPOSURE_RE.search(line)
        if exposure_match:
            last_exposure = exposure_match.group("seconds").strip()
            candidate_filter = exposure_match.group("filter").strip()
            if candidate_filter:
                last_filter = candidate_filter
            last_gain = exposure_match.group("gain").strip()
            last_offset = exposure_match.group("offset").strip()

        filter_match = FILTER_SWITCH_RE.search(line)
        if filter_match:
            candidate_filter = filter_match.group("filter").strip()
            if candidate_filter and candidate_filter.lower() not in {
                "wheel",
                "chooser",
                "successfully",
            }:
                last_filter = candidate_filter

        saved_match = SAVED_IMAGE_RE.search(line)
        if not saved_match:
            continue

        image_path = saved_match.group("path").strip()
        parsed = parse_saved_filename(image_path)
        if not parsed:
            continue

        if not parsed["filter_name"]:
            parsed["filter_name"] = last_filter
        if not parsed["exposure_seconds"]:
            parsed["exposure_seconds"] = last_exposure
        if not parsed["gain"]:
            parsed["gain"] = last_gain
        if not parsed["offset"]:
            parsed["offset"] = last_offset

        try:
            relative_log = str(log_path.relative_to(repo_root))
        except ValueError:
            relative_log = str(log_path)

        records.append(
            ExposureRecord(
                session_id=session_id,
                log_path=relative_log,
                line_number=line_number,
                timestamp=parse_timestamp(line),
                image_path=image_path,
                filename=parsed["filename"],
                frame_type=parsed["frame_type"],
                binning=parsed["binning"],
                exposure_seconds=parsed["exposure_seconds"],
                gain=parsed["gain"],
                offset=parsed["offset"],
                target_name=parsed["target_name"],
                telescope=parsed["telescope"],
                camera_temperature_c=parsed["camera_temperature_c"],
                filter_name=parsed["filter_name"],
                sequence_number=parsed["sequence_number"],
            )
        )

    return records


def write_exposures_csv(path: Path, records: list[ExposureRecord]) -> None:
    fieldnames = list(ExposureRecord.__dataclass_fields__.keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def write_summary_csv(path: Path, records: list[ExposureRecord]) -> None:
    grouped: dict[tuple[str, str, str], dict[str, float | int | str]] = defaultdict(
        lambda: {
            "image_count": 0,
            "integration_seconds": 0.0,
            "first_timestamp": "",
            "last_timestamp": "",
        }
    )

    for record in records:
        key = (
            record.session_id,
            record.target_name or "UNKNOWN",
            record.filter_name or "UNKNOWN",
        )
        item = grouped[key]
        item["image_count"] = int(item["image_count"]) + 1

        try:
            item["integration_seconds"] = float(item["integration_seconds"]) + float(
                record.exposure_seconds or 0
            )
        except ValueError:
            pass

        if record.timestamp:
            if not item["first_timestamp"] or record.timestamp < str(item["first_timestamp"]):
                item["first_timestamp"] = record.timestamp
            if not item["last_timestamp"] or record.timestamp > str(item["last_timestamp"]):
                item["last_timestamp"] = record.timestamp

    fieldnames = [
        "session_id",
        "target_name",
        "filter_name",
        "image_count",
        "integration_seconds",
        "integration_hours",
        "first_timestamp",
        "last_timestamp",
    ]

    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for (session_id, target_name, filter_name), item in sorted(grouped.items()):
            integration_seconds = float(item["integration_seconds"])
            writer.writerow(
                {
                    "session_id": session_id,
                    "target_name": target_name,
                    "filter_name": filter_name,
                    "image_count": item["image_count"],
                    "integration_seconds": f"{integration_seconds:.2f}",
                    "integration_hours": f"{integration_seconds / 3600:.4f}",
                    "first_timestamp": item["first_timestamp"],
                    "last_timestamp": item["last_timestamp"],
                }
            )


def write_report(path: Path, logs: list[Path], records: list[ExposureRecord]) -> None:
    targets = Counter(record.target_name or "UNKNOWN" for record in records)
    filters = Counter(record.filter_name or "UNKNOWN" for record in records)
    sessions = Counter(record.session_id or "UNKNOWN" for record in records)

    lines = [
        "=" * 78,
        "DIGITAL STARGATE ANALYTICS v2.8 - TARGET METRICS REPORT",
        "=" * 78,
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"NINA log files scanned: {len(logs)}",
        f"Saved images parsed: {len(records)}",
        f"Sessions found: {len(sessions)}",
        f"Targets found: {len(targets)}",
        f"Filters found: {len(filters)}",
        "",
        "TARGETS",
        "-" * 78,
    ]

    if targets:
        for name, count in targets.most_common():
            lines.append(f"- {name}: {count} image(s)")
    else:
        lines.append("- Nessun target estratto")

    lines.extend(["", "FILTERS", "-" * 78])
    if filters:
        for name, count in filters.most_common():
            lines.append(f"- {name}: {count} image(s)")
    else:
        lines.append("- Nessun filtro estratto")

    lines.extend(["", "SESSIONS", "-" * 78])
    if sessions:
        for name, count in sessions.most_common():
            lines.append(f"- {name}: {count} image(s)")
    else:
        lines.append("- Nessuna sessione estratta")

    lines.extend(["", "SAMPLE RECORDS", "-" * 78])
    for record in records[:20]:
        lines.append(
            f"- {record.session_id} | {record.target_name or 'UNKNOWN'} | "
            f"{record.filter_name or 'UNKNOWN'} | {record.exposure_seconds}s | "
            f"{record.filename}"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract target and filter metrics from NINA log files."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root; default is current directory.",
    )
    parser.add_argument(
        "--sessions-root",
        type=Path,
        help="Sessions root; default is <repo-root>/data/sessions.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory; default is <repo-root>/data/analytics/history.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    sessions_root = (
        args.sessions_root.resolve()
        if args.sessions_root
        else repo_root / "data" / "sessions"
    )
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else repo_root / "data" / "analytics" / "history"
    )

    if not sessions_root.exists():
        raise SystemExit(f"Sessions root not found: {sessions_root}")

    output_dir.mkdir(parents=True, exist_ok=True)

    logs = list(iter_log_files(sessions_root))
    records: list[ExposureRecord] = []

    for log_path in logs:
        records.extend(extract_records(log_path, repo_root))

    # Defensive deduplication: one physical image must produce one record.
    unique_records: list[ExposureRecord] = []
    seen_images: set[tuple[str, str]] = set()
    for record in records:
        key = (record.session_id, record.filename.lower())
        if key in seen_images:
            continue
        seen_images.add(key)
        unique_records.append(record)
    records = unique_records

    exposures_path = output_dir / "target-exposures.csv"
    summary_path = output_dir / "target-summary.csv"
    report_path = output_dir / "target-metrics-report.txt"

    write_exposures_csv(exposures_path, records)
    write_summary_csv(summary_path, records)
    write_report(report_path, logs, records)

    print(f"NINA logs scanned: {len(logs)}")
    print(f"Saved images parsed: {len(records)}")
    print(f"Created: {exposures_path}")
    print(f"Created: {summary_path}")
    print(f"Created: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
