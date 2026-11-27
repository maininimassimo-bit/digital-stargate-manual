import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.append(sys.argv[1])
import numpy as np
from astropy.io import fits


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checked(path, expected):
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    require(actual == expected, f"Input hash changed: {path.name}")
    return path


def cut(image, x, y, r):
    grid = image[y-r:y+r+1, x-r:x+r+1]
    require(grid.shape == (2*r+1, 2*r+1), "Incomplete stamp")
    return grid


def mask_union(stamps):
    bad = np.logical_or.reduce([row["bad"] for row in stamps])
    symmetric_bad = np.zeros_like(bad)
    for turns in range(4):
        rotated = np.rot90(bad, turns)
        symmetric_bad |= rotated | np.fliplr(rotated)
    return ~symmetric_bad


def load_stamps(source, cfg, reference, r):
    pam = fits.getdata(checked(source / cfg["pam"]["filename"], cfg["pam"]["sha256"]))
    rows = []
    previous = {row["id"]: row for row in reference["results"]}
    require(len(previous) == 6, "Unexpected reference population")
    for exposure in cfg["exposures"]:
        obs = exposure["id"]
        prior = previous[obs]
        require(prior["star"] == exposure["star"], "Reference star mismatch")
        x, y = prior["peakXYZeroBased"]
        with fits.open(checked(source / (obs + "_flt.fits"), exposure["flt"]), memmap=False) as hdus:
            sci = hdus["SCI"]
            dx, dy = (-int(sci.header[key]) for key in ("LTV1", "LTV2"))
            signal = cut(sci.data, x, y, r).astype(float) * cut(pam, x+dx, y+dy, r)
            dq = cut(hdus["DQ"].data, x, y, r).astype(int)
        require(np.isfinite(signal).all(), "Invalid signal")
        rows.append({"id": obs, "star": prior["star"], "signal": signal, "dq": dq,
                     "bad": ~np.isin(dq, cfg["allowedDQ"])})
    return rows


def annulus(distance, radii):
    return (distance >= radii[0]) & (distance <= radii[1])


def coverage(region, mask, minimum):
    count = int(region.sum())
    kept = int((region & mask).sum())
    require(count > 0 and kept / count >= minimum, "Insufficient shared pixel coverage")
    return {"retained": kept, "geometric": count}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("astropy_runtime")
    parser.add_argument("protocol", type=Path)
    parser.add_argument("pinned_inputs", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    cfg = json.loads(args.protocol.read_bytes())
    source = args.pinned_inputs
    ref = json.loads(checked(source / "riscontro.json", cfg["parentReportSha256"]).read_bytes())
    parent = json.loads(checked(source / "protocollo.json", cfg["parentProtocolSha256"]).read_bytes())
    r = max(limit[1] for limit in cfg["skyAnnuli"])
    stamps = load_stamps(source, parent, ref, r)
    dy, dx = np.mgrid[-r:r+1, -r:r+1]
    distance = np.hypot(dx, dy)
    shared = mask_union(stamps)
    diagnostics = []
    for bounds in cfg["wingAnnuli"]:
        geometric = annulus(distance, bounds)
        wing = geometric & shared
        wing_coverage = coverage(geometric, shared, cfg["minimumWingCoverage"])
        for sky_bounds in cfg["skyAnnuli"]:
            sky_geometric = annulus(distance, sky_bounds)
            sky = sky_geometric & shared
            sky_coverage = coverage(sky_geometric, shared, cfg["minimumSkyCoverage"])
            observations = []
            for stamp in stamps:
                signal = stamp["signal"] - np.median(stamp["signal"][sky])
                total = float(signal[wing].sum())
                require(total > 0, "Nonpositive shared wing sum")
                contrasts = {}
                for width in cfg["stripeHalfWidths"]:
                    along_x = wing & (abs(dy) <= width)
                    along_y = wing & (abs(dx) <= width)
                    require(along_x.sum() == along_y.sum() and along_x.any(), "Asymmetric sampling")
                    x = float(signal[along_x].sum())
                    y = float(signal[along_y].sum())
                    contrasts[str(width)] = {"xFraction": x / total, "yFraction": y / total,
                                             "yMinusXPercentOfWing": 100 * (y-x) / total}
                excluded = np.column_stack((dx[geometric & stamp["bad"]], dy[geometric & stamp["bad"]],
                                            stamp["dq"][geometric & stamp["bad"]]))
                observations.append({"id": stamp["id"], "star": stamp["star"], "wingE": total,
                                     "stripes": contrasts, "rejectedOffsetsXYDQ": excluded.tolist()})
            diagnostics.append({"wingPx": bounds, "skyPx": sky_bounds, "wingCoverage": wing_coverage,
                                "skyCoverage": sky_coverage, "observations": observations})
    report = {
        "schema": cfg["schema"], "protocolSha256": hashlib.sha256(args.protocol.read_bytes()).hexdigest(),
        "settings": diagnostics, "coreRecovered": False, "scientificClosures": 0,
    }
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
