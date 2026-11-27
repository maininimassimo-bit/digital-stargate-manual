import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("first_protocol", "first_report", "first_verifier", "edge_source", "protocol", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np


def pinned(path, digest):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest, path.name
    return raw


def load_functions(raw, filename, wanted, namespace):
    tree = ast.parse(raw)
    functions = [s for s in tree.body if isinstance(s, ast.FunctionDef) and s.name in wanted]
    assert {s.name for s in functions} == wanted
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(filename), "exec"), namespace)


protocol_sha = "8f3d6811cc2d423fe185e67243d8d95de719ae9d6fa4440e2fece5ee176bcb25"
follow = json.loads(pinned(args.protocol, protocol_sha))
plan = json.loads(pinned(args.first_protocol, follow["initialProtocolSha256"]))
first = json.loads(pinned(args.first_report, follow["initialReportSha256"]))
assert np.__version__ == "2.3.5" and first["referenceDisagreements"] == 5
scope = {"np": np, "plan": plan, "quad": {}}
load_functions(pinned(args.edge_source, plan["priorEdgeSourceSha256"]), args.edge_source,
               {"integrate_edges","circular_exact","differences"}, scope)
load_functions(pinned(args.first_verifier, follow["initialVerifierSha256"]), args.first_verifier,
               {"area_rule","area_pixel"}, scope)
scope["rules"] = {order:scope["area_rule"](order, plan["areaSubdivisions"]) for order in plan["areaOrders"]}


def composite_legendre(divisions, order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    mapped = (nodes[None,:]+1+2*np.arange(divisions)[:,None])/divisions-1
    return mapped.ravel(), np.tile(weights/divisions, divisions)


for rule in follow["rules"]:
    div, order = rule["divisions"], rule["order"]
    label = f"{div}x{order}"
    scope["quad"][label] = composite_legendre(div, order)
labels = list(scope["quad"])
results = []
for initial in first["cases"]:
    case = initial["case"]
    geom, flux = plan["geometry"], plan["totalElectronsInfinitePlane"]
    profile = {label:scope["integrate_edges"](case, geom, flux, label) for label in labels}
    reference = profile[labels[-1]]
    assert np.isfinite(reference).all() and np.min(reference) >= -1e-10
    assert 0 < reference.sum() <= flux + plan["absoluteFiniteFieldSumToleranceElectrons"]
    ref2d = [abs(reference[y,x]-scope["area_pixel"](case, y, x, plan["areaOrders"][-1]))
             for y,x in plan["selectedAreaPixels"]]
    if case["beta"] == 1.5 and case["axisRatio"] == 1:
        exact = scope["circular_exact"](case, geom, flux)
        control = scope["differences"](reference, exact)
        assert control["maxPixelElectrons"] <= plan["absolutePixelToleranceElectrons"]
        assert control["finiteFieldElectrons"] <= plan["absoluteFiniteFieldSumToleranceElectrons"]
    shifts = {label:scope["differences"](profile[label], reference) for label in labels[:-1]}
    decisions = {label: (v["maxPixelElectrons"] <= plan["absolutePixelToleranceElectrons"] and
                         v["finiteFieldElectrons"] <= plan["absoluteFiniteFieldSumToleranceElectrons"])
                 for label,v in shifts.items()}
    results.append(dict(case=case, priorReferenceFailed=not initial["referenceAgrees"],
                        maximumSelectedPixelToAreaRefElectrons=float(max(ref2d)),
                        priorAreaRefinementMaxElectrons=max(x["areaRefinementElectrons"] for x in initial["selectedAreaChecks"]),
                        deltaToHighestComposite=shifts, ruleWithinTolerance=decisions))

assert len(results) == 72
report = dict(protocol="BKL046_MOFFAT_COMPOSITE_EDGE_DEVELOPMENT_V1", protocolSha256=protocol_sha,
              initialReportSha256=follow["initialReportSha256"], referenceRule=labels[-1],
              independentAreaToleranceElectrons=plan["absolutePixelToleranceElectrons"],
              failuresByCompositeRule={label:sum(not row["ruleWithinTolerance"][label] for row in results)
                                       for label in labels[:-1]},
              independentAreaFailures=sum(max(row["maximumSelectedPixelToAreaRefElectrons"],
                                               row["priorAreaRefinementMaxElectrons"]) >
                                           plan["absolutePixelToleranceElectrons"] for row in results),
              priorFailedObservationCountPreserved=sum(r["priorReferenceFailed"] for r in results),
              cases=results, nativeExecutions=0, scientificClosures=0)
payload = json.dumps(report, indent=2, allow_nan=False) + "\n"
with args.output.open("x", encoding="utf-8", newline="\n") as f:
    f.write(payload)
