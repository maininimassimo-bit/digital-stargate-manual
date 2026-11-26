from argparse import ArgumentParser
import ast
from hashlib import sha256
from io import BytesIO
from itertools import combinations,product
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

parser=ArgumentParser()
for name in ("protocol","fixture","math","packages","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np
from astropy.io import fits


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def digest(data):
    return sha256(data).hexdigest()


def pin(path,expected):
    data=path.read_bytes()
    require(digest(data)==expected,f"Changed {path.name}")
    return data


PIN="f9b1f8b40c5f5804fd1bb5ed1dcf5ad37d7aa0989e498197413557aaa1a9a5fe"
plan=json.loads(pin(args.protocol,PIN))
fixture=json.loads(pin(args.fixture/"riscontro.json",plan["fixture"]))
arm=next(a for a in fixture["arms"] if a["id"]=="unmasked")
w,h=plan["sizeXY"]
y,x=np.indices((h,w))
coords=np.column_stack((x.ravel(),y.ravel()))
parity=(2*(y%2)+x%2).ravel()
r=max(w,h)//2
points=np.arange(-r,r+1)

funcs={"clip_batch","intersections","resample"}
nodes=[n for n in ast.parse(pin(args.math,plan["math"])).body if isinstance(n,ast.FunctionDef) and n.name in funcs]
require({n.name for n in nodes}==funcs,"Changed polygon kernel")
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(args.math),"exec"))
ns="http://www.pixinsight.com/xdrz"
ET.register_namespace("",ns)
ET.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")


def q(name):
    return f"{{{ns}}}{name}"


def input_bytes(name):
    return pin(args.fixture/name,fixture["outputs"][name])


inputs={}
exposures=[]
for i,(xml,cfa) in enumerate(zip(arm["xdrz"],arm["cfa"],strict=True)):
    root=ET.fromstring(input_bytes(xml))
    name=Path(root.find(q("SourceImage")).text).name
    mosaic=Path(root.find(q("CFASourceImage")).text).name
    require(mosaic==cfa and root.find(q("RejectionMap")) is None,"Changed source layout")
    node=root.find(q("AlignmentMatrix"))
    matrix=np.array([float(s) for s in node.text.split(",")]).reshape(3,3)
    require(np.array_equal(matrix[:2,:2],np.eye(2)) and np.array_equal(matrix[2],[0,0,1]),
            "Fixture requires a pure translation")
    if i==1:
        matrix[:2,2]=plan["fractionalBTranslation"]
        node.text=",".join(format(v,".17g") for v in matrix.ravel())
    require(root.find(q("AlignmentOrigin")).attrib=={"x":"0.0","y":"0.0"} and
            root.find(q("CFASourceImage")).get("pattern")=="RGGB","Unexpected fixture origin or phase")
    root.find(q("SourceImage")).text=plan["fixtureRoot"]+name
    root.find(q("CFASourceImage")).text=plan["fixtureRoot"]+mosaic
    inputs[xml]=ET.tostring(root,encoding="utf8",xml_declaration=True)+b"\n"
    inputs[name]=input_bytes(name)
    inputs[mosaic]=input_bytes(mosaic)
    with fits.open(BytesIO(inputs[mosaic]),memmap=False) as entries:
        require(len(entries)==1 and entries[0].data.shape==(h,w) and np.isfinite(entries[0].data).all(),
                "Unexpected CFA shape")
        exposures.append((entries[0].data.astype(float).ravel(),matrix))


def direct(flux,inverse,width):
    dest=coords+inverse[:2,2]
    nearest=np.rint(dest).astype(int)
    weight=np.zeros((4,h,w))
    value=np.zeros_like(weight)
    for dx,dy in product((-1,0,1),repeat=2):
        positions=nearest+np.array([dx,dy])
        separation=positions-dest
        half=width/2
        left=np.maximum(-half,separation-.5)
        right=np.minimum(half,separation+.5)
        coefficients=np.maximum(0,right-left).prod(axis=1)/width**2
        u,v=positions.T
        yes=(u>=0)&(v>=0)&(u<w)&(v<h)&(coefficients>0)
        dest_idx=(parity[yes],v[yes],u[yes])
        np.add.at(weight,dest_idx,coefficients[yes])
        np.add.at(value,dest_idx,coefficients[yes]*flux[yes])
    return np.stack((weight,value),axis=1)


def rgb(planes):
    return np.stack((planes[0],planes[1]+planes[2],planes[3]))


def encode_fixture(arr):
    stream=BytesIO()
    fits.PrimaryHDU(arr.astype(np.float32)).writeto(stream)
    return fits.getdata(BytesIO(stream.getvalue())).astype(float)


models={}
numerical_differences=[]
for width in plan["widths"]:
    independent=np.zeros((4,2,h,w))
    polygon=np.zeros_like(independent)
    for flux,forward in exposures:
        inverse=np.linalg.inv(forward)
        independent+=direct(flux,inverse,width)
        poly=resample(coords,parity,np.vstack([flux,flux]),inverse,width,np.array([r,r]))
        polygon+=poly[:,:2,:h,:w]
    np.testing.assert_allclose(polygon,independent,atol=2e-13,rtol=0)
    numerical_differences.append(float(np.max(np.abs(polygon-independent))))
    integrated=rgb(independent)
    weight=integrated[:,0]
    support=weight>1e-8
    value=np.divide(integrated[:,1],weight,out=np.zeros_like(weight),where=support)
    profile_maps=dict(raw=weight,globalMax=weight/weight.max(),
                      channelMax=weight/weight.max(axis=(1,2))[:,None,None])
    for profile in plan["profiles"]:
        models[width,profile]=(value,profile_maps[profile],support)

gaps=[float(np.max(np.abs(wa-wb)))
      for (a,(_,wa,_)),(b,(_,wb,_)) in combinations(models.items(),2) if a[0]!=b[0]]
require(min(gaps)>=plan["minimumWrongWidthMapGap"],"Width profiles not separated by frozen margin")
test=[]
for (width,profile),(value,weight,support) in models.items():
    observed_i,observed_w=encode_fixture(value),encode_fixture(weight)
    matches=[(w,p) for (w,p),(v,predicted,s) in models.items()
             if np.array_equal(observed_w>1e-8,s)
             and np.max(np.abs(observed_w-predicted))<=plan["weightTolerance"]
             and np.max(np.abs(observed_i[s]-v[s]))<=plan["intensityTolerance"]]
    require(matches==[(width,profile)],"FITS evidence did not distinguish width and profile")
    test.append(dict(width=width,profile=profile,uniqueMatch=True))
oracles=np.stack([np.stack((i,w)) for i,w,_ in models.values()])
stream=BytesIO()
np.save(stream,oracles,allow_pickle=False)
inputs["predictions.npy"]=stream.getvalue()
meta=dict(schema=plan["schema"],protocolSha256=PIN,
          modelOrder=[dict(width=w,profile=p) for w,p in models],
          sourceFiles={name:digest(raw) for name,raw in sorted(inputs.items())},nativeExecutions=0)
inputs["manifest.json"]=(json.dumps(meta,indent=2,sort_keys=True)+"\n").encode()
package=args.output/"testimone.zip"
with ZipFile(package,"x") as archive:
    for name,raw in sorted(inputs.items()):
        archive.writestr(ZipInfo(name,(2026,1,1,0,0,0)),raw,ZIP_DEFLATED)
with ZipFile(package) as archive:
    require(archive.testzip() is None and all(archive.read(n)==v for n,v in inputs.items()),"ZIP differs")
report=dict(meta,archiveSha256=digest(package.read_bytes()),minimumWrongWidthMapGap=min(gaps),
            directVsPolygonMaximumError=max(numerical_differences),floatingFitsChecks=test,
            nativeProvenanceVerified=False,admissionRequested=False,scientificClosures=0)
with (args.output/"riscontro.json").open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
    out.write("\n")
