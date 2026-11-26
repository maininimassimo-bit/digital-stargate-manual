"""Test a cross-band pointing predictor on archived GD153 comparison apertures."""
import argparse
from collections import Counter
from hashlib import sha256
from io import BytesIO
from itertools import combinations
import json
from math import log10
from pathlib import Path
import sys
import warnings
from zipfile import ZipFile

PIN = "a632c8449f27b3c2310cafa491c2fd7565e10e8425b6926107e4347c442dc8d6"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path, pin):
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == pin, f"Input changed: {path.name}")
    return raw


def archived(path, pin, member, checksum):
    with ZipFile(BytesIO(read(path,pin))) as bundle:
        need(bundle.namelist().count(member) == 1, "Archive member changed")
        raw = bundle.read(member)
    need(sha256(raw).hexdigest() == checksum, "Archived report changed")
    return json.loads(raw)


def helper(path,pin,name):
    scope = {"__name__":"verified_helper"}
    exec(compile(read(path,pin),str(path),"exec"),scope)
    return scope[name]


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("root","poses","dither","clean","donors","measure","dependencies","report"):
        cli.add_argument(name,type=Path)
    args = cli.parse_args()
    p = json.loads(read(args.root/"protocollo.json",PIN))
    source = json.loads(read(args.poses/"protocollo.json",p["poseProtocol"]))
    method = json.loads(read(args.measure/"protocollo.json",p["measurementProtocol"]))
    donor = json.loads(read(args.donors/"protocollo-centro.json",p["donorProtocol"]))
    donor_peak = helper(args.donors/"misura-centro.py",p["donorProgram"],"donor_peak")
    measure = helper(args.measure/"misura.py",p["measurementProgram"],"measure")
    observed = archived(args.dither,p["ditherArchive"],"riscontro.json",p["ditherReport"])
    clean = archived(args.clean,p["cleanArchive"],"riscontro-verificato.json",p["cleanReport"])
    baseline = {r["file"]:r for r in clean["rows"]}
    rows = observed["rows"]

    sys.path.insert(0,str(args.dependencies))
    import astropy
    import numpy as np
    from astropy.io import fits
    from astropy.wcs import FITSFixedWarning, WCS
    warnings.filterwarnings("ignore",category=FITSFixedWarning)
    need((np.__version__,astropy.__version__)==("2.3.5","7.2.0"),"Runtime changed")
    pam_name="UVIS1wfc3_map.fits"
    pam=fits.getdata(BytesIO(read(args.poses/"source"/pam_name,source["inputs"][pam_name])))
    groups={(r["visit"],tuple(r["postarg"])) for r in rows}
    need(len(groups)==16 and len(rows)==len(baseline)==48,"Cohort changed")
    key="local16to22:median:r{}"
    kept={(t["visit"],tuple(t["dither"])) for t in clean["triplets"]
          if all(key.format(radius) in t["measurements"] for radius in method["apertureRadii"])}
    need(len(kept)==4,"Qualified aperture control count changed")
    results=[]
    colors=[]
    modes=("detectorMidpoint","wcsMidpoint")
    for visit,offset in sorted(groups):
        group=[row for row in rows if row["visit"]==visit and tuple(row["postarg"])==offset]
        need(len(group)==3 and {r["band"] for r in group}==set(method["bands"]),"Band roster changed")
        data={}
        for row in group:
            name,band=row["file"],row["band"]
            others=[r for r in rows if r["visit"]==visit and r["band"]==band and tuple(r["postarg"])!=offset]
            need(len(others)==3,"Dither model requires three donor inputs")
            fit=np.linalg.solve(np.array([[1,*r["postarg"]] for r in others]),
                                np.array([r["peak"] for r in others]))
            search=np.array([1,*offset])@fit
            with fits.open(BytesIO(read(args.poses/"source"/name,source["inputs"][name])),memmap=False) as h:
                sci,err,dq=(h[k,1] for k in ("SCI","ERR","DQ"))
                need(sci.header["CCDCHIP"]==1 and h[0].header["FILTER"]==band,"Detector identity changed")
                arrays=(sci.data.astype(float),err.data.astype(float),dq.data.copy())
                data[band]=dict(row=row,wcs=WCS(sci.header,h).celestial,arrays=arrays,
                                header=sci.header.copy(),exptime=float(h[0].header["EXPTIME"]),
                                donor=donor_peak(np,arrays[0],arrays[2],search,donor))
        assessed = {}
        for band, item in data.items():
            row=item["row"]
            pinned=baseline[row["file"]]
            result=dict(file=row["file"],visit=visit,band=band,dither=offset,
                        benchmarkCenter=pinned.get("center"),methods={})
            results.append(result)
            assessed[band]=result
            companions=[d for b,d in data.items() if b!=band and d["donor"] is not None]
            for mode in modes:
                record=dict(state="DONOR_SUPPORT_REFUSED",fluxCalibratedRadii={},
                            exptimeSeconds=item["exptime"])
                result["methods"][mode]=record
                if len(companions)!=2:
                    continue
                xy=[np.array(d["donor"]["xy"]) for d in companions]
                if mode=="wcsMidpoint":
                    xy=[np.array(item["wcs"].world_to_pixel_values(*d["wcs"].pixel_to_world_values(*loc)))
                        for d,loc in zip(companions,xy,strict=True)]
                spread=float(np.linalg.norm(xy[0]-xy[1]))
                record["donorSeparationPx"]=spread
                if not np.isfinite(xy).all() or spread>donor["maximumDonorAgreementPx"]:
                    record["state"]="DONOR_DISAGREEMENT"
                    continue
                seed=(xy[0]+xy[1])/2
                record["seedXY"]=seed.tolist()
                height,width=item["arrays"][0].shape
                if not (28<=seed[0]<width-28 and 28<=seed[1]<height-28):
                    record["state"]="PREDICTED_BOUNDARY"
                    continue
                if "center" in pinned:
                    record["seedToBenchmarkPx"]=float(np.linalg.norm(seed-pinned["center"]))
                record["state"]=measure(np,*item["arrays"],pam,seed,item["header"],method,record)
                if "centerXY" in record and "center" in pinned:
                    record["recenteredToBenchmarkPx"]=float(np.linalg.norm(np.array(record["centerXY"])-pinned["center"]))
            if (visit,offset) in kept:
                control=dict(fluxCalibratedRadii={},exptimeSeconds=item["exptime"])
                control["state"]=measure(np,*item["arrays"],pam,np.array(pinned["center"]),item["header"],method,control)
                result["matchedEstimatorReference"]=control

        if (visit,offset) not in kept:
            continue
        color_case=dict(visit=visit,dither=offset,base={},alternatives={})
        colors.append(color_case)
        for mode in (*modes,"matched"):
            control=(lambda x:x["matchedEstimatorReference"]) if mode=="matched" else (lambda x:x["methods"][mode])
            per_radius={}
            for radius in map(str,method["apertureRadii"]):
                flux={b:r["fluxCalibratedRadii"][radius]
                      for b,x in assessed.items() if radius in (r:=control(x))["fluxCalibratedRadii"]}
                if len(flux)==3:
                    per_radius[radius]={f"{b}-{r}":-2500*log10(flux[b]/flux[r]) for b,r in combinations(method["bands"],2)}
            if mode=="matched":
                color_case["base"]=per_radius
            else:
                color_case["alternatives"][mode]=per_radius
        for mode,results_for_mode in color_case["alternatives"].items():
            shared=set(results_for_mode)&set(color_case["base"])
            color_case.setdefault("differences",{})[mode]={
                rr:{c:results_for_mode[rr][c]-color_case["base"][rr][c] for c in results_for_mode[rr]}
                for rr in sorted(shared)}
    out=dict(schema=p["schema"]+"_RESULT",protocolSha256=PIN,
             programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),rows=results,colorControls=colors,
             states={mode:Counter(r["methods"][mode]["state"] for r in results) for mode in modes},
             fieldTieVerified=False,scientificClosures=0,nativeExecutions=0)
    with args.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(out,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()