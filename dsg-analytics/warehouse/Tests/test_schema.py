"""Tests for the Digital StarGate warehouse logical schema."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


DSG_ANALYTICS_ROOT = Path(__file__).resolve().parents[2]

if str(DSG_ANALYTICS_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(DSG_ANALYTICS_ROOT),
    )


from warehouse.models import default_warehouse_schema
from warehouse.validators import validate_schema


class WarehouseSchemaTests(unittest.TestCase):
    """Validate the structure of the logical warehouse schema."""

    def setUp(self) -> None:
        """Create a fresh schema for every test."""

        self.schema = default_warehouse_schema()

    def test_schema_is_valid(self) -> None:
        """The default schema must pass the central validator."""

        validate_schema(self.schema)

    def test_expected_datasets_are_defined(self) -> None:
        """The schema must expose all planned warehouse datasets."""

        expected_names = {
            "sessions",
            "targets",
            "equipment",
            "weather",
            "quality",
        }

        actual_names = {
            dataset.name
            for dataset in self.schema.datasets
        }

        self.assertEqual(
            expected_names,
            actual_names,
        )

    def test_dataset_names_are_unique(self) -> None:
        """Dataset names must not be duplicated."""

        names = [
            dataset.name
            for dataset in self.schema.datasets
        ]

        self.assertEqual(
            len(names),
            len(set(names)),
        )

    def test_dataset_filenames_are_unique(self) -> None:
        """Parquet filenames must not be shared by different datasets."""

        filenames = [
            dataset.filename
            for dataset in self.schema.datasets
        ]

        self.assertEqual(
            len(filenames),
            len(set(filenames)),
        )

    def test_every_dataset_has_primary_key(self) -> None:
        """Every dataset must define at least one primary-key column."""

        for dataset in self.schema.datasets:
            with self.subTest(dataset=dataset.name):
                self.assertTrue(
                    dataset.primary_key,
                    msg=(
                        f"Dataset {dataset.name!r} does not define "
                        "a primary key."
                    ),
                )

    def test_every_dataset_has_columns(self) -> None:
        """Every dataset must define at least one output column."""

        for dataset in self.schema.datasets:
            with self.subTest(dataset=dataset.name):
                self.assertTrue(
                    dataset.columns,
                    msg=(
                        f"Dataset {dataset.name!r} does not define "
                        "any columns."
                    ),
                )

    def test_columns_are_unique_within_each_dataset(self) -> None:
        """A dataset must not contain duplicate column names."""

        for dataset in self.schema.datasets:
            with self.subTest(dataset=dataset.name):
                self.assertEqual(
                    len(dataset.columns),
                    len(set(dataset.columns)),
                    msg=(
                        f"Dataset {dataset.name!r} contains duplicate "
                        "column names."
                    ),
                )

    def test_primary_key_columns_exist_in_dataset_columns(self) -> None:
        """Every primary-key field must also be an output column."""

        for dataset in self.schema.datasets:
            with self.subTest(dataset=dataset.name):
                missing_columns = [
                    column
                    for column in dataset.primary_key
                    if column not in dataset.columns
                ]

                self.assertEqual(
                    [],
                    missing_columns,
                    msg=(
                        f"Dataset {dataset.name!r} references primary-key "
                        f"columns not present in its schema: "
                        f"{missing_columns}"
                    ),
                )

    def test_parquet_filenames_use_expected_extension(self) -> None:
        """Warehouse datasets must be stored as Parquet files."""

        for dataset in self.schema.datasets:
            with self.subTest(dataset=dataset.name):
                self.assertTrue(
                    dataset.filename.endswith(".parquet"),
                    msg=(
                        f"Dataset {dataset.name!r} has an invalid "
                        f"filename: {dataset.filename!r}"
                    ),
                )

    def test_equipment_schema_matches_configuration_summary(self) -> None:
        """The equipment dataset must expose the approved 15 columns."""

        equipment = next(
            dataset
            for dataset in self.schema.datasets
            if dataset.name == "equipment"
        )

        expected_columns = (
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

        self.assertEqual(
            ("configuration_id",),
            equipment.primary_key,
        )

        self.assertEqual(
            expected_columns,
            equipment.columns,
        )


if __name__ == "__main__":
    unittest.main()
