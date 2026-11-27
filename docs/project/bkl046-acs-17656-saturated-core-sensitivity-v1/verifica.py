from collections import Counter
from contextlib import ExitStack
from itertools import product
from pathlib import Path
import hashlib
import json
import runpy
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def checked(path, expected):
    if digest(path) != expected:
        raise ValueError(f"Input changed: {path.name}")
    return path


def positions(ops, long, short, component, cfg):
    xs, ys, flags = component
    med = [np.median(xs), np.median(ys)]
    world = long["wcs"].all_pix2world([med], 0, ra_dec_order=True)[0]
    ref = [ops["find_reference"](im, world, cfg) for im in short]
    if None in ref:
        raise ValueError("Short references no longer match")
    sw = [im["wcs"].all_pix2world([xy], 0, ra_dec_order=True)[0] for im, xy in zip(short, ref)]
    computed = np.array([ops["coordinate"](long, s) for s in sw])
    pixel = tuple(int(round(v)) for v in computed.mean(axis=0))
    return pixel, ref, sw


def values(rows, info, radius, bounds, displacement, cfg, pam, ops):
    long, *short = rows
    component, primary, ref = info
    shifted = tuple(v+d for v, d in zip(primary, displacement))
    cap = bounds[-1]
    yy, xx = np.mgrid[-cap:cap+1, -cap:cap+1]
    rr = np.hypot(yy, xx)
    ring = (rr >= bounds[0]) & (rr <= bounds[1])
    shape = rr <= radius
    st = [ops["stamp"](image, center, cap, pam) for image, center in zip(rows, [shifted, *ref])]
    if any(x is None for x in st):
        return {"status": "EDGE"}
    good = np.logical_and.reduce([np.isin(dq, [0, 64]) for _, dq in st])
    x, y = shifted
    xs, ys, flags = component
    sat = np.zeros_like(shape)
    sat[ys-y+cap, xs-x+cap] = True
    all_sat_used = bool(shape[sat].all())
    admitted = np.isin(st[0][1], [0, 64]) | (sat & np.isin(st[0][1], [256, 320]))
    admitted &= np.isin(st[1][1], [0, 64]) & np.isin(st[2][1], [0, 64])
    accepted = shape & admitted
    sky = ring & good
    if not all_sat_used or accepted.sum() < cfg["minimumApertureCoverage"]*shape.sum() or sky.sum() < cfg["minimumSkyPixels"]:
        return {"status": "SUPPORT", "allFullWellPixelsIncluded": all_sat_used,
                "excludedAperturePixels": int((shape & ~admitted).sum()), "skyPixels": int(sky.sum())}
    rates = [float((signal[accepted]-np.median(signal[sky])).sum())/seconds
             for (signal, quality), seconds in zip(st, (150, 40, 40))]
    a, b, c = rates
    if min(rates) <= 0:
        return {"status": "NONPOSITIVE_FLUX"}
    return {"status": "MEASURED", "rates": rates, "skyPixels": int(sky.sum()),
            "circlePixels": int(accepted.sum()), "longMinusShortPercent": 100*(2*a/(b+c)-1),
            "shortDisagreementPercent": 200*abs(c-b)/(b+c)}


def replica_support(images, centers, selected, pam, cfg, ops):
    cap = cfg["skyPx"][1]
    sample = [ops["stamp"](image, p, cap, pam) for image, p in zip(images, centers)]
    if any(row is None for row in sample):
        return {"status": "EDGE"}
    x, y = centers[0]
    xs, ys, _ = selected
    flag = np.zeros((2*cap+1,)*2, dtype=bool)
    for offset in range(-cfg["paddingPx"], cfg["paddingPx"]+1):
        flag[ys-y+cap+offset, xs-x+cap] = True
    coord = np.arange(-cap, cap+1)
    circle = np.hypot(coord[:, None], coord) <= cfg["radiiPx"][0]
    shape = circle | flag
    flags = [entry[1] for entry in sample]
    permits = [np.isin(dq, [0, 64]) for dq in flags]
    permits[0] |= flag & np.isin(flags[0], [256, 320])
    common = np.logical_and.reduce(permits)
    return {"shapePixels": int(shape.sum()), "commonPixels": int((common & shape).sum()),
            "trailExcludedPixels": int((flag & ~common).sum()),
            "excludedCountsByExposure": [
                {str(key): value for key, value in Counter(dq[shape & ~good].astype(int).tolist()).items()}
                for dq, good in zip(flags, permits)]}


def main():
    root, protocol, result = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    prefix = "jfdp02vfq"
    suffix = "jfdp02vdq"
    ops = runpy.run_path(str(checked(root/"verifica.py", cfg["parentCode"])))
    original = json.loads(checked(root/f"protocollo-{prefix}.json", cfg["primaryProtocol"]).read_bytes())
    sibling = json.loads(checked(root/f"protocollo-{suffix}.json", cfg["siblingProtocol"]).read_bytes())
    prior = json.loads(checked(root/f"riscontro-{prefix}.json", cfg["primaryReport"]).read_bytes())
    eligible = [row for row in prior["rows"] if row["status"] == "MEASURED"]
    if len(eligible) != 1 or eligible[0]["chip"] != 1:
        raise ValueError("Unexpected diagnostic subjects")
    center = eligible[0]["centerXY"]
    with ExitStack() as stack:
        def read(row):
            return ops["read_frame"](ops["open_input"](root/row["file"], row["sha256"], stack), row)[1]
        long, *short = [read(row) for row in original["inputs"]]
        another = read(sibling["inputs"][0])
        ref_path = checked(root/"wfc1_newpam.fits", original["pam"]["1"])
        pam = fits.getdata(ref_path)
        selected = [c for c in ops["connected_long"](long, original) if
                    [np.median(c[0]), np.median(c[1])] == center]
        if len(selected) != 1:
            raise ValueError("Long component ambiguous")
        primary, references, sky_centers = positions(ops, long, short, selected[0], original)
        sibling_xy = np.array([ops["coordinate"](another, world) for world in sky_centers]).mean(axis=0)
        matches = [item for item in ops["connected_long"](another, sibling)
                   if np.hypot(item[0]-sibling_xy[0], item[1]-sibling_xy[1]).min()
                   <= cfg["maximumSiblingPeakDistancePx"]]
        replica = {"predictedXY": sibling_xy.tolist(), "componentsWithinTolerance": len(matches)}
        if len(matches) == 1:
            replica["assessment"] = ops["assess"]([another, *short], pam, matches[0], sibling, 1, [150,40,40])
            alternate, alternate_refs, _ = positions(ops, another, short, matches[0], sibling)
            replica["apertureSupport"] = replica_support([another, *short], [alternate, *alternate_refs],
                                                          matches[0], pam, sibling, ops)
        settings = []
        for r, sky, dx, dy in product(cfg["radii"], cfg["skyAnnuli"], cfg["centerPerturbationsPx"],
                                     cfg["centerPerturbationsPx"]):
            details = values([long, *short], (selected[0], primary, references), r, sky, (dx,dy), cfg, pam, ops)
            settings.append({"radiusPx": r, "skyPx": sky, "longShiftXY": [dx,dy], **details})
    payload = {"schema": cfg["schema"], "protocolSha256": digest(protocol), "primaryCenterXY": primary,
               "shortCentersXY": references, "settings": settings, "replica": replica,
               "counts": dict(Counter(row["status"] for row in settings)), "scientificClosures": 0}
    with result.open("x", newline="\n", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
