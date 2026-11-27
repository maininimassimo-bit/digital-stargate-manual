"""Measure all geometric background cells on SHASSA and compare anchor layouts."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


def pin(path, expected):
    data = path.read_bytes()
    if sha256(data).hexdigest() != expected:
        raise ValueError(f"INPUT_CHANGED:{path.name}")
    return data


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "source", "dependencies", "report", "full"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    protocol_bytes = args.protocol.read_bytes()
    cfg = json.loads(protocol_bytes)
    old = json.loads(pin(args.source / "riscontro.json", cfg["sourceReportSha256"]))
    parent = json.loads(pin(args.source / "protocollo.json", old["protocolSha256"]))
    plate, geom, dark = [
        json.loads(pin(args.source / key, parent["inputs"][key]))
        for key in ("plate.json", "geometry.json", "cells.json")
    ]
    # The parent receipt supplies the exact geometry and data pins.
    source_map = args.source / "153.sm.fits.gz"
    pin(source_map, parent["inputs"][source_map.name])
    sys.path.insert(0, str(args.dependencies))
    import astropy
    from astropy import units as u
    from astropy.io import fits
    from astropy.wcs import WCS
    import numpy as np

    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    w, h = geom["shape"]
    cell = geom["cell"]
    assert w % cell == h % cell == 0
    ny, nx = h // cell, w // cell
    assert (ny, nx) == (12, 16)
    x, y = np.meshgrid(np.arange(nx), np.arange(ny))
    ij = np.column_stack((x.ravel(), y.ravel()))
    binned = (ij + .5) * cell - .5 + np.asarray(geom["origin"])
    centered = ((ij + .5) * cell - np.asarray((w, h)) / 2) / (np.asarray((w, h)) / 2)
    native = 2*binned + .5
    x, y = ((native - parent["plateCenterNative"]) / parent["fitScaleNative"]).T
    tangent = np.column_stack((np.ones(len(x)), x, y, x*x, x*y, y*y)) @ np.asarray(plate["coefficients"])
    target = WCS(naxis=2)
    target.wcs.crpix = [1, 1]
    target.wcs.crval = parent["tangentCenterIcrs"]
    target.wcs.cdelt = [plate["nominalArcsecPx"] / 3600] * 2
    target.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    target.wcs.radesys = "ICRS"
    sky = target.pixel_to_world(tangent[:, 0], tangent[:, 1])
    original = []
    for i, xy in enumerate(dark["anchorCells"]):
        hit, = np.flatnonzero(np.all(centered == xy, axis=1))
        original.append(int(hit))
        entry = old["anchors"][i]
        np.testing.assert_allclose(native[hit], entry["nativeXY"], rtol=0, atol=1e-12)
        np.testing.assert_allclose([sky[hit].ra.deg, sky[hit].dec.deg],
                                   [entry["raIcrsDeg"], entry["decIcrsDeg"]], rtol=0, atol=1e-10)
    all_cells = []
    with fits.open(source_map, memmap=False, do_not_scale_image_data=True) as hdus:
        hdr, image = hdus[0].header, hdus[0].data
        assert hdr["BUNIT"].strip() == "dR" and hdr["BSCALE"] == 1 and hdr["BZERO"] == 0
        atlas = WCS(hdr, fix=False).celestial
        np.testing.assert_allclose(atlas.pixel_scale_matrix, [[hdr["CD1_1"], hdr["CD1_2"]],
                                   [hdr["CD2_1"], hdr["CD2_2"]]], atol=1e-12, rtol=0)
        ax, ay = atlas.world_to_pixel(sky)
        for i, (cx, cy) in enumerate(zip(ax, ay, strict=True)):
            xi, yi = round(cx), round(cy)
            xx, yy = np.meshgrid(np.arange(xi-15, xi+16), np.arange(yi-15, yi+16))
            sep = atlas.pixel_to_world(xx, yy).separation(sky[i]).to_value(u.arcmin)
            border = np.concatenate((sep[0], sep[-1], sep[:, 0], sep[:, -1]))
            assert border.min() > max(cfg["radiiArcmin"])
            support = (xx >= 0) & (yy >= 0) & (xx < image.shape[1]) & (yy < image.shape[0])
            samples = np.full(xx.shape, hdr["BLANK"], dtype=np.int64)
            samples[support] = image[yy[support], xx[support]]
            entry = {"cell": i, "gridXY": ij[i].tolist(), "normalizedXY": centered[i].tolist(), "radii": {}}
            for r in cfg["radiiArcmin"]:
                within = sep <= r
                valid = samples[within & (samples != hdr["BLANK"])]
                n = int(within.sum())
                enough = len(valid) / n >= cfg["minimumCoverage"]
                entry["radii"][r] = {"expected": n, "valid": len(valid),
                                     "medianRayleigh": float(np.median(valid)) / 10 if enough else None}
            all_cells.append(entry)
    for i, index in enumerate(original):
        for k, radius in enumerate(cfg["radiiArcmin"]):
            expected = old["fields"]["153"]["rows"][i]["apertures"][k]
            measured = all_cells[index]["radii"][radius]
            assert (measured["expected"], measured["valid"], measured["medianRayleigh"]) == (
                expected["expectedPixels"], expected["validPixels"], expected["medianRayleigh"]
            )

    design = np.column_stack((np.ones(len(ij)), centered))

    def gain(indices):
        source = design[indices]
        if np.linalg.matrix_rank(source) != 3:
            return {"status": "RANK_DEFICIENT"}
        # A maps unit-independent anchor perturbations to fitted values.
        a = design @ np.linalg.pinv(source)
        sigma = np.sqrt(np.sum(a*a, axis=1))
        np.testing.assert_allclose(np.linalg.pinv(source) @ source, np.eye(3), atol=1e-12, rtol=0)
        return {"status": "FULL_RANK", "conditionNumber": float(np.linalg.cond(source)),
                "worstPredictionStdPerUnitAnchorStd": float(sigma.max())}

    def summarize(cells, values):
        return {"cells": cells, "medianAnchorRayleigh": float(np.median([values[i] for i in cells])),
                "maxAnchorRayleigh": max(values[i] for i in cells), "plane": gain(cells),
                "leaveOneOut": [dict(removed=i, **gain([j for j in cells if j != i])) for i in cells]}

    comparisons = {}
    for radius in cfg["radiiArcmin"]:
        values = [c["radii"][radius]["medianRayleigh"] for c in all_cells]
        ordered = sorted((n for n, v in enumerate(values) if v is not None), key=lambda i: (values[i], i))
        spatial = [
            next(i for i in ordered if ij[i][1] * 2 // ny == row and ij[i][0] * 3 // nx == col)
            for row in range(2) for col in range(3)
        ]
        assert len(set(spatial)) == 6
        comparisons[radius] = {"cellsMeasured": len(ordered),
                               "original": summarize(original, values),
                               "globalLowest": summarize(ordered[:6], values),
                               "stratifiedLowest": summarize(spatial, values)}
    full = (json.dumps(all_cells, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()
    with args.full.open("xb") as stream:
        stream.write(full)
    doc = {"schema": "BKL046_M8M20_SHASSA_ANCHOR_GEOMETRY_RESULT_V1",
           "protocolSha256": sha256(protocol_bytes).hexdigest(),
           "programSha256": sha256(Path(__file__).read_bytes()).hexdigest(),
           "fullReportSha256": sha256(full).hexdigest(), "comparisons": comparisons,
           "originalSixCellReadbacksVerified": True, "nativeExecutions": 0,
           "coobservedBroadbandAnchors": 0, "aduConversionQualified": False, "scientificClosures": 0}
    with args.report.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(doc, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
