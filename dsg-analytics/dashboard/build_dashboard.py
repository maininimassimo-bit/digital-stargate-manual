#!/usr/bin/env python3
"""Digital StarGate Analytics v3.0 - Executive Observatory Dashboard."""
from __future__ import annotations

import argparse
import csv
import html
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parents[1]

SESSIONS_RELATIVE_PATH = Path("data/analytics/history/sessions.csv")
CONFIG_SUMMARY_RELATIVE_PATH = Path("data/analytics/history/configuration-summary.csv")
TARGETS_RELATIVE_PATH = Path("data/analytics/history/targets.csv")
OUTPUT_RELATIVE_PATH = Path("docs/analytics/dashboard.html")


def read_csv(path: Path, required: bool = True) -> List[Dict[str, str]]:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"File non trovato: {path}")
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def to_float(value: object) -> Optional[float]:
    if value in (None, ""):
        return None

    try:
        return float(str(value).strip().replace(",", "."))
    except ValueError:
        return None


def to_int(value: object) -> int:
    number = to_float(value)
    return 0 if number is None else int(round(number))


def fmt_number(value: float, digits: int = 1) -> str:
    if math.isclose(value, round(value), abs_tol=10 ** (-(digits + 1))):
        return f"{int(round(value)):,}".replace(",", ".")

    return (
        f"{value:,.{digits}f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def fmt_optional(
    value: Optional[float],
    digits: int = 1,
    suffix: str = "",
) -> str:
    return "—" if value is None else f"{fmt_number(value, digits)}{suffix}"


def parse_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def escape(value: object) -> str:
    return html.escape(str(value or ""))


def mean(values: List[float]) -> Optional[float]:
    return sum(values) / len(values) if values else None


def rate(success: int, failed: int) -> Optional[float]:
    total = success + failed
    return 100.0 * success / total if total else None


def first_value(row: Dict[str, str], *keys: str) -> str:
    for key in keys:
        value = str(row.get(key) or "").strip()
        if value:
            return value
    return ""


def aggregate_kpis(
    sessions: List[Dict[str, str]],
) -> Dict[str, Optional[float]]:
    durations = [
        value
        for row in sessions
        if (value := to_float(row.get("duration_hours"))) is not None
    ]
    integrations = [
        value
        for row in sessions
        if (value := to_float(row.get("integration_hours"))) is not None
    ]
    completion = [
        value
        for row in sessions
        if (value := to_float(row.get("completion_pct"))) is not None
    ]
    rms_values = [
        value
        for row in sessions
        if (value := to_float(row.get("rms_total_arcsec"))) is not None
    ]
    weather = [
        value
        for row in sessions
        if (value := to_float(row.get("weather_safe_pct"))) is not None
    ]

    total_duration = sum(durations)
    total_integration = sum(integrations)

    completed = sum(to_int(row.get("light_completed")) for row in sessions)
    failed = sum(to_int(row.get("light_failed")) for row in sessions)

    autofocus_count = sum(
        to_int(row.get("autofocus_count")) for row in sessions
    )
    autofocus_failed = sum(
        to_int(row.get("autofocus_failed")) for row in sessions
    )

    dither_count = sum(
        to_int(row.get("dither_count")) for row in sessions
    )
    dither_failed = sum(
        to_int(row.get("dither_failed")) for row in sessions
    )

    ok_sessions = sum(
        1
        for row in sessions
        if str(row.get("severity") or "").strip().upper()
        in {"OK", "SUCCESS", "PASSED", "INFO"}
    )

    return {
        "session_count": float(len(sessions)),
        "ok_sessions": float(ok_sessions),
        "total_duration": total_duration,
        "total_integration": total_integration,
        "integration_efficiency": (
            100.0 * total_integration / total_duration
            if total_duration
            else None
        ),
        "average_completion": mean(completion),
        "average_rms": mean(rms_values),
        "average_weather_safe": mean(weather),
        "light_completed": float(completed),
        "light_failed": float(failed),
        "light_success_rate": rate(completed, failed),
        "autofocus_count": float(autofocus_count),
        "autofocus_success_rate": rate(
            max(autofocus_count - autofocus_failed, 0),
            autofocus_failed,
        ),
        "dither_count": float(dither_count),
        "dither_success_rate": rate(
            max(dither_count - dither_failed, 0),
            dither_failed,
        ),
    }


def aggregate_targets(
    targets: List[Dict[str, str]],
) -> Dict[str, object]:
    by_target: Dict[str, Dict[str, object]] = defaultdict(
        lambda: {
            "hours": 0.0,
            "images": 0,
            "sessions": set(),
            "filters": set(),
            "last_timestamp": "",
        }
    )
    by_filter: Dict[str, Dict[str, object]] = defaultdict(
        lambda: {
            "hours": 0.0,
            "images": 0,
            "targets": set(),
        }
    )

    total_hours = 0.0
    total_images = 0
    sessions = set()

    for row in targets:
        target_name = first_value(
            row,
            "target_name",
            "target",
            "object_name",
        ) or "Senza nome"

        filter_name = first_value(
            row,
            "filter_name",
            "filter",
        ) or "Non specificato"

        session_id = first_value(
            row,
            "session_id",
            "session",
        )

        integration_hours = (
            to_float(row.get("integration_hours"))
            or (
                (to_float(row.get("integration_seconds")) or 0.0)
                / 3600.0
            )
        )
        image_count = to_int(
            first_value(
                row,
                "image_count",
                "images",
                "frame_count",
            )
        )
        last_timestamp = first_value(
            row,
            "last_timestamp",
            "last_image_timestamp",
            "session_end",
        )

        total_hours += integration_hours
        total_images += image_count

        if session_id:
            sessions.add(session_id)

        target_data = by_target[target_name]
        target_data["hours"] = float(target_data["hours"]) + integration_hours
        target_data["images"] = int(target_data["images"]) + image_count
        target_data["filters"].add(filter_name)

        if session_id:
            target_data["sessions"].add(session_id)

        if last_timestamp > str(target_data["last_timestamp"]):
            target_data["last_timestamp"] = last_timestamp

        filter_data = by_filter[filter_name]
        filter_data["hours"] = float(filter_data["hours"]) + integration_hours
        filter_data["images"] = int(filter_data["images"]) + image_count
        filter_data["targets"].add(target_name)

    ranking = sorted(
        (
            {
                "target": target_name,
                "hours": float(data["hours"]),
                "images": int(data["images"]),
                "sessions": len(data["sessions"]),
                "filters": ", ".join(sorted(data["filters"])),
                "last_timestamp": str(data["last_timestamp"]),
            }
            for target_name, data in by_target.items()
        ),
        key=lambda item: (
            float(item["hours"]),
            int(item["images"]),
            str(item["target"]),
        ),
        reverse=True,
    )

    filters = sorted(
        (
            {
                "filter": filter_name,
                "hours": float(data["hours"]),
                "images": int(data["images"]),
                "targets": len(data["targets"]),
            }
            for filter_name, data in by_filter.items()
        ),
        key=lambda item: (
            float(item["hours"]),
            int(item["images"]),
            str(item["filter"]),
        ),
        reverse=True,
    )

    top_target = ranking[0]["target"] if ranking else "—"
    top_filter = filters[0]["filter"] if filters else "—"

    latest_target = "—"
    latest_candidates = [
        item
        for item in ranking
        if str(item.get("last_timestamp") or "")
    ]
    if latest_candidates:
        latest_target = max(
            latest_candidates,
            key=lambda item: str(item["last_timestamp"]),
        )["target"]

    return {
        "target_count": len(by_target),
        "session_count": len(sessions),
        "total_hours": total_hours,
        "total_images": total_images,
        "top_target": top_target,
        "top_filter": top_filter,
        "latest_target": latest_target,
        "ranking": ranking,
        "filters": filters,
    }


def monthly_aggregation(
    sessions: List[Dict[str, str]],
) -> List[Tuple[str, int, float, float, Optional[float]]]:
    grouped = defaultdict(
        lambda: {
            "sessions": 0,
            "duration": 0.0,
            "integration": 0.0,
            "rms": [],
        }
    )

    for row in sessions:
        dt = parse_datetime(row.get("session_start", ""))
        if not dt:
            continue

        group = grouped[dt.strftime("%Y-%m")]
        group["sessions"] += 1
        group["duration"] += to_float(row.get("duration_hours")) or 0.0
        group["integration"] += (
            to_float(row.get("integration_hours")) or 0.0
        )

        rms_value = to_float(row.get("rms_total_arcsec"))
        if rms_value is not None:
            group["rms"].append(rms_value)

    result = []
    for key, group in sorted(grouped.items()):
        efficiency = (
            100.0 * group["integration"] / group["duration"]
            if group["duration"]
            else 0.0
        )
        result.append(
            (
                key,
                group["sessions"],
                group["integration"],
                efficiency,
                mean(group["rms"]),
            )
        )

    return result


def month_label(key: str) -> str:
    months = [
        "Gen",
        "Feb",
        "Mar",
        "Apr",
        "Mag",
        "Giu",
        "Lug",
        "Ago",
        "Set",
        "Ott",
        "Nov",
        "Dic",
    ]

    try:
        dt = datetime.strptime(key, "%Y-%m")
        return f"{months[dt.month - 1]} {dt.year}"
    except ValueError:
        return key


def build_monthly_chart(
    monthly: List[Tuple[str, int, float, float, Optional[float]]],
) -> str:
    if not monthly:
        return '<div class="empty">Nessun dato mensile disponibile.</div>'

    width = max(920, 120 * len(monthly))
    height = 360
    left = 60
    right = 30
    top = 34
    bottom = 86
    chart_width = width - left - right
    chart_height = height - top - bottom
    max_integration = max(
        max((item[2] for item in monthly), default=1.0),
        1.0,
    )
    slot = chart_width / len(monthly)
    bar_width = min(56.0, slot * 0.48)

    parts = [
        (
            f'<svg viewBox="0 0 {width} {height}" '
            'role="img" aria-label="Trend mensile">'
        ),
        (
            f'<line x1="{left}" y1="{top}" '
            f'x2="{left}" y2="{top + chart_height}" class="axis"/>'
        ),
        (
            f'<line x1="{left}" y1="{top + chart_height}" '
            f'x2="{width - right}" y2="{top + chart_height}" '
            'class="axis"/>'
        ),
    ]

    for index in range(5):
        value = max_integration * index / 4
        y = top + chart_height - chart_height * index / 4
        parts.append(
            (
                f'<line x1="{left}" y1="{y:.1f}" '
                f'x2="{width - right}" y2="{y:.1f}" class="grid"/>'
            )
        )
        parts.append(
            (
                f'<text x="{left - 8}" y="{y + 4:.1f}" '
                f'text-anchor="end" class="tick">'
                f"{fmt_number(value, 1)}</text>"
            )
        )

    points = []

    for index, (
        key,
        count,
        integration,
        efficiency,
        rms_value,
    ) in enumerate(monthly):
        center_x = left + slot * index + slot / 2
        x = center_x - bar_width / 2
        bar_height = chart_height * integration / max_integration
        y = top + chart_height - bar_height
        label = month_label(key)

        parts.append(
            (
                f'<rect x="{x:.1f}" y="{y:.1f}" '
                f'width="{bar_width:.1f}" height="{bar_height:.1f}" '
                'rx="7" class="bar">'
                f"<title>{escape(label)}: "
                f"{fmt_number(integration, 1)} h; "
                f"{count} sessioni; "
                f"efficienza {fmt_number(efficiency, 1)}%</title>"
                "</rect>"
            )
        )
        parts.append(
            (
                f'<text x="{center_x:.1f}" '
                f'y="{max(y - 8, 18):.1f}" '
                'text-anchor="middle" class="value">'
                f"{fmt_number(integration, 1)}h</text>"
            )
        )
        parts.append(
            (
                f'<text x="{center_x:.1f}" '
                f'y="{top + chart_height + 24}" '
                'text-anchor="middle" class="xlabel">'
                f"{escape(label)}</text>"
            )
        )
        parts.append(
            (
                f'<text x="{center_x:.1f}" '
                f'y="{top + chart_height + 44}" '
                'text-anchor="middle" class="subvalue">'
                f"{count} sessioni</text>"
            )
        )

        if rms_value is not None:
            parts.append(
                (
                    f'<text x="{center_x:.1f}" '
                    f'y="{top + chart_height + 62}" '
                    'text-anchor="middle" class="subvalue">'
                    f"RMS {fmt_number(rms_value, 2)}″</text>"
                )
            )

        efficiency_y = (
            top
            + chart_height
            - chart_height * min(max(efficiency, 0), 100) / 100
        )
        points.append((center_x, efficiency_y, efficiency))

    if len(points) > 1:
        parts.append(
            '<polyline points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points)
            + '" class="efficiency-line"/>'
        )

    for x, y, efficiency in points:
        parts.append(
            (
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" '
                'class="efficiency-point">'
                f"<title>Efficienza {fmt_number(efficiency, 1)}%</title>"
                "</circle>"
            )
        )

    parts.append("</svg>")
    return "".join(parts)


def configuration_rows(summary: List[Dict[str, str]]) -> str:
    if not summary:
        return (
            '<tr><td colspan="8" class="empty-cell">'
            "Nessuna configurazione disponibile."
            "</td></tr>"
        )

    rows = []
    ordered = sorted(
        summary,
        key=lambda row: (
            to_float(row.get("total_integration_hours")) or 0.0
        ),
        reverse=True,
    )

    for row in ordered:
        rows.append(
            "<tr>"
            f"<td><strong>{escape(row.get('configuration_name') or row.get('configuration_id'))}</strong>"
            f"<div class='muted mono'>{escape(row.get('configuration_id'))}</div></td>"
            f"<td>{escape(row.get('telescope')) or '—'}</td>"
            f"<td>{escape(row.get('camera')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('session_count')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('total_duration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('total_integration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('integration_efficiency_pct')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('average_rms_total_arcsec')) or '—'}</td>"
            "</tr>"
        )

    return "".join(rows)


def recent_session_rows(
    sessions: List[Dict[str, str]],
    limit: int = 12,
) -> str:
    ordered = sorted(
        sessions,
        key=lambda row: (
            row.get("session_start", ""),
            row.get("session_id", ""),
        ),
        reverse=True,
    )[:limit]

    if not ordered:
        return (
            '<tr><td colspan="10" class="empty-cell">'
            "Nessuna sessione disponibile."
            "</td></tr>"
        )

    rows = []

    for row in ordered:
        severity = str(row.get("severity") or "").strip()
        upper = severity.upper()

        if upper in {"OK", "SUCCESS", "PASSED", "INFO"}:
            css_class = "status-good"
        elif upper in {"WARNING", "WARN", "DEGRADED", "PARTIAL"}:
            css_class = "status-warn"
        elif severity:
            css_class = "status-bad"
        else:
            css_class = "status-neutral"

        rows.append(
            "<tr>"
            f"<td class='mono'>{escape(row.get('session_id'))}</td>"
            f"<td>{escape(row.get('configuration_id')) or '—'}</td>"
            f"<td>{escape(row.get('session_start')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('duration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('integration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('completion_pct')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('rms_total_arcsec')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('weather_safe_pct')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('autofocus_count')) or '—'}</td>"
            f"<td><span class='status {css_class}'>"
            f"{escape(severity) or '—'}</span></td>"
            "</tr>"
        )

    return "".join(rows)


def target_rows(target_metrics: Dict[str, object]) -> str:
    ranking = target_metrics.get("ranking") or []
    if not ranking:
        return (
            '<tr><td colspan="6" class="empty-cell">'
            "Nessun target disponibile."
            "</td></tr>"
        )

    rows = []

    for index, item in enumerate(ranking, start=1):
        rows.append(
            "<tr>"
            f"<td class='rank'>{index}</td>"
            f"<td><strong>{escape(item['target'])}</strong></td>"
            f"<td>{escape(item['filters']) or '—'}</td>"
            f"<td class='num'>{fmt_number(float(item['hours']), 2)}</td>"
            f"<td class='num'>{fmt_number(float(item['images']), 0)}</td>"
            f"<td class='num'>{fmt_number(float(item['sessions']), 0)}</td>"
            "</tr>"
        )

    return "".join(rows)


def build_filter_chart(target_metrics: Dict[str, object]) -> str:
    filters = target_metrics.get("filters") or []
    if not filters:
        return '<div class="empty">Nessun dato filtro disponibile.</div>'

    max_hours = max(
        float(item["hours"])
        for item in filters
    ) or 1.0

    parts = ['<div class="filter-bars">']

    for item in filters:
        hours = float(item["hours"])
        width = max(2.0, 100.0 * hours / max_hours)

        parts.append(
            '<div class="filter-row">'
            '<div class="filter-heading">'
            f"<strong>{escape(item['filter'])}</strong>"
            f"<span>{fmt_number(hours, 2)} h · "
            f"{fmt_number(float(item['images']), 0)} immagini · "
            f"{fmt_number(float(item['targets']), 0)} target</span>"
            "</div>"
            '<div class="bar-track">'
            f'<div class="bar-fill" style="width:{width:.2f}%"></div>'
            "</div>"
            "</div>"
        )

    parts.append("</div>")
    return "".join(parts)


def target_summary_cards(target_metrics: Dict[str, object]) -> str:
    return "".join(
        [
            card(
                "Target distinti",
                fmt_number(
                    float(target_metrics.get("target_count") or 0),
                    0,
                ),
                "oggetti astronomici consolidati",
            ),
            card(
                "Immagini target",
                fmt_number(
                    float(target_metrics.get("total_images") or 0),
                    0,
                ),
                "frame associati ai target",
            ),
            card(
                "Integrazione target",
                fmt_optional(
                    float(target_metrics.get("total_hours") or 0),
                    2,
                    " h",
                ),
                "tempo utile ricostruito dai log NINA",
            ),
            card(
                "Sessioni target",
                fmt_number(
                    float(target_metrics.get("session_count") or 0),
                    0,
                ),
                "sessioni con target riconosciuto",
            ),
            card(
                "Target principale",
                escape(target_metrics.get("top_target") or "—"),
                "primo per ore di integrazione",
            ),
            card(
                "Filtro principale",
                escape(target_metrics.get("top_filter") or "—"),
                "primo per ore di utilizzo",
            ),
            card(
                "Ultimo target",
                escape(target_metrics.get("latest_target") or "—"),
                "ultimo oggetto acquisito",
            ),
        ]
    )


def card(label: str, value: str, note: str) -> str:
    return (
        '<article class="card">'
        f'<div class="kpi-label">{escape(label)}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-note">{escape(note)}</div>'
        "</article>"
    )


def render_dashboard(
    sessions: List[Dict[str, str]],
    summary: List[Dict[str, str]],
    targets: List[Dict[str, str]],
) -> str:
    session_kpis = aggregate_kpis(sessions)
    target_metrics = aggregate_targets(targets)
    monthly = monthly_aggregation(sessions)
    generated = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )

    session_cards = "".join(
        [
            card(
                "Sessioni",
                str(int(session_kpis["session_count"] or 0)),
                "sessioni consolidate",
            ),
            card(
                "Durata totale",
                fmt_optional(
                    session_kpis["total_duration"],
                    1,
                    " h",
                ),
                "tempo complessivo di osservazione",
            ),
            card(
                "Integrazione sessioni",
                fmt_optional(
                    session_kpis["total_integration"],
                    1,
                    " h",
                ),
                "tempo utile acquisito",
            ),
            card(
                "Efficienza",
                fmt_optional(
                    session_kpis["integration_efficiency"],
                    1,
                    "%",
                ),
                "integrazione / durata",
            ),
            card(
                "Completamento medio",
                fmt_optional(
                    session_kpis["average_completion"],
                    1,
                    "%",
                ),
                "media delle sessioni",
            ),
            card(
                "RMS medio",
                fmt_optional(
                    session_kpis["average_rms"],
                    2,
                    "″",
                ),
                "qualità media della guida",
            ),
            card(
                "Successo frame",
                fmt_optional(
                    session_kpis["light_success_rate"],
                    1,
                    "%",
                ),
                (
                    f"{fmt_number(session_kpis['light_completed'] or 0, 0)} "
                    "completati · "
                    f"{fmt_number(session_kpis['light_failed'] or 0, 0)} "
                    "falliti"
                ),
            ),
            card(
                "Meteo sicuro medio",
                fmt_optional(
                    session_kpis["average_weather_safe"],
                    1,
                    "%",
                ),
                "disponibilità condizioni sicure",
            ),
            card(
                "Autofocus",
                fmt_number(
                    session_kpis["autofocus_count"] or 0,
                    0,
                ),
                (
                    "successo "
                    f"{fmt_optional(session_kpis['autofocus_success_rate'], 1, '%')}"
                ),
            ),
            card(
                "Dithering",
                fmt_number(
                    session_kpis["dither_count"] or 0,
                    0,
                ),
                (
                    "successo "
                    f"{fmt_optional(session_kpis['dither_success_rate'], 1, '%')}"
                ),
            ),
            card(
                "Sessioni OK",
                fmt_number(
                    session_kpis["ok_sessions"] or 0,
                    0,
                ),
                "stato positivo esplicito",
            ),
            card(
                "Configurazioni",
                str(len(summary)),
                "profili strumentali consolidati",
            ),
        ]
    )

    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Digital StarGate Analytics</title>
<style>
:root {{
  --bg:#07111f;
  --panel:#0d1b2d;
  --panel2:#10243d;
  --text:#eef5ff;
  --muted:#9fb2ca;
  --accent:#58a6ff;
  --accent2:#8bd5ff;
  --border:#233a58;
  --good:#57d18c;
  --warn:#ffc857;
  --bad:#ff6b6b;
  color-scheme:dark;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0;
  font-family:Inter,Segoe UI,Arial,sans-serif;
  background:
    radial-gradient(
      circle at top right,
      rgba(88,166,255,.12),
      transparent 34rem
    ),
    var(--bg);
  color:var(--text);
}}
.container {{
  width:min(1480px,calc(100% - 32px));
  margin:0 auto;
}}
header {{ padding:44px 0 24px; }}
.eyebrow {{
  color:var(--accent2);
  text-transform:uppercase;
  letter-spacing:.16em;
  font-size:.78rem;
  font-weight:700;
}}
h1 {{
  margin:8px 0 6px;
  font-size:clamp(2rem,5vw,4rem);
  line-height:1;
}}
.subtitle,
.section-intro,
.muted {{
  color:var(--muted);
}}
.subtitle {{ max-width:980px; }}
.section-label {{
  margin:32px 0 12px;
  color:var(--accent2);
  text-transform:uppercase;
  letter-spacing:.12em;
  font-size:.75rem;
  font-weight:800;
}}
.kpi-grid {{
  display:grid;
  grid-template-columns:repeat(4,minmax(0,1fr));
  gap:16px;
  margin:16px 0 22px;
}}
.card {{
  background:
    linear-gradient(
      180deg,
      rgba(16,36,61,.98),
      rgba(13,27,45,.98)
    );
  border:1px solid var(--border);
  border-radius:18px;
  padding:20px;
  box-shadow:0 14px 40px rgba(0,0,0,.18);
}}
.kpi-label {{
  color:var(--muted);
  font-size:.88rem;
}}
.kpi-value {{
  margin-top:8px;
  font-size:clamp(1.6rem,4vw,2.5rem);
  font-weight:750;
  overflow-wrap:anywhere;
}}
.kpi-note {{
  margin-top:4px;
  color:var(--muted);
  font-size:.78rem;
}}
.section {{ margin:24px 0; }}
.section h2 {{
  margin:0 0 6px;
  font-size:1.3rem;
}}
.section-intro {{
  margin:0 0 16px;
  font-size:.9rem;
}}
.chart,
.table-wrap {{
  overflow-x:auto;
}}
svg {{
  width:100%;
  min-width:760px;
  height:auto;
}}
.axis {{ stroke:#6f88a6; }}
.grid {{ stroke:#223954; }}
.bar {{ fill:var(--accent); }}
.efficiency-line {{
  fill:none;
  stroke:var(--good);
  stroke-width:3;
}}
.efficiency-point {{
  fill:var(--good);
  stroke:var(--panel);
  stroke-width:2;
}}
.tick,
.xlabel {{
  fill:var(--muted);
  font-size:12px;
}}
.value {{
  fill:var(--text);
  font-size:12px;
  font-weight:700;
}}
.subvalue {{
  fill:var(--muted);
  font-size:11px;
}}
.split-grid {{
  display:grid;
  grid-template-columns:minmax(0,1.55fr) minmax(320px,.75fr);
  gap:16px;
}}
.filter-bars {{
  display:flex;
  flex-direction:column;
  gap:18px;
  padding:6px 0;
}}
.filter-heading {{
  display:flex;
  justify-content:space-between;
  gap:16px;
  color:var(--text);
  font-size:.9rem;
}}
.filter-heading span {{
  color:var(--muted);
  font-size:.8rem;
  text-align:right;
}}
.bar-track {{
  height:12px;
  background:rgba(159,178,202,.10);
  border:1px solid var(--border);
  border-radius:999px;
  margin-top:8px;
  overflow:hidden;
}}
.bar-fill {{
  height:100%;
  background:linear-gradient(
    90deg,
    var(--accent),
    var(--accent2)
  );
  border-radius:999px;
}}
table {{
  width:100%;
  border-collapse:collapse;
  min-width:1080px;
}}
th,
td {{
  padding:13px 12px;
  border-bottom:1px solid var(--border);
  text-align:left;
}}
th {{
  color:var(--muted);
  font-size:.78rem;
  text-transform:uppercase;
  letter-spacing:.07em;
}}
td {{ font-size:.9rem; }}
.num {{
  text-align:right;
  font-variant-numeric:tabular-nums;
}}
.rank {{
  width:46px;
  color:var(--accent2);
  font-weight:800;
  text-align:center;
}}
.muted {{
  font-size:.78rem;
  margin-top:4px;
}}
.mono {{
  font-family:Consolas,"Courier New",monospace;
}}
.empty,
.empty-cell {{
  color:var(--muted);
  padding:24px;
  text-align:center;
}}
.status {{
  display:inline-block;
  padding:4px 9px;
  border-radius:999px;
  font-size:.74rem;
  font-weight:700;
}}
.status-good {{
  color:var(--good);
  background:rgba(87,209,140,.12);
}}
.status-warn {{
  color:var(--warn);
  background:rgba(255,200,87,.12);
}}
.status-bad {{
  color:var(--bad);
  background:rgba(255,107,107,.12);
}}
.status-neutral {{
  color:var(--muted);
  background:rgba(159,178,202,.10);
}}
footer {{
  color:var(--muted);
  padding:18px 0 40px;
  font-size:.78rem;
}}
@media(max-width:1100px) {{
  .split-grid {{
    grid-template-columns:1fr;
  }}
}}
@media(max-width:1000px) {{
  .kpi-grid {{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }}
}}
@media(max-width:560px) {{
  .container {{
    width:min(100% - 20px,1480px);
  }}
  .kpi-grid {{
    grid-template-columns:1fr;
  }}
  header {{
    padding-top:28px;
  }}
  .filter-heading {{
    flex-direction:column;
  }}
  .filter-heading span {{
    text-align:left;
  }}
}}
</style>
</head>
<body>
<div class="container">
<header>
  <div class="eyebrow">Digital StarGate Observatory</div>
  <h1>Executive Observatory Dashboard</h1>
  <div class="subtitle">
    Sintesi operativa delle sessioni, dei target osservati,
    dell'efficienza di acquisizione, della qualità di guida
    e dell'affidabilità dei processi automatici.
  </div>
</header>

<div class="section-label">Session Analytics</div>
<section class="kpi-grid">
{session_cards}
</section>

<section class="section card">
  <h2>Trend mensile</h2>
  <p class="section-intro">
    Le barre indicano le ore di integrazione; la linea verde
    rappresenta l'efficienza mensile. Sotto ogni mese sono
    riportati sessioni e RMS.
  </p>
  <div class="chart">{build_monthly_chart(monthly)}</div>
</section>

<div class="section-label">Target Analytics</div>
<section class="kpi-grid">
{target_summary_cards(target_metrics)}
</section>

<section class="section split-grid">
  <article class="card">
    <h2>Classifica target</h2>
    <p class="section-intro">
      Ordinamento per ore complessive di integrazione.
    </p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Target</th>
            <th>Filtri</th>
            <th class="num">Integrazione h</th>
            <th class="num">Immagini</th>
            <th class="num">Sessioni</th>
          </tr>
        </thead>
        <tbody>
          {target_rows(target_metrics)}
        </tbody>
      </table>
    </div>
  </article>

  <article class="card">
    <h2>Distribuzione filtri</h2>
    <p class="section-intro">
      Ore di integrazione e immagini per filtro.
    </p>
    {build_filter_chart(target_metrics)}
  </article>
</section>

<div class="section-label">Configuration Analytics</div>
<section class="section card">
  <h2>Prestazioni per configurazione</h2>
  <p class="section-intro">
    Ordinamento per integrazione totale prodotta.
  </p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Configurazione</th>
          <th>Telescopio</th>
          <th>Camera</th>
          <th class="num">Sessioni</th>
          <th class="num">Durata h</th>
          <th class="num">Integrazione h</th>
          <th class="num">Efficienza %</th>
          <th class="num">RMS ″</th>
        </tr>
      </thead>
      <tbody>
        {configuration_rows(summary)}
      </tbody>
    </table>
  </div>
</section>

<div class="section-label">Operational Detail</div>
<section class="section card">
  <h2>Ultime sessioni</h2>
  <p class="section-intro">
    Dettaglio operativo delle 12 sessioni più recenti.
  </p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Sessione</th>
          <th>Configurazione</th>
          <th>Inizio</th>
          <th class="num">Durata h</th>
          <th class="num">Integrazione h</th>
          <th class="num">Completamento %</th>
          <th class="num">RMS ″</th>
          <th class="num">Meteo %</th>
          <th class="num">Autofocus</th>
          <th>Stato</th>
        </tr>
      </thead>
      <tbody>
        {recent_session_rows(sessions)}
      </tbody>
    </table>
  </div>
</section>

<footer>
  Generato automaticamente il {escape(generated)}
  · Digital StarGate Analytics v3.0
</footer>
</div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Genera la dashboard executive "
            "Digital StarGate Analytics v3.0."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
    )
    parser.add_argument(
        "--output",
        type=Path,
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    sessions = read_csv(
        repo_root / SESSIONS_RELATIVE_PATH,
        required=True,
    )
    summary = read_csv(
        repo_root / CONFIG_SUMMARY_RELATIVE_PATH,
        required=True,
    )
    targets = read_csv(
        repo_root / TARGETS_RELATIVE_PATH,
        required=False,
    )

    output_path = (
        args.output.resolve()
        if args.output
        else repo_root / OUTPUT_RELATIVE_PATH
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_dashboard(sessions, summary, targets),
        encoding="utf-8",
    )

    print(f"Sessioni lette: {len(sessions)}")
    print(f"Configurazioni lette: {len(summary)}")
    print(f"Righe target lette: {len(targets)}")
    print(f"Dashboard v3.0: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
