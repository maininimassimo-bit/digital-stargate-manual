"""Compare exact Stream34 memory counters with bracketed Windows system counters."""
import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys
from time import perf_counter_ns, sleep


GIB = 1024**3


def digest(value):
    return sha256(value).hexdigest()


def source_at(path,pin):
    data = path.read_bytes()
    if digest(data) != pin:
        raise ValueError("EXACT_SOURCE_CHANGED")
    return data


def perf_query():
    class Performance(ctypes.Structure):
        count = ["CommitTotal","CommitLimit","CommitPeak","PhysicalTotal","PhysicalAvailable",
                 "SystemCache","KernelTotal","KernelPaged","KernelNonpaged","PageSize"]
        _fields_ = [("cb",wintypes.DWORD)] + [(name,ctypes.c_size_t) for name in count] + [
            (name,wintypes.DWORD) for name in ("HandleCount","ProcessCount","ThreadCount")]
    f = ctypes.WinDLL("psapi",use_last_error=True).GetPerformanceInfo
    f.argtypes = (ctypes.POINTER(Performance),wintypes.DWORD)
    f.restype = wintypes.BOOL
    def sample():
        info = Performance()
        info.cb = ctypes.sizeof(info)
        if not f(ctypes.byref(info),info.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        return {"pageSizeBytes":info.PageSize,"systemCommitTotalBytes":info.CommitTotal*info.PageSize,
                "systemCommitLimitBytes":info.CommitLimit*info.PageSize,
                "availablePhysicalBytes":info.PhysicalAvailable*info.PageSize,
                "totalPhysicalBytes":info.PhysicalTotal*info.PageSize}
    return sample


def disposition(v,before,after):
    lower,upper = sorted((before,after))
    if v < lower:
        return "BELOW_BRACKET",lower-v
    if v > upper:
        return "ABOVE_BRACKET",v-upper
    return "WITHIN_BRACKET",0


def summarize(rows):
    classify = {"WITHIN_BRACKET":0,"BELOW_BRACKET":0,"ABOVE_BRACKET":0}
    phys_classify = dict.fromkeys(classify,0)
    rejected = 0
    overshoot = 0
    for row in rows:
        a,b = row["systemBefore"],row["systemAfter"]
        proc = row["stream34"]
        assert proc["stage"] == "OPERATOR_BEFORE_CUSTODIAN"
        assert proc["minimumAvailablePhysicalBytes"] == 8*GIB
        assert proc["minimumAvailableCommitBytes"] == 12*GIB
        assert proc["processHandlesOpened"] == 0 and proc["nativeAdmissionGranted"] is False
        assert proc["continuousMemoryBoundAttested"] is False
        for q in (a,b):
            assert q["pageSizeBytes"] > 0
            assert q["systemCommitLimitBytes"] >= q["systemCommitTotalBytes"] >= 0
            assert 0 <= q["availablePhysicalBytes"] <= q["totalPhysicalBytes"]
        avail_before,avail_after = (q["systemCommitLimitBytes"]-q["systemCommitTotalBytes"] for q in (a,b))
        status,extra = disposition(proc["availableCommitBytes"],avail_before,avail_after)
        classify[status] += 1
        overshoot = max(overshoot,extra)
        status,_ = disposition(proc["availablePhysicalBytes"],a["availablePhysicalBytes"],b["availablePhysicalBytes"])
        phys_classify[status] += 1
        reason = []
        if proc["availablePhysicalBytes"] < 8*GIB: reason.append("PHYSICAL_RESERVE_BELOW_8_GIB")
        if proc["availableCommitBytes"] < 12*GIB: reason.append("COMMIT_RESERVE_BELOW_12_GIB")
        assert reason == proc["budgetReasons"]
        rejected += bool(reason)
    return {"samples":len(rows),"thresholdRefusals":rejected,"processCommitVsSystemBracket":classify,
            "streamPhysicalVsSystemBracket":phys_classify,"maximumCommitDistanceOutsideBracketBytes":overshoot,
            "minExactPhysicalAvailableBytes":min(r["stream34"]["availablePhysicalBytes"] for r in rows),
            "minExactProcessCommitAvailableBytes":min(r["stream34"]["availableCommitBytes"] for r in rows),
            "maximumBracketSpanUs":max(r["intervalNs"] for r in rows)//1000,
            "totalPhysicalBytes":rows[0]["systemBefore"]["totalPhysicalBytes"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",choices=("capture","verify"))
    parser.add_argument("protocol",type=Path)
    parser.add_argument("report",type=Path)
    parser.add_argument("--source",type=Path)
    parser.add_argument("--loader",type=Path)
    args = parser.parse_args()
    raw = args.protocol.read_bytes()
    cfg = json.loads(raw)
    assert [disposition(v,10,20) for v in (9,10,21)] == [
        ("BELOW_BRACKET",1),("WITHIN_BRACKET",0),("ABOVE_BRACKET",1)]
    if args.mode == "verify":
        j = json.loads(args.report.read_bytes())
        assert j["protocolSha256"] == digest(raw)
        assert j["programSha256"] == digest(Path(__file__).read_bytes())
        assert j["summary"] == summarize(j["rows"])
        assert len(j["rows"]) == cfg["sampleCount"]
        assert j["admissionRequested"] is False and j["continuousMemoryBoundAttested"] is False
        print(json.dumps(j["summary"],sort_keys=True))
        return
    assert platform.node().upper() == "DSG-SHARED" and sys.platform == "win32"
    module = {"__name__":"pinned_gate_extract","__file__":str(args.loader)}
    exec(compile(source_at(args.loader,cfg["loaderSha256"]),str(args.loader),"exec"),module)
    subject = json.loads(source_at(args.source/"launcher-subject.json",cfg["candidateSubject"]))
    gate = module["load_gate"](args.source,subject)
    query = perf_query()
    rows = []
    for i in range(cfg["sampleCount"]):
        start = perf_counter_ns()
        a = query()
        try:
            exact = gate["require_host_reserves"]("OPERATOR_BEFORE_CUSTODIAN")
        except gate["MemoryReserveUnavailable"] as exc:
            exact = exc.snapshot
        b = query()
        rows.append({"sequence":i,"intervalNs":perf_counter_ns()-start,"systemBefore":a,
                     "stream34":exact,"systemAfter":b})
        if i+1 < cfg["sampleCount"]:
            sleep(cfg["intervalMs"]/1000)
    j = {"schema":"BKL046_STREAM34_VM_COMMIT_CROSSCHECK_RESULT_V1","host":"DSG-SHARED",
         "recordedAtUtc":datetime.now(timezone.utc).isoformat(),"programSha256":digest(Path(__file__).read_bytes()),
         "protocolSha256":digest(raw),"summary":summarize(rows),"rows":rows,
         "launcherContextObserved":False,"continuousMemoryBoundAttested":False,
         "admissionRequested":False,"nativeExecutions":0,"scientificClosures":0}
    with args.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(j,f,indent=2,sort_keys=True)
        f.write("\n")
    print(json.dumps(j["summary"],sort_keys=True))


if __name__ == "__main__":
    main()
