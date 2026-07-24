from pathlib import Path
import json

import pandas as pd

from analytics.metadata import (
    DatasetMetadata,
    MetadataGenerator,
)
from analytics.models import SESSION_STATISTICS


def test_create_dataset_metadata():

    dataframe = pd.DataFrame(
        {
            "date": ["2026-07-24"],
            "sessions": [1],
            "total_hours": [3.5],
            "average_hours": [3.5],
            "longest_session_hours": [3.5],
        }
    )

    metadata = MetadataGenerator.create_dataset_metadata(
        SESSION_STATISTICS,
        dataframe,
    )

    assert metadata.name == "session_statistics"
    assert metadata.filename == "session_statistics.parquet"
    assert metadata.rows == 1
    assert metadata.columns == 5


def test_build_metadata():

    dataset = DatasetMetadata(
        name="session_statistics",
        filename="session_statistics.parquet",
        rows=10,
        columns=5,
    )

    metadata = MetadataGenerator.build(
        datasets=[dataset],
        duration_seconds=0.75,
    )

    assert metadata["version"] == "1.0.0"
    assert metadata["duration_seconds"] == 0.75
    assert len(metadata["datasets"]) == 1
    assert metadata["datasets"][0]["rows"] == 10


def test_write_metadata(tmp_path: Path):

    dataset = DatasetMetadata(
        name="session_statistics",
        filename="session_statistics.parquet",
        rows=3,
        columns=5,
    )

    output = MetadataGenerator.write(
        output_directory=tmp_path,
        datasets=[dataset],
        duration_seconds=1.25,
    )

    assert output.exists()

    content = json.loads(output.read_text())

    assert content["version"] == "1.0.0"
    assert len(content["datasets"]) == 1
    assert content["datasets"][0]["name"] == "session_statistics"