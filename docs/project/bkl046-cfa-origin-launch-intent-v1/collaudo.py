import importlib.util
import json
from pathlib import Path
import sys

home,out=map(Path,sys.argv[1:])
spec=importlib.util.spec_from_file_location("purpose",home/"prepara.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
context={"operation":mod.OPERATION,"reservation":"348eaf20-c65c-438c-b808-eb1c163f9a31",
         "planSha256":mod.PLAN_PIN,"candidateSha256":mod.BATCH_PIN}
base,entry=mod.prepare(context)
assert mod.digest(entry)==base["entrySha256"]
assert base["command"][-1]=="-r="+base["entryPath"]
assert base["runDirectory"]==f"O:/BKL046-CFA-origine-nativa-v1/{context['reservation']}"
assert base["scope"]=="PREPARED_COMMAND_NOT_ADMISSION"
again,again_entry=mod.prepare(context)
assert base==again and entry==again_entry
assert not Path(base["runDirectory"]).exists()
negatives=[]
def expect(label,reason,params=context,reader=Path.read_bytes):
    try:
        mod.prepare(params,reader)
    except ValueError as e:
        assert str(e)==reason
        negatives.append({"case":label,"reason":reason,"accepted":False})
        return
    raise AssertionError(label+" accepted")
expect("other-operation","INTENT_CONTEXT_DIFFERS",{**context,"operation":"other"})
expect("other-batch","INTENT_CONTEXT_DIFFERS",{**context,"candidateSha256":"0"*64})
expect("invalid-reservation","INVALID_RESERVATION",{**context,"reservation":"../other"})
for name in ("CURRENT.json","batch-origine.js","ImageIntegration-pxm.dll","shear-a-edge05-origin0.5.xdrz","shear-a-cfa.fits"):
    def mutated(path):
        result=path.read_bytes()
        return result+b" " if path.name==name else result
    expect(name+"-changed","UNEXPECTED_BYTES:"+name,reader=mutated)
report={"schema":"BKL046_CFA_ORIGIN_INTENT_OFFLINE_TEST_V1","intent":base,"repeatedByteForByte":True,
        "rejected":negatives,"canonicalStateRead":False,"nativeExecutions":0}
out.write_bytes((json.dumps(report,sort_keys=True,indent=2)+"\n").encode())
