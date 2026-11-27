from collections import defaultdict
import ast
import struct
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

root, wheel, runtime, vc, output = map(Path, sys.argv[1:])
handles = [os.add_dll_directory(str(runtime/"rawpy")), os.add_dll_directory(str(vc))]
sys.path.insert(0,str(runtime))
import numpy as np
import rawpy


def sha(data):
    return hashlib.sha256(data).hexdigest()


def measure(row,cfg,exif):
    raw = (root/"input"/row["file"]).read_bytes()
    if sha(raw) != row["sha256"]:
        raise ValueError("Raw capture hash mismatch")
    with rawpy.imread(BytesIO(raw)) as camera:
        pixels = camera.raw_image_visible
        layout = camera.raw_colors_visible
        colors = camera.color_desc.decode("ascii")
        metadata = camera.camera_white_level_per_channel
        black = camera.black_level_per_channel
        shape = pixels.shape
        full = camera.white_level
        if pixels.ndim != 2 or any(d%2 for d in shape):
            raise ValueError("Unsupported CFA shape")
        phase = [colors[int(layout[y,x])] for y,x in ((0,0),(0,1),(1,0),(1,1))]
        if phase != ["R","G","G","B"]:
            raise ValueError("Unexpected CFA phase")
        flags = np.zeros(tuple(d//2 for d in shape),dtype=np.uint8)
        planes = []
        for i, (y,x) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            color = int(layout[y,x])
            if not np.all(layout[y::2,x::2] == color):
                raise ValueError("Nonperiodic channel layout")
            label = ("R","G1","G2","B")[i]
            plane = pixels[y::2,x::2]
            hist = np.bincount(plane.ravel(),minlength=65536)
            white = int(metadata[color] if metadata is not None else full)
            floor = int(black[color])
            if not 0 <= floor < white < 65536:
                raise ValueError("Invalid level")
            near = {}
            for fraction in cfg["thresholdsBelowWhiteFraction"]:
                threshold = int(np.ceil(white-fraction*(white-floor)))
                near[str(fraction)] = {"thresholdRaw":threshold,"countsAtOrAbove":int(hist[threshold:].sum())}
            active = plane >= white
            flags[active] |= 1 << i
            tail = np.flatnonzero(hist)[-6:][::-1]
            planes.append({"label":label,"detectorColorIndex":color,"whiteLevel":white,"blackLevel":floor,
              "maxRaw":int(tail[0]),"pixels":int(plane.size),"countsAtWhite":int(hist[white]),
              "countsAboveWhite":int(hist[white+1:].sum()),"near":near,
              "topCodes":[[int(code),int(hist[code])] for code in tail]})
        kinds = np.bincount(flags.ravel(),minlength=16)
        packed = {str(mask):int(n) for mask,n in enumerate(kinds) if mask and n}
        other = exif(raw)
        record = {"input":row["file"],"camera":row["camera"],"group":row["group"],
                  "shapeYX":list(shape),"cropOriginYX":[camera.sizes.top_margin,camera.sizes.left_margin],
                  "iso":other["iso"],"seconds":other["secondsNumerator"]/other["secondsDenominator"],
                  "globalWhite":int(full),"channelMetadataUsed":metadata is not None,
                  "phases":planes,"hitCellsByPhaseBitMask":packed,
                  "cellsWithSomeButNotAllPhasesAtWhite":int(kinds[1:15].sum()),
                  "cellsWithAllPhasesAtWhite":int(kinds[15])}
    return record,flags


def recurrence(entries):
    masks = [row[1] for row in entries]
    if any(m.shape != masks[0].shape for m in masks):
        raise ValueError("Detector coverage changed within group")
    hit = [mask != 0 for mask in masks]
    all_hits = np.logical_and.reduce(hit)
    same_phase = np.bitwise_and.reduce(masks) != 0
    union = np.logical_or.reduce(hit)
    return {"unionCells":int(union.sum()),"recurringInAllCells":int(all_hits.sum()),
            "samePhaseRecurringInAllCells":int(same_phase.sum())}, np.bitwise_or.reduce(masks)


def main():
    cfg_path = root/"protocollo.json"
    cfg = json.loads(cfg_path.read_bytes())
    if (rawpy.__version__,rawpy.libraw_version,np.__version__) != ("0.25.1",(0,21,4),"2.3.5"):
        raise ValueError("Unexpected decoder")
    if sha(wheel.read_bytes()) != cfg["rawpyWheelSha256"]:
        raise ValueError("Unexpected package")
    with ZipFile(wheel) as z:
        for member in z.namelist():
            if member.startswith("rawpy/") and not member.endswith("/"):
                if (runtime/member).read_bytes() != z.read(member):
                    raise ValueError("Decoder member hash differs")
    reader = (root/"lettore-exif.py").read_bytes()
    if sha(reader) != cfg["exifSourceSha256"]:
        raise ValueError("Changed EXIF reader")
    definitions = [item for item in ast.parse(reader).body if isinstance(item, ast.FunctionDef) and item.name == "exif"]
    if len(definitions) != 1:
        raise ValueError("EXIF function missing")
    def require(ok, message):
        if not ok:
            raise ValueError(message)
    namespace = {"struct": struct, "require": require}
    exec(compile(ast.Module(body=definitions, type_ignores=[]), "pinned-exif", "exec"), namespace)
    exif = namespace["exif"]
    groups = defaultdict(list)
    rows = []
    for row in cfg["inputs"]:
        value, flags = measure(row,cfg,exif)
        rows.append(value)
        groups[(row["camera"],row["group"])].append((value,flags))
    summaries, unions = {}, {}
    for (camera,group), values in groups.items():
        report, union = recurrence(values)
        summaries[camera+"/"+group]=report
        unions[camera,group]=union
    a,b = (unions["EOS40D",tag] for tag in ("light","dark"))
    output_data = {"schema":cfg["schema"],"protocolSha256":sha(cfg_path.read_bytes()),"frames":rows,
          "groups":summaries,"darkAndLightHitCellsSamePhase40D":int(((a&b)!=0).sum()),
          "scientificClosures":0,"physicalFullWellMeasured":False}
    with output.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(output_data,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
