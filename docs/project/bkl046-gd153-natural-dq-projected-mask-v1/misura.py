"""Measure the effect of projecting real GD153 DQ masks onto intact apertures."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from math import isclose, log10
from pathlib import Path
from statistics import median
import sys
import warnings
from zipfile import ZipFile

PIN = "332dd68575af5517b439affaaa42102bf6482e103dc757e815677f5d0b19e723"


def check(ok, message):
    if not ok:
        raise ValueError(message)


def read(path, pin):
    data = path.read_bytes()
    check(sha256(data).hexdigest() == pin, f"Changed input: {path.name}")
    return data


def extract(path, pin, name, expected):
    with ZipFile(BytesIO(read(path, pin))) as archive:
        check(archive.namelist().count(name) == 1, f"Ambiguous archive member: {name}")
        data = archive.read(name)
    check(sha256(data).hexdigest() == expected, f"Changed archive member: {name}")
    return data


def helper(path, archive_pin, program_pin, function):
    program = extract(path, archive_pin, "misura.py", program_pin)
    scope = {"__name__": "verified_helper", "__file__": str(path)}
    exec(compile(program, str(path), "exec"), scope)
    return scope[function]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("protocol", "source", "sameVisit", "clean", "geometry", "estimator", "dependencies", "report"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    p = json.loads(read(args.protocol, PIN))
    pose = json.loads(read(args.source / "protocollo.json", p["poseProtocol"]))
    natural = json.loads(extract(args.sameVisit, p["sameVisitArchive"], "riscontro.json", p["sameVisitReport"]))
    clean = json.loads(extract(args.clean, p["cleanArchive"], "riscontro-verificato.json", p["cleanReport"]))
    sample = helper(args.geometry, p["geometryArchive"], p["geometryProgram"], "sample_mask")
    evaluate = helper(args.estimator, p["estimatorArchive"], p["estimatorProgram"], "evaluate")

    sys.path.insert(0, str(args.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import FITSFixedWarning, WCS

    warnings.filterwarnings("ignore", category=FITSFixedWarning)
    check((np.__version__, astropy.__version__) == ("2.3.5", "7.2.0"), "Dependency version changed")
    ref_key = p["comparisonAperture"]
    folder = args.source / "source"
    pam_name = "UVIS1wfc3_map.fits"
    pam = fits.getdata(BytesIO(read(folder / pam_name, pose["inputs"][pam_name])))
    source_rows = {row["file"]: row for row in clean["rows"]}
    check(set(source_rows) == {entry["file"] for entry in pose["observations"]} and len(source_rows) == 48,
          "Input coverage differs")
    rows = [row for row in natural["cases"] if row["family"] == "nativeCoreDq" and row["state"] == "MEASURED"]
    check(len(rows) == 2, "Expected two native DQ cases with clean comparison")

    records = []
    for damaged in rows:
        name, band = damaged["file"], damaged["band"]
        center = np.array(damaged["center"])
        baseline = damaged["phases"]
        check([phase["offsetPx"] for phase in baseline] == p["phaseOffsetsPx"], "Phase linkage differs")
        with fits.open(BytesIO(read(folder / name, pose["inputs"][name])), memmap=False) as h:
            sci = h["SCI", 1]
            check(h[0].header["FILTER"] == band and sci.header["CCDCHIP"] == 1, "Mask identity differs")
            damaged_wcs = WCS(sci.header, h).celestial
            usable = (h["DQ", 1].data == 0) & np.isfinite(sci.data)

        controls = [row for row in clean["rows"] if row["band"] == band and ref_key in row["measurements"]]
        check(all(any(ref == row["file"] for row in controls) for ref in damaged["referenceFiles"]),
              "Same-visit reference absent from intact inputs")
        for control in controls:
            ref = control["file"]
            check(ref != name, "Comparison contains damaged pose")
            xy = np.array(control["center"])
            with fits.open(BytesIO(read(folder / ref, pose["inputs"][ref])), memmap=False) as h:
                sci = h["SCI", 1]
                check(h[0].header["FILTER"] == band and sci.header["CCDCHIP"] == 1, "Control identity differs")
                cwcs = WCS(sci.header, h).celestial
                height, width = sci.data.shape
                ox, oy = (abs(float(sci.header[key])) for key in ("LTV1", "LTV2"))
                check((int(ox), int(oy)) == (ox, oy), "Non-integral PAM offset")
                ox, oy = int(ox), int(oy)
                image = sci.data.astype(float) * pam[oy:oy + height, ox:ox + width]
                yy, xx = np.indices(image.shape)
                r2 = (xx - xy[0])**2 + (yy - xy[1])**2
                aperture = r2 <= p["radiusPx"]**2
                truth = image[aperture] - control["measurements"][ref_key]["sky"]
                total = float(truth.sum())
                target_total = control["measurements"][ref_key]["rate"] * float(h[0].header["EXPTIME"])
                check((h["DQ", 1].data[aperture] == 0).all() and np.isfinite(truth).all()
                      and total > 0 and isclose(total, target_total, rel_tol=p["identityTolerance"]),
                      "Intact aperture reference changed")
                pixel = np.column_stack((xx[aperture], yy[aperture]))
                rings = np.floor(np.sqrt(r2[aperture])).astype(int)
                core = r2[aperture] <= p["coreRadiusPx"]**2
                projected = np.stack(damaged_wcs.world_to_pixel_values(*cwcs.pixel_to_world_values(*pixel.T)), axis=1)
                anchor = np.array(damaged_wcs.world_to_pixel_values(*cwcs.pixel_to_world_values(*xy)))
            shift = center - anchor
            check(np.isfinite(projected).all() and np.isfinite(shift).all(), "Non-finite mask transformation")
            for policy in p["policies"]:
                for phase in baseline:
                    offset = phase["offsetPx"]
                    keep = sample(np, usable, projected + shift + offset, policy)
                    estimates = evaluate(np, truth, keep, rings)
                    effect = {key: -2500 * log10(value / total) if value is not None and value > 0 else None
                              for key, value in estimates.items()}
                    if keep.all():
                        check(all(value is not None and abs(value) <= 1e-10 for value in effect.values()),
                              "Fully supported aperture changed")
                    records.append(dict(damaged=name, damagedVisit=damaged["visit"], band=band, intactReference=ref,
                                        intactVisit=control["visit"], originalSameVisitComparator=ref in damaged["referenceFiles"],
                                        policy=policy, offsetPx=offset, centerAlignmentShiftPx=shift.tolist(),
                                        apertureMissing=int((~keep).sum()), coreMissing=int((core & ~keep).sum()),
                                        inducedDifferenceMillimag=effect,
                                        observedDifferenceMillimag=phase.get("withinVisitDifferenceMillimag", {})))

    summaries = []
    for row in rows:
        for policy in p["policies"]:
            for only_sibling in (True, False):
                pool = [entry for entry in records if entry["damaged"] == row["file"] and entry["policy"] == policy
                        and entry["originalSameVisitComparator"] == only_sibling]
                for method in ("zero", "area", "annularMedian"):
                    pairs = [(a, b) for entry in pool
                             if (a := entry["inducedDifferenceMillimag"].get(method)) is not None
                             and (b := entry["observedDifferenceMillimag"].get(method)) is not None]
                    values = [a for a, _ in pairs]
                    check(values, "Empty impact group")
                    summaries.append(dict(damaged=row["file"], policy=policy, originalSameVisitComparator=only_sibling,
                                          method=method, scenarios=len(pool), comparableScenarios=len(pairs),
                                          distinctIntactReferences=len({c["intactReference"] for c in pool}),
                                          distinctIntactVisits=len({c["intactVisit"] for c in pool}),
                                          inducedRange=[min(values), max(values)], inducedMedian=median(values),
                                          observedRange=[min(b for _, b in pairs), max(b for _, b in pairs)],
                                          nearestAbsoluteDifference=min(abs(a - b) for a, b in pairs)))
    output = dict(schema=p["schema"] + "_RESULT", protocolSha256=PIN,
                  programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  nativeDqCases=len(rows), independentTargets=1, projectedScenarios=len(records),
                  records=records, summary=summaries, sameExposureTruthVerified=False,
                  nativeExecutions=0, scientificClosures=0)
    with args.report.open("x", newline="\n", encoding="utf-8") as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()