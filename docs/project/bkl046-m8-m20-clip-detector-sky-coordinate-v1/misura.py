"""Compare recurring clipped CFA sites in detector and affine sky coordinates."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from math import floor
from pathlib import Path
import sys
from zipfile import ZipFile


PARITIES = {"R": (0, 0), "G1": (1, 0), "G2": (0, 1), "B": (1, 1)}
MODELS = ("detector", "binned", "mosaic")


def pinned_json(path, expected):
    data = path.read_bytes()
    assert sha256(data).hexdigest() == expected, path
    return json.loads(data)


def clipped_sites(np, fits, archive, rows, member_key, date_key, expected_type):
    with ZipFile(archive) as z:
        for row in rows:
            data = z.read(row[member_key])
            assert sha256(data).hexdigest() == row["sha256"]
            with fits.open(BytesIO(data), memmap=False, uint=True) as hdus:
                header = hdus[0].header
                assert header["DATE-OBS"] == row[date_key] and header["IMAGETYP"] == expected_type
                assert header["BITPIX"] == 16 and header["BSCALE"] == 1 and header["BZERO"] == 32768
                assert header["BAYERPAT"] == "RGGB" and header["EXPTIME"] == 180 and header["GAIN"] == 100
                image = hdus[0].data
                assert image.dtype == np.uint16 and image.shape == (4176, 6248)
                yield np.argwhere(image == 65535)[:, ::-1]


def project(points, forward, np):
    inverse = np.linalg.inv(forward)
    return points @ inverse[:2, :2].T + inverse[:2, 2]


def nearest_counts(source, target, radii):
    side = radii[-1]
    cells = {}
    for x, y in target.tolist():
        cells.setdefault((floor(x / side), floor(y / side)), []).append((x, y))
    hit = [0] * len(radii)
    squares = [radius * radius for radius in radii]
    for x, y in source.tolist():
        col, row = floor(x / side), floor(y / side)
        best = min(
            ((x-u)**2 + (y-v)**2
             for dcol in (-1, 0, 1) for drow in (-1, 0, 1)
             for u, v in cells.get((col+dcol, row+drow), ())),
            default=float("inf"),
        )
        for i, limit in enumerate(squares):
            hit[i] += best <= limit
    return hit


def main():
    cli = argparse.ArgumentParser()
    for name in ("protocol", "lightArchive", "lightReceipt", "darkArchive", "darkReceipt",
                 "geometry", "prior", "dependencies", "report"):
        cli.add_argument(name, type=Path)
    a = cli.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    for key in ("lightArchive", "darkArchive"):
        with getattr(a, key).open("rb") as f:
            assert file_digest(f, "sha256").hexdigest() == p[key]
    lights = pinned_json(a.lightReceipt, p["lightReceipt"])["rows"]
    darks = pinned_json(a.darkReceipt, p["darkReceipt"])["sourceMembers"]["dark"]
    matrices = pinned_json(a.geometry, p["geometry"])
    prior = pinned_json(a.prior, p["prior"])
    assert len(lights) == len(darks) == 15
    assert matrices["coordinateConvention"] == "zero-based integer pixel centers, x then y, forward column-vector map"
    assert matrices["imageShapeXY"] == [6248, 4176]
    assert matrices["validationPairs"] == 742
    by_name = {row["member"]: row for row in matrices["referenceToInputAffine"]}
    assert set(by_name) == {row["member"] for row in lights[1:]}

    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    point = np.array([[10, 10]])
    shifted = np.array([[13, 14]])
    translation = np.array([[1, 0, 3], [0, 1, 4], [0, 0, 1]])
    assert nearest_counts(point, shifted, p["radii"]) == [0, 0, 0]
    assert nearest_counts(point, project(shifted, translation, np), p["radii"]) == [1, 1, 1]
    assert nearest_counts(point, np.array([[11, 11]]), p["radii"]) == [0, 1, 1]

    defects = list(clipped_sites(np, fits, a.darkArchive, darks[:1], "file", "date", "Dark"))
    defect, = defects
    assert defect.shape == (1, 2) and (defect[0] % 2 == 0).all()
    assert all(row["ceiling"] == 1 for row in prior["darkEventsByFrame"])
    assert prior["bands"]["R"]["clippedLightEvents"]["darkCeiling"] == 15
    points = list(clipped_sites(np, fits, a.lightArchive, lights, "member", "dateObs", "Light"))
    observed = {parity: 0 for parity in PARITIES}
    excluded_edges = 0
    frames = []
    margin = p["margin"]
    minimum = 2
    maximum = np.array(matrices["imageShapeXY"]) - 1
    for i, (row, xy) in enumerate(zip(lights, points, strict=True)):
        keep = (xy != defect[0]).any(axis=1)
        assert len(xy) - np.count_nonzero(keep) == 1
        for parity, (x, y) in PARITIES.items():
            observed[parity] += int(np.count_nonzero((xy % 2 == (x, y)).all(axis=1)))
        xy = xy[keep]
        transforms = {model: np.eye(3) for model in MODELS}
        if i:
            record = by_name[row["member"]]
            for model in MODELS[1:]:
                transform = np.array(record[model])
                assert np.array_equal(transform[2], [0, 0, 1])
                for landmark in record["validationLandmarks"]:
                    np.testing.assert_allclose(
                        (transform @ [*landmark["reference"], 1])[:2], landmark[model], atol=1e-9, rtol=0
                    )
                corners = np.array([[0, 0], [maximum[0], 0], [0, maximum[1]], maximum])
                forward_delta = corners @ transform[:2, :2].T + transform[:2, 2] - corners
                assert np.abs(forward_delta).max() < margin - minimum
                transforms[model] = transform
        positions = {m: project(xy, transforms[m], np) for m in MODELS}
        inside = np.logical_and.reduce(
            [((value >= margin) & (value <= maximum - margin)).all(axis=1) for value in positions.values()]
        )
        excluded_edges += len(xy) - int(np.count_nonzero(inside))
        frames.append({
            parity: {
                model: positions[model][inside & (xy % 2 == (x, y)).all(axis=1)]
                for model in MODELS
            }
            for parity, (x, y) in PARITIES.items()
        })
    assert all(observed[b] == prior["bands"][b]["clippedLightEvents"]["allSites"] for b in PARITIES)

    radii = p["radii"]
    summary = {m: [0] * len(radii) for m in MODELS}
    summary_by_parity = {
        b: {"opportunities": 0, "hits": {m: [0] * len(radii) for m in MODELS}} for b in PARITIES
    }
    pairs = []
    total = 0
    for i, first in enumerate(frames):
        for j in range(i+1, len(frames)):
            second = frames[j]
            bands = {}
            for parity in PARITIES:
                n = len(first[parity]["detector"]) + len(second[parity]["detector"])
                hits = {}
                for model in MODELS:
                    left, right = first[parity][model], second[parity][model]
                    forward, backward = nearest_counts(left, right, radii), nearest_counts(right, left, radii)
                    hits[model] = [a+b for a,b in zip(forward, backward, strict=True)]
                    for ir, value in enumerate(hits[model]):
                        summary[model][ir] += value
                        summary_by_parity[parity]["hits"][model][ir] += value
                summary_by_parity[parity]["opportunities"] += n
                total += n
                bands[parity] = {"opportunities": n, "hits": hits}
            pairs.append({"first": lights[i]["sha256"], "second": lights[j]["sha256"], "bands": bands})
    assert len(pairs) == 105 and total == 14 * (sum(observed.values()) - 15 - excluded_edges)
    report = {"schema": "BKL046_M8M20_CLIP_COORDINATE_COMPARISON_RESULT_V1",
              "programSha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "protocolSha256": sha256(raw).hexdigest(), "matchingRadiiPx": radii,
              "excludedDarkCeilingEvents": 15, "excludedEdgeEvents": excluded_edges,
              "opportunities": total, "hits": summary, "byParity": summary_by_parity,
              "pairs": pairs, "nativeExecutions": 0, "scientificClosures": 0}
    with a.report.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
