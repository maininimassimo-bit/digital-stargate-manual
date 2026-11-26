import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import SimpleNamespace

parser = argparse.ArgumentParser()
for name in ("replay_bundle", "geometry", "candidates", "cohort", "packages", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

PINS = {
    "acs/paired_acs.py": "bf10145a6195a0e4e3773a326b42f248131e73cefe9ccbfe9b593e44bc27f915",
    "acs/riscontro.json": "fd0f4ca1cacd3a31299eb94d21145c9300bc7fc06eaa5c927b7ff8e5c32b6fe7",
    "gaia/paired_gaia.py": "87e0ee1eda3fad64c0a30e948b1602f3fdbabab4d5398a186f1d03ed289a6ddf",
    "gaia/riscontro-definitivo.json": "967776bea29bc659008d39b1821e668a1057043131023ec8b2bc908f7db31c78",
}
COHORT = "7f094328aee738a929a1c208eb90eeab37fbe78c6b46ed6204bcd7f393ac8c7b"


def pinned(path, digest):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError(f"Input changed: {path.name}")
    return raw


def module(name, edits=()):
    path = args.replay_bundle / name
    source = pinned(path, PINS[name]).decode("utf-8")
    for before, after in edits:
        assert source.count(before) == 1
        source = source.replace(before, after)
    scope = {"__name__": "verified_replay", "__file__": str(path), "PAIRS": {}}
    exec(compile(source, str(path), "exec"), scope)
    return scope


anchor = "    d = long_xy - short_xy"
acs = module("acs/paired_acs.py", (
    (anchor, anchor + "\n    PAIRS.update({k: (float(np.linalg.norm(v)), float(np.linalg.norm(s)))\n"
     "                  for k, v, s in zip(both, d, avg - old_xy, strict=True)})"),
    ("    return dict(schema=", "    EXTVER_CHIP.update({i: int(headers[i - 1]) for i in (1, 2)})\n"
     "    return dict(schema="),
    ('    with fits.open(args.geometry / frames[0], mode="readonly", memmap=True) as parent:',
     '    with fits.open(args.geometry / frames[0], mode="readonly", memmap=True) as parent:\n'
     '        headers = [parent["SCI", i].header["CCDCHIP"] for i in (1, 2)]'),
))
acs["EXTVER_CHIP"] = {}
bundle = args.replay_bundle
values = SimpleNamespace(pilot=bundle / "centroids/centroid_pilot.py",
                         receipt=bundle / "centroids/riscontro.json",
                         geometry=args.geometry, candidates=args.candidates,
                         historical=args.cohort, prior=bundle / "match/register_gaia.py")
acs_result = acs["main"](values)
assert acs_result == json.loads(pinned(bundle / "acs/riscontro.json", PINS["acs/riscontro.json"]))
gaia = module("gaia/paired_gaia.py")
trace, baseline = gaia["run"](values.prior, bundle / "match/riscontro.json", args.geometry, args.cohort)
expected = json.loads(pinned(bundle / "gaia/riscontro-definitivo.json", PINS["gaia/riscontro-definitivo.json"]))
assert gaia["compare"](trace, baseline) == expected["chipResults"]
cohort = json.loads(pinned(args.cohort, COHORT))["records"]
epochs = ("j8f866kfq_flc.fits", "j8f866khq_flc.fits")


def summarize(ids):
    common = [acs["PAIRS"][k] for k in ids if k in acs["PAIRS"]]
    stable = [shift for repeat, shift in common if repeat <= 0.3]
    return dict(cohort=len(ids), paired2006=len(common), stableWithin0_3Px=len(stable),
                stableFractionOfCohort=len(stable) / len(ids) if ids else None,
                stableEpochDisplacementP90Px=float(np.quantile(stable, .9)) if stable else None)


by_chip = []
for extension, chip in acs["EXTVER_CHIP"].items():
    names = {key: [] for key in ("SAME_GAIA_BOTH_2002", "DIFFERENT_GAIA_BOTH_2002",
                                  "GAIA_ONLY_ONE_2002", "GAIA_NEITHER_2002")}
    short, long = [trace[epoch, str(chip)] for epoch in epochs]
    assert len(short) == baseline["observations"][epochs[0]][str(chip)]["holdout"]["uniqueMatches"]
    globals_for_chip = [i for i, row in enumerate(cohort) if row["scienceExtver"] == extension]
    for local, global_index in enumerate(globals_for_chip):
        if local in short and local in long:
            key = "SAME_GAIA_BOTH_2002" if short[local][0] == long[local][0] else "DIFFERENT_GAIA_BOTH_2002"
        elif local in short or local in long:
            key = "GAIA_ONLY_ONE_2002"
        else:
            key = "GAIA_NEITHER_2002"
        names[key].append(global_index)
    by_chip.append(dict(chip=chip, groups={key:summarize(ids) for key, ids in names.items()}))

assert sum(group["cohort"] for row in by_chip for group in row["groups"].values()) == len(cohort) == 736
assert sum(group["paired2006"] for row in by_chip for group in row["groups"].values()) == 192
report = dict(protocol="BKL046_NGC6341_ACS_REPEATABILITY_STRATIFIED_BY_GAIA_SELECTION_V1",
              originalAcsAndGaiaReportsReplayed=True, pinnedReplays=PINS, cohortSha256=COHORT,
              repeatabilityCutPx=0.3, chips=by_chip, absoluteIdentityTruthEstablished=False,
              falsePositiveRateEstimated=False, completenessEstimated=False,
              nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write("\n")
