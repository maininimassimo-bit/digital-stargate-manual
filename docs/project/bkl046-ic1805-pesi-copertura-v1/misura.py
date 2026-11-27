"""Derive weight concentration from the frozen IC 1805 footprint geometry."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

parser=argparse.ArgumentParser()
for key in ("protocol","prior_protocol","prior_report","packages","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np
assert np.__version__=="2.3.5"


def pinned(path,digest):
    raw=path.read_bytes()
    assert sha256(raw).hexdigest()==digest,path.name
    return json.loads(raw)


pin="c4c230d099bb5200d17c611b1708f1de85513f43b0adcb9e58d3d6035150972b"
cfg=pinned(args.protocol,pin)
prior=pinned(args.prior_report,cfg["priorReportSha256"])
p=pinned(args.prior_protocol,cfg["priorProtocolSha256"])
sites=np.asarray([[0,0],[1,0],[0,1],[1,1]])
EPS=1e-12


def area(distance,width):
    return np.prod(np.clip((1+width)/2-distance,0,width),axis=-1)


def positive_divide(a,b):
    return np.divide(a,b,out=np.zeros_like(a,dtype=float),where=b>0)


def summarize(shifts,width,radius):
    centers=sites[None,:,None,:]-np.asarray(shifts)[:,None,None,:]
    separation=np.abs((sites[None,None,:,:]-centers+1)%2-1)
    nominal=area(separation,width)
    np.testing.assert_allclose(nominal.sum(axis=-1),width**2,rtol=0,atol=2e-12)
    lower=area(separation+radius,width)
    upper=area(np.maximum(separation-radius,0),width)
    assert np.all(lower<=nominal+EPS) and np.all(nominal<=upper+EPS)
    positive=((separation+radius < (1+width)/2-EPS).all(axis=-1)).sum(axis=0)
    n_eff=positive_divide(nominal.sum(axis=0)**2,(nominal**2).sum(axis=0))
    bound_squares=positive_divide(lower.sum(axis=0)**2,(upper**2).sum(axis=0))
    bound_largest=positive_divide(lower.sum(axis=0),upper.max(axis=0))
    low=np.maximum(bound_squares,bound_largest)
    assert np.all(low<=n_eff+EPS)
    share=positive_divide(nominal.max(axis=0),nominal.sum(axis=0))
    if radius==0:
        np.testing.assert_allclose(low,n_eff,rtol=0,atol=1e-12)
        assert np.all(n_eff<=positive+EPS)
    return positive, n_eff, low, share


rows=[]
for star in prior["rows"]:
    properties=[]
    for width in p["dropWidths"]:
        previous=star["byDrop"][str(width)]
        for index,radius in enumerate(p["radiusPx"]):
            halves=[summarize(h,width,radius) for h in star["shiftsByHalf"]]
            for k,half in enumerate(halves):
                assert half[0].tolist()==previous[index]["counts"][k]
            minima=[float(min(values[entry].min() for values in halves)) for entry in range(3)]
            largest_share=float(max(values[3].max() for values in halves))
            properties.append(dict(width=width,radius=radius,minPositiveCount=int(minima[0]),
                          minNominalEffectiveCount=minima[1],minConservativeBound=minima[2],
                          maximumNominalSingleExposureWeightShare=largest_share))
    rows.append(dict(ordinal=star["referenceOrdinal"],properties=properties))
assert len(rows)==prior["eligibleStars"]==72
summary=[]
n=cfg["thresholdForDiagnosticComparison"]
for width in p["dropWidths"]:
    for radius in p["radiusPx"]:
        values=[next(x for x in row["properties"] if x["width"]==width and x["radius"]==radius) for row in rows]
        summary.append(dict(width=width,radius=radius,
                sufficientPositiveCount=sum(x["minPositiveCount"]>=n for x in values),
                sufficientNominalEffectiveCount=sum(x["minNominalEffectiveCount"]>=n-EPS for x in values),
                sufficientConservativeEffectiveCount=sum(x["minConservativeBound"]>=n-EPS for x in values),
                medianWorstNominalEffectiveCount=float(np.median([x["minNominalEffectiveCount"] for x in values])),
                maxSingleExposureNominalShare=max(x["maximumNominalSingleExposureWeightShare"] for x in values)))
result=dict(protocol=cfg["schema"],protocolSha256=pin,originalCountsExactlyReproduced=True,
            eligibleStars=len(rows),diagnosticThreshold=n,summary=summary,rows=rows,
            expectedNativeWeightModelVerified=False,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf-8",newline="\n") as f:
    json.dump(result,f,indent=2,allow_nan=False)
    f.write("\n")
