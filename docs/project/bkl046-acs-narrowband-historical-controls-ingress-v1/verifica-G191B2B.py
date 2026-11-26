"""Acquire and verify the six G191B2B HST ACS exposure products identified by CADC."""
from concurrent.futures import ThreadPoolExecutor
import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

target, catalog, dependencies, mode = sys.argv[1:]
target, catalog = map(Path,(target,catalog))
sys.path.insert(0,dependencies)
import numpy as np
from astropy.io import fits

PLAN_IDS = {
    "j8v604xdq":"F606W","j8v604xeq":"F606W",
    "j8v604xhq":"F658N","j8v604xiq":"F658N",
    "j8v604xkq":"F660N","j8v604xlq":"F660N",
}


def require(ok, label):
    if not ok:
        raise ValueError(label)


def check(item):
    obs,band=item
    leaf=obs+"_flt.fits"
    path=target/leaf
    url="https://mast.stsci.edu/api/v0.1/Download/file?"+urlencode({"uri":"mast:HST/product/"+leaf})
    if mode=="fetch":
        with urlopen(url,timeout=20) as stream:
            require(stream.status==200,"MAST HTTP error")
            raw=stream.read(24000001)
    else:
        raw=path.read_bytes()
    require(28800<len(raw)<=24000000 and len(raw)%2880==0,"Unexpected container size")
    with fits.open(BytesIO(raw),memmap=False) as hdus:
        hdus.verify("exception")
        h=hdus[0].header
        sci=hdus["SCI",1]
        ht=sci.header
        require((h["ROOTNAME"].lower(),h["TARGNAME"].upper().replace(" ",""),int(h["PROPOSID"]),h["DETECTOR"])
                ==(obs,"G191B2B",10054,"WFC") and band in (h["FILTER1"],h["FILTER2"]),
                "Exposure source or optical identity differs")
        dq=hdus["DQ",1].data
        require(sci.data.shape==dq.shape==hdus["ERR",1].data.shape,"Plane dimensions disagree")
        audit=dict(source="G191B2B",obsId=obs,band=band,aperture=h["APERTURE"],amp=h["CCDAMP"],
                   pctecorr=h["PCTECORR"],chip=int(ht["CCDCHIP"]),expSeconds=float(h["EXPTIME"]),
                   expStartMjd=float(h["EXPSTART"]),lTv=[float(ht[key]) for key in ("LTV1","LTV2")],
                   exposureFlag=h["EXPFLAG"],planeShape=list(dq.shape),
                   saturatedFlags=int(np.count_nonzero(dq&256)),sha256=sha256(raw).hexdigest(),
                   bytes=len(raw),url=url)
    if mode=="fetch":
        with path.open("xb") as f:f.write(raw)
    return audit


raw=catalog.read_bytes()
listed={row["observationID"]:row["energy_bandpassName"] for row in csv.DictReader(raw.decode().splitlines())
        if row["target_name"]=="G191B2B" and re.fullmatch(r"j8v604[a-z0-9]{2}q",row["observationID"])}
require(listed==PLAN_IDS,"Pinned CADC candidate roster differs")
with ThreadPoolExecutor(6) as pool:
    exposures=list(pool.map(check,PLAN_IDS.items()))
print(json.dumps(dict(schema="BKL046_ACS_G191B2B_10054_EXPOSURE_INGRESS_V1",acquiredImages=len(exposures),
                      catalogueSha256=sha256(raw).hexdigest(),exposures=exposures,
                      postSM4TransferNominallyApplicable=False,
                      photometricComparisons=0,scientificClosures=0),indent=2,sort_keys=True))
