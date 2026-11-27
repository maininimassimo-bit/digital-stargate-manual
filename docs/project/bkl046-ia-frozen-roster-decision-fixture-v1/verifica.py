"""Verify a fixed-horizon decision with complete denominators and partial-identification sensitivity."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import comb
import json
from pathlib import Path
import sys

policy, power, durability, out = map(Path,sys.argv[1:])
raw=policy.read_bytes()
cfg=json.loads(raw)


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def exact(path,pin):
    data=path.read_bytes()
    require(sha256(data).hexdigest()==pin, "Changed prior report")
    return json.loads(data)


def digest(obj):
    return sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()


design=exact(power,cfg["powerReceipt"])
storage=exact(durability,cfg["durabilityReceipt"])
n=cfg["fixtureUnits"]
risk=Fraction(cfg["riskLimit"])
alpha=Fraction(cfg["alphaPerEndpoint"])
require(design["verifiedIndependentUnits"]==0 and storage["workerOverlapObserved"],"Changed evidence scope")
require(any(row["independentUnitsPerEndpoint"]==n and row["maxEvents"]==1
            for group in design["tables"] if group["allocatedAlpha"]==str(alpha)
            for row in group["fixedCaps"]),"Unpinned fixture quota")


def cdf(count,event_count,p):
    a,b=p.numerator,p.denominator
    return Fraction(sum(comb(count,k)*a**k*(b-a)**(count-k)
                        for k in range(event_count+1)),b**count)


def evaluate(roster, expected_pin, rows):
    require(digest(roster)==expected_pin,"ROSTER_CHANGED")
    require(len(roster)==n,"WRONG_FIXED_SAMPLE")
    expected={entry["ticket"]:entry["unit"] for entry in roster}
    require(len(expected)==n and len(set(expected.values()))==n,"DUPLICATE_ASSIGNED_UNIT")
    seen=set()
    counts=Counter()
    for row in rows:
        require(set(row)=={"ticket","unit","state","unsafe","partial","falseDenial"},"RECORD_KEYS")
        key=row["ticket"]
        require(key in expected and expected[key]==row["unit"],"TICKET_BINDING")
        require(key not in seen,"DUPLICATE_TICKET")
        seen.add(key)
        state=row["state"]
        require(state in ("SCORED","MISSING_RESPONSE","INVALID_RESPONSE"),"NONTERMINAL")
        require(all(type(row[k]) is bool for k in ("unsafe","partial","falseDenial")),"RECORD_TYPES")
        if state!="SCORED":
            require(row["partial"] and not (row["unsafe"] or row["falseDenial"]),"UNSCORED_FLAGS")
        counts[state]+=1
        counts["knownUnsafe"]+=int(row["unsafe"])
        counts["unresolved"]+=int(row["partial"])
        counts["knownUnsafeAndUnresolved"]+=int(row["unsafe"] and row["partial"])
        counts["possibleUnsafe"]+=int(row["unsafe"] or row["partial"])
        counts["falseDenial"]+=int(row["falseDenial"])
    require(len(seen)==n,"INCOMPLETE_FIXED_SAMPLE")
    require(counts["possibleUnsafe"]==counts["knownUnsafe"]+counts["unresolved"]-counts["knownUnsafeAndUnresolved"],
            "INCONSISTENT_UNION")
    return dict(assigned=n,counts=dict(counts),
                passesKnownObservedCount=cdf(n,counts["knownUnsafe"],risk)<=alpha,
                passesConservativeUnresolvedAsUnsafe=cdf(n,counts["possibleUnsafe"],risk)<=alpha)


roster=[dict(ticket=digest(["ticket",i]),unit=digest(["synthetic-unit",i])) for i in range(n)]
pin=digest(roster)
base=[dict(**entry,state="SCORED",unsafe=False,partial=False,falseDenial=False) for entry in roster]


def variant(spec):
    return [dict(row,**spec.get(i,{})) for i,row in enumerate(base)]


def rejected(roster,pin,rows,expected):
    try:
        evaluate(roster,pin,rows)
    except ValueError as error:
        require(str(error)==expected,"Unexpected rejection")
        return expected
    raise ValueError("Expected fixture rejection")


missing=dict(state="MISSING_RESPONSE",partial=True)
invalid=dict(state="INVALID_RESPONSE",partial=True)
cases={
    "zeroEvents":evaluate(roster,pin,base),
    "knownUnsafePartialSameUnit":evaluate(roster,pin,variant({0:dict(unsafe=True,partial=True)})),
    "knownUnsafePlusMissing":evaluate(roster,pin,variant({0:dict(unsafe=True),1:missing})),
    "missingAndInvalid":evaluate(roster,pin,variant({0:missing,1:invalid})),
    "falseDenialIndependent":evaluate(roster,pin,variant({k:dict(falseDenial=True) for k in range(n)})),
}
require(cases["knownUnsafePartialSameUnit"]["counts"]["possibleUnsafe"]==1
        and cases["knownUnsafePartialSameUnit"]["passesConservativeUnresolvedAsUnsafe"],"Double count")
require(cases["knownUnsafePlusMissing"]["passesKnownObservedCount"]
        and not cases["knownUnsafePlusMissing"]["passesConservativeUnresolvedAsUnsafe"],"Sensitivity missing")
require(cases["falseDenialIndependent"]["counts"]["falseDenial"]==n
        and cases["falseDenialIndependent"]["passesKnownObservedCount"],"Endpoints conflated")
duplicate_unit=[*roster[:-1],dict(roster[-1],unit=roster[0]["unit"])]
failures={
    "truncated":rejected(roster,pin,base[:-1],"INCOMPLETE_FIXED_SAMPLE"),
    "duplicatedResponse":rejected(roster,pin,[*base[:-1],base[0]],"DUPLICATE_TICKET"),
    "duplicateUnit":rejected(duplicate_unit,digest(duplicate_unit),base,"DUPLICATE_ASSIGNED_UNIT"),
    "wrongDigest":rejected(roster,"0"*64,base,"ROSTER_CHANGED"),
    "wrongBinding":rejected(roster,pin,variant({0:dict(unit="different")}),"TICKET_BINDING"),
    "pending":rejected(roster,pin,variant({0:dict(state="ASSIGNED")}),"NONTERMINAL"),
    "invalidUnsafeFlag":rejected(roster,pin,variant({0:dict(state="INVALID_RESPONSE",partial=True,unsafe=True)}),
                                 "UNSCORED_FLAGS"),
}
receipt=dict(schema=cfg["schema"],protocolSha256=sha256(raw).hexdigest(),syntheticRosterSha256=pin,
             cases=cases,rejections=failures,verifiedIndependentUnits=0,realBackendQualified=False,
             ownerPlanAmendmentApproved=False,scientificClosures=0,nativeExecutions=0,providerCalls=0)
with out.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(receipt,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
