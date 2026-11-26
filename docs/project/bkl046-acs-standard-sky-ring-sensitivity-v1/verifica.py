"""Re-evaluate the pinned ACS outer-aperture range under alternate sky medians."""
from hashlib import sha256
import json
from pathlib import Path
from statistics import mean
import sys

import numpy as np

PIN = "56abfe8cc1191276c77a57ceea653d1610500f812a1e199eef9a1b7d7385bea9"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pinned(path, value):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == value, "Input digest changed")
    return raw


def pedestal(path, previous, baseline, plan, pam, fits):
    x, y = previous["peak"]
    cx, cy = previous["center"]
    with fits.open(path, memmap=False) as image:
        hdu = image["SCI",1]
        ox, oy = [-hdu.header[field] for field in ("LTV1","LTV2")]
        require((ox,oy) == (int(ox),int(oy)), "Noninteger PAM offsets")
        ox, oy = int(ox), int(oy)
        roi = np.s_[y-42:y+43,x-42:x+43]
        area = pam[oy+y-42:oy+y+43,ox+x-42:ox+x+43]
        signal = hdu.data[roi].astype(float)*area
        errors = image["ERR",1].data[roi].astype(float)*area
        dq = image["DQ",1].data[roi]
    require(area.shape == (85,85) and (area > 0).all() and np.isfinite(area).all(), "Broken PAM region")
    yy, xx = np.indices(signal.shape, dtype=float)
    xx, yy = xx+x-42-cx, yy+y-42-cy
    rr = xx*xx + yy*yy
    suitable = (dq == 0) & np.isfinite(signal) & np.isfinite(errors) & (errors >= 0.)
    a, b = baseline["backgroundRing"]
    ring = (rr >= a*a) & (rr <= b*b)
    quadrant = (xx < 0).astype(int) + 2*(yy < 0).astype(int)
    cases = {"original":ring}
    for lo, hi in plan["annuli"]:
        cases[f"annulus-{lo}-{hi}"] = (rr>=lo*lo)&(rr<=hi*hi)
    for q in plan["quadrantJackknife"]:
        cases[f"omit-quadrant-{q}"] = ring & (quadrant != q)
    medians = {}
    for name, support in cases.items():
        available = support & suitable
        require(support.any() and available.sum() >= plan["minimumSkySupport"] * support.sum(),
                f"Sky support fails for {name}")
        medians[name] = float(np.median(signal[available]))
    return medians


def translate(interval, delta, n, exposure):
    return [x - delta*n/exposure for x in interval]


def ratio(bands, plan):
    a, b = (bands[name] for name in plan["bands"])
    require(len(a)==len(b)==2 and all(x[0]>0 for x in a+b), "Missing positive band intervals")
    return [mean(x[0] for x in a)/mean(x[1] for x in b), mean(x[1] for x in a)/mean(x[0] for x in b)]


def main():
    protocol, parent, gd71inputs, gd153inputs, gd71old, gd153old, photometry, pam_path, deps, out = map(Path,sys.argv[1:])
    plan = json.loads(pinned(protocol,PIN))
    parent_plan = json.loads(pinned(parent/"protocollo.json",plan["parentProtocolSha256"]))
    parent_receipt = json.loads(pinned(parent/"riscontro.json",plan["parentResultSha256"]))
    raw = pinned(parent/"verifica.py",plan["parentRunnerSha256"])
    env = {"__name__":"verified_aperture_runner"}
    exec(compile(raw,"verified_aperture_runner.py","exec"),env)
    sys.path.insert(0,str(deps))
    from astropy.io import fits
    env["verify"](pam_path,parent_plan["pam"])
    pam = fits.getdata(pam_path)
    base = json.loads(pinned(photometry,parent_plan["apertureComparison"]))["targets"]
    require(translate([6.,8.],1.,4,2.) == [4.,6.], "Pedestal sign control failed")
    targets = {}
    for star, inp, old in (("GD71",gd71inputs,gd71old),("GD153",gd153inputs,gd153old)):
        rows = json.loads(pinned(old,parent_plan[star.lower()+"Growth"]))["rows"]
        manifest = json.loads(pinned(inp,parent_plan[star.lower()+"Inputs"]))["inputs"]
        sources = {row["obsId"]+"_flt.fits":row for row in manifest}
        root = inp.parent
        frozen = parent_receipt["targets"][star]["exposures"]
        archive = {label: [] for label in plan["bands"]}
        for row, check in zip(rows,frozen,strict=True):
            if row["band"] not in archive:
                continue
            file = root / row["file"]
            exact = env["evaluate"](file,row,sources[row["file"]],pam,fits,parent_plan)
            require(exact == check, "Pinned range differs from preceding measurement")
            medians = pedestal(file,row,parent_plan,plan,pam,fits)
            archive[row["band"]].append((row,check,medians))
        out_rows = {}
        for radius in plan["radii"]:
            key = str(radius)
            scenarios = next(iter(archive[plan["bands"][0]]))[2].keys()
            spread = {}
            for scenario in scenarios:
                per_band = {}
                for band, records in archive.items():
                    per_band[band] = [translate(estimate["radii"][key]["rateSensitivityRange"],
                                      medians[scenario]-medians["original"],
                                      row["apertures"][key]["required"],row["exp"])
                                      for row,estimate,medians in records]
                spread[scenario] = per_band
            fixed = {case:ratio(bands,plan) for case,bands in spread.items()}
            require(fixed["original"] == parent_receipt["targets"][star]["radii"][key]["ratioRange"],
                    "Baseline ratio does not match")
            extreme = {}
            for band in plan["bands"]:
                choices = zip(*(result[band] for result in spread.values()),strict=True)
                extreme[band] = [[min(pair[0] for pair in options),max(pair[1] for pair in options)]
                                 for options in choices]
            bounds = ratio(extreme,plan)
            gaia = base[star]["gaiaRatio"]
            out_rows[key] = dict(sharedSkyScenarios=fixed, independentSkyChoiceEnvelope=bounds,
                                 additionalRatioIncreaseFromUpperEdge=gaia/bounds[1]-1,
                                 gaiaWithinTestedEnvelope=bounds[0]<=gaia<=bounds[1])
        deltas = [abs(value-m["original"]) for samples in archive.values() for _,_,m in samples
                  for value in m.values()]
        targets[star] = dict(radii=out_rows, maxSkyMedianShiftElectronPerAreaCorrectedPixel=max(deltas))
    report = dict(schema="BKL046_ACS_SKY_RING_SENSITIVITY_RESULT_V1", protocolSha256=PIN,
                  targets=targets, originalDqStatesPreserved=True, uncertaintyCalibrated=False,
                  scientificClosures=0, nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
