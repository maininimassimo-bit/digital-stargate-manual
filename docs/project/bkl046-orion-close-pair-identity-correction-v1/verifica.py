from xml.etree import ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

from collections import Counter
import hashlib
import io
import json
import math
from pathlib import Path
import re
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



def from_sexagesimal(ra,dec):
    def angle(parts):
        sign=-1 if parts[0].startswith("-") else 1
        a,b,c=map(float,parts)
        return sign*(abs(a)+b/60+c/3600)
    return [15*angle(ra),angle(dec)]


def identities(root,cfg):
    xml=checked(root/"gaia.xml",cfg["gaiaSha256"])
    ns={"v":"http://www.ivoa.net/xml/VOTable/v1.3"}
    body=ET.fromstring(xml).find("v:RESOURCE",ns)
    statuses=[i.attrib["value"] for i in body.findall("v:INFO",ns) if i.attrib["name"]=="QUERY_STATUS"]
    if statuses!=["OK"]:
        raise ValueError("Incomplete Gaia response")
    tab=body.find("v:TABLE",ns)
    cols=[f.attrib["name"] for f in tab.findall("v:FIELD",ns)]
    rows=[dict(zip(cols,[col.text for col in tr.findall("v:TD",ns)],strict=True))
          for tr in tab.findall("v:DATA/v:TABLEDATA/v:TR",ns)]
    by_id={v["source_id"]:v for v in rows}
    out={}
    for label,sha in cfg["simbadSha256"].items():
        name=int(label)
        source=checked(root/f"H97-{name}.txt",sha).decode("utf-8")
        if name==488:
            aliases=[]
            for line in source.splitlines():
                if line.startswith(("1|","2|")):
                    candidate=line.split("|")
                    m=candidate[4].split()
                    aliases.append(dict(name=candidate[2].strip(),icrsJ2000=from_sexagesimal(m[:3],m[3:])))
            if len(aliases)!=2:
                raise ValueError("Ambiguous result roster changed")
            out[name]=dict(status="AMBIGUOUS_IDENTIFIER",alternatives=aliases)
            continue
        pos=re.search(r"^Coordinates\(ICRS,ep=J2000,eq=2000\):\s*(.+?)\s*\(",source,re.M)
        identifier=set(re.findall(r"Gaia DR3 (\d+)",source))
        main=re.search(r"^Object (.+?)\s+---",source,re.M)
        if len(identifier)!=1 or pos is None or main is None:
            raise ValueError("Missing unique SIMBAD identity")
        uid=identifier.pop()
        gaia=by_id[uid]
        astrometry={k:float(gaia[k]) for k in ("ra","dec","pmra","pmdec","ref_epoch")}
        m=pos.group(1).split()
        simbad=from_sexagesimal(m[:3],m[3:])
        calc=project(astrometry,2000)
        accuracy=SkyCoord(*simbad,unit=u.deg).separation(SkyCoord(*calc,unit=u.deg)).arcsec
        if accuracy>cfg["maximumCatalogAgreementArcsec"]:
            raise ValueError("Gaia ID position does not reproduce SIMBAD")
        out[name]=dict(status="IDENTIFIED",name=main.group(1).strip(),gaiaId=uid,
                       simbadICRSJ2000=simbad,motionCatalog=astrometry,agreementArcsec=float(accuracy))
    return out


def project(row,epoch):
    dt=epoch-row["ref_epoch"]
    return [row["ra"]+dt*row["pmra"]/(3.6e6*np.cos(np.deg2rad(row["dec"]))),
            row["dec"]+dt*row["pmdec"]/3.6e6]


def main():
    cfg_bytes=(root/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_bytes)
    if mode not in ("acquire","replay") or (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Unexpected runtime or mode")
    old=json.loads(checked(prior/"riscontro.json",cfg["rosterSha256"]))["observations"]
    items={v["root"]:v for v in json.loads(checked(prior/"fits-objects.json",cfg["objectManifestSha256"]))}
    names=identities(root,cfg)
    cache=root/"ranges"
    manifest=root/"range-sha256.json"
    expected={} if mode=="acquire" else json.loads(manifest.read_bytes())
    stamps=Path(sys.argv[6])
    stamps.mkdir()
    rows=[]
    used={}
    for item in old:
        case=names[item["h97"]]
        if case["status"]!="IDENTIFIED":
            continue
        epoch=float(Time(item["date"]+"T"+item["startUtc"],scale="utc").jyear)
        coord=project(case["motionCatalog"],epoch)
        src=dict(h97=item["h97"],locationJ2000=coord,separationMas=item["nacoSeparationMas"])
        run,pins=analyze(items[item["root"]],src,cfg,cache,expected,stamps)
        if "xyCatalogNearest" in run:
            old_stamp=read_old_stamp(prior,item)
            test=np.array(run["xyCatalogNearest"])
            run["oldStampContainsUpdatedTarget"]=bool(np.all(test>=old_stamp) and np.all(test<old_stamp+41))
            run["oldToNewDetectorPx"]=float(np.linalg.norm(test-np.array(item["xyCatalogNearest"])))
        run["targetCoordinatesAtExposureEpoch"]=coord
        run["observationEpochJulianYear"]=epoch
        rows.append(run)
        used.update(pins)
        print(run["h97"],run["root"],run["status"],run.get("oldStampContainsUpdatedTarget"),
              run.get("oldToNewDetectorPx"),flush=True)
    if mode=="acquire":
        with manifest.open("x",encoding="ascii",newline="\n") as f:
            f.write(json.dumps(used,sort_keys=True,indent=2)+"\n")
    elif used!=expected:
        raise ValueError("Replay range set differs")
    result=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(cfg_bytes).hexdigest(),
                rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),identities=names,
                observations=rows,nativeExecutions=0,scientificClosures=0)
    with report.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")


def read_old_stamp(prior,item):
    data=checked(prior/"stamps"/item["stampFile"],item["stampSha256"])
    with np.load(io.BytesIO(data),allow_pickle=False) as archive:
        return archive["lowerXY"]


if __name__=="__main__":
    main()
