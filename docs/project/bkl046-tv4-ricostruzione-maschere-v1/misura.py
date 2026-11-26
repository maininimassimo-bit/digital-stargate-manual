import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for name in ("protocol", "mask_recovery", "tv4_prediction", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()


def pinned(path, digest):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError(f"Unexpected bytes: {path.name}")
    return raw


pin = "306a8e33d799b29449f1d024659e37ff2de48ce96b1799ec4286c0bd6f4ca6ca"
plan = json.loads(pinned(args.protocol,pin))
parent = args.mask_recovery
pinned(parent/"protocollo.json",plan["parentProtocolSha256"])
known = json.loads(pinned(parent/"riscontro.json",plan["parentReceiptSha256"]))
stats = defaultdict(list)


def evaluate(stage, model, group, frame, region, fraction, cut, original, predicted, clipped):
    import numpy as np
    observed = clipped >= cut
    lost = original > cut
    replacement = np.maximum(predicted,cut)
    variants = {"observed":observed}
    for offset in plan["predictorOffsetsDn"]:
        decision = predicted >= cut+offset
        variants[f"forecast_{offset}"] = decision
        variants[f"intersection_{offset}"] = observed&decision
    if not np.any(lost):
        return
    baseline_error = float(np.abs(clipped-original).sum())
    for label, selected in variants.items():
        assert selected.shape == original.shape
        output = np.where(selected,replacement,clipped)
        error = output-original
        changed = output != clipped
        if label == "observed" or label.startswith("intersection_"):
            assert np.array_equal(output[~observed],original[~observed])
        key = (stage,model,group,region,fraction,label)
        stats[key].append(dict(frame=frame, lostPixels=int(lost.sum()),
            overwrittenMeasurablePixels=int(np.count_nonzero(changed & ~observed)),
            missedLostPixels=int(np.count_nonzero(lost & ~selected)),
            baselineAbsoluteErrorDn=baseline_error,absoluteErrorDn=float(np.abs(error).sum()),
            signedIntegratedErrorDn=float(error.sum()),
            absoluteErrorOnMeasurableDn=float(np.abs(error[~observed]).sum())))


original_path = parent/"misura.py"
source = pinned(original_path,plan["parentSourceSha256"]).decode("utf-8")
anchor = "        estimate = np.where(marked,np.maximum(forecast,ceiling),clipped)"
assert source.count(anchor)==1
source = source.replace(anchor, anchor +
    "\n        EVALUATE(stage,model,group,frame,region,fraction,ceiling,original,forecast,clipped)")
args.output.mkdir()
replay = args.output/"previous"
argv = sys.argv
try:
    sys.argv = [str(original_path),str(parent/"protocollo.json"),str(args.tv4_prediction),str(replay)]
    ns = {"__name__":"verified_prior_mask_recovery","__file__":str(original_path),"EVALUATE":evaluate}
    exec(compile(source,str(original_path),"exec"),ns)
finally:
    sys.argv = argv
assert json.loads(pinned(replay/"riscontro.json",plan["parentReceiptSha256"]))==known
summary = []
for key, frames in sorted(stats.items()):
    fields = [k for k in frames[0] if k!="frame"]
    counts = {k:sum(f[k] for f in frames) for k in fields}
    if key[-1] == "observed":
        assert counts["missedLostPixels"] == counts["overwrittenMeasurablePixels"] == 0
    summary.append(dict(**dict(zip(("training","model","group","region","fraction","mask"),key,strict=True)),
                        frames=len(frames), **counts,
                        fractionalAbsoluteErrorReduction=1-counts["absoluteErrorDn"]/counts["baselineAbsoluteErrorDn"]))
assert summary
report = dict(protocol=plan["schema"],protocolSha256=pin,parentReportReproduced=True,
              parentReportSha256=plan["parentReceiptSha256"],onlyRegionsWithOriginalGroundTruth=True,
              thresholdSelected=False, cases=summary,scientificClosures=0,nativeExecutions=0)
for name,value in (("riscontro.json",report),("dettaglio.json",[
        dict(key=list(key),frames=val) for key,val in sorted(stats.items())])):
    with (args.output/name).open("x",encoding="utf-8",newline="\n") as f:
        json.dump(value,f,indent=2,allow_nan=False)
        f.write("\n")
