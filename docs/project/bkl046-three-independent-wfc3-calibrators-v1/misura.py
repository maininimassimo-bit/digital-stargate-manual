"""Screen three WFC3 calibrators and measure only complete dither-matched triplets."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from io import BytesIO
from itertools import combinations
import json
from math import log10
from pathlib import Path
import sys
import warnings

PIN = "cd890601b037508ce9eeca7d9bb78cbec39f7230235f1fcada1f28cf85122e54"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return sha256(raw).hexdigest()


def verified(path, pin):
    raw = path.read_bytes()
    require(digest(raw) == pin, f"SHA-256 mismatch: {path.name}")
    return raw


def measure(np, data, error, quality, pam, seed, header, p, result):
    x, y = np.rint(seed).astype(int)
    patch = data[y-4:y+5, x-4:x+5]
    if not np.isfinite(patch).all():
        return "NONFINITE_CENTROID_PATCH"
    iy, ix = np.unravel_index(np.argmax(patch), patch.shape)
    x, y = x + ix - 4, y + iy - 4
    result["peakXY"] = [int(x), int(y)]
    delta = float(np.linalg.norm(np.array([x,y]) - seed))
    result["peakOffsetPx"] = delta
    if delta > p["maxPeakDistancePx"]:
        return "PEAK_OFFSET"
    core = data[y-3:y+4, x-3:x+4]
    flags = quality[y-3:y+4, x-3:x+4]
    result["coreDqPixels"] = int(np.count_nonzero(flags))
    result["coreDqOr"] = int(np.bitwise_or.reduce(flags.ravel(), initial=0))
    if not np.isfinite(core).all() or flags.any():
        return "CORE_DQ"
    weights = np.maximum(core-np.median(core), 0)
    if weights.sum() <= 0:
        return "CENTROID_WITHOUT_SIGNAL"
    coords = np.arange(-3, 4)
    x = float(x + (weights * coords[None, :]).sum()/weights.sum())
    y = float(y + (weights * coords[:, None]).sum()/weights.sum())
    result["centerXY"] = [x, y]
    height, width = data.shape
    ox, oy = (abs(float(header[name])) for name in ("LTV1", "LTV2"))
    require((int(ox), int(oy)) == (ox, oy), "Non-integral PAM offsets")
    ox, oy = int(ox), int(oy)
    correction = pam[oy:oy+height, ox:ox+width]
    require(correction.shape == data.shape and np.isfinite(correction).all() and (correction > 0).all(),
            "PAM footprint")
    sci, err = data * correction, error * correction
    yy, xx = np.ogrid[:height, :width]
    radius2 = (xx-x)**2 + (yy-y)**2
    good = (quality == 0) & np.isfinite(sci) & np.isfinite(err) & (err > 0)
    inner, outer = p["skyAnnulus"]
    if not (outer <= x < width-outer and outer <= y < height-outer):
        return "SKY_BOUNDARY"
    sky = (radius2 >= inner**2) & (radius2 <= outer**2)
    observed = sky & good
    if observed.sum() < p["minSkyFraction"] * sky.sum():
        return "SKY_SUPPORT"
    level = float(np.median(sci[observed]))
    scale = float(header["PHOTFLAM"])
    require(float(header["PHTFLAM1"]) > 0 and abs(scale / float(header["PHTFLAM1"])-1) < 1e-6,
            "UVIS1 FLUXCORR convention differs")
    for radius in p["apertureRadii"]:
        ap = radius2 <= radius**2
        if not good[ap].all():
            continue
        flux = float(np.sum(sci[ap] - level))
        if flux > 0:
            result["fluxCalibratedRadii"][str(radius)] = flux * scale / result["exptimeSeconds"]
    return "MEASURED_BOTH_RADII" if len(result["fluxCalibratedRadii"]) == len(p["apertureRadii"]) else "APERTURE_SUPPORT"


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("root", "dependencies", "report"):
        cli.add_argument(name, type=Path)
    cli.add_argument("acquisition_sha256")
    args = cli.parse_args()
    root = args.root
    p = json.loads(verified(root / "protocollo.json", PIN))
    capture = json.loads(verified(root / "acquisizione.json", args.acquisition_sha256))
    require(capture["protocolSha256"] == PIN
            and digest((root/"acquisisci.py").read_bytes()) == capture["programSha256"], "Acquisition lineage")
    verified(root / "catalogo.json", p["catalogSha256"])
    expected = {r["obs_id"]: dict(r, target=v["target"], visit=v["visit"])
                for v in p["selected"] for r in v["rows"]}
    require(len(expected) == len(capture["records"]) == 30 and set(expected) ==
            {r["observation"] for r in capture["records"]}, "Cohort changed")
    records = []
    for r in capture["records"]:
        row = expected[r["observation"]]
        require((r["target"], r["visit"], r["proposal"], r["band"], r["targetAlias"], r["obsid"]) ==
                (row["target"], row["visit"], int(row["proposal_id"]), row["filters"], row["target_name"], str(row["obsid"])),
                "Acquisition catalog identity differs")
        folder = root / "source"
        verified(folder / f'{r["observation"]}-query.json', r["querySha256"])
        verified(folder / f'{r["observation"]}-products.json', r["productsSha256"])
        if r["entries"]:
            records.extend(dict(r, **member, status="EXACT_FLC", catalogStartMjd=row["t_min"],
                                catalogEndMjd=row["t_max"]) for member in r["entries"])
        else:
            records.append(dict(r, file=None, status="NO_PUBLIC_FLC"))

    sys.path.insert(0, str(args.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import FITSFixedWarning, WCS

    warnings.filterwarnings("ignore", category=FITSFixedWarning)
    require((np.__version__, astropy.__version__) == ("2.3.5", "7.2.0"), "Dependencies changed")
    pams = {int(k): fits.getdata(BytesIO(verified(root/f"UVIS{k}wfc3_map.fits", pin))) for k,pin in p["pam"].items()}
    rows = []
    for record in records:
        file = record["file"]
        result = dict(file=file, visit=record["visit"], band=record["band"], proposal=record["proposal"],
                      state=record["status"], target=record["target"], observation=record["observation"],
                      fluxCalibratedRadii={})
        rows.append(result)
        if record["status"] != "EXACT_FLC":
            continue
        stem = file.removesuffix("_flc.fits")
        folder = root / "source"
        blob = verified(folder / file, record["sha256"])
        require(len(blob) == record["bytes"], "FLC length changed")
        with fits.open(BytesIO(blob), memmap=False) as h:
            hd = h[0].header
            require((hd["ROOTNAME"].lower(), hd["PROPOSID"], hd["TARGNAME"], hd["FILTER"]) ==
                    (stem, record["proposal"], record["targetAlias"], record["band"]), "FLC identity differs")
            require(record["catalogStartMjd"]-1e-5 <= float(hd["EXPSTART"]) <= record["catalogEndMjd"]+1e-5, "Observation timing identity differs")
            result.update(flag=hd["EXPFLAG"], scan=hd["SCAN_TYP"], startMjd=float(hd["EXPSTART"]),
                          exptimeSeconds=float(hd["EXPTIME"]), dither=[float(hd[k]) for k in ("POSTARG1","POSTARG2")])
            if (hd["EXPFLAG"], hd["SCAN_TYP"], hd["PCTECORR"], hd["FLUXCORR"]) != ("NORMAL","N","COMPLETE","COMPLETE"):
                result["state"] = "EXPOSURE_METADATA"
                continue
            possible = []
            for sci in (ext for ext in h if ext.name == "SCI"):
                wcs = WCS(sci.header, h).celestial
                seed = np.array(wcs.world_to_pixel_values(hd["RA_TARG"], hd["DEC_TARG"]))
                height, width = sci.data.shape
                if np.isfinite(seed).all() and 28 <= seed[0] < width-28 and 28 <= seed[1] < height-28:
                    possible.append((sci,seed))
            if len(possible) != 1:
                result["state"] = "TARGET_CHIP_UNRESOLVED"
                continue
            (sci, seed), = possible
            chip, extver = sci.header["CCDCHIP"], sci.header["EXTVER"]
            result.update(chip=chip, seedXY=seed.tolist())
            error, quality = h["ERR",extver], h["DQ",extver]
            require(sci.header["BUNIT"] == error.header["BUNIT"] == "ELECTRONS"
                    and sci.data.shape == error.data.shape == quality.data.shape, "SCI/ERR/DQ footprint")
            result["state"] = measure(np, sci.data.astype(float), error.data.astype(float), quality.data,
                                      pams[chip], seed, sci.header, p, result)

    groups = defaultdict(list)
    for r in rows:
        if "chip" in r:
            groups[(r["target"], r["visit"], r["chip"], tuple(r["dither"]))].append(r)
    triplets = []
    for (target, visit, chip, offset), group in sorted(groups.items()):
        by_band = {b: [r for r in group if r["band"] == b and r["state"] == "MEASURED_BOTH_RADII"] for b in p["bands"]}
        row = dict(target=target, visit=visit, chip=chip, dither=offset, eligible={b: len(v) for b,v in by_band.items()},
                   state="INCOMPLETE_OR_AMBIGUOUS_SUPPORT")
        triplets.append(row)
        if all(len(v) == 1 for v in by_band.values()):
            band_rows = {b: v[0] for b,v in by_band.items()}
            starts = [r["startMjd"] for r in band_rows.values()]
            span = max(starts)-min(starts)
            row["spanDays"] = span
            if span > p["maxTripletSpanDays"]:
                row["state"] = "TIME_LIMIT"
                continue
            colors = {}
            for radius in p["apertureRadii"]:
                flux = {b: r["fluxCalibratedRadii"][str(radius)] for b,r in band_rows.items()}
                colors[str(radius)] = {f"{a}-{b}": -2500*log10(flux[a]/flux[b]) for a,b in combinations(p["bands"],2)}
            row.update(state="COMPLETE", files=[r["file"] for r in band_rows.values()], rawColorsMillimag=colors)

    result = dict(schema="BKL046_WFC3_THREE_CALIBRATOR_POINTING_RESULT_V1", programSha256=digest(Path(__file__).read_bytes()),
                  protocolSha256=PIN, acquisitionSha256=args.acquisition_sha256, rows=rows, triplets=triplets,
                  counts=Counter(r["state"] for r in rows), targets=sorted({r["target"] for r in rows}), independentOfGD153Target=True,
                  qualifiedVisits=sorted({r["visit"] for r in triplets if r["state"] == "COMPLETE"}),
                  scientificClosures=0, nativeExecutions=0)
    with args.report.open("x", encoding="utf-8", newline="\n") as h:
        json.dump(result,h,indent=2,sort_keys=True,allow_nan=False)
        h.write("\n")


if __name__ == "__main__":
    main()