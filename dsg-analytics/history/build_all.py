#!/usr/bin/env python3
"""Digital StarGate Analytics 2.6 - unified local build pipeline.

Runs, in order:
1. Historical consolidation and validation
2. Configuration summary generation
3. HTML dashboard generation
4. Final output verification

Only Python standard-library modules are required.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

CONSOLIDATE_SCRIPT = SCRIPT_DIR / "consolidate_history.py"
SUMMARY_SCRIPT = SCRIPT_DIR / "build_configuration_summary.py"
DASHBOARD_SCRIPT = SCRIPT_DIR / "build_dashboard.py"

SESSIONS_CSV = REPO_ROOT / "data" / "analytics" / "history" / "sessions.csv"
CONFIGURATION_SUMMARY_CSV = (
    REPO_ROOT / "data" / "analytics" / "history" / "configuration-summary.csv"
)
VALIDATION_REPORT_JSON = (
    REPO_ROOT / "data" / "analytics" / "history" / "validation-report.json"
)
VALIDATION_REPORT_MD = REPO_ROOT / "docs" / "analytics" / "history-validation.md"
CONFIGURATION_SUMMARY_MD = (
    REPO_ROOT / "docs" / "analytics" / "configuration-summary.md"
)
DASHBOARD_HTML = REPO_ROOT / "docs" / "analytics" / "dashboard.html"


@dataclass
class StepResult:
    name: str
    success: bool
    elapsed_seconds: float
    return_code: int = 0
    detail: str = ""


def print_header() -> None:
    print("=" * 61)
    print("DIGITAL STARGATE ANALYTICS")
    print("Unified Build Pipeline 2.6")
    print("=" * 61)


def format_elapsed(seconds: float) -> str:
    return f"{seconds:.2f}s"


def run_python_step(
    name: str,
    script: Path,
    arguments: Optional[Iterable[str]] = None,
) -> StepResult:
    if not script.exists():
        return StepResult(
            name=name,
            success=False,
            elapsed_seconds=0.0,
            return_code=2,
            detail=f"Script non trovato: {script}",
        )

    command = [sys.executable, str(script)]
    if arguments:
        command.extend(arguments)

    print(f"\n[START] {name}")
    print("Comando:", " ".join(command))

    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    elapsed = time.perf_counter() - started

    if completed.stdout.strip():
        print(completed.stdout.rstrip())

    if completed.stderr.strip():
        print(completed.stderr.rstrip(), file=sys.stderr)

    success = completed.returncode == 0
    marker = "OK" if success else "ERRORE"
    print(f"[{marker}] {name} ({format_elapsed(elapsed)})")

    return StepResult(
        name=name,
        success=success,
        elapsed_seconds=elapsed,
        return_code=completed.returncode,
        detail="" if success else f"Codice di uscita {completed.returncode}",
    )


def read_csv_count(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def load_validation_report() -> dict:
    if not VALIDATION_REPORT_JSON.exists():
        return {}

    try:
        return json.loads(VALIDATION_REPORT_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def verify_output(path: Path, label: str) -> Optional[str]:
    if not path.exists():
        return f"{label}: file mancante ({path})"
    if path.stat().st_size == 0:
        return f"{label}: file vuoto ({path})"
    return None


def verification_step() -> StepResult:
    print("\n[START] Verifica artefatti finali")
    started = time.perf_counter()

    expected_outputs = (
        (SESSIONS_CSV, "Storico sessioni"),
        (CONFIGURATION_SUMMARY_CSV, "Riepilogo configurazioni CSV"),
        (VALIDATION_REPORT_JSON, "Report validazione JSON"),
        (VALIDATION_REPORT_MD, "Report validazione Markdown"),
        (CONFIGURATION_SUMMARY_MD, "Riepilogo configurazioni Markdown"),
        (DASHBOARD_HTML, "Dashboard HTML"),
    )

    problems = [
        problem
        for path, label in expected_outputs
        if (problem := verify_output(path, label)) is not None
    ]

    elapsed = time.perf_counter() - started

    if problems:
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        print(f"[ERRORE] Verifica artefatti finali ({format_elapsed(elapsed)})")
        return StepResult(
            name="Verifica artefatti finali",
            success=False,
            elapsed_seconds=elapsed,
            return_code=2,
            detail=f"{len(problems)} artefatti non validi",
        )

    print(f"[OK] Verifica artefatti finali ({format_elapsed(elapsed)})")
    return StepResult(
        name="Verifica artefatti finali",
        success=True,
        elapsed_seconds=elapsed,
    )


def print_summary(results: list[StepResult]) -> None:
    validation = load_validation_report()

    session_count = read_csv_count(SESSIONS_CSV)
    configuration_count = read_csv_count(CONFIGURATION_SUMMARY_CSV)
    error_count = int(validation.get("error_count", 0) or 0)
    warning_count = int(validation.get("warning_count", 0) or 0)
    validation_status = str(validation.get("status", "NON DISPONIBILE"))

    print("\n" + "=" * 61)
    print("RISULTATO BUILD")
    print("=" * 61)

    for result in results:
        marker = "OK" if result.success else "ERRORE"
        detail = f" - {result.detail}" if result.detail else ""
        print(
            f"{marker:<7} {result.name:<34} "
            f"{format_elapsed(result.elapsed_seconds):>8}{detail}"
        )

    print("-" * 61)
    print(f"Sessioni consolidate : {session_count}")
    print(f"Configurazioni        : {configuration_count}")
    print(f"Errori validazione    : {error_count}")
    print(f"Avvisi validazione    : {warning_count}")
    print(f"Stato validazione     : {validation_status}")
    print(f"Dashboard             : {DASHBOARD_HTML}")
    print("=" * 61)


def main() -> int:
    global REPO_ROOT
    global CONSOLIDATE_SCRIPT, SUMMARY_SCRIPT, DASHBOARD_SCRIPT
    global SESSIONS_CSV, CONFIGURATION_SUMMARY_CSV
    global VALIDATION_REPORT_JSON, VALIDATION_REPORT_MD
    global CONFIGURATION_SUMMARY_MD, DASHBOARD_HTML

    parser = argparse.ArgumentParser(
        description="Esegue l'intera pipeline Digital StarGate Analytics."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Radice del repository.",
    )
    parser.add_argument(
        "--mode",
        choices=("update", "rebuild", "check"),
        default="update",
        help="Modalita passata al consolidatore.",
    )
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Considera gli avvisi di validazione come errore di build.",
    )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="Non rigenera il riepilogo configurazioni.",
    )
    parser.add_argument(
        "--skip-dashboard",
        action="store_true",
        help="Non rigenera la dashboard HTML.",
    )
    args = parser.parse_args()

    REPO_ROOT = args.repo_root.resolve()
    script_dir = REPO_ROOT / "dsg-analytics" / "history"

    CONSOLIDATE_SCRIPT = script_dir / "consolidate_history.py"
    SUMMARY_SCRIPT = script_dir / "build_configuration_summary.py"
    DASHBOARD_SCRIPT = script_dir / "build_dashboard.py"

    SESSIONS_CSV = REPO_ROOT / "data" / "analytics" / "history" / "sessions.csv"
    CONFIGURATION_SUMMARY_CSV = (
        REPO_ROOT / "data" / "analytics" / "history" / "configuration-summary.csv"
    )
    VALIDATION_REPORT_JSON = (
        REPO_ROOT / "data" / "analytics" / "history" / "validation-report.json"
    )
    VALIDATION_REPORT_MD = (
        REPO_ROOT / "docs" / "analytics" / "history-validation.md"
    )
    CONFIGURATION_SUMMARY_MD = (
        REPO_ROOT / "docs" / "analytics" / "configuration-summary.md"
    )
    DASHBOARD_HTML = REPO_ROOT / "docs" / "analytics" / "dashboard.html"

    print_header()
    print(f"Repository : {REPO_ROOT}")
    print(f"Modalita   : {args.mode}")

    consolidate_args = ["--repo-root", str(REPO_ROOT), "--mode", args.mode]
    if args.strict_warnings:
        consolidate_args.append("--strict-warnings")

    results: list[StepResult] = []

    consolidate = run_python_step(
        "Consolidamento e validazione",
        CONSOLIDATE_SCRIPT,
        consolidate_args,
    )
    results.append(consolidate)

    if not consolidate.success:
        print_summary(results)
        print("\nBUILD FAILED: consolidamento non completato.")
        return consolidate.return_code or 2

    if not args.skip_summary:
        summary = run_python_step(
            "Riepilogo configurazioni",
            SUMMARY_SCRIPT,
        )
        results.append(summary)
        if not summary.success:
            print_summary(results)
            print("\nBUILD FAILED: riepilogo configurazioni non completato.")
            return summary.return_code or 2

    if not args.skip_dashboard:
        dashboard = run_python_step(
            "Generazione dashboard",
            DASHBOARD_SCRIPT,
        )
        results.append(dashboard)
        if not dashboard.success:
            print_summary(results)
            print("\nBUILD FAILED: dashboard non generata.")
            return dashboard.return_code or 2

    verification = verification_step()
    results.append(verification)

    print_summary(results)

    validation = load_validation_report()
    validation_errors = int(validation.get("error_count", 0) or 0)
    validation_warnings = int(validation.get("warning_count", 0) or 0)

    if not verification.success or validation_errors:
        print("\nBUILD FAILED")
        return 2

    if args.strict_warnings and validation_warnings:
        print("\nBUILD FAILED: sono presenti avvisi di validazione.")
        return 3

    print("\nBUILD SUCCESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
