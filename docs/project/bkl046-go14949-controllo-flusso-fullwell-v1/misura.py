"""Compare frozen full-well aperture results with same-visit unsaturated controls."""
import argparse
from contextlib import ExitStack
from hashlib import sha256
import json
from pathlib import Path

parser=argparse.ArgumentParser()
for key in ("protocol","parent","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()


def pinned(path,digest):
    raw=path.read_bytes()
    assert sha256(raw).hexdigest()==digest,path.name
    return raw


pin="fe965178f8414df8176dc2df514fedcf2fe299e721e2d44aebe65a923919ac24"
recipe=json.loads(pinned(args.protocol,pin))
parent=args.parent
source=pinned(parent/"verifica.py",recipe["parentSourceSha256"])
plan=json.loads(pinned(parent/"protocollo.json",recipe["parentProtocolSha256"]))
expected=json.loads(pinned(parent/"riscontro.json",recipe["parentReceiptSha256"]))
scope={"__name__":"pinned_aperture","__file__":str(parent/"verifica.py")}
exec(compile(source,str(parent/"verifica.py"),"exec"),scope)
args.output.mkdir()
previous=args.output/"replay-parent.json"
scope["main"](previous)
assert json.loads(pinned(previous,recipe["parentReceiptSha256"]))==expected
base=scope["BASE"]
reader=scope["read"]
fits=scope["fits"]
np=scope["np"]
depth=base/"BKL046-GO14949-registrazione-profondita-v1"
cross={r["index"]:r for r in reader(depth/"riscontro.json",plan["crossDepthPin"])["rows"]}
roles={role:(n,t,digest) for role,n,t,digest in
       reader(depth/"protocollo.json",plan["crossDepthProtocolPin"])["roles"]}
geometry={}
for key,name in (("primary","BKL046-GO14949-guida-fullwell-primary-v1"),
                 ("repeat","BKL046-GO14949-guida-fullwell-replica-v1")):
    rows=reader(base/name/"riscontro.json",plan["geometryReceipts"][key])["rows"]
    geometry[key]={r["index"]:r for r in rows if r["chip"]==2 and r["oddTile"] and r["guideValid"]
                   and r["longUnsatCentroidState"]=="MEASURED" and r["dqScreen"]=="CLEAR"}

indexes=sorted(geometry["primary"].keys() & geometry["repeat"].keys())
assert indexes and not set(indexes)&set(plan["indices"])
results=[]
with ExitStack() as stack:
    mapfile=base/"BKL046-ACS-GitHub-MAST-d6df7a4fbfeb/wfc2_newpam.fits"
    assert scope["pin"](mapfile)==plan["pamPin"]
    pam=stack.enter_context(fits.open(mapfile,mode="readonly",memmap=True))[0].data
    short_name,short_time,short_pin=roles["B40"]
    images={"B40": (scope["image"](stack,base/"BKL046-GO14949-quadrupoli-v1"/short_name,
                                    short_pin,short_time),short_time)}
    for name,folder,file in (("primary","BKL046-GO14949-guida-fullwell-v1","jdg301bwq_flc.fits"),
                             ("repeat","BKL046-GO14949-guida-fullwell-replica-v1","jdg301byq_flc.fits")):
        images[name]=(scope["image"](stack,base/folder/file,plan["longPins"][name],400),400)
    for i in indexes:
        measured={}
        for name,(frame,time) in images.items():
            center=(cross[i]["measured"]["B40"] if name=="B40"
                    else geometry[name][i]["affinePredictedCenter"])
            measured[name]=scope["observe"](frame,pam,center,recipe["apertureRadiusPx"],time,False,plan)
        results.append(dict(index=i,rates=measured))

original=[r for r in expected["measures"] if r["radiusPx"]==recipe["apertureRadiusPx"]]
assert len(original)==3
clean=[r for r in results if all(v["state"]=="MEASURED" for v in r["rates"].values())]
assert clean


def rate(row,name):
    return row["rates"][name]["electronsPerSecond"]


def summary(rows):
    return {name:[rate(row,name)/rate(row,"B40")-1 for row in rows] for name in ("primary","repeat")}


saturated,controls=summary(original),summary(clean)
control_min,control_max=(f(rate(row,"B40") for row in clean) for f in (min,max))
overlap=sum(control_min<=rate(row,"B40")<=control_max for row in original)
assert all(np.isfinite(value) for dataset in (saturated,controls)
           for values in dataset.values() for value in values)
report=dict(protocol=recipe["schema"],protocolSha256=pin,previousReportExact=True,
            controlCandidates=len(indexes),controlsMeasured=len(clean),
            saturatedDiagnostics=len(original),saturatedBrightnessWithinControlRange=overlap,
            referenceBrightnessControlRange=[control_min,control_max],
            referenceBrightnessSaturated=[rate(row,"B40") for row in original],
            saturatedRelativeToB40=saturated,controlsRelativeToB40={
              name:dict(minimum=min(values),median=float(np.median(values)),maximum=max(values),
                        p05p95=np.quantile(values,[.05,.95]).tolist())
              for name,values in controls.items()},
            geometricAdmissionChanged=False,validatedSaturatedFluxRecovery=False,
            scientificClosures=0,nativeExecutions=0)
for name,body in (("riscontro.json",report),("dettaglio.json",results)):
    with (args.output/name).open("x",encoding="utf-8",newline="\n") as out:
        json.dump(body,out,indent=2,allow_nan=False)
        out.write("\n")
