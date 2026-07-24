"""
Analytics dataset definitions.

Digital StarGate
Analytics Foundation (AN-001)
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AnalyticsDataset:
    """
    Descrive un dataset prodotto dal modulo Analytics.
    """

    name: str
    filename: str
    primary_key: Tuple[str, ...]
    columns: Tuple[str, ...]


SESSION_STATISTICS = AnalyticsDataset(
    name="session_statistics",
    filename="session_statistics.parquet",
    primary_key=("date",),
    columns=(
        "date",
        "sessions",
        "total_hours",
        "average_hours",
        "longest_session_hours",
    ),
)

WEATHER_STATISTICS = AnalyticsDataset(
    name="weather_statistics",
    filename="weather_statistics.parquet",
    primary_key=("date",),
    columns=(
        "date",
        "temperature_mean",
        "humidity_mean",
        "pressure_mean",
        "wind_mean",
        "sqm_mean",
        "safe_percentage",
    ),
)

QUALITY_STATISTICS = AnalyticsDataset(
    name="quality_statistics",
    filename="quality_statistics.parquet",
    primary_key=("date",),
    columns=(
        "date",
        "fwhm_mean",
        "fwhm_min",
        "fwhm_max",
        "fwhm_std",
    ),
)

TARGET_STATISTICS = AnalyticsDataset(
    name="target_statistics",
    filename="target_statistics.parquet",
    primary_key=("target",),
    columns=(
        "target",
        "sessions",
        "total_hours",
    ),
)

EQUIPMENT_STATISTICS = AnalyticsDataset(
    name="equipment_statistics",
    filename="equipment_statistics.parquet",
    primary_key=("equipment",),
    columns=(
        "equipment",
        "sessions",
        "hours",
    ),
)

NIGHTLY_STATISTICS = AnalyticsDataset(
    name="nightly_statistics",
    filename="nightly_statistics.parquet",
    primary_key=("date",),
    columns=(
        "date",
        "sessions",
        "hours",
        "sqm_mean",
        "fwhm_mean",
    ),
)

ALL_DATASETS = (
    SESSION_STATISTICS,
    WEATHER_STATISTICS,
    QUALITY_STATISTICS,
    TARGET_STATISTICS,
    EQUIPMENT_STATISTICS,
    NIGHTLY_STATISTICS,
)