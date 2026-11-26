from argparse import ArgumentParser
import ast
import base64
from hashlib import sha256
from io import BytesIO
from itertools import product
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

parser=ArgumentParser()
for name in ("protocol","fixture","classifier","packages","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np
from astropy.io import fits


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def pin(path,expected):
    data=path.read_bytes()
    require(sha(data)==expected,f"Changed {path.name}")
    return data


PIN="8a051f79801e562a1e804b60e5bb684cf436c195499ebfef1d8664264a9a059f"
plan=json.loads(pin(args.protocol,PIN))
receipt=json.loads(pin(args.fixture/"riscontro.json",plan["fixture"]))
require(receipt["settings"]["dropShrink"]==.7 and receipt["settings"]["scale"]==1,"Changed frozen geometry")
SHAPE=(3,28,32)
TOLERANCE=1e-6
SUPPORT=1e-8
ARMS=("unmasked","mask-green","mask-wrong-channel","zero-detector","zero-reference")
sources={"classify_map","classify_set","transformed","profiled_models","classify_scale"}
nodes=[n for n in ast.parse(pin(args.classifier,plan["classifier"])).body
       if isinstance(n,ast.FunctionDef) and n.name in sources]
require({n.name for n in nodes}==sources,"Changed classifier source")
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(args.classifier),"exec"))
require([a["id"] for a in receipt["arms"]]==list(ARMS),"Changed control roster")
ns={"x":"http://www.pixinsight.com/xdrz"}


def fixture(name):
    return pin(args.fixture/name,receipt["outputs"][name])


def image(name):
    with fits.open(BytesIO(fixture(name)),memmap=False) as hdus:
        require(len(hdus)==1 and np.isfinite(hdus[0].data).all(),"Invalid synthetic FITS")
        return hdus[0].data.astype(float)


def placement(xml,expected_file):
    root=ET.fromstring(fixture(xml))
    cfa=root.find("x:CFASourceImage",ns)
    require(Path(cfa.text).name==expected_file and cfa.get("pattern")=="RGGB","Unexpected CFA input")
    require(root.find("x:AlignmentOrigin",ns).attrib=={"x":"0.0","y":"0.0"},"Changed fixture origin")
    matrix=np.array([float(v) for v in root.findtext("x:AlignmentMatrix",namespaces=ns).split(",")]).reshape(3,3)
    require(np.array_equal(matrix[:2,:2],np.eye(2)) and np.array_equal(matrix[2],[0,0,1])
            and np.array_equal(matrix[:2,2],np.rint(matrix[:2,2])),"Unexpected noninteger placement")
    shift=np.rint(matrix[:2,2]).astype(int)
    coordinates=root.findall("x:RejectionMap/x:ChannelData",ns)
    mask=(np.array([np.frombuffer(base64.b64decode(p.text,validate=True),dtype=np.uint8)
                    for p in coordinates]).reshape(SHAPE) if coordinates else np.zeros(SHAPE,dtype=np.uint8))
    require(np.isin(mask,[0,4]).all(),"Unexpected rejection flag")
    return shift,mask


arms={row["id"]:[(image(cfa),*placement(xml,cfa)) for xml,cfa in zip(row["xdrz"],row["cfa"],strict=True)]
      for row in receipt["arms"]}
yy,xx=np.indices(SHAPE[1:])
colors=(xx%2+yy%2).ravel()


def integrate(arm,width,coordinates,zero_behaviour):
    sums=np.zeros(SHAPE)
    weights=np.zeros(SHAPE)
    for mosaic,shift,mask in arms[arm]:
        require(mosaic.shape==SHAPE[1:],"Unexpected mosaic dimensions")
        x,y=xx.ravel()-shift[0],yy.ravel()-shift[1]
        sample=mosaic.ravel()
        for dx,dy in product((-1,0,1),repeat=2):
            u,v=x+dx,y+dy
            # Integer placement maps the square to the exact detector center.
            def overlap(step):
                return max(0.,min(width/2,step+.5)-max(-width/2,step-.5))
            coefficient=overlap(dx)*overlap(dy)/width**2
            if coefficient==0:
                continue
            inside=(u>=0)&(u<SHAPE[2])&(v>=0)&(v<SHAPE[1])
            ids=np.flatnonzero(inside)
            mx,my=(xx.ravel()[ids],yy.ravel()[ids]) if coordinates=="detector" else (u[ids],v[ids])
            keep=mask[colors[ids],my,mx]==0
            if zero_behaviour=="exclude":
                keep&=sample[ids]!=0
            ids=ids[keep]
            index=(colors[ids],v[ids],u[ids])
            np.add.at(weights,index,coefficient)
            np.add.at(sums,index,sample[ids]*coefficient)
    return np.divide(sums,weights,out=np.zeros_like(sums),where=weights>0),weights


names=("unmasked","detector","reference","zero-detector-retained","zero-reference-retained")
maps=[]
comparisons=[]
for width in plan["widths"]:
    models={"unmasked":integrate("unmasked",width,"detector","retain"),
            "detector":integrate("mask-green",width,"detector","retain"),
            "reference":integrate("mask-green",width,"reference","retain"),
            "zero-detector-retained":integrate("zero-detector",width,"detector","retain"),
            "zero-reference-retained":integrate("zero-reference",width,"reference","retain")}
    for name in ("unmasked","detector","reference"):
        v,w=models[name]
        np.testing.assert_allclose(w,image(f"{name}-expected-weight.fits"),atol=plan["weightTolerance"],rtol=0)
        np.testing.assert_allclose(v[w>0],image(f"{name}-expected-rgb.fits")[w>0],atol=plan["intensityTolerance"],rtol=0)
    for label in plan["placements"]:
        v,w=models[f"zero-{label}-retained"]
        np.testing.assert_allclose(v[w>0],image(f"zero-{label}-retained-expected-rgb.fits")[w>0],
                                   atol=plan["intensityTolerance"],rtol=0)
    maps.append(np.asarray([models[name] for name in names]))
    for placement_name,behavior,profile in product(plan["placements"],plan["zeroModes"],plan["scales"]):
        pairs={}
        for arm in ARMS:
            v,w=integrate(arm,width,placement_name,behavior if arm.startswith("zero-") else "retain")
            pairs[arm]=(v,transformed(w,profile))
        verdict=classify_scale(pairs,models)
        scope=verdict["profileResults"][profile]
        require(verdict["scaleStatus"]=="UNIQUE_PROFILE" and verdict["weightProfile"]==profile
                and scope["greenMaskCoordinateModel"]==placement_name
                and scope["status"]==("ZERO_WEIGHT_RETAINED" if behavior=="retain" else "ZERO_SAMPLE_EXCLUDED"),
                "Two-width discrimination failed")
        comparisons.append(dict(width=width,scale=profile,rejectionCoordinates=placement_name,zeroBehavior=behavior))
np.testing.assert_allclose(maps[0],maps[1],rtol=0,atol=1e-14)
meta=dict(schema=plan["schema"],protocolSha256=PIN,widths=plan["widths"],models=names,
          axes=["width","model","intensity_or_weight","channel","y","x"],
          channels=["R","G","B"],nativeProvenanceVerified=False)
out=args.output/"oracoli.zip"
with ZipFile(out,"x") as archive:
    stream=BytesIO()
    np.save(stream,np.asarray(maps),allow_pickle=False)
    archive.writestr(ZipInfo("oracoli.npy",(2026,1,1,0,0,0)),stream.getvalue(),ZIP_DEFLATED)
    archive.writestr(ZipInfo("manifest.json",(2026,1,1,0,0,0)),
                     json.dumps(meta,indent=2,sort_keys=True)+"\n",ZIP_DEFLATED)
with ZipFile(out) as archive:
    np.testing.assert_array_equal(np.load(BytesIO(archive.read("oracoli.npy")),allow_pickle=False),maps)
report=dict(meta,fixtureSha256=plan["fixture"],oracleSha256=sha(out.read_bytes()),
            archivedPredictionsReproduced=True,numericalCases=len(comparisons),
            cases=comparisons,maximumDifferenceBetweenWidths=float(np.max(np.abs(maps[0]-maps[1]))),
            launcherModified=False,admissionRequested=False,nativeExecutions=0,scientificClosures=0)
with (args.output/"riscontro.json").open("x",encoding="utf8",newline="\n") as f:
    json.dump(report,f,indent=2,sort_keys=True,allow_nan=False)
    f.write("\n")
