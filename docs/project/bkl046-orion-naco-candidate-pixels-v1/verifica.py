import re
import xml.etree.ElementTree as ET
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
from astropy.io import fits, votable
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
                  gaiaId=source["gaiaId"],projectedICRS=source["locationJ2000"])
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
        path=stamps/("{}-{}.npz".format(source["h97"],item["root"]))
        with path.open("xb") as f:
            np.savez(f,sci=signal,err=error,dq=quality,lowerXY=np.array([x-r,y-r],dtype="<i4"))
        return dict(base,status="RECORDED",peakXY=[x+dx,y+dy],
                    peakSkyRaDec=[float(loc.ra.deg),float(loc.dec.deg)],
                    peakOffsetArcsec=float(loc.separation(target).arcsec),
                    peakAtOuterSearch=math.hypot(dx,dy)>=cfg["peakSearchPx"]-0.5,
                    dqAtPeak=int(quality[dy+r,dx+r]),atCatalog=at_catalog,atPeak=centered,
                    stampFile=path.name,stampSha256=hashlib.sha256(path.read_bytes()).hexdigest()),reader.used



def project(row, epoch):
    dt = epoch-row["ref_epoch"]
    return [row["ra"]+dt*row["pmra"]/(3.6e6*math.cos(math.radians(row["dec"]))),
            row["dec"]+dt*row["pmdec"]/3.6e6]


def identity_catalog(cfg):
    raw = checked(root/"gaia.xml", cfg["gaiaSha256"])
    ns = {"v": "http://www.ivoa.net/xml/VOTable/v1.3"}
    resource = ET.fromstring(raw).find("v:RESOURCE", ns)
    if [x.get("value") for x in resource.findall("v:INFO", ns) if x.get("name") == "QUERY_STATUS"] != ["OK"]:
        raise ValueError("Gaia query status changed")
    table = votable.parse_single_table(io.BytesIO(raw)).to_table()
    rows = [dict(zip(table.colnames, row, strict=True)) for row in table]
    by_id = {str(r["source_id"]): r for r in rows}
    if len(rows) != len(by_id) or len(by_id) != len(cfg["simbadSha256"]):
        raise ValueError("Gaia cardinality mismatch")
    output = {}
    used = set()
    for key, sha in sorted(cfg["simbadSha256"].items(), key=lambda x: int(x[0])):
        raw = checked(root/f"H97-{key}.txt",sha).decode("utf-8")
        names = re.findall(r"^Object (.+?)\s+---", raw, re.M)
        gaia = set(re.findall(r"Gaia DR3 (\d+)", raw))
        coords = re.findall(r"^Coordinates\(ICRS,ep=J2000,eq=2000\):\s*(.+?)\s*\(",raw,re.M)
        if len(names)!=1 or len(gaia)!=1 or len(coords)!=1 or not re.search(rf"\[H97b\] +{key}\b", raw):
            raise ValueError(f"Unresolved SIMBAD identity H97 {key}")
        uid = gaia.pop()
        if uid in used or uid not in by_id:
            raise ValueError(f"Unresolved Gaia identity H97 {key}")
        used.add(uid)
        record = by_id[uid]
        astrometry = {k:float(record[k]) for k in ("ra","dec","pmra","pmdec","ref_epoch")}
        src = SkyCoord(coords[0],unit=(u.hourangle,u.deg))
        predicted = SkyCoord(*project(astrometry, 2000),unit=u.deg)
        agreement = src.separation(predicted).arcsec
        output[int(key)] = dict(gaiaId=uid, title=names[0], j2000=project(astrometry,2000),
                                catalogueAgreementArcsec=float(agreement),
                                status="AGREES" if agreement <= cfg["maximumAgreementArcsec"] else "POSITION_DISAGREES",
                                gaiaRuWe=float(record["ruwe"]), gaiaGmag=float(record["phot_g_mean_mag"]),
                                gaiaSolution=int(record["astrometric_params_solved"]),
                                gaiaDuplicatedSource=bool(record["duplicated_source"]), motionCatalog=astrometry)
    return output


def main():
    raw = (root/"protocollo.json").read_bytes()
    cfg = json.loads(raw)
    if mode not in ("acquire","replay") or (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Runtime or mode changed")
    ids = identity_catalog(cfg)
    observations = json.loads(checked(prior/"riscontro.json",cfg["rosterSha256"]))["records"]
    candidates = [r for r in observations if r["cohortCandidate"]]
    if set(ids) != {r["h97"] for r in candidates}:
        raise ValueError("Candidate roster changed")
    items = {p["root"]:p for p in json.loads(checked(root/"fits-objects.json",cfg["objectManifestSha256"]))}
    if set(items) != {o["id"] for r in candidates for o in r["hstPotentialExposures"]}:
        raise ValueError("Exposure roster changed")
    epoch = {}
    for name, item in items.items():
        primary = checked(root/"prefixes"/f"{name}.bin",item["prefixSha256"])
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",message="File may have been truncated.*")
            header = fits.getheader(io.BytesIO(primary),ext=0)
        epoch[name] = float(Time(header["DATE-OBS"]+"T"+header["TIME-OBS"],scale="utc").jyear)
    cache = root/"ranges"
    manifest = root/"range-sha256.json"
    expected = {} if mode=="acquire" else json.loads(manifest.read_bytes())
    stamps = Path(sys.argv[6])
    stamps.mkdir(exist_ok=True)
    if any(stamps.iterdir()):
        raise ValueError("Stamp output directory must be empty")
    if mode=="acquire":
        cache.mkdir(exist_ok=True)
    rows = []
    used = {}
    for candidate in candidates:
        key = candidate["h97"]
        identity = ids[key]
        historic = SkyCoord(*candidate["h97CatalogLocationJ2000"],unit=u.deg)
        offset = float(historic.separation(SkyCoord(*identity["j2000"],unit=u.deg)).arcsec)
        for exposure in candidate["hstPotentialExposures"]:
            name = exposure["id"]
            if identity["status"] != "AGREES":
                rows.append(dict(h97=key,root=name,status="IDENTITY_NOT_CONFIRMED"))
                continue
            coords = project(identity["motionCatalog"],epoch[name])
            source = dict(h97=key,gaiaId=identity["gaiaId"],locationJ2000=coords)
            row,pins = analyze(items[name],source,cfg,cache,expected,stamps)
            core = row.get("atPeak",{}).get("disks",{}).get("3",{})
            usable = (row["status"]=="RECORDED" and not row["peakAtOuterSearch"]
                      and row["peakOffsetArcsec"]<=cfg["maximumPeakResidualArcsec"]
                      and core["fullWell"]==core["adc"]==0)
            row.update(geometricAndUnsaturated=usable,historicalToGaiaArcsec=offset,
                       observationEpochJulianYear=epoch[name])
            rows.append(row)
            used.update(pins)
            print(key,name,row["status"],usable,flush=True)
    if mode=="acquire":
        with manifest.open("x",encoding="utf-8",newline="\n") as f:
            json.dump(used,f,sort_keys=True,indent=2)
            f.write("\n")
    elif used!=expected:
        raise ValueError("Replay range set differs")
    result = dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(raw).hexdigest(),
                  rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
                  identities=ids,observations=rows,opticalNegativeLabelsQualified=0,
                  nativeExecutions=0,scientificClosures=0)
    with report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()