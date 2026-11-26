"""Check exact FLC endpoint availability for the public FLT roots of the selected associations."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


def need(ok,why):
    if not ok:
        raise ValueError(why)


def main():
    root=Path(sys.argv[1])
    capture=(root/"acquisizione.json").read_bytes()
    a=json.loads(capture)
    need(len(a["records"])==9 and not any(r["entries"] for r in a["records"]),"Association result changed")
    tasks=[]
    for r in a["records"]:
        path=root/"source"/(r["observation"]+"-products.json")
        raw=path.read_bytes()
        need(sha256(raw).hexdigest()==r["productsSha256"],"Catalog product response changed")
        for item in json.loads(raw)["data"]:
            flt=item["productFilename"]
            if (item["project"],item["productType"],item["productSubGroupDescription"],item["dataRights"])!=(
                    "CALWF3","SCIENCE","FLT","PUBLIC") or not re.fullmatch(r"i[a-z0-9]{7}q_flt[.]fits",flt):
                continue
            need(flt.startswith(r["visit"]) and item["filters"]==r["band"]
                 and item["dataURI"]=="mast:HST/product/"+flt,"FLT identity changed")
            tasks.append(dict(flt=flt,flc=flt.replace("_flt.","_flc."),band=r["band"],visit=r["visit"],
                              target=r["target"],association=r["observation"]))
    need(len(tasks)==len({t["flt"] for t in tasks})==21,"Public FLT roster differs")

    def request(task):
        url="https://mast.stsci.edu/api/v0.1/Download/file?"+urlencode({"uri":"mast:HST/product/"+task["flc"]})
        try:
            with urlopen(url,timeout=25) as f:
                result=dict(httpStatus=f.status, startsWithFitsHeader=f.read(10)==b"SIMPLE  =",
                            mediaType=f.headers.get_content_type())
        except HTTPError as e:
            need(e.code==404,f"Unexpected archive status: {task['flc']}")
            payload=e.read(4096)
            result=dict(httpStatus=e.code, startsWithFitsHeader=False, responseSha256=sha256(payload).hexdigest())
        return dict(task,request=url,result=result)

    with ThreadPoolExecutor(max_workers=6) as pool:
        rows=list(pool.map(request,sorted(tasks,key=lambda t:t["flt"])))
    result=dict(schema="BKL046_EXTERNAL_WFC3_FLT_ROOT_FLC_LOOKUP_V1",sourceCaptureSha256=sha256(capture).hexdigest(),
                programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows,
                verifiedAvailable=sum(r["result"]["startsWithFitsHeader"] for r in rows),
                notFound=sum(r["result"]["httpStatus"]==404 for r in rows),
                scientificClosures=0,nativeExecutions=0)
    with (root/"riscontro-endpoint.json").open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True)
        f.write("\n")
    print(json.dumps({k:result[k] for k in ("verifiedAvailable","notFound")},sort_keys=True))


if __name__=="__main__":
    main()