"""Compare target and neighborhood angle selection across two NGC 6341 exposures."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import file_digest, sha256
from itertools import product
import json
from pathlib import Path
from statistics import median
import sys


def need(ok,why):
    if not ok:
        raise ValueError(why)


def read(path,pin):
    data=path.read_bytes()
    need(sha256(data).hexdigest()==pin,"Changed bytes: "+path.name)
    return data


def library(np,x,y,parameters):
    q,angle,width,beta=parameters.T
    angle=np.deg2rad(angle)
    c,s=np.cos(angle),np.sin(angle)
    scale=width/(2*np.sqrt(2**(1/beta)-1))
    ans=np.zeros((len(x),len(q)))
    for dx,dy in product((-1/3,0.,1/3),repeat=2):
        u=(x[:,None]+dx)*c+(y[:,None]+dy)*s
        v=-(x[:,None]+dx)*s+(y[:,None]+dy)*c
        ans+=(1+(q*u*u+v*v/q)/scale**2)**(-beta)
    return ans/9


def loss(np,image,quality,seed,params,plan):
    cx,cy=seed
    left,top=int(np.floor(cx))-5,int(np.floor(cy))-5
    if left<0 or top<0 or left+11>image.shape[1] or top+11>image.shape[0]:
        return "EDGE",None
    patch=image[top:top+11,left:left+11]
    dq=quality[top:top+11,left:left+11]
    x,y=np.meshgrid(np.arange(left,left+11)-cx,np.arange(top,top+11)-cy)
    aperture=x*x+y*y<=plan["radius"]**2
    if ((dq[aperture]&256)!=0).any():
        return "SATURATED_DQ",None
    good=aperture&(dq==0)&np.isfinite(patch)
    if good.sum()<plan["minValid"]:
        return "INSUFFICIENT_SUPPORT",None
    x,y,z=x[good],y[good],patch[good].astype(float)
    design=np.column_stack((np.ones(len(x)),x/5,y/5))
    qr,_=np.linalg.qr(design)
    target=z-qr@(qr.T@z)
    templates=library(np,x,y,params)
    models=templates-qr@(qr.T@templates)
    norms=(models**2).sum(axis=0)
    cross=models.T@target
    energy=float(np.sum((z-z.mean())**2))
    if energy<=0 or (norms<=0).any():
        return "DEGENERATE_FIT",None
    out=np.maximum(0,float(target@target)-cross**2/norms)/energy
    out[cross<=0]=np.inf
    return "MEASURED",out


def analyze(np,stars,params):
    groups=defaultdict(list)
    for row in stars:
        groups[tuple(row["zone"])].append(row)
    circle=np.flatnonzero(params[:,0]==1)
    ell=np.flatnonzero(params[:,0]<1)
    bank={int(angle):np.flatnonzero((params[:,1]==angle)&(params[:,0]<1)) for angle in sorted(set(params[ell,1]))}
    rows=[]
    for group in groups.values():
        for target in group:
            for j in (0,1):
                result=dict(star=target["star"],chip=target["chip"],zone=target["zone"],trainingExposure=j)
                train,held=target["loss"][j],target["loss"][1-j]
                peers=[r for r in group if r is not target and r["loss"][j] is not None]
                result["trainingPeers"]=len(peers)
                if train is None or held is None:
                    result.update(state="REFERENCE_REJECTED",supportStates=target["states"])
                elif not peers:
                    result.update(state="NO_ZONE_PEERS")
                else:
                    scores={k:float(np.mean([np.min(r["loss"][j][indices]) for r in peers])) for k,indices in bank.items()}
                    angle=min(scores,key=lambda k:(scores[k],k))
                    idx=[int(indices[np.argmin(train[indices])]) for indices in (circle,ell,bank[angle])]
                    if not np.isfinite(scores[angle]) or not np.all(np.isfinite(train[idx])) or not np.all(np.isfinite(held[idx])) or held[idx[0]]<=0:
                        result.update(state="INVALID_POSITIVE_AMPLITUDE")
                    else:
                        cir,own,regional=map(float,held[idx])
                        result.update(state="MEASURED",ownAngle=float(params[idx[1],1]),zoneAngle=angle,
                                      ownGain=(cir-own)/cir,zoneGain=(cir-regional)/cir,ownMinusZone=(regional-own)/cir)
                rows.append(result)
    return rows


def main():
    cli=ArgumentParser(description=__doc__)
    for key in ("protocol","positions","exposures","dependencies","output"):
        cli.add_argument(key,type=Path)
    a=cli.parse_args()
    raw=a.protocol.read_bytes()
    p=json.loads(raw)
    positions=json.loads(read(a.positions,p["positions"]))["records"]
    need(len(positions)==736,"Star roster changed")
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    need((np.__version__,astropy.__version__)==("2.3.5","7.2.0"),"Library versions")
    params=np.array([(q,angle,w,b) for q in p["ratios"]
       for angle in ([0] if q==1 else range(0,180,p["angleStep"])) for w,b in product(p["fwhm"],p["betas"])])
    stars=[dict(star=i,chip=None,zone=None,states=[],loss=[]) for i in range(len(positions))]
    for j,(name,pin) in enumerate(p["files"].items()):
        path=a.exposures/name
        with path.open("rb") as f:
            need(file_digest(f,"sha256").hexdigest()==pin,"FLC changed")
        with fits.open(path,mode="readonly",memmap=True) as hdus:
            header=hdus[0].header
            need(header["FILTER1"]=="F606W" and header["PROPOSID"]==9453
                 and header["EXPTIME"]==[5.,90.][j],"Filter or exposure changed")
            for i,position in enumerate(positions):
                ext=position["scienceExtver"]
                chip=hdus["SCI",ext].header["CCDCHIP"]
                seed=position["centers"][j]
                result=stars[i]
                if j==0:
                    result["chip"]=chip
                    x,y=seed
                    result["zone"]=[chip,int(x)//p["zonePixels"],int(y)//p["zonePixels"]]
                else:
                    need(chip==result["chip"],"Physical chip changed")
                label,score=loss(np,hdus["SCI",ext].data,hdus["DQ",ext].data,seed,params,p)
                result["states"].append(label)
                result["loss"].append(score)
    rows=analyze(np,stars,params)
    need(len(rows)==1472,"Direction coverage")
    summary=[]
    for chip in sorted({r["chip"] for r in rows}):
        for j in (0,1):
            cohort=[r for r in rows if (r["chip"],r["trainingExposure"])==(chip,j)]
            accepted=[r for r in cohort if r["state"]=="MEASURED"]
            summary.append(dict(chip=chip,trainingExposure=[5,90][j],states=Counter(r["state"] for r in cohort),
              ownGainMedian=median(r["ownGain"] for r in accepted),zoneGainMedian=median(r["zoneGain"] for r in accepted),
              ownMinusZoneMedian=median(r["ownMinusZone"] for r in accepted),
              ownStrictlyBetter=sum(r["ownMinusZone"]>1e-12 for r in accepted),
              ownStrictlyWorse=sum(r["ownMinusZone"]<-1e-12 for r in accepted)))
    result=dict(schema=p["schema"],protocolSha256=sha256(raw).hexdigest(),programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                summary=summary,rows=rows,nativeExecutions=0,scientificClosures=0)
    with a.output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()