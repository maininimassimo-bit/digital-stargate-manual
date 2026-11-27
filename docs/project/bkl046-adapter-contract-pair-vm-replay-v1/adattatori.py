"""Reconcile the pinned adapter contrast and classify remaining disagreements."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

protocol, sources, output = map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)
source_dir=sources/"version-backend-offline-contract-pair-g-v1"
program=sources/"replay_two_research_adapter_schemas_g_v2.py"

def digest(data):
    return sha256(data).hexdigest()
def exact(path,pin):
    data=path.read_bytes()
    if digest(data)!=pin:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return data

reference=exact(program,p["referenceProgramSha256"])
before=exact(source_dir/"report.json",p["historicalReportSha256"])
fixtures_raw=exact(source_dir/"frozen-fixtures.json",p["historicalFixturesSha256"])
fixtures=json.loads(fixtures_raw)

# Load only the archived helper definitions. It extracts selected pure runtime
# contract functions from pinned sources, without loading provider modules.
ctx={"__file__":str(program),"__name__":"archived_contract_helpers"}
exec(compile(reference,str(program),"exec"),ctx)
documents={}
for name,pin in ctx["SOURCES"].items():
    docs=json.loads(exact(source_dir/name,pin))
    documents.update({row["file"]:row["sha256"] for row in (docs["files"] if isinstance(docs,dict) else docs)})
assert len(documents)==12
for name in documents:
    assert re.fullmatch(r"[a-f0-9]{40}/[a-z_]+\.py",name)
files={name:exact(source_dir/name,pin) for name,pin in documents.items()}
new=ctx["build"](files,ctx["NEW"])

cases=[]
for item in fixtures["fixtures"]:
    state=item["state"]
    schema=new["schema"](state)
    gaps=[]
    for decision in item["decisions"]:
        if not ctx["conforms"](schema,decision):
            continue
        try:
            new["decide"](decision,state)
        except new["ProtocolError"] as error:
            gaps.append({"action":decision["action"],"reason":str(error),
                         "fixtureDecisionSha256":digest(json.dumps(decision,sort_keys=True,separators=(",",":")).encode())})
    cases.append({"fixture":item["id"],"gaps":gaps})
observed=json.loads(before)
expect={row["id"]:row["counts"]["newSchemaPermitsRuntimeRejected"] for row in observed["cases"]}
assert {row["fixture"]:len(row["gaps"]) for row in cases}==expect
gaps=[row for item in cases for row in item["gaps"]]
assert len(gaps)==43 and observed["comparisonCount"]==1680

with tempfile.TemporaryDirectory(prefix="contract-",dir=output) as temporary:
    root=Path(temporary)
    dest=root/source_dir.name
    dest.mkdir()
    replay_program=root/program.name
    replay_program.write_bytes(reference)
    for name,pin in ctx["SOURCES"].items():
        (dest/name).write_bytes(exact(source_dir/name,pin))
    for name,data in files.items():
        target=dest/name
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(data)
    completed=subprocess.run([sys.executable,"-I","-B","-S",str(replay_program)],
                             capture_output=True,text=True,timeout=40)
    if completed.returncode!=0:
        raise RuntimeError(completed.stderr)
    assert (dest/"frozen-fixtures.json").read_bytes()==fixtures_raw
    assert (dest/"report.json").read_bytes()==before

assert all(row["counts"]["validRemovedBySchema"]==0 and row["stopPreserved"] for row in observed["cases"])
assert observed["providerCalls"]==0
result={"schema":"BKL046_VM_ADAPTER_OFFLINE_REPLAY_V1","protocolSha256":digest(raw),
        "programSha256":digest(Path(__file__).read_bytes()),"revisions":observed["revisions"],
        "sourceBlobs":len(files),"exactArchiveReplay":True,"pairedDecisions":observed["comparisonCount"],
        "invalidRemoved":observed["removedInvalid"],"remainingRuntimeRejections":len(gaps),
        "gapsByAction":dict(Counter(row["action"] for row in gaps)),
        "gapsByReason":dict(Counter(row["reason"] for row in gaps)),
        "fixtures":cases,"stopControlsPreserved":len(cases),"providerCalls":0,"nativeExecutions":0,"scientificClosures":0}
with (output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(result,sort_keys=True,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ("pairedDecisions","invalidRemoved","remainingRuntimeRejections",
                                     "gapsByAction","gapsByReason")},sort_keys=True))
