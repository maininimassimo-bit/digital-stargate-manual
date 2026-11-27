from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
from threading import Event, Thread
import time

root,batch,out=map(Path,sys.argv[1:])
sys.path.insert(0,str(root))
from padre import run_owned
from prepara import ROOTS, verified_sources, write_report

plan,rosters=verified_sources(batch)
primitive=root/"windows-hold.py"
reservation="52d471bc-3d3d-42ea-ad47-29146dbd36a5"


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def write_denied(file):
    try:
        with file.open("r+b"):
            pass
    except OSError as error:
        require(error.errno==13,"Unexpected write-open failure")
        return True
    raise ValueError("Unexpected write access while child was live")


def run_case(mode):
    with TemporaryDirectory(dir=out.parent,prefix="witness-") as directory:
        scope=Path(directory)
        roots={}
        names=[]
        for group in rosters:
            paths=scope/group/"input"
            paths.mkdir(parents=True)
            roots[group]=paths
            for name in rosters[group]:
                target=paths/name
                shutil.copyfile(Path(ROOTS[group])/name,target)
                names.append(target)
        if mode=="bad-input":
            names[-1].write_bytes(names[-1].read_bytes()+b"\n")
        run=scope/reservation
        ready,allow_exit=scope/"running.json",scope/"allow-exit"
        script=b"// isolated lifecycle witness\n"
        prepared={"value":False}
        observed=Event()
        checked={}

        def prepare():
            prepared["value"]=True
            return (dict(reservation=reservation,scriptSha256=sha256(script).hexdigest(),
                         runDirectory=str(run),scriptPath=str(run/"batch-entry.js")),script)

        def command(_):
            return [sys.executable,"-I","-B","-S",str(root/"figlio-test.py"),str(ready),str(allow_exit)]

        def parent_work(intent, work, original):
            checked["original"]=original.identity
            observed.set()
            if mode=="parent-error":
                raise RuntimeError("INJECTED_READINESS_FAILURE")
            require(original.wait(15)["exitCode"]==0,"Witness did not exit cleanly")
            return True

        def monitor():
            try:
                require(observed.wait(7),"Original handle not observed")
                end=time.monotonic()+7
                while not ready.exists() and time.monotonic()<end:
                    time.sleep(.02)
                require(ready.is_file(),"Test child did not report readiness")
                require(json.loads(ready.read_bytes())["pid"]==checked["original"]["pid"],
                        "Observed witness was not the original")
                if mode=="parent-error":
                    time.sleep(.25)
                checked["deny"]=sum(write_denied(file) for file in names+[run/"batch-entry.js"])
            except BaseException as error:
                checked["error"]=error
            finally:
                allow_exit.touch()

        worker=None
        if mode!="bad-input":
            worker=Thread(target=monitor)
            worker.start()
        try:
            try:
                result=run_owned(plan,rosters,roots,primitive,prepare,command,parent_work)
            except (RuntimeError,ValueError) as error:
                if mode=="parent-error":
                    require(str(error)=="INJECTED_READINESS_FAILURE","Original cause was lost")
                elif mode=="bad-input":
                    require("Input changed:" in str(error) and not prepared["value"] and not run.exists(),
                            "Input mismatch reached launch preparation")
                else:
                    raise
            else:
                require(mode=="normal" and result is True,"Unexpected parent result")
        finally:
            if worker:
                worker.join(timeout=15)
                require(not worker.is_alive(),"Controller did not stop")
        if worker:
            if "error" in checked:
                raise checked["error"]
            require(checked.get("deny")==25,"Incomplete input/entrypoint protection")
            for file in names+[run/"batch-entry.js"]:
                with file.open("r+b"):
                    pass
        return dict(case=mode,deniedWhileLive=checked.get("deny",0),preparationReached=prepared["value"],
                    writableAfterExit=25 if worker else 0)


write_report(out,dict(schema="BKL046_TWO_DROP_PARENT_INPUT_LIFECYCLE_FIXTURES_V1",
    cases=[run_case(mode) for mode in ("normal","parent-error","bad-input")],
    realWindowsWitness=True,operationalR4RegistryAccessed=False,admissionRequested=False,
    nativeExecutions=0,scientificClosures=0))
