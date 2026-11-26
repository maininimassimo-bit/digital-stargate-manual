"""Record the boundary found when launching a distinct restricted fixture."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

out=Path(sys.argv[1])
root=Path(__file__).resolve().parent
exe=Path("C:/Windows/System32/cmd.exe")
flags=subprocess.CREATE_NO_WINDOW
env={"SystemRoot":r"C:\Windows","WINDIR":r"C:\Windows"}


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


with TemporaryDirectory(prefix="bkl046-process-control-",dir=out.parent) as tmp:
    folder=Path(tmp)
    source=folder/"input.txt"
    answer=folder/"output.txt"
    source.write_bytes(b"ordinary fixture")
    action=f'type "{source}" > "{answer}"'
    completed=subprocess.run(f'"{exe}" /d /v:off /c {action}',executable=str(exe),cwd=folder,env=env,
                             creationflags=flags,timeout=15,capture_output=True)
    require(completed.returncode==0 and answer.read_bytes()==source.read_bytes(),"Ordinary command control failed: "+str(completed.returncode))
    expected={"variante-iniziale.py":"Unexpected witness exit 3221225794",
              "variante-desktop.py":"Unexpected witness exit 3221225794",
              "variante-stazione.py":"[Errno 5] Create separate window station"}
    proofs={}
    for name,rejection in expected.items():
        file=root/name
        report=folder/(name+".json")
        raw=file.read_bytes()
        child=subprocess.run([sys.executable,"-I","-B","-S",str(file),str(report)],
                             capture_output=True,timeout=35,creationflags=flags)
        text=child.stderr.decode(errors="replace")
        require(child.returncode==1 and rejection in text and not report.exists(),
                "Different fixture outcome: "+name+" "+text.splitlines()[-1])
        proofs[name]=dict(programSha256=sha256(raw).hexdigest(),error=rejection,
                          successfulRestrictedFixtureReceiptCreated=False)
report=dict(schema="BKL046_IA_RESTRICTED_PROCESS_STARTUP_BOUNDARY_V1",
            ordinaryCmdControlPass=True,checkedTrials=proofs,
            restrictedChildPrimaryTokenObservedInFirstTwo=True,
            restrictedChildExecutedFileTests=False,separateProcessIsolationVerified=False,
            localSecurityPolicyChanged=False,providerCalls=0,independentConfirmationUnits=0,
            nativeExecutions=0,scientificClosures=0)
with out.open("x",encoding="utf-8",newline="\n") as f:
    json.dump(report,f,sort_keys=True,indent=2,allow_nan=False)
    f.write("\n")
