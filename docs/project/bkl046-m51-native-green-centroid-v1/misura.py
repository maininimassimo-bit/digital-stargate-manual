from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser = ArgumentParser()
for arg in ("protocol", "gaia", "capture", "matcher", "rawpy", "dependencies", "vc", "output"):
    parser.add_argument(arg, type=Path)
args = parser.parse_args()


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def exact(path, digest):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == digest, f"Changed {path.name}")
    return raw


PIN = "15cfc52b25a3f191df49bbff720adc0a6dc22aa3ba67ab4c5f98677a3b7acb95"
config = json.loads(exact(args.protocol, PIN))
parent_raw = exact(args.gaia / "misura.py", config["gaiaProgramSha256"])
prior_raw = exact(args.gaia / "riscontro.json", config["gaiaReportSha256"])
with TemporaryDirectory(prefix="gaia-reference-", dir=args.output.parent) as temp:
    require(Path(temp).resolve().parent == args.output.parent.resolve(), "Invalid staging directory")
    prior_copy = Path(temp) / "replay.json"
    saved = sys.argv
    try:
        sys.argv = [str(args.gaia / "misura.py"), *map(str, (args.gaia, args.capture, args.matcher,
                                    args.rawpy, args.dependencies, args.vc, prior_copy))]
        environment = {"__name__": "__main__"}
        exec(compile(parent_raw, str(args.gaia / "misura.py"), "exec"), environment)
    finally:
        sys.argv = saved
    require(prior_copy.read_bytes() == prior_raw, "The Gaia association replay changed")

import numpy as np
import rawpy

receipt, contexts = environment["receipt"],environment["contexts"]
center, similarity = environment["center"],environment["similarity"]
rad, fit_rad = config["radiusPx"],config["fitRadiusPx"]
ry,rx = np.mgrid[-rad:rad+1,-rad:rad+1]
r2 = rx*rx+ry*ry
core, annulus = r2<=fit_rad**2,(r2>=(rad-3)**2)&(r2<=rad**2)


def samples(data, seed, white):
    x,y = np.rint(seed).astype(int)
    patch = data[y-rad:y+rad+1,x-rad:x+rad+1]
    if patch.shape != rx.shape:
        return None, "edge"
    observations = []
    for oy,ox in ((0,1),(1,0)):
        green = ((y+ry)%2==oy)&((x+rx)%2==ox)
        background = patch[green&annulus].astype(float)
        med = np.median(background)
        sigma = max(1.,1.4826*np.median(np.abs(background-med)))
        where = core & green
        values = patch[where].astype(float)
        if values.max()>=white-config["adcGuardBelowWhite"]:
            return None, "saturation"
        signal = values-med
        good = signal>=max(sigma*config["minimumNoiseMultiple"], config["minimumPeakFraction"]*signal.max())
        if good.sum()<config["minimumSameParitySamples"]:
            return None, "weak"
        observations.append((rx[where][good],ry[where][good],signal[good]))
    return ((x,y),observations), None


def fitted(origin, seed, observations):
    u,v,intensity = (np.concatenate(items) for items in zip(*observations, strict=True))
    labels = np.concatenate([np.full(len(values), i) for i, (_,_,values) in enumerate(observations)])
    design = [np.ones(len(u)),u,v,u*u,u*v,v*v]
    if len(observations)>1:
        design.append(labels)
    weights=np.sqrt(intensity/intensity.max())
    coeff,_,rank,_=np.linalg.lstsq(np.column_stack(design)*weights[:,None],np.log(intensity)*weights,rcond=None)
    if rank!=len(design):
        return None
    hessian=np.array(((2*coeff[3],coeff[4]),(coeff[4],2*coeff[5])))
    limits=np.linalg.eigvalsh(-hessian)
    if limits[0]<1/config["maximumSigmaPx"]**2 or limits[1]>1/config["minimumSigmaPx"]**2:
        return None
    xy=np.asarray(origin)-np.linalg.solve(hessian,coeff[1:3])
    return xy if np.linalg.norm(xy-seed)<=config["maxMovePx"] else None


def measure(data, white, detections):
    positions = {}
    rejected = Counter()
    for group in ("train","test"):
        positions[group] = {}
        for key, xy in detections[group].items():
            seed = (xy+center)*2+.5
            values,reason=samples(data,seed,white)
            if reason:
                rejected[reason]+=1
                continue
            origin,obs=values
            solutions=[fitted(origin,seed,selection) for selection in ([obs[0]],[obs[1]],obs)]
            if any(value is None for value in solutions):
                rejected["fit_or_center_rejected"]+=1
                continue
            positions[group][key]=dict(zip(config["methods"],(seed,*solutions),strict=True))
    return positions,dict(sorted(rejected.items()))


def compare(reference, target):
    selection={k: sorted(set(reference[k]).intersection(target[k])) for k in ("train","test")}
    primary=dict(training=len(selection["train"]),heldout=len(selection["test"]))
    if primary["training"]<config["minimumCommonTrain"] or primary["heldout"]<config["minimumCommonHoldout"]:
        return dict(status="INSUFFICIENT_COMMON_SAMPLE",**primary)
    result={}
    for method in config["methods"]:
        tx,ty,hx,hy=(np.asarray([points[group][j][method] for j in selection[group]])
                     for group in ("train","test") for points in (reference,target))
        matrix,vector=similarity(tx,ty)
        coef,_,rank,_=np.linalg.lstsq(np.column_stack((tx,np.ones(len(tx)))),ty,rcond=None)
        require(rank==3,"Degenerate affine geometry")
        result[method]={}
        for name,pred in (("similarity",hx@matrix+vector),("affine",hx@coef[:2]+coef[2])):
            err=np.linalg.norm(pred-hy,axis=1)
            result[method][name]=dict(medianPx=float(np.median(err)),p90Px=float(np.quantile(err,.9)))
    return dict(status="COMMON_FIT_SAMPLE",**primary,heldoutIds=selection["test"],metrics=result)


iy,ix=np.indices((43,43))
known=np.array((21.29,20.86))
base=np.exp(-.5*((ix-known[0])**2/2.6**2+(iy-known[1])**2/2.0**2))
fixture=350.+np.where(iy%2==0,7000.,5100.)*base
controls, reason=samples(fixture,np.array((21.,21.)),16383)
require(reason is None,"Synthetic star returned insufficient support")
origin,obs=controls
require(all(np.linalg.norm(fitted(origin,np.array((21.,21.)),selection)-known)<.04
            for selection in ([obs[0]],[obs[1]],obs)),"Synthetic centroid drift")
outputs,scores=[],[]
for item, previous in zip(receipt["samples"],contexts,strict=True):
    raw=exact(args.capture/"originali"/item["file"],item["sha256"])
    with rawpy.imread(BytesIO(raw)) as frame:
        fitted_points,rejected=measure(frame.raw_image_visible,frame.white_level,previous)
    outputs.append(fitted_points)
    separate=[np.linalg.norm(point["G1"]-point["G2"]) for point in fitted_points["test"].values()]
    scores.append(dict(sha256=item["sha256"],trainAccepted=len(fitted_points["train"]),
                       heldoutAccepted=len(fitted_points["test"]),rejectReasons=rejected,
                       twoGreensHeldoutP90Px=float(np.quantile(separate,.9)) if separate else None))
report=dict(schema=config["schema"],protocolSha256=PIN,currentGaiaReplayExact=True,frames=scores,
            relativeToFirst=[compare(outputs[0],other) for other in outputs[1:]],
            scientificClosures=0,nativeExecutions=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
