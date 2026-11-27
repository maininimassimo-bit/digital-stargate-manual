"""Replay the historical deterministic v18–v20 comparison on the VM."""
from hashlib import sha256
import json
from pathlib import Path
import sys

config, source, output=map(Path,sys.argv[1:])
raw=config.read_bytes()
p=json.loads(raw)

def digest(raw):
    return sha256(raw).hexdigest()

def checked(path, pin):
    raw=path.read_bytes()
    if digest(raw)!=pin:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return raw

history=source/"version-backend-knowledge-v18-v20-exact-g-v1"
plan=json.loads(checked(history/"protocol.json",p["historicalProtocolSha256"]))
old=json.loads(checked(history/"report.json",p["historicalReportSha256"]))
assert old["protocolSha256"]==p["historicalProtocolSha256"]
reader=source/p["reader"]
namespace={"__name__":"frozen_local_reader","__file__":str(reader)}
exec(compile(checked(reader,plan["readerSha256"]),str(reader),"exec"),namespace)
versions={}
for label,pin in plan["knowledgePins"].items():
    name="Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-g-v"+label+".json"
    dataset=namespace["load"](source/name,pin)
    audit=namespace["audit"](dataset)
    assert audit["requirements"]==4920 and audit["scientificClosures"]==0
    versions[int(label)]=dataset

comparisons=[]
for item in old["fileComparisons"]:
    left=versions[item["before"]]["requirements"]
    right=versions[item["after"]]["requirements"]
    assert left.keys()==right.keys()
    changes=[]
    decision_changes=0
    for key in left:
        a,b=left[key],right[key]
        if a!=b:
            if a["residual"]["recordedDisposition"]!=b["residual"]["recordedDisposition"]:
                decision_changes+=1
            assert {k:v for k,v in a.items() if k!="additionalScopedEvidenceIds"}=={
                     k:v for k,v in b.items() if k!="additionalScopedEvidenceIds"}
            before=a["additionalScopedEvidenceIds"]
            after=b["additionalScopedEvidenceIds"]
            assert after==before+[item["addedCard"]]
            changes.append(key)
    result={"before":item["before"],"after":item["after"],"rows":len(left),
            "changedEvidenceRows":changes,"changedDecisions":decision_changes}
    assert changes==item["requirementRowsWithAddedEvidence"]
    assert decision_changes==item["recordedDecisionChanges"]==0
    comparisons.append(result)

checks={}
queries=0
for order in plan["executionOrder"]:
    for version in order:
        for identifier in plan["workflowProbes"]:
            response=namespace["inspect"](versions[version],identifier)
            fingerprint=digest(json.dumps(response,sort_keys=True,separators=(",",":"),
                                ensure_ascii=False,allow_nan=False).encode())
            key=(version,identifier)
            if key in checks:
                assert checks[key]==fingerprint
            checks[key]=fingerprint
            queries+=1
            assert response["nativeExecutionAuthorizedByThisQuery"] is False
            cards=[r["id"] for r in response["scopedEvidence"]]
            expect=old["readerChecks"]["matchedWorkflows"][identifier]["evidenceByVersion"][str(version)]
            assert cards==expect

try:
    namespace["inspect"](versions[20],"process:drizzleintegration")
except ValueError as error:
    assert str(error).startswith("Unknown exact identifier:")
else:
    raise AssertionError("CASE_VARIANT_ACCEPTED")
assert queries==old["readerChecks"]["successfulWorkflowInvocations"]==24
assert len(checks)==old["readerChecks"]["repeatOrderChecks"]==12
for version in (19,20):
    card,axis=plan["expectedEvidenceAdditions"][str(version)]
    assert card in versions[version]["axisEvidenceIndex"][axis]
    assert card not in versions[version-1]["axisEvidenceIndex"][axis]

result={"schema":"BKL046_VERSION_BACKEND_FIXED_READER_VM_REPLAY_V1","protocolSha256":digest(raw),
        "programSha256":digest(Path(__file__).read_bytes()),"historicalProtocolSha256":p["historicalProtocolSha256"],
        "readerSha256":plan["readerSha256"],"knowledgePins":plan["knowledgePins"],"auditedVersions":len(versions),
        "comparisons":comparisons,"queries":queries,"repeatOrderChecks":len(checks),"invalidCaseVariantRejected":True,
        "queryFingerprints":[{"version":v,"request":ident,"sha256":pin} for (v,ident),pin in sorted(checks.items())],
        "providerCalls":0,"modelTrials":0,"nativeExecutions":0,"scientificClosures":0}
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(result,sort_keys=True,indent=2)+"\n")
print(json.dumps({"comparisons":comparisons,"queries":queries}))
