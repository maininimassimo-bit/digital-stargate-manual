from importlib.util import module_from_spec,spec_from_file_location
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

root,oracle,comparator,deps,out=map(Path,sys.argv[1:])
spec=spec_from_file_location("origin",root/"classifica.py")
mod=module_from_spec(spec)
spec.loader.exec_module(mod)
plan=json.loads((root/"piano.json").read_bytes())
report=json.loads((oracle/"riscontro.json").read_bytes())
tests=[]

def populate(path,sequence):
    for case,mapping in zip(plan["cases"],sequence,strict=True):
        for kind in plan["fitsKinds"]:
            shutil.copyfile(oracle/"oracoli"/f"{mapping}-{kind}.fits",path/f"{case['id']}-{kind}.fits")

def check(label, sequence, problem=None):
    with TemporaryDirectory(dir=out.parent,prefix="scenario-") as work:
        folder=Path(work)
        populate(folder,sequence)
        if problem=="missing":
            (folder/"zero-origin0-rgb.fits").unlink()
        elif problem=="extra":
            shutil.copyfile(folder/"zero-origin0-rgb.fits",folder/"extra.fits")
        elif problem=="mismatched":
            shutil.copyfile(oracle/"oracoli"/"half-matrix-as-zero-weight.fits",folder/"zero-origin0-weight.fits")
        elif problem=="nonfinite":
            from astropy.io import fits
            f=folder/"zero-origin0-rgb.fits"
            with fits.open(f,mode="update",memmap=False) as hdus:
                hdus[0].data[0,0,0]=float("nan")
        try:
            result=mod.run(root,oracle,comparator,deps,folder)
        except ValueError as err:
            expect="NONFINITE_OR_NONFLOAT:zero-origin0-rgb.fits" if problem=="nonfinite" else "OUTPUT_NAMESPACE_DIFFERS"
            assert problem in {"missing","extra","nonfinite"} and str(err)==expect
            tests.append({"case":label,"status":"REJECTED_INPUT","reason":str(err)})
            return
        expect={"unmodeled":"UNMODELED_SEQUENCE","mismatched":"UNRESOLVED_CASE"}.get(problem,"MATCHED_TESTED_HYPOTHESIS")
        assert result["status"]==expect and result["hypotheses"]==([label] if problem is None else [])
        tests.append({"case":label,"status":expect,"hypotheses":result["hypotheses"]})

for label,sequence in report["predictedSignatures"].items():
    check(label,sequence)
check("all-baseline",["baseline"]*4,"unmodeled")
for problem in ("mismatched","missing","extra","nonfinite"):
    check(problem,report["predictedSignatures"]["use-declared"],problem)
out.write_bytes((json.dumps({"schema":"BKL046_CFA_ORIGIN_CLASSIFIER_FIXTURE_V1","cases":tests,
                            "nativeExecutions":0,"admissionRequested":False},indent=2,sort_keys=True)+"\n").encode())
