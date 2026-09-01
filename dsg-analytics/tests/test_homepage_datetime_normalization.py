#!/usr/bin/env python3
"""Regression coverage for homepage mixed timezone session timestamps."""
from __future__ import annotations

import importlib.util
from datetime import timezone
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "homepage" / "refresh_homepage.py"
spec = importlib.util.spec_from_file_location("refresh_homepage", MODULE_PATH)
assert spec and spec.loader
homepage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(homepage)


def test_as_dt_normalizes_naive_and_aware_values_to_utc() -> None:
    naive = homepage.as_dt("2026-08-31T23:55:55")
    aware = homepage.as_dt("2026-09-01T00:10:00+02:00")
    zulu = homepage.as_dt("2026-08-31T22:30:00Z")

    assert naive is not None and naive.tzinfo == timezone.utc
    assert aware is not None and aware.tzinfo == timezone.utc
    assert zulu is not None and zulu.tzinfo == timezone.utc
    assert aware.isoformat() == "2026-08-31T22:10:00+00:00"


def test_build_operational_section_accepts_mixed_naive_and_aware_sessions() -> None:
    sessions = [
        {
            "session_id": "older-naive",
            "session_start": "2026-08-31T20:00:00",
            "session_end": "2026-08-31T23:00:00",
            "integration_hours": "1.0",
            "light_completed": "10",
            "telescope": "Legacy scope",
            "camera": "Legacy camera",
            "configuration_id": "LEGACY",
            "severity": "GREEN",
        },
        {
            "session_id": "latest-aware",
            "session_start": "2026-09-01T00:30:00+00:00",
            "session_end": "2026-09-01T01:30:00+00:00",
            "integration_hours": "2.0",
            "light_completed": "20",
            "telescope": "Celestron C8 XLT",
            "camera": "QHY695A",
            "configuration_id": "C8_QHY695A_BIN1",
            "severity": "GREEN",
        },
    ]
    targets = [{"session_id": "latest-aware", "target_name": "M 27"}]
    metadata = [
        {
            "session_id": "latest-aware",
            "metadata_state": "REGISTERED",
            "target_name": "M 27",
            "ra_deg": "299.9",
            "dec_deg": "22.721111",
            "configuration_id": "C8_QHY695A_BIN1",
        }
    ]

    rendered = homepage.build_operational_section(sessions, targets, metadata)

    assert "latest-aware" in rendered
    assert "M 27" in rendered
    assert "QHY695A" in rendered
    assert "RA 19h 59m 36s" in rendered
    assert "Dec +22° 43′ 16″" in rendered


if __name__ == "__main__":
    test_as_dt_normalizes_naive_and_aware_values_to_utc()
    test_build_operational_section_accepts_mixed_naive_and_aware_sessions()
    print("Homepage datetime normalization regression tests PASS")
