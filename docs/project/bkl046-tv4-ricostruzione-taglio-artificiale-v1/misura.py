import argparse
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


pin = "45a56dff86e09b8b87af667a5c13c07f398b3621d31c484374051d20a17ae4e3"
cfg = json.loads(pinned(args.protocol, pin))
parent = args.parent
known = json.loads(pinned(parent/"riscontro.json",cfg["priorReportSha256"]))
pinned(parent/"protocollo.json",cfg["priorProtocolSha256"])
rows = []
skipped = 0


def capture(stage, model, group, frame, region, forecast, original, physical_ceiling):
    import numpy as np

    global skipped
    assert np.isfinite(forecast).all() and np.max(original) <= physical_ceiling
    if np.any(original == physical_ceiling):
        skipped += 1
        return
    row = dict(training=stage,model=model,group=group,frame=frame,region=region,
               originalTotalDn=float(original.sum()), originalMaxDn=float(original.max()), cases=[])
    for fraction in cfg["artificialCeilingFractions"]:
        ceiling = int(physical_ceiling*fraction)
        # Integral-valued input at the artificial limit is ambiguous in the
        # observed clipped frame, so equality is included in the mask.
        marked = original >= ceiling
        lost = original > ceiling
        clipped = np.minimum(original,ceiling)
        estimate = np.where(marked,np.maximum(forecast,ceiling),clipped)
        assert np.array_equal(estimate[~marked],original[~marked])
        delta_clip = clipped-original
        delta_estimate = estimate-original
        row["cases"].append(dict(fraction=fraction, artificialCeilingDn=ceiling,
              marked=int(np.count_nonzero(marked)), actuallyChanged=int(np.count_nonzero(lost)),
              unchangedOutsideMask=True, baselineAbsoluteErrorDn=float(np.abs(delta_clip).sum()),
              recoveredAbsoluteErrorDn=float(np.abs(delta_estimate).sum()),
              baselineSignedTotalErrorDn=float(delta_clip.sum()),
              recoveredSignedTotalErrorDn=float(delta_estimate.sum())))
    rows.append(row)


script = parent/"verifica.py"
code = pinned(script,cfg["priorSourceSha256"]).decode("utf-8")
anchor = "                        by_region[region]=measure(pred,raw,ceiling)"
assert code.count(anchor) == 1
namespace = {"__name__":"verified_replay","__file__":str(script),"CAPTURE":capture}
exec(compile(code.replace(anchor,anchor+"\n                        CAPTURE(stage,model,group,name,region,pred,raw,ceiling)"),
             str(script),"exec"),namespace)
args.output.mkdir()
baseline = args.output/"replay-parent.json"
namespace["main"](baseline)
assert json.loads(pinned(baseline,cfg["priorReportSha256"])) == known
assert len(rows)+skipped == sum(len(r["results"]) for r in known["records"])
summary = []
for key in sorted({tuple(r[k] for k in ("training","model","group","region")) for r in rows}):
    cohort = [r for r in rows if tuple(r[k] for k in ("training","model","group","region"))==key]
    output = []
    for i,fraction in enumerate(cfg["artificialCeilingFractions"]):
        cases = [r["cases"][i] for r in cohort]
        fields = ("marked","actuallyChanged","baselineAbsoluteErrorDn","recoveredAbsoluteErrorDn",
                  "baselineSignedTotalErrorDn","recoveredSignedTotalErrorDn")
        values = {k:sum(row[k] for row in cases) for k in fields}
        initial = values["baselineAbsoluteErrorDn"]
        output.append(dict(fraction=fraction,**values,
                           fractionalMaeReduction=1-values["recoveredAbsoluteErrorDn"]/initial if initial else None,
                           framesWithLowerAbsoluteError=sum(c["recoveredAbsoluteErrorDn"]<c["baselineAbsoluteErrorDn"]
                                                            for c in cases)))
    summary.append(dict(**dict(zip(("training","model","group","region"),key,strict=True)),
                        frames=len(cohort),results=output))
report = dict(protocol=cfg["schema"],protocolSha256=pin,
              exactParentReplay=True,originallyCensoredRegionEvaluationsExcluded=skipped,
              regionEvaluations=len(rows),actualSaturatedFluxRecovered=False,
              anyThresholdSelected=False, summary=summary,scientificClosures=0,nativeExecutions=0)
for filename,value in (("riscontro.json",report),("dettaglio.json",rows)):
    with (args.output/filename).open("x",encoding="utf-8",newline="\n") as f:
        json.dump(value,f,indent=2,allow_nan=False)
        f.write("\n")
