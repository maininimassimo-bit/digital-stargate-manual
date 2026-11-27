"""Validate readiness on the original child handle for the XDRZ origin batch."""
from hashlib import sha256
from pathlib import Path
import stat
import time

from cfa_window_bridge import CfaWindowBridge
from parent_barrier import record, require
from window_identity import Windows

CASES=("zero-origin0","zero-origin05","half-origin0","half-origin05")
OPERATION="BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001"
PLAN="ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a"

def expected_marker(intent):
    require(intent["operation"]==OPERATION and intent["planSha256"]==PLAN,"WRONG_READY_INTENT")
    return {"schema":"BKL046_CFA_ORIGIN_BATCH_MARKER_V1","scope":"OUTPUT_MARKER_NOT_ADMISSION",
            "operation":OPERATION,"planSha256":PLAN,"reservation":intent["reservation"],"cases":list(CASES)}

def reread_marker(path, expected):
    info=path.lstat()
    require(stat.S_ISREG(info.st_mode) and not getattr(info,"st_file_attributes",0)&0x400,
            "BATCH_MARKER_REDIRECTED")
    with path.open("rb") as file:
        raw=file.read(4097)
    require(record(raw,set(expected))==expected,"BATCH_MARKER_CONTEXT_DIFFERS")
    return raw

def await_ready(intent, run, original, custody_alive, timeout):
    require(type(timeout) in (int,float) and 0<timeout<=600,"INVALID_READY_DEADLINE")
    run=Path(run)
    require(run.name==intent["reservation"],"RESERVATION_PATH_DIFFERS")
    expected=expected_marker(intent)
    marker=run/"batch.done.json"
    windows=Windows()
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        custody_alive()
        facts=original._facts()
        require(not facts["exited"],"ORIGINAL_EXITED_BEFORE_READY")
        try:
            raw=reread_marker(marker,expected)
        except FileNotFoundError:
            time.sleep(.025)
            continue
        visible=windows.windows(facts["pid"],visible=True)
        require(len(visible)<=1,"ORIGINAL_WINDOW_AMBIGUOUS")
        if not visible:
            time.sleep(.025)
            continue
        require(raw==reread_marker(marker,expected),"BATCH_MARKER_CHANGED_DURING_READY")
        require(original._facts()==facts,"ORIGINAL_IDENTITY_CHANGED_DURING_READY")
        custody_alive()
        context={"operation":OPERATION,"reservation":expected["reservation"],"plan":PLAN,
                 "subject":intent["batchSha256"],"batchMarkerSha256":sha256(raw).hexdigest(),"entryScriptSha256":intent["entrySha256"],
                 "imageSha256":intent["imageSha256"],"pid":facts["pid"],"creationFiletime":facts["creationFiletime"]}
        return context,CfaWindowBridge(original,context)
    raise TimeoutError("ORIGIN_BATCH_OR_WINDOW_NOT_READY")
