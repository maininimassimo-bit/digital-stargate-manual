"""Test the distinction between calculable evidence and exposed scope labels in Native64."""
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

protocol, pool, previous, out = map(Path,sys.argv[1:])
raw=protocol.read_bytes()
cfg=json.loads(raw)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def checked(path,pin):
    data=path.read_bytes()
    require(sha256(data).hexdigest()==pin,"Changed source")
    return json.loads(data)


cases=checked(pool,cfg["requests"])
legacy=checked(previous,cfg["jointReceipt"])
require(len(cases)==legacy["packets"]==64 and legacy["independentConfirmationUnits"]==0,"Changed corpus")
distribution=Counter()
score={key:Counter() for key in ("alwaysNo","countsOnlyWithAbstention","literalMetadataReader")}
counterfactual_changes=0
all_agree=Counter()


def labels(request):
    counters=request["counts"]
    require(all(type(number) is int and number>=0 for number in counters.values()),"Counter type")
    require(all(sum(endpoint["counts"][key] for endpoint in request["endpoints"])==count
                for key,count in counters.items()),"Numerical evidence differs")
    numerical=(counters["relativeBeyondOwner5"]==0,
               counters["unsupported"]==0 and counters["supportMismatches"]==0)
    flags=request["runScope"]
    literal=(flags["populationVarianceValidated"],flags["scientificAdmission"])
    require(all(type(flag) is bool for flag in literal),"Missing scope flags")
    return numerical, literal


def add(acc, observation, truth):
    acc["assignedClaims"]+=len(truth)
    acc["answeredClaims"]+=sum(x is not None for x in observation)
    acc["correctClaims"]+=sum(a==b and a is not None for a,b in zip(observation,truth,strict=True))
    acc["abstainedClaims"]+=sum(a is None for a in observation)
    acc["falsePositiveClaims"]+=sum(a is True and not b for a,b in zip(observation,truth,strict=True))
    acc["falseNegativeClaims"]+=sum(a is False and b for a,b in zip(observation,truth,strict=True))
    acc["completeCorrectTickets"]+=int(observation==truth)
    acc["ticketsWithAbstention"]+=int(any(x is None for x in observation))


for req in cases.values():
    require(len(req["claims"])==len(set(req["claims"]))==4,"Claim identities differ")
    numerical,literal=labels(req)
    truth=numerical+literal
    distribution[sum(truth)]+=1
    add(score["alwaysNo"],(False,)*4,truth)
    add(score["countsOnlyWithAbstention"],numerical+(None,None),truth)
    add(score["literalMetadataReader"],truth,truth)

    # This sensitivity check changes metadata only. These are not possible or attested workflow outcomes.
    versions=[]
    for pop,workflow in product((False,True),repeat=2):
        clone=dict(req,runScope=dict(req["runScope"],populationVarianceValidated=pop,
                                     scientificAdmission=workflow))
        computed,declared=labels(clone)
        require(computed==numerical,"Scope-only edit changed numeric evidence")
        versions.append(computed+declared)
        counterfactual_changes+=sum(a!=b for a,b in zip(computed+declared,truth,strict=True))
    for i,claim in enumerate(req["claims"]):
        all_agree[claim]+=int(len({v[i] for v in versions})==1)

require(dict(distribution)=={int(k):v for k,v in legacy["supportedClaimsPerPacket"].items()},
        "Fixture label mix changed")
require(score["alwaysNo"]["falseNegativeClaims"]==sum(n*k for k,n in distribution.items()),
        "Always-No consistency")
require(sorted(all_agree.values())==[0,0,64,64],"Ablation failed")
require(score["countsOnlyWithAbstention"]["correctClaims"]==128 and
        score["literalMetadataReader"]["correctClaims"]==256,"Unexpected baseline")

report=dict(schema=cfg["schema"],protocolSha256=sha256(raw).hexdigest(),knownTickets=len(cases),
            scoreByDeterministicRule={label:dict(result) for label,result in score.items()},
            invariantToScopeFlagChangesByClaim=dict(all_agree),scopeFlagsDirectlyEncodeClaims=128,
            syntheticMetadataChangeChecks=counterfactual_changes,independentConfirmationUnits=0,
            providerCalls=0,nativeExecutions=0,scientificClosures=0)
with out.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
