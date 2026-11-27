from hashlib import sha256
import json
from pathlib import Path, PureWindowsPath
import socket
import sys

candidate,source,out=map(Path,sys.argv[1:])
SUBJECT="94db7ebe9d92af0fa16f67da4a45636bea24918b782dcd415f1b8dd5a8bfa423"
AUDIT="64baecec37f7521b06336a0010baf6ec6c67ead3f0405a92d292cf2ce2fe157f"
raw=source.read_bytes()
if sha256(raw).hexdigest()!=AUDIT:
    raise ValueError("Changed permission probe")
namespace={"__name__":"acl_diagnostic"}
exec(compile(raw,str(source),"exec"),namespace)

audit=namespace["audit_access"]
fresh=namespace["fresh_bytes"]
FILE,DIRECTORY=namespace["FILE"],namespace["DIRECTORY"]
if socket.gethostname().upper()!="DSG-SHARED" or namespace["ctypes"].windll.shell32.IsUserAnAdmin():
    raise ValueError("Expected ordinary DSG-Shared token")
subject=json.loads(fresh(candidate/"launcher-subject.json",SUBJECT))
inactive="'use strict';\nmodule.exports = null;\n".encode()
paths={**subject["memberSha256"],**subject["assetSha256"],"launcher-subject.json":SUBJECT,
       "managed-activation.cjs":sha256(inactive).hexdigest()}
for name,pin in paths.items():
    if PureWindowsPath(name).name!=name:
        raise ValueError("Invalid candidate payload")
    fresh(candidate/name,pin)
candidate_results={name:audit(candidate/name,FILE) for name in paths}
runtime =candidate/"runtime"
manifest=json.loads(fresh(candidate/"runtime-files.json",subject["comparatorRuntimeManifestSha256"]))["files"]
runtime_status={}
for suffix in (".py",".pyd",".dll"):
    entries=[rel for rel in sorted(manifest) if rel.lower().endswith(suffix)]
    if entries:
        name=entries[0]
        file=runtime/name
        fresh(file,manifest[name]["sha256"])
        runtime_status[suffix]={"file":name,"permission":audit(file,FILE)["status"]}
pf=Path("C:/Program Files")
destination=pf/"DigitalStarGate"
checks=dict(ordinaryCannotCreateUnderProgramFiles=audit(pf,{"addDirectory":DIRECTORY["addDirectory"]})["status"]=="DENIED_ALL",
            protectedDestinationPresent=destination.exists(),
            pixInsightExecutableControl=audit(pf/"PixInsight"/"bin"/"PixInsight.exe",FILE)["status"])
for name,pin in paths.items():
    fresh(candidate/name,pin)
report=dict(schema="BKL046_TWO_DROP_ORDINARY_TOKEN_DEPLOYMENT_AUDIT_V1",
            subjectSha256=SUBJECT,payloadFilesAudited=len(paths),
            payloadFilesWithMutationRights=sum(v["status"]=="MUTATION_RIGHT_PRESENT" for v in candidate_results.values()),
            candidateFolder=audit(candidate,DIRECTORY)["status"],runtimeFolder=audit(runtime,DIRECTORY)["status"],
            runtimeExamples=runtime_status,**checks,installedProtectedCandidateVerified=False,
            admissionRequested=False,nativeExecutions=0)
with out.open("x",encoding="utf8",newline="\n") as output:
    json.dump(report,output,indent=2,sort_keys=True)
    output.write("\n")
