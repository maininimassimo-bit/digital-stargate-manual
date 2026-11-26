from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
from itertools import product
import json
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

parser=ArgumentParser()
for name in ("protocol","cropped","prior","kit","calibrated","packages","full_oracle","output"):
    parser.add_argument(name,type=Path)
parser.add_argument("--request",type=Path)
parser.add_argument("--request-sha256")
args=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pin(path,digest):
    require(isinstance(digest,str) and re.fullmatch("[0-9a-f]{64}",digest),"Invalid expected SHA-256")
    data=path.read_bytes()
    require(sha256(data).hexdigest()==digest,f"Changed {path.name}")
    return data


PIN="68760e3b29dbe82f3cc46d31d504eb43066dd3612eff15bb3df950f5a48feaff"
plan=json.loads(pin(args.protocol,PIN))
cropped_code=args.cropped/"compara.py"
source=pin(cropped_code,plan["croppedComparator"])
source_report=pin(args.cropped/"riscontro.json",plan["croppedReport"])
with TemporaryDirectory(dir=args.output.parent) as scratch:
    replay=Path(scratch)/"replay.json"
    original=sys.argv
    sys.argv=[str(cropped_code),*map(str,(args.cropped/"protocollo.json",args.prior,args.kit,args.calibrated,
                                         args.packages,replay))]
    previous={"__name__":"__main__","__file__":str(cropped_code)}
    try:
        exec(compile(source,str(cropped_code),"exec"),previous)
    finally:
        sys.argv=original
    require(replay.read_bytes()==source_report,"Cropped comparator replay changed")

np,fits=(previous[k] for k in ("np","fits"))
with ZipFile(BytesIO(pin(args.full_oracle,plan["fullOracle"]))) as archive:
    meta=previous["record"](archive.read("oracle.json"))
    formats=(meta["arms"],meta["widths"],meta["channels"],meta["shapeYX"])
    require(formats==(["unit","signal"],[1.0,.7],["R","Gsum","B"],[48,48])
            and meta["variants"]==["masked","unmasked","zeroAduWithWeight"]
            and meta["hypotheses"]==plan["modes"],"Invalid full oracle axes")
    intensity,weights,support=(np.load(BytesIO(archive.read(name+".npy")),allow_pickle=False)
                               for name in ("intensity","weights","support"))

require(intensity.shape==(3,3,2,2,2,48,48) and weights.shape==support.shape==(3,3,2,2,48,48)
        and np.isfinite(intensity).all() and np.isfinite(weights).all() and (weights>=0).all()
        and support.dtype==np.bool_ and np.array_equal(support,weights>1e-8),"Invalid full oracle")
x0,y0,x1,y1=meta["cropBoundsXY"]
cropped_i,cropped_w,cropped_s=previous["data"][:3]
np.testing.assert_array_equal(support[...,y0:y1,x0:x1],cropped_s)
np.testing.assert_allclose(intensity[...,y0:y1,x0:x1],cropped_i,atol=1e-10,rtol=0)
np.testing.assert_allclose(weights[...,y0:y1,x0:x1],cropped_w,atol=1e-10,rtol=0)


def expected(config):
    require(set(config)=={"geometry","calibration","drop","origin","mask","inputSha256","fullOracleSha256"},
            "Unexpected run selection")
    require(config["inputSha256"]==previous["plan"]["inputs"] and config["fullOracleSha256"]==plan["fullOracle"],
            "Run bound to different inputs")
    geometry,cal,drop,origin,mask=(config[k] for k in ("geometry","calibration","drop","origin","mask"))
    require(geometry in previous["MODEL"] and cal in previous["CALIBRATION"]
            and type(drop) in (int,float) and drop in previous["DROP"],
            "Unknown geometry, calibration or width")
    require(origin in ("center0","edge05") and mask in ("detector","reference"),
            "Unresolved origin or mask")
    k=previous["DROP"].index(drop)
    j=previous["MODEL"].index(geometry)
    c=previous["CALIBRATION"].index(cal)
    return intensity[0,:,k,j,c],weights[0,:,k,j],support[0,:,k,j]


def scales(w):
    channel=w.max(axis=(1,2))
    require((channel>0).all(),"Undefined full-map scale")
    return dict(identity=np.ones(3),global_expected_peak=np.repeat(channel.max(),3),
                expected_peak_by_channel=channel)


def classify(config,measured_i,measured_w):
    target_i,target_w,target_s=expected(config)
    require((measured_w>=0).all(),"Negative observed weight")
    d=abs(measured_i-target_i)
    intensity_error=float(np.max(d[target_s]))
    rows={}
    for mode,denominator in scales(target_w).items():
        raw_units=measured_w*denominator[:,None,None]
        weight_ok=np.allclose(raw_units,target_w,atol=previous["WEIGHT_ATOL"],rtol=previous["WEIGHT_RTOL"])
        support_ok=np.array_equal(raw_units>1e-8,target_s)
        rows[mode]=dict(expectedDenominatorRgb=denominator.tolist(),
                        maxAbsWeightErrorModelUnits=float(np.max(np.abs(raw_units-target_w))),
                        weightsMatch=bool(weight_ok),supportMatches=bool(support_ok),
                        intensityMatches=intensity_error<=previous["VALUE_ATOL"],
                        compatible=bool(weight_ok and support_ok and intensity_error<=previous["VALUE_ATOL"]))
    matches=[name for name,item in rows.items() if item["compatible"]]
    result=dict(status="UNIQUE_NUMERICAL_HYPOTHESIS" if len(matches)==1 else "UNRESOLVED",
                matchingHypotheses=matches,hypotheses=rows,maxAbsSupportedIntensityError=intensity_error)
    if len(matches)==1:
        denominator=rows[matches[0]]["expectedDenominatorRgb"]
        convention=dict(origin=config["origin"],mask=config["mask"],
                        weightMode="linear_global_scale_per_channel",weightScaleRgb=(1/np.array(denominator)).tolist(),
                        inputsSha256=previous["plan"]["inputs"],oracleSha256=previous["plan"]["oracle"])
        result["croppedReadback"]=previous["numerical_compare"](
            convention,config["geometry"],config["calibration"],config["drop"],measured_i,measured_w)
    return result


def fits_fixture(data):
    stream=BytesIO()
    fits.PrimaryHDU(data.astype(np.float32)).writeto(stream)
    return previous["load_fits"](stream.getvalue())


def selftest():
    base=dict(inputSha256=previous["plan"]["inputs"],fullOracleSha256=plan["fullOracle"])
    counts={mode:0 for mode in plan["modes"]}
    for geometry,cal,drop,origin,mask in product(meta["arms"],("A","B"),meta["widths"],
                                                ("center0","edge05"),("detector","reference")):
        config=dict(base,geometry=geometry,calibration=cal,drop=drop,origin=origin,mask=mask)
        i,w,s=expected(config)
        for mode,denominator in scales(w).items():
            result=classify(config,fits_fixture(i),fits_fixture(w/denominator[:,None,None]))
            require(result["matchingHypotheses"]==[mode] and
                    len(result["croppedReadback"]["descriptorSha256ByPose"])==14,"Wrong hypothesis or case binding")
            counts[mode]+=1
    config=dict(base,geometry="signal",calibration="A",drop=.7,origin="edge05",mask="reference")
    i,w,s=expected(config)
    altered=w.copy()
    altered[0,y0-1,x0]=w.max()
    require(altered[0,y0-1,x0]!=w[0,y0-1,x0],"Outside crop perturbation had no effect")
    missing=w.copy()
    missing[tuple(np.argwhere(s)[0])]=0
    wrong_intensity=i.copy()
    wrong_intensity[s]+=1e-4
    roi=w[:,y0:y1,x0:x1]
    bugs=dict(croppedGlobal=(i,w/roi.max()),croppedByChannel=(i,w/roi.max(axis=(1,2))[:,None,None]),
              weightOutsideCrop=(i,altered),scaledFromObserved=(i,w*.97),
              missingSupport=(i,missing),changedIntensity=(wrong_intensity,w),
              omittedRejection=(intensity[1,:,1,1,0],weights[1,:,1,1]))
    for mode,(observed_i,observed_w) in bugs.items():
        report=classify(config,fits_fixture(observed_i),fits_fixture(observed_w))
        require(report["status"]=="UNRESOLVED" and not report["matchingHypotheses"]
                and "croppedReadback" not in report,f"Accepted altered synthetic map: {mode}")
    return dict(uniqueSyntheticFits=counts,unresolvedSyntheticVariations=list(bugs),
                totalSyntheticMatches=sum(counts.values()))


if args.request is None:
    require(args.request_sha256 is None,"Request pin without request")
    evidence="OFFLINE_SYNTHETIC_FITS_FIXTURES"
    result=selftest()
else:
    spec=previous["record"](pin(args.request,args.request_sha256))
    require(set(spec)=={"selection","intensity","intensitySha256","weight","weightSha256"},
            "Expected one intensity and weight map")
    def load(field):
        name=spec[field]
        require(isinstance(name,str) and re.fullmatch(r"[a-zA-Z0-9_.-]+\.fits",name),"Expected local FITS filename")
        path=args.request.parent/name
        require(path.is_file() and not path.is_symlink(),"Invalid supplied FITS")
        return previous["load_fits"](pin(path,spec[field+"Sha256"]))
    result=classify(spec["selection"],load("intensity"),load("weight"))
    result.update(selection=spec["selection"],requestSha256=args.request_sha256,
                  intensitySha256=spec["intensitySha256"],weightSha256=spec["weightSha256"])
    evidence="UNATTESTED_NUMERICAL_COMPARISON"
result.update(schema=plan["schema"],protocolSha256=PIN,evidence=evidence,fullOracleSha256=plan["fullOracle"],
              nativeProvenanceVerified=False,admissionRequested=False,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as stream:
    json.dump(result,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
