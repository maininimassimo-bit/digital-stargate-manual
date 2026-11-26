"""Compare held-out input covariance against the independent-input Roman baseline."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import ModuleType


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path,pin):
    raw=path.read_bytes()
    require(sha(raw)==pin,"Input changed: "+path.name)
    return raw


def load_tiles(np,root,captures,band,frames):
    files=[r for r in captures if r["band"]==band]
    require(len(files)==80,"Expected 80 captured band ranges")
    frames_by_exposure={}
    rails=np.zeros((32,64,64),dtype=bool)
    for row in files:
        i,j=row["exposure"],row["frame"]
        name=f"{band}-E{i:03}-r{j:02}.bin"
        require(row["file"]==name and (i,j) not in frames_by_exposure,"Duplicate or changed range")
        raw=read(root/name,row["sha256"])
        data=np.frombuffer(raw,dtype=">i2").reshape(64,4224).astype(np.float64)+32768
        tiles=data[:,:4096].reshape(64,32,128)[:,:,32:96].swapaxes(0,1)
        rails|=(tiles==0)|(tiles==65535)
        frames_by_exposure[i,j]=tiles
    require(set(frames_by_exposure)=={(i,j) for i in range(1,21) for j in frames},"Band coverage")
    return frames_by_exposure,rails


def block_covariance(np,image,usable):
    sample=image[:63,:63].reshape(21,3,21,3).swapaxes(1,2).reshape(21,21,9)[usable]
    require(len(sample)>=360,"Insufficient training blocks")
    cov=np.cov(sample,rowvar=False,ddof=1)
    mean_var=np.trace(cov)/9
    require(mean_var>0,"Nonpositive input variance")
    return cov/mean_var


def compare(np,kernel,tiles,rails,prior,frames,band):
    result=[]
    w=np.outer([.5,1,.5],[.5,1,.5]).reshape(9)
    require(float(w@w)==2.25,"Unexpected weight gain")
    supports=[kernel.plan_support(np,rail) for rail in rails]
    training_masks=[~r[:63,:63].reshape(21,3,21,3).swapaxes(1,2).any(axis=(2,3)) for r in rails]
    for j in frames[1:]:
        for c,(mask,support) in enumerate(supports):
            a=[tiles[i,j][c]-tiles[i,0][c] for i in range(1,21)]
            pairs=list(zip(a[::2],a[1::2],strict=True))
            shapes=[block_covariance(np,(second-first)/np.sqrt(2),training_masks[c]) for first,second in pairs]
            for p,(first,second) in enumerate(pairs):
                ref=prior[2*p+1,j,c]
                require(ref["state"]=="MEASURED","Prior support changed")
                m=kernel.evaluate(np,first,second,mask,support)
                np.testing.assert_allclose([m["inputVariance"],m["sumVariance"],m["fullError"]],
                    [ref["inputVariance"],ref["sumVariance"],ref["fullError"]],rtol=1e-12)
                train=[s for i,s in enumerate(shapes) if i!=p]
                require(len(train)==9,"Wrong training cohort")
                predicted=m["inputVariance"]*(w@np.mean(train,axis=0)@w)
                require(predicted>0,"Nonpositive covariance prediction")
                result.append(dict(band=band,frame=j,channel=c,firstExposure=2*p+1,
                    independentError=m["fullError"],learnedError=float(abs(predicted/m["sumVariance"]-1)),
                    trainingPatches=int(training_masks[c].sum())))
    return result


def summarize(np,rows,bands,frames):
    result=[]
    for band in bands:
        for j in frames[1:]:
            data=[r for r in rows if (r["band"],r["frame"])==(band,j)]
            require(len(data)==320,"Missing comparisons")
            a=np.asarray([r["independentError"] for r in data])
            b=np.asarray([r["learnedError"] for r in data])
            ch=np.asarray([r["channel"] for r in data])
            first=np.asarray([r["firstExposure"] for r in data])
            result.append(dict(band=band,frame=j,comparisons=len(data),independentMedian=float(np.median(a)),
                learnedMedian=float(np.median(b)),independentP95=float(np.quantile(a,.95)),learnedP95=float(np.quantile(b,.95)),
                channelsImproved=sum(bool(np.median(b[ch==c])<np.median(a[ch==c])) for c in range(32)),
                heldPairsImproved=sum(bool(np.median(b[first==i])<np.median(a[first==i])) for i in range(1,21,2))))
    return result


def save(path,obj):
    raw=(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    with path.open("xb") as f:
        f.write(raw)
    return sha(raw)


def main():
    cli=ArgumentParser(description=__doc__)
    for name in ("policy","spatial","channels","dependencies","output"):
        cli.add_argument(name,type=Path)
    args=cli.parse_args()
    raw=args.policy.read_bytes()
    cfg=json.loads(raw)
    src=args.spatial/"cattura"
    capture=json.loads(read(src/"acquisizione.json",cfg["captureSHA"]))
    previous=json.loads(read(args.spatial/"riscontro.json",cfg["spatialReportSHA"]))
    kernel=ModuleType("kernel")
    prog=args.channels/"misura.py"
    exec(compile(read(prog,cfg["channelsProgramSHA"]),str(prog),"exec"),vars(kernel))
    sys.path.insert(0,str(args.dependencies))
    import numpy as np
    require(np.__version__=="2.3.5","Unexpected NumPy")
    frames=cfg["frames"]
    rows=[]
    for band in cfg["bands"]:
        prior={(r["firstExposure"],r["frame"],r["channel"]):r for r in previous["newBandComparisons"][band]}
        tiles,rails=load_tiles(np,src/"source",capture["captures"],band,frames)
        rows.extend(compare(np,kernel,tiles,rails,prior,frames,band))
    require(len(rows)==1920,"Total count")
    args.output.mkdir()
    detail=save(args.output/"tutti-gli-esiti.json",rows)
    save(args.output/"riscontro.json",dict(schema=cfg["schema"],protocolSha256=sha(raw),
         programSha256=sha(Path(__file__).read_bytes()),detailSha256=detail,phase=cfg["phase"],
         trainingPairsPerFold=9,verifiedParentComparisons=len(rows),summary=summarize(np,rows,cfg["bands"],frames),
         incidentDoseVerified=False,nativeExecutions=0,scientificClosures=0))


if __name__=="__main__":
    main()