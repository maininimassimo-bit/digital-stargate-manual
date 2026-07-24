"""
Base class for Analytics calculators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from analytics.context import PipelineContext


class BaseCalculator(ABC):
    """
    Base interface implemented by every Analytics calculator.
    """

    #: Unique calculator name
    name: str = ""

    #: Output parquet filename
    output_filename: str = ""

    @abstractmethod
    def run(self, context: PipelineContext) -> pd.DataFrame:
        """
        Execute the calculator.

        Parameters
        ----------
        context
            Shared Analytics pipeline context containing Warehouse datasets.

        Returns
        -------
        pandas.DataFrame
            Analytics result.
        """
        raise NotImplementedError