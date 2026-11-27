from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

working, prior, anchors, raw_runtime, dependencies, vc, output = map(Path,sys.argv[1:])
handles = [os.add_dll_directory(str(raw_runtime/"rawpy")), os.add_dll_directory(str(vc))]
sys.path[:0] = [str(raw_runtime),str(dependencies)]
import numpy as np
import rawpy
from scipy.spatial import cKDTree


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def checked(path, expected):
    data = path.read_bytes()
    if sha(data) != expected:
        raise ValueError(f"Changed input {path.name}")
    return data


def samples(raw, plateau):
    with rawpy.imread(BytesIO(raw)) as camera:
        original = camera.raw_image_visible
        colors = camera.raw_colors_visible
        metadata = camera.camera_white_level_per_channel
        if metadata is None or tuple(original.shape) != (3670,5496):
            raise ValueError("Incorrect 6D decoder metadata")
        out = {}
        for key, defined in (("metadataLimit", None),("twoCodePlateau", plateau)):
            points = []
            for phase,(y,x) in enumerate(((0,0),(0,1),(1,0),(1,1))):
                plane = original[y::2,x::2]
                color = colors[y,x]
                if not np.all(colors[y::2,x::2] == color):
                    raise ValueError("Nonperiodic CFA")
                match = plane >= metadata[color] if defined is None else np.isin(plane,defined)
                row,col = np.where(match)
                points.extend(zip(2*col+x,2*row+y,np.full(len(row),phase)))
            out[key] = np.asarray(points,dtype=int).reshape(-1,3)
    return out


def project(points, record):
    t = np.deg2rad(record["similarityAngleDegrees"])
    c,s = np.cos(t),np.sin(t)
    matrix = record["similarityScale"]*np.array([[c,s],[-s,c]])
    mid = np.array([5496/2,3670/2])
    return (points-mid) @ matrix + mid + record["centralShiftNativeXY"]


def interior(points, radius):
    return np.all((points >= radius) & (points < np.array([5496,3670])-radius),axis=1)


def nearest(query, data):
    if not len(data):
        return np.full(len(query),np.inf)
    return cKDTree(data).query(query)[0]


def counts(source, target, xy, radius):
    distances = nearest(xy,target[:,:2])
    phase_hits = np.zeros(len(xy),dtype=bool)
    for phase in range(4):
        selector = source[:,2] == phase
        own = target[target[:,2] == phase,:2]
        phase_hits[selector] = nearest(xy[selector],own) <= radius
    return {"anyPhase":int((distances <= radius).sum()),"samePhase":int(phase_hits.sum())}


def main():
    cfg_raw = (working/"protocollo.json").read_bytes()
    cfg = json.loads(cfg_raw)
    pinned = json.loads(checked(prior/"protocollo.json",cfg["cfaProtocolSha256"]))
    frozen_report = json.loads(checked(prior/"riscontro.json",cfg["cfaReportSha256"]))
    archive = json.loads(checked(anchors,cfg["associationSha256"]))
    reports = {row["input"]:row for row in frozen_report["frames"]}
    input_rows = [row for row in pinned["inputs"] if row["camera"] == "EOS6D"]
    expected_decoder = (rawpy.__version__,rawpy.libraw_version,np.__version__)
    if expected_decoder != ("0.25.1",(0,21,4),"2.3.5"):
        raise ValueError("Wrong decoder build")
    wheel = prior/"rawpy-0.25.1-cp312-cp312-win_amd64.whl"
    checked(wheel,pinned["rawpyWheelSha256"])
    with ZipFile(wheel) as packed:
        for name in packed.namelist():
            if name.startswith("rawpy/") and not name.endswith("/"):
                if (raw_runtime/name).read_bytes() != packed.read(name):
                    raise ValueError("Wrong decoder member")
    photos = {}
    for row in input_rows:
        name = row["file"]
        original = checked(prior/"input"/name,row["sha256"])
        sets = samples(original,cfg["plateauCodes"])
        frozen_count = sum(v["countsAtWhite"]+v["countsAboveWhite"] for v in reports[name]["phases"])
        if len(sets["metadataLimit"]) != frozen_count:
            raise ValueError("Raw threshold count changed")
        photos[row["sha256"]] = sets
    key = input_rows[0]["sha256"]
    base = photos[key]
    rows = []
    for candidate in archive["records"]:
        target = photos[candidate["sha256"]]
        fitted = candidate["stellar"]
        if fitted["status"] != "CONDITIONAL_HELDOUT_COMPARISON":
            raise ValueError("Unverified field transform")
        for label,start in base.items():
            xy = project(start[:,:2],fitted)
            regions = []
            for radius in cfg["matchRadiiNativePx"]:
                keep = interior(start[:,:2],radius) & interior(xy,radius)
                for offset in cfg["positionControlsNativePx"]:
                    keep &= interior(xy+offset,radius)
                common = start[keep]
                experiments = {str(offset):counts(common,target[label],xy[keep]+offset,radius)
                               for offset in cfg["positionControlsNativePx"]}
                regions.append({"radiusPx":radius,"eligible":len(common),
                    "detector":counts(common,target[label],common[:,:2],radius),
                    "sky":counts(common,target[label],xy[keep],radius),
                    "offsetControl":experiments})
            rows.append({"threshold":label,"targetSha256":candidate["sha256"],"sourceCount":len(start),
                         "targetCount":len(target[label]),"fieldFitP90Px":fitted["metrics"]["similarity"]["p90NativePx"],
                         "regions":regions})
    result = {"schema":cfg["schema"],"protocolSha256":sha(cfg_raw),"comparisons":rows,
              "scientificClosures":0}
    with output.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
