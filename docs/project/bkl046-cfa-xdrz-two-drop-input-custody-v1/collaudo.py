from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import shutil
import sys
from tempfile import TemporaryDirectory

source,batch,archive,primitive,out=map(Path,sys.argv[1:])
module=runpy.run_path(str(source),run_name="isolated_custody")
plan,expected=module["verified_sources"](batch)
actual={k:Path(v) for k,v in module["ROOTS"].items()}
hold=module["hold_inputs"]

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def fixture(base,mode):
    roots={}
    for group in expected:
        parent=base/group
        parent.mkdir()
        dest=parent/"input"
        dest.mkdir()
        roots[group]=dest
        for name in expected[group]:
            if mode=="missing-fits" and group=="fractional" and name=="integer-b-cfa.fits":
                continue
            shutil.copyfile(actual[group]/name,dest/name)
    return roots

deny=0
reports=[]
for mode in ("good","changed-xdrz","missing-fits","writer-already-open"):
    with TemporaryDirectory(dir=out.parent,prefix="custody-") as scratch:
        roots=fixture(Path(scratch),mode)
        guarded=roots["fractional"]/"integer-b-cfa.fits"
        if mode=="changed-xdrz":
            target=roots["fractional"]/"integer-b-unmasked.xdrz"
            target.write_bytes(target.read_bytes()+b"\n")
        writer=guarded.open("r+b") if mode=="writer-already-open" else None
        try:
            try:
                with hold(plan,expected,roots,primitive):
                    require(mode=="good","Unexpectedly held invalid inputs")
                    for group,catalog in expected.items():
                        for name,sha in catalog.items():
                            path=roots[group]/name
                            require(sha256(path.read_bytes()).hexdigest()==sha,"Changed held read")
                            try:
                                with path.open("r+b"):
                                    pass
                            except OSError as e:
                                require(e.errno==13,"Unexpected write denial")
                                deny+=1
                            else:
                                raise AssertionError("A write handle was granted")
            except (OSError,ValueError) as error:
                correct = {
                    "changed-xdrz":"Input changed:",
                    "missing-fits":"Input member missing",
                    "writer-already-open":"WinError 32",
                }
                require(mode in correct and correct[mode] in str(error),f"Unexpected scenario failure: {error}")
                reports.append(dict(case=mode,enteredCustody=False))
            else:
                require(mode=="good","Failure scenario accepted")
        finally:
            if writer:
                writer.close()
        for item in roots["integer"].iterdir():
            with item.open("r+b") as stream:
                require(sha256(stream.read()).hexdigest()==expected["integer"][item.name],
                        "Premature custody release changed inputs")
        if mode=="good":
            for item in roots["fractional"].iterdir():
                with item.open("r+b") as stream:
                    require(sha256(stream.read()).hexdigest()==expected["fractional"][item.name],
                            "Fractional source changed after release")

with TemporaryDirectory(dir=out.parent,prefix="stage-test-") as scratch:
    target=Path(scratch)/"input"
    stage=module["stage_fractional"]
    require(stage(archive,target,expected["fractional"]),"Initial stage did not materialize")
    require(not stage(archive,target,expected["fractional"]),"Idempotent stage was replaced")
    invalid=target/"integer-a-cfa.fits"
    corrupt=invalid.read_bytes()+b"\n"
    invalid.write_bytes(corrupt)
    try:
        stage(archive,target,expected["fractional"])
    except ValueError:
        require(invalid.read_bytes()==corrupt,"Corrupt stage was overwritten")
        reports.append(dict(case="staged-content-changed",enteredCustody=False))
    else:
        raise ValueError("Corrupt existing stage was accepted")

try:
    module["build_ephemeral_intent"]({},batch,Path(),Path(),Path())
except ValueError as error:
    require("Unexpected parent binding" in str(error),"Wrong binding rejection")
    reports.append(dict(case="wrong-parent-binding",enteredCustody=False))
else:
    raise ValueError("Foreign binding accepted")

module["write_report"](out,dict(schema="BKL046_TWO_DROP_NTFS_INPUT_CUSTODY_V1",writeHandlesDenied=deny,
    directReadsWhileHeld=24,inputCatalog={k:len(v) for k,v in expected.items()},writeHandlesAfterClose=24,
    negatives=reports,nativeExecutions=0,admissionRequested=False,scientificClosures=0))
