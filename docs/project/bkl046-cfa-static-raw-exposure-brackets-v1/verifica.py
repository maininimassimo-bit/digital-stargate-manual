import ast
from collections import defaultdict
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import struct
import sys
from zipfile import ZipFile

root,wheel,runtime,vc,out = map(Path,sys.argv[1:])
dlls=[os.add_dll_directory(str(runtime/"rawpy")),os.add_dll_directory(str(vc))]
sys.path.insert(0,str(runtime))
import numpy as np
import rawpy


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pinned(path,expected):
    data=path.read_bytes()
    require(sha(data)==expected,f"Changed input {path.name}")
    return data


def main():
    cfg_raw=(root/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_raw)
    with ZipFile(BytesIO(pinned(wheel,cfg["wheelSha256"]))) as package:
        for name in package.namelist():
            if name.startswith("rawpy/") and not name.endswith("/"):
                require((runtime/name).read_bytes()==package.read(name),"Unexpected wheel member")
    require((rawpy.__version__,rawpy.libraw_version,np.__version__)==("0.25.1",(0,21,4),"2.3.5"),"Wrong decoder version")
    reader=pinned(root/"lettore-exif.py",cfg["exifReaderSha256"])
    functions=[n for n in ast.parse(reader).body if isinstance(n,ast.FunctionDef) and n.name=="exif"]
    require(len(functions)==1,"Missing EXIF reader")
    ns={"require":require,"struct":struct}
    exec(compile(ast.Module(body=functions,type_ignores=[]),"pinned-exif","exec"),ns)
    capture=json.loads(pinned(root/"acquisizione.json",cfg["receiptSha256"]))
    require(len(capture["records"])==10,"Missing acquisition")
    grouped=defaultdict(list)
    for row in capture["records"]:
        blob=pinned(root/"originali"/row["file"],row["sha256"])
        meta=ns["exif"](blob)
        with rawpy.imread(BytesIO(blob)) as raw:
            samples=raw.raw_image_visible
            colors=raw.raw_colors_visible
            require(samples.ndim==2,"Not a CFA plane")
            h,w=(dim-dim%2 for dim in samples.shape)
            cells=np.zeros((h//2,w//2),dtype=np.uint8)
            labels,planes=[],[]
            per_channel=raw.camera_white_level_per_channel
            for phase,(y,x) in enumerate(((0,0),(0,1),(1,0),(1,1))):
                color=int(colors[y,x])
                labels.append(raw.color_desc[color:color+1].decode())
                require(np.all(colors[y::2,x::2]==color),"Nonperiodic visible mosaic")
                plane=samples[y:h:2,x:w:2]
                threshold=int(raw.white_level if per_channel is None else per_channel[color])
                black=int(raw.black_level_per_channel[color])
                require(0 <= black < threshold <= 65535,"Invalid declared levels")
                hit=plane>=threshold
                cells[hit] |= (1 << phase)
                histogram=np.bincount(plane.ravel(),minlength=65536)
                codes=np.flatnonzero(histogram)[-4:]
                planes.append({"white":threshold,"black":black,"sitesAtOrAbove":int(hit.sum()),
                               "maximumObserved":int(codes[-1]),
                               "upperCodes":[[int(v),int(histogram[v])] for v in codes[::-1]]})
            counts=np.bincount(cells.ravel(),minlength=16)
            grouped[row["scene"]].append({"file":row["file"],"model":meta["model"],"iso":meta["iso"],
                "exposureSeconds":meta["secondsNumerator"]/meta["secondsDenominator"],
                "shapeYX":list(samples.shape),"phase":"".join(labels),
                "cropYX":[raw.sizes.top_margin,raw.sizes.left_margin],
                "perChannelWhiteReported":per_channel is not None,"planes":planes,
                "partialPhaseCells":int(counts[1:15].sum()),"allPhaseCells":int(counts[15])})
    scenes={}
    for scene,items in grouped.items():
        items.sort(key=lambda row:row["exposureSeconds"])
        comparable=len({(row["model"],row["iso"],tuple(row["shapeYX"]),row["phase"],tuple(row["cropYX"])) for row in items})==1
        times=[row["exposureSeconds"] for row in items]
        scenes[scene]={"consistentCaptureAndGeometry":comparable,"uniqueExposureTimes":len(set(times)),
            "shortestHasNoThresholdHits":items[0]["partialPhaseCells"]==0 and items[0]["allPhaseCells"]==0,
            "longestHasPartialPhaseHits":items[-1]["partialPhaseCells"]>0,"rows":items}
    data={"schema":cfg["schema"],"protocolSha256":sha(cfg_raw),"scenes":scenes,
          "registrationVerified":False,"scientificClosures":0}
    with out.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
