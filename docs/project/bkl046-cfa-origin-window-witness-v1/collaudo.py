from hashlib import sha256
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

root, modules, source, dependencies, output = map(Path,sys.argv[1:])
cfg=json.loads((modules/"pins.json").read_bytes())
for name,pin in cfg.items():
    assert sha256((modules/name).read_bytes()).hexdigest()==pin
sys.path.insert(0,str(modules))
from cfa_window_bridge import CfaWindowBridge
from harness import launch
from parent_cfa import serve
from window_identity import Windows

RUN="348eaf20-c65c-438c-b808-eb1c163f9a31"
authority=source/"autorita"
verifier=source/"verifica-batch.py"
assert sha256(verifier.read_bytes()).hexdigest()=="1a2036157bb31e4bf7a09408e7bef25051d19ff0e8fe891ab513690f7483aa06"

def get(path):
    return json.loads(path.read_bytes())

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def run_case(mode):
    with TemporaryDirectory(dir=modules,prefix="fixture-") as one, TemporaryDirectory(dir=modules,prefix="fixture-") as two:
        local,foreign_dir=Path(one),Path(two)
        fixture=source/"fixture"/"use-declared"
        receipt=local/"comparison.json"
        subprocess.run([sys.executable,"-I","-B","-S",str(verifier),RUN,str(authority),
                        str(authority/"oracoli-prova"),str(authority/"verifica-v4.py"),
                        str(dependencies),str(fixture),str(receipt)],check=True,timeout=10,
                       creationflags=subprocess.CREATE_NO_WINDOW,stdout=subprocess.PIPE)
        authorized=get(receipt)
        assert authorized["reservation"]==RUN and authorized["classification"]["hypotheses"]==["use-declared"]
        pin=digest(receipt)
        run=local/"run"
        run.mkdir()
        original,proof=launch(local,"visible-original")
        foreign=None
        try:
            foreign,other_proof=launch(foreign_dir,"visible-foreign")
            foreign_window=other_proof["windows"][0]
            context={"operation":authorized["operation"],"reservation":RUN,
                     "pid":proof["pid"],"creationFiletime":proof["creationFiletime"],
                     "batchMarkerSha256":authorized["markerSha256"],"plan":authorized["classification"]["planSha256"]}
            bridge=CfaWindowBridge(original,context)
            terminal=io.StringIO()
            verified_capture=False

            class Commands:
                actions=("find","capture","arm","find","close")
                index=0
                def readline(self,size):
                    nonlocal verified_capture
                    action=self.actions[self.index]
                    self.index+=1
                    ctrl=run/"control"
                    msg={"action":action,"reply":f"reply-{self.index}","context":context}
                    if action in ("capture","arm","close"):
                        slot=4 if action=="close" else 1
                        window=get(ctrl/f"reply-{slot}.json")["window"]
                        assert int(window["hwnd"])==proof["windows"][0]
                        assert int(window["hwnd"])!=foreign_window
                        msg["window"]=dict(window)
                    if action=="capture" and mode=="other-window":
                        msg["window"]["hwnd"]=str(foreign_window)
                    if action in ("arm","close"):
                        if mode=="receipt-changed" and action=="close":
                            with receipt.open("ab") as f:
                                f.write(b" ")
                        if digest(receipt)!=pin:
                            raise ValueError("ORIGIN_RECEIPT_CHANGED")
                        bitmap=ctrl/"frame.bmp"
                        raw=bitmap.read_bytes()
                        data_offset=int.from_bytes(raw[10:14],"little")
                        pixels=memoryview(raw)[data_offset:]
                        colors={(pixels[i],pixels[i+1],pixels[i+2]) for i in range(0,len(pixels),4)}
                        assert (0x28,0x53,0xb6) in colors and (0xeb,0xa4,0x27) not in colors
                        assert digest(bitmap)==get(ctrl/"reply-2.json")["sha256"]
                        verified_capture=True
                        msg.update(capture=digest(bitmap),comparison=pin)
                    message=(json.dumps(msg)+"\n").encode()
                    assert len(message)<size
                    return message

            reason={"other-window":"CFA window scope changed","receipt-changed":"ORIGIN_RECEIPT_CHANGED"}.get(mode)
            try:
                serve(run,context,bridge,original,Commands(),terminal)
                assert reason is None
            except ValueError as e:
                if reason is None or str(e)!=reason:
                    raise
            ctrl=run/"control"
            observed=[json.loads(line) for line in terminal.getvalue().splitlines()]
            if reason is None:
                assert observed[-1]["status"]=="CFA_NATIVE_EXIT_OBSERVED"
                assert get(ctrl/"reply-5.json")["comparison"]==pin
                assert get(local/"wm-close.json")=={"hwnd":proof["windows"][0]}
                assert not Windows().u.IsWindow(proof["windows"][0])
            else:
                assert not (ctrl/"reply-5.json").exists()
                assert not (local/"wm-close.json").exists()
                assert not original._facts()["exited"]
                assert Windows().u.IsWindow(proof["windows"][0])
            assert not foreign._facts()["exited"] and Windows().u.IsWindow(foreign_window)
            assert not (foreign_dir/"wm-close.json").exists()
            return {"case":mode,"originalCaptureVerified":verified_capture,
                    "originalOrdinaryClose":reason is None,"foreignUnaffected":True,
                    "comparisonPinned":True,"reason":reason}
        finally:
            (local/"close").touch()
            assert original.wait(5)["exitCode"]==0
            if foreign is not None:
                (foreign_dir/"close").touch()
                assert foreign.wait(5)["exitCode"]==0

r={"schema":"BKL046_CFA_ORIGIN_WINDOW_WITNESS_V1",
   "cases":[run_case(case) for case in ("valid","other-window","receipt-changed")],
   "witnessWindows":True,"pixInsightLaunched":False,"admissionRequested":False,"scientificClosures":0}
output.write_bytes((json.dumps(r,indent=2,sort_keys=True)+"\n").encode())
