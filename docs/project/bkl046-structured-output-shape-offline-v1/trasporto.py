"""Separate the documented Structured Outputs shape from runtime decision checks."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, parent, sources, out=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)

def sha(data):
    return sha256(data).hexdigest()

def exact(path,pin):
    data=path.read_bytes()
    if sha(data)!=pin:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return data

parent_protocol=parent/"protocollo.json"
exact(parent_protocol,p["parentProtocolSha256"])
exact(parent/"schema-candidato.py",p["candidateProgramSha256"])
source=parent/"verifica.py"
head,marker,_=exact(source,p["parentVerifierSha256"]).decode().partition("\nruns=[]")
assert marker
scope={"__file__":str(source),"__name__":"frozen_adapter_verifier"}
sys.argv=[str(source),str(parent_protocol),str(sources),str(out)]
exec(compile(head,str(source),"exec"),scope)
engine=scope["engine"]
fixtures=scope["fixtures"]
candidate=scope["candidate"]
primitive=scope["helpers"]["conforms"]
UNSUPPORTED={"not","allOf","dependentRequired","dependentSchemas","if","then","else"}

def omit_local_only(node):
    if type(node) is list:
        return [omit_local_only(item) for item in node]
    if type(node) is dict:
        return {key:omit_local_only(value) for key,value in node.items() if key!="not"}
    return node

def make_wire(state):
    branches=candidate["build_schema"](engine["schema"](state),state)
    return {"type":"object","properties":{"decision":omit_local_only(branches)},
            "required":["decision"],"additionalProperties":False}

def check_wire(schema,root=True):
    if UNSUPPORTED & set(schema):
        raise ValueError("UNSUPPORTED_SCHEMA_KEYWORD")
    if root and (schema.get("type")!="object" or "anyOf" in schema):
        raise ValueError("INVALID_SCHEMA_ROOT")
    if schema.get("type")=="object":
        if schema.get("additionalProperties") is not False or set(schema["required"])!=schema["properties"].keys():
            raise ValueError("OPEN_OR_OPTIONAL_OBJECT")
        for child in schema["properties"].values():
            check_wire(child,False)
    if "anyOf" in schema:
        for branch in schema["anyOf"]:
            check_wire(branch,False)

def accepts_wire(schema, wrapped):
    return candidate["local_conforms"](schema,wrapped,primitive)

def finalize(schema, wrapped, state):
    if not accepts_wire(schema,wrapped):
        return "WIRE_REJECTED"
    try:
        decision=engine["decide"](wrapped["decision"],state)
    except engine["ProtocolError"] as error:
        return str(error)
    return decision

rows=[]
for group in fixtures["fixtures"]:
    state=group["state"]
    schema=make_wire(state)
    check_wire(schema)
    result={"fixture":group["id"],"compared":len(group["decisions"]),"runtimeAccepted":0,
            "wireAcceptsRuntimeRejects":0,"falseRejections":0,"acceptedByBoth":0,"remainingRuntimeReasons":{}}
    for decision in group["decisions"]:
        try:
            expected=engine["decide"](decision,state)
        except engine["ProtocolError"]:
            expected=None
        observed=finalize(schema,{"decision":decision},state)
        valid=expected is not None
        if type(observed) is dict:
            assert observed==expected
        result["runtimeAccepted"]+=valid
        result["acceptedByBoth"]+=type(observed) is dict
        result["falseRejections"]+=valid and type(observed) is not dict
        if not valid and observed!="WIRE_REJECTED":
            result["wireAcceptsRuntimeRejects"]+=1
            reasons=result["remainingRuntimeReasons"]
            reasons[observed]=reasons.get(observed,0)+1
    rows.append(result)

stats={key:sum(x[key] for x in rows) for key in rows[0] if key not in ("fixture","remainingRuntimeReasons")}
assert stats=={"compared":1680,"runtimeAccepted":16,"wireAcceptsRuntimeRejects":2,
               "falseRejections":0,"acceptedByBoth":16}
assert {k for row in rows for k in row["remainingRuntimeReasons"]}=={"RESEARCH_IDENTICAL_TRIAL_REPLAY"}

state=fixtures["fixtures"][0]["state"]
schema=make_wire(state)
stop={"action":"STOP","bindingSha256":engine["sha"](state),"parentId":state["selectedId"],
      "checkpointId":None,"step":None,"rationale":"Control","limitations":"Control"}
assert finalize(schema,{"decision":stop},state)==stop
assert finalize(schema,stop,state)=="WIRE_REJECTED"
assert finalize(schema,{"decision":stop,"extra":True},state)=="WIRE_REJECTED"
assert finalize(schema,{"decision":{**stop,"rationale":"é"*751}},state)=="RESEARCH_DECISION_TEXT_LIMIT"
try:
    check_wire(candidate["build_schema"](engine["schema"](state),state))
except ValueError as error:
    assert str(error)=="INVALID_SCHEMA_ROOT"
else:
    raise AssertionError("ROOT_UNION_ACCEPTED")

report={"schema":"BKL046_ADAPTER_STRUCTURED_OUTPUT_SHAPE_OFFLINE_V1","protocolSha256":sha(raw),
        "programSha256":sha(Path(__file__).read_bytes()),"documentation":p["reference"],"totals":stats,
        "fixtures":rows,"testedStructuralConstraints":"root object, nested branches, required closed objects",
        "actualProviderSchemaAcceptanceVerified":False,"providerCalls":0,"nativeExecutions":0,
        "scientificClosures":0}
with out.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(report,sort_keys=True,indent=2)+"\n")
print(json.dumps(stats,sort_keys=True))
