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



def open_subject(item,cfg,cache,expected):
    reader=FitsRanges(cache,item,cfg["blockBytes"],expected,mode=="acquire")
    if hashlib.sha256(reader.read(65536)).hexdigest()!=item["prefixSha256"]:
        raise ValueError("Primary FITS prefix differs from prior check")
    reader.seek(0)
    return reader


def chip_geometry(sci,hdus):
    dq=hdus["DQ",sci.ver]
    if dq.shape!=sci.shape or sci.header["BUNIT"]!="ELECTRONS":
        raise ValueError("Unexpected SCI/DQ geometry")
    return dq,WCS(sci.header,hdus).celestial



def fit_background(values,good,x,y,inner,outer):
    r=np.hypot(x,y)
    sample=good&(r>=inner)&(r<=outer)
    keep=sample.copy()
    for _ in range(4):
        if keep.sum()<100:
            return None
        design=np.column_stack((np.ones(int(keep.sum())),x[keep],y[keep]))
        fit=np.linalg.lstsq(design,values[keep],rcond=None)[0]
        plane=fit[0]+fit[1]*x+fit[2]*y
        residual=values-plane
        median=np.median(residual[keep])
        mad=1.4826*np.median(np.abs(residual[keep]-median))
        if not np.isfinite(mad) or mad<=0:
            return None
        keep=sample&(np.abs(residual-median)<=3*mad)
    if keep.sum()<100:
        return None
    design=np.column_stack((np.ones(int(keep.sum())),x[keep],y[keep]))
    fit=np.linalg.lstsq(design,values[keep],rcond=None)[0]
    plane=fit[0]+fit[1]*x+fit[2]*y
    return plane,mad,int(keep.sum()),np.linalg.inv(design.T@design)


def aperture_summary(values,errors,quality,good,x,y,center,radius,annulus,scale):
    distance=np.hypot(x-center[0],y-center[1])
    inside=distance<=radius
    background=fit_background(values,good,x-center[0],y-center[1],*annulus)
    n=int(inside.sum())
    entry=dict(status="MEASURED",pixels=n,goodPixels=int((inside&good).sum()),
               saturatedPixels=int((inside&((quality&2304)!=0)).sum()))
    if entry["goodPixels"]!=n or background is None:
        entry["status"]="INCOMPLETE_APERTURE" if entry["goodPixels"]!=n else "BACKGROUND_UNAVAILABLE"
        return entry
    plane,scatter,sky_n,cov=background
    flux=float((values[inside]-plane[inside]).sum())
    sum_design=np.array([n,(x[inside]-center[0]).sum(),(y[inside]-center[1]).sum()])
    sigma=math.sqrt(float((errors[inside]**2).sum()+scatter**2*(sum_design@cov@sum_design)))
    entry.update(fluxDensity=flux*scale,formalSigma=sigma*scale,
                 formalSnr=flux/sigma,backgroundPixels=sky_n)
    return entry


def measure(sci,hdus,item,predicted,point,pams,cfg):
    p=hdus[0].header
    dq,wcs=chip_geometry(sci,hdus)
    err=hdus["ERR",sci.ver]
    if err.shape!=sci.shape:
        raise ValueError("Unexpected ERR plane")
    px,py=(float(v) for v in wcs.world_to_pixel(point))
    ix,iy=round(px),round(py)
    chip=sci.header["CCDCHIP"]
    if chip!=predicted["chip"] or [ix,iy]!=predicted["pixelXY"]:
        raise ValueError("Prior WCS footprint did not reproduce")
    radius=cfg["stampHalfWidthPx"]
    h,w=sci.shape
    if not (radius<=ix<w-radius and radius<=iy<h-radius):
        return dict(root=item["root"],status="STAMP_OUTSIDE")
    ys,xs=slice(iy-radius,iy+radius+1),slice(ix-radius,ix+radius+1)
    dx,dy=(-int(sci.header[key]) for key in ("LTV1","LTV2"))
    pam=pams[chip]
    area=pam[ys.start+dy:ys.stop+dy,xs.start+dx:xs.stop+dx]
    if area.shape!=(2*radius+1,2*radius+1) or not (np.isfinite(area)&(area>0)).all():
        raise ValueError("Invalid area-map section")
    values=sci.section[ys,xs]*area
    errors=err.section[ys,xs]*area
    quality=dq.section[ys,xs]
    good=(quality==0)&np.isfinite(values)&np.isfinite(errors)&(errors>0)
    y,x=np.mgrid[-radius:radius+1,-radius:radius+1]
    base=fit_background(values,good,x,y,*cfg["skyAnnuliPx"][0])
    if base is None:
        return dict(root=item["root"],status="PEAK_BACKGROUND_UNAVAILABLE")
    search=np.hypot(x,y)<=cfg["searchRadiusPx"]
    residual=values-base[0]
    score=np.where(search&good,residual,-np.inf)
    iy_local,ix_local=np.unravel_index(score.argmax(),score.shape)
    ypeak,xpeak=(int(y[iy_local,ix_local]),int(x[iy_local,ix_local]))
    if not np.isfinite(score.max()) or np.hypot(xpeak,ypeak)>=cfg["searchRadiusPx"]-0.5:
        return dict(root=item["root"],status="PEAK_ABSENT_OR_ON_SEARCH_EDGE")
    center_disk=(np.hypot(x-xpeak,y-ypeak)<=cfg["centroidRadiusPx"])&good
    weights=np.maximum(residual[center_disk],0)
    if weights.sum()<=0:
        return dict(root=item["root"],status="NONPOSITIVE_PEAK")
    cx=float(np.sum(x[center_disk]*weights)/weights.sum())
    cy=float(np.sum(y[center_disk]*weights)/weights.sum())
    detected=wcs.pixel_to_world(ix+cx,iy+cy).icrs
    photflam=float(sci.header.get("PHOTFLAM",p.get("PHOTFLAM",0)))
    if photflam<=0 or not np.isfinite(photflam):
        raise ValueError("Invalid PHOTFLAM")
    scale=photflam/item["f658nExposureSeconds"]
    out=[]
    for ann in cfg["skyAnnuliPx"]:
        entry={}
        for aperture in cfg["apertureRadiiPx"]:
            entry[str(aperture)]=aperture_summary(values,errors,quality,good,x,y,(cx,cy),aperture,ann,scale)
        out.append(dict(annulusPx=ann,apertures=entry))
    return dict(root=item["root"],status="MEASURED_WITH_RETAINED_FAILURES",chip=chip,
                wcsPredictionXY=[px,py],detectedXY=[ix+cx,iy+cy],
                skyRaDec=[float(detected.ra.deg),float(detected.dec.deg)],
                offsetFromCandidateArcsec=float(detected.separation(point).arcsec),
                photflam=photflam,measurements=out)


def compare(measured,cfg):
    if any("measurements" not in v for v in measured):
        return dict(status="NO_ASSOCIATED_PEAK_IN_AT_LEAST_ONE_REFERENCE")
    sky=[SkyCoord(*m["skyRaDec"],unit=u.deg) for m in measured]
    max_sep=max(float(a.separation(b).arcsec) for i,a in enumerate(sky) for b in sky[i+1:])
    each=[]
    for ann_index,ann in enumerate(cfg["skyAnnuliPx"]):
        for r in cfg["apertureRadiiPx"]:
            sample=[m["measurements"][ann_index]["apertures"][str(r)] for m in measured]
            if any(v["status"]!="MEASURED" for v in sample):
                result=dict(status="SUPPORT_INCOMPLETE",referenceStatuses=[v["status"] for v in sample])
            else:
                a,b,held=(v["fluxDensity"] for v in sample)
                if min(a,b,held)<=0 or min(v["formalSnr"] for v in sample)<cfg["minimumFormalSnr"]:
                    result=dict(status="NONPOSITIVE_OR_LOW_FORMAL_SNR")
                else:
                    short_mean=(a+b)/2
                    repeat=100*(b-a)/short_mean
                    residual=100*(held-short_mean)/short_mean
                    result=dict(status="MEASURED",shortRepeatPct=repeat,heldoutMinusShortPct=residual,
                                passesPhotometricTolerance=(abs(repeat)<=cfg["maximumShortRepeatPct"]
                                    and abs(residual)<=cfg["maximumHeldoutResidualPct"]))
            each.append(dict(annulusPx=ann,radiusPx=r,**result))
    trusted=max_sep<=cfg["maximumInterReferencePeakArcsec"]
    primary=next(v for v in each if v["radiusPx"]==cfg["primaryAperturePx"]
                 and v["annulusPx"]==cfg["skyAnnuliPx"][0])
    return dict(status="DIAGNOSTIC_FLC_APERTURES",maxPairwisePeakSeparationArcsec=max_sep,
                withinAstrometricTolerance=trusted,primaryPass=trusted and primary.get("passesPhotometricTolerance",False),
                comparisons=each)



def evaluate(item,candidates,cfg,pams,cache,expected):
    reader=open_subject(item,cfg,cache,expected)
    results=[]
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        chips=[(s,WCS(s.header,hdus).celestial) for s in hdus if s.name=="SCI"]
        for c in candidates:
            sky=SkyCoord(*c["skyRaDec"],unit=u.deg)
            hits=[]
            for sci,wcs in chips:
                xy=np.asarray(wcs.world_to_pixel(sky),float)
                if not np.isfinite(xy).all():
                    continue
                x,y=(round(v) for v in xy)
                h,w=sci.shape
                if 0<=x<w and 0<=y<h:
                    hits.append((sci,{"chip":sci.header["CCDCHIP"],"pixelXY":[x,y]}))
            if len(hits)>1:
                raise ValueError("Candidate falls in both chips of one exposure")
            if not hits:
                results.append(dict(root=item["root"],status="OUTSIDE_ALL_CHIPS"))
                continue
            sci,guess=hits[0]
            results.append(measure(sci,hdus,item,guess,sky,pams,cfg))
    print(item["root"],Counter(v["status"] for v in results),flush=True)
    return results,reader.used



def choose_controls(first,target,cfg,cache,expected):
    reader=open_subject(first,cfg,cache,expected)
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        selected=None
        for sci in hdus:
            if sci.name!="SCI":
                continue
            dq,wcs=chip_geometry(sci,hdus)
            xy=np.asarray(wcs.world_to_pixel(target),float)
            if not np.isfinite(xy).all():
                continue
            x,y=(round(v) for v in xy)
            h,w=sci.shape
            r=cfg["controlSearchHalfWidthPx"]
            if not (r<=x<w-r and r<=y<h-r):
                continue
            if selected is not None:
                raise ValueError("Search tile fits on multiple chips")
            selected=(sci,dq,wcs,x,y,r)
        if selected is None:
            raise ValueError("Frozen control search tile is not on detector")
        sci,dq,wcs,x,y,r=selected
        box=np.s_[y-r:y+r+1,x-r:x+r+1]
        values=sci.section[box].astype(float)
        good=(dq.section[box]==0)&np.isfinite(values)
        center=values[8:-8,8:-8]
        shifted=[values[8+dy:values.shape[0]-8+dy,8+dx:values.shape[1]-8+dx]
                 for dy,dx in ((0,6),(0,-6),(6,0),(-6,0),(4,4),(4,-4),(-4,4),(-4,-4))]
        strength=center-np.median(shifted,axis=0)
        top=good[8:-8,8:-8] & np.isfinite(strength) & (strength>=cfg["minimumDetectionContrastElectrons"])
        for dy,dx in ((1,0),(-1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)):
            region=np.s_[8+dy:values.shape[0]-8+dy,8+dx:values.shape[1]-8+dx]
            top &= good[region] & (values[region]<=center)
        ys,xs=np.nonzero(top)
        rank=sorted(zip(ys.tolist(),xs.tolist(),strict=True),
                    key=lambda yx:(-strength[yx],yx))
        keep=[]
        controls=[]
        for iy,ix in rank:
            position=(x-r+8+ix,y-r+8+iy)
            if math.hypot(position[0]-x,position[1]-y)<cfg["excludeTargetRadiusPx"]:
                continue
            if any(math.hypot(position[0]-a,position[1]-b)<cfg["minimumControlSeparationPx"]
                   for a,b in keep):
                continue
            keep.append(position)
            sky=wcs.pixel_to_world(*position).icrs
            controls.append(dict(id=len(keep),selectionXY=list(position),
                                 contrastElectrons=float(strength[iy,ix]),
                                 skyRaDec=[float(sky.ra.deg),float(sky.dec.deg)]))
            if len(keep)==cfg["maximumControls"]:
                break
    return controls,reader.used


def diagnostic_flux(obs,cfg):
    if "measurements" not in obs:
        return None
    row=obs["measurements"][0]["apertures"][str(cfg["controlAperturePx"])]
    if row["status"]!="MEASURED" or row["formalSnr"]<cfg["minimumFormalSnr"] or row["fluxDensity"]<=0:
        return None
    return row["fluxDensity"]


def control_metrics(rows,cfg):
    series=[diagnostic_flux(r,cfg) for r in rows]
    if any(v is None for v in series):
        return dict(status="INSUFFICIENT_SUPPORT_OR_SNR",usableApertures=sum(v is not None for v in series))
    coords=[SkyCoord(*r["skyRaDec"],unit=u.deg) for r in rows]
    sep=max(float(a.separation(b).arcsec) for i,a in enumerate(coords) for b in coords[i+1:])
    if sep>cfg["maximumInterReferencePeakArcsec"]:
        return dict(status="ASTROMETRY_INCONSISTENT",maxSeparationArcsec=sep)
    a,b,h1,h2=series
    den=(a+b)/2
    repeat=100*(b-a)/den
    if abs(repeat)>cfg["maximumShortRepeatPct"]:
        return dict(status="SHORT_EXPOSURES_DISAGREE",shortRepeatPct=repeat)
    return dict(status="MEASURED",shortRepeatPct=repeat,
                maxSeparationArcsec=sep,shortMeanFluxDensity=den,
                holdoutMinusShortPct=[100*(h1-den)/den,100*(h2-den)/den])


def summarize(rows,target,cfg):
    good=[r["metrics"] for r in rows if r["metrics"]["status"]=="MEASURED"]
    matched=[r for r in good if (cfg["brightnessFactors"][0]<=r["shortMeanFluxDensity"]/target<=cfg["brightnessFactors"][1])]
    def stats(seq):
        out=dict(n=len(seq))
        if seq:
            a=np.asarray([v["holdoutMinusShortPct"] for v in seq])
            out.update(medians=np.median(a,axis=0).tolist(),p90Abs=np.quantile(np.abs(a),.9,axis=0).tolist(),
                       ranges=np.column_stack([a.min(axis=0),a.max(axis=0)]).tolist())
        return out
    return dict(all=stats(good),matchedBrightness=stats(matched),
                sufficientControls=(len(good)>=cfg["minimumControls"] and len(matched)>=cfg["minimumBrightnessMatched"]))


def main():
    cfg_bytes=(root/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_bytes)
    if mode not in ("acquire","replay") or (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Unexpected mode or runtime")
    subjects=json.loads(checked(prior/"riscontro-intestazioni.json",cfg["priorReportSha256"]))
    previous=Path(sys.argv[6])
    alternative=Path(sys.argv[7])
    phot=json.loads(checked(previous/"riscontro.json",cfg["photometryReportSha256"]))
    alt=json.loads(checked(alternative/"riscontro.json",cfg["alternativeReportSha256"]))
    target_row=next(r for r in phot["results"] if r["candidate"]==cfg["targetCandidate"])
    target_alt=next(r for r in alt["results"] if r["candidate"]==cfg["targetCandidate"])
    short=target_row["observations"][:2]
    longer=[next(r for r in target_alt["altReferences"] if r["root"]==n) for n in cfg["controlHoldoutRoots"]]
    target_stats=control_metrics(short+longer,cfg)
    if target_stats["status"]!="MEASURED":
        raise ValueError("Prior diagnostic target not reproduced")
    target=SkyCoord(*short[0]["skyRaDec"],unit=u.deg)
    pams={}
    for chip in (1,2):
        name=f"wfc{chip}_newpam.fits"
        blob=checked(previous/name,cfg["pamSha256"][str(chip)])
        with fits.open(io.BytesIO(blob),memmap=False) as hdus:
            pams[chip]=hdus[0].data
    items={m["root"]:m for m in subjects["members"]}
    order=cfg["referenceRoots"][:2]+cfg["controlHoldoutRoots"]
    if [items[n]["f658nExposureSeconds"] for n in order]!=[150,150,509,509]:
        raise ValueError("Control reference roster changed")
    cache=root/"ranges"
    manifest=root/"range-sha256.json"
    expected={} if mode=="acquire" else json.loads(manifest.read_bytes())
    controls,used=choose_controls(items[order[0]],target,cfg,cache,expected)
    print("frozen controls",len(controls),flush=True)
    with ThreadPoolExecutor(max_workers=cfg["concurrentObjects"]) as pool:
        read=[pool.submit(evaluate,items[name],controls,cfg,pams,cache,expected) for name in order]
        computed=[task.result() for task in read]
    for _,ranges in computed:
        used.update(ranges)
    if mode=="acquire":
        with manifest.open("x",encoding="ascii",newline="\n") as stream:
            stream.write(json.dumps(used,sort_keys=True,indent=2)+"\n")
    elif used!=expected:
        raise ValueError("Replay used a different range set")
    rows=[]
    for i,c in enumerate(controls):
        obs=[take[0][i] for take in computed]
        row=dict(selection=c,observations=obs,metrics=control_metrics(obs,cfg))
        rows.append(row)
    summary=summarize(rows,target_stats["shortMeanFluxDensity"],cfg)
    result=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(cfg_bytes).hexdigest(),
                rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),target=target_stats,
                controlSummary=summary,controls=rows,
                scientificClosures=0,nativeExecutions=0)
    with report.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps(summary),flush=True)


if __name__=="__main__":
    main()
