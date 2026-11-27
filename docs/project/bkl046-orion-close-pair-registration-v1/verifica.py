from concurrent.futures import ThreadPoolExecutor

from collections import Counter
import hashlib
import io
import json
import math
from pathlib import Path
import sys
from urllib.request import Request, urlopen
import warnings

root,runtime,prior,report = map(Path,sys.argv[1:5])
mode=sys.argv[5]
sys.path.insert(0,str(runtime))
import astropy
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS, FITSFixedWarning
import astropy.units as u
import numpy as np


def checked(path,pin):
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=pin:
        raise ValueError(f"Input changed: {path.name}")
    return data


class FitsRanges(io.RawIOBase):
    def __init__(self, directory, item, stride, expected, allow_fetch):
        super().__init__()
        self.directory=directory
        self.item=item
        self.size=item["dataBytes"]
        self.stride=stride
        self.expected=expected
        self.allow_fetch=allow_fetch
        self.position=0
        self.blocks={}
        self.used={}
    def readable(self):
        return True
    def seekable(self):
        return True
    def tell(self):
        return self.position
    def seek(self,offset,whence=io.SEEK_SET):
        origin={io.SEEK_SET:0,io.SEEK_CUR:self.position,io.SEEK_END:self.size}[whence]
        self.position=origin+offset
        if self.position<0:
            raise ValueError("Negative FITS offset")
        return self.position
    def block(self,start):
        if start in self.blocks:
            return self.blocks[start]
        length=min(self.stride,self.size-start)
        end=start+length-1
        path=self.directory/f"{self.item['root']}-{start}.bin"
        if path.exists():
            data=path.read_bytes()
        else:
            if not self.allow_fetch:
                raise ValueError(f"Replay range unavailable: {path.name}")
            req=Request(self.item["archiveUrl"],headers={"Range":f"bytes={start}-{end}",
                                                         "If-Match":self.item["objectEtag"]})
            with urlopen(req,timeout=15) as reply:
                if (reply.status!=206 or reply.headers["ETag"]!=self.item["objectEtag"]
                    or reply.headers["Content-Range"]!=f"bytes {start}-{end}/{self.size}"):
                    raise ValueError("Unexpected FITS object revision or range")
                data=reply.read(length+1)
            if len(data)!=length:
                raise ValueError("FITS range length differs")
            with path.open("xb") as f:
                f.write(data)
        digest=hashlib.sha256(data).hexdigest()
        if len(data)!=length or (not self.allow_fetch and digest!=self.expected[path.name]):
            raise ValueError(f"FITS range byte check failed: {path.name}")
        self.used[path.name]=digest
        self.blocks[start]=data
        return data
    def read(self,n=-1):
        length=max(0,self.size-self.position) if n<0 else min(n,max(0,self.size-self.position))
        if length>12*self.stride:
            raise ValueError("FITS requested too much in one read")
        pieces=[]
        while length:
            start=(self.position//self.stride)*self.stride
            offset=self.position-start
            block=self.block(start)
            take=min(length,len(block)-offset)
            pieces.append(block[offset:offset+take])
            length-=take
            self.position+=take
        return b"".join(pieces)
    def readinto(self,buffer):
        blob=self.read(len(buffer))
        buffer[:len(blob)]=blob
        return len(blob)




def detect(item,row,cfg,cache,expected):
    reader=FitsRanges(cache,item,cfg["blockBytes"],expected,mode=="acquire")
    if hashlib.sha256(reader.read(65536)).hexdigest()!=item["prefixSha256"]:
        raise ValueError("FITS prefix changed")
    reader.seek(0)
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        p=hdus[0].header
        if p["ROOTNAME"].lower()!=item["root"] or "F555W" not in (p["FILTER1"],p["FILTER2"]):
            raise ValueError("FITS subject changed")
        sci=hdus["SCI",row["scienceExtVer"]]
        dq=hdus["DQ",sci.ver]
        err=hdus["ERR",sci.ver]
        if sci.header["CCDCHIP"]!=row["chip"] or sci.shape!=dq.shape or sci.shape!=err.shape:
            raise ValueError("Chip plane grid changed")
        wcs=WCS(sci.header,hdus).celestial
        x,y=row["xyCatalogNearest"]
        h,w=sci.shape
        r=cfg["searchHalfWidthPx"]
        a,b=max(0,x-r),min(w,x+r+1)
        c,d=max(0,y-r),min(h,y+r+1)
        values=sci.section[c:d,a:b].astype(float)
        mask=(dq.section[c:d,a:b]==0)&np.isfinite(values)
        noise=err.section[c:d,a:b].astype(float)
        core=values[8:-8,8:-8]
        v=values.shape
        offsets=((0,6),(0,-6),(6,0),(-6,0),(4,4),(4,-4),(-4,4),(-4,-4))
        sky_median=np.median([values[8+dy:v[0]-8+dy,8+dx:v[1]-8+dx] for dy,dx in offsets],axis=0)
        amplitude=core-sky_median
        sigma=noise[8:-8,8:-8]
        rankmask=(mask[8:-8,8:-8] & (amplitude>=cfg["peakContrastElectrons"])
                  & np.isfinite(sigma)&(sigma>0)&(amplitude>=cfg["peakSnr"]*sigma))
        neighbors=((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
        for dy,dx in neighbors:
            region=np.s_[8+dy:v[0]-8+dy,8+dx:v[1]-8+dx]
            rankmask &= mask[region]&(values[region]<=core)
        yy,xx=np.nonzero(rankmask)
        ranked=sorted(zip(yy.tolist(),xx.tolist(),strict=True),key=lambda p:(-amplitude[p],p))
        stamps=[]
        xy_positions=[]
        for sy,sx in ranked:
            cx=sx+8
            cy=sy+8
            rx,ry=a+cx,c+cy
            if math.hypot(rx-x,ry-y)<cfg["excludeObjectRadiusPx"]:
                continue
            if any(math.hypot(rx-px,ry-py)<cfg["minimumPeakSeparationPx"] for px,py in xy_positions):
                continue
            area=values[cy-2:cy+3,cx-2:cx+3]-sky_median[sy,sx]
            bright=np.maximum(area,0)
            if bright.sum()<=0 or np.count_nonzero(bright>=0.12*amplitude[sy,sx])<3:
                continue
            t=np.arange(-2,3)
            det_x=rx+float(np.sum(bright*t[None,:])/bright.sum())
            det_y=ry+float(np.sum(bright*t[:,None])/bright.sum())
            xy_positions.append((rx,ry))
            stamps.append((det_x,det_y,float(amplitude[sy,sx])))
            if len(stamps)==cfg["maximumPeaks"]:
                break
        if not stamps:
            return {},reader.used
        det=np.array(stamps)
        sky=wcs.pixel_to_world(det[:,0],det[:,1]).icrs
        sky_list=[dict(pixelXY=xy.tolist(),peakElectrons=float(amp),raDeg=float(ra),decDeg=float(dec))
                  for xy,amp,ra,dec in zip(det[:,:2],det[:,2],sky.ra.deg,sky.dec.deg,strict=True)]
        return dict(boundsXY=[a,b,c,d],stars=sky_list),reader.used


def sky_xy(stars,center):
    if not stars:
        return np.zeros((0,2))
    coords=SkyCoord([s["raDeg"] for s in stars],[s["decDeg"] for s in stars],unit=u.deg)
    e,n=center.spherical_offsets_to(coords)
    return np.column_stack([e.arcsec,n.arcsec])


def unique_pairs(left,right,delta,tol):
    distances=np.linalg.norm((left+delta)[:,None,:]-right[None,:,:],axis=2)
    near=distances<=tol
    return [(int(i),int(j)) for i,j in np.argwhere(near)
            if near[i,:].sum()==1 and near[:,j].sum()==1]


def coarse_translation(train,right,cfg):
    delta=(right[None,:,:]-train[:,None,:]).reshape(-1,2)
    delta=delta[np.linalg.norm(delta,axis=1)<=cfg["coarseSearchArcsec"]]
    if not len(delta):
        return None
    counts=np.array([(np.linalg.norm(delta-u,axis=1)<=cfg["coarseVoteArcsec"]).sum() for u in delta])
    if int(counts.max())<cfg["minimumTrain"]:
        return None
    winner=delta[counts.argmax()]
    selected=delta[np.linalg.norm(delta-winner,axis=1)<=cfg["coarseVoteArcsec"]]
    return np.median(selected,axis=0)


def residual_rows(right,i_left,i_right,pred):
    diff=right[i_right]-pred
    return dict(leftIndex=int(i_left),rightIndex=int(i_right),residualArcsec=np.linalg.norm(diff).item())


def model_summary(first,second,a,b,cfg):
    ref=SkyCoord(*a["peakSkyRaDec"],unit=u.deg)
    l=sky_xy(first.get("stars",[]),ref)
    r=sky_xy(second.get("stars",[]),ref)
    split_rank=np.argsort(l[:,0],kind="stable")
    train_idx=split_rank[np.arange(len(l))%cfg["holdoutEvery"]!=0]
    test_idx=split_rank[np.arange(len(l))%cfg["holdoutEvery"]==0]
    base=dict(h97=a["h97"],leftRoot=a["root"],rightRoot=b["root"],
              leftTotal=len(l),rightTotal=len(r),trainInputs=len(train_idx),holdoutInputs=len(test_idx))
    if len(train_idx)<cfg["minimumTrain"] or len(r)<cfg["minimumTrain"]:
        return dict(base,status="INSUFFICIENT_DETECTIONS")
    delta=coarse_translation(l[train_idx],r,cfg)
    if delta is None:
        return dict(base,status="NO_COHERENT_TRANSLATION")
    train_pairs=unique_pairs(l[train_idx],r,delta,cfg["coarseMatchArcsec"])
    if len(train_pairs)<cfg["minimumTrain"]:
        return dict(base,status="INSUFFICIENT_TRAIN_MATCHES",trainPairs=len(train_pairs))
    ti,tj=np.array(train_pairs).T
    la,rb=l[train_idx[ti]],r[tj]
    delta=np.median(rb-la,axis=0)
    test_pairs=unique_pairs(l[test_idx],r,delta,cfg["holdoutAssociationArcsec"])
    left_ids={int(train_idx[i]) for i in ti}
    right_ids={int(j) for j in tj}
    test_pairs=[(i,j) for i,j in test_pairs if j not in right_ids]
    if not test_pairs:
        return dict(base,status="NO_UNCONSUMED_HOLDOUT_MATCHES",trainPairs=len(train_pairs))
    hi,hj=np.array(test_pairs).T
    if left_ids&set(test_idx[hi]):
        raise ValueError("Training leaked into holdout")
    control_res=[residual_rows(r,i,j,l[i]+delta) for i,j in zip(test_idx[hi],hj,strict=True)]
    p90=float(np.quantile([p["residualArcsec"] for p in control_res],.9))
    affine=None
    design=np.column_stack([np.ones(len(la)),la])
    if len(la)>=cfg["minimumTrainAffine"] and np.linalg.matrix_rank(design)==3:
        coef=np.linalg.lstsq(design,rb,rcond=None)[0]
        predicted=np.column_stack([np.ones(len(hi)),l[test_idx[hi]]])@coef
        affine=float(np.quantile(np.linalg.norm(r[hj]-predicted,axis=1),.9))
    limits=min(cfg["maximumP90Mas"],a["nacoSeparationMas"]*cfg["maxFractionOfNacoSeparation"])
    other=SkyCoord(*b["peakSkyRaDec"],unit=u.deg)
    east,north=ref.spherical_offsets_to(other)
    peak=np.array([east.arcsec,north.arcsec])
    return dict(base,status="MEASURED",trainPairs=len(la),holdoutPairs=len(hi),holdoutResiduals=control_res,
                eastNorthTranslationArcsec=delta.tolist(),primaryP90Mas=1000*p90,diagnosticAffineP90Mas=None if affine is None else 1000*affine,
                maxAcceptedP90Mas=limits,withinPrimaryTolerance=(len(hi)>=cfg["minimumHoldout"] and 1000*p90<=limits),
                peakResidualAfterFieldTranslationMas=1000*np.linalg.norm(peak-delta).item())


def main():
    protocol=(root/"protocollo.json").read_bytes()
    cfg=json.loads(protocol)
    if mode not in ("acquire","replay") or (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Runtime or mode changed")
    obs=json.loads(checked(prior/"riscontro.json",cfg["preflightReportSha256"]))["observations"]
    items={x["root"]:x for x in json.loads(checked(prior/"fits-objects.json",cfg["objectManifestSha256"]))}
    if len(obs)!=6 or any(x["status"]!="RECORDED" for x in obs):
        raise ValueError("Frozen preflight cutout roster changed")
    cache=root/"ranges"
    manifest=root/"range-sha256.json"
    expected={} if mode=="acquire" else json.loads(manifest.read_bytes())
    used={}
    with ThreadPoolExecutor(max_workers=cfg["parallelObjects"]) as pool:
        jobs=[pool.submit(detect,items[row["root"]],row,cfg,cache,expected) for row in obs]
        out=[task.result() for task in jobs]
    for _,pins in out:
        used.update(pins)
    if mode=="acquire":
        with manifest.open("x",encoding="ascii",newline="\n") as f:
            f.write(json.dumps(used,sort_keys=True,indent=2)+"\n")
    elif used!=expected:
        raise ValueError("Replay read a different range set")
    comparisons=[]
    for i in (0,2,4):
        comparisons.append(model_summary(out[i][0],out[i+1][0],obs[i],obs[i+1],cfg))
    result=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(protocol).hexdigest(),
                rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
                detections={row["root"]:det for row,(det,_) in zip(obs,out,strict=True)},
                pairs=comparisons,scientificClosures=0,nativeExecutions=0)
    with report.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for r in comparisons:
        print(r["h97"],r["status"],r.get("trainPairs"),r.get("holdoutPairs"),r.get("primaryP90Mas"),r.get("withinPrimaryTolerance"),flush=True)


if __name__=="__main__":
    main()
