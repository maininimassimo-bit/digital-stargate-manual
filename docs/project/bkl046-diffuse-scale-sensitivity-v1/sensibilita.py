from hashlib import sha256
import json
from pathlib import Path
import sys

scope, field, previous, capture, stars, deps, wheel, vc, output = sys.argv[1:]
scope, previous, output = map(Path,(scope,previous,output))
path = scope/"protocollo.json"
p_bytes = path.read_bytes()
p_hash = sha256(p_bytes).hexdigest()
assert p_hash == "b8c4dead4aec23b0034a948b71e18e0ae06e74e75e01b8cd297e44580d5d3baf"
p = json.loads(p_bytes)
field_pin = p["fields"][field]
past_bytes = (previous/"riscontro.json").read_bytes()
assert sha256(past_bytes).hexdigest() == field_pin["report"]
past = json.loads(past_bytes)
assert past["protocolSha256"] == field_pin["protocol"]
base_file = previous/"riferimenti.py"
base_bytes = base_file.read_bytes()
assert sha256(base_bytes).hexdigest() == past["programSha256"]
source = base_bytes.decode()
delimiter = "\ncomparisons = []\n"
assert source.count(delimiter) == 1
prefix = source.split(delimiter,1)[0]
base_args = [str(previous),capture,stars, deps, str(output)]
if field == "IC1805":
    base_args = [str(previous),capture,stars,wheel,deps,vc,str(output)]
namespace = {"__file__":str(base_file)}
sys.argv = [str(base_file),*base_args]
exec(compile(prefix,str(base_file),"exec"),namespace)
np = namespace["np"]
refs, targets = namespace["refs"],namespace["targets"]
design, train = namespace["design"],namespace["train"]
images, groups, common = [namespace[k] for k in ("images","groups","common")]
scores = namespace["scores"]
assert refs == past["references"] and targets == past["targets"]
assert len(past["cases"]) == field_pin["pairs"]
baseline = {(r["referenceIndex"],r["targetIndex"]): r for r in past["cases"]}
results = []
for target in targets:
    # Removing the common-support median changes only the additive intercept.
    contrast = images[target] - np.median(images[target][common])
    for ref in refs:
        difference = images[target] - images[ref]
        previous_case = baseline[(ref,target)]
        runs = []
        for scale in p["scales"]:
            trial = difference + (scale-1)*contrast
            measures = np.array([np.median(trial[s][common[s]]) for s in groups])
            folds = []
            for i,select in enumerate((train,~train)):
                offset, plane = [scores(design,measures,select,k) for k in (1,3)]
                passed = (plane["medianAbsoluteADU"] <= .9*offset["medianAbsoluteADU"]
                          and plane["p90AbsoluteADU"] <= offset["p90AbsoluteADU"])
                folds.append({"trainParity":i,"offset":offset,"plane":plane,"pass":passed})
            if scale == 1:
                assert folds == previous_case["folds"]
            runs.append({"scale":scale,"folds":folds,"passedBoth":all(f["pass"] for f in folds)})
        results.append({"reference":ref,"target":target,"cases":runs})
summary = []
for k,scale in enumerate(p["scales"]):
    true_nominal, true_trial, gained, lost = 0,0,0,0
    p90_delta = []
    for row in results:
        nominal = row["cases"][p["scales"].index(1)]
        perturbed = row["cases"][k]
        n, t = nominal["passedBoth"],perturbed["passedBoth"]
        true_nominal += n
        true_trial += t
        gained += (not n and t)
        lost += (n and not t)
        for f,g in zip(nominal["folds"],perturbed["folds"],strict=True):
            p90_delta.append(abs(f["plane"]["p90AbsoluteADU"]-g["plane"]["p90AbsoluteADU"]))
    summary.append({"scale":scale,"nominalPassingPairs":true_nominal,"passingPairs":true_trial,
                    "changedFromFailToPass":gained,"changedFromPassToFail":lost,
                    "p90FoldAbsoluteChangeInPlaneP90ADU":float(np.quantile(p90_delta,.9))})
result = dict(schema="BKL046_DIFFUSE_SCALE_SENSITIVITY_V1", field=field, protocolSha256=p_hash,
              priorReportSha256=field_pin["report"], programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
              exactPriorFoldsReproduced=len(results)*2, results=results,summary=summary,
              nativeExecutions=0,scientificClosures=0)
output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8",newline="\n")
