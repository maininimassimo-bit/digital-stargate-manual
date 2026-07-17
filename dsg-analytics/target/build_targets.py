#!/usr/bin/env python3
"""Digital StarGate Analytics v2.8 - Build targets dataset.

Reads:
    data/analytics/history/target-exposures.csv

Writes:
    data/analytics/history/targets.csv
    data/analytics/history/targets-report.txt

The output contains one aggregated row for each combination of:
session, target, filter, telescope, frame type, binning, gain and offset.

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


GROUP_FIELDS = [
    "session_id",
    "target_name",
    "filter_name",
    "telescope",
    "frame_type",
    "binning",
    "gain",
    "offset",
]


def clean(value: Any, fallback: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text or fallback


def parse_float(value: Any) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0


def read_exposures(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def aggregate(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, ...], dict[str, Any]] = defaultdict(
        lambda: {
            "image_count": 0,
            "integration_seconds": 0.0,
            "first_timestamp": "",
            "last_timestamp": "",
            "temperature_sum": 0.0,
            "temperature_count": 0,
            "first_image_path": "",
            "last_image_path": "",
        }
    )

    for row in rows:
        normalized = {
            "session_id": clean(row.get("session_id"), "UNKNOWN"),
            "target_name": clean(row.get("target_name"), "UNKNOWN"),
            "filter_name": clean(row.get("filter_name"), "UNKNOWN"),
            "telescope": clean(row.get("telescope"), "UNKNOWN"),
            "frame_type": clean(row.get("frame_type"), "UNKNOWN"),
            "binning": clean(row.get("binning"), "UNKNOWN"),
            "gain": clean(row.get("gain"), "UNKNOWN"),
            "offset": clean(row.get("offset"), "UNKNOWN"),
        }

        key = tuple(normalized[field] for field in GROUP_FIELDS)
        item = grouped[key]

        item["image_count"] += 1
        item["integration_seconds"] += parse_float(row.get("exposure_seconds"))

        timestamp = clean(row.get("timestamp"))
        if timestamp:
            if not item["first_timestamp"] or timestamp < item["first_timestamp"]:
                item["first_timestamp"] = timestamp
            if not item["last_timestamp"] or timestamp > item["last_timestamp"]:
                item["last_timestamp"] = timestamp

        temperature = clean(row.get("camera_temperature_c"))
        if temperature:
            value = parse_float(temperature)
            item["temperature_sum"] += value
            item["temperature_count"] += 1

        image_path = clean(row.get("image_path"))
        if image_path:
            if not item["first_image_path"]:
                item["first_image_path"] = image_path
            item["last_image_path"] = image_path

    output: list[dict[str, str]] = []

    for key, item in sorted(grouped.items()):
        record = dict(zip(GROUP_FIELDS, key))
        integration_seconds = float(item["integration_seconds"])
        temperature_count = int(item["temperature_count"])
        avg_temperature = (
            float(item["temperature_sum"]) / temperature_count
            if temperature_count
            else 0.0
        )

        record.update(
            {
                "image_count": str(item["image_count"]),
                "integration_seconds": f"{integration_seconds:.2f}",
                "integration_hours": f"{integration_seconds / 3600:.4f}",
                "average_exposure_seconds": (
                    f"{integration_seconds / item['image_count']:.2f}"
                    if item["image_count"]
                    else "0.00"
                ),
                "average_camera_temperature_c": (
                    f"{avg_temperature:.2f}" if temperature_count else ""
                ),
                "first_timestamp": item["first_timestamp"],
                "last_timestamp": item["last_timestamp"],
                "first_image_path": item["first_image_path"],
                "last_image_path": item["last_image_path"],
            }
        )
        output.append(record)

    return output


def write_targets(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = GROUP_FIELDS + [
        "image_count",
        "integration_seconds",
        "integration_hours",
        "average_exposure_seconds",
        "average_camera_temperature_c",
        "first_timestamp",
        "last_timestamp",
        "first_image_path",
        "last_image_path",
    ]

    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    source_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> None:
    total_images = sum(int(row["image_count"]) for row in target_rows)
    total_seconds = sum(float(row["integration_seconds"]) for row in target_rows)

    targets = sorted(
        {
            row["target_name"]
            for row in target_rows
            if row["target_name"] != "UNKNOWN"
        }
    )
    sessions = sorted(
        {
            row["session_id"]
            for row in target_rows
            if row["session_id"] != "UNKNOWN"
        }
    )
    filters = sorted(
        {
            row["filter_name"]
            for row in target_rows
            if row["filter_name"] != "UNKNOWN"
        }
    )

    lines = [
        "=" * 78,
        "DIGITAL STARGATE ANALYTICS v2.8 - TARGETS DATASET REPORT",
        "=" * 78,
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"Exposure rows read: {len(source_rows)}",
        f"Aggregated target rows: {len(target_rows)}",
        f"Sessions: {len(sessions)}",
        f"Targets: {len(targets)}",
        f"Filters: {len(filters)}",
        f"Total images: {total_images}",
        f"Total integration hours: {total_seconds / 3600:.4f}",
        "",
        "AGGREGATED ROWS",
        "-" * 78,
    ]

    for row in target_rows:
        lines.append(
            f"- {row['session_id']} | {row['target_name']} | "
            f"{row['filter_name']} | {row['image_count']} image(s) | "
            f"{row['integration_hours']} h | {row['telescope']}"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate target exposure records into targets.csv."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root; default is current directory.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Input target-exposures.csv path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output targets.csv path.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Output targets-report.txt path.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    history_dir = repo_root / "data" / "analytics" / "history"

    input_path = (
        args.input.resolve()
        if args.input
        else history_dir / "target-exposures.csv"
    )
    output_path = (
        args.output.resolve()
        if args.output
        else history_dir / "targets.csv"
    )
    report_path = (
        args.report.resolve()
        if args.report
        else history_dir / "targets-report.txt"
    )

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    source_rows = read_exposures(input_path)
    target_rows = aggregate(source_rows)

    write_targets(output_path, target_rows)
    write_report(report_path, source_rows, target_rows)

    print(f"Exposure rows read: {len(source_rows)}")
    print(f"Aggregated target rows: {len(target_rows)}")
    print(f"Created: {output_path}")
    print(f"Created: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
