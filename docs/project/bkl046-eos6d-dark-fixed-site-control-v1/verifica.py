import ast
from collections import Counter
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import struct
import sys
from zipfile import ZipFile

root, prior, decoder, vc, output = map(Path,sys.argv[1:])
dlls = [os.add_dll_directory(str(decoder/"rawpy")),os.add_dll_directory(str(vc))]
sys.path.insert(0,str(decoder))
import numpy as np
import rawpy


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verified(file,expected):
    blob=file.read_bytes()
    if sha(blob)!=expected:
        raise ValueError(f"Hash changed: {file.name}")
    return blob


def require(condition,message):
    if not condition:
        raise ValueError(message)


def main():
    protocol=(root/"protocollo.json").read_bytes()
    cfg=json.loads(protocol)
    require((rawpy.__version__,rawpy.libraw_version,np.__version__)==("0.25.1",(0,21,4),"2.3.5"),"Decoder changed")
    old=json.loads(verified(prior/"protocollo.json",cfg["beforeProtocol"]))
    report=json.loads(verified(prior/"riscontro.json",cfg["beforeReport"]))
    wheel=prior/"rawpy-0.25.1-cp312-cp312-win_amd64.whl"
    with ZipFile(BytesIO(verified(wheel,old["rawpyWheelSha256"]))) as bundle:
        for member in bundle.namelist():
            if member.startswith("rawpy/") and not member.endswith("/"):
                require((decoder/member).read_bytes()==bundle.read(member),"Decoder binary changed")
    pin = json.loads(verified(root/"dark"/"acquisizione.json",cfg["darkReceiptSha256"]))
    require(pin["darkEntries"]==25 and len(pin["samples"])==3, "Dark cohort changed")
    code=verified(prior/"lettore-exif.py",old["exifSourceSha256"])
    functions=[n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef) and n.name=="exif"]
    require(len(functions)==1,"Missing EXIF reader")
    ns={"require":require,"struct":struct}
    exec(compile(ast.Module(body=functions,type_ignores=[]),"pinned-exif","exec"),ns)
    groups={"light":[(prior/"input"/r["file"],r["sha256"]) for r in old["inputs"] if r["camera"]=="EOS6D"],
            "dark":[(root/"dark"/r["file"],r["sha256"]) for r in pin["samples"]]}
    rows, measured = {}, {}
    for group, items in groups.items():
        measured[group]=[]
        rows[group]=[]
        for path,digest in items:
            raw=verified(path,digest)
            capture=ns["exif"](raw)
            require(capture["model"]=="Canon EOS 6D", "Wrong camera")
            with rawpy.imread(BytesIO(raw)) as camera:
                pix=camera.raw_image_visible
                cmap=camera.raw_colors_visible
                require(tuple(pix.shape)==(3670,5496) and
                    (camera.sizes.top_margin,camera.sizes.left_margin)==(38,72),"Sensor geometry changed")
                require(camera.camera_white_level_per_channel==[12507]*4,"Code limits changed")
                phases=[pix[y::2,x::2].copy() for y,x in ((0,0),(0,1),(1,0),(1,1))]
                labels="".join(camera.color_desc[int(cmap[y,x]):int(cmap[y,x])+1].decode() 
                               for y,x in ((0,0),(0,1),(1,0),(1,1)))
                require(labels=="RGGB","Unexpected visible phase")
            measured[group].append(phases)
            rows[group].append({"file":path.name,"iso":capture["iso"],"seconds":
                capture["secondsNumerator"]/capture["secondsDenominator"],"maximumRaw":[int(p.max()) for p in phases]})
    matched=[i for i,d in enumerate(rows["dark"]) if
             all(d["iso"]==item["iso"] and d["seconds"]==item["seconds"] for item in rows["light"])]
    summary=[]
    recurring_masks=[]
    for i, label in enumerate(("R","G1","G2","B")):
        light=np.stack([pieces[i] for pieces in measured["light"]])
        dark=np.stack([pieces[i] for pieces in measured["dark"]])
        hit = light >= cfg["whiteMetadataDN"]
        recurring = np.all(hit,axis=0)
        recurring_masks.append(recurring)
        dark_hit = dark >= cfg["whiteMetadataDN"]
        plateau = np.all(np.isin(light,cfg["plateauCodes"]),axis=0)
        tests=[]
        for j,item in enumerate(dark):
            top=float(np.quantile(item,cfg["darkTailPercentile"],method="higher"))
            vals=item[recurring]
            tests.append({"dark":rows["dark"][j]["file"],"tailThresholdDN":top,
                "allDarkAtWhite":int(dark_hit[j].sum()),
                "recurrentLightSitesAtWhiteInDark":int(dark_hit[j][recurring].sum()),
                "recurrentLightSitesAtDarkTail":int((vals>=top).sum()),
                "recurrentLightSiteDarkMaxDN":int(vals.max()) if len(vals) else None})
        summary.append({"phase":label,"lightHitInAllAtWhite":int(recurring.sum()),
            "lightHitInAllAtPlateau":int(plateau.sum()),"dark":tests,
            "darkAtWhiteInAllAndLightAtWhiteInAll":int((np.all(dark_hit,axis=0)&recurring).sum())})
    if int(np.logical_or.reduce(recurring_masks).sum()) != report["groups"]["EOS6D/light"]["samePhaseRecurringInAllCells"]:
        raise ValueError("Recurring-pixel coverage mismatch")
    data={"schema":cfg["schema"],"protocolSha256":sha(protocol),"capture":rows,"phases":summary,
          "matchedDarkFiles":[rows["dark"][i]["file"] for i in matched],
          "temperatureVerified":False,"scientificClosures":0}
    with output.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
