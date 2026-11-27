"""Extract replayable riquadri of the CALSPEC standards from the MAST FLT files."""
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import warnings

root, runtime, output, stamps = map(Path, sys.argv[1:])
sys.path.insert(0, str(runtime))
import astropy
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.time import Time
import astropy.units as u
from astropy.wcs import FITSFixedWarning, WCS
import numpy as np


def pinned(path, digest):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=digest:
        raise ValueError(f"Changed input {path.name}")
    return raw


def parse_identity(b):
    s=b.decode("utf-8")
    sky=re.findall(r"^Coordinates\(ICRS,ep=J2000,eq=2000\):\s*(.+?)\s*\(",s,re.M)
    name=re.findall(r"^Object (.+?)\s+---",s,re.M)
    motion=re.findall(r"^Proper motions:\s+(\S+)\s+(\S+)",s,re.M)
    ident=set(re.findall(r"Gaia DR3 (\d+)",s))
    if len(sky)!=1 or len(name)!=1 or len(motion)!=1 or len(ident)!=1:
        raise ValueError("Ambiguous CALSPEC identity")
    c=SkyCoord(sky[0],unit=(u.hourangle,u.deg))
    return dict(name=name[0],gaiaDR3=next(iter(ident)),
                j2000ICRS=(float(c.ra.deg),float(c.dec.deg)),pmMasYear=tuple(map(float,motion[0])))


def read_exposure(meta,identity,cfg):
    b=pinned(root/"data"/meta["name"],meta["sha256"])
    if len(b)!=meta["bytes"] or len(b)!=meta["mastCatalogBytes"]:
        raise ValueError("MAST product size changed")
    with fits.open(io.BytesIO(b),memmap=False) as h, warnings.catch_warnings():
        warnings.simplefilter("ignore",FITSFixedWarning)
        p=h[0].header
        if (p["ROOTNAME"]!=meta["root"] or p["TARGNAME"]!=meta["target"]
                or p["PROPOSID"]!=meta["proposal"] or p["INSTRUME"]!="ACS" or p["DETECTOR"]!="WFC"
                or "F555W" not in (p["FILTER1"],p["FILTER2"]) or not p["SUBARRAY"]):
            raise ValueError(f"FITS identity mismatch {meta['root']}")
        scis=[a for a in h if a.name=="SCI"]
        if len(scis)!=1:
            raise ValueError("Unexpected subarray extension count")
        sci=scis[0]
        dq,err=h["DQ",sci.ver],h["ERR",sci.ver]
        if not sci.shape==dq.shape==err.shape or sci.header["BUNIT"]!="ELECTRONS":
            raise ValueError("Unexpected science geometry or units")
        year=float(Time((p["EXPSTART"]+p["EXPEND"])/2,format="mjd",scale="utc").jyear)
        at=SkyCoord(*identity["j2000ICRS"],unit=u.deg)
        target=at.spherical_offsets_by(*(np.asarray(identity["pmMasYear"])*(year-2000)*u.mas))
        wcs=WCS(sci.header,h).celestial
        x1,y1=wcs.world_to_pixel(target)
        if not np.isfinite([x1,y1]).all():
            return dict(status="WCS_FAILED")
        x0,y0=int(round(float(x1))),int(round(float(y1)))
        r=cfg["stampRadius"]
        if not (r<=x0<sci.shape[1]-r and r<=y0<sci.shape[0]-r):
            return dict(status="STAMP_CROSSES_EDGE",predictedXY=[x0,y0])
        cut=np.s_[y0-r:y0+r+1,x0-r:x0+r+1]
        z,e,q=sci.section[cut].astype("<f4"),err.section[cut].astype("<f4"),dq.section[cut].astype("<i4")
        yy,xx=np.mgrid[-r:r+1,-r:r+1]
        search=(xx*xx+yy*yy<=cfg["searchRadius"]**2)&np.isfinite(z)&((q&cfg["badGeometryMask"])==0)
        if not search.any():
            return dict(status="NO_PEAK")
        row,col=np.unravel_index(np.argmax(np.where(search,z,-np.inf)),z.shape)
        dx,dy=int(xx[row,col]),int(yy[row,col])
        peak=(x0+dx,y0+dy)
        offset=float(wcs.pixel_to_world(*peak).separation(target).arcsec)
        rr=(xx-dx)**2+(yy-dy)**2
        core=rr<=cfg["coreRadius"]**2
        nfull=int(np.count_nonzero(core&((q&256)!=0)))
        nadc=int(np.count_nonzero(core&((q&2048)!=0)))
        valid=(q==0)&np.isfinite(z)&np.isfinite(e)&(e>0)
        sector=np.floor(np.mod(np.arctan2(yy-dy,xx-dx),2*np.pi)/(np.pi/4)).astype(int)
        wing=[int(np.count_nonzero(valid&(rr>=16)&(rr<=81)&(sector==i))) for i in range(8)]
        ltv=[float(sci.header[k]) for k in ("LTV1","LTV2")]
        ltm=[float(sci.header[k]) for k in ("LTM1_1","LTM2_2")]
        if ltm!=[1,1] or any(sci.header.get(k,0)!=0 for k in ("LTM1_2","LTM2_1")):
            raise ValueError("Unsupported subarray transform")
        filename=meta["root"]+".npz"
        with (stamps/filename).open("xb") as out:
            np.savez(out,sci=z,err=e,dq=q,lowerXY=np.array([x0-r,y0-r],dtype="<i4"))
        checks=dict(centering=offset<=cfg["maxWcsOffsetArcsec"] and math_radius(dx,dy)<cfg["searchRadius"]-0.5,
                    core=nfull==nadc==0,wing=min(wing)>=cfg["minimumWingSupport"])
        return dict(status="RECORDED",chip=int(sci.header["CCDCHIP"]),visit=p["APERTURE"],
                    mjd=float(p["EXPSTART"]),epoch=year,exposureSeconds=float(p["EXPTIME"]),
                    predictedXY=[x0,y0],peakXY=peak,ltv=ltv,chipPeakXY=[peak[i]-ltv[i] for i in (0,1)],
                    offsetArcsec=offset,fullWellNearPeak=nfull,adcNearPeak=nadc,wingCleanPerSector=wing,
                    peakElectrons=float(z[row,col]),dqAtPeak=int(q[row,col]),checks=checks,fitEligible=all(checks.values()),
                    stampFile=filename,stampSha256=hashlib.sha256((stamps/filename).read_bytes()).hexdigest())


def math_radius(x,y):
    return (x*x+y*y)**0.5


def main():
    raw=(root/"protocollo.json").read_bytes()
    cfg=json.loads(raw)
    data={n:pinned(root/n,p) for n,p in cfg["pins"].items()}
    obs=json.loads(data["mast.json"])
    products=json.loads(data["mast-products.json"])
    if any(v["status"]!="COMPLETE" or len(v["data"])!=v["paging"]["rowsFiltered"] for v in (obs,products)):
        raise ValueError("MAST listing incomplete")
    manifest=json.loads(data["flt-selected.json"])
    target_names={x["target"] for x in manifest}
    ids={name:parse_identity(data[name+".txt"]) for name in sorted(target_names)}
    parents=Counter(x["parentObservation"] for x in manifest)
    if (len(ids)!=4 or len(parents)!=cfg["expectedAssociations"]
            or len({x["name"] for x in manifest})!=cfg["expectedFltFiles"] or set(parents.values())!={2}):
        raise ValueError("Unexpected FLT sample")
    if (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Runtime changed")
    stamps.mkdir()
    results=[]
    for item in manifest:
        measured=read_exposure(item,ids[item["target"]],cfg)
        results.append(dict(root=item["root"],target=item["target"],parentObservation=item["parentObservation"],
                            proposal=item["proposal"],**measured))
    report=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(raw).hexdigest(),
                mastPreSm4Rows=sum(x["t_min"]<54955 for x in obs["data"]),
                associations=len(parents),samples=results,identities=ids,nativeExecutions=0,scientificClosures=0)
    with output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()
