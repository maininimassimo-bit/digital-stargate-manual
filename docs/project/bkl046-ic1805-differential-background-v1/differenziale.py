from hashlib import file_digest, sha256
from io import BytesIO
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

root, capture, stars, wheel, deps, vc, out = map(Path, sys.argv[1:])
dlls = [os.add_dll_directory(str(wheel / "rawpy")), os.add_dll_directory(str(vc))]
sys.path[:0] = [str(wheel), str(deps)]
import numpy as np
import rawpy


def digest(path):
    with path.open("rb") as handle:
        return file_digest(handle, "sha256").hexdigest()


p_path = root / "protocollo.json"
p_hash = digest(p_path)
assert p_hash == "33d9b9cdc5752f554e8feb20c25d02a160edf8bb920a53c4b15eb5b0720635a2"
p = json.loads(p_path.read_bytes())
archive = capture / "HeartNebula.zip"
cap_receipt = capture / "riscontro.json"
assert digest(archive) == p["captureZip"]
assert digest(cap_receipt) == p["captureReceipt"]
assert digest(stars) == p["stellarReceipt"]
assert (rawpy.__version__, tuple(rawpy.libraw_version), np.__version__) == ("0.25.1", (0, 21, 4), "2.3.5")
geometry = json.loads(stars.read_bytes())
lights = json.loads(cap_receipt.read_bytes())["inputs"]["lights"]
rows = geometry["rows"]
assert [r["member"] for r in rows] == [r["member"] for r in lights]
assert rows[0]["member"] == geometry["referenceMember"]

width, height = p["shape"]
x0, y0 = p["origin"]
gx, gy = np.meshgrid(np.arange(width) + x0, np.arange(height) + y0)
cx, cy = geometry["referenceOriginBinned"]
affine = np.stack((np.ones_like(gx), (gx-cx)/1024, (gy-cy)/1024), axis=-1)
x = (gx-x0-(width-1)/2)/(width/2)
y = (gy-y0-(height-1)/2)/(height/2)
basis = np.stack((np.ones_like(x), x, y, x*x, x*y, y*y), axis=-1)
profile = np.exp(-0.5*((x/.58)**2+(y/.39)**2))
aperture = x*x+y*y <= .65**2
cell = p["cell"]
cells = [(slice(j,j+cell), slice(i,i+cell)) for j in range(0,height,cell)
         for i in range(0,width,cell)]
even = np.array([(s[0].start//cell+s[1].start//cell)%2 == 0 for s in cells])


def decode(z, entry):
    raw = z.read(entry["member"])
    assert sha256(raw).hexdigest() == entry["sha256"]
    assert entry["iso"] == 800 and entry["secondsNumerator"] == 60*entry["secondsDenominator"]
    with rawpy.imread(BytesIO(raw)) as camera:
        assert camera.white_level == 16224 and camera.raw_pattern.tolist() == [[0,1],[3,2]]
        assert camera.raw_image_visible.shape == (2602,3908) and camera.color_desc == b"RGBG"
        g1, g2 = camera.raw_image_visible[::2,1::2], camera.raw_image_visible[1::2,::2]
        good = (g1 < p["rawRejectAtOrAbove"]) & (g2 < p["rawRejectAtOrAbove"])
        return (g1.astype(float)+g2)/2, good


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


def solve(diff, valid, terms):
    usable = np.array([valid[s].mean() >= .9 for s in cells])
    groups = [s for s, include in zip(cells,usable,strict=True) if include]
    measured = np.array([np.median(diff[s][valid[s]]) for s in groups])
    design = np.array([np.median(basis[s][valid[s], :terms],axis=0) for s in groups])
    train = even[usable]
    assert min(train.sum(), (~train).sum()) >= 24
    beta, _, rank, _ = np.linalg.lstsq(design[train],measured[train],rcond=None)
    assert rank == terms
    err = (measured-design@beta)[~train]
    return basis[...,:terms]@beta, {
        "train": int(train.sum()), "heldOut": int((~train).sum()),
        "heldOutMedianAbsoluteADU": float(np.median(np.abs(err))),
        "heldOutP90AbsoluteADU": float(np.quantile(np.abs(err),.9)),
        "heldOutBiasADU": float(np.median(err)),
    }


def signal_recovery(delta, injected, valid):
    ap = aperture & valid
    flux = float(delta[ap].sum()/injected[ap].sum()-1)
    l2 = float(np.linalg.norm((delta-injected)[valid])/np.linalg.norm(injected[valid]))
    return {"relativeFluxError": flux, "relativeL2": l2, "passed": max(abs(flux), l2) <= p["signalTolerance"]}


results = []
with ZipFile(archive) as z:
    image, good = decode(z, lights[0])
    ref = image[gy,gx]
    ref_mask = good[gy,gx]
    test_plane = 2 + x - y
    plane, _ = solve(test_plane, np.ones_like(ref_mask), 3)
    assert np.quantile(np.abs(test_plane-plane), .99) < .005
    for index in p["indices"][1:]:
        row = rows[index]
        assert row["status"] == "evaluated" and row["p90NativePx"] <= p["maximumRegistrationP90NativePx"]
        displacement = affine @ np.asarray(row["coefficients"])
        frame, good = decode(z, lights[index])
        target, mask = align(frame,good,(gx+displacement[...,0],gy+displacement[...,1]))
        naive, naive_mask = align(frame,good,(gx,gy))
        valid = mask & ref_mask & naive_mask
        result = {"index": index, "member": row["member"], "rawSha256": lights[index]["sha256"],
                  "registrationP90NativePx": row["p90NativePx"], "validFraction": float(valid.mean()), "models": {}}
        difference = target-ref
        assert p["photoScale"] == 1
        for terms in p["models"]:
            surface, metrics = solve(difference,valid,terms)
            _, no_registration = solve(naive-ref,valid,terms)
            corrected = target-surface
            injection = {}
            for amplitude in p["injectADU"]:
                signal = amplitude*profile
                same, _ = solve((target+signal)-(ref+signal),valid,terms)
                unequal, _ = solve((target+signal)-ref,valid,terms)
                injection[str(amplitude)] = {
                    "common": signal_recovery(target+signal-same-corrected,signal,valid),
                    "targetOnly": signal_recovery(target+signal-unequal-corrected,signal,valid),
                }
            result["models"][str(terms)] = {"registered": metrics, "unalignedControl": no_registration,
                                            "injectionsAfterAlignment": injection}
        constant = result["models"]["1"]["registered"]
        for terms in (3,6):
            metrics = result["models"][str(terms)]["registered"]
            metrics["passesPredictionCriterion"] = (
                metrics["heldOutMedianAbsoluteADU"] <= constant["heldOutMedianAbsoluteADU"] *
                (1-p["maeImprovementMinimumPercent"]/100) and
                metrics["heldOutP90AbsoluteADU"] <= constant["heldOutP90AbsoluteADU"])
        results.append(result)

report = {"schema": "BKL046_IC1805_DIFFERENTIAL_V1", "protocolSha256": p_hash,
          "programSha256": digest(Path(__file__)), "reference": rows[0]["member"],
          "referenceSha256": lights[0]["sha256"], "cases": results,
          "nativeExecutions": 0, "scientificClosures": 0}
out.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n",encoding="utf-8",newline="\n")
