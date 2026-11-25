from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

base,preparer,output=map(Path,sys.argv[1:])
modules=base/"moduli"
for name,expected in json.loads((modules/"pins.json").read_bytes()).items():
    assert sha256((modules/name).read_bytes()).hexdigest()==expected
sys.path[:0]=[str(base),str(modules)]
from harness import launch
from pronto import await_ready,expected_marker,OPERATION,PLAN

raw=preparer.read_bytes()
assert sha256(raw).hexdigest()=="13c011ede4c4efc1d1a32b20b933f83c47adebe9734b329c1367dc1f24c87beb"
preparation={"__name__":"prepare_origin"}
exec(compile(raw,str(preparer),"exec"),preparation)
rid="348eaf20-c65c-438c-b808-eb1c163f9a31"
intent,entry=preparation["prepare"]({"operation":OPERATION,"reservation":rid,"planSha256":PLAN,
                                    "candidateSha256":preparation["BATCH_PIN"]})
assert sha256(entry).hexdigest()==intent["entrySha256"]

cases=[]
for mode,reason in (
    ("valid",None),
    ("foreign-marker","BATCH_MARKER_CONTEXT_DIFFERS"),
    ("missing-marker","ORIGIN_BATCH_OR_WINDOW_NOT_READY"),
    ("original-exited","ORIGINAL_EXITED_BEFORE_READY"),
    ("inputs-lost","INPUT_CUSTODY_LOST"),
):
    with TemporaryDirectory(dir=modules,prefix="fixture-") as root:
        folder=Path(root)
        run=folder/rid
        run.mkdir()
        marker=expected_marker(intent)
        if mode=="foreign-marker":
            marker["reservation"]="e4658a0d-ac2d-4d16-a9ba-c0b8d0f87ac3"
        marker_path=run/"batch.done.json"
        if mode!="missing-marker":
            marker_path.write_text(json.dumps(marker),encoding="utf-8")
        original,proof=launch(folder,"visible-original")
        try:
            if mode=="original-exited":
                (folder/"close").touch()
                assert original.wait(5)["exitCode"]==0
            def custody():
                if mode=="inputs-lost":
                    raise ValueError("INPUT_CUSTODY_LOST")
            try:
                scope, bridge=await_ready(intent,run,original,custody,0.25 if mode=="missing-marker" else 2)
                assert reason is None and scope["pid"]==proof["pid"] and scope["creationFiletime"]==proof["creationFiletime"]
                assert scope["batchMarkerSha256"]==sha256(marker_path.read_bytes()).hexdigest()
                assert scope["entryScriptSha256"]==sha256(entry).hexdigest()
                assert int(bridge.find(scope)["hwnd"])==proof["windows"][0]
            except (ValueError,TimeoutError) as e:
                if str(e)!=reason:
                    raise
            cases.append({"case":mode,"ready":reason is None,"reason":reason})
            assert not (folder/"wm-close.json").exists()
        finally:
            (folder/"close").touch()
            assert original.wait(5)["exitCode"]==0
r={"schema":"BKL046_CFA_ORIGIN_READY_WITNESS_OFFLINE_V1","cases":cases,
   "originalProcessHandleUsed":True,"originalWindowObserved":True,"inputLossSimulated":True,
   "pixInsightLaunched":False,"coordinatorStateAccessed":False,"scientificClosures":0}
output.write_bytes((json.dumps(r,indent=2,sort_keys=True)+"\n").encode())
