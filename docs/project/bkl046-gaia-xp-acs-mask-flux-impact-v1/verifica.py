"""Quantify the effect of an eight-sample Gaia XP omission on ACS band estimates."""
import ast
from hashlib import sha256
from io import BytesIO
from itertools import combinations
import json
from pathlib import Path
import runpy
import sys
from zipfile import ZipFile

import numpy as np

PIN = "18b11860d6d97076737eb130320e475d832f0d05318d3e56c244030a125ba423"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pinned(path, expected):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == expected, "Digest mismatch")
    return data


def functions(path, expected):
    code = pinned(path, expected)
    namespace = {"__name__": "verified_module", "__file__": str(path)}
    exec(compile(code, str(path), "exec"), namespace)
    return namespace


def function(nodes, name):
    return next(node for node in nodes if isinstance(node, ast.FunctionDef) and node.name == name)


def weights(acs_dir, plan, grid):
    prior = json.loads(pinned(acs_dir / "protocol.json", plan["acsProtocolSha256"]))
    source = ast.parse(pinned(acs_dir / "measure.py", prior["runnerSha256"]))
    integration = function(function(source.body, "main").body, "integration")
    env = {"np": np, "grid": grid}
    exec(compile(ast.Module(body=[integration], type_ignores=[]), "verified-integration", "exec"), env)
    sys.path.insert(0, prior["packages"])
    from astropy.io import fits
    helper = Path(prior["helper"])
    pinned(helper, prior["helperSha256"])
    runtime = runpy.run_path(str(helper))
    require(runtime["EPOCH"] == prior["epochMjd"], "ACS epoch changed")
    path = Path(prior["capture"])
    capture = json.loads(pinned(path, prior["captureSha256"]))
    require(capture["routes"] == prior["routes"], "ACS paths changed")
    components = {}
    for name in sorted({item for route in prior["routes"].values() for item in route}):
        pinned(path.parent / name, capture["components"][name]["sha256"])
        wave, transmission = runtime["throughput"](np, fits, name)
        components[name] = (wave / 10, transmission)
    design = []
    for name in plan["filters"]:
        chain = [components[item] for item in prior["routes"][name]]
        a, b = [env["integration"](chain, order) for order in plan["quadratureOrders"]]
        np.testing.assert_allclose(a[0], b[0], rtol=1e-9, atol=1e-12)
        np.testing.assert_allclose(a[1], b[1], rtol=1e-9, atol=1e-12)
        design.append(a[0])
    return np.stack(design)


def summarize(flux, covariance, reconstructed, design, mask, labels):
    masked = design.copy()
    masked[:, mask] = 0.
    total = design @ flux
    kept = masked @ flux
    require((total > 0).all() and (kept > 0).all(), "Nonpositive flux")
    scales = np.sqrt(np.diag(covariance))
    historical = reconstructed * np.outer(scales, scales)
    full = design @ covariance @ design.T
    conditional = masked @ covariance @ masked.T
    historical_masked = masked @ historical @ masked.T
    require(all((np.diag(x) > 0).all() for x in (full, conditional, historical_masked)),
            "Nonpositive projected variance")
    bands = {}
    for i, name in enumerate(labels):
        before = np.sqrt(full[i, i]) / total[i]
        after = np.sqrt(conditional[i, i]) / kept[i]
        bands[name] = dict(fractionFluxOmitted=float(1 - kept[i]/total[i]),
                           fractionDesignWeightOmitted=float(1 - masked[i].sum()/design[i].sum()),
                           relativeSigmaFullConditional=float(before),
                           relativeSigmaMaskedConditional=float(after),
                           relativeSigmaMaskedHistorical=float(np.sqrt(historical_masked[i, i])/kept[i]),
                           maskedToFullConditionalSigma=float(after/before))
    pairs = {}
    for i, j in combinations(range(len(labels)), 2):
        a, b = total[i], total[j]
        c, d = kept[i], kept[j]
        def relative_sigma(matrix, numerator, denominator):
            variance = (matrix[i, i]/numerator**2 + matrix[j, j]/denominator**2
                        - 2*matrix[i, j]/(numerator*denominator))
            require(variance > 0, "Nonpositive variance of log flux ratio")
            return float(np.sqrt(variance))
        base = relative_sigma(full, a, b)
        after = relative_sigma(conditional, c, d)
        pairs[labels[i] + "/" + labels[j]] = dict(
            relativeRatioChange=float((c/d)/(a/b)-1),
            relativeSigmaFullConditional=base,
            relativeSigmaMaskedConditional=after,
            relativeSigmaMaskedHistorical=relative_sigma(historical_masked, c, d),
            maskedToFullConditionalSigma=after/base)
    return bands, pairs


def main():
    (protocol, mask_dir, cohort_dir, collector_path, support_path, cohort_sources,
     capsule_path, acs_dir, out) = map(Path, sys.argv[1:])
    plan = json.loads(pinned(protocol, PIN))
    mask_plan = json.loads(pinned(mask_dir / "protocollo.json", plan["maskProtocolSha256"]))
    mask_receipt = json.loads(pinned(mask_dir / "riscontro.json", plan["maskReceiptSha256"]))
    cp = json.loads(pinned(cohort_dir / "protocollo.json", plan["cohortProtocolSha256"]))
    require(np.__version__ == cp["numpy"] and mask_receipt["fixedMasksPassing"] == 4, "Mask premise changed")
    correl = functions(support_path, cp["supportRunnerSha256"])["correlation"]
    collect = functions(collector_path, cp["cohortCollectorSha256"])["collect_inputs"]
    previous = json.loads(pinned(cohort_sources / "riscontro.json", cp["cohortReportSha256"]))["cases"]
    actual, inputs = collect(cohort_sources, cp["cohortRunnerSha256"])
    require(actual == previous and set(inputs) == set(previous), "Cohort replay differs")
    with ZipFile(BytesIO(pinned(capsule_path, mask_plan["historicalCapsuleSha256"]))) as z:
        blob = z.read("objects/Matrici-GaiaXPy-campionamento-reale-v1.npz")
    require(sha256(blob).hexdigest() == mask_plan["historicalMatrixSha256"], "Historical matrix changed")
    with np.load(BytesIO(blob), allow_pickle=False) as data:
        grid = data["gridNm"]
        arrays = [(data["predictedFlux"], data["conditionalCovariance"],
                   correl(data["pinnedSourceCovariance"], True))]
    for identity in sorted(inputs):
        wavelengths, flux, _, conditional, corr, _ = inputs[identity]
        require(np.array_equal(grid, wavelengths), "Wavelengths differ")
        arrays.append((flux, conditional, corr))
    start, width = mask_plan["startIndex"], mask_plan["width"]
    mask = slice(start, start + width)
    require(grid.shape == (mask_plan["size"],) and len(arrays) == 4
            and [float(grid[start]), float(grid[start+width-1])] == mask_receipt["fixedWindowNm"],
            "Wavelength mask differs")
    design = weights(acs_dir, plan, grid)
    fixture_design = np.array([[1., 0., 0.], [0., 1., 0.]])
    channels, pairs = summarize(np.ones(3), np.eye(3), np.eye(3), fixture_design,
                                slice(2,3), ("a","b"))
    require(channels["a"]["fractionFluxOmitted"] == 0 and pairs["a/b"]["relativeRatioChange"] == 0,
            "Unaffected band fixture failed")
    rows = []
    for number, (flux, cond, corr) in enumerate(arrays):
        bands, pairs = summarize(flux, cond, corr, design, mask, plan["filters"])
        rows.append(dict(case="v571" if number == 0 else number, bands=bands, pairs=pairs))
    result = dict(schema="BKL046_GAIAXP_ACS_MASK_IMPACT_RESULT_V1", protocolSha256=PIN,
                  sampleWindowNm=mask_receipt["fixedWindowNm"], sampleCount=width, sources=rows,
                  passbandsRenormalized=False, samePassbandAfterMask=False,
                  systematicCalibrationIncluded=False, externalPhotometryVerified=False,
                  scientificClosures=0, nativeExecutions=0)
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
