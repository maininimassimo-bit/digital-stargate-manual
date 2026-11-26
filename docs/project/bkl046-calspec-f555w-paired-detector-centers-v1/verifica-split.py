"""Identify repeatable bright peaks across the two pre-SM4 FLTs of each association."""
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import sys

root, runtime, output, stamps=map(Path,sys.argv[1:])
sys.path.insert(0,str(runtime))
from astropy.io import fits
import numpy as np


def pinned(path,digest):
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=digest:
        raise ValueError(f"Changed {path.name}")
    return data


def load(item):
    with fits.open(io.BytesIO(pinned(root/"data"/item["name"],item["sha256"])),memmap=False) as h:
        return tuple(h[k,1].data.copy() for k in ("SCI","ERR","DQ"))


def mutual_candidates(data,cases,cfg):
    if any(a[0].shape!=data[0][0].shape for a in data):
        raise ValueError("Split shapes differ")
    if cases[0]["ltv"]!=cases[1]["ltv"] or cases[0]["chip"]!=cases[1]["chip"]:
        raise ValueError("Split aperture differs")
    signal=[]
    h,w=data[0][0].shape
    for (z,e,q),case in zip(data,cases,strict=True):
        y,x=np.indices(z.shape)
        a,b=case["predictedXY"]
        allowed=(abs(x-a)<=cfg["searchHalfWidthPixels"])&(abs(y-b)<=cfg["searchHalfWidthPixels"])
        allowed&=(x>=cfg["stampRadius"])&(y>=cfg["stampRadius"])&(x<w-cfg["stampRadius"])&(y<h-cfg["stampRadius"])
        mask=allowed & np.isfinite(z) & np.isfinite(e) & (e>0) & (q==0)
        signal.append(np.where(mask,z,-np.inf))
    half=cfg["localMatchRadiusPixels"]
    idx=np.argwhere(signal[0]>=cfg["minimumPeakElectrons"])
    choices=[]
    for y,x in idx:
        win=signal[1][y-half:y+half+1,x-half:x+half+1]
        iy,ix=np.unravel_index(np.argmax(win),win.shape)
        if np.hypot(iy-half,ix-half)>cfg["maximumMutualPeakDistancePixels"]:
            continue
        two=win[iy,ix]
        if two>=cfg["minimumPeakElectrons"]:
            choices.append((float(min(signal[0][y,x],two)),int(x),int(y),int(x-half+ix),int(y-half+iy)))
    if not choices:
        return None
    _,x,y,x1,y1=max(choices)
    return ((x,y),(x1,y1))


def record(pixels,case,center,cfg):
    if center is None:
        return dict(root=case["root"],status="NO_COINCIDENT_BRIGHT_PEAK")
    x,y=center
    r=cfg["stampRadius"]
    cut=np.s_[y-r:y+r+1,x-r:x+r+1]
    z,e,q=(a[cut] for a in pixels)
    yy,xx=np.mgrid[-r:r+1,-r:r+1]
    rr=xx*xx+yy*yy
    valid=(q==0)&np.isfinite(z)&np.isfinite(e)&(e>0)
    sky=valid&(rr>=121)&(rr<=225)
    core=rr<=cfg["coreRadius"]**2
    nfull=int(np.count_nonzero(core&((q&256)!=0)))
    nadc=int(np.count_nonzero(core&((q&2048)!=0)))
    aperture=core&valid
    snr=float(np.sum(z[aperture]-np.median(z[sky]))/np.linalg.norm(e[aperture]))
    sector=np.floor(np.mod(np.arctan2(yy,xx),2*np.pi)/(np.pi/4)).astype(int)
    wing=[int(np.count_nonzero(valid&(rr>=16)&(rr<=81)&(sector==i))) for i in range(8)]
    checks=dict(core=nfull==nadc==0,wing=min(wing)>=cfg["minimumWingSupport"],
                snr=snr>=cfg["minimumPositiveApertureSignalToNoise"])
    f=stamps/(case["root"]+".npz")
    with f.open("xb") as out:
        np.savez(out,sci=z.astype("<f4"),err=e.astype("<f4"),dq=q.astype("<i4"),
                 lowerXY=np.array([x-r,y-r],dtype="<i4"))
    return dict(root=case["root"],status="RECORDED",chip=case["chip"],mjd=case["mjd"],peakXY=center,
                chipPeakXY=[center[i]-case["ltv"][i] for i in (0,1)],
                offsetFromWcsPredictionPixels=[x-case["predictedXY"][0],y-case["predictedXY"][1]],
                target=case["target"],signalToNoise=snr,peakElectrons=float(z[r,r]),fullWellNearPeak=nfull,
                adcNearPeak=nadc,wingCleanPerSector=wing,fitEligible=all(checks.values()),checks=checks,
                stampFile=f.name,stampSha256=hashlib.sha256(f.read_bytes()).hexdigest())


def main():
    raw=(root/"protocollo-split.json").read_bytes()
    cfg=json.loads(raw)
    pinned(root/"verifica-WCS.py",cfg["wcsProgramSha256"])
    wcs=json.loads(pinned(root/"riscontro.json",cfg["wcsReportSha256"]))
    manifest_bytes=(root/"protocollo.json").read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest()!=wcs["protocolSha256"]:
        raise ValueError("WCS protocol changed")
    manifest_hash=json.loads(manifest_bytes)["pins"]["flt-selected.json"]
    manifest={item["root"]:item for item in json.loads(pinned(root/"flt-selected.json",manifest_hash))}
    assoc=defaultdict(list)
    for case in wcs["samples"]:
        assoc[case["parentObservation"]].append(case)
    stamps.mkdir()
    output_rows=[]
    for parent,cases in sorted(assoc.items()):
        if len(cases)!=2 or any(c["status"]!="RECORDED" for c in cases):
            raise ValueError("Unexpected association")
        data=[load(manifest[case["root"]]) for case in cases]
        centers=mutual_candidates(data,cases,cfg)
        records=[record(d,c,x,cfg) for d,c,x in zip(data,cases,centers or (None,None),strict=True)]
        output_rows.append(dict(association=parent,target=cases[0]["target"],exposures=records,
                                bothFitEligible=all(r.get("fitEligible",False) for r in records)))
    with output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(raw).hexdigest(),associations=output_rows,
                       nativeExecutions=0,scientificClosures=0),out,sort_keys=True,indent=2,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()
