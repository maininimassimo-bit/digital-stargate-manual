"""Recover the official association membership for four GD153 visits in HST 12334 and 14021."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

root=Path(sys.argv[1])
catalog=(root/"observations.json").read_bytes()
rows=[row for row in json.loads(catalog)["data"]
      if row["proposal_id"] in ("12334","14021") and re.fullmatch("(?:ibnx(?:02|14)|icrw0[67])[a-z0-9]{2}0",row["obs_id"])]
if len(rows)!=12 or len({row["obs_id"][:6] for row in rows})!=4:
    raise ValueError("Expected four historical triplets")
source=root/"source"

def get(endpoint,limit,data=None):
    with urlopen(endpoint,data=data,timeout=25) as response:
        if response.status!=200:
            raise ValueError("MAST status")
        raw=response.read(limit+1)
    if not 0<len(raw)<=limit:
        raise ValueError("Unexpected MAST size")
    return raw

def write(path,raw):
    with path.open("xb") as out:
        out.write(raw)
    return sha256(raw).hexdigest()

def association(row):
    obs=row["obs_id"]
    request=dict(service="Mast.Caom.Products",params=dict(obsid=str(row["obsid"])),
                 page=1,pagesize=1000,format="json")
    q=json.dumps(request,sort_keys=True,separators=(",",":")).encode()
    request_path=source/(obs+"-query.json")
    if request_path.exists():
        if request_path.read_bytes()!=q: raise ValueError("Stored request changed")
        request_pin=sha256(q).hexdigest()
    else:
        request_pin=write(request_path,q)
    response_path=source/(obs+"-products.json")
    if response_path.exists():
        raw=response_path.read_bytes()
        response_pin=sha256(raw).hexdigest()
    else:
        raw=get("https://mast.stsci.edu/api/v0/invoke",2*1024**2,urlencode({"request":q}).encode())
        response_pin=write(response_path,raw)
    response=json.loads(raw)
    if response["status"]!="COMPLETE":
        raise ValueError("Incomplete association results")
    products=[p for p in response["data"]
              if p["productSubGroupDescription"]=="FLC" and p["productType"]=="SCIENCE"
              and p["project"]=="CALWF3" and p["dataRights"]=="PUBLIC"]
    if len({p["productFilename"] for p in products})!=len(products):
        raise ValueError("Expected distinct exposures in "+obs)
    selected=[]
    for p in products:
        filename=p["productFilename"]
        if not re.fullmatch("i[a-z0-9]{8}_flc[.]fits",filename.lower()) or not filename.lower().startswith(obs[:6]) or \
           p["dataURI"]!="mast:HST/product/"+filename or p["filters"]!=row["filters"]:
            raise ValueError("Product/association identity")
        # Download and verify only members selected before opening FITS headers.
        uri="https://mast.stsci.edu/api/v0.1/Download/file?"+urlencode({"uri":p["dataURI"]})
        destination=source/filename
        prior=destination.exists()
        blob=destination.read_bytes() if prior else get(uri,80*1024**2)
        if not blob.startswith(b"SIMPLE  =") or len(blob)%2880:
            raise ValueError("Incomplete FITS container")
        selected.append(dict(file=filename,sha256=sha256(blob).hexdigest() if prior else write(destination,blob),bytes=len(blob),
                             proposal=int(row["proposal_id"]),association=obs,filter=row["filters"],visit=obs[:6],
                             mastObsId=p["obsID"],uri=p["dataURI"]))
    print(obs,len(selected),file=sys.stderr,flush=True)
    return dict(association=obs,filter=row["filters"],requestSha256=request_pin,
                responseSha256=response_pin,rows=selected)

with ThreadPoolExecutor(max_workers=5) as p:
    results=list(p.map(association,sorted(rows,key=lambda row:row["t_min"])))
allfiles=[p["file"] for row in results for p in row["rows"]]
if len(allfiles)!=len(set(allfiles)):
    raise ValueError("Association files overlap")
result=dict(schema="BKL046_GD153_EXTERNAL_STARE_CANDIDATES_CAPTURE_V1",catalogSha256=sha256(catalog).hexdigest(),associations=results)
write(root/"acquisizione.json",(json.dumps(result,sort_keys=True,indent=2)+"\n").encode())
print(len(results),len(allfiles))
