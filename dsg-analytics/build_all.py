#!/usr/bin/env python3
"""Digital StarGate Analytics - Complete build pipeline."""
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

    command = [sys.executable, str(step.script), "--repo-root", str(repo_root)]

    print()
    print("=" * 78)
    print(f"STEP: {step.name}")
    print("=" * 78)
    print("Command:", " ".join(f'"{p}"' if " " in p else p for p in command))

    completed = subprocess.run(command, cwd=repo_root, check=False)

    if completed.returncode != 0:
        raise RuntimeError(
            f"Step '{step.name}' failed with exit code {completed.returncode}."
        )

    print(f"Completed: {step.name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the complete Digital StarGate Analytics build."
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--skip-dashboard", action="store_true")
    parser.add_argument("--skip-homepage", action="store_true")
    parser.add_argument("--skip-status", action="store_true")
    args = parser.parse_args()

    root = args.repo_root.resolve()
    analytics = root / "dsg-analytics"

    steps = [
        BuildStep(
            "Consolidate session history",
            analytics / "history" / "consolidate_history.py",
        ),
        BuildStep(
            "Build configuration summary",
            analytics / "configuration" / "build_configuration_summary.py",
        ),
        BuildStep(
            "Extract target metrics",
            analytics / "target" / "extract_target_metrics.py",
        ),
        BuildStep(
            "Build targets dataset",
            analytics / "target" / "build_targets.py",
        ),
    ]

    if not args.skip_dashboard:
        steps.append(
            BuildStep(
                "Build dashboard",
                analytics / "dashboard" / "build_dashboard.py",
            )
        )

    if not args.skip_status:
        steps.append(
            BuildStep(
                "Build Observatory Status",
                analytics / "status" / "build_observatory_status.py",
            )
        )

    if not args.skip_homepage:
        steps.append(
            BuildStep(
                "Update dynamic homepage",
                analytics / "homepage" / "build_homepage.py",
            )
        )

    started = datetime.now()

    print("=" * 78)
    print("DIGITAL STARGATE ANALYTICS - COMPLETE BUILD")
    print("=" * 78)
    print(f"Repository: {root}")
    print(f"Started at: {started.isoformat(timespec='seconds')}")
    print(f"Python: {sys.executable}")

    try:
        for step in steps:
            run_step(step, root)
    except (FileNotFoundError, RuntimeError) as exc:
        print()
        print("BUILD FAILED")
        print(str(exc))
        return 1

    finished = datetime.now()

    print()
    print("=" * 78)
    print("BUILD COMPLETED SUCCESSFULLY")
    print("=" * 78)
    print(f"Finished at: {finished.isoformat(timespec='seconds')}")
    print(f"Duration: {finished - started}")

    if not args.skip_dashboard:
        print("Dashboard rebuilt.")

    if not args.skip_status:
        print(
            "Observatory Status updated: "
            f"{root / 'docs' / 'status' / 'index.md'}"
        )

    if not args.skip_homepage:
        print(f"Homepage updated: {root / 'docs' / 'index.md'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
