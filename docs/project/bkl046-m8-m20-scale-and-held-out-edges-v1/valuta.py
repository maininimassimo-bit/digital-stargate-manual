"""Recompute M8/M20 held-out edge performance at each archived stellar scale."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, base, empirical, edge_protocol, unit_edges, dependencies, output = map(Path, sys.argv[1:])
protocol_bytes = protocol.read_bytes()
p = json.loads(protocol_bytes)


def pinned(path, expected):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected:
        raise ValueError(f"Source changed: {path.name}")
    return raw


pins = p["sourcePins"]
prior = json.loads(pinned(base / "riscontro.json", pins["reference"]))
scales = json.loads(pinned(empirical, pins["empirical"]))
edge_definition = json.loads(pinned(edge_protocol, pins["bands"]))
edge_prior = json.loads(pinned(unit_edges, pins["edges"]))
source = base / "riferimenti.py"
boot, marker, _ = pinned(source, prior["programSha256"]).decode().partition("\ncomparisons = []\n")
assert marker
namespace = {"__file__": str(source)}
sys.argv = [str(source), str(base), str(base / "capture"), str(base / "stellar" / "riscontro.json"),
            str(dependencies), str(output)]
exec(compile(boot, str(source), "exec"), namespace)
np = namespace["np"]
images, common, groups, design, train, scores, cell = (
    namespace[k] for k in ("images", "common", "groups", "design", "train", "scores", "cell"))
coordinates = np.array([(s[1].start//cell, s[0].start//cell) for s in groups])
edge_folds = {}
for name in ("left", "right", "top", "bottom"):
    axis, start = edge_definition["bands"][name]
    selected = (coordinates[:, axis] >= start) & (coordinates[:, axis] < start + edge_definition["bandWidthCells"])
    assert int(selected.sum()) == (24 if axis == 0 else 32)
    edge_folds[name] = ~selected


def evaluate(data, fit):
    offset, plane = [scores(design, data, fit, terms) for terms in (1, 3)]
    ok = (plane["medianAbsoluteADU"] <= offset["medianAbsoluteADU"] * (1 - p["threshold"])
          and plane["p90AbsoluteADU"] <= offset["p90AbsoluteADU"])
    return {"offset": offset, "plane": plane, "pass": ok}


edge_cases = {(r["reference"], r["target"]): r for r in edge_prior["results"]}
scale_cases = {(r["ref"], r["target"]): r for r in scales["cases"]}
pairs = {(r["referenceIndex"], r["targetIndex"]): r for r in prior["cases"]}
assert set(edge_cases) == set(scale_cases) == set(pairs) and len(pairs) == p["pairs"]

results = []
for (ref, target), old in pairs.items():
    difference = images[target] - images[ref]
    contrast = images[target] - np.median(images[target][common])
    delta_bins = [difference[s][common[s]] for s in groups]
    contrast_bins = [contrast[s][common[s]] for s in groups]

    def compare(scale, expected_folds):
        assert np.isfinite(scale) and scale > 0
        data = np.array([np.median(d + (scale-1)*c) for d,c in zip(delta_bins, contrast_bins, strict=True)])
        checkerboard = [{"trainParity": i, **evaluate(data, fold)} for i,fold in enumerate((train, ~train))]
        assert checkerboard == expected_folds
        edges = {name: evaluate(data, fit) for name,fit in edge_folds.items()}
        checker_pass = all(row["pass"] for row in checkerboard)
        edge_pass = all(row["pass"] for row in edges.values())
        return {"checkerboardPass": checker_pass, "allEdgesPass": edge_pass,
                "jointPass": checker_pass and edge_pass, "edges": edges}

    unit = compare(1.0, old["folds"])
    assert unit["allEdgesPass"] == edge_cases[ref, target]["allEdgesPass"]
    assert all(res == edge_cases[ref, target]["bands"][name] for name,res in unit["edges"].items())
    trials = []
    archived = scale_cases[ref, target]["trials"]
    assert len(archived) == p["scalesPerPair"]
    for trial in archived:
        outcome = compare(trial["scale"], trial["folds"])
        assert outcome["checkerboardPass"] == trial["passBoth"]
        trial_meta = {key: trial[key] for key in ("parity", "calibration", "center", "withheldTile", "scale")}
        trials.append({**trial_meta, **outcome})
    counts = {name: sum(row[name] for row in trials) for name in ("checkerboardPass", "allEdgesPass", "jointPass")}
    results.append({"reference":ref, "target":target,"unit":unit,"passesByCriterion":counts,"trials":trials})

counts = ("checkerboardPass", "allEdgesPass", "jointPass")
summary = {
    "pairs":len(results),
    "scalesPerPair":p["scalesPerPair"],
    "trials":sum(len(row["trials"]) for row in results),
    "unitPasses":{name:sum(row["unit"][name] for row in results) for name in counts},
    "trialPasses":{name:sum(row["passesByCriterion"][name] for row in results) for name in counts},
    "pairsPassingAny":{name:sum(row["passesByCriterion"][name]>0 for row in results) for name in counts},
    "pairsPassingAll":{name:sum(row["passesByCriterion"][name]==p["scalesPerPair"] for row in results) for name in counts},
}
common = dict(schema="BKL046_M8M20_SCALE_AND_EDGE_V1", protocolSha256=sha256(protocol_bytes).hexdigest(),
              programSha256=sha256(Path(__file__).read_bytes()).hexdigest(), sources=pins,
              summary=summary,nativeExecutions=0,scientificClosures=0)
full = (json.dumps({**common,"cases":results}, sort_keys=True, separators=(",",":"))+"\n").encode()
with (output / "tutti-gli-esiti.json").open("xb") as stream:
    stream.write(full)
public = {**common,"fullReportSha256":sha256(full).hexdigest(),
          "pairs":[{k:row[k] for k in ("reference","target","passesByCriterion")} for row in results]}
with (output / "riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(public,sort_keys=True,indent=2)+"\n")
print(json.dumps(summary))
