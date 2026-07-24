"""
Metadata generation for Analytics pipeline outputs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable

import pandas as pd

from analytics.models import AnalyticsDataset


@dataclass(frozen=True, slots=True)
class DatasetMetadata:
    """
    Metadata describing a generated Analytics dataset.
    """

    name: str
    filename: str
    rows: int
    columns: int


class MetadataGenerator:
    """
    Build and write metadata for Analytics pipeline outputs.
    """

    METADATA_FILENAME = "metadata.json"
    VERSION = "1.0.0"

    @staticmethod
    def create_dataset_metadata(
        dataset: AnalyticsDataset,
        dataframe: pd.DataFrame,
    ) -> DatasetMetadata:
        """
        Create metadata for a generated Analytics dataset.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Dataset metadata can only be created from a pandas.DataFrame."
            )

        return DatasetMetadata(
            name=dataset.name,
            filename=dataset.filename,
            rows=len(dataframe.index),
            columns=len(dataframe.columns),
        )

    @classmethod
    def build(
        cls,
        datasets: Iterable[DatasetMetadata],
        duration_seconds: float,
    ) -> dict[str, object]:
        """
        Build the metadata document.
        """
        if duration_seconds < 0:
            raise ValueError("duration_seconds cannot be negative.")

        generated_at = datetime.now(timezone.utc).isoformat().replace(
            "+00:00",
            "Z",
        )

        return {
            "version": cls.VERSION,
            "generated_at": generated_at,
            "duration_seconds": round(duration_seconds, 3),
            "datasets": [
                asdict(dataset)
                for dataset in datasets
            ],
        }

    @classmethod
    def write(
        cls,
        output_directory: Path,
        datasets: Iterable[DatasetMetadata],
        duration_seconds: float,
    ) -> Path:
        """
        Write metadata.json to the Analytics output directory.
        """
        output_directory = Path(output_directory)
        output_directory.mkdir(parents=True, exist_ok=True)

        metadata = cls.build(
            datasets=datasets,
            duration_seconds=duration_seconds,
        )

        output_path = output_directory / cls.METADATA_FILENAME
        output_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        return output_path
