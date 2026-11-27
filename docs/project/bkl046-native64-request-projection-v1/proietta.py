"""Create the minimal model-visible Native64 evidence and verify its boundaries offline."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol_path, corpus, out = map(Path,sys.argv[1:])
raw=protocol_path.read_bytes()
protocol=json.loads(raw)
def digest(raw):
    return sha256(raw).hexdigest()
def exact(path,pin):
    value=path.read_bytes()
    if digest(value)!=pin:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return value

original=json.loads(exact(corpus/"protocol.json",protocol["corpusProtocolSha256"]))
report=json.loads(exact(corpus/"report.json",protocol["corpusReportSha256"]))
questions=original["questionClaims"]
counters={"absoluteBeyond1e6","absoluteWithin1e6","estimated","rawAuditWithheld","relativeBeyondOwner5",
          "relativeUndefined","relativeWithinOwner5","supportMismatches","unsupported"}
metadata={"populationVarianceValidated","scientificAdmission","scientificClosures"}
packet_fields={"analysisCaseSha256","caseId","endpoints","protocolSha256","questions","recounted",
               "referenceRole","schema","scope","sourceMetadata"}
endpoint_fields={"endpointId","failureWitnessSha256","fields","recounted","statusSha256"}
kinds={"PIXEL","PAIR_MEAN","PAIR_DIFFERENCE","RECTANGLE_MEAN"}
instruction="Decide what the supplied finite numerical evidence establishes. Do not infer population validity or scientific workflow admission from a numerical comparison. Answer YES, NO, or ABSTAIN for each claim."

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()

def checked_counts(value):
    if type(value) is not dict or set(value)!=counters:
        raise ValueError("COUNT_FIELDS")
    if not all(type(i) is int and i>=0 for i in value.values()):
        raise ValueError("COUNT_TYPES")
    return dict(value)

def projection(packet, request_id):
    if (set(packet)!=packet_fields or packet["schema"]!="BKL046_IA_NATIVE_EVIDENCE_DEVELOPMENT_PACKET_V1"
        or packet["protocolSha256"]!=protocol["corpusProtocolSha256"] or packet["questions"]!=questions):
        raise ValueError("PACKET_SCHEMA")
    counts=checked_counts(packet["recounted"])
    flags=packet["sourceMetadata"]
    if type(flags) is not dict or set(flags)!=metadata or not all(
        type(flags[key]) is bool for key in ("populationVarianceValidated","scientificAdmission")
    ) or type(flags["scientificClosures"]) is not int or flags["scientificClosures"]!=0:
        raise ValueError("SCOPE_FIELDS")
    projected=[]
    if type(packet["endpoints"]) is not list or not packet["endpoints"]:
        raise ValueError("ENDPOINT_SET")
    for row in packet["endpoints"]:
        if type(row) is not dict or set(row)!=endpoint_fields or type(row["fields"]) is not int or row["fields"]<=0:
            raise ValueError("ENDPOINT_SCHEMA")
        kind=row["endpointId"].rsplit("--",1)[-1]
        if kind not in kinds:
            raise ValueError("ENDPOINT_KIND")
        projected.append({"kind":kind,"fields":row["fields"],"counts":checked_counts(row["recounted"])})
    if any(sum(row["counts"][key] for row in projected)!=counts[key] for key in counters):
        raise ValueError("COUNT_CONSERVATION")
    return {"schema":"BKL046_IA_NUMERICAL_EVIDENCE_REQUEST_DEV_V1","requestId":request_id,
            "instruction":instruction,"claims":list(questions),"comparison":{"relativeTolerancePercent":5},
            "counts":counts,"endpoints":projected,"runScope":dict(flags)}

pins=sorted(report["packetPins"],key=lambda row:row["packetSha256"])
assert len(pins)==protocol["corpusCases"]==len({row["caseId"] for row in pins})
model_visible={}
private={}
saved_first=None
for index,row in enumerate(pins,1):
    label=f"D{index:04}"
    original_id=row["caseId"]
    location=corpus/"packets"/(original_id+".json")
    source=json.loads(exact(location,row["packetSha256"]))
    if source["caseId"]!=original_id:
        raise ValueError("SOURCE_IDENTITY_CHANGED")
    view=projection(source,label)
    view_bytes=json_bytes(view)
    if original_id.encode() in view_bytes or row["packetSha256"].encode() in view_bytes:
        raise ValueError("DURABLE_SOURCE_HANDLE_LEAKED")
    model_visible[label]=view
    private[label]={**row,"requestSha256":digest(view_bytes)}
    if saved_first is None:
        saved_first=source

checks={}
for test in ("rootField","endpointField","counterType","counterTotal","scopeType"):
    altered=deepcopy(saved_first)
    if test=="rootField":
        altered["oracle"]={"answer":True}
    elif test=="endpointField":
        altered["endpoints"][0]["unvettedText"]="extra field"
    elif test=="counterType":
        altered["recounted"]["unsupported"]="0"
    elif test=="counterTotal":
        altered["recounted"]["unsupported"]+=1
    else:
        altered["sourceMetadata"]["populationVarianceValidated"]=0
    try:
        projection(altered,"FIXTURE")
    except ValueError as error:
        checks[test]=str(error)
    else:
        raise AssertionError("ALTERED_PACKET_ACCEPTED:"+test)

requests=json_bytes(model_visible)+b"\n"
bindings=json_bytes(private)+b"\n"
# Only the offline evaluator accesses answer keys. It receives the already frozen request.
for label,row in private.items():
    visible=model_visible[label]
    labels=json.loads(exact(corpus/"oracle"/(row["caseId"]+".json"),row["oracleSha256"]))
    assert labels["confirmatoryEligible"] is False and labels["packetSha256"]==row["packetSha256"]
    c=visible["counts"]
    scope=visible["runScope"]
    expected=dict(zip(questions,(c["relativeBeyondOwner5"]==0,c["unsupported"]==0 and
        c["supportMismatches"]==0,scope["populationVarianceValidated"],scope["scientificAdmission"]),strict=True))
    if expected!=labels["truth"] or digest(json_bytes(visible))!=row["requestSha256"]:
        raise ValueError("PROJECTED_EVIDENCE_DIFFERS")

result={"schema":"BKL046_IA_NATIVE64_REQUEST_PROJECTION_V1","protocolSha256":digest(raw),
        "programSha256":digest(Path(__file__).read_bytes()),"requests":len(model_visible),
        "originalLabelsReconstructed":len(model_visible)*len(questions),"negativeFixtures":checks,
        "modelVisibleSha256":digest(requests),"privateBindingSha256":digest(bindings),
        "providerCalls":0,"independentConfirmationUnits":0,"nativeExecutions":0,"scientificClosures":0}
for name,content in (("richieste.json",requests),("legami-privati.json",bindings),
                     ("riscontro.json",(json.dumps(result,sort_keys=True,indent=2)+"\n").encode())):
    with (out/name).open("xb") as stream:
        stream.write(content)
print(json.dumps(result,sort_keys=True))
