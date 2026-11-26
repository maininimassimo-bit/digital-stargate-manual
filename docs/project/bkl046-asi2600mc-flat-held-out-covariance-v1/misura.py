"""Predict bilinear flat variance using covariance learned on other exposure pairs."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys
from types import ModuleType


def digest(data):
    return sha256(data).hexdigest()


def checked(path, pin):
    raw = path.read_bytes()
    if digest(raw) != pin:
        raise ValueError(f"SHA-256 differs: {path.name}")
    return raw


def weight_vector(np, fx, fy):
    kernel = np.outer([1-fy, fy], [1-fx, fx])
    w = np.zeros((3,3))
    for y in range(2):
        for x in range(2):
            w[y:y+2,x:x+2] += kernel
    return w.ravel()


def shapes(np, images, previous, halves):
    bands = {"R": (0,0), "G1": (0,1), "G2": (1,0), "B": (1,1)}
    baseline = {}
    for tile in range(9):
        for band in bands:
            seq = [row["meanAdu"] for row in previous["shortDark"] if row["tile"] == tile
                   and row["band"] == band and row["status"] == "MEASURED"]
            assert len(seq) == 7
            baseline[tile,band] = np.median(seq)
    cx, cy = np.meshgrid(np.linspace(-1,1,64), np.linspace(-1,1,64))
    design = np.stack((np.ones_like(cx),cx,cy),axis=-1)
    strata = [(i//3+i%3)%2 for i in range(9)]
    matrices = {}
    for pair,index in enumerate(range(0,14,2)):
        for band,(r,c) in bands.items():
            first,second = ([tile[r::2,c::2].astype(float)-baseline[i,band]
                             for i,tile in enumerate(images[k])] for k in (index,index+1))
            assert min(tile.mean() for tile in first+second) > 0
            ratios = [b.mean()/a.mean() for a,b in zip(first,second,strict=True)]
            for tile,(a,b) in enumerate(zip(first,second,strict=True)):
                scale = np.median([v for k,v in enumerate(ratios) if strata[k] != strata[tile]])
                scaled = (b-scale*a)/np.sqrt(1+scale**2)
                raw = (b-a)/np.sqrt(2)
                for fold,(lo,hi) in enumerate(halves):
                    start,stop = halves[1-fold]
                    coeff,_,rank,_ = np.linalg.lstsq(design[:,start:stop].reshape(-1,3),
                                                    scaled[:,start:stop].ravel(),rcond=None)
                    assert rank == 3
                    sub = scaled[:,lo:hi]
                    modes = dict(raw=raw[:,lo:hi],scaled=sub,plane=sub-design[:,lo:hi]@coeff)
                    for mode,img in modes.items():
                        v = img[:63,:29]
                        sample = v[:,:27].reshape(21,3,9,3).swapaxes(1,2).reshape(189,9)
                        cov = np.cov(sample,rowvar=False,ddof=1)
                        cov = cov/(np.trace(cov)/9)
                        assert np.linalg.eigvalsh(cov)[0] >= -1e-12
                        matrices[pair,tile,band,fold,mode] = (cov,float(np.var(v,ddof=1)))
    return matrices


def compare(np, source_rows, matrices, phases):
    results = []
    for row in source_rows:
        pair,tile,band,fold,i = (row[k] for k in ("pair","tile","band","fold","phaseIndex"))
        w = weight_vector(np,*phases[i])
        modes = {}
        for mode,m in row["modes"].items():
            held_key = (pair,tile,band,fold,mode)
            train = [matrices[(k,tile,band,fold,mode)][0] for k in range(7) if k != pair]
            assert len(train) == 6
            var = matrices[held_key][1]
            empirical = m["empirical"]
            reference = m["independentInputFull"]
            np.testing.assert_allclose(var*(w@w),reference,rtol=1e-12,atol=1e-10)
            learned = var*(w @ np.mean(train,axis=0) @ w)
            assert learned > 0
            modes[mode] = dict(independentError=abs(reference/empirical-1),learnedError=abs(learned/empirical-1))
        results.append(dict(pair=pair,tile=tile,band=band,fold=fold,phaseIndex=i,modes=modes))
    return results


def summarize(np, rows, phases):
    summary = []
    for i,phase in enumerate(phases):
        group = [row for row in rows if row["phaseIndex"] == i]
        assert len(group) == 504
        out = {}
        for mode in ("raw","scaled","plane"):
            a = np.array([row["modes"][mode]["independentError"] for row in group])
            b = np.array([row["modes"][mode]["learnedError"] for row in group])
            pair = np.array([row["pair"] for row in group])
            pairs = [dict(pair=p, independentMedian=float(np.median(a[pair==p])),
                          learnedMedian=float(np.median(b[pair==p]))) for p in range(7)]
            out[mode] = dict(independentMedian=float(np.median(a)),learnedMedian=float(np.median(b)),
                             independentP95=float(np.quantile(a,.95)),learnedP95=float(np.quantile(b,.95)),
                             independentWithin10=int(np.count_nonzero(a<=.1)),learnedWithin10=int(np.count_nonzero(b<=.1)),
                             lowerPairMedians=sum(p["learnedMedian"] < p["independentMedian"] for p in pairs),
                             pairMedians=pairs)
        summary.append(dict(phaseXY=phase,modes=out))
    return summary


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("protocol","source","dependencies","output"):
        cli.add_argument(name,type=Path)
    args = cli.parse_args()
    raw = args.protocol.read_bytes()
    cfg = json.loads(raw)
    src = args.source
    parent = ModuleType("parent")
    program = src/"misura.py"
    exec(compile(checked(program,cfg["parentProgramSha256"]),str(program),"exec"),vars(parent))
    protocol = json.loads(checked(src/"protocollo.json",cfg["parentProtocolSha256"]))
    rows = json.loads(checked(src/"misure"/"tutti-gli-esiti.json",cfg["parentReportSha256"]))
    prior = src/"prior"
    old = parent.pinned(prior/"riscontro.json",protocol["priorReportSha256"])
    previous = parent.pinned(prior/"tutti-gli-esiti.json",protocol["priorFullSha256"])
    plan = parent.pinned(prior/"protocollo.json",old["protocolSha256"])
    receipt = parent.pinned(prior/"calibration-receipt.json",plan["calibrationReceiptSha256"])
    flat = src/"Flats_3s.zip"
    with flat.open("rb") as f:
        assert file_digest(f,"sha256").hexdigest() == protocol["flatArchiveSha256"] == plan["archivePins"]["flat"]
    sys.path.insert(0,str(args.dependencies))
    import astropy
    from astropy.io import fits
    import numpy as np
    assert (np.__version__,astropy.__version__) == ("2.3.5","7.2.0")
    phases,halves = protocol["phaseXY"],protocol["parityColumns"]
    for phase in phases:
        w = weight_vector(np,*phase)
        np.testing.assert_allclose(w @ np.eye(9) @ w,parent.operators(np,*phase)[0],rtol=1e-12)
        np.testing.assert_allclose(w @ np.ones((9,9)) @ w,16,rtol=1e-12)
    images = parent.load_tiles(fits,flat,receipt["sourceMembers"]["flat"],old["tiles"],plan["rejectAtOrAbove"])
    matrices = shapes(np,images,previous,halves)
    assert len(matrices) == 1512 and len(rows) == 2520
    results = compare(np,rows,matrices,phases)
    args.output.mkdir()
    full = (json.dumps(results,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
    (args.output/"tutti-gli-esiti.json").write_bytes(full)
    report = dict(schema=cfg["schema"],protocolSha256=digest(raw),programSha256=digest(Path(__file__).read_bytes()),
                  parentReportSha256=cfg["parentReportSha256"],fullReportSha256=digest(full),
                  heldOutPairs=7,trainingPairsPerFold=6,trainingBlocksPerSourceMatrix=189,
                  summary=summarize(np,results,phases),nativeExecutions=0,scientificClosures=0)
    with (args.output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as f:
        json.dump(report,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()