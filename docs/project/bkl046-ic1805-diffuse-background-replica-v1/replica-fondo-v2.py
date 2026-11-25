"""Test whether held-out background error predicts weak-signal preservation."""
from hashlib import file_digest,sha256
from io import BytesIO
from itertools import product
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

root,capture,packages,out,vc=map(Path,sys.argv[1:])
dll_handles=[os.add_dll_directory(str(root/'runtime-rawpy'/'rawpy')),os.add_dll_directory(str(vc))]
sys.path[:0]=[str(root/'runtime-rawpy'),str(packages)]
import rawpy
sys.path.insert(0,str(packages))
import astropy
from astropy.io import fits
import numpy as np

def digest(path):
    with path.open("rb") as f:
        return file_digest(f,"sha256").hexdigest()

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

raw=(root/"protocollo.json").read_bytes()
p=json.loads(raw)
archive=capture/"HeartNebula.zip"
receipt=capture/"riscontro.json"
require(digest(archive)==p["captureZip"] and digest(receipt)==p["captureReceipt"],"inputs changed")
assert (astropy.__version__,np.__version__)==("7.2.0","2.3.5")
meta=json.loads(receipt.read_bytes())
assert (rawpy.__version__,tuple(rawpy.libraw_version))==("0.25.1",(0,21,4))
modes=sorted(meta["inputs"]["lights"],key=lambda row:row["dateTimeOriginal"])
require(len(modes)==39 and all(x["iso"]==800 and x["secondsNumerator"]/x["secondsDenominator"]==60 for x in modes),
        "unexpected raw light acquisition modes")
require(sha256(raw).hexdigest()=="a0c5c02c80331705f3885707c871082938a9bd9786a1cb99ea91e88854e8b972",
        "predeclared replication plan modified")
n=p["sideBinned"]
cell=p["cellBinned"]
u=(np.arange(n)-(n-1)/2)/(n/2)
X,Y=np.meshgrid(u,u)
pix=np.stack((np.ones_like(X),X,Y,X**2,X*Y,Y**2),axis=-1)
bins=list(product(range(n//cell),repeat=2))
train=np.asarray([(i+j)%2==0 for i,j in bins])
design=np.asarray([np.median(pix[i*cell:(i+1)*cell,j*cell:(j+1)*cell].reshape(-1,6),axis=0) for i,j in bins])
mask=X**2+Y**2<=.65**2

def model(image):
    measures=np.array([np.median(image[i*cell:(i+1)*cell,j*cell:(j+1)*cell]) for i,j in bins])
    predictions=[]
    for terms in (3,6):
        A=design[:,:terms]
        fit,_,rank,_=np.linalg.lstsq(A[train],measures[train],rcond=None)
        require(rank==terms,"rank-deficient fit")
        error=np.median(np.abs((A@fit-measures)[~train]))
        surface=pix[:,:,:terms]@fit
        predictions.append((float(error),image-surface))
    choice=int(predictions[1][0]<predictions[0][0])
    return predictions,choice

# Plane and invariance controls. Small evaluation tolerance accounts for rounding only.
plane=100+7*X-3*Y
mock,choice=model(plane)
np.testing.assert_allclose(mock[0][1],0,rtol=0,atol=1e-10)
np.testing.assert_allclose(model(plane+500)[0][0][1],mock[0][1],rtol=0,atol=1e-10)

templates=[]
for name,major,minor in (("shortFilament",.38,.045),("longFilament",1.10,.045)):
    for deg in p["angles"]:
        theta=np.deg2rad(deg)
        b=np.cos(theta)*X+np.sin(theta)*Y
        a=-np.sin(theta)*X+np.cos(theta)*Y
        templates.append((name,deg,np.exp(-.5*((a/minor)**2+(b/major)**2))))
templates.append(("broadDiffuse",None,np.exp(-.5*((X/.58)**2+(Y/.39)**2))))
# Signals include wings outside the measurement aperture; remaining signal is tracked across the field.
def score(delta,signal):
    flux=float((delta[mask].sum()-signal[mask].sum())/signal[mask].sum())
    shape=float(np.linalg.norm(delta-signal)/np.linalg.norm(signal))
    return dict(relativeFluxError=flux,relativeL2=shape,passed=max(abs(flux),shape)<=p["relativeTolerance"])

rows=[]
with ZipFile(archive) as z:
    for index in p["frameIndices"]:
        entry=modes[index]
        data=z.read(entry["member"])
        require(sha256(data).hexdigest()==entry["sha256"],"changed light exposure")
        with rawpy.imread(BytesIO(data)) as target:
            image=target.raw_image_visible
            require(list(image.shape)==p["rawVisibleDimensions"] and target.raw_pattern.tolist()==[[0,1],[3,2]]
                    and target.color_desc==b"RGBG" and target.white_level==16224,"changed detector geometry")
            for y,x in product(p["tileStartsY"],p["tileStartsX"]):
                stamp=image[y:y+2*n,x:x+2*n]
                require(stamp.shape==(2*n,2*n) and x%2==y%2==0,"grid changed")
                sky=(stamp[::2,1::2].astype(float)+stamp[1::2,::2])/2
                dif=np.diff(sky,axis=1)
                scale=float(1.4826*np.median(np.abs(dif-np.median(dif)))/np.sqrt(2))
                require(scale>0,"degenerate background")
                original,selected0=model(sky)
                require(np.array_equal(model(sky)[0][selected0][1],original[selected0][1]),"null contrast differs")
                for name,angle,template in templates:
                    for amplitude in p["amplitudeNoise"]:
                        signal=amplitude*scale*template
                        added,selected1=model(sky+signal)
                        fixed=[score(added[i][1]-original[i][1],signal) for i in (0,1)]
                        adaptive=score(added[selected1][1]-original[selected0][1],signal)
                        rows.append(dict(frame=index,tile=[x,y],profile=name,angle=angle,amplitudeNoise=amplitude,
                                         proxyScaleAdu=scale,validationErrorBefore=[m[0] for m in original],
                                         validationErrorAfter=[m[0] for m in added],chosenBefore=selected0,
                                         chosenAfter=selected1,fixed=fixed,adaptive=adaptive))
assert len(rows)==3*9*9*3
summary={}
for name in ("shortFilament","longFilament","broadDiffuse"):
    cases=[r for r in rows if r["profile"]==name]
    sub={}
    for method,i in (("plane",0),("quadratic",1),("selected",None)):
        material=[r["adaptive"] if i is None else r["fixed"][i] for r in cases]
        sub[method]=dict(passCount=sum(r["passed"] for r in material),
                         medianSignedFluxPct=round(float(np.median([m["relativeFluxError"] for m in material]))*100,7),
                         medianL2Pct=round(float(np.median([m["relativeL2"] for m in material]))*100,7))
    summary[name]=dict(cases=len(cases),changedDegree=sum(r["chosenBefore"]!=r["chosenAfter"] for r in cases),byMethod=sub,
                       selectedFailedWhereOtherFixedPassed=sum(not r["adaptive"]["passed"] and
                                 any(v["passed"] for v in r["fixed"]) for r in cases))
res=dict(schema="BKL046_IC1805_DIFFUSE_SPATIAL_MODEL_FROZEN_REPLICATION_V1",summary=summary,rows=rows,
         captureArchiveSha256=p["captureZip"],parentEstimatorSha256=p["archivedEstimatorSha256"],
         selectedInputs=[modes[i]["sha256"] for i in p["frameIndices"]],
         independentField=True,signalInjectionIsDigital=True,
         scientificClosures=0,nativeExecutions=0,protocolSha256=sha256(raw).hexdigest(),programSha256=digest(Path(__file__)))
with out.open("xb") as f:
    f.write((json.dumps(res,sort_keys=True,indent=2,allow_nan=False)+"\n").encode())
print(json.dumps(dict(sha256=digest(out),summary=summary,cases=len(rows))))
