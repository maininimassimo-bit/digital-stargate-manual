"""Trace spatially localized LIN0 aperture-variance features through captured ramp reads."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, previous, decoder, capture, packages, output = map(Path,sys.argv[1:])
raw = protocol.read_bytes()
plan = json.loads(raw)


def exact(path, pin):
    data = path.read_bytes()
    if sha256(data).hexdigest() != pin:
        raise ValueError(f"Changed input {path.name}")
    return data


prior = json.loads(exact(previous/"riscontro.json",plan["previous"]))
metadata = json.loads(exact(capture/"acquisizione.json",plan["capture"]))
env = dict(__name__="archived_decoder")
exec(compile(exact(decoder,plan["decoder"]),str(decoder),"exec"),env)
sys.path.insert(0,str(packages))
import numpy as np
if np.__version__ != "2.3.5":
    raise ValueError("Unexpected NumPy")

readings=(0,1,5,10)
band="upper"
captures=[dict(member,exposure=exposure["exposure"])
          for exposure in metadata["records"] for member in exposure["members"][1:]]
frames, rails=env["decode"](np,capture/"source",captures,band,30,readings)
w=np.array([[.25,.5,.25],[.5,1.,.5],[.25,.5,.25]])
outer=np.ones((11,11),dtype=bool)
outer[3:8,3:8]=False


def metrics(patch):
    window=patch[4:7,4:7]
    rim=np.median(patch[outer])
    return float(np.sum(w*(window-rim)))


# A uniform additive background cancels, and a central pixel retains its unit coefficient.
fixture=np.full((11,11),200.)
fixture[5,5]+=37
if metrics(fixture) != 37:
    raise ValueError("Control of spatial projection failed")


def summarise(exposure_values, focus):
    ids=np.arange(1,31)
    baseline=np.array([value for j,value in enumerate(exposure_values,1) if j not in focus])
    median=float(np.median(baseline))
    mad=float(1.4826*np.median(abs(baseline-median)))
    order=sorted(zip(ids,exposure_values,strict=True),key=lambda row:abs(row[1]-median),reverse=True)
    return dict(referenceMedian=median,referenceRobustScale=mad,
                referenceMin=float(baseline.min()),referenceMax=float(baseline.max()),
                focus=[dict(exposure=i,value=float(exposure_values[i-1])) for i in focus],
                topExposures=[dict(exposure=int(i),value=float(v)) for i,v in order[:5]])


models=[]
for c in (4,15):
    case=next(row for row in prior["summaries"][band]["topFiveRows"] if row["channel"]==c)
    x,y=case["largestWindowXY"]
    first=case["firstExposure"]
    focus=(first,first+1)
    window=(slice(y-4,y+7),slice(x-4,x+7))
    if rails[c][window].shape!=(11,11) or rails[c][window].any():
        raise ValueError("Rail or geometry in local diagnostic support")
    values=np.array([[metrics(frames[i,j][c][window]) for i in range(1,31)] for j in readings])
    steps={}
    for group, i, j in (("read0",None,0),("from0_to1",0,1),("from1_to5",1,2),
                        ("from5_to10",2,3),("from0_to10",0,3)):
        measured=values[j] if i is None else values[j]-values[i]
        steps[group]=summarise(measured,focus)
    for j in range(1,4):
        a,b=focus
        double=(frames[b,readings[j]][c]-frames[b,0][c])-(frames[a,readings[j]][c]-frames[a,0][c])
        wv=float(w.ravel()@double[y:y+3,x:x+3].ravel()/np.sqrt(2))
        steps[f"pairWindowRead{readings[j]}"]=wv
    models.append(dict(channel=c,windowXY=[x,y],firstExposure=first,metrics=steps))
report=dict(schema=plan["schema"],protocolSha256=sha256(raw).hexdigest(),previousSha256=plan["previous"],
            verifiedExposureCount=30,verifiedReads=list(readings),band=band,cases=models,
            physicalCauseEstablished=False,scientificClosures=0,nativeExecutions=0)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
