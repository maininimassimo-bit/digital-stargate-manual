import pandas as pd
import pytest

from analytics.models import SESSION_STATISTICS
from analytics.validator import OutputValidator, ValidationError


def test_validate_success():

    dataframe = pd.DataFrame(
        {
            "date": ["2026-07-24"],
            "sessions": [1],
            "total_hours": [3.5],
            "average_hours": [3.5],
            "longest_session_hours": [3.5],
        }
    )

    OutputValidator.validate(
        dataframe=dataframe,
        dataset=SESSION_STATISTICS,
    )


def test_missing_column():

    dataframe = pd.DataFrame(
        {
            "date": ["2026-07-24"],
            "sessions": [1],
            "total_hours": [3.5],
            "average_hours": [3.5],
        }
    )

    with pytest.raises(ValidationError, match="Missing columns"):
        OutputValidator.validate(
            dataframe=dataframe,
            dataset=SESSION_STATISTICS,
        )


def test_duplicate_primary_key():

    dataframe = pd.DataFrame(
        {
            "date": ["2026-07-24", "2026-07-24"],
            "sessions": [1, 2],
            "total_hours": [3.5, 4.0],
            "average_hours": [3.5, 2.0],
            "longest_session_hours": [3.5, 2.5],
        }
    )

    with pytest.raises(ValidationError, match="contains duplicates"):
        OutputValidator.validate(
            dataframe=dataframe,
            dataset=SESSION_STATISTICS,
        )


def test_null_primary_key():

    dataframe = pd.DataFrame(
        {
            "date": [None],
            "sessions": [1],
            "total_hours": [3.5],
            "average_hours": [3.5],
            "longest_session_hours": [3.5],
        }
    )

    with pytest.raises(ValidationError, match="contains null values"):
        OutputValidator.validate(
            dataframe=dataframe,
            dataset=SESSION_STATISTICS,
        )


def test_not_dataframe():

    with pytest.raises(
        ValidationError,
        match="Calculator output must be a pandas.DataFrame",
    ):
        OutputValidator.validate(
            dataframe=[],
            dataset=SESSION_STATISTICS,
        )
