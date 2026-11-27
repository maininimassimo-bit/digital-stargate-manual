"""Score leave-one-exposure-out recovery of artificially censored raw CFA codes."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import runpy
import sys


def sha(path):
    with path.open("rb") as data:
        return file_digest(data, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "alternativeKit", "coordinateKit", "lightArchive",
                 "lightReceipt", "darkArchive", "dependencies", "report"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    assert sha(a.alternativeKit / "misura.py") == p["alternativeProgram"]
    alt = runpy.run_path(str(a.alternativeKit / "misura.py"))
    assert sha(a.alternativeKit / "riscontro.json") == p["alternativeReport"]
    alt_report = json.loads((a.alternativeKit / "riscontro.json").read_bytes())
    assert alt_report["programSha256"] == p["alternativeProgram"]
    assert sha(a.alternativeKit / "protocollo.json") == alt_report["protocolSha256"]
    controls = json.loads((a.alternativeKit / "protocollo.json").read_bytes())
    assert sha(a.coordinateKit / "misura.py") == controls["coordinateProgramSha256"]
    base = runpy.run_path(str(a.coordinateKit / "misura.py"))
    pinned = base["pinned_json"]
    origin = pinned(a.coordinateKit / "riscontro.json", controls["coordinateReportSha256"])
    frozen = pinned(a.coordinateKit / "protocollo.json", origin["protocolSha256"])
    geo = pinned(a.coordinateKit / "geometria-riscontro.json", frozen["geometry"])
    darks = pinned(a.coordinateKit / "calibratori-riscontro.json", frozen["darkReceipt"])["sourceMembers"]["dark"]
    lights = pinned(a.lightReceipt, frozen["lightReceipt"])["rows"]
    assert len(lights) == len(darks) == 15
    assert sha(a.lightArchive) == frozen["lightArchive"] and sha(a.darkArchive) == frozen["darkArchive"]

    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    read_frames, project, nearest = (alt[key] for key in ("read_frames", "transform", "nearest"))
    models = base["MODELS"]
    transforms = {row["member"]: row for row in geo["referenceToInputAffine"]}
    dark = next(read_frames(np, fits, a.darkArchive, darks[:1], "file", "date", "Dark"))
    defect, = np.argwhere(dark == 65535)[:, ::-1]
    del dark
    maximum = np.array(geo["imageShapeXY"]) - 1
    margin = frozen["margin"]
    low = p["censorCode"]
    high = p["targetRanges"][-1][-1]
    assert p["targetRanges"] == [[low, 50000], [50000, high]]

    forward, frames = [], []
    truth = []
    for index, image in enumerate(read_frames(np, fits, a.lightArchive, lights, "member", "dateObs", "Light")):
        xy = np.argwhere((image >= low) & (image < high))[:, ::-1]
        matrices = {m: np.eye(3) for m in models}
        if index:
            for m in models[1:]:
                matrices[m] = np.array(transforms[lights[index]["member"]][m])
        forward.append(matrices)
        positions = {m: project(xy, np.linalg.inv(matrices[m])) for m in models}
        inside = np.logical_and.reduce([
            ((v >= margin) & (v <= maximum - margin)).all(axis=1) for v in positions.values()
        ]) & (xy != defect).any(axis=1)
        xy = xy[inside]
        truth.append(image[xy[:, 1], xy[:, 0]].copy())
        frames.append((xy, {k: v[inside] for k, v in positions.items()}))

    designs = [("detector", 1)] + [("affineConsensus", x) for x in p["radii"]]
    samples = [{design: np.full((len(xy), len(lights)), np.nan, np.float32) for design in designs}
               for xy, _ in frames]
    for j, image in enumerate(read_frames(np, fits, a.lightArchive, lights, "member", "dateObs", "Light")):
        for i, (xy, positions) in enumerate(frames):
            if i == j:
                continue
            grids, distances = {}, {}
            for m in models:
                grids[m], distances[m] = nearest(np, project(positions[m], forward[j][m]), xy % 2)
                assert ((grids[m] >= 0) & (grids[m] <= maximum)).all()
            same = (grids["binned"] == grids["mosaic"]).all(axis=1)
            for design, radius in designs:
                axis = "binned" if design == "affineConsensus" else design
                grid = grids[axis]
                values = image[grid[:, 1], grid[:, 0]]
                use = (distances[axis] <= radius**2) & (values < p["candidateCodeExclusive"])
                use &= (grid != defect).any(axis=1)
                if design == "affineConsensus":
                    use &= same & (distances["mosaic"] <= radius**2)
                samples[i][design, radius][use, j] = values[use]

    groups = []
    for name, radius in designs:
        counts, predicted = [], []
        for i, saved in enumerate(samples):
            graph = saved[name, radius]
            assert np.isnan(graph[:, i]).all()
            n = np.count_nonzero(~np.isnan(graph), axis=1)
            estimates = np.full(len(n), np.nan)
            estimates[n > 0] = np.nanmedian(graph[n > 0], axis=1)
            counts.append(n)
            predicted.append(estimates)
        for first, last in p["targetRanges"]:
            for band, phase in (("all", None), *base["PARITIES"].items()):
                chosen = []
                for (xy, _), value in zip(frames, truth, strict=True):
                    mask = (value >= first) & (value < last)
                    if phase is not None:
                        mask &= (xy % 2 == phase).all(axis=1)
                    chosen.append(mask)
                for minimum in p["minimumOtherFrames"]:
                    errors, capped, frame_medians = [], [], []
                    for found, estimate, true, selected in zip(counts, predicted, truth, chosen, strict=True):
                        keep = selected & (found >= minimum)
                        ref = true[keep].astype(float)
                        delta = (estimate[keep] - ref) / ref
                        errors.extend(delta.tolist())
                        capped.extend(((low-ref)/ref).tolist())
                        if len(delta):
                            frame_medians.append(float(np.median(np.abs(delta))))
                    x = np.asarray(errors)
                    absolute = np.abs(x)
                    groups.append({
                        "model": name, "radius": radius, "minimumOtherFrames": minimum,
                        "range": [first, last], "parity": band,
                        "referenceEvents": sum(int(mask.sum()) for mask in chosen),
                        "eventsEstimated": len(x),
                        "withinFivePercent": int(np.count_nonzero(absolute <= p["descriptiveRelativeErrorLimit"])),
                        "improvedOverCensoredCode": int(np.count_nonzero(absolute < np.abs(capped))),
                        "medianSignedRelativeError": float(np.median(x)) if len(x) else None,
                        "medianAbsoluteRelativeError": float(np.median(absolute)) if len(x) else None,
                        "p90AbsoluteRelativeError": float(np.quantile(absolute, .9)) if len(x) else None,
                        "framesWithEstimates": len(frame_medians),
                        "frameMedianAbsoluteErrorRange": [min(frame_medians), max(frame_medians)] if frame_medians else None,
                    })
    for row in groups:
        assert 0 <= row["withinFivePercent"] <= row["eventsEstimated"] <= row["referenceEvents"]
    for row in (item for item in groups if item["parity"] == "all"):
        k = ("model", "radius", "minimumOtherFrames", "range")
        children = [v for v in groups if v["parity"] != "all" and all(v[i] == row[i] for i in k)]
        assert len(children) == 4
        for n in ("referenceEvents", "eventsEstimated", "withinFivePercent"):
            assert sum(v[n] for v in children) == row[n]
    report = {"schema": "BKL046_M8M20_HELDOUT_ARTIFICIAL_CENSORING_RESULT_V1",
              "programSha256": sha(Path(__file__)), "protocolSha256": sha256(raw).hexdigest(),
              "referenceFrames": len(lights), "targetEventsPerFrame": [len(x) for x in truth],
              "realClippingRecoveryVerified": False, "nativeExecutions": 0, "scientificClosures": 0,
              "groups": groups}
    with a.report.open("x", encoding="utf-8", newline="\n") as dst:
        json.dump(report, dst, indent=2, sort_keys=True, allow_nan=False)
        dst.write("\n")


if __name__ == "__main__":
    main()
