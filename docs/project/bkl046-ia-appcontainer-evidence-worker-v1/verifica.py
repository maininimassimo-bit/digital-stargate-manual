"""Exercise real NTFS opens under a restricted thread token on DSG-Shared."""
from contextlib import ExitStack
import ctypes as c
from ctypes import wintypes as w
from hashlib import sha256
import json
import os
import subprocess
from uuid import uuid4
from pathlib import Path
import socket
import sys
from tempfile import TemporaryDirectory

source, out=map(Path,sys.argv[1:])
WORKER_PIN="cc82b2cff5f883ce2d1d880c35983154edad96683163007e23fff2f833fff21e"
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




class Attributes(c.Structure):
    _fields_=[("length",w.DWORD),("descriptor",c.c_void_p),("inherit",w.BOOL)]


pid=bind(kernel,"GetCurrentProcess",w.HANDLE)
close=bind(kernel,"CloseHandle",w.BOOL,w.HANDLE)
release=bind(kernel,"LocalFree",c.c_void_p,c.c_void_p)
token=bind(adv,"OpenProcessToken",w.BOOL,w.HANDLE,w.DWORD,c.POINTER(w.HANDLE))
token_info=bind(adv,"GetTokenInformation",w.BOOL,w.HANDLE,c.c_int,c.c_void_p,w.DWORD,c.POINTER(w.DWORD))
sid_to_string=bind(adv,"ConvertSidToStringSidW",w.BOOL,c.c_void_p,c.POINTER(c.c_void_p))
make_sd=bind(adv,"ConvertStringSecurityDescriptorToSecurityDescriptorW",w.BOOL,
             w.LPCWSTR,w.DWORD,c.POINTER(c.c_void_p),c.POINTER(w.DWORD))
create=bind(kernel,"CreateFileW",w.HANDLE,w.LPCWSTR,w.DWORD,w.DWORD,c.POINTER(Attributes),
            w.DWORD,w.DWORD,w.HANDLE)
read=bind(kernel,"ReadFile",w.BOOL,w.HANDLE,c.c_void_p,w.DWORD,c.POINTER(w.DWORD),c.c_void_p)
write=bind(kernel,"WriteFile",w.BOOL,w.HANDLE,c.c_void_p,w.DWORD,c.POINTER(w.DWORD),c.c_void_p)
mkdir=bind(kernel,"CreateDirectoryW",w.BOOL,w.LPCWSTR,c.POINTER(Attributes))


def new_descriptor(stack,sddl):
    out=c.c_void_p()
    checked(make_sd(sddl,1,c.byref(out),None),"Compile isolated DACL")
    stack.callback(release,out)
    return Attributes(c.sizeof(Attributes),out,False)


def open_handle(path,mask,flags=0,attributes=None,state=3):
    return create(str(path),mask,7,None if attributes is None else c.byref(attributes),state,flags,None)






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





class Startup(c.Structure):
    _fields_=[("cb",w.DWORD),("reserved",w.LPWSTR),("desktop",w.LPWSTR),("title",w.LPWSTR),
              *[(n,w.DWORD) for n in ("x","y","xsize","ysize","xchars","ychars","fill","flags")],
              ("show",w.WORD),("reserved_length",w.WORD),("reserved_pointer",c.c_void_p),
              ("stdin",w.HANDLE),("stdout",w.HANDLE),("stderr",w.HANDLE)]


class ProcessInfo(c.Structure):
    _fields_=[("process",w.HANDLE),("thread",w.HANDLE),("pid",w.DWORD),("tid",w.DWORD)]


resume=bind(kernel,"ResumeThread",w.DWORD,w.HANDLE)
wait=bind(kernel,"WaitForSingleObject",w.DWORD,w.HANDLE,w.DWORD)
exit_code=bind(kernel,"GetExitCodeProcess",w.BOOL,w.HANDLE,c.POINTER(w.DWORD))
terminate=bind(kernel,"TerminateProcess",w.BOOL,w.HANDLE,w.UINT)
current_pid=bind(kernel,"GetCurrentProcessId",w.DWORD)




class ExtendedStartup(c.Structure):
    _fields_=[("initial",Startup),("attributes",c.c_void_p)]


class Capabilities(c.Structure):
    _fields_=[("sid",c.c_void_p),("capabilities",c.c_void_p),("count",w.DWORD),("reserved",w.DWORD)]


userenv=c.WinDLL("userenv",use_last_error=True)
profile=bind(userenv,"CreateAppContainerProfile",c.c_long,w.LPCWSTR,w.LPCWSTR,w.LPCWSTR,
             c.c_void_p,w.DWORD,c.POINTER(c.c_void_p))
delete_profile=bind(userenv,"DeleteAppContainerProfile",c.c_long,w.LPCWSTR)
free_sid=bind(adv,"FreeSid",c.c_void_p,c.c_void_p)
equal_sid=bind(adv,"EqualSid",w.BOOL,c.c_void_p,c.c_void_p)
initialize=bind(kernel,"InitializeProcThreadAttributeList",w.BOOL,c.c_void_p,w.DWORD,w.DWORD,
                c.POINTER(c.c_size_t))
add_attribute=bind(kernel,"UpdateProcThreadAttribute",w.BOOL,c.c_void_p,w.DWORD,c.c_size_t,
                   c.c_void_p,c.c_size_t,c.c_void_p,c.c_void_p)
delete_attrs=bind(kernel,"DeleteProcThreadAttributeList",None,c.c_void_p)
spawn_container=bind(kernel,"CreateProcessW",w.BOOL,w.LPCWSTR,w.LPWSTR,c.c_void_p,c.c_void_p,
           w.BOOL,w.DWORD,c.c_void_p,w.LPCWSTR,c.POINTER(ExtendedStartup),c.POINTER(ProcessInfo))


def hresult(value,step):
    if value!=0:
        raise ValueError(f"{step}: HRESULT 0x{value & 0xffffffff:08X}")


def sid_string(stack,source):
    value=c.c_void_p()
    checked(sid_to_string(source,c.byref(value)),"Convert token identity")
    stack.callback(release,value)
    return c.wstring_at(value.value)


def start_container(sid,root,request,oracle,response,worker):
    exe=Path(sys.executable)
    command=c.create_unicode_buffer(subprocess.list2cmdline(
        [str(exe),"-I","-B","-S",str(worker),str(request),str(oracle),str(response)]))
    variables={k:os.environ[k] for k in ("SystemRoot","WINDIR","USERPROFILE","LOCALAPPDATA","TEMP","TMP")}
    variables["PATH"]=r"C:\Windows\System32"
    environment=c.create_unicode_buffer("\0".join(f"{k}={v}" for k,v in variables.items())+"\0\0")
    size=c.c_size_t()
    require(not initialize(None,1,0,c.byref(size)) and c.get_last_error()==122 and size.value,
            "Unexpected attribute allocation result")
    attrs=c.create_string_buffer(size.value)
    checked(initialize(attrs,1,0,c.byref(size)),"Initialize process attributes")
    try:
        caps=Capabilities(sid,None,0,0)
        checked(add_attribute(attrs,0,0x00020009,c.byref(caps),c.sizeof(caps),None,None),
                "Set AppContainer process attribute")
        startup=ExtendedStartup()
        startup.initial.cb=c.sizeof(startup)
        startup.attributes=c.cast(attrs,c.c_void_p)
        child=ProcessInfo()
        checked(spawn_container(str(exe),command,None,None,False,0x08080404,
                          environment,str(root),c.byref(startup),c.byref(child)),
                          "Launch AppContainer test process")
        try:
            require(child.pid!=current_pid() and child.pid>0,"Expected different process")
            handle=w.HANDLE()
            checked(token(child.process,8,c.byref(handle)),"Open child token")
            try:
                returned=w.DWORD()
                constrained=w.DWORD()
                checked(token_info(handle,29,c.byref(constrained),4,c.byref(returned)),
                        "Verify TokenIsAppContainer")
                require(constrained.value==1,"AppContainer token not applied")
                token_info(handle,31,None,0,c.byref(returned))
                require(0<returned.value<65536,"Unexpected AppContainer identity length")
                sidbuf=c.create_string_buffer(returned.value)
                checked(token_info(handle,31,sidbuf,len(sidbuf),c.byref(returned)),
                        "Verify AppContainer SID")
                actual=c.cast(sidbuf,c.POINTER(c.c_void_p))[0]
                require(bool(equal_sid(actual,sid)),"Unexpected child AppContainer identity")
                token_info(handle,30,None,0,c.byref(returned))
                capbuf=c.create_string_buffer(returned.value)
                checked(token_info(handle,30,capbuf,len(capbuf),c.byref(returned)),"Verify capabilities")
                require(c.cast(capbuf,c.POINTER(w.DWORD))[0]==0,"Unexpected token capabilities")
            finally:
                checked(close(handle),"Close child token")
            checked(resume(child.thread)!=0xffffffff,"Resume AppContainer test process")
            require(wait(child.process,10000)==0,"AppContainer child did not terminate")
            code=w.DWORD()
            checked(exit_code(child.process,c.byref(code)),"Read AppContainer child exit")
            require(code.value==0,f"AppContainer child exit 0x{code.value:08X}")
        finally:
            if wait(child.process,0)==258:
                checked(terminate(child.process,1),"Stop timed out synthetic child")
                require(wait(child.process,5000)==0,"Child still running")
            checked(close(child.thread),"Close child thread")
            checked(close(child.process),"Close child process")
    finally:
        delete_attrs(attrs)


require(socket.gethostname().upper()=="DSG-SHARED" and not c.windll.shell32.IsUserAnAdmin(),
        "Expected ordinary DSG-Shared process")
with TemporaryDirectory(dir=out.parent,prefix="bkl046-container-") as tmp, ExitStack() as stack:
    identity=w.HANDLE()
    checked(token(pid(),8,c.byref(identity)),"Open current token")
    stack.callback(close,identity)
    needed=w.DWORD()
    token_info(identity,1,None,0,c.byref(needed))
    require(0<needed.value<65536,"Unexpected token data length")
    buf=c.create_string_buffer(needed.value)
    checked(token_info(identity,1,buf,len(buf),c.byref(needed)),"Get token identity")
    owner=sid_string(stack,c.cast(buf,c.POINTER(c.c_void_p))[0])
    profile_name="DigitalStarGate.BKL046.Fixture."+uuid4().hex
    sid=c.c_void_p()
    hresult(profile(profile_name,"BKL046 test","Temporary AppContainer fixture",None,0,c.byref(sid)),
            "Create AppContainer fixture")
    stack.callback(lambda: hresult(delete_profile(profile_name),"Remove AppContainer fixture"))
    stack.callback(free_sid,sid)
    actor=sid_string(stack,sid)
    protected=f"D:P(A;;FA;;;{owner})(A;;FA;;;SY)(A;;RC;;;OW)"
    root=Path(tmp)/"separation"
    dacl=new_descriptor(stack,protected+f"(A;;0x1200a9;;;{actor})")
    checked(mkdir(str(root),c.byref(dacl)),"Create fixture directory")
    request,oracle,response,worker=(root/file for file in ("request.json","oracle.json","response.json","worker.py"))
    file_policy=new_descriptor(stack,protected+f"(A;;0x120089;;;{actor})")
    request_bytes=(source/"richieste-fixture.json").read_bytes()
    oracle_bytes=(source/"oracolo-fixture.json").read_bytes()
    require(sha256(request_bytes).hexdigest()=="7fadba3564fd2b074ff725687a96c46107d67ea65594df56f43480c0e2add597",
            "Changed synthetic requests")
    require(sha256(oracle_bytes).hexdigest()=="33916bb2495b6963b9a797f92b730cfabbb7afd2f1c37f5db30245b5e3472521",
            "Changed synthetic oracle")
    script=Path(__file__).with_name("worker.py").read_bytes()
    require(sha256(script).hexdigest()==WORKER_PIN,"Changed worker source")
    create_fixture(request,file_policy,request_bytes)
    create_fixture(oracle,new_descriptor(stack,protected),oracle_bytes)
    create_fixture(worker,file_policy,script)
    create_fixture(response,new_descriptor(stack,protected+f"(A;;0x12019f;;;{actor})S:(ML;;NW;;;LW)"),b"")
    start_container(sid,root,request,oracle,response,worker)
    raw_reply=response.read_bytes()
    verdict=json.loads(raw_reply)
    require(set(verdict)=={"readDenied","writeDenied","rows"} and verdict["readDenied"] is True
            and verdict["writeDenied"] is True,"Worker access boundary not verified")
    expected=json.loads(oracle_bytes)
    require(verdict["rows"]==expected and len(expected)==32,"Unexpected worker decisions")
    require(oracle.read_bytes()==oracle_bytes and request.read_bytes()==request_bytes,"Inputs changed")
report=dict(schema="BKL046_IA_APPCONTAINER_EVIDENCE_WORKER_V1",
            workerSha256=WORKER_PIN,replySha256=sha256(raw_reply).hexdigest(),
            syntheticTickets=32,verifiedFixtureClaims=128,distinctProcess=True,
            appContainerTokenAndSidChecked=True,capabilitiesGranted=0,
            handleInheritanceDisabled=True,profileDeleted=True,readRequestAndWriteResponseVerified=True,
            oracleReadDeniedByFixture=True,oracleWriteDeniedByFixture=True,oracleBytesUnchanged=True,
            productionAclsChanged=False,providerCalls=0,independentConfirmationUnits=0,
            scientificClosures=0,nativeExecutions=0)
with out.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
