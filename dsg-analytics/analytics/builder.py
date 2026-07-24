from __future__ import annotations

from pathlib import Path

import pandas as pd

from analytics.calculators import get_calculators
from analytics.repository import AnalyticsRepository


class AnalyticsBuilder:
    """
    Builds all Analytics datasets starting from the Warehouse.
    """

    def __init__(
        self,
        warehouse_directory: Path,
        output_directory: Path,
    ) -> None:

        self.repository = AnalyticsRepository(warehouse_directory)
        self.output_directory = Path(output_directory)

        self.calculators = get_calculators()

    def _load_datasets(self) -> dict[str, pd.DataFrame]:

        return {
            "sessions": self.repository.load_sessions(),
            "targets": self.repository.load_targets(),
            "equipment": self.repository.load_equipment(),
            "quality": self.repository.load_quality(),
            "weather": self.repository.load_weather(),
        }

    def build(self) -> list[Path]:

        self.output_directory.mkdir(parents=True, exist_ok=True)

        warehouse = self._load_datasets()

        generated_files: list[Path] = []

        for calculator in self.calculators:

            result = calculator.run(warehouse)

            destination = (
                self.output_directory
                / calculator.output_filename
            )

            result.to_parquet(destination, index=False)

            generated_files.append(destination)

        return generated_files