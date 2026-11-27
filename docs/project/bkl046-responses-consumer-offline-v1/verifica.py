"""Replay the candidate response consumer using exact adapter inputs and local fixtures."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, transport, local, historical, output=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)

def digest(content):
    return sha256(content).hexdigest()

def check(path,pin):
    content=path.read_bytes()
    if digest(content)!=pin:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return content

old_protocol=transport/"protocollo.json"
check(old_protocol,p["transportProtocolSha256"])
source=transport/"trasporto.py"
prefix,marker,_=check(source,p["transportProgramSha256"]).decode().partition("\nrows=[]")
assert marker
ctx={"__file__":str(source),"__name__":"frozen_wire"}
sys.argv=[str(source),str(old_protocol),str(local),str(historical),str(output)]
exec(compile(prefix,str(source),"exec"),ctx)
engine=ctx["engine"]
guard=Path(__file__).with_name("consuma.py")
guard_raw=guard.read_bytes()
consumer={"__name__":"response_consumer"}
exec(compile(guard_raw,str(guard),"exec"),consumer)
model=p["fixedModelFixture"]

def body(value,case="test"):
    return {"id":"resp_"+case,"object":"response","status":"completed",
            "model":model,"output":[{"type":"message","role":"assistant","status":"completed",
                                      "content":[{"type":"output_text","text":json.dumps(value)}]}]}

def run(raw_response,schema,state,seen):
    try:
        nested=consumer["extract"](raw_response,model,seen)
    except consumer["RejectedResponse"] as error:
        return {"state":str(error),"runtimeCalled":False}
    result=ctx["finalize"](schema,nested,state)
    return {"state":"ACCEPTED" if type(result) is dict else result,"wireOrDecisionChecked":True,"result":result}

def encode(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()

positives=0
for group in ctx["fixtures"]["fixtures"]:
    state=group["state"]
    schema=ctx["make_wire"](state)
    for decision in group["decisions"]:
        try:
            valid=engine["decide"](decision,state)
        except engine["ProtocolError"]:
            continue
        result=run(encode(body({"decision":decision})),schema,state,set())
        assert result["state"]=="ACCEPTED" and result["result"]==valid
        positives+=1
assert positives==16

state=ctx["fixtures"]["fixtures"][0]["state"]
schema=ctx["make_wire"](state)
stop={"action":"STOP","bindingSha256":engine["sha"](state),"parentId":state["selectedId"],
      "checkpointId":None,"step":None,"rationale":"Control","limitations":"Control"}
good=body({"decision":stop})
msg=good["output"][0]
cases={
 "incomplete":({**good,"status":"incomplete","incomplete_details":{"reason":"max_output_tokens"}},"RESPONSE_INCOMPLETE"),
 "nonterminal":({**good,"status":"in_progress"},"RESPONSE_NOT_COMPLETED"),
 "completionWithError":({**good,"error":{"code":"fixture"}},"RESPONSE_NOT_COMPLETED"),
 "providerMismatch":({**good,"model":"different-fixture-model"},"MODEL_IDENTITY_MISMATCH"),
 "unexpectedTool":({**good,"output":[{"type":"function_call"},msg]},"UNEXPECTED_OUTPUT_ITEM"),
 "twoMessages":({**good,"output":[msg,msg]},"ASSISTANT_MESSAGE_REQUIRED"),
 "refusal":({**good,"output":[{**msg,"content":[{"type":"refusal","refusal":"Fixture"}]}]},"RESPONSE_REFUSAL"),
 "mixedRefusal":({**good,"output":[{**msg,"content":msg["content"]+[{"type":"refusal"}]}]},"RESPONSE_REFUSAL"),
 "multipleTexts":({**good,"output":[{**msg,"content":msg["content"]*2}]},"SINGLE_STRUCTURED_TEXT_REQUIRED"),
 "staleBinding":(body({"decision":{**stop,"bindingSha256":"0"*64}}),"WIRE_REJECTED"),
 "longUtf8":(body({"decision":{**stop,"rationale":"é"*751}}),"RESEARCH_DECISION_TEXT_LIMIT"),
}
summary={}
for label,(response,expect) in cases.items():
    result=run(encode(response),schema,state,set())
    assert result["state"]==expect
    summary[label]=expect
ambiguous=deepcopy(good)
ambiguous["output"][0]["content"][0]["text"]='{"decision":{},"decision":{}}'
assert run(encode(ambiguous),schema,state,set())["state"]=="DUPLICATE_JSON_KEY"
summary["duplicateNestedKey"]="DUPLICATE_JSON_KEY"
assert run(b"{",schema,state,set())["state"]=="MALFORMED_JSON"
summary["truncatedJson"]="MALFORMED_JSON"
assert run(b'{"n":1e999}',schema,state,set())["state"]=="NONFINITE_JSON_NUMBER"
summary["nonfiniteJson"]="NONFINITE_JSON_NUMBER"
assert run(b"["*3000+b"]"*3000,schema,state,set())["state"]=="MALFORMED_JSON"
summary["excessiveNesting"]="MALFORMED_JSON"
assert run(b" "*65537,schema,state,set())["state"]=="RESPONSE_SIZE"
summary["oversize"]="RESPONSE_SIZE"
with_reasoning={**good,"output":[{"type":"reasoning","summary":[]},msg]}
seen=set()
assert run(encode(with_reasoning),schema,state,seen)["state"]=="ACCEPTED"
assert run(encode(with_reasoning),schema,state,seen)["state"]=="DUPLICATE_RESPONSE_ID"
summary["duplicateId"]="DUPLICATE_RESPONSE_ID"
result={"schema":"BKL046_ADAPTER_RESPONSES_CONSUMER_OFFLINE_V1","protocolSha256":digest(raw),
        "programSha256":digest(Path(__file__).read_bytes()),"consumerSha256":digest(guard_raw),
        "validArchivedDecisionsPreserved":positives,"negativeFixtures":summary,
        "reasoningAndSingleTextFixtureAccepted":True,"providerCalls":0,"nativeExecutions":0,"scientificClosures":0}
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(result,sort_keys=True,indent=2)+"\n")
print(json.dumps(result,sort_keys=True))
