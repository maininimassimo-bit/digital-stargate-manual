"""Build the targets warehouse dataset."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from warehouse.models import DatasetDefinition
from warehouse.repository import WarehouseRepository


class TargetsDatasetBuildError(RuntimeError):
    """Raised when the targets dataset cannot be built."""


def _clean_text(value: Any) -> str:
    """Return a stripped string or an empty string."""

    if value is None:
        return ""

    return str(value).strip()


def _required_text(
    value: Any,
    *,
    field_name: str,
    row_number: int,
) -> str:
    """Read and validate a required text field."""

    text = _clean_text(value)

    if not text:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has an empty "
                f"{field_name!r} value."
            )
        )

    return text


def _optional_float(
    value: Any,
    *,
    field_name: str,
    row_number: int,
) -> float | None:
    """Convert an optional value to float."""

    text = _clean_text(value)

    if not text:
        return None

    try:
        return float(text)
    except (TypeError, ValueError) as exc:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has an invalid "
                f"floating-point value for {field_name!r}: "
                f"{value!r}"
            )
        ) from exc


def _optional_int(
    value: Any,
    *,
    field_name: str,
    row_number: int,
) -> int | None:
    """Convert an optional value to integer."""

    text = _clean_text(value)

    if not text:
        return None

    try:
        numeric_value = float(text)
    except (TypeError, ValueError) as exc:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has an invalid "
                f"integer value for {field_name!r}: {value!r}"
            )
        ) from exc

    if not numeric_value.is_integer():
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has a "
                f"non-integer value for {field_name!r}: "
                f"{value!r}"
            )
        )

    return int(numeric_value)


def _required_int(
    value: Any,
    *,
    field_name: str,
    row_number: int,
) -> int:
    """Convert a required value to integer."""

    converted = _optional_int(
        value,
        field_name=field_name,
        row_number=row_number,
    )

    if converted is None:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has an empty "
                f"{field_name!r} value."
            )
        )

    return converted


def _required_float(
    value: Any,
    *,
    field_name: str,
    row_number: int,
) -> float:
    """Convert a required value to float."""

    converted = _optional_float(
        value,
        field_name=field_name,
        row_number=row_number,
    )

    if converted is None:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has an empty "
                f"{field_name!r} value."
            )
        )

    return converted


def _parse_datetime(
    value: Any,
    *,
    field_name: str,
    row_number: int,
) -> datetime:
    """Parse a required ISO-8601 datetime value."""

    text = _required_text(
        value,
        field_name=field_name,
        row_number=row_number,
    )

    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has an invalid "
                f"{field_name!r} timestamp: {value!r}"
            )
        ) from exc


def _read_csv_rows(
    path: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    """Read the Analytics targets CSV."""

    if not path.is_file():
        raise TargetsDatasetBuildError(
            f"Targets Analytics source not found: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    except OSError as exc:
        raise TargetsDatasetBuildError(
            f"Unable to read targets source {path}: {exc}"
        ) from exc

    if not fieldnames:
        raise TargetsDatasetBuildError(
            f"Targets source has no header: {path}"
        )

    return fieldnames, rows


def _validate_source_columns(
    fieldnames: list[str],
) -> None:
    """Validate columns required from targets.csv."""

    required_columns = {
        "session_id",
        "target_name",
        "filter_name",
        "telescope",
        "frame_type",
        "binning",
        "gain",
        "offset",
        "image_count",
        "integration_seconds",
        "integration_hours",
        "average_exposure_seconds",
        "average_camera_temperature_c",
        "first_timestamp",
        "last_timestamp",
        "first_image_path",
        "last_image_path",
    }

    missing_columns = sorted(
        required_columns - set(fieldnames)
    )

    if missing_columns:
        raise TargetsDatasetBuildError(
            (
                "Targets Analytics source is missing required "
                f"columns: {missing_columns}"
            )
        )


def _transform_target_row(
    source: dict[str, str],
    row_number: int,
) -> dict[str, Any]:
    """Transform one Analytics target aggregate."""

    session_id = _required_text(
        source.get("session_id"),
        field_name="session_id",
        row_number=row_number,
    )

    target_name = _required_text(
        source.get("target_name"),
        field_name="target_name",
        row_number=row_number,
    )

    filter_name = _required_text(
        source.get("filter_name"),
        field_name="filter_name",
        row_number=row_number,
    )

    telescope = _required_text(
        source.get("telescope"),
        field_name="telescope",
        row_number=row_number,
    )

    frame_type = _required_text(
        source.get("frame_type"),
        field_name="frame_type",
        row_number=row_number,
    )

    binning = _required_text(
        source.get("binning"),
        field_name="binning",
        row_number=row_number,
    )

    gain = _required_int(
        source.get("gain"),
        field_name="gain",
        row_number=row_number,
    )

    offset = _required_int(
        source.get("offset"),
        field_name="offset",
        row_number=row_number,
    )

    image_count = _required_int(
        source.get("image_count"),
        field_name="image_count",
        row_number=row_number,
    )

    integration_seconds = _required_float(
        source.get("integration_seconds"),
        field_name="integration_seconds",
        row_number=row_number,
    )

    integration_hours = _required_float(
        source.get("integration_hours"),
        field_name="integration_hours",
        row_number=row_number,
    )

    average_exposure_seconds = _required_float(
        source.get("average_exposure_seconds"),
        field_name="average_exposure_seconds",
        row_number=row_number,
    )

    average_camera_temperature_c = _optional_float(
        source.get("average_camera_temperature_c"),
        field_name="average_camera_temperature_c",
        row_number=row_number,
    )

    first_timestamp = _parse_datetime(
        source.get("first_timestamp"),
        field_name="first_timestamp",
        row_number=row_number,
    )

    last_timestamp = _parse_datetime(
        source.get("last_timestamp"),
        field_name="last_timestamp",
        row_number=row_number,
    )

    if image_count <= 0:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has invalid "
                f"image_count: {image_count}"
            )
        )

    if integration_seconds < 0:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has negative "
                f"integration_seconds: {integration_seconds}"
            )
        )

    if integration_hours < 0:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has negative "
                f"integration_hours: {integration_hours}"
            )
        )

    if average_exposure_seconds <= 0:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has invalid "
                "average_exposure_seconds: "
                f"{average_exposure_seconds}"
            )
        )

    if last_timestamp < first_timestamp:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} has an invalid "
                "timestamp range: "
                f"{first_timestamp.isoformat()} -> "
                f"{last_timestamp.isoformat()}"
            )
        )

    acquisition_span_hours = round(
        (
            last_timestamp - first_timestamp
        ).total_seconds()
        / 3600.0,
        4,
    )

    expected_hours = integration_seconds / 3600.0

    if abs(expected_hours - integration_hours) > 0.001:
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} contains "
                "inconsistent integration values: "
                f"{integration_seconds} seconds versus "
                f"{integration_hours} hours."
            )
        )

    expected_integration_seconds = (
        image_count * average_exposure_seconds
    )

    tolerance_seconds = max(
        0.1,
        image_count * 0.01,
    )

    if (
        abs(
            expected_integration_seconds
            - integration_seconds
        )
        > tolerance_seconds
    ):
        raise TargetsDatasetBuildError(
            (
                f"Targets source row {row_number} contains "
                "inconsistent exposure totals: "
                f"{image_count} images x "
                f"{average_exposure_seconds} seconds != "
                f"{integration_seconds} seconds."
            )
        )

    return {
        "session_id": session_id,
        "target_name": target_name,
        "filter_name": filter_name,
        "telescope": telescope,
        "frame_type": frame_type,
        "binning": binning,
        "gain": gain,
        "offset": offset,
        "image_count": image_count,
        "integration_seconds": integration_seconds,
        "integration_hours": integration_hours,
        "average_exposure_seconds": (
            average_exposure_seconds
        ),
        "average_camera_temperature_c": (
            average_camera_temperature_c
        ),
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "acquisition_span_hours": (
            acquisition_span_hours
        ),
        "first_image_path": _required_text(
            source.get("first_image_path"),
            field_name="first_image_path",
            row_number=row_number,
        ),
        "last_image_path": _required_text(
            source.get("last_image_path"),
            field_name="last_image_path",
            row_number=row_number,
        ),
    }


def transform_target_rows(
    source_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Transform all Analytics target rows."""

    output_rows = [
        _transform_target_row(
            source,
            row_number=index,
        )
        for index, source in enumerate(
            source_rows,
            start=2,
        )
    ]

    return output_rows


def _dataset_definition(
    repository: WarehouseRepository,
) -> DatasetDefinition:
    """Return the logical targets definition."""

    for dataset in repository.schema().datasets:
        if dataset.name == "targets":
            return dataset

    raise TargetsDatasetBuildError(
        "Warehouse schema does not define targets."
    )


def _validate_output_columns(
    output_rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    """Ensure transformed rows match the schema."""

    expected_columns = set(definition.columns)

    for index, row in enumerate(
        output_rows,
        start=1,
    ):
        actual_columns = set(row)

        missing_columns = sorted(
            expected_columns - actual_columns
        )

        unexpected_columns = sorted(
            actual_columns - expected_columns
        )

        if missing_columns or unexpected_columns:
            raise TargetsDatasetBuildError(
                (
                    f"Transformed targets row {index} does not "
                    "match the warehouse schema. "
                    f"Missing: {missing_columns}; "
                    f"unexpected: {unexpected_columns}"
                )
            )


def _primary_key(
    row: dict[str, Any],
    definition: DatasetDefinition,
) -> tuple[Any, ...]:
    """Return a dataset primary-key tuple."""

    return tuple(
        row[column]
        for column in definition.primary_key
    )


def _validate_primary_key(
    output_rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    """Ensure the composite primary key is unique."""

    seen: set[tuple[Any, ...]] = set()
    duplicates: set[tuple[Any, ...]] = set()

    for row in output_rows:
        key = _primary_key(
            row,
            definition,
        )

        if key in seen:
            duplicates.add(key)

        seen.add(key)

    if duplicates:
        formatted_duplicates = [
            " | ".join(str(value) for value in key)
            for key in sorted(duplicates)
        ]

        raise TargetsDatasetBuildError(
            (
                "Duplicate targets primary keys detected: "
                f"{formatted_duplicates}"
            )
        )


def _write_parquet_atomic(
    output_path: Path,
    rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    """Write targets.parquet atomically."""

    try:
        import pandas as pd
    except ImportError as exc:
        raise TargetsDatasetBuildError(
            "pandas is required to build targets.parquet."
        ) from exc

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = output_path.with_suffix(
        output_path.suffix + ".tmp"
    )

    dataframe = pd.DataFrame(
        rows,
        columns=list(definition.columns),
    )

    try:
        dataframe.to_parquet(
            temporary_path,
            engine="pyarrow",
            index=False,
        )
        temporary_path.replace(output_path)
    except (
        ImportError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        temporary_path.unlink(
            missing_ok=True
        )

        raise TargetsDatasetBuildError(
            (
                f"Unable to write targets dataset "
                f"{output_path}: {exc}"
            )
        ) from exc


def build_targets_dataset(
    repository: WarehouseRepository,
) -> tuple[Path, int, Path]:
    """
    Build targets.parquet from Analytics targets.csv.

    Returns:
        Output path, row count and source path.
    """

    source_path = (
        repository.repository_root
        / "data"
        / "analytics"
        / "history"
        / "targets.csv"
    )

    fieldnames, source_rows = _read_csv_rows(
        source_path
    )

    _validate_source_columns(
        fieldnames
    )

    output_rows = transform_target_rows(
        source_rows
    )

    definition = _dataset_definition(
        repository
    )

    _validate_output_columns(
        output_rows,
        definition,
    )

    _validate_primary_key(
        output_rows,
        definition,
    )

    output_path = repository.targets_path()

    _write_parquet_atomic(
        output_path,
        output_rows,
        definition,
    )

    return (
        output_path,
        len(output_rows),
        source_path,
    )