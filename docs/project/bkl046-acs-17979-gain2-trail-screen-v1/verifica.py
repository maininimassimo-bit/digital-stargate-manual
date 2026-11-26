from collections import Counter
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import find_objects, label, maximum_filter


def check(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def open_input(path, expected, stack):
    check(sha(path) == expected, f"Input hash changed: {path.name}")
    return stack.enter_context(fits.open(path, memmap=False))


def read_frame(hdus, role):
    primary = hdus[0].header
    check(primary["PROPOSID"] == 17979 and primary["EXPTIME"] == (150 if role == "long" else 40),
          "Unexpected visit or exposure time")
    check(primary["CCDGAIN"] == 2 and not primary["SUBARRAY"] and
          "F606W" in (primary["FILTER1"], primary["FILTER2"]), "Unexpected detector setup")
    images = {}
    for hdu in (hdu for hdu in hdus if hdu.name == "SCI"):
        h = hdu.header
        check(h["BUNIT"] == "ELECTRONS", "Unexpected units")
        images[h["CCDCHIP"]] = {
            "sci": hdu.data, "dq": hdus["DQ", hdu.ver].data, "wcs": WCS(h, hdus),
            "offset": [-int(h[key]) for key in ("LTV1", "LTV2")],
        }
    check(set(images) == {1, 2}, "Both chips required")
    return images


def stamp(images, center, radius, pam):
    x, y = (int(round(v)) for v in center)
    ny, nx = images["sci"].shape
    if not (radius <= x < nx-radius and radius <= y < ny-radius):
        return None
    sx, sy = images["offset"]
    slx, sly = slice(x-radius, x+radius+1), slice(y-radius, y+radius+1)
    area = pam[sly.start+sy:sly.stop+sy, slx.start+sx:slx.stop+sx]
    check(area.shape == (2*radius+1,)*2, "PAM slice changed")
    return images["sci"][sly, slx].astype(float)*area, images["dq"][sly, slx]


def coordinate(frame, world):
    xy = frame["wcs"].all_world2pix([world], 0, quiet=True, ra_dec_order=True)[0]
    return tuple(float(v) for v in xy)


def find_reference(frame, world, cfg):
    xy = coordinate(frame, world)
    if not np.isfinite(xy).all():
        return None
    x, y = map(lambda v: int(round(v)), xy)
    r = cfg["shortSearchPx"]
    sci = frame["sci"]
    if not (r <= y < sci.shape[0]-r and r <= x < sci.shape[1]-r):
        return None
    window = sci[y-r:y+r+1, x-r:x+r+1]
    iy, ix = np.unravel_index(np.nanargmax(window), window.shape)
    peak = (int(x-r+ix), int(y-r+iy))
    if np.hypot(peak[0]-xy[0], peak[1]-xy[1]) > cfg["maximumPeakOffsetPx"]:
        return None
    return peak


def connected_long(long, cfg):
    mask = (long["dq"] & 256) != 0
    components, _ = label(mask)
    for index, bounds in enumerate(find_objects(components), 1):
        yy, xx = bounds
        if yy.stop-yy.start < cfg["minimumVerticalSpanPx"]:
            continue
        dy, dx = np.where(components[bounds] == index)
        ys, xs = dy+yy.start, dx+xx.start
        flags = long["dq"][ys, xs].astype(int)
        yield xs, ys, flags


def assess(images, pam, component, cfg, chip):
    long, sa, sb = images
    xs, ys, flags = component
    mixed = int(np.count_nonzero(~np.isin(flags, [256, 320])))
    descriptor = {"chip": chip, "componentPixels": len(xs),
                  "centerXY": [float(np.median(xs)), float(np.median(ys))],
                  "verticalSpan": int(ys.max()-ys.min()+1), "mixedPixels": mixed,
                  "flagCounts": {str(value): count for value, count in Counter(flags.tolist()).items()}}
    if mixed:
        return descriptor | {"status": "MIXED_TRAIL_FLAGS"}
    center = descriptor["centerXY"]
    world = long["wcs"].all_pix2world([center], 0, ra_dec_order=True)[0]
    positions = [find_reference(ref, world, cfg) for ref in (sa, sb)]
    if None in positions:
        return descriptor | {"status": "SHORT_MATCH_MISSING"}
    ref_world = [ref["wcs"].all_pix2world([xy], 0, ra_dec_order=True)[0]
                 for ref, xy in zip((sa, sb), positions)]
    long_a, long_b = (np.array(coordinate(long, w)) for w in ref_world)
    if np.linalg.norm(long_a-long_b) > cfg["maximumShortDisagreementPx"]:
        return descriptor | {"status": "SHORT_MATCH_DISAGREEMENT"}
    x, y = peak_long = tuple(int(round(v)) for v in (long_a+long_b)/2)
    if np.hypot(xs-x, ys-y).min() > cfg["maximumTrailDistancePx"]:
        return descriptor | {"status": "LONG_CENTER_OFF_TRAIL"}
    r = cfg["skyPx"][1]
    boxes = [stamp(frame, peak, r, pam) for frame, peak in zip(images, [peak_long, *positions])]
    if any(box is None for box in boxes) or np.max(np.maximum(abs(xs-x), abs(ys-y))) >= cfg["skyPx"][0]-cfg["paddingPx"]:
        return descriptor | {"status": "WINDOW_OR_SKY_OVERLAP"}
    yy, xx = np.mgrid[-r:r+1, -r:r+1]
    distance = np.hypot(xx, yy)
    aperture = distance <= cfg["radiiPx"][0]
    trail = np.zeros_like(aperture)
    for offset in range(-cfg["paddingPx"], cfg["paddingPx"]+1):
        trail[ys-y+r+offset, xs-x+r] = True
    shape = aperture | trail
    sky_ring = (distance >= cfg["skyPx"][0]) & (distance <= r)
    core_region = distance <= cfg["referenceCleanRadiusPx"]
    skies, good = [], []
    for idx, (signal, quality) in enumerate(boxes):
        allowed = np.isin(quality, [0, 64])
        sky_valid = sky_ring & allowed
        if not np.isfinite(signal).all() or sky_valid.sum() < cfg["minimumSkyPixels"]:
            return descriptor | {"status": "SKY_OR_SIGNAL_INVALID"}
        sky = float(np.median(signal[sky_valid]))
        skies.append(sky)
        if idx == 0:
            allowed |= trail & np.isin(quality, [256, 320])
        else:
            if not allowed[core_region].all() or np.any((quality[shape] & (256 | 2048)) != 0):
                return descriptor | {"status": "SHORT_CORE_OR_SUPPORT_FLAGGED"}
            neighbors = (distance > cfg["isolationRadiusPx"]) & shape
            peaks = signal == maximum_filter(signal, size=3, mode="nearest")
            if np.any(neighbors & peaks & (signal-sky > cfg["neighborLimitFraction"]*(signal[r, r]-sky))):
                return descriptor | {"status": "BRIGHT_NEIGHBOR"}
        good.append(allowed)
    mask = np.logical_and.reduce(good)
    if not mask[trail].all() or (shape & mask).sum() < cfg["minCoverageFraction"]*shape.sum():
        return descriptor | {"status": "UNUSABLE_COMMON_APERTURE"}
    results = []
    for region in (aperture, shape):
        rates = [float((data[region & mask]-sky).sum())/exposure
                 for (data, _), sky, exposure in zip(boxes, skies, (150, 40, 40))]
        if min(rates) <= 0:
            return descriptor | {"status": "NONPOSITIVE_RATE"}
        results.append(rates)
    (l0, a0, b0), (l1, a1, b1) = results
    short_delta = 100*abs(a1-b1)/((a1+b1)/2)
    return descriptor | {
        "status": "MEASURED" if short_delta <= cfg["maxShortRepeatPercent"] else "SHORT_RATE_DISAGREEMENT",
        "shortRepeatPercent": short_delta, "circleLongMinusShortPercent": 100*(l0/((a0+b0)/2)-1),
        "trailLongMinusShortPercent": 100*(l1/((a1+b1)/2)-1),
        "actualFlaggedOutsideCircle": int(np.count_nonzero((np.hypot(xs-x, ys-y) > cfg["radiiPx"][0]))),
        "extraPixels": int((shape & ~aperture & mask).sum()), "fluxRates": results,
    }


def main():
    base, file, output = map(Path, sys.argv[3:])
    cfg = json.loads(file.read_bytes())
    with ExitStack() as stack:
        frames = [read_frame(open_input(base / row["file"], row["sha256"], stack), row["role"])
                  for row in cfg["inputs"]]
        pams = {int(chip): fits.getdata(base / f"wfc{chip}_newpam.fits")
                for chip in cfg["pam"] if sha(base / f"wfc{chip}_newpam.fits") == cfg["pam"][chip]}
        check(set(pams) == {1, 2}, "PAM files changed")
        rows = []
        for chip in (1, 2):
            images = [frame[chip] for frame in frames]
            for component in connected_long(images[0], cfg):
                rows.append(assess(images, pams[chip], component, cfg, chip))
    statuses = Counter(row["status"] for row in rows)
    report = {"schema": cfg["schema"], "protocolSha256": sha(file), "counts": dict(statuses),
              "rows": rows, "scientificClosures": 0}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
