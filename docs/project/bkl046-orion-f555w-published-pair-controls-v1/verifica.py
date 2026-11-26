import re
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
from astropy.time import Time
from astropy.utils import iers
iers.conf.auto_download = False
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



def choose_peak(image,quality,x,y,cfg):
    allowed=np.isfinite(image)&((quality&cfg["badGeometryMask"])==0)
    inside=x*x+y*y<=cfg["peakSearchPx"]**2
    scores=np.where(inside&allowed,image,-np.inf)
    if not np.isfinite(scores.max()):
        return None
    peak=np.unravel_index(scores.argmax(),scores.shape)
    return int(x[peak]),int(y[peak])


def count_regions(values,dq,x,y,cfg):
    finite=np.isfinite(values)
    good=finite&(dq==0)
    fw=finite&((dq&256)!=0)
    adc=finite&((dq&2048)!=0)
    result={}
    dist=np.hypot(x,y)
    for r in cfg["coreRadiiPx"]:
        box=dist<=r
        result[str(r)]=dict(total=int(box.sum()),unflagged=int((box&good).sum()),fullWell=int((box&fw).sum()),
                            adc=int((box&adc).sum()))
    rmin,rmax=cfg["wingAnnulusPx"]
    wing=(dist>=rmin)&(dist<=rmax)
    theta=np.mod(np.arctan2(y,x),2*np.pi)
    sectors=np.floor(theta/(np.pi/4)).astype(int)
    return dict(disks=result,wing=dict(
        radii=[rmin,rmax],pixels=int(wing.sum()),unflagged=int((wing&good).sum()),
        cleanPerSector=[int((wing&good&(sectors==i)).sum()) for i in range(8)]))


def analyze(item,source,cfg,cache,expected,stamps):
    reader=FitsRanges(cache,item,cfg["blockBytes"],expected,mode=="acquire")
    if hashlib.sha256(reader.read(65536)).hexdigest()!=item["prefixSha256"]:
        raise ValueError("FLC prefix changed")
    reader.seek(0)
    target=SkyCoord(*source["locationJ2000"],unit=u.deg)
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        p=hdus[0].header
        if (p["ROOTNAME"].lower()!=item["root"] or p["INSTRUME"]!="ACS" or p["DETECTOR"]!="WFC"
            or p["PROPOSID"]!=10246 or "F555W" not in (p["FILTER1"],p["FILTER2"]) or p["EXPTIME"]!=385):
            raise ValueError("FLC instrument or exposure changed")
        where=[]
        for sci in hdus:
            if sci.name!="SCI":
                continue
            wcs=WCS(sci.header,hdus).celestial
            xy=np.asarray(wcs.world_to_pixel(target),float)
            if not np.isfinite(xy).all():
                continue
            x,y=(round(v) for v in xy)
            h,w=sci.shape
            if 0<=x<w and 0<=y<h:
                where.append((sci,wcs,x,y))
        base=dict(h97=source["h97"],root=item["root"],date=p["DATE-OBS"],startUtc=p["TIME-OBS"],
                  expSeconds=float(p["EXPTIME"]),ccdGain=float(p["CCDGAIN"]),
                  nacoSeparationMas=source["separationMas"])
        if len(where)>1:
            raise ValueError("Catalog position intersects two detector chips")
        if not where:
            return dict(base,status="OUTSIDE_CHIPS"),reader.used
        sci,wcs,x,y=where[0]
        dq=hdus["DQ",sci.ver]
        err=hdus["ERR",sci.ver]
        if dq.shape!=sci.shape or err.shape!=sci.shape or sci.header["BUNIT"]!="ELECTRONS":
            raise ValueError("SCI/DQ/ERR shape or unit changed")
        r=cfg["stampRadiusPx"]
        h,w=sci.shape
        base.update(chip=sci.header["CCDCHIP"],scienceExtVer=sci.ver,xyCatalogNearest=[x,y])
        if not (r<=x<w-r and r<=y<h-r):
            return dict(base,status="STAMP_CROSSES_EDGE"),reader.used
        box=np.s_[y-r:y+r+1,x-r:x+r+1]
        signal=sci.section[box].astype("<f4")
        quality=dq.section[box].astype("<i4")
        error=err.section[box].astype("<f4")
        grid_y,grid_x=np.mgrid[-r:r+1,-r:r+1]
        peak=choose_peak(signal,quality,grid_x,grid_y,cfg)
        if peak is None:
            return dict(base,status="PEAK_NOT_AVAILABLE"),reader.used
        dx,dy=peak
        if max(cfg["coreRadiiPx"]+[cfg["wingAnnulusPx"][1]])+max(abs(dx),abs(dy))>r:
            raise ValueError("Peak window is clipped")
        centered=count_regions(signal,quality,grid_x-dx,grid_y-dy,cfg)
        at_catalog=count_regions(signal,quality,grid_x,grid_y,cfg)
        loc=wcs.pixel_to_world(x+dx,y+dy).icrs
        path=stamps/(item["root"]+".npz")
        with path.open("xb") as f:
            np.savez(f,sci=signal,err=error,dq=quality,lowerXY=np.array([x-r,y-r],dtype="<i4"))
        return dict(base,status="RECORDED",peakXY=[x+dx,y+dy],
                    peakSkyRaDec=[float(loc.ra.deg),float(loc.dec.deg)],
                    peakOffsetArcsec=float(loc.separation(target).arcsec),
                    peakAtOuterSearch=math.hypot(dx,dy)>=cfg["peakSearchPx"]-0.5,
                    dqAtPeak=int(quality[dy+r,dx+r]),atCatalog=at_catalog,atPeak=centered,
                    stampFile=path.name,stampSha256=hashlib.sha256(path.read_bytes()).hexdigest()),reader.used



def angular(ra,dec):
    def degrees(parts):
        a,b,c=map(float,parts)
        return math.copysign(abs(a)+b/60+c/3600,a)
    return [15*degrees(ra),degrees(dec)]


def catalog_identity(subject,cfg):
    name=subject["twoMassId"]
    raw=checked(root/(name+".txt"),cfg["simbadSha256"][name]).decode()
    title=re.findall(r"^Object (.+?)\s+---",raw,re.M)
    pos=re.findall(r"^Coordinates\(ICRS,ep=J2000,eq=2000\):\s*(.+?)\s*\(",raw,re.M)
    motion=re.findall(r"^Proper motions:\s+(\S+)\s+(\S+)",raw,re.M)
    if len(title)!=1 or len(pos)!=1 or len(motion)!=1:
        raise ValueError(f"Unresolved source {name}")
    tokens=pos[0].split()
    coord=angular(tokens[:3],tokens[3:])
    p=np.array([float(v) for v in motion[0]]) if "~" not in motion[0] else None
    remote=SkyCoord(*coord,unit=u.deg)
    prior=SkyCoord(*subject["approximateTwoMassLocationJ2000"],unit=u.deg)
    distance=float(remote.separation(prior).arcsec)
    if distance>cfg["maximum2massAndSimbadDifferenceArcsec"]:
        raise ValueError("SIMBAD coordinate differs from 2MASS identity")
    ids=sorted(set(re.findall(r"Gaia DR3 (\d+)",raw)))
    if len(ids)!=1:
        raise ValueError("No unique Gaia ID in SIMBAD")
    return dict(name=title[0].strip(),gaiaId=ids[0],coordinateJ2000=coord,
                simbadTo2massArcsec=distance,properMotionMasPerYear=None if p is None else p.tolist())


def current_coords(identity,epoch):
    ra,dec=identity["coordinateJ2000"]
    p=identity["properMotionMasPerYear"]
    if p is None:
        return [ra,dec]
    t=epoch-2000
    return [ra+p[0]*t/(3.6e6*np.cos(np.deg2rad(dec))),dec+p[1]*t/3.6e6]


def process(item,subject,identity,cfg,cache,expected,stamps):
    primary=checked(root/"prefixes"/(item["root"]+".bin"),item["prefixSha256"])
    header=fits.getheader(io.BytesIO(primary),ext=0)
    epoch=float(Time(header["DATE-OBS"]+"T"+header["TIME-OBS"],scale="utc").jyear)
    coord=current_coords(identity,epoch)
    seeded=dict(locationJ2000=coord,h97=subject["catalogRow"],separationMas=1000*subject["separationArcsec"])
    row,pins=analyze(item,seeded,cfg,cache,expected,stamps)
    row["catalogRow"]=row.pop("h97")
    # The inherited fitter expects "h97" as a tracking key. Here it is the optical catalog row.
    row["h97"]=row["catalogRow"]
    row["catalogSeparationMas"]=row.pop("nacoSeparationMas")
    row["catalogFluxRatioF555W"]=subject["fluxRatioF555W"]
    row["twoMassId"]=subject["twoMassId"]
    row["expectedCoordinateAtExposure"]=coord
    row["dateCorrectedWithProperMotion"]=identity["properMotionMasPerYear"] is not None
    return row,pins


def main():
    config=(root/"protocollo.json").read_bytes()
    cfg=json.loads(config)
    if mode not in ("acquire","replay") or (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Runtime changed")
    report0=json.loads(checked(prior/"riscontro.json",cfg["rosterSha256"]))
    objects=json.loads(checked(root/"fits-objects.json",cfg["objectManifestSha256"]))
    items={i["root"]:i for i in objects}
    subjects=[r for r in report0["acsF555W"] if len(r["hstPotentialExposures"].get("F555W",[]))>=2]
    if [r["catalogRow"] for r in subjects]!=cfg["expectedCatalogRows"]:
        raise ValueError("Comparison roster changed")
    identities={s["twoMassId"]:catalog_identity(s,cfg) for s in subjects}
    work=[(items[o["id"]],s,identities[s["twoMassId"]]) for s in subjects
          for o in s["hstPotentialExposures"]["F555W"]]
    if len(work)!=11 or len(items)!=11:
        raise ValueError("Frozen FLC roster changed")
    cache=root/"ranges"
    if mode=="acquire":
        cache.mkdir(exist_ok=True)
    stamps=Path(sys.argv[6])
    stamps.mkdir()
    manifest=root/"range-sha256.json"
    expected={} if mode=="acquire" else json.loads(manifest.read_bytes())
    with ThreadPoolExecutor(max_workers=cfg["parallelObjects"]) as pool:
        jobs=[pool.submit(process,i,s,a,cfg,cache,expected,stamps) for i,s,a in work]
        results=[job.result() for job in jobs]
    rows=[]
    used={}
    for row,pins in results:
        rows.append(row)
        used.update(pins)
        print(row["catalogRow"],row["root"],row["status"],row.get("atPeak",{}).get("disks",{}).get("3"),flush=True)
    if mode=="acquire":
        with manifest.open("x",encoding="ascii",newline="\n") as stream:
            stream.write(json.dumps(used,sort_keys=True,indent=2)+"\n")
    elif used!=expected:
        raise ValueError("Replay ranges differ")
    result=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(config).hexdigest(),
                rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
                identities=identities,observations=rows,nativeExecutions=0,scientificClosures=0)
    with report.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
