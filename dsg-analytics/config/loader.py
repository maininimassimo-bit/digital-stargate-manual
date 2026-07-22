from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class PlatformConfigurationError(RuntimeError):
    """Raised when the platform configuration is missing or invalid."""


def load_platform_config(repo_root: Path) -> dict[str, Any]:
    """Load and validate the central platform configuration."""

    config_file = (
        repo_root
        / "dsg-analytics"
        / "config"
        / "platform.yml"
    )

    if not config_file.is_file():
        raise PlatformConfigurationError(
            f"Configuration file not found: {config_file}"
        )

    try:
        with config_file.open("r", encoding="utf-8") as stream:
            config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise PlatformConfigurationError(
            f"Invalid YAML configuration: {config_file}"
        ) from exc

    if not isinstance(config, dict):
        raise PlatformConfigurationError(
            "The platform configuration must contain a YAML mapping."
        )

    platform = config.get("platform")

    if not isinstance(platform, dict):
        raise PlatformConfigurationError(
            "Missing or invalid 'platform' configuration section."
        )

    for required_field in ("name", "version"):
        if not platform.get(required_field):
            raise PlatformConfigurationError(
                f"Missing platform field: platform.{required_field}"
            )

    return config


def get_pipeline(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the configured build pipeline."""

    pipeline = config.get("pipeline")

    if not isinstance(pipeline, list):
        raise PlatformConfigurationError(
            "Missing or invalid 'pipeline' configuration section."
        )

    if not pipeline:
        raise PlatformConfigurationError(
            "The configured pipeline is empty."
        )

    return pipeline