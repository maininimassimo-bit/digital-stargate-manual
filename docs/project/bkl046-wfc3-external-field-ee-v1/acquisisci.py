"""Acquire six exact WFC3 calibration exposures for the independent-field test."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.parse import urlencode

PIN = "3e7df34612344d0c3b851191724b6d258c1c99c319b635c1c5e50af9477175e9"


def digest(raw):
    return sha256(raw).hexdigest()


def need(ok, message):
    if not ok:
        raise ValueError(message)


def save(path, data):
    if path.exists():
        need(path.read_bytes() == data, f"Stored file changed: {path.name}")
    else:
        with path.open("xb") as f:
            f.write(data)


def fetch(uri):
    for attempt in range(3):
        try:
            with urlopen(uri, timeout=45) as response:
                need(response.status == 200, "Unexpected archive response")
                data = response.read(268435457)
            need(0 < len(data) <= 268435456 and data.startswith(b"SIMPLE  =") and len(data) % 2880 == 0,
                 "Unexpected FITS container")
            return data
        except (HTTPError, URLError, TimeoutError) as exc:
            if isinstance(exc, HTTPError) and exc.code == 404:
                return None
            if attempt == 2 or isinstance(exc, HTTPError) and exc.code not in (408,429,500,502,503,504):
                raise
            time.sleep(attempt+1)


def main():
    root=Path(sys.argv[1])
    spec=(root/"protocollo.json").read_bytes()
    need(digest(spec)==PIN,"Frozen protocol differs")
    p=json.loads(spec)
    catalog=(root/"catalogo.json").read_bytes()
    need(digest(catalog)==p["catalogSha256"],"Frozen catalog differs")
    todo=[r for v in p["selected"] for r in v["rows"]]
    need(len(todo)==len({r["obs_id"] for r in todo})==6,"Frozen rows differ")

    def acquire(row):
        obs=row["obs_id"]
        need(row["dataRights"]=="PUBLIC" and row["target_name"] in ("47TUC","OMEGA-CEN")
             and row["proposal_id"]=="11452" and re.fullmatch(r"i[a-z0-9]{7}q",obs),"Unexpected catalog source")
        name=obs+"_flc.fits"
        uri="mast:HST/product/"+name
        request=dict(method="GET",url="https://mast.stsci.edu/api/v0.1/Download/file?"+urlencode({"uri":uri}))
        q=(json.dumps(request,sort_keys=True)+"\n").encode()
        base=root/"source"
        save(base/(obs+"-query.json"),q)
        path=base/name
        raw=path.read_bytes() if path.exists() else fetch(request["url"])
        if raw is None:
            response=dict(httpStatus=404,receivedFITS=False)
            entries=[]
        else:
            need(raw.startswith(b"SIMPLE  =") and len(raw)%2880==0,"Stored FITS container differs")
            save(path,raw)
            response=dict(httpStatus=200,receivedFITS=True,bytes=len(raw),sha256=digest(raw))
            entries=[dict(file=name,uri=uri,bytes=len(raw),sha256=digest(raw))]
        result=(json.dumps(response,sort_keys=True)+"\n").encode()
        save(base/(obs+"-products.json"),result)
        return dict(observation=obs,visit=obs[:6],band=row["filters"],obsid=str(row["obsid"]),
                    proposal=11452,target=row["target_name"],targetAlias=row["target_name"],entries=entries,
                    querySha256=digest(q),productsSha256=digest(result))

    with ThreadPoolExecutor(max_workers=4) as workers:
        records=[]
        for count, result in enumerate(workers.map(acquire,sorted(todo,key=lambda r:r["obs_id"])),1):
            records.append(result)
            print(f"{count}/{len(todo)} exact roots checked",flush=True)
    archive=dict(schema="BKL046_WFC3_CLUSTER_DIRECT_CAPTURE_V1",protocolSha256=PIN,
                 programSha256=digest(Path(__file__).read_bytes()),records=records)
    save(root/"acquisizione.json",(json.dumps(archive,sort_keys=True,indent=2)+"\n").encode())
    print(json.dumps(dict(catalog=len(records),acquired=sum(bool(r["entries"]) for r in records))))


if __name__=="__main__":
    main()