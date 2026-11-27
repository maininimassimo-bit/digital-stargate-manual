import ast
from hashlib import sha256
from io import BytesIO
from itertools import combinations
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

root, controls, comparison, deps, out = map(Path,sys.argv[1:])
sys.path.insert(0,str(deps))
import numpy as np
import astropy
from astropy.io import fits

def digest(raw):
    return sha256(raw).hexdigest()

def pinned(path, expected):
    raw=path.read_bytes()
    if digest(raw)!=expected:
        raise ValueError("input changed: "+path.name)
    return raw

def functions(raw, names):
    nodes=[n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    scope={"np":np}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"<pinned functions>","exec"),scope)
    return [scope[k] for k in names]

raw=(root/"protocollo.json").read_bytes()
pin=digest(raw)
assert pin=="99f551c87642c6d4248ecfc1dded553f5a21cfbb4687511a9fa182894e3c9eeb"
p=json.loads(raw)
assert (np.__version__,astropy.__version__)==("2.3.5","7.2.0")
fixture=controls/"fixture"
manifest=json.loads(pinned(fixture/"manifest.json",p["manifest"]))
clip, area=functions(pinned(controls/"genera.py",p["generator"]),("polygon_clip","polygon_area"))
matches,=functions(pinned(comparison,p["comparator"]),("matches",))

def read(name):
    return pinned(fixture/name,manifest["files"][name])

def data(name):
    with fits.open(BytesIO(read(name)),memmap=False) as hdus:
        assert len(hdus)==1
        return hdus[0].data.astype(float)

names=("unmasked","detector","reference","wrong-channel","shear")
oracles={n:tuple(data(f"{n}-expected-{k}.fits") for k in ("rgb","weight")) for n in names}

def difference(pair1,pair2):
    v1,w1=pair1
    v2,w2=pair2
    s1,s2=w1>1e-8,w2>1e-8
    common=s1&s2
    return {"differentSupportSamples":int(np.count_nonzero(s1!=s2)),
            "maxAbsWeight":float(np.max(np.abs(w1-w2))),
            "maxAbsIntensityOnCommonSupport":float(np.max(np.abs(v1[common]-v2[common]))),
            "acceptedByExactComparator":bool(matches(pair1,pair2))}

pairs=[]
for left,right in combinations(names[:-1],2):
    pairs.append({"left":left,"right":right,**difference(oracles[left],oracles[right])})
assert next(r["acceptedByExactComparator"] for r in pairs if (r["left"],r["right"])==("unmasked","wrong-channel"))
assert not next(r["acceptedByExactComparator"] for r in pairs if (r["left"],r["right"])==("detector","reference"))
roundtrip={n:difference(tuple(a.astype(np.float32).astype(float) for a in v),v) for n,v in oracles.items()}
assert all(v["acceptedByExactComparator"] for v in roundtrip.values())

def translation(x,y):
    return np.array([[1.,0.,x],[0.,1.,y],[0.,0.,1.]])

def source(label,variant):
    r=ET.fromstring(read(f"shear-{label}-{variant}.xdrz"))
    ns={"d":"http://www.pixinsight.com/xdrz"}
    orig=r.find("d:AlignmentOrigin",ns)
    sx,sy=[float(orig.attrib[k]) for k in ("x","y")]
    M=np.fromstring(r.find("d:AlignmentMatrix",ns).text,sep=",").reshape(3,3)
    cfa=r.find("d:CFASourceImage",ns)
    assert cfa.attrib["pattern"]==p["channels"]
    return M,(sx,sy),data(Path(cfa.text).name)

def render(sources,convert):
    weight=np.zeros((3,28,32))
    numerator=np.zeros_like(weight)
    drop=p["dropShrink"]
    corners=drop/2*np.array([[-1,-1],[1,-1],[1,1],[-1,1]])
    for M,(sx,sy),samples in sources:
        assert samples.shape==(28,32)
        inverse=np.linalg.inv(translation(-sx,-sy)@M@translation(sx,sy) if convert else M)
        A,b=inverse[:2,:2],inverse[:2,2]
        normalizer=drop**2*abs(np.linalg.det(A))
        for y,x in np.ndindex(samples.shape):
            channel=x%2+y%2
            polygon=(corners+[x,y])@A.T+b
            low=np.maximum(np.ceil(polygon.min(axis=0)-.5).astype(int),[0,0])
            high=np.minimum(np.floor(polygon.max(axis=0)+.5).astype(int),[31,27])
            for j in range(low[1],high[1]+1):
                for i in range(low[0],high[0]+1):
                    poly=[v-[i,j] for v in polygon]
                    for axis in (0,1):
                        poly=clip(poly,axis,-.5,1)
                        poly=clip(poly,axis,.5,-1)
                    w=area(poly)/normalizer
                    weight[channel,j,i]+=w
                    numerator[channel,j,i]+=w*samples[y,x]
    intensity=np.divide(numerator,weight,out=np.zeros_like(weight),where=weight>1e-12)
    return intensity,weight

geometry={}
for variant in p["shearVariants"]:
    sources=[source(label,variant) for label in "abc"]
    geometry[variant]={mode:difference(render(sources,convert),oracles["shear"])
                      for mode,convert in (("rawAsCenterZero",False),("normalizeSerializedOrigin",True))}
assert geometry["center0"]["rawAsCenterZero"]["acceptedByExactComparator"]
assert not geometry["edge05"]["rawAsCenterZero"]["acceptedByExactComparator"]
assert all(g["normalizeSerializedOrigin"]["acceptedByExactComparator"] for g in geometry.values())

r={"schema":"BKL046_CFA_FROZEN_ORACLE_MARGIN_V1","protocolSha256":pin,
   "programSha256":digest(Path(__file__).read_bytes()),"integerPairComparisons":pairs,
   "binary32Conversion":roundtrip,"shearAgainstFrozenOracle":geometry,
   "arithmeticModel":"Archived polygon primitives applied to pinned serialized inputs",
   "scientificClosures":0,"nativeExecutions":0}
out.write_bytes((json.dumps(r,sort_keys=True,indent=2)+"\n").encode())
