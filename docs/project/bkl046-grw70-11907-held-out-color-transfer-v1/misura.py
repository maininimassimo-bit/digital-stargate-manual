"""Measure a disjoint set of GRW70 FLC exposures under the frozen Gaia aperture rules."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
from io import BytesIO, StringIO
from itertools import combinations
import json
from math import log10
from pathlib import Path
import sys
import warnings

PIN = "dc50e15a65edb68b78356a6c85ab818ec689387d81cdb449ce08f4eb12ab963f"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path, pin):
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == pin, f"Input differs: {path.name}")
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("root", "original", "dependencies", "report"):
        parser.add_argument(name, type=Path)
    parser.add_argument("capture_sha256")
    args = parser.parse_args()
    root, origin = args.root, args.original
    p = json.loads(read(root/"protocollo.json", PIN))
    parent = json.loads(read(origin/"protocollo.json", p["cohortProtocolSha256"]))
    lineage = json.loads(read(root/"acquisizione.json", args.capture_sha256))
    need(lineage["protocolSha256"] == PIN, "Capture protocol changed")
    read(root/"acquisisci.py", lineage["programSha256"])
    read(root/"catalogo.json", p["catalogSha256"])
    candidates = csv.DictReader(StringIO(read(root/"gaia.csv", p["gaiaCsvSha256"]).decode()))
    gaia, = [row for row in candidates if row["source_id"] == p["gaiaSource"]]
    helper = read(origin/"misura.py", p["measureSha256"])
    namespace = {"__name__":"verified_helper"}
    exec(compile(helper,str(origin/"misura.py"),"exec"), namespace)
    measure = namespace["measure"]

    sys.path.insert(0,str(args.dependencies))
    import numpy as np
    import astropy
    import astropy.units as u
    from astropy.coordinates import CartesianRepresentation, Distance, ICRS, SkyCoord, get_body_barycentric
    from astropy.io import fits
    from astropy.time import Time
    from astropy.wcs import WCS, FITSFixedWarning

    warnings.filterwarnings("ignore", category=FITSFixedWarning)
    need((np.__version__,astropy.__version__) == ("2.3.5","7.2.0"), "Runtime versions differ")
    target = SkyCoord(ra=float(gaia["ra"])*u.deg, dec=float(gaia["dec"])*u.deg,
                      distance=Distance(parallax=float(gaia["parallax"])*u.mas),
                      pm_ra_cosdec=float(gaia["pmra"])*u.mas/u.yr, pm_dec=float(gaia["pmdec"])*u.mas/u.yr,
                      radial_velocity=p["radialVelocityKms"]*u.km/u.s,
                      obstime=Time(float(gaia["ref_epoch"]),format="jyear",scale="tcb"),frame="icrs")
    pams = {int(chip):fits.getdata(BytesIO(read(root/f"UVIS{chip}wfc3_map.fits",pin)))
            for chip,pin in parent["pam"].items()}
    fixed = {r["obs_id"]:r for v in p["selected"] for r in v["rows"]}
    need(len(fixed) == len(lineage["records"]) == 126 and len(p["selected"]) == 42
         and set(fixed) == {r["observation"] for r in lineage["records"]}, "Frozen visit coverage differs")
    rows = []
    for record in lineage["records"]:
        obs = record["observation"]
        cat = fixed[obs]
        name = obs+"_flc.fits"
        folder = root / "source"
        read(folder/(obs+"-query.json"),record["querySha256"])
        read(folder/(obs+"-products.json"),record["productsSha256"])
        row = dict(file=name,visit=obs[:6],band=cat["filters"],state="NO_EXACT_PUBLIC_FLC",fluxCalibratedRadii={})
        rows.append(row)
        if not record["entries"]:
            continue
        entry, = record["entries"]
        need((entry["file"],record["visit"],record["band"],record["proposal"],record["targetAlias"]) ==
             (name,obs[:6],cat["filters"],int(cat["proposal_id"]),cat["target_name"]), "Catalog identity differs")
        raw = read(folder/name,entry["sha256"])
        need(len(raw) == entry["bytes"], "FLC length differs")
        with fits.open(BytesIO(raw),memmap=False) as h:
            header = h[0].header
            sci,error,quality = (h[key,1] for key in ("SCI","ERR","DQ"))
            need((header["ROOTNAME"].lower(),header["TARGNAME"],header["PROPOSID"],header["FILTER"]) ==
                 (obs,cat["target_name"],11907,cat["filters"]) and
                 abs(header["EXPSTART"]-cat["t_min"]) <= 1e-6, "Exposure identity differs")
            chip = sci.header["CCDCHIP"]
            row.update(chip=chip,startMjd=float(header["EXPSTART"]),exptimeSeconds=float(header["EXPTIME"]),
                       dither=[header["POSTARG1"],header["POSTARG2"]],flag=header["EXPFLAG"],scan=header["SCAN_TYP"])
            if (header["SCAN_TYP"],header["EXPFLAG"],header["PCTECORR"],header["FLUXCORR"]) != (
                    "N","NORMAL","COMPLETE","COMPLETE"):
                row["state"]="EXPOSURE_METADATA"
                continue
            need(sci.header["BUNIT"] == error.header["BUNIT"] == "ELECTRONS"
                 and sci.data.shape == error.data.shape == quality.data.shape, "FLC plane shape or units")
            epoch = Time((header["EXPSTART"]+header["EXPEND"])/2,format="mjd",scale="utc")
            body = target.apply_space_motion(new_obstime=epoch)
            vector = CartesianRepresentation(body.cartesian.xyz.to(u.au))
            geocenter = SkyCoord(ICRS(vector-get_body_barycentric("earth",epoch)))
            wcs = WCS(sci.header,h).celestial
            seed = np.array(wcs.world_to_pixel_values(geocenter.ra.deg,geocenter.dec.deg))
            height,width = sci.data.shape
            row["seedXY"]=seed.tolist()
            if not (np.isfinite(seed).all() and 28 <= seed[0] < width-28 and 28 <= seed[1] < height-28):
                row["state"]="GAIA_SEED_OUT_OF_BOUNDS"
                continue
            case = sci.data.astype(float),error.data.astype(float),quality.data
            row["state"]=measure(np,*case,pams[chip],seed,sci.header,parent,row)

    visits=[]
    for visit in sorted({row["visit"] for row in rows}):
        rr=[row for row in rows if row["visit"]==visit]
        need(len(rr)==3 and {row["band"] for row in rr}==set(parent["bands"]),"Triplet identity differs")
        result=dict(visit=visit,state="INELIGIBLE",colorMillimag={}, qualifiedRadii={})
        visits.append(result)
        if not all("startMjd" in r for r in rr):
            continue
        span=max(r["startMjd"] for r in rr)-min(r["startMjd"] for r in rr)
        result["spanDays"]=span
        geometry={(r["chip"],tuple(r["dither"])) for r in rr}
        if len(geometry)!=1 or span>parent["maxTripletSpanDays"]:
            continue
        (result["chip"],result["dither"]),=geometry
        for radius in map(str,parent["apertureRadii"]):
            flux={r["band"]:r["fluxCalibratedRadii"][radius] for r in rr if radius in r["fluxCalibratedRadii"]}
            result["qualifiedRadii"][radius]=len(flux)
            if len(flux)==3:
                result["colorMillimag"][radius]={f"{b}-{r}":-2500*log10(flux[b]/flux[r])
                                                  for b,r in combinations(parent["bands"],2)}
        if len(result["colorMillimag"])==2:
            result["state"]="BOTH_RADII"
            left,right=result["colorMillimag"]["5"],result["colorMillimag"]["10"]
            result["change10Minus5Millimag"]={c:right[c]-left[c] for c in left}
    report=dict(schema=p["schema"]+"_RESULT",protocolSha256=PIN,acquisitionSha256=args.capture_sha256,
                programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),counts=Counter(r["state"] for r in rows),
                rows=rows,visits=visits,allRadiiVisits=sum(v["state"]=="BOTH_RADII" for v in visits),
                nativeExecutions=0,scientificClosures=0)
    with args.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(report,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()