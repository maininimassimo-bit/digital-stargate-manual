"""Perform forced photometry for the only additional Gaia reference candidate."""
from collections import defaultdict
import csv
from hashlib import sha256
from io import BytesIO
import json
from math import ceil, sqrt
from pathlib import Path
import sys

import numpy as np

PIN="b9603b6ae8396f32a9f89a0276a950452de3900163b8c1af71c8cd4a02572218"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, expected):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==expected,"Input digest differs")
    return raw


def forced(hdus, position, spec):
    img=hdus["SCI",1].data
    err=hdus["ERR",1].data
    dq=hdus["DQ",1].data
    x,y=position
    cx,cy=np.rint(position).astype(int)
    a,b=spec["skyAnnulusPx"]
    radius=ceil(b)+1
    if not (radius<=cx<img.shape[1]-radius and radius<=cy<img.shape[0]-radius):
        return {"state":"SKY_BOUNDARY"}
    roi=np.s_[cy-radius:cy+radius+1,cx-radius:cx+radius+1]
    yy,xx=np.indices(img[roi].shape,dtype=float)
    r2=(xx+cx-radius-x)**2+(yy+cy-radius-y)**2
    plane=img[roi].astype(float)
    error=err[roi].astype(float)
    flags=dq[roi]
    valid=np.isfinite(plane)&np.isfinite(error)&(error>=0)
    aperture=r2<=spec["aperturePx"]**2
    annulus=(r2>=a*a)&(r2<=b*b)
    sky=annulus & valid & (flags==0)
    if not np.all((valid&np.isin(flags,spec["acceptedDq"]))[aperture]) or sky.sum()<0.7*annulus.sum():
        return {"state":"DQ_OR_SKY_INCOMPLETE"}
    median=float(np.median(plane[sky]))
    mad=float(np.median(np.abs(plane[sky]-median)))
    sky_term=1.253314*1.4826*mad*int(aperture.sum())/sqrt(sky.sum())
    noise=sqrt(float(np.sum(error[aperture]**2))+sky_term**2)
    require(noise>0,"Invalid diagnostic noise")
    signal=float(np.sum(plane[aperture]-median))
    return dict(state="MEASURED_DIAGNOSTIC",pixels=int(aperture.sum()),signalElectrons=signal,
                diagnosticNoiseElectrons=noise,diagnosticSnr=signal/noise,
                exceedsIndividualThreshold=signal/noise>=spec["minimumIndividualDiagnosticSnr"])


def main():
    params, previous, parent_plan, archive, field, deps, out=map(Path,sys.argv[1:])
    spec=json.loads(pinned(params,PIN))
    prev=json.loads(pinned(previous/"riscontro.json",spec["precedingReceiptSha256"]))
    parent=json.loads(pinned(parent_plan,prev["protocolSha256"]))
    code=pinned(previous/"verifica.py",spec["precedingVerifierSha256"])
    env={"__name__":"pinned_astrometry"}
    exec(compile(code,"pinned-astrometry.py","exec"),env)
    rows={row["source_id"]:row for row in csv.DictReader(pinned(field,parent["gaiaFieldSha256"]).decode().splitlines())}
    target, reference=(rows[spec[key]] for key in ("targetGaiaId","secondGaiaId"))
    manifest={row["obsId"]:row for row in json.loads(pinned(archive/"riscontro.json",parent["ingressSha256"]))["exposures"]}
    sys.path.insert(0,str(deps))
    from astropy.io import fits
    from astropy.wcs import WCS
    visits={}
    for visit, item in prev["visits"].items():
        details=[]
        successes=defaultdict(int)
        for row in item["exposures"]:
            name=row["obsId"]
            require(row["otherGaiaIdsCandidateShift"]==[spec["secondGaiaId"]],"Reference roster changed")
            raw=pinned(archive/(name+"_flt.fits"),manifest[name]["sha256"])
            with fits.open(BytesIO(raw),memmap=False) as hdus:
                h=hdus[0].header
                w=WCS(hdus["SCI",1].header,hdus)
                t=2000+((h["EXPSTART"]+h["EXPEND"])/2-51544.5)/365.25
                predicted=w.all_pix2world([row["peakPx"]],0,ra_dec_order=True)[0]+env["world"](reference,t)-env["world"](target,t)
                position=w.all_world2pix([predicted],0,ra_dec_order=True)[0]
                result=forced(hdus,position,spec)
            successes[row["band"]]+=bool(result.get("exceedsIndividualThreshold"))
            details.append(dict(obsId=name,band=row["band"],expectedPositionPx=position.tolist(),**result))
        visits[visit]=dict(results=details,repeatDetectionByBand=dict(successes),
                           satisfiesRepeatRule=any(x==2 for x in successes.values()))
    report=dict(schema="BKL046_GD71_9020_SECOND_REFERENCE_RESULT_V1",protocolSha256=PIN,
                visits=visits, candidateGaiaMagnitude=float(reference["phot_g_mean_mag"]),
                epochAstrometryIndependentlyCalibrated=False,
                repeatedCandidateDetectionEveryVisit=all(x["satisfiesRepeatRule"] for x in visits.values()),
                scientificClosures=0, earlierRejectionsPreserved=8, nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
