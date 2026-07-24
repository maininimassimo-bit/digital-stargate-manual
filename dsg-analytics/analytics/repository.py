"""
Analytics repository.

Provides read-only access to Warehouse datasets.
"""

from pathlib import Path

import pandas as pd


class AnalyticsRepository:
    """
    Read-only repository for Warehouse datasets.
    """

    def __init__(self, warehouse_path: Path):
        self.warehouse_path = Path(warehouse_path)

        if not self.warehouse_path.exists():
            raise FileNotFoundError(
                f"Warehouse directory not found: {self.warehouse_path}"
            )

    def _load(self, filename: str) -> pd.DataFrame:
        path = self.warehouse_path / filename

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_parquet(path)

    def load_sessions(self):
        return self._load("sessions.parquet")

    def load_targets(self):
        return self._load("targets.parquet")

    def load_equipment(self):
        return self._load("equipment.parquet")

    def load_quality(self):
        return self._load("quality.parquet")

    def load_weather(self):
        return self._load("weather.parquet")