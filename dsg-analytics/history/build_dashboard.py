#!/usr/bin/env python3
"""Digital StarGate Analytics v2.4 - generate a self-contained HTML dashboard."""

from __future__ import annotations

import argparse
import csv
import html
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parents[1]

SESSIONS_RELATIVE_PATH = Path("data/analytics/history/sessions.csv")
CONFIG_SUMMARY_RELATIVE_PATH = Path("data/analytics/history/configuration-summary.csv")
OUTPUT_RELATIVE_PATH = Path("docs/analytics/dashboard.html")


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"File non trovato: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def to_float(value: object) -> Optional[float]:
    if value in (None, ""):
        return None
    try:
        return float(str(value).strip().replace(",", "."))
    except ValueError:
        return None


def to_int(value: object) -> Optional[int]:
    number = to_float(value)
    return None if number is None else int(round(number))


def fmt_number(value: float, digits: int = 1) -> str:
    if math.isclose(value, round(value), abs_tol=10 ** (-(digits + 1))):
        return f"{int(round(value)):,}".replace(",", ".")
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_optional(value: Optional[float], digits: int = 1, suffix: str = "") -> str:
    if value is None:
        return "—"
    return f"{fmt_number(value, digits)}{suffix}"


def parse_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def escape(value: object) -> str:
    return html.escape(str(value or ""))


def aggregate_kpis(sessions: List[Dict[str, str]]) -> Dict[str, Optional[float]]:
    durations = [v for row in sessions if (v := to_float(row.get("duration_hours"))) is not None]
    integrations = [v for row in sessions if (v := to_float(row.get("integration_hours"))) is not None]
    completion = [v for row in sessions if (v := to_float(row.get("completion_pct"))) is not None]
    rms = [v for row in sessions if (v := to_float(row.get("rms_total_arcsec"))) is not None]

    total_duration = sum(durations)
    total_integration = sum(integrations)

    return {
        "session_count": float(len(sessions)),
        "total_duration": total_duration,
        "total_integration": total_integration,
        "integration_efficiency": (
            100.0 * total_integration / total_duration if total_duration > 0 else None
        ),
        "average_completion": sum(completion) / len(completion) if completion else None,
        "average_rms": sum(rms) / len(rms) if rms else None,
        "light_completed": float(sum(to_int(row.get("light_completed")) or 0 for row in sessions)),
        "light_failed": float(sum(to_int(row.get("light_failed")) or 0 for row in sessions)),
    }


def monthly_aggregation(sessions: List[Dict[str, str]]) -> List[Tuple[str, int, float]]:
    grouped: Dict[str, Dict[str, float]] = defaultdict(lambda: {"sessions": 0.0, "integration": 0.0})

    for row in sessions:
        dt = parse_datetime(row.get("session_start", ""))
        if not dt:
            continue
        key = dt.strftime("%Y-%m")
        grouped[key]["sessions"] += 1
        grouped[key]["integration"] += to_float(row.get("integration_hours")) or 0.0

    return [
        (key, int(values["sessions"]), values["integration"])
        for key, values in sorted(grouped.items())
    ]


def month_label(key: str) -> str:
    try:
        dt = datetime.strptime(key, "%Y-%m")
        months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                  "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        return f"{months[dt.month - 1]} {dt.year}"
    except ValueError:
        return key


def build_bar_chart(monthly: List[Tuple[str, int, float]]) -> str:
    if not monthly:
        return '<div class="empty">Nessun dato mensile disponibile.</div>'

    width = 900
    height = 320
    pad_left = 56
    pad_right = 20
    pad_top = 24
    pad_bottom = 70
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom
    max_value = max((integration for _, _, integration in monthly), default=0.0)
    max_value = max(max_value, 1.0)
    slot = chart_w / len(monthly)
    bar_w = min(54.0, slot * 0.58)

    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Ore di integrazione per mese">',
        '<line x1="56" y1="24" x2="56" y2="250" class="axis"/>',
        '<line x1="56" y1="250" x2="880" y2="250" class="axis"/>',
    ]

    for i in range(5):
        value = max_value * i / 4
        y = pad_top + chart_h - chart_h * i / 4
        parts.append(f'<line x1="{pad_left}" y1="{y:.1f}" x2="{width-pad_right}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{pad_left-8}" y="{y+4:.1f}" text-anchor="end" class="tick">{fmt_number(value,1)}</text>')

    for index, (key, sessions_count, integration) in enumerate(monthly):
        x = pad_left + slot * index + (slot - bar_w) / 2
        h = chart_h * integration / max_value
        y = pad_top + chart_h - h
        label = month_label(key)
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" '
            f'rx="7" class="bar"><title>{escape(label)}: {fmt_number(integration,1)} h, '
            f'{sessions_count} sessioni</title></rect>'
        )
        parts.append(
            f'<text x="{x + bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" class="value">'
            f'{fmt_number(integration,1)}h</text>'
        )
        parts.append(
            f'<text x="{x + bar_w/2:.1f}" y="{pad_top+chart_h+24}" '
            f'text-anchor="middle" class="xlabel">{escape(label)}</text>'
        )

    parts.append('</svg>')
    return "".join(parts)


def configuration_rows(summary: List[Dict[str, str]]) -> str:
    if not summary:
        return '<tr><td colspan="8" class="empty-cell">Nessuna configurazione disponibile.</td></tr>'

    rows = []
    for row in summary:
        rows.append(
            "<tr>"
            f"<td><strong>{escape(row.get('configuration_name') or row.get('configuration_id'))}</strong>"
            f"<div class='muted mono'>{escape(row.get('configuration_id'))}</div></td>"
            f"<td>{escape(row.get('telescope'))}</td>"
            f"<td>{escape(row.get('camera'))}</td>"
            f"<td class='num'>{escape(row.get('session_count'))}</td>"
            f"<td class='num'>{escape(row.get('total_duration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('total_integration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('integration_efficiency_pct')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('average_rms_total_arcsec')) or '—'}</td>"
            "</tr>"
        )
    return "".join(rows)


def recent_session_rows(sessions: List[Dict[str, str]], limit: int = 10) -> str:
    sorted_sessions = sorted(
        sessions,
        key=lambda row: (row.get("session_start", ""), row.get("session_id", "")),
        reverse=True,
    )[:limit]

    if not sorted_sessions:
        return '<tr><td colspan="8" class="empty-cell">Nessuna sessione disponibile.</td></tr>'

    rows = []
    for row in sorted_sessions:
        rows.append(
            "<tr>"
            f"<td class='mono'>{escape(row.get('session_id'))}</td>"
            f"<td>{escape(row.get('configuration_id'))}</td>"
            f"<td>{escape(row.get('session_start'))}</td>"
            f"<td class='num'>{escape(row.get('duration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('integration_hours')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('completion_pct')) or '—'}</td>"
            f"<td class='num'>{escape(row.get('rms_total_arcsec')) or '—'}</td>"
            f"<td>{escape(row.get('severity')) or '—'}</td>"
            "</tr>"
        )
    return "".join(rows)


def render_dashboard(
    sessions: List[Dict[str, str]],
    configuration_summary: List[Dict[str, str]],
) -> str:
    kpis = aggregate_kpis(sessions)
    monthly = monthly_aggregation(sessions)
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Digital StarGate Analytics</title>
<style>
:root {{
  color-scheme: dark;
  --bg: #07111f;
  --panel: #0d1b2d;
  --panel-2: #10243d;
  --text: #eef5ff;
  --muted: #9fb2ca;
  --accent: #58a6ff;
  --accent-2: #8bd5ff;
  --border: #233a58;
  --good: #57d18c;
  --warn: #ffc857;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: Inter, Segoe UI, Arial, sans-serif;
  background:
    radial-gradient(circle at top right, rgba(88,166,255,.12), transparent 34rem),
    var(--bg);
  color: var(--text);
}}
.container {{ width: min(1400px, calc(100% - 32px)); margin: 0 auto; }}
header {{ padding: 44px 0 24px; }}
.eyebrow {{ color: var(--accent-2); text-transform: uppercase; letter-spacing: .16em; font-size: .78rem; font-weight: 700; }}
h1 {{ margin: 8px 0 6px; font-size: clamp(2rem, 5vw, 4rem); line-height: 1; }}
.subtitle {{ color: var(--muted); max-width: 760px; }}
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(4, minmax(0,1fr));
  gap: 16px;
  margin: 22px 0;
}}
.card {{
  background: linear-gradient(180deg, rgba(16,36,61,.98), rgba(13,27,45,.98));
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 14px 40px rgba(0,0,0,.18);
}}
.kpi-label {{ color: var(--muted); font-size: .88rem; }}
.kpi-value {{ margin-top: 8px; font-size: clamp(1.6rem, 4vw, 2.5rem); font-weight: 750; }}
.kpi-note {{ margin-top: 4px; color: var(--muted); font-size: .78rem; }}
.section {{ margin: 24px 0; }}
.section h2 {{ margin: 0 0 14px; font-size: 1.3rem; }}
.chart {{ overflow-x: auto; }}
svg {{ width: 100%; min-width: 720px; height: auto; }}
.axis {{ stroke: #6f88a6; stroke-width: 1; }}
.grid {{ stroke: #223954; stroke-width: 1; }}
.bar {{ fill: var(--accent); }}
.tick,.xlabel {{ fill: var(--muted); font-size: 12px; }}
.value {{ fill: var(--text); font-size: 12px; font-weight: 700; }}
.table-wrap {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; min-width: 980px; }}
th, td {{ padding: 13px 12px; border-bottom: 1px solid var(--border); text-align: left; }}
th {{ color: var(--muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .07em; }}
td {{ font-size: .9rem; }}
.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
.muted {{ color: var(--muted); font-size: .78rem; margin-top: 4px; }}
.mono {{ font-family: Consolas, "Courier New", monospace; }}
.empty, .empty-cell {{ color: var(--muted); padding: 24px; text-align: center; }}
footer {{ color: var(--muted); padding: 18px 0 40px; font-size: .78rem; }}
@media (max-width: 1000px) {{
  .kpi-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
}}
@media (max-width: 560px) {{
  .container {{ width: min(100% - 20px, 1400px); }}
  .kpi-grid {{ grid-template-columns: 1fr; }}
  header {{ padding-top: 28px; }}
}}
</style>
</head>
<body>
<div class="container">
<header>
  <div class="eyebrow">Digital StarGate Observatory</div>
  <h1>Analytics Dashboard</h1>
  <div class="subtitle">Sintesi operativa dello storico delle sessioni e delle configurazioni di acquisizione.</div>
</header>

<section class="kpi-grid">
  <article class="card">
    <div class="kpi-label">Sessioni</div>
    <div class="kpi-value">{int(kpis['session_count'] or 0)}</div>
    <div class="kpi-note">sessioni consolidate</div>
  </article>
  <article class="card">
    <div class="kpi-label">Durata totale</div>
    <div class="kpi-value">{fmt_optional(kpis['total_duration'], 1, ' h')}</div>
    <div class="kpi-note">tempo complessivo di sessione</div>
  </article>
  <article class="card">
    <div class="kpi-label">Integrazione</div>
    <div class="kpi-value">{fmt_optional(kpis['total_integration'], 1, ' h')}</div>
    <div class="kpi-note">tempo utile acquisito</div>
  </article>
  <article class="card">
    <div class="kpi-label">Efficienza</div>
    <div class="kpi-value">{fmt_optional(kpis['integration_efficiency'], 1, '%')}</div>
    <div class="kpi-note">integrazione / durata</div>
  </article>
  <article class="card">
    <div class="kpi-label">Completamento medio</div>
    <div class="kpi-value">{fmt_optional(kpis['average_completion'], 1, '%')}</div>
    <div class="kpi-note">media delle sessioni</div>
  </article>
  <article class="card">
    <div class="kpi-label">RMS medio</div>
    <div class="kpi-value">{fmt_optional(kpis['average_rms'], 2, '″')}</div>
    <div class="kpi-note">guida totale</div>
  </article>
  <article class="card">
    <div class="kpi-label">Frame completati</div>
    <div class="kpi-value">{fmt_number(kpis['light_completed'] or 0, 0)}</div>
    <div class="kpi-note">light completati</div>
  </article>
  <article class="card">
    <div class="kpi-label">Frame falliti</div>
    <div class="kpi-value">{fmt_number(kpis['light_failed'] or 0, 0)}</div>
    <div class="kpi-note">light non completati</div>
  </article>
</section>

<section class="section card">
  <h2>Andamento mensile dell'integrazione</h2>
  <div class="chart">{build_bar_chart(monthly)}</div>
</section>

<section class="section card">
  <h2>Prestazioni per configurazione</h2>
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
      <tbody>{configuration_rows(configuration_summary)}</tbody>
    </table>
  </div>
</section>

<section class="section card">
  <h2>Ultime sessioni</h2>
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
          <th>Stato</th>
        </tr>
      </thead>
      <tbody>{recent_session_rows(sessions)}</tbody>
    </table>
  </div>
</section>

<footer>Generato automaticamente il {escape(generated)} · Digital StarGate Analytics v2.4</footer>
</div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    sessions_path = repo_root / SESSIONS_RELATIVE_PATH
    summary_path = repo_root / CONFIG_SUMMARY_RELATIVE_PATH
    output_path = args.output.resolve() if args.output else repo_root / OUTPUT_RELATIVE_PATH

    sessions = read_csv(sessions_path)
    configuration_summary = read_csv(summary_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_dashboard(sessions, configuration_summary),
        encoding="utf-8",
    )

    print(f"Sessioni lette: {len(sessions)}")
    print(f"Configurazioni lette: {len(configuration_summary)}")
    print(f"Dashboard: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
