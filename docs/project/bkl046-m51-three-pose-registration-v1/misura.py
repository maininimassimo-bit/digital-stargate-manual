"""Check M51 pairwise and chained registration on a common Gaia holdout."""
import contextlib
from hashlib import sha256
import io
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

protocol, parent, output = map(Path, sys.argv[1:4])
raw_protocol = protocol.read_bytes()
plan = json.loads(raw_protocol)


def exact(path, pin):
    data = path.read_bytes()
    if sha256(data).hexdigest() != pin:
        raise ValueError(f"Changed input {path.name}")
    return data


source = parent / "misura.py"
code = exact(source, plan["codeSha256"])
expected = exact(parent / "riscontro.json", plan["reportSha256"])
parent_args = sys.argv[4:]
ns = dict(__name__="__main__")
with TemporaryDirectory(dir=output.parent) as temp:
    replay = Path(temp) / "parent.json"
    sys.argv = [str(source), str(parent / "protocollo.json"), *parent_args, str(replay)]
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, str(source), "exec"), ns)
    if replay.read_bytes() != expected:
        raise ValueError("Signal-weighted parent did not replay exactly")

np = ns["np"]
prediction = ns["prediction"]
frames = ns["frames"]
proxies = ns["proxies"]
ids = {subset: sorted(set.intersection(*(set(frame[subset]) for frame in frames)))
       for subset in ("train", "test")}
if min(map(len, ids.values())) < plan["minimumCommon"] or set(ids["train"]) & set(ids["test"]):
    raise ValueError("Insufficient or overlapping common Gaia sets")


def robust_weights(x, y, base):
    weights = base
    for _ in range(plan["maxIterations"]):
        residual = np.linalg.norm(prediction(x, y, x, weights) - y, axis=1)
        scale = max(float(np.median(residual)) / np.sqrt(2 * np.log(2)), plan["scaleFloorPx"])
        cutoff = plan["tuning"] * scale
        update = base * cutoff / np.maximum(residual, cutoff)
        if np.max(abs(update - weights)) < 1e-9:
            return update
        weights = update
    return weights


# A known similarity with one displaced training point tests robust recovery.
x = np.array([[i, j] for i in range(5) for j in range(4)], dtype=float)
y = x @ np.array([[1.01, .02], [-.02, 1.01]]) + [4., 6.]
corrupted = y.copy()
corrupted[0] += [10., -11.]
w = np.ones(len(x))
unit_error = np.linalg.norm(prediction(x, corrupted, x[1:], w) - y[1:], axis=1)
robust_error = np.linalg.norm(prediction(x, corrupted, x[1:], robust_weights(x, corrupted, w)) - y[1:], axis=1)
if float(np.quantile(robust_error, .9)) > .07 or np.quantile(robust_error, .9) >= np.quantile(unit_error, .9):
    raise ValueError("Controlled displaced training point check failed")


def centroids(frame, subset, method):
    return np.asarray([frames[frame][subset][key][method] for key in ids[subset]])


def stats(observed, predicted, threshold):
    error = np.linalg.norm(observed - predicted, axis=1)
    p90 = float(np.quantile(error, .9))
    return dict(p50Px=float(np.median(error)), p90Px=p90,
                countWithinThreshold=int((error <= threshold).sum()),
                p90WithinThreshold=p90 <= threshold)


results = {}
for method in plan["methods"]:
    chains = {}
    for weighting in ("unit", "signal", "signalRobust"):
        mapping = {}
        scores = {}
        for a, b in plan["pairs"]:
            x, y = (centroids(i, "train", method) for i in (a, b))
            strength = np.asarray([min(proxies[a]["train"][key], proxies[b]["train"][key])
                                   for key in ids["train"]])
            limit = np.sqrt(ns["plan"]["maximumWeightRatio"])
            weight = (np.ones(len(x)) if weighting == "unit" else
                      np.clip((strength / np.median(strength))**2, 1/limit, limit))
            if weighting == "signalRobust":
                weight = robust_weights(x, y, weight)
            mapping[a, b] = (x, y, weight)
            guess = prediction(x, y, centroids(a, "test", method), weight)
            scores[f"{a}-{b}"] = stats(centroids(b, "test", method), guess, plan["thresholdPx"])
        first = centroids(0, "test", method)
        x01, y01, w01 = mapping[0, 1]
        x12, y12, w12 = mapping[1, 2]
        x02, y02, w02 = mapping[0, 2]
        direct = prediction(x02, y02, first, w02)
        chained = prediction(x12, y12, prediction(x01, y01, first, w01), w12)
        scores["0-1-2"] = stats(centroids(2, "test", method), chained, plan["thresholdPx"])
        scores["directVersusChained"] = stats(direct, chained, plan["thresholdPx"])
        chains[weighting] = scores
    results[method] = chains

receipt = dict(schema=plan["schema"], protocolSha256=sha256(raw_protocol).hexdigest(),
               parentReceiptSha256=plan["reportSha256"], commonTraining=len(ids["train"]),
               commonHoldout=len(ids["test"]), holdoutIds=ids["test"], results=results,
               nativeExecutions=0, scientificClosures=0)
with output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(receipt, stream, indent=2, sort_keys=True, allow_nan=False)
    stream.write("\n")
