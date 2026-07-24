"""Build the weather warehouse dataset."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from ..models import DatasetDefinition
from ..repository import WarehouseRepository


class WeatherDatasetBuildError(RuntimeError):
    """Raised when the weather dataset cannot be built."""


SOURCE_COLUMNS = (
    "timestamp",
    "source",
    "temperature_c",
    "humidity_pct",
    "dew_point_c",
    "wind_speed_kmh",
    "wind_gust_kmh",
    "cloud_cover_pct",
    "rain_rate_mm_h",
    "pressure_hpa",
    "sqm_mag_arcsec2",
    "sky_temperature_c",
    "safe",
    "notes",
)

NUMERIC_COLUMNS = (
    "temperature_c",
    "humidity_pct",
    "dew_point_c",
    "wind_speed_kmh",
    "wind_gust_kmh",
    "cloud_cover_pct",
    "rain_rate_mm_h",
    "pressure_hpa",
    "sqm_mag_arcsec2",
    "sky_temperature_c",
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
        raise WeatherDatasetBuildError(
            f"Row {row_number}: column '{column}' cannot be empty."
        )

    return value



def _optional_text(
    row: dict[str, str],
    column: str,
) -> str:
    """Return an optional text field."""

    return _clean_text(row.get(column))



def _optional_float(
    row: dict[str, str],
    column: str,
    row_number: int,
) -> float | None:
    """Parse an optional floating-point field."""

    raw_value = _clean_text(row.get(column))

    if not raw_value:
        return None

    try:
        return float(raw_value)
    except ValueError as exc:
        raise WeatherDatasetBuildError(
            f"Row {row_number}: column '{column}' must be numeric, "
            f"got {raw_value!r}."
        ) from exc



def _parse_datetime(
    row: dict[str, str],
    column: str,
    row_number: int,
) -> datetime:
    """Parse a required ISO-8601 datetime field."""

    raw_value = _required_text(row, column, row_number)

    try:
        value = datetime.fromisoformat(
            raw_value.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise WeatherDatasetBuildError(
            f"Row {row_number}: column '{column}' must contain a valid "
            f"ISO-8601 timestamp, got {raw_value!r}."
        ) from exc

    if value.tzinfo is None:
        raise WeatherDatasetBuildError(
            f"Row {row_number}: column '{column}' must include a timezone, "
            f"got {raw_value!r}."
        )

    return value



def _parse_bool(
    row: dict[str, str],
    column: str,
    row_number: int,
) -> bool:
    """Parse a required boolean field."""

    raw_value = _required_text(
        row,
        column,
        row_number,
    ).casefold()

    if raw_value in {"true", "1", "yes", "y", "si", "sì"}:
        return True

    if raw_value in {"false", "0", "no", "n"}:
        return False

    raise WeatherDatasetBuildError(
        f"Row {row_number}: column '{column}' must contain a boolean "
        f"value, got {raw_value!r}."
    )



def _read_csv_rows(
    source_path: Path,
) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    """Read weather observations and return rows plus field names."""

    if not source_path.is_file():
        raise WeatherDatasetBuildError(
            f"Weather source file not found: {source_path}"
        )

    try:
        with source_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            reader = csv.DictReader(handle)

            if reader.fieldnames is None:
                raise WeatherDatasetBuildError(
                    f"Weather source has no header: {source_path}"
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
                if any(_clean_text(value) for value in row.values())
            ]
    except OSError as exc:
        raise WeatherDatasetBuildError(
            f"Unable to read weather source {source_path}: {exc}"
        ) from exc

    return rows, fieldnames



def _validate_source_columns(
    fieldnames: tuple[str, ...],
) -> None:
    """Validate the weather source columns."""

    missing_columns = [
        column
        for column in SOURCE_COLUMNS
        if column not in fieldnames
    ]

    if missing_columns:
        raise WeatherDatasetBuildError(
            "Weather source is missing required columns: "
            f"{missing_columns}"
        )



def _validate_optional_range(
    value: float | None,
    column: str,
    row_number: int,
    minimum: float | None = None,
    maximum: float | None = None,
    minimum_exclusive: bool = False,
) -> None:
    """Validate an optional numeric value against configured bounds."""

    if value is None:
        return

    if minimum is not None:
        invalid_minimum = (
            value <= minimum
            if minimum_exclusive
            else value < minimum
        )

        if invalid_minimum:
            operator = "greater than" if minimum_exclusive else "at least"
            raise WeatherDatasetBuildError(
                f"Row {row_number}: column '{column}' must be {operator} "
                f"{minimum}, got {value}."
            )

    if maximum is not None and value > maximum:
        raise WeatherDatasetBuildError(
            f"Row {row_number}: column '{column}' must be at most "
            f"{maximum}, got {value}."
        )



def _transform_weather_row(
    row: dict[str, str],
    row_number: int,
) -> dict[str, Any]:
    """Validate and transform one weather observation."""

    timestamp = _parse_datetime(
        row,
        "timestamp",
        row_number,
    )
    source = _required_text(
        row,
        "source",
        row_number,
    )

    values = {
        column: _optional_float(row, column, row_number)
        for column in NUMERIC_COLUMNS
    }

    _validate_optional_range(
        values["humidity_pct"],
        "humidity_pct",
        row_number,
        minimum=0,
        maximum=100,
    )
    _validate_optional_range(
        values["wind_speed_kmh"],
        "wind_speed_kmh",
        row_number,
        minimum=0,
    )
    _validate_optional_range(
        values["wind_gust_kmh"],
        "wind_gust_kmh",
        row_number,
        minimum=0,
    )
    _validate_optional_range(
        values["cloud_cover_pct"],
        "cloud_cover_pct",
        row_number,
        minimum=0,
        maximum=100,
    )
    _validate_optional_range(
        values["rain_rate_mm_h"],
        "rain_rate_mm_h",
        row_number,
        minimum=0,
    )
    _validate_optional_range(
        values["pressure_hpa"],
        "pressure_hpa",
        row_number,
        minimum=0,
        minimum_exclusive=True,
    )
    _validate_optional_range(
        values["sqm_mag_arcsec2"],
        "sqm_mag_arcsec2",
        row_number,
        minimum=0,
        minimum_exclusive=True,
    )

    wind_speed = values["wind_speed_kmh"]
    wind_gust = values["wind_gust_kmh"]

    if (
        wind_speed is not None
        and wind_gust is not None
        and wind_gust < wind_speed
    ):
        raise WeatherDatasetBuildError(
            f"Row {row_number}: wind_gust_kmh cannot be lower than "
            "wind_speed_kmh."
        )

    return {
        "timestamp": timestamp,
        "source": source,
        "temperature_c": values["temperature_c"],
        "humidity_pct": values["humidity_pct"],
        "dew_point_c": values["dew_point_c"],
        "wind_speed_kmh": values["wind_speed_kmh"],
        "wind_gust_kmh": values["wind_gust_kmh"],
        "cloud_cover_pct": values["cloud_cover_pct"],
        "rain_rate_mm_h": values["rain_rate_mm_h"],
        "pressure_hpa": values["pressure_hpa"],
        "sqm_mag_arcsec2": values["sqm_mag_arcsec2"],
        "sky_temperature_c": values["sky_temperature_c"],
        "safe": _parse_bool(row, "safe", row_number),
        "notes": _optional_text(row, "notes"),
    }



def transform_weather_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Transform and validate all weather source rows."""

    transformed_rows = [
        _transform_weather_row(row, row_number)
        for row_number, row in enumerate(rows, start=2)
    ]

    transformed_rows.sort(
        key=lambda row: (
            row["timestamp"],
            row["source"],
        )
    )

    _validate_primary_key(transformed_rows)

    return transformed_rows



def _dataset_definition(
    repository: WarehouseRepository,
) -> DatasetDefinition:
    """Return the weather dataset definition."""

    for dataset in repository.schema().datasets:
        if dataset.name == "weather":
            return dataset

    raise WeatherDatasetBuildError(
        "Warehouse schema does not define the weather dataset."
    )



def _validate_output_columns(
    rows: list[dict[str, Any]],
    definition: DatasetDefinition,
) -> None:
    """Ensure transformed rows match the warehouse schema."""

    expected_columns = tuple(definition.columns)

    if not rows:
        if expected_columns != SOURCE_COLUMNS:
            raise WeatherDatasetBuildError(
                "The empty weather dataset cannot be written because the "
                "warehouse schema columns do not match the weather source "
                f"contract. Expected {SOURCE_COLUMNS}, got "
                f"{expected_columns}."
            )
        return

    for row_number, row in enumerate(rows, start=1):
        actual_columns = tuple(row.keys())

        if actual_columns != expected_columns:
            raise WeatherDatasetBuildError(
                f"Transformed weather row {row_number} does not match the "
                f"warehouse schema. Expected {expected_columns}, got "
                f"{actual_columns}."
            )



def _primary_key(
    row: dict[str, Any],
) -> tuple[Any, ...]:
    """Return the logical primary key for one weather observation."""

    return (
        row["timestamp"],
        row["source"],
    )



def _validate_primary_key(
    rows: list[dict[str, Any]],
) -> None:
    """Reject duplicate weather primary keys."""

    seen: set[tuple[Any, ...]] = set()

    for row_number, row in enumerate(rows, start=1):
        key = _primary_key(row)

        if key in seen:
            raise WeatherDatasetBuildError(
                "Duplicate weather primary key at transformed row "
                f"{row_number}: {key}"
            )

        seen.add(key)



def _weather_frame(
    rows: list[dict[str, Any]],
    columns: tuple[str, ...],
) -> pd.DataFrame:
    """Create a typed weather DataFrame, including for an empty source."""

    frame = pd.DataFrame(
        rows,
        columns=list(columns),
    )

    frame["timestamp"] = pd.to_datetime(
        frame["timestamp"],
        utc=True,
    )

    for column in NUMERIC_COLUMNS:
        frame[column] = pd.to_numeric(
            frame[column],
            errors="coerce",
        ).astype("float64")

    frame["source"] = frame["source"].astype("string")
    frame["safe"] = frame["safe"].astype("bool")
    frame["notes"] = frame["notes"].astype("string")

    return frame



def _write_parquet_atomic(
    rows: list[dict[str, Any]],
    output_path: Path,
    columns: tuple[str, ...],
) -> None:
    """Write the weather dataset atomically as Parquet."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = output_path.with_suffix(
        output_path.suffix + ".tmp"
    )

    frame = _weather_frame(rows, columns)

    try:
        frame.to_parquet(
            temporary_path,
            index=False,
            engine="pyarrow",
        )
        temporary_path.replace(output_path)
    except Exception as exc:
        temporary_path.unlink(missing_ok=True)

        raise WeatherDatasetBuildError(
            f"Unable to write weather dataset {output_path}: {exc}"
        ) from exc



def build_weather_dataset(
    repository: WarehouseRepository,
) -> tuple[Path, int, Path]:
    """Build weather.parquet from weather-observations.csv."""

    source_path = (
        repository.repository_root
        / "data"
        / "analytics"
        / "weather"
        / "weather-observations.csv"
    )

    definition = _dataset_definition(repository)

    rows, fieldnames = _read_csv_rows(source_path)
    _validate_source_columns(fieldnames)

    transformed_rows = transform_weather_rows(rows)
    _validate_output_columns(transformed_rows, definition)

    output_path = repository.weather_path()

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
