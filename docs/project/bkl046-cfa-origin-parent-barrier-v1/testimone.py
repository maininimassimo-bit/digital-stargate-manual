from hashlib import sha256
import json
from pathlib import Path
import sys

state, mode = Path(sys.argv[1]).resolve(), sys.argv[2]
file=Path(__file__).parent/"barriera.py"
raw=file.read_bytes()
assert sha256(raw).hexdigest()=="3079ade4179df04753e5406520ec2c5e751f18abb1d9cec5668f0870eab27b9f"
scope={"__name__":"fixture_parent"}
exec(compile(raw,str(file),"exec"),scope)
binding=scope["_wait"](state)
rid=binding["reservation"]
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
    "operation":binding["operation"],"reservation":rid,
    "planSha256":binding["casePlanSha256"],"candidateSha256":binding["subjectSha256"],
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
print(json.dumps(dict(status="ENTRY_STAGED",reservation=rid)),flush=True)
next_frame=sys.stdin.buffer.readline(1025)
decision=scope["record"](next_frame,{"reservation","comparisonSha256"})
assert decision["reservation"]==rid
assert len(decision["comparisonSha256"])==64

result=serve_fixture(Path(__file__).parent/"moduli",state/"measure",rid,decision["comparisonSha256"],intent["entrySha256"],mode)
print(json.dumps(dict(reservation=rid,boundParent=True,window=result,stage=observation)),flush=True)
sys.exit(0 if result["originalOrdinaryClose"] else 8)
