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
request=scope["record"](wire,{"reservation","acquired","original","comparison"})
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
sys.path.insert(0,str(Path(__file__).parent))
from stage import stage
from finestra import serve_fixture

p=Path(__file__).parent/"prepara.py"
pin="13c011ede4c4efc1d1a32b20b933f83c47adebe9734b329c1367dc1f24c87beb"
source=p.read_bytes()
assert sha256(source).hexdigest()==pin
prepare={"__name__":"origin_intent","__file__":str(p)}
exec(compile(source,str(p),"exec"),prepare)
intent,entry=prepare["prepare"]({
    "operation":record["operation"],"reservation":rid,
    "planSha256":prepare["PLAN_PIN"],"candidateSha256":prepare["BATCH_PIN"],
})
base=state/"entry-fixture"
base.mkdir()
try:
    stage(intent,entry+b" ",base)
except ValueError as error:
    assert str(error)=="ENTRY_BYTES_DIFFER" and not (base/rid).exists()
else:
    raise ValueError("altered entry unexpectedly staged")
target=stage(intent,entry,base)
try:
    stage(intent,entry,base)
except FileExistsError:
    assert target.read_bytes()==entry
else:
    raise ValueError("duplicate reservation unexpectedly staged")
observation={"reservation":rid,"realCommandExecuted":False,"entrySha256":sha256(entry).hexdigest(),
             "exactReadback":target.read_bytes()==entry,"badBytesRejected":True,"duplicateRefused":True}
result=serve_fixture(Path(__file__).parent/"moduli",state/"measure",rid,request["comparison"],intent["entrySha256"],mode)
print(json.dumps(dict(reservation=rid,boundParent=True,window=result,stage=observation)),flush=True)
sys.exit(0 if result["originalOrdinaryClose"] else 8)
