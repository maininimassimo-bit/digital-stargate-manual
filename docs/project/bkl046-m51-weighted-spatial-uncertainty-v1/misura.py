import json
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser = ArgumentParser()
for name in ("protocol", "source", "centroid", "gaia", "capture", "matcher", "rawpy", "dependencies", "vc", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected, f"Changed {path.name}")
    return raw


PIN = "4ec4c13634cff9ddd919b9f01e4213c1c1d07935aa22ee4803528f65528e9102"
plan = json.loads(pinned(args.protocol, PIN))
source = pinned(args.source/"misura.py", plan["sourceCode"])
source_report = pinned(args.source/"riscontro.json", plan["sourceReport"])
with TemporaryDirectory(dir=args.output.parent) as temp:
    path = Path(temp)/"replay.json"
    saved = sys.argv
    try:
        sys.argv = [str(args.source/"misura.py"), *map(str, (
            args.source/"protocollo.json", args.centroid, args.gaia, args.capture,
            args.matcher, args.rawpy, args.dependencies, args.vc, path))]
        previous = {"__name__":"__main__"}
        exec(compile(source, sys.argv[0], "exec"), previous)
    finally:
        sys.argv = saved
    require(path.read_bytes() == source_report, "Prior signal weighting replay changed")

import numpy as np

fit = previous["prediction"]
random = np.random.default_rng(plan["randomSeed"])
prior = json.loads(source_report)
frames, proxies = previous["frames"], previous["proxies"]


def endpoints(unit, weighted):
    a, b = np.quantile(unit, .9), np.quantile(weighted, .9)
    return np.array((a,b,b-a))


def uncertainty(unit, weighted, cells, blocks, draws):
    observations = np.array([endpoints(unit[index],weighted[index]) for index in draws])
    influence = {}
    for cell in blocks:
        kept = cells != cell
        require(kept.sum() >= plan["minDeleteBlockStars"], "Too few stars after block deletion")
        influence[str(cell)] = endpoints(unit[kept],weighted[kept]).tolist()
    return dict(
        estimate=endpoints(unit,weighted).tolist(),
        bootstrapPercentiles=np.quantile(observations,plan["percentiles"],axis=0).tolist(),
        deleteOneBlock=influence,
    )


def compare(index, target, target_proxy):
    ref, ref_proxy = frames[0], proxies[0]
    train=sorted(ref["train"].keys() & target["train"].keys())
    test=sorted(ref["test"].keys() & target["test"].keys())
    previous_result=prior["relativeToFirst"][index]
    require(test == previous_result["heldoutIds"] and len(train) == previous_result["training"],
            "Training or held-out sample changed")
    anchors=np.array([ref["test"][k]["pairedPreview"] for k in test])
    dimensions=np.array((plan["frameWidth"],plan["frameHeight"]))
    divisions=np.array((plan["columns"],plan["rows"]))
    require(np.all((anchors>=0)&(anchors<dimensions)), "Star outside visible sensor")
    sectors=np.floor(anchors/dimensions*divisions).astype(int)
    cells=sectors[:,1]*plan["columns"]+sectors[:,0]
    blocks=np.unique(cells)
    require(len(blocks)>=plan["minOccupiedBlocks"], "Too few occupied spatial blocks")
    groups=[np.flatnonzero(cells==cell) for cell in blocks]
    choices=random.integers(len(blocks), size=(plan["draws"],len(blocks)))
    draws=[np.concatenate([groups[i] for i in row]) for row in choices]
    strength=np.array([min(ref_proxy["train"][k],target_proxy["train"][k]) for k in train])
    cut=float(np.median(strength))
    require(cut==previous_result["trainingMedianProxy"], "Training proxy changed")
    limit=np.sqrt(previous["plan"]["maximumWeightRatio"])
    weighted=np.clip((strength/cut)**2,1/limit,limit)
    result={}
    for method in previous["plan"]["methods"]:
        a,b,x,y=(np.array([frame[group][k][method] for k in keys])
                  for group,keys in (("train",train),("test",test)) for frame in (ref,target))
        unit_error=np.linalg.norm(fit(a,b,x,np.ones(len(a)))-y,axis=1)
        weighted_error=np.linalg.norm(fit(a,b,x,weighted)-y,axis=1)
        expected=[previous_result["metrics"][method][kind]["p90Px"] for kind in ("unit","weighted")]
        require(np.allclose(endpoints(unit_error,weighted_error)[:2],expected,atol=1e-12,rtol=0),
                "Reconstructed residual distribution changed")
        result[method]=uncertainty(unit_error,weighted_error,cells,blocks,draws)
    return dict(training=len(train), heldout=len(test), occupiedBlocks=len(blocks),
                blockCounts={str(cell):len(group) for cell,group in zip(blocks,groups,strict=True)},metrics=result)


synthetic=np.arange(10.)
require(np.allclose(endpoints(synthetic,synthetic-2),[8.1,6.1,-2.]),"Paired difference control failed")
report=dict(schema=plan["schema"],protocolSha256=PIN,sourceReplayedExactly=True,
            endpointOrder=plan["endpoints"],percentileOrder=plan["percentiles"],
            relativeToFirst=[compare(i, frame, proxy) for i,(frame,proxy) in enumerate(
                zip(frames[1:],proxies[1:],strict=True))],
            nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
