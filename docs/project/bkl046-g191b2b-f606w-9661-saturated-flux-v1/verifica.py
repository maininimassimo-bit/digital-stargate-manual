import hashlib
import json
from pathlib import Path
import sys

sys.path.append(sys.argv[1])
import numpy as np
from astropy.io import fits


def verify(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def checked(path, expected):
    verify(digest(path) == expected, f"Input hash changed: {path.name}")
    return path


def cut(array, center, radius):
    x, y = center
    data = array[y-radius:y+radius+1, x-radius:x+radius+1]
    verify(data.shape == (2*radius+1, 2*radius+1), "Cutout crosses detector edge")
    return data


def load_image(path, receipt):
    with fits.open(path, memmap=False) as hdus:
        primary = hdus[0].header
        verify(primary["ROOTNAME"] == receipt["obs"] and primary["PROPOSID"] == 9661, "Wrong visit or exposure")
        verify(primary["APERTURE"] == "WFC1-2K" and primary["CCDAMP"] == "B" and primary["CCDGAIN"] == 4,
               "Wrong detector configuration")
        verify("F606W" in (primary["FILTER1"], primary["FILTER2"]), "Wrong filter")
        sci = next(hdu for hdu in hdus if hdu.name == "SCI" and hdu.header["CCDCHIP"] == 1)
        verify(sci.header["BUNIT"] == "ELECTRONS", "Wrong units")
        return {
            "sci": sci.data, "dq": hdus["DQ", sci.ver].data,
            "err": hdus["ERR", sci.ver].data,
            "peak": tuple(receipt["candidates"][0]["peakXYZeroBased"]),
            "ltv": tuple(-int(sci.header[key]) for key in ("LTV1", "LTV2")),
            "exptime": primary["EXPTIME"], "expstart": primary["EXPSTART"],
            "photflam": sci.header.get("PHOTFLAM", primary.get("PHOTFLAM")),
        }


def register(short, long, cfg):
    inner, radius = cfg["registrationAnnulus"]
    yy, xx = np.mgrid[-radius:radius+1, -radius:radius+1]
    rr = np.hypot(xx, yy)
    region = (rr >= inner) & (rr <= radius) & (abs(xx) > cfg["registrationExcludedColumnHalfWidth"])
    ref = cut(short["sci"], short["peak"], radius)
    refgood = np.isin(cut(short["dq"], short["peak"], radius), [0, 64])
    shift = cfg["registrationShiftPx"]
    ox, oy = long["peak"]
    fits_found = []
    for dy in range(-shift, shift+1):
        for dx in range(-shift, shift+1):
            center = (ox+dx, oy+dy)
            dql = cut(long["dq"], center, radius)
            valid = region & refgood & np.isin(dql, [0, 64])
            verify(valid.sum() >= 0.9 * region.sum(), "Too little unflagged registration support")
            measurement = cut(long["sci"], center, radius)
            coeff = float(np.corrcoef(ref[valid], measurement[valid])[0, 1])
            fits_found.append((coeff, center, int(valid.sum())))
    fits_found.sort(reverse=True)
    best, center, pixels = fits_found[0]
    next_best = fits_found[1][0]
    verify(best >= cfg["minimumCorrelation"] and best-next_best >= cfg["minimumCorrelationGap"],
           "Ambiguous integer registration")
    return center, {"correlation": best, "runnerUp": next_best, "pixels": pixels, "longCenterXY": center}


def load_stamp(image, center, radius, pam):
    x, y = center
    dx, dy = image["ltv"]
    area = cut(pam, (x+dx, y+dy), radius).astype(float)
    return (cut(image["sci"], center, radius).astype(float)*area,
            cut(image["err"], center, radius).astype(float)*area,
            cut(image["dq"], center, radius).astype(int))


def photometry(signal, errors, sky, region, time):
    values = signal[sky]
    n = int(region.sum())
    verify(n > 0 and values.size >= 100 and np.isfinite(errors[region]).all(), "Invalid photometry support")
    background = float(np.median(values))
    total = float((signal[region]-background).sum())
    verify(total > 0, "Nonpositive exposure sum")
    # ERR variance only. Background, CTE, calibration and covariance remain systematic terms.
    error = float(np.sqrt(np.square(errors[region]).sum()))
    return total/time, error/time, background


def expand_trail(flag, y, width):
    out = flag.copy()
    for distance in range(1, width+1):
        out[distance:, :] |= flag[:-distance, :]
        out[:-distance, :] |= flag[distance:, :]
    verify(not out[abs(y) == abs(y).max()].any(), "Trail expansion touches boundary")
    return out


def main():
    root, prior, cfg_path, output = map(Path, sys.argv[2:])
    cfg = json.loads(cfg_path.read_bytes())
    rows = json.loads(checked(prior / "riscontro.json", cfg["referenceReport"]).read_bytes())["images"]
    by_id = {row["obs"]: row for row in rows if row["identityMatched"]}
    short, long = [load_image(checked(prior / (item["id"]+"_flt.fits"), item["sha256"]), by_id[item["id"]])
                   for item in cfg["files"]]
    pam = fits.getdata(checked(root / "wfc1_newpam.fits", cfg["pam"]))
    long_center, registration = register(short, long, cfg)
    n = max(bounds[1] for bounds in cfg["skyAnnuli"])
    y, x = np.mgrid[-n:n+1, -n:n+1]
    distance = np.hypot(x, y)
    ss, se, sd = load_stamp(short, short["peak"], n, pam)
    ls, le, ld = load_stamp(long, long_center, n, pam)
    actual = (ld & 256) != 0
    verify(not np.any(sd & (256 | 2048)) and not np.any(ld & 2048), "Unexpected saturation regime")
    verify(actual.any() and not actual[distance > cfg["bleedSearchPx"]].any(), "Unexpected trail extent")
    strict = np.isin(sd, [0, 64]) & np.isin(ld, [0, 64])
    admitted = np.isin(sd, [0, 64]) & np.isin(ld, [0, 64, 256, 320])
    formats = {f"trail{w}": expand_trail(actual, y, w) for w in cfg["bleedPaddingPx"]}
    records = []
    for inner, outer in cfg["skyAnnuli"]:
        sky = strict & (distance >= inner) & (distance <= outer)
        for radius in cfg["radii"]:
            circle = distance <= radius
            modes = {"pairedMask": (circle, strict, strict), "excludeOnlyLongDQ256": (circle, admitted, strict),
                     "circleIncludesRecordedDQ256": (circle, admitted, admitted)}
            modes.update({key: (circle | extension, admitted, admitted) for key, extension in formats.items()})
            for mode, (shape, short_mask, long_mask) in modes.items():
                st, su, bs = photometry(ss, se, sky, shape & short_mask, short["exptime"])
                lt, lu, bl = photometry(ls, le, sky, shape & long_mask, long["exptime"])
                ratio = lt/st
                records.append({
                    "radiusPx": radius, "skyPx": [inner, outer], "mode": mode,
                    "shortEPerSecond": st, "longEPerSecond": lt,
                    "longMinusShortPercent": 100*(ratio-1),
                    "nominalErrOnlyPercent": 100*ratio*float(np.hypot(su/st, lu/lt)),
                    "retainedFullWellPixels": int((actual & shape & long_mask).sum()),
                    "shortPixels": int((shape & short_mask).sum()),
                    "longPixels": int((shape & long_mask).sum()),
                    "skyEPerPixel": [bs, bl],
                })
    limit = cfg["primary"]
    finding = next(row for row in records if row["radiusPx"] == limit["radiusPx"] and row["skyPx"] == limit["skyPx"]
                   and row["mode"] == "circleIncludesRecordedDQ256")
    report = {
        "schema": cfg["schema"], "protocolSha256": digest(cfg_path),
        "registration": registration, "exposureTimes": [short["exptime"], long["exptime"]],
        "minutesBetweenStarts": 1440*(long["expstart"]-short["expstart"]),
        "photflam": [short["photflam"], long["photflam"]],
        "fullWellPixels": int(actual.sum()), "trailMaxRadiusPx": float(distance[actual].max()),
        "primaryWithinDiagnosticTolerance": abs(finding["longMinusShortPercent"]) <= limit["acceptanceDifferentialPercent"],
        "settings": records, "corePixelRecoveryClaimed": False, "scientificClosures": 0,
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
