"""Capture and replay the Roman GAIN lab-housekeeping tails."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from statistics import mean, stdev, median
import struct
import sys
from types import ModuleType


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path, pin):
    raw=path.read_bytes()
    need(sha(raw)==pin,"Changed input: "+path.name)
    return raw


def tail(record):
    width,height,frames,integrations=record["dimensions"]
    science=2*width*height*frames*integrations
    return record["dataOffset"]+((science+2879)//2880)*2880


def capture(args, root, plan, raw_plan, parent):
    source=args.ramp/"acquisisci.py"
    module=ModuleType("capture")
    exec(compile(read(source,plan["parentAcquisitionSha256"]),str(source),"exec"),vars(module))
    root.mkdir()
    source_dir=root/"source"
    source_dir.mkdir()

    def get(record):
        offset=tail(record)
        length=record["objectBytes"]-offset
        need(0<length<=65536,"Unexpected tail size")
        data,tag,total=module.capture_range(record["url"],offset,length,record["etag"])
        need(total==record["objectBytes"],"Changed FITS length")
        name=f'E{record["exposure"]:03}-labhk.bin'
        (source_dir/name).write_bytes(data)
        return dict(exposure=record["exposure"],file=name,offset=offset,bytes=len(data),
                    sha256=sha(data),etag=tag)
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows=list(pool.map(get,parent))
    save(root/"acquisizione.json",dict(protocolSha256=sha(raw_plan),
                  sourceCaptureSha256=plan["parentCaptureSha256"],rows=rows,fullFitsHashesVerified=False))


def save(path,data):
    with path.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(data,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


def parse(fits, raw, plan):
    end=next((i for i in range(0,len(raw),80) if raw[i:i+8]==b"END     "),None)
    need(end is not None,"Missing FITS table END")
    offset=((end+80+2879)//2880)*2880
    hdr=fits.Header.fromstring(raw[:offset].decode("ascii"),sep="")
    need((hdr["XTENSION"],hdr["EXTNAME"],hdr["EXTVER"],hdr["NAXIS1"],hdr["PCOUNT"],hdr["TFIELDS"])
         ==("BINTABLE","LABHK",1,56,0,7),"Laboratory HDU format changed")
    n=hdr["NAXIS2"]
    need(n>0 and len(raw)==offset+((n*56+2879)//2880)*2880,"Laboratory table extent changed")
    need([hdr[f"TTYPE{i}"] for i in range(1,8)]==plan["fields"]
         and [hdr[f"TUNIT{i}"] for i in range(1,8)]==plan["units"]
         and all(hdr[f"TFORM{i}"]=="D" for i in range(1,8)),"Laboratory schema changed")
    return n,list(struct.iter_unpack(">7d",raw[offset:offset+n*56]))


def cv(values):
    return stdev(values)/abs(mean(values))


def replay(args,root,plan,raw_plan,parent):
    sys.path.insert(0,str(args.dependencies))
    from astropy.io import fits
    import numpy as np
    need(np.__version__=="2.3.5","Unexpected NumPy version")
    cap=json.loads(read(root/"acquisizione.json",args.capture_pin))
    need(cap["sourceCaptureSha256"]==plan["parentCaptureSha256"] and cap["protocolSha256"]==sha(raw_plan),
         "Capture lineage changed")
    need([r["exposure"] for r in cap["rows"]]==list(range(1,22)),"Capture roster changed")
    source=root/"source"
    need({p.name for p in source.iterdir()}=={r["file"] for r in cap["rows"]},"Unexpected tail files")
    rows=[]
    for record,item in zip(parent,cap["rows"],strict=True):
        e=record["exposure"]
        need(item["file"]==f"E{e:03}-labhk.bin" and item["offset"]==tail(record)
             and item["etag"]==record["etag"] and item["bytes"]+item["offset"]==record["objectBytes"],
             "Tail linkage changed")
        raw=read(source/item["file"],item["sha256"])
        need(len(raw)==item["bytes"],"Tail length")
        n,values=parse(fits,raw,plan)
        data=np.asarray(values)
        need(np.all(np.isfinite(data)) and np.all(np.diff(data[:,0])>0),"Invalid laboratory samples")
        meta=record["metadata"]
        date=datetime.fromisoformat(meta["DATE-BEG"]).replace(tzinfo=timezone.utc)
        start=date.timestamp()/86400+40587
        times=(data[:,0]-start)*86400
        windows=[]
        for offset in plan["nominalStartOffsetsGroups"]:
            for frame in plan["frames"]:
                lo=offset*meta["TGROUP"]
                hi=(offset+frame)*meta["TGROUP"]
                window=dict(offsetGroups=offset,frame=frame,duration=hi-lo)
                if times[0]>lo or times[-1]<hi:
                    window.update(state="NOT_BRACKETED")
                else:
                    t=np.r_[lo,times[(times>lo)&(times<hi)],hi]
                    v=np.interp(t,times,data[:,5])
                    window.update(state="BRACKETED",mctVoltSeconds=float(np.trapezoid(v,t)))
                windows.append(window)
        rows.append(dict(exposure=e,count=n,samples=values,relativeSeconds=times.tolist(),windows=windows))
    center=json.loads(read(args.center/"riscontro.json",plan["centerReportSha256"]))
    signals={}
    for row in center["rows"]:
        if row["state"]=="MEASURED":
            signals.setdefault((row["firstExposure"],row["frame"]),[]).append(row["signal"])
    summaries=[]
    for offset in plan["nominalStartOffsetsGroups"]:
        for j in plan["frames"]:
            paired=[]
            for i in range(1,21,2):
                a,b=[next(w for w in rows[k-1]["windows"] if (w["offsetGroups"],w["frame"])==(offset,j))
                     for k in (i,i+1)]
                if a["state"]!=b["state"] or a["state"]!="BRACKETED":
                    paired.append(dict(firstExposure=i,state="NOT_BRACKETED"))
                    continue
                need(len(signals[i,j])==32,"Science pair coverage changed")
                signal=median(signals[i,j])
                integral=(a["mctVoltSeconds"]+b["mctVoltSeconds"])/2
                need(integral>0,"Nonpositive MCT integral")
                paired.append(dict(firstExposure=i,state="MEASURED",voltsSeconds=integral,
                                   meanNominalSeconds=(a["duration"]+b["duration"])/2,
                                   signalPerSecond=2*signal/(a["duration"]+b["duration"]),
                                   signalPerVoltSecond=signal/integral))
            valid=[r for r in paired if r["state"]=="MEASURED"]
            item=dict(frame=j,offsetGroups=offset,validPairs=len(valid),pairs=paired)
            if len(valid)>=2:
                item.update(signalPerSecondCv=cv([r["signalPerSecond"] for r in valid]),
                            signalPerVoltSecondCv=cv([r["signalPerVoltSecond"] for r in valid]))
            summaries.append(item)
    samples=[v for r in rows for v in r["samples"]]
    unique=set(v[0] for v in samples)
    summary=dict(extension="LABHK",exposures=len(rows),samples=len(samples),distinctTimestamps=len(unique),
        mctVoltsMin=min(v[5] for v in samples),mctVoltsMax=max(v[5] for v in samples),
        siNegativeSamples=sum(v[6]<0 for v in samples),siNonnegativeSamples=sum(v[6]>=0 for v in samples),
        nominalTiming=summaries)
    save(args.report,dict(schema=plan["schema"],captureSha256=args.capture_pin,programSha256=sha(Path(__file__).read_bytes()),
         protocolSha256=sha(raw_plan),centerReportSha256=plan["centerReportSha256"],summary=summary,rows=rows,
         calibratedDoseVerified=False,nativeExecutions=0,scientificClosures=0))


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root",type=Path)
    cli.add_argument("ramp",type=Path)
    sub=cli.add_subparsers(dest="mode",required=True)
    sub.add_parser("capture")
    r=sub.add_parser("replay")
    for name in ("center","dependencies","report"):
        r.add_argument(name,type=Path)
    r.add_argument("capture_pin")
    args=cli.parse_args()
    policy=(args.root/"protocollo.json").read_bytes()
    plan=json.loads(policy)
    parent=json.loads(read(args.ramp/"acquisizione.json",plan["parentCaptureSha256"]))["records"]
    data_root=args.root/"cattura"
    if args.mode=="capture":
        capture(args,data_root,plan,policy,parent)
    else:
        replay(args,data_root,plan,policy,parent)


if __name__=="__main__":
    main()