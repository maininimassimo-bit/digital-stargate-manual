"""Reread a CFA archive and a separately retained R4 release receipt."""
import argparse
from datetime import datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
import re
import stat
import uuid

OPERATION = "BKL046_CFA_XDRZ_SYNTHETIC_DSG_SHARED_001"
PLAN = "377aea9a4decbf470a95c92f7f85852bc59f5e056b76a8c7ae110e842fcfd6e7"
SUBJECT = "e7704c47e1321baca27257e65a2a472065f38762fb65567a6e6352194084b856"
CASES = ["integer-unmasked","integer-green-mask","integer-wrong-channel","shear-center0","shear-edge05"]
EXPORTS = {f"{case}-{kind}.fits" for case in CASES for kind in ("rgb","weight")}
FILES = EXPORTS | {"comparison.json","batch.done.json","events.txt","window.bmp",
                   "normal-close.json","r4-acquired.json","r4-original.json"}

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def hexdigest(data):
    return sha256(data).hexdigest()

def parse(data):
    def pairs(items):
        out = {}
        for k,v in items:
            require(k not in out,"DUPLICATE_JSON_KEY")
            out[k] = v
        return out
    return json.loads(data,object_pairs_hook=pairs)

def plain(path, directory=False):
    info = path.lstat()
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    require(expected(info.st_mode) and not getattr(info,"st_file_attributes",0)&0x400,"NON_ORDINARY_PATH")
    return info

def get(path):
    plain(path)
    return path.read_bytes()

def stamp(value):
    moment = datetime.fromisoformat(value)
    require(moment.utcoffset()==timedelta(0),"INVALID_R4_UTC")
    return moment

def audit(directory, release, marker_pin, release_pin):
    plain(directory,True)
    marker = get(directory/"ARCHIVED.json")
    require(hexdigest(marker)==marker_pin,"ARCHIVE_MARKER_PIN_DIFFERS")
    release_bytes = get(release)
    require(hexdigest(release_bytes)==release_pin,"RELEASE_PIN_DIFFERS")
    released = parse(release_bytes)
    m = parse(marker)
    require((m["schema"],m["state"])==("BKL046_CFA_ARCHIVED_EVIDENCE_V1","EVIDENCE_ARCHIVED_NOT_RELEASED"),"ARCHIVE_SCOPE_DIFFERS")
    context = m["context"]
    rid = context["reservation"]
    require(str(uuid.UUID(rid,version=4))==rid and directory.name==rid,"ARCHIVE_RESERVATION_DIFFERS")
    require((context["operation"],context["plan"],context["subject"])==(OPERATION,PLAN,SUBJECT),"CFA_CONTEXT_DIFFERS")
    require(set(p.name for p in directory.iterdir())==FILES|{"ARCHIVED.json"},"ARCHIVE_NAMESPACE_DIFFERS")
    members=m["members"]
    require(len(members)==len(FILES) and {x["name"] for x in members}==FILES,"MANIFEST_NAMESPACE_DIFFERS")
    content={}
    for item in members:
        name=item["name"]
        data=get(directory/name)
        require(len(data)==item["length"] and hexdigest(data)==item["sha256"],"MEMBER_DIFFERS:"+name)
        content[name]=data
    terminal=m["terminal"]
    require(terminal==dict(context=context,status="CFA_NATIVE_EXIT_OBSERVED",nativeExitCode=0,
                           scientificClosures=0),"TERMINAL_CONTEXT_DIFFERS")
    batch_bytes=content["batch.done.json"]
    require(hexdigest(batch_bytes)==context["batchMarkerSha256"],"BATCH_HASH_DIFFERS")
    require(parse(batch_bytes)==dict(schema="BKL046_CFA_XDRZ_BATCH_OUTPUT_MARKER_V1",scope="OUTPUT_MARKER_NOT_ADMISSION",
                                     operation=OPERATION,planSha256=PLAN,subjectSha256=SUBJECT,reservation=rid,cases=CASES),
            "BATCH_CONTEXT_DIFFERS")
    comparison=parse(content["comparison.json"])
    require(comparison["mode"]=="SUPPLIED_OUTPUTS_COMPARISON_ONLY" and comparison["planSha256"]==PLAN
            and comparison["provesCoordinatorAdmission"] is False,"COMPARISON_SCOPE_DIFFERS")
    require(comparison["exportHashes"]=={n:hexdigest(content[n]) for n in EXPORTS}
            and comparison["eventHash"]==hexdigest(content["events.txt"]),"COMPARISON_LINK_DIFFERS")
    close=parse(content["normal-close.json"])
    require(close["context"]==context and type(close["nativeExit"]) is int and close["nativeExit"]==0
            and close["capture"]==hexdigest(content["window.bmp"])
            and close["comparison"]==hexdigest(content["comparison.json"]),"CLOSE_LINK_DIFFERS")
    require(all(close["window"][n]==context[n] for n in ("pid","creationFiletime")),"WINDOW_CONTEXT_DIFFERS")
    original=parse(content["r4-original.json"])
    require(set(original)=={"pid","callerPid","creationFiletime"}
            and all(type(v) is int and v>0 for v in original.values()),"PARENT_RECORD_DIFFERS")
    acquired=parse(content["r4-acquired.json"])
    require(acquired["protocol"]=="DSG_PI_SERIAL_V1" and acquired["milestone"]=="BKL-046"
            and acquired["reservation"]==rid and acquired["operation"]==OPERATION,"ACQUIRED_SCOPE_DIFFERS")
    require(set(released)==set(acquired)|{"releasedUTC","parentExitCode"} and
            {k:released[k] for k in acquired}==acquired and type(released["parentExitCode"]) is int
            and released["parentExitCode"]==0,"RELEASE_CONTEXT_DIFFERS")
    require(stamp(released["releasedUTC"])>=stamp(acquired["startedUTC"]),"RELEASE_TIME_DIFFERS")
    require(get(directory/"ARCHIVED.json")==marker and get(release)==release_bytes and
            {p.name for p in directory.iterdir()}==FILES|{"ARCHIVED.json"},"CUSTODY_CHANGED_DURING_READ")
    return {"status":"ARCHIVE_AND_RELEASE_RECEIPT_MATCH","reservation":rid,"verifiedMembers":len(content),
            "markerSha256":marker_pin,"releaseSha256":release_pin,"nativeExecutionAttestedByAudit":False}

if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("archive",type=Path)
    cli.add_argument("release",type=Path)
    cli.add_argument("markerSha256")
    cli.add_argument("releaseSha256")
    a=cli.parse_args()
    print(json.dumps(audit(a.archive,a.release,a.markerSha256,a.releaseSha256),sort_keys=True))
