import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

parser=argparse.ArgumentParser()
for key in ("protocol","prior_geometry","prior_weights","packages","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np
assert np.__version__=="2.3.5"


def pinned(path,digest):
    raw=path.read_bytes()
    assert sha256(raw).hexdigest()==digest,path.name
    return json.loads(raw)


pin="efd3f340d581938c9041301664ee9801062421ac8ebca2b93c5b42814501b318"
plan=pinned(args.protocol,pin)
last=pinned(args.prior_weights,plan["baselineWeightedReceiptSha256"])
geometry=pinned(args.prior_geometry,plan["priorGeometrySha256"])
prior={r["ordinal"]:r["properties"] for r in last["rows"]}
sites=np.asarray([[0,0],[1,0],[0,1],[1,1]])
threshold=plan["thresholdForDiagnosticComparison"]


def measure(weights):
    coverage=weights.sum(axis=0)
    square=(weights**2).sum(axis=0)
    ess=np.divide(coverage**2,square,out=np.zeros_like(coverage),where=square>0)
    return int((weights>1e-12).sum(axis=0).min()),float(ess.min()),coverage


rows=[]
for source in geometry["rows"]:
    index=source["referenceOrdinal"]
    tests=[]
    for width in plan["dropWidths"]:
        original=next(p for p in prior[index] if p["width"]==width and p["radius"]==0)
        cases=[]
        nominal=[]
        for h,shifts in enumerate(source["shiftsByHalf"]):
            centers=sites[None,:,None,:]-np.asarray(shifts)[:,None,None,:]
            distance=np.abs((sites[None,None,:,:]-centers+1)%2-1)
            w=np.prod(np.clip((1+width)/2-distance,0,width),axis=-1)
            np.testing.assert_allclose(w.sum(axis=-1),width**2,rtol=0,atol=2e-12)
            count,ess,total=measure(w)
            nominal.append((count,ess))
            for i in range(len(w)):
                remaining=w[np.arange(len(w))!=i]
                after_count,after_ess,after_total=measure(remaining)
                ratio=np.divide(after_total,total,out=np.ones_like(total),where=total>0)
                assert np.all((ratio>=0)&(ratio<=1+1e-12))
                cases.append(dict(half=h,omittedLocalOrdinal=i,minPositiveCount=after_count,
                                  minEffectiveCount=after_ess,minimumRemainingWeightFraction=float(ratio.min())))
        assert min(x[0] for x in nominal)==original["minPositiveCount"]
        original_ess=min(x[1] for x in nominal)
        assert abs(original_ess-original["minNominalEffectiveCount"])<=1e-12
        worst=min(c["minEffectiveCount"] for c in cases)
        tests.append(dict(width=width,nominalMinEffectiveCount=original_ess,
                          allOmissionsMaintainTwo=worst>=threshold-1e-12,
                          worstOmissionEffectiveCount=worst,
                          atLeastOneOmissionCausesEmptyCell=any(c["minPositiveCount"]==0 for c in cases),
                          previouslyNominalTwo=original_ess>=threshold-1e-12,
                          cases=cases))
    rows.append(dict(ordinal=index,tests=tests))

summary=[]
for width in plan["dropWidths"]:
    items=[next(x for x in row["tests"] if x["width"]==width) for row in rows]
    assert len(items)==72
    summary.append(dict(width=width,starsNominalTwo=sum(x["previouslyNominalTwo"] for x in items),
                        allSingleOmissionsMaintainTwo=sum(x["allOmissionsMaintainTwo"] for x in items),
                        starsWithAnEmptyCellUnderOneOmission=sum(x["atLeastOneOmissionCausesEmptyCell"] for x in items),
                        medianWorstEffectiveCount=float(np.median([x["worstOmissionEffectiveCount"] for x in items]))))
result=dict(protocol=plan["schema"],protocolSha256=pin,exactNominalWeightsReproduced=True,
            summary=summary,rows=rows,scientificClosures=0,nativeExecutions=0)
with args.output.open("x",encoding="utf-8",newline="\n") as out:
    json.dump(result,out,indent=2,allow_nan=False)
    out.write("\n")
