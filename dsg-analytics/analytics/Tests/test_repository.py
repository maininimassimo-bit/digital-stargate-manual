import tempfile
import unittest
from pathlib import Path

import pandas as pd

from analytics.repository import AnalyticsRepository


class AnalyticsRepositoryTests(unittest.TestCase):

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()

        self.root = Path(self.temp.name)

        dataframe = pd.DataFrame({"id": [1]})

        for dataset in (
            "sessions",
            "targets",
            "equipment",
            "quality",
            "weather",
        ):
            dataframe.to_parquet(self.root / f"{dataset}.parquet")

    def tearDown(self):
        self.temp.cleanup()

    def test_load_sessions(self):
        repo = AnalyticsRepository(self.root)
        self.assertEqual(len(repo.load_sessions()), 1)

    def test_load_targets(self):
        repo = AnalyticsRepository(self.root)
        self.assertEqual(len(repo.load_targets()), 1)

    def test_load_equipment(self):
        repo = AnalyticsRepository(self.root)
        self.assertEqual(len(repo.load_equipment()), 1)

    def test_load_quality(self):
        repo = AnalyticsRepository(self.root)
        self.assertEqual(len(repo.load_quality()), 1)

    def test_load_weather(self):
        repo = AnalyticsRepository(self.root)
        self.assertEqual(len(repo.load_weather()), 1)

    def test_missing_directory(self):
        with self.assertRaises(FileNotFoundError):
            AnalyticsRepository(Path("directory_does_not_exist"))

    def test_missing_dataset(self):

        (self.root / "weather.parquet").unlink()

        repo = AnalyticsRepository(self.root)

        with self.assertRaises(FileNotFoundError):
            repo.load_weather()


if __name__ == "__main__":
    unittest.main()