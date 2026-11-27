"""Screen new GD153 visits without relaxing pointing, DQ, or time controls."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


def digest(blob):
    return sha256(blob).hexdigest()


def read(path,pin):
    raw=path.read_bytes()
    assert digest(raw)==pin,path
    return raw


def measure(np,fits,wcs,time,path,product,gaia,pam,p):
    with fits.open(path,memmap=False) as h:
        ph=h[0].header
        assert (ph["PROPOSID"],ph["FILTER"])==(product["proposal"],product["filter"])
        assert ph["TARGNAME"].replace("-","").replace(" ","").upper()=="GD153"
        sci=h["SCI",1]
        sh=sci.header
        chip=int(sh["CCDCHIP"])
        row={"file":product["file"],"visit":product["visit"],"band":product["filter"],"chip":chip,
             "dither":[float(ph[k]) for k in ("POSTARG1","POSTARG2")],"dateMjd":float(ph["EXPSTART"]),
             "state":"UNPROCESSED","measurements":{}}
        row["mode"]={k:ph[k] for k in ("SCAN_TYP","EXPFLAG","PCTECORR","FLUXCORR")}
        row["mode"]["BUNIT"]=sh["BUNIT"]
        if (ph["SCAN_TYP"],ph["EXPFLAG"],ph["PCTECORR"],ph["FLUXCORR"],sh["BUNIT"])!=(
            "N","NORMAL","COMPLETE","COMPLETE","ELECTRONS"):
            row["state"]="MODE_OR_CALIBRATION_REFUSED"
            return row
        f=lambda k:float(gaia[k])
        dt=time(row["dateMjd"],format="mjd",scale="utc").jyear-f("ref_epoch")
        ra=f("ra")+dt*f("pmra")/(3600000*np.cos(np.deg2rad(f("dec"))))
        dec=f("dec")+dt*f("pmdec")/3600000
        xg,yg=wcs(sh,h).celestial.world_to_pixel_values(ra,dec)
        row["gaiaPixelXY"]=[float(xg),float(yg)]
        if not np.isfinite([xg,yg]).all():
            row["state"]="INVALID_WCS"
            return row
        image=sci.data.astype(float)
        quality=h["DQ",1].data
        ny,nx=image.shape
        x0,y0=np.floor(np.array([xg,yg])+.5).astype(int)
        d=p["searchPx"]
        if x0<d+3 or y0<d+3 or x0+d+3>=nx or y0+d+3>=ny:
            row["state"]="PREDICTION_AT_EDGE"
            return row
        box=image[y0-d:y0+d+1,x0-d:x0+d+1]
        if not np.isfinite(box).all():
            row["state"]="NONFINITE_SEARCH"
            return row
        j,i=np.unravel_index(box.argmax(),box.shape)
        xp,yp=x0-d+int(i),y0-d+int(j)
        row["peakXY"]=[int(xp),int(yp)]
        core=quality[yp-3:yp+4,xp-3:xp+4]
        row["coreDqNonzero"]=int(np.count_nonzero(core))
        row["coreDqCountsByBit"]={str(b):int(np.count_nonzero(core & b)) for b in p["qualityBits"]}
        if row["coreDqNonzero"]:
            row["state"]="CORE_DQ"
            return row
        yy,xx=np.mgrid[yp-2:yp+3,xp-2:xp+3]
        patch=image[yy,xx]
        weights=np.maximum(patch-np.median(patch),0)
        if weights.sum()<=0:
            row["state"]="CENTROID_EMPTY"
            return row
        x,y=[float(np.average(axis,weights=weights)) for axis in (xx,yy)]
        row["centerXY"]=[x,y]
        separation=float(np.hypot(x-xg,y-yg))
        row["distanceFromGaiaPx"]=separation
        if separation>p["maxGaiaOffsetPx"]:
            row["state"]="CENTROID_OFFSET"
            return row
        assert chip in pam
        offsets=[abs(float(sh[k])) for k in ("LTV1","LTV2")]
        assert all(q==int(q) for q in offsets)
        x0,y0=map(int,offsets)
        area=pam[chip][y0:y0+ny,x0:x0+nx]
        assert area.shape==image.shape
        corrected=image*area
        good=(quality==0)&np.isfinite(corrected)
        yy,xx=np.ogrid[:ny,:nx]
        r2=(xx-x)**2+(yy-y)**2
        row["state"]="APERTURE_SUPPORT_REFUSED"
        for label,(low,high) in p["annuli"].items():
            if not (high<=x<nx-high and high<=y<ny-high):
                continue
            full=(low**2<=r2)&(r2<=high**2)
            sky=full&good
            if sky.sum()<p["minCleanSkyFraction"]*full.sum():
                continue
            background=float(np.median(corrected[sky]))
            for radius in p["radii"]:
                active=r2<=radius**2
                if not good[active].all():
                    continue
                value=float(np.sum(corrected[active]-background)/ph["EXPTIME"])
                if value>0:
                    row["measurements"][f"{label}:r{radius}"]=value
                    row["state"]="EVALUATED"
        return row


def main():
    parser=argparse.ArgumentParser()
    for n in ("root","dependencies","report"):
        parser.add_argument(n,type=Path)
    a=parser.parse_args()
    raw=(a.root/"protocollo.json").read_bytes()
    p=json.loads(raw)
    capture=json.loads(read(a.root/"acquisizione.json",p["capture"]))
    read(a.root/"observations.json",capture["catalogSha256"])
    syspath=str(a.dependencies)
    sys.path.insert(0,syspath)
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.time import Time
    from astropy.wcs import WCS
    assert (np.__version__,astropy.__version__)==("2.3.5","7.2.0")
    gaia,=csv.DictReader(read(a.root/"gaia.csv",p["gaia"]).decode().splitlines())
    assert gaia["source_id"]=="3944400490365194368"
    pam={}
    for key,entry in p["pam"].items():
        source=a.root/entry["file"]
        read(source,entry["sha256"])
        pam[int(key)]=fits.getdata(source)
    rows=[]
    associations=[]
    for assoc in capture["associations"]:
        obs=assoc["association"]
        read(a.root/"source"/f"{obs}-query.json",assoc["requestSha256"])
        archive=json.loads(read(a.root/"source"/f"{obs}-products.json",assoc["responseSha256"]))
        flc={prod["productFilename"] for prod in archive["data"] if prod["productSubGroupDescription"]=="FLC"
             and prod["productType"]=="SCIENCE" and prod["project"]=="CALWF3" and prod["dataRights"]=="PUBLIC"}
        assert flc=={prod["file"] for prod in assoc["rows"]}
        associations.append({"association":obs,"filter":assoc["filter"],"publicCalwf3Flc":len(flc)})
        for product in assoc["rows"]:
            path=a.root/"source"/product["file"]
            assert len(read(path,product["sha256"]))==product["bytes"]
            rows.append(measure(np,fits,WCS,Time,path,product,gaia,pam,p))
    by_visit={}
    for row in rows:
        by_visit.setdefault((row["visit"],row["chip"],tuple(row["dither"])),[]).append(row)
    matched=[]
    bands=p["bands"]
    for (visit,chip,dither),group in sorted(by_visit.items()):
        assert len(group)==3 and {r["band"] for r in group}==set(bands)
        dt=max(r["dateMjd"] for r in group)-min(r["dateMjd"] for r in group)
        keys=set.intersection(*(set(r["measurements"]) for r in group)) if dt<=p["maxSpanDays"] else set()
        both=[mode for mode in p["annuli"] if all(f"{mode}:r{r}" in keys for r in p["radii"])]
        growth={}
        for mode in both:
            by_band={r["band"]:r["measurements"][f"{mode}:r10"]/r["measurements"][f"{mode}:r5"] for r in group}
            growth[mode]={f"{b}-{r}":float(-2500*np.log10(by_band[b]/by_band[r]))
                          for b,r in combinations(bands,2)}
        matched.append({"visit":visit,"chip":chip,"dither":dither,"spanDays":dt,
                        "matchedApertureGrowthMillimag":growth,"memberStates":sorted(r["state"] for r in group)})
    out={"schema":"BKL046_GD153_CALIBRATION_STARE_CANDIDATES_RESULT_V2","programSha256":digest(Path(__file__).read_bytes()),
         "protocolSha256":digest(raw),"associations":associations,"rows":rows,
         "groups":matched,"states":Counter(r["state"] for r in rows),
         "newThreeBandVisits":sorted({t["visit"] for t in matched if t["matchedApertureGrowthMillimag"]}),
         "nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(out,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
