"""Evaluate outer-aperture DQ support without modifying the archived photometry."""
from collections import Counter
from hashlib import file_digest, sha256
import json
from pathlib import Path
from statistics import mean
import sys

import numpy as np

PIN = "3830ff3101c8a039d40d4f39f564ad1d38959abf0611969d7d71c00c00aa737c"


def require(ok, label):
    if not ok:
        raise ValueError(label)


def load(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected, "Manifest digest differs")
    return json.loads(raw)


def verify(path, expected):
    with path.open("rb") as file:
        require(file_digest(file, "sha256").hexdigest() == expected, "FITS digest differs")


def bracket(values, radius, support, missing, plan):
    low = high = 0.
    for pos in missing:
        pool = values[support & (abs(radius - radius[pos]) <= plan["radialPeerHalfWidthPx"])]
        if len(pool) < plan["minimumPeerCount"]:
            return None
        low += float(pool.min())
        high += float(pool.max())
    return low, high


def control_positions(x, y, radius, available, missing, turn, plan):
    chosen = []
    for pos in missing:
        tx, ty = x[pos], y[pos]
        for _ in range(turn):
            tx, ty = -ty, tx
        candidates = np.flatnonzero(available & (abs(radius - radius[pos]) <= plan["radialPeerHalfWidthPx"]))
        candidates = [i for i in candidates if i not in chosen]
        if not candidates:
            return []
        closest = min(candidates, key=lambda i: (x[i]-tx)**2 + (y[i]-ty)**2)
        if (x[closest]-tx)**2 + (y[closest]-ty)**2 > 2.25:
            return []
        chosen.append(closest)
    return chosen


def evaluate(path, original, entry, pam, fits, plan):
    require(path.stat().st_size == entry["bytes"], "FITS size differs")
    verify(path, entry["sha256"])
    with fits.open(path, memmap=False) as hdus:
        h = hdus[0].header
        image = hdus["SCI",1]
        header = image.header
        band = h["FILTER1"] if h["FILTER2"].startswith("CLEAR") else h["FILTER2"]
        require(band == original["band"] == entry["band"] and h["CCDAMP"] == "B"
                and h["PROPOSID"] == 10054 and header["CCDCHIP"] == 1
                and h["EXPSTART"] == original["startMjd"] and h["EXPTIME"] == original["exp"],
                "ACS exposure lineage differs")
        x, y = original["peak"]
        cx, cy = original["center"]
        ox, oy = [-header[key] for key in ("LTV1","LTV2")]
        require((ox,oy) == (int(ox),int(oy)) and min(ox,oy) >= 0, "PAM offsets changed")
        ox, oy = int(ox), int(oy)
        roi = np.s_[y-42:y+43,x-42:x+43]
        area = pam[oy+y-42:oy+y+43,ox+x-42:ox+x+43]
        sample = (image.data[roi].astype(float)*area).ravel()
        error = (hdus["ERR",1].data[roi].astype(float)*area).ravel()
        flags = hdus["DQ",1].data[roi].ravel()
    require(area.shape == (85,85) and np.all(np.isfinite(area)&(area>0)), "PAM support changed")
    yy, xx = np.indices((85,85), dtype=float)
    xx, yy = (xx + x - 42 - cx).ravel(), (yy + y - 42 - cy).ravel()
    rr = xx**2+yy**2
    radial = np.sqrt(rr)
    good = np.isin(flags,plan["acceptedDq"]) & np.isfinite(sample) & np.isfinite(error) & (error>=0.)
    a,b = plan["backgroundRing"]
    sky = (rr >= a*a) & (rr <= b*b)
    real_sky = sky & good & (flags == 0)
    require(real_sky.sum() >= 0.7*sky.sum(), "Background support changed")
    values = sample - np.median(sample[real_sky])
    reports = {}
    for radius in plan["radii"]:
        key = str(radius)
        inside = rr <= radius**2
        keep = inside & good
        missing = np.flatnonzero(inside & ~good)
        expected = original["apertures"][key]
        require((int(keep.sum()),int(inside.sum())) == (expected["good"],expected["required"]),
                "Aperture support differs from archived reduction")
        summed = float(np.sum(values[keep]))
        report = dict(originalState=expected["state"], missingPixels=len(missing),
                      missingFlags={str(key):val for key,val in sorted(Counter(map(int,flags[missing])).items())})
        if expected["state"] == "MEASURED":
            require(len(missing)==0 and np.isclose(summed/h["EXPTIME"],expected["rate"],rtol=1e-11,atol=0),
                    "Archived aperture rate differs")
            diagnostic = (0.,0.)
        else:
            diagnostic = (bracket(values,radial,keep,missing,plan)
                          if len(missing) <= plan["maximumMissingFraction"]*inside.sum() else None)
        pseudo = []
        if len(missing) and diagnostic is not None:
            for turn in plan["pseudoMaskQuarterTurns"]:
                controls = control_positions(xx,yy,radial,keep,missing,turn,plan)
                if not controls:
                    continue
                remain = keep.copy()
                remain[controls] = False
                test = bracket(values,radial,remain,controls,plan)
                if test is not None:
                    truth = float(np.sum(values[controls]))
                    pseudo.append(test[0] <= truth <= test[1])
        report.update(peerTests=len(pseudo),peerTestsPassed=sum(pseudo))
        if diagnostic is not None:
            lo, hi = (summed+v for v in diagnostic)
            if lo>0:
                report["rateSensitivityRange"] = [lo/h["EXPTIME"], hi/h["EXPTIME"]]
        reports[key] = report
    return dict(band=band,radii=reports)


def summarize(exposures, plan, gaia):
    rows = {}
    for radius in plan["radii"]:
        key = str(radius)
        bands = {}
        for band in ("F658N","F660N"):
            cases = [x["radii"][key] for x in exposures if x["band"] == band]
            usable = [x["rateSensitivityRange"] for x in cases if "rateSensitivityRange" in x]
            require(len(cases)==2, "Band roster changed")
            if len(usable)==len(cases):
                bands[band] = [mean(x[i] for x in usable) for i in (0,1)]
        if len(bands) != 2:
            rows[key] = {"status":"INCOMPLETE_DIAGNOSTIC"}
            continue
        lo, hi = bands["F658N"]
        a, b = bands["F660N"]
        lower, upper = lo/b, hi/a
        peer = [x["radii"][key] for x in exposures if x["band"] in bands]
        rows[key] = dict(status="EMPIRICAL_RANGE", ratioRange=[lower,upper],
                         observedGapToGaiaFromRangeUpper=gaia/upper-1,
                         gaiaOverlapsRange=lower<=gaia<=upper,
                         peerTests=sum(x["peerTests"] for x in peer),
                         peerTestsPassed=sum(x["peerTestsPassed"] for x in peer))
    return rows


def main():
    spec, inputs71, inputs153, old71, old153, prior, pam_path, dependencies, out = map(Path,sys.argv[1:])
    plan = load(spec,PIN)
    sys.path.insert(0,str(dependencies))
    from astropy.io import fits
    verify(pam_path,plan["pam"])
    pam = fits.getdata(pam_path)
    control = np.array([1.,3.,2.])
    require(bracket(control, np.ones(3), np.array([True,True,False]), [2],
                    dict(radialPeerHalfWidthPx=1,minimumPeerCount=2)) == (1.,3.),
            "Peer range control failed")
    baseline = load(prior,plan["apertureComparison"])["targets"]
    reports = {}
    for star, inp, existing in (("GD71",inputs71,old71),("GD153",inputs153,old153)):
        manifest = load(inp,plan[star.lower()+"Inputs"])["inputs"]
        orig = load(existing,plan[star.lower()+"Growth"])["rows"]
        records = {row["obsId"]+"_flt.fits":row for row in manifest}
        require(len(records)==len(orig)==6 and set(records)=={item["file"] for item in orig},
                "Exposure set differs")
        exposures = [evaluate(inp.parent/row["file"],row,records[row["file"]],pam,fits,plan) for row in orig]
        reports[star] = dict(exposures=exposures, radii=summarize(exposures, plan, baseline[star]["gaiaRatio"]))
    report = dict(schema="BKL046_ACS_STANDARD_OUTER_APERTURE_DIAGNOSTIC_V1",
                  protocolSha256=PIN, verifiedExposures=12,
                  originalExcludedStatesPreserved=True, calibratedUncertaintyProvided=False,
                  extrapolatedInfiniteAperture=False, scientificClosures=0,nativeExecutions=0,
                  targets=reports)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
