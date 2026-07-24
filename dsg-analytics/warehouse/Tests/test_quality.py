"""Tests for the quality warehouse dataset."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

DSG_ANALYTICS_ROOT = Path(__file__).resolve().parents[2]
if str(DSG_ANALYTICS_ROOT) not in sys.path:
    sys.path.insert(0, str(DSG_ANALYTICS_ROOT))

from warehouse.datasets.quality import (
    QualityDatasetBuildError,
    extract_fwhm,
    transform_quality_rows,
)


class QualityDatasetTests(unittest.TestCase):
    def test_extract_fwhm(self) -> None:
        filename = (
            "LIGHT_1x1_600.00s_910_99_LDN_1320_"
            "2026-07-15_00-12-18_FWHM_8.45_Fok_113360.xisf"
        )
        self.assertEqual(extract_fwhm(filename), 8.45)

    def test_extract_fwhm_rejects_missing_token(self) -> None:
        with self.assertRaises(QualityDatasetBuildError):
            extract_fwhm("LIGHT_without_metric.xisf")

    def test_transform_quality_rows(self) -> None:
        exposures = [
            {
                "session_id": "S1",
                "timestamp": "2026-07-15T00:00:00+02:00",
                "filename": "LIGHT_FWHM_8.00_Fok_1.xisf",
                "frame_type": "LIGHT",
                "exposure_seconds": "600",
                "target_name": "LDN 1320",
                "camera_temperature_c": "-10.0",
                "filter_name": "LPRO",
            },
            {
                "session_id": "S1",
                "timestamp": "2026-07-15T00:10:00+02:00",
                "filename": "LIGHT_FWHM_6.00_Fok_2.xisf",
                "frame_type": "LIGHT",
                "exposure_seconds": "600",
                "target_name": "LDN 1320",
                "camera_temperature_c": "-9.8",
                "filter_name": "LPRO",
            },
        ]
        summaries = [
            {
                "session_id": "S1",
                "target_name": "LDN 1320",
                "filter_name": "LPRO",
                "image_count": "2",
                "integration_seconds": "1200",
                "integration_hours": "0.3333",
                "first_timestamp": "2026-07-15T00:00:00+02:00",
                "last_timestamp": "2026-07-15T00:10:00+02:00",
            }
        ]

        rows = transform_quality_rows(exposures, summaries)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["session_id"], "S1")
        self.assertEqual(row["image_count"], 2)
        self.assertEqual(row["average_fwhm"], 7.0)
        self.assertEqual(row["minimum_fwhm"], 6.0)
        self.assertEqual(row["maximum_fwhm"], 8.0)
        self.assertEqual(row["fwhm_stddev"], 1.4142)
        self.assertEqual(row["average_camera_temperature_c"], -9.9)


if __name__ == "__main__":
    unittest.main()
