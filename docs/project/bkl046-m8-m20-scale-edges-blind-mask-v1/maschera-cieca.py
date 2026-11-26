"""Evaluate the historical blind mask with the frozen M8/M20 full-grid injections."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, known, prior, rule_file, base, joint_path, dependencies, out = map(Path, sys.argv[1:])
raw = protocol.read_bytes()
config = json.loads(raw)

def pin(path, expected):
    content = path.read_bytes()
    if sha256(content).hexdigest() != expected:
        raise ValueError("SOURCE_CHANGED:" + path.name)
    return content

known_report = json.loads(pin(known / "riscontro.json", config["knownReportSha256"]))
known_protocol = known / "protocollo.json"
pin(known_protocol, config["knownProtocolSha256"])
source = known / "maschera.py"
prefix, marker, _ = pin(source, config["knownProgramSha256"]).decode().partition("\nmasks = {}")
assert marker
frozen = {"__file__": str(source)}
sys.argv = [str(source),str(known_protocol),str(prior),str(rule_file),
            str(base),str(joint_path),str(dependencies),str(out)]
exec(compile(prefix,str(source),"exec"),frozen)
np = frozen["np"]
design, groups, images, common, signals, support, assess, joint, train, signal_bins, geometry = (
    frozen[name] for name in ("design","groups","images","common","signals","support","assess","joint",
                              "train","signal_bins","geometry"))
parameters = frozen["config"]
rule = frozen["rule"]
cell = frozen["namespace"]["namespace"]["cell"]
positions = [(s[0].start//cell,s[1].start//cell) for s in groups]
assert positions == [(r,c) for r in range(12) for c in range(16)]


def mask(values):
    params,_,rank,_ = np.linalg.lstsq(design[train],values[train],rcond=None)
    assert rank==3
    residual = values-design @ params
    center=np.median(residual[train])
    scale=max(1e-9,1.4826*np.median(np.abs(residual[train]-center)))
    seeds=(residual>center+rule["maskSigma"]*scale).reshape(12,16)
    pixels=np.pad(seeds,1)
    return ~np.lib.stride_tricks.sliding_window_view(pixels,(3,3)).any(axis=(2,3)).ravel()


def fit(values,keep):
    result=[]
    for terms in (1,3):
        coeff,_,rank,_=np.linalg.lstsq(design[keep,:terms],values[keep],rcond=None)
        assert rank==terms
        result.append(coeff)
    return result


assert mask(design @ np.array([100.,7.,-3.])).all()
impulse=np.zeros(len(groups))
impulse[85]=100
dilated=np.flatnonzero(~mask(impulse))
assert set(dilated)=={68,69,70,84,85,86,100,101,102}
contaminated={name:np.array([np.max(cell)>=parameters["peakAdu"]*rule["blankTruthMaxFraction"]
                             for cell in bins]) for name,bins in signal_bins.items()}
for name,dirty in contaminated.items():
    assert int((~dirty).sum())==known_report["geometry"]["0.02"][name]["cleanCellsTotal"]

geometry_cache={}
def cached_geometry(keep):
    key=keep.tobytes()
    if key not in geometry_cache:
        geometry_cache[key]=geometry(keep)
    return geometry_cache[key]

results=[]
for pair in joint["cases"]:
    ref,target=pair["reference"],pair["target"]
    delta=images[target]-images[ref]
    contrast=images[target]-np.median(images[target][common])
    d_bins=[delta[s][valid] for s,valid in zip(groups,support,strict=True)]
    c_bins=[contrast[s][valid] for s,valid in zip(groups,support,strict=True)]
    scenarios=[("unitControl",None,1.)]
    scenarios.extend(("jointPass",i,t["scale"]) for i,t in enumerate(pair["trials"]) if t["jointPass"])
    for cohort,index,scale in scenarios:
        scaled=[d+(scale-1)*c for d,c in zip(d_bins,c_bins,strict=True)]
        before=np.array([np.median(d) for d in scaled])
        keep_before=mask(before)
        geo_before=cached_geometry(keep_before)
        before_fit=fit(before,keep_before) if geo_before["reason"] is None else None
        for name,signal in signals.items():
            added=np.array([np.median(d+s) for d,s in zip(scaled,signal_bins[name],strict=True)])
            keep_after=mask(added)
            geo_after=cached_geometry(keep_after)
            row={"cohort":cohort,"reference":ref,"target":target,"priorTrialIndex":index,
                 "scale":scale,"profile":name,"geometryBefore":geo_before,"geometryAfter":geo_after,
                 "maskChanged":bool(np.any(keep_before!=keep_after))}
            if before_fit is None or geo_after["reason"] is not None:
                row["status"]="ABSTAINED"
            else:
                after_fit=fit(added,keep_after)
                row["status"]="EVALUATED"
                row["models"]={model:assess(signal,a,b) for model,a,b in
                               zip(("offset","plane"),before_fit,after_fit,strict=True)}
            dirty=contaminated[name]
            row["contaminatedCellsKeptAfter"]=int((dirty & keep_after).sum())
            row["cleanCellsRejectedAfter"]=int((~dirty & ~keep_after).sum())
            results.append(row)

summary={}
for cohort,n in (("jointPass",parameters["expectedJointTrials"]),("unitControl",parameters["expectedUnitControls"])):
    summary[cohort]={}
    for name in signals:
        cases=[r for r in results if r["cohort"]==cohort and r["profile"]==name]
        assert len(cases)==n
        evaluated=[r for r in cases if r["status"]=="EVALUATED"]
        models={}
        for model in ("offset","plane"):
            values=[row["models"][model] for row in evaluated]
            if values:
                models[model]={"passes":sum(v["pass"] for v in values),
                               "medianFluxError":float(np.median([v["relativeFluxError"] for v in values])),
                               "medianRelativeL2":float(np.median([v["relativeL2"] for v in values]))}
        summary[cohort][name]={"evaluated":len(evaluated),"abstained":n-len(evaluated),
            "maskChanges":sum(r["maskChanged"] for r in cases),
            "medianContaminatedCellsKept":float(np.median([r["contaminatedCellsKeptAfter"] for r in cases])),
            "medianCleanCellsRejected":float(np.median([r["cleanCellsRejectedAfter"] for r in cases])),
            "models":models}
receipt={"schema":"BKL046_M8M20_BLIND_DIFFUSE_MASK_V1","protocolSha256":sha256(raw).hexdigest(),
         "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),"summary":summary,
         "source":config["knownReportSha256"],"nativeExecutions":0,"scientificClosures":0}
full=(json.dumps({**receipt,"results":results},sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
with (out/"tutti-gli-esiti.json").open("xb") as stream:
    stream.write(full)
receipt["fullReportSha256"]=sha256(full).hexdigest()
with (out/"riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps(summary,sort_keys=True))
