import argparse
import ast
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("protocol", "edge_source", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

assert np.__version__ == "2.3.5"
plan_raw = args.protocol.read_bytes()
protocol_sha = "997a4e3f2b1d5f5dcd7c7b7879b931631045fc7bd5aaacc1a33eb21ff73e0542"
assert sha256(plan_raw).hexdigest() == protocol_sha
plan = json.loads(plan_raw)
edge_raw = args.edge_source.read_bytes()
assert sha256(edge_raw).hexdigest() == plan["priorEdgeSourceSha256"]
tree = ast.parse(edge_raw)
names = {"integrate_edges", "circular_exact", "differences"}
functions = [stat for stat in tree.body if isinstance(stat, ast.FunctionDef) and stat.name in names]
assert {stat.name for stat in functions} == names
edge_orders = plan["edgeOrders"]
scope = {"np": np, "quad": {n: np.polynomial.legendre.leggauss(n) for n in edge_orders}}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(args.edge_source), "exec"), scope)


def area_rule(order, divisions):
    n, w = np.polynomial.legendre.leggauss(order)
    loc = ((n + 1)/2 + np.arange(divisions)[:, None]) / divisions
    return loc.ravel(), np.tile(w/(2*divisions), divisions)


rules = {n: area_rule(n, plan["areaSubdivisions"]) for n in plan["areaOrders"]}


def area_pixel(case, y, x, order):
    nodes, weights = rules[order]
    theta = np.deg2rad(case["angleDegrees"])
    dx = x + nodes[:, None] - (12.5 + case["phase"][0])
    dy = y + nodes[None, :] - (12.5 + case["phase"][1])
    a, q, b = case["alpha"], case["axisRatio"], case["beta"]
    u = (np.cos(theta)*dx + np.sin(theta)*dy)/a
    v = (-np.sin(theta)*dx + np.cos(theta)*dy)/(a*q)
    radiance = (1+u*u+v*v)**(-b) * plan["totalElectronsInfinitePlane"] * (b-1)/(np.pi*a*a*q)
    return float(np.sum(radiance * weights[:, None] * weights[None, :]))


def delta(diff):
    return diff["maxPixelElectrons"] <= plan["absolutePixelToleranceElectrons"] and \
           diff["finiteFieldElectrons"] <= plan["absoluteFiniteFieldSumToleranceElectrons"]


rows = []
for alpha, beta, shape, phase in product(plan["alpha"], plan["beta"], plan["shapes"], plan["phases"]):
    case = dict(alpha=alpha, beta=beta, axisRatio=shape["ratio"], angleDegrees=shape["angle"], phase=phase)
    flux, geom = plan["totalElectronsInfinitePlane"], plan["geometry"]
    grids = {n: scope["integrate_edges"](case, geom, flux, n) for n in edge_orders}
    ref = grids[edge_orders[-1]]
    assert (np.isfinite(ref).all() and np.min(ref) >= -1e-10
            and 0 < ref.sum() <= flux + plan["absoluteFiniteFieldSumToleranceElectrons"])
    edge = {str(n): scope["differences"](grids[n], ref) for n in edge_orders[:-1]}
    assert all(np.isfinite(v) for diff in edge.values() for v in diff.values())
    selected = []
    for y, x in plan["selectedAreaPixels"]:
        first, second = (area_pixel(case, y, x, n) for n in rules)
        selected.append(dict(pixel=[y,x], areaRefinementElectrons=abs(first-second),
                             edgeToAreaElectrons=abs(ref[y,x]-second)))
    analytic = None
    if beta == 1.5 and shape["ratio"] == 1:
        control = scope["circular_exact"](case, geom, flux)
        analytic = scope["differences"](ref, control)
    tol = plan["absolutePixelToleranceElectrons"]
    reference_checks = (delta(edge[str(edge_orders[-2])])
                        and max(max(x["areaRefinementElectrons"], x["edgeToAreaElectrons"]) for x in selected) <= tol
                        and (analytic is None or delta(analytic)))
    rows.append(dict(case=case, edgeAgainstHighestOrder=edge, selectedAreaChecks=selected,
                     circularSolidAngleCheck=analytic, referenceAgrees=reference_checks,
                     acceptedEdgeOrders=[int(n) for n, value in edge.items() if reference_checks and delta(value)]))

assert len(rows) == 72
result = dict(protocol="BKL046_MOFFAT_NARROW_DOMAIN_NUMERICAL_DEVELOPMENT_V1",
              protocolSha256=protocol_sha, priorEdgeSourceSha256=plan["priorEdgeSourceSha256"],
              cases=rows, referenceDisagreements=sum(not r["referenceAgrees"] for r in rows),
              failedEdgeOrders={str(n):sum(n not in r["acceptedEdgeOrders"] for r in rows) for n in edge_orders[:-1]},
              detectorOrInstrumentModelQualified=False, scientificClosures=0, nativeExecutions=0)
with args.output.open("x", encoding="utf-8", newline="\n") as out:
    json.dump(result, out, indent=2, allow_nan=False)
    out.write("\n")
