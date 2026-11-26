"""Fit CALSPEC science frames with the frozen Orion single/double ePSF code."""
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
import hashlib
import io
import json
import math
from pathlib import Path
import sys

root,runtime,parent,engine_root,output=map(Path,sys.argv[1:])
sys.path.insert(0,str(runtime))
import astropy
from astropy.io import fits
import numpy as np


def pinned(path, sha):
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=sha:
        raise ValueError(f"Changed input {path.name}")
    return data


def init_worker(spec):
    global engine,cfg,cube,header
    source=pinned(engine_root/"verifica-fit.py",spec["fitEngineSha256"]).decode("utf-8")
    engine={"__name__":"pinned_fit_engine"}
    boundary=source.index('\nraw=(root/"protocollo.json")')
    exec(compile(source[:boundary].replace("root,runtime,previous,output=map(Path,sys.argv[1:])","").replace("sys.path.insert(0,str(runtime))",""),"pinned_fit_engine.py","exec"),engine)
    cfg=json.loads(pinned(engine_root/"protocollo-fit.json",spec["fitEngineConfigSha256"]))
    data=pinned(engine_root/"fit"/cfg["library"],spec["fitLibrarySha256"])
    with fits.open(io.BytesIO(data),memmap=False) as h:
        header=h[0].header
        cube=h[0].data.astype(float)
    if ((astropy.__version__,np.__version__)!=("7.2.0","2.3.5")
            or cube.shape!=(9,90,101,101) or not np.isfinite(cube).all()
            or cfg["librarySha256"]!=spec["fitLibrarySha256"]):
        raise ValueError("Runtime or library changed")


def match(folds,spec):
    if len(folds)<2 or any(f["status"]!="MEASURED" for f in folds):
        return dict(allPositive=False,shapeConcordant=False,reason="FIT_UNAVAILABLE")
    d=[f["separationNominalMas"] for f in folds]
    r=[f["fit"]["two"]["secondaryToPrimaryFlux"] for f in folds]
    a=[f["detectorAxisDeg"] for f in folds]
    angles=[abs((m-n+90)%180-90) for m,n in combinations(a,2)]
    spans=dict(separationMas=max(d)-min(d),fluxRatioMinOverMax=min(r)/max(r),detectorAxialAngleDeg=max(angles))
    positive=all(f["fit"]["heldoutGain"]>spec["minimumTwoFoldGain"] for f in folds)
    concordance=(spans["separationMas"]<=spec["maximumSeparationSpanMas"]
                 and spans["fluxRatioMinOverMax"]>=spec["minimumFluxRatioConcordance"]
                 and spans["detectorAxialAngleDeg"]<=spec["maximumAxialAngleDifferenceDeg"])
    return dict(allPositive=positive,shapeConcordant=concordance,both=positive and concordance,spans=spans)


def measure(case,spec):
    if not case.get("fitEligible"):
        return dict(root=case["root"],status="PIXEL_CONTROL_INELIGIBLE",folds=[])
    path=parent/"stamps-split"/case["stampFile"]
    with np.load(io.BytesIO(pinned(path,case["stampSha256"])),allow_pickle=False) as z:
        sci,err,dq,lower=(z[k] for k in ("sci","err","dq","lowerXY"))
    if not sci.shape==err.shape==dq.shape==(41,41):
        raise ValueError("Unexpected stamp geometry")
    y,x=np.indices(sci.shape)
    x+=lower[0]-case["peakXY"][0]
    y+=lower[1]-case["peakXY"][1]
    good=(dq==0)&np.isfinite(sci)&np.isfinite(err)&(err>0)
    good &= (x*x+y*y)<=cfg["fitRadiusPx"]**2
    xy=np.column_stack((x[good],y[good]))
    z,e=sci[good].astype(float),err[good].astype(float)
    try:
        psfs=engine["loc_psfs"](cube,header,case["chipPeakXY"],case["chip"])
    except ValueError as ex:
        if str(ex)!="Source outside calibrated PSF grid":
            raise
        return dict(root=case["root"],status="OUTSIDE_LIBRARY_GRID",folds=[])
    folds=[]
    for i in (0,1):
        f=engine["fit_fold"](psfs,xy,z,e,(xy.sum(axis=1)%2)==i,cfg)
        row=dict(status=f["status"],fit=f)
        if f["status"]=="MEASURED":
            x1,y1,x2,y2=f["two"]["parametersPx"]
            row.update(separationNominalMas=f["two"]["separationPx"]*cfg["nominalMasPerPixel"],
                       detectorAxisDeg=math.degrees(math.atan2(y2-y1,x2-x1))%180)
        folds.append(row)
    verdict=match(folds,spec)
    return dict(root=case["root"],chip=case["chip"],status="FIT_EVALUATED",fitPixels=len(xy),
                apertureSNR=case["signalToNoise"],folds=folds,verdict=verdict)


def measure_association(assoc,spec):
    exp=[measure(case,spec) for case in assoc["exposures"]]
    same_chip=len({case.get("chip") for case in exp})==1
    folds=[fold for case in exp for fold in case["folds"]]
    joint=match(folds,spec) if len(folds)==4 and same_chip else dict(allPositive=False,shapeConcordant=False,
                                                                    reason="MISSING_COMPARABLE_SPLIT")
    return dict(association=assoc["association"],target=assoc["target"],exposures=exp,jointVerdict=joint)


def main():
    raw=(root/"protocollo.json").read_bytes()
    spec=json.loads(raw)
    source=json.loads(pinned(parent/"riscontro-split.json",spec["parentReportSha256"]))
    assoc=source["associations"]
    if (len(assoc)!=spec["expectedAssociations"] or sum(len(a["exposures"]) for a in assoc)!=spec["expectedExposures"]
            or any(len(a["exposures"])!=2 for a in assoc)):
        raise ValueError("Association set differs")
    results=[]
    with ProcessPoolExecutor(max_workers=4,initializer=init_worker,initargs=(spec,)) as pool:
        jobs=[pool.submit(measure_association,a,spec) for a in assoc]
        for job in jobs:
            r=job.result()
            results.append(r)
            print(r["association"],r["target"],r["jointVerdict"].get("both",False),flush=True)
    with output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(dict(schema=spec["schema"],protocolSha256=hashlib.sha256(raw).hexdigest(),results=results,
                       opticalNegativeLabelsQualified=0,nativeExecutions=0,scientificClosures=0),out,
                  sort_keys=True,indent=2,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()
