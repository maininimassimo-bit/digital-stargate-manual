#!/usr/bin/env python3
"""Digital StarGate Analytics v3.1 - native MkDocs Material dashboard."""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import build_dashboard as core

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parents[1]
OUTPUT_RELATIVE_PATH = Path("docs/analytics/dashboard.md")


@dataclass(frozen=True)
class DashboardModel:
    sessions: List[Dict[str, str]]
    summary: List[Dict[str, str]]
    targets: List[Dict[str, str]]
    session_kpis: Dict[str, Optional[float]]
    target_metrics: Dict[str, object]
    monthly: List[Tuple[str, int, float, float, Optional[float]]]
    generated: str


def build_model(
    sessions: List[Dict[str, str]],
    summary: List[Dict[str, str]],
    targets: List[Dict[str, str]],
) -> DashboardModel:
    return DashboardModel(
        sessions=sessions,
        summary=summary,
        targets=targets,
        session_kpis=core.aggregate_kpis(sessions),
        target_metrics=core.aggregate_targets(targets),
        monthly=core.monthly_aggregation(sessions),
        generated=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def card(label: str, value: str, note: str) -> str:
    return (
        '<article class="dsg-card dsg-kpi-card">'
        f'<div class="dsg-kpi-label">{core.escape(label)}</div>'
        f'<div class="dsg-kpi-value">{value}</div>'
        f'<div class="dsg-kpi-note">{core.escape(note)}</div>'
        '</article>'
    )


def render_session_cards(model: DashboardModel) -> str:
    k = model.session_kpis
    cards = [
        card("Sessioni", str(int(k["session_count"] or 0)), "sessioni consolidate"),
        card("Durata totale", core.fmt_optional(k["total_duration"], 1, " h"), "tempo complessivo di osservazione"),
        card("Integrazione sessioni", core.fmt_optional(k["total_integration"], 1, " h"), "tempo utile acquisito"),
        card("Efficienza", core.fmt_optional(k["integration_efficiency"], 1, "%"), "integrazione / durata"),
        card("Completamento medio", core.fmt_optional(k["average_completion"], 1, "%"), "media delle sessioni"),
        card("RMS medio", core.fmt_optional(k["average_rms"], 2, "″"), "qualità media della guida"),
        card(
            "Successo frame",
            core.fmt_optional(k["light_success_rate"], 1, "%"),
            f"{core.fmt_number(k['light_completed'] or 0, 0)} completati · {core.fmt_number(k['light_failed'] or 0, 0)} falliti",
        ),
        card("Meteo sicuro medio", core.fmt_optional(k["average_weather_safe"], 1, "%"), "disponibilità condizioni sicure"),
        card("Autofocus", core.fmt_number(k["autofocus_count"] or 0, 0), f"successo {core.fmt_optional(k['autofocus_success_rate'], 1, '%')}"),
        card("Dithering", core.fmt_number(k["dither_count"] or 0, 0), f"successo {core.fmt_optional(k['dither_success_rate'], 1, '%')}"),
        card("Sessioni OK", core.fmt_number(k["ok_sessions"] or 0, 0), "stato positivo esplicito"),
        card("Configurazioni", str(len(model.summary)), "profili, inclusi quelli non identificati"),
    ]
    return "".join(cards)


def render_target_cards(model: DashboardModel) -> str:
    metrics = model.target_metrics
    return "".join(
        [
            card("Target distinti", core.fmt_number(float(metrics.get("target_count") or 0), 0), "oggetti astronomici consolidati"),
            card("Immagini target", core.fmt_number(float(metrics.get("total_images") or 0), 0), "frame associati ai target"),
            card("Integrazione target", core.fmt_optional(float(metrics.get("total_hours") or 0), 2, " h"), "tempo utile ricostruito dai log NINA"),
            card("Sessioni target", core.fmt_number(float(metrics.get("session_count") or 0), 0), "sessioni con target riconosciuto"),
            card("Target principale", core.escape(metrics.get("top_target") or "—"), "primo per ore di integrazione"),
            card("Filtro principale", core.escape(metrics.get("top_filter") or "—"), "primo per ore di utilizzo"),
            card("Ultimo target", core.escape(metrics.get("latest_target") or "—"), "ultimo oggetto acquisito"),
        ]
    )


def render_target_rows(model: DashboardModel) -> str:
    ranking = model.target_metrics.get("ranking") or []
    if not ranking:
        return '<tr><td colspan="6" class="dsg-empty-cell">Nessun target disponibile.</td></tr>'

    rows = []
    for index, item in enumerate(ranking, start=1):
        rows.append(
            '<tr>'
            f'<td class="dsg-rank">{index}</td>'
            f'<td><strong>{core.escape(item["target"])}</strong></td>'
            f'<td>{core.escape(item["filters"]) or "—"}</td>'
            f'<td class="num">{core.fmt_number(float(item["hours"]), 2)}</td>'
            f'<td class="num">{core.fmt_number(float(item["images"]), 0)}</td>'
            f'<td class="num">{core.fmt_number(float(item["sessions"]), 0)}</td>'
            '</tr>'
        )
    return "".join(rows)


def render_filter_chart(model: DashboardModel) -> str:
    filters = model.target_metrics.get("filters") or []
    if not filters:
        return '<div class="dsg-empty">Nessun dato filtro disponibile.</div>'

    max_hours = max(float(item["hours"]) for item in filters) or 1.0
    parts = ['<div class="dsg-filter-bars">']
    for item in filters:
        hours = float(item["hours"])
        width = 100.0 * hours / max_hours
        parts.append(
            '<div class="dsg-filter-row">'
            '<div class="dsg-filter-heading">'
            f'<strong>{core.escape(item["filter"])}</strong>'
            f'<span>{core.fmt_number(hours, 2)} h · {core.fmt_number(float(item["images"]), 0)} immagini · {core.fmt_number(float(item["targets"]), 0)} target</span>'
            '</div>'
            '<div class="dsg-bar-track">'
            f'<div class="dsg-bar-fill" style="width:{width:.2f}%"></div>'
            '</div></div>'
        )
    parts.append('</div>')
    return "".join(parts)


def render_configuration_rows(model: DashboardModel) -> str:
    if not model.summary:
        return '<tr><td colspan="8" class="dsg-empty-cell">Nessuna configurazione disponibile.</td></tr>'

    ordered = sorted(
        model.summary,
        key=lambda row: core.to_float(row.get("total_integration_hours")) or 0.0,
        reverse=True,
    )
    rows = []
    for row in ordered:
        rows.append(
            '<tr>'
            f'<td><strong>{core.escape(row.get("configuration_name") or row.get("configuration_id"))}</strong>'
            f'<div class="dsg-muted dsg-mono">{core.escape(row.get("configuration_id"))}</div></td>'
            f'<td>{core.escape(row.get("telescope")) or "—"}</td>'
            f'<td>{core.escape(row.get("camera")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("session_count")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("total_duration_hours")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("total_integration_hours")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("integration_efficiency_pct")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("average_rms_total_arcsec")) or "—"}</td>'
            '</tr>'
        )
    return "".join(rows)


def render_recent_session_rows(model: DashboardModel, limit: int = 12) -> str:
    ordered = sorted(
        model.sessions,
        key=lambda row: (row.get("session_start", ""), row.get("session_id", "")),
        reverse=True,
    )[:limit]
    if not ordered:
        return '<tr><td colspan="10" class="dsg-empty-cell">Nessuna sessione disponibile.</td></tr>'

    rows = []
    for row in ordered:
        severity = str(row.get("severity") or "").strip()
        upper = severity.upper()
        if upper in {"OK", "SUCCESS", "PASSED", "INFO"}:
            css_class = "dsg-status-good"
        elif upper in {"WARNING", "WARN", "DEGRADED", "PARTIAL"}:
            css_class = "dsg-status-warn"
        elif severity:
            css_class = "dsg-status-bad"
        else:
            css_class = "dsg-status-neutral"

        rows.append(
            '<tr>'
            f'<td class="dsg-mono">{core.escape(row.get("session_id"))}</td>'
            f'<td>{core.escape(row.get("configuration_id")) or "—"}</td>'
            f'<td>{core.escape(row.get("session_start")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("duration_hours")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("integration_hours")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("completion_pct")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("rms_total_arcsec")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("weather_safe_pct")) or "—"}</td>'
            f'<td class="num">{core.escape(row.get("autofocus_count")) or "—"}</td>'
            f'<td><span class="dsg-status {css_class}">{core.escape(severity) or "—"}</span></td>'
            '</tr>'
        )
    return "".join(rows)


def visual_bars(items, unit="h") -> str:
    """Display source-derived magnitudes; missing values never become zero."""
    known = [value for _, value, _ in items if value is not None]
    maximum = max(known, default=0) or 1
    parts = ['<div class="dsg-ex-bars">']
    for label, value, note in items:
        width = 100 * value / maximum if value is not None else 0
        parts.append('<div class="dsg-ex-bar"><div><strong>' + core.escape(label) + '</strong><span>' + core.fmt_optional(value, 2, ' ' + unit) + '</span></div>'
                     + f'<div class="dsg-ex-track"><i style="width:{width:.3f}%"></i></div><small>{core.escape(note)}</small></div>')
    return ''.join(parts) + '</div>'


def monthly_visual(model: DashboardModel) -> str:
    if not model.monthly:
        return '<p>Nessun mese con dati disponibili.</p>'
    maximum = max(row[2] for row in model.monthly) or 1
    width = max(660, len(model.monthly) * 140)
    step = (width - 100) / len(model.monthly)
    svg = [f'<svg viewBox="0 0 {width} 300" role="img" aria-label="Ore di integrazione per mese"><defs><linearGradient id="executive-bars" x2="0" y2="1"><stop stop-color="#79edf2"/><stop offset="1" stop-color="#536ce5"/></linearGradient></defs>']
    for n in range(5):
        y = 230 - n * 45
        svg.append(f'<line x1="55" x2="{width-25}" y1="{y}" y2="{y}"/><text x="45" y="{y+5}" text-anchor="end">{core.fmt_number(maximum*n/4,1)}</text>')
    for i, (month, count, hours, efficiency, rms) in enumerate(model.monthly):
        x = 65 + step * i + step / 2
        height = 180 * hours / maximum
        svg.append(f'<rect x="{x-25}" y="{230-height}" width="50" height="{height}" rx="8" fill="url(#executive-bars)"><title>{core.escape(core.month_label(month))}: {core.fmt_number(hours,2)} h</title></rect><text x="{x}" y="{220-height}" text-anchor="middle">{core.fmt_number(hours,1)} h</text><text x="{x}" y="260" text-anchor="middle">{core.escape(core.month_label(month))}</text><text x="{x}" y="283" text-anchor="middle">{count} sessioni</text>')
    svg.append('</svg>')
    cards = ''.join(f'<article><strong>{core.escape(core.month_label(m))}</strong><span>{core.fmt_number(e,1)}% efficienza</span><meter min="0" max="100" value="{e}" aria-label="Efficienza {core.escape(m)}">{e}%</meter><small>RMS {core.fmt_optional(r,2,"″")}</small></article>' for m,c,h,e,r in model.monthly)
    return '<div class="dsg-ex-plot">'+''.join(svg)+'</div><div class="dsg-ex-months">'+cards+'</div>'


def render_dashboard(model: DashboardModel) -> str:
    return f'''# Executive Observatory Dashboard

<link rel="stylesheet" href="../../styles/executive-dashboard.css">
<script src="../../javascripts/executive-dashboard.js" defer></script>
<div class="dsg-dashboard dsg-executive" data-executive-dashboard data-snapshot="{hashlib.sha256(json.dumps([model.sessions, model.summary, model.targets], sort_keys=True).encode()).hexdigest()}">
  <div class="dsg-dashboard-hero">
    <span class="dsg-eyebrow">Digital StarGate Observatory</span>
    <h2>Dal cielo al dato.</h2>
    <p>Sintesi operativa delle sessioni, dei target osservati, dell'efficienza di acquisizione, della qualità di guida e dell'affidabilità dei processi automatici.</p>
    <nav aria-label="Sezioni dashboard"><a href="#executive-months">Andamento</a><a href="#executive-targets">Target</a><a href="#executive-setups">Setup</a><a href="#executive-sessions">Sessioni</a></nav>
    <p class="dsg-ex-refresh" role="status">Snapshot aggiornato dalla pipeline a ogni importazione.</p>
  </div>

  <div class="dsg-section-label">Session Analytics</div>
  <section class="dsg-kpi-grid">{render_session_cards(model)}</section>

  <section class="dsg-section dsg-card" id="executive-months">
    <h2>Trend mensile</h2>
    <p class="dsg-section-intro">Ore di integrazione per mese. Efficienza su scala 0–100% e RMS riportati separatamente.</p>
    {monthly_visual(model)}
  </section>

  <div class="dsg-section-label">Target Analytics</div>
  <section class="dsg-kpi-grid">{render_target_cards(model)}</section>

  <section class="dsg-section dsg-split-grid" id="executive-targets">
    <article class="dsg-card">
      <h2>Classifica target</h2>
      <p class="dsg-section-intro">Ordinamento per ore complessive di integrazione.</p>
      {visual_bars([(str(t['target']), float(t['hours']), str(t['images'])+' immagini') for t in model.target_metrics.get('ranking', [])])}
      <details><summary>Valori completi dei target</summary>
      <div class="dsg-table-wrap"><table><thead><tr><th>#</th><th>Target</th><th>Filtri</th><th class="num">Integrazione h</th><th class="num">Immagini</th><th class="num">Sessioni</th></tr></thead><tbody>{render_target_rows(model)}</tbody></table></div>
      </details>
    </article>
    <article class="dsg-card">
      <h2>Distribuzione filtri</h2>
      <p class="dsg-section-intro">Ore di integrazione e immagini per filtro.</p>
      {render_filter_chart(model)}
    </article>
  </section>

  <div class="dsg-section-label">Configuration Analytics</div>
  <section class="dsg-section dsg-card" id="executive-setups">
    <h2>Prestazioni per configurazione</h2>
    <p class="dsg-section-intro">Ordinamento per integrazione totale prodotta.</p>
    {visual_bars([(str(r.get('configuration_name') or r.get('configuration_id')),core.to_float(r.get('total_integration_hours')),str(r.get('session_count'))+' sessioni · efficienza '+str(r.get('integration_efficiency_pct'))+'%') for r in sorted(model.summary,key=lambda r:core.to_float(r.get('total_integration_hours')) or 0,reverse=True)])}
    <details><summary>Dettaglio completo delle configurazioni, inclusi i setup non identificati</summary>
    <div class="dsg-table-wrap"><table><thead><tr><th>Configurazione</th><th>Telescopio</th><th>Camera</th><th class="num">Sessioni</th><th class="num">Durata h</th><th class="num">Integrazione h</th><th class="num">Efficienza %</th><th class="num">RMS ″</th></tr></thead><tbody>{render_configuration_rows(model)}</tbody></table></div>
    </details>
  </section>

  <div class="dsg-section-label">Operational Detail</div>
  <section class="dsg-section dsg-card" id="executive-sessions">
    <h2>Ultime sessioni</h2>
    <p class="dsg-section-intro">Dettaglio operativo delle 12 sessioni più recenti.</p>
    <label class="dsg-ex-search">Cerca nelle ultime sessioni <input type="search" data-executive-search placeholder="Data, setup o stato"></label>
    <div class="dsg-table-wrap"><table><thead><tr><th>Sessione</th><th>Configurazione</th><th>Inizio</th><th class="num">Durata h</th><th class="num">Integrazione h</th><th class="num">Completamento %</th><th class="num">RMS ″</th><th class="num">Meteo %</th><th class="num">Autofocus</th><th>Stato</th></tr></thead><tbody>{render_recent_session_rows(model)}</tbody></table></div>
  </section>

  <p class="dsg-dashboard-footer">Generato automaticamente il {core.escape(model.generated)} · Digital StarGate Analytics v3.1</p>
</div>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera la dashboard nativa MkDocs Digital StarGate Analytics v3.1.")
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    sessions = core.read_csv(repo_root / core.SESSIONS_RELATIVE_PATH, required=True)
    summary = core.read_csv(repo_root / core.CONFIG_SUMMARY_RELATIVE_PATH, required=True)
    targets = core.read_csv(repo_root / core.TARGETS_RELATIVE_PATH, required=False)
    output_path = args.output.resolve() if args.output else repo_root / OUTPUT_RELATIVE_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_dashboard(build_model(sessions, summary, targets)), encoding="utf-8")

    print(f"Sessioni lette: {len(sessions)}")
    print(f"Configurazioni lette: {len(summary)}")
    print(f"Righe target lette: {len(targets)}")
    print(f"Dashboard v3.1: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
