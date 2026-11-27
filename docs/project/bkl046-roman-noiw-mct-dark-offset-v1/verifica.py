"""Read Roman NOIW dark-test telemetry and study conditional GAIN offset sensitivity."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from hashlib import sha256
import json
from math import isfinite, prod
from pathlib import Path
from statistics import mean, median, stdev
import struct
import sys
from types import ModuleType


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return sha256(raw).hexdigest()


def checked(path,pin):
    data=path.read_bytes()
    need(sha(data)==pin,"Changed file: "+path.name)
    return data


def save(path,obj):
    with path.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(obj,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


def padded(n):
    return ((n+2879)//2880)*2880


def header(fits,data):
    end=next((i for i in range(0,len(data),80) if data[i:i+8]==b"END     "),None)
    need(end is not None,"FITS header end absent")
    length=padded(end+80)
    return fits.Header.fromstring(data[:length].decode("ascii"),sep=""),length


def size(h):
    n=h["NAXIS"]
    if n==0:
        return 0
    return padded((abs(h["BITPIX"])//8)*(prod(h[f"NAXIS{i}"] for i in range(1,n+1))+h.get("PCOUNT",0))*h.get("GCOUNT",1))


def layout(headers,name):
    primary,sci,guide,lab=headers
    expected={"FILENAME":name,"TESTTYPE":"NOISE","DETECTOR":"21816","READMODE":"Diff",
              "OUTBUF":"PMOS","NGROUPS":56,"NOUTPUTS":32,"SCATEMP":95,"GUIDEWIN":True,"REFOUT":True}
    need(all(primary[k]==v for k,v in expected.items()) and primary["NAXIS"]==0
        and primary["NEXTEND"]==3,"NOIW primary changed")
    need([h["EXTNAME"] for h in (sci,guide,lab)]==["SCI","GUIDE","LABHK"],"NOIW HDU order")
    need([sci[f"NAXIS{i}"] for i in range(1,5)]==[4224,4096,56,1]
        and sci["BITPIX"]==16,"SCI shape or encoding changed")


def capture(args,plan,plan_raw,fits):
    module=ModuleType("http_reader")
    path=args.ramp/"acquisisci.py"
    exec(compile(checked(path,plan["parentAcquisitionProgramSha256"]),str(path),"exec"),vars(module))
    data_dir=args.root/"cattura"
    data_dir.mkdir()
    src=data_dir/"source"
    src.mkdir()

    def get(i):
        name=f"21816_E{i:03}.fits"
        url=plan["base"]+name
        tag=None
        at=0
        members=[]
        headers=[]

        def persist(phase,raw,offset):
            leaf=f"E{i:03}-{phase}.bin"
            (src/leaf).write_bytes(raw)
            members.append(dict(file=leaf,at=offset,bytes=len(raw),sha256=sha(raw)))

        for phase,length in (("primary",5760),("sci",2880),("guide",2880),("labhk",2880)):
            raw,tag,total=module.capture_range(url,at,length,tag)
            hdr,consumed=header(fits,raw)
            need(consumed==length,"Header layout changed")
            headers.append(hdr)
            persist(phase,raw,at)
            at+=length
            if phase!="labhk":
                at+=size(hdr)
        layout(headers,name)
        need(at+size(hdr)==total and size(hdr)<=65536,"Laboratory tail extent")
        raw,_,end=module.capture_range(url,at,size(hdr),tag)
        need(end==total,"FITS length changed")
        persist("table",raw,at)
        return dict(exposure=i,url=url,etag=tag,objectBytes=total,members=members)
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows=list(pool.map(get,range(1,plan["exposureCount"]+1)))
    save(data_dir/"acquisizione.json",dict(protocolSha256=sha(plan_raw),programSha256=sha(Path(__file__).read_bytes()),
                                          fullFitsHashesVerified=False,rows=rows))


def replay(args,plan,plan_raw,fits):
    root=args.root/"cattura"
    cap=json.loads(checked(root/"acquisizione.json",args.capture_pin))
    need(cap["protocolSha256"]==sha(plan_raw),"Protocol link changed")
    used=set()
    bytime={}
    exposures=[]
    need([r["exposure"] for r in cap["rows"]]==list(range(1,40)),"NOIW roster")
    for record in cap["rows"]:
        i=record["exposure"]
        identity=f"21816_E{i:03}.fits"
        need(record["url"]==plan["base"]+identity,"Source identity")
        headers=[]
        at=0
        entries=record["members"]
        need(len(entries)==5,"Expected 4 headers and table")
        for phase,entry in zip(("primary","sci","guide","labhk","table"),entries,strict=True):
            name=f"E{i:03}-{phase}.bin"
            need(entry["file"]==name and name not in used and entry["at"]==at,"Range roster or offset")
            used.add(name)
            raw=checked(root/"source"/name,entry["sha256"])
            need(len(raw)==entry["bytes"],"Range size")
            if phase=="table":
                need(len(raw)==size(hdr) and at+len(raw)==record["objectBytes"],"Table extent")
                continue
            hdr,length=header(fits,raw)
            need(length==len(raw),"Header extent")
            headers.append(hdr)
            at+=length
            if phase!="labhk":
                at+=size(hdr)
        layout(headers,identity)
        need((hdr["XTENSION"],hdr["NAXIS1"],hdr["TFIELDS"],hdr["PCOUNT"])==("BINTABLE",56,7,0)
             and [hdr[f"TTYPE{k}"] for k in range(1,8)]==plan["labProtocolFields"]
             and [hdr[f"TUNIT{k}"] for k in range(1,8)]==plan["units"]
             and all(hdr[f"TFORM{k}"]=="D" for k in range(1,8)),"Table schema")
        samples=list(struct.iter_unpack(">7d",raw[:56*hdr["NAXIS2"]]))
        need(samples and all(all(map(isfinite,s)) for s in samples),"Missing or nonfinite samples")
        for s in samples:
            need(s==bytime.setdefault(s[0],s),"Inconsistent sample at duplicate timestamp")
        exposures.append(dict(exposure=i,dateBeg=headers[0]["DATE-BEG"],count=len(samples),
                              timingCode=headers[0]["LODFILE"],samples=samples))
    need({p.name for p in (root/"source").iterdir()}==used,"Unexpected captured files")

    gain=json.loads(checked(args.gain/"riscontro.json",plan["gainReportSha256"]))
    mct=[s[5] for s in bytime.values()]
    dark_bounds=[min(mct),median(mct),max(mct)]
    sensitivity=[]
    for item in gain["summary"]["nominalTiming"]:
        accepted=[row for row in item["pairs"] if row["state"]=="MEASURED"]
        scenarios=[]
        for offset in [0,*dark_bounds]:
            series=[]
            for r in accepted:
                seconds=r["meanNominalSeconds"]
                signal=r["signalPerSecond"]*seconds
                denom=r["voltsSeconds"]-offset*seconds
                need(denom>0,"Nonpositive conditional MCT integral")
                series.append(signal/denom)
            scenarios.append(dict(offsetVolts=offset,signalToCorrectedIntegralCv=stdev(series)/abs(mean(series))))
        need(abs(scenarios[0]["signalToCorrectedIntegralCv"]-item["signalPerVoltSecondCv"])<1e-14,
             "Uncorrected GAIN reference differs")
        sensitivity.append(dict(frame=item["frame"],offsetGroups=item["offsetGroups"],pairs=len(accepted),scenarios=scenarios))
    date0=exposures[0]["dateBeg"]
    save(args.report,dict(schema=plan["schema"],protocolSha256=sha(plan_raw),programSha256=sha(Path(__file__).read_bytes()),
        captureSha256=args.capture_pin,gainReportSha256=plan["gainReportSha256"],exposures=exposures,
        summary=dict(noiwExposures=len(exposures),samples=sum(r["count"] for r in exposures),distinctTimestamps=len(bytime),
                     darkMctVoltsMinMedianMax=dark_bounds,gainMctVoltsMinMax=[gain["summary"]["mctVoltsMin"],gain["summary"]["mctVoltsMax"]],
                     daysFromFirstGainExposure=(datetime.fromisoformat(date0)-datetime.fromisoformat("2021-09-02T03:10:06")).total_seconds()/86400,
                     conditionalOffsetSensitivity=sensitivity),
        transferredOffsetVerified=False,calibratedDoseVerified=False,nativeExecutions=0,scientificClosures=0))


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root",type=Path)
    cli.add_argument("dependencies",type=Path)
    sub=cli.add_subparsers(dest="mode",required=True)
    cap=sub.add_parser("capture")
    cap.add_argument("ramp",type=Path)
    rep=sub.add_parser("replay")
    rep.add_argument("gain",type=Path)
    rep.add_argument("report",type=Path)
    rep.add_argument("capture_pin")
    args=cli.parse_args()
    raw=(args.root/"protocollo.json").read_bytes()
    plan=json.loads(raw)
    sys.path.insert(0,str(args.dependencies))
    from astropy.io import fits
    if args.mode=="capture":
        capture(args,plan,raw,fits)
    else:
        replay(args,plan,raw,fits)


if __name__=="__main__":
    main()