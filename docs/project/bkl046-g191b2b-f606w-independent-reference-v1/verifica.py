from pathlib import Path
import hashlib
import json
import sys

sys.path.append(sys.argv[1])
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS, NoConvergence
import astropy.units as u


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def measure(path, cfg):
    target = SkyCoord(cfg["raDeg"] * u.deg, cfg["decDeg"] * u.deg)
    with fits.open(path, memmap=False) as hdus:
        header = hdus[0].header
        if header["DETECTOR"] != "WFC" or "F606W" not in (header["FILTER1"], header["FILTER2"]):
            raise ValueError(f"Wrong detector or filter: {path.name}")
        candidates = []
        for plane in (hdu for hdu in hdus if hdu.name == "SCI"):
            world = WCS(plane.header, hdus).celestial
            try:
                x, y = world.world_to_pixel(target)
            except NoConvergence:
                continue
            if not np.isfinite([x, y]).all():
                continue
            data = plane.data
            dq = hdus["DQ", plane.ver].data.astype(np.int32)
            radius = cfg["searchHalfWidthPx"]
            xi, yi = int(round(float(x))), int(round(float(y)))
            if min(xi, yi) < radius or xi + radius >= data.shape[1] or yi + radius >= data.shape[0]:
                continue
            box = data[yi-radius:yi+radius+1, xi-radius:xi+radius+1]
            by, bx = (int(value) for value in np.unravel_index(np.nanargmax(box), box.shape))
            peak_x, peak_y = xi-radius+bx, yi-radius+by
            separation = float(target.separation(world.pixel_to_world(peak_x, peak_y)).arcsec)
            ly, lx = np.ogrid[:data.shape[0], :data.shape[1]]
            core = (ly-peak_y)**2 + (lx-peak_x)**2 <= cfg["coreRadiusPx"]**2
            candidates.append({"chip": plane.header["CCDCHIP"], "shape": list(data.shape),
                               "peakXYZeroBased": [peak_x, peak_y], "peakDistanceArcsec": separation,
                               "peakE": float(data[peak_y, peak_x]), "peakDQ": int(dq[peak_y, peak_x]),
                               "coreFullWellFlags": int(np.count_nonzero(dq[core] & 256)),
                               "coreADCFlags": int(np.count_nonzero(dq[core] & 2048)),
                               "coreOtherMaskFlags": int(np.count_nonzero(~np.isin(dq[core], [0, 64, 256, 2048]))),
                               "ltvXY": [plane.header["LTV1"], plane.header["LTV2"]]})
        eligible = [row for row in candidates if row["peakDistanceArcsec"] <= cfg["maximumMatchArcsec"]]
        result = {"obs": header["ROOTNAME"], "program": header["PROPOSID"], "target": header["TARGNAME"],
                  "date": header["DATE-OBS"], "expTime": header["EXPTIME"], "aperture": header["APERTURE"],
                  "amp": header["CCDAMP"], "gain": header["CCDGAIN"], "candidates": candidates,
                  "identityMatched": len(eligible) == 1}
        if len(eligible) == 1:
            image = eligible[0]
            result["coreClean"] = all(image[field] == 0 for field in
                                      ("coreFullWellFlags", "coreADCFlags", "coreOtherMaskFlags"))
        return result


def main():
    root = Path(sys.argv[2])
    protocol = Path(sys.argv[3])
    config = json.loads(protocol.read_bytes())
    results = []
    for entry in config["inputs"]:
        path = root / entry["file"]
        if sha(path) != entry["sha256"]:
            raise ValueError(f"Changed input: {path.name}")
        results.append(measure(path, config))
    report = {"protocolSha256": sha(protocol), "images": results, "scientificClosures": 0}
    with Path(sys.argv[4]).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
