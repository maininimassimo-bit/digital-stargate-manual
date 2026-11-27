from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys

parser = ArgumentParser()
parser.add_argument("inputs", type=Path)
parser.add_argument("packages", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

PLAN_PIN = "08c9fdda135892b70aefbd74bb9c4b6f0c2128279266ca3cb381fcd174114916"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def load(name, pin):
    data = (args.inputs / name).read_bytes()
    require(sha256(data).hexdigest() == pin, f"Changed input: {name}")
    return json.loads(data)


plan = load("protocollo.json", PLAN_PIN)
pins = plan["inputs"]
joined = load("gaia.json", pins["joinedGaia"])
responses = load("passband.json", pins["passband"])
require(responses["inputSha256"]["prior"] == pins["joinedGaia"], "Optical proxies use a different cohort")
output = {}
for field, flux_key in (("IC1805", "canonFlux"), ("M8M20", "zwoFlux")):
    flux_raw = load(flux_key + ".json", pins[flux_key])
    rows = {item["id"]: item for item in flux_raw["rows"]}
    measurements = joined[field]["rows"]
    optical = responses["fields"][field]
    predictors = {item["sourceId"]: item for item in optical["perStar"]}
    require(len(measurements) == len({item["sourceId"] for item in measurements}) == len(predictors),
            "Spectral cohort is not a one-to-one join")
    fit = np.array([row["fit"] for row in measurements], dtype=bool)
    require(fit.sum() == optical["train"] and (~fit).sum() == optical["test"], "Changed train and test split")
    flux = np.array([rows[row["rawId"]]["linearFluxAdu"] for row in measurements], dtype=np.float64)
    require(flux.shape == (len(measurements), 4, 3, 2, 2) and np.isfinite(flux).all() and (flux > 0).all(),
            "Unexpected parity photometry")
    require(all(row["fit"] == rows[row["rawId"]]["fit"] == predictors[row["sourceId"]]["fit"]
                for row in measurements), "Conflicting split flags")

    colors = {}
    for pattern, (blue, red) in plan["blueAndRedIndexes"].items():
        colors[pattern] = -2.5 * np.log10(flux[:, blue, :, :, plan["radiiIndex"]] /
                                          flux[:, red, :, :, plan["radiiIndex"]])
    archived = np.asarray([row["instrumentalBminusR6"] for row in measurements])
    np.testing.assert_allclose(colors["RGGB"], archived, atol=1e-12, rtol=0)
    cases = []
    for model in plan["models"][field]:
        predicted = np.asarray([predictors[row["sourceId"]]["colors"][model] for row in measurements])
        for i, method in enumerate(plan["methods"]):
            offsets = {}
            errors = {}
            for pattern, color in colors.items():
                offsets[pattern] = float(np.median(color[fit, i, 0] - predicted[fit]))
                errors[pattern] = color[~fit, i] - (predicted[~fit] + offsets[pattern])[:, None]
            p90 = {pattern: np.quantile(np.abs(values), .9, axis=0)
                   for pattern, values in errors.items()}
            np.testing.assert_allclose(p90["RGGB"], optical["metrics"][method][model]["p90Abs"],
                                       atol=1e-12, rtol=0)
            for j, calibration in enumerate(plan["calibrations"]):
                rank = sorted(p90, key=lambda k: (p90[k][j], k))
                winner, next_pattern = rank[:2]
                gap = float(p90[next_pattern][j] - p90[winner][j])
                per_star = [dict(
                    sourceId=row["sourceId"],
                    residualMag={pattern: float(values[k, j]) for pattern, values in errors.items()},
                ) for k, row in enumerate(np.asarray(measurements, dtype=object)[~fit])]
                cases.append(dict(model=model, method=method, calibration=calibration,
                                  p90={pattern: float(p90[pattern][j]) for pattern in rank},
                                  offsetA=offsets, winner=winner, runnerUp=next_pattern,
                                  runnerUpGapMag=gap, heldout=per_star))
    output[field] = dict(train=int(fit.sum()), heldOut=int((~fit).sum()), trials=cases,
                         winners={pattern: sum(trial["winner"] == pattern for trial in cases) for pattern in colors},
                         minimumGapMag=min(case["runnerUpGapMag"] for case in cases))
report = dict(schema=plan["schema"], protocolSha256=PLAN_PIN, nominalColorReproduced=True,
              priorP90Reproduced=True, fields=output, physicalRowOrderVerified=False,
              independentConfirmatoryStudy=False, nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf8", newline="\n") as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write("\n")
