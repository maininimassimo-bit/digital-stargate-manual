"""Apply the frozen Roman LIN0 persistent-step classifier to the separate GAIN acquisition."""
import ast
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

policy, lin_detector, lin_capture, gain, decoder, packages, output = map(Path,sys.argv[1:])
protocol=policy.read_bytes()
cfg=json.loads(protocol)


def exact(path,pin):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=pin:
        raise ValueError(f"Changed input {path.name}")
    return data


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


settings=json.loads(exact(lin_detector/"protocollo.json",cfg["linClassifierProtocol"]))
lin=json.loads(exact(lin_detector/"riscontro.json",cfg["linReport"]))
lc=json.loads(exact(lin_capture/"protocollo.json",cfg["linCaptureProtocol"]))
gc=json.loads(exact(gain/"protocollo.json",cfg["gainCaptureProtocol"]))
require(lc["bands"]==gc["bands"] and tuple(lc["frames"])==(0,1,5,10),"Different pixel/read coordinates")
captures=json.loads(exact(gain/"cattura"/"acquisizione.json",cfg["gainCapture"]))
ns=dict(__name__="stored_decoder")
exec(compile(exact(decoder,cfg["decoder"]),str(decoder),"exec"),ns)

sys.path.insert(0,str(packages))
import numpy as np
require(np.__version__=="2.3.5","Changed NumPy")
p=lin_detector/"misura.py"
tree=ast.parse(exact(p,cfg["linClassifier"]))
functions=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=="classify"]
require(len(functions)==1,"Classifier not found")
rules=dict(np=np,p=settings,z=settings["robustZ"])
exec(compile(ast.Module(body=functions,type_ignores=[]),str(p),"exec"),rules)
classify=rules["classify"]

lin_locations=Counter((group["band"],group["channel"],pixel["x"],pixel["y"])
                      for group in lin["groups"] for pixel in group["pixels"])
summary={}
events=[]
agreement={}
for band in ("lower","upper"):
    data,rails=ns["decode"](np,gain/"cattura"/"source",captures["captures"],band,20,(0,1,5,10))
    assessed=early_count=persistent_count=0
    grouping=set()
    for channel in range(32):
        valid=~rails[channel]
        target=np.stack([[data[i,j][channel]-data[i,0][channel] for j in (1,5,10)] for i in range(1,21)])
        centered=target-np.median(target[:,:,valid],axis=-1)[:,:,None,None]
        locations={(x,y):dict(band=band,channel=channel,x=x,y=y,lin0Detections=count,
                              eligibleInGain=bool(valid[y,x]),firstReadGainAdjustmentAdu=[],
                              gainEarly=0,gainPersistent=0)
                   for (b,c,x,y),count in lin_locations.items() if (b,c)==(band,channel)}
        for i in range(20):
            early, persistent, excess=classify(centered[i],np.delete(centered,i,axis=0))
            early,persistent=early&valid,persistent&valid
            early_count+=int(early.sum())
            persistent_count+=int(persistent.sum())
            assessed+=int(valid.sum())
            if persistent.any():
                ys,xs=np.nonzero(persistent)
                grouping.add((channel,i))
                events.extend(dict(band=band,channel=channel,exposure=i+1,x=int(x),y=int(y),
                                   excessAdu=excess[:,y,x].tolist()) for y,x in zip(ys,xs,strict=True))
            for (x,y),row in locations.items():
                if not row["eligibleInGain"]:
                    continue
                row["firstReadGainAdjustmentAdu"].append(float(excess[0,y,x]))
                row["gainEarly"]+=int(early[y,x])
                row["gainPersistent"]+=int(persistent[y,x])
        for coord,row in locations.items():
            x,y=coord
            row["railHitsByRead"]=dict(
                (str(j),{"zero":sum(int(data[i,j][channel,y,x])==0 for i in range(1,21)),
                         "full":sum(int(data[i,j][channel,y,x])==65535 for i in range(1,21))})
                for j in (0,1,5,10))
            values=row.pop("firstReadGainAdjustmentAdu")
            row["firstReadGainExcessRangeAdu"]=[min(values),max(values)] if values else None
            agreement[band,channel,*coord]=row
    summary[band]=dict(testedPixelExposures=assessed,earlyPixels=early_count,
                       persistentPixels=persistent_count,channelExposureGroups=len(grouping))
require(set(agreement)==set(lin_locations),"Incomplete coordinates")
report=dict(schema=cfg["schema"],protocolSha256=sha256(protocol).hexdigest(),sourceReadIndices=[0,1,5,10],
            lin0Summary=lin["summary"],gainSummary=summary,gainEvents=events,
            lin0DetectedLocationsEvaluated=[agreement[key] for key in sorted(agreement)],
            sourceExposures=20,referenceExposures=19,lin0ReferenceExposures=29,
            physicalCauseVerified=False,nativeExecutions=0,scientificClosures=0)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
