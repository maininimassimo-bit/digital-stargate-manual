"""Check field-reference availability without changing rejected GD71 astrometry."""
import csv
from hashlib import sha256
import json
from math import cos, radians
from pathlib import Path
import sys

import numpy as np

PIN="4f40cb9a2af0afecf50584ca5d738e37fcbcc957b875c56ff319532b3ea2c4f5"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pinned(path, expected):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==expected, "Digest changed")
    return raw


def world(row, year):
    ra,dec=float(row["ra"]),float(row["dec"])
    if row["pmra"] and row["pmdec"]:
        dt=year-float(row["ref_epoch"])
        ra+=dt*float(row["pmra"])/(3600000*cos(radians(dec)))
        dec+=dt*float(row["pmdec"])/3600000
    return np.array([ra,dec])


def tangent(world_a,world_b):
    delta=np.asarray(world_a)-np.asarray(world_b)
    return delta*np.array([3600*cos(radians(world_b[1])),3600.])


def brightest_patch(science, flags, plan):
    good=np.isfinite(science)&np.isin(flags,plan["eligibleDq"])
    detrended=science-float(np.median(science[good]))
    total=np.zeros((len(science)-4,science.shape[1]-4))
    counts=np.zeros(total.shape,dtype=int)
    for y in range(5):
        for x in range(5):
            area=np.s_[y:y+total.shape[0],x:x+total.shape[1]]
            total+=np.where(good[area],detrended[area],0.)
            counts+=good[area]
    control=good[2:-2,2:-2]&(counts>=plan["minimumWindowPixels"])
    require(control.any(),"No eligible source window")
    ys,xs=np.unravel_index(np.argmax(np.where(control,total,-np.inf)),total.shape)
    area=np.s_[ys:ys+5,xs:xs+5]
    weights=np.where(good[area],np.maximum(detrended[area],0.),0.)
    require(float(weights.sum())>0,"No positive candidate")
    dy,dx=np.indices((5,5))
    center=np.array([xs+float((dx*weights).sum()/weights.sum()),
                     ys+float((dy*weights).sum()/weights.sum())])
    return center,float(total[ys,xs])


def audit(plan,catalogue,reference,receipt,root,fits,WCS):
    blob=pinned(root/(receipt["obsId"]+"_flt.fits"),receipt["sha256"])
    require(len(blob)==receipt["bytes"],"Archive image size changed")
    from io import BytesIO
    with fits.open(BytesIO(blob),memmap=False) as image:
        primary=image[0].header
        sci=image["SCI",1]
        require(primary["ROOTNAME"].lower()==receipt["obsId"] and primary["PROPOSID"]==9020
                and primary["TARGNAME"].upper()=="GD71" and sci.header["CCDCHIP"]==receipt["chip"],
                "Unexpected exposure identity")
        flags=image["DQ",1].data
        science=sci.data.astype(float)
        wcs=WCS(sci.header,image)
        midpoint=(primary["EXPSTART"]+primary["EXPEND"])/2
        year=2000+(midpoint-51544.5)/365.25
        identity=world(reference,year)
        peak,electrons=brightest_patch(science,flags,plan)
        peak_world=wcs.all_pix2world([peak],0,ra_dec_order=True)[0]
        require(np.isfinite(peak_world).all(),"Invalid field transform")
        ny,nx=science.shape
        edge=np.array([(x,y) for x in range(nx) for y in (0,ny-1)]
                     +[(x,y) for y in range(1,ny-1) for x in (0,nx-1)])
        boundary=wcs.all_pix2world(edge,0,ra_dec_order=True)
        correction=identity-peak_world
        d_origin=np.linalg.norm(tangent(boundary,plan["gaiaFieldCenter"]),axis=1)
        d_shift=np.linalg.norm(tangent(boundary+correction,plan["gaiaFieldCenter"]),axis=1)
        require(max(d_origin.max(),d_shift.max())<plan["gaiaFieldRadiusDegrees"]*3600,
                "Archive cone does not enclose sampled boundaries")
        positions=np.stack([world(row,year) for row in catalogue])
        nominal=wcs.all_world2pix(positions,0,ra_dec_order=True)
        shifted=wcs.all_world2pix(positions-correction,0,ra_dec_order=True)
        def other_inside(pixels):
            return [row["source_id"] for row,(x,y) in zip(catalogue,pixels,strict=True)
                    if row["source_id"]!=reference["source_id"] and 0<=x<nx and 0<=y<ny]
        return dict(obsId=receipt["obsId"],visit=receipt["visit"],band=receipt["band"],
                    peakPx=peak.tolist(),candidateWindowElectrons=electrons,
                    rawCatalogueOffsetArcsec=tangent(peak_world,identity).tolist(),
                    maxBoundaryArcsecNominal=float(d_origin.max()),
                    maxBoundaryArcsecCandidateShift=float(d_shift.max()),
                    otherGaiaIdsNominal=other_inside(nominal),
                    otherGaiaIdsCandidateShift=other_inside(shifted))


def main():
    spec, root, rejected, field, dependencies, out=map(Path,sys.argv[1:])
    plan=json.loads(pinned(spec,PIN))
    archive=json.loads(pinned(root/"riscontro.json",plan["ingressSha256"]))["exposures"]
    previous=json.loads(pinned(rejected,plan["rejectedMeasurementSha256"]))["visits"]
    failed={row["obsId"] for visit in ("j8c103","j8c104") for row in previous[visit]["exposures"]
            if row["state"]=="PEAK_NOT_IDENTIFIED"}
    require(len(archive)==len(failed)==8 and failed=={row["obsId"] for row in archive},"Changed rejected roster")
    rows=list(csv.DictReader(pinned(field,plan["gaiaFieldSha256"]).decode().splitlines()))
    catalogue=[row for row in rows if np.linalg.norm(tangent([float(row["ra"]),float(row["dec"])],
                                    plan["gaiaFieldCenter"]))<=plan["gaiaFieldRadiusDegrees"]*3600]
    reference,=[row for row in catalogue if row["source_id"]==plan["gd71Id"]]
    sys.path.insert(0,str(dependencies))
    from astropy.io import fits
    from astropy.wcs import WCS
    data=[audit(plan,catalogue,reference,row,root,fits,WCS) for row in archive]
    reports={}
    for visit in ("j8c103","j8c104"):
        case=[row for row in data if row["visit"]==visit]
        require(len(case)==4,"Missing split")
        per_visit=np.array([row["peakPx"] for row in case])
        largest=max(float(np.linalg.norm(a-b)) for a in per_visit for b in per_visit)
        reports[visit]=dict(exposures=case,largestCandidateSeparationPx=largest,
            otherReferencesInEitherProjection=len({sid for row in case
                for sid in row["otherGaiaIdsNominal"]+row["otherGaiaIdsCandidateShift"]}))
    report=dict(schema="BKL046_GD71_9020_ASTROMETRY_DIAGNOSTIC_RESULT_V1",
                protocolSha256=PIN,arcsecondsConeDiameter=plan["gaiaFieldRadiusDegrees"]*7200,
                archiveGaiaConeRows=len(catalogue),rowsWithoutProperMotion=sum(not row["pmra"] for row in catalogue),
                visits=reports,astrometricCorrectionIndependentlyVerified=False,
                earlierRejectionsPreserved=len(failed),scientificClosures=0,nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
