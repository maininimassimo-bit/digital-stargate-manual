"""Measure the sensitivity of Roman variance transfer to pairs and readout blocks."""
from hashlib import sha256
import json
from pathlib import Path
import sys

config, parent, packages, output = map(Path, sys.argv[1:])
raw = config.read_bytes()
plan = json.loads(raw)


def exact(path, expected):
    data = path.read_bytes()
    if sha256(data).hexdigest() != expected:
        raise ValueError(f"Changed input {path.name}")
    return json.loads(data)


receipt = exact(parent/"riscontro.json", plan["parentReport"])
details = exact(parent/"dettaglio.json", plan["detail"])
if receipt["detailSha256"] != plan["detail"] or len(details) != 2880:
    raise ValueError("Unexpected cohort")
sys.path.insert(0, str(packages))
import numpy as np
if np.__version__ != "2.3.5":
    raise ValueError("Wrong NumPy")

bands = ("lower", "upper")
models = ("lin0Empirical", "gainEmpirical", "gainRawCovariance", "gainRawIndependent")
cohort = {(r["band"], r["firstExposure"],r["channel"]):r for r in details if r["state"] == "MEASURED"}
if len(cohort) != 960 or sum(r["state"] == "MEASURED" for r in details) != 960:
    raise ValueError("Unexpected eligibility grid")
errors = np.asarray([[[[abs(row[m]/row["targetVariance"] - 1) for m in models]
                        for row in [cohort[b,p,c] for c in range(32)]]
                       for p in range(1,30,2)] for b in bands])
if not np.isfinite(errors).all():
    raise ValueError("Invalid error values")

q = (.5,.95)
point = np.quantile(errors, q, axis=(1,2))
previous = {(r["band"],r["frame"]):r for r in receipt["summary"]}
baseline = np.array([[[previous[b,1]["models"][m][k] for m in models] for b in bands]
                     for k in ("medianAbsolute","p95Absolute")])
np.testing.assert_allclose(point,baseline,atol=1e-12,rtol=0)


def contrast(quantile):
    return 100*(quantile[...,1:] - quantile[...,:1])


seed = np.random.default_rng(plan["seed"])
replicates = plan["replicates"]
pair_draw = seed.integers(0,15,size=(replicates,15))
channels = {"pairsOnly": np.broadcast_to(np.arange(32),(replicates,32))}
for width in plan["channelBlockSizes"]:
    count = 32//width
    blocks = seed.integers(0,count,size=(replicates,count))
    channels[f"pairsAndChannels{width}"] = (blocks[...,None]*width + np.arange(width)).reshape(-1,32)
row_count = 15*32
observations = errors.reshape(2,row_count,4)
distributions = {}
for name, draw in channels.items():
    result = []
    for start in range(0,replicates,128):
        end = min(start+128,replicates)
        indices = (pair_draw[start:end,:,None]*32 + draw[start:end,None,:]).reshape(-1,row_count)
        sample = observations[:,indices]
        result.append(contrast(np.quantile(sample,q,axis=2)))
    distributions[name] = np.concatenate(result,axis=2)
omissions = np.stack([contrast(np.quantile(np.delete(errors,i,axis=1),q,axis=(1,2)))
                      for i in range(15)],axis=2)
summary = []
for j, percentile in enumerate((50,95)):
    for i, band in enumerate(bands):
        for k, model in enumerate(models[1:]):
            intervals = {name:np.quantile(values[j,i,:,k],(.025,.975)).tolist()
                         for name,values in distributions.items()}
            values = omissions[j,i,:,k]
            extrema = [*values,*(bound for pair in intervals.values() for bound in pair)]
            direction = "gainLower" if max(extrema) < 0 else ("lin0Lower" if min(extrema) > 0 else "mixed")
            summary.append(dict(band=band, percentile=percentile, model=model,
                                differencePercentagePoints=float(contrast(point)[j,i,k]),
                                intervals=intervals, leaveOnePair=[float(values.min()),float(values.max())],
                                robustDirection=direction))
report = dict(schema=plan["schema"], protocolSha256=sha256(raw).hexdigest(),
              parentReceiptSha256=plan["parentReport"], cohort=960,
              outsideGainRangeRetained=1920, exposurePairs=15, channels=32, summary=summary,
              nativeExecutions=0, scientificClosures=0)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
