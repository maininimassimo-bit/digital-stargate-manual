"""Measure potential raw short-exposure support in pinned DECam TPV footprints."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


def digest(data):
    return sha256(data).hexdigest()


def partition(np, pixel, shape, pad):
    i = np.floor(pixel).astype(int)
    left = i - pad
    right = i + 1 + pad
    return (left >= 0).all(axis=1) & (right < np.array(shape[::-1])).all(axis=1), i


def supported(np, image, mapped, low, guards):
    rounded = np.floor(mapped + .5).astype(int)
    nearest_ok = ((rounded >= 0) & (rounded < np.array(image.shape[::-1]))).all(axis=1)
    near_value = np.zeros(len(mapped), image.dtype)
    near_value[nearest_ok] = image[rounded[nearest_ok, 1], rounded[nearest_ok, 0]]
    inside, floor = partition(np, mapped, image.shape, 0)
    extended, _ = partition(np, mapped, image.shape, 1)

    def extrema(mask, offsets):
        lower = np.full(len(mapped), 65535, image.dtype)
        upper = np.zeros(len(mapped), image.dtype)
        for dy in offsets:
            for dx in offsets:
                value = image[floor[mask, 1] + dy, floor[mask, 0] + dx]
                lower[mask] = np.minimum(lower[mask], value)
                upper[mask] = np.maximum(upper[mask], value)
        return lower, upper

    min4, max4 = extrema(inside, range(2))
    min16, max16 = extrema(extended, range(-1, 3))
    result = {"nearestCovered": int(nearest_ok.sum()), "fourCovered": int(inside.sum()),
              "extendedCovered": int(extended.sum()),
              "nearestCodeZero": int(np.count_nonzero(nearest_ok & (near_value == 0))),
              "guards": []}
    good = []
    for g in guards:
        bound = low * g
        near = nearest_ok & (near_value > 0) & (near_value < bound)
        four = inside & (min4 > 0) & (max4 < bound)
        sixteen = extended & (min16 > 0) & (max16 < bound)
        assert not np.any(sixteen & ~four) and not np.any(four & ~near)
        result["guards"].append({"factor": g, "upperCodeExclusive": bound,
                                 "nearest": int(near.sum()), "allFour": int(four.sum()),
                                 "allSixteen": int(sixteen.sum())})
        good.append((near, four, sixteen))
    return result, good


def main():
    cli = argparse.ArgumentParser()
    for name in ("protocol", "sourceKit", "dependencies", "report"):
        cli.add_argument(name, type=Path)
    a = cli.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    previous = (a.sourceKit / "riscontro.json").read_bytes()
    assert digest(previous) == p["sourceReportSha256"]
    prior = json.loads(previous)
    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    image = np.arange(1, 26, dtype=np.uint16).reshape(5, 5)
    test, _ = supported(np, image, np.array([[2., 2.], [4., 4.], [-1., -1.]]), 100, [1.0])
    assert [test[k] for k in ("nearestCovered", "fourCovered", "extendedCovered")] == [2, 1, 1]
    frames = {}
    for field, row in prior["fields"].items():
        for entry in row["frames"]:
            f = a.sourceKit / entry["file"]
            assert digest(f.read_bytes()) == entry["sha256"]
            with fits.open(f, memmap=False) as hdus:
                hdu, = hdus
                data = hdu.data.copy()
                assert list(data.shape) == entry["shapeYX"]
                wcs = WCS(hdu.header).celestial
            frames.setdefault(field, []).append((entry, data, wcs))

    reports = []
    for field, srcs in frames.items():
        targets = srcs[:1] if field == "M20" else srcs[:2]
        for origin, long, source_wcs in srcs[1:]:
            shorter = [t for t in targets if t[0]["exposureSeconds"] < origin["exposureSeconds"]]
            if field == "M8":
                masks = {"aboveBothHeaderLevels": long >= max(origin["headerAmplifierLevelsADU"])}
                assert int(masks["aboveBothHeaderLevels"].sum()) == origin["atOrAboveBoth"]
                if origin["zeroCodes"]:
                    masks["zeroCode"] = long == 0
                    assert int(masks["zeroCode"].sum()) == origin["zeroCodes"]
            else:
                numerator, denominator = p["m20TopRational"]
                n = (long.size * numerator + denominator - 1) // denominator
                cutoff = int(np.partition(long.ravel(), long.size - n)[long.size - n])
                masks = {"brightControl": long >= cutoff}
            for label, mask in masks.items():
                coordinates = np.argwhere(mask)[:, ::-1]
                ra, dec = source_wcs.pixel_to_world_values(coordinates[:, 0], coordinates[:, 1])
                assert np.isfinite([ra, dec]).all()
                children = []
                union = np.zeros((len(p["guardLevels"]), 3, len(coordinates)), dtype=bool)
                for (target, short, target_wcs) in shorter:
                    x, y = target_wcs.world_to_pixel_values(ra, dec)
                    mapped = np.stack([x, y], axis=1)
                    assert np.isfinite(mapped).all()
                    rt_ra, rt_dec = target_wcs.pixel_to_world_values(x, y)
                    rev_x, rev_y = source_wcs.world_to_pixel_values(rt_ra, rt_dec)
                    error = np.hypot(rev_x-coordinates[:, 0], rev_y-coordinates[:, 1])
                    assert np.max(error) <= p["roundTripMaxPixels"]
                    result, per_guard = supported(np, short, mapped, min(target["headerAmplifierLevelsADU"]),
                                                  p["guardLevels"])
                    union |= np.asarray(per_guard)
                    children.append({"target": target["source"], "seconds": target["exposureSeconds"],
                                     "roundTripMaximumPx": round(float(error.max()), 9), **result})
                report = {"field": field, "source": origin["source"], "seconds": origin["exposureSeconds"],
                          "selection": label, "sourceSamples": len(coordinates), "byTarget": children,
                          "atLeastOneShorter": [
                              {"factor": g, "nearest": int(v[0].sum()), "allFour": int(v[1].sum()),
                               "allSixteen": int(v[2].sum())}
                              for g, v in zip(p["guardLevels"], union, strict=True)]}
                if label == "brightControl":
                    report["controlLowerCode"] = cutoff
                reports.append(report)
    assert len(reports) == 5
    out = {"schema": "BKL046_DECAM_HDR_SUPPORT_WCS_RESULT_V1",
           "protocolSha256": digest(raw), "programSha256": digest(Path(__file__).read_bytes()),
           "comparisons": reports, "registeredOnData": False, "fluxRecoveryVerified": False,
           "nativeExecutions": 0, "scientificClosures": 0}
    with a.report.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
