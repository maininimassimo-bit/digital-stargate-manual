"""Exercise the candidate with the archived 1680 fixed decisions and new controls."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, sources, output=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)

def digest(data):
    return sha256(data).hexdigest()
def exact(path,pin):
    blob=path.read_bytes()
    if digest(blob)!=pin:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return blob
def load_functions(prog,code):
    space={"__file__":str(prog),"__name__":"offline_test"}
    exec(compile(code,str(prog),"exec"),space)
    return space

program_path=sources/"replay_two_research_adapter_schemas_g_v2.py"
helpers=load_functions(program_path,exact(program_path,p["extractorSha256"]))
candidate_path=Path(__file__).with_name("schema-candidato.py")
candidate_bytes=candidate_path.read_bytes()
candidate=load_functions(candidate_path,candidate_bytes)
docs=[]
source=sources/"version-backend-offline-contract-pair-g-v1"
for name,pin in helpers["SOURCES"].items():
    content=json.loads(exact(source/name,pin))
    docs.extend(content["files"] if isinstance(content,dict) else content)
files={item["file"]:exact(source/item["file"],item["sha256"]) for item in docs}
assert len(files)==12
engine=helpers["build"](files,helpers["NEW"])
history=json.loads(exact(source/"report.json",p["archivedReportSha256"]))
fixtures=json.loads(exact(source/"frozen-fixtures.json",p["fixtureSha256"]))
assert history["fixtureSha256"]==p["fixtureSha256"]

runs=[]
for item in fixtures["fixtures"]:
    state=item["state"]
    historic=engine["schema"](state)
    proposed=candidate["build_schema"](historic,state)
    row={"fixture":item["id"],"comparisons":len(item["decisions"]),"runtimeAccepted":0,"historicGap":0,
         "candidateGap":0,"candidateFalseRejections":0}
    for decision in item["decisions"]:
        try:
            engine["decide"](decision,state)
        except engine["ProtocolError"]:
            valid=False
        else:
            valid=True
        old=helpers["conforms"](historic,decision)
        new=candidate["local_conforms"](proposed,decision,helpers["conforms"])
        assert not new or old
        row["runtimeAccepted"]+=valid
        row["historicGap"]+=old and not valid
        row["candidateGap"]+=new and not valid
        row["candidateFalseRejections"]+=valid and not new
    runs.append(row)

known=history["cases"]
for former,latter in zip(known,runs,strict=True):
    assert former["id"]==latter["fixture"]
    assert former["counts"]["newSchemaPermitsRuntimeRejected"]==latter["historicGap"]
    assert former["counts"]["bothRuntimeAccept"]==latter["runtimeAccepted"]
totals={k:sum(row[k] for row in runs) for k in runs[0] if k!="fixture"}
assert totals["comparisons"]==1680 and totals["historicGap"]==43
assert totals["candidateGap"]==totals["candidateFalseRejections"]==0

# New out-of-bank controls keep runtime enforcement separate from local schema.
state=fixtures["fixtures"][0]["state"]
valid_stop={"action":"STOP","bindingSha256":engine["sha"](state),"parentId":state["selectedId"],
            "checkpointId":None,"step":None,"rationale":"Fixture","limitations":"Fixture"}
schema=candidate["build_schema"](engine["schema"](state),state)
assert candidate["local_conforms"](schema,valid_stop,helpers["conforms"])
malformed={**valid_stop,"rationale":"é"*751}
assert candidate["local_conforms"](schema,malformed,helpers["conforms"])
try:
    engine["decide"](malformed,state)
except engine["ProtocolError"] as error:
    assert str(error)=="RESEARCH_DECISION_TEXT_LIMIT"
else:
    raise AssertionError("UTF8_LIMIT_NOT_ENFORCED")
changed={**valid_stop,"bindingSha256":"0"*64}
assert not candidate["local_conforms"](schema,changed,helpers["conforms"])

presentation={**state,"stage":"PRESENTATION"}
presentation_schema=candidate["build_schema"](engine["schema"](presentation),presentation)
test={**valid_stop,"action":"TEST","bindingSha256":engine["sha"](presentation),
      "step":{"process":"VIVIDNESS","parameters":{"saturation":.25}}}
assert candidate["local_conforms"](presentation_schema,test,helpers["conforms"])
assert engine["decide"](test,presentation)==test
for level in (-.01,.25001):
    outside={**test,"step":{"process":"VIVIDNESS","parameters":{"saturation":level}}}
    assert not candidate["local_conforms"](presentation_schema,outside,helpers["conforms"])
    try:
        engine["decide"](outside,presentation)
    except engine["ProtocolError"] as error:
        assert str(error)=="RESEARCH_VIVIDNESS_BOUND"
    else:
        raise AssertionError("VIVIDNESS_BOUND_NOT_ENFORCED")

result={"schema":"BKL046_ACTION_SPECIFIC_SCHEMA_OFFLINE_V1","vividnessBoundaryControls":3,"protocolSha256":digest(raw),
        "programSha256":digest(Path(__file__).read_bytes()),"candidateSha256":digest(candidate_bytes),
        "totals":totals,"fixtures":runs,"utf8RuntimeGuardStillRequired":True,"staleBindingRejected":True,
        "providerSchemaCompatibilityVerified":False,"deploymentApplied":False,
        "providerCalls":0,"nativeExecutions":0,"scientificClosures":0}
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(result,sort_keys=True,indent=2)+"\n")
print(json.dumps(totals,sort_keys=True))
