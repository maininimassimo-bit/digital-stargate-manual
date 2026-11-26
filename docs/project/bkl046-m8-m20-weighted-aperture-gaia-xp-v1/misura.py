from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser=ArgumentParser()
for key in ("protocol","aperture","phase","weights","photometry","data","packages","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pinned(path,expected):
    data=path.read_bytes()
    require(sha256(data).hexdigest()==expected,f"Changed {path.name}")
    return data


PIN="8c2b5c414179288e9be30f5669b2acb50016a39715c9ef6e804759c98f958c34"
plan=json.loads(pinned(args.protocol,PIN))
path=args.aperture/"misura.py"
source=pinned(path,plan["apertureCode"])
source_report=pinned(args.aperture/"riscontro.json",plan["apertureReport"])
joined=json.loads(pinned(args.phase/"gaia.json",plan["gaiaJoin"]))["M8M20"]["rows"]
optical=json.loads(pinned(args.phase/"passband.json",plan["passband"]))
require(optical["inputSha256"]["prior"]==plan["gaiaJoin"],"Optical predictions use another cohort")
predictions={r["sourceId"]:r for r in optical["fields"]["M8M20"]["perStar"]}
require(len(predictions)==len(joined)==len({r["rawId"] for r in joined}),"Nonunique cohort")
require(all(predictions[r["sourceId"]]["fit"]==r["fit"] for r in joined),"Cohort split changed")

with TemporaryDirectory(dir=args.output.parent) as scratch:
    replay=Path(scratch)/"replay.json"
    old_argv=sys.argv
    sys.argv=[str(path),*map(str,(args.aperture/"protocollo.json",args.weights,
                                 args.photometry,args.data,args.packages,replay))]
    aperture={"__name__":"__main__","__file__":str(path)}
    try:
        exec(compile(source,str(path),"exec"),aperture)
    finally:
        sys.argv=old_argv
    require(replay.read_bytes()==source_report,"Aperture replay changed")

np=aperture["np"]
requested={r["rawId"] for r in joined}
color_rows=defaultdict(dict)
for row in aperture["new"]["rows"]:
    star=row["star"]
    label=row["parity"]
    if label not in ("R","B") or star not in requested:
        continue
    key=(star,row["member"])
    require(label not in color_rows[key],"Duplicated aperture observation")
    color_rows[key][label]=np.array(row["flux"])
measurements=defaultdict(list)
for (star,member),bands in color_rows.items():
    if len(bands)==2:
        require((bands["R"]>0).all() and (bands["B"]>0).all(),"Nonpositive accepted flux")
        measurements[star].append(-2.5*np.log10(bands["B"]/bands["R"]))
require(measurements.keys()==requested,"Gaia cohort incomplete")
counts=np.array([len(measurements[r["rawId"]]) for r in joined])
require(min(counts)>=plan["minimumPairedPosesPerStar"],"Too few paired exposures")
data=np.array([np.median(measurements[r["rawId"]],axis=0) for r in joined])
fit=np.array([r["fit"] for r in joined],dtype=bool)
require(fit.sum()==plan["train"] and (~fit).sum()==plan["test"],"Unexpected field coverage")
heldout=[i for i,flag in enumerate(fit) if not flag]
shift=np.quantile(np.abs(data[~fit,:,1]-data[~fit,:,0]),.9,axis=0)
results={}
for response in plan["models"]:
    expected=np.array([predictions[r["sourceId"]]["colors"][response] for r in joined])
    zero=float(np.median(data[fit,0,0]-expected[fit]))
    error=data[~fit]-(expected[~fit]+zero)[:,None,None]
    metrics=np.quantile(np.abs(error),.9,axis=0)
    results[response]=dict(
        sharedOffsetMag=zero, p90AbsResidualMag=metrics.tolist(),
        medianSignedResidualMag=np.median(error,axis=0).tolist(),
        deltaP90WeightedMinusUnitMag=(metrics[:,1]-metrics[:,0]).tolist(),
        heldout=[dict(sourceId=joined[i]["sourceId"],pairedExposures=int(counts[i]),
                      residualMag=e.tolist()) for i,e in zip(heldout,error,strict=True)],
    )
report=dict(schema=plan["schema"],protocolSha256=PIN,apertureReplayIdentical=True,
            training=int(fit.sum()),heldout=int((~fit).sum()),pairedApertures=int(counts.sum()),
            pairedExposuresPerStar=[int(counts.min()),int(counts.max())],
            calibrationOrder=["A","B"],centerOrder=["unit","weighted"],
            heldoutShiftAbsP90Mag=shift.tolist(),models=results,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
