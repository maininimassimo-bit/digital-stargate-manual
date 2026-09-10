#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SESSIONS = ROOT / "data/analytics/history/sessions.csv"
CONFIG_CSV = ROOT / "data/analytics/history/configuration-summary.csv"
CONFIG_MD = ROOT / "docs/analytics/configuration-summary.md"
DASHBOARD_MD = ROOT / "docs/analytics/dashboard.md"
HISTORY_MD = ROOT / "docs/analytics/history-validation.md"
COMPARISON_JSON = ROOT / "docs/data/session-comparison-projection.json"
ANALYTICS_INDEX = ROOT / "docs/analytics/index.md"


def fail(message: str) -> None:
    raise SystemExit(f"Analytics Center consistency FAILED: {message}")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


sessions = read_csv(SESSIONS)
session_count = len(sessions)
if session_count == 0:
    fail("sessions.csv is empty")

config_rows = read_csv(CONFIG_CSV)
try:
    config_count = sum(int(row.get("session_count") or 0) for row in config_rows)
except ValueError as exc:
    fail(f"invalid configuration session_count: {exc}")
if config_count != session_count:
    fail(f"configuration summary covers {config_count} sessions, history contains {session_count}")

config_md = read_text(CONFIG_MD)
for row in config_rows:
    configuration_id = str(row.get("configuration_id") or "").strip()
    expected = str(row.get("session_count") or "").strip()
    if configuration_id and f"ID: `{configuration_id}`" not in config_md:
        fail(f"configuration-summary.md missing {configuration_id}")
    if expected and f"Sessioni: **{expected}**" not in config_md:
        fail(f"configuration-summary.md missing session count {expected} for {configuration_id}")

dashboard = read_text(DASHBOARD_MD)
match = re.search(
    r'<div class="dsg-kpi-label">Sessioni</div><div class="dsg-kpi-value">(\d+)</div>',
    dashboard,
)
if not match:
    fail("dashboard.md does not expose the Sessioni KPI")
if int(match.group(1)) != session_count:
    fail(f"dashboard reports {match.group(1)} sessions, history contains {session_count}")

history = read_text(HISTORY_MD)
history_match = re.search(r"^- Sessioni: \*\*(\d+)\*\*$", history, flags=re.MULTILINE)
if not history_match:
    fail("history-validation.md does not expose session count")
if int(history_match.group(1)) != session_count:
    fail(f"history validation reports {history_match.group(1)} sessions, history contains {session_count}")

if not COMPARISON_JSON.exists():
    fail("session-comparison-projection.json is missing")
comparison = json.loads(COMPARISON_JSON.read_text(encoding="utf-8"))
coverage = comparison.get("catalogCoverage") or {}
if int(coverage.get("totalSessions") or -1) != session_count:
    fail(
        "session comparison catalog coverage does not match analytics history: "
        f"{coverage.get('totalSessions')} vs {session_count}"
    )

analytics_index = read_text(ANALYTICS_INDEX)
if "[Dashboard Analytics](dashboard/)" not in analytics_index:
    fail("Analytics Center does not link the native MkDocs dashboard")
if "dashboard.html" in analytics_index:
    fail("Analytics Center still references legacy dashboard.html")

print(
    "Analytics Center consistency PASS: "
    f"sessions={session_count}; configurations={len(config_rows)}; "
    f"comparison={coverage.get('includedSessions')}/{coverage.get('totalSessions')} comparable"
)
