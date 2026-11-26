"""Check whether deleting a predeclared band removes the covariance failure."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

import numpy as np

PLAN_PIN = "bc78b08f30f9c581fb0fe06ac831547b48e5aea5dd31f1854c3b0a948a93bbf1"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected, "Changed pinned input")
    return raw


def functions(path, expected):
    env = {"__name__": "verified_module", "__file__": str(path)}
    exec(compile(pinned(path, expected), str(path), "exec"), env)
    return env


def eigenvalues_without(correlation, start, width):
    retained = np.r_[0:start, start + width:len(correlation)]
    return np.linalg.eigvalsh(correlation[np.ix_(retained, retained)])


def examine(case, observed, formal, start, width, tol, before_minimum):
    baseline = np.linalg.eigvalsh(observed)
    require(np.isclose(baseline[0], before_minimum, rtol=1e-12, atol=1e-13),
            "Full minimum differs from the preceding receipt")
    observed_fixed = eigenvalues_without(observed, start, width)
    formal_fixed = eigenvalues_without(formal, start, width)
    minima = []
    for control in range(len(observed) - width + 1):
        if control != start:
            minima.append((float(eigenvalues_without(observed, control, width)[0]), control))
    require(len(minima) == len(observed) - width, "Incomplete mask sweep")
    best_min, best_start = max(minima, key=lambda item: item[0])
    return dict(case=case, originalMinimum=float(baseline[0]),
                originalNegativeModes=int(np.count_nonzero(baseline < -tol)),
                fixedBandMinimum=float(observed_fixed[0]),
                fixedBandNegativeModes=int(np.count_nonzero(observed_fixed < -tol)),
                fixedFormalMinimum=float(formal_fixed[0]),
                otherMasksTested=len(minima),
                otherMasksPassing=sum(value >= -tol for value, _ in minima),
                disjointMasksPassing=sum(value >= -tol and (i + width <= start or i >= start + width)
                                         for value, i in minima),
                bestOtherMaskMinimum=best_min, bestOtherMaskStartIndex=best_start)


def main():
    (protocol, cohort_dir, collector_path, historical_dir, cohort_sources,
     capsule, out) = map(Path, sys.argv[1:])
    plan = json.loads(pinned(protocol, PLAN_PIN))
    cp = json.loads(pinned(cohort_dir / "protocollo.json", plan["cohortProtocolSha256"]))
    functions(cohort_dir / "verifica.py", plan["cohortSupportRunnerSha256"])
    cq = json.loads(pinned(cohort_dir / "riscontro.json", plan["cohortSupportReceiptSha256"]))
    hp = json.loads(pinned(historical_dir / "riscontro.json", plan["historicalSupportReceiptSha256"]))
    correl = functions(historical_dir / "verifica.py", cp["supportRunnerSha256"])["correlation"]
    read = functions(collector_path, cp["cohortCollectorSha256"])["collect_inputs"]
    reference = json.loads(pinned(cohort_sources / "riscontro.json", cp["cohortReportSha256"]))
    prior, cohort = read(cohort_sources, cp["cohortRunnerSha256"])
    require(prior == reference["cases"] and set(cohort) == set(prior)
            and len(cohort) == len(cq["cases"]) == cp["expectedSources"], "Cohort replay differs")
    with ZipFile(BytesIO(pinned(capsule, plan["historicalCapsuleSha256"]))) as z:
        blob = z.read("objects/Matrici-GaiaXPy-campionamento-reale-v1.npz")
    require(sha256(blob).hexdigest() == plan["historicalMatrixSha256"], "Historical matrix changed")
    with np.load(BytesIO(blob), allow_pickle=False) as data:
        grid = data["gridNm"]
        arrays = [("v571", correl(data["pinnedSourceCovariance"], True),
                   correl(data["conditionalCovariance"], False),
                   hp["results"][0]["fullMinimumEigenvalue"])]
    start, width, tol = plan["startIndex"], plan["width"], plan["tolerance"]
    require(grid.shape == (plan["size"],) and list(grid[start:start+width:width-1])
            == cq["historicalWindowNm"], "Fixed wavelength window changed")
    for case, identity in enumerate(sorted(cohort), 1):
        wavelengths, _, source, conditional, archived, _ = cohort[identity]
        observed = correl(source, True)
        require(np.array_equal(wavelengths, grid) and np.allclose(observed, archived, rtol=1e-14, atol=1e-14)
                and cq["cases"][case-1]["case"] == case, "Cohort matrices differ")
        arrays.append((case, observed, correl(conditional, False),
                       cq["cases"][case-1]["observed"]["fullMinimumEigenvalue"]))
    fixture = np.array([[1., 0.9, 0.9], [0.9, 1., -0.9], [0.9, -0.9, 1.]])
    require(np.linalg.eigvalsh(fixture)[0] < -tol
            and eigenvalues_without(fixture, 0, 1)[0] > 0, "Mask control failed")
    rows = [examine(case, observed, formal, start, width, tol, baseline)
            for case, observed, formal, baseline in arrays]
    result = dict(schema="BKL046_GAIA_XP_MASK_DIAGNOSTIC_RESULT_V1", protocolSha256=PLAN_PIN,
                  cases=rows, fixedWindowNm=cq["historicalWindowNm"],
                  fixedMasksPassing=sum(row["fixedBandNegativeModes"] == 0 for row in rows),
                  formalMasksPassing=sum(row["fixedFormalMinimum"] >= -tol for row in rows),
                  predeclaredExclusionDiagnosticOnly=True, independentCalibrationEstablished=False,
                  newAstrophysicalSources=0, scientificClosures=0, nativeExecutions=0)
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
