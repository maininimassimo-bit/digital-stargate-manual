from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

sys.path.append(sys.argv[1])
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
import astropy.units as u


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()


def checked(path, expected):
    if sha(path) != expected:
        raise ValueError(f"Hash changed: {path.name}")
    return path


def cut(image,x,y,radius):
    result = image[y-radius:y+radius+1,x-radius:x+radius+1]
    if result.shape != (2*radius+1,)*2:
        raise ValueError("Incomplete image stamp")
    return result


def study(path, exposure, target, pam, cfg):
    with fits.open(path,memmap=False) as h:
        p = h[0].header
        sci = h["SCI"]
        q = sci.header
        if (p["ROOTNAME"],p["PROPOSID"],p["CCDAMP"],p["APERTURE"],q["CCDCHIP"],q["BUNIT"]) != (
            exposure["obsId"],10054,"B","WFC1-1K",1,"ELECTRONS"):
            raise ValueError("Wrong instrument setup")
        if exposure["band"] not in (p["FILTER1"],p["FILTER2"]) or p["EXPTIME"] != exposure["expSeconds"]:
            raise ValueError("Band or timing changed")
        wcs = WCS(q,h).celestial
        px,py = (int(round(float(v))) for v in wcs.world_to_pixel(target))
        sr = cfg["centroidSearchPx"]
        search = cut(sci.data,px,py,sr)
        yy,xx = np.unravel_index(search.argmax(),search.shape)
        cx,cy = int(px-sr+xx),int(py-sr+yy)
        separation = float(wcs.pixel_to_world(cx,cy).separation(target).arcsec)
        if separation > cfg["maximumAstrometricSeparationArcsec"]:
            raise ValueError("Peak does not match target")
        dx,dy = (-int(q[key]) for key in ("LTV1","LTV2"))
        r = cfg["skyPx"][1]
        area = cut(pam,cx+dx,cy+dy,r)
        stamp = cut(sci.data,cx,cy,r).astype(float)*area
        quality = cut(h["DQ"].data,cx,cy,r).astype(int)
        valid = np.isin(quality,cfg["allowedDQ"]) & np.isfinite(stamp)
        photflam = float(q.get("PHOTFLAM",p.get("PHOTFLAM",0)))
        if not np.isfinite(photflam) or photflam <= 0:
            raise ValueError("PHOTFLAM missing")
        return {"obs":exposure["obsId"],"band":exposure["band"],"time":float(p["EXPTIME"]),
            "photflam":photflam,"centerXY":[cx,cy],"separationArcsec":separation,
            "centerDQ":int(quality[r,r]),"stamp":stamp,"quality":quality,"valid":valid}


def measurements(row,masks,distance,cfg):
    r = cfg["skyPx"][1]
    sky = row["valid"] & (distance >= cfg["skyPx"][0]) & (distance <= r)
    if sky.sum() < 150:
        raise ValueError("Insufficient background")
    level = float(np.median(row["stamp"][sky]))
    image = row["stamp"]-level
    quality = row["quality"]
    output = {k:v for k,v in row.items() if k not in ("stamp","quality","valid")}
    output["circles"] = {}
    geom_center = distance == 0
    for radius in cfg["radii"]:
        circle = distance <= radius
        fullwell = (quality & 256) != 0
        digital = (quality & 2048) != 0
        modes = {}
        for tag,mask in masks.items():
            keep = circle & (row["valid"] if mask is None else mask)
            if tag == "localPlusRecordedCenter":
                keep |= geom_center & (quality == 256)
            flux = float(image[keep].sum())/row["time"]
            if flux <= 0:
                raise ValueError("Nonpositive photometry")
            modes[tag] = {"pixels":int(keep.sum()),"rateEPerSec":flux,"fLambdaRecorded":flux*row["photflam"]}
        output["circles"][str(radius)] = {"geometricPixels":int(circle.sum()),
            "fullWellPixels":int((fullwell & circle).sum()),"adcPixels":int((digital & circle).sum()),
            "localOtherExcludedPixels":int((circle & ~row["valid"] & ~fullwell & ~digital).sum()),"modes":modes}
    return output


def main():
    root,pam_path,protocol,result = map(Path,sys.argv[2:])
    cfg = json.loads(protocol.read_bytes())
    prior = json.loads(checked(root/"riscontro.json",cfg["priorSha256"]).read_bytes())
    if len(prior["exposures"]) != 6:
        raise ValueError("Unexpected exposure roster")
    target = SkyCoord(*cfg["sourceRaDec"],unit="deg")
    pam = fits.getdata(checked(pam_path,cfg["pamSha256"]))
    data = [study(checked(root/(item["obsId"]+"_flt.fits"),item["sha256"]),item,target,pam,cfg)
            for item in prior["exposures"]]
    shared_mask = np.logical_and.reduce([row["valid"] for row in data])
    symmetric = np.logical_and.reduce([mask for turn in range(4) for mask in
                                      (np.rot90(shared_mask,turn),np.fliplr(np.rot90(shared_mask,turn)))])
    masks = {"localAllowed":None,"localPlusRecordedCenter":None,"sharedSymmetric":symmetric}
    coord = np.arange(-cfg["skyPx"][1],cfg["skyPx"][1]+1)
    distance = np.hypot(coord[:,None],coord)
    rows = [measurements(row,masks,distance,cfg) for row in data]
    summaries = {}
    for radius in cfg["radii"]:
        tag = str(radius)
        by_band = {}
        for mode in masks:
            gather = defaultdict(list)
            for row in rows:
                gather[row["band"]].append(row["circles"][tag]["modes"][mode]["fLambdaRecorded"])
            means = {band:float(np.mean(vals)) for band,vals in gather.items()}
            by_band[mode] = {"bandMeanFLambda":means,"f606wOverF660nRecorded":means["F606W"]/means["F660N"],
                             "f658nOverF660nRecorded":means["F658N"]/means["F660N"]}
        summaries[tag] = by_band
    payload = {"schema":cfg["schema"],"protocolSha256":sha(protocol),"rows":rows,"summaries":summaries,
               "channelTruthRecovered":False,"scientificClosures":0}
    with result.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(payload,indent=2,sort_keys=True,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
