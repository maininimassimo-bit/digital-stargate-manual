from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

root, capture, stars, deps, out = map(Path, sys.argv[1:])
sys.path.insert(0,str(deps))
import astropy
from astropy.io import fits
import numpy as np

def digest(path):
    with path.open("rb") as handle:
        return file_digest(handle, "sha256").hexdigest()

p_path = root/"protocollo.json"
p_hash = digest(p_path)
assert p_hash == "782be6cadd3963ad0c9a9d7257c4fa88222106b4f5ed369c6354d43b6edbc63b"
p = json.loads(p_path.read_bytes())
archive = capture/"Brutes_180s.zip"
receipt = capture/"riscontro-con-celle.json"
assert [digest(q) for q in (archive, receipt, stars)] == [p[k] for k in ("captureZip","captureReceipt","stellarReceipt")]
assert (astropy.__version__, np.__version__) == ("7.2.0","2.3.5")
lights = json.loads(receipt.read_bytes())["rows"]
fitted = json.loads(stars.read_bytes())["frames"]
assert len(lights) == 15 and [f["member"] for f in fitted] == [r["member"] for r in lights[1:]]
rows = [{"member":lights[0]["member"], "status":"evaluated","p90NativePx":0.0,"coefficients":np.zeros((3,2))}]
rows.extend({"member":f["member"],"status":"evaluated","p90NativePx":f["p90"]["stellarHuber"],
             "coefficients":np.array(f["huberCoefficients"])/2} for f in fitted)

width, height = p["shape"]
x0, y0 = p["origin"]
gx, gy = np.meshgrid(np.arange(width)+x0,np.arange(height)+y0)
affine = np.stack((np.ones_like(gx),(2*gx-3104)/2048,(2*gy-2076)/2048),axis=-1)
x = (gx-x0-(width-1)/2)/(width/2)
y = (gy-y0-(height-1)/2)/(height/2)
basis = np.stack((np.ones_like(x),x,y),axis=-1)
cell = p["cell"]
cells = [(slice(j,j+cell),slice(i,i+cell)) for j in range(0,height,cell) for i in range(0,width,cell)]
even = np.array([(s[0].start//cell+s[1].start//cell)%2 == 0 for s in cells])

def decode(z, entry):
    raw = z.read(entry["member"])
    assert sha256(raw).hexdigest() == entry["sha256"]
    with fits.open(BytesIO(raw),memmap=False,uint=True) as hdus:
        image = hdus[0].data
        hdr = hdus[0].header
        assert image.shape == (4176,6248) and hdr["BAYERPAT"] == "RGGB"
        assert float(hdr["EXPTIME"]) == 180
        g1,g2 = image[::2,1::2],image[1::2,::2]
        mask = (g1 < p["rawRejectAtOrAbove"]) & (g2 < p["rawRejectAtOrAbove"])
        return (g1.astype(float)+g2)/2,mask


def align(image, good, target_xy):
    px, py = target_xy
    ix, iy = np.floor(px).astype(int), np.floor(py).astype(int)
    assert ix.min() >= 0 and ix.max()+1 < image.shape[1]
    assert iy.min() >= 0 and iy.max()+1 < image.shape[0]
    u, v = px-ix, py-iy
    aligned = np.zeros(px.shape)
    valid = np.ones(px.shape, dtype=bool)
    for dy, wy in enumerate((1-v, v)):
        for dx, wx in enumerate((1-u, u)):
            aligned += image[iy+dy,ix+dx]*wy*wx
            valid &= good[iy+dy,ix+dx]
    return aligned, valid


def scores(design, measured, fold, terms):
    train = fold
    A = design[:, :terms]
    coefficient, _, rank, _ = np.linalg.lstsq(A[train], measured[train], rcond=None)
    assert rank == terms
    error = np.abs(measured[~train] - A[~train] @ coefficient)
    return {"medianAbsoluteADU": float(np.median(error)), "p90AbsoluteADU": float(np.quantile(error,.9))}


assert p["models"] == [1,3] and p["photoScale"] == 1
eligible, rejected = [], []
for i, row in enumerate(rows):
    if i in p["excludePreviouslyMeasured"]:
        continue
    if row["status"] == "evaluated" and row["p90NativePx"] <= p["maximumRegistrationP90NativePx"]:
        eligible.append(i)
    else:
        rejected.append(i)
refs = [eligible[i] for i in (0,len(eligible)//2,-1)]
targets = [i for i in eligible if i not in refs]
images = {}
common = np.ones(gx.shape, dtype=bool)
with ZipFile(archive) as z:
    for i in eligible:
        frame, good = decode(z, lights[i])
        shift = affine @ np.asarray(rows[i]["coefficients"])
        image, mask = align(frame,good,(gx+shift[...,0],gy+shift[...,1]))
        images[i] = image
        common &= mask

usable = np.array([common[s].mean() >= p["minimumValidPerCell"] for s in cells])
groups = [s for s,v in zip(cells,usable,strict=True) if v]
design = np.array([np.median(basis[s][common[s], :3],axis=0) for s in groups])
train = even[usable]
assert min(train.sum(), (~train).sum()) >= 24
plane = 2+x-y
plane_medians = np.array([np.median(plane[s][common[s]]) for s in groups])
for mask in (train, ~train):
    assert scores(design,plane_medians,mask,3)["p90AbsoluteADU"] < .005

comparisons = []
for ref in refs:
    for target in targets:
        difference = images[target] - images[ref]
        measures = np.array([np.median(difference[s][common[s]]) for s in groups])
        folds = []
        for i in p["folds"]:
            select = train if i == 0 else ~train
            baseline = scores(design,measures,select,1)
            affine_metrics = scores(design,measures,select,3)
            passed = (affine_metrics["medianAbsoluteADU"] <= baseline["medianAbsoluteADU"] *
                      (1-p["maeImprovementMinimumPercent"]/100) and
                      affine_metrics["p90AbsoluteADU"] <= baseline["p90AbsoluteADU"])
            folds.append({"trainParity": i, "offset": baseline, "plane": affine_metrics, "pass": passed})
        comparisons.append({"referenceIndex": ref, "targetIndex": target, "folds": folds,
                            "passBothFolds": all(row["pass"] for row in folds)})

summary = [{"referenceIndex": r, "pairs": len(targets),
            "passedBoth": sum(c["passBothFolds"] for c in comparisons if c["referenceIndex"] == r)}
           for r in refs]
invariant = [t for t in targets if all(c["passBothFolds"] for c in comparisons if c["targetIndex"] == t)]
report = {"schema": "BKL046_M8_M20_REFERENCE_TRANSFER_V1", "protocolSha256": p_hash,
          "programSha256": digest(Path(__file__)), "references": refs, "targets": targets,
          "frames": [{"index": i,"member": rows[i]["member"],"sha256": lights[i]["sha256"],
                      "registrationP90NativePx": rows[i]["p90NativePx"]} for i in eligible],
          "geometryRejected": rejected, "validFraction": float(common.mean()),
          "usableCellsByParity": [int(train.sum()),int((~train).sum())],
          "cases": comparisons, "summary": summary, "targetPassAllReferences": invariant,
          "nativeExecutions": 0, "scientificClosures": 0}
out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
