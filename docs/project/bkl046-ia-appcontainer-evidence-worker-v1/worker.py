# Frozen, synthetic evidence-only worker. It receives no oracle data.
import json
import os
from pathlib import Path
import sys

request,denied_path,response=map(Path,sys.argv[1:])
try:
    denied_path.read_bytes()
except PermissionError:
    read_denied=True
else:
    raise ValueError("Oracle reading unexpectedly allowed")

try:
    handle=os.open(denied_path,os.O_WRONLY)
except PermissionError:
    write_denied=True
else:
    os.close(handle)
    raise ValueError("Oracle writing unexpectedly allowed")

from hashlib import sha256
def require(ok,why):
    if not ok:
        raise ValueError(why)
def payload_digest(obj):
    return sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
claims=("numericalTolerance","fullSupport","fixedRosterComplete","fullReceiptChain")
statuses=("scored","missing","invalid")
expected_keys={"ticket","endpoints","assignedUnits","records","receipts"}
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
rows=json.loads(request.read_bytes())
response_body={ticket:dict(requestSha256=payload_digest(value),
                          answers=dict(zip(claims,adjudicate(value),strict=True)))
               for ticket,value in rows.items()}
out=json.dumps(dict(readDenied=read_denied,writeDenied=write_denied,rows=response_body),
               sort_keys=True,separators=(",",":"),allow_nan=False).encode()
with response.open("r+b") as stream:
    stream.write(out)
    stream.truncate()
