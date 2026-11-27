"""Verify new Roman SCI ranges and compare three fixed bands."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import ModuleType


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(raw):
    return sha256(raw).hexdigest()


def checked(path,pin):
    raw=path.read_bytes()
    need(digest(raw)==pin, f"SHA-256 changed: {path.name}")
    return raw


def row_key(row):
    return row["firstExposure"],row["frame"],row["channel"]


def summarize(np, band, rows, center, frames):
    need(len(rows)==len({row_key(r) for r in rows})==960,"Band roster changed")
    rec=[]
    for frame in frames[1:]:
        group=[r for r in rows if r["frame"]==frame and r["state"]=="MEASURED"]
        amps=[]
        for channel in range(32):
            selected=[r for r in group if r["channel"]==channel]
            if not selected:
                continue
            need(len(selected)==10,"Incomplete channel")
            med=lambda key:float(np.median([r[key] for r in selected]))
            amps.append(dict(channel=channel,fullErrorMedian=med("fullError"),diagonalErrorMedian=med("diagonalError")))
        paired=[r["fullError"]-center[row_key(r)]["fullError"] for r in group
                if center[row_key(r)]["state"]=="MEASURED"]
        rec.append(dict(frame=frame,band=band,comparisons=len(group),channels=len(amps),
             channelsWithLowerFullError=sum(r["fullErrorMedian"]<r["diagonalErrorMedian"] for r in amps),
             fullErrorMedian=float(np.median([r["fullError"] for r in group])),
             diagonalErrorMedian=float(np.median([r["diagonalError"] for r in group])),
             medianPairedFullErrorChangeVsCenter=float(np.median(paired)),pairedWithCenter=len(paired),byChannel=amps))
    return rec


def calculate(np, kernel, frames, source, manifest, cutoff):
    tiles={}
    rails=np.zeros((32,64,64),dtype=bool)
    for key,m in manifest.items():
        raw=checked(source/m["file"],m["sha256"])
        need(len(raw)==m["bytes"],"Unexpected row-band size")
        values=np.frombuffer(raw, dtype=">i2").reshape(64,4224).astype(np.float64)+32768
        science=values[:,:4096].reshape(64,32,128)[:,:,32:96].swapaxes(0,1)
        rails|=(science==0)|(science==65535)
        tiles[key]=science
    supports=[kernel.plan_support(np, r) for r in rails]
    masks=[dict(channel=c,railPixels=int(rails[c].sum()),retainedBlocks=int(mask.sum()))
           for c,(mask,_) in enumerate(supports)]
    rows=[]
    for first in range(1,21,2):
        second=first+1
        for frame in frames[1:]:
            a=tiles[first,frame]-tiles[first,0]
            b=tiles[second,frame]-tiles[second,0]
            for c,(mask,support) in enumerate(supports):
                row=dict(firstExposure=first,secondExposure=second,frame=frame,channel=c)
                if masks[c]["retainedBlocks"]<cutoff:
                    row.update(state="INSUFFICIENT_UNCLIPPED_SUPPORT")
                else:
                    row.update(state="MEASURED",**kernel.evaluate(np,a[c],b[c],mask,support))
                rows.append(row)
    return rows,masks


def main():
    cli=ArgumentParser(description=__doc__)
    for name in ("root","ramp","channels","dependencies","report"):
        cli.add_argument(name,type=Path)
    cli.add_argument("capture_pin")
    args=cli.parse_args()
    root=args.root
    plan_raw=(root/"protocollo.json").read_bytes()
    plan=json.loads(plan_raw)
    capture=json.loads(checked(root/"cattura"/"acquisizione.json",args.capture_pin))
    need(capture["protocolSha256"]==digest(plan_raw)
         and capture["programSha256"]==digest((root/"acquisisci.py").read_bytes())
         and capture["sourceCaptureSha256"]==plan["rampCaptureSha256"],"Capture lineage changed")
    prior=json.loads(checked(args.ramp/"acquisizione.json",plan["rampCaptureSha256"]))
    records={r["exposure"]:r for r in prior["records"]}
    previous=json.loads(checked(args.channels/"riscontro.json",plan["channelsReportSha256"]))
    kernel=ModuleType("kernel")
    src=args.channels/"misura.py"
    exec(compile(checked(src,plan["channelsProgramSha256"]),str(src),"exec"),vars(kernel))
    sys.path.insert(0,str(args.dependencies))
    import numpy as np
    need(np.__version__=="2.3.5","NumPy version changed")
    frames=plan["frames"]
    bands=plan["bands"]
    sources={name:{} for name in bands}
    used=set()
    for m in capture["captures"]:
        band,e,j=m["band"],m["exposure"],m["frame"]
        record=records[e]
        width,height,*_=record["dimensions"]
        y0,y1=bands[band]
        name=f"{band}-E{e:03}-r{j:02}.bin"
        need(1<=e<=20 and j in frames and m["file"]==name and name not in used
             and m["etag"]==record["etag"] and m["objectBytes"]==record["objectBytes"]
             and m["offset"]==record["dataOffset"]+2*width*(j*height+y0) and m["bytes"]==2*width*(y1-y0),
             "SCI range lineage changed")
        used.add(name)
        sources[band][e,j]=m
    raw=root/"cattura"/"source"
    need(len(used)==160 and {p.name for p in raw.iterdir()}==used,"Captured range set changed")
    center={row_key(r):r for r in previous["rows"]}
    summary=summarize(np,"center",previous["rows"],center,frames)
    rows_by_band={}
    masks_by_band={}
    for band,items in sources.items():
        rows,masks=calculate(np,kernel,frames,raw,items,plan["minRetainedBlocks"])
        summary.extend(summarize(np,band,rows,center,frames))
        rows_by_band[band]=rows
        masks_by_band[band]=masks
    result=dict(schema=plan["schema"],protocolSha256=digest(plan_raw),captureSha256=args.capture_pin,
                programSha256=digest(Path(__file__).read_bytes()),centerReportSha256=plan["channelsReportSha256"],
                newRanges=len(used),summary=summary,masks=masks_by_band,newBandComparisons=rows_by_band,
                incidentDoseVerified=False,fullFitsHashesVerified=False,nativeExecutions=0,scientificClosures=0)
    with args.report.open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()