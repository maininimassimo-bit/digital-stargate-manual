"""Measure variance propagation on illuminated ASI2600MC data under fixed bilinear shifts."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


def digest(data):
    return sha256(data).hexdigest()


def pinned(path, expected):
    data = path.read_bytes()
    assert digest(data) == expected, path
    return json.loads(data)


def operators(np, fx, fy):
    kernel = np.outer([1-fy, fy], [1-fx, fx])
    weights = np.zeros((3, 3))
    for y in range(2):
        for x in range(2):
            weights[y:y+2, x:x+2] += kernel
    assert abs(weights.sum()-4) < 1e-12
    return float(np.sum(weights**2)), float(4*np.sum(kernel**2))


def block_rows(image):
    ny, nx = image.shape
    return image.reshape(ny//2, 2, nx//2, 2).swapaxes(1, 2).reshape(-1, 4)


def measure(np, image, fx, fy, full, diagonal):
    v = image[:63, :29]
    x0 = (1-fx)*v[:-1, :-1] + fx*v[:-1, 1:]
    x1 = (1-fx)*v[1:, :-1] + fx*v[1:, 1:]
    shifted = (1-fy)*x0 + fy*x1
    assert shifted.shape == (62, 28)
    blocks = block_rows(shifted)
    cov = np.cov(blocks, rowvar=False, ddof=1)
    empirical = np.var(blocks.sum(axis=1), ddof=1)
    np.testing.assert_allclose(empirical, cov.sum(), rtol=1e-12, atol=1e-10)
    variance = np.var(v, ddof=1)
    assert empirical > 0 and np.trace(cov) > 0 and variance > 0
    return dict(empirical=empirical, empiricalDiagonal=np.trace(cov),
                independentInputFull=variance*full, independentInputDiagonal=variance*diagonal,
                outputBlocks=len(blocks))


def load_tiles(fits, filename, flat_receipts, tiles, saturation):
    assert len(flat_receipts) == 15
    images = []
    with ZipFile(filename) as archive:
        for row in flat_receipts[:14]:
            raw = archive.read(row["file"])
            assert digest(raw) == row["sha256"]
            with fits.open(BytesIO(raw), memmap=False, uint=True) as hdus:
                img, header = hdus[0].data, hdus[0].header
                assert (header["DATE-OBS"], header["IMAGETYP"], header["EXPTIME"]) == (row["date"], "Flat", 3)
                assert (header["BAYERPAT"], header["GAIN"], header["OFFSET"]) == ("RGGB", 100, 50)
                assert img.shape == (4176, 6248)
                selected = [img[y-64:y+64,x-64:x+64].copy() for x, y in tiles]
                assert all(tile.shape == (128,128) and tile.max() < saturation for tile in selected)
                images.append(selected)
    return images


def calculate(np, phases, halves, images, previous):
    assert halves == [[0, 30], [34, 64]]
    phase_ops = [operators(np, fx, fy) for fx, fy in phases]
    assert phase_ops[0] == (4, 4) and phase_ops[3] == (2.25, 1)
    bands = {"R": (0,0), "G1": (0,1), "G2": (1,0), "B": (1,1)}
    prior_ratios = {(r["pair"],r["tile"],r["band"]):r["blockVarianceRatio"] for r in previous["flat"]}
    assert len(prior_ratios) == 252
    baseline = {}
    for tile in range(9):
        for band in bands:
            seq = [r["meanAdu"] for r in previous["shortDark"]
                   if r["tile"] == tile and r["band"] == band and r["status"] == "MEASURED"]
            assert len(seq) == 7
            baseline[tile, band] = np.median(seq)
    cx, cy = np.meshgrid(np.linspace(-1, 1, 64), np.linspace(-1, 1, 64))
    design = np.stack((np.ones_like(cx), cx, cy), axis=-1)
    strata = [(i//3 + i%3) % 2 for i in range(9)]
    rows = []
    for pair, index in enumerate(range(0,14,2)):
        for band, (r,c) in bands.items():
            first, second = ([t[r::2,c::2].astype(float)-baseline[tile, band] for tile,t in enumerate(images[i])]
                             for i in (index, index+1))
            assert min(a.mean() for a in first + second) > 0
            ratios = [b.mean()/a.mean() for a,b in zip(first,second,strict=True)]
            for tile, (a,b) in enumerate(zip(first,second,strict=True)):
                scale = np.median([ratio for i,ratio in enumerate(ratios) if strata[i] != strata[tile]])
                raw = (b-a)/np.sqrt(2.)
                cov = np.cov(block_rows(raw), rowvar=False, ddof=1)
                np.testing.assert_allclose(cov.sum()/np.trace(cov),prior_ratios[pair,tile,band],atol=1e-12,rtol=0.)
                scaled = (b-scale*a)/np.sqrt(1.+scale**2)
                for fold, (lo,hi) in enumerate(halves):
                    train_lo,train_hi = halves[1-fold]
                    fitted,_,rank,_ = np.linalg.lstsq(design[:,train_lo:train_hi].reshape(-1,3),
                                                     scaled[:,train_lo:train_hi].ravel(),rcond=None)
                    assert rank == 3
                    sub = scaled[:,lo:hi]
                    modes = dict(raw=raw[:,lo:hi], scaled=sub, plane=sub-design[:,lo:hi] @ fitted)
                    for iphase, ((fx,fy),(full,diag)) in enumerate(zip(phases,phase_ops,strict=True)):
                        rows.append(dict(pair=pair,tile=tile,band=band,fold=fold,phaseIndex=iphase,
                                         illuminationScale=scale,
                                         modes={mode:measure(np,img,fx,fy,full,diag) for mode,img in modes.items()}))
    return rows


def summarize(np, rows, phases):
    results = []
    for i,phase in enumerate(phases):
        selected = [r for r in rows if r["phaseIndex"] == i]
        assert len(selected) == 504
        modes = {}
        for key in ("raw","scaled","plane"):
            values = [r["modes"][key] for r in selected]
            empirical = np.array([v["empirical"] for v in values])
            full = np.abs(np.array([v["independentInputFull"] for v in values])/empirical-1)
            diag = np.abs(np.array([v["independentInputDiagonal"] for v in values])/empirical-1)
            ratio = empirical/np.array([v["empiricalDiagonal"] for v in values])
            modes[key] = dict(empiricalSumToDiagonalMedian=float(np.median(ratio)),
                              fullRelativeErrorMedian=float(np.median(full)),
                              fullRelativeErrorP95=float(np.quantile(full,.95)),
                              diagonalRelativeErrorMedian=float(np.median(diag)),
                              fullWithinTenPercent=int(np.count_nonzero(full<=.1)),
                              diagonalWithinTenPercent=int(np.count_nonzero(diag<=.1)))
        results.append(dict(phaseXY=phase,measurements=len(selected),modes=modes))
    return results


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("protocol","prior","flat","dependencies","output"):
        cli.add_argument(name,type=Path)
    args = cli.parse_args()
    raw = args.protocol.read_bytes()
    cfg = json.loads(raw)
    assert cfg["schema"] == "BKL046_ASI2600MC_FLAT_BILINEAR_PROTOCOL_V1"
    old = pinned(args.prior/"riscontro.json",cfg["priorReportSha256"])
    previous = pinned(args.prior/"tutti-gli-esiti.json",cfg["priorFullSha256"])
    assert old["fullReportSha256"] == cfg["priorFullSha256"]
    plan = pinned(args.prior/"protocollo.json",old["protocolSha256"])
    receipt = pinned(args.prior/"calibration-receipt.json",plan["calibrationReceiptSha256"])
    with args.flat.open("rb") as f:
        assert file_digest(f,"sha256").hexdigest() == cfg["flatArchiveSha256"] == plan["archivePins"]["flat"]
    sys.path.insert(0,str(args.dependencies))
    import astropy
    from astropy.io import fits
    import numpy as np
    assert (np.__version__,astropy.__version__) == ("2.3.5","7.2.0")
    images = load_tiles(fits,args.flat,receipt["sourceMembers"]["flat"],old["tiles"],plan["rejectAtOrAbove"])
    rows = calculate(np,cfg["phaseXY"],cfg["parityColumns"],images,previous)
    args.output.mkdir()
    full = (json.dumps(rows,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
    (args.output/"tutti-gli-esiti.json").write_bytes(full)
    report = dict(schema="BKL046_ASI2600MC_FLAT_BILINEAR_RESULT_V1",protocolSha256=digest(raw),
                  programSha256=digest(Path(__file__).read_bytes()),fullReportSha256=digest(full),
                  pairTileParityCases=252,heldOutFlatFrames=1,rows=len(rows),outputsPerMode=434,
                  summary=summarize(np,rows,cfg["phaseXY"]),nativeExecutions=0,scientificClosures=0)
    with (args.output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as f:
        json.dump(report,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()