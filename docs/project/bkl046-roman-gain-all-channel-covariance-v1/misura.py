"""Compare Roman GAIN variance propagation across all 32 science channels."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


def sha(data):
    return sha256(data).hexdigest()


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def plan_support(np, rail):
    interior = rail[:63, :63]
    bad = np.lib.stride_tricks.sliding_window_view(interior, (3,3))[::2,::2].any(axis=(2,3))
    retained = ~bad
    y,x = np.nonzero(retained)
    eligible = np.zeros_like(interior)
    for dy in range(3):
        for dx in range(3):
            eligible[2*y+dy,2*x+dx] = True
    return retained, eligible


def evaluate(np, a, b, retained, eligible):
    delta = (b-a)/np.sqrt(2.)
    v = delta[:63,:63]
    shifted = (v[:-1,:-1]+v[1:,:-1]+v[:-1,1:]+v[1:,1:])/4
    blocks = shifted.reshape(31,2,31,2).swapaxes(1,2).reshape(31,31,4)[retained]
    measured = np.var(blocks.sum(axis=1),ddof=1)
    matrix = np.cov(blocks,rowvar=False,ddof=1)
    np.testing.assert_allclose(measured,matrix.sum(),rtol=1e-12,atol=1e-10)
    raw = np.var(v[eligible],ddof=1)
    need(raw>0 and measured>0,"Nonpositive variance")
    return dict(signal=float(np.mean((a+b)[:63,:63][eligible]/2)), inputVariance=float(raw),
                sumVariance=float(measured), sumToEmpiricalDiagonal=float(measured/np.trace(matrix)),
                fullError=float(abs(2.25*raw/measured-1)), diagonalError=float(abs(raw/measured-1)))

def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root",type=Path)
    cli.add_argument("dependencies",type=Path)
    cli.add_argument("output",type=Path)
    cli.add_argument("plan",type=Path)
    args=cli.parse_args()
    root=args.root
    plan_raw=args.plan.read_bytes()
    plan=json.loads(plan_raw)
    args.capture_pin=plan["captureSha256"]
    channels=list(range(plan["scienceChannels"]))
    protocol=(root/"protocollo.json").read_bytes()
    need(sha(protocol)==plan["parentProtocolSha256"],"Parent protocol changed")
    cfg=json.loads(protocol)
    raw=(root/"acquisizione.json").read_bytes()
    need(sha(raw)==args.capture_pin,"Capture file changed")
    a=json.loads(raw)
    need(a["protocolSha256"]==sha(protocol) and sha((root/"acquisisci.py").read_bytes())==a["acquisitionProgramSha256"],
         "Capture lineage changed")
    sys.path.insert(0,str(args.dependencies))
    import numpy as np
    from astropy.io import fits
    from types import ModuleType
    reader=ModuleType("acquisition")
    exec(compile((root/"acquisisci.py").read_bytes(),"acquisisci.py","exec"),vars(reader))
    n=cfg["exposures"]
    frames=cfg["frames"]
    y0,y1=cfg["bandRows"]
    q0,q1=cfg["channelOffset"]
    need([r["exposure"] for r in a["records"]]==list(range(1,n+1)) and len({r["etag"] for r in a["records"]})==n,
         "Cohort or source identities changed")
    series=[]
    used=set()
    rails=np.zeros((len(channels),64,64),dtype=bool)
    for r in a["records"]:
        i=r["exposure"]
        stem=f"21816_E{i:03}"
        need(r["url"]==cfg["base"]+stem+".fits","Source URL")
        expected=[None,*frames] if i<n else [None]
        need([m["frame"] for m in r["members"]]==expected,"Captured frame roster")
        frames_by_index={}
        for m in r["members"]:
            j=m["frame"]
            name=stem+"-header.bin" if j is None else f"{stem}-r{j:02}.bin"
            need(m["file"]==name and name not in used,"Member identity")
            used.add(name)
            b=(root/"source"/name).read_bytes()
            need(sha(b)==m["sha256"] and len(b)==m["bytes"],"Captured bytes changed")
            if j is None:
                start,dims,meta=reader.parse_header(b,fits,stem+".fits")
                need(meta==r["metadata"] and dims==r["dimensions"] and start==r["dataOffset"] and m["offset"]==0,
                     "Header linkage")
                width,height,*_=dims
            else:
                need(m["offset"]==start+2*width*(j*height+y0) and len(b)==2*width*(y1-y0),"SCI span linkage")
                data=np.frombuffer(b,dtype=">i2").reshape(y1-y0,width).astype(np.float64)+32768
                tiles=[data[:,128*c+q0:128*c+q1].copy() for c in channels]
                need(all(t.shape==(64,64) for t in tiles),"Tile shape")
                array=np.stack(tiles)
                rails |= (array==0)|(array==65535)
                frames_by_index[j]=array
        if i<n:
            series.append({j:frames_by_index[j]-frames_by_index[0] for j in frames[1:]})
    need({p.name for p in (root/"source").iterdir()}==used,"Capture directory differs")
    dates=[r["metadata"]["DATE-BEG"] for r in a["records"]]
    need(len(set(dates))==n and sorted(dates)==dates,"Exposure time ordering")
    need(len(series)==20 and len(frames)==4 and channels==list(range(32)),"Unexpected sample")
    supports = [plan_support(np,rail) for rail in rails]
    support_report = [dict(channel=c,railPixels=int(rails[c].sum()),retainedBlocks=int(blocks.sum()),
                           retainedInputPixels=int(support.sum()))
                      for c,(blocks,support) in enumerate(supports)]
    rows=[]
    for i in range(0,len(series),2):
        for j in frames[1:]:
            for channel,(blocks,support) in enumerate(supports):
                row=dict(firstExposure=i+1,secondExposure=i+2,frame=j,channel=channel)
                if support_report[channel]["retainedBlocks"] < plan["minRetainedBlocks"]:
                    row.update(state="INSUFFICIENT_UNCLIPPED_SUPPORT")
                else:
                    row.update(state="MEASURED",**evaluate(np,series[i][j][channel],series[i+1][j][channel],
                                                          blocks,support))
                rows.append(row)
    need(len(rows)==960,"Incomplete comparison roster")
    prior_pin=plan["parentReportSha256"]
    previous=(root/"riscontro.json").read_bytes()
    need(sha(previous)==prior_pin,"Parent report changed")
    verified=0
    lookup = {(r["firstExposure"],r["frame"],r["channel"]):r for r in rows}
    metrics=("inputVariance","sumVariance","sumToEmpiricalDiagonal","fullError","diagonalError")
    for ref in json.loads(previous)["rows"]:
        pair,frame,channel=(ref[k] for k in ("firstExposure","frame","channel"))
        if ref["state"]=="MEASURED":
            need(support_report[channel]["retainedBlocks"]==961,"Parent support changed")
            row=lookup[pair,frame,channel]
            np.testing.assert_allclose([row[k] for k in metrics],[ref[k] for k in metrics],rtol=1e-12,atol=1e-10)
            verified+=1
    need(verified==60,"Parent measurement coverage")
    summary=[]
    for j in frames[1:]:
        group=[r for r in rows if r["frame"]==j and r["state"]=="MEASURED"]
        channel_summary=[]
        for c in channels:
            selected=[r for r in group if r["channel"]==c]
            if selected:
                need(len(selected)==10,"Channel exposure coverage")
                channel_summary.append(dict(channel=c,fullErrorMedian=float(np.median([r["fullError"] for r in selected])),
                    diagonalErrorMedian=float(np.median([r["diagonalError"] for r in selected])),
                    empiricalSumToDiagonalMedian=float(np.median([r["sumToEmpiricalDiagonal"] for r in selected]))))
        summary.append(dict(frame=j,comparisons=len(group),channels=channel_summary,
                            channelsWithLowerFullError=sum(r["fullErrorMedian"]<r["diagonalErrorMedian"] for r in channel_summary),
                            aggregateFullErrorMedian=float(np.median([r["fullError"] for r in group])),
                            aggregateDiagonalErrorMedian=float(np.median([r["diagonalError"] for r in group]))))
    result=dict(schema=plan["schema"],protocolSha256=sha(plan_raw),programSha256=sha(Path(__file__).read_bytes()),
                captureSha256=args.capture_pin,parentReportSha256=prior_pin,verifiedParentVarianceComparisons=verified,
                supports=support_report,rows=rows,summary=summary,incidentDoseVerified=False,fullFitsHashesVerified=False,
                nativeExecutions=0,scientificClosures=0)
    with args.output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()