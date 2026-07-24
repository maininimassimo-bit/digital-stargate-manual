"""Tests for the weather warehouse dataset."""

from __future__ import annotations

import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

DSG_ANALYTICS_ROOT = Path(__file__).resolve().parents[2]
if str(DSG_ANALYTICS_ROOT) not in sys.path:
    sys.path.insert(0, str(DSG_ANALYTICS_ROOT))

from warehouse.datasets.weather import (
    SOURCE_COLUMNS,
    WeatherDatasetBuildError,
    build_weather_dataset,
    transform_weather_rows,
)
from warehouse.repository import WarehouseRepository


class WeatherDatasetTests(unittest.TestCase):
    """Unit and filesystem tests for the weather dataset builder."""

    def setUp(self) -> None:
        self.temp_dir = Path(
            tempfile.mkdtemp(prefix="dsg_weather_test_")
        )
        self.source_dir = (
            self.temp_dir
            / "data"
            / "analytics"
            / "weather"
        )
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.source_path = (
            self.source_dir / "weather-observations.csv"
        )
        self.repository = WarehouseRepository(self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @staticmethod
    def _valid_row(**overrides: str) -> dict[str, str]:
        row = {
            "timestamp": "2026-07-24T22:15:00+02:00",
            "source": "AAG CloudWatcher",
            "temperature_c": "18.4",
            "humidity_pct": "63.2",
            "dew_point_c": "11.2",
            "wind_speed_kmh": "7.5",
            "wind_gust_kmh": "12.0",
            "cloud_cover_pct": "18.0",
            "rain_rate_mm_h": "0.0",
            "pressure_hpa": "1014.8",
            "sqm_mag_arcsec2": "20.45",
            "sky_temperature_c": "-14.2",
            "safe": "true",
            "notes": "Clear and stable",
        }
        row.update(overrides)
        return row

    def _write_csv(
        self,
        rows: list[dict[str, str]],
        fieldnames: tuple[str, ...] = SOURCE_COLUMNS,
    ) -> None:
        with self.source_path.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=list(fieldnames),
            )
            writer.writeheader()
            writer.writerows(rows)

    def test_transform_weather_rows(self) -> None:
        rows = [
            self._valid_row(),
            self._valid_row(
                timestamp="2026-07-24T22:10:00+02:00",
                source="Backup Sensor",
                safe="no",
                notes="",
            ),
        ]

        transformed = transform_weather_rows(rows)

        self.assertEqual(len(transformed), 2)
        self.assertEqual(
            transformed[0]["source"],
            "Backup Sensor",
        )
        self.assertFalse(transformed[0]["safe"])
        self.assertEqual(transformed[0]["notes"], "")
        self.assertEqual(transformed[1]["temperature_c"], 18.4)
        self.assertTrue(transformed[1]["safe"])
        self.assertIsNotNone(
            transformed[1]["timestamp"].tzinfo
        )

    def test_build_weather_dataset_with_valid_csv(self) -> None:
        self._write_csv(
            [
                self._valid_row(),
                self._valid_row(
                    timestamp="2026-07-24T22:20:00+02:00",
                    humidity_pct="64.0",
                    safe="false",
                ),
            ]
        )

        output_path, row_count, source_path = (
            build_weather_dataset(self.repository)
        )

        self.assertEqual(
            source_path.resolve(),
            self.source_path.resolve(),
        )
        self.assertEqual(row_count, 2)
        self.assertTrue(output_path.is_file())
        self.assertEqual(
            output_path,
            self.repository.weather_path(),
        )

        frame = pd.read_parquet(output_path)
        self.assertEqual(len(frame), 2)
        self.assertEqual(tuple(frame.columns), SOURCE_COLUMNS)
        self.assertTrue(
            pd.api.types.is_datetime64tz_dtype(
                frame["timestamp"].dtype
            )
        )
        self.assertEqual(str(frame["source"].dtype), "string")
        self.assertEqual(str(frame["safe"].dtype), "bool")
        self.assertEqual(
            str(frame["temperature_c"].dtype),
            "float64",
        )
        self.assertEqual(frame.iloc[0]["source"], "AAG CloudWatcher")

    def test_header_only_csv_creates_empty_parquet(self) -> None:
        self._write_csv([])

        output_path, row_count, source_path = (
            build_weather_dataset(self.repository)
        )

        self.assertEqual(
            source_path.resolve(),
            self.source_path.resolve(),
        )
        self.assertEqual(row_count, 0)
        self.assertTrue(output_path.is_file())

        frame = pd.read_parquet(output_path)
        self.assertTrue(frame.empty)
        self.assertEqual(tuple(frame.columns), SOURCE_COLUMNS)
        self.assertEqual(str(frame["safe"].dtype), "bool")
        self.assertEqual(
            str(frame["temperature_c"].dtype),
            "float64",
        )

    def test_missing_source_file_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "Weather source file not found",
        ):
            build_weather_dataset(self.repository)

    def test_missing_required_column_is_rejected(self) -> None:
        fieldnames = tuple(
            column
            for column in SOURCE_COLUMNS
            if column != "pressure_hpa"
        )
        row = self._valid_row()
        row.pop("pressure_hpa")
        self._write_csv([row], fieldnames=fieldnames)

        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "missing required columns",
        ):
            build_weather_dataset(self.repository)

    def test_duplicate_primary_key_is_rejected(self) -> None:
        self._write_csv(
            [
                self._valid_row(),
                self._valid_row(temperature_c="19.1"),
            ]
        )

        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "Duplicate weather primary key",
        ):
            build_weather_dataset(self.repository)

    def test_invalid_numeric_value_is_rejected(self) -> None:
        self._write_csv(
            [self._valid_row(humidity_pct="not-a-number")]
        )

        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "must be numeric",
        ):
            build_weather_dataset(self.repository)

    def test_invalid_timestamp_is_rejected(self) -> None:
        self._write_csv(
            [self._valid_row(timestamp="24/07/2026 22:15")]
        )

        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "valid ISO-8601 timestamp",
        ):
            build_weather_dataset(self.repository)

    def test_timestamp_without_timezone_is_rejected(self) -> None:
        self._write_csv(
            [self._valid_row(timestamp="2026-07-24T22:15:00")]
        )

        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "must include a timezone",
        ):
            build_weather_dataset(self.repository)

    def test_invalid_boolean_is_rejected(self) -> None:
        self._write_csv([self._valid_row(safe="perhaps")])

        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "must contain a boolean value",
        ):
            build_weather_dataset(self.repository)

    def test_out_of_range_values_are_rejected(self) -> None:
        invalid_rows = (
            ("humidity_pct", "101"),
            ("cloud_cover_pct", "-1"),
            ("rain_rate_mm_h", "-0.1"),
            ("pressure_hpa", "0"),
            ("sqm_mag_arcsec2", "0"),
        )

        for column, value in invalid_rows:
            with self.subTest(column=column, value=value):
                self._write_csv(
                    [self._valid_row(**{column: value})]
                )

                with self.assertRaises(
                    WeatherDatasetBuildError
                ):
                    build_weather_dataset(self.repository)

    def test_wind_gust_lower_than_wind_speed_is_rejected(self) -> None:
        self._write_csv(
            [
                self._valid_row(
                    wind_speed_kmh="20",
                    wind_gust_kmh="10",
                )
            ]
        )

        with self.assertRaisesRegex(
            WeatherDatasetBuildError,
            "wind_gust_kmh cannot be lower",
        ):
            build_weather_dataset(self.repository)

    def test_optional_numeric_values_may_be_empty(self) -> None:
        empty_values = {
            column: ""
            for column in (
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
        }
        self._write_csv([self._valid_row(**empty_values)])

        output_path, row_count, _ = build_weather_dataset(
            self.repository
        )

        self.assertEqual(row_count, 1)
        frame = pd.read_parquet(output_path)

        for column in empty_values:
            with self.subTest(column=column):
                self.assertTrue(pd.isna(frame.iloc[0][column]))


if __name__ == "__main__":
    unittest.main()
