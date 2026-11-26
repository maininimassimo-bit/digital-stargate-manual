"""Exercise real NTFS opens under a restricted thread token on DSG-Shared."""
from contextlib import ExitStack
import ctypes as c
from ctypes import wintypes as w
from hashlib import sha256
import json
from pathlib import Path
import socket
import sys
from tempfile import TemporaryDirectory

out=Path(sys.argv[1])
adv=c.WinDLL("advapi32",use_last_error=True)
kernel=c.WinDLL("kernel32",use_last_error=True)
invalid=c.c_void_p(-1).value


def bind(dll,name,result,*args):
    fn=getattr(dll,name)
    fn.restype=result
    fn.argtypes=args
    return fn


def checked(ok, step):
    if not ok:
        raise OSError(c.get_last_error(),step)


def require(ok, message):
    if not ok:
        raise ValueError(message)


class SidAttributes(c.Structure):
    _fields_=[("sid",c.c_void_p),("attributes",w.DWORD)]


class Attributes(c.Structure):
    _fields_=[("length",w.DWORD),("descriptor",c.c_void_p),("inherit",w.BOOL)]


pid=bind(kernel,"GetCurrentProcess",w.HANDLE)
tid=bind(kernel,"GetCurrentThread",w.HANDLE)
close=bind(kernel,"CloseHandle",w.BOOL,w.HANDLE)
release=bind(kernel,"LocalFree",c.c_void_p,c.c_void_p)
token=bind(adv,"OpenProcessToken",w.BOOL,w.HANDLE,w.DWORD,c.POINTER(w.HANDLE))
thread_token=bind(adv,"OpenThreadToken",w.BOOL,w.HANDLE,w.DWORD,w.BOOL,c.POINTER(w.HANDLE))
token_info=bind(adv,"GetTokenInformation",w.BOOL,w.HANDLE,c.c_int,c.c_void_p,w.DWORD,c.POINTER(w.DWORD))
sid_from_string=bind(adv,"ConvertStringSidToSidW",w.BOOL,w.LPCWSTR,c.POINTER(c.c_void_p))
sid_to_string=bind(adv,"ConvertSidToStringSidW",w.BOOL,c.c_void_p,c.POINTER(c.c_void_p))
make_sd=bind(adv,"ConvertStringSecurityDescriptorToSecurityDescriptorW",w.BOOL,
             w.LPCWSTR,w.DWORD,c.POINTER(c.c_void_p),c.POINTER(w.DWORD))
restrict=bind(adv,"CreateRestrictedToken",w.BOOL,w.HANDLE,w.DWORD,w.DWORD,c.c_void_p,w.DWORD,c.c_void_p,
              w.DWORD,c.POINTER(SidAttributes),c.POINTER(w.HANDLE))
is_restricted=bind(adv,"IsTokenRestricted",w.BOOL,w.HANDLE)
as_user=bind(adv,"ImpersonateLoggedOnUser",w.BOOL,w.HANDLE)
revert=bind(adv,"RevertToSelf",w.BOOL)
create=bind(kernel,"CreateFileW",w.HANDLE,w.LPCWSTR,w.DWORD,w.DWORD,c.POINTER(Attributes),
            w.DWORD,w.DWORD,w.HANDLE)
read=bind(kernel,"ReadFile",w.BOOL,w.HANDLE,c.c_void_p,w.DWORD,c.POINTER(w.DWORD),c.c_void_p)
write=bind(kernel,"WriteFile",w.BOOL,w.HANDLE,c.c_void_p,w.DWORD,c.POINTER(w.DWORD),c.c_void_p)
mkdir=bind(kernel,"CreateDirectoryW",w.BOOL,w.LPCWSTR,c.POINTER(Attributes))
RESTRICTED_CODE="S-1-5-12"


def new_descriptor(stack,sddl):
    out=c.c_void_p()
    checked(make_sd(sddl,1,c.byref(out),None),"Compile isolated DACL")
    stack.callback(release,out)
    return Attributes(c.sizeof(Attributes),out,False)


def open_handle(path,mask,flags=0,attributes=None,state=3):
    return create(str(path),mask,7,None if attributes is None else c.byref(attributes),state,flags,None)


def result(path,mask,directory=False):
    flags=0x00200000|(0x02000000 if directory else 0)
    handle=open_handle(path,mask,flags)
    if handle==invalid:
        return c.get_last_error()
    checked(close(handle),"Close access-test handle")
    return 0


def values(path):
    return {name:result(path,mask) for name,mask in
            (("readData",0x1),("writeData",0x2),("delete",0x10000),
             ("writeDacl",0x40000),("writeOwner",0x80000))}


def payload(path):
    handle=open_handle(path,1)
    checked(handle!=invalid,"Read permitted fixture")
    try:
        reading=c.create_string_buffer(128)
        seen=w.DWORD()
        checked(read(handle,reading,len(reading),c.byref(seen),None),"Read fixture bytes")
        return reading.raw[:seen.value]
    finally:
        checked(close(handle),"Close fixture handle")


def create_fixture(path,descriptor,content):
    handle=open_handle(path,2,attributes=descriptor,state=1)
    checked(handle!=invalid,"Create isolated fixture file")
    try:
        written=w.DWORD()
        checked(write(handle,content,len(content),c.byref(written),None),"Write fixture bytes")
        require(written.value==len(content),"Partial fixture write")
    finally:
        checked(close(handle),"Close fixture file handle")


def put_response(path,content):
    handle=open_handle(path,2)
    checked(handle!=invalid,"Open response spool")
    try:
        written=w.DWORD()
        checked(write(handle,content,len(content),c.byref(written),None),"Write response spool")
        require(written.value==len(content),"Partial fixture response")
    finally:
        checked(close(handle),"Close response spool")



class Startup(c.Structure):
    _fields_=[("cb",w.DWORD),("reserved",w.LPWSTR),("desktop",w.LPWSTR),("title",w.LPWSTR),
              *[(n,w.DWORD) for n in ("x","y","xsize","ysize","xchars","ychars","fill","flags")],
              ("show",w.WORD),("reserved_length",w.WORD),("reserved_pointer",c.c_void_p),
              ("stdin",w.HANDLE),("stdout",w.HANDLE),("stderr",w.HANDLE)]


class ProcessInfo(c.Structure):
    _fields_=[("process",w.HANDLE),("thread",w.HANDLE),("pid",w.DWORD),("tid",w.DWORD)]


spawn=bind(adv,"CreateProcessAsUserW",w.BOOL,w.HANDLE,w.LPCWSTR,w.LPWSTR,c.c_void_p,c.c_void_p,
           w.BOOL,w.DWORD,c.c_void_p,w.LPCWSTR,c.POINTER(Startup),c.POINTER(ProcessInfo))
resume=bind(kernel,"ResumeThread",w.DWORD,w.HANDLE)
wait=bind(kernel,"WaitForSingleObject",w.DWORD,w.HANDLE,w.DWORD)
exit_code=bind(kernel,"GetExitCodeProcess",w.BOOL,w.HANDLE,c.POINTER(w.DWORD))
terminate=bind(kernel,"TerminateProcess",w.BOOL,w.HANDLE,w.UINT)
current_pid=bind(kernel,"GetCurrentProcessId",w.DWORD)


def evaluate_child(restricted,root,request,oracle,response):
    exe=Path("C:/Windows/System32/cmd.exe")
    require(all(not any(mark in str(path) for mark in ('"','%','!','&','\r','\n'))
                for path in (root,request,oracle,response)),"Unexpected fixture path")
    action=(f'type "{request}" > "{response}" || exit /b 91 & '
            f'type "{oracle}" >> "{response}" && exit /b 92 & exit /b 0')
    command=c.create_unicode_buffer(f'"{exe}" /d /v:off /c {action}')
    environment=c.create_unicode_buffer("SystemRoot=C:\\Windows\0WINDIR=C:\\Windows\0\0")
    info=Startup()
    info.cb=c.sizeof(Startup)
    child=ProcessInfo()
    # Suspended initially so the caller can check the actual primary token before any command executes.
    checked(spawn(restricted,str(exe),command,None,None,False,0x08000404,
                  environment,str(root),c.byref(info),c.byref(child)),"Start distinct restricted witness")
    try:
        require(child.pid and child.pid!=current_pid(),"Expected distinct process")
        handle=w.HANDLE()
        checked(token(child.process,8,c.byref(handle)),"Read child primary token")
        try:
            require(bool(is_restricted(handle)),"Child token not restricted")
        finally:
            checked(close(handle),"Close child token")
        checked(resume(child.thread)!=0xffffffff,"Resume restricted witness")
        require(wait(child.process,10000)==0,"Restricted witness did not terminate")
        code=w.DWORD()
        checked(exit_code(child.process,c.byref(code)),"Read child exit")
        require(code.value==0,f"Unexpected witness exit {code.value}")
        return {"distinctChildObserved":True,"restrictedPrimaryTokenCheckedBeforeResume":True,
                "win32HandleInheritanceDisabled":True,"fixtureCommandsExit":int(code.value)}
    finally:
        if wait(child.process,0)==258:
            checked(terminate(child.process,1),"Stop timed-out witness fixture")
            require(wait(child.process,5000)==0,"Witness fixture stop did not complete")
        checked(close(child.thread),"Close witness thread")
        checked(close(child.process),"Close witness process")

require(socket.gethostname().upper()=="DSG-SHARED" and not c.windll.shell32.IsUserAnAdmin(),
        "Expected ordinary DSG-Shared process")
with TemporaryDirectory(dir=out.parent,prefix="bkl046-restricted-") as scratch, ExitStack() as stack:
    proc=w.HANDLE()
    checked(token(pid(),0x000B,c.byref(proc)),"Open current token")
    stack.callback(close,proc)
    needed=w.DWORD()
    token_info(proc,1,None,0,c.byref(needed))
    require(0<needed.value<65536,"Unexpected token identity length")
    user=c.create_string_buffer(needed.value)
    checked(token_info(proc,1,user,len(user),c.byref(needed)),"Get local token user")
    user_sid=c.cast(user,c.POINTER(c.c_void_p))[0]
    name=c.c_void_p()
    checked(sid_to_string(user_sid,c.byref(name)),"Convert local token identity")
    account=c.wstring_at(name.value)
    stack.callback(release,name)
    rc=c.c_void_p()
    checked(sid_from_string(RESTRICTED_CODE,c.byref(rc)),"Get restricted-code SID")
    stack.callback(release,rc)
    sid=SidAttributes(rc,0)
    restricted=w.HANDLE()
    checked(restrict(proc,1,0,None,0,None,1,c.byref(sid),c.byref(restricted)),"Create restricted token")
    stack.callback(close,restricted)
    require(is_restricted(restricted),"Token lacks restriction")

    root=Path(scratch)/"separation"
    base=f"D:P(A;;FA;;;{account})(A;;FA;;;SY)(A;;RC;;;OW)"
    directory=new_descriptor(stack,base+f"(A;;0x1200a9;;;{RESTRICTED_CODE})")
    read_only=new_descriptor(stack,base+f"(A;;0x120089;;;{RESTRICTED_CODE})")
    secret=new_descriptor(stack,base)
    spool=new_descriptor(stack,base+f"(A;;0x12008b;;;{RESTRICTED_CODE})")
    checked(mkdir(str(root),c.byref(directory)),"Create isolated directory")
    request,oracle,answer=(root/name for name in ("request.txt","oracle.txt","response.txt"))
    create_fixture(request,read_only,b"request synthetic")
    create_fixture(oracle,secret,b"oracle synthetic")
    create_fixture(answer,spool,b"")
    require(payload(oracle)==b"oracle synthetic","Owner control unreadable")
    separate_spool=root/"response-process.txt"
    shell_spool=new_descriptor(stack,base+f"(A;;0x12019f;;;{RESTRICTED_CODE})")
    create_fixture(separate_spool,shell_spool,b"")
    child_report=evaluate_child(restricted,root,request,oracle,separate_spool)
    require(payload(separate_spool)==b"request synthetic" and payload(oracle)==b"oracle synthetic",
            "Child response or protected bytes differ")
    checked(as_user(restricted),"Impersonate restricted token")
    try:
        applied=w.HANDLE()
        checked(thread_token(tid(),0x8,True,c.byref(applied)),"Open active thread token")
        try:
            require(is_restricted(applied),"Thread token not restricted")
        finally:
            checked(close(applied),"Close active thread token")
        acl={name:values(path) for name,path in (("request",request),("oracle",oracle),("response",answer))}
        require(payload(request)==b"request synthetic","Restricted request byte check failed")
        require(acl["response"]["writeData"]==0,"Fixture response not writable")
        put_response(answer,b"response synthetic")
        parent_denial={name:result(root,mask,True)
                       for name,mask in (("addFile",2),("deleteChild",0x40),("writeDacl",0x40000))}
    finally:
        checked(revert(),"Leave restricted token")
    expected={"readData":5,"writeData":5,"delete":5,"writeDacl":5,"writeOwner":5}
    require(acl["oracle"]==expected and acl["request"]==dict(expected,readData=0),
            "Unexpected protected fixture rights")
    require(all(value==5 for value in parent_denial.values()),"Unexpected parent rights")
    require(payload(oracle)==b"oracle synthetic" and payload(answer)==b"response synthetic",
            "Owner readback failed")
report=dict(schema="BKL046_IA_RESTRICTED_PROCESS_FIXTURE_V1",actualRestrictedThreadTokenObserved=True,
            normalOwnerOracleReadVerified=True,restrictedNtfsAccessCodes=acl,
            restrictedParentAccessCodes=parent_denial,ownerResponseReadbackVerified=True,
            sourceSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
            separateProcessFixtureVerified=True, child=child_report,productionAclChanged=False,
            providerCalls=0,independentConfirmationUnits=0,nativeExecutions=0,scientificClosures=0)
with out.open("x",encoding="utf8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
