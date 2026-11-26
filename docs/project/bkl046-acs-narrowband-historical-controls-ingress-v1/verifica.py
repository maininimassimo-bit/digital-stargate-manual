"""Verify complete ACS 9020 files against the archived preflight headers."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

root, deps, mode = sys.argv[1:]
root = Path(root)
sys.path.insert(0,deps)
import numpy as np
from astropy.io import fits


def require(ok, why):
    if not ok:
        raise ValueError(why)


def check(row):
    name = row["obsId"] + "_flt.fits"
    path = root/name
    expected = int(row["contentRange"].rsplit("/",1)[1])
    url = "https://mast.stsci.edu/api/v0.1/Download/file?" + urlencode({"uri":"mast:HST/product/"+name})
    if mode == "fetch" and not path.exists():
        with urlopen(url,timeout=18) as source:
            require(source.status == 200,"MAST response failed")
            raw = source.read(expected+1)
    else:
        raw = path.read_bytes()
    require(len(raw)==expected, "FITS length differs")
    prefix = (root/(row["obsId"]+"-headers.bin")).read_bytes()
    require(raw.startswith(prefix) and sha256(prefix).hexdigest()==row["headersSha256"],"FITS headers differ")
    with fits.open(BytesIO(raw),memmap=False) as hdus:
        hdus.verify("exception")
        h = hdus[0].header
        sci, err, dq = (hdus[key,1].data for key in ("SCI","ERR","DQ"))
        require(list(sci.shape)==row["imageShape"] and sci.shape==err.shape==dq.shape
                and h["TARGNAME"].upper()=="GD71" and h["PROPOSID"]==9020
                and row["band"] in (h["FILTER1"],h["FILTER2"]),"FITS exposure differs")
        result = dict(obsId=row["obsId"], visit=row["visit"], band=row["band"],
                      amp=row["amp"], aperture=row["aperture"], chip=row["detectorChip"],
                      expStartMjd=row["mjd"], exposureSeconds=row["expSeconds"],
                      pctecorr=row["pctecorr"], totalSaturatedFlags=int(np.count_nonzero(dq&256)),
                      bytes=len(raw),sha256=sha256(raw).hexdigest(),url=url)
    if mode == "fetch" and not path.exists():
        with path.open("xb") as destination:
            destination.write(raw)
    return result


metadata=(root/"pose-9020.json").read_bytes()
catalogue = json.loads((root/"censimento.json").read_bytes())
for item in catalogue["results"]:
    require(item["status"]=="OK","Catalogue query failed")
    for extension, field in (("adql","querySha256"),("csv","sha256")):
        source=root/(item["target"]+"."+extension)
        require(sha256(source.read_bytes()).hexdigest()==item[field],"Catalogue receipt differs")
rows=json.loads(metadata)
require(len(rows)==8 and all(x["status"]=="VERIFIED_HEADER" for x in rows),"Headers incomplete")
with ThreadPoolExecutor(4) as pool:
    data=list(pool.map(check,rows))
require({(row["visit"],row["chip"],row["amp"]) for row in data} ==
        {("j8c103",1,"A"),("j8c104",2,"C")},"Unexpected instrument configuration")
print(json.dumps(dict(schema="BKL046_ACS_GD71_9020_ARCHIVAL_INPUTS_V1",exposures=data,
                      queryReceiptSha256=sha256((root/"censimento.json").read_bytes()).hexdigest(),
                      preflightSha256=sha256(metadata).hexdigest(),fitCount=len(data),
                      isolatesCte=False,scientificClosures=0),indent=2,sort_keys=True,allow_nan=False))
