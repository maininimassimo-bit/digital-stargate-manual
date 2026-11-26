
import hashlib
import json
from pathlib import Path
import re
from sys import argv

directory, report = map(Path,argv[1:])


def read(name, expected=None):
    data=(directory/name).read_bytes()
    digest=hashlib.sha256(data).hexdigest()
    if expected is not None and digest!=expected:
        raise ValueError(f"Input changed: {name}")
    return json.loads(data),digest


def polygons(stcs):
    if not stcs.startswith("POLYGON "):
        return []
    result = []
    for block in stcs.split("POLYGON ")[1:]:
        fields=[float(x) for x in block.split()]
        if len(fields)<6 or len(fields)%2:
            raise ValueError("Invalid footprint")
        result.append(list(zip(fields[::2],fields[1::2],strict=True)))
    return result


def contains(polygon,x,y):
    previous=polygon[-1]
    inside=False
    for current in polygon:
        xa,ya=previous
        xb,yb=current
        if (ya>y)!=(yb>y) and x<xa+(xb-xa)*(y-ya)/(yb-ya):
            inside=not inside
        previous=current
    return inside


def at(rows,point):
    by_filter={}
    for item,footprint in rows:
        if not any(contains(p,*point) for p in footprint):
            continue
        by_filter.setdefault(item["filter"],[]).append(item)
    return {k:sorted(v,key=lambda a:(a["seconds"],a["obsId"])) for k,v in sorted(by_filter.items())}


cfg,pin=read("protocollo.json")
m,query_pin=read("mast-box-request.json",cfg["requestSha256"])
raw,sha=read("mast-box-response.json",cfg["responseSha256"])
if raw["status"]!="COMPLETE" or raw["paging"]["pagesFiltered"]!=1 or len(raw["data"])!=raw["paging"]["rowsFiltered"]:
    raise ValueError("Catalog response incomplete")
filterset=set(cfg["filters"])
rows=[]
excluded={}
for rec in sorted(raw["data"],key=lambda a:a["obs_id"]):
    if (not re.fullmatch(r"j[a-z0-9]{8}",rec["obs_id"]) or rec["intentType"]!="science"
        or rec["dataRights"]!="PUBLIC" or rec["filters"] not in filterset
        or not rec["t_exptime"] or rec["t_exptime"]<=0):
        continue
    footprint=polygons(rec["s_region"] or "")
    if not footprint:
        kind=(rec["s_region"] or "ABSENT").split()[0]
        excluded[kind]=excluded.get(kind,0)+1
        continue
    rows.append((dict(
        obsId=rec["obs_id"], productGroupId=rec["obsid"], seconds=rec["t_exptime"],
        filter=rec["filters"], proposal=rec["proposal_id"], scienceUri=rec["dataURL"],
        associationLike=bool(re.search(r"[0-9]{3}$",rec["obs_id"])),
    ),footprint))

best={}
for iy in range(-cfg["meshHalfSteps"],cfg["meshHalfSteps"]+1):
    for ix in range(-cfg["meshHalfSteps"],cfg["meshHalfSteps"]+1):
        x,y=(round(v+n*cfg["meshStepDegrees"],8) for v,n in zip(cfg["probeRaDec"],(ix,iy),strict=True))
        nearby=at(rows,(x,y))
        for filt,obs in nearby.items():
            exposure=sorted({o["seconds"] for o in obs})
            rank=(len(exposure),exposure[-1]/exposure[0],-(ix*ix+iy*iy))
            if filt not in best or rank>best[filt][0]:
                best[filt]=(rank,dict(raDec=[x,y],records=obs,distinctCatalogSeconds=exposure))
out=dict(schema=cfg["schema"],protocolSha256=pin,querySha256=query_pin,responseSha256=sha,
         screeningModel="planar point-in-polygon at catalog resolution; observation times may be totals of associations",
         catalogRows=len(raw["data"]),screenedRows=len(rows),footprintKindsExcluded=excluded,
         point=dict(raDec=cfg["probeRaDec"],records=at(rows,cfg["probeRaDec"])),
         meshBest={f:entry[1] for f,entry in sorted(best.items())},
         nativeExecutions=0,scientificClosures=0)
with report.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(out,indent=2,sort_keys=True)+"\n")
for filt,item in out["meshBest"].items():
    print(filt,item["raDec"],item["distinctCatalogSeconds"],
          [(u["obsId"],u["proposal"]) for u in item["records"]])
