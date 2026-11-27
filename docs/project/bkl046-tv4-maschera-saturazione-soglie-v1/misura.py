"""Measure saturation-mask operating points on the same frozen held frames."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

parser = argparse.ArgumentParser()
for key in ("protocol", "parent", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()


def pinned(path, digest):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == digest, path.name
    return raw


pin = "49b8118618bb0a894ee38fbb5fd9dd3ccedf4ce507600865615711297521a589"
cfg = json.loads(pinned(args.protocol, pin))
parent = args.parent
pinned(parent/"protocollo.json",cfg["parentProtocolSha256"])
known = json.loads(pinned(parent/"riscontro.json",cfg["parentReportSha256"]))
rows = []


def capture(training, model, group, frame, region, pred, raw, ceiling):
    import numpy as np

    assert np.isfinite(pred).all() and np.max(raw) <= ceiling
    saturated = raw == ceiling
    normal = ~saturated
    score = pred-ceiling
    counts = {}
    for offset in cfg["decisionOffsetsDn"]:
        marked = score >= offset
        counts[str(offset)] = dict(correctMarked=int(np.count_nonzero(marked&saturated)),
                                   unsaturatedMarked=int(np.count_nonzero(marked&normal)),
                                   saturatedUnmarked=int(np.count_nonzero(~marked&saturated)),
                                   correctUnmarked=int(np.count_nonzero(~marked&normal)))
    bands = {}
    for margin in cfg["abstentionBandsDn"]:
        undecided = (score >= -margin) & (score < margin)
        bands[str(margin)] = dict(
            saturatedDeferred=int(np.count_nonzero(undecided&saturated)),
            unsaturatedDeferred=int(np.count_nonzero(undecided&normal)),
            saturatedDecidedSafe=int(np.count_nonzero((score < -margin)&saturated)),
            unsaturatedDecidedMarked=int(np.count_nonzero((score >= margin)&normal)))
    rows.append(dict(training=training,model=model,group=group,frame=frame,region=region,
                     saturated=int(np.count_nonzero(saturated)), unsaturated=int(np.count_nonzero(normal)),
                     fromCeilingWhenUnclippedAndFlaggedDn=
                         (np.quantile(ceiling-raw[(score>=0)&normal],[.05,.5,.95]).tolist()
                          if np.any((score>=0)&normal) else None), counts=counts, abstention=bands))


script = parent/"verifica.py"
source = pinned(script,cfg["parentSourceSha256"]).decode()
tag = "                        by_region[region]=measure(pred,raw,ceiling)"
assert source.count(tag)==1
scope = {"__name__":"pinned_prediction", "__file__":str(script), "CAPTURE":capture}
exec(compile(source.replace(tag,tag+"\n                        CAPTURE(stage,model,group,name,region,pred,raw,ceiling)"),
             str(script),"exec"),scope)
args.output.mkdir()
replay = args.output/"replay-parent.json"
scope["main"](replay)
assert json.loads(pinned(replay,cfg["parentReportSha256"])) == known
assert len(rows)==sum(len(row["results"]) for row in known["records"])
expected = {(x["training"],x["model"],x["group"],x["frame"],region):r
            for x in known["records"] for region,r in x["results"].items()}
groups = defaultdict(list)
for row in rows:
    key = tuple(row[k] for k in ("training","model","group","frame","region"))
    ref = expected[key]
    initial = row["counts"]["0"]
    assert list(initial.values())==[ref[k] for k in ("tp","fp","fn","tn")]
    groups[tuple(row[k] for k in ("training","model","group","region"))].append(row)


def summarize(items, kind, variants):
    res = {}
    for option in variants:
        label = str(option)
        res[label] = {k:sum(r[kind][label][k] for r in items) for k in items[0][kind][label]}
    return res


result = []
for (training, model, group, region), items in sorted(groups.items()):
    record = dict(training=training, model=model,group=group,region=region,frames=len(items),
                  saturated=sum(r["saturated"] for r in items),unsaturated=sum(r["unsaturated"] for r in items),
                  counts=summarize(items,"counts",cfg["decisionOffsetsDn"]),
                  abstention=summarize(items,"abstention",cfg["abstentionBandsDn"]))
    assert all(sum(c.values())==record["saturated"]+record["unsaturated"] for c in record["counts"].values())
    result.append(record)
report = dict(protocol=cfg["schema"],protocolSha256=pin,parentReportSha256=cfg["parentReportSha256"],
              exactParentReplay=True, evaluatedFrames=known["evaluatedFrames"],
              anyThresholdSelected=False, saturationFluxRecovered=False,
              results=result, scientificClosures=0,nativeExecutions=0)
with (args.output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as f:
    json.dump(report,f,indent=2,allow_nan=False)
    f.write("\n")
with (args.output/"dettaglio.json").open("x",encoding="utf-8",newline="\n") as f:
    json.dump(rows,f,indent=2,allow_nan=False)
    f.write("\n")
