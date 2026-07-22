#!/usr/bin/env python3
"""Digital StarGate Analytics - Complete build pipeline."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Any


@dataclass(frozen=True)
class BuildStep:
    """Single pipeline step."""

    identifier: str
    name: str
    script: Path


def run_step(step: BuildStep, repo_root: Path) -> None:
    """Run a single build step and stop the pipeline on failure."""

    if not step.script.is_file():
        raise FileNotFoundError(
            f"Required script not found for step "
            f"'{step.identifier}' ({step.name}): {step.script}"
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
    print(f"ID:   {step.identifier}")
    print("=" * 78)
    print(
        "Command:",
        " ".join(
            f'"{part}"' if " " in part else part
            for part in command
        ),
    )

    completed = subprocess.run(
        command,
        cwd=repo_root,
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            f"Step '{step.identifier}' failed "
            f"with exit code {completed.returncode}."
        )

    print(f"Completed: {step.name}")


def load_configuration_module(repo_root: Path) -> ModuleType:
    """Load the Digital StarGate configuration loader module."""

    loader_file = (
        repo_root
        / "dsg-analytics"
        / "config"
        / "loader.py"
    )

    if not loader_file.is_file():
        raise FileNotFoundError(
            f"Configuration loader not found: {loader_file}"
        )

    spec = importlib.util.spec_from_file_location(
        "dsg_platform_loader",
        loader_file,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Unable to load configuration loader: {loader_file}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def load_platform_configuration(
    repo_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load the platform configuration and configured pipeline."""

    module = load_configuration_module(repo_root)

    load_function = getattr(
        module,
        "load_platform_config",
        None,
    )

    pipeline_function = getattr(
        module,
        "get_pipeline",
        None,
    )

    if not callable(load_function):
        raise RuntimeError(
            "The configuration loader does not expose "
            "'load_platform_config(repo_root)'."
        )

    if not callable(pipeline_function):
        raise RuntimeError(
            "The configuration loader does not expose "
            "'get_pipeline(config)'."
        )

    config = load_function(repo_root)

    if not isinstance(config, dict):
        raise RuntimeError(
            "The platform configuration loader returned "
            "an invalid value."
        )

    pipeline = pipeline_function(config)

    if not isinstance(pipeline, list):
        raise RuntimeError(
            "The pipeline loader returned an invalid value."
        )

    return config, pipeline


def build_steps_from_config(
    analytics_root: Path,
    pipeline: list[dict[str, Any]],
    args: argparse.Namespace,
) -> list[BuildStep]:
    """Create executable build steps from platform.yml."""

    skip_identifiers = set()

    if args.skip_dashboard:
        skip_identifiers.add("dashboard")

    if args.skip_status:
        skip_identifiers.add("status")

    if args.skip_homepage:
        skip_identifiers.add("homepage")

    steps: list[BuildStep] = []
    identifiers: set[str] = set()

    for position, item in enumerate(pipeline, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(
                f"Pipeline item {position} must be a YAML mapping."
            )

        identifier = item.get("id")
        name = item.get("name")
        script = item.get("script")
        enabled = item.get("enabled", True)

        if not isinstance(identifier, str) or not identifier.strip():
            raise RuntimeError(
                f"Pipeline item {position} has an invalid or missing 'id'."
            )

        identifier = identifier.strip()

        if identifier in identifiers:
            raise RuntimeError(
                f"Duplicate pipeline identifier: {identifier}"
            )

        identifiers.add(identifier)

        if not isinstance(name, str) or not name.strip():
            raise RuntimeError(
                f"Pipeline step '{identifier}' "
                "has an invalid or missing 'name'."
            )

        if not isinstance(script, str) or not script.strip():
            raise RuntimeError(
                f"Pipeline step '{identifier}' "
                "has an invalid or missing 'script'."
            )

        if not isinstance(enabled, bool):
            raise RuntimeError(
                f"Pipeline step '{identifier}' "
                "must use true or false for 'enabled'."
            )

        if not enabled:
            print(
                f"Skipping disabled pipeline step: "
                f"{identifier} ({name})"
            )
            continue

        if identifier in skip_identifiers:
            print(
                f"Skipping pipeline step requested "
                f"from command line: {identifier}"
            )
            continue

        script_path = analytics_root / Path(script)

        steps.append(
            BuildStep(
                identifier=identifier,
                name=name.strip(),
                script=script_path,
            )
        )

    if not steps:
        raise RuntimeError(
            "No enabled pipeline steps are available for execution."
        )

    return steps


def main() -> int:
    """Run the complete Digital StarGate Analytics pipeline."""

    parser = argparse.ArgumentParser(
        description=(
            "Run the complete Digital StarGate Analytics build."
        )
    )

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--skip-dashboard",
        action="store_true",
    )
    parser.add_argument(
        "--skip-homepage",
        action="store_true",
    )
    parser.add_argument(
        "--skip-status",
        action="store_true",
    )

    args = parser.parse_args()

    root = args.repo_root.resolve()
    analytics_root = root / "dsg-analytics"

    try:
        config, pipeline = load_platform_configuration(root)

        steps = build_steps_from_config(
            analytics_root=analytics_root,
            pipeline=pipeline,
            args=args,
        )

    except (
        FileNotFoundError,
        RuntimeError,
        OSError,
        ImportError,
    ) as exc:
        print()
        print("CONFIGURATION ERROR")
        print(str(exc))
        return 1

    except Exception as exc:
        print()
        print("CONFIGURATION ERROR")
        print(
            "Unexpected error while loading "
            f"the platform configuration: {exc}"
        )
        return 1

    platform = config["platform"]
    started = datetime.now()

    print("=" * 78)
    print("DIGITAL STARGATE ANALYTICS - COMPLETE BUILD")
    print("=" * 78)
    print(f"Repository: {root}")
    print(
        f"Platform: "
        f"{platform['name']} {platform['version']}"
    )
    print(f"Configured steps: {len(pipeline)}")
    print(f"Executable steps: {len(steps)}")
    print(
        f"Started at: "
        f"{started.isoformat(timespec='seconds')}"
    )
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
    print(
        f"Finished at: "
        f"{finished.isoformat(timespec='seconds')}"
    )
    print(f"Duration: {finished - started}")

    executed_identifiers = {
        step.identifier
        for step in steps
    }

    if "dashboard" in executed_identifiers:
        print("Dashboard rebuilt.")

    if "status" in executed_identifiers:
        print(
            "Observatory Status updated: "
            f"{root / 'docs' / 'status' / 'index.md'}"
        )

    if "homepage" in executed_identifiers:
        print(
            f"Homepage updated: "
            f"{root / 'docs' / 'index.md'}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
