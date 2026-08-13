#!/usr/bin/env python3
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "2.0B.1"

DEFAULT_FIELDS = [
    "schema_version",
    "session_id",
    "session_start",
    "session_end",
    "configuration_id",
    "telescope",
    "camera",
    "guide_profile",
    "duration_hours",
    "integration_hours",
    "light_started",
    "light_completed",
    "light_failed",
    "completion_pct",
    "rms_ra_arcsec",
    "rms_dec_arcsec",
    "rms_total_arcsec",
    "weather_safe_pct",
    "autofocus_count",
    "autofocus_failed",
    "dither_count",
    "dither_failed",
    "severity",
    "source_metrics_path",
    "updated_at_utc",
]


def _value(mapping, key, default=None):
    value = mapping.get(key, default)
    return "" if value is None else value


def build_row(metrics, metrics_path):
    nina = metrics.get("nina", {})
    phd2 = metrics.get("phd2", {})

    light_started = int(nina.get("light_started") or 0)
    light_completed = int(nina.get("light_completed") or 0)

    light_failed = (
        int(nina.get("light_failed_explicit") or 0)
        + int(nina.get("light_interrupted_unmatched") or 0)
    )

    integration_seconds = nina.get("integration_seconds")

    completion_pct = ""
    if light_started > 0:
        completion_pct = round(
            (light_completed / light_started) * 100.0,
            2
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "session_id": metrics["session_id"],

        # Non inferire dati assenti dalle evidence.
        "session_start": "",
        "session_end": "",
        "configuration_id": "",
        "telescope": "",
        "camera": "",
        "guide_profile": "",
        "duration_hours": "",

        "integration_hours":
            ""
            if integration_seconds is None
            else round(float(integration_seconds) / 3600.0, 4),

        "light_started": light_started,
        "light_completed": light_completed,
        "light_failed": light_failed,
        "completion_pct": completion_pct,

        "rms_ra_arcsec": _value(phd2, "rms_ra_arcsec"),
        "rms_dec_arcsec": _value(phd2, "rms_dec_arcsec"),
        "rms_total_arcsec": _value(phd2, "rms_total_arcsec"),

        # Il contratto analyzer espone unsafe_pct_full_window,
        # non weather_safe_pct canonico 2.0B.1.
        "weather_safe_pct": "",

        "autofocus_count":
            int(nina.get("autofocus_started") or 0),

        "autofocus_failed":
            int(nina.get("autofocus_failed_explicit") or 0),

        "dither_count":
            int(nina.get("dither_requests") or 0),

        "dither_failed": "",

        "severity": _value(metrics, "severity"),

        "source_metrics_path":
            Path(metrics_path).as_posix(),

        "updated_at_utc":
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--history", required=True)
    args = parser.parse_args()

    metrics_path = Path(args.metrics)

    metrics = json.loads(
        metrics_path.read_text(encoding="utf-8")
    )

    row = build_row(metrics, metrics_path)

    history_path = Path(args.history)
    history_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    fieldnames = DEFAULT_FIELDS

    if history_path.exists():
        with history_path.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as handle:

            reader = csv.DictReader(handle)

            if reader.fieldnames:
                # Lo schema versionato esistente è authoritative.
                fieldnames = reader.fieldnames

            rows = list(reader)

    if "session_id" not in fieldnames:
        raise ValueError(
            "History schema does not contain required session_id column"
        )

    # Idempotenza per session_id.
    rows = [
        item
        for item in rows
        if item.get("session_id") != row["session_id"]
    ]

    rows.append({
        key: row.get(key, "")
        for key in fieldnames
    })

    rows.sort(
        key=lambda item: item.get("session_id", "")
    )

    with history_path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
