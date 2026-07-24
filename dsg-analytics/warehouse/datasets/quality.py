"""Build the quality warehouse dataset."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import datetime
from math import sqrt
from pathlib import Path
from typing import Any

import pandas as pd

from ..models import DatasetDefinition
from ..repository import WarehouseRepository


class QualityDatasetBuildError(RuntimeError):
    """Raised when the quality dataset cannot be built."""


EXPOSURE_SOURCE_COLUMNS = (
    "session_id",
    "timestamp",
    "filename",
    "frame_type",
    "exposure_seconds",
    "target_name",
    "camera_temperature_c",
    "filter_name",
)

SUMMARY_SOURCE_COLUMNS = (
    "session_id",
    "target_name",
    "filter_name",
    "image_count",
    "integration_seconds",
    "integration_hours",
    "first_timestamp",
    "last_timestamp",
)

FWHM_PATTERN = re.compile(
    r"(?:^|_)FWHM_(?P<value>[0-9]+(?:\.[0-9]+)?)(?:_|\.|$)",
    re.IGNORECASE,
)


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _read_csv_rows(
    source_path: Path,
    source_name: str,
) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    if not source_path.is_file():
        raise QualityDatasetBuildError(
            f"{source_name} source file not found: {source_path}"
        )

    try:
        with source_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            reader = csv.DictReader(handle)

            if reader.fieldnames is None:
                raise QualityDatasetBuildError(
                    f"{source_name} source has no header: {source_path}"
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
        raise QualityDatasetBuildError(
            f"Unable to read {source_name} source {source_path}: {exc}"
        ) from exc

    if not rows:
        raise QualityDatasetBuildError(
            f"{source_name} source contains no data rows: {source_path}"
        )

    return rows, fieldnames


def _validate_source_columns(
    fieldnames: tuple[str, ...],
    required_columns: tuple[str, ...],
    source_name: str,
) -> None:
    missing = [
        column
        for column in required_columns
        if column not in fieldnames
    ]

    if missing:
        raise QualityDatasetBuildError(
            f"{source_name} source is missing required columns: {missing}"
        )


def _required_text(
    row: dict[str, str],
    column: str,
    row_number: int,
    source_name: str,
) -> str:
    value = _clean_text(row.get(column))

    if not value:
        raise QualityDatasetBuildError(
            f"{source_name} row {row_number}: "
            f"column '{column}' cannot be empty."
        )

    return value


def _required_float(
    row: dict[str, str],
    column: str,
    row_number: int,
    source_name: str,
) -> float:
    raw_value = _required_text(
        row,
        column,
        row_number,
        source_name,
    )

    try:
        return float(raw_value)
    except ValueError as exc:
        raise QualityDatasetBuildError(
            f"{source_name} row {row_number}: "
            f"column '{column}' must be numeric, got {raw_value!r}."
        ) from exc


def _required_int(
    row: dict[str, str],
    column: str,
    row_number: int,
    source_name: str,
) -> int:
    raw_value = _required_text(
        row,
        column,
        row_number,
        source_name,
    )

    try:
        return int(raw_value)
    except ValueError as exc:
        raise QualityDatasetBuildError(
            f"{source_name} row {row_number}: "
            f"column '{column}' must be an integer, got {raw_value!r}."
        ) from exc


def _parse_datetime_text(
    row: dict[str, str],
    column: str,
    row_number: int,
    source_name: str,
) -> datetime:
    raw_value = _required_text(
        row,
        column,
        row_number,
        source_name,
    )

    try:
        return datetime.fromisoformat(
            raw_value.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise QualityDatasetBuildError(
            f"{source_name} row {row_number}: "
            f"column '{column}' must contain a valid ISO-8601 "
            f"timestamp, got {raw_value!r}."
        ) from exc


def extract_fwhm(filename: str) -> float:
    """Extract the FWHM value embedded in a N.I.N.A. filename."""

    match = FWHM_PATTERN.search(filename)

    if match is None:
        raise QualityDatasetBuildError(
            f"Filename does not contain a valid FWHM token: {filename!r}"
        )

    value = float(match.group("value"))

    if value <= 0:
        raise QualityDatasetBuildError(
            f"FWHM must be greater than zero in filename: {filename!r}"
        )

    return value


def _sample_stddev(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0

    mean = sum(values) / len(values)
    variance = sum(
        (value - mean) ** 2
        for value in values
    ) / (len(values) - 1)

    return sqrt(variance)


def transform_quality_rows(
    exposure_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Aggregate quality metrics by session, target and filter."""

    summary_by_key: dict[
        tuple[str, str, str],
        dict[str, Any],
    ] = {}

    for row_number, row in enumerate(summary_rows, start=2):
        key = (
            _required_text(row, "session_id", row_number, "target-summary"),
            _required_text(row, "target_name", row_number, "target-summary"),
            _required_text(row, "filter_name", row_number, "target-summary"),
        )

        if key in summary_by_key:
            raise QualityDatasetBuildError(
                f"Duplicate target-summary key at row {row_number}: {key}"
            )

        image_count = _required_int(
            row, "image_count", row_number, "target-summary"
        )
        integration_hours = _required_float(
            row, "integration_hours", row_number, "target-summary"
        )
        first_timestamp = _parse_datetime_text(
            row, "first_timestamp", row_number, "target-summary"
        )
        last_timestamp = _parse_datetime_text(
            row, "last_timestamp", row_number, "target-summary"
        )

        if image_count <= 0:
            raise QualityDatasetBuildError(
                f"target-summary row {row_number}: image_count must be greater than zero."
            )

        if integration_hours < 0:
            raise QualityDatasetBuildError(
                f"target-summary row {row_number}: integration_hours cannot be negative."
            )

        if last_timestamp < first_timestamp:
            raise QualityDatasetBuildError(
                f"target-summary row {row_number}: last_timestamp cannot precede first_timestamp."
            )

        summary_by_key[key] = {
            "image_count": image_count,
            "integration_hours": integration_hours,
            "first_timestamp": first_timestamp,
            "last_timestamp": last_timestamp,
        }

    grouped: dict[tuple[str, str, str], dict[str, list[float]]] = defaultdict(
        lambda: {"fwhm": [], "camera_temperature": []}
    )

    for row_number, row in enumerate(exposure_rows, start=2):
        session_id = _required_text(
            row, "session_id", row_number, "target-exposures"
        )
        target_name = _required_text(
            row, "target_name", row_number, "target-exposures"
        )
        filter_name = _required_text(
            row, "filter_name", row_number, "target-exposures"
        )
        frame_type = _required_text(
            row, "frame_type", row_number, "target-exposures"
        ).upper()

        if frame_type != "LIGHT":
            continue

        filename = _required_text(
            row, "filename", row_number, "target-exposures"
        )
        fwhm = extract_fwhm(filename)
        camera_temperature = _required_float(
            row, "camera_temperature_c", row_number, "target-exposures"
        )

        key = (session_id, target_name, filter_name)
        grouped[key]["fwhm"].append(fwhm)
        grouped[key]["camera_temperature"].append(camera_temperature)

    if not grouped:
        raise QualityDatasetBuildError(
            "No LIGHT exposure with a valid FWHM value was found."
        )

    transformed_rows: list[dict[str, Any]] = []

    for key in sorted(grouped):
        if key not in summary_by_key:
            raise QualityDatasetBuildError(
                f"No target-summary row found for quality key {key}."
            )

        values = grouped[key]
        fwhm_values = values["fwhm"]
        temperature_values = values["camera_temperature"]
        summary = summary_by_key[key]

        if len(fwhm_values) != summary["image_count"]:
            raise QualityDatasetBuildError(
                f"Image count mismatch for {key}: target-exposures has "
                f"{len(fwhm_values)}, target-summary reports "
                f"{summary['image_count']}."
            )

        transformed_rows.append(
            {
                "session_id": key[0],
                "target_name": key[1],
                "filter_name": key[2],
                "image_count": len(fwhm_values),
                "average_fwhm": round(sum(fwhm_values) / len(fwhm_values), 4),
                "minimum_fwhm": round(min(fwhm_values), 4),
                "maximum_fwhm": round(max(fwhm_values), 4),
                "fwhm_stddev": round(_sample_stddev(fwhm_values), 4),
                "average_camera_temperature_c": round(
                    sum(temperature_values) / len(temperature_values), 4
                ),
                "integration_hours": summary["integration_hours"],
                "first_timestamp": summary["first_timestamp"],
                "last_timestamp": summary["last_timestamp"],
            }
        )

    _validate_primary_key(transformed_rows)
    return transformed_rows


def _dataset_definition(repository: WarehouseRepository) -> DatasetDefinition:
    for dataset in repository.schema().datasets:
        if dataset.name == "quality":
            return dataset

    raise QualityDatasetBuildError(
        "Warehouse schema does not define the quality dataset."
    )


def _validate_output_columns(
    rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    expected_columns = tuple(definition.columns)

    for row_number, row in enumerate(rows, start=1):
        actual_columns = tuple(row.keys())

        if actual_columns != expected_columns:
            raise QualityDatasetBuildError(
                f"Transformed quality row {row_number} does not match the "
                f"warehouse schema. Expected {expected_columns}, got "
                f"{actual_columns}."
            )


def _primary_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["session_id"],
        row["target_name"],
        row["filter_name"],
    )


def _validate_primary_key(rows: list[dict[str, Any]]) -> None:
    seen: set[tuple[Any, ...]] = set()

    for row_number, row in enumerate(rows, start=1):
        key = _primary_key(row)

        if key in seen:
            raise QualityDatasetBuildError(
                f"Duplicate quality primary key at transformed row "
                f"{row_number}: {key}"
            )

        seen.add(key)


def _write_parquet_atomic(
    rows: list[dict[str, Any]],
    output_path: Path,
    columns: tuple[str, ...],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    frame = pd.DataFrame(rows, columns=list(columns))

    try:
        frame.to_parquet(temporary_path, index=False, engine="pyarrow")
        temporary_path.replace(output_path)
    except Exception as exc:
        temporary_path.unlink(missing_ok=True)
        raise QualityDatasetBuildError(
            f"Unable to write quality dataset {output_path}: {exc}"
        ) from exc


def build_quality_dataset(
    repository: WarehouseRepository,
) -> tuple[Path, int, tuple[Path, Path]]:
    """Build quality.parquet from target exposure and summary CSVs."""

    history_root = (
        repository.repository_root / "data" / "analytics" / "history"
    )
    exposures_path = history_root / "target-exposures.csv"
    summary_path = history_root / "target-summary.csv"
    definition = _dataset_definition(repository)

    exposure_rows, exposure_fields = _read_csv_rows(
        exposures_path, "target-exposures"
    )
    summary_rows, summary_fields = _read_csv_rows(
        summary_path, "target-summary"
    )

    _validate_source_columns(
        exposure_fields, EXPOSURE_SOURCE_COLUMNS, "target-exposures"
    )
    _validate_source_columns(
        summary_fields, SUMMARY_SOURCE_COLUMNS, "target-summary"
    )

    transformed_rows = transform_quality_rows(exposure_rows, summary_rows)
    _validate_output_columns(transformed_rows, definition)

    output_path = repository.quality_path()
    _write_parquet_atomic(transformed_rows, output_path, definition.columns)

    return output_path, len(transformed_rows), (exposures_path, summary_path)
