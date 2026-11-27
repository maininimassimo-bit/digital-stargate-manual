"""Validate covariance transfer across disjoint camera acquisition series."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("protocol", "previous", "calibrator_receipts", "fits_archives", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np
assert np.__version__ == "2.3.5"


def pinned(path, digest):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == digest, path.name
    return raw


pin = "1df6b44076693cc02a484b70459a7c514348bd447c8de314b831997a7f2b0981"
plan = json.loads(pinned(args.protocol,pin))
old_program = args.previous/"misura.py"
old_plan = args.previous/"protocollo.json"
source = pinned(old_program, plan["oldProgramSha256"]).decode("utf-8")
phases = json.loads(pinned(old_plan,plan["oldProtocolSha256"]))["phaseXY"]
canonical = json.loads(pinned(args.previous/"tutti-gli-esiti.json",plan["oldResultsSha256"]))
matrices = {}


def capture(key, pair, tile, band, plane):
    assert plane.shape == (63,63)
    blocks = plane.reshape(21,3,21,3).transpose(0,2,1,3).reshape(441,9)
    cov = np.cov(blocks,rowvar=False,ddof=1)
    assert np.linalg.eigvalsh(cov)[0] >= -1e-10
    ident = (key,pair,tile,band)
    assert ident not in matrices
    matrices[ident] = cov/(np.trace(cov)/9)


anchor = "                    raw_variance = np.var(v,ddof=1)"
assert source.count(anchor) == 1
traced = source.replace(anchor,anchor+"\n                    CAPTURE(key,pair,tile,band,v)")
space = {"__name__":"verified_previous", "__file__":str(old_program), "CAPTURE":capture}
exec(compile(traced,str(old_program),"exec"),space)
args.output.mkdir()
probe = args.output/"prior-replay"
probe.mkdir()
previous_args = sys.argv
try:
    sys.argv = [str(old_program),*[str(p) for p in (
        old_plan,args.calibrator_receipts,args.fits_archives,args.packages,probe)]]
    space["main"]()
finally:
    sys.argv = previous_args
assert json.loads(pinned(probe/"tutti-gli-esiti.json",plan["oldResultsSha256"])) == canonical
assert len(matrices) == 2*7*9*4


def kernel(phase):
    fx,fy = phase
    weights = np.zeros((3,3))
    for y in range(2):
        for x in range(2):
            weights[y:y+2,x:x+2] += np.outer([1-fy,fy],[1-fx,fx])
    return weights.ravel()


donors = {
    (mode,tile,band):np.mean([matrices[mode,k,tile,band] for k in range(7)],axis=0)
    for mode in canonical for tile in range(9) for band in ("R","G1","G2","B")
}
rows = []
for target,source_mode in [("dark","shortDark"),("shortDark","dark")]:
    for index,phase in enumerate(phases):
        w = kernel(phase)
        group = [row for row in canonical[target] if row["phaseIndex"] == index]
        records = []
        for r in group:
            pair,tile,band = (r[k] for k in ("pair","tile","band"))
            variance = r["inputVarianceAdu2"]
            reference = variance*(w @ w)
            assert np.isclose(reference,r["independentInputFullAdu2"],rtol=1e-12)
            within = np.mean([matrices[target,j,tile,band] for j in range(7) if j != pair],axis=0)
            transfer = variance*(w @ donors[source_mode,tile,band] @ w)
            same = variance*(w @ within @ w)
            measured = r["empiricalAdu2"]
            assert measured>0 and transfer>0 and same>0
            predictions = {"independent_input":reference,"within_series_covariance":same}
            for weight in plan["weights"][1:]:
                predictions[f"cross_series_weight_{weight:g}"] = (1-weight)*reference+weight*transfer
            records.append((pair,{k:abs(v/measured-1) for k,v in predictions.items()}))
        assert len(records)==252
        output = {}
        for label in records[0][1]:
            errors=np.asarray([r[1][label] for r in records])
            medians=[float(np.median([r[1][label] for r in records if r[0]==j])) for j in range(7)]
            output[label]=dict(median=float(np.median(errors)),p95=float(np.quantile(errors,.95)),
                               pairMedians=medians, within10=int(np.count_nonzero(errors<=.1)))
        rows.append(dict(target=target,covarianceSource=source_mode,phaseXY=phase,details=output))

payload = dict(protocol=plan["schema"],protocolSha256=pin,priorResultSha256=plan["oldResultsSha256"],
               originalResultsReproduced=True,targetCovarianceComparisonUsesDisjointFrames=True,
               crossSeriesDonorPairs=7, withinSeriesOtherPairs=6,
               anyWeightSelected=False, rows=rows,nativeExecutions=0,scientificClosures=0)
with (args.output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as f:
    json.dump(payload,f,indent=2,allow_nan=False)
    f.write("\n")
