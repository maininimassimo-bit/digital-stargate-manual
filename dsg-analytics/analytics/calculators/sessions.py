"""
Session Analytics calculator.
"""

import pandas as pd

from analytics.calculators.base import BaseCalculator


class SessionCalculator(BaseCalculator):

    name = "sessions"

    output_filename = "session_statistics.parquet"

    def run(self, warehouse):

        columns = (
            "date",
            "sessions",
            "total_hours",
            "average_hours",
            "longest_session_hours",
        )

        return pd.DataFrame(columns=columns)