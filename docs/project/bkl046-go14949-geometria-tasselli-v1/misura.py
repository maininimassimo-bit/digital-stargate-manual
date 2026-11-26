import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

parser=argparse.ArgumentParser()
for key in ("protocol","first_bundle","second_bundle","first_long","second_long","field40","cross_depth","axis_ledger","packages","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np

assert np.__version__=="2.3.5"


def pinned(path,expected):
    raw=path.read_bytes()
    assert sha256(raw).hexdigest()==expected,path.name
    return raw


pin="eb0afc8c0312a54e5bf9609ebe5bc07d2ef7b779473231cbc5b8e2d1a2f25280"
plan=json.loads(pinned(args.protocol,pin))
args.output.mkdir()
tables={}
anchor='                model_status="P90_WITHIN_LIMIT" if summary["affine"]["passes"] else "P90_OUTSIDE_LIMIT"'
for case,bundle,long_dir in zip(plan["exposures"],(args.first_bundle,args.second_bundle),
                                (args.first_long,args.second_long),strict=True):
    source=pinned(bundle/case["script"],case["sourceSha256"]).decode("utf-8")
    assert source.count(anchor)==1
    result={}
    def capture(chip,group,tile,validate,observed,models):
        assert int(chip) not in result
        result[int(chip)]={int(group[i]["index"]):dict(tile=np.asarray(tile[i]).tolist(),
            errors={name:float(np.linalg.norm(observed[i]-coords[i])) for name,coords in models.items()})
            for i in np.flatnonzero(validate)}
    patch=anchor+'\n                CAPTURE(chip,group,tile,validate,observed,{"translation":translation,"affine":affine})'
    scope={"__name__":"verified_geometry","__file__":str(bundle/case["script"]),"CAPTURE":capture}
    exec(compile(source.replace(anchor,patch),str(bundle/case["script"]),"exec"),scope)
    local=args.output/(case["id"]+"-replay.json")
    scope["main"](args.packages,args.field40,args.cross_depth,args.axis_ledger,
                  long_dir,bundle/"protocollo.json",local)
    assert pinned(local,case["receiptSha256"])==pinned(bundle/"riscontro.json",case["receiptSha256"])
    assert set(result)=={2}
    tables[case["id"]]=result[2]

limit=plan["centerErrorLimitPx"]
labels=("translation","affine")
per_exposure={}
for identifier,source in tables.items():
    rows=list(source.values())
    tiles=sorted({tuple(row["tile"]) for row in rows})
    details={}
    for label in labels:
        residual=[r["errors"][label] for r in rows]
        without=[]
        for tile in tiles:
            remainder=[r["errors"][label] for r in rows if tuple(r["tile"])!=tile]
            without.append(dict(omittedTile=tile,excluded=len(residual)-len(remainder),
                                p90Px=float(np.quantile(remainder,.9))))
        details[label]=dict(fullP90Px=float(np.quantile(residual,.9)),
            casesAboveLimit=sum(float(v)>limit for v in residual),
            tilesContainingCasesAboveLimit=len({tuple(r["tile"]) for r in rows if r["errors"][label]>limit}),
            p90WithoutSingleTile=without,
            diagnosticSubsetsAtOrBelowLimit=sum(w["p90Px"]<=limit for w in without))
    per_exposure[identifier]=dict(heldSources=len(rows),heldTiles=len(tiles),models=details)

first,second=tables["first"],tables["second"]
shared=sorted(first.keys()&second.keys())
assert len(shared)>20 and all(first[i]["tile"]==second[i]["tile"] for i in shared)
overlap={}
for label in labels:
    a={i for i in shared if first[i]["errors"][label]>limit}
    b={i for i in shared if second[i]["errors"][label]>limit}
    overlap[label]=dict(sharedAboveInFirst=len(a),sharedAboveInSecond=len(b),
                        sharedAboveInBoth=len(a&b),heldCommon=len(shared))
r=dict(protocol=plan["schema"],protocolSha256=pin,parentReceiptsExact=True,
       limitPx=limit,originalAdmissionChanged=False,admittedGeometries=0,
       scores=per_exposure,sharedHeldSources=overlap,scientificClosures=0,nativeExecutions=0)
with (args.output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as f:
    json.dump(r,f,indent=2,allow_nan=False)
    f.write("\n")
