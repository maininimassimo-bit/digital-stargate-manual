from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class PipelineContext:
    """
    Shared context passed to all Analytics calculators.
    """

    sessions: pd.DataFrame
    targets: pd.DataFrame
    equipment: pd.DataFrame
    quality: pd.DataFrame
    weather: pd.DataFrame
