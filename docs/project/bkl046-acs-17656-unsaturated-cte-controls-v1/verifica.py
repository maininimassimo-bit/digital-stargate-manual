from collections import Counter
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import runpy
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.wcs import WCS


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check(path, expected):
    if digest(path) != expected:
        raise ValueError(f"Input changed: {path.name}")
    return path


def json_pin(path, expected):
    return json.loads(check(path, expected).read_bytes())


def frame(path, exposure, flc, stack):
    h = stack.enter_context(fits.open(path, memmap=False))
    p = h[0].header
    if (p["PCTECORR"] == "COMPLETE") != flc or p["EXPTIME"] != exposure["exptime"]:
        raise ValueError("Unexpected product type")
    if p["ROOTNAME"] != exposure["file"].split("_")[0] or p["PROPOSID"] != 17656:
        raise ValueError("Unexpected product identity")
    sci = next(plane for plane in h if plane.name == "SCI" and plane.header["CCDCHIP"] == 1)
    if sci.header["BUNIT"] != "ELECTRONS":
        raise ValueError("Unexpected SCI units")
    wcs = WCS(sci.header, h)
    epoch = Time((p["EXPSTART"]+p["EXPEND"])/2, format="mjd", scale="utc").tcb.jyear
    offset = tuple(-int(sci.header[key]) for key in ("LTV1","LTV2"))
    return {"sci": sci.data, "dq": h["DQ", sci.ver].data,
            "wcs": wcs, "epoch": epoch, "offset": offset}


def at_square(item, center, cap, pam):
    x, y = (int(round(v)) for v in center)
    ox, oy = item["offset"]
    xs, ys = slice(x-cap,x+cap+1), slice(y-cap,y+cap+1)
    clipped = item["sci"][ys,xs]
    if clipped.shape != (2*cap+1,)*2:
        return None
    scale = pam[ys.start+oy:ys.stop+oy,xs.start+ox:xs.stop+ox]
    if scale.shape != clipped.shape:
        raise ValueError("Unsupported PAM geometry")
    signal = clipped.astype(float)*scale
    flags = item["dq"][ys,xs]
    return signal, flags


def rates(rows, aperture, sky, exposures, min_fraction, cfg):
    if any(row is None for row in rows):
        return "EDGE", None
    if any(np.any((dq[aperture] & (256 | 2048)) != 0) for _, dq in rows):
        return "SATURATION_DQ", None
    mask = np.logical_and.reduce([np.isin(dq, [0,64]) & np.isfinite(data) for data, dq in rows])
    usable = aperture & mask
    sky_support = sky & mask
    if usable.sum() < min_fraction*aperture.sum() or sky_support.sum() < cfg["minimumSkyPixels"]:
        return "SUPPORT", None
    values = [float((data[usable]-np.median(data[sky_support])).sum()/time)
              for (data, _), time in zip(rows, exposures)]
    if min(values) <= 0:
        return "NONPOSITIVE", None
    return "OK", (values, int(usable.sum()))


def stats(rows):
    out = {}
    for key in ("fltLongMinusShortPercent","flcLongMinusShortPercent","changePercentagePoints"):
        values = [row[key] for row in rows]
        out[key] = None if not values else {"median": float(np.median(values)),
          "min": min(values), "max": max(values), "p90Abs": float(np.quantile(np.abs(values),0.90))}
    return {"n": len(rows), **out}


def main():
    original, products, gaia, protocol, out, detail = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    gaia_cfg = json_pin(gaia/"protocollo-gaia.json", cfg["gaiaProtocol"])
    methods = runpy.run_path(str(check(gaia/"registra.py", cfg["gaiaCode"])))
    values, tiles, ids = methods["catalogue"](check(gaia/"gaia-dr3.csv", gaia_cfg["catalogSha256"]), gaia_cfg)
    cte_cfg = json_pin(products/"protocollo.json", cfg["cteProtocol"])
    cte_report = json_pin(products/"riscontro.json", cfg["cteReport"])
    central = next(row for row in cte_report["settings"] if row["skyPx"] == cfg["skyPx"])
    ref_rate = float(np.mean(central["flt"]["rates"][2:]))
    origin = json_pin(original/"protocollo-jfdp02vfq.json", cfg["originalProtocol"])
    sibling = json_pin(original/"protocollo-jfdp02vdq.json", cfg["siblingProtocol"])
    specs = [origin["inputs"][0], sibling["inputs"][0], *origin["inputs"][1:]]
    pam = fits.getdata(check(original/"wfc1_newpam.fits", origin["pam"]["1"]))
    flc_pins = {row["file"]: row["sha256"] for row in cte_cfg["flc"]}
    cap = cfg["skyPx"][1]
    yy, xx = np.mgrid[-cap:cap+1,-cap:cap+1]
    distance = np.hypot(xx,yy)
    aperture = distance <= cfg["radiusPx"]
    sky = (distance >= cfg["skyPx"][0]) & (distance <= cap)
    counts, measured, discarded = Counter(), [], []
    windows = {}
    with ExitStack() as stack:
        # Open and evaluate the short frames first so selection cannot use a long-frame measurement.
        for index in (2,3):
            entry = specs[index]
            windows[index] = frame(check(original/entry["file"],entry["sha256"]),entry,False,stack)
        def projections(im):
            world = methods["propagated"](values,im["epoch"])
            return im["wcs"].all_world2pix(world,0,quiet=True,ra_dec_order=True)
        predicted = {i:projections(windows[i]) for i in (2,3)}
        def pick(im, point):
            if not np.isfinite(point).all():
                return None
            _, center = methods["centroid"](im["sci"],im["dq"],point,gaia_cfg)
            return center
        selected = []
        for index, source in enumerate(ids):
            xy = [pick(windows[i],predicted[i][index]) for i in (2,3)]
            if any(center is None for center in xy):
                counts["SHORT_CENTROID"] += 1
                continue
            stamps = [at_square(windows[i], center, cap,pam) for i,center in zip((2,3),xy)]
            flag, estimate = rates(stamps,aperture,sky,[40,40],cfg["minimumShortSupportFraction"],cfg)
            if flag != "OK":
                counts["SHORT_"+flag] += 1
                continue
            vals,_ = estimate
            mean = sum(vals)/2
            relative = mean/ref_rate
            if not cfg["brightnessBins"][0][0] <= relative <= cfg["brightnessBins"][-1][1]:
                counts["SHORT_RATE_OUTSIDE_RANGE"] += 1
                continue
            if abs(vals[1]-vals[0])/mean*100 > cfg["maximumShortRepeatPercent"]:
                counts["SHORT_REPEAT"] += 1
                continue
            selected.append((index,source,xy,relative))
        counts["SHORT_SELECTED"] = len(selected)
        for index in (0,1):
            entry = specs[index]
            windows[index] = frame(check(original/entry["file"],entry["sha256"]),entry,False,stack)
            predicted[index] = projections(windows[index])
        corrected = {}
        for i,entry in enumerate(specs):
            name = entry["file"].replace("_flt","_flc")
            corrected[i] = frame(check(products/name,flc_pins[name]),entry,True,stack)
            if corrected[i]["offset"] != windows[i]["offset"] or corrected[i]["sci"].shape != windows[i]["sci"].shape:
                raise ValueError("FLT/FLC detector geometry mismatch")
        for index, source, short, relative in selected:
            hold = bool((2*tiles[index,0]+tiles[index,1]) % 4 == 0)
            long = [pick(windows[i],predicted[i][index]) for i in (0,1)]
            if any(center is None for center in long):
                counts["LONG_CENTROID"] += 1
                discarded.append({"source":source,"relativeRate":relative,"status":"LONG_CENTROID"})
                continue
            centers = [*long,*short]
            samples = [at_square(group[i],centers[i],cap,pam) for group in (windows,corrected) for i in range(4)]
            time = [150,150,40,40]*2
            outcome, measurement = rates(samples,aperture,sky,time,cfg["minimumSupportFraction"],cfg)
            counts[outcome] += 1
            if outcome != "OK":
                discarded.append({"source":source,"relativeRate":relative,"status":outcome})
                continue
            vals, count = measurement
            a = 100*((vals[0]+vals[1])/(vals[2]+vals[3])-1)
            b = 100*((vals[4]+vals[5])/(vals[6]+vals[7])-1)
            measured.append({"source":source,"relativeRate":relative,"holdout":hold,
                             "pixels":count,"meetsOriginalSupport":bool(count>=cfg["originalSupportFraction"]*aperture.sum()),
                             "fltLongMinusShortPercent":a,"flcLongMinusShortPercent":b,
                             "changePercentagePoints":b-a})
    summaries = []
    for left,right in cfg["brightnessBins"]:
        group = [row for row in measured if left <= row["relativeRate"] < right]
        summaries.append({"relativeShortRate":[left,right],"all":stats(group),
                         "holdout":stats([row for row in group if row["holdout"]])})
    report = {"schema":cfg["schema"],"protocolSha256":digest(protocol),"counts":dict(counts),
              "primaryTargetReferenceShortRate":ref_rate,"brightnessBins":summaries,
              "targetFLCMeanLongMinusShortPercent":float(np.mean(
                  [central["flc"][key] for key in ("primaryVsShortMeanPercent","replicaVsShortMeanPercent")])),
              "scientificClosures":0}
    for path,data in ((out,report),(detail,{"measured":measured,"rejected":discarded})):
        with path.open("x",newline="\n",encoding="utf-8") as stream:
            stream.write(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
