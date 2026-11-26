from argparse import ArgumentParser
import ast
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import sys

parser=ArgumentParser()
for key in ("study","capture","matcher","rawpy_packages","packages","vc","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()
dlls=[os.add_dll_directory(str(args.rawpy_packages/"rawpy")),os.add_dll_directory(str(args.vc))]
sys.path[:0]=[str(args.rawpy_packages),str(args.packages)]
import numpy as np
import rawpy
from astropy.io.votable import parse
from collections import defaultdict
from itertools import combinations,product

PIN="696279246de9c5e66797c69f01119c7172573ecb971d8a773989d36d63015795"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, expected):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==expected,"Changed source "+path.name)
    return raw


plan=json.loads(pinned(args.study/"protocollo.json",PIN))
stars_plan=json.loads(pinned(args.matcher/"protocollo.json",plan["sourceMatcherPlanSha256"]))
source=ast.parse(pinned(args.matcher/"misura.py",plan["sourceMatcherSha256"]))
wanted={"stars","distances","triangles","similarity","pairs","seed"}
functions=[node for node in source.body if isinstance(node,ast.FunctionDef) and node.name in wanted]
require(len(functions)==len(wanted),"Matcher functions changed")
matcher_config=dict(stars_plan,trainGatesBinned=plan["plateRefineGatesBinned"])
center=np.array(stars_plan["detectorShapeYX"][::-1])/4
env=dict(np=np, center=center, plan=matcher_config,require=require,defaultdict=defaultdict,
         combinations=combinations,product=product)
exec(compile(ast.Module(body=functions,type_ignores=[]),"pinned-matcher","exec"),env)
stars,distances,similarity,pairs,seed=(env[name] for name in ("stars","distances","similarity","pairs","seed"))
require(np.__version__=="2.3.5" and rawpy.__version__=="0.25.1" and rawpy.libraw_version==(0,21,4),
        "Unexpected runtime")

votable=parse(BytesIO(pinned(args.study/"gavo.vot",plan["gavoSha256"])))
statuses=[item.value for resource in votable.resources for item in resource.infos if item.name=="QUERY_STATUS"]
require(statuses==["OK"],"TAP query did not complete")
catalog=votable.get_first_table().to_table()
require(len(catalog)==len(set(map(int,catalog["source_id"])))==579,"Unexpected Gaia cohort")
id_values=np.asarray(catalog["source_id"],dtype=np.int64)
ra,dec=np.deg2rad(np.asarray(catalog["ra"],dtype=float)),np.deg2rad(np.asarray(catalog["dec"],dtype=float))
time=plan["captureJulianYear"]-plan["catalogEpoch"]
dpm=np.pi/(180*3600*1000)*time
ra+=np.asarray(catalog["pmra"],dtype=float)/np.cos(dec)*dpm
dec+=np.asarray(catalog["pmdec"],dtype=float)*dpm
origin_ra,origin_dec=np.deg2rad([plan["raDeg"],plan["decDeg"]])
d_ra=ra-origin_ra
den=np.sin(origin_dec)*np.sin(dec)+np.cos(origin_dec)*np.cos(dec)*np.cos(d_ra)
require((den>0).all(),"Invalid gnomonic projection")
xi=np.cos(dec)*np.sin(d_ra)/den
eta=(np.cos(origin_dec)*np.sin(dec)-np.sin(origin_dec)*np.cos(dec)*np.cos(d_ra))/den
sky=np.column_stack((xi,eta))*(180*3600/np.pi)/(2*plan["arcsecPerNativePixel"])
require(np.isfinite(sky).all() and np.linalg.norm(sky,axis=1).max()<plan["radiusDeg"]*3600/(2*plan["arcsecPerNativePixel"])+3,
        "Unexpected selection radius")
split=np.sum(np.floor(sky/plan["holdoutTileBinned"]).astype(int),axis=1)%2==0


def fit_plate(observed):
    hypotheses=[]
    for sign in (-1,1):
        ref=sky*np.array((sign,1))
        result=seed(ref[split],observed)
        if result:
            hypotheses.append((sign,ref,result))
    if not hypotheses:
        return {"status":"NO_CATALOG_TRANSFORM"},{}
    sign,ref,(_,_,matrix,shift)=min(hypotheses,key=lambda item:(-item[2][0],item[2][1]))
    training=ref[split]
    for gate in plan["plateRefineGatesBinned"]:
        ii,jj,_=pairs(training,observed,matrix,shift,gate)
        if len(ii)<24:
            return dict(status="INSUFFICIENT_GAIA_TRAINING", count=len(ii)),{}
        matrix,shift=similarity(training[ii],observed[jj])
    designs=np.column_stack((training[ii],np.ones(len(ii))))
    affine,_,rank,_=np.linalg.lstsq(designs,observed[jj],rcond=None)
    require(rank==3,"Degenerate plate training")
    all_hold=ref[~split]
    predicted=all_hold@affine[:2]+affine[2]
    available=observed[~np.isin(np.arange(len(observed)),jj)]
    assert len(available)>2
    i,j,res=pairs(all_hold,available,affine[:2],affine[2],plan["maxGaiaMatchBinned"])
    next_best=np.partition(distances(predicted[i],available),1,axis=1)[:,1]
    accepted=next_best>=plan["minAlternativeBinned"]**2
    i,j,res=i[accepted],j[accepted],res[accepted]
    if len(i)<plan["minimumHoldout"]:
        return dict(status="INSUFFICIENT_GAIA_HOLDOUT",training=len(ii),heldout=len(i)),{}
    ids=id_values[~split][i]
    positions={int(k):p for k,p in zip(ids,available[j],strict=True)}
    train_ids=id_values[split][ii]
    train_positions={int(k):p for k,p in zip(train_ids,observed[jj],strict=True)}
    return dict(status="MATCHED_GAIA_IDENTITIES", training=len(ii),heldout=len(i),handedness=sign,
                heldoutP90NativePx=float(np.quantile(res*2,.9)),heldoutIds=[int(k) for k in ids],
                plateScaleArcsecPerNativePixel=float(plan["arcsecPerNativePixel"]/np.linalg.norm(matrix[0])),
                projectionOriginNativeXY=((shift+center)*2).tolist()), dict(train=train_positions,test=positions)


def compare(a,b):
    if not a or not b:
        return dict(status="UNRESOLVED_CATALOG_LINK")
    train=sorted(set(a["train"]).intersection(b["train"]))
    test=sorted(set(a["test"]).intersection(b["test"]))
    if len(train)<20 or len(test)<plan["minimumHoldout"]:
        return dict(status="INSUFFICIENT_SHARED_IDENTITIES",training=len(train),heldout=len(test))
    xtr,ytr=(np.asarray([side["train"][key] for key in train]) for side in (a,b))
    xte,yte=(np.asarray([side["test"][key] for key in test]) for side in (a,b))
    matrix,shift=similarity(xtr,ytr)
    translation=np.median(ytr-xtr,axis=0)
    diag={name:float(np.quantile(2*np.linalg.norm(pred-yte,axis=1),.9)) for name,pred in
          (("translation",xte+translation),("similarity",xte@matrix+shift))}
    return dict(status="COMMON_GAIA_IDENTITIES",training=len(train),heldout=len(test),
                heldoutP90NativePx=diag,heldoutIds=test,
                angleDegrees=float(np.degrees(np.arctan2(matrix[0,1],matrix[0,0]))))


originals=args.capture/"originali"
receipt=json.loads(pinned(originals/"acquisizione.json",plan["acquisitionSha256"]))
rows,contexts=[],[]
for sample in receipt["samples"]:
    with rawpy.imread(BytesIO(pinned(originals/sample["file"],sample["sha256"]))) as frame:
        observed=stars(frame.raw_image_visible,frame.white_level)
    evaluated,positions=fit_plate(observed)
    rows.append(dict(sha256=sample["sha256"],plate=evaluated))
    contexts.append(positions)
report=dict(schema=plan["schema"],protocolSha256=PIN,viewerReferenceCount=len(catalog),frames=rows,
            relativeToFirst=[compare(contexts[0],other) for other in contexts[1:]],
            independentCatalog="Gaia DR3 via GAVO",nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
