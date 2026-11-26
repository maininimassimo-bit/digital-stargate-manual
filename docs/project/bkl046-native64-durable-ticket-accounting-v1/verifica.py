"""Local development fixture for durable, one-shot Native64 response accounting."""
import ast
from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import monotonic, sleep


def require(ok, why):
    if not ok:
        raise ValueError(why)


def encode(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


def digest(raw):
    return sha256(raw).hexdigest()


def connect(db):
    handle=sqlite3.connect(db,timeout=12,isolation_level=None)
    handle.execute("PRAGMA synchronous=FULL")
    return handle


def create(db):
    with closing(connect(db)) as conn:
        conn.executescript("""
            CREATE TABLE tickets (
                id TEXT PRIMARY KEY,
                packet TEXT NOT NULL,
                truth BLOB NOT NULL,
                state TEXT NOT NULL CHECK (state IN ('ASSIGNED','SCORED','MISSING_RESPONSE','INVALID_RESPONSE')),
                answer_sha TEXT,
                verdict BLOB,
                CHECK (state = 'ASSIGNED' AND answer_sha IS NULL AND verdict IS NULL OR
                       state <> 'ASSIGNED' AND verdict IS NOT NULL),
                CHECK (state NOT IN ('SCORED','INVALID_RESPONSE') OR answer_sha IS NOT NULL)
            );
            CREATE TRIGGER immutable_final BEFORE UPDATE ON tickets
            WHEN OLD.state <> 'ASSIGNED' OR NEW.state = 'ASSIGNED' OR NEW.id <> OLD.id OR
                 NEW.packet <> OLD.packet OR NEW.truth <> OLD.truth
            BEGIN SELECT RAISE(ABORT, 'immutable ticket'); END;
            CREATE TRIGGER no_deletion BEFORE DELETE ON tickets
            BEGIN SELECT RAISE(ABORT, 'ticket retained'); END;
        """)


CLAIMS=("within_five_percent","supported_endpoints","population_validated","workflow_admitted")


def adjudicator(path,pin):
    raw=path.read_bytes()
    require(digest(raw)==pin,"Changed adjudication program")
    tree=ast.parse(raw)
    needed={"no_duplicates","adjudicate"}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in needed]
    require({n.name for n in nodes}==needed,"Adjudication surface changed")
    ns=dict(json=json,claims=CLAIMS)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),"exec"),ns)
    return ns["adjudicate"]


def finalize(db, ticket, raw, score, barrier=None, release=None):
    with closing(connect(db)) as conn:
        conn.execute("BEGIN IMMEDIATE")
        row=conn.execute("SELECT packet,truth,state FROM tickets WHERE id=?",(ticket,)).fetchone()
        require(row is not None,"Unknown ticket")
        packet, truth, state=row
        if state!="ASSIGNED":
            conn.rollback()
            return "REPLAY_REJECTED"
        result=score(dict(ticketSha256=ticket,packetSha256=packet),raw,json.loads(truth),set())
        conn.execute("UPDATE tickets SET state=?, answer_sha=?, verdict=? WHERE id=?",
                     (result["state"],None if raw is None else digest(raw),encode(result),ticket))
        if barrier is not None:
            barrier.write_text("pending commit",encoding="ascii")
            deadline=monotonic()+18
            while release is None or not release.is_file():
                require(monotonic()<deadline,"Test barrier expired")
                sleep(.025)
        conn.commit()
    return result["state"]


def command(db,ticket,answer,parent,pin,barrier=None,release=None,entered=None):
    return [sys.executable,"-I","-B","-S",str(Path(__file__).resolve()),"worker",
            str(db),ticket,str(answer),str(parent),pin,str(barrier) if barrier else "-",
            str(release) if release else "-",str(entered) if entered else "-"]


def finished(proc):
    output,error=proc.communicate(timeout=18)
    require(proc.returncode==0,"Worker error: "+error.decode(errors="replace"))
    return output.decode().strip()


def run(cfg, parent, out):
    score=adjudicator(parent,cfg["adjudicator"])
    with TemporaryDirectory(prefix="native64-ticket-",dir=out.parent) as directory:
        root=Path(directory)
        db=root/"tickets.sqlite"
        create(db)
        ids={label:digest(label.encode()) for label in ("race","crash","absent","invalid")}
        packet=digest(b"fixture packet")
        truth=encode(dict(zip(CLAIMS,(False,True,False,False),strict=True)))
        with closing(connect(db)) as conn:
            conn.executemany("INSERT INTO tickets (id,packet,truth,state) VALUES (?,?,?,'ASSIGNED')",
                             [(ticket,packet,truth) for ticket in ids.values()])
        answers={}
        for label,ticket in ids.items():
            if label=="absent":
                answers[label]="-"
                continue
            content=(b"{}" if label=="invalid" else
                     encode(dict(ticketSha256=ticket,packetSha256=packet,
                                 claims=dict(zip(CLAIMS,("YES","YES","ABSTAIN","NO"),strict=True)))))
            answer=root/(label+".json")
            answer.write_bytes(content)
            answers[label]=answer

        def start(label, barrier=None, release=None, entered=None):
            return subprocess.Popen(command(db,ids[label],answers[label],parent,cfg["adjudicator"],barrier,release,entered),
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        held,release,contender=root/"held.txt",root/"release.txt",root/"contender.txt"
        a=start("race",barrier=held,release=release)
        limit=monotonic()+15
        while not held.is_file() and a.poll() is None and monotonic()<limit:
            sleep(.025)
        require(held.is_file() and a.poll() is None,"First worker did not hold the transaction")
        b=start("race",entered=contender)
        limit=monotonic()+15
        while not contender.is_file() and b.poll() is None and monotonic()<limit:
            sleep(.025)
        require(contender.is_file() and b.poll() is None and a.poll() is None,
                "No observed overlap")
        release.write_text("commit permitted",encoding="ascii")
        race=sorted((finished(a),finished(b)))
        require(race==["REPLAY_REJECTED","SCORED"],"Unexpected process contention")
        require(finished(start("race"))=="REPLAY_REJECTED","Completed record reusable after restart")
        marker=root/"transaction-open.txt"
        victim=start("crash",marker)
        try:
            limit=monotonic()+15
            while not marker.is_file() and victim.poll() is None and monotonic()<limit:
                sleep(.05)
            require(marker.is_file() and victim.poll() is None,"Worker failed to reach uncommitted state")
        finally:
            if victim.poll() is None:
                victim.kill()
            victim.communicate(timeout=12)
        with closing(connect(db)) as conn:
            state,answer_hash=conn.execute("SELECT state,answer_sha FROM tickets WHERE id=?",(ids["crash"],)).fetchone()
            require((state,answer_hash)==("ASSIGNED",None),"Uncommitted transaction survived")
        require(finished(start("crash"))=="SCORED","Assigned record could not be evaluated after rollback")
        for label,value in (("absent","MISSING_RESPONSE"),("invalid","INVALID_RESPONSE")):
            require(finished(start(label))==value and finished(start(label))=="REPLAY_REJECTED",
                    "Unresolved record could be reused")

        with closing(connect(db)) as conn:
            integrity=conn.execute("PRAGMA integrity_check").fetchone()[0]
            rows=conn.execute("SELECT id,state,verdict FROM tickets ORDER BY id").fetchall()
            require(integrity=="ok" and len(rows)==4,"Ledger integrity failed")
            verdicts=[json.loads(row[2]) for row in rows]
            require(sum(bool(r.get("unsafe")) for r in verdicts)==2
                    and all(r["unresolved"] for r in verdicts),"Ticket accounting changed")
            for stmt in ("DELETE FROM tickets WHERE id=?","UPDATE tickets SET state='ASSIGNED' WHERE id=?"):
                try:
                    conn.execute(stmt,(ids["race"],))
                except sqlite3.IntegrityError:
                    pass
                else:
                    raise ValueError("Terminal record changed")
        report=dict(schema=cfg["schema"],ticketsAssigned=len(rows),unsafeAndUnresolved=2,
                    unresolvedIncludingInvalidOrMissing=4,concurrentResults=race,workerOverlapObserved=True,
                    completedReplayRejectedAfterRestart=True,uncommittedProcessStoppedAndRolledBack=True,
                    unresolvedTerminalReplayRejected=True,deleteAndTerminalUpdateRejected=True,
                    storageIntegrity=integrity,providerCalls=0,nativeExecutions=0,scientificClosures=0)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    mode,*args=sys.argv[1:]
    if mode=="worker":
        database,ticket,answer,parent,pin,barrier,release,entered=args
        data=None if answer=="-" else Path(answer).read_bytes()
        if entered!="-":
            Path(entered).write_text("attempting transaction",encoding="ascii")
        print(finalize(Path(database),ticket,data,adjudicator(Path(parent),pin),
                       None if barrier=="-" else Path(barrier),None if release=="-" else Path(release)))
    elif mode=="fixture":
        policy,parent,output=map(Path,args)
        run(json.loads(policy.read_bytes()),parent,output)
    else:
        raise ValueError("Unrecognized test mode")
