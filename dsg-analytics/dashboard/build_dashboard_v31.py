#!/usr/bin/env python3
"""Digital StarGate Analytics v3.1 - native MkDocs Material dashboard."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import build_dashboard as legacy

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
        session_kpis=legacy.aggregate_kpis(sessions),
        target_metrics=legacy.aggregate_targets(targets),
        monthly=legacy.monthly_aggregation(sessions),
        generated=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def render_session_cards(model: DashboardModel) -> str:
    k = model.session_kpis
    cards = [
        legacy.card("Sessioni", str(int(k["session_count"] or 0)), "sessioni consolidate"),
        legacy.card("Durata totale", legacy.fmt_optional(k["total_duration"], 1, " h"), "tempo complessivo di osservazione"),
        legacy.card("Integrazione sessioni", legacy.fmt_optional(k["total_integration"], 1, " h"), "tempo utile acquisito"),
        legacy.card("Efficienza", legacy.fmt_optional(k["integration_efficiency"], 1, "%"), "integrazione / durata"),
        legacy.card("Completamento medio", legacy.fmt_optional(k["average_completion"], 1, "%"), "media delle sessioni"),
        legacy.card("RMS medio", legacy.fmt_optional(k["average_rms"], 2, "″"), "qualità media della guida"),
        legacy.card(
            "Successo frame",
            legacy.fmt_optional(k["light_success_rate"], 1, "%"),
            f"{legacy.fmt_number(k['light_completed'] or 0, 0)} completati · {legacy.fmt_number(k['light_failed'] or 0, 0)} falliti",
        ),
        legacy.card("Meteo sicuro medio", legacy.fmt_optional(k["average_weather_safe"], 1, "%"), "disponibilità condizioni sicure"),
        legacy.card("Autofocus", legacy.fmt_number(k["autofocus_count"] or 0, 0), f"successo {legacy.fmt_optional(k['autofocus_success_rate'], 1, '%')}"),
        legacy.card("Dithering", legacy.fmt_number(k["dither_count"] or 0, 0), f"successo {legacy.fmt_optional(k['dither_success_rate'], 1, '%')}"),
        legacy.card("Sessioni OK", legacy.fmt_number(k["ok_sessions"] or 0, 0), "stato positivo esplicito"),
        legacy.card("Configurazioni", str(len(model.summary)), "profili strumentali consolidati"),
    ]
    return "".join(cards)


def render_dashboard(model: DashboardModel) -> str:
    return f'''# Executive Observatory Dashboard

<div class="dsg-dashboard">
  <div class="dsg-dashboard-hero">
    <span class="dsg-eyebrow">Digital StarGate Observatory</span>
    <p>
      Sintesi operativa delle sessioni, dei target osservati,
      dell'efficienza di acquisizione, della qualità di guida
      e dell'affidabilità dei processi automatici.
    </p>
  </div>

  <div class="dsg-section-label">Session Analytics</div>
  <section class="dsg-kpi-grid">
    {render_session_cards(model)}
  </section>

  <section class="dsg-section dsg-card">
    <h2>Trend mensile</h2>
    <p class="dsg-section-intro">
      Le barre indicano le ore di integrazione; la linea rappresenta
      l'efficienza mensile. Sotto ogni mese sono riportati sessioni e RMS.
    </p>
    <div class="dsg-chart">{legacy.build_monthly_chart(model.monthly)}</div>
  </section>

  <div class="dsg-section-label">Target Analytics</div>
  <section class="dsg-kpi-grid">
    {legacy.target_summary_cards(model.target_metrics)}
  </section>

  <section class="dsg-section dsg-split-grid">
    <article class="dsg-card">
      <h2>Classifica target</h2>
      <p class="dsg-section-intro">Ordinamento per ore complessive di integrazione.</p>
      <div class="dsg-table-wrap">
        <table>
          <thead><tr><th>#</th><th>Target</th><th>Filtri</th><th class="num">Integrazione h</th><th class="num">Immagini</th><th class="num">Sessioni</th></tr></thead>
          <tbody>{legacy.target_rows(model.target_metrics)}</tbody>
        </table>
      </div>
    </article>
    <article class="dsg-card">
      <h2>Distribuzione filtri</h2>
      <p class="dsg-section-intro">Ore di integrazione e immagini per filtro.</p>
      {legacy.build_filter_chart(model.target_metrics)}
    </article>
  </section>

  <div class="dsg-section-label">Configuration Analytics</div>
  <section class="dsg-section dsg-card">
    <h2>Prestazioni per configurazione</h2>
    <p class="dsg-section-intro">Ordinamento per integrazione totale prodotta.</p>
    <div class="dsg-table-wrap">
      <table>
        <thead><tr><th>Configurazione</th><th>Telescopio</th><th>Camera</th><th class="num">Sessioni</th><th class="num">Durata h</th><th class="num">Integrazione h</th><th class="num">Efficienza %</th><th class="num">RMS ″</th></tr></thead>
        <tbody>{legacy.configuration_rows(model.summary)}</tbody>
      </table>
    </div>
  </section>

  <div class="dsg-section-label">Operational Detail</div>
  <section class="dsg-section dsg-card">
    <h2>Ultime sessioni</h2>
    <p class="dsg-section-intro">Dettaglio operativo delle 12 sessioni più recenti.</p>
    <div class="dsg-table-wrap">
      <table>
        <thead><tr><th>Sessione</th><th>Configurazione</th><th>Inizio</th><th class="num">Durata h</th><th class="num">Integrazione h</th><th class="num">Completamento %</th><th class="num">RMS ″</th><th class="num">Meteo %</th><th class="num">Autofocus</th><th>Stato</th></tr></thead>
        <tbody>{legacy.recent_session_rows(model.sessions)}</tbody>
      </table>
    </div>
  </section>

  <p class="dsg-dashboard-footer">Generato automaticamente il {legacy.escape(model.generated)} · Digital StarGate Analytics v3.1</p>
</div>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera la dashboard nativa MkDocs Digital StarGate Analytics v3.1.")
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    sessions = legacy.read_csv(repo_root / legacy.SESSIONS_RELATIVE_PATH, required=True)
    summary = legacy.read_csv(repo_root / legacy.CONFIG_SUMMARY_RELATIVE_PATH, required=True)
    targets = legacy.read_csv(repo_root / legacy.TARGETS_RELATIVE_PATH, required=False)
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
