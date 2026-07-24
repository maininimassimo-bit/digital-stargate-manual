from pathlib import Path

import pandas as pd

from analytics.builder import AnalyticsBuilder
from analytics.context import PipelineContext


def test_builder_initialization(tmp_path: Path):

    warehouse = tmp_path / "warehouse"
    warehouse.mkdir()

    output = tmp_path / "output"

    builder = AnalyticsBuilder(
        warehouse_directory=warehouse,
        output_directory=output,
    )

    assert builder.output_directory == output
    assert len(builder.calculators) == 1


def test_builder_returns_generated_files(tmp_path: Path, monkeypatch):

    warehouse = tmp_path / "warehouse"
    warehouse.mkdir()

    output = tmp_path / "output"

    builder = AnalyticsBuilder(
        warehouse_directory=warehouse,
        output_directory=output,
    )

    dataframe = pd.DataFrame(
        {
            "date": [],
            "sessions": [],
            "total_hours": [],
            "average_hours": [],
            "longest_session_hours": [],
        }
    )

    empty = pd.DataFrame()

    monkeypatch.setattr(
        builder,
        "_load_datasets",
        lambda: PipelineContext(
            sessions=empty,
            targets=empty,
            equipment=empty,
            quality=empty,
            weather=empty,
        ),
    )

    builder.calculators[0].run = lambda context: dataframe

    generated = builder.build()

    assert len(generated) == 1
    assert generated[0].exists()
