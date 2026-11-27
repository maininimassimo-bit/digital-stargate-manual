from argparse import ArgumentParser
import base64
from hashlib import sha256
from io import BytesIO
from itertools import product
import json
import re
from math import hypot
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

parser=ArgumentParser()
for name in ("protocol","inputs","origin","weight","classifier","oracle","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def digest(data):
    return sha256(data).hexdigest()


def pin(path,expected):
    data=path.read_bytes()
    require(digest(data)==expected,f"Changed {path.name}")
    return data


PIN="0a684bc26b7f285babb1ebf1207790e610fbcc325d42a96e1f3265a90a891f7a"
plan=json.loads(pin(args.protocol,PIN))
pin(args.origin/"launcher-subject.json",plan["originSubject"])
origin=json.loads(pin(args.origin/"preflight-v3.json",plan["originPreflight"]))
require(origin["subjectSha256"]==plan["originSubject"] and origin["nativeExecutions"]==0,
        "The origin scope or evidence changed")
subject=json.loads(pin(args.weight/"launcher-subject.json",plan["weightSubject"]))
batch=pin(args.weight/"batch-cfa.js",subject["assetSha256"]["batch-cfa.js"]).decode("utf8")
weight_widths=[float(v) for v in re.findall(r"\bdropShrink:\s*([0-9.]+)",batch)]
require(weight_widths==[.70],"Unexpected control coverage")
weight_plan=json.loads(pin(args.weight/"piano-componenti.json",plan["weightPlan"]))
require(len(weight_plan["cases"])==5 and weight_plan["scientificClosures"]==0,"Changed weight control")
classifier=json.loads(pin(args.classifier,plan["classifier"]))
require(classifier["fullOracleSha256"]==plan["fullOracle"] and classifier["nativeExecutions"]==0,
        "Changed classifier scope")
pin(args.oracle,plan["fullOracle"])

ns={"x":"http://www.pixinsight.com/xdrz"}
index={}
with ZipFile(BytesIO(pin(args.inputs,plan["inputs"]))) as archive:
    manifest=json.loads(archive.read("input-manifest.json"))
    for row in manifest["entries"]:
        name=row["xdrz"]
        key=tuple(row[k] for k in ("geometry","calibration","origin","mask","pose"))
        require(key not in index,"Duplicate descriptor selection")
        raw=archive.read(name)
        h=digest(raw)
        require(h==manifest["files"][name],"Altered descriptor")
        root=ET.fromstring(raw)
        matrix=tuple(float(v) for v in root.findtext("x:AlignmentMatrix",namespaces=ns).split(","))
        require(len(matrix)==9 and matrix[6:]==(0.,0.,1.),"Unexpected affine serialization")
        parts=root.findall("x:RejectionMap/x:ChannelData",ns)
        mask=b"".join(base64.b64decode(x.text,validate=True) for x in parts)
        require(len(mask)==(0 if row["mask"]=="unmasked" else 3*48**2),"Invalid mask dimensions")
        index[key]=dict(sha256=h,matrix=matrix,mask=mask,name=name)
require(len(index)==336 and manifest["conditionalOnSyntheticResult"],"Unexpected candidate descriptor domain")
runs=[]
for geometry,calibration,width,origin,mask in product(
        plan["geometry"],plan["calibration"],plan["widths"],plan["origins"],plan["masks"]):
    paths=[index[geometry,calibration,origin,mask,pose] for pose in range(1,plan["frames"]+1)]
    runs.append(dict(geometry=geometry,calibration=calibration,drop=width,origin=origin,mask=mask,
                     descriptors=[dict(name=r["name"],sha256=r["sha256"]) for r in paths],
                     selected=False))
require(len(runs)==32,"Incomplete conditional case matrix")
paired=[]
for geometry,calibration,origin,pose in product(
        plan["geometry"],plan["calibration"],plan["origins"],range(1,plan["frames"]+1)):
    a,b=(index[geometry,calibration,origin,mask,pose]["mask"] for mask in plan["masks"])
    paired.append(sum(p!=q for p,q in zip(a,b,strict=True)))
origins=[]
for geometry,calibration,mask,pose in product(
        plan["geometry"],plan["calibration"],plan["masks"],range(1,plan["frames"]+1)):
    a,b=(index[geometry,calibration,v,mask,pose]["matrix"] for v in plan["origins"])
    delta=[v-u for u,v in zip(a,b,strict=True)]
    require(max(abs(d) for i,d in enumerate(delta) if i not in (2,5))==0.,"Half-origin changed linear terms")
    origins.append(hypot(delta[2],delta[5]))
record=dict(schema=plan["schema"],protocolSha256=PIN,inputSha256=plan["inputs"],
            fullOracleSha256=plan["fullOracle"],conditionalCaseCount=len(runs),
            casesPerFixedOriginAndMask=8,descriptorsPerCase=plan["frames"],
            rejectionMapComparisons=len(paired),identicalRejectionMaps=sum(v==0 for v in paired),
            largestDifferentMaskSamples=max(paired),originSerializationTranslations=[min(origins),max(origins)],
            validationRequired={
                "origin":{"candidateSubjectSha256":plan["originSubject"],"verifiedNativeReceipt":False},
                "rejectionAndWeights":{"candidateSubjectSha256":plan["weightSubject"],"verifiedNativeReceipt":False,
                                       "coveredWidthsOfFrozenCandidate":weight_widths,
                                       "uncoveredScientificWidths":[v for v in plan["widths"] if v not in weight_widths]},
                "scienceLauncher":{"reviewedAndAdmitted":False}},
            chosenConvention=None,runs=runs,admissionRequested=False,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as f:
    json.dump(record,f,indent=2,sort_keys=True,allow_nan=False)
    f.write("\n")
