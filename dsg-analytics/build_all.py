#!/usr/bin/env python3
"""Digital StarGate Analytics - Complete build pipeline.

Pipeline order:
1. Consolidate session history
2. Build configuration summary
3. Extract target exposure metrics from NINA logs
4. Build aggregated targets dataset
5. Build HTML dashboard

The script stops immediately if any stage fails.
Standard library only.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class BuildStep:
    name: str
    script: Path


def run_step(step: BuildStep, repo_root: Path) -> None:
    if not step.script.exists():
        raise FileNotFoundError(
            f"Required script not found for step '{step.name}': {step.script}"
        )

    command = [
        sys.executable,
        str(step.script),
        "--repo-root",
        str(repo_root),
    ]

    print()
    print("=" * 78)
    print(f"STEP: {step.name}")
    print("=" * 78)
    print("Command:", " ".join(f'"{part}"' if " " in part else part for part in command))

    completed = subprocess.run(
        command,
        cwd=repo_root,
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            f"Step '{step.name}' failed with exit code {completed.returncode}."
        )

    print(f"Completed: {step.name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the complete Digital StarGate Analytics build."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root; default is current directory.",
    )
    parser.add_argument(
        "--skip-dashboard",
        action="store_true",
        help="Run all data-generation steps without rebuilding the dashboard.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    analytics_root = repo_root / "dsg-analytics"

    steps = [
        BuildStep(
            "Consolidate session history",
            analytics_root / "history" / "consolidate_history.py",
        ),
        BuildStep(
            "Build configuration summary",
            analytics_root / "configuration" / "build_configuration_summary.py",
        ),
        BuildStep(
            "Extract target metrics",
            analytics_root / "target" / "extract_target_metrics.py",
        ),
        BuildStep(
            "Build targets dataset",
            analytics_root / "target" / "build_targets.py",
        ),
    ]

    if not args.skip_dashboard:
        steps.append(
            BuildStep(
                "Build dashboard",
                analytics_root / "dashboard" / "build_dashboard.py",
            )
        )

    started_at = datetime.now()

    print("=" * 78)
    print("DIGITAL STARGATE ANALYTICS - COMPLETE BUILD")
    print("=" * 78)
    print(f"Repository: {repo_root}")
    print(f"Started at: {started_at.isoformat(timespec='seconds')}")
    print(f"Python: {sys.executable}")

    try:
        for step in steps:
            run_step(step, repo_root)
    except (FileNotFoundError, RuntimeError) as exc:
        print()
        print("BUILD FAILED")
        print(str(exc))
        return 1

    finished_at = datetime.now()
    duration = finished_at - started_at

    print()
    print("=" * 78)
    print("BUILD COMPLETED SUCCESSFULLY")
    print("=" * 78)
    print(f"Finished at: {finished_at.isoformat(timespec='seconds')}")
    print(f"Duration: {duration}")
    print()
    print("Generated datasets:")
    print(f"- {repo_root / 'data' / 'analytics' / 'history' / 'sessions.csv'}")
    print(
        f"- {repo_root / 'data' / 'analytics' / 'history' / 'configuration-summary.csv'}"
    )
    print(
        f"- {repo_root / 'data' / 'analytics' / 'history' / 'target-exposures.csv'}"
    )
    print(f"- {repo_root / 'data' / 'analytics' / 'history' / 'targets.csv'}")

    if not args.skip_dashboard:
        print("Dashboard rebuild requested.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
