"""
Base class for Analytics calculators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseCalculator(ABC):
    """
    Base interface implemented by every Analytics calculator.
    """

    #: Unique calculator name
    name: str = ""

    #: Output parquet filename
    output_filename: str = ""

    @abstractmethod
    def run(self, warehouse: dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Execute the calculator.

        Parameters
        ----------
        warehouse
            Dictionary containing Warehouse datasets.

        Returns
        -------
        pandas.DataFrame
            Analytics result.
        """
        raise NotImplementedError