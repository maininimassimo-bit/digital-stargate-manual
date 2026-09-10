#!/usr/bin/env python3
"""Fail if available full-window weather evidence is lost by analytics history."""
from __future__ import annotations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORY = ROOT / 'data/analytics/history/sessions.csv'

with HISTORY.open('r', encoding='utf-8-sig', newline='') as handle:
    rows = list(csv.DictReader(handle))

checked = 0
errors = []
for row in rows:
    source = str(row.get('source_metrics_path') or '').strip()
    if not source:
        continue
    path = ROOT / source
    if not path.exists():
        continue
    metrics = json.loads(path.read_text(encoding='utf-8-sig'))
    unsafe = metrics.get('weather', {}).get('weather_unsafe_pct_full_window')
    if unsafe is None or unsafe == '':
        continue
    try:
        expected = round(100.0 - float(unsafe), 2)
    except (TypeError, ValueError):
        continue
    if expected < 0.0 or expected > 100.0:
        continue
    checked += 1
    actual_raw = str(row.get('weather_safe_pct') or '').strip()
    try:
        actual = round(float(actual_raw), 2)
    except ValueError:
        errors.append(f"{row.get('session_id')}: weather evidence exists but weather_safe_pct is missing/invalid")
        continue
    if actual != expected:
        errors.append(f"{row.get('session_id')}: expected SAFE {expected:.2f}, got {actual:.2f}")

if errors:
    print('Analytics weather propagation FAILED')
    for error in errors:
        print(f'- {error}')
    raise SystemExit(1)

print(f'Analytics weather propagation PASS: {checked} sessions with governed full-window weather evidence')
print('Semantics: descriptive full-window analytics only; NO_SAFETY_AUTHORITY')
