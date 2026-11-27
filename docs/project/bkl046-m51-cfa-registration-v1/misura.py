from argparse import ArgumentParser
import ast
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import sys

parser = ArgumentParser()
for name in ("protocol", "capture", "reference_code", "rawpy_packages", "packages", "vc", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()
libraries = [os.add_dll_directory(str(args.rawpy_packages / "rawpy")), os.add_dll_directory(str(args.vc))]
sys.path[:0] = [str(args.rawpy_packages), str(args.packages)]
import numpy as np
import rawpy

PROTOCOL = "fe62b1c372e20dec8cbc7365e12c5e196a64e799a59d31d21a3639b2d1afc7b0"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path, pin):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == pin, "Changed input: " + path.name)
    return raw


plan = json.loads(read(args.protocol, PROTOCOL))
summary = json.loads(read(args.capture / "riscontro.json", plan["cameraPhaseSha256"]))
receipt = json.loads(read(args.capture / "originali" / "acquisizione.json", plan["acquisitionSha256"]))
require(summary["acquisitionSha256"] == plan["acquisitionSha256"], "Acquisition and phase receipt disagree")
source = ast.parse(read(args.reference_code, plan["registrationSourceSha256"]))
selected = [node for node in source.body if isinstance(node, ast.FunctionDef) and node.name in ("prepare", "register")]
require(len(selected) == 2, "Registration reference missing")
environment = dict(np=np, require=require)
exec(compile(ast.Module(body=selected, type_ignores=[]), "pinned-mosaic-translation", "exec"), environment)
prepare, register = environment["prepare"], environment["register"]
require(rawpy.__version__ == "0.25.1" and rawpy.libraw_version == (0,21,4) and np.__version__ == "2.3.5",
        "Changed analysis environment")


def green_patch(data, y, x, width):
    require((x | y | width) & 1 == 0, "CFA crop with odd parity")
    region = data[y:y+width, x:x+width]
    require(region.shape == (width, width), "CFA region outside image")
    return .5 * (region[::2, 1::2].astype(float) + region[1::2, ::2])


def central(data):
    patch = green_patch(data, *plan["coarseRegionOriginYX"], plan["coarseRegionNativeWidth"])
    side = patch.shape[0]
    factor = plan["coarseFactorOnGreen"]
    return prepare(patch.reshape(side//factor, factor, side//factor, factor).mean(axis=(1, 3)))


def peak(a, b, limit):
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return None
    correlation = np.fft.fftshift(np.fft.ifft2(np.fft.fft2(a).conj() * np.fft.fft2(b)).real)
    middle = correlation.shape[0] // 2
    box = correlation[middle-limit:middle+limit+1, middle-limit:middle+limit+1]
    row, col = np.unravel_index(np.argmax(box), box.shape)
    return dict(xy=[int(col-limit), int(row-limit)], correlation=float(box[row,col] / norm),
                searchEdge=bool(row in (0,2*limit) or col in (0,2*limit)))


def local_tiles(reference, target, coarse):
    base = np.asarray(coarse, dtype=int) * (2 * plan["coarseFactorOnGreen"])
    width = 2 * plan["tileBinned"]
    out = []
    for y in plan["tileOriginsY"]:
        for x in plan["tileOriginsX"]:
            xx, yy = x + base[0], y + base[1]
            if not (0 <= xx <= target.shape[1] - width and 0 <= yy <= target.shape[0] - width):
                out.append(dict(originYX=[y, x], status="OUTSIDE_TARGET"))
                continue
            a = prepare(green_patch(reference, y, x, width))
            b = prepare(green_patch(target, yy, xx, width))
            trial = peak(a, b, plan["localSearchBinned"])
            if not trial or trial["searchEdge"] or trial["correlation"] < plan["minLocalCorrelation"]:
                out.append(dict(originYX=[y, x], status="UNRELIABLE_LOCAL_PEAK", peak=trial))
                continue
            fine = 2 * register(a, b, plan["localSearchBinned"], plan["stepBinned"])
            out.append(dict(originYX=[y, x], status="MEASURED", peak=trial, shiftXY=(base + fine).tolist()))
    return out


def describe(tiles):
    measured = [row for row in tiles if row["status"] == "MEASURED"]
    if len(measured) < plan["minAcceptedTilesForAffine"]:
        return dict(acceptedTiles=len(measured), classification="INSUFFICIENT_LOCAL_EVIDENCE")
    positions = np.asarray([row["originYX"][::-1] for row in measured], dtype=float)
    positions -= np.median(positions, axis=0)
    design = np.column_stack((np.ones(len(positions)), positions / 1024))
    shifts = np.asarray([row["shiftXY"] for row in measured])
    median = np.median(shifts, axis=0)
    distance = np.linalg.norm(shifts - median, axis=1)
    residual_affine, residual_constant = [], []
    for i in range(len(measured)):
        train = np.arange(len(measured)) != i
        coef, _, rank, _ = np.linalg.lstsq(design[train], shifts[train], rcond=None)
        require(rank == 3, "Degenerate tile geometry")
        residual_affine.append(float(np.linalg.norm(shifts[i] - design[i] @ coef)))
        residual_constant.append(float(np.linalg.norm(shifts[i] - np.median(shifts[train], axis=0))))
    stable = float(distance.max()) <= plan["maxTileDisagreementNativePx"]
    return dict(acceptedTiles=len(measured), medianShiftNativeXY=median.tolist(),
                maximumTileDisagreementNativePx=float(distance.max()),
                leaveOneTileOutMedianResidualPx=dict(translation=float(np.median(residual_constant)),
                                                     affine=float(np.median(residual_affine))),
                classification="TRANSLATION_WITHIN_TOLERANCE" if stable else "REGION_DEPENDENT_SHIFT",
                stableGlobalParityXY=[int(v) for v in np.rint(median).astype(int) % 2] if stable and
                np.all(np.abs(shifts - np.rint(median)) + plan["stepBinned"] < .5) else None)


control = np.random.default_rng(35129).normal(size=(160, 160))
moved = np.roll(control, (4,-3), axis=(0,1))
require(peak(control,moved,20)["xy"] == [-3,4], "Coarse translation sign control")
np.testing.assert_allclose(register(control,moved,20,.025), [-3,4], atol=1e-10, rtol=0)
reference = None
records = []
for item, phase in zip(receipt["samples"], summary["exposures"], strict=True):
    require(item["sha256"] == phase["sha256"] and phase["visiblePhase"] == "RGGB", "Changed cohort")
    with rawpy.imread(BytesIO(read(args.capture / "originali" / item["file"], item["sha256"]))) as handle:
        data = handle.raw_image_visible.copy()
    require(list(data.shape) == plan["detectorShapeYX"], "Changed camera geometry")
    if reference is None:
        reference = data
        reference_preview = central(reference)
        continue
    candidates = {"stored": data, "rotate180": data[::-1, ::-1]}
    scores = {name: peak(reference_preview, central(im), plan["coarseSearch"]) for name, im in candidates.items()}
    valid = sorted((name for name in candidates if scores[name] is not None and not scores[name]["searchEdge"]),
                   key=lambda key: -scores[key]["correlation"])
    selected = valid[0] if valid else None
    if (selected is None or scores[selected]["correlation"] < plan["minimumCoarseCorrelation"]
            or len(valid) > 1 and scores[selected]["correlation"] - scores[valid[1]]["correlation"] < plan["minimumOrientationGap"]):
        detail = dict(classification="ORIENTATION_OR_COARSE_SHIFT_UNRESOLVED")
        offsets = []
        selected = None
    else:
        offsets = local_tiles(reference,candidates[selected],scores[selected]["xy"])
        detail = describe(offsets)
    records.append(dict(sha256=item["sha256"], coarse=scores, selectedOrientation=selected,
                        tiles=offsets, outcome=detail))
result = dict(schema=plan["schema"], protocolSha256=PROTOCOL, records=records,
              deliberateDitherProven=False, nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf8", newline="\n") as stream:
    json.dump(result, stream, indent=2, allow_nan=False)
    stream.write("\n")
