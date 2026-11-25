from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

root,out=map(Path,sys.argv[1:])
authority=root/"fonti"
manifest=authority/"batch-manifest.json"
primitive=authority/"archive_hold.py"
inputs=json.loads(manifest.read_bytes())
files=[(authority/"xdrz"/name,sha) for name,sha in inputs["xdrzSha256"].items()]
files.extend((authority/"fits"/name,sha) for name,sha in inputs["fitsInputsSha256"].items())
assert len(files)==18
for path,expected in files:
    assert sha256(path.read_bytes()).hexdigest()==expected

def spawn(source):
    return subprocess.Popen([sys.executable,"-I","-B","-S",str(root/"trattieni.py"),
                             str(manifest),str(primitive),str(source/"xdrz"),str(source/"fits")],
                            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NO_WINDOW)

def fixture(temporary):
    source=Path(temporary)
    for name in ("xdrz","fits"):
        shutil.copytree(authority/name,source/name)
    return source

with TemporaryDirectory(dir=out.parent,prefix="input-") as name:
    source=fixture(name)
    with spawn(source) as child:
        ready=json.loads(child.stdout.readline())
        assert ready=={"status":"HELD","xdrz":12,"fits":6}
        denied=0
        for original,expected in files:
            path=source/original.parent.name/original.name
            assert sha256(path.read_bytes()).hexdigest()==expected
            try:
                with path.open("r+b"):
                    pass
            except OSError as error:
                assert error.errno==13
                denied+=1
            else:
                raise AssertionError("write handle accepted while held")
        child.stdin.close()
        assert json.loads(child.stdout.readline())=={"status":"CLOSED"}
        assert child.wait(timeout=10)==0
        for original,expected in files:
            with (source/original.parent.name/original.name).open("r+b") as reader:
                assert sha256(reader.read()).hexdigest()==expected

scenarios=[]
for mode in ("changed-xdrz","missing-fits","writer-already-open"):
    with TemporaryDirectory(dir=out.parent,prefix="input-") as name:
        source=fixture(name)
        xml=next((source/"xdrz").glob("*.xdrz"))
        fit=next((source/"fits").glob("*.fits"))
        held=None
        if mode=="changed-xdrz":
            xml.write_bytes(xml.read_bytes()+b"\n")
        elif mode=="missing-fits":
            fit.unlink()
        else:
            held=fit.open("r+b")
        try:
            with spawn(source) as child:
                stdout,stderr=child.communicate(timeout=10)
                assert child.returncode!=0 and b'"HELD"' not in stdout
                expected={"changed-xdrz":b"MEMBER_DIFFERS:","missing-fits":b"FileNotFoundError",
                          "writer-already-open":b"[WinError 32]"}[mode]
                assert expected in stderr,stderr
        finally:
            if held is not None:
                held.close()
        # A failed hold must release its handles on previously validated members.
        for path in (source/"xdrz").iterdir():
            with path.open("r+b"):
                pass
        scenarios.append({"case":mode,"ready":False,"previousHandlesReleased":True})
report={"schema":"BKL046_CFA_ORIGIN_INPUT_CUSTODY_WINDOWS_V1","inputsTested":len(files),
        "readableWhileHeld":len(files),"writeDenied":denied,"writableAfterClose":len(files),
        "negative":scenarios,"fixtureOnVMNTFS":True,"nativeExecutions":0,"admissionRequested":False}
out.write_bytes((json.dumps(report,indent=2,sort_keys=True)+"\n").encode())
