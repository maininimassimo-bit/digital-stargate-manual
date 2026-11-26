"""Audit the original acquisition inventory for usable coobserved sky controls."""
import argparse
from datetime import datetime, timedelta
from hashlib import file_digest, sha256
import json
from math import asin, cos, degrees, radians, sin, sqrt
from pathlib import Path
import re
from zipfile import ZipFile


KEYS = ("IMAGETYP", "DATE-OBS", "EXPTIME", "RA", "DEC", "FILTER", "INSTRUME",
        "GAIN", "OFFSET", "BAYERPAT", "XBINNING", "YBINNING", "NAXIS1", "NAXIS2")


def read(path, pin):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != pin:
        raise ValueError("PIN_CHANGED:" + path.name)
    return json.loads(raw)


def value_of(card):
    value = card[10:].lstrip()
    if value.startswith("'"):
        m = re.match(r"'((?:[^']|'')*)'", value)
        if m is None:
            raise ValueError("BAD_FITS_STRING")
        return m[1].replace("''", "'").strip()
    return float(value.split("/", 1)[0].strip().replace("D", "E"))


def inventory_entry(z, label, p, row):
    h = sha256()
    result = {}
    with z.open(row["file"]) as f:
        for _ in range(128):
            raw = f.read(2880)
            assert len(raw) == 2880
            h.update(raw)
            ended = False
            for i in range(0, len(raw), 80):
                card = raw[i:i+80].decode("ascii")
                key = card[:8].strip()
                if key == "END":
                    ended = True
                    break
                if key in KEYS and card[8:10] == "= ":
                    assert key not in result, key
                    result[key] = value_of(card)
            if ended:
                break
        else:
            raise ValueError("NO_FITS_HEADER_END")
        while block := f.read(1024 * 1024):
            h.update(block)
    assert h.hexdigest() == row["sha256"]
    assert result["IMAGETYP"] == row["type"] == p["targetPartition"][label]
    assert result["DATE-OBS"] == row["date"]
    assert result["EXPTIME"] == row["exposureS"]
    return {"memberSha256": h.hexdigest(), "header": result}


def separation(ra, dec, anchor):
    a, b, c, d = map(radians, (ra, dec, *anchor))
    haversine = sin((b-d)/2)**2 + cos(b) * cos(d) * sin((a-c)/2)**2
    return degrees(2*asin(min(1., sqrt(haversine))))


def run(protocol, calibration, receipt, archives):
    captures = {}
    summaries = {}
    for key, path in archives.items():
        name, pin = calibration["archivePins"][key]
        assert path.name == name
        with path.open("rb") as f:
            assert file_digest(f, "sha256").hexdigest() == pin, path.name
        rows = receipt["sourceMembers"][key]
        with ZipFile(path) as z:
            expected = {r["file"] for r in rows}
            actual = [item.filename for item in z.infolist() if not item.is_dir()]
            assert len(expected) == len(actual) == len(rows) == 15
            assert set(actual) == expected
            entries = [inventory_entry(z, key, protocol, row) for row in rows]
        captures[key] = entries
        headers = [e["header"] for e in entries]
        times = [datetime.fromisoformat(h["DATE-OBS"]) for h in headers]
        end = max(t + timedelta(seconds=h["EXPTIME"]) for t, h in zip(times, headers, strict=True))
        observed = sorted({(h["RA"], h["DEC"]) for h in headers if "RA" in h and "DEC" in h})
        summaries[key] = {"members": len(entries), "firstDateObs": min(times).isoformat(),
                         "lastExposureEndFromHeader": end.isoformat(), "uniqueObjectCoordinatesDeg": observed,
                         "imageTypes": sorted({h["IMAGETYP"] for h in headers}),
                         "filterHeaderValues": sorted({h["FILTER"] for h in headers if "FILTER" in h}),
                         "instrument": sorted({h["INSTRUME"] for h in headers}),
                         "integerSettings": {k: sorted({int(h[k]) for h in headers}) for k in
                           ("GAIN", "OFFSET", "XBINNING", "YBINNING")}}
    coords = summaries["light"]["uniqueObjectCoordinatesDeg"]
    anchor = protocol["referenceTangentDeg"]
    shifts = [{"coords": row, "separationFromTangentDeg": separation(*row, anchor)} for row in coords]
    return captures, summaries, shifts


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "calibration", "receipt", "light", "dark", "flat", "shortDark", "output"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    plan = json.loads(a.protocol.read_bytes())
    calibration = read(a.calibration, plan["calibrationProtocolSha256"])
    receipt = read(a.receipt, plan["calibrationReportSha256"])
    assert receipt["protocolSha256"] == plan["calibrationProtocolSha256"]
    archives = {name: getattr(a, name) for name in plan["targetPartition"]}
    entries, summaries, pointing = run(plan, calibration, receipt, archives)
    bound = max(row["separationFromTangentDeg"] for row in pointing)
    # A small metadata displacement inside the nominal camera margin remains
    # within the target footprint. This does not certify exact telescope positions.
    assert bound < plan["targetMetadataContainmentScreenDeg"]
    doc = {"schema": "BKL046_M8M20_OPTICAL_ANCHOR_ACQUISITION_AUDIT_RESULT_V1",
           "programSha256": sha256(Path(__file__).read_bytes()).hexdigest(),
           "protocolSha256": sha256(a.protocol.read_bytes()).hexdigest(),
           "maxTargetMetadataSeparationDeg": bound,"summaries": summaries, "memberHeaderReadback": entries, "targetObjectCoordinateReadbacks": pointing,
           "membersVerified": sum(row["members"] for row in summaries.values()),
           "separateSkyExposuresIdentified": 0, "coobservedBroadbandAnchors": 0,
           "classification": "NO_SEPARATE_SKY_POINTING_IN_FOUR_PINNED_ARCHIVES",
           "nativeExecutions": 0, "scientificClosures": 0}
    with a.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(doc, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
