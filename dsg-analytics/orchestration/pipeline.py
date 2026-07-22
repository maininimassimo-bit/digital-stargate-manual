"""Dependency-aware pipeline orchestration for Digital StarGate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


class PipelineOrchestrationError(RuntimeError):
    """Raised when a pipeline execution plan cannot be created."""


@dataclass(frozen=True)
class PipelineStep:
    identifier: str
    name: str
    script: Path
    depends_on: tuple[str, ...]


@dataclass(frozen=True)
class SkippedStep:
    identifier: str
    name: str
    reason: str


@dataclass(frozen=True)
class PipelinePlan:
    steps: tuple[PipelineStep, ...]
    skipped: tuple[SkippedStep, ...]


def _build_item_map(
    pipeline: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    item_map: dict[str, dict[str, Any]] = {}
    positions: dict[str, int] = {}

    for position, item in enumerate(pipeline):
        identifier = str(item["id"]).strip()

        if identifier in item_map:
            raise PipelineOrchestrationError(
                f"Duplicate pipeline identifier: {identifier}"
            )

        item_map[identifier] = item
        positions[identifier] = position

    return item_map, positions


def _resolve_skipped_steps(
    pipeline: list[dict[str, Any]],
    requested_skips: set[str],
) -> tuple[set[str], dict[str, str]]:
    item_map, _ = _build_item_map(pipeline)

    unknown = requested_skips.difference(item_map)
    if unknown:
        raise PipelineOrchestrationError(
            "Unknown requested pipeline skip identifiers: "
            + ", ".join(sorted(unknown))
        )

    skipped: set[str] = set()
    reasons: dict[str, str] = {}

    for item in pipeline:
        identifier = str(item["id"]).strip()
        if not item.get("enabled", True):
            skipped.add(identifier)
            reasons[identifier] = "disabled in pipeline.yml"

    for identifier in requested_skips:
        skipped.add(identifier)
        reasons[identifier] = "skipped from command line"

    changed = True
    while changed:
        changed = False

        for item in pipeline:
            identifier = str(item["id"]).strip()
            if identifier in skipped:
                continue

            dependencies = [
                str(dep).strip()
                for dep in item.get("depends_on", [])
            ]

            unavailable = [
                dep for dep in dependencies if dep in skipped
            ]

            if unavailable:
                skipped.add(identifier)
                reasons[identifier] = (
                    "dependency skipped: " + ", ".join(unavailable)
                )
                changed = True

    return skipped, reasons


def _topological_order(
    pipeline: list[dict[str, Any]],
    skipped: set[str],
) -> list[str]:
    item_map, positions = _build_item_map(pipeline)

    active = [
        str(item["id"]).strip()
        for item in pipeline
        if str(item["id"]).strip() not in skipped
    ]
    active_set = set(active)

    indegree = {identifier: 0 for identifier in active}
    dependents = {identifier: [] for identifier in active}

    for identifier in active:
        dependencies = [
            str(dep).strip()
            for dep in item_map[identifier].get("depends_on", [])
            if str(dep).strip() in active_set
        ]

        indegree[identifier] = len(dependencies)

        for dep in dependencies:
            dependents[dep].append(identifier)

    ready = sorted(
        [identifier for identifier, degree in indegree.items() if degree == 0],
        key=positions.__getitem__,
    )

    ordered: list[str] = []

    while ready:
        identifier = ready.pop(0)
        ordered.append(identifier)

        for dependent in sorted(
            dependents[identifier],
            key=positions.__getitem__,
        ):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
                ready.sort(key=positions.__getitem__)

    if len(ordered) != len(active):
        unresolved = sorted(
            active_set.difference(ordered),
            key=positions.__getitem__,
        )
        raise PipelineOrchestrationError(
            "Unable to resolve pipeline execution order. "
            "Possible circular dependency involving: "
            + ", ".join(unresolved)
        )

    return ordered


def create_pipeline_plan(
    analytics_root: Path,
    pipeline: list[dict[str, Any]],
    requested_skips: Iterable[str] = (),
) -> PipelinePlan:
    requested = {
        str(identifier).strip()
        for identifier in requested_skips
        if str(identifier).strip()
    }

    skipped_ids, reasons = _resolve_skipped_steps(
        pipeline,
        requested,
    )
    ordered_ids = _topological_order(pipeline, skipped_ids)
    item_map, positions = _build_item_map(pipeline)

    steps = tuple(
        PipelineStep(
            identifier=identifier,
            name=str(item_map[identifier]["name"]).strip(),
            script=analytics_root
            / Path(str(item_map[identifier]["script"]).strip()),
            depends_on=tuple(
                str(dep).strip()
                for dep in item_map[identifier].get("depends_on", [])
            ),
        )
        for identifier in ordered_ids
    )

    skipped = tuple(
        SkippedStep(
            identifier=identifier,
            name=str(item_map[identifier]["name"]).strip(),
            reason=reasons[identifier],
        )
        for identifier in sorted(
            skipped_ids,
            key=positions.__getitem__,
        )
    )

    if not steps:
        raise PipelineOrchestrationError(
            "No executable pipeline steps remain after skip resolution."
        )

    return PipelinePlan(steps=steps, skipped=skipped)
