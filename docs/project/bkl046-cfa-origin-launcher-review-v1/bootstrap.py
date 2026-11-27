from hashlib import sha256
from importlib.abc import MetaPathFinder,Loader
from importlib.util import spec_from_loader
import json
import os
from pathlib import Path
import re
import stat
import sys

root=Path(sys.argv[1])
subject=json.loads(sys.argv[2])
members={}

class Frozen(MetaPathFinder,Loader):
    def find_spec(self,name,path=None,target=None):
        if name in members:
            return spec_from_loader(name,self,origin=str(root/(name+".py")))
        return None
    def create_module(self,spec):
        return None
    def exec_module(self,module):
        module.__file__=str(root/(module.__name__+".py"))
        exec(compile(members[module.__name__],module.__file__,"exec"),module.__dict__)

def checked(path,pin):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=pin:
        raise ValueError("PACKAGE_BYTES_CHANGED:"+path.name)
    return data

for name,pin in subject["memberSha256"].items():
    if re.fullmatch(r"[A-Za-z0-9_.-]+\.(?:py|cjs)",name) is None:
        raise ValueError("INVALID_MEMBER_NAME")
    if name.endswith(".py"):
        members[name[:-3]]=checked(root/name,pin)
sys.meta_path.insert(0,Frozen())

def preflight():
    from runtime_guard import verify_inventory
    pins=checked(root/"runtime-files.json",subject["authoritySha256"]["runtime-files.json"])
    count=verify_inventory("O:/BKL046-ACS-WFC-runtime-7.2.0",pins,subject["authoritySha256"]["runtime-files.json"])
    if count!=3824:
        raise ValueError("ORIGIN_COMPARATOR_RUNTIME_DIFFERS")
    for key in ("work","archive"):
        path=Path(subject[key])
        obs=path.lstat()
        if not stat.S_ISDIR(obs.st_mode) or getattr(obs,"st_file_attributes",0)&0x400:
            raise ValueError("ORIGIN_STORAGE_ROOT_DIFFERS:"+key)
    source=Path("K:/DigitalStarGate/pixinsight-coordination-20261114-r1/coordinator.py")
    namespace={"__file__":str(source),"__name__":"origin_preflight"}
    exec(compile(checked(source,subject["r4"]["coordinator.py"]),str(source),"exec"),namespace)
    if namespace["scan_pixinsight"]():
        raise ValueError("PIXINSIGHT_ALREADY_PRESENT")
    print(json.dumps({"comparatorFilesVerified":count,"rootsVerified":True,"pixInsightProcesses":0}))

mode=sys.argv[3]
if mode=="preflight":
    preflight()
elif mode=="parent":
    from parent_origine import run_bound_parent
    sys.cfa_capture_command=[sys.executable,"-I","-B","-S","-c",members["bootstrap"].decode("utf-8"),
                             str(root),sys.argv[2],"capture"]
    run_bound_parent()
elif mode=="compare":
    import uuid
    from runtime_guard import verify_inventory
    env=root/"runtime-files.json"
    pin=subject["authoritySha256"]["runtime-files.json"]
    if verify_inventory("O:/BKL046-ACS-WFC-runtime-7.2.0",checked(env,pin),pin)!=3824:
        raise ValueError("ORIGIN_COMPARATOR_RUNTIME_DIFFERS")
    rid=sys.argv[4]
    if str(uuid.UUID(rid,version=4))!=rid:
        raise ValueError("INVALID_COMPARISON_RESERVATION")
    authority=root/"autorita"
    run=Path(subject["work"])/rid
    verifier=authority/"verifica-batch.py"
    source=checked(verifier,subject["authoritySha256"]["autorita/verifica-batch.py"])
    sys.argv=[str(verifier),rid,str(authority),str(authority/"oracoli-prova"),str(authority/"verifica-v4.py"),
              "O:/BKL046-ACS-WFC-runtime-7.2.0",str(run),str(run/"control"/"comparison.json")]
    exec(compile(source,str(verifier),"exec"),{"__file__":str(verifier),"__name__":"__main__"})
elif mode=="check-import":
    from parent_origine import run_bound_parent
    if not callable(run_bound_parent):
        raise ValueError("PARENT_ENTRY_UNAVAILABLE")
    print(json.dumps({"parentLoaded":True,"members":len(members),"launched":False}))

elif mode in ("hold","capture"):
    name={"hold":"custodia","capture":"capture_worker"}[mode]
    file=str(root/(name+".py"))
    exec(compile(members[name],file,"exec"),{"__file__":file,"__name__":"__main__"})
else:
    raise ValueError("INVALID_PACKAGE_ROLE")
