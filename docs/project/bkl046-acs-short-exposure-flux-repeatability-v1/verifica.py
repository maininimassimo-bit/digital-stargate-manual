from collections import Counter
from pathlib import Path
import json
import runpy
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.wcs import WCS


def weights(x, y, centroid, radius, n):
    phase = (np.arange(n)+0.5)/n-0.5
    dx = x[:, :, None, None]-centroid[0]+phase[:, None]
    dy = y[:, :, None, None]-centroid[1]+phase[None, :]
    return (dx*dx+dy*dy <= radius*radius).mean(axis=(2, 3))


def aperture(image, dq, err, pam, center, radius, cfg):
    width = cfg["skyAnnulus"][1]+1
    x, y = (int(round(v)) for v in center)
    ys, xs = slice(y-width, y+width+1), slice(x-width, x+width+1)
    science, dq, err, pam = [plane[ys, xs] for plane in (image, dq, err, pam)]
    if science.shape != (2*width+1,)*2:
        return "EDGE", None
    yy, xx = np.mgrid[y-width:y+width+1, x-width:x+width+1]
    dist = np.hypot(xx-center[0], yy-center[1])
    ap = weights(xx, yy, center, radius, cfg["oversampling"])
    selected = ap > 0
    usable = np.isin(dq, cfg["allowedDQ"]) & np.isfinite(science) & np.isfinite(pam)
    if not usable[selected].all() or not np.isfinite(err[selected]).all():
        return "APERTURE_DQ", None
    sky = usable & (dist >= cfg["skyAnnulus"][0]) & (dist <= cfg["skyAnnulus"][1])
    if sky.sum() < cfg["minimumSkyPixels"]:
        return "SKY_COVERAGE", None
    corrected = science.astype(float)*pam
    background = float(np.median(corrected[sky]))
    flux = float(np.sum(ap[selected]*(corrected[selected]-background)))
    if flux <= 0:
        return "NONPOSITIVE_FLUX", None
    err_e = float(np.sqrt(np.square(ap[selected]*err[selected]*pam[selected]).sum()))
    return "OK", {"rate": flux/40, "nominalErrRate": err_e/40, "sky": background}


def inspect_image(path, entry, pams, values, ids, tiles, cfg, gcfg, method):
    with fits.open(path, memmap=False) as f:
        p = f[0].header
        if p["ROOTNAME"].lower() != entry["id"] or p["PROPOSID"] != entry["program"] or p["EXPTIME"] != 40:
            raise ValueError("Wrong exposure")
        epoch = Time((p["EXPSTART"]+p["EXPEND"])/2, format="mjd", scale="utc").tcb.jyear
        world = method["propagated"](values, epoch)
        records = {}
        for plane in (hdu for hdu in f if hdu.name == "SCI"):
            h = plane.header
            dq = f["DQ", plane.ver].data
            err = f["ERR", plane.ver].data
            chip = h["CCDCHIP"]
            if h["BUNIT"] != "ELECTRONS":
                raise ValueError("Wrong units")
            ox, oy = (-int(h[key]) for key in ("LTV1", "LTV2"))
            height, width = plane.data.shape
            pam = pams[chip][oy:oy+height, ox:ox+width]
            if pam.shape != plane.data.shape:
                raise ValueError("PAM geometry mismatch")
            centers = WCS(h, f).all_world2pix(world, 0, quiet=True, ra_dec_order=True)
            for index, location in enumerate(centers):
                if not np.isfinite(location).all():
                    continue
                outcome, center = method["centroid"](plane.data, dq, location, gcfg)
                if outcome != "MATCH":
                    continue
                tile = tiles[index]
                records[(ids[index], chip)] = {"holdout": (2*tile[0]+tile[1]) % 4 == 0,
                    "centerXY": center.tolist(),
                    "measurements": {radius: aperture(plane.data, dq, err, pam, center, radius, cfg)
                                     for radius in cfg["radii"]}}
        return records


def magnitude_stats(values):
    if not values:
        return None
    return {"n": len(values), "medianPercent": float(np.median(values)),
            "p90AbsolutePercent": float(np.quantile(abs(np.asarray(values)), 0.9)),
            "maxAbsolutePercent": float(np.max(abs(np.asarray(values))))}


def main():
    base, provenance, protocol, output, detail = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    import hashlib
    def verified(path, expected):
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != expected:
            raise ValueError(f"Changed input: {path.name}")
        return path
    method = runpy.run_path(str(verified(provenance/"registra.py", cfg["gaiaCode"])))
    gcfg = json.loads(verified(provenance/"protocollo-gaia.json", cfg["gaiaProtocol"]).read_bytes())
    values, tiles, ids = method["catalogue"](verified(provenance/"gaia-dr3.csv", gcfg["catalogSha256"]), gcfg)
    pams = {int(chip): fits.getdata(verified(base/f"wfc{chip}_newpam.fits", digest))
            for chip, digest in cfg["pam"].items()}
    images = []
    for item in gcfg["inputs"]:
        path = verified(provenance/(item["id"]+"_flt.fits"), item["sha256"])
        images.append(inspect_image(path, item, pams, values, ids, tiles, cfg, gcfg, method))
    common_ids = sorted(set.intersection(*(set(image) for image in images)))
    rows, counts, cuts = [], Counter(), []
    for source, chip in common_ids:
        source_rows = [image[source, chip] for image in images]
        holdout = bool(source_rows[0]["holdout"])
        for radius in cfg["radii"]:
            attempts = [row["measurements"][radius] for row in source_rows]
            status = [code for code, measurement in attempts]
            if status != ["OK", "OK", "OK"]:
                counts[str(radius)] += 1
                cuts.append({"id": source, "chip": chip, "radius": radius, "statuses": status})
                continue
            rate = [measurement["rate"] for _, measurement in attempts]
            a, b, c = rate
            rows.append({"id": source, "chip": chip, "radius": radius, "holdout": holdout,
                         "rates": rate, "withinVisitPercent": 200*(b-a)/(a+b),
                         "acrossVisitsPercent": 100*(2*c/(a+b)-1)})
    summary = {}
    for radius in cfg["radii"]:
        summary[str(radius)] = {}
        for chip in (1, 2):
            population = [row for row in rows if row["radius"] == radius and row["chip"] == chip]
            split = {}
            for label, group in (("all", population), ("heldOut", [row for row in population if row["holdout"]])):
                split[label] = {
                    "withinVisit": magnitude_stats([row["withinVisitPercent"] for row in group]),
                    "acrossVisits": magnitude_stats([row["acrossVisitsPercent"] for row in group]),
                    "withinTwoPercentBoth": sum(
                        abs(row["withinVisitPercent"]) <= cfg["referenceRepeatThresholdPercent"]
                        and abs(row["acrossVisitsPercent"]) <= cfg["referenceRepeatThresholdPercent"]
                        for row in group),
                    "n": len(group),
                }
            summary[str(radius)][str(chip)] = split
    report = {"schema": cfg["schema"], "protocolSha256": hashlib.sha256(protocol.read_bytes()).hexdigest(),
              "commonSources": len(common_ids), "rejectedByRadius": dict(counts),
              "summary": summary, "saturatedPhotometryPerformed": False, "scientificClosures": 0}
    for path, payload in ((output, report), (detail, {"accepted": rows, "rejected": cuts})):
        with path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
