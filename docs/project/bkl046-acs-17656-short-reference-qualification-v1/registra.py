from collections import Counter
from csv import DictReader
from itertools import combinations, product
import json
from pathlib import Path
import runpy
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.wcs import WCS
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree
import hashlib


def checked(path, expected):
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != expected:
        raise ValueError(f"Changed input: {path.name}")
    return path


def catalogue(path, cfg):
    def eligible(row):
        keys = ("pmra", "pmdec", "pmra_error", "pmdec_error", "ruwe", "phot_g_mean_mag")
        if any(not row[key] for key in keys) or row["astrometric_params_solved"] not in ("31", "95"):
            return False
        return (float(row["ruwe"]) < cfg["maxRUWE"] and
                max(float(row["pmra_error"]), float(row["pmdec_error"])) <= cfg["maxMotionErrorMasPerYear"] and
                cfg["gaiaMagRange"][0] <= float(row["phot_g_mean_mag"]) <= cfg["gaiaMagRange"][1])
    with path.open(encoding="utf-8-sig", newline="") as stream:
        entries = list(DictReader(stream))
    rows = [row for row in entries if eligible(row)]
    select = ("ra", "dec", "ref_epoch", "pmra", "pmdec")
    values = np.array([[float(row[key]) for key in select] for row in rows])
    origin = np.asarray(cfg["skyOrigin"])
    scale = np.array([np.cos(np.deg2rad(origin[1])), 1.0])*3600
    sky = (values[:, :2]-origin)*scale
    other_points = (np.array([[float(row["ra"]), float(row["dec"])] for row in entries])-origin)*scale
    nearest = cKDTree(other_points).query(sky, k=2)[0][:, 1]
    keep = nearest > cfg["maxGaiaNeighborArcsec"]
    tiles = np.floor(sky[keep]/cfg["skyTileArcsec"]).astype(int)
    ids = np.asarray([row["source_id"] for row in rows])[keep]
    return values[keep], tiles, ids


def propagated(data, year):
    world = data[:, :2].copy()
    dt = (year-data[:, 2])/3_600_000
    world[:, 0] += dt*data[:, 3]/np.cos(np.deg2rad(data[:, 1]))
    world[:, 1] += dt*data[:, 4]
    return world


def centroid(data, dq, prediction, cfg):
    x, y = (int(round(value)) for value in prediction)
    sky_r = cfg["backgroundOuterPx"]
    coverage = min(x, data.shape[1]-x-1, y, data.shape[0]-y-1)
    if coverage < sky_r:
        return "OUTSIDE", None
    patch = data[y-sky_r:y+sky_r+1, x-sky_r:x+sky_r+1]
    quality = dq[y-sky_r:y+sky_r+1, x-sky_r:x+sky_r+1]
    search = cfg["searchHalfWidthPx"]
    grid = np.arange(-sky_r, sky_r+1)
    rr = np.hypot(grid[:, None], grid)
    sky_mask = (rr >= 6) & (rr <= sky_r) & np.isin(quality, [0, 64]) & np.isfinite(patch)
    if sky_mask.sum() < 40:
        return "SKY", None
    background = float(np.median(patch[sky_mask]))
    central = slice(sky_r-search, sky_r+search+1)
    window = patch[central, central]
    if not np.isfinite(window).all():
        return "NONFINITE", None
    iy, ix = np.unravel_index(np.argmax(window), window.shape)
    amplitude = float(window[iy, ix])-background
    if amplitude < cfg["minimumPeakAboveSkyE"]:
        return "PEAK_BELOW_MINIMUM", None
    if window[iy, ix] > cfg["maximumFullWellSafePeakE"]:
        return "PEAK_ABOVE_LIMIT", None
    yy, xx = np.indices(window.shape)
    far = np.hypot(yy-iy, xx-ix) > cfg["minimumCompanionSeparationPx"]
    peaks = (window == maximum_filter(window, size=3, mode="nearest")) & far
    if np.any((window-background)[peaks] > amplitude*cfg["companionPeakRatio"]):
        return "AMBIGUOUS_PEAK", None
    px, py = ix+sky_r-search, iy+sky_r-search
    c = cfg["centroidHalfWidthPx"]
    cols, rows = slice(px-c, px+c+1), slice(py-c, py+c+1)
    good = np.isin(quality[rows, cols], [0, 64])
    if not good.all() or not np.isfinite(patch[rows, cols]).all():
        return "CORE_DQ", None
    weight = np.maximum(patch[rows, cols].astype(float)-background, 0)
    support = np.arange(-c, c+1)
    measured = np.array([x+px-sky_r+(weight*support).sum()/weight.sum(),
                         y+py-sky_r+(weight*support[:, None]).sum()/weight.sum()])
    if np.linalg.norm(measured-prediction) > cfg["maximumCentroidDisplacementPx"]:
        return "CENTROID_DISPLACEMENT", None
    return "MATCH", measured


def measure_image(hdus, values, tiles, ids, cfg, fit_cfg, previous):
    t = hdus[0].header
    epoch = Time((t["EXPSTART"]+t["EXPEND"])/2, format="mjd", scale="utc").tcb.jyear
    world = propagated(values, epoch)
    by_chip = {}
    for sci in (hdu for hdu in hdus if hdu.name == "SCI"):
        chip = sci.header["CCDCHIP"]
        wcs = WCS(sci.header, hdus)
        pred = wcs.all_world2pix(world, 0, quiet=True, ra_dec_order=True)
        dq = hdus["DQ", sci.ver].data
        counts = Counter()
        rows = []
        for i, point in enumerate(pred):
            if not np.isfinite(point).all():
                counts["NONFINITE_WCS"] += 1
                continue
            status, measured = centroid(sci.data, dq, point, cfg)
            counts[status] += 1
            if status == "MATCH":
                rows.append((i, measured))
        index = np.asarray([row[0] for row in rows], dtype=int)
        actual = np.asarray([row[1] for row in rows]).reshape(-1, 2)
        summary = previous["fit"](pred[index], actual, tiles[index], fit_cfg)
        spatial_hold = (2*tiles[index, 0]+tiles[index, 1]) % 4 == 0
        summary.update({"statusCounts": dict(counts), "epochJyearTCB": float(epoch)})
        by_chip[chip] = (summary, set(ids[index]), set(ids[index[spatial_hold]]))
    return by_chip


def main():
    work, photos, protocol, output = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    prev_code = checked(work / "base-fit.py", cfg["parentCodeSha256"])
    previous = runpy.run_path(str(prev_code))
    fit_cfg = json.loads(checked(work / "base-protocol.json", cfg["parentProtocolSha256"]).read_bytes())
    values, tiles, ids = catalogue(checked(work / "gaia-dr3.csv", cfg["catalogSha256"]), cfg)
    result = {}
    for record in cfg["inputs"]:
        obs = record["id"]
        image = checked(photos / (obs+"_flt.fits"), record["sha256"])
        with fits.open(image, memmap=False) as hdus:
            header = hdus[0].header
            if (header["ROOTNAME"].lower() != obs or header["PROPOSID"] != record["program"]
                    or header["CCDGAIN"] != 2 or header["EXPTIME"] != 40
                    or "F606W" not in (header["FILTER1"], header["FILTER2"])):
                raise ValueError("Wrong FITS identity")
            result[obs] = measure_image(hdus, values, tiles, ids, cfg, fit_cfg, previous)
    shared = []
    for (left_obs, right_obs), lc, sc in product(combinations(result, 2), (1, 2), (1, 2)):
        _, left, left_hold = result[left_obs][lc]
        _, right, right_hold = result[right_obs][sc]
        shared.append({"left": left_obs, "right": right_obs, "chips": [lc, sc],
                       "matchedGaiaIdsInBoth": len(left & right), "heldOutGaiaIdsInBoth": len(left_hold & right_hold)})
    report = {"schema": cfg["schema"], "protocolSha256": hashlib.sha256(protocol.read_bytes()).hexdigest(),
              "eligibleGaiaSources": len(ids), "sharedIds": shared,
              "fits": {obs: {chip: values[0] for chip, values in frames.items()} for obs, frames in result.items()},
              "photometryPerformed": False, "scientificClosures": 0}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
