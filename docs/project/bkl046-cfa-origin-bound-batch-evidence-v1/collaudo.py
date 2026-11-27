from importlib.util import module_from_spec,spec_from_file_location
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

home, deps, output = map(Path,sys.argv[1:])
spec=spec_from_file_location("bound",home/"verifica-batch.py")
mod=module_from_spec(spec)
spec.loader.exec_module(mod)
fixture=home/"fixture"
authority=home/"autorita"
oracle=authority/"oracoli-prova"
cmp=authority/"verifica-v4.py"
reservation="348eaf20-c65c-438c-b808-eb1c163f9a31"
all_results=[]
for name in ("fixed-half","fixed-zero","use-declared"):
    result=mod.verify(reservation,authority,oracle,cmp,deps,fixture/name)
    assert result["classification"]["hypotheses"]==[name]
    all_results.append({"case":name,"log":result["eventsSha256"],"marker":result["markerSha256"],"accepted":True})

def edit_event(sample,index,change):
    file=sample/"events.txt"
    lines=file.read_text(encoding="utf-8").splitlines()
    kind,raw=lines[index].split(" ",1)
    event=json.loads(raw)
    change(event)
    lines[index]=kind+" "+json.dumps(event)
    file.write_text("\n".join(lines)+"\n",encoding="utf-8")

def wrong_marker(sample):
    path=sample/"batch.done.json"
    marker=json.loads(path.read_bytes())
    marker["reservation"]="e4658a0d-ac2d-4d16-a9ba-c0b8d0f87ac3"
    path.write_text(json.dumps(marker),encoding="utf-8")

def wrong_input(sample):
    edit_event(sample,0,lambda r:r["settings"]["inputData"][0].__setitem__(1,r["settings"]["inputData"][1][1]))

def wrong_export(sample):
    edit_event(sample,1,lambda r:r.__setitem__("weights",r["intensity"]))

def wrong_knob(sample):
    edit_event(sample,0,lambda r:r["settings"].__setitem__("dropShrink",.5))

def blank_source(sample):
    edit_event(sample,0,lambda r:r.__setitem__("source"," "))

def enum_drift(sample):
    edit_event(sample,2,lambda r:r["settings"].__setitem__("cfaPattern",2))

def missing_line(sample):
    p=sample/"events.txt"
    p.write_text("\n".join(p.read_text(encoding="utf-8").splitlines()[:-1])+"\n",encoding="utf-8")

for label,change,reason in (
    ("foreign-reservation",wrong_marker,"MARKER_CONTEXT_DIFFERS"),
    ("wrong-declared-input",wrong_input,"INPUT_DECLARATION_DIFFERS"),
    ("wrong-output-event",wrong_export,"EXPORT_DECLARATION_DIFFERS"),
    ("changed-drop-shrink",wrong_knob,"SETTINGS_DIFFERS"),
    ("blank-source",blank_source,"SOURCE_READBACK_MISSING"),
    ("enum-drift",enum_drift,"ENUMERATORS_INCONSISTENT"),
    ("incomplete-log",missing_line,"TRANSCRIPT_COUNT_DIFFERS"),
):
    with TemporaryDirectory(dir=output.parent,prefix="altered-") as folder:
        sample=Path(folder)/"run"
        shutil.copytree(fixture/"use-declared",sample)
        change(sample)
        try:
            mod.verify(reservation,authority,oracle,cmp,deps,sample)
        except ValueError as e:
            assert str(e)==reason
            all_results.append({"case":label,"reason":reason,"accepted":False})
        else:
            raise AssertionError(label+" accepted")
report={"schema":"BKL046_CFA_ORIGIN_BOUND_BATCH_OFFLINE_TEST_V1","cases":all_results,
        "coordinatorRegistryAccessed":False,"nativeExecutions":0}
output.write_bytes((json.dumps(report,indent=2,sort_keys=True)+"\n").encode())
