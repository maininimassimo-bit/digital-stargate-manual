"""Test weak-signal preservation on the M8/M20 common-support grid."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, base, joint_path, dependencies, output = map(Path, sys.argv[1:])
protocol_raw = protocol.read_bytes()
p = json.loads(protocol_raw)

def pinned(path, expected):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected:
        raise ValueError("SOURCE_CHANGED:" + path.name)
    return raw

joint = json.loads(pinned(joint_path, p["priorJointSha256"]))
reference = json.loads(pinned(base / "riscontro.json", p["referenceSha256"]))
source = base / "riferimenti.py"
boot, marker, _ = pinned(source, reference["programSha256"]).decode().partition("\ncomparisons = []\n")
assert marker and joint["sources"]["reference"] == p["referenceSha256"]
namespace = {"__file__":str(source)}
sys.argv = [str(source),str(base),str(base/"capture"),str(base/"stellar"/"riscontro.json"),
            str(dependencies),str(output)]
exec(compile(boot,str(source),"exec"),namespace)
np = namespace["np"]
images, common, groups, design, basis, x, y = (
    namespace[k] for k in ("images","common","groups","design","basis","x","y"))
aperture = (x**2 + y**2 <= p["apertureRadius"]**2)[common]
samples = basis[common]
signals = {r["name"]:p["peakAdu"]*np.exp(-.5*((x/r["sigmaX"])**2+(y/r["sigmaY"])**2))
           for r in p["profiles"]}
support = [common[s] for s in groups]
signal_bins = {name:[signal[s][valid] for s,valid in zip(groups,support,strict=True)]
               for name,signal in signals.items()}
signals = {name:signal[common] for name,signal in signals.items()}
assert len(joint["cases"]) == p["expectedUnitControls"] and len(groups) == 192

def fit(data):
    result = []
    for terms in (1,3):
        coeff, _, rank, _ = np.linalg.lstsq(design[:,:terms],data,rcond=None)
        assert rank == terms
        result.append(coeff)
    return result

def assess(signal, before, after):
    # Analytical evaluation of (injected image - refit) - (original image - original fit).
    fitted_change = before - after
    terms = len(fitted_change)
    adjustment = samples[:,:terms] @ fitted_change
    flux_error = float(adjustment[aperture].sum()/signal[aperture].sum())
    l2 = float(np.sqrt(np.sum(adjustment**2)/np.sum(signal**2)))
    return {"relativeFluxError":flux_error,"relativeL2":l2,
            "pass":max(abs(flux_error),l2)<=p["relativeTolerance"]}

control = fit(design @ np.array([100.,7.,-3.]))
np.testing.assert_allclose(control[1], [100.,7.,-3.],rtol=0,atol=1e-10)
assert assess(signals["broadDiffuse"],control[1],control[1]) == {
    "relativeFluxError":0.,"relativeL2":0.,"pass":True}
rows = []
scenarios = []
for pair in joint["cases"]:
    ref,target = pair["reference"],pair["target"]
    delta = images[target]-images[ref]
    contrast = images[target]-np.median(images[target][common])
    d_bins = [delta[s][valid] for s,valid in zip(groups,support,strict=True)]
    c_bins = [contrast[s][valid] for s,valid in zip(groups,support,strict=True)]
    cases = [("unitControl",None,1.)]
    cases.extend(("jointPass",i,r["scale"]) for i,r in enumerate(pair["trials"]) if r["jointPass"])
    for cohort,index,scale in cases:
        assert np.isfinite(scale) and scale > 0
        scenario = {"cohort":cohort,"reference":ref,"target":target,"priorTrialIndex":index,"scale":scale}
        scenarios.append(scenario)
        original_bins = [d+(scale-1)*c for d,c in zip(d_bins,c_bins,strict=True)]
        original = fit(np.array([np.median(q) for q in original_bins]))
        for name, signal in signals.items():
            added = fit(np.array([np.median(q+s) for q,s in zip(original_bins,signal_bins[name],strict=True)]))
            models = {model:assess(signal,before,after)
                      for model,before,after in zip(("offset","plane"),original,added,strict=True)}
            rows.append({**scenario,"profile":name,"models":models})

summary = {}
for cohort,count in (("unitControl",p["expectedUnitControls"]),("jointPass",p["expectedJointTrials"])):
    assert sum(r["cohort"] == cohort for r in scenarios)==count
    profiles = {}
    for name in signals:
        cases = [r for r in rows if r["cohort"]==cohort and r["profile"]==name]
        assert len(cases)==count
        profiles[name] = {model: {
            "passes":sum(r["models"][model]["pass"] for r in cases),
            "medianFluxError":float(np.median([r["models"][model]["relativeFluxError"] for r in cases])),
            "medianRelativeL2":float(np.median([r["models"][model]["relativeL2"] for r in cases])),
        } for model in ("offset","plane")}
    summary[cohort] = {"scenarios":count,"profiles":profiles}

common_fields = {"schema":"BKL046_M8M20_SCALE_EDGE_DIFFUSE_INJECTION_V1",
    "protocolSha256":sha256(protocol_raw).hexdigest(),
    "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),
    "jointSourceSha256":p["priorJointSha256"], "summary":summary,"nativeExecutions":0,"scientificClosures":0}
full = (json.dumps({**common_fields,"results":rows},sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
with (output/"tutti-gli-esiti.json").open("xb") as stream:
    stream.write(full)
receipt = {**common_fields,"fullReportSha256":sha256(full).hexdigest()}
with (output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps(summary,sort_keys=True))
