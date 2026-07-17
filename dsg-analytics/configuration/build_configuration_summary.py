#!/usr/bin/env python3
"""Build Digital StarGate analytics summaries grouped by equipment configuration."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parents[1]

INPUT_RELATIVE_PATH = Path("data/analytics/history/sessions.csv")
OUTPUT_CSV_RELATIVE_PATH = Path(
    "data/analytics/history/configuration-summary.csv"
)
OUTPUT_MD_RELATIVE_PATH = Path(
    "docs/analytics/configuration-summary.md"
)

OUTPUT_COLUMNS = [
    "configuration_id",
    "configuration_name",
    "telescope",
    "camera",
    "session_count",
    "total_duration_hours",
    "total_integration_hours",
    "integration_efficiency_pct",
    "light_started",
    "light_completed",
    "light_failed",
    "average_completion_pct",
    "average_rms_total_arcsec",
    "first_session_start",
    "last_session_end",
]


def to_float(value: object) -> Optional[float]:
    if value in (None, ""):
        return None

    try:
        return float(str(value).strip().replace(",", "."))
    except ValueError:
        return None


def to_int(value: object) -> Optional[int]:
    number = to_float(value)
    if number is None:
        return None
    return int(round(number))


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"File non trovato: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def average(values: List[float]) -> str:
    if not values:
        return ""

    return f"{sum(values) / len(values):.4f}".rstrip("0").rstrip(".")


def decimal(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def build_summary(
    sessions: List[Dict[str, str]],
    equipment_registry: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    registry_by_id = {
        str(row.get("configuration_id", "")).strip(): row
        for row in equipment_registry
        if str(row.get("configuration_id", "")).strip()
    }

    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    for row in sessions:
        configuration_id = str(
            row.get("configuration_id", "") or "UNKNOWN"
        ).strip()

        grouped[configuration_id].append(row)

    summaries: List[Dict[str, str]] = []

    for configuration_id, rows in sorted(grouped.items()):
        registry = registry_by_id.get(configuration_id, {})

        durations = [
            value
            for row in rows
            if (value := to_float(row.get("duration_hours"))) is not None
        ]

        integrations = [
            value
            for row in rows
            if (value := to_float(row.get("integration_hours"))) is not None
        ]

        completion_values = [
            value
            for row in rows
            if (value := to_float(row.get("completion_pct"))) is not None
        ]

        rms_values = [
            value
            for row in rows
            if (value := to_float(row.get("rms_total_arcsec"))) is not None
        ]

        total_duration = sum(durations)
        total_integration = sum(integrations)

        efficiency = ""
        if total_duration > 0:
            efficiency = decimal(
                100.0 * total_integration / total_duration,
                2,
            )

        started = sum(
            value
            for row in rows
            if (value := to_int(row.get("light_started"))) is not None
        )

        completed = sum(
            value
            for row in rows
            if (value := to_int(row.get("light_completed"))) is not None
        )

        failed = sum(
            value
            for row in rows
            if (value := to_int(row.get("light_failed"))) is not None
        )

        starts = sorted(
            row.get("session_start", "")
            for row in rows
            if row.get("session_start", "")
        )

        ends = sorted(
            row.get("session_end", "")
            for row in rows
            if row.get("session_end", "")
        )

        summaries.append(
            {
                "configuration_id": configuration_id,
                "configuration_name": str(
                    registry.get("configuration_name", "")
                ),
                "telescope": str(
                    registry.get("telescope")
                    or rows[0].get("telescope", "")
                ),
                "camera": str(
                    registry.get("camera")
                    or rows[0].get("camera", "")
                ),
                "session_count": str(len(rows)),
                "total_duration_hours": decimal(total_duration),
                "total_integration_hours": decimal(total_integration),
                "integration_efficiency_pct": efficiency,
                "light_started": str(started),
                "light_completed": str(completed),
                "light_failed": str(failed),
                "average_completion_pct": average(completion_values),
                "average_rms_total_arcsec": average(rms_values),
                "first_session_start": starts[0] if starts else "",
                "last_session_end": ends[-1] if ends else "",
            }
        )

    return summaries


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def markdown_value(value: str) -> str:
    return value if value not in ("", None) else "—"


def write_markdown(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Riepilogo per configurazione",
        "",
        "Report generato dallo storico delle sessioni Digital StarGate.",
        "",
    ]

    if not rows:
        lines.append("Nessuna sessione disponibile.")
    else:
        for row in rows:
            title = (
                row["configuration_name"]
                or row["configuration_id"]
            )

            lines.extend(
                [
                    f"## {title}",
                    "",
                    f"- ID: `{row['configuration_id']}`",
                    f"- Telescopio: {markdown_value(row['telescope'])}",
                    f"- Camera: {markdown_value(row['camera'])}",
                    f"- Sessioni: **{row['session_count']}**",
                    (
                        "- Durata complessiva: "
                        f"**{markdown_value(row['total_duration_hours'])} h**"
                    ),
                    (
                        "- Integrazione complessiva: "
                        f"**{markdown_value(row['total_integration_hours'])} h**"
                    ),
                    (
                        "- Efficienza di integrazione: "
                        f"**{markdown_value(row['integration_efficiency_pct'])}%**"
                    ),
                    (
                        "- Completamento medio: "
                        f"**{markdown_value(row['average_completion_pct'])}%**"
                    ),
                    (
                        "- RMS totale medio: "
                        f"**{markdown_value(row['average_rms_total_arcsec'])}″**"
                    ),
                    (
                        "- Frame: "
                        f"{row['light_completed']} completati, "
                        f"{row['light_failed']} falliti, "
                        f"{row['light_started']} avviati"
                    ),
                    (
                        "- Periodo: "
                        f"`{markdown_value(row['first_session_start'])}` – "
                        f"`{markdown_value(row['last_session_end'])}`"
                    ),
                    "",
                ]
            )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    sessions_path = repo_root / INPUT_RELATIVE_PATH
    registry_path = (
        repo_root
        / "data"
        / "analytics"
        / "configurations"
        / "equipment-registry.csv"
    )
    output_csv = repo_root / OUTPUT_CSV_RELATIVE_PATH
    output_md = repo_root / OUTPUT_MD_RELATIVE_PATH

    sessions = read_csv(sessions_path)
    registry = read_csv(registry_path)

    summary = build_summary(sessions, registry)

    write_csv(output_csv, summary)
    write_markdown(output_md, summary)

    print(f"Sessioni lette: {len(sessions)}")
    print(f"Configurazioni riepilogate: {len(summary)}")
    print(f"CSV: {output_csv}")
    print(f"Markdown: {output_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())