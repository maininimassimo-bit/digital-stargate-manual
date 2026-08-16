#!/usr/bin/env python3
"""Refresh the homepage status sections from governed roadmap and analytics data."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

START_MARKER = "<!-- DSG:AUTO-HOMEPAGE:START -->"
END_MARKER = "<!-- DSG:AUTO-HOMEPAGE:END -->"
PROGRAM_PATTERN = re.compile(
    r'<section class="dsg-program-section">\s*'
    r'<div class="dsg-section-intro">\s*'
    r'<span class="dsg-section-kicker">STATO DEL PROGRAMMA</span>.*?'
    r'</section>\s*(?=' + re.escape(START_MARKER) + r')',
    re.DOTALL,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def as_float(value: object) -> float:
    try:
        return float(str(value or "0").strip().replace(",", "."))
    except ValueError:
        return 0.0


def as_int(value: object) -> int:
    return int(round(as_float(value)))


def esc(value: object) -> str:
    text = str(value or "").strip()
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        if text
        else "—"
    )


def decimal(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def roadmap_state(roadmap: dict) -> dict:
    items = [item for wave in roadmap.get("waves", []) for item in wave.get("items", [])]
    current_id = str(roadmap.get("currentPackage") or "—")
    current = next((item for item in items if item.get("id") == current_id), {})
    summary = roadmap.get("summary", {})
    return {
        "current_id": current_id,
        "current_title": str(current.get("title") or "Architecture Package corrente"),
        "project_status": str(roadmap.get("projectStatus") or "—"),
        "next_milestone": str(roadmap.get("nextMilestone") or "—"),
        "target": str(roadmap.get("target") or "—"),
        "completed": as_int(summary.get("completed")),
        "active": as_int(summary.get("active")),
        "planned": as_int(summary.get("planned")),
        "total": as_int(summary.get("total")),
        "percent": max(0, min(100, as_int(summary.get("percentCompleted")))),
    }


def build_program_section(state: dict) -> str:
    return f'''<section class="dsg-program-section">
  <div class="dsg-section-intro">
    <span class="dsg-section-kicker">STATO DEL PROGRAMMA</span>
    <h2>Architettura e avanzamento corrente</h2>
  </div>

  <div class="dsg-program-panel">
    <article>
      <span class="dsg-program-label">ARCHITECTURE PACKAGE</span>
      <span class="dsg-program-value">{esc(state['current_id'])} <span class="dsg-status-pill">{esc(state['project_status']).upper()}</span></span>
      <span class="dsg-program-detail">{esc(state['current_title'])}</span>
      <div class="dsg-progress" aria-label="Avanzamento programma: {state['percent']} percento"><span style="width: {state['percent']}%"></span></div>
    </article>

    <article>
      <span class="dsg-program-label">PROSSIMA MILESTONE</span>
      <span class="dsg-program-value">{esc(state['next_milestone'])}</span>
      <span class="dsg-program-detail">Milestone derivata dalla roadmap governata.</span>
    </article>

    <article>
      <span class="dsg-program-label">AVANZAMENTO PROGRAMMA</span>
      <span class="dsg-program-value">{state['percent']}%</span>
      <span class="dsg-program-detail">{state['completed']} completati · {state['active']} attivi · {state['planned']} pianificati su {state['total']} elementi.</span>
    </article>

    <article>
      <span class="dsg-program-label">TARGET PROGRAMMA</span>
      <span class="dsg-program-value">{esc(state['target'])}</span>
      <span class="dsg-program-detail">Fonte: docs/data/roadmap.json, projection governata.</span>
    </article>
  </div>
</section>

'''


def build_operational_section(sessions: list[dict[str, str]], targets: list[dict[str, str]]) -> str:
    session_count = len(sessions)
    total_integration = sum(as_float(row.get("integration_hours")) for row in sessions)
    completed_images = sum(as_int(row.get("light_completed")) for row in sessions)
    distinct_targets = {
        row.get("target_name", "").strip()
        for row in targets
        if row.get("target_name", "").strip()
    }
    return f'''{START_MARKER}
<section class="dsg-program-section">
  <div class="dsg-section-intro">
    <span class="dsg-section-kicker">OSSERVATORIO E DATI</span>
    <h2>Indicatori operativi</h2>
  </div>

  <div class="dsg-kpi-grid">
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Sessioni</span>
      <span class="dsg-kpi__value dsg-counter" data-value="{session_count}">0</span>
      <span class="dsg-kpi__detail">storico disponibile</span>
    </div>
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Integrazione</span>
      <span class="dsg-kpi__value dsg-counter" data-value="{total_integration:.2f}" data-decimals="2" data-suffix=" h">0</span>
      <span class="dsg-kpi__detail">totale acquisito</span>
    </div>
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Immagini</span>
      <span class="dsg-kpi__value dsg-counter" data-value="{completed_images}">0</span>
      <span class="dsg-kpi__detail">light completati</span>
    </div>
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Target</span>
      <span class="dsg-kpi__value dsg-counter" data-value="{len(distinct_targets)}">0</span>
      <span class="dsg-kpi__detail">oggetti distinti</span>
    </div>
  </div>
  <div class="dsg-enterprise-meta">
    <strong>PROJECTION GOVERNATA</strong>
    <span>{session_count} sessioni · {decimal(total_integration)} h · {completed_images} light · {len(distinct_targets)} target</span>
    <span>Fonti: data/analytics/history/sessions.csv e targets.csv.</span>
  </div>
</section>
{END_MARKER}'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.repo_root.resolve()

    homepage = root / "docs" / "index.md"
    roadmap = read_json(root / "docs" / "data" / "roadmap.json")
    sessions = read_csv(root / "data" / "analytics" / "history" / "sessions.csv")
    targets = read_csv(root / "data" / "analytics" / "history" / "targets.csv")

    text = homepage.read_text(encoding="utf-8-sig")
    state = roadmap_state(roadmap)
    program_section = build_program_section(state)
    operational_section = build_operational_section(sessions, targets)

    text, program_count = PROGRAM_PATTERN.subn(program_section, text, count=1)
    if program_count != 1:
        raise RuntimeError("Homepage program status section not found or ambiguous")

    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start < 0 or end < start:
        raise RuntimeError("Homepage automatic block markers missing or invalid")
    end += len(END_MARKER)
    text = text[:start] + operational_section + text[end:]

    homepage.write_text(text, encoding="utf-8", newline="\n")
    print(
        "Homepage refreshed: "
        f"package={state['current_id']} progress={state['percent']}% "
        f"sessions={len(sessions)} integration={decimal(sum(as_float(row.get('integration_hours')) for row in sessions))}h "
        f"images={sum(as_int(row.get('light_completed')) for row in sessions)} targets={len({row.get('target_name', '').strip() for row in targets if row.get('target_name', '').strip()})}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
