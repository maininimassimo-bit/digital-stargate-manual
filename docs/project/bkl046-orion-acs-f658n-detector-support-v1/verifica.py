
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


def sample(item,sky,cfg,cache,expected):
    flags=np.full(sky.shape,-1,dtype=np.int64)
    flux=np.full(sky.shape,np.nan)
    chips=[]
    reader=FitsRanges(cache,item,cfg["blockBytes"],expected,mode=="acquire")
    prefix=reader.read(65536)
    if hashlib.sha256(prefix).hexdigest()!=item["prefixSha256"]:
        raise ValueError("Primary FITS prefix differs from prior check")
    reader.seek(0)
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        p=hdus[0].header
        if p["ROOTNAME"].lower()!=item["root"] or p["EXPTIME"]!=item["f658nExposureSeconds"]:
            raise ValueError("Unexpected FITS subject")
        for sci in hdus:
            if sci.name!="SCI":
                continue
            dq=hdus["DQ",sci.ver]
            if dq.shape!=sci.shape or sci.header["BUNIT"]!="ELECTRONS":
                raise ValueError("Unexpected SCI/DQ geometry or units")
            wcs=WCS(sci.header,hdus).celestial
            x,y=wcs.world_to_pixel(sky)
            finite=np.isfinite(x)&np.isfinite(y)
            xi,yi=(np.rint(np.where(finite,v,-1)).astype(int) for v in (x,y))
            h,w=sci.shape
            keep=finite&(xi>=0)&(xi<w)&(yi>=0)&(yi<h)
            if np.any(keep&(flags>=0)):
                raise ValueError("Same sky sample intersects two chips within one FITS file")
            ix,iy=xi[keep],yi[keep]
            info={"ccdChip":sci.header["CCDCHIP"],"extver":sci.ver,"gridSamples":int(keep.sum())}
            if len(ix):
                a,b,c,d=int(ix.min()),int(ix.max()),int(iy.min()),int(iy.max())
                if b-a>300 or d-c>300:
                    raise ValueError("Projection window exceeds bound")
                patch=sci.section[c:d+1,a:b+1]
                quality=dq.section[c:d+1,a:b+1]
                flags[keep]=quality[iy-c,ix-a]
                flux[keep]=patch[iy-c,ix-a]
                info["boundsXY"]=[a,b,c,d]
                info["uniqueDetectorPixels"]=len(set(zip(ix.tolist(),iy.tolist(),strict=True)))
            chips.append(info)
    finite=(flags>=0)&np.isfinite(flux)
    valid=finite & ~((flags & cfg["badGeometryMask"])!=0)
    sat=valid & ((flags&cfg["saturationMask"])!=0)
    good=valid & (flags==0)
    if np.any(sat & good):
        raise ValueError("Saturation and clean masks coincide")
    hist=Counter(int(v) for v in flags[finite])
    summary=dict(root=item["root"],seconds=item["f658nExposureSeconds"],date=item["date"],chips=chips,
                 validSamples=int(valid.sum()),goodSamples=int(good.sum()),saturatedSamples=int(sat.sum()),
                 saturatedFullWell=int((valid&((flags&256)!=0)).sum()),
                 saturatedADC=int((valid&((flags&2048)!=0)).sum()),
                 dqHistogram=dict(sorted(hist.items())))
    return summary,valid,good,sat,reader.used


def main():
    cfg_bytes=(root/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_bytes)
    if (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
        raise ValueError("Runtime version changed")
    previous=json.loads(checked(prior/"riscontro-intestazioni.json",cfg["priorReportSha256"]))
    cache=root/"ranges"
    if mode=="acquire":
        cache.mkdir(exist_ok=True)
    manifest=root/"range-sha256.json"
    expected={} if mode=="acquire" else json.loads(manifest.read_bytes())
    center=SkyCoord(*previous["geometryPoint"],unit=u.deg,frame="icrs")
    n=cfg["halfGridSteps"]
    dy,dx=np.mgrid[-n:n+1,-n:n+1]*cfg["gridSpacingArcsec"]
    relative=SkyCoord(lon=dx*u.arcsec,lat=dy*u.arcsec,frame=center.skyoffset_frame())
    sky=relative.icrs
    used={}
    data={}
    geometry=[]
    for item in previous["members"]:
        row,valid,good,sat,pins=sample(item,sky,cfg,cache,expected)
        used.update(pins)
        geometry.append(row)
        data[item["root"]]=(valid,good,sat)
        print(row["root"],row["validSamples"],row["saturatedSamples"],flush=True)
    if mode=="acquire":
        with manifest.open("x",encoding="ascii",newline="\n") as stream:
            stream.write(json.dumps(used,sort_keys=True,indent=2)+"\n")
    elif used!=expected:
        raise ValueError("Replay used a different range set")
    short=[r["root"] for r in geometry if r["seconds"]==150]
    held=[r["root"] for r in geometry if r["seconds"]==340]
    if len(short)!=2 or len(held)!=1:
        raise ValueError("Reference roster changed")
    predictors=np.logical_and.reduce([data[name][1] for name in short])
    withheld=data[held[0]][1]
    base=predictors&withheld
    comparison={}
    for row in geometry:
        if row["seconds"]<=340:
            continue
        valid,_,sat=data[row["root"]]
        common=base&valid
        comparison[row["root"]]=dict(commonCleanReferenceSamples=int(common.sum()),
                                      longFlaggedAndAllReferencesClear=int((common&sat).sum()))
    longest=[r["root"] for r in geometry if r["seconds"] in (774,822)]
    if len(longest)!=2:
        raise ValueError("Long comparison roster changed")
    intersection=base & data[longest[0]][2] & data[longest[1]][2]
    shared=dict(exposures=longest,gridPositions=int(intersection.sum()),
                offsetsArcsecXY=np.column_stack([dx[intersection],dy[intersection]]).tolist())
    result=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(cfg_bytes).hexdigest(),
                rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
                rangeBlocks=len(used),gridPositions=sky.size,exposures=geometry,
                shortAndHeldoutGoodSamples=int(base.sum()),comparison=comparison,sharedLongSaturation=shared,
                sampleSemantics="Nearest real detector pixel at each fixed sky position, counts can repeat detector pixels.",
                nativeExecutions=0,scientificClosures=0)
    with report.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps(comparison),flush=True)


if __name__=="__main__":
    main()
