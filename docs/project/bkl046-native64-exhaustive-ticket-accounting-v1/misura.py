"""Exhaustively verify joint error and abstention accounting against Native64 fixtures."""
import ast
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

protocol, ancestral, projected, out=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
cfg=json.loads(raw)


def exact(path,pin):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=pin:
        raise ValueError("Changed input "+path.name)
    return data


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


code=ancestral/"verifica.py"
tree=ast.parse(exact(code,cfg["adjudicator"]))
names={"hash_bytes","no_duplicates","json_bytes","ticket","adjudicate"}
defs=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names]
require({f.name for f in defs}==names,"Changed adjudication surface")
ns=dict(sha256=sha256,json=json)
exec(compile(ast.Module(body=defs,type_ignores=[]),str(code),"exec"),ns)
prior=json.loads(exact(ancestral/"tutti-gli-esiti.json",cfg["prior"]))
requests=json.loads(exact(projected/"richieste.json",cfg["requests"]))
links=json.loads(exact(projected/"legami-privati.json",cfg["links"]))
archived={row["caseId"]:row["verdicts"] for row in prior["developmentCases"]}
require(len(requests)==len(links)==len(archived)==64 and set(requests)==set(links),"Changed cohort")
totals, action_counts, terminals=Counter(),Counter(),Counter()
supports=Counter()
decisions=("YES","NO","ABSTAIN")
for uid, request in requests.items():
    link=links[uid]
    key=link["caseId"]
    claims=tuple(request["claims"])
    require(ns["hash_bytes"](ns["json_bytes"](request))==link["requestSha256"],"Projection digest")
    require(len(claims)==len(set(claims))==4,"Claim count")
    ns["claims"]=claims
    count=request["counts"]
    scope=request["runScope"]
    values=(count["relativeBeyondOwner5"]==0, count["unsupported"]==0 and count["supportMismatches"]==0,
            scope["populationVarianceValidated"],scope["scientificAdmission"])
    require(all(type(v) is bool for v in values),"Unclassified truth")
    truth=dict(zip(claims,values,strict=True))
    seen=archived[key]
    require([claim for claim in claims if not truth[claim]]==seen["allYes"]["falseAffirmations"]
            and [claim for claim in claims if truth[claim]]==seen["allNo"]["falseDenials"],"Oracle differs")
    supports[sum(values)]+=1
    ticket=ns["ticket"](key,link["packetSha256"])
    identity=ticket["ticketSha256"]
    for combination in product(decisions,repeat=4):
        choices=dict(zip(claims,combination,strict=True))
        body=ns["json_bytes"](dict(ticketSha256=identity,packetSha256=link["packetSha256"],claims=choices))
        result=ns["adjudicate"](ticket,body,truth,set())
        fa=[claim for claim,decision in choices.items() if decision=="YES" and not truth[claim]]
        fn=[claim for claim,decision in choices.items() if decision=="NO" and truth[claim]]
        abstain=[claim for claim,decision in choices.items() if decision=="ABSTAIN"]
        require(result["state"]=="SCORED" and (result["falseAffirmations"],result["falseDenials"],
                                              result["abstainedClaims"])==(fa,fn,abstain),"Oracle mismatch")
        require((result["unsafe"],result["unresolved"])==(bool(fa),bool(abstain)),"Broken flags")
        label="+".join(tag for tag,selected in (("unsafe",fa),("falseDenial",fn),("abstention",abstain)) if selected)
        totals[label or "correctComplete"]+=1
        action_counts["assignedValidFixtures"]+=1
        action_counts["withAtLeastOneYes"]+=int("YES" in combination)
        action_counts["unsafeFixtures"]+=int(bool(fa))
        action_counts["unsafeAndUnresolved"]+=int(bool(fa) and bool(abstain))
        action_counts["unresolvedFixtures"]+=int(bool(abstain))
        action_counts["completeFixtures"]+=int(not abstain)
        action_counts["unsafeAmongComplete"]+=int(bool(fa) and not abstain)
        action_counts["noAffirmativeButIncorrect"]+=int("YES" not in combination and bool(fn))
    for label, answer in (("missing",None),("invalid",b"{}")):
        used=set()
        terminal=ns["adjudicate"](ticket,answer,truth,used)
        require(terminal["unresolved"] and terminal["state"]==seen[
            "missingResponse" if label=="missing" else "missingClaim"]["state"],"Terminal mismatch")
        require(ns["adjudicate"](ticket,answer,truth,used)["state"]=="REPLAY_REJECTED","Terminal ticket reused")
        terminals[label]+=1

total=64*3**4
require(sum(totals.values())==total and action_counts["assignedValidFixtures"]==total
        and totals["correctComplete"]==64,"Incomplete enumeration")
require(action_counts["unsafeFixtures"]==action_counts["unsafeAmongComplete"]+action_counts["unsafeAndUnresolved"],
        "Unsafe false affirmations lost during accounting")
report=dict(schema=cfg["schema"],protocolSha256=sha256(raw).hexdigest(),
            packets=64,decisionVectors=total,jointOutcomes=dict(totals),
            ticketAccounting=dict(action_counts),terminalFixtures=dict(terminals),
            assignedIncludingTerminalFixtures=total+sum(terminals.values()),
            unresolvedIncludingTerminalFixtures=action_counts["unresolvedFixtures"]+sum(terminals.values()),
            supportedClaimsPerPacket=dict(supports),independentConfirmationUnits=0,
            providerCalls=0,scientificClosures=0,nativeExecutions=0)
with out.open("x",encoding="utf-8",newline="\n") as f:
    json.dump(report,f,sort_keys=True,indent=2,allow_nan=False)
    f.write("\n")
