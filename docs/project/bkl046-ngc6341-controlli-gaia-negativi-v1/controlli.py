import argparse
import hashlib
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("pilot", "expected", "inputs", "historical", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))

import astropy
import numpy as np

assert (astropy.__version__, np.__version__) == ("7.2.0", "2.3.5")
PILOT = "3d04b697eda86b3dfbd787172d4b5099f6c2334a4680f4899c1fb221e8883186"
EXPECTED = "b4402ddb36b9c9ecd8bb04f8491bba961c63032809abff7581f8c108dd1ed64c"
RADII = (0.5, 0.75, 1.0, 1.5, 2.0)
OFFSET_NORMS = (8, 16, 32)
DIRECTIONS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
rows = []


def pinned(path, digest):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError(f"Input changed: {path.name}")
    return raw


def matched(held, catalogue, radius):
    i, j, _ = instrumented["pair"](np, held, catalogue, radius)
    assert len(i) == len(set(i)) == len(set(j))
    return dict(zip(map(int, i), map(int, j), strict=True))


def control(exposure, chip, held, aligned, ids):
    reference = matched(held, aligned, 1.0)
    assert list(reference) == list(ids)
    radius_results = []
    for radius in RADII:
        variant = matched(held, aligned, radius)
        same = sum(variant[key] == reference[key] for key in variant.keys() & reference.keys())
        swapped = len(variant.keys() & reference.keys()) - same
        radius_results.append(dict(radiusPx=radius, accepted=len(variant),
                                   sameAsReference=same, differentIdentity=swapped,
                                   lostReference=len(reference.keys() - variant.keys()),
                                   additionalCentroids=len(variant.keys() - reference.keys())))
    controls = []
    for norm in OFFSET_NORMS:
        for x, y in DIRECTIONS:
            delta = np.asarray((x, y)) * norm / np.hypot(x, y)
            assert np.isclose(np.linalg.norm(delta), norm) and norm > 2
            variant = matched(held, aligned + delta, 1.0)
            same = sum(variant[key] == reference[key] for key in variant.keys() & reference.keys())
            assert same == 0
            controls.append(dict(normPx=norm, direction=[x, y], accepted=len(variant),
                                 reusedCentroids=len(variant.keys() & reference.keys())))
    counts = [c["accepted"] for c in controls]
    rows.append(dict(exposure=exposure, chip=chip, heldCentroids=len(held),
                     referenceAccepted=len(reference), radiusSensitivity=radius_results,
                     shiftedControls=controls, shiftAcceptedMinimum=min(counts),
                     shiftAcceptedMedian=float(np.median(counts)), shiftAcceptedMaximum=max(counts)))


source = pinned(args.pilot, PILOT).decode("utf-8")
anchor = '                by_chip[str(science.header["CCDCHIP"])] = dict('
assert source.count(anchor) == 1
source = source.replace(anchor,
    "                CONTROL(exposure, science.header['CCDCHIP'], held, aligned, ids)\n" + anchor)
instrumented = {"__name__": "instrumented_pilot", "__file__": str(args.pilot), "CONTROL": control}
exec(compile(source, str(args.pilot), "exec"), instrumented)
assert instrumented["main"](args.inputs, args.historical) == json.loads(pinned(args.expected, EXPECTED))
assert len(rows) == 4 and all(len(x["shiftedControls"]) == 24 for x in rows)
result = dict(protocol="BKL046_NGC6341_HELD_GAIA_NEGATIVE_SHIFTS_V1",
              originalReportReproduced=True, pilotSha256=PILOT, originalReportSha256=EXPECTED,
              epochAndCalibrationFixed=True, rowwiseShiftRefit=False,
              radiusReferencePx=1.0, shiftNormsPx=list(OFFSET_NORMS), rows=rows,
              falsePositiveRateEstimated=False, completenessEstimated=False,
              nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf-8", newline="\n") as out:
    json.dump(result, out, indent=2, allow_nan=False)
    out.write("\n")
