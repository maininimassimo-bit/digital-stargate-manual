from argparse import ArgumentParser
from contextlib import ExitStack, contextmanager
import hashlib
import json
import msvcrt
import os
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET
from zipfile import ZipFile

PLAN="841fea0e7bc282073fe21dd1fae08c183347084376e3bbdf3632bb062853d01b"
CONTRACT="a2f32c59f7185f1ba18e7e4d3379663a232d2ab9c98db54466eed62003492568"
BATCH="056896b3d8ca6355f65d4efe9fde13f394c164619c43a5be5cd5dc531d82f8b6"
FRACTIONAL="e6c1a6c7c4a9199e9131f824153268a6ad64f90d0b33b6edc320c802c361c733"
SELECTOR="da446f4272522fd192f6de3dab61fb63b22a0f4f8491772ae4475ca0cb2518dd"
WIN32="417d0c3860925a1ba6ddc8c5721ebb190ec8ab9ae9c904df43344aec0129f04c"
OPERATION="BKL046_CFA_XDRZ_TWO_DROP_CONTROL_DSG_SHARED_001"
RUN="O:/BKL046-CFA-XDRZ-controllo-due-depositi-runs-v1/"
ROOTS={"integer":"O:/BKL046-CFA-XDRZ-valor-zero-tre-ingressi-v1/fixture/",
       "fractional":"O:/BKL046-CFA-XDRZ-testimone-larghezza-v1/input/"}
NS={"x":"http://www.pixinsight.com/xdrz"}
NAME=re.compile(r"[a-z0-9][a-z0-9-]*\.(fits|xdrz)")
HEX=re.compile(r"[0-9a-f]{64}")
UUID=re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}")


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def verified(path,expected):
    raw=path.read_bytes()
    require(digest(raw)==expected,f"Changed bytes: {path.name}")
    return raw


def verified_sources(batch_dir):
    plan=json.loads(verified(batch_dir/"piano.json",PLAN))
    contract=json.loads(verified(batch_dir/"contratto.json",CONTRACT))
    require(plan["operation"]==contract["operation"]==OPERATION and contract["planSha256"]==PLAN
            and plan["fractionalArchiveSha256"]==FRACTIONAL and len(plan["cases"])==12,"Plan binding differs")
    catalog={}
    for label,key in (("integer","integerInputPins"),("fractional","fractionalInputPins")):
        catalog[label]={n:h for n,h in plan[key].items() if n.startswith("integer-") and NAME.fullmatch(n)}
        require(all(HEX.fullmatch(h) for h in catalog[label].values()),"Invalid pinned member")
    require(tuple(map(len,catalog.values()))==(15,9),"Unexpected physical input roster")
    return plan,catalog


def dependencies(label,raw):
    root=ET.fromstring(raw)
    paths={}
    for key in ("SourceImage","CFASourceImage"):
        value=root.findtext("x:"+key,namespaces=NS)
        require(isinstance(value,str) and value.startswith(ROOTS[label]),"Unexpected embedded input path")
        name=value[len(ROOTS[label]):]
        require(NAME.fullmatch(name) and name.endswith(".fits"),"Invalid linked image")
        paths[key]=name
    require(paths["SourceImage"]!=paths["CFASourceImage"],"Same RGB and CFA input")
    return list(paths.values())


def stage_fractional(archive,dest,roster):
    require(dest.is_absolute() and dest.name=="input" and dest.parent.is_dir(),"Unexpected staging location")
    require(not getattr(dest.parent.lstat(),"st_file_attributes",0)&0x400,"Redirected staging parent")
    verified(archive,FRACTIONAL)
    with ZipFile(archive) as packaged:
        manifest=json.loads(packaged.read("manifest.json"))
        require(set(packaged.namelist())==set(manifest["sourceFiles"])|{"manifest.json"}
                and {n:h for n,h in manifest["sourceFiles"].items() if NAME.fullmatch(n)}==roster,
                "Staged archive roster differs")
        payload={n:packaged.read(n) for n in roster}
    require(all(digest(v)==roster[n] for n,v in payload.items()),"Staged byte mismatch")
    if dest.exists():
        require(not getattr(dest.lstat(),"st_file_attributes",0)&0x400 and dest.is_dir()
                and {p.name for p in dest.iterdir()}==roster.keys(),"Unexpected existing stage")
        require(all(verified(dest/n,h)==payload[n] for n,h in roster.items()),"Staged readback mismatch")
        return False
    scratch=Path(tempfile.mkdtemp(dir=dest.parent,prefix="stage-"))
    require(scratch.resolve().parent==dest.parent.resolve(),"Staging path escaped")
    for name,raw in payload.items():
        with (scratch/name).open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    for name,h in roster.items():
        verified(scratch/name,h)
    scratch.rename(dest)
    return True


def win32(path):
    namespace={"__name__":"pinned_windows_custody"}
    exec(compile(verified(path,WIN32),str(path),"exec"),namespace)
    return namespace


@contextmanager
def hold_inputs(plan,rosters,roots,primitive):
    api=win32(primitive)
    opener=api["open_held"]
    close=api["kernel"].CloseHandle
    handles={}
    with ExitStack() as stack:
        for kind,root in roots.items():
            require(root.is_absolute() and root.resolve()==root,"Redirected input directory")
            stage_parent=root.parent
            stack.callback(close,opener(stage_parent,directory=True))
            stack.callback(close,opener(root,directory=True))
            require(all((root/name).is_file() for name in rosters[kind]),"Input member missing")
            held={}
            for name,expected in sorted(rosters[kind].items()):
                handle=opener(root/name)
                try:
                    fd=msvcrt.open_osfhandle(handle,os.O_RDONLY|os.O_BINARY)
                except OSError:
                    close(handle)
                    raise
                file=stack.enter_context(os.fdopen(fd,"rb"))
                require(hashlib.file_digest(file,"sha256").hexdigest()==expected,f"Input changed: {name}")
                held[name]=file
            handles[kind]=held
        seen=set()
        for row in plan["cases"]:
            label=row["group"]
            require(row["root"]==ROOTS[label] and len(set(row["files"]))==3,"Changed case paths")
            require(row["xdrzSha256"]==[rosters[label][name] for name in row["files"]],
                    "Changed case input binding")
            for name in row["files"]:
                source=handles[label][name]
                source.seek(0)
                for candidate in [name,*dependencies(label,source.read())]:
                    require(candidate in handles[label],"Unheld descriptor dependency")
                    seen.add((label,candidate))
        require(seen=={(k,n) for k,group in rosters.items() for n in group},"Unreferenced physical input")
        yield handles
        for group,files in handles.items():
            for name,file in files.items():
                file.seek(0)
                require(hashlib.file_digest(file,"sha256").hexdigest()==rosters[group][name],
                        f"Input changed during custody: {name}")


def build_ephemeral_intent(context,batch_dir,selector,install,authority):
    require(set(context)=={"operation","caseId","reservation","pid","casePlanSha256","subjectSha256"}
            and context["operation"]==OPERATION and context["caseId"]=="all-twelve-control-cases"
            and context["casePlanSha256"]==PLAN and context["subjectSha256"]==CONTRACT
            and type(context["pid"]) is int and context["pid"]==os.getpid()
            and UUID.fullmatch(context["reservation"]),"Unexpected parent binding")
    selected=json.loads(verified(selector,SELECTOR))
    require(selected["protocol"]=="DSG_PI_COMMON_COORDINATION_R4"
            and selected["newScientificPlanBindingRequired"] is True,"Changed R4 selector")
    receipt=json.loads(verified(authority/"riscontro.json","677460604bd564285b0571a7149f22f7ae6ea7aed27e5badc1d71b42b0474a0f"))
    for name,h in receipt["runtimeFiles"].items():
        verified(install/name,h)
    source=verified(batch_dir/"batch-cfa.js",BATCH)
    reservation=context["reservation"]
    root=RUN+reservation
    binding=dict(operation=OPERATION,planSha256=PLAN,componentContractSha256=CONTRACT,reservation=reservation)
    script=source+b"\nrunCfaXdrzBatch("+json.dumps(binding,separators=(",",":"),sort_keys=True).encode("ascii")+b");\n"
    return dict(reservation=reservation,operation=OPERATION,planSha256=PLAN,subjectSha256=CONTRACT,
                scriptSha256=digest(script),runDirectory=root,scriptPath=root+"/batch-entry.js"),script


def write_report(path,report):
    with path.open("x",encoding="utf8",newline="\n") as out:
        json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    parser=ArgumentParser()
    for key in ("batch","archive","primitives","selector","install","report"):
        parser.add_argument(key,type=Path)
    a=parser.parse_args()
    frozen,catalog=verified_sources(a.batch)
    actual={key:Path(location) for key,location in ROOTS.items()}
    staged=stage_fractional(a.archive,actual["fractional"],catalog["fractional"])
    fixture_context=dict(operation=OPERATION,caseId="all-twelve-control-cases",casePlanSha256=PLAN,subjectSha256=CONTRACT,
                         pid=os.getpid(),reservation="52d471bc-3d3d-42ea-ad47-29146dbd36a5")
    with hold_inputs(frozen,catalog,actual,a.primitives) as handles:
        intent,script=build_ephemeral_intent(fixture_context,a.batch,a.selector,a.install,actual["integer"])
        require(digest(script)==intent["scriptSha256"],"Ephemeral script changed")
        result=dict(schema="BKL046_TWO_DROP_INPUT_STAGE_CHECK_V1",createStage=staged,
                    planSha256=PLAN,stagedFractionalZipSha256=FRACTIONAL,held={k:len(v) for k,v in handles.items()},
                    referencedCases=len(frozen["cases"]),runtimeFilesVerified=3,
                    inMemoryScriptSha256=intent["scriptSha256"],nativeExecutions=0,admissionRequested=False)
    write_report(a.report,result)
