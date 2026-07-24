"""Warehouse builder for Digital StarGate Analytics."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .datasets import (
    build_equipment_dataset,
    build_quality_dataset,
    build_sessions_dataset,
    build_targets_dataset,
)
from .models import (
    WarehouseMetadata,
    WarehouseSchema,
    default_warehouse_schema,
)
from .repository import WarehouseRepository
from .validators import validate_schema


class WarehouseBuildError(RuntimeError):
    """Raised when warehouse initialization or build fails."""


def _atomic_write_json(
    path: Path,
    payload: dict[str, Any],
) -> None:
    """Write a JSON document atomically."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = path.with_suffix(
        path.suffix + ".tmp"
    )

    try:
        temporary_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(path)
    except OSError as exc:
        temporary_path.unlink(missing_ok=True)

        raise WarehouseBuildError(
            f"Unable to write {path}: {exc}"
        ) from exc


def initialize_warehouse(
    repository_root: Path,
    schema: WarehouseSchema | None = None,
) -> tuple[Path, Path]:
    """Initialize warehouse schema and metadata files."""

    effective_schema = (
        schema or default_warehouse_schema()
    )

    validate_schema(effective_schema)

    repository = WarehouseRepository(
        repository_root
    )

    repository.warehouse_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    metadata = WarehouseMetadata.architecture_ready(
        effective_schema
    )

    _atomic_write_json(
        repository.schema_path,
        effective_schema.to_dict(),
    )

    _atomic_write_json(
        repository.metadata_path,
        metadata.to_dict(),
    )

    return (
        repository.schema_path,
        repository.metadata_path,
    )


def _current_timestamp() -> str:
    """Return a local timezone-aware timestamp."""

    return datetime.now().astimezone().isoformat(
        timespec="seconds"
    )


def _relative_source_path(
    repository: WarehouseRepository,
    source_path: Path,
) -> str:
    """Return a portable repository-relative source path."""

    try:
        relative_path = source_path.resolve().relative_to(
            repository.repository_root
        )
    except ValueError:
        return source_path.as_posix()

    return relative_path.as_posix()


def build_warehouse(
    repository_root: Path,
) -> tuple[Path, Path, Path, Path, Path, Path]:
    """Initialize and populate the current warehouse datasets."""

    schema_path, metadata_path = initialize_warehouse(
        repository_root
    )

    repository = WarehouseRepository(
        repository_root
    )

    sessions_path, session_rows, sessions_source = (
        build_sessions_dataset(repository)
    )

    targets_path, target_rows, targets_source = (
        build_targets_dataset(repository)
    )

    equipment_path, equipment_rows, equipment_source = (
        build_equipment_dataset(repository)
    )

    quality_path, quality_rows, quality_sources = (
        build_quality_dataset(repository)
    )

    metadata = repository.metadata()
    now = _current_timestamp()

    relative_sessions_source = _relative_source_path(
        repository,
        sessions_source,
    )

    relative_targets_source = _relative_source_path(
        repository,
        targets_source,
    )

    relative_equipment_source = _relative_source_path(
        repository,
        equipment_source,
    )

    relative_quality_sources = [
        _relative_source_path(
            repository,
            source_path,
        )
        for source_path in quality_sources
    ]

    metadata["status"] = "partially_populated"
    metadata["updated_at"] = now

    metadata["source_files"] = [
        relative_sessions_source,
        relative_targets_source,
        relative_equipment_source,
        *relative_quality_sources,
    ]

    metadata["warnings"] = [
        (
            "Release 5.2 populates sessions.parquet, "
            "targets.parquet, equipment.parquet and "
            "quality.parquet. The weather dataset "
            "remains pending."
        )
    ]

    metadata["datasets"]["sessions"].update(
        {
            "rows": session_rows,
            "status": "populated",
            "source": relative_sessions_source,
            "updated_at": now,
        }
    )

    metadata["datasets"]["targets"].update(
        {
            "rows": target_rows,
            "status": "populated",
            "source": relative_targets_source,
            "updated_at": now,
        }
    )

    metadata["datasets"]["equipment"].update(
        {
            "rows": equipment_rows,
            "status": "populated",
            "source": relative_equipment_source,
            "updated_at": now,
        }
    )

    metadata["datasets"]["quality"].update(
        {
            "rows": quality_rows,
            "status": "populated",
            "source": relative_quality_sources,
            "updated_at": now,
        }
    )

    _atomic_write_json(
        metadata_path,
        metadata,
    )

    return (
        schema_path,
        metadata_path,
        sessions_path,
        targets_path,
        equipment_path,
        quality_path,
    )
