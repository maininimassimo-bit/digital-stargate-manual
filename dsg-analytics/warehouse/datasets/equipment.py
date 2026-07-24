"""Build the equipment warehouse dataset."""

from __future__ import annotations

import csv
from datetime import datetime
from math import isclose
from pathlib import Path
from typing import Any

import pandas as pd

from ..models import DatasetDefinition
from ..repository import WarehouseRepository


class EquipmentDatasetBuildError(RuntimeError):
    """Raised when the equipment dataset cannot be built."""


SOURCE_COLUMNS = (
    "configuration_id",
    "configuration_name",
    "telescope",
    "camera",
    "session_count",
    "total_duration_hours",
    "total_integration_hours",
    "integration_efficiency_pct",
    "light_started",
    "light_completed",
    "light_failed",
    "average_completion_pct",
    "average_rms_total_arcsec",
    "first_session_start",
    "last_session_end",
)


def _clean_text(value: object) -> str:
    """Return a stripped textual value."""

    if value is None:
        return ""

    return str(value).strip()


def _required_text(
    row: dict[str, str],
    column: str,
    row_number: int,
) -> str:
    """Return a required non-empty text field."""

    value = _clean_text(row.get(column))

    if not value:
        raise EquipmentDatasetBuildError(
            f"Row {row_number}: column '{column}' cannot be empty."
        )

    return value


def _required_int(
    row: dict[str, str],
    column: str,
    row_number: int,
) -> int:
    """Parse a required integer field."""

    raw_value = _required_text(
        row,
        column,
        row_number,
    )

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: column '{column}' must be "
                f"an integer, got {raw_value!r}."
            )
        ) from exc

    return value


def _required_float(
    row: dict[str, str],
    column: str,
    row_number: int,
) -> float:
    """Parse a required floating-point field."""

    raw_value = _required_text(
        row,
        column,
        row_number,
    )

    try:
        value = float(raw_value)
    except ValueError as exc:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: column '{column}' must be "
                f"numeric, got {raw_value!r}."
            )
        ) from exc

    return value


def _parse_datetime(
    row: dict[str, str],
    column: str,
    row_number: int,
) -> datetime:
    """Parse an ISO-8601 datetime field."""

    raw_value = _required_text(
        row,
        column,
        row_number,
    )

    try:
        return datetime.fromisoformat(
            raw_value.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: column '{column}' must contain "
                f"a valid ISO-8601 timestamp, got {raw_value!r}."
            )
        ) from exc


def _read_csv_rows(
    source_path: Path,
) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    """Read source CSV rows and return rows plus field names."""

    if not source_path.is_file():
        raise EquipmentDatasetBuildError(
            f"Equipment source file not found: {source_path}"
        )

    try:
        with source_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            reader = csv.DictReader(handle)

            if reader.fieldnames is None:
                raise EquipmentDatasetBuildError(
                    f"Equipment source has no header: {source_path}"
                )

            fieldnames = tuple(
                _clean_text(field)
                for field in reader.fieldnames
            )

            rows = [
                {
                    _clean_text(key): _clean_text(value)
                    for key, value in row.items()
                    if key is not None
                }
                for row in reader
            ]

    except OSError as exc:
        raise EquipmentDatasetBuildError(
            f"Unable to read equipment source {source_path}: {exc}"
        ) from exc

    if not rows:
        raise EquipmentDatasetBuildError(
            f"Equipment source contains no data rows: {source_path}"
        )

    return rows, fieldnames


def _validate_source_columns(
    fieldnames: tuple[str, ...],
) -> None:
    """Validate the configuration-summary source columns."""

    missing_columns = [
        column
        for column in SOURCE_COLUMNS
        if column not in fieldnames
    ]

    if missing_columns:
        raise EquipmentDatasetBuildError(
            (
                "Equipment source is missing required columns: "
                f"{missing_columns}"
            )
        )


def _transform_equipment_row(
    row: dict[str, str],
    row_number: int,
) -> dict[str, Any]:
    """Validate and transform one configuration summary row."""

    session_count = _required_int(
        row,
        "session_count",
        row_number,
    )
    total_duration_hours = _required_float(
        row,
        "total_duration_hours",
        row_number,
    )
    total_integration_hours = _required_float(
        row,
        "total_integration_hours",
        row_number,
    )
    integration_efficiency_pct = _required_float(
        row,
        "integration_efficiency_pct",
        row_number,
    )
    light_started = _required_int(
        row,
        "light_started",
        row_number,
    )
    light_completed = _required_int(
        row,
        "light_completed",
        row_number,
    )
    light_failed = _required_int(
        row,
        "light_failed",
        row_number,
    )
    average_completion_pct = _required_float(
        row,
        "average_completion_pct",
        row_number,
    )
    average_rms_total_arcsec = _required_float(
        row,
        "average_rms_total_arcsec",
        row_number,
    )

    first_session_start = _parse_datetime(
        row,
        "first_session_start",
        row_number,
    )
    last_session_end = _parse_datetime(
        row,
        "last_session_end",
        row_number,
    )

    if session_count <= 0:
        raise EquipmentDatasetBuildError(
            f"Row {row_number}: session_count must be greater than zero."
        )

    if total_duration_hours < 0:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: total_duration_hours "
                "cannot be negative."
            )
        )

    if total_integration_hours < 0:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: total_integration_hours "
                "cannot be negative."
            )
        )

    if total_integration_hours > total_duration_hours:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: total_integration_hours cannot "
                "exceed total_duration_hours."
            )
        )

    if not 0 <= integration_efficiency_pct <= 100:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: integration_efficiency_pct "
                "must be between 0 and 100."
            )
        )

    if any(
        value < 0
        for value in (
            light_started,
            light_completed,
            light_failed,
        )
    ):
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: light frame counters "
                "cannot be negative."
            )
        )

    if light_completed + light_failed != light_started:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: light_started must equal "
                "light_completed + light_failed."
            )
        )

    if not 0 <= average_completion_pct <= 100:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: average_completion_pct "
                "must be between 0 and 100."
            )
        )

    if average_rms_total_arcsec < 0:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: average_rms_total_arcsec "
                "cannot be negative."
            )
        )

    if last_session_end < first_session_start:
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: last_session_end cannot "
                "precede first_session_start."
            )
        )

    expected_efficiency = (
        0.0
        if total_duration_hours == 0
        else total_integration_hours
        / total_duration_hours
        * 100
    )

    if not isclose(
        integration_efficiency_pct,
        expected_efficiency,
        rel_tol=0.0,
        abs_tol=0.02,
    ):
        raise EquipmentDatasetBuildError(
            (
                f"Row {row_number}: integration_efficiency_pct "
                f"({integration_efficiency_pct}) is inconsistent with "
                "total_integration_hours / total_duration_hours "
                f"({expected_efficiency:.4f})."
            )
        )

    return {
        "configuration_id": _required_text(
            row,
            "configuration_id",
            row_number,
        ),
        "configuration_name": _required_text(
            row,
            "configuration_name",
            row_number,
        ),
        "telescope": _required_text(
            row,
            "telescope",
            row_number,
        ),
        "camera": _required_text(
            row,
            "camera",
            row_number,
        ),
        "session_count": session_count,
        "total_duration_hours": total_duration_hours,
        "total_integration_hours": total_integration_hours,
        "integration_efficiency_pct": integration_efficiency_pct,
        "light_started": light_started,
        "light_completed": light_completed,
        "light_failed": light_failed,
        "average_completion_pct": average_completion_pct,
        "average_rms_total_arcsec": average_rms_total_arcsec,
        "first_session_start": first_session_start,
        "last_session_end": last_session_end,
    }


def transform_equipment_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Transform and validate all equipment source rows."""

    transformed_rows = [
        _transform_equipment_row(
            row,
            row_number,
        )
        for row_number, row in enumerate(
            rows,
            start=2,
        )
    ]

    _validate_primary_key(
        transformed_rows
    )

    return transformed_rows


def _dataset_definition(
    repository: WarehouseRepository,
) -> DatasetDefinition:
    """Return the equipment dataset definition."""

    for dataset in repository.schema().datasets:
        if dataset.name == "equipment":
            return dataset

    raise EquipmentDatasetBuildError(
        "Warehouse schema does not define the equipment dataset."
    )


def _validate_output_columns(
    rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    """Ensure transformed rows match the warehouse schema."""

    expected_columns = tuple(definition.columns)

    for row_number, row in enumerate(
        rows,
        start=1,
    ):
        actual_columns = tuple(row.keys())

        if actual_columns != expected_columns:
            raise EquipmentDatasetBuildError(
                (
                    f"Transformed equipment row {row_number} does not "
                    "match the warehouse schema. "
                    f"Expected {expected_columns}, got {actual_columns}."
                )
            )


def _primary_key(
    row: dict[str, Any],
) -> tuple[Any, ...]:
    """Return the logical primary key for one equipment row."""

    return (row["configuration_id"],)


def _validate_primary_key(
    rows: list[dict[str, Any]],
) -> None:
    """Reject duplicate equipment primary keys."""

    seen: set[tuple[Any, ...]] = set()

    for row_number, row in enumerate(
        rows,
        start=1,
    ):
        key = _primary_key(row)

        if key in seen:
            raise EquipmentDatasetBuildError(
                (
                    "Duplicate equipment primary key at transformed "
                    f"row {row_number}: {key}"
                )
            )

        seen.add(key)


def _write_parquet_atomic(
    rows: list[dict[str, Any]],
    output_path: Path,
    columns: tuple[str, ...],
) -> None:
    """Write the equipment dataset atomically as Parquet."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = output_path.with_suffix(
        output_path.suffix + ".tmp"
    )

    frame = pd.DataFrame(
        rows,
        columns=list(columns),
    )

    try:
        frame.to_parquet(
            temporary_path,
            index=False,
            engine="pyarrow",
        )
        temporary_path.replace(output_path)
    except Exception as exc:
        temporary_path.unlink(missing_ok=True)

        raise EquipmentDatasetBuildError(
            f"Unable to write equipment dataset {output_path}: {exc}"
        ) from exc


def build_equipment_dataset(
    repository: WarehouseRepository,
) -> tuple[Path, int, Path]:
    """Build equipment.parquet from configuration-summary.csv."""

    source_path = (
        repository.repository_root
        / "data"
        / "analytics"
        / "history"
        / "configuration-summary.csv"
    )

    definition = _dataset_definition(
        repository
    )

    rows, fieldnames = _read_csv_rows(
        source_path
    )

    _validate_source_columns(
        fieldnames
    )

    transformed_rows = transform_equipment_rows(
        rows
    )

    _validate_output_columns(
        transformed_rows,
        definition,
    )

    output_path = repository.equipment_path()

    _write_parquet_atomic(
        transformed_rows,
        output_path,
        definition.columns,
    )

    return (
        output_path,
        len(transformed_rows),
        source_path,
    )
