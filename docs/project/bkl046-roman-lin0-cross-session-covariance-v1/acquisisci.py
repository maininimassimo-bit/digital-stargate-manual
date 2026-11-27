"""Capture two fixed Roman LIN0 bands by exact byte range."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import ModuleType


def require(ok,why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return sha256(raw).hexdigest()


def parse(raw,fits,name):
    def segment(start):
        end=next(i for i in range(start,len(raw),80) if raw[i:i+8]==b"END     ")
        stop=(end+80+2879)//2880*2880
        return fits.Header.fromstring(raw[start:stop].decode("ascii"),sep=""),stop
    h,p=segment(0)
    s,start=segment(p)
    expected=dict(FILENAME=name,DETECTOR="21816",TESTTYPE="LINEARITY",WAVELEN=1400.0,READMODE="Diff",
                  SCESN="105",NOUTPUTS=32,NGROUPS=42,FASTAX4="A1",REFOUT=True,DEINTERL=True)
    require(all(h[k]==v for k,v in expected.items()) and s["EXTNAME"]=="SCI"
            and (s["BITPIX"],s["BSCALE"],s["BZERO"])==(16,1,32768)
            and [s[f"NAXIS{i}"] for i in range(1,5)]==[4224,4096,42,1],"LIN0 FITS configuration")
    return start,{k:h[k] for k in ("DATE-BEG","TGROUP","READMODE","LODFILE","SCESN","WAVELEN")}


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for n in ("root","ramp","dependencies"):
        cli.add_argument(n,type=Path)
    args=cli.parse_args()
    raw=(args.root/"protocollo.json").read_bytes()
    cfg=json.loads(raw)
    source=args.ramp/"acquisisci.py"
    acq_raw=source.read_bytes()
    require(sha(acq_raw)==cfg["gainHelper"],"Range helper changed")
    acq=ModuleType("range_helper")
    exec(compile(acq_raw,str(source),"exec"),vars(acq))
    sys.path.insert(0,str(args.dependencies))
    from astropy.io import fits
    target=args.root/"cattura"
    src=target/"source"
    src.mkdir(parents=True)

    def capture(i):
        name=f"21816_E{i:03}.fits"
        url=cfg["base"]+name
        header,tag,total=acq.capture_range(url,0,17280)
        start,meta=parse(header,fits,name)
        members=[]
        def save(leaf,payload,offset,band,frame):
            (src/leaf).write_bytes(payload)
            members.append(dict(file=leaf,sha256=sha(payload),bytes=len(payload),offset=offset,band=band,frame=frame))
        save(f"E{i:03}-header.bin",header,0,None,None)
        for band,(y0,y1) in cfg["bands"].items():
            for j in cfg["frames"]:
                at=start+2*4224*(j*4096+y0)
                payload,_,observed=acq.capture_range(url,at,2*4224*(y1-y0),tag)
                require(observed==total,"LIN0 FITS size changed")
                save(f"{band}-E{i:03}-r{j:02}.bin",payload,at,band,j)
        return dict(exposure=i,url=url,etag=tag,objectBytes=total,meta=meta,dataOffset=start,members=members)
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows=list(pool.map(capture,range(1,31)))
    result=dict(protocolSha256=sha(raw),programSha256=sha(Path(__file__).read_bytes()),
                fullFitsHashesVerified=False,records=rows)
    with (target/"acquisizione.json").open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True)
        f.write("\n")


if __name__=="__main__":
    main()