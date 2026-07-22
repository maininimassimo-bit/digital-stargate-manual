"""Build the sessions warehouse dataset."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from warehouse.models import DatasetDefinition
from warehouse.repository import WarehouseRepository


class SessionsDatasetBuildError(RuntimeError):
    """Raised when the sessions dataset cannot be built."""


def _clean_text(value: Any) -> str:
    """Return a stripped string or an empty string."""

    if value is None:
        return ""

    return str(value).strip()


def _optional_float(
    value: Any,
    *,
    field_name: str,
    session_id: str,
) -> float | None:
    """
    Convert an optional value to float.

    Empty values are converted to None. Invalid non-empty values raise
    a dataset build error.
    """

    text = _clean_text(value)

    if not text:
        return None

    try:
        return float(text)
    except (TypeError, ValueError) as exc:
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has an invalid floating-point "
                f"value for {field_name!r}: {value!r}"
            )
        ) from exc


def _optional_int(
    value: Any,
    *,
    field_name: str,
    session_id: str,
) -> int | None:
    """
    Convert an optional value to integer.

    Empty values are converted to None. Values such as ``1.0`` are
    accepted only when they represent an integer.
    """

    text = _clean_text(value)

    if not text:
        return None

    try:
        numeric_value = float(text)
    except (TypeError, ValueError) as exc:
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has an invalid integer value "
                f"for {field_name!r}: {value!r}"
            )
        ) from exc

    if not numeric_value.is_integer():
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has a non-integer value "
                f"for {field_name!r}: {value!r}"
            )
        )

    return int(numeric_value)


def _parse_datetime(
    value: Any,
    *,
    field_name: str,
    session_id: str,
) -> datetime:
    """Parse a required ISO-8601 datetime value."""

    text = _clean_text(value)

    if not text:
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has an empty "
                f"{field_name!r} value."
            )
        )

    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has an invalid "
                f"{field_name!r} value: {value!r}"
            )
        ) from exc


def _read_csv_rows(
    path: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    """Read the Analytics sessions CSV."""

    if not path.is_file():
        raise SessionsDatasetBuildError(
            f"Sessions Analytics source not found: {path}"
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
        raise SessionsDatasetBuildError(
            f"Unable to read sessions source {path}: {exc}"
        ) from exc

    if not fieldnames:
        raise SessionsDatasetBuildError(
            f"Sessions source has no header: {path}"
        )

    return fieldnames, rows


def _validate_source_columns(
    fieldnames: list[str],
) -> None:
    """Validate the minimum columns required from sessions.csv."""

    required_columns = {
        "schema_version",
        "session_id",
        "session_start",
        "session_end",
        "configuration_id",
        "telescope",
        "camera",
        "duration_hours",
        "integration_hours",
        "light_started",
        "light_completed",
        "light_failed",
        "completion_pct",
        "rms_ra_arcsec",
        "rms_dec_arcsec",
        "rms_total_arcsec",
        "autofocus_count",
        "autofocus_failed",
        "dither_count",
        "severity",
        "source_metrics_path",
        "updated_at_utc",
    }

    missing_columns = sorted(
        required_columns - set(fieldnames)
    )

    if missing_columns:
        raise SessionsDatasetBuildError(
            (
                "Sessions Analytics source is missing required "
                f"columns: {missing_columns}"
            )
        )


def _validate_unique_session_ids(
    rows: list[dict[str, Any]],
) -> None:
    """Ensure session_id is a valid primary key."""

    seen: set[str] = set()
    duplicates: set[str] = set()

    for row in rows:
        session_id = _clean_text(row.get("session_id"))

        if session_id in seen:
            duplicates.add(session_id)

        seen.add(session_id)

    if duplicates:
        raise SessionsDatasetBuildError(
            (
                "Duplicate session IDs detected: "
                f"{sorted(duplicates)}"
            )
        )


def _transform_session_row(
    source: dict[str, str],
    row_number: int,
) -> dict[str, Any]:
    """Transform one Analytics session into warehouse format."""

    session_id = _clean_text(source.get("session_id"))

    if not session_id:
        raise SessionsDatasetBuildError(
            (
                "Sessions Analytics source contains an empty "
                f"session_id at data row {row_number}."
            )
        )

    session_start = _parse_datetime(
        source.get("session_start"),
        field_name="session_start",
        session_id=session_id,
    )

    session_end = _parse_datetime(
        source.get("session_end"),
        field_name="session_end",
        session_id=session_id,
    )

    if session_end <= session_start:
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has an invalid time window: "
                f"{session_start.isoformat()} -> "
                f"{session_end.isoformat()}"
            )
        )

    duration_hours = _optional_float(
        source.get("duration_hours"),
        field_name="duration_hours",
        session_id=session_id,
    )

    integration_hours = _optional_float(
        source.get("integration_hours"),
        field_name="integration_hours",
        session_id=session_id,
    )

    if duration_hours is not None and duration_hours < 0:
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has negative "
                f"duration_hours: {duration_hours}"
            )
        )

    if integration_hours is not None and integration_hours < 0:
        raise SessionsDatasetBuildError(
            (
                f"Session {session_id!r} has negative "
                f"integration_hours: {integration_hours}"
            )
        )

    integration_efficiency_pct: float | None = None

    if duration_hours not in (None, 0.0):
        integration_efficiency_pct = round(
            ((integration_hours or 0.0) / duration_hours)
            * 100.0,
            4,
        )

    record: dict[str, Any] = {
        "schema_version": _clean_text(
            source.get("schema_version")
        ),
        "session_id": session_id,
        "session_start": session_start,
        "session_end": session_end,
        "session_date": session_start.date(),
        "configuration_id": _clean_text(
            source.get("configuration_id")
        ),
        "telescope": _clean_text(
            source.get("telescope")
        ),
        "camera": _clean_text(
            source.get("camera")
        ),
        "guide_profile": _clean_text(
            source.get("guide_profile")
        ),
        "duration_hours": duration_hours,
        "integration_hours": integration_hours,
        "integration_efficiency_pct": (
            integration_efficiency_pct
        ),
        "light_started": _optional_int(
            source.get("light_started"),
            field_name="light_started",
            session_id=session_id,
        ),
        "light_completed": _optional_int(
            source.get("light_completed"),
            field_name="light_completed",
            session_id=session_id,
        ),
        "light_failed": _optional_int(
            source.get("light_failed"),
            field_name="light_failed",
            session_id=session_id,
        ),
        "completion_pct": _optional_float(
            source.get("completion_pct"),
            field_name="completion_pct",
            session_id=session_id,
        ),
        "rms_ra_arcsec": _optional_float(
            source.get("rms_ra_arcsec"),
            field_name="rms_ra_arcsec",
            session_id=session_id,
        ),
        "rms_dec_arcsec": _optional_float(
            source.get("rms_dec_arcsec"),
            field_name="rms_dec_arcsec",
            session_id=session_id,
        ),
        "rms_total_arcsec": _optional_float(
            source.get("rms_total_arcsec"),
            field_name="rms_total_arcsec",
            session_id=session_id,
        ),
        "weather_safe_pct": _optional_float(
            source.get("weather_safe_pct"),
            field_name="weather_safe_pct",
            session_id=session_id,
        ),
        "autofocus_count": _optional_int(
            source.get("autofocus_count"),
            field_name="autofocus_count",
            session_id=session_id,
        ),
        "autofocus_failed": _optional_int(
            source.get("autofocus_failed"),
            field_name="autofocus_failed",
            session_id=session_id,
        ),
        "dither_count": _optional_int(
            source.get("dither_count"),
            field_name="dither_count",
            session_id=session_id,
        ),
        "dither_failed": _optional_int(
            source.get("dither_failed"),
            field_name="dither_failed",
            session_id=session_id,
        ),
        "severity": _clean_text(
            source.get("severity")
        ),
        "source_metrics_path": _clean_text(
            source.get("source_metrics_path")
        ),
        "updated_at_utc": _clean_text(
            source.get("updated_at_utc")
        ),
    }

    return record


def transform_session_rows(
    source_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Transform and validate all Analytics session rows."""

    output_rows = [
        _transform_session_row(
            source,
            row_number=index,
        )
        for index, source in enumerate(
            source_rows,
            start=2,
        )
    ]

    _validate_unique_session_ids(output_rows)

    return output_rows


def _validate_output_columns(
    output_rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    """Ensure transformed rows match the logical schema."""

    expected_columns = set(definition.columns)

    for index, row in enumerate(output_rows, start=1):
        actual_columns = set(row)

        missing_columns = sorted(
            expected_columns - actual_columns
        )
        unexpected_columns = sorted(
            actual_columns - expected_columns
        )

        if missing_columns or unexpected_columns:
            raise SessionsDatasetBuildError(
                (
                    f"Transformed sessions row {index} does not match "
                    f"the warehouse schema. Missing: {missing_columns}; "
                    f"unexpected: {unexpected_columns}"
                )
            )


def _dataset_definition(
    repository: WarehouseRepository,
) -> DatasetDefinition:
    """Return the logical definition of the sessions dataset."""

    for dataset in repository.schema().datasets:
        if dataset.name == "sessions":
            return dataset

    raise SessionsDatasetBuildError(
        "Warehouse schema does not define the sessions dataset."
    )


def _write_parquet_atomic(
    output_path: Path,
    rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    """Write the sessions Parquet file atomically."""

    try:
        import pandas as pd
    except ImportError as exc:
        raise SessionsDatasetBuildError(
            "pandas is required to build sessions.parquet."
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
        temporary_path.unlink(missing_ok=True)

        raise SessionsDatasetBuildError(
            f"Unable to write sessions dataset {output_path}: {exc}"
        ) from exc


def build_sessions_dataset(
    repository: WarehouseRepository,
) -> tuple[Path, int, Path]:
    """
    Build sessions.parquet from Analytics sessions.csv.

    Returns:
        Tuple containing output path, row count and source path.
    """

    source_path = (
        repository.repository_root
        / "data"
        / "analytics"
        / "history"
        / "sessions.csv"
    )

    fieldnames, source_rows = _read_csv_rows(source_path)
    _validate_source_columns(fieldnames)

    output_rows = transform_session_rows(source_rows)

    definition = _dataset_definition(repository)
    _validate_output_columns(
        output_rows,
        definition,
    )

    output_path = repository.sessions_path()

    _write_parquet_atomic(
        output_path,
        output_rows,
        definition,
    )

    return output_path, len(output_rows), source_path