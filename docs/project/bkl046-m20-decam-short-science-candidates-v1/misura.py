"""Bind independent science-chip short exposures and test transfer without resampling."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import runpy
import sys
from urllib.parse import parse_qs, urlsplit
from xml.etree import ElementTree


def sha(path):
    with path.open("rb") as file:
        return file_digest(file, "sha256").hexdigest()


def in_section(np, x, y, bounds):
    x0, x1, y0, y1 = bounds
    return (x >= x0) & (x < x1) & (y >= y0) & (y < y1)


def quantify(np, measure, left, right, p):
    _, a, av, aw = left
    _, b, bv, bw = right
    margin, search = p["margin"], p["searchPx"]
    view = a[margin:-margin, margin:-margin]
    maxmask = np.ones(view.shape, dtype=bool)
    for y in range(-2,3):
        for x in range(-2,3):
            if x or y:
                maxmask &= view >= a[margin+y:a.shape[0]-margin+y,margin+x:a.shape[1]-margin+x]
    peaks = (np.argwhere(maxmask)[:, ::-1]+margin).tolist()
    peaks.sort(key=lambda xy: (-int(a[xy[1],xy[0]]),xy[1],xy[0]))
    candidates, used, results = [], set(), []
    for x,y in peaks:
        if any((x-u)**2+(y-v)**2 < p["minCenterSeparationPx"]**2 for u,v in candidates) or not av[y,x]:
            continue
        origin = measure(np,a,av,(x,y),p)
        if not origin:
            continue
        candidates.append((x,y))
        cohort = "fit" if ((x//p["splitTilePx"])+(y//p["splitTilePx"]))%2==0 else "heldOut"
        wcs_xy = np.array(bw.world_to_pixel_values(*aw.pixel_to_world_values(*origin["xy"])))
        u,v = np.floor(wcs_xy+0.5).astype(int)
        row = {"cohort":cohort,"origin":origin,"targetHeaderXY":wcs_xy.tolist()}
        results.append(row)
        if min(u,v) < search or u+search >= b.shape[1] or v+search >= b.shape[0]:
            row["status"] = "OUTSIDE"
            continue
        area = np.s_[v-search:v+search+1,u-search:u+search+1]
        box = np.where(bv[area], b[area], -np.inf)
        j,i = np.unravel_index(box.argmax(),box.shape)
        point = (u-search+int(i),v-search+int(j))
        if point in used or not np.isfinite(box[j,i]):
            row["status"] = "NO_UNIQUE_PEAK"
            continue
        match = measure(np,b,bv,point,p)
        if not match:
            row["status"] = "MEASUREMENT_REFUSED"
            continue
        used.add(point)
        row.update(status="MATCH", matched=match, offset=(np.array(match["xy"])-wcs_xy).tolist())
    fit = [r for r in results if r["status"] == "MATCH" and r["cohort"] == "fit"]
    affected, held, usable = None, [], []
    if len(fit) >= 3:
        affected = np.median([r["offset"] for r in fit],axis=0)
        for r in results:
            if r["status"] == "MATCH":
                r["residualPx"] = float(np.linalg.norm(r["offset"]-affected))
                if r["residualPx"] <= p["maxHoldoutOffsetPx"]:
                    (held if r["cohort"] == "heldOut" else usable).append(r)
    photometry = []
    status = "INSUFFICIENT_MATCHES"
    if min(len(usable),len(held)) >= 3:
        status = "DIAGNOSTIC_MEASURED"
        for i, radius in enumerate(p["aperturesPx"]):
            def ratios(group):
                return np.array([r["matched"]["flux"][i]/r["origin"]["flux"][i] for r in group])
            scale = np.median(ratios(usable))
            test = np.abs(ratios(held)/scale-1)
            photometry.append({"radiusPx":radius,"measuredScaleFit":float(scale),
                               "scalePerExposureTimeRatio":float(scale*left[0]["seconds"]/right[0]["seconds"]),
                               "heldOutMedianAbsoluteError":float(np.median(test)),
                               "heldOutP90AbsoluteError":float(np.quantile(test,.9))})
    return {"from":left[0]["image"],"to":right[0]["image"],"status":status,
            "fitInitialMatches":len(fit),"fitAccepted":len(usable),"heldOutAccepted":len(held),
            "fitOffsetXY":affected.tolist() if affected is not None else None,
            "photometry":photometry,"candidates":results}


def main():
    parser = argparse.ArgumentParser()
    for name in ("root","reference","repeatabilityKit","dependencies","report"):
        parser.add_argument(name,type=Path)
    a = parser.parse_args()
    proto = a.root/"protocollo.json"
    p = json.loads(proto.read_bytes())
    base = a.repeatabilityKit/"misura.py"
    assert sha(base) == p["repeatabilityProgram"]
    helpers = runpy.run_path(str(base))
    source_catalog = a.reference/"M20-votable.xml"
    assert sha(source_catalog) == p["catalogSha256"]
    cat = ElementTree.parse(source_catalog).find(".//{*}TABLE")
    cols = [child.get("name") for child in cat.findall("{*}FIELD")]
    catalog = {}
    for row in cat.findall(".//{*}TR"):
        item = dict(zip(cols,[node.text for node in row],strict=True))
        parsed = parse_qs(urlsplit(item["access_url"]).query)
        catalog[parsed["siaRef"][0]] = item
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    assert (np.__version__, astropy.__version__) == ("2.3.5","7.2.0")
    frames = {}
    for item in p["inputs"]:
        row = catalog[item["image"]]
        where = {"new":a.root,"original":a.reference,"prior":a.repeatabilityKit}
        crop,full = [where[item[k+"Root"]]/item[k] for k in ("crop","full")]
        assert sha(crop) == item["cropSha256"] and sha(full) == item["fullSha256"]
        with fits.open(crop,memmap=False) as aa, fits.open(full,memmap=False) as bb:
            h, = aa
            wide, = bb
            assert h.data.dtype == np.uint16 and wide.data.shape == (4146,2160)
            assert h.header["DETPOS"] == wide.header["DETPOS"]
            assert h.header["DETPOS"][0] in "NS"
            assert h.header["DATE-OBS"] == row["date_obs"] and h.header["EXPTIME"] == float(row["exptime"])
            assert h.header["FILTER"].startswith("r DECam") and row["obs_bandpass"] == "r"
            x0,y0 = [round(wide.header[k]-h.header[k]) for k in ("CRPIX1","CRPIX2")]
            ymax,xmax = h.data.shape
            assert np.array_equal(h.data,wide.data[y0:y0+ymax,x0:x0+xmax])
            owcs, fwcs = WCS(h.header).celestial,WCS(wide.header).celestial
            np.testing.assert_allclose(owcs.pixel_to_world_values([0,xmax-1],[0,ymax-1]),
                                        fwcs.pixel_to_world_values([x0,x0+xmax-1],[y0,y0+ymax-1]),rtol=0,atol=1e-10)
            yi,xi = np.indices(h.data.shape)
            science = in_section(np,xi+x0,yi+y0,helpers["section"](wide.header["DATASEC"]))
            amp = [in_section(np,xi+x0,yi+y0,helpers["section"](wide.header["DATASEC"+k])) for k in "AB"]
            assert not (amp[0]&amp[1]).any() and np.array_equal(amp[0]|amp[1],science)
            over = ((amp[0] & (h.data >= wide.header["SATURATA"])) |
                    (amp[1] & (h.data >= wide.header["SATURATB"])))
            mx,my = owcs.world_to_pixel_values(p["targetRa"],p["targetDec"])
            center = (0 <= mx < xmax and 0 <= my < ymax and in_section(np,mx+x0,my+y0,helpers["section"](wide.header["DATASEC"])))
            meta = {"image":item["image"],"detector":h.header["DETPOS"],"ccd":int(h.header["CCDNUM"]),
                    "program":row["project_code"],"timestamp":row["date_obs"],"seconds":float(row["exptime"]),
                    "airmass":float(row["airmass"]),"insideDataSection":int(science.sum()),
                    "atOrAboveAmplifierLevel":int(over.sum()),"skyCenterInScienceCrop":bool(center)}
            frames[item["image"]] = (meta,h.data.copy(),science & ~over & (h.data > 0),owcs)
    results = [quantify(np,helpers["measure"],frames[x],frames[y],p["photometry"]) for x,y in p["pairs"]]
    doc = {"schema":"BKL046_M20_SHORT_SCIENCE_TRANSFER_RESULT_V1","programSha256":sha(Path(__file__)),
           "protocolSha256":sha(proto),"frames":[row[0] for row in frames.values()],"comparisons":results,
           "sameNightDifferentDurationQualified":False,"fluxRecoveryVerified":False,
           "nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as file:
        json.dump(doc,file,indent=2,sort_keys=True,allow_nan=False)
        file.write("\n")


if __name__ == "__main__":
    main()
