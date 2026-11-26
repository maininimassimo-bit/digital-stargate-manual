"""Compute exact fixed-sample thresholds and operating characteristics for the IA plan."""
from fractions import Fraction
from hashlib import sha256
from math import comb
import json
from pathlib import Path
import sys

protocol, lineage, native, out=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)


def checked(path, expected):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=expected:
        raise ValueError("Changed evidence input")
    return json.loads(data)


guard=checked(lineage,p["lineageGuard"])
known=checked(native,p["nativeFixture"])
if guard["independentConfirmationUnits"] or known["independentConfirmationUnits"]:
    raise ValueError("Historical inputs changed eligibility")


def cdf(n,k,p):
    if k>=n:
        return Fraction(1)
    if k<0:
        return Fraction(0)
    a,b=p.numerator,p.denominator
    q=b-a
    weighted=sum(comb(n,j)*a**j*q**(k-j) for j in range(k+1))
    return Fraction(weighted*q**(n-k),b**n)


def minimum_n(k,limit,alpha):
    low,high=k+1,2*(k+1)
    while cdf(high,k,limit)>alpha:
        high*=2
    while low<high:
        m=(low+high)//2
        if cdf(m,k,limit)<=alpha:
            high=m
        else:
            low=m+1
    if not cdf(low,k,limit)<=alpha<cdf(low-1,k,limit):
        raise ValueError("Missing exact minimality certificate")
    return low


if cdf(4,1,Fraction(1,2))!=Fraction(5,16):
    raise ValueError("Small exact CDF fixture")
limit,alpha=Fraction(p["pLimit"]),Fraction(p["alpha"])
alternatives=[Fraction(x) for x in p["alternatives"]]
tables=[]
for families in p["families"]:
    budget=alpha/families
    rows=[]
    for k in p["errorCaps"]:
        n=minimum_n(k,limit,budget)
        rows.append(dict(maxEvents=k,independentUnitsPerEndpoint=n,
                         tailAtLimit=float(cdf(n,k,limit)),tailOneFewer=float(cdf(n-1,k,limit)),
                         powerAtAlternatives=[float(cdf(n,k,q)) for q in alternatives]))
    tables.append(dict(simultaneousEndpoints=families,allocatedAlpha=str(budget),fixedCaps=rows))
if [row["independentUnitsPerEndpoint"] for row in tables[-1]["fixedCaps"]]!=p["historicalQuotas"]:
    raise ValueError("Historical quotas not reproduced")
if tables[0]["fixedCaps"][0]["independentUnitsPerEndpoint"]!=299:
    raise ValueError("Zero-event known threshold changed")

# A separate planning calculation finds the smallest fixed sample for each illustrated power target.
power_goal=Fraction(p["powerTarget"])
bench={}
for q in alternatives:
    for k in range(p["searchCap"]+1):
        n=minimum_n(k,limit,alpha/p["families"][-1])
        achieved=cdf(n,k,q)
        if achieved>=power_goal:
            bench[str(q)]=dict(units=n,maxEvents=k,power=float(achieved))
            break
    else:
        bench[str(q)]=dict(status="OUTSIDE_PREDECLARED_SEARCH",maxEventsSearched=p["searchCap"])

counts=known["ticketAccounting"]
report=dict(schema=p["schema"],protocolSha256=sha256(raw).hexdigest(),pLimit=str(limit),
            familywiseAlpha=str(alpha),alternatives=[str(q) for q in alternatives],tables=tables,
            minimumFixedDesignAtPowerTargetByAlternative=bench,
            historicalQuotasArithmeticallyReproduced=True,
            verifiedIndependentUnits=0,actualRiskEstimate=None,ownerPlanAmendmentApproved=False,
            omittedByScoredOnlyFixture=known["assignedIncludingTerminalFixtures"]-counts["assignedValidFixtures"],
            omittedUnsafeByCompleteOnlyFixture=counts["unsafeAndUnresolved"],
            nativeExecutions=0,providerCalls=0,scientificClosures=0)
with out.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
