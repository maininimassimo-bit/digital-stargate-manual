"""Compare pinned ACS chip/time throughput to the GD71 historical visit ratios."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import runpy
from statistics import mean
import sys

import numpy as np

PIN="02760d221e0e4d995082bf8c046c522f151b4e2f84f2c3732b65b5083aa33d80"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, expected):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==expected,"Pinned input differs")
    return raw


def calc(integral, chain, grid, spectra, orders):
    (rates, sensitivity, outside), (check, sensitivity8, outside8) = [
        integral(chain,grid,spectra,n) for n in orders]
    np.testing.assert_allclose(rates,check,rtol=1e-9,atol=0.)
    np.testing.assert_allclose([sensitivity,outside],[sensitivity8,outside8],rtol=1e-9,atol=1e-15)
    require((rates>0).all(),"Nonpositive band prediction")
    return rates,sensitivity,outside


def main():
    protocol, astrometry, archive, prev, library, calspec_path, gaia_path, acs_path, reference, out=map(Path,sys.argv[1:])
    plan=json.loads(pinned(protocol,PIN))
    ast=json.loads(pinned(astrometry,plan["fit9020Sha256"]))["visits"]
    history=json.loads(pinned(prev,plan["previousComparisonSha256"]))["comparisons"]["GD71"]
    data=json.loads(pinned(gaia_path,plan["gaiaSpectraSha256"]))
    wave=np.array(data["gridNm"])*10
    flux=np.array(data["spectra"]["GD71"]["flux"])*100
    receipt=json.loads(pinned(archive/"riscontro.json",plan["ingress9020Sha256"]))
    require(len(receipt["exposures"])==8,"Exposure roster differs")
    acs=json.loads(pinned(acs_path,plan["acsProtocolSha256"]))
    sys.path.insert(0,acs["packages"])
    from astropy.io import fits
    functions={"__name__":"archive_photometry"}
    exec(compile(pinned(library,plan["integrationRunnerSha256"]),"archive_photometry.py","exec"),functions)
    integral=functions["integral"]
    spect=functions["calspec"]
    factor=functions["RATE_FACTOR"]
    wavelength,ref_flux=spect(calspec_path,plan["gd71CalspecSha256"],fits)
    ref_grid=np.interp(wave,wavelength,ref_flux)
    helper=Path(acs["helper"])
    pinned(helper,acs["helperSha256"])
    throughput=runpy.run_path(str(helper))["throughput"]
    source=Path(acs["capture"])
    captured=json.loads(pinned(source,acs["captureSha256"]))
    require(captured["routes"]==acs["routes"],"ACS paths differ")
    names={item for route in acs["routes"].values() for item in route}
    for name in names:
        pinned(source.parent/name,captured["components"][name]["sha256"])
    wfc2=plan["chip2ReferenceFile"]
    pinned(reference/wfc2,plan["chip2ReferenceSha256"])
    require(all(sum("ccd1_mjd" in key for key in route)==1 for route in acs["routes"].values()),
            "Missing replaceable response")
    measurements={}
    for visit in ast:
        entries=[row for row in receipt["exposures"] if row["visit"]==visit]
        require(len(entries)==4 and ast[visit]["heldOutTargetSplitsPass"],"Incomplete visit")
        measured=[]
        for row in entries:
            blob=pinned(archive/(row["obsId"]+"_flt.fits"),row["sha256"])
            with fits.open(BytesIO(blob),memmap=False) as image:
                sma=image["SCI",1].header
                require(sma["CCDCHIP"]==row["chip"] and image[0].header["EXPSTART"]==row["expStartMjd"],
                        "Chip or exposure epoch differs")
                photflam=sma["PHOTFLAM"]
            centres={}
            for chip in (row["chip"],1):
                if str(chip) in centres:
                    continue
                throughput.__globals__["EPOCH"]=row["expStartMjd"]
                response=[]
                for original in acs["routes"][row["band"].lower()]:
                    item=wfc2 if chip==2 and "ccd1_mjd" in original else original
                    throughput.__globals__["DEST"]=reference if item==wfc2 else source.parent
                    response.append(throughput(np,fits,item))
                rates,sensitivity,tail=calc(integral,response,wave,[flux,ref_grid],plan["quadratureOrders"])
                physical,check,other=calc(integral,response,wavelength,[ref_flux],plan["quadratureOrders"])
                require(abs(check/sensitivity-1)<1e-9 and other<=1e-10,"Inconsistent wavelength coverage")
                centres[str(chip)]=dict(gaia=float(rates[0]),calspecSameGrid=float(rates[1]),
                                       calspecFull=float(physical[0]),gaiaOutOfGrid=tail,
                                       relativeModelVsHeaderPhotflam=1/(sensitivity*factor)/photflam-1)
            measured.append(dict(exposure=row["obsId"],band=row["band"],chip=row["chip"],responses=centres))
        chips={row["chip"] for row in measured}
        require(len(chips)==1,"Unexpected mixed-chip visit")
        chip=str(next(iter(chips)))
        first,second=plan["bands"]
        ref={}
        for key in ("gaia","calspecSameGrid","calspecFull"):
            def ratio(c):
                a,b=([row["responses"][c][key] for row in measured if row["band"]==band]
                     for band in (first,second))
                require(len(a)==len(b)==2,"Incomplete split")
                return mean(a)/mean(b)
            ref[key]=dict(asObservedChip=ratio(chip),ifWfc1=ratio("1"))
        observe=ast[visit]["narrowbandRatiosDiagnostic"]
        points={str(r):dict(measured=observe[str(r)],measuredVsGaia=observe[str(r)]/ref["gaia"]["asObservedChip"]-1,
                           measuredVsCalspec=observe[str(r)]/ref["calspecFull"]["asObservedChip"]-1)
                for r in plan["radii"]}
        measurements[visit]=dict(chip=int(chip),predictions=ref,apertures=points,rows=measured)
    a,b=(measurements[name] for name in ("j8c103","j8c104"))
    difference={key:dict(ownChip=a["predictions"][key]["asObservedChip"]/b["predictions"][key]["asObservedChip"]-1,
                         bothWfc1=a["predictions"][key]["ifWfc1"]/b["predictions"][key]["ifWfc1"]-1)
                for key in ("gaia","calspecSameGrid","calspecFull")}
    observed={str(r):a["apertures"][str(r)]["measured"]/b["apertures"][str(r)]["measured"]-1
              for r in plan["radii"]}
    anchor=history["ratios"]["F658N/F660N"]
    report=dict(schema="BKL046_GD71_9020_CHIP_THROUGHPUT_RESULT_V1",protocolSha256=PIN,
                visits=measurements,chipAndEpochPredictedRatioDifference=difference,
                observedVisitRatioDifference=observed,
                program10054Reference=dict(observed3px=anchor["observedApertureRate"],
                  gaia=anchor["gaiaFullGridRate"],calspec=anchor["calspecFullRate"]),
                separateReadoutApertureCteEffectEstablished=False,scientificClosures=0,nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as output:
        json.dump(report,output,indent=2,sort_keys=True,allow_nan=False)
        output.write("\n")


if __name__=="__main__":
    main()
