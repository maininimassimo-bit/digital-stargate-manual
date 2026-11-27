"""Evaluate a uniform positive-step diagnostic across the acquired Roman LIN0 tiles."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, prior_dir, decoder, capture, packages, output=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)


def exact(path,pin):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=pin:
        raise ValueError(f"Changed input {path.name}")
    return data


ancestor=json.loads(exact(prior_dir/"riscontro.json",p["previous"]))
provenance=json.loads(exact(capture/"acquisizione.json",p["capture"]))
module=dict(__name__="pinned_decoder")
exec(compile(exact(decoder,p["decoder"]),str(decoder),"exec"),module)
sys.path.insert(0,str(packages))
import numpy as np
if np.__version__!="2.3.5":
    raise ValueError("Changed NumPy")

sources=[dict(m,exposure=r["exposure"]) for r in provenance["records"] for m in r["members"][1:]]
frames=(0,1,5,10)
bands=("lower","upper")
z=p["robustZ"]


def classify(test, reference):
    median=np.median(reference,axis=0)
    scale=np.maximum(p["minNoiseAdu"],1.4826*np.median(abs(reference-median),axis=0))
    excess=test-median
    persistent=(excess[1:] >= p["minPersistentFraction"]*excess[0]).all(axis=0)
    early=excess[0]>=z*scale[0]
    return early, early&persistent&(excess[1:]>=z*scale[1:]).all(axis=0), excess


fixture=np.zeros((29,3,2,2))
trial=np.array([[[180.,180.],[-180.,0.]],[[160.,10.],[-160.,0.]],[[140.,0.],[-140.,0.]]])
early, persistent, _=classify(trial,fixture)
np.testing.assert_array_equal(early,[[True,True],[False,False]])
np.testing.assert_array_equal(persistent,[[True,False],[False,False]])

summary={}
groups=[]
for band in bands:
    data, rails=module["decode"](np,capture/"source",sources,band,30,frames)
    assessed=early_pixels=persistent_pixels=0
    candidates=[]
    for c in range(32):
        valid=~rails[c]
        transformed=np.stack([[data[i,j][c]-data[i,0][c] for j in frames[1:]]
                              for i in range(1,31)])
        centered=transformed-np.median(transformed[:,:,valid],axis=-1)[:,:,None,None]
        for i in range(30):
            past=np.delete(centered,i,axis=0)
            early,persistent,excess=classify(centered[i],past)
            early,persistent=early&valid,persistent&valid
            assessed+=int(valid.sum())
            early_pixels+=int(early.sum())
            if not persistent.any():
                continue
            persistent_pixels+=int(persistent.sum())
            ys,xs=np.nonzero(persistent)
            candidate=dict(channel=c,exposure=i+1,persistenceCount=len(xs),
                           pixels=[dict(x=int(x),y=int(y),excessAdu=excess[:,y,x].tolist())
                                   for y,x in zip(ys,xs,strict=True)])
            candidates.append(candidate)
            groups.append(dict(band=band,**candidate))
    summary[band]=dict(testedPixelExposures=assessed,earlyPixels=early_pixels,
                       persistentPixels=persistent_pixels,channelExposureGroups=len(candidates))

localized=next(item for item in ancestor["cases"] if item["channel"]==4)
known_x,known_y=localized["windowXY"]
known_exposure=localized["firstExposure"]+1
matched=[pixel for row in groups if row["band"]=="upper" and row["channel"]==4 and row["exposure"]==known_exposure
         for pixel in row["pixels"] if known_x<=pixel["x"]<known_x+3 and known_y<=pixel["y"]<known_y+3]
report=dict(schema=p["schema"],protocolSha256=sha256(raw).hexdigest(),summary=summary, groups=groups,
            knownExploratoryWindowPixelsRecovered=len(matched), independentDiscoveryVerified=False,
            causalAttributionVerified=False, sampleMembershipChanged=False,
            nativeExecutions=0,scientificClosures=0)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
