import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

PLAN = "ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a"
MANIFEST = "c340a6e939e27ceee6a5d17fcde275c062994b35d581bc6f043ac1f2c5796ec9"
CLASSIFIER = "cd8976b93abc63ce0c2733ee3456b8dfe2eb91a4a54f586ae089090a7722b589"
ROOT = "O:/BKL046-CFA-origine-nativa-v1"
INPUT = "O:/BKL046-CFA-origine-fattoriale-v1/prodotti/xdrz/"
SETTINGS = {"enableCFA":True,"scale":1,"dropShrink":0.70,"useLUT":False,
            "enableRejection":False,"enableImageWeighting":False,"enableSurfaceSplines":False,
            "enableLocalNormalization":False,"enableAdaptiveNormalization":False,
            "truncateOnOutOfRange":False,"closePreviousImages":False,"showImages":False}
ENUMS = ("onError","cfaPattern","kernelFunction")

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def digest(raw):
    return sha256(raw).hexdigest()

def read_pin(path,pin):
    raw=path.read_bytes()
    require(digest(raw)==pin,"AUTHORITY_CHANGED:"+path.name)
    return raw

def pairs(items):
    result={}
    for k,v in items:
        require(k not in result,"DUPLICATE_JSON_KEY")
        result[k]=v
    return result

def parse(raw):
    return json.loads(raw,object_pairs_hook=pairs)

def event(line,kind):
    prefix=kind+" "
    require(line.startswith(prefix),"UNEXPECTED_EVENT_ORDER")
    return parse(line[len(prefix):])

def verify(binding, plan_dir, oracle_dir, comparator, deps, run):
    require(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",binding) is not None,
            "INVALID_EXPECTED_RESERVATION")
    plan=parse(read_pin(plan_dir/"piano.json",PLAN))
    manifest=parse(read_pin(plan_dir/"batch-manifest.json",MANIFEST))
    require(manifest["planSha256"]==PLAN and manifest["caseOrder"]==[c["id"] for c in plan["cases"]],
            "AUTHORITY_PLAN_DIFFERS")
    marker_file=run/"batch.done.json"
    log_file=run/"events.txt"
    marker_bytes=marker_file.read_bytes()
    log=log_file.read_bytes()
    expected=dict(schema="BKL046_CFA_ORIGIN_BATCH_MARKER_V1",scope="OUTPUT_MARKER_NOT_ADMISSION",
                  operation=manifest["operation"],planSha256=PLAN,reservation=binding,cases=manifest["caseOrder"])
    require(parse(marker_bytes)==expected,"MARKER_CONTEXT_DIFFERS")
    lines=log.decode("utf-8").splitlines()
    require(len(lines)==2*len(plan["cases"]),"TRANSCRIPT_COUNT_DIFFERS")
    enums=None
    for i,case in enumerate(plan["cases"]):
        case_id=case["id"]
        parameters=event(lines[2*i],"DSG_CFA_PARAMETERS")
        outputs=event(lines[2*i+1],"DSG_CFA_EXPORT")
        require(set(parameters)=={"caseId","settings","source"} and parameters["caseId"]==case_id,
                "PARAMETER_CASE_DIFFERS")
        require(type(parameters["source"]) is str and parameters["source"].strip(),"SOURCE_READBACK_MISSING")
        settings=parameters["settings"]
        require(set(settings)==set(SETTINGS)|set(ENUMS)|{"inputData"},"SETTINGS_NAMESPACE_DIFFERS")
        require(all(type(settings[k]) is type(v) and settings[k]==v for k,v in SETTINGS.items()),
                "SETTINGS_DIFFERS")
        observed_enums=[settings[k] for k in ENUMS]
        require(all(type(n) is int for n in observed_enums) and (enums is None or enums==observed_enums),
                "ENUMERATORS_INCONSISTENT")
        enums=observed_enums
        inputs=[f"shear-{label}-{case['matrix']}-origin{case['origin']:.1f}.xdrz" for label in "abc"]
        require(all(n in manifest["xdrzSha256"] for n in inputs),"INPUT_NOT_IN_MANIFEST")
        observed=settings["inputData"]
        require(type(observed) is list and len(observed)==3 and
                all(type(r) is list and len(r)==3 and r[0] is True and r[1:]==[INPUT+n,""]
                    for r,n in zip(observed,inputs,strict=True)),"INPUT_DECLARATION_DIFFERS")
        prefix=f"{ROOT}/{binding}/outputs/{case_id}"
        require(outputs==dict(caseId=case_id,intensity=prefix+"-rgb.fits",weights=prefix+"-weight.fits"),
                "EXPORT_DECLARATION_DIFFERS")

    classifier=plan_dir/"classifica.py"
    source=read_pin(classifier,CLASSIFIER)
    namespace={"__name__":"sealed_classifier","__file__":str(classifier)}
    exec(compile(source,str(classifier),"exec"),namespace)
    result=namespace["run"](plan_dir,oracle_dir,comparator,deps,run/"outputs")
    require(marker_file.read_bytes()==marker_bytes and log_file.read_bytes()==log,"TRANSCRIPT_CHANGED_DURING_READ")
    return {"schema":"BKL046_CFA_ORIGIN_BOUND_BATCH_EVIDENCE_V1","reservation":binding,"operation":manifest["operation"],
            "batchSha256":manifest["candidateSha256"],"markerSha256":digest(marker_bytes),"eventsSha256":digest(log),
            "reportedEnumerators":enums,"classification":result,"verifiedRuntimeObservation":False,
            "provesCoordinatorAdmission":False,"scientificClosures":0}

if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("reservation")
    for n in ("planDirectory","oracleDirectory","comparator","dependencies","runDirectory","receipt"):
        cli.add_argument(n,type=Path)
    a=cli.parse_args()
    r=verify(a.reservation,a.planDirectory,a.oracleDirectory,a.comparator,a.dependencies,a.runDirectory)
    with a.receipt.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(r["classification"]["status"])
