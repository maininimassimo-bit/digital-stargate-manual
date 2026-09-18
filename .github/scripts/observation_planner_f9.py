#!/usr/bin/env python3
"""F9 MeteoHub ICON-2I current-night projection builder.

Raw GRIB files live only in a TemporaryDirectory. The durable result is a
sanitised JSON projection; exact site/grid coordinates are never emitted.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import tempfile
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = "https://meteohub.agenziaitaliameteo.it/nwp/ICON-2I_SURFACE_PRESSURE_LEVELS"
VARIABLES = ("CLCT", "T_2M", "TD_2M", "TOT_PREC", "U_10M", "V_10M", "VMAX_10M")
MAX_FILE_BYTES = 250_000_000
MAX_TOTAL_BYTES = 1_500_000_000
SITE_PATH = Path("governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.approved.json")
F8_PATH = Path("docs/data/observation-planner-f8-current-astronomy-suitability.json")
SUITABILITY_PATH = Path("docs/data/observation-planner-f8-suitability-evidence.json")
TARGET_CATALOG_PATH = Path("docs/data/observation-planner-target-catalog.json")
OUTPUT_PATH = Path("docs/data/observation-planner-f9-current-night.json")


class ContractError(RuntimeError):
    pass


def utc(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Digital-StarGate-F9/1.0 (+github.com/maininimassimo-bit/digital-stargate-manual)"})
    with urllib.request.urlopen(req, timeout=30) as response:
        if response.status != 200:
            raise ContractError(f"HTTP_{response.status}")
        return response.read(1_000_000).decode("utf-8")


def discover_run(now: dt.datetime) -> str:
    runs = sorted(set(re.findall(r'href="(\d{10})/"', get_text(BASE + "/"))))
    eligible = []
    for run in runs:
        instant = dt.datetime.strptime(run, "%Y%m%d%H").replace(tzinfo=dt.timezone.utc)
        age = (now - instant).total_seconds() / 3600
        if 0 <= age <= 18:
            eligible.append(run)
    if not eligible:
        raise ContractError("NO_FRESH_ICON2I_RUN")
    return eligible[-1]


def discover_file(run: str, variable: str) -> str:
    listing = get_text(f"{BASE}/{run}/{variable}/")
    files = sorted(set(re.findall(r'href=\"([^\"]+\.grib)\"', listing)))
    if len(files) != 1:
        raise ContractError(f"VARIABLE_FILE_NOT_UNIQUE:{variable}")
    return files[0]


def download(url: str, destination: Path) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Digital-StarGate-F9/1.0 (+github.com/maininimassimo-bit/digital-stargate-manual)"})
    size = 0
    digest = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=180) as response, destination.open("xb") as out:
        if response.status != 200 or response.headers.get_content_type() != "application/octet-stream":
            raise ContractError("INVALID_GRIB_RESPONSE")
        while chunk := response.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_FILE_BYTES:
                raise ContractError("GRIB_FILE_BOUND_EXCEEDED")
            digest.update(chunk)
            out.write(chunk)
    return size, digest.hexdigest()


def read_series(path: Path, latitude: float, longitude: float) -> tuple[dict[dt.datetime, float], str]:
    from eccodes import codes_get, codes_grib_find_nearest, codes_grib_new_from_file, codes_release
    result: dict[dt.datetime, float] = {}
    unit = ""
    with path.open("rb") as stream:
        while True:
            gid = codes_grib_new_from_file(stream)
            if gid is None:
                break
            try:
                valid_date = int(codes_get(gid, "validityDate"))
                valid_time = int(codes_get(gid, "validityTime"))
                unit = str(codes_get(gid, "units"))
                nearest = codes_grib_find_nearest(gid, latitude, longitude)[0]
                value = float(nearest["value"])
                if not math.isfinite(value):
                    raise ContractError("NON_FINITE_GRIB_VALUE")
                instant = dt.datetime.strptime(f"{valid_date:08d}{valid_time:04d}", "%Y%m%d%H%M").replace(tzinfo=dt.timezone.utc)
                result[instant] = value
            finally:
                codes_release(gid)
    if not result:
        raise ContractError("EMPTY_GRIB_SERIES")
    return result, unit


def rh_from_temperature(temp_c: float, dew_c: float) -> float:
    a, b = 17.625, 243.04
    return max(0.0, min(100.0, 100 * math.exp(a * dew_c / (b + dew_c) - a * temp_c / (b + temp_c))))


def weather_rows(series: dict[str, dict[dt.datetime, float]]) -> dict[dt.datetime, dict[str, float]]:
    common = sorted(set.intersection(*(set(values) for values in series.values())))
    if len(common) < 24:
        raise ContractError("INCOMPLETE_VARIABLE_INTERSECTION")
    precipitation_previous = None
    rows = {}
    for instant in common:
        t = series["T_2M"][instant] - 273.15
        td = series["TD_2M"][instant] - 273.15
        accumulated = series["TOT_PREC"][instant]
        delta = 0.0 if precipitation_previous is None else accumulated - precipitation_previous
        if delta < -0.001:
            raise ContractError("PRECIPITATION_ACCUMULATOR_REGRESSION")
        precipitation = max(0.0, delta)
        precipitation_previous = accumulated
        u, v = series["U_10M"][instant], series["V_10M"][instant]
        rows[instant] = {
            "cloudCoverPct": round(max(0.0, min(100.0, series["CLCT"][instant])), 1),
            "relativeHumidityPct": round(rh_from_temperature(t, td), 1),
            "precipitationMm": round(precipitation, 3),
            "windSpeedKmh": round(math.hypot(u, v) * 3.6, 1),
            "windGustKmh": round(max(0.0, series["VMAX_10M"][instant]) * 3.6, 1),
        }
    return rows


def altaz(ra_deg: float, dec_deg: float, jd: float, latitude: float, longitude: float) -> tuple[float, float]:
    t = (jd - 2451545.0) / 36525.0
    gmst = (280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t - t * t * t / 38710000) % 360
    ha = math.radians((gmst + longitude - ra_deg) % 360)
    dec, lat = math.radians(dec_deg), math.radians(latitude)
    altitude = math.asin(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(ha))
    azimuth = math.atan2(-math.sin(ha), math.tan(dec) * math.cos(lat) - math.sin(lat) * math.cos(ha))
    return math.degrees(altitude), math.degrees(azimuth) % 360


def angular_separation(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    r1, r2, d1, d2 = map(math.radians, (ra1, ra2, dec1, dec2))
    cosine = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def illuminated_fraction(sun_ra: float, sun_dec: float, moon_ra: float, moon_dec: float) -> float:
    """Return the geocentric lunar illuminated fraction from one ephemeris solution."""
    elongation = math.radians(angular_separation(sun_ra, sun_dec, moon_ra, moon_dec))
    return (1 - math.cos(elongation)) / 2


def astronomy(instant: dt.datetime, latitude: float, longitude: float, elevation: float, targets: list[dict]) -> dict:
    import swisseph as swe
    hour = instant.hour + instant.minute / 60 + instant.second / 3600
    jd = swe.julday(instant.year, instant.month, instant.day, hour, swe.GREG_CAL)
    # Explicit Moshier mode prevents Swiss Ephemeris from silently switching
    # between external ephemeris files and its bundled local implementation.
    flags = swe.FLG_MOSEPH | swe.FLG_EQUATORIAL
    sun = swe.calc_ut(jd, swe.SUN, flags)[0]
    moon = swe.calc_ut(jd, swe.MOON, flags)[0]
    geopos = (longitude, latitude, elevation)
    sun_az_south, sun_alt, _ = swe.azalt(jd, swe.EQU2HOR, geopos, 0, 0, sun[:3])
    moon_az_south, moon_alt, _ = swe.azalt(jd, swe.EQU2HOR, geopos, 0, 0, moon[:3])
    illumination = illuminated_fraction(sun[0], sun[1], moon[0], moon[1])
    facts = {"solarAltitudeDeg": round(sun_alt, 2), "moonAltitudeDeg": round(moon_alt, 2),
             "moonAzimuthDeg": round((moon_az_south + 180) % 360, 2), "moonIlluminatedFraction": round(illumination, 3), "targets": {}}
    for target in targets:
        altitude, azimuth = altaz(target["raDegJ2000"], target["decDegJ2000"], jd, latitude, longitude)
        facts["targets"][target["targetKey"]] = {"altitudeDeg": round(altitude, 2), "azimuthDeg": round(azimuth, 2),
            "moonSeparationDeg": round(angular_separation(target["raDegJ2000"], target["decDegJ2000"], moon[0], moon[1]), 2)}
    return facts


def factors(weather: dict, astro: dict) -> tuple[float, float]:
    darkness = max(0.0, min(1.0, -astro["solarAltitudeDeg"] / 18.0))
    altitude = max(0.0, min(1.0, astro["altitudeDeg"] / 60.0))
    lunar = max(0.0, min(1.0, astro["moonSeparationDeg"] / 90.0))
    astronomy_factor = 0.55 * altitude + 0.25 * lunar + 0.20 * darkness
    weather_factor = (0.55 * (1 - weather["cloudCoverPct"] / 100) + 0.20 * (1 if weather["precipitationMm"] == 0 else 0)
                      + 0.15 * (1 - weather["relativeHumidityPct"] / 100) + 0.10 * max(0, 1 - weather["windSpeedKmh"] / 40))
    return round(astronomy_factor, 4), round(weather_factor, 4)


def candidate_case(setup: dict, target: dict) -> dict:
    """Bounded advisory suitability for a public catalog candidate."""
    short_fov_arcmin = min(setup["fovDeg"].values()) * 60
    extent = float(target["angularSizeEquivalentArcmin"])
    ratio = extent / short_fov_arcmin
    framing = round(max(20.0, min(100.0, 100.0 - max(0.0, ratio - 0.7) * 55)), 1)
    expected = "EMISSION_LINE" if any("SHO" in item or "Extreme" in item for item in setup["filterFamilies"]) else "BROADBAND_CONTINUUM"
    filter_signal = 95.0 if target["preferredSignalFamily"] == expected else 75.0
    scale = 92.0 if extent >= 30 and setup["effectiveFocalLengthMm"] <= 800 else (88.0 if extent < 30 else 72.0)
    aggregate = round(0.45 * framing + 0.30 * filter_signal + 0.25 * scale, 1)
    reasons = ["CATALOG_COORDINATES_PUBLICLY_GOVERNED", "SUITABILITY_IS_ADVISORY_DERIVED", "TARGET_NOT_PRESENT_IN_IMPORTED_SESSION_HISTORY"]
    reasons.append("TARGET_EXTENT_FITS_DECLARED_FOV" if ratio <= 1.0 else "TARGET_EXTENT_EXCEEDS_DECLARED_SHORT_FOV")
    return {"setupId": setup["setupId"], "targetKey": target["targetKey"],
            "inputs": {"framingRatioToShortFov": round(ratio, 3), "imageScaleArcsecPx": setup["imageScaleArcsecPx"],
                        "filterFamilyUsedForAssessment": setup["filterFamilies"][0], "targetSignalFamily": target["preferredSignalFamily"]},
            "components": {"framing": framing, "filterSignal": filter_signal, "imageScaleObjectClass": scale},
            "aggregateScore": aggregate, "reasonCodes": reasons}


def build_projection(now: dt.datetime, run: str, retrieval: dt.datetime, weather: dict, files: list[dict], site: dict, f8: dict, suitability: dict) -> dict:
    run_time = dt.datetime.strptime(run, "%Y%m%d%H").replace(tzinfo=dt.timezone.utc)
    age = (retrieval - run_time).total_seconds() / 3600
    if age < 0 or age > 18:
        raise ContractError("STALE_RUN")
    geo = site["sitePayload"]["geodesy"]
    local = now.astimezone(ZoneInfo(site["sitePayload"]["timezoneIana"]))
    night_date = local.date() if local.hour >= 12 else local.date() - dt.timedelta(days=1)
    start = dt.datetime.combine(night_date, dt.time(15), tzinfo=dt.timezone.utc)
    instants = [start + dt.timedelta(hours=i) for i in range(16)]
    if any(i not in weather for i in instants):
        raise ContractError("CURRENT_NIGHT_NOT_COVERED")
    catalog = json.loads(TARGET_CATALOG_PATH.read_text(encoding="utf-8"))
    history_keys = {item["targetKey"] for item in f8["targetProfiles"]}
    targets = [dict(item, acquisitionState="ACQUIRED_HISTORY") for item in f8["targetProfiles"]]
    targets.extend(dict(item, acquisitionState="NOT_YET_ACQUIRED") for item in catalog["targets"] if item["targetKey"] not in history_keys)
    rows = []
    for instant in instants:
        a = astronomy(instant, geo["latitudeDeg"], geo["longitudeDeg"], geo["elevationM"], targets)
        target_rows = {}
        for target in targets:
            values = a["targets"][target["targetKey"]]
            af, wf = factors(weather[instant], {**values, "solarAltitudeDeg": a["solarAltitudeDeg"]})
            target_rows[target["targetKey"]] = {**values, "astronomyFactor": af, "weatherFactor": wf}
        rows.append({"validAtUtc": utc(instant), "solarAltitudeDeg": a["solarAltitudeDeg"], "moonAltitudeDeg": a["moonAltitudeDeg"],
                     "moonIlluminatedFraction": a["moonIlluminatedFraction"], "weather": weather[instant], "targets": target_rows})
    case_map = {(c["setupId"], c["targetKey"]): c for c in suitability["cases"]}
    for setup in f8["setupProfiles"]:
        for target in targets:
            case_map.setdefault((setup["setupId"], target["targetKey"]), candidate_case(setup, target))
    provenance = list(suitability["catalogProvenance"])
    provenance.extend({"targetKey": item["targetKey"], "sourceAuthority": item["catalogEvidence"], "sourceIdentifier": item["targetName"], "fact": "PUBLIC_CATALOG_COORDINATE_AND_EXTENT"} for item in catalog["targets"])
    suitability_public = {"methodId": suitability["methodId"], "componentWeights": suitability["componentWeights"],
                          "componentSemantics": suitability["componentSemantics"], "catalogProvenance": provenance,
                          "sourceBindings": {**suitability["sourceBindings"], "targetCatalog": str(TARGET_CATALOG_PATH).replace("\\", "/")}, "cases": []}
    for case in case_map.values():
        suitability_public["cases"].append({"setupId": case["setupId"], "targetKey": case["targetKey"], "inputs": case["inputs"],
                                             "components": case["components"], "aggregateScore": case["aggregateScore"], "reasonCodes": case["reasonCodes"]})
    rankings = []
    for setup in f8["setupProfiles"]:
        ranked = []
        for target in targets:
            case = case_map[(setup["setupId"], target["targetKey"])]
            windows = []
            for first, second in zip(rows, rows[1:]):
                a, b = first["targets"][target["targetKey"]], second["targets"][target["targetKey"]]
                if first["solarAltitudeDeg"] > -18 or second["solarAltitudeDeg"] > -18 or a["altitudeDeg"] <= 0 or b["altitudeDeg"] <= 0:
                    continue
                score = 100 * (0.6 * ((a["astronomyFactor"] + b["astronomyFactor"]) / 2) + 0.3 * ((a["weatherFactor"] + b["weatherFactor"]) / 2) + 0.1 * case["aggregateScore"] / 100)
                windows.append({"fromUtc": first["validAtUtc"], "toUtcExclusive": utc(dt.datetime.fromisoformat(second["validAtUtc"].replace("Z", "+00:00")) + dt.timedelta(hours=1)),
                                "advisoryScore": round(score, 1), "meanAltitudeDeg": round((a["altitudeDeg"] + b["altitudeDeg"]) / 2, 1),
                                "meanCloudCoverPct": round((first["weather"]["cloudCoverPct"] + second["weather"]["cloudCoverPct"]) / 2, 1)})
            windows.sort(key=lambda x: (-x["advisoryScore"], x["fromUtc"]))
            ranked.append({"targetKey": target["targetKey"], "targetName": target["targetName"], "acquisitionState": target["acquisitionState"], "setupSuitabilityScore": case["aggregateScore"], "bestWindows": windows[:3]})
        ranked.sort(key=lambda x: (-(x["bestWindows"][0]["advisoryScore"] if x["bestWindows"] else -1), x["targetKey"]))
        rankings.append({"setupId": setup["setupId"], "targets": ranked})
    return {"schemaVersion": "1.0", "projectionType": "BKL031_F9_REPEATABLE_CURRENT_NIGHT", "generatedAtUtc": utc(retrieval),
            "environment": "EVALUATION", "authority": "NONE", "consumerMode": "READ_ONLY",
            "site": {"publicLabel": site["sitePayload"]["publicationPolicy"]["siteLabelGeneralized"], "timezoneIana": site["sitePayload"]["timezoneIana"], "coordinateDisclosure": "PROHIBITED"},
            "forecast": {"providerId": "METEOHUB", "upstreamAuthorityId": "ITALIAMETEO_ARPAE", "modelId": "ICON_2I", "runInitialisationUtc": utc(run_time),
                         "retrievedAtUtc": utc(retrieval), "runAgeHoursAtRetrieval": round(age, 6), "freshnessState": "FRESH", "sourceFiles": files},
            "nightWindow": {"fromUtc": utc(instants[0]), "toUtcExclusive": utc(instants[-1] + dt.timedelta(hours=1))},
            "method": {"id": "BKL031-F9-SWISSEPH-MOSHIER-SIDEREAL@1.0", "ephemerisMode": "EXPLICIT_MOSEPH_NO_FALLBACK", "scoreWeights": f8["method"]["scoreWeights"], "displayFilter": "solarAltitudeDeg <= -18 and targetAltitudeDeg > 0"},
            "setupProfiles": f8["setupProfiles"], "targetProfiles": targets, "targetCatalog": {"catalogId": catalog["catalogId"], "catalogCompleteness": catalog["catalogCompleteness"], "candidateCount": len(catalog["targets"])}, "suitabilityEvidence": suitability_public, "hourly": rows, "rankings": rankings,
            "boundaries": {"recurringTraffic": True, "maximumAcquisitionsPerDay": 2, "monetaryBudgetEur": 0, "rawGribRetention": "NONE_EPHEMERAL_ONLY",
                           "readinessAuthority": False, "automaticTargetSelection": False, "schedulingAuthority": False, "actionAuthority": "NONE", "commandAuthority": "NONE",
                           "safetyAuthority": "LOCAL_PHYSICAL_INTERLOCKS", "protectedCoordinatesPublished": False},
            "attribution": {"source": "Agenzia ItaliaMeteo / ARPAE ICON-2I via MeteoHub", "license": "CC BY 4.0", "licenseUrl": "https://creativecommons.org/licenses/by/4.0/"}}


def validate_projection(data: dict, now: dt.datetime | None = None) -> None:
    if (data.get("schemaVersion") != "1.0" or data.get("projectionType") != "BKL031_F9_REPEATABLE_CURRENT_NIGHT"
            or data.get("environment") != "EVALUATION" or data.get("authority") != "NONE" or data.get("consumerMode") != "READ_ONLY"):
        raise ContractError("IDENTITY_OR_AUTHORITY")
    forecast = data.get("forecast", {})
    if (forecast.get("providerId") != "METEOHUB" or forecast.get("upstreamAuthorityId") != "ITALIAMETEO_ARPAE"
            or forecast.get("modelId") != "ICON_2I" or forecast.get("freshnessState") != "FRESH"):
        raise ContractError("FORECAST_LINEAGE")
    boundary = data.get("boundaries", {})
    expected = {"recurringTraffic": True, "maximumAcquisitionsPerDay": 2, "monetaryBudgetEur": 0, "rawGribRetention": "NONE_EPHEMERAL_ONLY", "readinessAuthority": False,
                "automaticTargetSelection": False, "schedulingAuthority": False, "actionAuthority": "NONE", "commandAuthority": "NONE", "safetyAuthority": "LOCAL_PHYSICAL_INTERLOCKS", "protectedCoordinatesPublished": False}
    if any(boundary.get(k) != v for k, v in expected.items()):
        raise ContractError("BOUNDARY")
    raw = json.dumps(data).lower()
    for key in ("latitudedeg", "longitudedeg", "elevationm", "gridlatitude", "gridlongitude"):
        if key in raw:
            raise ContractError("PROTECTED_COORDINATE_KEY")
    if data.get("site", {}).get("coordinateDisclosure") != "PROHIBITED" or not data["site"].get("publicLabel"):
        raise ContractError("SITE_PUBLICATION_POLICY")
    source_files = forecast.get("sourceFiles", [])
    if ({item.get("variable") for item in source_files} != set(VARIABLES) or len(source_files) != len(VARIABLES)
            or any(not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256", ""))) for item in source_files)
            or any(not isinstance(item.get("byteLength"), int) or not 0 < item["byteLength"] <= MAX_FILE_BYTES or not item.get("unit") for item in source_files)
            or sum(item["byteLength"] for item in source_files) > MAX_TOTAL_BYTES):
        raise ContractError("SOURCE_FILE_EVIDENCE")
    try:
        run = dt.datetime.fromisoformat(forecast["runInitialisationUtc"].replace("Z", "+00:00"))
        retrieved = dt.datetime.fromisoformat(forecast["retrievedAtUtc"].replace("Z", "+00:00"))
        generated = dt.datetime.fromisoformat(data["generatedAtUtc"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError) as exc:
        raise ContractError("FORECAST_TIMESTAMPS") from exc
    age = (retrieved - run).total_seconds() / 3600
    if not 0 <= age <= 18 or generated != retrieved or abs(float(forecast.get("runAgeHoursAtRetrieval", -1)) - age) > 0.000001:
        raise ContractError("FORECAST_FRESHNESS_EVIDENCE")
    if data.get("method", {}).get("ephemerisMode") != "EXPLICIT_MOSEPH_NO_FALLBACK":
        raise ContractError("EPHEMERIS_MODE")
    if data.get("attribution", {}).get("license") != "CC BY 4.0":
        raise ContractError("ATTRIBUTION")
    suitability = data.get("suitabilityEvidence", {})
    weights = suitability.get("componentWeights", {})
    if suitability.get("methodId") != "BKL031-F8-SETUP-SUITABILITY@1.1" or set(weights) != {"framing", "filterSignal", "imageScaleObjectClass"} or abs(sum(float(v) for v in weights.values()) - 1) > 0.000001:
        raise ContractError("SUITABILITY_METHOD")
    hourly, rankings = data.get("hourly", []), data.get("rankings", [])
    if len(hourly) != 16 or not rankings:
        raise ContractError("INCOMPLETE_PROJECTION")
    try:
        instants = [dt.datetime.fromisoformat(row["validAtUtc"].replace("Z", "+00:00")) for row in hourly]
    except (KeyError, TypeError, ValueError) as exc:
        raise ContractError("HOURLY_TIMESTAMPS") from exc
    if any(b - a != dt.timedelta(hours=1) for a, b in zip(instants, instants[1:])):
        raise ContractError("NON_CONTIGUOUS_HOURLY")
    window = data.get("nightWindow", {})
    if window.get("fromUtc") != utc(instants[0]) or window.get("toUtcExclusive") != utc(instants[-1] + dt.timedelta(hours=1)):
        raise ContractError("NIGHT_WINDOW")
    target_keys = {item.get("targetKey") for item in data.get("targetProfiles", [])}
    setup_ids = {item.get("setupId") for item in data.get("setupProfiles", [])}
    if None in target_keys or None in setup_ids or not target_keys or not setup_ids or {item.get("setupId") for item in rankings} != setup_ids:
        raise ContractError("PROFILE_BINDING")
    for row in hourly:
        weather = row.get("weather", {})
        if (not 0 <= weather.get("cloudCoverPct", -1) <= 100 or not 0 <= weather.get("relativeHumidityPct", -1) <= 100
                or weather.get("precipitationMm", -1) < 0 or weather.get("windSpeedKmh", -1) < 0 or weather.get("windGustKmh", -1) < 0
                or set(row.get("targets", {})) != target_keys):
            raise ContractError("HOURLY_VALUES")
    if any({target.get("targetKey") for target in ranking.get("targets", [])} != target_keys for ranking in rankings):
        raise ContractError("RANKING_BINDING")
    expected_cases = {(setup_id, target_key) for setup_id in setup_ids for target_key in target_keys}
    cases = suitability.get("cases", [])
    if {(case.get("setupId"), case.get("targetKey")) for case in cases} != expected_cases:
        raise ContractError("SUITABILITY_BINDING")
    for case in cases:
        components = case.get("components", {})
        if set(components) != set(weights) or any(not 0 <= float(value) <= 100 for value in components.values()) or not 0 <= float(case.get("aggregateScore", -1)) <= 100 or not case.get("reasonCodes"):
            raise ContractError("SUITABILITY_COMPONENTS")
    if now is not None:
        current_age = (now - run).total_seconds()
        if current_age < 0 or current_age > 18 * 3600:
            raise ContractError("STALE_PROJECTION")


def acquire(now: dt.datetime) -> dict:
    site = json.loads(SITE_PATH.read_text(encoding="utf-8"))
    if site.get("lifecycle", {}).get("state") != "APPROVED" or site["sitePayload"].get("classification") != "PROTECTED_EXACT_SITE":
        raise ContractError("SITE_AUTHORITY_UNAVAILABLE")
    geo = site["sitePayload"]["geodesy"]
    run = discover_run(now)
    series, evidence, total = {}, [], 0
    with tempfile.TemporaryDirectory(prefix="dsg-f9-grib-") as temporary:
        root = Path(temporary)
        for variable in VARIABLES:
            path = root / f"{variable}.grib"
            filename = discover_file(run, variable)
            size, digest = download(f"{BASE}/{run}/{variable}/{filename}", path)
            total += size
            if total > MAX_TOTAL_BYTES:
                raise ContractError("GRIB_TOTAL_BOUND_EXCEEDED")
            values, unit = read_series(path, geo["latitudeDeg"], geo["longitudeDeg"])
            series[variable] = values
            evidence.append({"variable": variable, "sha256": digest, "byteLength": size, "unit": unit})
        weather = weather_rows(series)
        projection = build_projection(now, run, dt.datetime.now(dt.timezone.utc), weather, evidence, site,
                                      json.loads(F8_PATH.read_text(encoding="utf-8")), json.loads(SUITABILITY_PATH.read_text(encoding="utf-8")))
    validate_projection(projection)
    return projection


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--validate", type=Path)
    args = parser.parse_args()
    if args.validate:
        validate_projection(json.loads(args.validate.read_text(encoding="utf-8")), dt.datetime.now(dt.timezone.utc))
        print("F9 projection verification OK")
        return
    now = dt.datetime.now(dt.timezone.utc)
    projection = acquire(now)
    args.output.write_text(json.dumps(projection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "UPDATED", "run": projection["forecast"]["runInitialisationUtc"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
