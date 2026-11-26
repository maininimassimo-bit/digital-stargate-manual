
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



def flag_components(mark):
    pending={(int(y),int(x)) for y,x in np.argwhere(mark)}
    while pending:
        seed=pending.pop()
        group=[seed]
        for y,x in group:
            for dy,dx in ((1,0),(-1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)):
                pixel=(y+dy,x+dx)
                if pixel in pending:
                    pending.remove(pixel)
                    group.append(pixel)
        yield np.asarray(group)


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


def long_components(item,cfg,cache,expected):
    reader=open_subject(item,cfg,cache,expected)
    found=[]
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        for sci in hdus:
            if sci.name!="SCI":
                continue
            dq,wcs=chip_geometry(sci,hdus)
            flags=dq.data
            mark=((flags&cfg["detectFullWellMask"])!=0)&((flags&cfg["badGeometryMask"])==0)
            for pixels in flag_components(mark):
                y,x=pixels.mean(axis=0)
                sky=wcs.pixel_to_world(x,y).icrs
                at=pixels[:,0],pixels[:,1]
                found.append(dict(chip=sci.header["CCDCHIP"],xy=[float(x),float(y)],
                                  count=len(pixels),raDeg=float(sky.ra.deg),decDeg=float(sky.dec.deg),
                                  adcCount=int(((flags[at]&2048)!=0).sum())))
    return sorted(found,key=lambda a:(a["chip"],a["xy"])),reader.used


def match_components(a,b,max_arcsec):
    left=SkyCoord([row["raDeg"] for row in a],[row["decDeg"] for row in a],unit=u.deg)
    right=SkyCoord([row["raDeg"] for row in b],[row["decDeg"] for row in b],unit=u.deg)
    distance=left[:,None].separation(right[None,:]).arcsec
    near=distance<=max_arcsec
    accepted=[]
    for i,j in np.argwhere(near):
        if near[i,:].sum()!=1 or near[:,j].sum()!=1:
            continue
        ra=(a[i]["raDeg"]+b[j]["raDeg"])/2
        dec=(a[i]["decDeg"]+b[j]["decDeg"])/2
        accepted.append(dict(left=int(i),right=int(j),separationArcsec=float(distance[i,j]),
                             skyRaDec=[ra,dec]))
    return accepted,int(near.sum())


def reference_support(item,cfg,cache,expected,candidates):
    reader=open_subject(item,cfg,cache,expected)
    r=cfg["referenceRadiusPx"]
    y,x=np.ogrid[-r:r+1,-r:r+1]
    disk=x*x+y*y<=r*r
    supports=[{"status":"OUTSIDE_OR_EDGE"} for _ in candidates]
    if len(candidates)==0:
        return supports,reader.used
    ra,dec=np.asarray([c["skyRaDec"] for c in candidates]).T
    sky=SkyCoord(ra,dec,unit=u.deg)
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        for sci in hdus:
            if sci.name!="SCI":
                continue
            dq,wcs=chip_geometry(sci,hdus)
            x,y=wcs.world_to_pixel(sky)
            h,w=sci.shape
            for i,(px,py) in enumerate(zip(x,y,strict=True)):
                if not np.isfinite([px,py]).all():
                    continue
                ix,iy=round(px),round(py)
                if not (r<=ix<w-r and r<=iy<h-r):
                    continue
                if supports[i]["status"]!="OUTSIDE_OR_EDGE":
                    raise ValueError("Pair falls on two chips")
                box=np.s_[iy-r:iy+r+1,ix-r:ix+r+1]
                flags=dq.section[box][disk]
                data=sci.section[box][disk]
                center_flag=int(dq.section[iy:iy+1,ix:ix+1][0,0])
                finite=np.isfinite(data)
                status="CLEAN" if (flags==0).all() and finite.all() else "DQ_OR_NONFINITE"
                supports[i]=dict(status=status,chip=sci.header["CCDCHIP"],
                                 pixelXY=[ix,iy],centerDq=center_flag,
                                 goodPixels=int(((flags==0)&finite).sum()),aperturePixels=int(disk.sum()),
                                 saturationFlagged=int(((flags&cfg["anySaturationMask"])!=0).sum()))
    return supports,reader.used


def main():
    cfg_bytes=(root/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_bytes)
    if mode not in ("acquire","replay") or (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Unexpected mode or runtime")
    subjects=json.loads(checked(prior/"riscontro-intestazioni.json",cfg["priorReportSha256"]))
    items={m["root"]:m for m in subjects["members"]}
    order=cfg["replicaRoots"]+cfg["referenceRoots"]
    expected_order=[774,822,150,150,340]
    if [items[name]["f658nExposureSeconds"] for name in order]!=expected_order:
        raise ValueError("Exposure roles changed")
    cache=root/"ranges"
    if mode=="acquire":
        cache.mkdir(exist_ok=True)
    manifest=root/"range-sha256.json"
    expected={} if mode=="acquire" else json.loads(manifest.read_bytes())
    comps=[]
    ranges={}
    for name in cfg["replicaRoots"]:
        found,used=long_components(items[name],cfg,cache,expected)
        comps.append(found)
        ranges.update(used)
        print(name,len(found),sum(c["count"] for c in found),flush=True)
    if not all(comps):
        raise ValueError("No flagged detector components")
    candidates,within=match_components(*comps,cfg["matchRadiusArcsec"])
    for name in cfg["referenceRoots"]:
        supports,used=reference_support(items[name],cfg,cache,expected,candidates)
        for c,s in zip(candidates,supports,strict=True):
            c.setdefault("referenceSupport",{})[name]=s
        ranges.update(used)
        print(name,Counter(s["status"] for s in supports),flush=True)
    eligible=0
    for c in candidates:
        c["allReferenceDisksClean"]=all(
            s["status"]=="CLEAN" for s in c["referenceSupport"].values())
        eligible+=c["allReferenceDisksClean"]
    if mode=="acquire":
        with manifest.open("x",encoding="ascii",newline="\n") as stream:
            stream.write(json.dumps(ranges,sort_keys=True,indent=2)+"\n")
    elif ranges!=expected:
        raise ValueError("Replay used a different range set")
    output=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(cfg_bytes).hexdigest(),
                rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
                ranges=len(ranges), components=dict(zip(cfg["replicaRoots"],comps,strict=True)),
                allPairsInsideRadius=within,candidates=candidates,
                oneToOnePairs=len(candidates),allReferenceDisksClean=eligible,
                scientificClosures=0,nativeExecutions=0)
    with report.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(output,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("pairs",within,"one to one",len(candidates),"clean",eligible,flush=True)


if __name__=="__main__":
    main()
