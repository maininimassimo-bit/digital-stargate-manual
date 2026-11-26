"""Measure GD71 and G191B2B ACS visits using the pinned 3–20 pixel aperture rules."""
from collections import Counter
from hashlib import file_digest, sha256
import json
from math import cos, radians, sqrt
from pathlib import Path
from statistics import mean
import sys

import numpy as np

PIN = "a272ce12238d18d5cb1027efc9dfc839d3f993a7158a47678bd4ee531959e4fb"


def require(ok, label):
    if not ok:
        raise ValueError(label)


def checked(path, pin):
    with path.open("rb") as stream:
        require(file_digest(stream,"sha256").hexdigest()==pin, "Pinned bytes differ")


def load(path, pin):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest()==pin, "Pinned receipt differs")
    return json.loads(raw)


def measure(path, row, star, plan, pam, fits, WCS):
    checked(path,row["sha256"])
    require(path.stat().st_size==row["bytes"], "FITS size differs")
    with fits.open(path,memmap=False) as hdus:
        h = hdus[0].header
        img = hdus["SCI",1]
        t = img.header
        names = (h["APERTURE"], h["CCDAMP"], t["CCDCHIP"], h["PCTECORR"])
        require(names==(row["aperture"],row["amp"],row["chip"],row["pctecorr"])
                and h["ROOTNAME"].lower()==row["obsId"] and h["EXPFLAG"]=="NORMAL" and t["BUNIT"]=="ELECTRONS"
                and h["TARGNAME"].upper().replace(" ","")==star and row["band"] in (h["FILTER1"],h["FILTER2"]),
                "FITS physical identity differs")
        ra,dec,pmra,pmdec=plan["astrometricJ2000"][star]
        dt=((h["EXPSTART"]+h["EXPEND"])/2-51544.5)/365.25
        predicted=[ra+dt*pmra/(3600000*cos(radians(dec))),dec+dt*pmdec/3600000]
        loc,header_loc=WCS(t,hdus).all_world2pix([predicted,[h["RA_TARG"],h["DEC_TARG"]]],0,ra_dec_order=True)
        x0,y0 = np.rint(loc).astype(int)
        data=img.data
        flags=hdus["DQ",1].data
        noise=hdus["ERR",1].data
        span=plan["centroidSearchRadiusPx"]
        ny,nx=data.shape
        result=dict(band=row["band"],obsId=row["obsId"],chip=row["chip"],amp=row["amp"],
                    source=star, aperture=row["aperture"],state="NO_APERTURE",radii={})
        if not (span <= x0 < nx-span and span <= y0 < ny-span):
            result["state"]="SEARCH_OUTSIDE_IMAGE"
            return result
        region=np.s_[y0-span:y0+span+1,x0-span:x0+span+1]
        cut=data[region]
        yy,xx=np.indices(cut.shape)-span
        eligible=(xx*xx+yy*yy<=span**2)&np.isfinite(cut)
        require(eligible.any(),"Empty search region")
        iy,ix=np.unravel_index(np.argmax(np.where(eligible,cut,-np.inf)),cut.shape)
        y,x=y0+iy-span,x0+ix-span
        distances=[float(np.linalg.norm(point-[x,y])) for point in (loc,header_loc)]
        result.update(peak=[int(x),int(y)],distancesToCatalogueAndHeaderPx=distances)
        if distances[0]>span or distances[1]>plan["maxDistanceFromHeaderTargetPx"] or cut[iy,ix]<1000:
            result["state"]="PEAK_NOT_IDENTIFIED"
            return result
        if not (42 <= x < nx-42 and 42 <= y < ny-42):
            result["state"]="SKY_BOUNDARY"
            return result
        central=data[y-2:y+3,x-2:x+3].astype(float)
        weights=np.maximum(central-np.median(central),0.)
        yy,xx=np.indices(central.shape,dtype=float)-2
        dy,dx=np.sum([yy*weights,xx*weights],axis=(1,2))/np.sum(weights)
        ox,oy=[-t[k] for k in ("LTV1","LTV2")]
        require((ox,oy)==(int(ox),int(oy)) and min(ox,oy)>=0 and t["LTM1_1"]==t["LTM2_2"]==1.,
                "PAM coordinate transform differs")
        ox,oy=int(ox),int(oy)
        footprint=pam[oy+y-42:oy+y+43,ox+x-42:ox+x+43]
        require(footprint.shape==(85,85) and np.all(np.isfinite(footprint)&(footprint>0)),"Invalid PAM support")
        roi=np.s_[y-42:y+43,x-42:x+43]
        electrons=data[roi].astype(float)
        flux=electrons*footprint
        dq=flags[roi]
        err=noise[roi]
        yy,xx=np.indices(dq.shape,dtype=float)-42
        r2=(yy-dy)**2+(xx-dx)**2
        accepted=np.isin(dq,plan["referenceDq"])&np.isfinite(flux)&np.isfinite(err)&(err>=0.)
        a,b=plan["skyRingPx"]
        ring=(r2>=a*a)&(r2<=b*b)
        sky=ring&accepted&(dq==0)
        if sky.sum()<0.7*ring.sum():
            result["state"]="SKY_INCOMPLETE"
            return result
        pedestal=np.median(flux[sky])
        raw_sky=np.median(electrons[sky])
        result.update(state="EVALUATED",centerDetectorPx=[float(ox+x+dx),float(oy+y+dy)],
                      prePamSkyElectronPerPixel=float(raw_sky))
        for radius in plan["radiiPx"]:
            aperture=r2<=radius**2
            bits=Counter(map(int,dq[aperture & (dq!=0)]))
            stored=dict(state="EXCLUDED_DQ_OR_SUPPORT",dqCounts={str(flag):n for flag,n in bits.items()},
                        saturatedPixels=int(np.count_nonzero((dq[aperture]&256)!=0)))
            if np.all(accepted[aperture]):
                measured=float(np.sum(flux[aperture]-pedestal))
                uncorrected=float(np.sum(electrons[aperture]-raw_sky))
                if measured>0:
                    stored.update(state="MEASURED",rate=measured/h["EXPTIME"],prePamElectron=uncorrected,
                                  countWithinDocumentedThreePixelCteFluxRange=(
                                      50<=uncorrected<=80000 if radius==3 else None))
            result["radii"][str(radius)]=stored
        return result


def summarize(rows,plan):
    out={}
    for radius in plan["radiiPx"]:
        key=str(radius)
        bands={}
        for item in rows:
            value=item["radii"].get(key)
            if value and value["state"]=="MEASURED":
                bands.setdefault(item["band"],[]).append(value["rate"])
        ranges={}
        for a,b in (("F658N","F660N"),("F658N","F606W"),("F660N","F606W")):
            if bands.get(a) and bands.get(b):
                ranges[a+"/"+b]=dict(value=mean(bands[a])/mean(bands[b]),
                                    exposureCounts=[len(bands[a]),len(bands[b])])
        out[key]=dict(ratios=ranges,measuredPerBand={name:len(values) for name,values in bands.items()})
    return out


def main():
    protocol, gd71, g191, pam1, pam2, dependencies, gd71prior, out=map(Path,sys.argv[1:])
    plan=load(protocol,PIN)
    sys.path.insert(0,str(dependencies))
    from astropy.io import fits
    from astropy.wcs import WCS
    pams={}
    for number, path in ((1,pam1),(2,pam2)):
        checked(path,plan["pamByChip"][str(number)])
        pams[number]=fits.getdata(path)
    receipts={}
    for root,pin,star,count in ((gd71,plan["files9020Sha256"],"GD71",8),
                                (g191,plan["filesG191Sha256"],"G191B2B",6)):
        sources=load(root/"riscontro.json",pin)["exposures"]
        require(len(sources)==count,"Exposure roster differs")
        for row in sources:
            visit=row.get("visit",row["obsId"][:6])
            result=measure(root/(row["obsId"]+"_flt.fits"),row,star,plan,pams[row["chip"]],fits,WCS)
            receipts.setdefault(visit,[]).append(result)
    require({key:len(value) for key,value in receipts.items()}=={"j8c103":4,"j8c104":4,"j8v604":6},
            "Visit roster differs")
    prior=load(gd71prior,plan["gd71ReferenceSha256"])["overview"]
    visits={name:dict(exposures=rows,apertures=summarize(rows,plan)) for name,rows in receipts.items()}
    report=dict(schema="BKL046_ACS_HISTORICAL_NARROWBAND_MEASUREMENT_RESULT_V1",protocolSha256=PIN,
                visits=visits, gd71Program10054Reference={key:prior[key]["ratios"] for key in ("3","5","10")},
                cteCorrectionApplied=False,separateChipAmplifierEpoch=True,
                scientificClosures=0,nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
