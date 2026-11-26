"""Compare field-level interval estimators on independent development repeats."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("prior", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

assert np.__version__ == "2.3.5"
PRIOR = "1b4edb8724a7bd79b021e65fd528f0ff05a6e744c4abc75d9e07a62bd2ecfb4d"
PLAN = "4392df161ab0c8f4075a6f83ce6e65160b5caf970b41b84898a33c16ba42433b"
raw = args.prior.read_bytes()
assert sha256(raw).hexdigest() == PRIOR
previous = json.loads(raw)
assert previous["scientificPlanSha256"] == PLAN and previous["partition"] == "DEVELOPMENT_ONLY"
critical = previous["criticalTByIndependentFieldCount"]
trials = 2048
draws = 511
scenarios = [
    ("clustered_normal", .25, 61),
    ("clustered_strong_skew", .50, 16),
    ("clustered_strong_skew", .50, 31),
    ("clustered_strong_skew", .50, 61),
    ("clustered_strong_skew", .50, 101),
]
effects = (0, .2, .4, .8)


def generator(identity):
    seed = int.from_bytes(sha256(identity.encode()).digest()[:8], "big")
    return str(seed), np.random.Generator(np.random.PCG64(seed))


def simulate(mode, rho, fields, repeat):
    label = f"DSG_PI_DEV_V2/bootstrap-fields-v1/{mode}/{fields}/{repeat}"
    data_seed, data_rng = generator(label + "/sample")
    bootstrap_seed, bootstrap_rng = generator(label + "/resample")
    if mode.endswith("skew"):
        shared = data_rng.exponential(size=(trials, fields)) - 1
    else:
        shared = data_rng.standard_normal(size=(trials, fields))
    data = np.sqrt(rho) * shared + np.sqrt((1-rho)/16) * data_rng.standard_normal((trials, fields))
    sample_mean = data.mean(axis=1)
    sem = data.std(axis=1, ddof=1) / np.sqrt(fields)
    field_sd = np.sqrt(rho + (1-rho)/16)
    offsets = float(critical[str(fields)]) * sem
    endpoints = {
        "field_t": np.column_stack((sample_mean-offsets, sample_mean+offsets)),
        "field_bootstrap_percentile": np.empty((trials, 2)),
        "field_bootstrap_studentized": np.empty((trials, 2)),
    }
    for start in range(0, trials, 16):
        end = min(start+16, trials)
        samples = data[start:end]
        indexes = bootstrap_rng.integers(fields, size=(len(samples), draws, fields))
        boot = samples[np.arange(len(samples))[:, None, None], indexes]
        means = boot.mean(axis=2)
        errors = boot.std(axis=2, ddof=1) / np.sqrt(fields)
        if not (errors > 0).all():
            raise ValueError("Degenerate bootstrap resample")
        bounds = np.quantile(means, (.025, .975), axis=1).T
        pivots = (means - sample_mean[start:end, None]) / errors
        qlow, qhigh = np.quantile(pivots, (.025, .975), axis=1)
        bounds_t = np.column_stack((sample_mean[start:end] - qhigh * sem[start:end],
                                    sample_mean[start:end] - qlow * sem[start:end]))
        endpoints["field_bootstrap_percentile"][start:end] = bounds
        endpoints["field_bootstrap_studentized"][start:end] = bounds_t

    coverage = {}
    results = {}
    for method, bounds in endpoints.items():
        lo, hi = bounds.T
        assert (lo <= hi).all() and np.isfinite(bounds).all()
        below_zero = hi < 0
        above_zero = lo > 0
        cover = ~(below_zero | above_zero)
        coverage[method] = cover
        reject = []
        for effect in effects:
            shift = effect * field_sd
            reject.append(int(((lo + shift > 0) | (hi + shift < 0)).sum()))
        assert reject[0] == trials-int(cover.sum())
        results[method] = dict(covered=int(cover.sum()), belowTruth=int(below_zero.sum()),
                               aboveTruth=int(above_zero.sum()), rejectionCounts=reject,
                               medianWidthFieldSd=float(np.median(hi-lo))/field_sd)

    studentized = coverage["field_bootstrap_studentized"]
    baseline = coverage["field_t"]
    return dict(mode=mode, rho=rho, fields=fields, repeat=repeat, sampleSeed=data_seed,
                resamplingSeed=bootstrap_seed, methods=results,
                pairedCoverageDiscordance=dict(studentizedOnly=int((studentized & ~baseline).sum()),
                                                fieldTOnly=int((baseline & ~studentized).sum())))


rows = [simulate(mode, rho, fields, repeat) for mode, rho, fields in scenarios for repeat in ("A", "B")]
assert len({row[key] for row in rows for key in ("sampleSeed", "resamplingSeed")}) == 2*len(rows)
report = dict(protocol="BKL046_FIELD_BOOTSTRAP_DEVELOPMENT_V1", priorReportSha256=PRIOR,
              scientificPlanSha256=PLAN, numpy=np.__version__, trialsPerRepeat=trials,
              resamplesPerTrial=draws, effectsInFieldStandardDeviation=effects,
              partition="DEVELOPMENT_ONLY", dataRows=rows,
              calibrationGatesFrozen=False, independentVerificationSeedsConsumed=False,
              scientificClosures=0, nativeExecutions=0)
with args.output.open("x", encoding="utf-8", newline="\n") as out:
    json.dump(report, out, indent=2, allow_nan=False)
    out.write("\n")
