"""Test transfer of covariance shape across sampled Roman GAIN ramp levels."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import ModuleType

policy, parent, spatial, channels, packages, out = map(Path, sys.argv[1:])
protocol = policy.read_bytes()
cfg = json.loads(protocol)


def exact(path, pin):
    data = path.read_bytes()
    if sha256(data).hexdigest() != pin:
        raise ValueError(f"Changed input {path.name}")
    return data


def require(ok, message):
    if not ok:
        raise ValueError(message)


parent_ns = ModuleType("held_pair")
pcode = parent / "misura.py"
exec(compile(exact(pcode, cfg["parentCode"]), str(pcode), "exec"), vars(parent_ns))
prior = json.loads(exact(parent / "riscontro.json", cfg["parentReceipt"]))
parent_cfg = json.loads(exact(parent / "protocollo.json", cfg["parentPolicy"]))
details = json.loads(exact(parent / "misure" / "tutti-gli-esiti.json", prior["detailSha256"]))
keyed = {(row["band"], row["frame"], row["channel"], row["firstExposure"]): row for row in details}
require(len(keyed) == len(details) == 1920, "Changed held-out grid")
kernel = ModuleType("kernel")
kcode = channels / "misura.py"
exec(compile(exact(kcode, parent_cfg["channelsProgramSHA"]), str(kcode), "exec"), vars(kernel))
capture_path = spatial / "cattura"
capture = json.loads(exact(capture_path / "acquisizione.json", parent_cfg["captureSHA"]))
sys.path.insert(0, str(packages))
import numpy as np
require(np.__version__ == "2.3.5", "Changed NumPy")
frames = parent_cfg["frames"]
levels = frames[1:]
pair_indices = tuple(range(10))
w = np.outer([.5, 1, .5], [.5, 1, .5]).reshape(9)

rows = []
for band in parent_cfg["bands"]:
    tiles, rails = parent_ns.load_tiles(np, capture_path / "source", capture["captures"], band, frames)
    for c, rail in enumerate(rails):
        mask, support = kernel.plan_support(np, rail)
        grid = ~rail[:63, :63].reshape(21, 3, 21, 3).swapaxes(1, 2).any(axis=(2, 3))
        pairs, covariances = {}, {}
        for level in levels:
            values = [tiles[i, level][c] - tiles[i, 0][c] for i in range(1, 21)]
            pairs[level] = list(zip(values[::2], values[1::2], strict=True))
            covariances[level] = [parent_ns.block_covariance(np, (b-a) / np.sqrt(2), grid)
                                  for a, b in pairs[level]]
        for p in pair_indices:
            train = [i for i in pair_indices if i != p]
            require(len(train) == 9, "Wrong training pair exclusion")
            shapes = {level: np.mean([covariances[level][i] for i in train], axis=0)
                      for level in levels}
            for target in levels:
                a, b = pairs[target][p]
                measured = kernel.evaluate(np, a, b, mask, support)
                ref = keyed[band, target, c, 2*p+1]
                scale = measured["inputVariance"] / measured["sumVariance"]
                errors = {str(level): float(abs(scale * (w @ shape @ w) - 1))
                          for level, shape in shapes.items()}
                np.testing.assert_allclose([errors[str(target)], measured["fullError"]],
                                           [ref["learnedError"], ref["independentError"]], atol=1e-12, rtol=0)
                alternatives = [shapes[level] for level in levels if level != target]
                pooled = float(abs(scale * (w @ np.mean(alternatives, axis=0) @ w) - 1))
                rows.append(dict(band=band, channel=c, target=target, firstExposure=2*p+1,
                                 independent=ref["independentError"], matched=ref["learnedError"],
                                 perLevel=errors, pooledOther=pooled))

require(len(rows) == len(keyed), "Incomplete replay")
summary = []
for band in parent_cfg["bands"]:
    for target in levels:
        group = [row for row in rows if row["band"] == band and row["target"] == target]
        require(len(group) == 320, "Incomplete summary cells")
        match = np.asarray([r["matched"] for r in group])
        independent = np.asarray([r["independent"] for r in group])
        exposure = np.asarray([r["firstExposure"] for r in group])
        alternatives = {str(level): np.asarray([r["perLevel"][str(level)] for r in group])
                        for level in levels if level != target}
        alternatives["pooledOther"] = np.asarray([r["pooledOther"] for r in group])
        comparisons = {"independent": independent, "matched": match, **alternatives}
        summary.append(dict(band=band, target=target, rows=len(group),
                            models={name: dict(median=float(np.median(values)),
                                               p95=float(np.quantile(values, .95)),
                                               pairMediansBetterThanMatched=sum(
                                                   bool(np.median(values[exposure == i]) < np.median(match[exposure == i]))
                                                   for i in range(1, 21, 2)))
                                    for name, values in comparisons.items()}))
out.mkdir()
detail = parent_ns.save(out / "dettaglio.json", rows)
parent_ns.save(out / "riscontro.json", dict(schema=cfg["schema"], protocolSha256=sha256(protocol).hexdigest(),
               programSha256=sha256(Path(__file__).read_bytes()).hexdigest(), detailSha256=detail,
               matchedEndpointsReproduced=len(rows), summary=summary, incidentDoseVerified=False,
               nativeExecutions=0, scientificClosures=0))
