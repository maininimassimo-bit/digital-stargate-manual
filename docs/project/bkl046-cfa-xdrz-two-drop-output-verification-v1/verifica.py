from argparse import ArgumentParser
import ast
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

parser=ArgumentParser()
for k in ("protocol","batch","integer","fractional","classifier","packages","report"):
    parser.add_argument(k,type=Path)
parser.add_argument("--outputs",type=Path)
parser.add_argument("--reservation")
parser.add_argument("--marker-sha256")
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np
from astropy.io import fits


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path,maximum):
    require(path.is_file() and not path.is_symlink(),f"Invalid evidence file {path.name}")
    with path.open("rb") as stream:
        raw=stream.read(maximum+1)
    require(0<len(raw)<=maximum,f"Invalid evidence size {path.name}")
    return raw


def pin(path,expected,maximum=4_194_304):
    raw=read(path,maximum)
    require(sha(raw)==expected,f"Changed {path.name}")
    return raw


def unique(pairs):
    data={}
    for k,v in pairs:
        require(k not in data,"Duplicate JSON field")
        data[k]=v
    return data


def record(raw):
    return json.loads(raw,object_pairs_hook=unique)


PIN="18a713ebe51bde9d99f686f427e10a09014647fc71494f331477ef7c50d969d6"
plan=record(pin(args.protocol,PIN))
batch=record(pin(args.batch/"piano.json",plan["plan"]))
contract=record(pin(args.batch/"contratto.json",plan["contract"]))
pin(args.batch/"batch-cfa.js",plan["batch"])
require(batch["operation"]==contract["operation"] and contract["planSha256"]==plan["plan"]
        and len(batch["cases"])==contract["caseCount"]==12,"Wrong batch identity")
SHAPE=(3,28,32)
TOLERANCE=plan["weightAtol"]
SUPPORT=1e-8
ARMS=("unmasked","mask-green","mask-wrong-channel","zero-detector","zero-reference")
NAMES=("unmasked","detector","reference","zero-detector-retained","zero-reference-retained")
profiles={"raw":"RAW","globalMax":"GLOBAL_MAX","channelMax":"CHANNEL_MAX"}
nodes=[n for n in ast.parse(pin(args.classifier,plan["classifier"])).body
       if isinstance(n,ast.FunctionDef) and n.name in {"classify_map","classify_set","transformed","profiled_models","classify_scale","fits_map"}]
require(len(nodes)==6,"Wrong classifier functions")
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(args.classifier),"exec"))
with ZipFile(BytesIO(pin(args.integer,plan["integerOracle"]))) as package:
    meta=record(package.read("manifest.json"))
    require(tuple(meta["models"])==NAMES and meta["widths"]==[.7,1],"Wrong integer axes")
    values=np.load(BytesIO(package.read("oracoli.npy")),allow_pickle=False)
require(values.shape==(2,5,2,*SHAPE),"Wrong integer shape")
integer={drop:{name:tuple(data) for name,data in zip(NAMES,pair,strict=True)}
         for drop,pair in zip(meta["widths"],values,strict=True)}
with ZipFile(BytesIO(pin(args.fractional,plan["fractionalOracle"]))) as package:
    meta=record(package.read("manifest.json"))
    raw=package.read("predictions.npy")
    require(sha(raw)==meta["sourceFiles"]["predictions.npy"],"Wrong fractional prediction bytes")
    maps=np.load(BytesIO(raw),allow_pickle=False)
require(maps.shape==(6,2,*SHAPE),"Wrong fractional shape")
fractional={(item["width"],profiles[item["profile"]]):tuple(data)
            for item,data in zip(meta["modelOrder"],maps,strict=True)}
require(set(fractional)=={(w,p) for w in integer for p in profiles.values()},"Incomplete fractional reference")

knobs=dict(enableCFA=True,scale=1,useLUT=False,enableImageWeighting=False,enableSurfaceSplines=False,
           enableLocalNormalization=False,enableAdaptiveNormalization=False,truncateOnOutOfRange=False,
           closePreviousImages=False,showImages=False)
enums=("onError","cfaPattern","kernelFunction")
cases=batch["cases"]
markers=("batch.done.json","events.txt","console.log")
names=(*markers,*(f'{c["id"]}-{suffix}.fits' for c in cases for suffix in ("rgb","weight")))
operation=batch["operation"]


def canonical_marker(reservation):
    return dict(schema="BKL046_CFA_XDRZ_TWO_DROP_MARKER_CANDIDATE_V1",scope="OUTPUT_MARKER_NOT_ADMISSION",
                operation=operation,planSha256=plan["plan"],componentContractSha256=plan["contract"],
                reservation=reservation,cases=[row["id"] for row in cases])


def payload(path,name):
    return read(path/name,4_194_304 if name=="console.log" else 262_144)


def classify_fractional(observed_i,observed_w):
    if not np.isfinite(observed_w).all() or (observed_w<0).any():
        return []
    matches=[]
    for (width,profile),(model_i,model_w) in fractional.items():
        support=model_w>SUPPORT
        if (np.array_equal(support,observed_w>SUPPORT) and np.isfinite(observed_i[support]).all()
                and np.allclose(observed_w,model_w,atol=TOLERANCE,rtol=0)
                and np.allclose(observed_i[support],model_i[support],atol=plan["intensityAtol"],rtol=0)):
            matches.append(dict(width=width,profile=profile))
    return matches


def settings_for(case):
    return dict(knobs,dropShrink=case["drop"],enableRejection=case["rejection"],
                inputData=[[True,case["root"]+n,""] for n in case["files"]])


def inspect(path,reservation,marker_pin):
    require(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",reservation),
            "Invalid reservation")
    require({p.name for p in path.iterdir()}==set(names),"Unexpected output roster")
    data={n:payload(path,n) for n in names}
    require(sha(data[markers[0]])==marker_pin and
            record(data[markers[0]])==canonical_marker(reservation),"Wrong written marker")
    lines=data[markers[1]].decode("utf8").splitlines()
    require(len(lines)==24,"Incomplete parameter and export transcript")
    root=plan["root"]+reservation+"/products/"
    console_markers=["DSG_CFA_NATIVE_BEGIN "+reservation]
    observed_enums=None
    fits_by_case={}
    observations=[]
    for c,pars,exp in zip(cases,lines[::2],lines[1::2],strict=True):
        name=c["id"]
        require(pars.startswith("DSG_CFA_PARAMETERS ") and exp.startswith("DSG_CFA_EXPORT "),"Wrong event order")
        p,v=(record(line.split(" ",1)[1]) for line in (pars,exp))
        require(p["caseId"]==v["caseId"]==name,"Wrong case identity")
        expected=settings_for(c)
        settings=p["settings"]
        require(set(settings)==expected.keys()|set(enums) and all(settings[k]==value for k,value in expected.items())
                and all(type(settings[k]) is type(expected[k]) for k in knobs if k!="scale")
                and settings["enableRejection"] is c["rejection"]
                and type(settings["scale"]) is int and type(settings["dropShrink"]) in (int,float),
                "Wrong effective configuration")
        these=[settings[e] for e in enums]
        require(all(type(e) is int and e>=0 for e in these) and (observed_enums is None or these==observed_enums),
                "Wrong enumeration")
        observed_enums=these
        require(isinstance(p["source"],str) and 0<len(p["source"].strip())<=65536,"Missing effective process source")
        require(v["intensity"]==root+name+"-rgb.fits" and v["weights"]==root+name+"-weight.fits"
                and v["weightMeaning"]==contract["weightOutput"] and v["geometryGroup"]==c["group"]
                and type(v["effectiveDropShrink"]) in (int,float) and v["effectiveDropShrink"]==c["drop"]
                and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,127}",v["weightWindowId"]),
                "Wrong export identity or width")
        console_markers.append(f'DSG_CFA_NATIVE_CASE {name} {v["weightWindowId"]}')
        fits_by_case[name]=tuple(fits_map(data[name+"-"+suffix+".fits"]) for suffix in ("rgb","weight"))
        observations.append(dict(case=name,declaredDrop=c["drop"],postExecutionDrop=v["effectiveDropShrink"],
                                 processSourceSha256=sha(p["source"].encode("utf8"))))
    console_markers.append("DSG_CFA_NATIVE_END "+reservation)
    pattern=re.compile(r"(?<!\S)DSG_CFA_NATIVE_(?:BEGIN|CASE|END)\b.*$")
    found=[m.group().strip() for line in data[markers[2]].decode("utf8").splitlines()
           if (m:=pattern.search(line))]
    require(found==console_markers,"Native console markers differ")
    widths=[]
    decisions=[]
    for tag,width in (("070",.7),("100",1)):
        witness=classify_fractional(*fits_by_case[tag+"-fractional"])
        integer_out=classify_scale({name:fits_by_case[tag+"-"+name] for name in ARMS},integer[width])
        combined=None
        profile=integer_out["weightProfile"]
        if profile is not None and witness==[dict(width=width,profile=profile)]:
            outcome=integer_out["profileResults"][profile]
            if outcome["status"] in ("ZERO_SAMPLE_EXCLUDED","ZERO_WEIGHT_RETAINED"):
                combined=dict(profile=profile,coordinates=outcome["greenMaskCoordinateModel"],zeros=outcome["status"])
        decisions.append(combined)
        widths.append(dict(requestedWidth=width,witnessMatches=witness,integer=integer_out,combined=combined))
    status=("UNRESOLVED" if any(x is None for x in decisions) else
            "CONSISTENT_NUMERICAL_CONVENTION" if decisions[0]==decisions[1] else "WIDTH_DEPENDENT_CONVENTION")
    require({p.name for p in path.iterdir()}==set(names) and
            all(sha(payload(path,n))==sha(data[n]) for n in names),"Outputs changed during comparison")
    return dict(status=status,widths=widths,observations=observations,
                outputSha256={n:sha(raw) for n,raw in data.items()})


def selftest(base):
    reservation="52d471bc-3d3d-42ea-ad47-29146dbd36a5"
    root=plan["root"]+reservation+"/products/"
    roster=dict(zip(ARMS,("unmasked","detector","unmasked","zero-detector-retained","zero-reference-retained"),strict=True))
    test={}
    for mode,expected in (
        ("global","CONSISTENT_NUMERICAL_CONVENTION"),("channel","CONSISTENT_NUMERICAL_CONVENTION"),
        ("different-width-profile","WIDTH_DEPENDENT_CONVENTION"),("wrong-width-fits","UNRESOLVED"),
        ("wrong-console",None),("wrong-export-width",None),("missing-map",None)):
        path=base/mode
        path.mkdir()
        marker=json.dumps(canonical_marker(reservation)).encode()
        (path/markers[0]).write_bytes(marker)
        events=[]
        console=["DSG_CFA_NATIVE_BEGIN "+reservation]
        for idx,c in enumerate(cases):
            width=c["drop"]
            name=c["id"]
            profile="CHANNEL_MAX" if mode=="channel" or (mode=="different-width-profile" and width==1) else "GLOBAL_MAX"
            if c["group"]=="fractional":
                ref_width=.7 if mode=="wrong-width-fits" and width==1 else width
                a,b=fractional[ref_width,profile]
            else:
                value,weight=integer[width][roster[name.split("-",1)[1]]]
                a,b=value,transformed(weight,profile)
            for kind,arr in (("rgb",a),("weight",b)):
                if mode=="missing-map" and idx==11 and kind=="weight":
                    continue
                fits.PrimaryHDU(arr.astype(np.float32)).writeto(path/f"{name}-{kind}.fits")
            which=f"weight_{idx}"
            console.append(f"DSG_CFA_NATIVE_CASE {name} {which}")
            p=dict(caseId=name,settings=dict(settings_for(c),onError=0,cfaPattern=0,kernelFunction=1),
                   source=f"fixture: dropShrink = {width}")
            export_width=1 if mode=="wrong-export-width" and idx==0 else width
            e=dict(caseId=name,intensity=root+name+"-rgb.fits",weights=root+name+"-weight.fits",
                   effectiveDropShrink=export_width,geometryGroup=c["group"],weightWindowId=which,
                   weightMeaning=contract["weightOutput"])
            events.extend(("DSG_CFA_PARAMETERS "+json.dumps(p),"DSG_CFA_EXPORT "+json.dumps(e)))
        console.append("DSG_CFA_NATIVE_END "+reservation)
        if mode=="wrong-console":
            console.pop(4)
        (path/markers[1]).write_bytes(("\n".join(events)+"\n").encode())
        (path/markers[2]).write_bytes(("\n".join(console)+"\n").encode())
        try:
            result=inspect(path,reservation,sha(marker))
        except ValueError as error:
            require(expected is None,f"Unexpected fixture rejection: {error}")
            test[mode]=str(error)
        else:
            require(result["status"]==expected,f"Wrong fixture outcome for {mode}")
            test[mode]=result["status"]
    return test


if args.outputs is None:
    require(args.marker_sha256 is None and args.reservation is None,"Partial supplied-run arguments")
    with TemporaryDirectory(dir=args.report.parent) as scratch:
        result=dict(syntheticCases=selftest(Path(scratch)))
    evidence="OFFLINE_SYNTHETIC_FITS_FIXTURES"
else:
    require(isinstance(args.reservation,str) and isinstance(args.marker_sha256,str),"Missing supplied-run identity")
    result=inspect(args.outputs,args.reservation,args.marker_sha256)
    evidence="UNATTESTED_NUMERICAL_COMPARISON"
result.update(schema=plan["schema"],protocolSha256=PIN,evidence=evidence,planSha256=plan["plan"],
              nativeProvenanceVerified=False,admissionRequested=False,nativeExecutions=0,scientificClosures=0)
with args.report.open("x",encoding="utf8",newline="\n") as out:
    json.dump(result,out,indent=2,sort_keys=True,allow_nan=False)
    out.write("\n")
