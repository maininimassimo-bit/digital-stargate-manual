from argparse import ArgumentParser
import ast
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

parser=ArgumentParser()
for name in ("protocol","baseline","numerics","calibrated","cropped","packages","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import astropy
from astropy.io import fits
import numpy as np


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def digest(raw):
    return sha256(raw).hexdigest()


def pin(path,expected):
    raw=path.read_bytes()
    require(digest(raw)==expected,f"Changed {path.name}")
    return raw


PIN="1ada808ec63a81642606d70e2521328f53d2b438ff97168a092bd937bb48ae61"
plan=json.loads(pin(args.protocol,PIN))
require((astropy.__version__,np.__version__)==("7.2.0","2.3.5"),"Changed numerical runtime")
baseline=json.loads(pin(args.baseline,plan["baseline"]))
expected_matrices=baseline["forwardMatrices"]
old=pin(args.cropped,plan["oracolo"])
with ZipFile(BytesIO(old)) as source:
    meta=json.loads(source.read("oracle.json"))
    require(meta["star"]==plan["star"] and meta["matrixAxes"]==plan["arms"]
            and meta["dropWidths"]==plan["widths"] and meta["variants"]==plan["variants"]
            and meta["channels"]==["R","Gsum","B"],"Unexpected cropped oracle dimensions")
    prior_i,prior_w,prior_s=(np.load(BytesIO(source.read(f"{name}.npy")),allow_pickle=False)
                            for name in ("intensity","weights","support"))
functions={"clip_batch","intersections","resample"}
nodes=[n for n in ast.parse(pin(args.numerics,plan["math"])).body
       if isinstance(n,ast.FunctionDef) and n.name in functions]
require({n.name for n in nodes}==functions,"Changed overlap kernel")
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(args.numerics),"exec"))
side=plan["size"]
require(side%2==0 and len(expected_matrices)==14,"Unexpected even padded grid")
r=side//2
points=np.arange(-r,r+1)
grid_center=np.array([r,r])
pixels=np.indices((side,side))
parity=2*(pixels[0]%2)+pixels[1]%2
# Axes: parity, width, arm, weight/flux A/flux B, padded y, padded x.
stack=np.zeros((4,2,2,3,len(points),len(points)))
reject=np.zeros_like(stack)
centers=[]


def decode_fits(raw):
    with fits.open(BytesIO(raw),memmap=False) as hdus:
        require(len(hdus)==1,"Unexpected FITS layout")
        h=hdus[0]
        require(h.data.shape==(side,side) and h.verify_checksum()==h.verify_datasum()==1
                and (h.header["BAYERPAT"],h.header["XBAYROFF"],h.header["YBAYROFF"],
                     h.header["DSGADUN"],h.header["DSGADUB"])==("RGGB",0,0,262144,65536),
                "Unexpected calibrated FITS geometry")
        return h.data.astype(float)*262144-65536


with ZipFile(BytesIO(pin(args.calibrated,plan["calibrated"]))) as source:
    raw=source.read("manifest.json")
    require(digest(raw)==plan["calibratedManifest"],"Changed source manifest")
    manifest=json.loads(raw)
    require(len(manifest["frames"])==14,"Changed exposure count")
    def member(name):
        raw=source.read(name)
        require(digest(raw)==manifest["files"][name],"Changed calibrated ZIP member")
        return raw
    for ordinal,(item,matrix_row) in enumerate(zip(manifest["frames"],expected_matrices,strict=True),1):
        frame=json.loads(member(item["manifest"]))
        require(frame["ordinal"]==ordinal and frame["member"]==matrix_row["member"],"Frame order changed")
        stamp,=[row for row in frame["stamps"] if row["star"]==plan["star"]]
        require(all(o%2==0 for o in stamp["cropOriginXY"]),"CFA crop parity changed")
        centers.append(np.array(stamp["centerXY"]))
        keep=np.unpackbits(np.frombuffer(bytes.fromhex(stamp["validMaskBitsLE"]),np.uint8),
                           bitorder="little").reshape((side,side)).astype(bool)
        require(int(keep.sum())==stamp["validSamples"],"Changed valid sample count")
        values=np.asarray([decode_fits(member(stamp["files"][name])) for name in ("A","B")])
        t=np.eye(3)
        t[:2,2]=stamp["cropOriginXY"]
        for model,name in enumerate(("binned","mosaic")):
            local=np.linalg.inv(t)@np.asarray(matrix_row[name])@t
            inverse=np.linalg.inv(local)
            for width,drop in enumerate(plan["widths"]):
                for mask,target in ((keep,stack),(~keep,reject)):
                    if mask.any():
                        positions=np.column_stack((pixels[1][mask],pixels[0][mask]))
                        target[:,width,model]+=resample(positions,parity[mask],values[:,mask],inverse,drop,grid_center)

require(all(np.array_equal(c,centers[0]) for c in centers),"Reference crop center changed")


def rgb(buffer):
    whole=buffer[...,:side,:side]
    return np.stack((whole[0],whole[1]+whole[2],whole[3]),axis=0)


accepted,discarded=rgb(stack),rgb(reject)
zeros=accepted.copy()
zeros[:,:,:,0]+=discarded[:,:,:,0]
variants=np.asarray([accepted,accepted+discarded,zeros])
weights=variants[:,:,:,:,0]
counts=variants[:,:,:,:,1:]
support=weights>1e-8
linear=np.divide(counts,weights[...,None,:,:],out=np.zeros_like(counts),where=support[...,None,:,:])
encoded=np.where(support[...,None,:,:],(linear+65536)/262144,0.)
require(np.isfinite(encoded).all() and np.isfinite(weights).all() and (weights>=0).all(),
        "Nonfinite full oracle")
x,y=np.rint(centers[0]).astype(int)
roi=(slice(y-14,y+15),slice(x-14,x+15))
crop_w=weights[(...,*roi)]
crop_i=encoded[(...,*roi)]
np.testing.assert_array_equal(support[(...,*roi)],prior_s)
np.testing.assert_allclose(crop_w,prior_w,atol=plan["weightAtol"],rtol=0)
np.testing.assert_allclose(crop_i,prior_i,atol=plan["intensityAtol"],rtol=0)
maxima=weights.max(axis=(-1,-2))
small_max=crop_w.max(axis=(-1,-2))
require((maxima>0).all(),"Undefined expected scale")
whole=maxima.max(axis=1,keepdims=True)
modes={"identity":weights,"global_expected_peak":weights/whole[...,None,None],
       "expected_peak_by_channel":weights/maxima[...,None,None]}
np.testing.assert_allclose(modes["global_expected_peak"].max(axis=(1,4,5)),np.ones((3,2,2)),atol=1e-14)
np.testing.assert_allclose(modes["expected_peak_by_channel"].max(axis=(-1,-2)),np.ones_like(maxima),atol=1e-14)
spread=np.max(np.abs(modes["global_expected_peak"]-modes["expected_peak_by_channel"]),axis=(1,4,5))
require((spread>0.01).all(),"Normalization alternatives are not numerically separated")

out=args.output/"oracolo-pieno.zip"
metadata=dict(schema=plan["schema"],protocolSha256=PIN,star=plan["star"],shapeYX=[side,side],
              channels=["R","Gsum","B"],arms=plan["arms"],widths=plan["widths"],variants=plan["variants"],
              cropBoundsXY=list(map(int,(x-14,y-14,x+15,y+15))),hypotheses=plan["relativeScaleHypotheses"],
              wholeMapPeaks=whole[:,0].tolist(),wholeMapChannelPeaks=maxima.tolist(),
              croppedChannelPeaks=small_max.tolist(),retainedWeightSemanticsVerifiedNatively=False)
with ZipFile(out,"x") as package:
    for name,value in (("intensity",encoded),("weights",weights),("support",support)):
        stream=BytesIO()
        np.save(stream,value,allow_pickle=False)
        package.writestr(ZipInfo(f"{name}.npy",(2026,1,1,0,0,0)),stream.getvalue(),ZIP_DEFLATED)
    package.writestr(ZipInfo("oracle.json",(2026,1,1,0,0,0)),json.dumps(metadata,indent=2,sort_keys=True)+"\n",ZIP_DEFLATED)
with ZipFile(out) as package:
    require(package.testzip() is None and json.loads(package.read("oracle.json"))==metadata,
            "Invalid full oracle archive")
result=dict(metadata,oracleSha256=digest(out.read_bytes()),
            cropMaxWeightError=float(np.max(np.abs(crop_w-prior_w))),
            cropMaxIntensityError=float(np.max(np.abs(crop_i-prior_i))),
            maskedFullPeakAboveCroppedCount=int((maxima[0]>small_max[0]+1e-10).sum()),
            maskedLargestPeakDifference=float((maxima[0]-small_max[0]).max()),
            maxMapDifferenceGlobalVersusChannel=spread.tolist(),nativeExecutions=0,scientificClosures=0)
with (args.output/"riscontro.json").open("x",encoding="utf8",newline="\n") as stream:
    json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
    stream.write("\n")
