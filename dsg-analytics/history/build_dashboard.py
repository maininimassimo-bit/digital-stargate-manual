#!/usr/bin/env python3
"""Digital StarGate Analytics v2.7 - Executive Dashboard."""
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
SESSIONS_RELATIVE_PATH = Path('data/analytics/history/sessions.csv')
CONFIG_SUMMARY_RELATIVE_PATH = Path('data/analytics/history/configuration-summary.csv')
OUTPUT_RELATIVE_PATH = Path('docs/analytics/dashboard.html')


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f'File non trovato: {path}')
    with path.open('r', encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def to_float(value: object) -> Optional[float]:
    if value in (None, ''):
        return None
    try:
        return float(str(value).strip().replace(',', '.'))
    except ValueError:
        return None


def to_int(value: object) -> int:
    number = to_float(value)
    return 0 if number is None else int(round(number))


def fmt_number(value: float, digits: int = 1) -> str:
    if math.isclose(value, round(value), abs_tol=10 ** (-(digits + 1))):
        return f'{int(round(value)):,}'.replace(',', '.')
    return f'{value:,.{digits}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def fmt_optional(value: Optional[float], digits: int = 1, suffix: str = '') -> str:
    return '—' if value is None else f'{fmt_number(value, digits)}{suffix}'


def parse_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def escape(value: object) -> str:
    return html.escape(str(value or ''))


def mean(values: List[float]) -> Optional[float]:
    return sum(values) / len(values) if values else None


def rate(success: int, failed: int) -> Optional[float]:
    total = success + failed
    return 100.0 * success / total if total else None


def aggregate_kpis(sessions: List[Dict[str, str]]) -> Dict[str, Optional[float]]:
    durations = [v for r in sessions if (v := to_float(r.get('duration_hours'))) is not None]
    integrations = [v for r in sessions if (v := to_float(r.get('integration_hours'))) is not None]
    completion = [v for r in sessions if (v := to_float(r.get('completion_pct'))) is not None]
    rms = [v for r in sessions if (v := to_float(r.get('rms_total_arcsec'))) is not None]
    weather = [v for r in sessions if (v := to_float(r.get('weather_safe_pct'))) is not None]
    total_duration = sum(durations)
    total_integration = sum(integrations)
    completed = sum(to_int(r.get('light_completed')) for r in sessions)
    failed = sum(to_int(r.get('light_failed')) for r in sessions)
    af_count = sum(to_int(r.get('autofocus_count')) for r in sessions)
    af_failed = sum(to_int(r.get('autofocus_failed')) for r in sessions)
    dither_count = sum(to_int(r.get('dither_count')) for r in sessions)
    dither_failed = sum(to_int(r.get('dither_failed')) for r in sessions)
    ok_sessions = sum(1 for r in sessions if str(r.get('severity') or '').strip().upper() in {'OK','SUCCESS','PASSED','INFO'})
    return {
        'session_count': float(len(sessions)),
        'ok_sessions': float(ok_sessions),
        'total_duration': total_duration,
        'total_integration': total_integration,
        'integration_efficiency': 100.0 * total_integration / total_duration if total_duration else None,
        'average_completion': mean(completion),
        'average_rms': mean(rms),
        'average_weather_safe': mean(weather),
        'light_completed': float(completed),
        'light_failed': float(failed),
        'light_success_rate': rate(completed, failed),
        'autofocus_count': float(af_count),
        'autofocus_success_rate': rate(max(af_count - af_failed, 0), af_failed),
        'dither_count': float(dither_count),
        'dither_success_rate': rate(max(dither_count - dither_failed, 0), dither_failed),
    }


def monthly_aggregation(sessions: List[Dict[str, str]]) -> List[Tuple[str, int, float, float, Optional[float]]]:
    grouped = defaultdict(lambda: {'sessions': 0, 'duration': 0.0, 'integration': 0.0, 'rms': []})
    for row in sessions:
        dt = parse_datetime(row.get('session_start', ''))
        if not dt:
            continue
        group = grouped[dt.strftime('%Y-%m')]
        group['sessions'] += 1
        group['duration'] += to_float(row.get('duration_hours')) or 0.0
        group['integration'] += to_float(row.get('integration_hours')) or 0.0
        rms = to_float(row.get('rms_total_arcsec'))
        if rms is not None:
            group['rms'].append(rms)
    result = []
    for key, group in sorted(grouped.items()):
        efficiency = 100.0 * group['integration'] / group['duration'] if group['duration'] else 0.0
        result.append((key, group['sessions'], group['integration'], efficiency, mean(group['rms'])))
    return result


def month_label(key: str) -> str:
    months = ['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic']
    try:
        dt = datetime.strptime(key, '%Y-%m')
        return f'{months[dt.month - 1]} {dt.year}'
    except ValueError:
        return key


def build_monthly_chart(monthly: List[Tuple[str, int, float, float, Optional[float]]]) -> str:
    if not monthly:
        return '<div class="empty">Nessun dato mensile disponibile.</div>'
    width = max(920, 120 * len(monthly))
    height, left, right, top, bottom = 360, 60, 30, 34, 86
    chart_w, chart_h = width-left-right, height-top-bottom
    max_int = max(max((x[2] for x in monthly), default=1.0), 1.0)
    slot = chart_w / len(monthly)
    bar_w = min(56.0, slot * .48)
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Trend mensile">']
    parts += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+chart_h}" class="axis"/>',
              f'<line x1="{left}" y1="{top+chart_h}" x2="{width-right}" y2="{top+chart_h}" class="axis"/>']
    for i in range(5):
        value = max_int * i / 4
        y = top + chart_h - chart_h * i / 4
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{left-8}" y="{y+4:.1f}" text-anchor="end" class="tick">{fmt_number(value,1)}</text>')
    points = []
    for i, (key, count, integration, efficiency, rms) in enumerate(monthly):
        cx = left + slot*i + slot/2
        x = cx - bar_w/2
        h = chart_h * integration / max_int
        y = top + chart_h - h
        label = month_label(key)
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="7" class="bar"><title>{escape(label)}: {fmt_number(integration,1)} h; {count} sessioni; efficienza {fmt_number(efficiency,1)}%</title></rect>')
        parts.append(f'<text x="{cx:.1f}" y="{max(y-8,18):.1f}" text-anchor="middle" class="value">{fmt_number(integration,1)}h</text>')
        parts.append(f'<text x="{cx:.1f}" y="{top+chart_h+24}" text-anchor="middle" class="xlabel">{escape(label)}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{top+chart_h+44}" text-anchor="middle" class="subvalue">{count} sessioni</text>')
        if rms is not None:
            parts.append(f'<text x="{cx:.1f}" y="{top+chart_h+62}" text-anchor="middle" class="subvalue">RMS {fmt_number(rms,2)}″</text>')
        ey = top + chart_h - chart_h * min(max(efficiency,0),100)/100
        points.append((cx, ey, efficiency))
    if len(points) > 1:
        parts.append('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x,y,_ in points) + '" class="efficiency-line"/>')
    for x, y, efficiency in points:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" class="efficiency-point"><title>Efficienza {fmt_number(efficiency,1)}%</title></circle>')
    parts.append('</svg>')
    return ''.join(parts)


def configuration_rows(summary: List[Dict[str, str]]) -> str:
    if not summary:
        return '<tr><td colspan="8" class="empty-cell">Nessuna configurazione disponibile.</td></tr>'
    rows = []
    ordered = sorted(summary, key=lambda r: to_float(r.get('total_integration_hours')) or 0.0, reverse=True)
    for row in ordered:
        rows.append('<tr>'
                    f"<td><strong>{escape(row.get('configuration_name') or row.get('configuration_id'))}</strong><div class='muted mono'>{escape(row.get('configuration_id'))}</div></td>"
                    f"<td>{escape(row.get('telescope')) or '—'}</td>"
                    f"<td>{escape(row.get('camera')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('session_count')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('total_duration_hours')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('total_integration_hours')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('integration_efficiency_pct')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('average_rms_total_arcsec')) or '—'}</td></tr>")
    return ''.join(rows)


def recent_session_rows(sessions: List[Dict[str, str]], limit: int = 12) -> str:
    ordered = sorted(sessions, key=lambda r: (r.get('session_start',''), r.get('session_id','')), reverse=True)[:limit]
    if not ordered:
        return '<tr><td colspan="10" class="empty-cell">Nessuna sessione disponibile.</td></tr>'
    rows = []
    for row in ordered:
        severity = str(row.get('severity') or '').strip()
        upper = severity.upper()
        css = 'status-good' if upper in {'OK','SUCCESS','PASSED','INFO'} else 'status-warn' if upper in {'WARNING','WARN','DEGRADED','PARTIAL'} else 'status-bad' if severity else 'status-neutral'
        rows.append('<tr>'
                    f"<td class='mono'>{escape(row.get('session_id'))}</td>"
                    f"<td>{escape(row.get('configuration_id')) or '—'}</td>"
                    f"<td>{escape(row.get('session_start')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('duration_hours')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('integration_hours')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('completion_pct')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('rms_total_arcsec')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('weather_safe_pct')) or '—'}</td>"
                    f"<td class='num'>{escape(row.get('autofocus_count')) or '—'}</td>"
                    f"<td><span class='status {css}'>{escape(severity) or '—'}</span></td></tr>")
    return ''.join(rows)


def render_dashboard(sessions: List[Dict[str, str]], summary: List[Dict[str, str]]) -> str:
    k = aggregate_kpis(sessions)
    monthly = monthly_aggregation(sessions)
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Digital StarGate Analytics</title>
<style>
:root{{--bg:#07111f;--panel:#0d1b2d;--panel2:#10243d;--text:#eef5ff;--muted:#9fb2ca;--accent:#58a6ff;--accent2:#8bd5ff;--border:#233a58;--good:#57d18c;--warn:#ffc857;--bad:#ff6b6b;color-scheme:dark}}
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:radial-gradient(circle at top right,rgba(88,166,255,.12),transparent 34rem),var(--bg);color:var(--text)}}
.container{{width:min(1480px,calc(100% - 32px));margin:0 auto}} header{{padding:44px 0 24px}} .eyebrow{{color:var(--accent2);text-transform:uppercase;letter-spacing:.16em;font-size:.78rem;font-weight:700}}
h1{{margin:8px 0 6px;font-size:clamp(2rem,5vw,4rem);line-height:1}} .subtitle,.section-intro,.muted{{color:var(--muted)}} .subtitle{{max-width:900px}}
.kpi-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:22px 0}} .card{{background:linear-gradient(180deg,rgba(16,36,61,.98),rgba(13,27,45,.98));border:1px solid var(--border);border-radius:18px;padding:20px;box-shadow:0 14px 40px rgba(0,0,0,.18)}}
.kpi-label{{color:var(--muted);font-size:.88rem}} .kpi-value{{margin-top:8px;font-size:clamp(1.6rem,4vw,2.5rem);font-weight:750}} .kpi-note{{margin-top:4px;color:var(--muted);font-size:.78rem}}
.section{{margin:24px 0}} .section h2{{margin:0 0 6px;font-size:1.3rem}} .section-intro{{margin:0 0 16px;font-size:.9rem}} .chart,.table-wrap{{overflow-x:auto}} svg{{width:100%;min-width:760px;height:auto}}
.axis{{stroke:#6f88a6}} .grid{{stroke:#223954}} .bar{{fill:var(--accent)}} .efficiency-line{{fill:none;stroke:var(--good);stroke-width:3}} .efficiency-point{{fill:var(--good);stroke:var(--panel);stroke-width:2}}
.tick,.xlabel{{fill:var(--muted);font-size:12px}} .value{{fill:var(--text);font-size:12px;font-weight:700}} .subvalue{{fill:var(--muted);font-size:11px}}
table{{width:100%;border-collapse:collapse;min-width:1080px}} th,td{{padding:13px 12px;border-bottom:1px solid var(--border);text-align:left}} th{{color:var(--muted);font-size:.78rem;text-transform:uppercase;letter-spacing:.07em}} td{{font-size:.9rem}} .num{{text-align:right;font-variant-numeric:tabular-nums}} .muted{{font-size:.78rem;margin-top:4px}} .mono{{font-family:Consolas,'Courier New',monospace}} .empty,.empty-cell{{color:var(--muted);padding:24px;text-align:center}}
.status{{display:inline-block;padding:4px 9px;border-radius:999px;font-size:.74rem;font-weight:700}} .status-good{{color:var(--good);background:rgba(87,209,140,.12)}} .status-warn{{color:var(--warn);background:rgba(255,200,87,.12)}} .status-bad{{color:var(--bad);background:rgba(255,107,107,.12)}} .status-neutral{{color:var(--muted);background:rgba(159,178,202,.10)}} footer{{color:var(--muted);padding:18px 0 40px;font-size:.78rem}}
@media(max-width:1000px){{.kpi-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}} @media(max-width:560px){{.container{{width:min(100% - 20px,1480px)}}.kpi-grid{{grid-template-columns:1fr}}header{{padding-top:28px}}}}
</style></head><body><div class="container">
<header><div class="eyebrow">Digital StarGate Observatory</div><h1>Executive Analytics Dashboard</h1><div class="subtitle">Sintesi operativa delle sessioni, dell'efficienza di acquisizione, della qualità di guida e dell'affidabilità dei processi automatici.</div></header>
<section class="kpi-grid">
{''.join([
card('Sessioni', str(int(k['session_count'] or 0)), 'sessioni consolidate'),
card('Durata totale', fmt_optional(k['total_duration'],1,' h'), 'tempo complessivo di osservazione'),
card('Integrazione', fmt_optional(k['total_integration'],1,' h'), 'tempo utile acquisito'),
card('Efficienza', fmt_optional(k['integration_efficiency'],1,'%'), 'integrazione / durata'),
card('Completamento medio', fmt_optional(k['average_completion'],1,'%'), 'media delle sessioni'),
card('RMS medio', fmt_optional(k['average_rms'],2,'″'), 'qualità media della guida'),
card('Successo frame', fmt_optional(k['light_success_rate'],1,'%'), f"{fmt_number(k['light_completed'] or 0,0)} completati · {fmt_number(k['light_failed'] or 0,0)} falliti"),
card('Meteo sicuro medio', fmt_optional(k['average_weather_safe'],1,'%'), 'disponibilità condizioni sicure'),
card('Autofocus', fmt_number(k['autofocus_count'] or 0,0), f"successo {fmt_optional(k['autofocus_success_rate'],1,'%')}"),
card('Dithering', fmt_number(k['dither_count'] or 0,0), f"successo {fmt_optional(k['dither_success_rate'],1,'%')}"),
card('Sessioni OK', fmt_number(k['ok_sessions'] or 0,0), 'stato positivo esplicito'),
card('Configurazioni', str(len(summary)), 'profili strumentali consolidati'),
])}
</section>
<section class="section card"><h2>Trend mensile</h2><p class="section-intro">Le barre indicano le ore di integrazione; la linea verde rappresenta l'efficienza mensile. Sotto ogni mese sono riportati sessioni e RMS.</p><div class="chart">{build_monthly_chart(monthly)}</div></section>
<section class="section card"><h2>Prestazioni per configurazione</h2><p class="section-intro">Ordinamento per integrazione totale prodotta.</p><div class="table-wrap"><table><thead><tr><th>Configurazione</th><th>Telescopio</th><th>Camera</th><th class="num">Sessioni</th><th class="num">Durata h</th><th class="num">Integrazione h</th><th class="num">Efficienza %</th><th class="num">RMS ″</th></tr></thead><tbody>{configuration_rows(summary)}</tbody></table></div></section>
<section class="section card"><h2>Ultime sessioni</h2><p class="section-intro">Dettaglio operativo delle 12 sessioni più recenti.</p><div class="table-wrap"><table><thead><tr><th>Sessione</th><th>Configurazione</th><th>Inizio</th><th class="num">Durata h</th><th class="num">Integrazione h</th><th class="num">Completamento %</th><th class="num">RMS ″</th><th class="num">Meteo %</th><th class="num">Autofocus</th><th>Stato</th></tr></thead><tbody>{recent_session_rows(sessions)}</tbody></table></div></section>
<footer>Generato automaticamente il {escape(generated)} · Digital StarGate Analytics v2.7</footer></div></body></html>'''


def card(label: str, value: str, note: str) -> str:
    return f'<article class="card"><div class="kpi-label">{escape(label)}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></article>'


def main() -> int:
    parser = argparse.ArgumentParser(description='Genera la dashboard executive Digital StarGate.')
    parser.add_argument('--repo-root', type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    sessions = read_csv(repo_root / SESSIONS_RELATIVE_PATH)
    summary = read_csv(repo_root / CONFIG_SUMMARY_RELATIVE_PATH)
    output_path = args.output.resolve() if args.output else repo_root / OUTPUT_RELATIVE_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_dashboard(sessions, summary), encoding='utf-8')
    print(f'Sessioni lette: {len(sessions)}')
    print(f'Configurazioni lette: {len(summary)}')
    print(f'Dashboard v2.7: {output_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
