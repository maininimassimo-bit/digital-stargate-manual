from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser = ArgumentParser()
for name in ("protocol", "parent", "gaia", "capture", "matcher", "rawpy", "dependencies", "vc", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()


def exact(path, expected):
    data = path.read_bytes()
    if sha256(data).hexdigest() != expected:
        raise ValueError(f"Changed {path.name}")
    return data


PIN = "6d1af15ea0c5a9437297c834b6d7e6594d755a2889522a2ef2c1f5dd00d33736"
plan = json.loads(exact(args.protocol, PIN))
prior = exact(args.parent / "misura.py", plan["parentCode"])
prior_report = exact(args.parent / "riscontro.json", plan["parentReport"])
with TemporaryDirectory(dir=args.output.parent) as temp:
    replay = Path(temp) / "replay.json"
    previous_argv = sys.argv
    try:
        sys.argv = [str(args.parent / "misura.py"), *map(str, (
            args.parent / "protocollo.json", args.gaia, args.capture, args.matcher,
            args.rawpy, args.dependencies, args.vc, replay))]
        namespace = {"__name__": "__main__"}
        exec(compile(prior, sys.argv[0], "exec"), namespace)
    finally:
        sys.argv = previous_argv
    if replay.read_bytes() != prior_report:
        raise ValueError("Centroid report replay changed")

import numpy as np

similarity = namespace["similarity"]
height, width = plan["detectorShapeYX"]
origin = np.array(((width - 1) / 2, (height - 1) / 2))
scale = width / 2


def fit(design, target):
    coefficient, _, rank, singular_values = np.linalg.lstsq(design, target, rcond=None)
    if rank != design.shape[1] or singular_values[0] / singular_values[-1] > plan["maxCondition"]:
        return None
    return coefficient


def polynomial(xy, quadratic):
    x, y = xy.T
    terms = [np.ones(len(x)), x, y]
    if quadratic:
        terms.extend((x*x, x*y, y*y))
    return np.column_stack(terms)


def radial(xy):
    return xy * np.sum(xy*xy, axis=1)[:, None]


def radial_design(xy, matrix, offset):
    x, y = xy.T
    ones, zeros = np.ones(len(x)), np.zeros(len(x))
    dx, dy = (radial(xy) @ matrix - radial(xy @ matrix + offset)).T
    horizontal = np.column_stack((x, -y, ones, zeros, dx))
    vertical = np.column_stack((y, x, zeros, ones, dy))
    return np.stack((horizontal, vertical), axis=1).reshape(-1, 5)


def predictions(x, y, test):
    matrix, offset = similarity(x, y)
    result = {"similarity": test @ matrix + offset}
    for name in ("affine", "quadratic"):
        quadratic = name == "quadratic"
        coef = fit(polynomial(x, quadratic), y)
        result[name] = polynomial(test, quadratic) @ coef if coef is not None else None
    coef = fit(radial_design(x, matrix, offset), y.ravel())
    result["similarityPlusRadialDifference"] = (
        (radial_design(test, matrix, offset) @ coef).reshape(-1, 2) if coef is not None else None
    )
    return result


def verify_fixture():
    generator = np.random.default_rng(6246)
    samples = generator.uniform(-0.6, 0.6, size=(70, 2))
    matrix = np.array(((1., 0.02), (-0.02, 1.)))
    shift = np.array((.18, -.14))
    similarity_target = samples @ matrix + shift
    nonlinear = similarity_target + np.column_stack((.013*samples[:,0]**2, -.021*samples[:,0]*samples[:,1]))
    for target, name in ((similarity_target, "similarityPlusRadialDifference"), (nonlinear, "quadratic")):
        actual = predictions(samples[:50], target[:50], samples[50:])[name]
        if actual is None or np.max(np.linalg.norm((actual-target[50:])*scale, axis=1)) > plan["fixtureTolerancePx"]:
            raise ValueError(f"Synthetic model control failed: {name}")


def compare(reference, target):
    train = sorted(reference["train"].keys() & target["train"].keys())
    test = sorted(reference["test"].keys() & target["test"].keys())
    if len(train) < plan["minimumTrain"] or len(test) < plan["minimumTest"]:
        raise ValueError("Insufficient common stars")
    metrics = {}
    for method in plan["methods"]:
        x, y, x_test, y_test = (
            (np.asarray([frame[group][key][method] for key in keys]) - origin) / scale
            for group, keys in (("train", train), ("test", test)) for frame in (reference, target)
        )
        estimates = predictions(x, y, x_test)
        metrics[method] = {}
        for name in plan["models"]:
            if estimates[name] is None:
                metrics[method][name] = {"status": "ILL_CONDITIONED"}
                continue
            errors = np.linalg.norm((estimates[name]-y_test)*scale, axis=1)
            p90 = float(np.quantile(errors, .9))
            metrics[method][name] = {
                "medianPx": float(np.median(errors)), "p90Px": p90,
                "diagnosticThresholdMet": p90 <= plan["diagnosticP90Px"],
            }
    return {"training": len(train), "heldout": len(test), "heldoutIds": test, "metrics": metrics}


verify_fixture()
frames = namespace["outputs"]
report = {
    "schema": plan["schema"], "protocolSha256": PIN, "centroidReplayExact": True,
    "syntheticControlsPassed": True, "relativeToFirst": [compare(frames[0], other) for other in frames[1:]],
    "nativeExecutions": 0, "scientificClosures": 0,
}
with args.output.open("x", encoding="utf8", newline="\n") as destination:
    json.dump(report, destination, indent=2, allow_nan=False)
    destination.write("\n")
