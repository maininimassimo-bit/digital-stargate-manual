from __future__ import annotations

import pandas as pd

from analytics.models import AnalyticsDataset


class ValidationError(ValueError):
    """Raised when an Analytics dataset is invalid."""


class OutputValidator:
    """
    Validate Analytics calculator outputs.
    """

    @staticmethod
    def validate(
        dataframe: pd.DataFrame,
        dataset: AnalyticsDataset,
    ) -> None:

        if not isinstance(dataframe, pd.DataFrame):
            raise ValidationError(
                "Calculator output must be a pandas.DataFrame."
            )

        duplicated = dataframe.columns[dataframe.columns.duplicated()]

        if len(duplicated):
            raise ValidationError(
                f"Duplicated columns: {list(duplicated)}"
            )

        missing = [
            column
            for column in dataset.columns
            if column not in dataframe.columns
        ]

        if missing:
            raise ValidationError(
                f"Missing columns: {missing}"
            )

        # Supporta sia chiavi primarie singole che composte
        primary_keys = (
            dataset.primary_key
            if isinstance(dataset.primary_key, tuple)
            else (dataset.primary_key,)
        )

        missing_keys = [
            key
            for key in primary_keys
            if key not in dataframe.columns
        ]

        if missing_keys:
            raise ValidationError(
                f"Primary key columns not found: {missing_keys}"
            )

        if dataframe[list(primary_keys)].isna().any().any():
            raise ValidationError(
                "Primary key contains null values."
            )

        if dataframe.duplicated(subset=list(primary_keys)).any():
            raise ValidationError(
                "Primary key contains duplicates."
            )
