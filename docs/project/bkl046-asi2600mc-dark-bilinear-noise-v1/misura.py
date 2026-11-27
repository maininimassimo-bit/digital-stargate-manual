"""Compare measured dark resampling noise with finite bilinear propagation."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


def digest(data):
    return sha256(data).hexdigest()


def read(path, expected):
    data = path.read_bytes()
    assert digest(data) == expected, path
    return json.loads(data)


def moments(np, fx, fy):
    kernel = np.outer([1 - fy, fy], [1 - fx, fx])
    weights = np.zeros((3, 3))
    for y in range(2):
        for x in range(2):
            weights[y:y+2, x:x+2] += kernel
    assert abs(np.sum(weights) - 4) < 1e-12
    return float(np.sum(weights**2)), float(4*np.sum(kernel**2))


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "prior", "archives", "dependencies", "output"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    raw = a.protocol.read_bytes()
    cfg = json.loads(raw)
    old = read(a.prior / "riscontro.json", cfg["priorReportSha256"])
    plan = read(a.prior / "protocollo.json", old["protocolSha256"])
    receipts = read(a.prior / "calibration-receipt.json", plan["calibrationReceiptSha256"])["sourceMembers"]
    sys.path.insert(0, str(a.dependencies))
    import astropy
    from astropy.io import fits
    import numpy as np
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    bands = {"R": (0,0), "G1": (0,1), "G2": (1,0), "B": (1,1)}
    phases = cfg["phaseXY"]
    operators = [moments(np, fx, fy) for fx, fy in phases]
    assert operators[0] == (4, 4) and operators[3] == (2.25, 1)
    all_results = {}
    for key, filename, kind, seconds in (
        ("dark", "Darks_180s.zip", "Dark", 180), ("shortDark", "Offsets_3s.zip", "Bias", 3)
    ):
        archive = a.archives / filename
        with archive.open("rb") as stream:
            assert file_digest(stream, "sha256").hexdigest() == plan["archivePins"][key]
        assert len(receipts[key]) == 15
        original = []
        with ZipFile(archive) as z:
            for row in receipts[key][:14]:
                raw_image = z.read(row["file"])
                assert digest(raw_image) == row["sha256"]
                with fits.open(BytesIO(raw_image), memmap=False, uint=True) as hdus:
                    img, hdr = hdus[0].data, hdus[0].header
                    assert hdr["DATE-OBS"] == row["date"] and hdr["IMAGETYP"] == kind and hdr["EXPTIME"] == seconds
                    assert hdr["BAYERPAT"] == "RGGB" and img.shape == (4176,6248)
                    original.append([img[y-64:y+64,x-64:x+64].copy() for x,y in old["tiles"]])
        rows = []
        for pair, k in enumerate(range(0,14,2)):
            for tile, (f, s) in enumerate(zip(original[k],original[k+1],strict=True)):
                assert max(np.max(f), np.max(s)) < plan["rejectAtOrAbove"]
                diff = (s.astype(float)-f)/np.sqrt(2.)
                for band, (r,c) in bands.items():
                    v = diff[r::2,c::2][:63,:63]
                    raw_variance = np.var(v,ddof=1)
                    for index, ((fx,fy), (full,diag)) in enumerate(zip(phases,operators,strict=True)):
                        x0 = (1-fx)*v[:-1,:-1] + fx*v[:-1,1:]
                        x1 = (1-fx)*v[1:,:-1] + fx*v[1:,1:]
                        shifted = (1-fy)*x0 + fy*x1
                        assert shifted.shape == (62,62)
                        blocks = shifted.reshape(31,2,31,2).transpose(0,2,1,3).reshape(-1,4)
                        cov = np.cov(blocks,rowvar=False,ddof=1)
                        empirical = np.var(blocks.sum(axis=1),ddof=1)
                        np.testing.assert_allclose(empirical,cov.sum(),rtol=1e-12,atol=1e-10)
                        rows.append({"pair":pair,"tile":tile,"band":band,"phaseIndex":index,
                             "inputVarianceAdu2":float(raw_variance),"sampleBlocks":len(blocks),
                             "empiricalAdu2":float(empirical),"empiricalDiagonalAdu2":float(np.trace(cov)),
                             "independentInputFullAdu2":float(raw_variance*full),
                             "independentInputDiagonalAdu2":float(raw_variance*diag)})
        all_results[key] = rows

    summary = {}
    for key, data in all_results.items():
        summary[key] = []
        for i, (phase,(full,diag)) in enumerate(zip(phases,operators,strict=True)):
            rows = [r for r in data if r["phaseIndex"] == i]
            assert len(rows) == 252
            def ratio(num,den):
                return np.asarray([r[num]/r[den] for r in rows])
            correction = ratio("empiricalAdu2","empiricalDiagonalAdu2")
            full_error = np.abs(ratio("independentInputFullAdu2","empiricalAdu2")-1)
            diagonal_error = np.abs(ratio("independentInputDiagonalAdu2","empiricalAdu2")-1)
            summary[key].append({
                "phaseXY":phase, "observations":len(rows), "unitInputVarianceFull":full,
                "unitInputVarianceDiagonal":diag, "empiricalSumToDiagonalMedian":float(np.median(correction)),
                "empiricalSumToDiagonalP05P95":np.quantile(correction,[.05,.95]).tolist(),
                "diagonalRelativeErrorMedian":float(np.median(diagonal_error)),
                "fullRelativeErrorMedian":float(np.median(full_error)),
                "fullRelativeErrorP95":float(np.quantile(full_error,.95)),
                "fullWithinTenPercent":int(np.count_nonzero(full_error<=.1)),
                "diagonalWithinTenPercent":int(np.count_nonzero(diagonal_error<=.1))
            })

    def save(name, value):
        data = (json.dumps(value,sort_keys=True,indent=2,allow_nan=False) + "\n").encode()
        with (a.output / name).open("xb") as stream:
            stream.write(data)
        return digest(data)
    full = save("tutti-gli-esiti.json",all_results)
    save("riscontro.json",{"schema":"BKL046_ASI2600MC_DARK_BILINEAR_RESULT_V1",
          "protocolSha256":digest(raw),"programSha256":digest(Path(__file__).read_bytes()),
          "fullReportSha256":full,"pairsPerSeries":7,"heldOutPerSeries":1,"summary":summary,
          "nativeExecutions":0,"scientificClosures":0})


if __name__ == "__main__":
    main()
