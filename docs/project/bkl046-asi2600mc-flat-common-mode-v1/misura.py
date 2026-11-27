"""Measure whether a global illumination change explains raw flat covariance."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


def sha(data):
    return sha256(data).hexdigest()


def pinned(path, expected):
    raw = path.read_bytes()
    assert sha(raw) == expected, path.name
    return json.loads(raw)


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "prior", "archive", "dependencies", "output"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    raw = a.protocol.read_bytes()
    cfg = json.loads(raw)
    prior = pinned(a.prior / "riscontro.json", cfg["priorReportSha256"])
    previous = pinned(a.prior / "tutti-gli-esiti.json", cfg["priorFullSha256"])
    assert prior["fullReportSha256"] == cfg["priorFullSha256"]
    plan = pinned(a.prior / "protocollo.json", prior["protocolSha256"])
    receipt = pinned(a.prior / "calibration-receipt.json", plan["calibrationReceiptSha256"])
    with a.archive.open("rb") as f:
        assert file_digest(f, "sha256").hexdigest() == cfg["flatArchiveSha256"] == plan["archivePins"]["flat"]
    sys.path.insert(0, str(a.dependencies))
    import astropy
    from astropy.io import fits
    import numpy as np

    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    bands = {"R": (0, 0), "G1": (0, 1), "G2": (1, 0), "B": (1, 1)}
    xy = prior["tiles"]
    half = plan["tilePixels"] // 2
    assert len(xy) == 9 and half == 64
    lookup = {(row["pair"], row["tile"], row["band"]): row for row in previous["flat"]}
    assert len(lookup) == 252
    dark = {}
    for i in range(9):
        for band in bands:
            records = [row["meanAdu"] for row in previous["shortDark"]
                       if row["tile"] == i and row["band"] == band and row["status"] == "MEASURED"]
            assert len(records) == 7
            dark[i, band] = np.median(records)
    entries = receipt["sourceMembers"]["flat"]
    assert len(entries) == 15
    samples = []
    with ZipFile(a.archive) as z:
        for e in entries[:14]:
            data = z.read(e["file"])
            assert sha(data) == e["sha256"]
            with fits.open(BytesIO(data), memmap=False, uint=True) as hdus:
                hdr, img = hdus[0].header, hdus[0].data
                assert hdr["DATE-OBS"] == e["date"] and hdr["IMAGETYP"] == "Flat" and hdr["EXPTIME"] == 3
                assert hdr["BAYERPAT"] == "RGGB" and hdr["GAIN"] == 100 and hdr["OFFSET"] == 50
                assert img.shape == (4176, 6248)
                samples.append([img[y-half:y+half,x-half:x+half].copy() for x, y in xy])
    cx, cy = np.meshgrid(np.linspace(-1., 1., 64), np.linspace(-1., 1., 64))
    detector_plane = np.stack((np.ones_like(cx), cx, cy), axis=-1)
    bx, by = np.meshgrid(np.arange(32), np.arange(32))
    folds = ((bx+by) % 2).ravel()

    def blocks(image):
        return image.reshape(32, 2, 32, 2, *image.shape[2:]).swapaxes(1, 2).reshape(-1, 4, *image.shape[2:])

    design = blocks(detector_plane)
    strata = [(i//3 + i%3) % 2 for i in range(9)]

    def result(array):
        cov = np.cov(array, rowvar=False, ddof=1)
        diagonal = np.trace(cov)
        assert diagonal > 0
        return {"blockVarianceRatio": float(cov.sum()/diagonal),
                "blockSumVarianceAdu2": float(cov.sum()), "diagonalAdu2": float(diagonal)}

    rows = []
    for pair, k in enumerate(range(0, 14, 2)):
        for band, (r, c) in bands.items():
            first = [t[r::2,c::2].astype(float) for t in samples[k]]
            second = [t[r::2,c::2].astype(float) for t in samples[k+1]]
            assert all(np.max(t) < plan["rejectAtOrAbove"] for t in first + second)
            ratio = []
            for i, (fa, fb) in enumerate(zip(first, second, strict=True)):
                baseline = dark[i, band]
                assert min(fa.mean(), fb.mean()) > baseline
                ratio.append((fb.mean()-baseline)/(fa.mean()-baseline))
            for i, (fa, fb) in enumerate(zip(first, second, strict=True)):
                base = dark[i, band]
                scale = np.median([v for j, v in enumerate(ratio) if strata[i] != strata[j]])
                assert scale > 0
                unadjusted = blocks((fb-fa)/np.sqrt(2.))
                scaled = blocks((fb-base-scale*(fa-base))/np.sqrt(1.+scale**2))
                np.testing.assert_allclose(result(unadjusted)["blockVarianceRatio"],
                    lookup[pair,i,band]["blockVarianceRatio"], atol=1e-12, rtol=0)
                scenarios = []
                for fold in (0, 1):
                    train = folds != fold
                    held = ~train
                    coef, _, rank, _ = np.linalg.lstsq(design[train].reshape(-1,3),
                                                      scaled[train].ravel(), rcond=None)
                    assert rank == 3
                    scenarios.append({"fold": fold, "raw": result(unadjusted[held]), "scaled": result(scaled[held]),
                                      "scaledPlaneRemoved": result(scaled[held]-design[held] @ coef)})
                rows.append({"pair": pair, "tile": i, "band": band, "trainOnlyScale": float(scale),
                             "heldTileRatio": float(ratio[i]), "folds": scenarios})
    summary = {}
    for band in bands:
        work = [r for r in rows if r["band"] == band]
        summary[band] = {"measurements": len(work)*2,
                         "maxAbsTrainingScaleChange": max(abs(r["trainOnlyScale"]-1) for r in work)}
        for mode in ("raw", "scaled", "scaledPlaneRemoved"):
            vals = [fold[mode]["blockVarianceRatio"] for row in work for fold in row["folds"]]
            summary[band][mode] = {"p95": float(np.quantile(vals,.95)), "median": float(np.median(vals)),
                                  "above1p2": sum(x > 1.2 for x in vals)}
    full = (json.dumps(rows, sort_keys=True, separators=(",",":"), allow_nan=False)+"\n").encode()
    with (a.output / "tutti-gli-esiti.json").open("xb") as f:
        f.write(full)
    result_doc = {"schema": "BKL046_ASI2600MC_FLAT_COMMON_MODE_RESULT_V1",
                  "protocolSha256": sha(raw), "programSha256": sha(Path(__file__).read_bytes()),
                  "fullReportSha256": sha(full), "summary": summary, "pairedTilesAndParities": len(rows),
                  "verifiedOriginalFullBlockRatios": len(lookup), "nativeExecutions": 0, "scientificClosures": 0}
    with (a.output / "riscontro.json").open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result_doc,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
