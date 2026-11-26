from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser=ArgumentParser()
for name in ("protocol","source","calibrators","packages","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pin(path,expected):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==expected,f"Changed {path.name}")
    return raw


PIN="1f0eb0df5e381a65cc9063ed3b0912caeac43b255829266c00c1b2fbe8ee3697"
plan=json.loads(pin(args.protocol,PIN))
path=args.source/"misura.py"
raw=pin(path,plan["sourceCode"])
baseline=pin(args.source/"riscontro.json",plan["sourceReport"])
with TemporaryDirectory(dir=args.output.parent) as temp:
    replay=Path(temp)/"replay.json"
    saved=sys.argv
    sys.argv=[str(path),*map(str,(args.source/"protocollo.json",args.calibrators,args.packages,replay))]
    incoming={"__name__":"__main__"}
    try:
        exec(compile(raw,str(path),"exec"),incoming)
    finally:
        sys.argv=saved
    require(replay.read_bytes()==baseline,"Flat variance replay changed")

np=incoming["np"]
flats,darks,mask=(incoming[name] for name in ("flats","dark","mask"))
roles,tiles=incoming["roles"],incoming["train_tiles"]
prior=incoming["rows"]
parities=incoming["plan"]["parities"]
width=plan["window"]
require(width==7,"Wrong window geometry")
sources={(r["pair"],r["parity"],r["tile"]):r for r in prior}
shifts=np.arange(width)-width//2
y,x=np.meshgrid(shifts,shifts,indexing="ij")

def kernel(size):
    core=np.maximum(abs(x),abs(y))<=size//2
    border=np.maximum(abs(x),abs(y))==width//2
    coefficients=np.zeros_like(x,dtype=float)
    coefficients[core]=1
    coefficients[border]=-float(core.sum())/border.sum()
    np.testing.assert_allclose([coefficients.sum(),(coefficients*x).sum(),(coefficients*y).sum()],
                               [0,0,0],atol=1e-14,rtol=0)
    return coefficients.ravel()


weights={r:kernel(r) for r in plan["apertures"]}
for v in weights.values():
    scale=np.arange(1.,50.)
    truth=np.diag(scale)
    np.testing.assert_allclose(v@truth@v,np.sum(v*v*scale),atol=1e-12,rtol=0)


def windows(array):
    q=array.shape[-1]//width
    edge=q*width
    return array[:edge,:edge].reshape(q,width,q,width).transpose(0,2,1,3).reshape(q*q,width**2)


def ratio(data,vector):
    diag=float(np.var(data,axis=0,ddof=1)@(vector*vector))
    empirical=float(np.var(data@vector,ddof=1))
    require(diag>0 and empirical>0,"Degenerate aperture estimate")
    return float(np.sqrt(empirical/diag))


rows=[]
for pair in range(len(roles)):
    for t,trained in enumerate(tiles):
        for c,parity in enumerate(parities):
            reference=sources[pair,parity,t]
            alpha=reference["illuminationRatio"]
            a,b=flats[pair,:,t,c]
            d1,d2=darks[pair,:,t,c]
            valid=mask[t,c]&(a<incoming["plan"]["rawSaturationAdu"])&(b<incoming["plan"]["rawSaturationAdu"])
            accepted=windows(valid).all(axis=1)
            require(int(valid.sum())==reference["usableSamples"],"Changed physical sample mask")
            require(accepted.sum()>=plan["minimumWindows"],"Incomplete compensated window support")
            fields=dict(flat=(a-alpha*b)/np.sqrt(1+alpha**2),shortDark=(d1-d2)/np.sqrt(2))
            for kind,field in fields.items():
                samples=windows(field)[accepted]
                values={str(size):ratio(samples,v) for size,v in weights.items()}
                rows.append(dict(pair=pair,tile=t,parity=parity,frameType=kind,
                                 trainPair=bool(roles[pair]),trainTile=bool(trained),
                                 completeWindows=int(accepted.sum()),stdRatio=values))

summary={}
for parity in parities:
    summary[parity]={}
    for kind in ("flat","shortDark"):
        group=[r for r in rows if r["parity"]==parity and r["frameType"]==kind]
        train=[r for r in group if r["trainPair"] and r["trainTile"]]
        test=[r for r in group if not r["trainPair"] and not r["trainTile"]]
        require(len(train)==72 and len(test)==51,"Changed exposure/space transfer cohort")
        arms={}
        for size in plan["apertures"]:
            key=str(size)
            estimate=float(np.median([r["stdRatio"][key] for r in train]))
            result=np.array([r["stdRatio"][key] for r in test])
            def error(pred):
                return float(np.quantile(np.abs(result-pred)/result,.9)*100.)
            arms[key]=dict(trainingFactor=estimate,heldoutMedianFactor=float(np.median(result)),
                          diagonalRelativeP90Pct=error(1.),trainedFactorRelativeP90Pct=error(estimate))
        summary[parity][kind]=dict(training=len(train),heldout=len(test),kernels=arms)

report=dict(schema=plan["schema"],protocolSha256=PIN,sourceVarianceReplayIdentical=True,
            smallestCompleteWindowSet=min(r["completeWindows"] for r in rows),
            summary=summary,rows=rows,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
