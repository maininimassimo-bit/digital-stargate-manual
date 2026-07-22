"""Build logging and reporting for Digital StarGate Analytics."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any


class BuildReportingError(RuntimeError):
    """Raised when build logging or report persistence fails."""


@dataclass
class StepExecutionReport:
    """Execution result for one pipeline step."""

    identifier: str
    name: str
    script: str
    depends_on: list[str]
    status: str = "pending"
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    exit_code: int | None = None
    error: str | None = None
    _started_perf_counter: float | None = field(
        default=None,
        repr=False,
        compare=False,
    )

    def start(self) -> None:
        self.status = "running"
        self.started_at = _now_iso()
        self._started_perf_counter = perf_counter()

    def finish(
        self,
        status: str,
        exit_code: int | None = None,
        error: str | None = None,
    ) -> None:
        self.status = status
        self.finished_at = _now_iso()
        self.exit_code = exit_code
        self.error = error

        if self._started_perf_counter is not None:
            self.duration_seconds = round(
                perf_counter() - self._started_perf_counter,
                3,
            )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("_started_perf_counter", None)
        return data


@dataclass
class SkippedStepReport:
    """Skipped pipeline step included in the build report."""

    identifier: str
    name: str
    reason: str


@dataclass
class BuildExecutionReport:
    """Complete build execution report."""

    build_id: str
    platform_name: str
    repository_root: str
    started_at: str
    finished_at: str | None
    duration_seconds: float | None
    status: str
    configured_steps: int
    executable_steps: int
    steps: list[StepExecutionReport]
    skipped_steps: list[SkippedStepReport]
    error: str | None = None
    _started_perf_counter: float = field(
        default_factory=perf_counter,
        repr=False,
        compare=False,
    )

    def finish(
        self,
        status: str,
        error: str | None = None,
    ) -> None:
        self.status = status
        self.error = error
        self.finished_at = _now_iso()
        self.duration_seconds = round(
            perf_counter() - self._started_perf_counter,
            3,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "build_id": self.build_id,
            "platform_name": self.platform_name,
            "repository_root": self.repository_root,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "status": self.status,
            "configured_steps": self.configured_steps,
            "executable_steps": self.executable_steps,
            "steps": [step.to_dict() for step in self.steps],
            "skipped_steps": [
                asdict(step)
                for step in self.skipped_steps
            ],
            "error": self.error,
        }


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(
        timespec="seconds"
    )


def create_build_id() -> str:
    """Create a sortable local-time build identifier."""

    return datetime.now().astimezone().strftime(
        "%Y%m%dT%H%M%S%z"
    )


def configure_build_logger(
    repository_root: Path,
    build_id: str,
    verbose: bool = False,
) -> tuple[logging.Logger, Path]:
    """Configure console and file logging for one build."""

    log_directory = (
        repository_root
        / "data"
        / "analytics"
        / "builds"
        / "logs"
    )
    log_directory.mkdir(parents=True, exist_ok=True)

    log_path = log_directory / f"build-{build_id}.log"

    logger = logging.getLogger("digital_stargate.build")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(
        logging.DEBUG if verbose else logging.INFO
    )
    console_handler.setFormatter(
        logging.Formatter("%(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger, log_path


def persist_build_report(
    repository_root: Path,
    report: BuildExecutionReport,
) -> tuple[Path, Path]:
    """
    Write the latest report and append one record to build history.

    Returns:
        Tuple containing latest-build.json and build-history.jsonl paths.
    """

    output_directory = (
        repository_root
        / "data"
        / "analytics"
        / "builds"
    )
    output_directory.mkdir(parents=True, exist_ok=True)

    latest_path = output_directory / "latest-build.json"
    history_path = output_directory / "build-history.jsonl"

    payload = report.to_dict()

    try:
        temporary_path = latest_path.with_suffix(".json.tmp")
        temporary_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(latest_path)

        with history_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            )

    except OSError as exc:
        raise BuildReportingError(
            f"Unable to persist build reports: {exc}"
        ) from exc

    return latest_path, history_path
