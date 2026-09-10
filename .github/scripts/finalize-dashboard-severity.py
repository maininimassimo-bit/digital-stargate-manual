#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SESSIONS = ROOT / "data/analytics/history/sessions.csv"
DASHBOARD = ROOT / "docs/analytics/dashboard.md"

with SESSIONS.open("r", encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

counts = {"GREEN": 0, "YELLOW": 0, "RED": 0}
for row in rows:
    severity = str(row.get("severity") or "").strip().upper()
    if severity in counts:
        counts[severity] += 1

text = DASHBOARD.read_text(encoding="utf-8")

# Clarify that weather is descriptive evidence over the imported CSV window only.
text = text.replace("Meteo sicuro medio", "Meteo SAFE full-window medio")
text = text.replace("disponibilità condizioni sicure", "media descrittiva su sessioni con evidence; NO_SAFETY_AUTHORITY")
text = text.replace("<th class=\"num\">Meteo %</th>", "<th class=\"num\">Meteo SAFE % (full-window)</th>")

# Replace the legacy OK card with explicit governed severity counts.
legacy_pattern = re.compile(
    r'<article class="dsg-card dsg-kpi-card"><div class="dsg-kpi-label">Sessioni OK</div>'
    r'<div class="dsg-kpi-value">[^<]*</div><div class="dsg-kpi-note">stato positivo esplicito</div></article>'
)
replacement = (
    '<article class="dsg-card dsg-kpi-card"><div class="dsg-kpi-label">Sessioni GREEN</div>'
    f'<div class="dsg-kpi-value">{counts["GREEN"]}</div><div class="dsg-kpi-note">severity governata GREEN</div></article>'
    '<article class="dsg-card dsg-kpi-card"><div class="dsg-kpi-label">Sessioni YELLOW</div>'
    f'<div class="dsg-kpi-value">{counts["YELLOW"]}</div><div class="dsg-kpi-note">severity governata YELLOW</div></article>'
    '<article class="dsg-card dsg-kpi-card"><div class="dsg-kpi-label">Sessioni RED</div>'
    f'<div class="dsg-kpi-value">{counts["RED"]}</div><div class="dsg-kpi-note">severity governata RED</div></article>'
)
text, replaced = legacy_pattern.subn(replacement, text, count=1)
if replaced != 1:
    raise SystemExit("Dashboard finalization failed: legacy Sessioni OK card not found")

# Align visual state classes with the governed GREEN/YELLOW/RED taxonomy.
text = re.sub(r'class="dsg-status [^"]+">GREEN</span>', 'class="dsg-status dsg-status-good">GREEN</span>', text)
text = re.sub(r'class="dsg-status [^"]+">YELLOW</span>', 'class="dsg-status dsg-status-warn">YELLOW</span>', text)
text = re.sub(r'class="dsg-status [^"]+">RED</span>', 'class="dsg-status dsg-status-bad">RED</span>', text)

DASHBOARD.write_text(text, encoding="utf-8")
print(
    "Dashboard severity finalization PASS: "
    f"GREEN={counts['GREEN']}; YELLOW={counts['YELLOW']}; RED={counts['RED']}"
)
