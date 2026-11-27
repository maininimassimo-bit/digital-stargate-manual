"""Compare fixed translations of a pixel-integrated PSF under ideal Poisson noise."""
import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("protocol", "information_receipt", "edge_source", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

assert np.__version__ == "2.3.5"


def pinned(path, digest):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == digest, path.name
    return raw


pin = "286de669b6b0fe7af3f61d0cde2925024976fc13897189045840140aa793e2bd"
plan = json.loads(pinned(args.protocol, pin))
info = json.loads(pinned(args.information_receipt, plan["priorInformationReceiptSha256"]))
assert info["lowerBoundsOnly"] and len(info["rows"]) == 144
source = pinned(args.edge_source, plan["edgeSourceSha256"])
assert plan["partition"] == "DEVELOPMENT_ONLY"
edge, = (node for node in ast.parse(source).body
         if isinstance(node, ast.FunctionDef) and node.name == "integrate_edges")
base_nodes, base_weights = np.polynomial.legendre.leggauss(plan["quadratureOrder"])
quad = {d: (((base_nodes[None,:]+1+2*np.arange(d)[:,None])/d-1).ravel(), np.tile(base_weights/d,d))
        for d in plan["quadratureDivisions"]}
scope = {"np": np, "quad": quad}
exec(compile(ast.Module(body=[edge], type_ignores=[]), str(args.edge_source), "exec"), scope)
integrate = scope["integrate_edges"]


def profile(case):
    flux = plan["fluxElectrons"]
    geom = plan["geometry"]
    low, high = (integrate(case,geom,flux,d) for d in plan["quadratureDivisions"])
    assert np.max(np.abs(low-high)) <= plan["pixelToleranceElectrons"]
    assert abs(low.sum()-high.sum()) <= plan["fieldToleranceElectrons"]
    means = high.ravel() + plan["backgroundElectrons"]
    assert np.isfinite(means).all() and (means > 0).all()
    return means


def draw(means, label):
    seed = int.from_bytes(sha256(("DSG_PI_DEV_V2/moffat-position/" + label).encode()).digest()[:8], "big")
    rng = np.random.Generator(np.random.PCG64(seed))
    return str(seed), rng.poisson(means, size=(plan["drawsPerHypothesis"],len(means)))


def compare(reference, stats, candidate, label):
    seed, alternative = draw(candidate,label)
    weight = np.log1p((candidate-reference)/reference)
    difference = np.sum(candidate-reference)
    # Center the Poisson sum to keep the two small terms of the score separate.
    d0 = (stats-reference) @ weight
    d1 = (alternative-candidate) @ weight
    expectation0 = np.sum(reference * weight - (candidate-reference))
    expectation1 = np.sum(candidate * weight - (candidate-reference))
    correct0 = int(np.count_nonzero(d0+expectation0 <= 0))
    correct1 = int(np.count_nonzero(d1+expectation1 > 0))
    h = float(np.sum((np.sqrt(candidate)-np.sqrt(reference))**2))
    t = int(plan["drawsPerHypothesis"])
    return dict(alternativeSeed=seed, correctReference=correct0, correctAlternative=correct1,
                equalPriorAccuracy=(correct0+correct1)/(2*t),
                optimalErrorLowerBound=float((1-np.sqrt(-np.expm1(-h)))/2),
                optimalErrorUpperBound=float(0.5*np.exp(-h/2)),
                klReferenceToAlternative=max(0.,float(-expectation0)),
                klAlternativeToReference=max(0.,float(expectation1)))


groups = []
for shape in plan["shapes"]:
    for i, phase in enumerate(plan["phases"]):
        label = f"{shape['id']}/{i}"
        source_case = {k:v for k,v in shape.items() if k != "id"}
        case = dict(source_case, phase=phase)
        reference = profile(case)
        seed, stats = draw(reference,label)
        rows = []
        for axis in (0,1):
            for step in plan["displacementsPx"]:
                shift = list(phase)
                shift[axis] += step
                candidate = profile(dict(case, phase=shift))
                result = compare(reference,stats,candidate,f"{label}/{axis}/{step}")
                rows.append(dict(axis="x" if axis==0 else "y", shiftPx=step, **result))
        groups.append(dict(shape=shape["id"], baselinePhase=phase, referenceSeed=seed, alternatives=rows))

assert len(groups) == 6 and sum(len(g["alternatives"]) for g in groups) == 72
report = dict(protocol="BKL046_MOFFAT_PHASE_DISCRIMINATION_DEVELOPMENT_V1", protocolSha256=pin,
              drawsPerHypothesis=plan["drawsPerHypothesis"], baselineReuseWithinGroup=True,
              allOtherSceneParametersKnown=True, groups=groups, nativeExecutions=0,
              scientificClosures=0, scienceThresholdsFrozen=False)
with args.output.open("x", encoding="utf-8", newline="\n") as out:
    json.dump(report, out, indent=2, allow_nan=False)
    out.write("\n")
