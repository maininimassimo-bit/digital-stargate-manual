
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
from subprocess import run
from zipfile import ZipFile
import io
import json
import re
import struct
import zlib


def require(expected, reason):
    if not expected:
        raise ValueError(reason)


def metadata(blob):
    require(blob[:2] in (b"II",b"MM") and blob[8:10] == b"CR","not Canon CR2")
    order = "<" if blob[:2] == b"II" else ">"
    def read(fmt,offset):
        return struct.unpack_from(order+fmt,blob,offset)
    def entries(offset):
        count, = read("H",offset)
        require(count<=1024,"too many TIFF entries")
        return {tag:(kind,n,at+8) for at in range(offset+2,offset+2+12*count,12)
                for tag,kind,n in [read("HHI",at)]}
    def field(table,tag,kind,size):
        actual,n,at = table[tag]
        require(actual==kind and 0<n*size<=256,"invalid TIFF field")
        if n*size>4:
            at, = read("I",at)
        require(0<=at<=len(blob)-n*size,"TIFF field extends outside sampled prefix")
        return blob[at:at+n*size]
    def string(table,tag):
        return field(table,tag,2,1).rstrip(b"\0").decode("ascii")
    root = entries(read("I",4)[0])
    pointer, = struct.unpack(order+"I",field(root,34665,4,4))
    exif = entries(pointer)
    a,b = struct.unpack(order+"II",field(exif,33434,5,8))
    iso, = struct.unpack(order+"H",field(exif,34855,3,2))
    require(a>0 and b>0 and iso>0,"invalid exposure")
    return dict(camera=string(root,272),exposureFraction=f"{a}/{b}",iso=iso,
                originalLocalTime=string(exif,36867))


def parse_prefix(blob,name):
    magic,_,flags,compression,_,_,_,_,_,n,x=struct.unpack_from("<4s5H3I2H",blob)
    require(magic==b"PK\x03\x04" and flags&1==0 and compression==8,"local header differs")
    require(blob[30:30+n].decode("ascii")==name,"local header name differs")
    part = blob[30+n+x:]
    require(len(part)>0,"prefix has no payload")
    return metadata(zlib.decompressobj(-15).decompress(part,65536))


def acquire(start, length, cfg):
    end=start+length-1
    reply=run(["curl.exe","--silent","--show-error","--fail","--location","--proto","=https",
               "--range",f"{start}-{end}","--header","If-Match: "+cfg["etag"],
               "--max-time","15","--max-filesize",str(length),
               "--dump-header","-","--output","-",cfg["url"]],
              capture_output=True,check=True,timeout=20)
    require(b"\r\n\r\n" in reply.stdout,"missing response headers")
    headers,blob=reply.stdout.split(b"\r\n\r\n",1)
    lines=headers.decode("ascii").splitlines()
    fields={k.lower():v.strip() for k,v in (line.split(":",1) for line in lines[1:] if ":" in line)}
    require(re.match(r"^HTTP/(?:1\.1|2) 206(?: |$)",lines[0]) is not None
            and fields.get("etag")==cfg["etag"]
            and fields.get("content-range")==f"bytes {start}-{end}/{cfg['size']}"
            and len(blob)==length,"origin range differs")
    return blob


def main():
    parser=ArgumentParser()
    parser.add_argument("directory",type=Path)
    parser.add_argument("mode",choices=("acquire","replay"))
    parser.add_argument("report",type=Path)
    args=parser.parse_args()
    cfg_bytes=(args.directory/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_bytes)
    tail=(args.directory/"central-tail.bin").read_bytes()
    require(sha256(tail).hexdigest()==cfg["tailSha256"],"central directory tail changed")
    with ZipFile(io.BytesIO(tail)) as source:
        entries=source.infolist()
        candidates=sorted((e for e in entries if re.fullmatch(
            r"OrionNebula/(lights|darks|flats|biases)/IMG_[0-9]{4}\.CR2",e.filename)),key=lambda e:e.filename)
    require(len(entries)==len({e.filename for e in entries}),"ambiguous ZIP")
    require(len(candidates)==sum(cfg["expectedRawCounts"].values()),"raw count differs")
    root=args.directory/"prefixes"
    if args.mode=="acquire":
        root.mkdir(exist_ok=True)

    def inspect(entry):
        name=entry.filename
        dest=root/(name.split("/")[-2]+"-"+name.split("/")[-1]+".bin")
        start=entry.header_offset+cfg["size"]-len(tail)
        if not dest.exists() and args.mode=="acquire":
            blob=acquire(start,cfg["sampleBytes"],cfg)
            result=parse_prefix(blob,name)
            with dest.open("xb") as f:
                f.write(blob)
        else:
            blob=dest.read_bytes()
            result=parse_prefix(blob,name)
        return dict(name=name,offset=start,prefixSha256=sha256(blob).hexdigest(),**result)

    with ThreadPoolExecutor(max_workers=cfg["httpConcurrency"]) as pool:
        rows=list(pool.map(inspect,candidates))

    groups={}
    for row in rows:
        kind=row["name"].split("/")[-2]
        keys=groups.setdefault(kind,{})
        mode=f"{row['camera']} | ISO {row['iso']} | {row['exposureFraction']} s"
        keys[mode]=keys.get(mode,0)+1
    require({k:sum(v.values()) for k,v in groups.items()}==cfg["expectedRawCounts"],"group counts differ")
    report=dict(schema=cfg["schema"],source=cfg["url"],sourceEtag=cfg["etag"],
                prefixBytes=cfg["sampleBytes"],protocolSha256=sha256(cfg_bytes).hexdigest(),
                countsByExposure=groups,records=rows,scientificClosures=0,nativeExecutions=0)
    with args.report.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps(groups,sort_keys=True))


if __name__=="__main__":
    main()
