"""Measure paired DECam M20 science-frame repeatability after excluding FN1."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import re
import sys


def digest(path):
    with path.open("rb") as data:
        return file_digest(data, "sha256").hexdigest()


def section(text):
    x, x1, y, y1 = map(int, re.fullmatch(r"\[(\d+):(\d+),(\d+):(\d+)\]", text).groups())
    return x-1, x1, y-1, y1


def measure(np, image, usable, point, p):
    x, y = map(int, point)
    outer = p["skyAnnulusPx"][1] + 2
    if min(x, y) < outer or x+outer >= image.shape[1] or y+outer >= image.shape[0]:
        return None
    region = np.s_[y-outer:y+outer+1, x-outer:x+outer+1]
    values = image[region].astype(float)
    coords = np.arange(-outer, outer+1, dtype=float)
    dx, dy = np.meshgrid(coords, coords)
    square = dx**2 + dy**2
    sky = (square >= p["skyAnnulusPx"][0]**2) & (square <= p["skyAnnulusPx"][1]**2)
    center = square <= p["centroidPx"]**2
    valid = usable[region]
    if not (valid[sky].all() and valid[center].all()):
        return None
    median = float(np.median(values[sky]))
    noise = max(1, 1.4826 * float(np.median(np.abs(values[sky]-median))))
    if values[outer, outer]-median < p["peakBackgroundSnr"] * noise:
        return None
    weights = np.maximum(values[center]-median, 0)
    cx = np.average(dx[center], weights=weights)
    cy = np.average(dy[center], weights=weights)
    if cx**2 + cy**2 > 2.25:
        return None
    square = (dx-cx)**2 + (dy-cy)**2
    flux = []
    for radius in p["aperturesPx"]:
        aperture = square <= radius**2
        if not valid[aperture].all():
            return None
        flux.append(float((values[aperture]-median).sum()))
    if min(flux) <= 0:
        return None
    return {"xy": [x+float(cx), y+float(cy)], "flux": flux,
            "snrPeak": float((values[outer, outer]-median)/noise),
            "shapeRadiusPx": float(np.sqrt(np.average(square[center], weights=weights)))}


def main():
    cli = argparse.ArgumentParser()
    for name in ("root", "sourceKit", "dependencies", "report"):
        cli.add_argument(name, type=Path)
    a = cli.parse_args()
    proto = a.root / "protocollo.json"
    p = json.loads(proto.read_bytes())
    source_report = a.sourceKit / "riscontro.json"
    assert digest(source_report) == p["sourceReportSha256"]
    prior = json.loads(source_report.read_bytes())
    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")

    frames = []
    identities = []
    for row in prior["fields"]["M20"]["frames"]:
        small = a.sourceKit / row["file"]
        wide = "wide-" + row["file"]
        full = a.root / wide
        assert digest(small) == row["sha256"] and digest(full) == p["wideSha256"][wide]
        with fits.open(full, memmap=False) as whole, fits.open(small, memmap=False) as crop:
            w, = whole
            c, = crop
            keys = ("DATASEC", "DETPOS", "EXPTIME", "CCDNUM", "CCDSEC", "EXTNAME")
            assert all(w.header[key] == c.header[key] for key in keys)
            assert w.header["DETPOS"] == w.header["EXTNAME"]
            pos = w.header["DETPOS"]
            assert c.data.dtype == np.uint16
            x0, y0 = [round(w.header[key]-c.header[key]) for key in ("CRPIX1", "CRPIX2")]
            h, width = c.data.shape
            assert np.array_equal(w.data[y0:y0+h, x0:x0+width], c.data)
            wcs = WCS(c.header).celestial
            wc = WCS(w.header).celestial
            np.testing.assert_allclose(wcs.pixel_to_world_values([0,width-1],[0,h-1]),
                                       wc.pixel_to_world_values([x0,x0+width-1],[y0,y0+h-1]), atol=1e-10, rtol=0)
            ymin, xmin = np.indices(c.data.shape)
            x1, x2, y1, y2 = section(w.header["DATASEC"])
            inside = (x1 <= xmin+x0) & (xmin+x0 < x2) & (y1 <= ymin+y0) & (ymin+y0 < y2)
            identities.append({"source": row["source"], "detector": pos, "ccd": row["CCDNUM"],
                               "duration": row["exposureSeconds"], "arrayYX": list(w.data.shape),
                               "cropOriginXY": [x0,y0], "insideDataSection": int(inside.sum()),
                               "acceptedScienceDetector": pos == p["detectorRequired"]})
            if pos == p["controlFocusDetector"]:
                assert row["exposureSeconds"] == 30 and w.data.shape == (2098,2160)
                continue
            assert pos == p["detectorRequired"] and row["exposureSeconds"] == 180 and w.data.shape == (4146,2160)
            threshold = min(c.header["SATURATA"], c.header["SATURATB"])
            valid = inside & (c.data > 0) & (c.data < threshold)
            frames.append((c.data.copy(), valid, wcs))
    assert len(frames) == 2
    (ref, good, ref_w), (target, usable, target_w) = frames

    search = p["searchPx"]
    border = p["margin"]
    image = ref[border:-border, border:-border]
    maxima = np.ones(image.shape, dtype=bool)
    for vy in range(-p["peakStep"]//2+1, p["peakStep"]//2+1):
        for vx in range(-p["peakStep"]//2+1, p["peakStep"]//2+1):
            if vx or vy:
                maxima &= image >= ref[border+vy:ref.shape[0]-border+vy,
                                       border+vx:ref.shape[1]-border+vx]
    peaks = (np.argwhere(maxima)[:, ::-1] + border).tolist()
    peaks.sort(key=lambda xy: (-int(ref[xy[1],xy[0]]), xy[1], xy[0]))
    accepted, results = [], []
    seen = set()
    for x, y in peaks:
        if not good[y,x] or any((x-u)**2+(y-v)**2 < p["minCenterSeparationPx"]**2 for u,v in accepted):
            continue
        left = measure(np, ref, good, (x,y), p)
        if left is None:
            continue
        accepted.append((x,y))
        sky = ref_w.pixel_to_world_values(*left["xy"])
        guess = np.array(target_w.world_to_pixel_values(*sky))
        u,v = np.floor(guess+0.5).astype(int)
        cohort = "fit" if ((x//p["splitTilePx"])+(y//p["splitTilePx"]))%2==0 else "heldOut"
        row = {"reference": left, "cohort": cohort, "targetWcsXY": guess.tolist()}
        results.append(row)
        if min(u,v) < search or u+search >= target.shape[1] or v+search >= target.shape[0]:
            row["status"] = "OUTSIDE"
            continue
        box = target[v-search:v+search+1,u-search:u+search+1].astype(float)
        valid = usable[v-search:v+search+1,u-search:u+search+1]
        box[~valid] = -np.inf
        yy,xx = np.unravel_index(box.argmax(),box.shape)
        point = (u-search+int(xx),v-search+int(yy))
        if point in seen or not np.isfinite(box[yy,xx]):
            row["status"] = "NO_UNIQUE_PEAK"
            continue
        right = measure(np,target,usable,point,p)
        if right is None:
            row["status"] = "MEASUREMENT_REFUSED"
            continue
        seen.add(point)
        row.update(status="MATCH", target=right, offset=(np.array(right["xy"])-guess).tolist())

    train = [r for r in results if r["status"] == "MATCH" and r["cohort"] == "fit"]
    shift, fit, held = None, [], []
    if len(train) >= 3:
        shift = np.median([r["offset"] for r in train], axis=0)
        for r in results:
            if r["status"] == "MATCH":
                r["deltaAfterFitPx"] = float(np.linalg.norm(r["offset"]-shift))
        fit = [r for r in train if r["deltaAfterFitPx"] <= p["maxHoldoutOffsetPx"]]
        held = [r for r in results if r["status"] == "MATCH" and r["cohort"] == "heldOut"
                and r["deltaAfterFitPx"] <= p["maxHoldoutOffsetPx"]]
    status = ("DIAGNOSTIC_MEASURED" if len(held) >= 3 and len(fit) >= 3 else "INSUFFICIENT_MATCHES")

    def pair_ratios(matches):
        return np.array([np.array(r["target"]["flux"])/r["reference"]["flux"] for r in matches])

    controls = []
    if status == "DIAGNOSTIC_MEASURED":
        transfer = np.median(pair_ratios(fit), axis=0)
        ratios = pair_ratios(held)
        signed = ratios/transfer - 1
        absolute = np.abs(signed)
        controls = [{"radius": radius, "medianTargetToReferenceFit": float(transfer[i]),
                     "medianTargetToReferenceHeldOut": float(np.median(ratios[:,i])),
                     "heldOutMedianAbsoluteRelativeError": float(np.median(absolute[:,i])),
                     "heldOutP90AbsoluteRelativeError": float(np.quantile(absolute[:,i],.9)),
                     "heldOutWithinFivePercent": int(np.count_nonzero(absolute[:,i] <= .05))}
                    for i,radius in enumerate(p["aperturesPx"])]
    out = {"schema": "BKL046_M20_DECAM_R_REPEATABILITY_RESULT_V1", "protocolSha256": digest(proto),
           "programSha256": digest(Path(__file__)), "frames": identities,
           "candidates": results, "fitAccepted": len(fit), "heldOutAccepted": len(held),
           "fitOffsetXY": shift.tolist() if shift is not None else None, "status": status, "matchesBeforeFit": len(train),
           "heldOutOffsetMedianBeforePx": float(np.median([np.linalg.norm(r["offset"]) for r in held])) if held else None,
           "heldOutOffsetMedianAfterPx": float(np.median([r["deltaAfterFitPx"] for r in held])) if held else None,
           "apertures": controls, "shortScienceTransferVerified": False,
           "nativeExecutions": 0, "scientificClosures": 0}
    with a.report.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(out,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
