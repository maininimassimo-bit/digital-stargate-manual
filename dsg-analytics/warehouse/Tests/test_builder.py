"""Integration tests for the warehouse builder."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

DSG_ANALYTICS_ROOT = Path(__file__).resolve().parents[2]

if str(DSG_ANALYTICS_ROOT) not in sys.path:
    sys.path.insert(0, str(DSG_ANALYTICS_ROOT))

from warehouse.builder import build_warehouse


class WarehouseBuilderTests(unittest.TestCase):
    """Integration tests for build_warehouse()."""

    def setUp(self) -> None:
        self.original_repo = Path(__file__).resolve().parents[3]

        self.temp_dir = Path(
            tempfile.mkdtemp(prefix="dsg_warehouse_test_")
        )

        shutil.copytree(
            self.original_repo / "data",
            self.temp_dir / "data",
        )

    def tearDown(self) -> None:
        shutil.rmtree(
            self.temp_dir,
            ignore_errors=True,
        )

    def test_complete_build(self) -> None:
        (
            schema_path,
            metadata_path,
            sessions_path,
            targets_path,
            equipment_path,
            quality_path,
            weather_path,
        ) = build_warehouse(self.temp_dir)

        #
        # Files created
        #

        self.assertTrue(schema_path.exists())
        self.assertTrue(metadata_path.exists())

        self.assertTrue(sessions_path.exists())
        self.assertTrue(targets_path.exists())
        self.assertTrue(equipment_path.exists())
        self.assertTrue(quality_path.exists())
        self.assertTrue(weather_path.exists())

        #
        # JSON validity
        #

        with schema_path.open(
            encoding="utf-8"
        ) as fp:
            schema = json.load(fp)

        with metadata_path.open(
            encoding="utf-8"
        ) as fp:
            metadata = json.load(fp)

        self.assertIn("datasets", schema)
        self.assertIn("datasets", metadata)

        #
        # Parquet readability
        #

        sessions = pd.read_parquet(sessions_path)
        targets = pd.read_parquet(targets_path)
        equipment = pd.read_parquet(equipment_path)
        quality = pd.read_parquet(quality_path)
        weather = pd.read_parquet(weather_path)

        self.assertGreater(len(sessions), 0)
        self.assertGreater(len(targets), 0)
        self.assertGreater(len(equipment), 0)
        self.assertGreater(len(quality), 0)

        # Weather può anche essere vuoto (CSV con sola intestazione)
        self.assertGreaterEqual(len(weather), 0)

        #
        # Metadata consistency
        #

        self.assertEqual(
            metadata["datasets"]["sessions"]["rows"],
            len(sessions),
        )

        self.assertEqual(
            metadata["datasets"]["targets"]["rows"],
            len(targets),
        )

        self.assertEqual(
            metadata["datasets"]["equipment"]["rows"],
            len(equipment),
        )

        self.assertEqual(
            metadata["datasets"]["quality"]["rows"],
            len(quality),
        )

        self.assertEqual(
            metadata["datasets"]["weather"]["rows"],
            len(weather),
        )

        self.assertEqual(
            metadata["datasets"]["sessions"]["status"],
            "populated",
        )

        self.assertEqual(
            metadata["datasets"]["targets"]["status"],
            "populated",
        )

        self.assertEqual(
            metadata["datasets"]["equipment"]["status"],
            "populated",
        )

        self.assertEqual(
            metadata["datasets"]["quality"]["status"],
            "populated",
        )

        self.assertEqual(
            metadata["datasets"]["weather"]["status"],
            "populated",
        )

        #
        # Warehouse completed
        #

        self.assertEqual(
            metadata["status"],
            "populated",
        )

        self.assertEqual(
            metadata["warnings"],
            [],
        )

        self.assertEqual(
            len(metadata["datasets"]["quality"]["source"]),
            2,
        )

        self.assertGreaterEqual(
            len(metadata["datasets"]["weather"]["source"]),
            1,
        )


if __name__ == "__main__":
    unittest.main()
