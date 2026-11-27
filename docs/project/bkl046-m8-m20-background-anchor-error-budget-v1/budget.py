"""Compute exact finite-box error budgets for independent background anchors."""
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

protocol, injection, base, joint, dependencies, output = map(Path,sys.argv[1:])
raw = protocol.read_bytes()
study = json.loads(raw)

def read(path, pin):
    data = path.read_bytes()
    if sha256(data).hexdigest() != pin:
        raise ValueError("SOURCE_CHANGED:" + path.name)
    return data

injection_report = json.loads(read(injection/"riscontro.json", study["injectionReportSha256"]))
injection_protocol = injection/"protocollo.json"
read(injection_protocol,injection_report["protocolSha256"])
source = injection/"iniezioni.py"
prefix, separator, _ = read(source,study["injectionProgramSha256"]).decode().partition("\ncontrol = fit(")
assert separator
scope={"__file__":str(source)}
sys.argv=[str(source),str(injection_protocol),str(base),str(joint),str(dependencies),str(output)]
exec(compile(prefix,str(source),"exec"),scope)
np=scope["np"]
samples, aperture, profiles, parameters = (scope[k] for k in ("samples","aperture","signals","p"))
target = parameters["relativeTolerance"]
ap = samples[aperture]
assert aperture.sum()>0 and len(profiles)==3
corners=np.array(list(product((-1.,1.),repeat=6)))
assert len(corners)==64

results={}
for layout,anchors in study["anchorLayouts"].items():
    assert len(anchors)==6 and len(set(map(tuple,anchors)))==6
    coordinates=np.array(anchors)
    assert np.abs(coordinates).max()<=1
    full_design=np.column_stack((np.ones(len(anchors)),coordinates))
    results[layout]={}
    for model,terms in (("offset",1),("plane",3)):
        design=full_design[:,:terms]
        if np.linalg.matrix_rank(design)!=terms:
            results[layout][model]={"status":"ABSTAIN_RANK_DEFICIENT"}
            continue
        inv=np.linalg.pinv(design)
        true_coeff=np.array([100.,7.,-3.])[:terms]
        np.testing.assert_allclose(inv@(design@true_coeff),true_coeff,atol=1e-10,rtol=0)
        trial_coeff=corners@inv.T
        moment=ap[:,:terms].sum(axis=0)
        gram=samples[:,:terms].T@samples[:,:terms]
        worst_flux=np.max(np.abs(trial_coeff@moment))
        worst_l2=np.sqrt(np.max(np.einsum("ij,jk,ik->i",trial_coeff,gram,trial_coeff)))
        # Verify the quadratic moment reduction against direct detector readback.
        check=trial_coeff[13]
        np.testing.assert_allclose(check@gram@check,np.sum((samples[:,:terms]@check)**2),rtol=1e-12)
        # A common +1 ADU anchor bias must propagate as a +1 ADU sky offset.
        np.testing.assert_allclose(inv@np.ones(6),np.eye(terms)[0],rtol=0,atol=1e-12)
        budgets={}
        for name,signal in profiles.items():
            flux_amp=float(worst_flux/signal[aperture].sum())
            l2_amp=float(worst_l2/np.linalg.norm(signal))
            budget=min(target/flux_amp,target/l2_amp)
            budgets[name]={
              "maxAdmissiblePerAnchorErrorAdu":budget,
              "worstRelativeFluxPerAdu":flux_amp,"worstRelativeL2PerAdu":l2_amp,
              "candidateBounds":[{"anchorErrorAdu":b,"worstRelativeFlux":b*flux_amp,
                 "worstRelativeL2":b*l2_amp,"bothWithinTolerance":b<=budget}
                 for b in study["candidateBoundsAdu"]],
            }
        results[layout][model]={"status":"EVALUATED","condition":float(np.linalg.cond(design)),
          "verticesChecked":len(corners),"profiles":budgets}

report={"schema":"BKL046_M8M20_INDEPENDENT_BACKGROUND_ANCHOR_ERROR_V1",
        "protocolSha256":sha256(raw).hexdigest(),"programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),
        "source":study["injectionReportSha256"],"supportSamples":len(samples),"apertureSamples":int(aperture.sum()),
        "layouts":results,"realAnchorsMeasured":0,"nativeExecutions":0,"scientificClosures":0}
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps({layout:{model:{name:q["maxAdmissiblePerAnchorErrorAdu"] for name,q in r.get("profiles",{}).items()}
                   for model,r in result.items()} for layout,result in results.items()}))
