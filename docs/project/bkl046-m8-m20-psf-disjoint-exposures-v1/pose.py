"""Compare PSF angles between disjoint cohorts of native Bayer exposures."""
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

protocol, mosaics, prior, dependencies, output = map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)
sys.path.insert(0,str(dependencies))
from astropy.io import fits
import astropy
import numpy as np
assert (astropy.__version__,np.__version__)==("7.2.0","2.3.5")

def digest(data,pin):
    if sha256(data).hexdigest()!=pin:
        raise ValueError("PIN_MISMATCH")
    return data

old=json.loads(digest(prior.read_bytes(),p["priorSha256"]))
stars=sorted({row["id"] for row in old["injections"]})
assert len(stars)==p["heldOutStars"]==old["heldout"]
with mosaics.open("rb") as stream:
    assert file_digest(stream,"sha256").hexdigest()==p["mosaicSha256"]

shapes=[(q,angle,scale) for q in p["axisRatios"] for angle in
        ([0] if q==1 else range(0,180,p["angleStep"])) for scale in p["widthFactors"]]
shape_array=np.array(shapes)
ratios,angles,scales=shape_array.T
circular=np.flatnonzero(ratios==1)
elliptical=np.flatnonzero(ratios<1)

def library(x,y,width):
    degrees=np.deg2rad(angles)
    c,s=np.cos(degrees),np.sin(degrees)
    alpha=width*scales/(2*np.sqrt(2**(1/p["beta"])-1))
    raster=np.zeros((len(x),len(shapes)))
    for dy in (-1/3,0.,1/3):
        for dx in (-1/3,0.,1/3):
            u=(x[:,None]+dx)*c+(y[:,None]+dy)*s
            v=-(x[:,None]+dx)*s+(y[:,None]+dy)*c
            raster+=(1+(ratios*u*u+v*v/ratios)/alpha**2)**(-p["beta"])
    return raster/9

def losses(x,y,z,models):
    plane=np.column_stack((np.ones(len(x)),x/10,y/10))
    basis,_=np.linalg.qr(plane)
    target=z-basis@(basis.T@z)
    templates=models-basis@(basis.T@models)
    norm=np.sum(templates**2,axis=0)
    cross=templates.T@target
    energy=float((z-z.mean())@(z-z.mean()))
    if energy<=0 or np.linalg.matrix_rank(plane)!=3 or not np.all(norm>0):
        raise ValueError("INVALID_POSE_SAMPLE")
    residual=np.maximum(0.,float(target@target)-cross**2/norm)/energy
    residual[cross<=0]=np.inf
    return residual

def axial(a,b):
    return abs((a-b+90)%180-90)

def evaluate(sets):
    folds=[]
    for i in (0,1):
        training=np.stack(sets[i]).sum(axis=0)
        validation=np.stack(sets[1-i]).sum(axis=0)
        ci=circular[int(np.argmin(training[circular]))]
        ei=elliptical[int(np.argmin(training[elliptical]))]
        if not np.isfinite([training[ci],training[ei],validation[ci],validation[ei]]).all():
            folds.append({"status":"UNQUALIFIED"})
            continue
        gain=(validation[ci]-validation[ei])/validation[ci] if validation[ci]>0 else 0.
        folds.append({"status":"EVALUATED","heldOutGain":float(gain),"candidate":shapes[ei],
                      "circleWidthFactor":float(scales[ci])})
    enough=all(f["status"]=="EVALUATED" and f["heldOutGain"]>=p["minGain"] and
               f["candidate"][0]<=p["maxRatio"] for f in folds)
    angle=None
    if enough and axial(folds[0]["candidate"][1],folds[1]["candidate"][1])<=p["maxAngularDifference"]:
        directions=np.deg2rad([2*f["candidate"][1] for f in folds])
        angle=float(np.rad2deg(np.angle(np.exp(1j*directions).sum()))/2%180)
    return {"qualified":angle is not None,"angle":angle,"folds":folds}

x,y=np.meshgrid(np.arange(-8.,9.,2),np.arange(-8.,9.,2))
x,y=x.ravel(),y.ravel()
models=library(x,y,3.)
idx=shapes.index((.65,45,1))
toy=40+.8*x-.3*y+15*models[:,idx]
sol=losses(x,y,toy,models)
assert sol[idx]<1e-14
explicit=library(x,y,3.)[:,0]
matrix=np.column_stack((explicit,np.ones(len(x)),x/10,y/10))
fit=np.linalg.lstsq(matrix,toy,rcond=None)[0]
assert fit[0]>0 and abs(sol[0]-np.sum((toy-matrix@fit)**2)/np.sum((toy-toy.mean())**2))<1e-12
result=evaluate([[sol],[sol]])
assert result["qualified"] and axial(result["angle"],45)<1e-8

score_bank={star:{band:[[],[]] for band in ("red","blue")} for star in stars}
phases={star:[[],[]] for star in stars}
with ZipFile(mosaics) as archive:
    manifest=json.loads(digest(archive.read("manifest.json"),p["manifestSha256"]))
    assert manifest["colorPattern"]=="RGGB" and manifest["detectorStampShapeXY"]==[48,48]
    xx,yy=np.meshgrid(np.arange(48),np.arange(48))
    half_members=[[],[]]
    for ref in manifest["frames"]:
        name=ref["manifest"]
        frame=json.loads(digest(archive.read(name),manifest["files"][name]))
        h=frame["half"]
        assert h in (0,1) and frame["ordinal"]==ref["ordinal"]
        half_members[h].append(frame["member"])
        lookup={r["star"]:r for r in frame["stamps"]}
        for star in stars:
            row=lookup[star]
            assert all(v%2==0 for v in row["cropOriginXY"])
            name=row["files"][p["calibration"]]
            image_raw=digest(archive.read(name),manifest["files"][name])
            with fits.open(BytesIO(image_raw),memmap=False,checksum=True) as hdus:
                image=hdus[0].data.astype(float)*manifest["scaleAdu"]-manifest["offsetAdu"]
            center=np.asarray(row["referenceToFrameAffine"]["mosaic"]) @ np.array([*row["centerXY"],1.])
            assert center[2]==1 and np.isfinite(center).all()
            center_x,center_y=center[:2]
            x,y=xx-center_x,yy-center_y
            phases[star][h].append([float(center_x%2),float(center_y%2)])
            valid=np.unpackbits(np.frombuffer(bytes.fromhex(row["validMaskBitsLE"]),dtype=np.uint8),
                                bitorder="little",count=48*48).reshape(48,48).astype(bool)
            assert int(valid.sum())==row["validSamples"]
            inside=(x*x+y*y<=p["radius"]**2)&valid
            for i,(band,par) in enumerate((("red",0),("blue",1))):
                support=inside & (xx%2==par)&(yy%2==par)
                assert support.sum()>=p["minValid"]
                ax,ay=x[support],y[support]
                bank=library(ax,ay,old["fwhmNativePxRedBlue"][i])
                score_bank[star][band][h].append(losses(ax,ay,image[support],bank))
assert [len(m) for m in half_members]==[p["expectedPosesPerHalf"]]*2 and not (set(half_members[0])&set(half_members[1]))

rows=[]
for star,bands in score_bank.items():
    fits_by_band={band:evaluate(sets) for band,sets in bands.items()}
    red,blue=[fits_by_band[b]["angle"] for b in ("red","blue")]
    rows.append({"star":star,"fits":fits_by_band,
                 "chromaticAngleDifference":axial(red,blue) if red is not None and blue is not None else None,
                 "phaseInParityGrid":phases[star]})
chromatic=[row["chromaticAngleDifference"] for row in rows if row["chromaticAngleDifference"] is not None]
summary={"stars":len(rows),"posesPerHalf":[len(m) for m in half_members],
         "qualified":{band:sum(r["fits"][band]["qualified"] for r in rows) for band in ("red","blue")},
         "evaluatedFolds":{band:sum(fold["status"]=="EVALUATED" for row in rows
                                   for fold in row["fits"][band]["folds"]) for band in ("red","blue")},
         "gainPassesBothFolds":{band:sum(all(fold["status"]=="EVALUATED" and fold["heldOutGain"]>=p["minGain"]
                                           for fold in row["fits"][band]["folds"]) for row in rows)
                               for band in ("red","blue")},
         "chromaticComparable":len(chromatic),"chromaticWithin15":sum(a<=15 for a in chromatic)}
r={"schema":"BKL046_M8M20_PSF_DISJOINT_EXPOSURES_V1","protocolSha256":sha256(raw).hexdigest(),
   "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),"summary":summary,"rows":rows,
   "nativeExecutions":0,"scientificClosures":0}
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps(summary,sort_keys=True))
