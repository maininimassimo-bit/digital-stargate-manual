"""Repository API for Digital StarGate warehouse datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import WarehouseSchema, default_warehouse_schema


class WarehouseRepository:
    """
    Central path and metadata access layer for warehouse consumers.

    Dataset loading will be added during Sprint 2, when parquet
    population is introduced.
    """

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        self.warehouse_root = (
            self.repository_root
            / "data"
            / "analytics"
            / "warehouse"
        )

    @property
    def schema_path(self) -> Path:
        return self.warehouse_root / "warehouse-schema.json"

    @property
    def metadata_path(self) -> Path:
        return self.warehouse_root / "warehouse-metadata.json"

    def dataset_path(self, dataset_name: str) -> Path:
        schema = self.schema()
        definitions = {
            dataset.name: dataset
            for dataset in schema.datasets
        }

        try:
            definition = definitions[dataset_name]
        except KeyError as exc:
            raise KeyError(
                f"Unknown warehouse dataset: {dataset_name}"
            ) from exc

        return self.warehouse_root / definition.filename

    def schema(self) -> WarehouseSchema:
        """
        Return the code-defined schema.

        The persisted JSON representation is intended for audit,
        interoperability and future migrations.
        """

        return default_warehouse_schema()

    def metadata(self) -> dict[str, Any]:
        if not self.metadata_path.is_file():
            raise FileNotFoundError(
                f"Warehouse metadata not found: {self.metadata_path}"
            )

        with self.metadata_path.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        if not isinstance(data, dict):
            raise ValueError(
                "Warehouse metadata root must be a JSON object."
            )

        return data

    def is_initialized(self) -> bool:
        return (
            self.schema_path.is_file()
            and self.metadata_path.is_file()
        )

    def sessions_path(self) -> Path:
        return self.dataset_path("sessions")

    def targets_path(self) -> Path:
        return self.dataset_path("targets")

    def equipment_path(self) -> Path:
        return self.dataset_path("equipment")

    def weather_path(self) -> Path:
        return self.dataset_path("weather")

    def quality_path(self) -> Path:
        return self.dataset_path("quality")
