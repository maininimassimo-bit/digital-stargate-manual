
import hashlib
import io
import json
from pathlib import Path
import sys

root,runtime,previous,output=map(Path,sys.argv[1:])
sys.path.insert(0,str(runtime))
import astropy
from astropy.io import fits
import numpy as np


def read(path,pin):
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=pin:
        raise ValueError(f"Changed input: {path.name}")
    return data


def nodes(header,key,count):
    return np.array([header[f"{key}{i:02d}"] for i in range(1,count+1)],float)


def loc_psfs(cube,header,xy,chip):
    # On the STScI WFC grid the first five Y rows are chip WFC2 (SCI,1).
    xx=nodes(header,"IPSFX",9)
    yy=nodes(header,"JPSFY",10)
    start=0 if chip==2 else 5
    yy=yy[start:start+5]-(2048 if chip==1 else 0)
    x,y=np.array(xy,dtype=float)+1
    if not (xx[0]<=x<=xx[-1] and yy[0]<=y<=yy[-1]):
        raise ValueError("Source outside calibrated PSF grid")
    i=np.clip(np.searchsorted(xx,x)-1,0,7)
    j=np.clip(np.searchsorted(yy,y)-1,0,3)
    u=(x-xx[i])/(xx[i+1]-xx[i])
    v=(y-yy[j])/(yy[j+1]-yy[j])
    k=9*(start+j)+i
    return ((1-v)*((1-u)*cube[:,k]+u*cube[:,k+1])+v*((1-u)*cube[:,k+9]+u*cube[:,k+10]))


def interp(psf,dx,dy):
    x,y=50+4*dx,50+4*dy
    inside=(x>=0)&(x<100)&(y>=0)&(y<100)
    x,y=np.where(inside,x,0),np.where(inside,y,0)
    i,j=x.astype(int),y.astype(int)
    a,b=x-i,y-j
    z=(1-b)*((1-a)*psf[j,i]+a*psf[j,i+1])+b*((1-a)*psf[j+1,i]+a*psf[j+1,i+1])
    return np.where(inside,z,0)


def trial(psf,xy,z,sigma,rows,params,cfg):
    coords=np.asarray(params).reshape(-1,2)
    radii=np.linalg.norm(coords,axis=1)
    if np.max(radii)>cfg["centerBoundPx"]:
        return None
    if len(coords)==2:
        d=np.linalg.norm(coords[0]-coords[1])
        if d<cfg["separationBoundsPx"][0] or d>cfg["separationBoundsPx"][1]:
            return None
    design=np.column_stack([*(interp(psf,xy[:,0]-x,xy[:,1]-y) for x,y in coords),
                            np.ones(len(xy)),xy])
    a=design[rows]/sigma[rows,None]
    b=z[rows]/sigma[rows]
    coefficients,_,rank,_=np.linalg.lstsq(a,b,rcond=None)
    if rank!=design.shape[1] or (coefficients[:len(coords)]<=0).any():
        return None
    if len(coords)==2 and coefficients[:2].min()/coefficients[:2].max()<cfg["minimumModelFluxRatio"]:
        return None
    modeled=design@coefficients
    score=float(np.sum(((z[rows]-modeled[rows])/sigma[rows])**2))
    return score,np.asarray(params),coefficients,modeled


def refine(seed,steps,fn):
    best=fn(seed)
    if best is None:
        return None
    for step in steps:
        for _ in range(8):
            improve=best
            for dim in range(len(seed)):
                for sign in (-1,1):
                    position=best[1].copy()
                    position[dim]+=step*sign
                    candidate=fn(position)
                    if candidate is not None and candidate[0]<improve[0]:
                        improve=candidate
            if improve is best:
                break
            best=improve
    return best


def fits_one(psf,xy,z,sigma,rows,cfg):
    def fn(p):
        return trial(psf,xy,z,sigma,rows,p,cfg)
    grid=np.arange(-2,2.1,1)
    seeds=[m for y in grid for x in grid if (m:=fn([x,y])) is not None]
    if not seeds:
        return None
    top=min(seeds,key=lambda c:c[0])
    return refine(top[1],cfg["fitStepsPx"],fn)


def fits_two(psf,xy,z,sigma,rows,one,cfg):
    def fn(p):
        return trial(psf,xy,z,sigma,rows,p,cfg)
    pos=one[1]
    angles=np.arange(cfg["initialDirectionCount"])*2*np.pi/cfg["initialDirectionCount"]
    moves=np.column_stack([np.cos(angles),np.sin(angles)])
    kicks=[(pos-.25*vec*d,pos+.75*vec*d) for d in cfg["initialSeparationPx"] for vec in moves]
    many=[v for a,b in kicks if (v:=fn(np.concatenate([a,b]))) is not None]
    if not many:
        return None
    seeds=sorted(many,key=lambda c:c[0])[:cfg["dualStarts"]]
    return min((refine(seed[1],cfg["fitStepsPx"],fn) for seed in seeds),key=lambda v:v[0])


def evaluate(model,focus,hold,z,sigma,ncomponents):
    score,p,coefs,pred=model
    result=dict(focusIndex=focus,trainingChi2=score,
                heldoutChi2PerPixel=float(np.mean(((z[hold]-pred[hold])/sigma[hold])**2)),
                parametersPx=p.tolist())
    if ncomponents==2:
        bright=int(coefs[1]>coefs[0])
        result.update(separationPx=float(np.linalg.norm(p[:2]-p[2:])),
                      secondaryToPrimaryFlux=float(coefs[1-bright]/coefs[bright]))
    return result


def fit_fold(psfs,xy,z,err,train,cfg):
    hold=~train
    singles=[]
    doubles=[]
    for i,psf in enumerate(psfs):
        one=fits_one(psf,xy,z,err,train,cfg)
        if one is None:
            continue
        singles.append(evaluate(one,i,hold,z,err,1))
        two=fits_two(psf,xy,z,err,train,one,cfg)
        if two is not None:
            doubles.append(evaluate(two,i,hold,z,err,2))
    if not singles or not doubles:
        return dict(status="FIT_UNAVAILABLE",singleByFocus=singles,dualByFocus=doubles)
    one=min(singles,key=lambda p:p["trainingChi2"])
    two=min(doubles,key=lambda p:p["trainingChi2"])
    return dict(status="MEASURED",one=one,two=two,singleByFocus=singles,dualByFocus=doubles,
                heldoutGain=one["heldoutChi2PerPixel"]-two["heldoutChi2PerPixel"],
                trainingPixels=int(train.sum()),holdoutPixels=int(hold.sum()))


def data_item(row,cfg,psfs,previous):
    stamp=read(previous/"stamps"/row["stampFile"],row["stampSha256"])
    with np.load(io.BytesIO(stamp),allow_pickle=False) as d:
        sci,err,dq=d["sci"],d["err"],d["dq"]
        lower=d["lowerXY"]
    if sci.shape!=(41,41) or sci.shape!=err.shape or sci.shape!=dq.shape:
        raise ValueError("Unexpected cutout geometry")
    y,x=np.indices(sci.shape)
    x=x+lower[0]-row["peakXY"][0]
    y=y+lower[1]-row["peakXY"][1]
    keep=(dq==0)&np.isfinite(sci)&np.isfinite(err)&(err>0)&((x*x+y*y)<=cfg["fitRadiusPx"]**2)
    xy=np.column_stack((x[keep],y[keep]))
    z=sci[keep].astype(float)
    e=err[keep].astype(float)
    base=dict(h97=row["h97"],root=row["root"],fitPixels=len(z),
              minimumCleanWingSectors=min(row["atPeak"]["wing"]["cleanPerSector"]))
    if base["minimumCleanWingSectors"]<cfg["minimumPixelsPerWingSector"]:
        return dict(base,status="INSUFFICIENT_WING_SECTORS")
    folds=[fit_fold(psfs,xy,z,e,((xy[:,0]+xy[:,1])%2)==i,cfg) for i in (0,1)]
    return dict(base,status="MEASURED",folds=folds)


def verify_model(psf,cfg):
    yy,xx=np.mgrid[-7:8,-7:8]
    xy=np.column_stack((xx.ravel(),yy.ravel()))
    p=np.array([.15,-.17,1.4,.61])
    blend=40000*interp(psf,xy[:,0]-p[0],xy[:,1]-p[1])+23000*interp(psf,xy[:,0]-p[2],xy[:,1]-p[3])
    data=blend+100+xy[:,0]*.3
    train=(xy[:,0]+xy[:,1])%2==0
    fit=fit_fold(psf[None],xy,data,np.full(len(data),5.),train,cfg)
    actual=float(np.linalg.norm(p[:2]-p[2:]))
    measured=fit["two"]["separationPx"]
    if abs(actual-measured)>cfg["syntheticMaxSeparationErrorPx"] or fit["heldoutGain"]<=0:
        raise ValueError("Known binary did not reproduce")
    return dict(kind="same-library noiseless numerical check",expectedSeparationPx=actual,
                recoveredSeparationPx=measured,heldoutGain=fit["heldoutGain"])


raw=(root/"protocollo.json").read_bytes()
cfg=json.loads(raw)
if (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
    raise ValueError("Runtime changed")
data=read(root/cfg["library"],cfg["librarySha256"])
with fits.open(io.BytesIO(data),memmap=False) as h:
    header=h[0].header
    cube=h[0].data.astype(float)
    if cube.shape!=(9,90,101,101) or not np.isfinite(cube).all() or (header["NXPSFS"],header["NYPSFS"])!=(9,10):
        raise ValueError("Unexpected F555W PSF grid")
positions=json.loads(read(previous/"riscontro.json",cfg["previousReportSha256"]))["observations"]
control=verify_model(loc_psfs(cube,header,[2541,1917],2)[4],cfg)
reports=[]
for obs in positions:
    report=data_item(obs,cfg,loc_psfs(cube,header,obs["peakXY"],obs["chip"]),previous)
    reports.append(report)
    print(obs["root"],report["status"],[r.get("heldoutGain") for r in report.get("folds",[])],flush=True)
result=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(raw).hexdigest(),
            psfShape=list(cube.shape),numericalCheck=control,results=reports,nativeExecutions=0,scientificClosures=0)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
