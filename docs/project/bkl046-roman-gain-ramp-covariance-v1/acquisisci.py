"""Capture header and fixed science row bands with checked HTTP ranges."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def capture_range(url, lo, length, tag=None):
    hi = lo+length-1
    headers = {"Range":f"bytes={lo}-{hi}","Accept-Encoding":"identity"}
    if tag is not None:
        headers["If-Match"] = tag
    with urlopen(Request(url,headers=headers),timeout=25) as response:
        match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)",response.headers.get("Content-Range",""))
        received = response.headers.get("ETag","")
        require(response.status == 206 and match and tuple(map(int,match.groups()[:2])) == (lo,hi)
                and received.startswith('"') and (tag is None or tag == received),
                "Range or identity changed")
        raw = response.read(length+1)
        require(len(raw) == length,"Range length")
        return raw, received, int(match[3])


def parse_header(raw, fits, name):
    def segment(start):
        for offset in range(start,len(raw),80):
            if raw[offset:offset+8] == b"END     ":
                stop = (offset+80+2879)//2880*2880
                return fits.Header.fromstring(raw[start:stop].decode("ascii"),sep=""),stop
        raise ValueError("Missing FITS END")
    p,offset = segment(0)
    sci,start = segment(offset)
    dims = [sci[f"NAXIS{i}"] for i in range(1,5)]
    require(p["NAXIS"]==0 and p["FILENAME"]==name and p["TESTTYPE"]=="GAIN"
            and p["DETECTOR"]=="21816" and p["READMODE"]=="Diff" and p["REFOUT"]
            and p["WAVELEN"]==1400 and p["NOUTPUTS"]==32 and p["NGROUPS"]==11
            and sci["EXTNAME"]=="SCI" and sci["BITPIX"]==16 and sci["BZERO"]==32768
            and sci["BSCALE"]==1 and dims==[4224,4096,11,1],"Science header changed")
    return start,dims,{k:p[k] for k in ("DATE-BEG","TGROUP","EFFEXPTM","READMODE","DETECTOR")}


def main():
    cli = ArgumentParser(description=__doc__)
    for name in ("protocol","dependencies","output"):
        cli.add_argument(name,type=Path)
    a = cli.parse_args()
    raw = a.protocol.read_bytes()
    cfg = json.loads(raw)
    require(cfg["schema"]=="BKL046_ROMAN_GAIN_RAMP_V1","Protocol")
    sys.path.insert(0,str(a.dependencies))
    from astropy.io import fits
    source = a.output/"source"
    source.mkdir(parents=True)

    def get(i):
        stem=f"21816_E{i:03}"
        name=stem+".fits"
        url=cfg["base"]+name
        header,tag,total=capture_range(url,0,cfg["headerBytes"])
        start,dims,meta=parse_header(header,fits,name)
        width,height,*_=dims
        members=[]
        def save(filename,payload,offset,frame):
            (source/filename).write_bytes(payload)
            members.append(dict(file=filename,sha256=sha256(payload).hexdigest(),offset=offset,bytes=len(payload),frame=frame))
        save(stem+"-header.bin",header,0,None)
        y0,y1=cfg["bandRows"]
        if i<cfg["exposures"]:
            for j in cfg["frames"]:
                offset=start+2*width*(j*height+y0)
                pixels,_,size=capture_range(url,offset,2*width*(y1-y0),tag)
                require(size==total,"Object length changed")
                save(f"{stem}-r{j:02}.bin",pixels,offset,j)
        return dict(exposure=i,url=url,etag=tag,objectBytes=total,dimensions=dims,dataOffset=start,
                    metadata=meta,members=members)
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows=list(pool.map(get,range(1,cfg["exposures"]+1)))
    result=dict(schema="BKL046_ROMAN_GAIN_RANGE_CAPTURE_V1",protocolSha256=sha256(raw).hexdigest(),
                acquisitionProgramSha256=sha256(Path(__file__).read_bytes()).hexdigest(),records=rows,
                fullFitsHashesVerified=False)
    with (a.output/"acquisizione.json").open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True)
        f.write("\n")


if __name__=="__main__":
    main()