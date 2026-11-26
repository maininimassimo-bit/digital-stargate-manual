"""Build and verify a synthetic two-anchor GitHub transcript without publishing openings."""
from argparse import ArgumentParser
import ast
from hashlib import sha256
from hmac import compare_digest
import json
from pathlib import Path
from secrets import token_hex

parser=ArgumentParser(description=__doc__)
parser.add_argument("mode",choices=("oracle","responses","verify"))
for name in ("protocol","previous","source","work"):
    parser.add_argument(name,type=Path)
arg=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def load(path,pin=None):
    raw=path.read_bytes()
    require(pin is None or sha256(raw).hexdigest()==pin,"Changed input")
    return json.loads(raw)


def emit(path,obj):
    with path.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(obj,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


p=load(arg.protocol)
prior_code=arg.previous/"verifica.py"
raw=prior_code.read_bytes()
require(sha256(raw).hexdigest()==p["verifier"],"Changed commit-reveal verifier")
old_policy=arg.previous/"protocollo.json"
rules=sha256(old_policy.read_bytes()).hexdigest()
require(rules==p["verifierProtocol"],"Changed commit-reveal protocol")
requests=load(arg.source/"richieste-fixture.json",p["fixtureRequests"])
oracle=load(arg.source/"oracolo-fixture.json",p["fixtureOracle"])
names={"digest","oracle_commit","seal","verify"}
nodes=[n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name in names]
require({n.name for n in nodes}==names,"Missing verifier routines")
env=dict(sha256=sha256,json=json,compare_digest=compare_digest,rules=rules,
         requests=requests,oracle=oracle,require=require)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(prior_code),"exec"),env)
digest,seal,verify=[env[name] for name in ("digest","seal","verify")]

root=arg.work
first=root/"impegno-oracolo.json"
second=root/"registro-risposte.json"
openings_path=root/"aperture-locali.json"
if arg.mode=="oracle":
    openings={k:dict(v,nonce=token_hex(32)) for k,v in oracle.items()}
    committed=seal(openings)
    emit(openings_path,openings)
    emit(first,committed)
elif arg.mode=="responses":
    oracle_anchor=load(root/"rilettura-oracolo.json")
    committed=load(first)
    require(oracle_anchor["contentSha256"]==sha256(first.read_bytes()).hexdigest()
            and oracle_anchor["verified"] and oracle_anchor["reason"]=="valid","Missing first remote anchor")
    response=dict(protocol=rules,phase="RESPONSES_SEALED",oracleAnchor=digest(committed),
                  oracleGitCommit=oracle_anchor["commit"],tickets={})
    for i,(ticket,req) in enumerate(sorted(requests.items())):
        state="missing" if i==0 else ("invalid" if i==1 else "scored")
        body=None if i==0 else ({"fixtureMalformed":True} if i==1 else {"fixtureReply":ticket})
        response["tickets"][ticket]=dict(requestSha256=digest(req),state=state,
                                         responseSha256=None if body is None else digest(body))
    emit(second,response)
else:
    committed=load(first)
    terminal=load(second)
    a=load(root/"rilettura-oracolo.json")
    b=load(root/"rilettura-risposte.json")
    for anchor,path in ((a,first),(b,second)):
        require(anchor["contentSha256"]==sha256(path.read_bytes()).hexdigest() and
                anchor["verified"] and anchor["reason"]=="valid","Invalid remote anchor")
    require(b["parents"]==[a["commit"]] and terminal["oracleGitCommit"]==a["commit"],
            "GitHub phase order drift")
    n=verify(committed,digest(committed),terminal,digest(terminal),load(openings_path))
    require(n==32,"Incomplete verification")
    counts={state:sum(r["state"]==state for r in terminal["tickets"].values())
            for state in ("scored","missing","invalid")}
    emit(root/"riscontro.json",dict(schema=p["schema"],oracleAnchor=a,responseAnchor=b,
         orderedGitHubCommitsVerified=True,hostReportedVerifiedSignatures=2,fixtureTickets=n,
         states=counts,oracleOpeningsPublished=False,providerCallAttestation=False,providerCalls=0,
         independentCustodyVerified=False,independentConfirmationUnits=0,scientificClosures=0,
         nativeExecutions=0))
