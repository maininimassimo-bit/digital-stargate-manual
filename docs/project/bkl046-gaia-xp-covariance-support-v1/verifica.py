"""Measure support of the historical Gaia XP correlation failure offline."""
from hashlib import file_digest, sha256
from io import BytesIO
import json
from math import comb
from pathlib import Path
import sys
from zipfile import ZipFile

import numpy as np

PLAN_PIN = "4ae0f1748c455e9f2f112e53d95aaf1d26cfb28ba04f2e487c62b89dae931fa7"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def eigen_min(matrix):
    return float(np.linalg.eigvalsh(matrix)[0])


def correlation(matrix, mirror):
    require(np.isfinite(matrix).all() and (np.diag(matrix) > 0).all(), "Invalid covariance")
    scale = np.sqrt(np.diag(matrix))
    normalized = matrix / scale[:, None] / scale[None, :]
    if mirror:
        lower = np.tril(normalized, -1)
        normalized = lower + lower.T
    else:
        require(np.max(np.abs(normalized - normalized.T)) < 1e-12, "Unexpected asymmetry")
        normalized = (normalized + normalized.T) / 2
    np.fill_diagonal(normalized, 1.)
    return normalized


def all_triples(matrix, screen, tolerance):
    best = (float("inf"), None)
    checked = 0
    screen_count = 0
    for i in range(len(matrix) - 2):
        for j in range(i + 1, len(matrix) - 1):
            a, b, c = matrix[i, j], matrix[i, j+1:], matrix[j, j+1:]
            determinants = 1 + 2*a*b*c - a*a - b*b - c*c
            index = int(np.argmin(determinants))
            trial = float(determinants[index])
            checked += len(determinants)
            screen_count += int(np.count_nonzero(determinants < screen))
            if trial < best[0]:
                best = (trial, (i, j, j + 1 + index))
    require(checked == comb(len(matrix), 3), "Incomplete triple enumeration")
    det, locations = best
    minimum = eigen_min(matrix[np.ix_(locations, locations)])
    return dict(checked=checked, belowDeterminantScreen=screen_count, minimumDeterminant=det,
                smallestDeterminantWitness=list(locations), witnessMinimumEigenvalue=minimum,
                witnessBelowEigenvalueTolerance=minimum < -tolerance)


def shortest_window(matrix, tolerance, full_minimum):
    if full_minimum >= -tolerance:
        return None  # Interlacing bounds every principal submatrix by the full minimum.
    checks = {}

    def worst(width):
        if width not in checks:
            result = min((eigen_min(matrix[i:i+width, i:i+width]), i)
                         for i in range(len(matrix) - width + 1))
            checks[width] = result
        return checks[width]

    low, high = 1, len(matrix)
    while high - low > 1:
        middle = (high + low) // 2
        if worst(middle)[0] < -tolerance:
            high = middle
        else:
            low = middle
    minimum, start = worst(high)
    previous, _ = worst(low)
    require(minimum < -tolerance <= previous and high == low + 1, "Window boundary failed")
    return dict(width=high, startIndex=start, minimumEigenvalue=minimum,
                widthBelow=low, minimumEigenvalueAtWidthBelow=previous,
                widthsExhaustivelyChecked=sorted(checks))


def summarize(name, matrix, plan):
    tolerance = plan["absoluteCorrelationEigenvalueTolerance"]
    full = eigen_min(matrix)
    pair_min = 1 - float(np.max(np.abs(matrix - np.eye(len(matrix)))))
    triples = all_triples(matrix, plan["tripleDeterminantScreen"], tolerance)
    window = shortest_window(matrix, tolerance, full)
    return dict(case=name, fullMinimumEigenvalue=full, allPairCount=comb(len(matrix), 2),
                allPairMinimumEigenvalue=pair_min, triples=triples, shortestContiguousWindow=window)


def main():
    plan_path, archive_path, result_path = map(Path, sys.argv[1:])
    raw = plan_path.read_bytes()
    require(sha256(raw).hexdigest() == PLAN_PIN, "Protocol changed")
    plan = json.loads(raw)
    require(np.__version__ == plan["numpyVersion"], "NumPy version differs")
    with archive_path.open("rb") as stream:
        require(file_digest(stream, "sha256").hexdigest() == plan["archiveSha256"], "Archive changed")
    with ZipFile(archive_path) as archive:
        member = "objects/Matrici-GaiaXPy-campionamento-reale-v1.npz"
        require(archive.namelist().count(member) == 1, "Unexpected member multiplicity")
        blob = archive.read(member)
    require(sha256(blob).hexdigest() == plan["matrixSha256"], "Matrix changed")
    with np.load(BytesIO(blob), allow_pickle=False) as data:
        historical = data["pinnedSourceCovariance"]
        conditional = data["conditionalCovariance"]
    n = plan["size"]
    require(historical.shape == conditional.shape == (n, n), "Unexpected shape")
    controls = np.full((3, 3), -0.75)
    np.fill_diagonal(controls, 1.)
    require(all_triples(controls, -1e-12, 1e-8)["witnessBelowEigenvalueTolerance"],
            "Indefinite triple control failed")
    require(shortest_window(controls, 1e-8, eigen_min(controls))["width"] == 3,
            "Contiguous support control failed")
    matrices = (correlation(historical, True), correlation(conditional, False), np.eye(n))
    rows = [summarize(name, matrix, plan) for name, matrix in zip(plan["comparators"], matrices, strict=True)]
    require(rows[-1]["fullMinimumEigenvalue"] == 1 and rows[-1]["triples"]["belowDeterminantScreen"] == 0,
            "Diagonal comparator failed")
    result = dict(schema="BKL046_GAIA_XP_COVARIANCE_SUPPORT_RESULT_V1", protocolSha256=PLAN_PIN,
                  sampleCount=n, results=rows, independentAstrophysicalSources=0,
                  scientificClosures=0, nativeExecutions=0)
    with result_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
