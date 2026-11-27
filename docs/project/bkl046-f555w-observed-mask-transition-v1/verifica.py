"""Compare transition widths with independently acquired guides and saved detector flag shapes."""
import hashlib
import io
import json
from pathlib import Path
import sys

root, runtime, calspec, orion, output = map(Path, sys.argv[1:])
sys.path.insert(0,str(runtime))
import numpy as np


def pinned(path,digest):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=digest:
        raise ValueError(f"Changed input {path.name}")
    return raw


def centered(base, row):
    with np.load(io.BytesIO(pinned(base/row["stampFile"],row["stampSha256"])),allow_pickle=False) as f:
        v=[f[k] for k in ("sci","err","dq")]
        at=np.array(row["peakXY"])-f["lowerXY"]
    if any(a.shape!=(41,41) for a in v):
        raise ValueError("Unexpected detector stamp")
    x,y=at
    if min(x,y)<18 or max(x,y)>22:
        padded=[]
        for a in v:
            fill=np.nan if a.dtype.kind=="f" else 1
            b=np.pad(a,((10,10),(10,10)),constant_values=fill)
            padded.append(b[y-8:y+29,x-8:x+29])
        return padded
    return [a[y-18:y+19,x-18:x+19] for a in v]


Y,X=np.mgrid[-18:19,-18:19]
R=np.hypot(X,Y)


def shift(image,x,y):
    point_x=18+X+x
    point_y=18+Y+y
    i=np.clip(np.floor(point_x).astype(int),0,35)
    j=np.clip(np.floor(point_y).astype(int),0,35)
    a=point_x-i
    b=point_y-j
    valid=(point_x>=0)&(point_x<=36)&(point_y>=0)&(point_y<=36)
    points=((1-a)*(1-b),a*(1-b),(1-a)*b,a*b)
    values=(image[j,i],image[j,i+1],image[j+1,i],image[j+1,i+1])
    mixed=sum(w*np.where(w==0,0,v) for w,v in zip(points,values,strict=True))
    return np.where(valid,mixed,np.nan)


def calibrate(first, second, spec, fit_scale):
    ref,err,flag=first
    guide,gerr,gflag=second
    usable=(flag==0)&np.isfinite(ref)&np.isfinite(err)&(err>0)
    ann=usable&(R>=spec["alignmentAnnulus"][0])&(R<=spec["alignmentAnnulus"][1])
    clean=(gflag==0)&np.isfinite(guide)&np.isfinite(gerr)&(gerr>0)
    source=np.where(clean,guide,np.nan)
    cuts=np.arange(-spec["alignmentMaximumShift"],spec["alignmentMaximumShift"]+spec["alignmentStep"]/2,spec["alignmentStep"])
    trials=[]
    for dx in cuts:
        for dy in cuts:
            aligned=shift(source,dx,dy)
            index=ann&np.isfinite(aligned)
            if index.sum()<0.8*ann.sum():
                continue
            weights=1/err[index]
            nuisance=np.column_stack((np.ones(index.sum()),X[index],Y[index]))
            a=np.column_stack((aligned[index],nuisance)) if fit_scale else nuisance
            b=ref[index] if fit_scale else ref[index]-aligned[index]
            coef,_,rank,_=np.linalg.lstsq(a*weights[:,None],b*weights,rcond=None)
            if rank!=a.shape[1] or (fit_scale and coef[0]<=0):
                continue
            if not fit_scale:
                coef=np.r_[1.,coef]
            pred=coef[0]*aligned+coef[1]+coef[2]*X+coef[3]*Y
            rms=float(np.sqrt(np.mean(((ref[index]-pred[index])/err[index])**2)))
            trials.append((rms,float(dx),float(dy),coef,pred,int(index.sum())))
    if not trials:
        return None
    return min(trials,key=lambda v:v[:3])


def mask_geometry(mask,spec):
    points=np.argwhere(mask)
    d=np.min(np.hypot(Y[:,:,None]-(points[:,0]-18),X[:,:,None]-(points[:,1]-18)),axis=2)
    return d,(d<=spec["boundaryRadius"])&~mask


def measure(first,pred,mask,dist,rim,spec):
    ref,err,flag=first
    valid=(flag==0)&np.isfinite(ref)&np.isfinite(err)&(err>0)
    expected=(R<=spec["apertureRadius"])
    sky=valid&(R>=spec["alignmentAnnulus"][0])&(R<=spec["alignmentAnnulus"][1])
    if not np.all(valid[expected]) or not np.all(np.isfinite(pred[expected|rim|mask])) or rim.sum()==0:
        return dict(status="INCOMPLETE_PIXEL_SUPPORT")
    reference=float(np.sum(ref[expected]-np.median(ref[sky])))
    if reference<=0:
        raise ValueError("Reference aperture not positive")
    directions=((np.s_[1:,:],np.s_[:-1,:]),(np.s_[:,1:],np.s_[:,:-1]))
    links=[((mask[a]!=mask[b]) & valid[a] & valid[b]) for a,b in directions]
    if not any(v.any() for v in links):
        return dict(status="INCOMPLETE_BOUNDARY_SUPPORT")
    results=[]
    for width in spec["transitionWidths"]:
        if width==0:
            mix=mask.astype(float)
        else:
            mix=0.5*(1+np.cos(np.pi*np.minimum(dist/width,1)))
        difference=np.where(mix>0,mix*(pred-ref),0.)
        rim_valid=rim&valid
        pct=float(np.sum(difference[expected])/reference*100)
        crossing=np.concatenate([(difference[a]-difference[b])[link]
                                 for (a,b),link in zip(directions,links,strict=True)])
        results.append(dict(width=width,corePixels=int(mask.sum()),validRimPixels=int(rim_valid.sum()),
                            boundaryEdges=len(crossing),
                            boundaryGradientRMSElectrons=float(np.sqrt(np.mean(crossing**2))),
                            boundaryGradientP95AbsElectrons=float(np.quantile(np.abs(crossing),0.95)),
                            apertureFluxErrorPct=pct,passedFlux=abs(pct)<=spec["maximumAbsFluxErrorPct"],
                            rimRMSElectrons=float(np.sqrt(np.mean(difference[rim_valid]**2))),
                            rimMaxAbsElectrons=float(np.max(np.abs(difference[rim_valid]))),
                            maskedRMSElectrons=float(np.sqrt(np.mean(difference[mask&valid]**2)))))
    return dict(status="MEASURED",variants=results)


def main():
    raw=(root/"protocollo.json").read_bytes()
    spec=json.loads(raw)
    refs=json.loads(pinned(calspec/"riscontro-split.json",spec["calspecSha256"]))["associations"]
    durations=json.loads(pinned(calspec/"riscontro.json",spec["calspecWcsSha256"]))["samples"]
    seconds={r["root"]:r["exposureSeconds"] for r in durations}
    if len(seconds)!=2*len(refs):
        raise ValueError("Exposure duration roster changed")
    source=json.loads(pinned(orion/"riscontro.json",spec["orionSha256"]))["observations"]
    templates=[]
    for row in source:
        if row["status"]!="RECORDED":
            continue
        _,_,flag=centered(orion/"stamps",row)
        region=((flag&(256|2048))!=0)&(R<=spec["coreMaskMaximumRadius"])
        if not region.any():
            raise ValueError("Expected empirical mask is empty")
        dist,rim=mask_geometry(region,spec)
        templates.append((str(row["h97"])+"/"+row["root"],region,dist,rim))
    if (np.__version__!="2.3.5" or len(refs)!=spec["associationCount"] or len(templates)!=spec["maskCount"]
            or len({t[0] for t in templates})!=len(templates)):
        raise ValueError("Unexpected runtime or roster")
    all_results=[]
    for assoc in refs:
        left,right=assoc["exposures"]
        if seconds[left["root"]]!=seconds[right["root"]] or seconds[left["root"]]<=0:
            raise ValueError("Fixed scale requires two equal positive exposure times")
        if not assoc["bothFitEligible"]:
            raise ValueError("Reference pair not eligible")
        first=centered(calspec/"stamps-split",left)
        second=centered(calspec/"stamps-split",right)
        for method in spec["guideScaleMethods"]:
            fit=calibrate(first,second,spec,method=="WING_FIT")
            if fit is None:
                all_results.append(dict(association=assoc["association"],target=assoc["target"],method=method,
                                        status="ALIGNMENT_UNAVAILABLE",
                                        trials=[dict(mask=m,status="ALIGNMENT_UNAVAILABLE") for m,_,_,_ in templates]))
                continue
            rms,dx,dy,coef,pred,n=fit
            trials=[dict(mask=name,**measure(first,pred,region,dist,rim,spec)) for name,region,dist,rim in templates]
            all_results.append(dict(association=assoc["association"],target=assoc["target"],method=method,status="ALIGNED",
                                  alignment=dict(dx=dx,dy=dy,coef=coef.tolist(),residualRmsInErrUnits=rms,trainingPixels=n),
                                  trials=trials))
    with output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(dict(schema=spec["schema"],protocolSha256=hashlib.sha256(raw).hexdigest(),results=all_results,
                       nativeExecutions=0,scientificClosures=0),out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()
