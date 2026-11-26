"""Exercise exact v11 host-memory ordering without a process or live coordinator."""
import argparse
import ast
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace


def digest(raw):
    return sha256(raw).hexdigest()


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def get_source(root, subject, name):
    raw = (root / name).read_bytes()
    require(digest(raw) == subject["memberSha256"][name], "MEMBER_CHANGED:" + name)
    return ast.parse(raw, filename=name)


def compile_nodes(nodes, name, scope):
    tree = ast.Module(body=nodes, type_ignores=[])
    exec(compile(tree, name, "exec"), scope)


def definitions(source, fields):
    def name(node):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            return node.name
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            return node.targets[0].id
        return None
    items = [node for node in source.body if name(node) in fields]
    require({name(node) for node in items} == fields, "SOURCE_SYMBOLS_CHANGED")
    return items


def load_gate(root, subject):
    layout = "weighted_native_memory_budget_h_v1.py"
    scope = {"ctypes":ctypes, "wt":wintypes, "datetime":datetime, "timezone":timezone}
    compile_nodes(definitions(get_source(root,subject,layout),{"MemoryStatus"}),layout,scope)
    gate = "native_stream_host_memory_preflight_h_v1.py"
    names = {"STAGES","MIN_PHYSICAL","MIN_COMMIT","MemoryReserveUnavailable","evaluate","require_host_reserves"}
    compile_nodes(definitions(get_source(root,subject,gate),names),gate,scope)
    return scope


def case(root, subject, gate, initial, final, fault=None):
    physical, commit = gate["MIN_PHYSICAL"], gate["MIN_COMMIT"]
    events = []
    readings = iter([initial, final])
    scripted = []

    def os_query(pointer):
        item = next(readings)
        events.append("GlobalMemoryStatusEx")
        if item is None:
            return 0
        memory = ctypes.cast(pointer,ctypes.POINTER(gate["MemoryStatus"])).contents
        require(memory.dwLength == ctypes.sizeof(gate["MemoryStatus"]),"MEMORY_LAYOUT")
        memory.ullAvailPhys,memory.ullAvailPageFile = item
        scripted.append(item)
        return 1

    old = gate["ctypes"]
    gate["ctypes"] = SimpleNamespace(WinDLL=lambda *_args, **_kwargs:SimpleNamespace(GlobalMemoryStatusEx=os_query),
                                     sizeof=ctypes.sizeof, POINTER=ctypes.POINTER, byref=ctypes.byref,
                                     get_last_error=lambda:31, WinError=lambda code:OSError(code,"OS_QUERY_FAILED"))

    def reserve(stage):
        events.append(stage)
        return gate["require_host_reserves"](stage)

    class PriorHost:
        pass

    class Original:
        def __init__(self):
            self.child = None
            events.append("allocateCustody")

        def launch(self,*args,**kwargs):
            events.append("nativeCreateStub")
            self.child = SimpleNamespace(pid=42)

    class TestPath:
        def __truediv__(self, name):
            return SimpleNamespace(open=lambda mode:self.open(name,mode))

        def open(self,name,mode):
            assert mode == "xb"
            events.append(name)
            return name

    def write(name, value):
        events.append(name)
        if name == "memory-000000.json" and fault=="after-create-write":
            raise OSError("MEMORY_RECEIPT_WRITE_FAILED")

    def publish(_pin):
        events.append("observePublisher")
        return {"fixture":True}

    scope = {"PriorHost":PriorHost,"require_host_reserves":reserve,"need":require,
              "OriginalChildCustody":Original,"EXE":"not-started.exe","SHA":digest,
              "os":SimpleNamespace(environ={}),"require":require,"observe":publish}
    real_name = "native_stream_complete_real_host_h_v2.py"
    host, = definitions(get_source(root,subject,real_name),{"RealHost"})
    compile_nodes([host],real_name,scope)
    vm_name = "stream34_vm_host.py"
    vm, = definitions(get_source(root,subject,vm_name),{"VmHost"})
    vm.body = [method for method in vm.body if isinstance(method,ast.FunctionDef)
               and method.name == "launch_once"]
    compile_nodes([vm],vm_name,scope)
    obj = scope["VmHost"]()
    obj.retention = SimpleNamespace(raise_if_requested=lambda:events.append("retention"))
    obj._publisher_at_launch = None
    obj._scan = lambda:[]
    obj.assert_inputs = lambda _ctx:events.append("assertInputs")
    obj.root = TestPath()
    obj.scope = SimpleNamespace(sp="subject fixture",rp="review fixture",publisher_receipt_sha256="publisher fixture")
    obj.temp = "unused"
    obj.logs = []
    obj.owner = None
    obj.now = lambda:"fixture UTC"
    ctx=dict(sourceSha256="source fixture",bindingRaw=b"binding fixture")
    result = "PASSED"
    reasons = []
    try:
        obj.launch_once(ctx,SimpleNamespace(write_json=write))
    except gate["MemoryReserveUnavailable"] as error:
        result = "RESERVE_REFUSED"
        reasons = error.snapshot["budgetReasons"]
    except OSError as error:
        result = "OS_QUERY_FAILED" if "OS_QUERY_FAILED" in str(error) else str(error)
    finally:
        gate["ctypes"] = old
    launched = events.count("nativeCreateStub")
    return {"outcome":result,"reasons":reasons,"events":events,"stubCreations":launched,
            "ownerRetainedAfterStub":obj.owner is not None and obj.owner.child is not None,
            "physicalThresholdBytes":physical,"commitThresholdBytes":commit}


def main():
    p = argparse.ArgumentParser()
    for n in ("protocol","source","report"):
        p.add_argument(n,type=Path)
    a = p.parse_args()
    raw = a.protocol.read_bytes()
    cfg = json.loads(raw)
    subject_raw = (a.source/"launcher-subject.json").read_bytes()
    require(digest(subject_raw) == cfg["subjectSha256"],"SUBJECT_CHANGED")
    subject = json.loads(subject_raw)
    gate = load_gate(a.source,subject)
    phy, com = gate["MIN_PHYSICAL"], gate["MIN_COMMIT"]
    require((phy,com) == (8589934592,12884901888),"THRESHOLDS_CHANGED")
    live_stage = gate["STAGES"]
    require(len(live_stage)==4,"STAGES_CHANGED")
    grid=[]
    for x in (phy-1,phy,phy+1):
        for y in (com-1,com,com+1):
            got = gate["evaluate"]({"availablePhysicalBytes":x,"availableCommitBytes":y})
            expected = (["PHYSICAL_RESERVE_BELOW_8_GIB"] if x < phy else []) + (
                ["COMMIT_RESERVE_BELOW_12_GIB"] if y < com else [])
            assert got == expected
            grid.append({"supportsPhysical":x>=phy,"supportsCommit":y>=com,"reasons":got})
    threshold=(phy,com)
    cases = {
        "atBothThresholds":case(a.source,subject,gate,threshold,threshold),
        "initialPhysicalBelow":case(a.source,subject,gate,(phy-1,com),threshold),
        "lastPhysicalBelow":case(a.source,subject,gate,threshold,(phy-1,com)),
        "lastCommitBelow":case(a.source,subject,gate,threshold,(phy,com-1)),
        "lastQueryFailed":case(a.source,subject,gate,threshold,None),
        "receiptFailureAfterStub":case(a.source,subject,gate,threshold,threshold,"after-create-write"),
    }
    yes = cases["atBothThresholds"]
    assert yes["events"][-3:] == ["GlobalMemoryStatusEx","nativeCreateStub","memory-000000.json"]
    assert yes["outcome"] == "PASSED"
    first = cases["initialPhysicalBelow"]
    assert first["outcome"] == "RESERVE_REFUSED" and "launch-intent.json" not in first["events"]
    for name in ("lastPhysicalBelow","lastCommitBelow","lastQueryFailed"):
        refused = cases[name]
        assert refused["events"][-1] == "GlobalMemoryStatusEx"
        assert "launch-intent.json" in refused["events"] and refused["stubCreations"] == 0
        assert refused["outcome"] == ("OS_QUERY_FAILED" if name=="lastQueryFailed" else "RESERVE_REFUSED")
    receipt = cases["receiptFailureAfterStub"]
    assert receipt["stubCreations"] == 1 and receipt["ownerRetainedAfterStub"] is True
    assert receipt["outcome"] == "MEMORY_RECEIPT_WRITE_FAILED"
    report = {"schema":"BKL046_STREAM34_MEMORY_ORDER_OFFLINE_RESULT_V1",
              "protocolSha256":digest(raw),"programSha256":digest(Path(__file__).read_bytes()),
              "subjectSha256":cfg["subjectSha256"],"boundaryGrid":grid,"launchHostScenarios":cases,
              "continuousMemoryBoundAttested":False,"canonicalGateAccessed":False,"admissionRequested":False,
              "nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(report,f,indent=2,sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
