"""Read-only Windows permission check for the exact unactivated CFA v3 payload."""
import ctypes
from ctypes import wintypes
from hashlib import sha256
import json
from pathlib import Path, PureWindowsPath
import re
import socket
import stat
import sys

SUBJECT = "8d4ba1c9268399de1ac98dccf17c622877cb25eca23118ecfb8388241a22849a"
INACTIVE = "dc290fe87e79ef7ded865d47649a1c66a1ffcb3733dc604319d20e74ca46f8b3"
DESTINATION = Path("C:/Program Files/DigitalStarGate")
CONTROL = Path("C:/Program Files/PixInsight/bin/PixInsight.exe")

kernel = ctypes.WinDLL("kernel32", use_last_error=True)
open_existing = kernel.CreateFileW
open_existing.argtypes = [wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID,
                          wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
open_existing.restype = wintypes.HANDLE
kernel.CloseHandle.argtypes = [wintypes.HANDLE]
kernel.CloseHandle.restype = wintypes.BOOL
invalid_handle = ctypes.c_void_p(-1).value

COMMON = {"delete":0x10000,"writeDacl":0x40000,"writeOwner":0x80000,"writeAttributes":0x100,
          "writeExtendedAttributes":0x10}
FILE = {**COMMON,"writeData":2,"appendData":4}
DIRECTORY = {**COMMON,"addFile":2,"addDirectory":4,"deleteChild":0x40}
ANCESTOR = {key:COMMON[key] for key in ("delete","writeDacl","writeOwner","writeAttributes")}
ANCESTOR["deleteChild"] = DIRECTORY["deleteChild"]


def check_path(path):
    if not path.is_absolute():
        raise ValueError("ABSOLUTE_PATH_REQUIRED")
    for component in (*reversed(path.parents),path):
        info=component.lstat()
        if info.st_file_attributes & 0x400:
            raise ValueError("REPARSE_POINT_REFUSED:" + component.name)
    return info


def audit_access(path, rights):
    check_path(path)
    result={}
    for name,access in rights.items():
        handle=open_existing(str(path),access,7,None,3,0x02200000,None)
        if handle==invalid_handle:
            winerror=ctypes.get_last_error()
            result[name]={"status":"DENIED" if winerror in (5,1314) else "INCONCLUSIVE","error":winerror}
        else:
            if not kernel.CloseHandle(handle):
                raise ctypes.WinError(ctypes.get_last_error())
            result[name]={"status":"GRANTED"}
    if set(item["status"] for item in result.values())=={"DENIED"}:
        status="DENIED_ALL"
    elif any(item["status"]=="GRANTED" for item in result.values()):
        status="MUTATION_RIGHT_PRESENT"
    else:
        status="INCONCLUSIVE"
    return {"status":status,"rights":result}


def fresh_bytes(path, expected):
    before=check_path(path)
    if not stat.S_ISREG(before.st_mode):
        raise ValueError("NONREGULAR_MEMBER:"+path.name)
    data=path.read_bytes()
    after=check_path(path)
    fields=("st_dev","st_ino","st_size","st_mtime_ns","st_nlink")
    if any(getattr(before,k)!=getattr(after,k) for k in fields) or sha256(data).hexdigest()!=expected:
        raise ValueError("PAYLOAD_CHANGED:"+path.name)
    return data


def main():
    candidate, output = map(Path,sys.argv[1:])
    if socket.gethostname().upper()!="DSG-SHARED" or ctypes.windll.shell32.IsUserAnAdmin():
        raise ValueError("EXPECTED_NON_ELEVATED_DSG_SHARED_OPERATOR")
    subject=json.loads(fresh_bytes(candidate/"launcher-subject.json",SUBJECT))
    essentials={**subject["memberSha256"],**subject["authoritySha256"],
                "launcher-subject.json":SUBJECT,"managed-activation.cjs":INACTIVE}
    paths={}
    for relative,pin in essentials.items():
        components=relative.split("/")
        if not all(re.fullmatch(r"[A-Za-z0-9_.-]+",part) and not part.startswith(".")
                   and not part.endswith(".") and not PureWindowsPath(part).is_reserved() for part in components):
            raise ValueError("INVALID_PAYLOAD_PATH")
        path=candidate.joinpath(*components)
        fresh_bytes(path,pin)
        paths[relative]=path

    file_results={name:audit_access(path,FILE) for name,path in paths.items()}
    subdirs={path.parent for path in paths.values() if path.parent!=candidate}
    folder_results={str(path.relative_to(candidate)):audit_access(path,DIRECTORY)
                    for path in sorted({candidate,*subdirs})}
    parent_results={str(path):audit_access(path,ANCESTOR) for path in candidate.parents}
    for name,path in paths.items():
        fresh_bytes(path,essentials[name])
    combined=[*file_results.values(),*folder_results.values(),*parent_results.values()]
    try:
        installed=DESTINATION.lstat()
    except FileNotFoundError:
        deployment="PROTECTED_DESTINATION_ABSENT"
    else:
        deployment="DESTINATION_PRESENT_NOT_EVALUATED"
    report={"schema":"BKL046_CFA_V3_ORDINARY_TOKEN_DACL_AUDIT_V1","subjectSha256":SUBJECT,
        "verifiedPayloadFiles":len(file_results),"fileAccess":file_results,"directoryAccess":folder_results,
        "ancestorAccess":parent_results,"filesWithMutationRights":sum(
          item["status"]=="MUTATION_RIGHT_PRESENT" for item in file_results.values()),
        "ordinaryTokenDenialsComplete":all(item["status"]=="DENIED_ALL" for item in combined),
        "knownProtectedFileControl":audit_access(CONTROL,FILE),
        "deployment":deployment,"nativeAdmissionRequested":False,"nativeExecutions":0}
    with output.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("verifiedPayloadFiles","filesWithMutationRights",
                      "ordinaryTokenDenialsComplete","deployment")}))
    print("Control:",report["knownProtectedFileControl"]["status"])


if __name__=="__main__":
    main()
