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
dlls=[os.add_dll_directory(str(root/'runtime-rawpy'/'rawpy')),os.add_dll_directory(str(vc))]
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

raw=(root/"protocollo-maschera.json").read_bytes()
p=json.loads(raw)
archive=capture/"HeartNebula.zip"
receipt=capture/"riscontro.json"
require(digest(archive)==p["captureZip"] and digest(receipt)==p["captureReceipt"],"inputs changed")
assert (astropy.__version__,np.__version__)==("7.2.0","2.3.5")
meta=json.loads(receipt.read_bytes())
modes=sorted(meta["inputs"]["lights"],key=lambda row:row["dateTimeOriginal"])
require(len(modes)==39 and (rawpy.__version__,tuple(rawpy.libraw_version))==("0.25.1",(0,21,4)),
        "unexpected raw reader or light membership")
require(sha256(raw).hexdigest()=="7171ffbc633ed31f11989aa50dfadea9c3ccea99c437bd36e7626ebb85f46d91","frozen mask replication protocol changed")
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

def medians(image):
    return np.array([np.median(image[i*cell:(i+1)*cell,j*cell:(j+1)*cell]) for i,j in bins])

def masked_model(image,usable):
    select=train&usable
    withheld=~train&usable
    counts=[int(select.sum()),int(withheld.sum())]
    if min(counts)<min(p["minimumFitCells"],p["minimumValidationCells"]):
        return None,counts
    values=medians(image)
    fits=[]
    for t in (3,6):
        A=design[:,:t]
        param,_,rank,singular=np.linalg.lstsq(A[select],values[select],rcond=None)
        if rank!=t or singular[0]/singular[-1]>p["maxDesignCondition"]:
            continue
        err=np.median(np.abs((A@param-values)[withheld]))
        fits.append((err,t,image-pix[:,:,:t]@param))
    if not fits:
        return None,counts
    return min(fits,key=lambda f:f[0]),counts

def practical(image):
    observed=medians(image)
    H=design[:,:3]
    coef,_,_,_=np.linalg.lstsq(H[train],observed[train],rcond=None)
    residual=observed-H@coef
    med=np.median(residual[train])
    scale=max(1e-9,1.4826*np.median(np.abs(residual[train]-med)))
    bad=(residual>med+p["maskSigma"]*scale).reshape(n//cell,n//cell)
    padded=np.pad(bad,1)
    return ~np.lib.stride_tricks.sliding_window_view(padded,(3,3)).any(axis=(2,3)).ravel()

def known(template):
    return np.array([np.max(template[i*cell:(i+1)*cell,j*cell:(j+1)*cell])<p["blankTruthMaxFraction"]
                     for i,j in bins])

def difference(sky,signal,keep_before,keep_after):
    a,b=masked_model(sky,keep_before),masked_model(sky+signal,keep_after)
    if a[0] is None or b[0] is None:
        return dict(status="abstained",supportBefore=a[1],supportAfter=b[1])
    return dict(status="evaluated",supportBefore=a[1],supportAfter=b[1],
                beforeDegree=a[0][1],afterDegree=b[0][1],**score(b[0][2]-a[0][2],signal))

open_mask=np.ones(len(bins),dtype=bool)
plane=100+3*X+4*Y
f,count=masked_model(plane,open_mask)
assert count==[32,32] and f is not None
np.testing.assert_allclose(f[2],0,rtol=0,atol=1e-10)
assert masked_model(plane,np.zeros(len(bins),dtype=bool))[0] is None
broad=np.ones_like(plane)
assert not known(broad).any()

rows=[]
with ZipFile(archive) as z:
    for index in p["frameIndices"]:
        item=modes[index]
        data=z.read(item["member"])
        require(sha256(data).hexdigest()==item["sha256"],"changed light")
        with rawpy.imread(BytesIO(data)) as exposure:
            image=exposure.raw_image_visible
            require(list(image.shape)==p["rawVisibleDimensions"] and exposure.raw_pattern.tolist()==[[0,1],[3,2]]
                    and exposure.color_desc==b"RGBG","changed CFA detector geometry")
            for y,x in product(p["tileStartsY"],p["tileStartsX"]):
                stamp=image[y:y+2*n,x:x+2*n]
                sky=(stamp[::2,1::2].astype(float)+stamp[1::2,::2])/2
                delta=np.diff(sky,axis=1)
                contrast=float(1.4826*np.median(np.abs(delta-np.median(delta)))/np.sqrt(2))
                keep=practical(sky)
                for name,angle,template in templates:
                    control=known(template)
                    for amplitude in p["amplitudeNoise"]:
                        signal=amplitude*contrast*template
                        measured=difference(sky,signal,keep,practical(sky+signal))
                        capped=difference(sky,signal,control,control)
                        base=difference(sky,signal,open_mask,open_mask)
                        rows.append(dict(frame=index,tile=[x,y],profile=name,angle=angle,amplitude=amplitude,
                                          unmasked=base,blindMask=measured,knownProfileMask=capped))
assert len(rows)==729
summary={}
for name in ("shortFilament","longFilament","broadDiffuse"):
    subset=[r for r in rows if r["profile"]==name]
    summary[name]={}
    for key in ("unmasked","blindMask","knownProfileMask"):
        live=[r[key] for r in subset if r[key]["status"]=="evaluated"]
        summary[name][key]=dict(total=len(subset),evaluated=len(live),abstained=len(subset)-len(live),
                               passed=sum(r["passed"] for r in live),
                               medianFluxErrorPct=None if not live else round(100*float(np.median(
                                   [r["relativeFluxError"] for r in live])),8))
receipt=dict(schema="BKL046_IC1805_DIFFUSE_MASK_FROZEN_REPLICATION_V1",summary=summary,rows=rows,
             scientificClosures=0,nativeExecutions=0,protocolSha256=sha256(raw).hexdigest(),programSha256=digest(Path(__file__)))
with out.open("xb") as f:
    f.write((json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False)+"\n").encode())
print(json.dumps(dict(sha256=digest(out),summary=summary)))
