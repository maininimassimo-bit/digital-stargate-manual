#!/usr/bin/env python3
"""Fail-closed runtime preflight for the unbuilt BKL-031 F3-A3 candidate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path


EXPECTED_PROFILE_ID = "BKL-031-F3-A3-METHOD-PROFILE-001"
EXPECTED_PROFILE_SHA256 = "e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca"
EXPECTED_IERS_SHA256 = "43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc"
EXPECTED_PACKAGES = {
    "astropy": "8.0.1",
    "astropy-iers-data": "0.2026.9.14.0.56.43",
    "certifi": "2026.7.22",
    "jplephem": "2.24",
    "numpy": "2.5.3",
    "packaging": "26.3",
    "pyerfa": "2.0.1.5",
    "PyYAML": "6.0.3",
    "sgp4": "2.27",
    "skyfield": "1.55",
}


def require_environment(name: str, expected: str) -> str:
    value = os.environ.get(name)
    if value != expected:
        raise RuntimeError(f"{name} must equal the reviewed value")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    require_environment("DSG_EXTERNAL_PROVIDER_POLICY", "DENY")
    profile_path = Path(
        require_environment(
            "DSG_METHOD_PROFILE_PATH",
            "/app/dsg/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json",
        )
    )
    require_environment("DSG_METHOD_PROFILE_SHA256", EXPECTED_PROFILE_SHA256)
    iers_path = Path(
        require_environment(
            "DSG_IERS_ARTIFACT_PATH",
            "/app/dsg/artifacts/iers/astropy_iers_data-0.2026.9.14.0.56.43-py3-none-any.whl",
        )
    )
    require_environment("DSG_IERS_SHA256", EXPECTED_IERS_SHA256)

    if sha256(profile_path) != EXPECTED_PROFILE_SHA256:
        raise RuntimeError("method profile digest mismatch")
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    if profile.get("profileId") != EXPECTED_PROFILE_ID:
        raise RuntimeError("method profile identity mismatch")
    if profile.get("runtimeAuthority") is not False:
        raise RuntimeError("method profile unexpectedly grants runtime authority")
    if profile.get("timeData", {}).get("snapshotKind") != "IERS_A":
        raise RuntimeError("IERS snapshot kind mismatch")
    if profile.get("timeData", {}).get("autoDownloadDuringExecution") is not False:
        raise RuntimeError("execution-time IERS download is not disabled")
    if sha256(iers_path) != EXPECTED_IERS_SHA256:
        raise RuntimeError("IERS artifact digest mismatch")

    for distribution, expected_version in EXPECTED_PACKAGES.items():
        actual_version = importlib.metadata.version(distribution)
        if actual_version != expected_version:
            raise RuntimeError(
                f"{distribution} version mismatch: expected {expected_version}, received {actual_version}"
            )

    from astropy.utils import iers
    from astropy.time import Time

    if iers.conf.auto_download is not False:
        raise RuntimeError("Astropy IERS auto-download is enabled")
    if iers.conf.iers_degraded_accuracy != "error":
        raise RuntimeError("Astropy IERS degraded accuracy is not fail-closed")

    campaign_mjd = float(Time("2026-09-16T00:00:00Z", scale="utc").mjd)
    iers_a = iers.IERS_A.open(iers.IERS_A_FILE)
    coverage_min_mjd = float(iers_a["MJD"].min().value)
    coverage_max_mjd = float(iers_a["MJD"].max().value)
    if not coverage_min_mjd <= campaign_mjd <= coverage_max_mjd:
        raise RuntimeError(
            "reviewed IERS-A artifact does not cover campaign preparation: "
            f"{coverage_min_mjd} <= {campaign_mjd} <= {coverage_max_mjd} failed"
        )

    print(
        "BKL-031 F3-A3 container preflight passed: exact method profile, "
        "IERS artifact/coverage, package set and offline policy verified; "
        f"IERS_A_MJD={coverage_min_mjd}..{coverage_max_mjd}"
    )


if __name__ == "__main__":
    main()
