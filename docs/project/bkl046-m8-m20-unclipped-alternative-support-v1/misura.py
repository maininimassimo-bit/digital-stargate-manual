"""Measure observed alternatives to clipped CFA events without interpolating samples."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import runpy
import sys
from zipfile import ZipFile


def read_frames(np, fits, path, rows, name_key, date_key, kind):
    with ZipFile(path) as archive:
        for row in rows:
            data = archive.read(row[name_key])
            assert sha256(data).hexdigest() == row["sha256"]
            with fits.open(BytesIO(data), memmap=False, uint=True) as hdus:
                h = hdus[0].header
                assert h["DATE-OBS"] == row[date_key] and h["IMAGETYP"] == kind
                assert h["BITPIX"] == 16 and h["BSCALE"] == 1 and h["BZERO"] == 32768
                assert h["BAYERPAT"] == "RGGB" and h["EXPTIME"] == 180 and h["GAIN"] == 100
                image = hdus[0].data
                assert image.dtype == np.uint16 and image.shape == (4176, 6248)
                yield image


def transform(points, matrix):
    return points @ matrix[:2, :2].T + matrix[:2, 2]


def nearest(np, projected, parity):
    xy = 2 * np.floor((projected - parity) / 2 + 0.5).astype(int) + parity
    return xy, np.sum((projected - xy) ** 2, axis=1)


def main():
    cli = argparse.ArgumentParser()
    for name in ("protocol", "sourceKit", "lightArchive", "lightReceipt", "darkArchive", "dependencies", "report"):
        cli.add_argument(name, type=Path)
    a = cli.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    kit = a.sourceKit
    def sha(path):
        with path.open("rb") as f:
            return file_digest(f, "sha256").hexdigest()

    source_program = kit / "misura.py"
    assert sha(source_program) == p["coordinateProgramSha256"]
    source = runpy.run_path(str(source_program))
    pinned = source["pinned_json"]
    prior = pinned(kit / "riscontro.json", p["coordinateReportSha256"])
    old = pinned(kit / "protocollo.json", prior["protocolSha256"])
    geo = pinned(kit / "geometria-riscontro.json", old["geometry"])
    darks = pinned(kit / "calibratori-riscontro.json", old["darkReceipt"])["sourceMembers"]["dark"]
    lights = pinned(a.lightReceipt, old["lightReceipt"])["rows"]
    assert len(lights) == len(darks) == 15
    assert sha(a.lightArchive) == old["lightArchive"] and sha(a.darkArchive) == old["darkArchive"]
    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    grid, sq = nearest(np, np.array([[1.0, 2.01], [1.99, 3.0]]), np.array([[0, 0], [1, 0]]))
    assert grid.tolist() == [[2, 2], [1, 4]] and (sq >= 1).all()
    models = source["MODELS"]
    by_name = {row["member"]: row for row in geo["referenceToInputAffine"]}
    assert set(by_name) == {row["member"] for row in lights[1:]}
    dark = next(read_frames(np, fits, a.darkArchive, darks[:1], "file", "date", "Dark"))
    defect, = np.argwhere(dark == 65535)[:, ::-1]
    del dark
    maximum = np.array(geo["imageShapeXY"]) - 1
    margin = old["margin"]
    forward, frames = [], []
    for i, image in enumerate(read_frames(np, fits, a.lightArchive, lights, "member", "dateObs", "Light")):
        xy = np.argwhere(image == 65535)[:, ::-1]
        kept = (xy != defect).any(axis=1)
        assert len(xy) - np.count_nonzero(kept) == 1
        xy = xy[kept]
        matrices = {m: np.eye(3) for m in models}
        if i:
            for m in models[1:]:
                matrices[m] = np.array(by_name[lights[i]["member"]][m])
        forward.append(matrices)
        positions = {m: transform(xy, np.linalg.inv(matrices[m])) for m in models}
        inside = np.logical_and.reduce([
            ((v >= margin) & (v <= maximum - margin)).all(axis=1) for v in positions.values()
        ])
        frames.append((xy[inside], {m: v[inside] for m, v in positions.items()}))
    counts_by_frame = [len(xy) for xy, _ in frames]
    assert sum(counts_by_frame) * 14 == prior["opportunities"]

    # The consensus requires the same actual target sample under both affine estimates.
    kinds = (*models, "affineConsensus")
    radii, thresholds = p["radii"], p["thresholds"]
    keys = [(k, r, t) for k in kinds for r in radii for t in thresholds]
    counts = [{key: np.zeros(len(xy), np.uint8) for key in keys} for xy, _ in frames]
    for j, image in enumerate(read_frames(np, fits, a.lightArchive, lights, "member", "dateObs", "Light")):
        for i, (xy, positions) in enumerate(frames):
            if i == j:
                continue
            grid, distances, values = {}, {}, {}
            for m in models:
                grid[m], distances[m] = nearest(np, transform(positions[m], forward[j][m]), xy % 2)
                assert ((grid[m] >= 0) & (grid[m] <= maximum)).all()
                values[m] = image[grid[m][:, 1], grid[m][:, 0]]
            same = (grid["binned"] == grid["mosaic"]).all(axis=1)
            for m, radius, threshold in keys:
                chosen = "binned" if m == "affineConsensus" else m
                usable = (distances[chosen] <= radius**2) & (values[chosen] < threshold)
                usable &= (grid[chosen] != defect).any(axis=1)
                if m == "affineConsensus":
                    usable &= same & (distances["mosaic"] <= radius**2)
                counts[i][m, radius, threshold] += usable

    by_parity = {}
    for band, phase in source["PARITIES"].items():
        mask = [(xy % 2 == phase).all(axis=1) for xy, _ in frames]
        rows = []
        for model, radius, threshold in keys:
            histogram = sum(
                (np.bincount(results[model, radius, threshold][selected], minlength=15)
                 for results, selected in zip(counts, mask, strict=True)),
                start=np.zeros(15, np.int64),
            )
            rows.append({"model": model, "radius": radius, "upperCodeExclusive": threshold,
                         "eventsByNumberOfAlternatives": histogram.tolist()})
        by_parity[band] = rows
    totals = []
    for index, key in enumerate(keys):
        hist = [sum(row[index]["eventsByNumberOfAlternatives"][n] for row in by_parity.values())
                for n in range(15)]
        assert sum(hist) == sum(counts_by_frame)
        model, radius, threshold = key
        totals.append({"model": model, "radius": radius, "upperCodeExclusive": threshold,
                       "eventsByNumberOfAlternatives": hist,
                       "atLeastOne": sum(hist[1:]), "atLeastThree": sum(hist[3:])})
    for radius in radii:
        for threshold in thresholds:
            for frame in counts:
                consensus = frame["affineConsensus", radius, threshold]
                assert (consensus <= frame["binned", radius, threshold]).all()
                assert (consensus <= frame["mosaic", radius, threshold]).all()
    output = {"schema": "BKL046_M8M20_UNCLIPPED_ALTERNATIVES_RESULT_V1",
              "protocolSha256": sha256(raw).hexdigest(), "programSha256": sha(Path(__file__)),
              "targetFramesPerEvent": 14, "sourceFrames": 15,
              "clippedEventsCompared": sum(counts_by_frame), "countsBySourceFrame": counts_by_frame,
              "totals": totals, "byParity": by_parity, "photometricRecoveryVerified": False,
              "nativeExecutions": 0, "scientificClosures": 0}
    with a.report.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(output, out, indent=2, sort_keys=True, allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
