"""Develop interval and sample-size checks under synthetic paired field effects."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("campaign", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

assert np.__version__ == "2.3.5"
PLAN = "4392df161ab0c8f4075a6f83ce6e65160b5caf970b41b84898a33c16ba42433b"
raw = args.campaign.read_bytes()
assert sha256(raw).hexdigest() == PLAN
plan = json.loads(raw)
assert plan["dataPartitions"]["development"]["seedNamespace"] == "DSG_PI_DEV_V2"
assert "Independent repeat sample sizing/power and interval coverage before calibration." in plan["remainingDevelopmentRequirements"]

# NIST table, 0.975 column, degrees of freedom equal to fields minus one.
CRITICAL = {8: 2.365, 16: 2.131, 31: 2.042, 61: 2.000, 101: 1.984}
SOURCES = 16
TRIALS = 4096
EFFECTS = (0.0, 0.2, 0.4, 0.8)
MODES = (
    ("independent_normal", 0.0),
    ("clustered_normal", 0.25),
    ("clustered_skew", 0.25),
    ("clustered_strong_skew", 0.50),
)
REPEATS = ("development-A", "development-B")


def seed_for(mode, fields, repeat):
    identity = f"DSG_PI_DEV_V2/paired-intervals/{mode}/{fields}/{repeat}"
    return identity, int.from_bytes(sha256(identity.encode()).digest()[:8], "big")


def simulate(mode, correlation, fields, repeat):
    identity, seed = seed_for(mode, fields, repeat)
    rng = np.random.Generator(np.random.PCG64(seed))
    if mode.endswith("skew"):
        shared = rng.exponential(size=(TRIALS, fields, 1)) - 1
    else:
        shared = rng.standard_normal(size=(TRIALS, fields, 1))
    source = rng.standard_normal(size=(TRIALS, fields, SOURCES))
    differences = np.sqrt(1-correlation) * source + np.sqrt(correlation) * shared
    by_field = differences.mean(axis=2)
    means = by_field.mean(axis=1)
    field_sd = np.sqrt(correlation + (1-correlation)/SOURCES)
    half_field = CRITICAL[fields] * by_field.std(axis=1, ddof=1) / np.sqrt(fields)
    half_naive = 1.96 * differences.reshape(TRIALS, -1).std(axis=1, ddof=1) / np.sqrt(fields*SOURCES)
    evaluations = []
    for label, half in (("field_t", half_field), ("naive_source_normal", half_naive)):
        hits = int(np.sum(np.abs(means) <= half))
        rejections = [int(np.sum(np.abs(means + effect * field_sd) > half)) for effect in EFFECTS]
        assert rejections[0] == TRIALS - hits
        evaluations.append(dict(method=label, covered=hits, coverFraction=hits/TRIALS,
                                medianHalfWidthFieldSd=float(np.median(half))/field_sd,
                                rejectionCounts=rejections))
    return dict(scenario=mode, sourceIntraclassCorrelation=correlation, fields=fields,
                replicate=repeat, seedNamespace=identity, seed=str(seed), trials=TRIALS,
                effectsInFieldMeanSd=EFFECTS, measurements=evaluations)


results = [simulate(name, rho, fields, rep) for name, rho in MODES
           for fields in CRITICAL for rep in REPEATS]
assert len({row["seed"] for row in results}) == len(results)
report = dict(protocol="BKL046_PAIRED_FIELD_INTERVAL_DEVELOPMENT_V1",
              scientificPlanSha256=PLAN, numpy=np.__version__, generator="PCG64",
              partition="DEVELOPMENT_ONLY", sourcesPerField=SOURCES,
              criticalTByIndependentFieldCount=CRITICAL, rows=results,
              calibrationOrVerificationSeedsConsumed=False, scientificThresholdsSet=False,
              scientificClosures=0, nativeExecutions=0)
with args.output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write("\n")
