"""Validation helpers for warehouse schemas and metadata."""

from __future__ import annotations

from .models import WarehouseSchema


class WarehouseValidationError(RuntimeError):
    """Raised when a warehouse schema is invalid."""


def validate_schema(schema: WarehouseSchema) -> None:
    """Validate structural invariants of the warehouse schema."""

    if schema.schema_version < 1:
        raise WarehouseValidationError(
            "Warehouse schema_version must be greater than zero."
        )

    if not schema.datasets:
        raise WarehouseValidationError(
            "Warehouse schema must define at least one dataset."
        )

    names: set[str] = set()
    filenames: set[str] = set()

    for dataset in schema.datasets:
        if not dataset.name.strip():
            raise WarehouseValidationError(
                "Dataset name cannot be empty."
            )

        if dataset.name in names:
            raise WarehouseValidationError(
                f"Duplicate dataset name: {dataset.name}"
            )
        names.add(dataset.name)

        if dataset.filename in filenames:
            raise WarehouseValidationError(
                f"Duplicate dataset filename: {dataset.filename}"
            )
        filenames.add(dataset.filename)

        if not dataset.filename.endswith(".parquet"):
            raise WarehouseValidationError(
                (
                    f"Dataset '{dataset.name}' must use a "
                    ".parquet filename."
                )
            )

        if not dataset.columns:
            raise WarehouseValidationError(
                f"Dataset '{dataset.name}' has no columns."
            )

        duplicate_columns = {
            column
            for column in dataset.columns
            if dataset.columns.count(column) > 1
        }
        if duplicate_columns:
            raise WarehouseValidationError(
                (
                    f"Dataset '{dataset.name}' has duplicate columns: "
                    f"{sorted(duplicate_columns)}"
                )
            )

        missing_keys = [
            key
            for key in dataset.primary_key
            if key not in dataset.columns
        ]
        if missing_keys:
            raise WarehouseValidationError(
                (
                    f"Dataset '{dataset.name}' primary key references "
                    f"unknown columns: {missing_keys}"
                )
            )
