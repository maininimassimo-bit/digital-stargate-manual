"""Assess split sensitivity of the frozen M8/M20 detector-anchor measurements."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from math import fsum
from pathlib import Path
from statistics import mean, quantiles


def read_pinned(path, expected):
    data = path.read_bytes()
    assert sha256(data).hexdigest() == expected, path.name
    return json.loads(data)


def model(positions, deltas):
    # Complete rectangular layout makes the centered x/y columns orthogonal.
    x, y = zip(*positions, strict=True)
    x0, y0 = mean(x), mean(y)
    dx, dy = [v - x0 for v in x], [v - y0 for v in y]
    assert abs(fsum(a * b for a, b in zip(dx, dy, strict=True))) < 1e-14
    bx = fsum(a * b for a, b in zip(dx, deltas, strict=True)) / fsum(v * v for v in dx)
    by = fsum(a * b for a, b in zip(dy, deltas, strict=True)) / fsum(v * v for v in dy)
    offset = mean(deltas) - bx * x0 - by * y0
    result = [offset, bx, by]
    extreme = max(abs(offset + bx * x + by * y) for x, y in product((-1, 1), repeat=2))
    return result, extreme


def contrast(matrix, left, positions):
    right = sorted(set(range(len(matrix))) - set(left))
    a, b = [list(zip(*(matrix[i] for i in half), strict=True)) for half in (left, right)]
    deltas = [mean(y) - mean(x) for x, y in zip(a, b, strict=True)]
    coeff, extreme = model(positions, deltas)
    return {"maxAnchorDifferenceAdu": max(map(abs, deltas)), "maxPlaneCornerAdu": extreme,
            "planeAdu": coeff, "deltasAdu": deltas}


def distribution(rows):
    result = {}
    for metric in ("maxAnchorDifferenceAdu", "maxPlaneCornerAdu"):
        values = sorted(row[metric] for row in rows)
        q = quantiles(values, n=100, method="inclusive")
        result[metric] = {"minimum": values[0], "p05": q[4], "median": q[49],
                          "p95": q[94], "maximum": values[-1]}
    return result


def run(plan, baseline):
    positions = baseline["anchorCells"]
    frames = baseline["measurements"]
    assert len(frames) == 14 and baseline["heldOutDarkFrames"] == 1
    assert len({r["sourceSha256"] for r in frames}) == 14
    assert len(positions) == 6 and set(map(tuple, positions)) == set(product(
        sorted({r[0] for r in positions}), sorted({r[1] for r in positions})))
    known = [1.0, 2.0, -3.0]
    control = [known[0] + known[1] * x + known[2] * y for x, y in positions]
    found, extreme = model(positions, control)
    assert max(abs(a - b) for a, b in zip(known, found, strict=True)) < 1e-12
    assert abs(extreme - 6.0) < 1e-12
    all_splits = [(0, *pair) for pair in combinations(range(1, 14), 6)]
    matched = [(0, *(2 * j + parity for j, parity in enumerate(flags, 1)))
               for flags in product((0, 1), repeat=6)]
    assert len(all_splits) == plan["allPartitions"] and len(matched) == plan["adjacentPairedPartitions"]
    assert set(matched).issubset(all_splits)
    original = tuple(range(0, 14, 2))
    chronological = tuple(range(7))
    assert original in matched and chronological not in matched
    report = {}
    full = {}
    for stat in ("mean", "median"):
        matrix = [[cell[stat] for cell in frame["values"]] for frame in frames]
        values = {split: contrast(matrix, split, positions) for split in all_splits}
        historic = baseline["differences"][stat]
        assert abs(values[original]["maxAnchorDifferenceAdu"] - historic["maxAbsoluteAdu"]) < 1e-10
        assert max(abs(a - b) for a, b in zip(values[original]["planeAdu"],
                                              historic["planeCoefficientsAdu"], strict=True)) < 1e-10
        report[stat] = {"all": distribution(values.values()), "adjacentPaired": distribution(
            [values[split] for split in matched]), "originalInterleaved": values[original],
            "chronological": values[chronological]}
        full[stat] = [{"firstHalf": split, **row} for split, row in values.items()]
    return report, full


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "source_report", "receipt", "full"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    plan = json.loads(args.protocol.read_bytes())
    baseline = read_pinned(args.source_report, plan["priorReportSha256"])
    report, full = run(plan, baseline)
    data = (json.dumps(full, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()
    with args.full.open("xb") as stream:
        stream.write(data)
    doc = {"schema": "BKL046_DARK_SPLIT_SENSITIVITY_V1", "inputDarkFrames": 14, "heldOutDarkFrames": 1,
           "additionalDarkFrames": 0, "independentOpticalAnchors": 0, "nativeExecutions": 0,
           "scientificClosures": 0, "protocolSha256": sha256(args.protocol.read_bytes()).hexdigest(),
           "programSha256": sha256(Path(__file__).read_bytes()).hexdigest(),
           "fullReportSha256": sha256(data).hexdigest(), "outcomes": report}
    with args.receipt.open("xb") as stream:
        stream.write((json.dumps(doc, sort_keys=True, indent=2, allow_nan=False) + "\n").encode())


if __name__ == "__main__":
    main()
