"""Read-only Stream34 v11 prerequisite audit. No authority, custodian or native start."""
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import socket
import sys
from zipfile import ZipFile

kit, output = map(Path, sys.argv[1:])
if socket.gethostname().upper() != "DSG-SHARED":
    raise ValueError("WRONG_HOST")
def digest(raw):
    return sha256(raw).hexdigest()

handoff_raw = (kit / "fascicolo.json").read_bytes()
if digest(handoff_raw) != "127ec442dad584f58af505128054e3ad9e9df696564161c92bf8fe803aa5c264":
    raise ValueError("HANDOFF_CHANGED")
handoff = json.loads(handoff_raw)
archive_bytes = (kit / "candidata-v11.zip").read_bytes()
if digest(archive_bytes) != handoff["archiveSha256"]:
    raise ValueError("ARCHIVE_CHANGED")
with ZipFile(io.BytesIO(archive_bytes)) as archive:
    names = archive.namelist()
    if len(names) != 70 or set(names) != set(handoff["archiveMembers"]):
        raise ValueError("ARCHIVE_MEMBER_SET_CHANGED")
    payload = {}
    for name, pin in handoff["archiveMembers"].items():
        raw = archive.read(name)
        if digest(raw) != pin:
            raise ValueError("ARCHIVE_MEMBER_CHANGED:" + name)
        payload[name] = raw

subject_raw = payload["launcher-subject.json"]
if digest(subject_raw) != handoff["subjectSha256"]:
    raise ValueError("SUBJECT_CHANGED")
subject = json.loads(subject_raw)
members = {}
for name, pin in subject["memberSha256"].items():
    raw = payload[name]
    if digest(raw) != pin:
        raise ValueError("INTERNAL_SUBJECT_MEMBER_CHANGED:" + name)
    if name.endswith(".py"):
        members[name] = raw

bootstrap = {"__name__": "verified_offline_bootstrap"}
exec(compile(payload["stream34_bootstrap.py"], "stream34_bootstrap.py", "exec"), bootstrap)
sys.meta_path.insert(0, bootstrap["FrozenModules"](kit, members))
import stream34_vm_scope as scope
from collect_guardian_binding import coordinator_module
from native_stream_host_memory_preflight_h_v1 import require_host_reserves, MemoryReserveUnavailable
from publisher_guard import observe

checks = {}
def audit(label, operation):
    try:
        checks[label] = {"status":"OK", "value":operation()}
    except MemoryReserveUnavailable as error:
        checks[label] = {"status":"INSUFFICIENT", "value":error.snapshot}
    except (OSError, ValueError) as error:
        checks[label] = {"status":"ERROR", "type":type(error).__name__,
                         "code":getattr(error,"winerror",None), "reason":str(error)}
    except Exception as error:
        checks[label] = {"status":"ERROR", "type":type(error).__name__,
                         "reason":str(error)[:300]}

def runtime():
    verified = {}
    for path,pin in scope.RUNTIME_FILES.items():
        if path == Path(sys.executable):
            if not path.is_absolute() or digest(path.read_bytes()) != pin:
                raise ValueError("PYTHON_RUNTIME_CHANGED")
        else:
            scope.stable_digest(path,pin)
        verified[path.name] = pin
    return verified

def inputs():
    plan_raw = payload["input-plan.json"]
    if digest(plan_raw) != scope.PLAN_SHA or scope.PLAN_SHA != handoff["inputPlanSha256"]:
        raise ValueError("INPUT_PLAN_CHANGED")
    plan = json.loads(plan_raw)
    root = scope.rootpath(Path(plan["nativeRoot"]),False)
    if os.path.lexists(root):
        raise ValueError("ONE_SHOT_NAMESPACE_PRESENT")
    verified = []
    for item in plan["files"]:
        path = Path(item["path"])
        if path.parent != scope.INPUT_BASE / "inputs":
            raise ValueError("INPUT_ROOT_CHANGED")
        info = scope.stable_digest(path,item["sha256"])
        if info.st_dev != scope.PARENT_ID[0] or info.st_size != item["bytes"]:
            raise ValueError("INPUT_IDENTITY_CHANGED")
        verified.append((info.st_dev,info.st_ino,info.st_size))
    if len(verified) != 8 or len(set(verified)) != 8 or sum(x[2] for x in verified) != plan["totalBytes"]:
        raise ValueError("INPUT_COVERAGE_CHANGED")
    return {"files":len(verified), "bytes":sum(x[2] for x in verified), "oneShotPresentAtRead":False}

def coordinator():
    verified = {name: digest(scope.pinned(scope.R4_ROOT / name,pin)) for name,pin in scope.R4_PINS.items()}
    return {"files":verified, "activePresentAtRead":os.path.lexists(scope.R4_ROOT/"state"/"active.json")}

def study_registry():
    data=scope.pinned(scope.INPUT_BASE/"Registro-studio-PixInsight.v600.staged.json",scope.STUDY_REGISTRY_SHA,limit=67108864)
    event=json.loads(data)["resumeStudyEvents"][-1]
    if event["manifest"]!="Manifest-ripresa-v600.json" or event["completeStudy"] is not False:
        raise ValueError("FROZEN_STUDY_REGISTRY_CHANGED")
    return {"sha256":digest(data),"completeStudy":False}

audit("runtime",runtime)
audit("inputs",inputs)
audit("coordinator",coordinator)
audit("studyRegistry",study_registry)
audit("hostMemory",lambda:require_host_reserves("OPERATOR_BEFORE_CUSTODIAN"))
audit("pixInsightInventory",lambda:{"count":len(coordinator_module().scan_pixinsight())})
audit("publisherObservation",lambda:observe(scope.PUBLISHER_SHA))

report = {"schema":"BKL046_STREAM34_V11_READONLY_CHECKPOINT_V1",
          "subjectSha256":digest(subject_raw),"archiveSha256":digest(archive_bytes),
          "archiveMembersVerified":len(payload),"checks":checks,
          "approvalLanesInspected":{"adjacentFiles":sorted(name for name in
              ("trust.json","ARB.json","RQ.json","ARB.origin.json","RQ.origin.json") if (kit/name).is_file()),
              "authenticatedApprovalsVerified":False},
          "admissionRequested":False,"nativeExecutions":0,"scientificClosures":0}
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(report,sort_keys=True,indent=2)+"\n")
print(json.dumps({name:item["status"] for name,item in checks.items()},sort_keys=True))
