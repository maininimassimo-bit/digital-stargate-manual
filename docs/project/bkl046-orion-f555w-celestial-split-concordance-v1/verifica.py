"""Transfer the CALSPEC concordance rule to sky-projected Orion positive controls."""
import ast
from collections import defaultdict
import hashlib
import io
from itertools import combinations
import json
from pathlib import Path
import sys
import warnings

root,runtime,source,calspec,literature,output=map(Path,sys.argv[1:])
sys.path.insert(0,str(runtime))
import astropy
from astropy.io import fits
from astropy.wcs import FITSFixedWarning,WCS
import numpy as np


def pinned(path, sha):
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=sha:
        raise ValueError(f"Changed {path.name}")
    return data


def axis_delta(a,b):
    return abs((a-b+90)%180-90)


def concordance(folds,criteria,real_sky):
    if len(folds)<2:
        return dict(status="INSUFFICIENT_FOLDS",passes=False)
    d=[f["celestialSeparationMas" if real_sky else "nominalSeparationMas"] for f in folds]
    q=[f["relativeSecondaryFlux"] for f in folds]
    a=[f["axialSkyPAdeg" if real_sky else "axialDetectorDeg"] for f in folds]
    span=dict(separationMas=max(d)-min(d),fluxRatioMinOverMax=min(q)/max(q),
              axialAngleDeg=max(axis_delta(u,v) for u,v in combinations(a,2)))
    checks=dict(positiveAllGains=all(f["heldoutGain"]>criteria["minimumTwoFoldGain"] for f in folds),
                separation=span["separationMas"]<=criteria["maximumSeparationSpanMas"],
                fluxRatio=span["fluxRatioMinOverMax"]>=criteria["minimumFluxRatioConcordance"],
                orientation=span["axialAngleDeg"]<=criteria["maximumAxialAngleDifferenceDeg"])
    return dict(status="EVALUATED",passes=all(checks.values()),span=span,checks=checks)


def reconstruct(reader, meta, obs, fit_row, catalog, policy, stride, manifest):
    if obs["status"]!="RECORDED" or fit_row["status"]!="MEASURED":
        return dict(root=obs["root"],status="UNAVAILABLE",cause=fit_row.get("cause",obs["status"]),folds=[]),{}
    store=reader(source/"ranges",meta,stride,manifest,False)
    with fits.open(store,memmap=False,lazy_load_hdus=False) as h, warnings.catch_warnings():
        warnings.simplefilter("ignore",FITSFixedWarning)
        if h[0].header["ROOTNAME"].lower()!=obs["root"]:
            raise ValueError("Projection image identity changed")
        sci=h["SCI",obs["scienceExtVer"]]
        if sci.header["CCDCHIP"]!=obs["chip"]:
            raise ValueError("Projection chip changed")
        wcs=WCS(sci.header,h).celestial
        folds=[]
        for f in fit_row["folds"]:
            if f["status"]!="MEASURED":
                continue
            two=f["two"]
            x,y=obs["peakXY"]
            ax,ay,bx,by=two["parametersPx"]
            a=wcs.pixel_to_world(x+ax,y+ay).icrs
            b=wcs.pixel_to_world(x+bx,y+by).icrs
            sep=float(a.separation(b).mas)
            north_east=float(a.position_angle(b).deg%180)
            detector=float(np.degrees(np.arctan2(by-ay,bx-ax))%180)
            ratio=two["secondaryToPrimaryFlux"]
            pa_error=axis_delta(north_east,catalog["paDegrees"])
            folds.append(dict(nominalSeparationMas=two["separationNominalMas"],celestialSeparationMas=sep,
                              axialSkyPAdeg=north_east,axialDetectorDeg=detector,
                              relativeSecondaryFlux=ratio,heldoutGain=f["heldoutGain"],
                              axialDistanceToCatalogDeg=pa_error,
                              catalogPAWithinTolerance=pa_error<=policy["catalogComparisonPositionAngleToleranceDeg"]))
    if len(folds)!=2:
        raise ValueError("Fitted exposure lost a held-out fold")
    return dict(root=obs["root"],status="PROJECTED",detectorChip=obs["chip"],folds=folds,
                oldCatalogSeparationAndFluxBoth=fit_row["passBothFolds"]),store.used


def main():
    raw=(root/"protocollo.json").read_bytes()
    policy=json.loads(raw)
    files={name:pinned(source/name,sha) for name,sha in policy["sourcePins"].items()}
    criteria=json.loads(pinned(calspec/"protocollo.json",policy["calSpecCriterionSha256"]))
    reference=json.loads(pinned(literature/"riscontro.json",policy["literatureRosterSha256"]))
    catalog={r["catalogRow"]:r for r in reference["acsF555W"]}
    recorded=json.loads(files["riscontro.json"])["observations"]
    fits_report=json.loads(files["riscontro-fit.json"])["results"]
    pins=json.loads(files["range-sha256.json"])
    meta={item["root"]:item for item in json.loads(files["fits-objects.json"])}
    if (len(recorded)!=len(fits_report) or len(recorded)!=policy["expectedRecordCount"]
            or sorted({o["catalogRow"] for o in recorded})!=policy["expectedRows"]
            or (astropy.__version__,np.__version__)!=("7.2.0","2.3.5")):
        raise ValueError("Report coverage or runtime changed")
    old_cfg=(source/"protocollo.json").read_bytes()
    if hashlib.sha256(old_cfg).hexdigest()!=json.loads(files["riscontro.json"])["protocolSha256"]:
        raise ValueError("Source reader configuration changed")
    stride=json.loads(old_cfg)["blockBytes"]
    module=ast.parse(files["verifica.py"])
    reader_node=next(x for x in module.body if isinstance(x,ast.ClassDef) and x.name=="FitsRanges")
    reader_scope={"io":io,"hashlib":hashlib}
    exec(compile(ast.Module(body=[reader_node],type_ignores=[]),"pinned_range_reader.py","exec"),reader_scope)
    by_row=defaultdict(list)
    loaded={}
    for o,f in zip(recorded,fits_report,strict=True):
        key=o["catalogRow"]
        if f["catalogRow"]!=key or f["root"]!=o["root"]:
            raise ValueError("Observation/fit identity mismatch")
        row,used=reconstruct(reader_scope["FitsRanges"],meta[o["root"]],o,f,catalog[key],policy,stride,pins)
        row["perExposureDetectorCriterion"]=concordance(row["folds"],criteria,False)
        row["perExposureCelestialCriterion"]=concordance(row["folds"],criteria,True)
        by_row[key].append(row)
        loaded.update(used)
    results=[]
    for key,rows in sorted(by_row.items()):
        available=sum(r["status"]=="PROJECTED" for r in rows)
        measures=[m for r in rows for m in r["folds"]]
        combined=concordance(measures,criteria,True) if available>=2 else dict(passes=False,status="FEWER_THAN_TWO_EXPOSURES")
        degrees=catalog[key]["paDegrees"]
        results.append(dict(row=key,target=catalog[key]["twoMassId"],catalogPAdeg=degrees,
                            catalogPAsigmaDeg=catalog[key]["paSigmaDegrees"],availableExposures=available,
                            crossExposureCelestialCriterion=combined,
                            allProjectedPAsAgreeWithCatalog=bool(measures) and all(f["catalogPAWithinTolerance"] for f in measures),
                            bothOriginalCatalogMatchedExposures=sum(r.get("oldCatalogSeparationAndFluxBoth",False) for r in rows),
                            exposures=rows))
    with output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(dict(schema=policy["schema"],protocolSha256=hashlib.sha256(raw).hexdigest(),
                       results=results,replayedRanges=loaded,nativeExecutions=0,scientificClosures=0),
                  out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()
