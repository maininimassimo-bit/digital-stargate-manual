"""Compare detector-only repeatability on the three frozen SHASSA anchor layouts."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
from itertools import combinations
import json
from pathlib import Path
import sys
from zipfile import ZipFile


def read(path, expected):
    data = path.read_bytes()
    assert sha256(data).hexdigest() == expected, path.name
    return data


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "selection", "previous", "dark_zip", "dark_receipt",
                 "injection", "reference", "joint", "dependencies", "output"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    with a.dark_zip.open("rb") as stream:
        assert file_digest(stream, "sha256").hexdigest() == p["darkArchiveSha256"]
    source_rows = json.loads(read(a.dark_receipt, p["originalDarkReceiptSha256"]))["sourceMembers"]["dark"]
    old = json.loads(read(a.previous, p["priorDarkReportSha256"]))
    assert len(source_rows) == 15 and [row["date"] for row in source_rows] == sorted(
        {r["date"] for r in source_rows})
    assert [r["sha256"] for r in source_rows[:14]] == [r["sourceSha256"] for r in old["measurements"]]
    selection = json.loads(read(a.selection, p["selectionReportSha256"]))
    choice = selection["comparisons"][str(p["selectionRadiusArcmin"])]
    names = ("original", "globalLowest", "stratifiedLowest")
    layouts = {name: choice[name]["cells"] for name in names}
    assert all(len(set(cells)) == 6 for cells in layouts.values())
    all_cells = sorted({i for row in layouts.values() for i in row})
    injection = json.loads(read(a.injection / "riscontro.json", p["injectionReportSha256"]))
    injection_plan = a.injection / "protocollo.json"
    read(injection_plan, injection["protocolSha256"])
    prog = a.injection / "iniezioni.py"
    head, end, _ = read(prog, p["injectionProgramSha256"]).decode().partition("\ncontrol = fit(")
    assert end
    script_argv = sys.argv
    sys.argv = list(map(str, (prog, injection_plan, a.reference, a.joint, a.dependencies, a.output)))
    scope = {"__file__": str(prog)}
    try:
        exec(compile(head, str(prog), "exec"), scope)
    finally:
        sys.argv = script_argv
    np = scope["np"]
    fits = scope["namespace"]["fits"]
    assert scope["p"]["peakAdu"] == 2
    g = scope["groups"]
    common = scope["common"]
    xx, yy = scope["x"], scope["y"]
    positions = np.array([[float(xx[s].mean()), float(yy[s].mean())] for s in g])
    np.testing.assert_allclose(positions[layouts["original"]], old["anchorCells"], atol=1e-12, rtol=0)
    ox, oy = scope["namespace"]["p"]["origin"]
    values = np.zeros((14, len(g), 2))
    with ZipFile(a.dark_zip) as z:
        for i, entry in enumerate(source_rows[:14]):
            data = z.read(entry["file"])
            assert sha256(data).hexdigest() == entry["sha256"]
            with fits.open(BytesIO(data), memmap=False, uint=True) as hdu:
                image = hdu[0].data
                h = hdu[0].header
                assert image.shape == (4176, 6248) and h["IMAGETYP"] == "Dark"
                assert h["BAYERPAT"] == "RGGB" and h["EXPTIME"] == 180 and h["DATE-OBS"] == entry["date"]
                for col in all_cells:
                    row, column = g[col]
                    tile = image[2*(oy+row.start):2*(oy+row.stop), 2*(ox+column.start):2*(ox+column.stop)]
                    greens = (tile[::2, 1::2].astype(float) + tile[1::2, ::2]) / 2
                    support = common[row, column]
                    assert support.shape == greens.shape and support.any()
                    sample = greens[support]
                    values[i, col] = np.mean(sample), np.median(sample)
    statistics = ("mean", "median")
    original_samples = [[[entry[method] for method in statistics] for entry in row["values"]]
                        for row in old["measurements"]]
    np.testing.assert_array_equal(values[:, layouts["original"], :], original_samples)
    splits = [(0, *group) for group in combinations(range(1, 14), 6)]
    assert len(splits) == p["partitions"]
    weights = np.full((len(splits), 14), 1 / 7)
    for i, half in enumerate(splits):
        weights[i, list(half)] = -1 / 7
    interleaved = splits.index(tuple(range(0, 14, 2)))
    chronological = splits.index(tuple(range(7)))
    samples, aperture, signals = (scope[k] for k in ("samples", "aperture", "signals"))
    gram = samples.T @ samples
    moment = samples[aperture].sum(axis=0)
    metrics = {}
    for name, ids in layouts.items():
        design = np.column_stack((np.ones(6), positions[ids]))
        inverse = np.linalg.pinv(design)
        np.testing.assert_allclose(inverse @ design, np.eye(3), atol=1e-12, rtol=0)
        metrics[name] = {}
        for m, method in enumerate(statistics):
            measure = values[:, ids, m]
            delta = weights @ (measure - measure.mean(axis=0))
            coefficients = delta @ inverse.T
            trial = samples @ coefficients[interleaved]
            sqnorm = np.einsum("ij,jk,ik->i", coefficients, gram, coefficients)
            np.testing.assert_allclose(sqnorm[interleaved], np.sum(trial**2), atol=1e-10, rtol=1e-12)
            largest = np.max(np.abs(delta), axis=1)
            if name == "original":
                np.testing.assert_allclose(delta[interleaved], old["differences"][method]["anchorDeltaAdu"],
                                           atol=1e-12, rtol=0)

            def describe(x):
                return {k: float(np.quantile(x, q)) for k, q in
                        (("median", .5), ("p95", .95), ("max", 1))}

            windows = {}
            for key, signal in signals.items():
                rel_flux = np.abs(coefficients @ moment) / np.sum(signal[aperture])
                rel_l2 = np.sqrt(sqnorm) / np.linalg.norm(signal)
                both = np.maximum(rel_flux, rel_l2) <= p["profileTolerance"]
                if name == "original":
                    h = old["differences"][method]["relativeProfileEffects"][key]
                    np.testing.assert_allclose([rel_flux[interleaved], rel_l2[interleaved]],
                                               [h["relativeFluxChange"], h["relativeL2Change"]],
                                               atol=1e-12, rtol=0)
                windows[key] = {
                    "flux": describe(rel_flux), "l2": describe(rel_l2), "bothWithinTolerance": int(both.sum()),
                    "interleaved": [float(rel_flux[interleaved]), float(rel_l2[interleaved])],
                    "chronological": [float(rel_flux[chronological]), float(rel_l2[chronological])]
                }
            metrics[name][method] = {"maxAnchorDifferenceAdu": describe(largest), "profiles": windows}
    doc = {"schema": "BKL046_M8M20_SHASSA_DARK_LAYOUT_RESULT_V1",
           "protocolSha256": sha256(raw).hexdigest(), "programSha256": sha256(Path(__file__).read_bytes()).hexdigest(),
           "framesRead": len(values), "heldOutDarkFrames": 1, "distinctCellsMeasured": len(all_cells),
           "balancedPartitionsPerMethod": len(splits), "cutRadiusArcmin": p["selectionRadiusArcmin"],
           "layoutCells": layouts, "originalCellMeasurementsAndEndpointsReproduced": True,
           "metrics": metrics, "nativeExecutions": 0, "scientificClosures": 0,
           "coobservedBroadbandAnchors": 0}
    with a.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(doc, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
