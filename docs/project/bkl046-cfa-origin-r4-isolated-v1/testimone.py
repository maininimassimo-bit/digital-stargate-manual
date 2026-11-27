from hashlib import sha256
import json
import msvcrt
import os
from pathlib import Path
import sys

state, barrier, mode = sys.argv[1:]
state=Path(state)
b=Path(barrier)
raw=b.read_bytes()
if sha256(raw).hexdigest()!="7e035dfac74a0574d8b39f2b5700c347b80ecd149564d1aaca6506348cba003b":
    raise ValueError("barrier bytes changed")
scope={"__name__":"fixture_parent"}
exec(compile(raw,str(b),"exec"),scope)
born=scope["creation_filetime"]()
pid,caller=os.getpid(),os.getppid()
msvcrt.setmode(3,os.O_BINARY)
with os.fdopen(3,"wb",buffering=0) as pipe:
    pipe.write(f"{pid} {born}\n".encode("ascii"))
wire=sys.stdin.buffer.readline(2049)
request=scope["record"](wire,{"reservation","acquired","original"})
rid=request["reservation"]
assert len(rid)==36
active=(state/"active.json").read_bytes()
assert active==(state/(rid+"-acquired.json")).read_bytes()
assert sha256(active).hexdigest()==request["acquired"]
capture=(state/(rid+"-original.json")).read_bytes()
assert sha256(capture).hexdigest()==request["original"]
record=json.loads(active)
assert (record["reservation"],record["operation"],record["milestone"])==(rid,"BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001","BKL-046")
assert json.loads(capture)==dict(pid=pid,callerPid=caller,creationFiletime=int(born))
print(json.dumps(dict(reservation=rid,boundParent=True)),flush=True)
sys.exit(7 if mode=="parent-failed" else 0)
