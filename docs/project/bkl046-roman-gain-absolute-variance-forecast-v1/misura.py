"""Predict absolute Roman aperture variance from exposures disjoint from the target."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import ModuleType

policy, heritage, parent, spatial, channels, packages, out = map(Path, sys.argv[1:])
raw = policy.read_bytes()
cfg = json.loads(raw)


def exact(path, pin):
    data = path.read_bytes()
    if sha256(data).hexdigest() != pin:
        raise ValueError(f"Changed input {path.name}")
    return data


def require(ok, message):
    if not ok:
        raise ValueError(message)


history = json.loads(exact(heritage / "protocollo.json", cfg["heritagePolicy"]))
receipt = json.loads(exact(heritage / "riscontro.json", cfg["heritageReceipt"]))
prior = json.loads(exact(parent / "riscontro.json", history["parentReceipt"]))
settings = json.loads(exact(parent / "protocollo.json", history["parentPolicy"]))
ref_rows = json.loads(exact(parent / "misure" / "tutti-gli-esiti.json", prior["detailSha256"]))
refs = {(r["band"], r["frame"], r["channel"], r["firstExposure"]): r for r in ref_rows}
require(len(refs) == len(ref_rows) == receipt["matchedEndpointsReproduced"] == 1920, "Wrong cohort")
parent_ns = ModuleType("held_pairs")
pcode = parent / "misura.py"
exec(compile(exact(pcode, history["parentCode"]), str(pcode), "exec"), vars(parent_ns))
kernel = ModuleType("kernel")
kcode = channels / "misura.py"
exec(compile(exact(kcode, settings["channelsProgramSHA"]), str(kcode), "exec"), vars(kernel))
capture_path = spatial / "cattura"
capture = json.loads(exact(capture_path / "acquisizione.json", settings["captureSHA"]))
sys.path.insert(0, str(packages))
import numpy as np
require(np.__version__ == "2.3.5", "Wrong NumPy")
levels = settings["frames"][1:]
w = np.outer([.5, 1, .5], [.5, 1, .5]).reshape(9)
diag_gain = float(w@w)


def linear(x0, y0, x1, y1, scale):
    require(x1 > x0, "Nonincreasing training-level signals")
    return float(y0 + (scale-x0)*(y1-y0)/(x1-x0))


require(linear(1., 5., 4., 11., 0.) == 3. and linear(1., 5., 4., 11., 2.) == 7.,
        "Linear fixture failed")
rows = []
for band in settings["bands"]:
    tiles, rails = parent_ns.load_tiles(np, capture_path / "source", capture["captures"], band, settings["frames"])
    for channel, rail in enumerate(rails):
        retain, eligible = kernel.plan_support(np, rail)
        grid = ~rail[:63, :63].reshape(21, 3, 21, 3).swapaxes(1, 2).any(axis=(2, 3))
        metrics, shape_gain = {}, {}
        for level in levels:
            images = [tiles[i, level][channel] - tiles[i, 0][channel] for i in range(1, 21)]
            pairs = list(zip(images[::2], images[1::2], strict=True))
            metrics[level] = [kernel.evaluate(np, a, b, retain, eligible) for a,b in pairs]
            shape_gain[level] = [float(w @ parent_ns.block_covariance(np, (b-a)/np.sqrt(2), grid) @ w)
                                 for a,b in pairs]
        for held in range(10):
            train = [i for i in range(10) if i != held]
            med = {level: {metric: float(np.median([metrics[level][i][metric] for i in train]))
                           for metric in ("signal", "inputVariance", "sumVariance")} for level in levels}
            gain = {level: float(np.mean([shape_gain[level][i] for i in train])) for level in levels}
            for level in levels:
                reference = metrics[level][held]
                anchor = refs[band,level,channel,2*held+1]
                observed = reference["sumVariance"]
                np.testing.assert_allclose(
                    [abs(gain[level]*reference["inputVariance"]/observed-1), reference["fullError"]],
                    [anchor["learnedError"], anchor["independentError"]], atol=1e-12, rtol=0)
                lo, hi = [source for source in levels if source != level]
                x0, x1, x = med[lo]["signal"], med[hi]["signal"], med[level]["signal"]
                raw_prediction = linear(x0, med[lo]["inputVariance"], x1, med[hi]["inputVariance"], x)
                predictions = {
                    "sameLevelIndependent": med[level]["inputVariance"]*diag_gain,
                    "sameLevelCovariance": med[level]["inputVariance"]*gain[level],
                    "sameLevelEmpirical": med[level]["sumVariance"],
                    "otherLevelsEmpiricalLinear": linear(x0, med[lo]["sumVariance"],
                                                         x1, med[hi]["sumVariance"], x),
                    "otherLevelsRawLinearPooledCovariance": raw_prediction*(gain[lo]+gain[hi])/2,
                }
                rows.append(dict(band=band, channel=channel, level=level, firstExposure=held*2+1,
                                 empiricalVariance=observed, predictions=predictions))
require(len(rows) == 1920, "Wrong result grid")
summary = []
for band in settings["bands"]:
    for level in levels:
        matched = [r for r in rows if (r["band"], r["level"]) == (band,level)]
        observation = np.array([r["empiricalVariance"] for r in matched])
        require(len(matched) == 320 and np.all(observation > 0), "Unexpected reference coverage")
        pair_ids = np.array([r["firstExposure"] for r in matched])
        models = {}
        for name in matched[0]["predictions"]:
            values = np.array([r["predictions"][name] for r in matched])
            require(np.all(np.isfinite(values)), "Nonfinite variance prediction")
            signed = values/observation - 1
            errors = abs(signed)
            models[name] = dict(medianError=float(np.median(errors)), p95Error=float(np.quantile(errors,.95)),
                                medianSignedError=float(np.median(signed)), nonpositive=int((values <= 0).sum()),
                                pairMedianErrors=[float(np.median(errors[pair_ids == i])) for i in range(1,21,2)])
        summary.append(dict(band=band, level=level, comparisons=len(matched), models=models))
out.mkdir()
detail = parent_ns.save(out / "dettaglio.json", rows)
parent_ns.save(out / "riscontro.json", dict(schema=cfg["schema"], protocolSha256=sha256(raw).hexdigest(),
               programSha256=sha256(Path(__file__).read_bytes()).hexdigest(), detailSha256=detail,
               referenceRowsVerified=len(rows), summary=summary, incidentDoseVerified=False,
               nativeExecutions=0, scientificClosures=0))
