"""Verify an offline commit-and-reveal transcript for low-entropy decision labels."""
from copy import deepcopy
from hashlib import sha256
from hmac import compare_digest
from itertools import product
import json
from pathlib import Path
from secrets import token_hex
import sys

protocol, source, out=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
cfg=json.loads(raw)


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def checked(path,pin):
    data=path.read_bytes()
    require(sha256(data).hexdigest()==pin,"Changed source")
    return json.loads(data)


def digest(obj):
    return sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()


requests=checked(source/"richieste-fixture.json",cfg["requests"])
oracle=checked(source/"oracolo-fixture.json",cfg["oracle"])
previous=checked(source/"riscontro.json",cfg["previous"])
require(len(oracle)==len(requests)==previous["fixtureTickets"]==32 and set(oracle)==set(requests),"Cohort")
require(digest(oracle)==previous["separateOracleSha256"] and digest(requests)==previous["requestSetSha256"],
        "Packet-set binding")
rules=sha256(raw).hexdigest()


def oracle_commit(ticket,request_hash,labels,nonce):
    return digest(["BKL046_ORACLE_COMMIT_V1",rules,ticket,request_hash,labels,nonce])


def seal(bank):
    public={}
    for ticket,value in bank.items():
        public[ticket]=dict(requestSha256=value["requestSha256"],
                            oracleDigest=oracle_commit(ticket,value["requestSha256"],value["answers"],value["nonce"]))
    return dict(protocol=rules,phase="ORACLE_COMMITTED",tickets=public)


def verify(committed,committed_pin,terminal,terminal_pin,openings):
    require(compare_digest(digest(committed),committed_pin),"ORACLE_ANCHOR")
    require(committed["phase"]=="ORACLE_COMMITTED" and committed["protocol"]==rules,"ORACLE_PHASE")
    require(compare_digest(digest(terminal),terminal_pin),"TERMINAL_ANCHOR")
    require(terminal["phase"]=="RESPONSES_SEALED" and terminal["protocol"]==rules,"TERMINAL_PHASE")
    require(terminal["oracleAnchor"]==committed_pin,"TRANSCRIPT_ORDER")
    tickets=committed["tickets"]
    require(set(tickets)==set(terminal["tickets"])==set(openings)==set(requests),"TRANSCRIPT_COVERAGE")
    seen=set()
    for ticket in sorted(tickets):
        capsule=tickets[ticket]
        end=terminal["tickets"][ticket]
        opened=openings[ticket]
        pin=digest(requests[ticket])
        require(capsule["requestSha256"]==end["requestSha256"]==opened["requestSha256"]==pin,
                "REQUEST_BINDING")
        require(set(opened["answers"])==set(oracle[ticket]["answers"])
                and all(type(x) is bool for x in opened["answers"].values()),"LABEL_SCHEMA")
        nonce=opened["nonce"]
        require(type(nonce) is str and len(bytes.fromhex(nonce))==32 and len(nonce)==64
                and nonce not in seen,"NONCE_POLICY")
        seen.add(nonce)
        digest_check=oracle_commit(ticket,pin,opened["answers"],nonce)
        require(compare_digest(capsule["oracleDigest"],digest_check),"ORACLE_OPENING")
        state=end["state"]
        require(state in ("scored","missing","invalid"),"NOT_TERMINAL")
        declared=end["responseSha256"]
        require((declared is None) if state=="missing" else
                (type(declared) is str and len(bytes.fromhex(declared))==32 and len(declared)==64),
                "RESPONSE_STATE_BINDING")
    return len(seen)


openings={ticket:dict(value,nonce=token_hex(32)) for ticket,value in oracle.items()}
committed=seal(openings)
oracle_pin=digest(committed)
guessed=0
for ticket,value in oracle.items():
    present=value["answers"]
    weak=digest(present)
    names=sorted(present)
    candidates=[dict(zip(names,decisions,strict=True)) for decisions in product((False,True),repeat=4)]
    require(sum(digest(c)==weak for c in candidates)==1,"Weak commitment control changed")
    guesses=[oracle_commit(ticket,value["requestSha256"],guess,"") for guess in candidates]
    guessed+=int(committed["tickets"][ticket]["oracleDigest"] in guesses)

terminal=dict(protocol=rules,phase="RESPONSES_SEALED",oracleAnchor=oracle_pin,tickets={})
for i,(ticket,value) in enumerate(sorted(oracle.items())):
    state="missing" if i==0 else ("invalid" if i==1 else "scored")
    payload=None if i==0 else ({"malformed":True} if i==1 else {"synthetic":ticket})
    terminal["tickets"][ticket]=dict(requestSha256=value["requestSha256"],state=state,
                                      responseSha256=None if i==0 else digest(payload))
terminal_pin=digest(terminal)
verified=verify(committed,oracle_pin,terminal,terminal_pin,openings)

first,second=sorted(openings)[:2]
mutations=[]


def fixture(label,c=committed,cp=oracle_pin,t=terminal,tp=terminal_pin,o=openings,why=None):
    try:
        verify(c,cp,t,tp,o)
    except ValueError as error:
        require(str(error)==why,"Wrong failure precedence")
        mutations.append(label)
    else:
        raise ValueError("Altered transcript accepted")


bad=deepcopy(openings)
claim=next(iter(bad[first]["answers"]))
bad[first]["answers"][claim]=not bad[first]["answers"][claim]
fixture("alteredLabels",o=bad,why="ORACLE_OPENING")
bad=deepcopy(openings)
bad[first]["requestSha256"]=openings[second]["requestSha256"]
fixture("transplantedOpening",o=bad,why="REQUEST_BINDING")
bad=deepcopy(terminal)
del bad["tickets"][first]
fixture("droppedTerminalEvenIfRepinned",t=bad,tp=digest(bad),why="TRANSCRIPT_COVERAGE")
bad=deepcopy(terminal)
bad["oracleAnchor"]="0"*64
fixture("differentOracleAnchor",t=bad,tp=digest(bad),why="TRANSCRIPT_ORDER")
bad=deepcopy(terminal)
bad["tickets"][second]["responseSha256"]="1"*64
fixture("terminalBytesChanged",t=bad,why="TERMINAL_ANCHOR")
bad=deepcopy(openings)
bad[second]["nonce"]=bad[first]["nonce"]
bad_public=seal(bad)
bad_pin=digest(bad_public)
linked=dict(terminal,oracleAnchor=bad_pin)
fixture("reusedNonceEvenIfRepinned",c=bad_public,cp=bad_pin,t=linked,tp=digest(linked),
        o=bad,why="NONCE_POLICY")

require(guessed==0 and verified==32 and len(mutations)==6,"Transcript fixture failed")
report=dict(schema=cfg["schema"],protocolSha256=rules,verifiedTickets=verified,
            deterministicWeakLabelDigestsRecovered=len(oracle),guessesPerTicket=16,
            noNonceGuessMatches=guessed,liveRandomNoncesUsed=True,nonceBits=256,
            terminalScored=30,terminalMissing=1,terminalInvalid=1,alteredFixturesRejected=mutations,
            independentAnchoringVerified=False,isolatedOracleCustodyVerified=False,
            independentConfirmationUnits=0,providerCalls=0,nativeExecutions=0,scientificClosures=0)
with out.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
