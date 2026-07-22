#!/usr/bin/env python3
"""Digital StarGate Analytics - Dependency-aware build pipeline."""

from __future__ import annotations

import argparse
import importlib.util
import logging
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from orchestration.pipeline import (
    PipelineOrchestrationError,
    PipelinePlan,
    PipelineStep,
    create_pipeline_plan,
)
from orchestration.reporting import (
    BuildExecutionReport,
    BuildReportingError,
    SkippedStepReport,
    StepExecutionReport,
    configure_build_logger,
    create_build_id,
    persist_build_report,
)


def load_module_from_file(
    module_name: str,
    module_path: Path,
) -> ModuleType:
    """Load a Python module from a file path."""

    if not module_path.is_file():
        raise FileNotFoundError(
            f"Configuration loader not found: {module_path}"
        )

    spec = importlib.util.spec_from_file_location(
        module_name,
        module_path,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Unable to load module from {module_path}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def load_configurations(
    repository_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load and validate platform and pipeline configuration."""

    loader = load_module_from_file(
        "dsg_config_loader",
        repository_root
        / "dsg-analytics"
        / "config"
        / "loader.py",
    )

    platform_config = loader.load_platform_config(
        repository_root
    )
    pipeline_config = loader.load_pipeline_config(
        repository_root
    )
    pipeline = loader.get_pipeline(pipeline_config)

    return platform_config, pipeline


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Build all Digital StarGate analytics outputs with "
            "dependency-aware orchestration and execution reports."
        )
    )

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root directory.",
    )
    parser.add_argument(
        "--skip-dashboard",
        action="store_true",
        help="Skip dashboard and dependent steps.",
    )
    parser.add_argument(
        "--skip-status",
        action="store_true",
        help="Skip status and dependent steps.",
    )
    parser.add_argument(
        "--skip-homepage",
        action="store_true",
        help="Skip homepage generation.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug-level console logging.",
    )

    return parser.parse_args()


def get_platform_name(
    configuration: dict[str, Any],
) -> str:
    """Return a human-readable platform name."""

    platform = configuration.get("platform", {})

    if isinstance(platform, dict):
        name = platform.get("name")

        if isinstance(name, str) and name.strip():
            return name.strip()

    return "Digital StarGate Analytics"


def create_execution_report(
    build_id: str,
    platform_name: str,
    repository_root: Path,
    pipeline_count: int,
    plan: PipelinePlan,
) -> BuildExecutionReport:
    """Create the initial in-memory build report."""

    step_reports = [
        StepExecutionReport(
            identifier=step.identifier,
            name=step.name,
            script=str(step.script),
            depends_on=list(step.depends_on),
        )
        for step in plan.steps
    ]

    skipped_reports = [
        SkippedStepReport(
            identifier=step.identifier,
            name=step.name,
            reason=step.reason,
        )
        for step in plan.skipped
    ]

    from datetime import datetime

    return BuildExecutionReport(
        build_id=build_id,
        platform_name=platform_name,
        repository_root=str(repository_root),
        started_at=datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        finished_at=None,
        duration_seconds=None,
        status="running",
        configured_steps=pipeline_count,
        executable_steps=len(plan.steps),
        steps=step_reports,
        skipped_steps=skipped_reports,
    )


def log_pipeline_plan(
    logger: logging.Logger,
    configured_count: int,
    plan: PipelinePlan,
) -> None:
    """Write the resolved execution plan to console and log file."""

    logger.info("Configured steps: %s", configured_count)
    logger.info("Executable steps: %s", len(plan.steps))
    logger.info("Execution order:")

    for position, step in enumerate(plan.steps, start=1):
        dependencies = (
            ", ".join(step.depends_on)
            if step.depends_on
            else "none"
        )

        logger.info(
            "  %s. %s (depends on: %s)",
            position,
            step.identifier,
            dependencies,
        )

    if plan.skipped:
        logger.info("Skipped steps:")

        for step in plan.skipped:
            logger.info(
                "  - %s: %s",
                step.identifier,
                step.reason,
            )


def run_step(
    step: PipelineStep,
    step_report: StepExecutionReport,
    repository_root: Path,
    logger: logging.Logger,
) -> None:
    """Run one pipeline step and update its execution report."""

    if not step.script.is_file():
        message = (
            f"Required script not found for step "
            f"'{step.identifier}' ({step.name}): {step.script}"
        )
        step_report.start()
        step_report.finish(
            status="failed",
            exit_code=None,
            error=message,
        )
        raise FileNotFoundError(message)

    command = [
        sys.executable,
        str(step.script),
        "--repo-root",
        str(repository_root),
    ]

    logger.info("")
    logger.info("=" * 72)
    logger.info("STEP: %s", step.identifier)
    logger.info("NAME: %s", step.name)
    logger.info("SCRIPT: %s", step.script)
    logger.info("=" * 72)
    logger.debug("Command: %s", command)

    step_report.start()

    try:
        completed = subprocess.run(
            command,
            cwd=repository_root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as exc:
        step_report.finish(
            status="failed",
            exit_code=None,
            error=str(exc),
        )
        raise

    if completed.stdout:
        for line in completed.stdout.rstrip().splitlines():
            logger.info(line)

    if completed.returncode != 0:
        message = (
            f"Step '{step.identifier}' failed with exit code "
            f"{completed.returncode}."
        )
        step_report.finish(
            status="failed",
            exit_code=completed.returncode,
            error=message,
        )
        raise RuntimeError(message)

    step_report.finish(
        status="success",
        exit_code=completed.returncode,
    )

    logger.info(
        "STEP COMPLETED: %s | duration: %.3f s",
        step.identifier,
        step_report.duration_seconds or 0.0,
    )


def persist_report_safely(
    repository_root: Path,
    report: BuildExecutionReport,
    logger: logging.Logger,
) -> None:
    """Persist report and log any persistence failure."""

    try:
        latest_path, history_path = persist_build_report(
            repository_root,
            report,
        )
    except BuildReportingError as exc:
        logger.error("REPORTING ERROR")
        logger.error("%s", exc)
        return

    logger.info("Latest report: %s", latest_path)
    logger.info("Build history: %s", history_path)


def main() -> int:
    """Run the complete build pipeline."""

    args = parse_arguments()

    repository_root = args.repo_root.resolve()
    analytics_root = repository_root / "dsg-analytics"
    build_id = create_build_id()

    try:
        logger, log_path = configure_build_logger(
            repository_root,
            build_id,
            verbose=args.verbose,
        )
    except (OSError, BuildReportingError) as exc:
        print()
        print("LOGGING ERROR")
        print(str(exc))
        return 1

    logger.info("")
    logger.info("=" * 72)
    logger.info("Digital StarGate Analytics")
    logger.info("RELEASE 4.2 BUILD PIPELINE")
    logger.info("Build ID: %s", build_id)
    logger.info("Repository root: %s", repository_root)
    logger.info("Log file: %s", log_path)
    logger.info("=" * 72)

    try:
        configuration, pipeline = load_configurations(
            repository_root
        )

        requested_skips: set[str] = set()

        if args.skip_dashboard:
            requested_skips.add("dashboard")

        if args.skip_status:
            requested_skips.add("status")

        if args.skip_homepage:
            requested_skips.add("homepage")

        plan = create_pipeline_plan(
            analytics_root=analytics_root,
            pipeline=pipeline,
            requested_skips=requested_skips,
        )

    except (
        FileNotFoundError,
        RuntimeError,
        OSError,
        ImportError,
        PipelineOrchestrationError,
    ) as exc:
        logger.error("")
        logger.error("CONFIGURATION ERROR")
        logger.error("%s", exc)
        return 1

    platform_name = get_platform_name(configuration)

    report = create_execution_report(
        build_id=build_id,
        platform_name=platform_name,
        repository_root=repository_root,
        pipeline_count=len(pipeline),
        plan=plan,
    )

    logger.info("Platform: %s", platform_name)
    log_pipeline_plan(logger, len(pipeline), plan)

    try:
        for step, step_report in zip(
            plan.steps,
            report.steps,
            strict=True,
        ):
            run_step(
                step=step,
                step_report=step_report,
                repository_root=repository_root,
                logger=logger,
            )

    except (
        FileNotFoundError,
        RuntimeError,
        OSError,
    ) as exc:
        report.finish(
            status="failed",
            error=str(exc),
        )

        logger.error("")
        logger.error("BUILD FAILED")
        logger.error("%s", exc)
        logger.error(
            "Build duration: %.3f s",
            report.duration_seconds or 0.0,
        )

        persist_report_safely(
            repository_root,
            report,
            logger,
        )

        return 1

    report.finish(status="success")

    logger.info("")
    logger.info("=" * 72)
    logger.info("BUILD COMPLETED SUCCESSFULLY")
    logger.info(
        "Build duration: %.3f s",
        report.duration_seconds or 0.0,
    )
    logger.info("=" * 72)

    persist_report_safely(
        repository_root,
        report,
        logger,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
