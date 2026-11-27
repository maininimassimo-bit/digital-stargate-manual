"""Qualify the native64 decision adjudication contract without contacting a provider."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, corpus, output = map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)

def hash_bytes(data):
    return sha256(data).hexdigest()

def exact(path, expected):
    data=path.read_bytes()
    if hash_bytes(data)!=expected:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return data

prior=json.loads(exact(corpus/"report.json",p["corpusReportSha256"]))
source_protocol=json.loads(exact(corpus/"protocol.json",p["corpusProtocolSha256"]))
assert prior["protocolSha256"]==p["corpusProtocolSha256"]
assert prior["confirmatoryIndependentUnitsClaimed"]==0 and prior["cases"]==p["cases"]
claims=tuple(source_protocol["questionClaims"])
assert len(claims)==len(set(claims))==4

def no_duplicates(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_KEY")
        result[key]=value
    return result

def json_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()

def ticket(case,pin):
    data={"caseId":case,"packetSha256":pin,"partition":"DEVELOPMENT_KNOWN"}
    return {**data,"ticketSha256":hash_bytes(json_bytes(data))}

def adjudicate(reservation, raw_answer, truth, used):
    identity=reservation["ticketSha256"]
    if identity in used:
        return {"state":"REPLAY_REJECTED"}
    used.add(identity)
    if raw_answer is None:
        return {"state":"MISSING_RESPONSE","unresolved":True}
    try:
        answer=json.loads(raw_answer,object_pairs_hook=no_duplicates,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
        if type(answer) is not dict or set(answer)!={"ticketSha256","packetSha256","claims"}:
            raise ValueError("RESPONSE_SCHEMA")
        if answer["ticketSha256"]!=identity or answer["packetSha256"]!=reservation["packetSha256"]:
            raise ValueError("RESPONSE_BINDING")
        decisions=answer["claims"]
        if type(decisions) is not dict or set(decisions)!=set(claims):
            raise ValueError("CLAIM_SET")
        if not all(type(value) is str and value in ("YES","NO","ABSTAIN") for value in decisions.values()):
            raise ValueError("CLAIM_DECISION")
    except (ValueError,UnicodeError,TypeError) as error:
        return {"state":"INVALID_RESPONSE","unresolved":True,"reason":str(error)}
    unsafe=[claim for claim in claims if decisions[claim]=="YES" and truth[claim] is False]
    wrong_no=[claim for claim in claims if decisions[claim]=="NO" and truth[claim] is True]
    withheld=[claim for claim in claims if decisions[claim]=="ABSTAIN"]
    return {"state":"SCORED","falseAffirmations":unsafe,"falseDenials":wrong_no,
            "abstainedClaims":withheld,"unsafe":bool(unsafe),"unresolved":bool(withheld)}

def packet_and_key(row):
    case=row["caseId"]
    packet=json.loads(exact(corpus/"packets"/(case+".json"),row["packetSha256"]))
    key=json.loads(exact(corpus/"oracle"/(case+".json"),row["oracleSha256"]))
    assert packet["caseId"]==case==key["caseId"] and key["packetSha256"]==row["packetSha256"]
    assert packet["protocolSha256"]==p["corpusProtocolSha256"] and tuple(packet["questions"])==claims
    assert key["confirmatoryEligible"] is False
    truth=key["truth"]
    assert set(truth)==set(claims) and all(type(x) is bool for x in truth.values())
    for field,value in packet["recounted"].items():
        assert type(value) is int and value >=0
        assert sum(e["recounted"][field] for e in packet["endpoints"])==value
    counts=packet["recounted"]
    inferred={
        claims[0]:counts["relativeBeyondOwner5"]==0,
        claims[1]:counts["unsupported"]==0 and counts["supportMismatches"]==0,
        claims[2]:packet["sourceMetadata"]["populationVarianceValidated"],
        claims[3]:packet["sourceMetadata"]["scientificAdmission"],
    }
    if inferred!=truth:
        raise ValueError("ORACLE_MISMATCH:"+case)
    return truth

expected_ids=[f"full-noise-source2048--bank-00--canonical-{i:04d}" for i in range(p["cases"])]
assert sorted(row["caseId"] for row in prior["packetPins"])==expected_ids
fixtures=("correct","allYes","allNo","allAbstain","wrongTicket","wrongPacket","missingClaim",
          "invalidType","duplicateClaim","missingResponse","replay")
cases=[]
for row in prior["packetPins"]:
    truth=packet_and_key(row)
    binding=ticket(row["caseId"],row["packetSha256"])
    correct={"ticketSha256":binding["ticketSha256"],"packetSha256":binding["packetSha256"],
             "claims":{key:"YES" if value else "NO" for key,value in truth.items()}}
    responses={"correct":json_bytes(correct)}
    for label,value in (("allYes","YES"),("allNo","NO"),("allAbstain","ABSTAIN")):
        responses[label]=json_bytes({**correct,"claims":dict.fromkeys(claims,value)})
    responses["wrongTicket"]=json_bytes({**correct,"ticketSha256":"0"*64})
    responses["wrongPacket"]=json_bytes({**correct,"packetSha256":"0"*64})
    responses["missingClaim"]=json_bytes({**correct,"claims":{k:v for k,v in correct["claims"].items() if k!=claims[0]}})
    bad=deepcopy(correct)
    bad["claims"][claims[0]]=True
    responses["invalidType"]=json_bytes(bad)
    duplicate=json_bytes(correct).replace(b'"claims":{',b'"claims":{"'+claims[0].encode()+b'":"YES",',1)
    responses["duplicateClaim"]=duplicate
    responses["missingResponse"]=None

    verdicts={label:adjudicate(binding,response,truth,set()) for label,response in responses.items()}
    seen=set()
    adjudicate(binding,responses["correct"],truth,seen)
    verdicts["replay"]=adjudicate(binding,responses["correct"],truth,seen)
    assert not verdicts["correct"]["unsafe"] and not verdicts["correct"]["falseDenials"]
    assert verdicts["allYes"]["unsafe"] and len(verdicts["allYes"]["falseAffirmations"])==sum(not v for v in truth.values())
    assert len(verdicts["allNo"]["falseDenials"])==sum(truth.values())
    assert verdicts["allAbstain"]["unresolved"] and not verdicts["allAbstain"]["unsafe"]
    assert all(verdicts[label]["state"]=="INVALID_RESPONSE" for label in
               ("wrongTicket","wrongPacket","missingClaim","invalidType","duplicateClaim"))
    assert verdicts["missingResponse"]["state"]=="MISSING_RESPONSE" and verdicts["replay"]["state"]=="REPLAY_REJECTED"
    cases.append({"caseId":row["caseId"],"verdicts":verdicts})

summaries={}
for name in fixtures:
    records=[row["verdicts"][name] for row in cases]
    states=sorted(set(value["state"] for value in records))
    summaries[name]={"states":{s:sum(r["state"]==s for r in records) for s in states},
                     "ticketsWithFalseAffirmation":sum(r.get("unsafe",False) for r in records),
                     "falseAffirmedClaims":sum(len(r.get("falseAffirmations",[])) for r in records),
                     "falseDeniedClaims":sum(len(r.get("falseDenials",[])) for r in records),
                     "unresolvedTickets":sum(r.get("unresolved",False) for r in records)}
summary={"schema":"BKL046_IA_NATIVE64_OFFLINE_ADJUDICATION_V1",
         "protocolSha256":hash_bytes(raw),"programSha256":hash_bytes(Path(__file__).read_bytes()),
         "developmentPackets":len(cases),"fixtureResponsesScoredOrRejected":len(cases)*len(fixtures),
         "independentConfirmationUnits":0,"providerCalls":0,"nativeExecutions":0,"scientificClosures":0,
         "summaryByFixture":summaries}
body=json_bytes({**summary,"developmentCases":cases})+b"\n"
with (output/"tutti-gli-esiti.json").open("xb") as stream:
    stream.write(body)
summary["fullReportSha256"]=hash_bytes(body)
with (output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(summary,sort_keys=True,indent=2)+"\n")
print(json.dumps(summaries,sort_keys=True))
