"""Stress fixed NGC 6341 shape choices with validation-only template shifts."""
import argparse
from collections import Counter
from hashlib import file_digest, sha256
from itertools import product
import json
from pathlib import Path
from statistics import median
import sys
from types import ModuleType


def need(ok,why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path,pin):
    raw=path.read_bytes()
    need(sha(raw)==pin,"Changed bytes: "+path.name)
    return raw


def save(path,obj):
    raw=(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    with path.open("xb") as f:
        f.write(raw)
    return sha(raw)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for n in ("plan","parent","dependencies","output"):
        cli.add_argument(n,type=Path)
    a=cli.parse_args()
    policy=a.plan.read_bytes()
    cfg=json.loads(policy)
    program=a.parent/"misura.py"
    source=read(program,cfg["parentProgram"]).decode()
    changes=(("def loss(np,image,quality,seed,params,plan):","def loss(np,image,quality,seed,params,plan,shift):"),
             ("    templates=library(np,x,y,params)","    templates=library(np,x-shift[0],y-shift[1],params)"))
    for old,new in changes:
        need(source.count(old)==1,"Template hook changed")
        source=source.replace(old,new)
    parent=ModuleType("parent")
    exec(compile(source,str(program),"exec"),vars(parent))
    p=json.loads(read(a.parent/"protocollo.json",cfg["parentProtocol"]))
    reference=json.loads(read(a.parent/"riscontro.json",cfg["parentReport"]))
    positions=json.loads(read(a.parent/"posizioni.json",p["positions"]))["records"]
    need(len(positions)==736,"Position roster changed")
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    need((np.__version__,astropy.__version__)==("2.3.5","7.2.0"),"Runtime changed")
    levels=cfg["shiftsPx"]
    params=np.array([(q,angle,w,b) for q in p["ratios"]
        for angle in ([0] if q==1 else range(0,180,p["angleStep"]))
        for w,b in product(p["fwhm"],p["betas"])])
    stars=[dict(star=i,states=[],zone=None,chip=None,loss=[]) for i in range(len(positions))]
    for e,(name,pin) in enumerate(p["files"].items()):
        path=a.parent/name
        with path.open("rb") as f:
            need(file_digest(f,"sha256").hexdigest()==pin,"FLC changed")
        with fits.open(path,mode="readonly",memmap=True) as hdus:
            for star,pos in zip(stars,positions,strict=True):
                ext=pos["scienceExtver"]
                sci,dq=hdus["SCI",ext],hdus["DQ",ext]
                c=sci.header["CCDCHIP"]
                seed=pos["centers"][e]
                if e==0:
                    star["chip"]=c
                    star["zone"]=[c,int(seed[0])//p["zonePixels"],int(seed[1])//p["zonePixels"]]
                else:
                    need(star["chip"]==c,"Physical CCD changed")
                l=[parent.loss(np,sci.data,dq.data,seed,params,p,shift) for shift in levels]
                need(len({status for status,_ in l})==1,"Validation support changed")
                star["states"].append(l[0][0])
                star["loss"].append([scores for _,scores in l])
    def fit(direction, variant):
        return [dict(star,loss=[star["loss"][e][0 if e==direction else variant] for e in (0,1)])
                for star in stars]

    def key(r):
        return r["star"],r["trainingExposure"]

    metrics=("ownGain","zoneGain","ownMinusZone")
    ref={key(row):row for row in reference["rows"]}
    by_level=[]
    for k,shift in enumerate(levels):
        combined={}
        for direction in (0,1):
            rows=parent.analyze(np,fit(direction,k),params)
            combined.update({key(r):r for r in rows if r["trainingExposure"]==direction})
        need(combined.keys()==ref.keys(),"Comparison roster changed")
        if k==0:
            for ident,actual in combined.items():
                old=ref[ident]
                need({k:v for k,v in actual.items() if k not in metrics}==
                     {k:v for k,v in old.items() if k not in metrics},"Zero-shift case changed")
                if actual["state"]=="MEASURED":
                    np.testing.assert_allclose([actual[m] for m in metrics],[old[m] for m in metrics],rtol=0,atol=1e-12)
        by_level.append(combined)
    paired={i for i in ref if all(r[i]["state"]=="MEASURED" for r in by_level)}
    summary=[]
    for k,all_rows in enumerate(by_level):
        for chip in (1,2):
            for e in (0,1):
                subset=[r for r in all_rows.values() if (r["chip"],r["trainingExposure"])==(chip,e)]
                valid=[r for r in subset if key(r) in paired]
                summary.append(dict(shift=levels[k],chip=chip,trainingExposure=[5,90][e],
                     coverage=dict(Counter(r["state"] for r in subset)),commonCases=len(valid),
                     ownGainMedian=median(r["ownGain"] for r in valid),
                     zoneGainMedian=median(r["zoneGain"] for r in valid),
                     ownMinusZoneMedian=median(r["ownMinusZone"] for r in valid)))
    a.output.mkdir()
    detail=save(a.output/"tutti-gli-esiti.json",[list(rows.values()) for rows in by_level])
    save(a.output/"riscontro.json",dict(schema=cfg["schema"],protocolSha256=sha(policy),
        programSha256=sha(Path(__file__).read_bytes()),parentReportSha256=cfg["parentReport"],detailSha256=detail,
        baselineComparisons=len(ref),shiftCount=len(levels),summary=summary,
        centerUncertaintyCalibrated=False,nativeExecutions=0,scientificClosures=0))


if __name__=="__main__":
    main()