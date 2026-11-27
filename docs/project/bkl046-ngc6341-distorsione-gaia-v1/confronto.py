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
pilot_sha = "3d04b697eda86b3dfbd787172d4b5099f6c2334a4680f4899c1fb221e8883186"
report_sha = "b4402ddb36b9c9ecd8bb04f8491bba961c63032809abff7581f8c108dd1ed64c"


def pinned(path, digest):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError(f"Input changed: {path.name}")
    return data


def stats(distance):
    assert len(distance) and np.isfinite(distance).all()
    return dict(count=len(distance), medianPx=float(np.median(distance)),
                p90Px=float(np.quantile(distance, 0.90)), maximumPx=float(distance.max()),
                atMost1Px=int(np.count_nonzero(distance <= 1)))


training_state = {}
rows = []


def record_training(measured, predicted, obs_index, pred_index, kept):
    assert not training_state
    training_state.update(points=measured[obs_index[kept]],
                          candidateIndices=pred_index[kept],
                          reference=predicted[pred_index[kept]])


def compare(exposure, chip, wcs, catalog_world, training, seeds, held, aligned, ids):
    points = training_state.pop("points")
    indices = training_state.pop("candidateIndices")
    reference = training_state.pop("reference")
    assert np.array_equal(reference, seeds[indices])
    assert set(map(tuple, points)) <= set(map(tuple, training))
    distorted_ids, partners, distances = module["pair"](np, held, aligned, 1.0)
    assert np.array_equal(ids, distorted_ids)
    assert not set(indices) & set(partners)
    linear = wcs.wcs_world2pix(catalog_world, 0, ra_dec_order=True)
    assert np.isfinite(linear[np.r_[indices, partners]]).all()
    origin = linear[indices].mean(axis=0)

    def basis(pixel):
        return np.column_stack(((pixel - origin) / 2048, np.ones(len(pixel))))

    fitted, _, rank, _ = np.linalg.lstsq(basis(linear[indices]), points, rcond=None)
    assert rank == 3
    train_error = np.linalg.norm(basis(linear[indices]) @ fitted - points, axis=1)
    absent_error = np.linalg.norm(basis(linear[partners]) @ fitted - held[ids], axis=1)
    rows.append(dict(exposure=exposure, chip=chip, fixedTrainingPairs=len(indices),
                     heldCentroidsInOriginalCohort=len(held), fixedIdentities=len(ids),
                     originalDistortionRetained=stats(distances),
                     distortionOmittedWithRefit=stats(absent_error),
                     distortionOmittedTrainingResidual=stats(train_error)))


source = pinned(args.pilot, pilot_sha).decode("utf-8")
edits = [
    ("    return fitted, dict(candidatePairs=len(i),",
     "    RECORD_TRAINING(observed, predicted, i, j, keep)\n"
     "    return fitted, dict(candidatePairs=len(i),"),
    ("                by_chip[str(science.header[\"CCDCHIP\"])] = dict(",
     "                COMPARE(exposure, science.header['CCDCHIP'], wcs, world[bounds], "
     "training, seeds, held, aligned, ids)\n"
     "                by_chip[str(science.header[\"CCDCHIP\"])] = dict("),
]
for original, instrumented in edits:
    assert source.count(original) == 1
    source = source.replace(original, instrumented)
module = {"__name__": "instrumented_pilot", "__file__": str(args.pilot),
          "RECORD_TRAINING": record_training, "COMPARE": compare}
exec(compile(source, str(args.pilot), "exec"), module)
result = module["main"](args.inputs, args.historical)
assert result == json.loads(pinned(args.expected, report_sha))
assert len(rows) == 4 and not training_state
report = dict(protocol="BKL046_NGC6341_DISTORTION_OMISSION_FIXED_GAIA_IDENTITIES_V1",
              pilotSha256=pilot_sha, originalReportSha256=report_sha,
              originalReportReproduced=True, trainingPartition="even 256 px tiles",
              holdoutPartition="odd 256 px tiles",
              holdoutScope="Original mutual unambiguous <=1 px matches with distortion retained",
              trainingStrategy="Reused original inliers and fit affine output from core-only WCS",
              heldIdentitiesRematched=False, rows=rows, scientificClosures=0,
              nativeExecutions=0)
with args.output.open("x", encoding="utf-8", newline="\n") as out:
    json.dump(report, out, indent=2, allow_nan=False)
    out.write("\n")
