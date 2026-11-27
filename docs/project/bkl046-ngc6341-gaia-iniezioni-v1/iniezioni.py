import argparse
from collections import Counter
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
KINDS = ("offset_0_25", "offset_0_75", "offset_1_25", "duplicate_detections", "source_absent_decoy", "coincident_decoy")
RADII = (0.5, 1.0, 1.5, 2.0)
rows = []


def pinned(path, expected):
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected, path.name
    return data


def inject(exposure, chip, shape, catalogue):
    height, width = shape
    assert np.isfinite(catalogue).all()
    tile_edges = np.mod(catalogue, 256)
    safe = np.all((catalogue >= 12) & (catalogue < np.array([width, height]) - 12), axis=1)
    safe &= np.all((tile_edges >= 12) & (tile_edges < 244), axis=1)
    safe &= instrumented["parity"](np, catalogue)
    coordinates = []
    truths = []
    labels = []
    candidates = np.flatnonzero(safe)
    assert len(candidates) >= 20
    for ordinal, index in enumerate(candidates):
        kind = KINDS[ordinal % len(KINDS)]
        theta = (ordinal * 137 % 360) * np.pi / 180
        direction = np.array([np.cos(theta), np.sin(theta)])
        magnitude = (0.25, 0.75, 1.25, 0.30, 8.0, 0.20)[ordinal % len(KINDS)]
        source = catalogue[index]
        offsets = (magnitude, -magnitude) if kind == "duplicate_detections" else (magnitude,)
        for offset in offsets:
            coordinates.append(source + offset * direction)
            truths.append(-1 if kind in ("source_absent_decoy", "coincident_decoy") else index)
            labels.append(kind)

    observed = np.asarray(coordinates)
    assert instrumented["parity"](np, observed).all()
    results = []
    for radius in RADII:
        i, j, _ = instrumented["pair"](np, observed, catalogue, radius)
        assert len(i) == len(set(i)) == len(set(j))
        matched = dict(zip(i.tolist(), j.tolist(), strict=True))
        counts = {kind: Counter() for kind in KINDS}
        duplicate_correct_sources = set()
        for k, (truth, kind) in enumerate(zip(truths, labels, strict=True)):
            if k not in matched:
                outcome = "unmatched"
            elif matched[k] == truth:
                outcome = "correct"
                if kind == "duplicate_detections":
                    duplicate_correct_sources.add(int(truth))
            elif truth == -1:
                outcome = "accepted_decoy"
            else:
                outcome = "wrong_identity"
            counts[kind][outcome] += 1
        assert sum(sum(x.values()) for x in counts.values()) == len(observed)
        results.append(dict(radiusPx=radius, byCase={k:dict(v) for k,v in counts.items()},
                            duplicateTruthSourcesRecovered=len(duplicate_correct_sources)))
    rows.append(dict(exposure=exposure, chip=chip, predictedSourcesInOriginalPilot=len(catalogue),
                     injectedSourceSites=len(candidates), simulatedDetections=len(observed),
                     casesByRadius=results))


source = pinned(args.pilot, PILOT).decode("utf-8")
anchor = '                by_chip[str(science.header["CCDCHIP"])] = dict('
assert source.count(anchor) == 1
source = source.replace(anchor,
    "                INJECT(exposure, science.header['CCDCHIP'], science.data.shape, aligned)\n" + anchor)
instrumented = {"__name__": "instrumented_pilot", "__file__": str(args.pilot), "INJECT": inject}
exec(compile(source, str(args.pilot), "exec"), instrumented)
assert instrumented["main"](args.inputs, args.historical) == json.loads(pinned(args.expected, EXPECTED))
assert len(rows) == 4
report = dict(protocol="BKL046_NGC6341_GAIA_MATCHER_SYNTHETIC_TRUTH_V1", pilotSha256=PILOT,
              originalReportSha256=EXPECTED, originalReportReproduced=True,
              simulatedCentroids=True, realCalibratedCatalogueGeometry=True,
              simulatedPixelImages=False, catalogueRefittedToInjections=False,
              nativeExecutions=0, scientificClosures=0, results=rows)
with args.output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write("\n")
