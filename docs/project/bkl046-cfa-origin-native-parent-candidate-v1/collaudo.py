import io
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

base,fixtures,out=map(Path,sys.argv[1:])
sys.path.insert(0,str(base/"moduli"))
import parent_origine as mod
from hashlib import sha256

rid="348eaf20-c65c-438c-b808-eb1c163f9a31"
binding={"operation":mod.prepara.OPERATION,"reservation":rid,"casePlanSha256":mod.prepara.PLAN_PIN,
         "subjectSha256":mod.prepara.BATCH_PIN}
real_stage,real_hold=mod.stage,mod.hold_inputs

def denied(path):
    try:
        with path.open("r+b"):
            pass
    except OSError as e:
        assert e.errno==13
    else:
        raise AssertionError("write access opened while held")

cases=[]
for mode,reason in (
    ("valid",None),
    ("changed-entry","STAGED_ENTRY_BYTES_DIFFERS"),
    ("records-changed","R4_RECORDS_CHANGED_BEFORE_LAUNCH"),
    ("spawn-exception","TEST_SPAWN_FAILED"),
    ("image-differs","TEST_IMAGE_DIFFERS"),
):
    with TemporaryDirectory(dir=base,prefix="fixture-") as directory:
        root=Path(directory)
        inputs={}
        for name in ("fits","xdrz"):
            inputs[name]=root/name
            shutil.copytree(fixtures/name,inputs[name])
        mod.prepara.ROOT=root
        native_entry=root/rid/"batch-entry.js"
        proof=root/"fits"/"shear-a-cfa.fits"
        calls=[]
        def scratch_hold(stack):
            manifest=json.loads((fixtures/"batch-manifest.json").read_bytes())
            calls.append("hold-inputs")
            assert mod.hold(stack,manifest["xdrzSha256"],inputs["xdrz"],vars(mod.archive_hold),".xdrz")==12
            assert mod.hold(stack,manifest["fitsInputsSha256"],inputs["fits"],vars(mod.archive_hold),".fits")==6
        mod.hold_inputs=scratch_hold
        def staging(intent,entry,path):
            target=real_stage(intent,entry,path)
            if mode=="changed-entry":
                target.write_bytes(entry+b" ")
            calls.append("stage")
            return target
        mod.stage=staging
        def revalidate():
            denied(native_entry)
            denied(proof)
            calls.append("check-r4")
            if mode=="records-changed":
                raise RuntimeError("R4_RECORDS_CHANGED_BEFORE_LAUNCH")
        class Intercepted:
            child=None
            def launch(self,command,**kwargs):
                assert command[0]=="C:/Program Files/PixInsight/bin/PixInsight.exe"
                assert command[-1]=="-r="+native_entry.as_posix()
                assert kwargs["cwd"]==native_entry.parent
                denied(native_entry)
                denied(proof)
                calls.append("intercept-spawn")
                if mode=="spawn-exception":
                    raise RuntimeError("TEST_SPAWN_FAILED")
                self.child=object()
            def wait_observation(self,_):
                denied(native_entry)
                denied(proof)
                calls.append("observe-original")
                return {"exitCode":0}
        mod.OriginalChildCustody=Intercepted
        mod.OriginalHandleWitness=lambda owner:owner.child
        def verify_image(child,path,pin):
            assert child is not None and path.name=="PixInsight.exe"
            assert pin=="76d2339130b58be3d112b66cafc578d9f859d80c96842b2ba2dfbbdcdc8b2943"
            calls.append("verify-image")
            if mode=="image-differs":
                raise ValueError("TEST_IMAGE_DIFFERS")
        mod.verify_image=verify_image
        def ready(intent,run,child,health,timeout):
            assert intent["reservation"]==rid and run==native_entry.parent and timeout==300 and child is not None
            health()
            calls.append("ready")
            return {"reservation":rid},object()
        mod.await_ready=ready
        def serve(run,ready,bridge,child,_frames,_events):
            assert run==native_entry.parent and ready=={"reservation":rid} and bridge and child
            calls.append("serve")
        mod.serve=serve
        try:
            mod.execute_bound(binding,io.BytesIO(),io.StringIO(),revalidate)
            assert reason is None
        except (RuntimeError,ValueError) as e:
            if str(e)!=reason:
                raise
        expected={
            "changed-entry":["hold-inputs","stage"],
            "records-changed":["hold-inputs","stage","check-r4"],
            "spawn-exception":["hold-inputs","stage","check-r4","intercept-spawn"],
            "image-differs":["hold-inputs","stage","check-r4","intercept-spawn","verify-image","observe-original"],
            "valid":["hold-inputs","stage","check-r4","intercept-spawn","verify-image","ready","serve","observe-original"],
        }
        assert calls==expected[mode],calls
        for p in (proof,native_entry):
            with p.open("r+b"):
                pass
        cases.append({"case":mode,"calls":calls,"failure":reason})
report={"schema":"BKL046_CFA_ORIGIN_NATIVE_PARENT_DRY_TEST_V1","cases":cases,
        "originalAppSpawnIntercepted":True,"recordsRevalidationSimulated":True,
        "scratchInputAndEntryHandlesReal":True,"nativeExecutions":0,"coordinatorStateAccessed":False}
out.write_bytes((json.dumps(report,indent=2,sort_keys=True)+"\n").encode())
