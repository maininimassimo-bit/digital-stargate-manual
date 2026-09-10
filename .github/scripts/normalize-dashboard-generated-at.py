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

candidates = sorted(
    str(row.get("updated_at_utc") or "").strip()
    for row in rows
    if str(row.get("updated_at_utc") or "").strip()
)
if not candidates:
    raise SystemExit("Dashboard timestamp normalization failed: no updated_at_utc evidence available")

source_timestamp = candidates[-1]
text = DASHBOARD.read_text(encoding="utf-8")
pattern = r"(Generato automaticamente il )[^·\n]+( · Digital StarGate Analytics v3\.1)"
updated, count = re.subn(pattern, rf"\g<1>{source_timestamp}\g<2>", text, count=1)
if count != 1:
    raise SystemExit("Dashboard timestamp normalization failed: generated footer not found")

DASHBOARD.write_text(updated, encoding="utf-8")
print(f"Dashboard generated-at normalized to source evidence: {source_timestamp}")
