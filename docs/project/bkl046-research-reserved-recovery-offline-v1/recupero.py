"""Exercise the archived research recovery branch across independent processes."""
import argparse
import ast
from copy import deepcopy
from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import os
import time
import tempfile
from types import SimpleNamespace


def digest(data):
    return sha256(data).hexdigest()


def read(path,pin):
    data=path.read_bytes()
    if digest(data)!=pin:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return data


def load_sources(protocol, flow, origin):
    helper=origin/"replay_two_research_adapter_schemas_g_v2.py"
    ns={"__file__":str(helper),"__name__":"archived_extract"}
    exec(compile(read(helper,protocol["extractorSha256"]),str(helper),"exec"),ns)
    source=origin/"version-backend-offline-contract-pair-g-v1"
    files={}
    for name,pin in ns["SOURCES"].items():
        docs=json.loads(read(source/name,pin))
        for row in docs["files"] if type(docs) is dict else docs:
            files[row["file"]]=read(source/row["file"],row["sha256"])
    engine=ns["build"](files,ns["NEW"])
    counters={"generateCalled":0}
    def unexpected(*args,**kwargs):
        counters["generateCalled"]+=1
        raise AssertionError("OUTBOUND_BOUNDARY_REACHED")
    context={**engine,"decode":json.loads,"contract":SimpleNamespace(**engine),
             "generate":unexpected,"knowledge_packet":unexpected}
    tree=ast.parse(read(flow,protocol["flowSha256"]))
    cls=next(item for item in tree.body if isinstance(item,ast.ClassDef) and item.name=="ResearchFlowMixin")
    names={"research_decision","_research_complete"}
    methods=[node for node in cls.body if isinstance(node,ast.FunctionDef) and node.name in names]
    assert {method.name for method in methods}==names
    exec(compile(ast.Module(body=methods,type_ignores=[]),str(flow),"exec"),context)
    return context,counters


def store_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


class LabFlow:
    broker=SimpleNamespace(worker_id="fixture-worker")

    def __init__(self,database,context):
        self.database=database
        self.db=sqlite3.connect(database,timeout=15)
        self.store=self
        self.research_decision=context["research_decision"].__get__(self)
        self._research_complete=context["_research_complete"].__get__(self)

    def research_enabled(self):
        return True

    def get(self,key):
        row=self.db.execute("select raw from objects where key=?",(key,)).fetchone()
        return (row[0],1) if row is not None else (None,0)

    def _research(self,_request):
        return json.loads(self.db.execute("select raw from cursor").fetchone()[0])

    def _research_mutate(self,request,operation):
        if self.database.name=="race.sqlite":
            self.database.with_name("ready-"+str(os.getpid())).touch(exist_ok=False)
            deadline=time.monotonic()+10
            while len(list(self.database.parent.glob("ready-*")))!=2:
                if time.monotonic()>=deadline:
                    raise TimeoutError("RACE_SYNC_FAILED")
                time.sleep(.01)
        self.db.execute("begin immediate")
        try:
            updated=operation(self._research(request),0)
            self.db.execute("update cursor set raw=?",(store_bytes(updated),))
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return updated


def initial():
    return {"approved":True,"status":"API_RESERVED","apiCalls":1,"cancelRequested":False,
            "nativeTrials":0,"stage":"DETAIL","selectedId":"CP001",
            "checkpoints":{"CP001":{"domain":"LINEAR_ATTESTED","verified":True}},
            "pending":{"owner":"fixture","ordinal":1,"kind":"API"},"decisions":[]}


def create_database(path,case,context):
    row=initial()
    reservation=deepcopy(row)
    if case=="changedPending":
        row["pending"]["ordinal"]=2
    if case=="cancelledBeforeRecovery":
        row["cancelRequested"]=True
    answer={"decision":{"action":"STOP","bindingSha256":context["sha"](reservation),
                        "parentId":"CP001","checkpointId":None,"step":None,
                        "rationale":"Fixture","limitations":"Fixture"},
            "provider":{"responseId":"resp_fixture"}}
    if case=="changedDecision":
        answer["decision"]["bindingSha256"]="0"*64
    db=sqlite3.connect(path)
    try:
        db.execute("create table cursor(raw blob not null)")
        db.execute("create table objects(key text primary key,raw blob not null)")
        db.execute("insert into cursor values (?)",(store_bytes(row),))
        if case!="missingReservation":
            db.execute("insert into objects values (?,?)",("science/research-reservations/fixture/1",store_bytes(reservation)))
        if case!="missingResult":
            db.execute("insert into objects values (?,?)",("science/research-decisions/fixture/1",store_bytes(answer)))
        db.commit()
    finally:
        db.close()


def observe(path):
    with closing(sqlite3.connect(path)) as db:
        row=json.loads(db.execute("select raw from cursor").fetchone()[0])
    return {"status":row["status"],"decisions":len(row["decisions"]),"apiCalls":row["apiCalls"],
            "pendingPresent":row["pending"] is not None}


def worker(database,context,counters):
    instance=LabFlow(database,context)
    try:
        result=instance.research_decision("fixture",{"workerId":"fixture-worker","comparison":{}})
        state=result["status"]
    except context["ProtocolError"] as error:
        state=str(error)
    finally:
        instance.db.close()
    return {"result":state,"generateCalled":counters["generateCalled"]}


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("mode",choices=("test","worker"))
    for name in ("protocol","flow","sources","target"):
        cli.add_argument(name,type=Path)
    args=cli.parse_args()
    protocol=json.loads(args.protocol.read_bytes())
    ctx,counters=load_sources(protocol,args.flow,args.sources)
    if args.mode=="worker":
        print(json.dumps(worker(args.target,ctx,counters)))
        return
    def spawn(db):
        return subprocess.Popen([sys.executable,"-I","-B","-S",__file__,"worker",str(args.protocol),
                                 str(args.flow),str(args.sources),str(db)],stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,text=True)

    def collect(process):
        stdout,stderr=process.communicate(timeout=25)
        if process.returncode:
            raise RuntimeError(stderr)
        result=json.loads(stdout)
        assert result["generateCalled"]==0
        return result["result"]

    results={}
    expected={"missingResult":"RESEARCH_RESERVED_NO_KNOWN_RESPONSE_NO_RETRY",
              "missingReservation":"RESEARCH_RESERVED_NO_KNOWN_RESPONSE_NO_RETRY",
              "changedDecision":"RESEARCH_DECISION_CHANGED","changedPending":"RESEARCH_RESERVED_STATE_CHANGED",
              "cancelledBeforeRecovery":"STOPPED_FOR_REVIEW","validRestart":"STOPPED_FOR_REVIEW"}
    with tempfile.TemporaryDirectory(prefix="recovery-",dir=args.target.parent) as tmp:
        root=Path(tmp)
        for case,outcome in expected.items():
            db=root/(case+".sqlite")
            create_database(db,case,ctx)
            initial_state=observe(db)
            observed=collect(spawn(db))
            final=observe(db)
            assert observed==outcome and final["apiCalls"]==1
            assert (final["decisions"]==1 and not final["pendingPresent"] if observed=="STOPPED_FOR_REVIEW"
                    else final==initial_state)
            row={"observed":observed,"final":final}
            if observed=="STOPPED_FOR_REVIEW":
                row["replay"]=collect(spawn(db))
                assert row["replay"]=="RESEARCH_DECISION_STATE" and observe(db)==final
            results[case]=row

        db=root/"race.sqlite"
        create_database(db,"race",ctx)
        pair=[spawn(db),spawn(db)]
        observed=[collect(process) for process in pair]
        assert observed.count("STOPPED_FOR_REVIEW")==1
        assert set(observed)=={"STOPPED_FOR_REVIEW","RESEARCH_RESERVED_STATE_CHANGED"}
        final=observe(db)
        assert final=={"status":"STOPPED_FOR_REVIEW","decisions":1,"apiCalls":1,"pendingPresent":False}
        results["concurrentConsumers"]={"successes":1,"rejected":1,"final":final}
    report={"schema":"BKL046_RESEARCH_RESERVED_RECOVERY_OFFLINE_V1",
            "programSha256":digest(Path(__file__).read_bytes()),"flowSha256":protocol["flowSha256"],
            "cases":results,"providerCalls":0,"nativeExecutions":0,"scientificClosures":0}
    with args.target.open("x",encoding="utf-8",newline="\n") as out:
        out.write(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps(results,sort_keys=True))


if __name__=="__main__":
    main()
