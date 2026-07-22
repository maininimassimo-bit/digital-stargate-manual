"""Domain model for a Digital StarGate observing session."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SessionMetadata:
    """Validated metadata loaded from a session manifest."""

    session_id: str
    session_path: Path
    manifest_path: Path
    schema_version: str
    observatory: str
    timezone_id: str
    start_local: datetime
    end_local: datetime
    report_status: str
    severity: str
    diagnostic_level: int
    generated_at_local: datetime | None
    files: tuple[dict[str, Any], ...]

    @property
    def duration(self) -> timedelta:
        """Return the declared duration of the observing session."""
        return self.end_local - self.start_local

    @property
    def duration_hours(self) -> float:
        """Return the session duration expressed in decimal hours."""
        return self.duration.total_seconds() / 3600.0

    def contains(self, timestamp: datetime) -> bool:
        """Return True when timestamp belongs to the session window.

        The interval is start-inclusive and end-exclusive:

            start_local <= timestamp < end_local

        A naive timestamp is interpreted in the session timezone.
        """
        from zoneinfo import ZoneInfo

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=ZoneInfo(self.timezone_id))

        return self.start_local <= timestamp < self.end_local
