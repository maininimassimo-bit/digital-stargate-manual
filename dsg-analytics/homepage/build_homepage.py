#!/usr/bin/env python3
"""Generate the dynamic Digital StarGate enterprise homepage block."""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

START_MARKER = "<!-- DSG:AUTO-HOMEPAGE:START -->"
END_MARKER = "<!-- DSG:AUTO-HOMEPAGE:END -->"


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def as_float(value):
    try:
        return float(str(value or "0").strip().replace(",", "."))
    except ValueError:
        return 0.0


def as_int(value):
    return int(round(as_float(value)))


def as_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def dec(value, digits=2):
    return f"{value:.{digits}f}".replace(".", ",")


def date(value):
    parsed = as_dt(value)
    return parsed.strftime("%d/%m/%Y %H:%M") if parsed else "—"


def esc(value):
    text = str(value or "").strip()
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("|", r"\|")
        .replace("\n", " ")
        if text
        else "—"
    )


def status(value):
    severity = str(value or "").strip().upper()
    return {
        "GREEN": "🟢 GREEN",
        "YELLOW": "🟡 YELLOW",
        "RED": "🔴 RED",
    }.get(severity, esc(severity))


def git_value(root: Path, *args: str, fallback: str = "—") -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True, text=True
        )
        value = result.stdout.strip()
        return value or fallback
    except (OSError, subprocess.CalledProcessError):
        return fallback


def git_activity(root: Path, limit: int = 5):
    raw = git_value(
        root,
        "log",
        f"-{limit}",
        "--date=format:%d/%m %H:%M",
        "--pretty=%ad%x1f%h%x1f%s",
        fallback="",
    )
    events = []
    for line in raw.splitlines():
        parts = line.split("\x1f", 2)
        if len(parts) == 3:
            events.append({"time": parts[0], "sha": parts[1], "title": parts[2]})
    return events


def count_files(root: Path, pattern: str) -> int:
    return sum(1 for path in root.glob(pattern) if path.is_file())


def directory_size(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}".replace(".", ",")
        value /= 1024
    return "—"


def roadmap_summary(roadmap: dict):
    waves = roadmap.get("waves", [])
    items = [item for wave in waves for item in wave.get("items", [])]
    current_package = str(roadmap.get("currentPackage") or "—")
    active_item = next((item for item in items if item.get("id") == current_package), {})
    return {
        "current_package": current_package,
        "current_title": str(active_item.get("title") or "Architecture Package corrente"),
        "project_status": str(roadmap.get("projectStatus") or "—"),
        "next_milestone": str(roadmap.get("nextMilestone") or "—"),
        "target": str(roadmap.get("target") or "—"),
        "architecture_packages": len(items),
        "active_packages": sum(1 for item in items if item.get("status") == "active"),
        "completed_packages": sum(1 for item in items if item.get("status") == "completed"),
    }


def activity_markup(events):
    if not events:
        return '<a class="dsg-quick-card"><strong>Nessuna attività disponibile</strong><span>La cronologia Git non è accessibile durante questa build.</span><em>—</em></a>'
    return "\n".join(
        f'<a class="dsg-quick-card" href="https://github.com/maininimassimo-bit/digital-stargate-manual/commit/{esc(event["sha"])}"><strong>{esc(event["time"])} · {esc(event["sha"])}</strong><span>{esc(event["title"])}</span><em>→</em></a>'
        for event in events
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.repo_root.resolve()

    history = root / "data" / "analytics" / "history"
    sessions = read_csv(history / "sessions.csv")
    targets = read_csv(history / "targets.csv")
    roadmap = read_json(root / "docs" / "data" / "roadmap.json")
    program = roadmap_summary(roadmap)

    homepage = root / "docs" / "index.md"
    if not homepage.exists():
        raise FileNotFoundError(f"Homepage not found: {homepage}")

    session_count = len(sessions)
    total_integration = sum(as_float(row.get("integration_hours")) for row in sessions)
    completed_images = sum(as_int(row.get("light_completed")) for row in sessions)
    distinct_targets = sorted(
        {row.get("target_name", "").strip() for row in targets if row.get("target_name", "").strip()}
    )

    latest = (
        max(
            sessions,
            key=lambda row: as_dt(row.get("session_end"))
            or as_dt(row.get("session_start"))
            or datetime.min,
        )
        if sessions
        else None
    )

    if latest:
        sid = latest.get("session_id", "").strip()
        latest_targets = sorted(
            {
                row.get("target_name", "").strip()
                for row in targets
                if row.get("session_id", "").strip() == sid
                and row.get("target_name", "").strip()
            }
        )
        target_text = ", ".join(esc(item) for item in latest_targets) or "—"
        config = (
            " · ".join(
                esc(item)
                for item in (latest.get("telescope", "").strip(), latest.get("camera", "").strip())
                if item
            )
            or esc(latest.get("configuration_id"))
        )
        latest_rows = {
            "session": esc(sid),
            "date": f"{date(latest.get('session_start'))} → {date(latest.get('session_end'))}",
            "target": target_text,
            "config": config,
            "integration": f"{dec(as_float(latest.get('integration_hours')))} h",
            "images": str(as_int(latest.get("light_completed"))),
            "rms": f"{dec(as_float(latest.get('rms_total_arcsec')), 3)} arcsec" if as_float(latest.get("rms_total_arcsec")) > 0 else "—",
            "status": status(latest.get("severity")),
        }
    else:
        latest_rows = {key: "—" for key in ("session", "date", "target", "config", "integration", "images", "rms", "status")}

    docs_root = root / "docs"
    document_count = count_files(docs_root, "**/*.md")
    adr_count = count_files(docs_root / "architecture", "ADR-*.md")
    assessment_count = count_files(docs_root / "architecture" / "assessments", "*.md")
    validation_count = count_files(docs_root / "architecture" / "validation", "*.md")
    script_count = count_files(root, "**/*.py") + count_files(root, "**/*.ps1") + count_files(root, "**/*.psm1")
    workflow_count = count_files(root / ".github" / "workflows", "*.yml") + count_files(root / ".github" / "workflows", "*.yaml")
    repository_size = human_size(directory_size(root))

    commit_sha = os.getenv("GITHUB_SHA") or git_value(root, "rev-parse", "HEAD")
    short_sha = commit_sha[:7] if commit_sha != "—" else "—"
    commit_title = git_value(root, "log", "-1", "--pretty=%s")
    branch = os.getenv("GITHUB_REF_NAME") or git_value(root, "branch", "--show-current")
    run_number = os.getenv("GITHUB_RUN_NUMBER", "—")
    build_status = "VALIDATA" if os.getenv("GITHUB_ACTIONS") == "true" else "LOCALE"
    generated_at = datetime.now().astimezone().strftime("%d/%m/%Y %H:%M %Z")
    activity = git_activity(root)

    block = f'''{START_MARKER}
<section class="dsg-program-section">
  <div class="dsg-section-intro"><span class="dsg-section-kicker">COMMAND CENTER</span><h2>Stato del programma e patrimonio documentale</h2></div>
  <div class="dsg-kpi-grid">
    <div class="dsg-kpi"><span class="dsg-kpi__label">Documenti</span><span class="dsg-kpi__value">{document_count}</span><span class="dsg-kpi__detail">pagine Markdown governate</span></div>
    <div class="dsg-kpi"><span class="dsg-kpi__label">Architecture Package</span><span class="dsg-kpi__value">{program['architecture_packages']}</span><span class="dsg-kpi__detail">{program['completed_packages']} completati · {program['active_packages']} attivi</span></div>
    <div class="dsg-kpi"><span class="dsg-kpi__label">Assessment</span><span class="dsg-kpi__value">{assessment_count}</span><span class="dsg-kpi__detail">review e baseline certificate</span></div>
    <div class="dsg-kpi"><span class="dsg-kpi__label">Validation</span><span class="dsg-kpi__value">{validation_count}</span><span class="dsg-kpi__detail">evidenze e readiness gate</span></div>
  </div>
  <div class="dsg-program-panel">
    <article><span class="dsg-program-label">PACKAGE CORRENTE</span><span class="dsg-program-value">{esc(program['current_package'])} <span class="dsg-status-pill">{esc(program['project_status']).upper()}</span></span><span class="dsg-program-detail">{esc(program['current_title'])}</span></article>
    <article><span class="dsg-program-label">TARGET PROGRAMMA</span><span class="dsg-program-value">{esc(program['target'])}</span><span class="dsg-program-detail">Evoluzione governata della piattaforma scientifica.</span></article>
    <article><span class="dsg-program-label">BUILD</span><span class="dsg-program-value">{build_status}</span><span class="dsg-program-detail">Run {esc(run_number)} · branch {esc(branch)}</span></article>
    <article><span class="dsg-program-label">ULTIMO COMMIT</span><span class="dsg-program-value">{esc(short_sha)}</span><span class="dsg-program-detail">{esc(commit_title)}</span></article>
  </div>
</section>

<section class="dsg-program-section">
  <div class="dsg-section-intro"><span class="dsg-section-kicker">REPOSITORY INTELLIGENCE</span><h2>Salute e composizione del repository</h2></div>
  <div class="dsg-program-panel">
    <article><span class="dsg-program-label">ARCHITETTURA</span><span class="dsg-program-value">{adr_count} ADR</span><span class="dsg-program-detail">{program['architecture_packages']} package architetturali registrati.</span></article>
    <article><span class="dsg-program-label">AUTOMAZIONE</span><span class="dsg-program-value">{script_count} script</span><span class="dsg-program-detail">Python e PowerShell versionati.</span></article>
    <article><span class="dsg-program-label">PIPELINE</span><span class="dsg-program-value">{workflow_count} workflow</span><span class="dsg-program-detail">GitHub Actions presenti nel repository.</span></article>
    <article><span class="dsg-program-label">DIMENSIONE</span><span class="dsg-program-value">{repository_size}</span><span class="dsg-program-detail">Dimensione rilevata durante la build.</span></article>
  </div>
</section>

<section class="dsg-program-section">
  <div class="dsg-section-intro"><span class="dsg-section-kicker">OBSERVATORY &amp; SCIENTIFIC DATA</span><h2>Ultimo stato pubblicato</h2></div>
  <div class="dsg-kpi-grid">
    <div class="dsg-kpi"><span class="dsg-kpi__label">Sessioni</span><span class="dsg-kpi__value">{session_count}</span><span class="dsg-kpi__detail">storico disponibile</span></div>
    <div class="dsg-kpi"><span class="dsg-kpi__label">Integrazione</span><span class="dsg-kpi__value">{dec(total_integration)} h</span><span class="dsg-kpi__detail">totale acquisito</span></div>
    <div class="dsg-kpi"><span class="dsg-kpi__label">Immagini</span><span class="dsg-kpi__value">{completed_images}</span><span class="dsg-kpi__detail">light completati</span></div>
    <div class="dsg-kpi"><span class="dsg-kpi__label">Target</span><span class="dsg-kpi__value">{len(distinct_targets)}</span><span class="dsg-kpi__detail">oggetti distinti</span></div>
  </div>
  <div class="dsg-program-panel">
    <article><span class="dsg-program-label">ULTIMA SESSIONE</span><span class="dsg-program-value">{latest_rows['session']}</span><span class="dsg-program-detail">{latest_rows['date']}</span></article>
    <article><span class="dsg-program-label">TARGET</span><span class="dsg-program-value">{latest_rows['target']}</span><span class="dsg-program-detail">{latest_rows['config']}</span></article>
    <article><span class="dsg-program-label">ACQUISIZIONE</span><span class="dsg-program-value">{latest_rows['integration']}</span><span class="dsg-program-detail">{latest_rows['images']} immagini completate</span></article>
    <article><span class="dsg-program-label">QUALITÀ</span><span class="dsg-program-value">{latest_rows['status']}</span><span class="dsg-program-detail">RMS totale {latest_rows['rms']}</span></article>
  </div>
</section>

<section class="dsg-quick-section">
  <div class="dsg-section-intro"><span class="dsg-section-kicker">LIVE ACTIVITY</span><h2>Ultime attività versionate</h2><p>Timeline derivata dalla cronologia Git; non rappresenta telemetria in tempo reale.</p></div>
  <div class="dsg-quick-grid">{activity_markup(activity)}</div>
</section>

<div class="dsg-enterprise-meta"><strong>AGGIORNAMENTO AUTOMATICO</strong><span>Generato il {generated_at}</span><span>Prossima milestone: {esc(program['next_milestone'])}</span><span>Fonte: repository e dataset versionati.</span></div>
{END_MARKER}'''

    text = homepage.read_text(encoding="utf-8-sig")
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise RuntimeError("Homepage markers missing or invalid in docs/index.md")

    end += len(END_MARKER)
    homepage.write_text(text[:start] + block + text[end:], encoding="utf-8", newline="\n")

    print("Dynamic enterprise homepage updated successfully.")
    print(f"Documents: {document_count}")
    print(f"Architecture packages: {program['architecture_packages']}")
    print(f"Assessments: {assessment_count}")
    print(f"Validation documents: {validation_count}")
    print(f"Scripts: {script_count}")
    print(f"Workflows: {workflow_count}")
    print(f"Sessions: {session_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
