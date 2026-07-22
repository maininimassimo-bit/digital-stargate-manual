"""Data models for the Digital StarGate Observatory Data Warehouse."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class DatasetDefinition:
    """Logical definition of one warehouse dataset."""

    name: str
    filename: str
    description: str
    primary_key: tuple[str, ...]
    columns: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["primary_key"] = list(self.primary_key)
        data["columns"] = list(self.columns)
        return data


@dataclass(frozen=True)
class WarehouseSchema:
    """Versioned logical schema of the warehouse."""

    schema_version: int
    datasets: tuple[DatasetDefinition, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "datasets": [
                dataset.to_dict()
                for dataset in self.datasets
            ],
        }


@dataclass
class WarehouseMetadata:
    """Build metadata persisted beside the warehouse datasets."""

    schema_version: int
    status: str
    created_at: str
    updated_at: str
    datasets: dict[str, dict[str, Any]] = field(
        default_factory=dict
    )
    source_files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @classmethod
    def architecture_ready(
        cls,
        schema: WarehouseSchema,
    ) -> "WarehouseMetadata":
        now = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        return cls(
            schema_version=schema.schema_version,
            status="architecture_ready",
            created_at=now,
            updated_at=now,
            datasets={
                dataset.name: {
                    "filename": dataset.filename,
                    "rows": 0,
                    "status": "not_populated",
                }
                for dataset in schema.datasets
            },
            warnings=[
                (
                    "Sprint 1 initializes the warehouse architecture. "
                    "Dataset population is introduced in Sprint 2."
                )
            ],
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_warehouse_schema() -> WarehouseSchema:
    """Return the Release 5.1 logical warehouse schema."""

    return WarehouseSchema(
        schema_version=1,
        datasets=(
            DatasetDefinition(
                name="sessions",
                filename="sessions.parquet",
                description=(
                    "One row for each consolidated observing session."
                ),
                primary_key=("session_id",),
                columns=(
                    "schema_version",
                    "session_id",
                    "session_start",
                    "session_end",
                    "session_date",
                    "configuration_id",
                    "telescope",
                    "camera",
                    "guide_profile",
                    "duration_hours",
                    "integration_hours",
                    "integration_efficiency_pct",
                    "light_started",
                    "light_completed",
                    "light_failed",
                    "completion_pct",
                    "rms_ra_arcsec",
                    "rms_dec_arcsec",
                    "rms_total_arcsec",
                    "weather_safe_pct",
                    "autofocus_count",
                    "autofocus_failed",
                    "dither_count",
                    "dither_failed",
                    "severity",
                    "source_metrics_path",
                    "updated_at_utc",
                ),
            ),
            DatasetDefinition(
                name="targets",
                filename="targets.parquet",
                description=(
                    "Aggregated target acquisitions grouped by observing "
                    "session and imaging configuration."
                ),
                primary_key=(
                    "session_id",
                    "target_name",
                    "filter_name",
                    "telescope",
                    "frame_type",
                    "binning",
                    "gain",
                    "offset",
                ),
                columns=(
                    "session_id",
                    "target_name",
                    "filter_name",
                    "telescope",
                    "frame_type",
                    "binning",
                    "gain",
                    "offset",
                    "image_count",
                    "integration_seconds",
                    "integration_hours",
                    "average_exposure_seconds",
                    "average_camera_temperature_c",
                    "first_timestamp",
                    "last_timestamp",
                    "acquisition_span_hours",
                    "first_image_path",
                    "last_image_path",
                ),
            ),
            DatasetDefinition(
                name="equipment",
                filename="equipment.parquet",
                description=(
                    "Aggregated utilization statistics by equipment item."
                ),
                primary_key=("equipment_id",),
                columns=(
                    "equipment_id",
                    "equipment_name",
                    "equipment_type",
                    "session_count",
                    "usage_hours",
                    "target_count",
                    "last_used_at",
                    "usage_percent",
                ),
            ),
            DatasetDefinition(
                name="weather",
                filename="weather.parquet",
                description=(
                    "Environmental conditions associated with sessions."
                ),
                primary_key=("session_id",),
                columns=(
                    "session_id",
                    "session_date",
                    "sqm",
                    "cloud_cover_percent",
                    "humidity_percent",
                    "wind_kmh",
                    "temperature_c",
                    "dew_point_c",
                ),
            ),
            DatasetDefinition(
                name="quality",
                filename="quality.parquet",
                description=(
                    "Image quality metrics associated with sessions."
                ),
                primary_key=("session_id",),
                columns=(
                    "session_id",
                    "session_date",
                    "target_name",
                    "fwhm_arcsec",
                    "hfr_pixels",
                    "seeing_arcsec",
                    "star_count",
                    "quality_score",
                ),
            ),
        ),
    )
