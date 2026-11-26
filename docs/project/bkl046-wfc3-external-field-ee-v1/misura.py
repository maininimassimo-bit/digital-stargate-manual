"""Compare published UVIS aperture terms with isolated stars in two external fields."""
import argparse
from collections import Counter
import csv
from hashlib import file_digest, sha256
from itertools import combinations, product
from io import BytesIO, StringIO
import json
from math import log10
from pathlib import Path
from statistics import median
import sys
import warnings

PIN="3e7df34612344d0c3b851191724b6d258c1c99c319b635c1c5e50af9477175e9"


def need(ok,message):
    if not ok:
        raise ValueError(message)


def pin(raw,expected):
    need(sha256(raw).hexdigest()==expected,"Input fingerprint differs")
    return raw


def peaks(np,frame,threshold,margin):
    sky=float(np.median(frame[np.isfinite(frame)]))
    center=frame[1:-1,1:-1]
    choose=np.isfinite(center)&(center>sky+threshold)
    for y,x in product(range(3),repeat=2):
        if (y,x)!=(1,1):
            choose &= center >= frame[y:y+center.shape[0],x:x+center.shape[1]]
    choose[:margin-1]=False
    choose[-margin+1:]=False
    choose[:,:margin-1]=False
    choose[:,-margin+1:]=False
    return np.argwhere(choose)[:,::-1]+1


def measure(np,frame,errs,dq,pam,seed,p):
    x,y=seed
    margin=p["edgeMargin"]
    h,w=frame.shape
    if not (margin <= x < w-margin and margin <= y < h-margin):
        return None,"NO_GEOMETRIC_OVERLAP"
    ix,iy=np.rint(seed).astype(int)
    half=4
    small=frame[iy-half:iy+half+1,ix-half:ix+half+1]
    if not np.isfinite(small).all():
        return None,"NONFINITE_PEAK_WINDOW"
    dy,dx=np.unravel_index(np.argmax(small),small.shape)
    px,py=ix+dx-half,iy+dy-half
    if np.hypot(px-x,py-y)>p["maxPeakOffsetPx"]:
        return None,"PEAK_OFFSET"
    core=frame[py-3:py+4,px-3:px+4]
    flags=dq[py-3:py+4,px-3:px+4]
    if flags.any() or not np.isfinite(core).all():
        return None,"CORE_DQ"
    weights=np.maximum(core-np.median(core),0)
    if weights.sum()<=0:
        return None,"CENTROID_WITHOUT_SIGNAL"
    coords=np.arange(-3,4)
    cx=float(px+np.sum(weights*coords[None,:])/weights.sum())
    cy=float(py+np.sum(weights*coords[:,None])/weights.sum())

    radius=p["neighborRadius"]+1
    box=np.s_[py-radius:py+radius+1,px-radius:px+radius+1]
    data=frame[box]*pam[box]
    sig=errs[box]*pam[box]
    quality=dq[box]
    size=np.arange(-radius,radius+1)
    yy,xx=np.meshgrid(size+py,size+px,indexing="ij")
    r2=(xx-cx)**2+(yy-cy)**2
    valid=np.isfinite(data)&np.isfinite(sig)&(sig>0)&(quality==0)
    inner,outer=p["skyAnnulus"]
    sky_geom=(r2>=inner**2)&(r2<=outer**2)
    used=valid&sky_geom
    if used.sum()<p["minSkyFraction"]*sky_geom.sum():
        return None,"SKY_SUPPORT"
    sky=float(np.median(data[used]))
    height=float(data[radius,radius]-sky)
    if height<p["minimumCentralElectron"]:
        return None,"WEAK_CENTRAL_SIGNAL"

    values=data[1:-1,1:-1]
    local=(r2[1:-1,1:-1]>5**2)&(r2[1:-1,1:-1] <= p["neighborRadius"]**2)&np.isfinite(values)
    for ry,rx in product(range(3),repeat=2):
        if (ry,rx)!=(1,1):
            local &= values>=data[ry:ry+values.shape[0],rx:rx+values.shape[1]]
    neighbor=max(p["detectSecondaryAboveElectron"],p["neighborPeakFraction"]*height)
    if (values[local]-sky>neighbor).any():
        return None,"NEIGHBOR_IN_ISOLATION_RADIUS"
    # Reject another bright peak in the localization region if the intended peak is ambiguous.
    secondary=((r2>=3**2)&(r2<=5**2)&valid)
    if secondary.any() and float(data[secondary].max()-sky)>height/p["minimumIdentityPeakFactor"]:
        return None,"AMBIGUOUS_INNER_PEAK"
    flux={}
    for r in p["radiusPx"]:
        geometry=r2<=r**2
        if not valid[geometry].all():
            return None,"APERTURE_DQ_OR_ERR"
        flux[str(r)]=float(np.sum(data[geometry]-sky))
    if not all(v>0 for v in flux.values()):
        return None,"NONPOSITIVE_FLUX"
    return dict(peak=[int(px),int(py)],centroid=[cx,cy],electrons=flux,peakAboveSky=height),"ACCEPTED"


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for k in ("root","dependencies","report"):
        cli.add_argument(k,type=Path)
    cli.add_argument("capture_sha256")
    a=cli.parse_args()
    r=a.root
    p=json.loads(pin((r/"protocollo.json").read_bytes(),PIN))
    pin((r/"catalogo.json").read_bytes(),p["catalogSha256"])
    c=json.loads(pin((r/"acquisizione.json").read_bytes(),a.capture_sha256))
    pin((r/"acquisisci.py").read_bytes(),c["programSha256"])
    need(c["protocolSha256"]==PIN and len(c["records"])==6,"Capture binding changed")
    acquisition={x["observation"]:x for x in c["records"]}

    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS,FITSFixedWarning
    warnings.filterwarnings("ignore",category=FITSFixedWarning)
    need((np.__version__,astropy.__version__)==("2.3.5","7.2.0"),"Runtime differs")
    pams={int(chip):fits.getdata(BytesIO(pin((r/f"UVIS{chip}wfc3_map.fits").read_bytes(),fp)))
          for chip,fp in p["pam"].items()}
    table={}
    for chip,fp in p["csv"].items():
        text=pin((r/f"wfc3uvis{chip}_aper_007_syn.csv").read_bytes(),fp).decode()
        table[int(chip)]={x["FILTER"]:[float(x[k]) for k in p["apertureColumns"]]
                          for x in csv.DictReader(StringIO(text)) if x["FILTER"] in p["bands"]}
        need(set(table[int(chip)])==set(p["bands"]),"EE rows changed")

    out=[]
    for field in p["selected"]:
        records={row["filters"]:acquisition[row["obs_id"]] for row in field["rows"]}
        info=dict(target=field["target"],visit=field["visit"],chips=[])
        out.append(info)
        if not all(x["entries"] for x in records.values()):
            info["state"]="MISSING_FLC"
            continue
        loaded={}
        epochs=[]
        frame_meta={}
        for band,row in records.items():
            entry,=row["entries"]
            obs=row["observation"]
            for suffix,field_name in (("-query.json","querySha256"),("-products.json","productsSha256")):
                pin((r/"source"/(obs+suffix)).read_bytes(),row[field_name])
            path=r/"source"/entry["file"]
            with path.open("rb") as f:
                need(file_digest(f,"sha256").hexdigest()==entry["sha256"],"FLC file pin")
            need(path.stat().st_size==entry["bytes"],"FLC length changed")
            with fits.open(path,memmap=False) as h:
                hd=h[0].header
                epochs.append(float(hd["EXPSTART"]))
                need((hd["ROOTNAME"].lower(),hd["TARGNAME"],hd["FILTER"],hd["PROPOSID"],hd["EXPTIME"])==
                     (obs,row["targetAlias"],band,11452,35.0),"FLC header identity")
                frame_meta[band]=dict(state=hd["EXPFLAG"],scan=hd["SCAN_TYP"],cte=hd["PCTECORR"],
                                      flux=hd["FLUXCORR"],aperture=hd["APERTURE"],start=epochs[-1])
                if (hd["EXPFLAG"],hd["SCAN_TYP"],hd["PCTECORR"],hd["FLUXCORR"])!=(
                        "NORMAL","N","COMPLETE","COMPLETE"):
                    continue
                for sci in (x for x in h if x.name=="SCI"):
                    v=sci.header["EXTVER"]
                    chip=sci.header["CCDCHIP"]
                    err,dq=h["ERR",v],h["DQ",v]
                    need(sci.data.shape==err.data.shape==dq.data.shape and sci.header["BUNIT"]=="ELECTRONS",
                         "Science plane structure")
                    ox,oy=(abs(float(sci.header[key])) for key in ("LTV1","LTV2"))
                    need((ox,oy)==(int(ox),int(oy)),"PAM offset")
                    oy,ox=int(oy),int(ox)
                    sy,sx=sci.data.shape
                    pam=pams[chip][oy:oy+sy,ox:ox+sx]
                    need(pam.shape==sci.data.shape,"PAM footprint")
                    loaded[chip,band]=(sci.data.copy(),err.data.copy(),dq.data.copy(),pam,WCS(sci.header,h).celestial)
        info["frames"]=frame_meta
        info["spanDays"]=max(epochs)-min(epochs)
        if info["spanDays"]>p["maxTimeSpanDays"] or not loaded:
            info["state"]="REFUSED_METADATA_OR_TIME"
            continue
        info["state"]="EVALUATED"
        for chip in (1,2):
            if any((chip,band) not in loaded for band in p["bands"]):
                continue
            data=loaded[chip,"F606W"]
            seeds=peaks(np,data[0],p["localMaxSignalElectron"],p["edgeMargin"])
            worlds=data[4].pixel_to_world_values(*seeds.T)
            predicted={band:np.stack(loaded[chip,band][4].world_to_pixel_values(*worlds),axis=1)
                       for band in p["bands"]}
            counters=Counter()
            accepted=[]
            seen={band:set() for band in p["bands"]}
            for i,point in enumerate(seeds):
                measured={}
                failure={}
                for band in p["bands"]:
                    seed=predicted[band][i] if band!="F606W" else point
                    b=loaded[chip,band]
                    value,status=measure(np,*b[:4],seed,p)
                    if value is None:
                        failure[band]=status
                    else:
                        measured[band]=value
                if failure:
                    counters.update(f"{band}:{status}" for band,status in failure.items())
                    continue
                keys={band:tuple(m["peak"]) for band,m in measured.items()}
                if any(key in seen[band] for band,key in keys.items()):
                    counters["DUPLICATE_IMAGE_PEAK"]+=1
                    continue
                for band,key in keys.items():
                    seen[band].add(key)
                growth={band:values["electrons"]["10"]/values["electrons"]["5"] for band,values in measured.items()}
                pairs=list(combinations(p["bands"],2))
                observed={f"{b}-{red}":-2500*log10(growth[b]/growth[red]) for b,red in pairs}
                results={}
                for label,t in (("physicalChip",table[chip]),("fullFrameUVIS2",table[2])):
                    expected={f"{b}-{red}":-2500*log10((t[b][1]/t[b][0])/(t[red][1]/t[red][0])) for b,red in pairs}
                    results[label]={color:value-expected[color] for color,value in observed.items()}
                accepted.append(dict(referencePeak=point.tolist(),peaks=keys,observed=observed,errors=results))
            summary={}
            if accepted:
                for key in ("zero","physicalChip","fullFrameUVIS2"):
                    summary[key]={}
                    for color in accepted[0]["observed"]:
                        values=[(m["observed"] if key=="zero" else m["errors"][key])[color] for m in accepted]
                        summary[key][color]=dict(medianSigned=median(values),medianAbsolute=median(map(abs,values)),
                                                 maxAbsolute=max(map(abs,values)))
            info["chips"].append(dict(chip=chip,candidates=len(seeds),qualifiedSources=len(accepted),sourceRows=accepted,
                                      bandVetoCounts=counters,summary=summary))
    report=dict(schema=p["schema"]+"_RESULT",protocolSha256=PIN,acquisitionSha256=a.capture_sha256,
                programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),fields=out,
                fieldPopulationInferenceVerified=False,scientificClosures=0,nativeExecutions=0)
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(report,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()