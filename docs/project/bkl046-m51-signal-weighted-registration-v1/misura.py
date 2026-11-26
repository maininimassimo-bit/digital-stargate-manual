from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
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


PIN = "92ccba719b5cbcbfebdfc30d96a40739dc02000007ec2397592e015d017e962a"
plan = json.loads(exact(args.protocol, PIN))
prior = exact(args.parent / "misura.py", plan["parentCode"])
previous_report = exact(args.parent / "riscontro.json", plan["parentReport"])
with TemporaryDirectory(dir=args.output.parent) as temp:
    replay = Path(temp) / "replay.json"
    previous_argv = sys.argv
    try:
        sys.argv = [str(args.parent / "misura.py"), *map(str, (
            args.parent / "protocollo.json", args.gaia, args.capture, args.matcher,
            args.rawpy, args.dependencies, args.vc, replay))]
        parent = {"__name__": "__main__"}
        exec(compile(prior, sys.argv[0], "exec"), parent)
    finally:
        sys.argv = previous_argv
    if replay.read_bytes() != previous_report:
        raise ValueError("Centroid replay changed")

import numpy as np
import rawpy

radius = parent["rad"]
rx, ry, core, annulus = (parent[key] for key in ("rx", "ry", "core", "annulus"))


def signal_proxy(data, seed):
    x, y = np.rint(seed).astype(int)
    patch = data[y-radius:y+radius+1, x-radius:x+radius+1]
    ratios = []
    for oy, ox in ((0, 1), (1, 0)):
        green = ((y+ry)%2 == oy) & ((x+rx)%2 == ox)
        sky = patch[green & annulus].astype(float)
        level = np.median(sky)
        noise = max(1., 1.4826*np.median(np.abs(sky-level)))
        ratios.append((float(patch[green & core].max())-level)/noise)
    proxy = min(ratios)
    if not np.isfinite(proxy) or proxy <= 0:
        raise ValueError("Invalid peak-to-noise proxy")
    return float(proxy)


def prediction(x, y, test, weights):
    weights = weights / weights.sum()
    x0, y0 = weights @ x, weights @ y
    u, v = x-x0, y-y0
    norm = weights @ np.sum(u*u, axis=1)
    a = (weights @ np.sum(u*v, axis=1)) / norm
    b = (weights @ (u[:, 0]*v[:, 1]-u[:, 1]*v[:, 0])) / norm
    matrix = np.array(((a,b),(-b,a)))
    return (test-x0) @ matrix + y0


def fixture():
    x = np.array(((10.,11.),(12.,17.),(15.,10.),(20.,20.)))
    y = x @ np.array(((.98,.02),(-.02,.98))) + np.array((2.,-8.))
    w = np.array((1.,4.,.25,2.))
    if not np.allclose(prediction(x[:3], y[:3], x[3:], w[:3]), y[3:], atol=1e-10, rtol=0):
        raise ValueError("Weighted similarity control failed")


def score(errors, subset):
    e = errors[subset]
    return dict(count=len(e), p90Px=float(np.quantile(e,.9)) if len(e)>=10 else None)


def compare(ref, target, ref_proxy, target_proxy):
    ids = {group: sorted(ref[group].keys() & target[group].keys()) for group in ("train","test")}
    if len(ids["train"]) < plan["minimumTrain"] or len(ids["test"]) < plan["minimumTest"]:
        raise ValueError("Too few common stars")
    strength = {group: np.array([min(ref_proxy[group][k],target_proxy[group][k]) for k in keys])
                for group,keys in ids.items()}
    cut = float(np.median(strength["train"]))
    limit = np.sqrt(plan["maximumWeightRatio"])
    weights = np.clip((strength["train"]/cut)**2, 1/limit, limit)
    less = strength["test"] < cut
    metrics = {}
    for method in plan["methods"]:
        x,y,tx,ty = (np.asarray([frame[group][key][method] for key in keys])
                      for group,keys in ids.items() for frame in (ref,target))
        methods = {}
        for name, w in (("unit", np.ones(len(x))), ("weighted", weights)):
            residual = np.linalg.norm(prediction(x,y,tx,w)-ty,axis=1)
            p90 = float(np.quantile(residual,.9))
            methods[name] = dict(p90Px=p90, belowTrainingMedian=score(residual,less),
                                 atOrAboveTrainingMedian=score(residual,~less),
                                 diagnosticThresholdMet=p90<=plan["diagnosticP90Px"])
        metrics[method] = methods
    return dict(training=len(ids["train"]),heldout=len(ids["test"]),heldoutIds=ids["test"],
                trainingMedianProxy=cut,metrics=metrics)


fixture()
frames = parent["outputs"]
proxies = []
for sample, points in zip(parent["receipt"]["samples"], frames, strict=True):
    data = exact(args.capture/"originali"/sample["file"], sample["sha256"])
    with rawpy.imread(BytesIO(data)) as image:
        proxies.append({group: {key: signal_proxy(image.raw_image_visible, pos["pairedPreview"])
                                for key,pos in stars.items()} for group,stars in points.items()})

report = dict(schema=plan["schema"],protocolSha256=PIN,centroidReplayExact=True,syntheticControlPassed=True,
              relativeToFirst=[compare(frames[0], frame, proxies[0], proxy)
                               for frame,proxy in zip(frames[1:],proxies[1:],strict=True)],
              nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
