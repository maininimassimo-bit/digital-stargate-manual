import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

work,prior,decoder,deps,vc,out = map(Path,sys.argv[1:])
dlls=[os.add_dll_directory(str(decoder/"rawpy")),os.add_dll_directory(str(vc))]
sys.path[:0]=[str(decoder),str(deps)]
import numpy as np
import rawpy
from scipy.ndimage import gaussian_filter


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(path, pin):
    data=path.read_bytes()
    if sha(data)!=pin:
        raise ValueError(f"Bytes changed: {path.name}")
    return data


def features(samples,black,sigma):
    preview=(np.maximum(samples[0::2,1::2]-black[1],0)+np.maximum(samples[1::2,0::2]-black[2],0))/2
    v=np.log1p(preview)
    return v-gaussian_filter(v,sigma)


def region(data,x,y,r):
    a=data[y-r:y+r,x-r:x+r]
    if a.shape!=(2*r,2*r):
        raise ValueError("Tile clipped")
    return a


def locate(first,other,x,y,cfg):
    s=cfg["searchCells"]
    r=cfg["tileSizeCfaCells"]//2
    base=region(first,x,y,r).astype(float)
    base -= base.mean()
    base_norm=np.sqrt((base*base).sum())
    score=np.empty((2*s+1,2*s+1))
    for dy in range(-s,s+1):
        for dx in range(-s,s+1):
            trial=region(other,x+dx,y+dy,r).astype(float)
            trial -= trial.mean()
            norm=base_norm*np.sqrt((trial*trial).sum())
            score[dy+s,dx+s]=(base*trial).sum()/norm if norm else 0
    y0,x0=np.unravel_index(score.argmax(),score.shape)
    high=float(score[y0,x0])
    if min(y0,x0)==0 or max(y0,x0)==2*s:
        return {"correlation":high,"shiftNativeXY":None,"qualified":False}
    center=score[y0,x0]
    def sub(a,b):
        denom = a+b-2*center
        return 0.5*(a-b)/denom if denom < 0 else 0.0
    shift=[float(2*(x0-s+sub(score[y0,x0-1],score[y0,x0+1]))),
           float(2*(y0-s+sub(score[y0-1,x0],score[y0+1,x0])))]
    ok=bool(np.hypot(*shift)<=cfg["maximumShiftNativePx"] and high>=cfg["minimumCorrelation"])
    return {"correlation":high,"shiftNativeXY":shift,"qualified":ok}


def response(photos,times,white,black,eligible,cfg):
    r=cfg["tileSizeCfaCells"]//2
    cap=cfg["observedCeilingDN"]
    result=[]
    for phase,(y,x) in enumerate(((0,0),(0,1),(1,0),(1,1))):
        selected=[]
        values=[image[y::2,x::2] for image in photos]
        for cx,cy in eligible:
            selected.append(np.stack([region(image,cx,cy,r).ravel() for image in values]))
        if not selected:
            result.append({"phase":phase,"eligibleAnchorCount":0,"exposures":[]})
            continue
        delta_raw=np.hstack(selected)
        # Work in stored DN, with the pinned per-frame decoder black subtraction.
        data=delta_raw-np.array([level[phase] for level in black])[:,None]
        rates=data/np.asarray(times)[:,None]
        mean=(rates[0]+rates[1])/2
        low=np.abs(rates[0]-rates[1])<=cfg["maximumAnchorDisagreementPercent"]*mean/100
        good=(data[:2].min(axis=0)>=cfg["anchorMinSignalDN"]) & low
        for i in (0,1):
            good &= delta_raw[i] < min(cap,white[i][phase])-cfg["anchorMarginDN"]
        levels=[]
        for i in (2,3,4):
            expected=mean*times[i]+black[i][phase]
            relative=(expected-black[i][phase])/(cap-black[i][phase])
            bands=[]
            for a,b in zip(cfg["relativeExpectedBins"][:-1],cfg["relativeExpectedBins"][1:]):
                keep=good & (relative>=a)&(relative<b)
                actual=delta_raw[i][keep]
                n=int(keep.sum())
                pct=100*(rates[i][keep]/mean[keep]-1)
                bands.append({"relativeToCeiling":[a,b],"n":n,
                              "observedPlateau":int((actual==cap).sum()),
                              "observedAtOrAboveDecoderLimit":int((actual>=white[i][phase]).sum()),
                              "medianDeparturePercent":float(np.median(pct)) if n else None,
                              "p90AbsoluteDeparturePercent":float(np.quantile(abs(pct),.9)) if n else None})
            levels.append({"seconds":times[i],"bands":bands})
        result.append({"phase":phase,"eligibleAnchorCount":int(good.sum()),"inputSamples":len(good),"exposures":levels})
    return result


def main():
    conf=(work/"protocollo.json").read_bytes()
    cfg=json.loads(conf)
    old=json.loads(verify(prior/"protocollo.json",cfg["parentProtocol"]))
    report=json.loads(verify(prior/"riscontro.json",cfg["parentReport"]))
    capture=json.loads(verify(prior/"acquisizione.json",cfg["acquisition"]))
    wheel=verify(prior/"rawpy-0.25.1-cp312-cp312-win_amd64.whl",old["wheelSha256"]) if (prior/"rawpy-0.25.1-cp312-cp312-win_amd64.whl").exists() else verify(decoder.parent/"rawpy-0.25.1-cp312-cp312-win_amd64.whl",old["wheelSha256"])
    with ZipFile(BytesIO(wheel)) as bundle:
        for name in bundle.namelist():
            if name.startswith("rawpy/") and not name.endswith("/"):
                if bundle.read(name)!=(decoder/name).read_bytes():
                    raise ValueError("Decoder changed")
    if (rawpy.__version__,rawpy.libraw_version,np.__version__) != ("0.25.1",(0,21,4),"2.3.5"):
        raise ValueError("Decoder runtime changed")
    files={item["file"]:item["sha256"] for item in capture["records"]}
    scenes={}
    for scene,context in report["scenes"].items():
        photos,black,white,times=[],[],[],[]
        for row in context["rows"]:
            data=verify(prior/"originali"/row["file"],files[row["file"]])
            if row["phase"]!="RGGB" or not context["consistentCaptureAndGeometry"]:
                raise ValueError("Unexpected capture geometry")
            with rawpy.imread(BytesIO(data)) as image:
                photos.append(image.raw_image_visible.astype(np.float32))
            black.append([p["black"] for p in row["planes"]])
            white.append([p["white"] for p in row["planes"]])
            times.append(row["exposureSeconds"])
        anchor=features(photos[0],black[0],cfg["filterSigmaCfaCells"])
        features_other=[features(photo,level,cfg["filterSigmaCfaCells"]) for photo,level in zip(photos[1:],black[1:])]
        tiles=[]
        eligible=[]
        for x in cfg["centersX"]:
            for y in cfg["centersY"]:
                shifts=[locate(anchor,moving,x,y,cfg) for moving in features_other]
                if all(row["qualified"] for row in shifts):
                    eligible.append((x,y))
                tiles.append({"centerXYCfaCells":[x,y],"checks":shifts})
        scenes[scene]={"tiles":tiles,"eligible":len(eligible),
                       "phaseResponses":response(photos,times,white,black,eligible,cfg)}
    payload={"schema":cfg["schema"],"protocolSha256":sha(conf),"scenes":scenes,"scientificClosures":0}
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(payload,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
