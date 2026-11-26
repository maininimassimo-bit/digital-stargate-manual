"""Evaluate fixed covariance weights without selecting on held ASI2600MC pairs."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("protocol", "held_study", "parent_study", "flat_archive", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import astropy
from astropy.io import fits
import numpy as np
assert (astropy.__version__, np.__version__) == ("7.2.0", "2.3.5")


def pinned(path, digest):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == digest, path.name
    return raw


pin = "2f0ffc69547af4bb50a5aa9ad1256973affcbe9ea4c87cdb9b33f5fc64b7f0f9"
cfg = json.loads(pinned(args.protocol, pin))
old = args.held_study
old_cfg = json.loads(pinned(old/"protocollo.json", cfg["oldProtocolSha256"]))
parent_dir = args.parent_study
parent_cfg = json.loads(pinned(parent_dir/"protocollo.json", old_cfg["parentProtocolSha256"]))
parent_rows = json.loads(pinned(parent_dir/"misure/tutti-gli-esiti.json", old_cfg["parentReportSha256"]))
old_results = json.loads(pinned(old/"misure/tutti-gli-esiti.json", cfg["oldFullResultsSha256"]))
parent_source = pinned(parent_dir/"misura.py", old_cfg["parentProgramSha256"])
parent_ns = {"__name__":"pinned_flat_bilinear"}
exec(compile(parent_source, str(parent_dir/"misura.py"), "exec"), parent_ns)

older = parent_dir/"prior"
summary = json.loads(pinned(older/"riscontro.json", parent_cfg["priorReportSha256"]))
data = json.loads(pinned(older/"tutti-gli-esiti.json", parent_cfg["priorFullSha256"]))
base_plan = json.loads(pinned(older/"protocollo.json", summary["protocolSha256"]))
receipt = json.loads(pinned(older/"calibration-receipt.json", base_plan["calibrationReceiptSha256"]))
with args.flat_archive.open("rb") as stream:
    assert file_digest(stream, "sha256").hexdigest() == parent_cfg["flatArchiveSha256"] == base_plan["archivePins"]["flat"]
tiles = parent_ns["load_tiles"](fits,args.flat_archive,receipt["sourceMembers"]["flat"],
                                summary["tiles"],base_plan["rejectAtOrAbove"])

verified = pinned(old/"misura.py", cfg["oldSourceSha256"]).decode()
anchor = '            modes[mode] = dict(independentError=abs(reference/empirical-1),learnedError=abs(learned/empirical-1))'
assert verified.count(anchor) == 1
verified = verified.replace(anchor, anchor + "\n            TRACE.append((pair, tile, band, fold, i, mode, reference, learned, empirical))")
old_ns = {"__name__":"pinned_held_covariance", "TRACE":[]}
exec(compile(verified,str(old/"misura.py"),"exec"),old_ns)
phase = parent_cfg["phaseXY"]
matrices = old_ns["shapes"](np,tiles,data,parent_cfg["parityColumns"])
observed_old = old_ns["compare"](np,parent_rows,matrices,phase)
assert observed_old == old_results and len(observed_old) == 2520
trace = old_ns["TRACE"]
assert len(trace) == 7560
result = []
weights = cfg["covarianceWeights"]
for phase_index, xy in enumerate(phase):
    for mode in ("raw","scaled","plane"):
        block = [x for x in trace if x[4] == phase_index and x[5] == mode]
        assert len(block) == 504
        p = np.asarray([row[0] for row in block])
        reference, empirical_covariance, measured = np.asarray([row[6:] for row in block]).T
        assert np.all(measured > 0)
        control_error = np.abs(reference/measured-1)
        control_pair = [float(np.median(control_error[p==i])) for i in range(7)]
        proposals = []
        for weight in weights:
            mixed = (1-weight)*reference + weight*empirical_covariance
            signed_error = mixed/measured - 1
            error = np.abs(signed_error)
            medians = [float(np.median(error[p==i])) for i in range(7)]
            proposals.append(dict(covarianceWeight=weight, medianError=float(np.median(error)),
                                  signedMedianError=float(np.median(signed_error)),
                                  p95Error=float(np.quantile(error,.95)),
                                  within10=int(np.count_nonzero(error<=cfg["successToleranceForComparability"])),
                                  pairMedians=medians, pairMediansImprovedVsIndependence=sum(
                                      a < b for a,b in zip(medians,control_pair,strict=True))))
        result.append(dict(phaseXY=xy, mode=mode, observations=len(block), weights=proposals))

assert len(result) == 15
report = dict(protocol="BKL046_ASI2600MC_FLAT_COVARIANCE_SHRINK_DEVELOPMENT_V1",
              protocolSha256=pin, priorFullResultsSha256=cfg["oldFullResultsSha256"],
              originalHeldOutResultsReproduced=True, exposurePairs=7, observationsPerCombination=504,
              anyWeightSelected=False, results=result,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf-8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
