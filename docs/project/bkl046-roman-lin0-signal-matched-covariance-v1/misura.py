"""Compare covariance-shape transfer from GAIN to LIN0."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import ModuleType


def need(ok,reason):
    if not ok: raise ValueError(reason)


def sha(raw): return sha256(raw).hexdigest()


def checked(path,pin):
    raw=path.read_bytes()
    need(sha(raw)==pin,"Changed input: "+path.name)
    return raw


def module(path,raw):
    m=ModuleType(path.stem)
    exec(compile(raw,str(path),"exec"),vars(m))
    return m


def decode(np,root,rows,band,n,frames):
    frames_by_exposure={}
    rail=np.zeros((32,64,64),bool)
    for row in rows:
        if row["band"]!=band: continue
        i,j=row["exposure"],row["frame"]
        name=f"{band}-E{i:03}-r{j:02}.bin"
        need(row["file"]==name and (i,j) not in frames_by_exposure,"Range identity")
        v=np.frombuffer(checked(root/name,row["sha256"]),dtype=">i2").reshape(64,4224)
        tiles=v[:,:4096].reshape(64,32,128)[:,:,32:96].swapaxes(0,1)
        rail|=(tiles==-32768)|(tiles==32767)
        frames_by_exposure[i,j]=tiles.astype(float)+32768
    need(set(frames_by_exposure)=={(i,j) for i in range(1,n+1) for j in frames},"Range coverage")
    return frames_by_exposure,rail


def pair_images(tiles,j,c,n):
    points=[tiles[i,j][c]-tiles[i,0][c] for i in range(1,n+1)]
    return list(zip(points[::2],points[1::2],strict=True))


def shapes(np,pairs,train):
    values=[]
    for a,b in pairs:
        v=((b-a)/np.sqrt(2.))[:63,:63].reshape(21,3,21,3).swapaxes(1,2).reshape(21,21,9)
        cov=np.cov(v[train],rowvar=False,ddof=1)
        need(np.trace(cov)>0,"Nonpositive input variance")
        values.append(9*cov/np.trace(cov))
    return np.stack(values)


def evaluate(np,kernel,base,target,raw_mask,cfg,band):
    w=np.outer([.5,1,.5],[.5,1,.5]).ravel()
    rows=[]
    support=[]
    for c,rail in enumerate(raw_mask):
        mask,used=kernel.plan_support(np,rail)
        train=~rail[:63,:63].reshape(21,3,21,3).swapaxes(1,2).any(axis=(2,3))
        n=int(mask.sum())
        support.append(dict(band=band,channel=c,retainedBlocks=n,trainingBlocks=int(train.sum())))
        source={}
        if n>=cfg["minimumSupportBlocks"]:
            need(train.sum()>=360,"Insufficient training support")
            for j in cfg["frames"][1:]:
                pairs=pair_images(base,j,c,20)
                level=float(np.median([np.mean((a+b)[:63,:63][used]/2) for a,b in pairs]))
                source[j]=(level,shapes(np,pairs,train).mean(axis=0))
            ordered=sorted(source.values(),key=lambda row:row[0])
            source_levels=[level for level,_ in ordered]
            need(source_levels==[source[j][0] for j in cfg["frames"][1:]]
                 and len(set(source_levels))==3,"Unexpected GAIN signal ordering")
        for j in cfg["frames"][1:]:
            pairs=pair_images(target,j,c,30)
            if n>=cfg["minimumSupportBlocks"]:
                target_shapes=shapes(np,pairs,train)
            for i,(a,b) in enumerate(pairs):
                row=dict(band=band,channel=c,frame=j,firstExposure=2*i+1)
                if n<cfg["minimumSupportBlocks"]:
                    row.update(state="INSUFFICIENT_UNCLIPPED_SUPPORT")
                else:
                    m=kernel.evaluate(np,a,b,mask,used)
                    internal=np.delete(target_shapes,i,axis=0).mean(axis=0)
                    ref=m["inputVariance"]/m["sumVariance"]
                    signal=m["signal"]
                    row.update(state="MEASURED",signal=signal,independentError=m["fullError"],
                        gainError=float(abs(ref*(w@source[j][1]@w)-1)),
                        lin0Error=float(abs(ref*(w@internal@w)-1)))
                    if signal<source_levels[0] or signal>source_levels[-1]:
                        row["signalMatch"]={"state":"OUTSIDE_GAIN_RANGE"}
                    else:
                        k=min(int(np.searchsorted(source_levels,signal,side="right")),len(ordered)-1)
                        lo,lshape=ordered[k-1]
                        hi,hshape=ordered[k]
                        f=(signal-lo)/(hi-lo)
                        shape=(1-f)*lshape+f*hshape
                        row["signalMatch"]=dict(state="MEASURED",lowerADU=lo,upperADU=hi,upperWeight=f,
                                                 error=float(abs(ref*(w@shape@w)-1)))
                rows.append(row)
    return rows,support


def summarize(np,rows,cfg):
    result=[]
    for band in cfg["bands"]:
        for j in cfg["frames"][1:]:
            base=[r for r in rows if (r["band"],r["frame"])==(band,j)]
            accepted=[r for r in base if r.get("signalMatch",{}).get("state")=="MEASURED"]
            item=dict(band=band,frame=j,combinations=len(base),signalMatched=len(accepted),
                      outsideGainRange=sum(r.get("signalMatch",{}).get("state")=="OUTSIDE_GAIN_RANGE" for r in base))
            if accepted:
                median=lambda field:float(np.median([r[field] for r in accepted]))
                item.update(independentMedian=median("independentError"),sameIndexGainMedian=median("gainError"),
                            matchedGainMedian=float(np.median([r["signalMatch"]["error"] for r in accepted])),
                            otherLin0Median=median("lin0Error"),targetSignalMedian=median("signal"),
                            improvedVsSameIndex=sum(r["signalMatch"]["error"]<r["gainError"] for r in accepted))
            result.append(item)
    return result

def save(path,obj):
    raw=(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    with path.open("xb") as f: f.write(raw)
    return sha(raw)


def main():
    cli=ArgumentParser(description=__doc__)
    for n in ("root","gain_bands","gain_ramp","channels","dependencies","output"):
        cli.add_argument(n,type=Path)
    cli.add_argument("capture_pin")
    cli.add_argument("policy",type=Path)
    a=cli.parse_args()
    new_policy=a.policy.read_bytes()
    policy=json.loads(new_policy)
    p=checked(a.root/"protocollo.json",policy["parentPlan"])
    cfg=json.loads(p)
    lin0_root=a.root/"cattura"
    lin=json.loads(checked(lin0_root/"acquisizione.json",a.capture_pin))
    acq=a.root/"acquisisci.py"
    loader=module(acq,checked(acq,lin["programSha256"]))
    need(lin["protocolSha256"]==sha(p),"Protocol lineage")
    gain_bands=a.gain_bands/"cattura"
    gain=json.loads(checked(gain_bands/"acquisizione.json",cfg["gainCapture"]))
    gain_ramp=json.loads(checked(a.gain_ramp/"acquisizione.json",gain["sourceCaptureSha256"]))
    prog=a.channels/"misura.py"
    kernel=module(prog,checked(prog,cfg["channelKernel"]))
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    from astropy.io import fits
    need(np.__version__=="2.3.5","NumPy version")
    limb=[]
    seen=set()
    metas=[]
    need([r["exposure"] for r in lin["records"]]==list(range(1,31)),"LIN0 roster")
    for record in lin["records"]:
        i=record["exposure"]
        name=f"21816_E{i:03}.fits"
        h,*members=record["members"]
        need(record["url"]==cfg["base"]+name and h["file"]==f"E{i:03}-header.bin"
             and h["offset"]==0 and h["bytes"]==17280 and len(members)==8,"LIN0 lineage")
        at,meta=loader.parse(checked(lin0_root/"source"/h["file"],h["sha256"]),fits,name)
        need(at==record["dataOffset"] and meta==record["meta"],"LIN0 header linkage")
        seen.add(h["file"])
        metas.append(meta)
        for m in members:
            start,stop=cfg["bands"][m["band"]]
            j=m["frame"]
            need(j in cfg["frames"] and m["offset"]==at+2*4224*(j*4096+start)
                 and m["bytes"]==2*4224*(stop-start) and m["file"] not in seen,"LIN0 byte range")
            seen.add(m["file"])
            limb.append(dict(m,exposure=i))
    need(len(seen)==270 and {p.name for p in (lin0_root/"source").iterdir()}==seen,"LIN0 captured set")
    dates=[m["DATE-BEG"] for m in metas]
    need(dates==sorted(set(dates)) and dates[-1]<gain_ramp["records"][0]["metadata"]["DATE-BEG"],
         "Expected separate chronological acquisitions")
    rows=[]
    support=[]
    for band in cfg["bands"]:
        x,rx=decode(np,gain_bands/"source",gain["captures"],band,20,cfg["frames"])
        y,ry=decode(np,lin0_root/"source",limb,band,30,cfg["frames"])
        r,s=evaluate(np,kernel,x,y,rx|ry,cfg,band)
        rows.extend(r)
        support.extend(s)
    reference=[{k:v for k,v in row.items() if k!="signalMatch"} for row in rows]
    expected=json.loads(checked(a.root/"tutti-gli-esiti.json",policy["parentDetail"]))
    need(len(reference)==len(expected)==2880,"Parent detail coverage")
    metrics=("signal","independentError","gainError","lin0Error")
    for observed,prior in zip(reference,expected,strict=True):
        need({k:v for k,v in observed.items() if k not in metrics}==
             {k:v for k,v in prior.items() if k not in metrics},"Parent row identity")
        if observed["state"]=="MEASURED":
            np.testing.assert_allclose([observed[k] for k in metrics],[prior[k] for k in metrics],rtol=1e-12)
    a.output.mkdir()
    detail=save(a.output/"tutti-gli-esiti.json",rows)
    save(a.output/"riscontro.json",dict(schema=policy["schema"],programSha256=sha(Path(__file__).read_bytes()),
         protocolSha256=sha(new_policy),parentDetailSha256=policy["parentDetail"],detailSha256=detail,
         captureSha256=a.capture_pin,verifiedParentComparisons=len(reference),summary=summarize(np,rows,cfg),
         calibratedDoseMatched=False,nativeExecutions=0,scientificClosures=0))



if __name__=="__main__":
    main()