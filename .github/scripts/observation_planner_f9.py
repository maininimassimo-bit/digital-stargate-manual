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
    illumination = float(swe.pheno_ut(jd, swe.MOON)[1])
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
    targets = f8["targetProfiles"]
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
            ranked.append({"targetKey": target["targetKey"], "targetName": target["targetName"], "setupSuitabilityScore": case["aggregateScore"], "bestWindows": windows[:3]})
        ranked.sort(key=lambda x: (-(x["bestWindows"][0]["advisoryScore"] if x["bestWindows"] else -1), x["targetKey"]))
        rankings.append({"setupId": setup["setupId"], "targets": ranked})
    return {"schemaVersion": "1.0", "projectionType": "BKL031_F9_REPEATABLE_CURRENT_NIGHT", "generatedAtUtc": utc(retrieval),
            "environment": "EVALUATION", "authority": "NONE", "consumerMode": "READ_ONLY",
            "site": {"publicLabel": site["sitePayload"]["publicationPolicy"]["siteLabelGeneralized"], "timezoneIana": site["sitePayload"]["timezoneIana"], "coordinateDisclosure": "PROHIBITED"},
            "forecast": {"providerId": "METEOHUB", "upstreamAuthorityId": "ITALIAMETEO_ARPAE", "modelId": "ICON_2I", "runInitialisationUtc": utc(run_time),
                         "retrievedAtUtc": utc(retrieval), "runAgeHoursAtRetrieval": round(age, 6), "freshnessState": "FRESH", "sourceFiles": files},
            "nightWindow": {"fromUtc": utc(instants[0]), "toUtcExclusive": utc(instants[-1] + dt.timedelta(hours=1))},
            "method": {"id": "BKL031-F9-SWISSEPH-MOSHIER-SIDEREAL@1.0", "ephemerisMode": "EXPLICIT_MOSEPH_NO_FALLBACK", "scoreWeights": f8["method"]["scoreWeights"], "displayFilter": "solarAltitudeDeg <= -18 and targetAltitudeDeg > 0"},
            "setupProfiles": f8["setupProfiles"], "targetProfiles": targets, "hourly": rows, "rankings": rankings,
            "boundaries": {"recurringTraffic": True, "maximumAcquisitionsPerDay": 2, "monetaryBudgetEur": 0, "rawGribRetention": "NONE_EPHEMERAL_ONLY",
                           "readinessAuthority": False, "automaticTargetSelection": False, "schedulingAuthority": False, "actionAuthority": "NONE", "commandAuthority": "NONE",
                           "safetyAuthority": "LOCAL_PHYSICAL_INTERLOCKS", "protectedCoordinatesPublished": False},
            "attribution": {"source": "Agenzia ItaliaMeteo / ARPAE ICON-2I via MeteoHub", "license": "CC BY 4.0", "licenseUrl": "https://creativecommons.org/licenses/by/4.0/"}}


def validate_projection(data: dict, now: dt.datetime | None = None) -> None:
    if data.get("projectionType") != "BKL031_F9_REPEATABLE_CURRENT_NIGHT" or data.get("authority") != "NONE" or data.get("consumerMode") != "READ_ONLY":
        raise ContractError("IDENTITY_OR_AUTHORITY")
    if data.get("forecast", {}).get("providerId") != "METEOHUB" or data["forecast"].get("modelId") != "ICON_2I" or data["forecast"].get("freshnessState") != "FRESH":
        raise ContractError("FORECAST_LINEAGE")
    boundary = data.get("boundaries", {})
    expected = {"maximumAcquisitionsPerDay": 2, "monetaryBudgetEur": 0, "rawGribRetention": "NONE_EPHEMERAL_ONLY", "readinessAuthority": False,
                "automaticTargetSelection": False, "schedulingAuthority": False, "actionAuthority": "NONE", "commandAuthority": "NONE", "safetyAuthority": "LOCAL_PHYSICAL_INTERLOCKS", "protectedCoordinatesPublished": False}
    if any(boundary.get(k) != v for k, v in expected.items()):
        raise ContractError("BOUNDARY")
    raw = json.dumps(data).lower()
    for key in ("latitudedeg", "longitudedeg", "elevationm", "gridlatitude", "gridlongitude"):
        if key in raw:
            raise ContractError("PROTECTED_COORDINATE_KEY")
    if not data.get("hourly") or not data.get("rankings"):
        raise ContractError("INCOMPLETE_PROJECTION")
    if now is not None:
        run = dt.datetime.fromisoformat(data["forecast"]["runInitialisationUtc"].replace("Z", "+00:00"))
        if (now - run).total_seconds() > 18 * 3600:
            raise ContractError("STALE_PROJECTION")


def acquire(now: dt.datetime) -> dict:
    site = json.loads(SITE_PATH.read_text(encoding="utf-8"))
    if site.get("lifecycle", {}).get("state") != "APPROVED" or site["sitePayload"].get("classification") != "PROTECTED_EXACT_SITE":
        raise ContractError("SITE_AUTHORITY_UNAVAILABLE")
    geo = site["sitePayload"]["geodesy"]
    run = discover_run(now)
    filename = f"ICON_2I_SURFACE_PRESSURE_LEVELS_{run}_surface-0.grib"
    series, evidence, total = {}, [], 0
    with tempfile.TemporaryDirectory(prefix="dsg-f9-grib-") as temporary:
        root = Path(temporary)
        for variable in VARIABLES:
            path = root / f"{variable}.grib"
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
        validate_projection(json.loads(args.validate.read_text(encoding="utf-8")))
        print("F9 projection verification OK")
        return
    now = dt.datetime.now(dt.timezone.utc)
    projection = acquire(now)
    args.output.write_text(json.dumps(projection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "UPDATED", "run": projection["forecast"]["runInitialisationUtc"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
