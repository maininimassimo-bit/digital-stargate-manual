from argparse import ArgumentParser
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

parser = ArgumentParser()
for key in ("plan", "calibration", "light", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np
from astropy.io import fits

PIN = "7ee9ce44fde021b21c71b95b084c060d11f480ea3671853b4e0df98e03c44c92"


def require(ok, label):
    if not ok:
        raise ValueError(label)


def pinned(path, pin):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == pin, f"Changed {path.name}")
    return json.loads(data)


plan = pinned(args.plan, PIN)
capture = pinned(args.calibration / "riscontro.json", plan["captureReceiptSha256"])
height, width = plan["shapeYX"]
tiles = [(y, x) for y in plan["tileOriginsY"] for x in plan["tileOriginsX"]]
extent = plan["tileSize"]
tile_y, tile_x = np.indices((extent, extent))


def images(group):
    declared = plan["archives"][group]
    root = args.light if group == "light" else args.calibration
    path = root / declared["file"]
    with path.open("rb") as raw:
        require(file_digest(raw, "sha256").hexdigest() == declared["sha256"], "Archive changed")
    rows = capture["sourceMembers"][group]
    require(len(rows) == len({r["file"] for r in rows}) == 15, "Unexpected cohort")
    with ZipFile(path) as archive:
        for row in rows:
            member = archive.getinfo(row["file"])
            require(0 < member.file_size <= 60_000_000, "Unexpected frame size")
            raw = archive.read(member)
            require(sha256(raw).hexdigest() == row["sha256"], "Frame changed")
            with fits.open(BytesIO(raw), memmap=False) as hdus:
                hdu = hdus[0]
                require(len(hdus) == 1 and hdu.data.shape == (height, width)
                        and hdu.header["INSTRUME"] == "ZWO ASI2600MC Pro"
                        and hdu.header["BAYERPAT"] == "RGGB" and hdu.header.get("ROWORDER") is None,
                        "Frame geometry or provenance changed")
                yield row["sha256"], hdu.data


def local_residual(data, y, x):
    neighboring = np.stack((data[y-2, x], data[y+2, x], data[y, x-2], data[y, x+2]))
    return data[y, x].astype(np.float64) - np.median(neighboring, axis=0)


def samples_for(data, anchors):
    y, x, levels = anchors.T
    y, x = y.astype(int), x.astype(int)
    results = {}
    for name, (ty, tx) in {
        "identity": (y, x), "flip-x": (y, width - 1 - x),
        "flip-y": (height - 1 - y, x), "rotate-180": (height - 1 - y, width - 1 - x),
    }.items():
        delta = local_residual(data, ty, tx)
        floor = np.maximum(plan["validationFloorAdu"], plan["validationFractionOfTraining"] * levels)
        results[name] = dict(persistent=int(np.count_nonzero(delta >= floor)),
                             medianFractionOfTraining=float(np.median(delta / levels)))
    return results


def select_anchors(datasets):
    med = np.median(np.asarray(datasets), axis=0)
    anchors = []
    for residual, (y0, x0) in zip(med, tiles, strict=True):
        used = []
        for index in np.argsort(-residual.ravel(), kind="stable"):
            y, x = divmod(int(index), extent)
            if residual[y, x] < plan["minTrainingMedianAdu"]:
                break
            if any(max(abs(y-a), abs(x-b)) < plan["minSeparationPx"] for a, b in used):
                continue
            used.append((y, x))
            anchors.append((y+y0, x+x0, float(residual[y, x])))
            if len(used) == plan["maxAnchorsPerTile"]:
                break
    require(len(anchors) >= 20, "Too few reproducible detector anchors")
    return np.asarray(anchors)


training = []
checks = {"dark_holdout": {}, "light": {}, "flat": {}}
anchors = None
for ordinal, (digest, data) in enumerate(images("dark")):
    if ordinal < plan["trainingDarkCount"]:
        training.append([local_residual(data, tile_y + y, tile_x + x) for y, x in tiles])
    else:
        if anchors is None:
            anchors = select_anchors(training)
        checks["dark_holdout"][digest] = samples_for(data, anchors)
for group in ("flat", "light"):
    for digest, data in images(group):
        checks[group][digest] = samples_for(data, anchors)
summary = {}
for group, rows in checks.items():
    summary[group] = {
        name: dict(minimum=min(counts), median=float(np.median(counts)), maximum=max(counts))
        for name in plan["transforms"]
        for counts in [[row[name]["persistent"] for row in rows.values()]]
    }

report = dict(schema=plan["schema"], protocolSha256=PIN, anchors=[
    dict(y=int(y), x=int(x), medianTrainingAdu=level) for y, x, level in anchors
], trainingDarkCount=len(training), testedFrames={key: len(value) for key, value in checks.items()},
              summary=summary, frameResults=checks, physicalRowOrderVerified=False,
              nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf8", newline="\n") as target:
    json.dump(report, target, indent=2, allow_nan=False)
    target.write("\n")
