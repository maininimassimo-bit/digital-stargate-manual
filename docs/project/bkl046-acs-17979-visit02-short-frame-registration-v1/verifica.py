import hashlib
from pathlib import Path
import json
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy import fft
from scipy.ndimage import uniform_filter
from scipy.signal import fftconvolve


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load(root, spec):
    path = root / (spec["id"]+"_flt.fits")
    if sha(path) != spec["sha256"]:
        raise ValueError("Changed FITS")
    with fits.open(path, memmap=False) as h:
        p = h[0].header
        if p["ROOTNAME"].lower() != spec["id"] or p["PROPOSID"] != 17979 or p["EXPTIME"] != 40:
            raise ValueError("Wrong short exposure")
        if p["CCDGAIN"] != 2 or "F606W" not in (p["FILTER1"], p["FILTER2"]):
            raise ValueError("Wrong instrument configuration")
        return {
            sci.header["CCDCHIP"]: (sci.data.astype(np.float32), h["DQ", sci.ver].data,
                                   WCS(sci.header, h))
            for sci in h if sci.name == "SCI"
        }


def feature(data, flags, cfg):
    valid = np.isin(flags, [0, 64]) & np.isfinite(data)
    clipped = np.where(valid, np.clip(data, *cfg["filteredClipE"]), 0).astype(np.float32)
    hood = uniform_filter(clipped, cfg["backgroundBoxWidthPx"])
    return np.where(valid, clipped-hood, 0)


def summed_windows(area, width):
    summed = np.pad(area.astype(float), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    return summed[width:, width:] - summed[:-width, width:] - summed[width:, :-width] + summed[:-width, :-width]


def template(reference, observed, cx, cy, cfg):
    w, s = cfg["templatePx"], cfg["searchPx"]
    r = w//2
    target = reference[cy-r:cy+r, cx-r:cx+r].astype(float)
    area = observed[cy-r-s:cy+r+s, cx-r-s:cx+r+s].astype(float)
    if target.shape != (w, w) or area.shape != (w+2*s, w+2*s):
        raise ValueError("Unexpected image boundary")
    target -= target.mean()
    numer = fftconvolve(area, target[::-1, ::-1], mode="valid")
    var_area = summed_windows(area**2, w) - summed_windows(area, w)**2/target.size
    denom = np.sqrt((target**2).sum()*np.maximum(var_area, 0))
    cor = np.divide(numer, denom, out=np.zeros_like(numer), where=denom>0)
    ry, rx = np.unravel_index(cor.argmax(), cor.shape)
    by, bx = np.ogrid[:cor.shape[0], :cor.shape[1]]
    excluded = (abs(by-ry) <= cfg["excludedPeakRadiusPx"]) & (abs(bx-rx) <= cfg["excludedPeakRadiusPx"])
    best = float(cor[ry, rx])
    alternative = float(cor[~excluded].max())
    return {"centerXY": [cx, cy], "bestXY": [int(rx-s), int(ry-s)], "correlation": best,
            "zeroShiftCorrelation": float(cor[s, s]), "margin": best-alternative,
            "supported": bool(best >= cfg["minimumTemplateCorrelation"] and
                         best-alternative >= cfg["minimumPeakMargin"] and max(abs(rx-s), abs(ry-s)) < s)}


def global_phase(ref, moving, cfg):
    y, x = ref.shape
    window = np.hanning(y).astype(np.float32)[:, None]*np.hanning(x).astype(np.float32)
    p = fft.rfft2(ref*window)
    q = fft.rfft2(moving*window)
    cross = q*np.conjugate(p)
    norm = abs(cross)
    phase = np.divide(cross, norm, out=np.zeros_like(cross), where=norm>0)
    corr = fft.fftshift(fft.irfft2(phase, s=ref.shape))
    cy, cx = y//2, x//2
    r = min(cfg["globalSearchPx"], cy-1, cx-1)
    band = corr[cy-r:cy+r+1, cx-r:cx+r+1]
    a, b = np.unravel_index(band.argmax(), band.shape)
    yy, xx = np.ogrid[:band.shape[0], :band.shape[1]]
    keep = (abs(yy-a) > 3) | (abs(xx-b) > 3)
    return {"bestXY": [int(b-r), int(a-r)], "peak": float(band[a, b]),
            "runnerUp": float(band[keep].max()), "zero": float(band[r, r]), "searchRadiusPx": r}


def main():
    photos, protocol, output = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    ref, mov = [load(photos, row) for row in cfg["files"]]
    x_shift, y_shift = cfg["controls"]["shiftXY"]
    report = {}
    centers = [(x,y) for y in cfg["tileCentersY"] for x in cfg["tileCentersX"]]
    for chip in (1, 2):
        ref_data, ref_dq, ref_wcs = ref[chip]
        mov_data, mov_dq, mov_wcs = mov[chip]
        original = feature(ref_data, ref_dq, cfg)
        shifted = feature(mov_data, mov_dq, cfg)
        simulated = np.roll(original*cfg["controls"]["scale"], (y_shift, x_shift), axis=(0, 1))
        control = template(original, simulated, *centers[0], cfg)
        if not control["supported"] or control["bestXY"] != [x_shift, y_shift]:
            raise ValueError("Failed positive translation control")
        sky = ref_wcs.all_pix2world(centers, 0, ra_dec_order=True)
        expected = mov_wcs.all_world2pix(sky, 0, ra_dec_order=True)-np.array(centers)
        records = [template(original, shifted, *center, cfg) for center in centers]
        for row, prediction in zip(records, expected):
            row["wcsPredictionXY"] = prediction.tolist()
        report[chip] = {"phase": global_phase(original, shifted, cfg), "positiveControl": control,
                        "templates": records, "supportedTiles": sum(row["supported"] for row in records)}
    payload = {"schema": cfg["schema"], "protocolSha256": sha(protocol), "chips": report,
               "scientificClosures": 0, "photometryPerformed": False}
    encoded = json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n"
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(encoded)


if __name__ == "__main__":
    main()
