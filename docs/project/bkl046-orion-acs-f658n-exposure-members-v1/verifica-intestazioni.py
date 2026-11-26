
from hashlib import sha256
import json
from pathlib import Path
import re
from sys import argv

directory, output = map(Path,argv[1:])


def read(name,sha):
    data=(directory/name).read_bytes()
    if sha256(data).hexdigest()!=sha:
        raise ValueError(f"Input changed: {name}")
    return data


def primary(data):
    if not data.startswith(b"SIMPLE  ="):
        raise ValueError("Source does not start with a FITS primary header")
    result={}
    for start in range(0,len(data)-80,80):
        card=data[start:start+80].decode("ascii")
        key=card[:8].strip()
        if key=="END":
            return result
        if card[8:10]=="= " and key not in result:
            value=card[10:].lstrip()
            result[key]=value.split("'")[1].strip() if value.startswith("'") else value.split("/",1)[0].strip()
    raise ValueError("Primary header does not end inside captured range")


cfg_raw=(directory/"protocollo-intestazioni.json").read_bytes()
cfg=json.loads(cfg_raw)
products=json.loads(read("mast-f658n-products-response.json",cfg["productResponseSha256"]))
request=json.loads(read("mast-f658n-products-request.json",cfg["productRequestSha256"]))
manifest=json.loads(read("fits-prefixes.json",cfg["prefixManifestSha256"]))
geometry=json.loads(read("riscontro.json",cfg["geometryReportSha256"]))
parents={x["productGroupId"]:x for x in geometry["meshBest"]["F658N"]["records"]}
if (products["status"]!="COMPLETE" or products["paging"]["pagesFiltered"]!=1 or
    set(map(int,request["params"]["obsid"].split(",")))!=parents.keys()):
    raise ValueError("Incomplete products for the geometric sample")
roster={r["productFilename"]:r for r in products["data"]
        if re.fullmatch(r"j[a-z0-9]{8}_flc\.fits",r["productFilename"])}
if len(manifest)!=len(roster) or set(roster)!={r["name"] for r in manifest}:
    raise ValueError("FLC roster changed")
results=[]
for item in sorted(manifest,key=lambda a:a["name"]):
    member=roster[item["name"]]
    blob=read("headers/"+item["name"]+".prefix",item["sha256"])
    if len(blob)!=65536 or member["parent_obsid"]!=item["parent"] or member["obs_id"]!=item["id"]:
        raise ValueError("FLC lineage or range changed")
    h=primary(blob)
    if (h["ROOTNAME"].lower()!=item["id"] or h["INSTRUME"]!="ACS" or h["DETECTOR"]!="WFC"
        or "F658N" not in (h["FILTER1"],h["FILTER2"]) or h["PROPOSID"]!=parents[item["parent"]]["proposal"]):
        raise ValueError("Physical header scope differs from catalog")
    results.append(dict(
        root=item["id"], association=parents[item["parent"]]["obsId"],
        f658nExposureSeconds=float(h["EXPTIME"]), gainElectronsPerAdu=float(h["CCDGAIN"]),
        otherFilter=h["FILTER2"] if h["FILTER1"]=="F658N" else h["FILTER1"],
        date=h["DATE-OBS"], startUtc=h["TIME-OBS"], expstartMjd=float(h["EXPSTART"]),
        aperture=h["APERTURE"], proposal=h["PROPOSID"], prefixSha256=item["sha256"],
        archiveUrl=item["s3Url"], objectEtag=item["etag"], dataBytes=item["contentBytes"]
    ))
summary={}
for parent in sorted(parents.values(),key=lambda a:a["seconds"]):
    members=[r for r in results if r["association"]==parent["obsId"]]
    total=sum(r["f658nExposureSeconds"] for r in members)
    if abs(total-parent["seconds"])>1e-6:
        raise ValueError("Member durations do not sum to the catalog duration")
    summary[parent["obsId"]]=dict(catalogSeconds=parent["seconds"],
                                  memberSeconds=sorted(r["f658nExposureSeconds"] for r in members),
                                  gains=sorted({r["gainElectronsPerAdu"] for r in members}),
                                  dates=sorted({r["date"] for r in members}))
report=dict(schema=cfg["schema"],protocolSha256=sha256(cfg_raw).hexdigest(),
            geometryPoint=geometry["meshBest"]["F658N"]["raDec"],groups=summary,members=results,
            commonSkyFootprintsOnly=True,pixelSupportVerified=False,nativeExecutions=0,scientificClosures=0)
with output.open("x",encoding="utf-8",newline="\n") as f:
    f.write(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(json.dumps(summary))
