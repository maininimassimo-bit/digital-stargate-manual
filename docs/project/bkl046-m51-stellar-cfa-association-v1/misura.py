from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
from io import BytesIO
from itertools import combinations, product
import json
import os
from pathlib import Path
import sys

parser = ArgumentParser()
for name in ("protocol", "source", "previous_report", "rawpy_packages", "packages", "vc", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()
libs = [os.add_dll_directory(str(args.rawpy_packages / "rawpy")), os.add_dll_directory(str(args.vc))]
sys.path[:0] = [str(args.rawpy_packages), str(args.packages)]
import numpy as np
import rawpy

PLAN = "58b7f521ad2a77f7a1c63968fbc85dc2da44cc043a34d4f239920724c2cb1489"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, digest):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == digest, f"Changed input {path.name}")
    return raw


plan = json.loads(pinned(args.protocol, PLAN))
prior = json.loads(pinned(args.previous_report, plan["previousRegistrationSha256"]))
originals = args.source / "originali"
capture = json.loads(pinned(originals / "acquisizione.json", plan["acquisitionSha256"]))
require(rawpy.__version__ == "0.25.1" and rawpy.libraw_version == (0,21,4) and np.__version__ == "2.3.5",
        "Changed detector decoder")
shape = tuple(plan["detectorShapeYX"])
center = np.array(shape[::-1]) / 4


def stars(data, white):
    green = .5 * (data[::2, 1::2].astype(np.float32) + data[1::2, ::2])
    g = green[6:-6, 6:-6]
    neighbors = [green[1:-11,6:-6], green[11:-1,6:-6], green[6:-6,1:-11], green[6:-6,11:-1]]
    highpass = g - np.median(np.stack(neighbors), axis=0)
    adjacent = [green[5:-7,6:-6], green[7:-5,6:-6], green[6:-6,5:-7], green[6:-6,7:-5]]
    peaks = np.logical_and.reduce([g > other for other in adjacent]) & (g < white - 256)
    points = []
    size = plan["tileSizeBinned"]
    ygrid, xgrid = np.indices((7,7))
    for y0 in range(0, g.shape[0], size):
        for x0 in range(0, g.shape[1], size):
            hp = highpass[y0:y0+size, x0:x0+size]
            floor = np.median(hp)
            sigma = 1.4826 * np.median(np.abs(hp-floor))
            rows, cols = np.where(peaks[y0:y0+size,x0:x0+size] & (hp > floor + plan["minSignalMAD"]*max(sigma,1.)))
            rank = np.argsort(-hp[rows,cols], kind="stable")
            tile = []
            for i in rank:
                y, x = int(rows[i]+y0+6), int(cols[i]+x0+6)
                if any((x-a)**2+(y-b)**2 < plan["minPeakDistanceBinned"]**2 for a,b in tile):
                    continue
                patch = green[y-3:y+4,x-3:x+4]
                values = np.maximum(patch - np.median(patch), 0).astype(float)
                total = values.sum()
                if total <= 0 or patch.max() >= white-256:
                    continue
                dx = float((values*xgrid).sum()/total - 3)
                dy = float((values*ygrid).sum()/total - 3)
                tile.append((x,y))
                points.append((x+dx,y+dy))
                if len(tile) >= plan["perTile"]:
                    break
    require(len(points) >= 70, "Too few independent peak locations")
    return np.asarray(points)-center


def distances(a,b):
    d = a[:,None,:]-b[None,:,:]
    return np.einsum("ijk,ijk->ij", d, d)


def triangles(a):
    d = distances(a,a)
    neighbors = np.argsort(d, axis=1, kind="stable")[:,1:1+plan["triangleNeighbors"]]
    ids = {tuple(sorted((i, int(j), int(k))))
           for i, nn in enumerate(neighbors) for j,k in combinations(nn,2)}
    for i,j,k in sorted(ids):
        verts = [i,j,k]
        opposite = np.array([d[j,k],d[i,k],d[i,j]])
        order = np.argsort(opposite, kind="stable")
        lengths = np.sqrt(opposite[order])
        low, mid, high = lengths
        if low < plan["minTriangleSide"] or high > plan["maxTriangleSide"] or min(mid-low,high-mid) < 2:
            continue
        vertices = a[[verts[o] for o in order]]
        u,v = vertices[1:]-vertices[0]
        cross = u[0]*v[1]-u[1]*v[0]
        if abs(cross) < .12*high*high:
            continue
        key = (int(low/high/plan["triangleRatioBin"]), int(mid/high/plan["triangleRatioBin"]),
               int(high/plan["triangleLengthBin"]), int(cross > 0))
        yield key,vertices,high


def similarity(a,b):
    ac,bc = a-a.mean(axis=0),b-b.mean(axis=0)
    cross = np.sum(ac[:,0]*bc[:,1]-ac[:,1]*bc[:,0])
    dot = np.sum(ac*bc)
    w = np.sum(ac*ac)
    require(w > 0, "Degenerate transformation")
    matrix = np.array(((dot,cross),(-cross,dot))) / w
    return matrix,b.mean(axis=0)-a.mean(axis=0) @ matrix


def pairs(a,b,matrix,shift,gate):
    d=distances(a@matrix+shift,b)
    i=np.arange(len(a))
    j=d.argmin(axis=1)
    keep=(d[i,j]<=gate**2)&(d.argmin(axis=0)[j]==i)
    return i[keep],j[keep],np.sqrt(d[i[keep],j[keep]])


def seed(a,b):
    index = defaultdict(list)
    for key, vertices, longest in triangles(b):
        index[key].append((vertices,longest))
    votes = defaultdict(list)
    for key, first, alen in triangles(a):
        u,v,n,sign=key
        for x,y,z in product(range(-1,2), repeat=3):
            for second, blen in index.get((u+x,v+y,n+z,sign), ()):
                if abs(blen/alen-1)>plan["maxScaleDifference"]:
                    continue
                matrix, shift = similarity(first,second)
                err=np.linalg.norm(first@matrix+shift-second,axis=1).max()
                if err>1.9:
                    continue
                theta=np.degrees(np.arctan2(matrix[0,1],matrix[0,0]))%360
                vote = (int(theta+0.5)%360,int(np.rint(shift[0]/12)),int(np.rint(shift[1]/12)))
                votes[vote].append((float(err),matrix,shift))
    ordered=sorted(votes, key=lambda k:(-len(votes[k]),k))[:plan["maxSeedHypotheses"]]
    models=[]
    for key in ordered:
        _, matrix, shift=min(votes[key],key=lambda item:item[0])
        i,j,r=pairs(a,b,matrix,shift,plan["trainGatesBinned"][0])
        if len(i)>=plan["minTrainMatches"]:
            models.append((len(i),float(np.median(r)),matrix,shift))
    return min(models,key=lambda item:(-item[0],item[1])) if models else None


def assess(a,b):
    bucket = np.floor((a+center)/plan["trainingHoldoutZoneBinned"]).astype(int)
    mask=np.sum(bucket,axis=1)%2==0
    train,test=a[mask],a[~mask]
    initial=seed(train,b)
    if initial is None:
        return dict(status="NO_RELIABLE_TRAINING_TRANSFORM", detectedReference=len(a), detectedTarget=len(b))
    _,_,matrix,shift=initial
    for gate in plan["trainGatesBinned"]:
        i,j,r=pairs(train,b,matrix,shift,gate)
        if len(i)<plan["minTrainMatches"]:
            return dict(status="INSUFFICIENT_TRAINING_MATCHES", count=len(i))
        matrix,shift=similarity(train[i],b[j])
    translation=np.median(b[j]-train[i],axis=0)
    regression=np.column_stack((train[i],np.ones(len(i))))
    coef,_,rank,_=np.linalg.lstsq(regression,b[j],rcond=None)
    require(rank==3, "Degenerate affine training geometry")
    available=b[np.logical_not(np.isin(np.arange(len(b)),j))]
    k,l,_=pairs(test,available,coef[:2],coef[2],plan["heldoutGateBinned"])
    if len(k)<12:
        return dict(status="INSUFFICIENT_HELDOUT_MATCHES", trainingMatches=len(i), heldoutMatches=len(k))
    values={}
    for name,pred in {
        "translation":test[k]+translation,
        "similarity":test[k]@matrix+shift,
        "affine":test[k]@coef[:2]+coef[2],
    }.items():
        r=2*np.linalg.norm(pred-available[l],axis=1)
        values[name]=dict(medianNativePx=float(np.median(r)),p90NativePx=float(np.quantile(r,.9)))
    xy=(test[k]+center)*2
    heldout_group=len({tuple(row) for row in np.floor(xy/(2*plan["trainingHoldoutZoneBinned"])).astype(int)})
    return dict(status="CONDITIONAL_HELDOUT_COMPARISON", detectedReference=len(a),detectedTarget=len(b),
                trainingMatches=len(i),heldoutMatches=len(k),heldoutZones=heldout_group,
                similarityAngleDegrees=float(np.degrees(np.arctan2(matrix[0,1],matrix[0,0]))),
                similarityScale=float(np.linalg.norm(matrix[0])),centralShiftNativeXY=(2*shift).tolist(),
                metrics=values,globalTranslationWithinTolerance=values["translation"]["p90NativePx"]<=plan["translationToleranceNativePx"])


rng=np.random.default_rng(5151)
control=rng.uniform(-900,900,(150,2))
angle=np.deg2rad(173.)
model=np.array(((np.cos(angle),np.sin(angle)),(-np.sin(angle),np.cos(angle))))
moved=control@model+[140.,-117.]
trial=assess(control,moved)
require(trial["status"]=="CONDITIONAL_HELDOUT_COMPARISON" and abs(trial["similarityAngleDegrees"]-173)<1e-6
        and trial["metrics"]["affine"]["p90NativePx"]<1e-7, "Known rotation failed")
series=[]
for sample in capture["samples"]:
    raw=pinned(originals/sample["file"],sample["sha256"])
    with rawpy.imread(BytesIO(raw)) as decoder:
        raw_plane=decoder.raw_image_visible
        require(raw_plane.shape==shape, "Changed input dimensions")
        series.append(stars(raw_plane,decoder.white_level))
reports=[]
for obs,target,source in zip(prior["records"],series[1:],capture["samples"][1:],strict=True):
    require(obs["sha256"]==source["sha256"], "Changed original reference ordering")
    reports.append(dict(sha256=source["sha256"], priorOutcome=obs["outcome"]["classification"],
                        stellar=assess(series[0],target)))
report=dict(schema=plan["schema"], protocolSha256=PLAN, records=reports,
            syntheticRotationRecovered=True, independentAstrometricCatalogUsed=False,
            deliberateDitherProven=False, nativeExecutions=0, scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as stream:
    json.dump(report,stream,indent=2,allow_nan=False)
    stream.write("\n")
