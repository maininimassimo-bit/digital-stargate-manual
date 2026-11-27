"""Read-only, operation-bound R4 continuation checks for the synthetic CFA parent."""

import ctypes
from ctypes import wintypes
import json
from hashlib import sha256
import uuid
import msvcrt
import os
import re
import sys

OPERATION="BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001"
R4_MANIFEST_SHA256="61d38f0160ba2650cea167e7e1a5fbe5af1d4b448ddc085f2f8845f36e7a4150"
PLAN_SHA256="ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a"
SUBJECT_SHA256="4aa98f614ab6e53c520662659ce91ce1a352b6d78291a20f2dd6cd9e0f0d9b3e"
CASES=frozenset(("all-four-origin-cases",))

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def record(raw,fields):
    require(type(raw) is bytes and 0<len(raw)<=4096,"wrong record bytes")
    def unique(items):
        result={}
        for key,value in items:
            require(key not in result,"duplicate record field")
            result[key]=value
        return result
    value=json.loads(raw.decode("utf-8"),object_pairs_hook=unique)
    require(type(value) is dict and set(value)==fields,"wrong record fields")
    return value


LIMIT = 1024
PROTOCOL = "BKL046_CFA_XDRZ_ORIGIN_START_BOUND_PARENT_V1"


def creation_filetime():
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    values = [wintypes.FILETIME() for _ in range(4)]
    if not kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(value) for value in values)):
        raise ctypes.WinError(ctypes.get_last_error())
    birth = (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime
    require(birth > 0, "NO_ORIGINAL_PARENT_CREATION_TIME")
    return str(birth)


def _wait(state):
    """Publish FD3 identity and accept the bounded first frame on the fixture channel."""
    birth = creation_filetime()
    pid, caller = os.getpid(), os.getppid()
    frame = f"{pid} {birth}\n".encode("ascii")
    msvcrt.setmode(3, os.O_BINARY)
    with os.fdopen(3, "wb", buffering=0) as identity_pipe:
        require(identity_pipe.write(frame) == len(frame), "PARENT_IDENTITY_SHORT_WRITE")
    first = sys.stdin.buffer.readline(LIMIT + 1)
    require(0 < len(first) <= LIMIT and first.endswith(b"\n"), "PARENT_BARRIER_FRAME_INVALID")
    value = record(first, {
        "protocol", "operation", "reservation", "manifestSha256", "pid",
        "callerPid", "creationFiletime", "activeSha256", "originalSha256",
        "planSha256", "subjectSha256", "caseId"
    })
    require(value["protocol"] == PROTOCOL and value["operation"] == OPERATION
            and value["manifestSha256"] == R4_MANIFEST_SHA256, "PARENT_BARRIER_SCOPE_MISMATCH")
    require(type(value["pid"]) is int and value["pid"] == pid
            and type(value["callerPid"]) is int and value["callerPid"] == caller
            and value["creationFiletime"] == birth, "PARENT_BARRIER_OWN_IDENTITY_MISMATCH")
    reservation = value["reservation"]
    require(type(reservation) is str and re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        reservation
    ) is not None, "PARENT_BARRIER_RESERVATION_INVALID")
    for key in ("activeSha256", "originalSha256"):
        require(type(value[key]) is str and re.fullmatch("[0-9a-f]{64}", value[key]) is not None,
                "PARENT_BARRIER_RECORD_PIN_INVALID")
    require(value["planSha256"]==PLAN_SHA256 and value["subjectSha256"]==SUBJECT_SHA256
            and value["caseId"] in CASES,"CFA control subject mismatch")
    require(str(uuid.UUID(reservation))==reservation,"invalid reservation format")

    active_path=state/"active.json"
    active_bytes=active_path.read_bytes()
    acquired=(state/(reservation+"-acquired.json")).read_bytes()
    original_bytes=(state/(reservation+"-original.json")).read_bytes()
    require(active_bytes==acquired==active_path.read_bytes(),"active and acquired records differ")
    require(sha256(active_bytes).hexdigest()==value["activeSha256"]
            and sha256(original_bytes).hexdigest()==value["originalSha256"],"record bytes changed")
    active=record(active_bytes,{"protocol","milestone","operation","reservation","coordinatorPid","startedUTC"})
    original=record(original_bytes,{"pid","creationFiletime","callerPid"})
    require(active["protocol"]=="DSG_PI_SERIAL_V1" and active["milestone"]=="BKL-046"
            and active["operation"]==OPERATION and active["reservation"]==reservation
            and type(active["coordinatorPid"]) is int and active["coordinatorPid"]>0
            and active["coordinatorPid"] not in (pid,caller),"active ownership mismatch")
    require(all(type(x) is int for x in original.values()) and
            original=={"pid":pid,"creationFiletime":int(birth),"callerPid":caller},
            "bound parent record mismatch")
    return {"operation":OPERATION,"caseId":value["caseId"],"reservation":reservation,
            "pid":pid,"casePlanSha256":PLAN_SHA256,"subjectSha256":SUBJECT_SHA256}

