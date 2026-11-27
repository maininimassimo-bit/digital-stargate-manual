"""Replay band-limited Roman GAIN ramp statistics from exact captured bytes."""
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


def evaluate(np, a, b):
    delta = (b-a)/np.sqrt(2.)
    v = delta[:63,:63]
    shifted = (v[:-1,:-1]+v[1:,:-1]+v[:-1,1:]+v[1:,1:])/4
    blocks = shifted.reshape(31,2,31,2).swapaxes(1,2).reshape(-1,4)
    measured = np.var(blocks.sum(axis=1),ddof=1)
    matrix = np.cov(blocks,rowvar=False,ddof=1)
    np.testing.assert_allclose(measured,matrix.sum(),rtol=1e-12,atol=1e-10)
    raw = np.var(v,ddof=1)
    need(raw>0 and measured>0,"Nonpositive variance")
    return dict(signal=float(np.mean((a+b)/2)), inputVariance=float(raw), sumVariance=float(measured),
                sumToEmpiricalDiagonal=float(measured/np.trace(matrix)), fullError=float(abs(2.25*raw/measured-1)),
                diagonalError=float(abs(raw/measured-1)))


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root",type=Path)
    cli.add_argument("dependencies",type=Path)
    cli.add_argument("output",type=Path)
    cli.add_argument("capture_pin")
    args=cli.parse_args()
    root=args.root
    protocol=(root/"protocollo.json").read_bytes()
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
    storage_rails={}
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
                tiles=[data[:,128*c+q0:128*c+q1].copy() for c in cfg["channels"]]
                need(all(t.shape==(64,64) for t in tiles),"Tile shape")
                for c,t in zip(cfg["channels"],tiles,strict=True):
                    storage_rails[i,j,c]=int(np.count_nonzero((t==0)|(t==65535)))
                frames_by_index[j]=np.stack(tiles)
        if i<n:
            series.append({j:frames_by_index[j]-frames_by_index[0] for j in frames[1:]})
    need({p.name for p in (root/"source").iterdir()}==used,"Capture directory differs")
    dates=[r["metadata"]["DATE-BEG"] for r in a["records"]]
    need(len(set(dates))==n and sorted(dates)==dates,"Exposure time ordering")
    rows=[]
    for i in range(0,len(series),2):
        for j in frames[1:]:
            for k,channel in enumerate(cfg["channels"]):
                row=dict(firstExposure=i+1,secondExposure=i+2,frame=j,channel=channel)
                clips=sum(storage_rails[e,f,channel] for e in (i+1,i+2) for f in (0,j))
                if clips:
                    row.update(state="EXCLUDED_STORAGE_RAIL",railSamples=clips)
                else:
                    row.update(state="MEASURED",**evaluate(np,series[i][j][k],series[i+1][j][k]))
                rows.append(row)
    summary = []
    for j in frames[1:]:
        group=[r for r in rows if r["frame"]==j and r["state"]=="MEASURED"]
        excluded=sum(r["frame"]==j and r["state"]=="EXCLUDED_STORAGE_RAIL" for r in rows)
        need(len(group)>0 and len(group)+excluded==30,"Incomplete comparison roster")
        stats={k:float(np.median([r[k] for r in group])) for k in (
            "signal","inputVariance","sumToEmpiricalDiagonal","fullError","diagonalError")}
        summary.append(dict(frame=j, comparisons=len(group),excludedStorageRail=excluded,**stats))
    result=dict(schema="BKL046_ROMAN_GAIN_RAMP_RESULT_V1",captureSha256=args.capture_pin,
                protocolSha256=sha(protocol),programSha256=sha(Path(__file__).read_bytes()),
                rows=rows,summary=summary,heldOutExposure=n,sourceRanges=len(used),
                storageRailPolicy="Exclude complete cell if either exposure clips in either source frame",
                incidentDoseVerified=False,fullFitsHashesVerified=False,nativeExecutions=0,scientificClosures=0)
    with args.output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()