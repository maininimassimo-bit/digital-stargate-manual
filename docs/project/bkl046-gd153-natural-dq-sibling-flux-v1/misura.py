"""Compare GD153 natural DQ apertures with clean, same-visit FLC siblings."""
import argparse
from collections import defaultdict
from hashlib import sha256
from io import BytesIO
import json
from math import isclose, log10
from pathlib import Path
from statistics import median
import sys
import warnings
from zipfile import ZipFile

PIN = "927f7bd4407b3f73a7391e0d3eb47f6e92669041614631c83755e471b4c293eb"


def check(ok, message):
    if not ok:
        raise ValueError(message)


def read(path, pin):
    data = path.read_bytes()
    check(sha256(data).hexdigest() == pin, f"Changed input: {path.name}")
    return data


def photometry(np, sci, dq, xy, p):
    x, y = xy
    inner, outer = p["skyAnnulusPx"]
    radius = p["radiusPx"]
    height, width = sci.shape
    if not (outer <= x < width - outer and outer <= y < height - outer):
        return {"state": "SKY_OUTSIDE"}
    yy, xx = np.ogrid[:height, :width]
    r2 = (xx - x)**2 + (yy - y)**2
    aperture = r2 <= radius**2
    sky_ring = (r2 >= inner**2) & (r2 <= outer**2)
    valid = (dq == 0) & np.isfinite(sci)
    sky_good = sky_ring & valid
    if sky_good.sum() < p["minimumGoodSkyFraction"] * sky_ring.sum():
        return {"state": "SKY_INCOMPLETE"}
    flags = int(np.bitwise_or.reduce(dq[aperture], initial=0))
    counts = dict(aperturePixels=int(aperture.sum()), missing=int((aperture & ~valid).sum()),
                  coreMissing=int(((r2 <= p["coreRadiusPx"]**2) & ~valid).sum()), dqBits=flags)
    if any(flags & code for code in p["flagsRejectedEntireAperture"]):
        return dict(state="SATURATION_DQ", **counts)
    if not (aperture & valid).any():
        return dict(state="NO_RETAINED_APERTURE", **counts)
    sky = float(np.median(sci[sky_good]))
    use = valid[aperture]
    rings = np.floor(np.sqrt(r2[aperture])).astype(int)
    samples = sci[aperture] - sky
    subtotal = float(samples[use].sum())
    area = subtotal * len(use) / int(use.sum())
    annular = subtotal
    for ring in np.unique(rings[~use]):
        observed = (rings == ring) & use
        if not observed.any():
            annular = None
            break
        annular += float(np.median(samples[observed])) * int(((rings == ring) & ~use).sum())
    return dict(state="MEASURED", sky=sky, **counts, flux=dict(zero=subtotal, area=area, annularMedian=annular))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("protocol", "source", "cleanArchive", "dependencies", "report"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    p = json.loads(read(args.protocol, PIN))
    pose = json.loads(read(args.source / "protocollo.json", p["poseProtocol"]))
    with ZipFile(BytesIO(read(args.cleanArchive, p["cleanArchive"]))) as archive:
        name = "riscontro-verificato.json"
        check(archive.namelist().count(name) == 1, "Ambiguous aperture report member")
        raw = archive.read(name)
    check(sha256(raw).hexdigest() == p["cleanReport"], "Aperture report changed")
    previous = json.loads(raw)

    sys.path.insert(0, str(args.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import FITSFixedWarning, WCS

    warnings.filterwarnings("ignore", category=FITSFixedWarning)
    check((np.__version__, astropy.__version__) == ("2.3.5", "7.2.0"), "Dependency version changed")
    data = args.source / "source"
    pam_name = "UVIS1wfc3_map.fits"
    with fits.open(BytesIO(read(data / pam_name, pose["inputs"][pam_name])), memmap=False) as handle:
        pam = next(hdu.data for hdu in handle if hdu.data is not None).astype(float)
    key = p["aperture"]
    templates = {row["file"]: row for row in previous["rows"]}
    check(set(templates) == {row["file"] for row in pose["observations"]} and len(templates) == 48,
          "Exposure coverage changed")
    siblings = defaultdict(list)
    wcs = {}
    clean_count = 0
    for name, row in templates.items():
        with fits.open(BytesIO(read(data / name, pose["inputs"][name])), memmap=False) as handle:
            header, sci = handle[0].header, handle["SCI", 1]
            wcs[name] = WCS(sci.header, handle).celestial
            check(wcs[name].has_celestial
                  and (header["FILTER"], header["TARGNAME"], header["PROPOSID"], header["EXPFLAG"],
                       header["SCAN_TYP"], header["PCTECORR"], header["FLUXCORR"], sci.header["CCDCHIP"],
                       sci.header["BUNIT"]) == (row["band"], "GD153", 11450, "NORMAL", "N", "COMPLETE",
                                                 "COMPLETE", 1, "ELECTRONS"), "FLC header mismatch")
            check(isclose(float(header["EXPSTART"]), row["startMjd"], rel_tol=0, abs_tol=1e-10)
                  and isclose(float(sci.header["PHOTFLAM"]), row["flam"], rel_tol=1e-12), "Timing or PHOTFLAM mismatch")
        if key in row["measurements"]:
            siblings[row["visit"], row["band"]].append(row)
            clean_count += 1

    cases = []
    for name, row in templates.items():
        is_clean = key in row["measurements"]
        family = "clean" if is_clean else "nativeCoreDq" if row["previousState"] == "REJECTED_CORE_DQ" else "otherApertureRejected"
        reference = [other for other in siblings[row["visit"], row["band"]] if other["file"] != name
                     and abs(row["startMjd"] - other["startMjd"]) <= p["maximumSameVisitTimeSpanDays"]]
        result = dict(file=name, visit=row["visit"], band=row["band"], previousState=row["state"], family=family,
                      referenceFiles=[other["file"] for other in reference], referenceCount=len(reference))
        cases.append(result)
        if not reference:
            result["state"] = "NO_CLEAN_SIBLING"
            continue
        predicted = np.array([wcs[name].world_to_pixel_values(
            *wcs[other["file"]].pixel_to_world_values(*other["center"])) for other in reference])
        check(np.isfinite(predicted).all(), "Non-finite WCS center")
        xy = np.median(predicted, axis=0)
        spread = float(np.linalg.norm(predicted - xy, axis=1).max()) if len(predicted) > 1 else None
        result.update(center=xy.tolist(), projectionSpreadPx=spread,
                      distanceFromMeasuredCenterPx=(float(np.linalg.norm(xy - row["center"]))
                                                    if "center" in row else None))
        if spread is not None and spread > p["maximumPredictionSpreadPx"]:
            result["state"] = "PROJECTION_DISAGREEMENT"
            continue
        baseline = median(other["flam"] * other["measurements"][key]["rate"] for other in reference)
        check(baseline > 0, "Non-positive clean sibling baseline")
        result["referenceFluxCalibrated"] = baseline
        with fits.open(BytesIO(read(data / name, pose["inputs"][name])), memmap=False) as handle:
            sci = handle["SCI", 1]
            height, width = sci.data.shape
            ox, oy = (abs(float(sci.header[k])) for k in ("LTV1", "LTV2"))
            check((int(ox), int(oy)) == (ox, oy), "Non-integral PAM offset")
            ox, oy = int(ox), int(oy)
            corrected = sci.data.astype(float) * pam[oy:oy + height, ox:ox + width]
            flags = handle["DQ", 1].data
            factor = row["flam"] / float(handle[0].header["EXPTIME"])
            if is_clean:
                control = photometry(np, corrected, flags, row["center"], p)
                check(control["state"] == "MEASURED" and control["missing"] == 0
                      and isclose(control["flux"]["zero"] * factor, row["measurements"][key]["rate"] * row["flam"],
                                  rel_tol=p["relativeCleanReplayTolerance"]), "Clean aperture replay differs")
            phases = []
            for offset in p["phasesPx"]:
                measure = photometry(np, corrected, flags, xy + offset, p)
                measure["offsetPx"] = offset
                if measure["state"] == "MEASURED":
                    measure["withinVisitDifferenceMillimag"] = {
                        method: -2500 * log10(value * factor / baseline) if value is not None and value > 0 else None
                        for method, value in measure["flux"].items()
                    }
                phases.append(measure)
        result.update(state=phases[0]["state"], phases=phases)
    report = dict(schema=p["schema"] + "_RESULT", protocolSha256=PIN,
                  programSha256=sha256(Path(__file__).read_bytes()).hexdigest(), allFLC=len(templates),
                  cleanReferenceExposures=clean_count, referenceVisits=len({r["visit"] for r in cases}),
                  cases=cases, independentTargets=1, sameExposureMissingPixelTruthVerified=False,
                  nativeExecutions=0, scientificClosures=0)
    with args.report.open("x", newline="\n", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()