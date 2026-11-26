from argparse import ArgumentParser
from contextlib import ExitStack
import ctypes as c
from ctypes import wintypes as w
from hashlib import sha256
from io import BytesIO
import json
import msvcrt
import os
from pathlib import Path, PurePosixPath
import stat
from tempfile import TemporaryDirectory
from uuid import uuid4
from zipfile import ZipFile

IMAGE_SHA="08a107e2a748de3911bb1b7e3badb03340bb92a5d954c7bb1e55f3f24566de7a"
SUBJECT="94db7ebe9d92af0fa16f67da4a45636bea24918b782dcd415f1b8dd5a8bfa423"
INACTIVE=b"'use strict';\nmodule.exports = null;\n"
BASE=Path("C:/Program Files/DigitalStarGate")
DEST=BASE/"BKL046-CFA-XDRZ-two-drop-v1"
OWNER_DACL=5
REPARSE=0x400
kernel=c.WinDLL("kernel32",use_last_error=True)
security=c.WinDLL("advapi32",use_last_error=True)
invalid=c.c_void_p(-1).value


def signature(dll,name,result,*types):
    symbol=getattr(dll,name)
    symbol.restype=result
    symbol.argtypes=types
    return symbol


class Attributes(c.Structure):
    _fields_=[("nLength",w.DWORD),("lpSecurityDescriptor",c.c_void_p),("bInheritHandle",w.BOOL)]


make_descriptor=signature(security,"ConvertStringSecurityDescriptorToSecurityDescriptorW",w.BOOL,
                          w.LPCWSTR,w.DWORD,c.POINTER(c.c_void_p),c.POINTER(w.DWORD))
create_dir=signature(kernel,"CreateDirectoryW",w.BOOL,w.LPCWSTR,c.POINTER(Attributes))
create_file=signature(kernel,"CreateFileW",w.HANDLE,w.LPCWSTR,w.DWORD,w.DWORD,c.POINTER(Attributes),
                      w.DWORD,w.DWORD,w.HANDLE)
close_handle=signature(kernel,"CloseHandle",w.BOOL,w.HANDLE)
free=signature(kernel,"LocalFree",c.c_void_p,c.c_void_p)
get_security=signature(security,"GetFileSecurityW",w.BOOL,w.LPCWSTR,w.DWORD,c.c_void_p,w.DWORD,c.POINTER(w.DWORD))
get_control=signature(security,"GetSecurityDescriptorControl",w.BOOL,c.c_void_p,c.POINTER(w.WORD),c.POINTER(w.DWORD))
get_owner=signature(security,"GetSecurityDescriptorOwner",w.BOOL,c.c_void_p,c.POINTER(c.c_void_p),c.POINTER(w.BOOL))
get_acl=signature(security,"GetSecurityDescriptorDacl",w.BOOL,c.c_void_p,c.POINTER(w.BOOL),
                  c.POINTER(c.c_void_p),c.POINTER(w.BOOL))
get_ace=signature(security,"GetAce",w.BOOL,c.c_void_p,w.DWORD,c.POINTER(c.c_void_p))
equal_sid=signature(security,"EqualSid",w.BOOL,c.c_void_p,c.c_void_p)


def need(ok,reason):
    if not ok:
        raise ValueError(reason)


def win(ok):
    if not ok:
        raise c.WinError(c.get_last_error())


def hash_bytes(raw):
    return sha256(raw).hexdigest()


def is_regular(path,directory):
    info=path.lstat()
    kind=stat.S_ISDIR if directory else stat.S_ISREG
    need(kind(info.st_mode) and not getattr(info,"st_file_attributes",0)&REPARSE,
         f"Unexpected or redirected object: {path.name}")


def ancestors(path):
    for parent in reversed(path.parents):
        is_regular(parent,True)


def inventory(package):
    subject=package.read("candidata/launcher-subject.json")
    need(hash_bytes(subject)==SUBJECT,"Wrong protected candidate subject")
    plan=json.loads(subject)
    root={**plan["memberSha256"],**plan["assetSha256"],
          "launcher-subject.json":SUBJECT,"managed-activation.cjs":hash_bytes(INACTIVE)}
    manifest_raw=package.read("candidata/runtime-files.json")
    need(hash_bytes(manifest_raw)==plan["comparatorRuntimeManifestSha256"],"Runtime manifest differs")
    manifest=json.loads(manifest_raw)["files"]
    need(len(manifest)==3824,"Runtime namespace differs")
    roster={name:(None,h) for name,h in root.items()}
    roster.update({f"runtime/{name}":(it["bytes"],it["sha256"]) for name,it in manifest.items()})
    listing=set(package.namelist())
    need(len(listing)==len(package.namelist()),"Duplicate ZIP entries")
    for name in roster:
        p=PurePosixPath(name)
        need(not p.is_absolute() and str(p)==name and all(
            ch not in (".","..") and not any(k in ch for k in ("\\",":")) for ch in p.parts)
            and f"candidata/{name}" in listing,"Invalid member path")
    need(package.read("candidata/managed-activation.cjs")==INACTIVE,"Candidate is already active")
    return roster


def descriptor_attributes(stack,directory):
    sd=c.c_void_p()
    flags="OICI" if directory else ""
    sddl=f"O:BAD:P(A;{flags};FA;;;BA)(A;{flags};FA;;;SY)(A;{flags};0x1200a9;;;BU)"
    win(make_descriptor(sddl,1,c.byref(sd),None))
    stack.callback(free,sd)
    return sd,Attributes(c.sizeof(Attributes),sd,False)


def parts(sd):
    flags,revision=w.WORD(),w.DWORD()
    win(get_control(sd,c.byref(flags),c.byref(revision)))
    owner,defaulted=c.c_void_p(),w.BOOL()
    win(get_owner(sd,c.byref(owner),c.byref(defaulted)))
    present,acl=w.BOOL(),c.c_void_p()
    win(get_acl(sd,c.byref(present),c.byref(acl),c.byref(defaulted)))
    need(owner.value and present.value and acl.value and flags.value&0x1000,
         "Owner or explicit protected DACL missing")
    count=int.from_bytes(c.string_at(acl.value+4,2),"little")
    items=[]
    for index in range(count):
        ace=c.c_void_p()
        win(get_ace(acl,index,c.byref(ace)))
        size=int.from_bytes(c.string_at(ace.value+2,2),"little")
        items.append(c.string_at(ace,size))
    return owner,sorted(items)


class Secure:
    def __init__(self,stack):
        self.directories=descriptor_attributes(stack,True)
        self.files=descriptor_attributes(stack,False)

    def mkdir(self,path):
        win(create_dir(str(path),c.byref(self.directories[1])))

    def write(self,path,raw):
        handle=create_file(str(path),0x40000000,0,c.byref(self.files[1]),1,0x80,None)
        if handle==invalid:
            raise c.WinError(c.get_last_error())
        try:
            fd=msvcrt.open_osfhandle(handle,os.O_WRONLY|os.O_BINARY)
        except BaseException:
            close_handle(handle)
            raise
        with os.fdopen(fd,"wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

    def verify(self,path,directory):
        is_regular(path,directory)
        needed=w.DWORD()
        get_security(str(path),OWNER_DACL,None,0,c.byref(needed))
        need(0<needed.value<=65536,"Unexpected security descriptor size")
        raw=c.create_string_buffer(needed.value)
        win(get_security(str(path),OWNER_DACL,raw,len(raw),c.byref(needed)))
        actual,aces=parts(raw)
        want,expected=parts((self.directories if directory else self.files)[0])
        need(equal_sid(actual,want) and aces==expected,f"Owner or permissions differ: {path.name}")


class Scratch:
    def mkdir(self,path):
        path.mkdir()

    def write(self,path,raw):
        with path.open("xb") as stream:
            stream.write(raw)

    def verify(self,path,directory):
        is_regular(path,directory)


def readback(root,roster,policy):
    policy.verify(root,True)
    found={}
    expected_dirs={parent.as_posix() for name in roster for parent in PurePosixPath(name).parents
                   if parent != PurePosixPath(".")}
    seen_dirs=set()
    todo=[root]
    while todo:
        base=todo.pop()
        for path in base.iterdir():
            relative=path.relative_to(root).as_posix()
            info=path.lstat()
            if stat.S_ISDIR(info.st_mode):
                policy.verify(path,True)
                need(relative in expected_dirs,"Unexpected installed directory")
                seen_dirs.add(relative)
                todo.append(path)
            else:
                policy.verify(path,False)
                need(relative in roster,"Unexpected installed file")
                size,h=roster[relative]
                raw=path.read_bytes()
                need((size is None or size==len(raw)) and hash_bytes(raw)==h,"Installed byte mismatch")
                found[relative]=h
    need(found.keys()==roster.keys() and seen_dirs==expected_dirs,"Missing installed file or directory")
    return len(found)


def materialize(package,roster,dest,policy):
    ancestors(dest)
    need(not os.path.lexists(dest),"Target already exists")
    stage=dest.with_name(".staging-"+uuid4().hex)
    policy.mkdir(stage)
    for name,(size,h) in roster.items():
        relative=PurePosixPath(name)
        current=stage
        for part in relative.parts[:-1]:
            current=current/part
            if not current.exists():
                policy.mkdir(current)
            else:
                is_regular(current,True)
        raw=package.read(f"candidata/{name}")
        need(hash_bytes(raw)==h and (size is None or size==len(raw)),"ZIP payload differs from subject")
        policy.write(current/relative.name,raw)
    readback(stage,roster,policy)
    stage.rename(dest)
    return readback(dest,roster,policy)


def main():
    parser=ArgumentParser()
    parser.add_argument("mode",choices=("self-test","install-inactive","verify-installed"))
    parser.add_argument("archive",type=Path)
    parser.add_argument("receipt",type=Path)
    args=parser.parse_args()
    raw=args.archive.read_bytes()
    need(hash_bytes(raw)==IMAGE_SHA,"Unexpected deployment archive")
    need(not os.path.lexists(args.receipt),"Receipt already exists")
    with ZipFile(BytesIO(raw)) as package, ExitStack() as stack:
        roster=inventory(package)
        if args.mode=="self-test":
            policy=Secure(stack)
            need(len(parts(policy.directories[0])[1])==len(parts(policy.files[0])[1])==3,
                 "Unexpected explicit Windows descriptor")
            with TemporaryDirectory(dir=args.receipt.parent,prefix="install-lab-") as lab:
                dest=Path(lab)/"candidate"
                count=materialize(package,roster,dest,Scratch())
                try:
                    materialize(package,roster,dest,Scratch())
                except ValueError as error:
                    need(str(error)=="Target already exists","Wrong refusal at existing target")
                else:
                    raise ValueError("Existing directory accepted")
                need(readback(dest,roster,Scratch())==count,"Replicated installation changed")
            evidence="ISOLATED_COPY"
        else:
            need(os.environ.get("COMPUTERNAME","").upper()=="DSG-SHARED","Expected DSG-Shared")
            admin=bool(c.windll.shell32.IsUserAnAdmin())
            policy=Secure(stack)
            if args.mode=="install-inactive":
                need(admin,"Installation requires an elevated token")
                ancestors(BASE)
                if not os.path.lexists(BASE):
                    policy.mkdir(BASE)
                policy.verify(BASE,True)
                count=materialize(package,roster,DEST,policy)
                evidence="INACTIVE_INSTALLATION"
            else:
                need(not admin,"Verification requires an ordinary token")
                ancestors(DEST)
                policy.verify(BASE,True)
                count=readback(DEST,roster,policy)
                evidence="ORDINARY_TOKEN_READBACK"
    result=dict(schema="BKL046_CFA_TWO_DROP_INACTIVE_INSTALLER_V1",archiveSha256=IMAGE_SHA,
                subjectSha256=SUBJECT,filesVerified=count,evidence=evidence,
                existingTargetOverwrite=False,activationConfigured=False,admissionRequested=False,nativeExecutions=0)
    with args.receipt.open("x",encoding="utf8",newline="\n") as output:
        json.dump(result,output,indent=2,sort_keys=True,allow_nan=False)
        output.write("\n")


if __name__=="__main__":
    main()
