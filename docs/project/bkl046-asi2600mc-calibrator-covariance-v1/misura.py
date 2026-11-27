"""Raw detector pair-difference covariance with disjoint Bayer-parity blocks."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
from itertools import product
import json
from pathlib import Path
import sys
from zipfile import ZipFile


SERIES = {"dark": ("Darks_180s.zip", "Dark", 180),
          "flat": ("Flats_3s.zip", "Flat", 3),
          "shortDark": ("Offsets_3s.zip", "Bias", 3)}
PARITY = {"R": (0, 0), "G1": (0, 1), "G2": (1, 0), "B": (1, 1)}


def sha(data):
    return sha256(data).hexdigest()


def measure(np, a, b, plan):
    keep = (a < plan["rejectAtOrAbove"]) & (b < plan["rejectAtOrAbove"])
    block_shape = (a.shape[0] // 2, 2, a.shape[1] // 2, 2)

    def blocks(p):
        return p.reshape(block_shape).transpose(0, 2, 1, 3).reshape(-1, 4)

    valid = blocks(keep).all(axis=1)
    fraction = np.mean(valid)
    if fraction < plan["minimumCompleteBlockFraction"]:
        return {"status": "REFUSED_SUPPORT", "fraction": float(fraction)}
    va, vb = blocks(a)[valid].astype(float), blocks(b)[valid].astype(float)
    diff = (vb - va) / np.sqrt(2.)
    c = np.cov(diff, rowvar=False, ddof=1)
    diag = np.trace(c)
    assert diag > 0
    empirical = np.var(diff.sum(axis=1), ddof=1)
    np.testing.assert_allclose(empirical, c.sum(), atol=1e-10, rtol=1e-12)
    rho = c / np.sqrt(np.outer(np.diag(c), np.diag(c)))
    return {"status": "MEASURED", "fraction": float(fraction), "meanAdu": float((va+vb).mean()/2),
            "avgPixelVarianceAdu2": float(diag/4), "blockSumVarianceAdu2": float(empirical),
            "blockVarianceRatio": float(empirical/diag),
            "rhoHorizontal": float((rho[0, 1]+rho[2, 3])/2),
            "rhoVertical": float((rho[0, 2]+rho[1, 3])/2)}


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "archive_dir", "receipt", "dependencies", "output"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    sys.path.insert(0, str(a.dependencies))
    import astropy
    from astropy.io import fits
    import numpy as np

    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    raw_plan = a.protocol.read_bytes()
    plan = json.loads(raw_plan)
    raw_receipt = a.receipt.read_bytes()
    assert sha(raw_receipt) == plan["calibrationReceiptSha256"]
    receipts = json.loads(raw_receipt)["sourceMembers"]
    half = plan["tilePixels"] // 2
    tiles = [(x, y) for y, x in product(plan["positionsY"], plan["positionsX"])]
    rs = np.random.default_rng(61)
    gauss = rs.normal(size=(30000, 4))
    cov = np.cov(gauss, rowvar=False, ddof=1)
    assert abs(cov.sum()/np.trace(cov)-1) < .02
    shared = np.repeat(gauss[:, :1], 4, axis=1)
    c = np.cov(shared, rowvar=False, ddof=1)
    assert c.sum()/np.trace(c) == 4
    records = {}

    for key, (filename, kind, seconds) in SERIES.items():
        archive = a.archive_dir / filename
        with archive.open("rb") as f:
            assert file_digest(f, "sha256").hexdigest() == plan["archivePins"][key]
        selected = receipts[key]
        assert len(selected) == 15 and sorted({row["date"] for row in selected}) == [row["date"] for row in selected]
        reads = []
        with ZipFile(archive) as z:
            for row in selected[:14]:
                data = z.read(row["file"])
                assert sha(data) == row["sha256"]
                with fits.open(BytesIO(data), memmap=False, uint=True) as hdus:
                    hdr, image = hdus[0].header, hdus[0].data
                    assert image.shape == (4176, 6248) and hdr["BAYERPAT"] == "RGGB"
                    assert hdr["DATE-OBS"] == row["date"] and hdr["IMAGETYP"] == kind and hdr["EXPTIME"] == seconds
                    assert hdr["GAIN"] == 100 and hdr["OFFSET"] == 50
                    reads.append([image[y-half:y+half, x-half:x+half].copy() for x, y in tiles])
        out = []
        for pair, i in enumerate(range(0, len(reads), 2)):
            for tile, (img1, img2) in enumerate(zip(reads[i], reads[i+1], strict=True)):
                for band, (row, col) in PARITY.items():
                    m = measure(np, img1[row::2, col::2], img2[row::2, col::2], plan)
                    out.append({"pair": pair, "tile": tile, "band": band, **m})
        records[key] = out
    summary = {}
    for key, rows in records.items():
        summary[key] = {}
        for band in PARITY:
            all_rows = [r for r in rows if r["band"] == band]
            eligible = [r for r in all_rows if r["status"] == "MEASURED"]
            summary[key][band] = {"measured": len(eligible), "refused": len(all_rows)-len(eligible)}
            for metric in ("meanAdu", "avgPixelVarianceAdu2", "blockVarianceRatio", "rhoHorizontal", "rhoVertical"):
                values = [r[metric] for r in eligible]
                summary[key][band][metric] = {name: float(np.quantile(values, q)) for name, q in
                    (("p05", .05), ("median", .5), ("p95", .95))}

    paired_flat_bias = {}
    for band in PARITY:
        summaries = []
        for tile in range(len(tiles)):
            def med(group, metric):
                return float(np.median([row[metric] for row in records[group]
                             if row["band"] == band and row["tile"] == tile and row["status"] == "MEASURED"]))
            signal = med("flat", "meanAdu") - med("shortDark", "meanAdu")
            excess = med("flat", "avgPixelVarianceAdu2") - med("shortDark", "avgPixelVarianceAdu2")
            summaries.append({"tile": tile, "meanSignalAdu": signal, "excessVarianceAdu2": excess,
                              "conditionalExcessVariancePerAdu": excess/signal if signal > 0 else None})
        paired_flat_bias[band] = summaries
    data = (json.dumps(records, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()
    with (a.output / "tutti-gli-esiti.json").open("xb") as f:
        f.write(data)
    result = {"schema": "BKL046_ASI2600MC_CALIBRATOR_COVARIANCE_RESULT_V1",
              "protocolSha256": sha(raw_plan), "programSha256": sha(Path(__file__).read_bytes()),
              "fullReportSha256": sha(data), "pairsPerSeries": 7, "heldOutPerSeries": 1,
              "tiles": tiles, "summary": summary, "conditionalSingleLevel": paired_flat_bias,
              "absoluteGainQualified": False, "doseLinearityQualified": False,
              "nativeExecutions": 0, "scientificClosures": 0}
    with (a.output / "riscontro.json").open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
