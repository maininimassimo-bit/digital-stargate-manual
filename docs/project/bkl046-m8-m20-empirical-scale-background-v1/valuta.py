from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

root, base, cap, stars, deps, scales, out = map(Path,sys.argv[1:])
raw = (root/"protocollo.json").read_bytes()
p_hash = sha256(raw).hexdigest()
assert p_hash == "19e2c4afaf9de25e5e3299bdaf64a1285941ef32cdff860b3b035951ebc9c9f2"
p = json.loads(raw)

def get(path,key):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == p[key],path
    return json.loads(raw)

prior = get(base/"riscontro.json","baseReport")
stellar = get(scales,"scaleReport")
assert stellar["authorities"]["pairs"] == p["baseReport"]
script = base/"riferimenti.py"
script_raw = script.read_bytes()
assert sha256(script_raw).hexdigest() == prior["programSha256"]
prefix, delimiter, _ = script_raw.decode().partition("\ncomparisons = []\n")
assert delimiter
scope = {"__file__":str(script)}
sys.argv = [str(script), *map(str,(base,cap,stars,deps,out))]
exec(compile(prefix,str(script),"exec"),scope)
np = scope["np"]
images,common,groups,design,train,scores = (scope[k] for k in ("images","common","groups","design","train","scores"))
empirical = {(r["referenceIndex"],r["targetIndex"]):r for r in stellar["rows"]}
assert set(empirical) == set(product(scope["refs"],scope["targets"]))
assert len(empirical) == len(prior["cases"]) == p["expectedPairs"]

results = []
for case in prior["cases"]:
    ref,target = case["referenceIndex"],case["targetIndex"]
    difference = images[target]-images[ref]
    contrast = images[target]-np.median(images[target][common])
    diff_bins = [difference[s][common[s]] for s in groups]
    contrast_bins = [contrast[s][common[s]] for s in groups]

    def evaluate(scale):
        measures = np.array([np.median(d+(scale-1)*c) for d,c in zip(diff_bins,contrast_bins,strict=True)])
        scores_by_fold = []
        for i,select in enumerate((train,~train)):
            offset, plane = [scores(design,measures,select,k) for k in (1,3)]
            passed = (plane["medianAbsoluteADU"] <= (1-p["minimumMedianImprovement"])*offset["medianAbsoluteADU"]
                      and plane["p90AbsoluteADU"] <= offset["p90AbsoluteADU"])
            scores_by_fold.append({"trainParity":i,"offset":offset,"plane":plane,"pass":passed})
        return scores_by_fold

    unit = evaluate(1)
    assert unit == case["folds"]
    tests = []
    source = empirical[(ref,target)]
    variants = source["variants"]
    assert len(variants) == p["variants"]
    for variant in variants:
        assert len(variant["folds"]) == p["withheldTiles"]
        measured = [(None,variant["fullScale"])]
        measured.extend((fold["withheldTile"],fold["fittedScale"]) for fold in variant["folds"])
        for tile,scale in measured:
            folds = evaluate(scale)
            tests.append({"parity":variant["parity"],"calibration":variant["calibration"],"center":variant["center"],
                          "withheldTile":tile,"scale":scale,"folds":folds,"passBoth":all(f["pass"] for f in folds)})
    passed = sum(t["passBoth"] for t in tests)
    status = "allPass" if passed == len(tests) else "mixed" if passed else "allFail"
    results.append({"ref":ref,"target":target,"unitPass":case["passBothFolds"],"passesWithStellarScale":passed,
                    "stellarScaleCount":len(tests),"status":status,"unitFolds":unit,"trials":tests})

stats = {
    "pairs":len(results),
    "empiricalTrials":sum(r["stellarScaleCount"] for r in results),
    "unitPass":sum(r["unitPass"] for r in results),
    "alwaysOppositeToUnit":sum((r["unitPass"] and r["status"]=="allFail")
                               or (not r["unitPass"] and r["status"]=="allPass") for r in results),
    "counts":{s:sum(r["status"]==s for r in results) for s in ("allPass","allFail","mixed")},
    "byReference":[{"index":i, "scenarios":{s:sum(r["ref"]==i and r["status"]==s for r in results)
                                          for s in ("allPass","allFail","mixed")}}
                   for i in scope["refs"]],
}
common_fields = dict(schema="BKL046_M8_M20_EMPIRICAL_SCALE_BACKGROUND_V1", protocolSha256=p_hash,
                     sourceScaleSha256=p["scaleReport"], sourceBackgroundSha256=p["baseReport"],
                     programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                     nativeExecutions=0,scientificClosures=0)
full = {**common_fields,"summary":stats,"cases":results}
full_bytes = (json.dumps(full,sort_keys=True,separators=(",",":"))+"\n").encode()
out.write_bytes(full_bytes)
public = {**common_fields,"summary":stats,"fullReportSha256":sha256(full_bytes).hexdigest(),
          "pairs":[{k:r[k] for k in ("ref","target","unitPass","stellarScaleCount","passesWithStellarScale","status")}
                   for r in results]}
out.with_name("riscontro.json").write_bytes((json.dumps(public,sort_keys=True,indent=2)+"\n").encode())
print(json.dumps(stats))
