#!/usr/bin/env python3
"""Generate the dynamic Digital StarGate homepage block."""
from __future__ import annotations
import argparse, csv
from datetime import datetime
from pathlib import Path

START_MARKER = "<!-- DSG:AUTO-HOMEPAGE:START -->"
END_MARKER = "<!-- DSG:AUTO-HOMEPAGE:END -->"

def read_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Required dataset not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def as_float(value):
    try:
        return float((value or "0").strip().replace(",", "."))
    except ValueError:
        return 0.0

def as_int(value):
    return int(round(as_float(value)))

def as_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None

def dec(value, digits=2):
    return f"{value:.{digits}f}".replace(".", ",")

def date(value):
    parsed = as_dt(value)
    return parsed.strftime("%d/%m/%Y %H:%M") if parsed else "—"

def esc(value):
    text = str(value or "").strip()
    return text.replace("|", r"\|").replace("\n", " ") if text else "—"

def status(value):
    severity = (value or "").strip().upper()
    return {"GREEN":"🟢 GREEN", "YELLOW":"🟡 YELLOW", "RED":"🔴 RED"}.get(severity, esc(severity))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.repo_root.resolve()
    history = root / "data" / "analytics" / "history"
    sessions = read_csv(history / "sessions.csv")
    targets = read_csv(history / "targets.csv")
    homepage = root / "docs" / "index.md"
    if not homepage.exists():
        raise FileNotFoundError(f"Homepage not found: {homepage}")

    session_count = len(sessions)
    total_integration = sum(as_float(r.get("integration_hours")) for r in sessions)
    completed_images = sum(as_int(r.get("light_completed")) for r in sessions)
    distinct_targets = sorted({r.get("target_name", "").strip() for r in targets if r.get("target_name", "").strip()})
    latest = max(sessions, key=lambda r: as_dt(r.get("session_end")) or as_dt(r.get("session_start")) or datetime.min) if sessions else None

    if latest:
        sid = latest.get("session_id", "").strip()
        latest_targets = sorted({r.get("target_name", "").strip() for r in targets if r.get("session_id", "").strip() == sid and r.get("target_name", "").strip()})
        target_text = ", ".join(esc(x) for x in latest_targets) or "—"
        config = " · ".join(esc(x) for x in (latest.get("telescope", "").strip(), latest.get("camera", "").strip()) if x) or esc(latest.get("configuration_id"))
        latest_rows = {
            "session": esc(sid),
            "date": f"{date(latest.get('session_start'))} → {date(latest.get('session_end'))}",
            "target": target_text,
            "config": config,
            "integration": f"{dec(as_float(latest.get('integration_hours')))} h",
            "images": str(as_int(latest.get("light_completed"))),
            "rms": f"{dec(as_float(latest.get('rms_total_arcsec')), 3)} arcsec" if as_float(latest.get('rms_total_arcsec')) > 0 else "—",
            "status": status(latest.get("severity")),
        }
    else:
        latest_rows = {k:"—" for k in ("session","date","target","config","integration","images","rms","status")}

    block = f'''{START_MARKER}
<div class="dsg-kpi-grid">

<div class="dsg-kpi"><span class="dsg-kpi__label">Sessioni</span><span class="dsg-kpi__value">{session_count}</span><span class="dsg-kpi__detail">storico disponibile</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Integrazione</span><span class="dsg-kpi__value">{dec(total_integration)} h</span><span class="dsg-kpi__detail">totale acquisito</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Immagini</span><span class="dsg-kpi__value">{completed_images}</span><span class="dsg-kpi__detail">light completati</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Target</span><span class="dsg-kpi__value">{len(distinct_targets)}</span><span class="dsg-kpi__detail">oggetti distinti</span></div>

</div>

## Ultima sessione

| Campo | Valore |
|---|---|
| Sessione | `{latest_rows['session']}` |
| Data | {latest_rows['date']} |
| Target | {latest_rows['target']} |
| Configurazione | {latest_rows['config']} |
| Integrazione | {latest_rows['integration']} |
| Immagini completate | {latest_rows['images']} |
| RMS totale | {latest_rows['rms']} |
| Stato | {latest_rows['status']} |

{END_MARKER}'''

    text = homepage.read_text(encoding="utf-8-sig")
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise RuntimeError("Homepage markers missing or invalid in docs/index.md")
    end += len(END_MARKER)
    homepage.write_text(text[:start] + block + text[end:], encoding="utf-8", newline="\n")
    print("Dynamic homepage updated successfully.")
    print(f"Sessions: {session_count}")
    print(f"Integration hours: {dec(total_integration)}")
    print(f"Completed images: {completed_images}")
    print(f"Distinct targets: {len(distinct_targets)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
