"""Test historical Gaia correlation window against a pinned three-source cohort."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np

PLAN_PIN = "5689907d721d4ee9b0b2a9bcb19969ef155711a24ac8baa1d227739ffe782754"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(path, expected):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == expected, "Input digest changed")
    return data


def load_functions(path, expected):
    raw = pinned(path, expected)
    namespace = {"__name__": "frozen_module", "__file__": str(path)}
    exec(compile(raw, str(path), "exec"), namespace)
    return namespace


def main():
    protocol, collector, support, cohort, out = map(Path, sys.argv[1:])
    plan = json.loads(pinned(protocol, PLAN_PIN))
    require(np.__version__ == plan["numpy"], "NumPy version changed")
    collect = load_functions(collector, plan["cohortCollectorSha256"])["collect_inputs"]
    helpers = load_functions(support, plan["supportRunnerSha256"])
    previous = json.loads(pinned(cohort / "riscontro.json", plan["cohortReportSha256"]))["cases"]
    observed, inputs = collect(cohort, plan["cohortRunnerSha256"])
    require(observed == previous and set(inputs) == set(previous)
            and len(inputs) == plan["expectedSources"], "Pinned cohort replay differs")
    n0 = plan["historicalStartIndex"]
    width = plan["historicalWidth"]
    target = slice(n0, n0 + width)
    threshold = plan["absoluteCorrelationEigenvalueTolerance"]
    reference_grid = None
    rows = []
    for case, identity in enumerate(sorted(inputs), 1):
        grid, _flux, source, conditional, reconstructed, _bands = inputs[identity]
        require(len(grid) == 343, "Unexpected grid size")
        if reference_grid is None:
            reference_grid = grid
        require(np.array_equal(grid, reference_grid), "Grid mismatch")
        corr = helpers["correlation"](source, True)
        require(np.allclose(corr, reconstructed, atol=1e-14, rtol=1e-14),
                "Archived correlation replay differs")
        formal = helpers["correlation"](conditional, False)
        observed_summary = helpers["summarize"]("historical-lower-triangle", corr, plan)
        formal_summary = helpers["summarize"]("formal-conditional", formal, plan)
        localized = observed_summary["shortestContiguousWindow"]
        overlap = 0
        span_nm = None
        if localized:
            start = localized["startIndex"]
            stop = start + localized["width"]
            overlap = max(0, min(stop, n0 + width) - max(start, n0))
            span_nm = [float(grid[start]), float(grid[stop - 1])]
        fixed_min = helpers["eigen_min"](corr[target, target])
        control_min = helpers["eigen_min"](formal[target, target])
        rows.append(dict(case=case, shortestWindowNm=span_nm,
                         shortestWindowOverlapWithHistoricalSamples=overlap,
                         fixedHistoricalWindowMinimumEigenvalue=fixed_min,
                         fixedHistoricalWindowFails=fixed_min < -threshold,
                         fixedFormalWindowMinimumEigenvalue=control_min,
                         observed=observed_summary, formal=formal_summary))
    result = dict(schema="BKL046_GAIA_XP_COHORT_SUPPORT_RESULT_V1", protocolSha256=PLAN_PIN,
                  sample="three archived sources distinct from v571, shared catalogue and model",
                  historicalWindowNm=[float(reference_grid[n0]), float(reference_grid[n0 + width - 1])],
                  cases=rows, fixedWindowFailures=sum(row["fixedHistoricalWindowFails"] for row in rows),
                  fixedFormalWindowFailures=sum(row["fixedFormalWindowMinimumEigenvalue"] < -threshold for row in rows),
                  newAstrophysicalSources=0, externalCalibrationIndependenceEstablished=False,
                  scientificClosures=0, nativeExecutions=0)
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
