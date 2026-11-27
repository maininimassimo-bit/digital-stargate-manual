"""Repeat the pinned GRW70 WFC3 aperture screen with an independent Gaia position."""
import argparse
import csv
from hashlib import sha256
from io import BytesIO, StringIO
from itertools import combinations
import json
from math import log10
from pathlib import Path
import sys
import warnings

PIN = "c65547e5ac7f9379a1f4247dc13b3ca7608e51f97c6f81dcadef985f8ecbc938"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path, pin):
    blob = path.read_bytes()
    need(sha256(blob).hexdigest() == pin, f"Input changed: {path.name}")
    return blob


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for arg in ("root", "original", "dependencies", "report"):
        cli.add_argument(arg, type=Path)
    args = cli.parse_args()
    root, origin = args.root, args.original
    p = json.loads(read(root / "protocollo.json", PIN))
    read(root/"gaia.adql", p["gaiaAdql"])
    candidates = list(csv.DictReader(StringIO(read(root/"gaia.csv", p["gaiaCsv"]).decode())))
    cohort = json.loads(read(origin/"protocollo.json", p["legacyProtocol"]))
    acquisition = json.loads(read(origin/"acquisizione.json", p["legacyAcquisition"]))
    prior = json.loads(read(origin/"riscontro.json", p["legacyReport"]))
    code = read(origin/"misura.py", p["legacyMeasure"])
    scope = {"__name__":"verified_measure", "__file__":str(origin/"misura.py")}
    exec(compile(code, str(origin/"misura.py"), "exec"), scope)
    measure = scope["measure"]

    sys.path.insert(0, str(args.dependencies))
    import astropy
    import astropy.units as u
    from astropy.coordinates import CartesianRepresentation, Distance, ICRS, SkyCoord, get_body_barycentric
    from astropy.io import fits
    from astropy.time import Time
    from astropy.wcs import FITSFixedWarning, WCS
    import numpy as np

    warnings.filterwarnings("ignore", category=FITSFixedWarning)
    need((np.__version__, astropy.__version__) == ("2.3.5", "7.2.0"), "Dependencies differ")
    optics = {int(chip): fits.getdata(BytesIO(read(origin/f"UVIS{chip}wfc3_map.fits", pin)))
              for chip,pin in cohort["pam"].items()}
    standard = SkyCoord(*p["calspecJ2000HmsDms"], unit=(u.hourangle, u.deg), frame="icrs")

    def coordinate(g, rv):
        return SkyCoord(ra=float(g["ra"])*u.deg, dec=float(g["dec"])*u.deg,
                        distance=Distance(parallax=float(g["parallax"])*u.mas), pm_ra_cosdec=float(g["pmra"])*u.mas/u.yr,
                        pm_dec=float(g["pmdec"])*u.mas/u.yr, radial_velocity=rv*u.km/u.s,
                        obstime=Time(float(g["ref_epoch"]), format="jyear", scale="tcb"), frame="icrs")

    matches = []
    for g in candidates:
        if not (11 <= float(g["phot_g_mean_mag"]) <= 14 and g["astrometric_params_solved"] in ("31","95")):
            continue
        astro = coordinate(g, p["calspecRadialVelocityKms"])
        separation = float(astro.apply_space_motion(new_obstime=Time("J2000")).separation(standard).arcsec)
        if separation <= p["maxJ2000MatchArcsec"]:
            matches.append((g,astro,separation))
    (gaia, target, match_arcsec), = matches
    need(gaia["source_id"] == p["gaiaSource"], "Gaia cross-match changed")
    zero_rv = coordinate(gaia, 0)

    initial = {row["file"]:row for row in prior["rows"] if row["target"] == "GRW70"}
    files = [(r, entry) for r in acquisition["records"] if r["target"] == "GRW70" for entry in r["entries"]]
    need(len(files) == len(initial) == 12 and {item["file"] for _,item in files} == set(initial),
         "GRW70 exposure coverage differs")
    rows = []
    for r, item in files:
        name = item["file"]
        old = initial[name]
        with fits.open(BytesIO(read(origin/"source"/name, item["sha256"])), memmap=False) as h:
            hd = h[0].header
            sci, error, quality = (h[ext,1] for ext in ("SCI","ERR","DQ"))
            need(sci.header["CCDCHIP"] == old["chip"] and hd["TARGNAME"] == r["targetAlias"]
                 and (hd["SCAN_TYP"],hd["EXPFLAG"],hd["PCTECORR"],hd["FLUXCORR"]) ==
                 ("N","NORMAL","COMPLETE","COMPLETE"), "Exposure identity changed")
            epoch = Time((hd["EXPSTART"]+hd["EXPEND"])/2, format="mjd", scale="utc")
            at_epoch = target.apply_space_motion(new_obstime=epoch)
            bary = CartesianRepresentation(at_epoch.cartesian.xyz.to(u.au))
            earth = get_body_barycentric("earth",epoch)
            corrected = SkyCoord(ICRS(bary - earth))
            no_rv = zero_rv.apply_space_motion(new_obstime=epoch)
            alternative = SkyCoord(ICRS(CartesianRepresentation(no_rv.cartesian.xyz.to(u.au))-earth))
            wcs = WCS(sci.header,h).celestial
            arrays = sci.data.astype(float),error.data.astype(float),quality.data
            height,width = sci.data.shape
            nominal = dict(visit=old["visit"], band=old["band"], chip=old["chip"], dither=old["dither"],
                           exptimeSeconds=old["exptimeSeconds"], startMjd=old["startMjd"])
            variants = {}
            worlds = {"header": (hd["RA_TARG"],hd["DEC_TARG"]),
                      "gaiaBarycentric": (at_epoch.ra.deg, at_epoch.dec.deg),
                      "gaiaGeocentric": (corrected.ra.deg, corrected.dec.deg),
                      "gaiaGeocentricZeroVelocity": (alternative.ra.deg, alternative.dec.deg)}
            for key, world in worlds.items():
                seed = np.array(wcs.world_to_pixel_values(*world))
                need(np.isfinite(seed).all() and 28 <= seed[0] < width-28 and 28 <= seed[1] < height-28,
                     f"Predicted center outside aperture domain: {name}")
                result = dict(nominal, fluxCalibratedRadii={}, seedXY=seed.tolist(),
                              offsetFromHeaderSeedPx=float(np.linalg.norm(seed - np.array(old["seedXY"]))))
                result["state"] = measure(np,*arrays,optics[old["chip"]],seed,sci.header,cohort,result)
                variants[key] = result
            need(variants["header"]["state"] == old["state"]
                 and variants["header"].get("peakOffsetPx") == old.get("peakOffsetPx")
                 and variants["header"]["fluxCalibratedRadii"] == old["fluxCalibratedRadii"], "Header replay differs")
            rows.append(dict(file=name, visit=old["visit"], band=old["band"], originalState=old["state"], variants=variants,
                             parallaxShiftOnFramePx=float(np.linalg.norm(np.array(variants["gaiaBarycentric"]["seedXY"]) -
                                                                         np.array(variants["gaiaGeocentric"]["seedXY"]))),
                             zeroVelocityShiftOnFramePx=float(np.linalg.norm(np.array(variants["gaiaGeocentric"]["seedXY"]) -
                                                                           np.array(variants["gaiaGeocentricZeroVelocity"]["seedXY"])))))

    triplets = []
    for visit in sorted({r["visit"] for r in rows}):
        group = [r["variants"]["gaiaGeocentric"] for r in rows if r["visit"] == visit]
        need(len(group) == 3 and {r["band"] for r in group} == set(cohort["bands"]), "Incomplete visit grid")
        span = max(r["startMjd"] for r in group) - min(r["startMjd"] for r in group)
        entry = dict(visit=visit, spanDays=span, allAperturesQualified=False, qualifiedRadii={}, rawColorsMillimag={})
        triplets.append(entry)
        if len({(r["chip"],tuple(r["dither"])) for r in group}) != 1 or span > cohort["maxTripletSpanDays"]:
            continue
        for radius in map(str,cohort["apertureRadii"]):
            supported = [r for r in group if radius in r["fluxCalibratedRadii"]]
            entry["qualifiedRadii"][radius] = len(supported)
            if len(supported) == 3:
                flux = {r["band"]:r["fluxCalibratedRadii"][radius] for r in supported}
                entry["rawColorsMillimag"][radius] = {f"{b}-{r}": -2500*log10(flux[b]/flux[r])
                                                       for b,r in combinations(cohort["bands"],2)}
        entry["allAperturesQualified"] = len(entry["rawColorsMillimag"]) == len(cohort["apertureRadii"])
    document = dict(schema=p["schema"]+"_RESULT", protocolSha256=PIN,
                    programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                    matchedSource=gaia["source_id"], matchAtJ2000Arcsec=match_arcsec, rows=rows, triplets=triplets,
                    scientificClosures=0, nativeExecutions=0, observerEarthCenter=True)
    with args.report.open("x", newline="\n", encoding="utf-8") as f:
        json.dump(document,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()