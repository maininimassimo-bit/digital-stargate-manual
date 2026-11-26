"""Check an evidence-only request format using a balanced development fixture."""
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
import sys

protocol, ablation, quota, out=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
cfg=json.loads(raw)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def checked(path,pin):
    data=path.read_bytes()
    require(sha256(data).hexdigest()==pin,"Changed prior report")
    return json.loads(data)


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


def digest(obj):
    return sha256(canonical(obj)).hexdigest()


a=checked(ablation,cfg["priorAblation"])
q=checked(quota,cfg["fixedRoster"])
require(a["scopeFlagsDirectlyEncodeClaims"]==128 and q["verifiedIndependentUnits"]==0,"Changed predecessor")

claims=("numericalTolerance","fullSupport","fixedRosterComplete","fullReceiptChain")
statuses=("scored","missing","invalid")
expected_keys={"ticket","endpoints","assignedUnits","records","receipts"}
case_ids=("reference","alternate")


def adjudicate(req):
    require(set(req)==expected_keys,"REQUEST_SCHEMA")
    assigned=req["assignedUnits"]
    require(type(assigned) is list and all(type(u) is str and u for u in assigned)
            and len(assigned)==len(set(assigned)) and assigned,"UNIT_SCHEMA")
    rows=req["records"]
    require(all(set(r)=={"unit","state"} and r["state"] in statuses for r in rows),"RECORD_SCHEMA")
    units=[row["unit"] for row in rows]
    require(len(set(units))==len(units) and set(units).issubset(assigned),"RECORD_BINDING")
    require(len(req["endpoints"])==2,"ENDPOINT_COUNT")
    for endpoint in req["endpoints"]:
        require(set(endpoint)=={"deltaMicro","baseMicro","expected","supported"}
                and all(type(v) is int for v in endpoint.values()),"ENDPOINT_SCHEMA")
        require(endpoint["baseMicro"]>0 and 0<=endpoint["supported"]<=endpoint["expected"],
                "ENDPOINT_RANGE")
    receipts=req["receipts"]
    require(set(receipts)=={"subject","review","quality","release"},"RECEIPT_SCHEMA")
    subject=receipts["subject"]
    review=receipts["review"]
    quality=receipts["quality"]
    release=receipts["release"]
    require(set(review)=={"id","subject"} and set(quality)=={"approvedReview","subject"},
            "REVIEW_SCHEMA")
    require(release is None or set(release)=={"subject","reservation","terminalCode"},"RELEASE_SCHEMA")
    return (
        all(100*abs(r["deltaMicro"])<=5*r["baseMicro"] for r in req["endpoints"]),
        all(r["supported"]==r["expected"] for r in req["endpoints"]),
        set(units)==set(assigned),
        review["subject"]==quality["subject"]==subject
        and quality["approvedReview"]==review["id"] and release is not None
        and release["subject"]==subject and release["terminalCode"]==0
    )


def fixture(ticket, expected, style):
    within,support,terminal,chain=expected
    variant=case_ids.index(style)
    base=2000+1000*variant
    limit=(base*5)//100
    delta=(-1 if variant else 1)*(limit+int(not within))
    assigned=["A","B","C"]
    rows=[dict(unit="A",state="scored"),dict(unit="B",state="missing")]
    if terminal:
        rows.append(dict(unit="C",state="invalid" if variant else "scored"))
    prerequisite={"id":"review-01","subject":"fixture-image"}
    quality={"approvedReview":"review-01" if chain or variant else "other-review","subject":"fixture-image"}
    release=None if (not chain and variant) else dict(subject="fixture-image",reservation="R-local",terminalCode=0)
    return dict(ticket=ticket,endpoints=[
                    dict(deltaMicro=delta,baseMicro=base,expected=64,supported=64-int(not support)),
                    dict(deltaMicro=0,baseMicro=base,expected=64,supported=64)],
                assignedUnits=assigned,records=rows,receipts=dict(subject="fixture-image",
                    review=prerequisite,quality=quality,release=release))


schedule=list(product(product((False,True),repeat=4),case_ids))
random.Random(cfg["seed"]).shuffle(schedule)
request_set={}
oracle={}
baseline=Counter()
labels=Counter()
pairs=Counter()
for index,(expected,style) in enumerate(schedule):
    ticket=f"T{index+1:03d}"
    req=fixture(ticket,expected,style)
    inferred=adjudicate(req)
    require(inferred==expected,"Derived factors differ from fixture oracle")
    request_set[ticket]=req
    oracle[ticket]=dict(requestSha256=digest(req),answers=dict(zip(claims,expected,strict=True)))
    pairs["".join(str(int(b)) for b in expected)]+=1
    for claim,yes in zip(claims,expected,strict=True):
        labels[claim]+=int(yes)
        baseline["alwaysNoCorrectClaims"]+=int(not yes)
        baseline["computedCorrectClaims"]+=1
    baseline["alwaysNoCorrectTickets"]+=int(not any(expected))
    baseline["computedCorrectTickets"]+=1

probe=next(iter(request_set.values()))
variants=(
    (dict(probe,runScope={"scientificAdmission":True}),"REQUEST_SCHEMA"),
    (dict(probe,endpoints=[dict(probe["endpoints"][0],verdict=True),probe["endpoints"][1]]),"ENDPOINT_SCHEMA"),
    (dict(probe,records=[*probe["records"],probe["records"][0]]),"RECORD_BINDING"),
)
for variant,code in variants:
    try:
        adjudicate(variant)
    except ValueError as error:
        require(str(error)==code,"Unexpected rejection")
    else:
        raise ValueError("Invalid evidence accepted")

require(len(pairs)==16 and set(pairs.values())=={2} and set(labels.values())=={16},"Unbalanced factorial")
report=dict(schema=cfg["schema"],protocolSha256=sha256(raw).hexdigest(),fixtureTickets=len(request_set),
            fixtureClaims=len(request_set)*len(claims),positiveLabelsPerClaim=dict(labels),jointLabelPatterns=len(pairs),
            aggregateScores=dict(baseline),requestSetSha256=digest(request_set),separateOracleSha256=digest(oracle),
            rejectedNegativeFixtures=len(variants),independentConfirmationUnits=0,
            actualOracleAccessIsolationVerified=False,providerCalls=0,nativeExecutions=0,scientificClosures=0)
out.mkdir()
for name,value in (("riscontro.json",report),("richieste-fixture.json",request_set),("oracolo-fixture.json",oracle)):
    with (out/name).open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(value,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")
