from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import runpy
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits


def verified(path, pin):
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != pin:
        raise ValueError(f"Input hash changed: {path.name}")
    return path


def pinned_json(path, pin):
    return json.loads(verified(path, pin).read_bytes())


def read_hdu(hdus, obs, is_flc, seconds, basis):
    p = hdus[0].header
    if (p["PCTECORR"] == "COMPLETE") != is_flc or p["ROOTNAME"] != obs or p["EXPTIME"] != seconds:
        raise ValueError("Unexpected product correction or identity")
    hdu = next(h for h in hdus if h.name == "SCI" and h.header["CCDCHIP"] == 1)
    h = hdu.header
    if h["BUNIT"] != "ELECTRONS":
        raise ValueError("Unexpected units")
    geom = [h["LTV1"], h["LTV2"], h["LTM1_1"], h["LTM2_2"], h["NAXIS1"], h["NAXIS2"]]
    if geom != basis:
        raise ValueError("Unmatched detector pixel coordinates")
    return {"sci": hdu.data, "dq": hdus["DQ", hdu.ver].data,
            "offset": [-int(h[key]) for key in ("LTV1", "LTV2")]}, {
        "obs": obs, "PCTECORR": p["PCTECORR"], "PCTETAB": p.get("PCTETAB"),
        "calVersion": p.get("CAL_VER"), "geom": geom,
    }


def main():
    working, original, sensitivity, common, protocol, out = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    prior = pinned_json(common/"riscontro.json", cfg["commonReport"])
    analysis = runpy.run_path(str(verified(common/"verifica.py", cfg["commonCode"])))
    sens = pinned_json(sensitivity/"protocollo.json", cfg["sensitivityProtocol"])
    guide = pinned_json(sensitivity/"riscontro.json", cfg["sensitivityReport"])
    base_a = pinned_json(original/"protocollo-jfdp02vfq.json", sens["primaryProtocol"])
    base_b = pinned_json(original/"protocollo-jfdp02vdq.json", sens["siblingProtocol"])
    legacy = runpy.run_path(str(verified(original/"verifica.py", sens["parentCode"])))
    prior_raw = pinned_json(original/"riscontro-jfdp02vfq.json", sens["primaryReport"])
    primary_center, = [row["centerXY"] for row in prior_raw["rows"] if row["status"] == "MEASURED"]
    centers = prior["centersXY"]
    flt_specs = [base_a["inputs"][0], base_b["inputs"][0], *base_a["inputs"][1:]]
    flc_pins = {item["file"]: item["sha256"] for item in cfg["flc"]}
    cap = max(row[-1] for row in cfg["skyAnnuli"])
    coords = np.arange(-cap, cap+1)
    distance = np.hypot(coords[:, None], coords)
    aperture = distance <= cfg["radiusPx"]
    pam = fits.getdata(verified(original/"wfc1_newpam.fits", base_a["pam"]["1"]))
    with ExitStack() as stack:
        flt, flc, attest = [], [], []
        for entry in flt_specs:
            obs = entry["file"].split("_", 1)[0]
            base = stack.enter_context(fits.open(verified(original/entry["file"], entry["sha256"]), memmap=False))
            new_name = obs+"_flc.fits"
            new = stack.enter_context(fits.open(verified(working/new_name, flc_pins[new_name]), memmap=False))
            plane = next(h.header for h in base if h.name == "SCI" and h.header["CCDCHIP"] == 1)
            geom = [plane[key] for key in ("LTV1","LTV2","LTM1_1","LTM2_2","NAXIS1","NAXIS2")]
            x, x_meta = read_hdu(base, obs, False, entry["exptime"], geom)
            y, y_meta = read_hdu(new, obs, True, entry["exptime"], geom)
            flt.append(x)
            flc.append(y)
            attest.append({"flt": x_meta, "flc": y_meta})
        targets = [
            analysis["component"](flt[0], legacy, base_a, primary_center),
            analysis["component"](flt[1], legacy, base_b, guide["replica"]["assessment"]["centerXY"]),
        ]
        pairs = [[legacy["stamp"](image, center, cap, pam) for image, center in zip(group, centers)]
                 for group in (flt, flc)]
        masks = []
        for group in pairs:
            if any(item is None for item in group):
                raise ValueError("Clipped stamp")
            good = [analysis["allowed"](group[i], cap, centers[i], targets[i]) for i in (0,1)]
            good.extend(analysis["allowed"](item, cap) for item in group[2:])
            masks.append(np.logical_and.reduce(good))
        first_support = aperture & masks[0]
        if int(first_support.sum()) != prior["sharedFourExposurePixels"]:
            raise ValueError("FLT reference support changed")
        support = first_support & masks[1]
        if support.sum() < 0.90*aperture.sum():
            raise ValueError("Insufficient common support for diagnostic")
        strict = np.logical_and.reduce([np.isin(item[1], [0,64]) for group in pairs for item in group])
        settings = []
        for inner, outer in cfg["skyAnnuli"]:
            sky = strict & (distance >= inner) & (distance <= outer)
            if sky.sum() < 400:
                raise ValueError("Insufficient shared sky")
            estimates = []
            for group in pairs:
                background = [float(np.median(signal[sky])) for signal, _ in group]
                estimates.append(analysis["estimate"](group, background, support))
            x, y = estimates
            shift = [100*(b/a-1) for a,b in zip(x["rates"],y["rates"])]
            settings.append({"skyPx": [inner,outer], "skyPixels": int(sky.sum()), "flt": x, "flc": y,
                             "rateChangeFLtoFLCPercent": shift,
                             "changePrimaryLongVsShortPercentagePoints":
                                 y["primaryVsShortMeanPercent"]-x["primaryVsShortMeanPercent"],
                             "changeReplicaLongVsShortPercentagePoints":
                                 y["replicaVsShortMeanPercent"]-x["replicaVsShortMeanPercent"]})
    payload = {"schema": cfg["schema"], "aperturePixels": int(aperture.sum()),
               "fltSharedPixels": int(first_support.sum()), "jointSharedPixels": int(support.sum()),
               "settings": settings, "provenance": attest, "scientificClosures": 0}
    with out.open("x", newline="\n", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
