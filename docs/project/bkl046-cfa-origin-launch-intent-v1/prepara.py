"""Build launch intent for the origin control. This module has no launch function."""
from hashlib import sha256
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

PLAN_PIN="ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a"
BATCH_PIN="4aa98f614ab6e53c520662659ce91ce1a352b6d78291a20f2dd6cd9e0f0d9b3e"
MANIFEST_PIN="c340a6e939e27ceee6a5d17fcde275c062994b35d581bc6f043ac1f2c5796ec9"
SELECTOR_PIN="da446f4272522fd192f6de3dab61fb63b22a0f4f8491772ae4475ca0cb2518dd"
RUNTIME_PLAN_PIN="377aea9a4decbf470a95c92f7f85852bc59f5e056b76a8c7ae110e842fcfd6e7"
OPERATION="BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001"
ROOT=Path("O:/BKL046-CFA-origine-nativa-v1")
BATCH=Path("O:/BKL046-CFA-origine-batch-v1")
AUTHORITY=Path("O:/BKL046-CFA-origine-classificatore-v1")
XDRZ=Path("O:/BKL046-CFA-origine-fattoriale-v1/prodotti/xdrz")
PRIOR=Path("O:/BKL046-CFA-XDRZ-tre-ingressi-v1")
SOURCE=PRIOR/"fixture"
INSTALL=Path("C:/Program Files/PixInsight")
SELECTOR=Path("K:/DigitalStarGate/pixinsight-coordination-20261114-r1/CURRENT.json")

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def digest(raw):
    return sha256(raw).hexdigest()

def checked(reader,path,pin):
    raw=reader(path)
    require(digest(raw)==pin,"UNEXPECTED_BYTES:"+path.name)
    return raw

def prepare(context, reader=Path.read_bytes):
    require(type(context) is dict and set(context)=={"operation","reservation","planSha256","candidateSha256"},
            "UNEXPECTED_INTENT_CONTEXT")
    expected={"operation":OPERATION,"planSha256":PLAN_PIN,"candidateSha256":BATCH_PIN}
    require(all(context[k]==v for k,v in expected.items()),"INTENT_CONTEXT_DIFFERS")
    rid=context["reservation"]
    require(type(rid) is str and re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",rid) is not None,
        "INVALID_RESERVATION")
    selector=json.loads(checked(reader,SELECTOR,SELECTOR_PIN))
    require(selector["protocol"]=="DSG_PI_COMMON_COORDINATION_R4"
            and selector["newScientificPlanBindingRequired"] is True,"SELECTOR_SCOPE_DIFFERS")
    plan=json.loads(checked(reader,AUTHORITY/"piano.json",PLAN_PIN))
    manifest=json.loads(checked(reader,BATCH/"batch-manifest.json",MANIFEST_PIN))
    source=checked(reader,BATCH/"batch-origine.js",BATCH_PIN)
    require(manifest["operation"]==OPERATION and manifest["planSha256"]==PLAN_PIN
            and manifest["candidateSha256"]==BATCH_PIN and [r["id"] for r in plan["cases"]]==manifest["caseOrder"],
            "MANIFEST_SCOPE_DIFFERS")
    runtime=json.loads(checked(reader,PRIOR/"piano-controllo.json",RUNTIME_PLAN_PIN))["runtimeFiles"]
    for relative,pin in runtime.items():
        checked(reader,INSTALL/relative,pin)
    require(len(manifest["xdrzSha256"])==12 and len(manifest["fitsInputsSha256"])==6,"INPUT_COUNT_DIFFERS")
    resolved=set()
    for filename,pin in manifest["xdrzSha256"].items():
        require(Path(filename).name==filename and filename.endswith(".xdrz"),"INVALID_INPUT_MEMBER")
        tree=ET.fromstring(checked(reader,XDRZ/filename,pin))
        for tag in ("SourceImage","CFASourceImage"):
            node=tree.find("{http://www.pixinsight.com/xdrz}"+tag)
            name=Path(node.text).name
            require(node.text==(SOURCE/name).as_posix() and name in manifest["fitsInputsSha256"],
                    "INPUT_REFERENCE_DIFFERS")
            resolved.add(name)
    require(resolved==set(manifest["fitsInputsSha256"]),"FITS_REFERENCE_SET_DIFFERS")
    for filename,pin in manifest["fitsInputsSha256"].items():
        checked(reader,SOURCE/filename,pin)
    run_dir=ROOT/rid
    entry=run_dir/"batch-entry.js"
    binding={k:context[k] for k in ("operation","planSha256","reservation")}
    entry_bytes=source+b"\nrunOriginBatch("+json.dumps(binding,ensure_ascii=True,sort_keys=True,
                                                         separators=(",",":")).encode("ascii")+b");\n"
    command=[(INSTALL/"bin"/"PixInsight.exe").as_posix(),"-n","--automation-mode",
             "--no-startup-scripts","--no-startup-check-updates","-r="+entry.as_posix()]
    intent={"schema":"BKL046_CFA_ORIGIN_LAUNCH_INTENT_V1","scope":"PREPARED_COMMAND_NOT_ADMISSION",
            **binding,"batchSha256":BATCH_PIN,"entrySha256":digest(entry_bytes),
            "imageSha256":runtime["bin/PixInsight.exe"],"selectorSha256":SELECTOR_PIN,
            "verifiedInputs":{"xdrz":12,"fits":6},"verifiedRuntimeFiles":len(runtime),
            "runDirectory":run_dir.as_posix(),"outputDirectory":(run_dir/"outputs").as_posix(),
            "entryPath":entry.as_posix(),"command":command,
            "requirementsBeforeLaunch":["authenticated ARB and RQ","protected activation","live original parent binding",
                                       "coordinator admission","input custody for entire execution"],
            "nativeExecutionStarted":False}
    return intent,entry_bytes
