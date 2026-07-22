"""Configuration loaders and validators for Digital StarGate."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class PlatformConfigurationError(RuntimeError):
    """Raised when a configuration file is invalid."""


def _load_yaml_mapping(
    config_file: Path,
    description: str,
) -> dict[str, Any]:
    if not config_file.is_file():
        raise PlatformConfigurationError(
            f"{description} file not found: {config_file}"
        )

    try:
        with config_file.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise PlatformConfigurationError(
            f"Invalid YAML in {config_file}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise PlatformConfigurationError(
            f"The {description.lower()} must contain a YAML mapping."
        )

    return data


def load_platform_config(repo_root: Path) -> dict[str, Any]:
    return _load_yaml_mapping(
        repo_root / "dsg-analytics" / "config" / "platform.yml",
        "Platform configuration",
    )


def load_pipeline_config(repo_root: Path) -> dict[str, Any]:
    return _load_yaml_mapping(
        repo_root / "dsg-analytics" / "config" / "pipeline.yml",
        "Pipeline configuration",
    )


def _validate_dependency_cycles(
    pipeline: list[dict[str, Any]],
) -> None:
    dependencies = {
        item["id"]: item["depends_on"]
        for item in pipeline
    }

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str, path: list[str]) -> None:
        if identifier in visiting:
            start = path.index(identifier)
            cycle = path[start:] + [identifier]
            raise PlatformConfigurationError(
                "Circular pipeline dependency detected: "
                + " -> ".join(cycle)
            )

        if identifier in visited:
            return

        visiting.add(identifier)
        path.append(identifier)

        for dependency in dependencies[identifier]:
            visit(dependency, path)

        path.pop()
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in dependencies:
        visit(identifier, [])


def get_pipeline(
    pipeline_config: dict[str, Any],
) -> list[dict[str, Any]]:
    raw_pipeline = pipeline_config.get("pipeline")

    if not isinstance(raw_pipeline, list) or not raw_pipeline:
        raise PlatformConfigurationError(
            "The pipeline configuration must contain a non-empty "
            "'pipeline' list."
        )

    identifiers: set[str] = set()
    normalized: list[dict[str, Any]] = []

    for position, item in enumerate(raw_pipeline, start=1):
        if not isinstance(item, dict):
            raise PlatformConfigurationError(
                f"Pipeline item {position} must be a YAML mapping."
            )

        for required in ("id", "name", "script"):
            if required not in item:
                raise PlatformConfigurationError(
                    f"Pipeline item {position} is missing '{required}'."
                )

        identifier = str(item["id"]).strip()
        name = str(item["name"]).strip()
        script = str(item["script"]).strip()
        enabled = item.get("enabled", True)
        depends_on = item.get("depends_on", [])

        if not identifier or not name or not script:
            raise PlatformConfigurationError(
                f"Pipeline item {position} contains empty required fields."
            )

        if identifier in identifiers:
            raise PlatformConfigurationError(
                f"Duplicate pipeline identifier: {identifier}"
            )

        if not isinstance(enabled, bool):
            raise PlatformConfigurationError(
                f"Pipeline item '{identifier}' has invalid 'enabled'."
            )

        if not isinstance(depends_on, list):
            raise PlatformConfigurationError(
                f"Pipeline item '{identifier}' must define "
                "'depends_on' as a list."
            )

        dependencies = [str(dep).strip() for dep in depends_on]

        identifiers.add(identifier)
        normalized.append(
            {
                "id": identifier,
                "name": name,
                "script": script,
                "enabled": enabled,
                "depends_on": dependencies,
            }
        )

    for item in normalized:
        for dependency in item["depends_on"]:
            if dependency not in identifiers:
                raise PlatformConfigurationError(
                    f"Pipeline item '{item['id']}' depends on unknown "
                    f"step '{dependency}'."
                )

    _validate_dependency_cycles(normalized)
    return normalized
