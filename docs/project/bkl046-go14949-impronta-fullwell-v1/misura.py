"""Compare DQ footprint stability on paired ACS full-well observations."""
import argparse
from collections import Counter
from hashlib import file_digest,sha256
from itertools import product
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("protocol","primary_bundle","replica_bundle","primary_fits","replica_fits","packages","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
from astropy.io import fits
import astropy
import numpy as np
assert (astropy.__version__,np.__version__)==("7.2.0","2.3.5")


def pinned(path,digest):
    raw=path.read_bytes()
    if sha256(raw).hexdigest()!=digest:
        raise ValueError(f"Unexpected bytes: {path.name}")
    return json.loads(raw)


def chip_dq(bundle,plan,filename):
    spec=plan["long"]
    path=bundle/spec["name"]
    if not path.is_file():
        path=filename
    assert path.name==spec["name"]
    with path.open("rb") as stream:
        assert file_digest(stream,"sha256").hexdigest()==spec["sha256"]
    with fits.open(path,mode="readonly",memmap=False) as h:
        assert h[0].header["PROPOSID"]==14949
        assert h[0].header["FILTER1"]=="F606W" and h[0].header["EXPTIME"]==400
        ext,=[i for i in (1,2) if h["SCI",i].header["CCDCHIP"]==2]
        return np.asarray(h["DQ",ext].data,dtype=np.uint16)


pin="4b81b01ce0a9e99a8d6b86a91939660e140265160bbaae37cdb58a796322f9fb"
cfg=pinned(args.protocol,pin)
baseline = {}
images = {}
for key,bundle,filename in (("primary",args.primary_bundle,args.primary_fits),
                            ("replica",args.replica_bundle,args.replica_fits)):
    report = pinned(bundle/"riscontro.json",cfg[key+"ReportSha256"])
    plan = pinned(bundle/"protocollo.json",cfg[key+"ProtocolSha256"])
    assert report["chips"]["2"]["geometricPrescreenPureFullWell"]==0
    assert plan["criteria"]["coreRadiusPx"]==3 and plan["criteria"]["fullWellBit"]==256 and plan["criteria"]["adcBit"]==2048
    baseline[key]={row["index"]:row for row in report["rows"] if
                   row["chip"]==2 and row["oddTile"] and row["guideValid"] and row["affinePredictedCenter"] is not None}
    images[key]=chip_dq(bundle,plan,filename)


def flags(image,center,offset,radius):
    x,y=np.rint(np.asarray(center)+offset).astype(int)
    n,m=image.shape
    assert radius<=x<m-radius and radius<=y<n-radius
    ly,lx=np.mgrid[-radius:radius+1,-radius:radius+1]
    inside=lx*lx+ly*ly<=radius*radius
    values=image[y+ly[inside],x+lx[inside]]
    words=dict(sorted(Counter(str(int(v)) for v in values).items()))
    relative=set(zip(lx[inside][(values&256)!=0].tolist(),ly[inside][(values&256)!=0].tolist(),strict=True))
    if np.any(values&2048):
        state="ADC_PRESENT"
    elif not relative:
        state="OTHER_DQ" if np.any(values) else "CLEAR"
    else:
        state="PURE_FULL_WELL" if np.all((values==0)|(values==256)) else "FULL_WELL_MIXED_DQ"
    return state,words,relative


common=sorted(set(baseline["primary"])&set(baseline["replica"]))
rows=[]
for i in common:
    forecasts={key:baseline[key][i]["affinePredictedCenter"] for key in baseline}
    radii=[]
    for radius in cfg["radiiPx"]:
        base={}
        footprints={}
        sensitivity={}
        for key in baseline:
            state,words,relative=flags(images[key],forecasts[key],(0,0),radius)
            if radius==3:
                assert (state,words)==(baseline[key][i]["dqScreen"],baseline[key][i]["dqWords"])
            footprints[key]=relative
            base[key]=dict(classification=state,dqWords=words,fullWellPixels=len(relative))
            senses=[flags(images[key],forecasts[key],offset,radius)[0]
                    for offset in product(cfg["centerCoordinatePerturbationsPx"],repeat=2)]
            sensitivity[key]=dict(Counter(senses))
        first,second = (footprints[k] for k in ("primary","replica"))
        overlap=len(first&second)
        union=len(first|second)
        radii.append(dict(radiusPx=radius,originalCenters=base,classificationUnderPerturbation=sensitivity,
                          relativeWellFlagOverlap=overlap,relativeWellFlagUnion=union))
    rows.append(dict(sourceIndex=i,radii=radii))

assert len(rows)>=60
selected = [r["sourceIndex"] for r in rows if all(x["classification"]=="PURE_FULL_WELL"
             for x in r["radii"][0]["originalCenters"].values())]
assert selected==[2,10,11]
result=dict(protocol=cfg["schema"],protocolSha256=pin,sourceReportsRevalidatedAtRadius3=True,
            commonGuideForecasts=len(common),pureAtOriginalRadiusBothExposures=selected,
            admittedGeometries=0,realSaturatedFluxRecovered=False,nativeExecutions=0,
            scientificClosures=0,rows=rows)
with args.output.open("x",encoding="utf-8",newline="\n") as f:
    json.dump(result,f,indent=2,allow_nan=False)
    f.write("\n")
