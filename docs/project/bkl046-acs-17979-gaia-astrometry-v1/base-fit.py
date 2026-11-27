from itertools import product
from pathlib import Path
import hashlib
import json
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def extract(science, dq, cfg):
    radius = cfg["centroidHalfWidthPx"]
    isolation = cfg["neighborIsolationPx"]
    no_flags = np.isin(dq, [0, 64])
    finite = np.isfinite(science)
    local = maximum_filter(np.where(finite, science, -np.inf), size=2*isolation+1, mode="nearest")
    bad = maximum_filter((~no_flags | ~finite).astype(np.uint8), size=2*isolation+1)
    points, tiles = [], []
    ny, nx = science.shape
    tile = cfg["tilePx"]
    edge = cfg["edgePx"]
    y_grid, x_grid = np.mgrid[-radius:radius+1, -radius:radius+1]
    for ty, y0 in enumerate(range(edge, ny-edge, tile)):
        ys = slice(y0, min(y0+tile, ny-edge))
        for tx, x0 in enumerate(range(edge, nx-edge, tile)):
            xs = slice(x0, min(x0+tile, nx-edge))
            section = science[ys, xs]
            background = float(np.nanmedian(section))
            use = (section == local[ys, xs]) & (bad[ys, xs] == 0)
            use &= (section-background >= cfg["minPeakAboveSkyE"]) & (section <= cfg["maxRecordedPeakE"])
            iy, ix = np.where(use)
            ranks = np.argsort(-section[iy, ix], kind="stable")[:cfg["peaksPerTile"]]
            for j, i in zip(iy[ranks]+y0, ix[ranks]+x0):
                patch = science[j-radius:j+radius+1, i-radius:i+radius+1]
                delta = np.maximum(patch.astype(float)-background, 0)
                total = delta.sum()
                offset_x = float((delta*x_grid).sum()/total)
                offset_y = float((delta*y_grid).sum()/total)
                points.append((i+offset_x, j+offset_y))
                tiles.append((tx, ty))
    return np.asarray(points).reshape(-1, 2), np.asarray(tiles).reshape(-1, 2)


def read_frame(root, info, cfg):
    filename = root / (info["id"]+"_flt.fits")
    if sha(filename) != info["sha256"]:
        raise ValueError("Input hash changed")
    frame = {}
    with fits.open(filename, memmap=False) as h:
        p = h[0].header
        if p["ROOTNAME"].lower() != info["id"] or p["PROPOSID"] != 17979 or p["CCDGAIN"] != 2:
            raise ValueError("Wrong exposure")
        for plane in (hdu for hdu in h if hdu.name == "SCI"):
            chip = plane.header["CCDCHIP"]
            wcs = WCS(plane.header, h)
            points, tiles = extract(plane.data, h["DQ", plane.ver].data, cfg)
            frame[chip] = {"wcs": wcs, "position": points, "tiles": tiles,
                           "world": wcs.all_pix2world(points, 0, ra_dec_order=True)}
    return frame


def pairs(long, short, cfg):
    predicted = short["wcs"].all_world2pix(long["world"], 0, quiet=True, ra_dec_order=True)
    positions = short["position"]
    good = np.isfinite(predicted).all(axis=1)
    predicted = predicted[good]
    tiles = long["tiles"][good]
    if len(predicted) < 2 or len(positions) < 2:
        return predicted[:0], positions[:0], tiles[:0]
    distance, neighbor = cKDTree(positions).query(predicted, k=2)
    rd, reverse = cKDTree(predicted).query(positions, k=2)
    picked = neighbor[:, 0]
    measured = positions[picked]
    limit = cfg["mutualSeparationRatio"]
    close = (distance[:, 0] <= cfg["mutualDistancePx"]) & (reverse[picked, 0] == np.arange(len(predicted)))
    close &= (limit*distance[:, 0] < distance[:, 1]) & (limit*rd[picked, 0] < rd[picked, 1])
    return predicted[close], measured[close], tiles[close]


def design(points, mode):
    bias = np.ones(len(points))
    if mode == "translation":
        return bias[:, None]
    scaled = (points-2048)/2048
    return np.column_stack((bias, scaled))


def stats(vector):
    norms = np.linalg.norm(vector, axis=1)
    if not len(norms):
        return None
    return {"medianPx": float(np.median(norms)), "p90Px": float(np.quantile(norms, 0.90)),
            "maxPx": float(norms.max()), "pairs": len(norms)}


def fit(predict, actual, tiles, cfg):
    hold = (2*tiles[:, 0]+tiles[:, 1]) % 4 == 0
    train = ~hold
    delta = actual-predict
    out = {"candidates": len(predict), "fitBeforeClipping": int(train.sum()), "holdout": int(hold.sum()),
           "holdoutTiles": len(set(map(tuple, tiles[hold]))),
           "originalHoldout": stats(delta[hold]), "models": {}}
    if train.sum() < cfg["minimumFitPairs"] or hold.sum() < cfg["minimumHoldoutPairs"]:
        return out
    for mode in ("translation", "affine"):
        basis = design(predict, mode)
        mask = train.copy()
        for _ in range(cfg["fitIterations"]):
            coeff, _, rank, _ = np.linalg.lstsq(basis[mask], delta[mask], rcond=None)
            if rank != basis.shape[1]:
                break
            norms = np.linalg.norm((delta-basis @ coeff)[mask], axis=1)
            median = np.median(norms)
            mad = 1.4826*np.median(abs(norms-median))
            threshold = max(cfg["fitResidualFloorPx"], median+cfg["fitClipMultiplier"]*mad)
            clipped = mask.copy()
            clipped[mask] = norms <= threshold
            if np.array_equal(clipped, mask) or clipped.sum() < cfg["minimumFitPairs"]:
                break
            mask = clipped
        coeff, _, rank, _ = np.linalg.lstsq(basis[mask], delta[mask], rcond=None)
        if rank != basis.shape[1]:
            continue
        test = stats((delta-basis @ coeff)[hold])
        qualified = (test["p90Px"] <= cfg["maximumHoldoutP90Px"] and test["maxPx"] <= cfg["maximumHoldoutPx"]
                     and out["holdoutTiles"] >= cfg["minimumHoldoutTiles"])
        out["models"][mode] = {"coefficientXY": coeff.tolist(), "trainRetained": int(mask.sum()),
                              "holdoutResidual": test, "withinDiagnosticThresholds": qualified}
    return out


def main():
    base, protocol, output = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    sources = {row["id"]: read_frame(base, row, cfg) for row in cfg["inputs"]}
    maps = []
    for long, short in product(("jfln05ykq", "jfln05ymq"), ("jfln02qtq", "jfln02qzq")):
        for long_chip, short_chip in product((1, 2), repeat=2):
            args = pairs(sources[long][long_chip], sources[short][short_chip], cfg)
            summary = fit(*args, cfg)
            maps.append({"long": long, "short": short, "chips": [long_chip, short_chip], **summary})
    report = {"schema": cfg["schema"], "protocolSha256": sha(protocol), "maps": maps,
              "guideCounts": {obs: {chip: len(frame["position"]) for chip, frame in planes.items()}
                              for obs, planes in sources.items()},
              "saturatedSourcesMeasured": 0, "scientificClosures": 0}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
