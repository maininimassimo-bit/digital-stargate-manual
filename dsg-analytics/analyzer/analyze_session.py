from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class SessionMetrics:
    session_id: str
    exposures_started: int = 0
    exposures_completed: int = 0
    exposures_failed: int = 0
    integration_seconds: float = 0.0
    autofocus_runs: int = 0
    autofocus_failures: int = 0
    dithers: int = 0
    phd2_guiding_sessions: int = 0
    phd2_rms_ra_arcsec: float | None = None
    phd2_rms_dec_arcsec: float | None = None
    phd2_rms_total_arcsec: float | None = None
    weather_rows: int = 0
    weather_unsafe_rows: int = 0
    severity: str = "GREEN"
    notes: list[str] | None = None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def find_files(root: Path, patterns: Iterable[str]) -> list[Path]:
    found: list[Path] = []
    for pattern in patterns:
        found.extend(root.rglob(pattern))
    return sorted(set(found))


def parse_nina(files: list[Path], m: SessionMetrics) -> None:
    started_re = re.compile(r"TakeExposure, ExposureTime\s+([0-9.]+).+ImageType\s+LIGHT", re.I)
    finished_re = re.compile(r"Finishing Category: Fotocamera, Item: TakeExposure, ExposureTime\s+([0-9.]+).+ImageType\s+LIGHT", re.I)
    for path in files:
        text = read_text(path)
        m.exposures_started += len(started_re.findall(text))
        completed = [float(x) for x in finished_re.findall(text)]
        m.exposures_completed += len(completed)
        m.integration_seconds += sum(completed)
        m.autofocus_runs += text.count("Starting Category: Focheggiatore, Item: RunAutofocus")
        m.autofocus_failures += len(re.findall(r"AutoFocus.*(?:fail|error|aborted)", text, re.I))
        m.dithers += text.count("Starting Category: Guida, Item: Dither")
        m.exposures_failed += len(re.findall(r"TakeExposure.*(?:fail|error|aborted)", text, re.I))
    if m.exposures_started > m.exposures_completed:
        m.exposures_failed = max(m.exposures_failed, m.exposures_started - m.exposures_completed)


def parse_phd2(files: list[Path], m: SessionMetrics) -> None:
    ra_vals: list[float] = []
    dec_vals: list[float] = []
    m.phd2_guiding_sessions = 0
    for path in files:
        text = read_text(path)
        m.phd2_guiding_sessions += text.count("Guiding Begins at")
        for line in text.splitlines():
            if not re.match(r"^\d+,", line):
                continue
            parts = next(csv.reader([line]))
            if len(parts) < 9:
                continue
            try:
                ra_vals.append(float(parts[7]))
                dec_vals.append(float(parts[8]))
            except (ValueError, IndexError):
                continue
    if ra_vals:
        m.phd2_rms_ra_arcsec = math.sqrt(sum(v * v for v in ra_vals) / len(ra_vals))
    if dec_vals:
        m.phd2_rms_dec_arcsec = math.sqrt(sum(v * v for v in dec_vals) / len(dec_vals))
    if m.phd2_rms_ra_arcsec is not None and m.phd2_rms_dec_arcsec is not None:
        m.phd2_rms_total_arcsec = math.sqrt(m.phd2_rms_ra_arcsec**2 + m.phd2_rms_dec_arcsec**2)


def parse_weather(files: list[Path], m: SessionMetrics) -> None:
    for path in files:
        with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                m.weather_rows += 1
                values = " ".join(str(v) for v in row.values()).lower()
                if "unsafe" in values or "false" in values:
                    m.weather_unsafe_rows += 1


def classify(m: SessionMetrics, thresholds: dict) -> None:
    severity = "GREEN"
    notes: list[str] = []
    rank = {"GREEN": 0, "YELLOW": 1, "ORANGE": 2, "RED": 3}

    def raise_to(level: str, note: str) -> None:
        nonlocal severity
        if rank[level] > rank[severity]:
            severity = level
        notes.append(note)

    rms = m.phd2_rms_total_arcsec
    if rms is not None:
        if rms >= thresholds["rms_total_red_arcsec"]:
            raise_to("RED", f"RMS totale elevato: {rms:.2f} arcsec")
        elif rms >= thresholds["rms_total_orange_arcsec"]:
            raise_to("ORANGE", f"RMS totale sopra soglia: {rms:.2f} arcsec")
        elif rms >= thresholds["rms_total_yellow_arcsec"]:
            raise_to("YELLOW", f"RMS totale da monitorare: {rms:.2f} arcsec")

    if m.exposures_failed >= thresholds["failed_exposures_red"]:
        raise_to("RED", f"Pose fallite: {m.exposures_failed}")
    elif m.exposures_failed >= thresholds["failed_exposures_orange"]:
        raise_to("ORANGE", f"Pose fallite: {m.exposures_failed}")
    elif m.exposures_failed >= thresholds["failed_exposures_yellow"]:
        raise_to("YELLOW", f"Pose fallite: {m.exposures_failed}")

    if m.autofocus_failures >= thresholds["autofocus_failures_orange"]:
        raise_to("ORANGE", f"Autofocus falliti: {m.autofocus_failures}")
    elif m.autofocus_failures >= thresholds["autofocus_failures_yellow"]:
        raise_to("YELLOW", f"Autofocus falliti: {m.autofocus_failures}")

    m.severity = severity
    m.notes = notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True, type=Path)
    parser.add_argument("--thresholds", type=Path, default=Path(__file__).parents[1] / "config" / "thresholds.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root: Path = args.session
    if not root.exists():
        raise SystemExit(f"Sessione non trovata: {root}")

    metrics = SessionMetrics(session_id=root.name)
    parse_nina(find_files(root, ["*.log"]), metrics)
    parse_phd2(find_files(root / "raw" / "phd2", ["*.txt", "*.log"]), metrics)
    parse_weather(find_files(root / "raw" / "weather", ["*.csv"]), metrics)

    thresholds = json.loads(args.thresholds.read_text(encoding="utf-8"))
    classify(metrics, thresholds)

    output = args.output or (root / "normalized" / "session-metrics.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(metrics), indent=2, ensure_ascii=False), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
