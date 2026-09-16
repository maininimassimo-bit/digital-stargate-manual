#!/usr/bin/env python3
"""Bounded, fail-closed BKL-031 F3-A3 synthetic scientific spike runner."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


PROFILE_ID = "BKL-031-F3-A3-METHOD-PROFILE-001"
PROFILE_SHA256 = "e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca"
KERNEL_SHA256 = "54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c"
KERNEL_URI = (
    "gs://digital-stargate-telemetry-183451329061-f3-data/"
    "bkl-031/f3-a3/artifacts/spk/de442s/sha256/"
    f"{KERNEL_SHA256}/de442s.bsp"
)
CAMPAIGN_ID = "BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001"
ALLOWED_TARGETS = frozenset({"mars", "moon"})
UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
MAX_REQUEST_BYTES = 262_144
MAX_TARGETS = 50
MAX_INSTANTS_PER_TARGET = 2_016
MAX_PAIRS = 10_000
MAX_SPAN = dt.timedelta(days=7)
MIN_GRID_STEP_SECONDS = 60


class ContractError(RuntimeError):
    """A governed input or environment violated the reviewed contract."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_utc(value: Any, label: str) -> dt.datetime:
    if not isinstance(value, str) or not UTC_PATTERN.fullmatch(value):
        raise ContractError(f"{label}: INVALID_UTC_INSTANT")
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed < dt.datetime(1850, 1, 1, tzinfo=dt.timezone.utc) or parsed >= dt.datetime(2150, 1, 1, tzinfo=dt.timezone.utc):
        raise ContractError(f"{label}: OUT_OF_COVERAGE")
    return parsed


def require_exact_environment() -> dict[str, str]:
    expected = {
        "DSG_EXECUTION_MODE": "VALIDATION_SPIKE",
        "DSG_SITE_PROFILE": "SYNTHETIC_ONLY",
        "DSG_EXTERNAL_PROVIDER_POLICY": "DENY",
        "DSG_KERNEL_SHA256": KERNEL_SHA256,
        "DSG_KERNEL_URI": KERNEL_URI,
        "DSG_METHOD_PROFILE_ID": PROFILE_ID,
        "DSG_METHOD_PROFILE_SHA256": PROFILE_SHA256,
    }
    for name, required in expected.items():
        if os.environ.get(name) != required:
            raise ContractError(f"{name}: REVIEWED_VALUE_REQUIRED")
    source_commit = os.environ.get("DSG_SOURCE_COMMIT", "")
    if not SHA_PATTERN.fullmatch(source_commit):
        raise ContractError("DSG_SOURCE_COMMIT: EXACT_COMMIT_REQUIRED")
    data_bucket = os.environ.get("DSG_DATA_BUCKET", "")
    evidence_bucket = os.environ.get("DSG_EVIDENCE_BUCKET", "")
    if data_bucket != "digital-stargate-telemetry-183451329061-f3-data":
        raise ContractError("DSG_DATA_BUCKET: REVIEWED_VALUE_REQUIRED")
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{1,61}[a-z0-9]", evidence_bucket) or evidence_bucket == data_bucket:
        raise ContractError("DSG_EVIDENCE_BUCKET: VALID_DEDICATED_BUCKET_REQUIRED")
    execution = os.environ.get("CLOUD_RUN_EXECUTION", "")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", execution):
        raise ContractError("CLOUD_RUN_EXECUTION: CLOUD_RUN_ID_REQUIRED")
    return {**expected, "DSG_SOURCE_COMMIT": source_commit, "DSG_DATA_BUCKET": data_bucket,
            "DSG_EVIDENCE_BUCKET": evidence_bucket, "CLOUD_RUN_EXECUTION": execution}


def validate_campaign(raw: bytes) -> dict[str, Any]:
    if len(raw) > MAX_REQUEST_BYTES:
        raise ContractError("REQUEST_BOUND_EXCEEDED: REQUEST_BYTES")
    try:
        campaign = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ContractError("INVALID_REQUEST: JSON") from exc
    if not isinstance(campaign, dict):
        raise ContractError("INVALID_REQUEST: OBJECT_REQUIRED")
    exact = {
        "schemaVersion": "1.0",
        "campaignId": CAMPAIGN_ID,
        "environment": "TEST",
        "authority": "NONE",
        "timeScale": "UTC",
        "frame": "ALTAZ",
        "datum": "WGS84",
        "refractionMode": "DISABLED",
    }
    for name, value in exact.items():
        if campaign.get(name) != value:
            raise ContractError(f"{name}: REVIEWED_VALUE_REQUIRED")
    site = campaign.get("site")
    if not isinstance(site, dict) or site.get("classification") != "SYNTHETIC_PUBLIC" or site.get("siteId") != "SYNTHETIC-MID-LATITUDE-001":
        raise ContractError("SITE_PROFILE: SYNTHETIC_REVIEWED_SITE_REQUIRED")
    if site.get("latitudeDegrees") != 45.0 or site.get("longitudeDegrees") != 10.0 or site.get("elevationMeters") != 0.0:
        raise ContractError("SITE_PROFILE: REVIEWED_VALUES_REQUIRED")
    targets = campaign.get("targets")
    instants = campaign.get("instantsUtc")
    if not isinstance(targets, list) or not targets or len(targets) > MAX_TARGETS or len(set(targets)) != len(targets):
        raise ContractError("REQUEST_BOUND_EXCEEDED: TARGETS")
    if any(target not in ALLOWED_TARGETS for target in targets):
        raise ContractError("INVALID_REQUEST: TARGET")
    if not isinstance(instants, list) or not instants or len(instants) > MAX_INSTANTS_PER_TARGET or len(set(instants)) != len(instants):
        raise ContractError("REQUEST_BOUND_EXCEEDED: INSTANTS")
    if len(targets) * len(instants) > MAX_PAIRS:
        raise ContractError("REQUEST_BOUND_EXCEEDED: PAIRS")
    parsed = [parse_utc(value, f"instantsUtc[{index}]") for index, value in enumerate(instants)]
    if parsed != sorted(parsed) or parsed[-1] - parsed[0] > MAX_SPAN:
        raise ContractError("REQUEST_BOUND_EXCEEDED: SPAN_OR_ORDER")
    transit = campaign.get("transit")
    if not isinstance(transit, dict) or transit.get("target") not in targets:
        raise ContractError("INVALID_REQUEST: TRANSIT_TARGET")
    start = parse_utc(transit.get("startUtc"), "transit.startUtc")
    end = parse_utc(transit.get("endUtc"), "transit.endUtc")
    if end <= start or end - start > MAX_SPAN:
        raise ContractError("REQUEST_BOUND_EXCEEDED: TRANSIT_SPAN")
    if transit.get("gridStepSeconds") != MIN_GRID_STEP_SECONDS:
        raise ContractError("REQUEST_BOUND_EXCEEDED: GRID_STEP")
    return campaign


def metadata_token() -> str:
    request = urllib.request.Request(
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
        headers={"Metadata-Flavor": "Google"},
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        payload = json.load(response)
    token = payload.get("access_token")
    if not isinstance(token, str) or not token:
        raise ContractError("GOOGLE_AUTH_TOKEN_UNAVAILABLE")
    return token


def storage_download(gs_uri: str, destination: Path, token: str) -> None:
    match = re.fullmatch(r"gs://([^/]+)/(.+)", gs_uri)
    if not match:
        raise ContractError("INVALID_GCS_URI")
    bucket, object_name = match.groups()
    url = "https://storage.googleapis.com/download/storage/v1/b/" + urllib.parse.quote(bucket, safe="") + "/o/" + urllib.parse.quote(object_name, safe="") + "?alt=media"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=30) as response, destination.open("xb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)


def storage_upload(bucket: str, object_name: str, payload: bytes, token: str) -> None:
    query = urllib.parse.urlencode({"uploadType": "media", "name": object_name, "ifGenerationMatch": "0"})
    url = "https://storage.googleapis.com/upload/storage/v1/b/" + urllib.parse.quote(bucket, safe="") + "/o?" + query
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("name") != object_name or result.get("bucket") != bucket:
        raise ContractError("EVIDENCE_UPLOAD_IDENTITY_MISMATCH")


def circular_difference_degrees(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def parabolic_peak_seconds(values: Any, index: int, step_seconds: int) -> float:
    if index <= 0 or index >= len(values) - 1:
        raise ContractError("TRANSIT_PEAK_AT_SEARCH_BOUNDARY")
    before = float(values[index - 1])
    center = float(values[index])
    after = float(values[index + 1])
    denominator = before - 2.0 * center + after
    if denominator >= 0.0 or denominator == 0.0:
        raise ContractError("TRANSIT_PEAK_NOT_CONCAVE")
    fractional_offset = 0.5 * (before - after) / denominator
    if abs(fractional_offset) > 1.0:
        raise ContractError("TRANSIT_PEAK_REFINEMENT_OUT_OF_CELL")
    return (index + fractional_offset) * step_seconds


def calculate(campaign: dict[str, Any], kernel_path: Path, profile: dict[str, Any]) -> dict[str, Any]:
    import astropy.units as u
    from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body, solar_system_ephemeris
    from astropy.time import Time
    from skyfield.api import load_file, load, wgs84

    site = campaign["site"]
    astropy_location = EarthLocation.from_geodetic(
        lon=site["longitudeDegrees"] * u.deg,
        lat=site["latitudeDegrees"] * u.deg,
        height=site["elevationMeters"] * u.m,
    )
    skyfield_ephemeris = load_file(str(kernel_path))
    timescale = load.timescale(builtin=True)
    skyfield_observer = skyfield_ephemeris["earth"] + wgs84.latlon(
        site["latitudeDegrees"], site["longitudeDegrees"], elevation_m=site["elevationMeters"]
    )
    thresholds = profile["thresholds"]
    vectors: list[dict[str, Any]] = []
    with solar_system_ephemeris.set(str(kernel_path)):
        for instant in campaign["instantsUtc"]:
            astropy_time = Time(instant, scale="utc", location=astropy_location)
            skyfield_time = timescale.from_datetime(parse_utc(instant, "instant"))
            method_positions: dict[str, Any] = {}
            for target in campaign["targets"]:
                primary_gcrs = get_body(target, astropy_time, location=astropy_location)
                primary_altaz = primary_gcrs.transform_to(
                    AltAz(obstime=astropy_time, location=astropy_location, pressure=0 * u.Pa)
                )
                secondary_apparent = skyfield_observer.at(skyfield_time).observe(skyfield_ephemeris[target]).apparent()
                secondary_alt, secondary_az, _ = secondary_apparent.altaz()
                altitude_error = abs(primary_altaz.alt.deg - secondary_alt.degrees) * 3600.0
                azimuth_error = circular_difference_degrees(primary_altaz.az.deg, secondary_az.degrees) * 3600.0
                spherical_error = primary_altaz.separation(
                    SkyCoord(alt=secondary_alt.degrees * u.deg, az=secondary_az.degrees * u.deg,
                             frame=AltAz(obstime=astropy_time, location=astropy_location, pressure=0 * u.Pa))
                ).arcsecond
                if min(primary_altaz.alt.deg, secondary_alt.degrees) >= thresholds["altitudeMinimumDegrees"]:
                    altitude_pass: bool | None = altitude_error <= thresholds["altitudeMaximumErrorArcseconds"]
                else:
                    altitude_pass = None
                if min(primary_altaz.alt.deg, secondary_alt.degrees) < thresholds["azimuthMinimumAltitudeDegrees"]:
                    azimuth_pass: bool | None = None
                elif max(primary_altaz.alt.deg, secondary_alt.degrees) <= thresholds["azimuthMaximumAltitudeDegrees"]:
                    azimuth_pass = azimuth_error <= thresholds["azimuthMaximumErrorArcseconds"]
                else:
                    azimuth_pass = spherical_error <= thresholds["nearZenithSphericalSeparationMaximumErrorArcseconds"]
                method_positions[target] = {"primary": primary_gcrs, "secondary": secondary_apparent}
                vectors.append({
                    "instantUtc": instant,
                    "target": target,
                    "primary": {"altitudeDegrees": primary_altaz.alt.deg, "azimuthDegrees": primary_altaz.az.deg},
                    "crossCheck": {"altitudeDegrees": secondary_alt.degrees, "azimuthDegrees": secondary_az.degrees},
                    "metrics": {"altitudeErrorArcseconds": altitude_error, "altitudePass": altitude_pass,
                                "azimuthErrorArcseconds": azimuth_error, "azimuthPass": azimuth_pass,
                                "sphericalErrorArcseconds": spherical_error},
                })
            primary_sep = method_positions["mars"]["primary"].separation(method_positions["moon"]["primary"]).arcsecond
            secondary_sep = method_positions["mars"]["secondary"].separation_from(method_positions["moon"]["secondary"]).arcseconds()
            separation_error = abs(primary_sep - secondary_sep)
            elongation_primary = get_body("sun", astropy_time).separation(get_body("moon", astropy_time)).rad
            earth = skyfield_ephemeris["earth"]
            elongation_secondary = earth.at(skyfield_time).observe(skyfield_ephemeris["sun"]).apparent().separation_from(
                earth.at(skyfield_time).observe(skyfield_ephemeris["moon"]).apparent()).radians
            illumination_primary = (1.0 - math.cos(elongation_primary)) / 2.0
            illumination_secondary = (1.0 - math.cos(elongation_secondary)) / 2.0
            vectors[-1]["sharedMetrics"] = {
                "targetMoonSeparationErrorArcseconds": separation_error,
                "targetMoonSeparationPass": separation_error <= thresholds["targetMoonSeparationMaximumErrorArcseconds"],
                "lunarIlluminationConvention": "GEOCENTRIC_APPARENT_ELONGATION_COSINE_APPROXIMATION",
                "lunarIlluminationAbsoluteDifference": abs(illumination_primary - illumination_secondary),
                "lunarIlluminationPass": abs(illumination_primary - illumination_secondary) <= thresholds["lunarIlluminationMaximumAbsoluteDifference"],
            }
        transit = campaign["transit"]
        transit_start = parse_utc(transit["startUtc"], "transit.startUtc")
        transit_end = parse_utc(transit["endUtc"], "transit.endUtc")
        step = dt.timedelta(seconds=transit["gridStepSeconds"])
        transit_datetimes = []
        cursor = transit_start
        while cursor <= transit_end:
            transit_datetimes.append(cursor)
            cursor += step
        astropy_transit_times = Time(transit_datetimes, scale="utc", location=astropy_location)
        astropy_transit_altitudes = get_body(
            transit["target"], astropy_transit_times, location=astropy_location
        ).transform_to(
            AltAz(obstime=astropy_transit_times, location=astropy_location, pressure=0 * u.Pa)
        ).alt.deg
        skyfield_transit_times = timescale.from_datetimes(transit_datetimes)
        skyfield_transit_altitudes = skyfield_observer.at(skyfield_transit_times).observe(
            skyfield_ephemeris[transit["target"]]
        ).apparent().altaz()[0].degrees
        primary_transit_index = int(astropy_transit_altitudes.argmax())
        secondary_transit_index = int(skyfield_transit_altitudes.argmax())
        primary_transit_seconds = parabolic_peak_seconds(astropy_transit_altitudes, primary_transit_index, transit["gridStepSeconds"])
        secondary_transit_seconds = parabolic_peak_seconds(skyfield_transit_altitudes, secondary_transit_index, transit["gridStepSeconds"])
        transit_error_seconds = abs(primary_transit_seconds - secondary_transit_seconds)
        primary_transit_time = transit_start + dt.timedelta(seconds=primary_transit_seconds)
        secondary_transit_time = transit_start + dt.timedelta(seconds=secondary_transit_seconds)
        transit_metric = {
            "target": transit["target"],
            "searchStartUtc": transit["startUtc"],
            "searchEndUtc": transit["endUtc"],
            "gridStepSeconds": transit["gridStepSeconds"],
            "primaryTransitUtc": primary_transit_time.isoformat(timespec="microseconds").replace("+00:00", "Z"),
            "crossCheckTransitUtc": secondary_transit_time.isoformat(timespec="microseconds").replace("+00:00", "Z"),
            "errorSeconds": transit_error_seconds,
            "pass": transit_error_seconds <= thresholds["transitCulminationMaximumErrorSeconds"],
            "method": "BOUNDED_ONE_MINUTE_GRID_WITH_LOCAL_PARABOLIC_REFINEMENT",
        }
    metric_passes = [value for vector in vectors for key, value in vector["metrics"].items() if key.endswith("Pass") and value is not None]
    metric_passes.extend(value for vector in vectors for key, value in vector.get("sharedMetrics", {}).items() if key.endswith("Pass"))
    metric_passes.append(transit_metric["pass"])
    return {"vectors": vectors, "metricPassCount": sum(metric_passes), "metricEvaluationCount": len(metric_passes),
            "transit": transit_metric, "allEvaluatedMetricsPass": all(metric_passes)}


def run(request_path: Path) -> None:
    started = time.monotonic()
    environment = require_exact_environment()
    raw_request = request_path.read_bytes()
    campaign = validate_campaign(raw_request)
    profile_path = Path(os.environ["DSG_METHOD_PROFILE_PATH"])
    if digest_file(profile_path) != PROFILE_SHA256:
        raise ContractError("METHOD_PROFILE_DIGEST_MISMATCH")
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    token = metadata_token()
    with tempfile.TemporaryDirectory(prefix="dsg-f3-a3-") as temporary:
        kernel_path = Path(temporary) / "de442s.bsp"
        storage_download(KERNEL_URI, kernel_path, token)
        if digest_file(kernel_path) != KERNEL_SHA256:
            raise ContractError("KERNEL_DIGEST_MISMATCH")
        scientific = calculate(campaign, kernel_path, profile)
        repeated = calculate(campaign, kernel_path, profile)
        repeatability_pass = canonical_bytes(scientific) == canonical_bytes(repeated)
        scientific["repeatabilityPass"] = repeatability_pass
        scientific["allEvaluatedMetricsPass"] = scientific["allEvaluatedMetricsPass"] and repeatability_pass
    normalized = {
        "campaignId": CAMPAIGN_ID,
        "requestSha256": digest_bytes(canonical_bytes(campaign)),
        "methodProfile": {"id": PROFILE_ID, "sha256": PROFILE_SHA256},
        "kernel": {"uri": KERNEL_URI, "sha256": KERNEL_SHA256},
        "sourceCommit": environment["DSG_SOURCE_COMMIT"],
        "networkCalls": {
            "privateGoogleApiCallCount": 3,
            "destinations": ["metadata.google.internal", "storage.googleapis.com"],
            "externalReferenceCallCount": 0,
        },
        "protectedSiteUse": "NOT_EXECUTED",
        "runtimeActivation": "NOT_EXECUTED",
        "scientific": scientific,
    }
    normalized_digest = digest_bytes(canonical_bytes(normalized))
    evidence = {**normalized, "schemaVersion": "1.0", "executionHost": "GOOGLE_CLOUD_RUN_JOB_EUROPE_WEST8",
                "executionId": environment["CLOUD_RUN_EXECUTION"], "normalizedResultSha256": normalized_digest,
                "durationMilliseconds": round((time.monotonic() - started) * 1000)}
    payload = canonical_bytes(evidence)
    object_name = f"bkl-031/f3-a3/scientific-spike/{environment['DSG_SOURCE_COMMIT']}/{environment['CLOUD_RUN_EXECUTION']}/evidence.json"
    storage_upload(environment["DSG_EVIDENCE_BUCKET"], object_name, payload, token)
    print(json.dumps({"status": "PASS" if scientific["allEvaluatedMetricsPass"] else "CONFLICTED_EVIDENCE",
                      "evidenceObject": object_name, "normalizedResultSha256": normalized_digest,
                      "externalReferenceCallCount": 0}, sort_keys=True))
    if not scientific["allEvaluatedMetricsPass"]:
        raise SystemExit(2)


def contract_self_test() -> None:
    fixture = Path(__file__).with_name("BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001.json").read_bytes()
    campaign = validate_campaign(fixture)
    if digest_bytes(canonical_bytes(campaign)) != digest_bytes(canonical_bytes(json.loads(fixture))):
        raise AssertionError("canonical request digest is unstable")
    mutations = []
    for mutate in (
        lambda value: value.update({"authority": "RUNTIME"}),
        lambda value: value["site"].update({"latitudeDegrees": 42.0}),
        lambda value: value["transit"].update({"gridStepSeconds": 30}),
        lambda value: value["targets"].append("jupiter"),
        lambda value: value["instantsUtc"].append("2150-01-01T00:00:00Z"),
    ):
        candidate = json.loads(fixture)
        mutate(candidate)
        mutations.append(candidate)
    for candidate in mutations:
        try:
            validate_campaign(canonical_bytes(candidate))
        except ContractError:
            continue
        raise AssertionError("negative contract mutation was accepted")
    if circular_difference_degrees(359.0, 1.0) != 2.0:
        raise AssertionError("circular difference is incorrect")
    peak = parabolic_peak_seconds([0.0, 1.0, 0.0], 1, 60)
    if peak != 60.0:
        raise AssertionError("parabolic peak refinement is incorrect")
    print("BKL-031 F3-A3 scientific runner contract self-test passed; no scientific calculation or network request executed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path)
    parser.add_argument("--contract-self-test", action="store_true")
    args = parser.parse_args()
    if args.contract_self_test:
        contract_self_test()
        return
    if args.request is None:
        raise ContractError("--request is required")
    run(args.request)


if __name__ == "__main__":
    main()
