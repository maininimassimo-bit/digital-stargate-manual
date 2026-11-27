from argparse import ArgumentParser
import ast
from hashlib import sha256
from io import BytesIO
from itertools import product
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile

parser=ArgumentParser()
for name in ("protocol","prior","kit","calibrated","packages","output"):
    parser.add_argument(name,type=Path)
parser.add_argument("--request",type=Path)
parser.add_argument("--request-sha256")
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import astropy
from astropy.io import fits
import numpy as np


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def digest(blob):
    return sha256(blob).hexdigest()


HEX=re.compile(r"[0-9a-f]{64}")
PIN="319ddde76eb184047e3b2b7f7227eed58b793a2b29ae8ec9448553fcebf37de9"

def pin(path,expected):
    require(isinstance(expected,str) and HEX.fullmatch(expected),"Invalid expected SHA-256")
    raw=path.read_bytes()
    require(digest(raw)==expected,f"Changed {path.name}")
    return raw


def reject_duplicates(pairs):
    unique={}
    for key,value in pairs:
        require(key not in unique,"Duplicate request field")
        unique[key]=value
    return unique


def record(raw):
    return json.loads(raw,object_pairs_hook=reject_duplicates)


plan=record(pin(args.protocol,PIN))
require((astropy.__version__,np.__version__)==("7.2.0","2.3.5"),"Changed FITS runtime")
MODEL=("unit","signal")
DROP=(1.,.7)
CALIBRATION=("A","B")
CHANNELS=("R","Gsum","B")
VALUE_ATOL=plan["intensityAbsoluteTolerance"]
WEIGHT_ATOL=plan["weightAbsoluteTolerance"]
WEIGHT_RTOL=plan["weightRelativeTolerance"]
functions={"load_fits","describe","compare"}
nodes=[node for node in ast.parse(pin(args.prior,plan["priorComparator"])).body
       if isinstance(node,ast.FunctionDef) and node.name in functions]
require({n.name for n in nodes}==functions,"Changed numerical comparison source")
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(args.prior),"exec"))

with ZipFile(BytesIO(pin(args.kit/"oracolo.zip",plan["oracle"]))) as archive:
    meta=record(archive.read("oracle.json"))
    require(meta["star"]==plan["star"] and meta["matrixAxes"]==list(MODEL)
            and meta["channels"]==list(CHANNELS) and meta["dropWidths"]==list(DROP)
            and meta["calibrationAxis"]==list(CALIBRATION)
            and meta["variants"]==["masked","unmasked","zeroAduWithWeight"],"Changed oracle scope")
    intensity,weight,support=(np.load(BytesIO(archive.read(f"{name}.npy")),allow_pickle=False)
                              for name in ("intensity","weights","support"))
require(intensity.shape==(3,3,2,2,2,29,29) and weight.shape==support.shape==(3,3,2,2,29,29)
        and np.isfinite(intensity).all() and np.isfinite(weight).all() and (weight>=0).all()
        and support.dtype==np.bool_ and np.array_equal(support,weight>1e-8),"Invalid oracle arrays")

with ZipFile(BytesIO(pin(args.kit/"ingressi.zip",plan["inputs"]))) as archive:
    manifest=record(archive.read("input-manifest.json"))
    require(manifest["star"]==plan["star"] and manifest["oracleSha256"]==plan["oracle"]
            and manifest["inputArchiveSha256"]==plan["calibrated"]
            and manifest["inputManifestSha256"]==plan["calibratedManifest"]
            and manifest["conditionalOnSyntheticResult"],"Invalid oracle-to-input binding")
    require(len(archive.namelist())==len(manifest["files"])+1
            and set(archive.namelist())==set(manifest["files"])|{"input-manifest.json"},
            "Invalid member list")
    require(all(digest(archive.read(n))==h for n,h in manifest["files"].items()),
            "Invalid ZIP member bytes")
    roster={r["xdrz"]:r for r in manifest["entries"]}
    require(len(roster)==len(manifest["entries"])==336,"Invalid descriptor roster")
    require(all({r["xdrz"],r["mosaic"],r["auxiliaryRgb"]}<=manifest["files"].keys()
                for r in roster.values()),"Descriptor points outside manifest")

with ZipFile(BytesIO(pin(args.calibrated,plan["calibrated"]))) as archive:
    raw=archive.read("manifest.json")
    require(digest(raw)==plan["calibratedManifest"],"Changed calibrated manifest")
    source=record(raw)
    centers=[]
    for order,row in enumerate(source["frames"],1):
        payload=archive.read(row["manifest"])
        require(digest(payload)==source["files"][row["manifest"]],"Changed frame manifest")
        frame=record(payload)
        require(frame["ordinal"]==order,"Changed exposure order")
        stamp,=[s for s in frame["stamps"] if s["star"]==plan["star"]]
        centers.append(np.asarray(stamp["centerXY"]))
    center=centers[0]
    require(len(centers)==14 and all(np.array_equal(x,center) for x in centers),
            "Changed descriptor reference center")
bounds=[*(np.rint(center).astype(int)-14),*(np.rint(center).astype(int)+15)]
require(all(r["oracleCropBoundsXY"]==bounds for r in roster.values()),"Changed ROI bounds")
data=(intensity,weight,support,manifest,center)


def validate(config):
    require(set(config)=={"origin","mask","weightMode","weightScaleRgb","inputsSha256","oracleSha256"},
            "Invalid convention fields")
    require(config["inputsSha256"]==plan["inputs"] and config["oracleSha256"]==plan["oracle"],
            "Convention bound to different inputs")
    require(config["origin"] in ("center0","edge05") and config["mask"] in ("detector","reference"),
            "Unresolved origin or rejection coordinates")
    require(config["weightMode"]=="linear_global_scale_per_channel","Unresolved weight semantics")
    scale=np.asarray(config["weightScaleRgb"],dtype=float)
    require(scale.shape==(3,) and np.isfinite(scale).all() and np.all(scale>0),"Invalid RGB weight scale")
    return scale


def numerical_compare(config,method,calibration,drop,observed_i,observed_w):
    scale=validate(config)
    result=compare(data,method,calibration,drop,config,scale,observed_i,observed_w)
    result["descriptorSha256ByPose"]=[manifest["files"][name] for name in result["xdrzFiles"]]
    return result


def expanded(image,crop):
    x0,y0,x1,y1=crop
    full=np.zeros((3,48,48),dtype=np.float32)
    full[:,y0:y1,x0:x1]=image
    file=BytesIO()
    fits.PrimaryHDU(full).writeto(file)
    return load_fits(file.getvalue())


def selftest():
    base=dict(origin="edge05",mask="reference",weightMode="linear_global_scale_per_channel",
              weightScaleRgb=[2.,4.,3.],inputsSha256=plan["inputs"],oracleSha256=plan["oracle"])
    passed=0
    for model,calibration,drop,origin,mask in product(MODEL,CALIBRATION,DROP,
                                                     ("center0","edge05"),("detector","reference")):
        config={**base,"origin":origin,"mask":mask}
        v,w,s,area,_,descriptors=describe(data,model,calibration,drop,config)
        scale=validate(config)
        report=numerical_compare(config,model,calibration,drop,expanded(v,area),
                                 expanded(w*scale[:,None,None],area))
        require(len(set(report["descriptorSha256ByPose"]))==len(descriptors)==14,"Lost descriptor binding")
        passed+=1
    method,calibration,drop="signal","A",.7
    i,w,s,area,_,_=describe(data,method,calibration,drop,base)
    idx=(slice(None),DROP.index(drop),MODEL.index(method))
    bad_weight=w.copy()
    bad_weight[tuple(np.argwhere(s)[0])]=0
    bad_value=i.copy()
    bad_value[s]+=1e-4
    rejects=[]
    cases=(
      ("omittedMask",base,intensity[(1,*idx,0)],weight[(1,*idx)]),
      ("zeroValueWithoutWeightRemoval",base,intensity[(2,*idx,0)],weight[(2,*idx)]),
      ("pixelChanged",base,bad_value,w),
      ("supportChanged",base,i,bad_weight),
      ("weightChanged",base,i,w*1.01),
      ("wrongPackage",{**base,"inputsSha256":"0"*64},i,w),
      ("wrongOracle",{**base,"oracleSha256":"0"*64},i,w),
      ("omittedConvention",{**base,"mask":"unmasked"},i,w),
      ("invalidScale",{**base,"weightScaleRgb":[2.,0.,3.]},i,w),
      ("estimatedScaleFromOutput",{**base,"weightMode":"per_image_estimated"},i,w),
    )
    for mode,configuration,bad_i,bad_w in cases:
        try:
            numerical_compare(configuration,method,calibration,drop,expanded(bad_i,area),
                              expanded(bad_w*np.asarray(base["weightScaleRgb"])[:,None,None],area))
        except ValueError as error:
            rejects.append(dict(case=mode,reason=str(error)))
        else:
            raise ValueError(f"Accepted invalid fixture: {mode}")
    return dict(validCases=passed,rejected=rejects)


if args.request is None:
    require(args.request_sha256 is None,"Request digest without request")
    result=selftest()
    evidence="OFFLINE_SYNTHETIC_FITS_FIXTURES"
else:
    config=record(pin(args.request,args.request_sha256))
    require(set(config)=={"geometry","calibration","drop","convention","intensityFile","intensitySha256","weightFile",
                          "weightSha256"},"Invalid comparison request")
    def load_asset(field,digest_key):
        name=config[field]
        require(isinstance(name,str) and re.fullmatch(r"[a-zA-Z0-9_.-]+\.fits",name),
                "FITS name must be a local filename")
        path=args.request.parent/name
        require(path.is_file() and not path.is_symlink(),"Invalid supplied FITS")
        return load_fits(pin(path,config[digest_key]))
    result=numerical_compare(config["convention"],config["geometry"],config["calibration"],config["drop"],
                             load_asset("intensityFile","intensitySha256"),
                             load_asset("weightFile","weightSha256"))
    result.update(requestSha256=args.request_sha256,intensitySha256=config["intensitySha256"],
                  weightSha256=config["weightSha256"])
    evidence="UNATTESTED_NUMERICAL_COMPARISON"
result.update(schema=plan["schema"],protocolSha256=PIN,evidence=evidence,inputsSha256=plan["inputs"],
              oracleSha256=plan["oracle"],nativeProvenanceVerified=False,admissionRequested=False,
              nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as stream:
    json.dump(result,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
