"""Test a Gaia-referenced translation independently in each DECam cutout."""
import argparse
import csv
from datetime import datetime
from hashlib import file_digest, sha256
import json
from pathlib import Path
import runpy
import sys


def sha(path):
    with path.open("rb") as data:
        return file_digest(data, "sha256").hexdigest()


def load_sources(path,p):
    pool=[]
    with path.open(newline="",encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            ra,dec=float(row["ra"]),float(row["dec"])
            if abs(ra-p["ra"])<=.09 and abs(dec-p["dec"])<=.09 and row["pmra"] and row["pmdec"]:
                pool.append((row["source_id"],ra,dec,float(row["ref_epoch"]),float(row["pmra"]),float(row["pmdec"])))
    assert len({row[0] for row in pool})==len(pool)
    return pool


def detect(np,measure,im,good,p):
    m=p["margin"]
    section=im[m:-m,m:-m]
    peak=good[m:-m,m:-m].copy()
    for y in range(-2,3):
        for x in range(-2,3):
            if y or x:
                peak &= section >= im[m+y:im.shape[0]-m+y,m+x:im.shape[1]-m+x]
    coords=(np.argwhere(peak)[:,::-1]+m).tolist()
    coords.sort(key=lambda xy:(-int(im[xy[1],xy[0]]),xy[1],xy[0]))
    seen=[]
    fits=[]
    for x,y in coords:
        if any((x-u)**2+(y-v)**2<p["minCenterSeparationPx"]**2 for u,v in seen):
            continue
        info=measure(np,im,good,(x,y),p)
        if info is not None:
            fits.append(info)
            seen.append((x,y))
    return fits


def links(np,det,world,shift,radius):
    if not len(det) or not len(world):
        return []
    delta=det[:,None,:]-world[None,:,:]-shift
    dist=np.sum(delta**2,axis=2)
    idx=np.argmin(dist,axis=1)
    inverse=np.argmin(dist,axis=0)
    return [(i,int(j),float(np.sqrt(dist[i,j]))) for i,j in enumerate(idx)
            if dist[i,j]<=radius**2 and inverse[j]==i]


def solve(np,world,train,held,p):
    radius=p["matchRadiusPx"]
    bound=p["searchLimitPx"]
    offsets=train[:,None,:]-world[None,:,:]
    flat=offsets.reshape(-1,2)
    possible=flat[(np.abs(flat)<=bound).all(axis=1)]
    centers, votes = np.unique(np.rint(possible/p["binPx"]).astype(int),axis=0,return_counts=True)
    if not len(centers):
        return {"status":"NO_HYPOTHESIS"}
    order=sorted(range(len(centers)),key=lambda i:(-int(votes[i]),centers[i,0],centers[i,1]))
    selected=[]
    for k in order[:p["maxHypotheses"]]:
        shift=centers[k]*p["binPx"]
        match=links(np,train,world,shift,radius)
        if len(match)>=3:
            shift=np.median([train[i]-world[j] for i,j,_ in match],axis=0)
            match=links(np,train,world,shift,radius)
        err=sum(x[2] for x in match)
        selected.append((len(match),err,shift))
    selected.sort(key=lambda item:(-item[0],item[1],float(item[2][0]),float(item[2][1])))
    n,_,shift=selected[0]
    train_fit=links(np,train,world,shift,radius)
    used={j for _,j,_ in train_fit}
    held_test=[(i,j,e) for i,j,e in links(np,held,world,shift,radius) if j not in used]
    masked=np.array([j not in used for j in range(len(world))])
    negatives=[len(links(np,held,world[masked],shift+[x,y],radius))
               for x in (-35,-18,0,18,35) for y in (-35,-18,0,18,35) if x or y]
    qualified=n>=p["minFit"] and len(held_test)>=p["minHeld"] and len(held_test)>max(negatives)
    return {"status":"EMPIRICAL_TRANSLATION" if qualified else "UNCONFIRMED",
            "shiftXY":shift.tolist(),"fitCount":n,"heldOutCount":len(held_test),
            "heldOutP90Px":float(np.quantile([m[2] for m in held_test],.9)) if held_test else None,
            "negativeMaximum":max(negatives),"negativeControls":negatives,
            "heldOutLinks":[{"detection":i,"catalogIndex":j,"residualPx":err} for i,j,err in held_test]}


def main():
    parser=argparse.ArgumentParser()
    for k in ("root","shortKit","referenceKit","previousKit","dependencies","report"):
        parser.add_argument(k,type=Path)
    a=parser.parse_args()
    proto=a.root/"protocollo.json"
    p=json.loads(proto.read_bytes())
    assert sha(a.shortKit/"protocollo.json")==p["shortProtocol"]
    assert sha(a.shortKit/"riscontro.json")==p["shortReport"]
    assert sha(a.previousKit/"misura.py")==p["priorProgram"]
    helpers=runpy.run_path(str(a.previousKit/"misura.py"))
    previous=json.loads((a.shortKit/"protocollo.json").read_bytes())
    catalog=a.root/"catalog.csv"
    assert sha(catalog)==p["catalog"]
    sources=load_sources(catalog,p)
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    from astropy.time import Time
    assert (np.__version__,astropy.__version__)==("2.3.5","7.2.0")
    report=[]
    roots={"new":a.shortKit,"original":a.referenceKit,"prior":a.previousKit}
    for row in previous["inputs"]:
        filename=roots[row["cropRoot"]]/row["crop"]
        full=roots[row["fullRoot"]]/row["full"]
        assert sha(filename)==row["cropSha256"] and sha(full)==row["fullSha256"]
        with fits.open(filename,memmap=False) as h, fits.open(full,memmap=False) as h_full:
            data=h[0].data
            header=h[0].header
            parent=h_full[0]
            x0,y0=[round(parent.header[k]-header[k]) for k in ("CRPIX1","CRPIX2")]
            ny,nx=data.shape
            assert np.array_equal(data,parent.data[y0:y0+ny,x0:x0+nx])
            iy,ix=np.indices(data.shape)
            active=np.zeros(data.shape,dtype=bool)
            for amp in "AB":
                l,r,b,t=helpers["section"](parent.header["DATASEC"+amp])
                active |= ((ix+x0>=l)&(ix+x0<r)&(iy+y0>=b)&(iy+y0<t)&
                           (data>0)&(data<parent.header["SATURAT"+amp]))
            detections=detect(np,helpers["measure"],data,active,previous["photometry"])
            by_tile=lambda d: (int(d["xy"][0])//p["tilePx"]+int(d["xy"][1])//p["tilePx"])%2
            train=np.array([d["xy"] for d in detections if by_tile(d)==0]).reshape(-1,2)
            test=np.array([d["xy"] for d in detections if by_tile(d)==1]).reshape(-1,2)
            vals=np.array([row[1:] for row in sources])
            ra,dec,epoch,pmx,pmy=vals.T
            dt=Time(header["DATE-OBS"],format="isot",scale="utc").jyear-epoch
            apparent_ra=ra+dt*pmx/(3_600_000*np.cos(np.deg2rad(dec)))
            apparent_dec=dec+dt*pmy/3_600_000
            x,y=WCS(header).celestial.world_to_pixel_values(apparent_ra,apparent_dec)
            points=np.column_stack([x,y])
            b=p["searchLimitPx"]
            keep=(points[:,0]>=-b)&(points[:,0]<=nx+b)&(points[:,1]>=-b)&(points[:,1]<=ny+b)
            ids=[s[0] for s,sel in zip(sources,keep,strict=True) if sel]
            result=solve(np,points[keep],train,test,p)
            for link in result.get("heldOutLinks",[]):
                link["sourceId"]=ids[link.pop("catalogIndex")]
            report.append({"image":row["image"],"detector":header["DETPOS"],"seconds":header["EXPTIME"],
                           "detections":len(detections),"fitCandidates":len(train),"heldOutCandidates":len(test),
                           "localGaiaCandidates":int(keep.sum()),**result})
    out={"schema":"BKL046_M20_DECAM_GAIA_TRANSLATION_RESULT_V1","protocolSha256":sha(proto),
         "programSha256":sha(Path(__file__)),"frames":report,"photometricTransferVerified":False,
         "nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(out,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
