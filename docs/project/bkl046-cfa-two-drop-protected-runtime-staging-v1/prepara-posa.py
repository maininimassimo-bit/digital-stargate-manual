from hashlib import file_digest,sha256
from io import BytesIO
import json
from pathlib import Path,PurePosixPath
import re
import stat
import sys
from zipfile import ZipFile

archive,source,out=map(Path,sys.argv[1:])
ARCHIVE="eaedba7cb581c3075b17ef1a5753ad0ded530f82e73d9357450578e364b9d6ec"
SOURCE_SUBJECT="4e4b6396c4e1bbf51469549492209e43a19b854e37966369a5800c2a992379b1"
REGEX=re.compile(r"[A-Za-z0-9_.+-]+")

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def digest(raw):
    return sha256(raw).hexdigest()

def rawfile(path):
    info=path.lstat()
    require(stat.S_ISREG(info.st_mode) and not getattr(info,"st_file_attributes",0)&0x400,
            "Runtime file not regular")
    raw=path.read_bytes()
    info2=path.lstat()
    require((info.st_dev,info.st_ino,info.st_size,info.st_mtime_ns)==
            (info2.st_dev,info2.st_ino,info2.st_size,info2.st_mtime_ns),"Runtime source changed while reading")
    return raw

def write(path,raw):
    with path.open("xb") as out:
        out.write(raw)

def encoded(value):
    return (json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()

def edit(raw,before,after):
    require(raw.count(before)==1,"Changed launcher anchor")
    return raw.replace(before,after)

frozen=rawfile(archive)
require(digest(frozen)==ARCHIVE,"Changed frozen launcher ZIP")
require(out.is_dir() and not any(out.iterdir()),"Use an empty staging directory")
with ZipFile(BytesIO(frozen)) as zip:
    original=zip.read("launcher-subject.json")
    require(digest(original)==SOURCE_SUBJECT,"Changed source subject")
    subject=json.loads(original)
    modules,assets=(subject[k] for k in ("memberSha256","assetSha256"))
    files={name:zip.read(name) for name in modules|assets}
    require(all(digest(files[n])==h for n,h in (modules|assets).items()),"Changed archived launcher bytes")
    inactive=zip.read("managed-activation.cjs")
    require(inactive==b"'use strict';\nmodule.exports = null;\n","Activation is not null")
    test=zip.read("collaudo-attivazione.cjs")

files["dispatcher.cjs"]=edit(files["dispatcher.cjs"],b'"O:/BKL046-ACS-WFC-runtime-7.2.0"',
                              b'path.join(__dirname, "runtime")')
files["bootstrap.py"]=edit(files["bootstrap.py"],b'verify_inventory("O:/BKL046-ACS-WFC-runtime-7.2.0"',
                            b'verify_inventory(root / "runtime"')
for n in ("dispatcher.cjs","bootstrap.py"):
    modules[n]=digest(files[n])
require(digest(files["runtime-files.json"])==subject["comparatorRuntimeManifestSha256"],"Runtime manifest differs")
inventory=json.loads(files["runtime-files.json"])["files"]
require(len(inventory)==3824,"Wrong runtime namespace")
runtime=out/"runtime"
runtime.mkdir()
for relative,item in inventory.items():
    key=PurePosixPath(relative)
    require(not key.is_absolute() and str(key)==relative and all(
            part not in (".","..") and not part.endswith(".") and REGEX.fullmatch(part) for part in key.parts),
            "Unsafe inventory path")
    a,b=(root.joinpath(*key.parts) for root in (source,runtime))
    require(a.resolve()==a,"Redirected input dependency")
    blob=rawfile(a)
    require(len(blob)==item["bytes"] and digest(blob)==item["sha256"],"Runtime source digest mismatch")
    b.parent.mkdir(parents=True,exist_ok=True)
    write(b,blob)
for name,raw in files.items():
    write(out/name,raw)
write(out/"managed-activation.cjs",inactive)
write(out/"collaudo-attivazione.cjs",test)
subject["dependsOnProtectedRuntimeDirectory"]="runtime"
subject["stagedParentSubjectSha256"]=SOURCE_SUBJECT
write(out/"launcher-subject.json",encoded(subject))
print(digest((out/"launcher-subject.json").read_bytes()))
