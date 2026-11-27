import argparse
import ast
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import stat
import sys

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def digest(raw):
    return sha256(raw).hexdigest()

def ordinary(path):
    info=path.lstat()
    require(stat.S_ISREG(info.st_mode) and not getattr(info,"st_file_attributes",0)&0x400,"INVALID_FILE:"+path.name)
    return path.read_bytes()

def pinned(path,sha):
    raw=ordinary(path)
    require(digest(raw)==sha,"PIN_DIFFERS:"+path.name)
    return raw

def run(root, archive, comparator, dependencies, outputs):
    sys.path.insert(0,str(dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    require((np.__version__,astropy.__version__)==("2.3.5","7.2.0"),"RUNTIME_DIFFERS")
    pin="ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a"
    plan=json.loads(pinned(root/"piano.json",pin))
    report=json.loads(pinned(archive/"riscontro.json",plan["originReport"]))
    script=pinned(comparator,plan["comparator"])
    fn=[n for n in ast.parse(script).body if isinstance(n,ast.FunctionDef) and n.name=="matches"]
    require(len(fn)==1,"PREDICATE_DIFFERS")
    scope={"np":np}
    exec(compile(ast.Module(body=fn,type_ignores=[]),str(comparator),"exec"),scope)

    def decoded(raw,label):
        with fits.open(BytesIO(raw),memmap=False) as hdus:
            require(len(hdus)==1 and isinstance(hdus[0],fits.PrimaryHDU),"WRONG_HDU:"+label)
            image=hdus[0].data
            require(image is not None and list(image.shape)==plan["outputShapeCHW"],"WRONG_GEOMETRY:"+label)
            require(image.dtype.kind=="f" and np.isfinite(image).all(),"NONFINITE_OR_NONFLOAT:"+label)
            return image.astype(float)

    kinds=plan["fitsKinds"]
    oracle_names=sorted({n for sig in report["predictedSignatures"].values() for n in sig})
    reference={}
    for name in oracle_names:
        pair=[]
        for kind in kinds:
            file=f"{name}-{kind}.fits"
            key="oracoli/"+file
            pair.append(decoded(pinned(archive/key,report["fixtureSha256"][key]),file))
        reference[name]=tuple(pair)
    cases=plan["cases"]
    require([(c["matrix"],c["origin"]) for c in cases]==[(r["matrix"],r["declaredOrigin"]) for r in report["rows"]],
            "ORDER_DIFFERS")
    names={f"{case['id']}-{kind}.fits" for case in cases for kind in kinds}
    require({p.name for p in outputs.iterdir()}==names,"OUTPUT_NAMESPACE_DIFFERS")
    output_hashes={}
    observed=[]
    for case in cases:
        actual=[]
        for kind in kinds:
            name=f"{case['id']}-{kind}.fits"
            raw=ordinary(outputs/name)
            output_hashes[name]=digest(raw)
            actual.append(decoded(raw,name))
        require((actual[1]>=0).all(),"NEGATIVE_WEIGHT:"+case["id"])
        hits=[name for name,oracle in reference.items() if scope["matches"](actual,oracle)]
        observed.append({"case":case["id"],"matches":hits})
    for name,sha in output_hashes.items():
        pinned(outputs/name,sha)
    require({p.name for p in outputs.iterdir()}==names,"OUTPUT_NAMESPACE_CHANGED_DURING_READ")
    complete=all(len(r["matches"])==1 for r in observed)
    sequence=[r["matches"][0] for r in observed] if complete else None
    hypotheses=[k for k,v in report["predictedSignatures"].items() if v==sequence] if complete else []
    status="MATCHED_TESTED_HYPOTHESIS" if len(hypotheses)==1 else "UNMODELED_SEQUENCE" if complete else "UNRESOLVED_CASE"
    return {"schema":"BKL046_CFA_ORIGIN_OUTPUT_CLASSIFICATION_V1","planSha256":pin,
            "oracleReportSha256":plan["originReport"],"status":status,"hypotheses":hypotheses,
            "cases":observed,"outputSha256":output_hashes,"provesNativeProvenance":False,
            "provesCoordinatorAdmission":False,"scientificClosures":0}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for field in ("planDirectory","oracleDirectory","comparator","dependencies","outputs","receipt"):
        parser.add_argument(field,type=Path)
    a=parser.parse_args()
    result=run(a.planDirectory,a.oracleDirectory,a.comparator,a.dependencies,a.outputs)
    with a.receipt.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(result["status"])
