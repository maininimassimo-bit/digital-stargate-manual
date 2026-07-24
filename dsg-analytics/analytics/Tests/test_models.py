import unittest

from analytics.models import ALL_DATASETS


class AnalyticsModelTests(unittest.TestCase):

    def test_dataset_names_are_unique(self):
        names = [d.name for d in ALL_DATASETS]
        self.assertEqual(len(names), len(set(names)))

    def test_dataset_filenames_are_unique(self):
        names = [d.filename for d in ALL_DATASETS]
        self.assertEqual(len(names), len(set(names)))

    def test_every_dataset_has_columns(self):
        for dataset in ALL_DATASETS:
            self.assertGreater(len(dataset.columns), 0)

    def test_every_dataset_has_primary_key(self):
        for dataset in ALL_DATASETS:
            self.assertGreater(len(dataset.primary_key), 0)

    def test_primary_key_exists(self):
        for dataset in ALL_DATASETS:
            for key in dataset.primary_key:
                self.assertIn(key, dataset.columns)


if __name__ == "__main__":
    unittest.main()