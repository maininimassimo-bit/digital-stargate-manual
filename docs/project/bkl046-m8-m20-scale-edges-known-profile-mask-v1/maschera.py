"""Measure recoverable support and signal transfer with a known-profile mask."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, prior, rule_file, base, joint_path, dependencies, out = map(Path, sys.argv[1:])
raw = protocol.read_bytes()
protocol_data = json.loads(raw)

def pin(path, expected):
    source = path.read_bytes()
    if sha256(source).hexdigest() != expected:
        raise ValueError("SOURCE_CHANGED:" + path.name)
    return source

baseline = json.loads(pin(prior/"riscontro.json", protocol_data["previousReportSha256"]))
rule = json.loads(pin(rule_file, protocol_data["maskRuleSourceSha256"]))
source = prior/"iniezioni.py"
prefix, separator, _ = pin(source, protocol_data["previousProgramSha256"]).decode().partition("\ncontrol = fit(")
assert separator
prior_protocol = prior/"protocollo.json"
pin(prior_protocol, baseline["protocolSha256"])
namespace = {"__file__":str(source)}
sys.argv = [str(source),str(prior_protocol),str(base),str(joint_path),str(dependencies),str(out)]
exec(compile(prefix,str(source),"exec"),namespace)
np = namespace["np"]
design, groups, images, common, samples, aperture, signals, support, assess, joint = (
    namespace[k] for k in ("design","groups","images","common","samples","aperture","signals","support","assess","joint"))
config = namespace["p"]
train = namespace["namespace"]["train"]
signal_bins = namespace["signal_bins"]
assert config["relativeTolerance"] == rule["relativeTolerance"]
assert protocol_data["standardPeakFraction"] == rule["blankTruthMaxFraction"]


def geometry(keep):
    splits = (keep & train, keep & ~train, keep)
    sizes = [int(part.sum()) for part in splits]
    conditions = []
    reason = None
    if (sizes[0] < rule["minimumFitCells"] or sizes[1] < rule["minimumValidationCells"]):
        reason = "INSUFFICIENT_CLEAN_CELLS"
    else:
        for part in splits:
            matrix = design[part]
            if np.linalg.matrix_rank(matrix) != 3:
                reason = "RANK_DEFICIENT"
                break
            conditions.append(float(np.linalg.cond(matrix)))
        if reason is None and max(conditions) > rule["maxDesignCondition"]:
            reason = "CONDITION_EXCEEDED"
    result = {"cleanCellsBySplit":sizes[:2],"cleanCellsTotal":sizes[2],
              "affineConditions":conditions,"reason":reason}
    if reason is None:
        matrix=design[keep]
        inverse=np.linalg.inv(matrix.T @ matrix)
        sample=samples[aperture]
        variance=np.einsum("ij,jk,ik->i",sample,inverse,sample)
        result["maxApertureLeverageSqrt"] = float(np.sqrt(variance.max()))
    return result

masks = {}
geometries = {}
for fraction in protocol_data["peakFractions"]:
    label=f"{fraction:.2f}"
    masks[label], geometries[label] = {}, {}
    for profile,bins in signal_bins.items():
        keep = np.array([np.max(cell) < config["peakAdu"]*fraction for cell in bins])
        masks[label][profile] = keep
        geometries[label][profile] = geometry(keep)

def fit(measures, keep):
    result=[]
    for terms in (1,3):
        coeff,_,rank,_=np.linalg.lstsq(design[keep,:terms],measures[keep],rcond=None)
        assert rank==terms
        result.append(coeff)
    return result

checks = geometry(np.ones(len(groups),dtype=bool))
assert checks["reason"] is None
affirm = fit(design @ np.array([100.,7.,-3.]),np.ones(len(groups),dtype=bool))
np.testing.assert_allclose(affirm[1],[100.,7.,-3.],rtol=0,atol=1e-10)
assert geometry(np.zeros(len(groups),dtype=bool))["reason"]=="INSUFFICIENT_CLEAN_CELLS"
rows = []
for pair in joint["cases"]:
    ref,target = pair["reference"],pair["target"]
    delta = images[target]-images[ref]
    contrast = images[target]-np.median(images[target][common])
    d_bins = [delta[s][valid] for s,valid in zip(groups,support,strict=True)]
    c_bins = [contrast[s][valid] for s,valid in zip(groups,support,strict=True)]
    cases = [("unitControl",None,1.)]
    cases.extend(("jointPass",i,t["scale"]) for i,t in enumerate(pair["trials"]) if t["jointPass"])
    for cohort,index,scale in cases:
        scenario={"cohort":cohort,"reference":ref,"target":target,"priorTrialIndex":index,"scale":scale}
        scaled = [d+(scale-1)*c for d,c in zip(d_bins,c_bins,strict=True)]
        initial = np.array([np.median(d) for d in scaled])
        for name, signal in signals.items():
            changed = np.array([np.median(d+s) for d,s in zip(scaled,signal_bins[name],strict=True)])
            for limit,profiles in masks.items():
                geo=geometries[limit][name]
                row = {**scenario,"profile":name,"peakFraction":limit}
                if geo["reason"] is not None:
                    rows.append({**row,"status":"ABSTAINED","reason":geo["reason"]})
                    continue
                keep=profiles[name]
                evaluated={model:assess(signal,a,b) for model,a,b in
                           zip(("offset","plane"),fit(initial,keep),fit(changed,keep),strict=True)}
                rows.append({**row,"status":"EVALUATED","models":evaluated})

summary={}
for cohort,n in (("jointPass",config["expectedJointTrials"]),("unitControl",config["expectedUnitControls"])):
    summary[cohort]={}
    for limit in masks:
        summary[cohort][limit]={}
        for name in signals:
            cases=[r for r in rows if r["cohort"]==cohort and r["peakFraction"]==limit and r["profile"]==name]
            assert len(cases)==n
            evaluated=[r for r in cases if r["status"]=="EVALUATED"]
            values={"evaluated":len(evaluated),"abstained":n-len(evaluated),"models":{}}
            for model in ("offset","plane"):
                metrics=[r["models"][model] for r in evaluated]
                if metrics:
                    values["models"][model]={
                        "passes":sum(m["pass"] for m in metrics),
                        "medianFluxError":float(np.median([m["relativeFluxError"] for m in metrics])),
                        "medianRelativeL2":float(np.median([m["relativeL2"] for m in metrics])),
                    }
            summary[cohort][limit][name]=values

receipt={"schema":"BKL046_M8M20_KNOWN_PROFILE_MASK_V1","protocolSha256":sha256(raw).hexdigest(),
         "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),"geometry":geometries,
         "unmaskedGeometry":checks,"summary":summary,"nativeExecutions":0,"scientificClosures":0}
full=(json.dumps({**receipt,"results":rows},sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
with (out/"tutti-gli-esiti.json").open("xb") as stream:
    stream.write(full)
receipt["fullReportSha256"]=sha256(full).hexdigest()
with (out/"riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps({"geometry":geometries,"standard":summary["jointPass"]["0.02"]}))
