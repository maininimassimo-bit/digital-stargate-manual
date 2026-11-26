"""Check repeatability of elliptical PSF orientation on historical M8/M20 holdouts."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, archive, dependencies, out = map(Path,sys.argv[1:])
raw=protocol.read_bytes()
p=json.loads(raw)
sys.path.insert(0,str(dependencies))
import numpy as np
assert np.__version__=="2.3.5"

def read(name,pin):
    data=(archive/name).read_bytes()
    if sha256(data).hexdigest()!=pin:
        raise ValueError("SOURCE_CHANGED:"+name)
    return json.loads(data)

previous=read("riscontro-verificato.json",p["priorSha256"])
stamps=read("stamps.json",p["stampsSha256"])
assert previous["inputSha256"]["stamps"] == p["stampsSha256"]
heldout=sorted({row["id"] for row in previous["injections"]})
by_id={row["id"]:row["stamp"] for row in stamps["rows"] if row.get("stamp")}
assert len(heldout)==p["expectedHeldOut"]==previous["heldout"] and set(heldout)<=by_id.keys()
beta=p["beta"]
angles=list(range(0,180,p["angleStepDegrees"]))
shapes=[(1.,0)] + [(q,theta) for q in p["axisRatios"] if q!=1 for theta in angles]

def library(x,y,fwhm):
    alpha=fwhm/(2*np.sqrt(2**(1/beta)-1))
    model=[]
    for q, angle in shapes:
        t=np.deg2rad(angle)
        c,s=np.cos(t),np.sin(t)
        raster=np.zeros(len(x))
        for dy in (-1/3,0.,1/3):
            for dx in (-1/3,0.,1/3):
                u,v=(x+dx)*c+(y+dy)*s,-(x+dx)*s+(y+dy)*c
                raster+=(1+(q*u*u+v*v/q)/alpha**2)**(-beta)
        model.append(raster/9)
    return np.stack(model,axis=1)

def axial(left,right):
    return abs((left-right+90)%180-90)

def fold(lib, background, observed, train):
    train_bg=background[train]
    target=observed[train]
    # Fit each profile together with the unchanged nuisance plane.
    scores=[]
    for i in range(lib.shape[1]):
        model=np.column_stack((lib[:,i],background))
        weights,_,rank,_=np.linalg.lstsq(model[train],target,rcond=None)
        if rank!=4 or weights[0]<=0:
            scores.append(None)
            continue
        residual=observed-model@weights
        scores.append((float(residual[train]@residual[train]),float(residual[~train]@residual[~train])))
    if scores[0] is None or not any(s is not None for s in scores[1:]):
        return {"status":"UNQUALIFIED"}
    best=min((i for i,s in enumerate(scores) if s is not None),key=lambda k:scores[k][0])
    circular=scores[0][1]
    gain=(circular-scores[best][1])/circular if circular>0 else 0.
    return {"status":"EVALUATED","ratio":shapes[best][0],"angle":shapes[best][1],
            "heldOutRelativeImprovement":gain}

def decide(lib, background, observed, select):
    folds=[fold(lib,background,observed,part) for part in (select,~select)]
    eligible=all(row["status"]=="EVALUATED"
                 and row["ratio"]<=p["maxAcceptedRatio"]
                 and row["heldOutRelativeImprovement"]>=p["minimumHeldOutImprovement"] for row in folds)
    qualified=eligible and axial(folds[0]["angle"],folds[1]["angle"])<=p["maxAngularDifferenceDegrees"]
    estimate=None
    if qualified:
        angles_rad=np.deg2rad([2*f["angle"] for f in folds])
        estimate=float(np.rad2deg(np.angle(np.exp(1j*angles_rad).sum()))/2%180)
    return {"qualified":qualified,"angle":estimate,"folds":folds}

x,y=np.meshgrid(np.arange(-8,9,dtype=float),np.arange(-8,9,dtype=float))
usable=x*x+y*y<=p["fitRadius"]**2
x,y=x[usable],y[usable]
train=(x.astype(int)+y.astype(int))%2==0
bg=np.column_stack((np.ones(len(x)),x/10,y/10))
lib=library(x,y,3.)
expected=shapes.index((.65,45))
solid=bg@np.array([30.,.2,-.1])
assert not decide(lib,bg,solid+10*lib[:,0],train)["qualified"]
toy=decide(lib,bg,solid+10*lib[:,expected],train)
assert toy["qualified"] and axial(toy["angle"],45)<1e-8
assert axial(179,1)==2

rows=[]
for label in heldout:
    stamp=by_id[label]
    u,v=np.meshgrid(np.asarray(stamp["grid"],dtype=float),np.asarray(stamp["grid"],dtype=float))
    xx,yy=u-stamp["centerOffset"][0],v-stamp["centerOffset"][1]
    mask=np.array(stamp["support"],dtype=bool)&(xx**2+yy**2<=p["fitRadius"]**2)
    select=(u[mask].astype(int)+v[mask].astype(int))%2==0
    assert min(int(select.sum()),int((~select).sum()))>=30
    xx,yy=xx[mask],yy[mask]
    background=np.column_stack((np.ones(len(xx)),xx/10,yy/10))
    frames=np.asarray(stamp["imageRBA_B"])
    assert frames.shape==(2,2,29,29)
    fits={}
    for i,band in enumerate(("red","blue")):
        models=library(xx,yy,previous["fwhmNativePxRedBlue"][i])
        fits[band]={cal:decide(models,background,frames[i,j][mask],select) for j,cal in enumerate(("A","B"))}
    comparisons={}
    candidates={"redAB":(fits["red"]["A"],fits["red"]["B"]),
                "blueAB":(fits["blue"]["A"],fits["blue"]["B"]),
                "redBlueA":(fits["red"]["A"],fits["blue"]["A"]),
                "redBlueB":(fits["red"]["B"],fits["blue"]["B"])}
    for key,(one,two) in candidates.items():
        comparisons[key]=axial(one["angle"],two["angle"]) if one["qualified"] and two["qualified"] else None
    rows.append({"star":label,"fits":fits,"crossAngleDegrees":comparisons})

summary={"stars":len(rows),
         "qualified":{band+cal:sum(r["fits"][band][cal]["qualified"] for r in rows)
                      for band in ("red","blue") for cal in ("A","B")},
         "comparisons":{}}
for key in rows[0]["crossAngleDegrees"]:
    angles_found=[r["crossAngleDegrees"][key] for r in rows if r["crossAngleDegrees"][key] is not None]
    summary["comparisons"][key]={"comparable":len(angles_found),
       "within15Degrees":sum(a<=15 for a in angles_found),
       "medianDegrees":float(np.median(angles_found)) if angles_found else None}
report={"schema":"BKL046_M8M20_PSF_ORIENTATION_TRANSFER_V1","protocolSha256":sha256(raw).hexdigest(),
        "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),"summary":summary,"rows":rows,
        "nativeExecutions":0,"scientificClosures":0}
with out.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps(summary,sort_keys=True))
