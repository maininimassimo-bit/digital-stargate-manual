"""Verify three CALSPEC counterpart positions and extract sampled Gaia DR3 products."""
import csv
import gzip
from hashlib import file_digest, sha256
import json
from math import cos, hypot, isfinite, radians
from pathlib import Path
import sys

from math import isclose

EXPECTED = {
    "GD153": ("3944400490365194368", 194.259675, 22.031286111111, "446881-450181"),
    "GD71": ("3348071631670500736", 88.115083333333, 15.887008333333, "380498-380760"),
    "GRW+70 5824": ("1686708050268594944", 204.710325, 70.285455555556, "188927-191879"),
}
CSV_PIN = "9a52d608ef6d53ba3dea6042d0618b625ecf1806f1f17342d31edc6394239df7"
QUERY_PIN = "7d8a625a7b795c0c5b3d1f733617755129f8495a8146eabf7b1ace6d5add07fc"
CDN_PIN = "72309df5ebc95d1bd7a11865b400205b6974612cbf60012f9beb0c14b307385d"


def require(ok, label):
    if not ok:
        raise ValueError(label)


def read(path, pin):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == pin, "Changed metadata")
    return raw


def position_at_j2000(row, ra0, dec0):
    dt = 2000 - float(row["ref_epoch"])
    ra, dec = float(row["ra"]), float(row["dec"])
    x = (ra - ra0) * 3600 * cos(radians(dec)) + float(row["pmra"])*dt/1000
    y = (dec - dec0)*3600 + float(row["pmdec"])*dt/1000
    return hypot(x, y)


def sample(path, sid, metadata):
    with path.open("rb") as stream:
        require(file_digest(stream, "sha256").hexdigest() == metadata["sha256"], "Changed gzip")
    require(path.stat().st_size == metadata["bytes"], "Changed size")
    with gzip.open(path,"rt",encoding="utf-8",newline="") as stream:
        rows = csv.DictReader(line for line in stream if not line.startswith("#"))
        require(rows.fieldnames == ["source_id", "solution_id", "ra", "dec", "flux", "flux_error"],
                "Unexpected table schema")
        candidates = [row for row in rows if row["source_id"] == sid]
    require(len(candidates) == 1, "Expected exactly one record")
    row = candidates[0]
    flux, error = [json.loads(row[field]) for field in ("flux", "flux_error")]
    require(len(flux) == len(error) == 343 and all(isfinite(x) for x in flux)
            and all(isfinite(x) and x > 0 for x in error), "Invalid spectrum samples")
    return row["solution_id"], float(row["ra"]), float(row["dec"]), flux, error


def main():
    root, output, spectra = map(Path, sys.argv[1:])
    read(root / "gaia.adql", QUERY_PIN)
    csv_bytes = read(root / "gaia.csv", CSV_PIN)
    values = list(csv.DictReader(csv_bytes.decode().splitlines()))
    rows = {row["source_id"]:row for row in values}
    require(len(rows)==len(values), "Duplicate catalog source")
    require(rows["740620316527646848"]["has_xp_sampled"] == "1", "Positive control missing")
    cdn = {row["file"]:row for row in json.loads(read(root / "cdn.json", CDN_PIN))}
    require(len(cdn) == len(EXPECTED), "Unexpected CDN roster")
    reports = {}
    content = {}
    for star, (sid, ra, dec, interval) in EXPECTED.items():
        row = rows[sid]
        offset = position_at_j2000(row, ra, dec)
        require(offset < 0.3 and all(row[key]=="1" for key in ("has_xp_continuous", "has_xp_sampled")),
                "Counterpart or product flags differ")
        if star == "GD71":
            other = [candidate for candidate in values if candidate["source_id"] not in
                     {sid, "740620316527646848", "3944400490365194368", "1686708050268594944"}
                     and candidate["pmra"] and candidate["pmdec"]]
            require(other and all(position_at_j2000(candidate, ra, dec)>0.3 for candidate in other),
                    "Ambiguous GD71 counterpart")
        lo, hi = map(int, interval.split("-"))
        require(lo <= int(sid) >> 43 <= hi, "Source outside file range")
        filename = f"XpSampledMeanSpectrum_{interval}.csv.gz"
        solution, sampled_ra, sampled_dec, flux, error = sample(root / filename, sid, cdn[filename])
        require(isclose(sampled_ra,float(row["ra"]),abs_tol=1e-9,rel_tol=0.)
                and isclose(sampled_dec,float(row["dec"]),abs_tol=1e-9,rel_tol=0.),
                "Sampled position mismatch")
        content[star] = dict(sourceId=sid, solutionId=solution, flux=flux, fluxError=error)
        reports[star] = dict(sourceId=sid, offsetJ2000Arcsec=offset, sampledPoints=len(flux),
                            hasContinuousProduct=True, sampledArchiveSha256=cdn[filename]["sha256"])
    raw = (json.dumps(dict(spectra=content, gridNm=list(range(336,1021,2))),sort_keys=True,
                      allow_nan=False,indent=2)+"\n").encode()
    report = dict(schema="BKL046_GAIA_CALSPEC_XP_INGRESS_V1", targets=reports, spectraSha256=sha256(raw).hexdigest(),
                  gaiaQuerySha256=QUERY_PIN, gaiaResultSha256=CSV_PIN, cdnReceiptSha256=CDN_PIN,
                  sampledOnly=True, fullCovarianceAvailableFromTheseSamples=False,
                  newPhotometricComparisons=0, scientificClosures=0)
    with spectra.open("xb") as result:
        result.write(raw)
    with output.open("x",encoding="utf-8",newline="\n") as result:
        result.write(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
