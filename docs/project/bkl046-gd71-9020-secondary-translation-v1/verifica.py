"""Fit a per-visit translation from a faint source and hold GD71 out of the fit."""
import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from statistics import mean
import sys

import numpy as np

PIN="d4406c3be5fdcb020136208e013cc30213a553889920ba2b42308bf80e510963"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, expected):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==expected,"Pinned input changed")
    return raw


def aperture_photometry(hdus, center, pam, plan):
    science=hdus["SCI",1]
    hdr=science.header
    exposure=float(hdus[0].header["EXPTIME"])
    x,y=np.rint(center).astype(int)
    roi=np.s_[y-42:y+43,x-42:x+43]
    ox,oy=-hdr["LTV1"],-hdr["LTV2"]
    require((ox,oy)==(int(ox),int(oy)) and hdr["LTM1_1"]==hdr["LTM2_2"]==1.,"PAM grid differs")
    ox,oy=int(ox),int(oy)
    area=pam[oy+y-42:oy+y+43,ox+x-42:ox+x+43]
    data=science.data[roi].astype(float)
    err=hdus["ERR",1].data[roi]
    dq=hdus["DQ",1].data[roi]
    require(area.shape==data.shape==err.shape==dq.shape==(85,85),"Aperture support changed")
    require(np.isfinite(area).all() and (area>0).all(),"Invalid area map")
    data*=area
    yy,xx=np.indices(data.shape,dtype=float)
    r2=(xx+x-42-center[0])**2+(yy+y-42-center[1])**2
    good=np.isfinite(data)&np.isfinite(err)&(err>=0)&np.isin(dq,[0,64])
    a,b=plan["skyAnnulusPx"]
    ring=(r2>=a*a)&(r2<=b*b)
    sky=ring&good&(dq==0)
    output={}
    for radius in plan["apertureRadiiPx"]:
        inside=r2<=radius**2
        row=dict(state="EXCLUDED_DQ_OR_SKY",missing=int(np.count_nonzero(inside&~good)))
        if not row["missing"] and sky.sum()>=0.7*ring.sum():
            rate=float(np.sum(data[inside]-np.median(data[sky]))/exposure)
            require(rate>0,"Unexpected nonpositive source")
            row=dict(state="MEASURED_TRANSLATION_DIAGNOSTIC",missing=0,electronsPerSecond=rate)
        output[str(radius)]=row
    return output


def main():
    protocol, pre, archive, field, pam1, pam2, dependencies, out=map(Path,sys.argv[1:])
    plan=json.loads(pinned(protocol,PIN))
    prev=json.loads(pinned(pre/"riscontro.json",plan["priorAstrometrySha256"]))
    second=json.loads(pinned(pre/"secondo-riscontro.json",plan["secondaryReceiptSha256"]))
    code=pinned(pre/"verifica.py",plan["primaryRunnerSha256"])
    env={"__name__":"historical_centroid"}
    exec(compile(code,"historical_centroid.py","exec"),env)
    catalogue={row["source_id"]:row for row in csv.DictReader(pinned(field,plan["gaiaSha256"]).decode().splitlines())}
    target,ref=(catalogue[plan["gaiaIds"][name]] for name in ("target","reference"))
    files=json.loads(pinned(archive/"riscontro.json",plan["fitsReceiptSha256"]))["exposures"]
    sys.path.insert(0,str(dependencies))
    from astropy.io import fits
    from astropy.wcs import WCS
    pams={i:fits.getdata(BytesIO(pinned(path,plan["pamByChip"][str(i)]))) for i,path in ((1,pam1),(2,pam2))}
    results={}
    for visit, box in plan["referenceBoxes"].items():
        cases=[row for row in files if row["visit"]==visit]
        require(len(cases)==4 and second["visits"][visit]["repeatDetectionByBand"][plan["fitBand"]]==2,
                "Faint reference ingress differs")
        adjusted=[]
        for row in cases:
            if row["band"]!=plan["fitBand"]:
                continue
            blob=pinned(archive/(row["obsId"]+"_flt.fits"),row["sha256"])
            with fits.open(BytesIO(blob),memmap=False) as hdus:
                head=hdus[0].header
                time=2000+((head["EXPSTART"]+head["EXPEND"])/2-51544.5)/365.25
                sci=hdus["SCI",1]
                dq=hdus["DQ",1].data
                x,y=box
                half=plan["boxHalfWidth"]
                roi=np.s_[y-half:y+half+1,x-half:x+half+1]
                center,score=env["brightest_patch"](sci.data[roi].astype(float),dq[roi],
                                         dict(eligibleDq=[0,64],minimumWindowPixels=24))
                center+=np.array([x-half,y-half])
                require(np.all(abs(center-np.array(box))<half-2),"Faint fit reaches search boundary")
                wcs=WCS(sci.header,hdus)
                observed=wcs.all_pix2world([center],0,ra_dec_order=True)[0]
                known=env["world"](ref,time)
                adjusted.append(dict(file=row["obsId"],positionPx=center.tolist(),score=score,
                                     shiftDegrees=(known-observed).tolist(),cataloguePosition=known.tolist()))
        require(len(adjusted)==2,"Fit split coverage differs")
        shifts=np.array([row["shiftDegrees"] for row in adjusted])
        transfer=np.mean(shifts,axis=0)
        origin=np.array(adjusted[0]["cataloguePosition"])
        discrepancy=float(np.linalg.norm(env["tangent"](origin+shifts[0]-shifts[1],origin)))
        check_rows=[]
        historical={row["obsId"]:row for row in prev["visits"][visit]["exposures"]}
        for row in cases:
            blob=pinned(archive/(row["obsId"]+"_flt.fits"),row["sha256"])
            with fits.open(BytesIO(blob),memmap=False) as hdus:
                head=hdus[0].header
                epoch=2000+((head["EXPSTART"]+head["EXPEND"])/2-51544.5)/365.25
                img=hdus["SCI",1]
                dq=hdus["DQ",1].data
                wcs=WCS(img.header,hdus)
                expected=wcs.all_world2pix([env["world"](target,epoch)-transfer],0,ra_dec_order=True)[0]
                found,_=env["brightest_patch"](img.data.astype(float),dq,
                                          dict(eligibleDq=[0,64],minimumWindowPixels=24))
                np.testing.assert_array_equal(found,historical[row["obsId"]]["peakPx"])
                residual=float(np.linalg.norm(found-expected))
                accepted=discrepancy<=plan["maximumReferenceSplitDifferenceArcsec"] and residual<=plan["maximumTargetResidualPx"]
                check=dict(obsId=row["obsId"],band=row["band"],predictedPx=expected.tolist(),
                           observedPx=found.tolist(),residualPx=residual,astrometricDiagnosticPass=accepted)
                if accepted:
                    check["apertures"]=aperture_photometry(hdus,found,pams[row["chip"]],plan)
            check_rows.append(check)
        validation=[row for row in check_rows if row["band"]==plan["validationBand"]]
        require(len(validation)==2,"Holdout split coverage differs")
        qualified=all(row["astrometricDiagnosticPass"] for row in validation)
        ratios={}
        if qualified:
            for n in plan["apertureRadiiPx"]:
                key=str(n)
                bands={}
                for label in (plan["fitBand"],plan["validationBand"]):
                    rates=[]
                    for row in check_rows:
                        datum=row.get("apertures",{}).get(key,{})
                        if row["band"]==label and datum.get("state")=="MEASURED_TRANSLATION_DIAGNOSTIC":
                            rates.append(datum["electronsPerSecond"])
                    if len(rates)==2:
                        bands[label]=mean(rates)
                if len(bands)==2:
                    ratios[key]=bands[plan["validationBand"]]/bands[plan["fitBand"]]
        results[visit]=dict(referenceFits=adjusted,splitAstrometryDifferenceArcsec=discrepancy,
                            fitUsesTargetCentroid=False,heldOutTargetSplitsPass=qualified,
                            predictedTargetRows=check_rows,narrowbandRatiosDiagnostic=ratios)
    report=dict(schema="BKL046_GD71_9020_SECONDARY_TRANSLATION_RESULT_V1",protocolSha256=PIN,visits=results,
                previousExclusionsPreserved=8,translationFitWithTargetExcluded=True,
                initialSearchRegionInformedByEarlierTargetCandidate=True,
                absoluteWcsIndependentCalibrationEstablished=False,cteCorrectionApplied=False,
                scientificClosures=0,nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
