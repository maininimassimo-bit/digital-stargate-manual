"""Poisson Fisher information for finite pixel-integrated Moffat models."""
import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
for key in ("protocol", "prior_report", "edge_source", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

assert np.__version__ == "2.3.5"


def pinned(path, digest):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == digest, path.name
    return raw


pin = "c455593904deb9376ea87c3092a79ae051ac568c90ef8bdee20c758122bce225"
plan = json.loads(pinned(args.protocol, pin))
prior = json.loads(pinned(args.prior_report, plan["parentNumericalReportSha256"]))
assert prior["independentAreaFailures"] == 0 and len(prior["cases"]) == 72
source = pinned(args.edge_source, plan["parentEdgeSourceSha256"])
edge_fn, = (node for node in ast.parse(source).body
            if isinstance(node, ast.FunctionDef) and node.name == "integrate_edges")
div = plan["quadratureDivisions"]
nodes, weights = np.polynomial.legendre.leggauss(plan["quadratureOrderPerDivision"])
mapped = ((nodes[None, :]+1+2*np.arange(div)[:, None])/div-1).ravel()
weights = np.tile(weights/div, div)
scope = {"np": np, "quad": {0:(mapped, weights)}}
exec(compile(ast.Module(body=[edge_fn], type_ignores=[]), str(args.edge_source), "exec"), scope)
edge = scope["integrate_edges"]
flux = plan["fluxElectronsInfinitePlane"]
shape = plan["geometry"]
point = (mapped + 1)/2
edge_weights = weights/2
yy, xx = np.mgrid[:shape[0], :shape[1]]


def density(case, x, y):
    a, q, b = case["alpha"], case["axisRatio"], case["beta"]
    theta = np.deg2rad(case["angleDegrees"])
    dx, dy = x-(12.5+case["phase"][0]), y-(12.5+case["phase"][1])
    u = np.cos(theta)*dx + np.sin(theta)*dy
    v = -np.sin(theta)*dx + np.cos(theta)*dy
    return flux*(b-1)/(np.pi*a*a*q) * (1+(u/a)**2+(v/(a*q))**2)**(-b)


area_nodes, area_weights = np.polynomial.legendre.leggauss(96)
area_grid = (((area_nodes+1)/2 + np.arange(4)[:, None])/4).ravel()
area_weights = np.tile(area_weights/8, 4)


def area_derivative(case, y, x, axis):
    a, q, b = case["alpha"], case["axisRatio"], case["beta"]
    theta = np.deg2rad(case["angleDegrees"])
    c, s = np.cos(theta), np.sin(theta)
    dx = x + area_grid[:, None] - (12.5 + case["phase"][0])
    dy = y + area_grid[None, :] - (12.5 + case["phase"][1])
    u, v = c*dx + s*dy, -s*dx + c*dy
    r = 1+(u/a)**2+(v/(a*q))**2
    slope = (c*u/a**2-s*v/(a*q)**2, s*u/a**2+c*v/(a*q)**2)[axis]
    derivative = 2*b*slope/r * density(case, x+area_grid[:, None], y+area_grid[None, :])
    return float(np.sum(derivative*area_weights[:, None]*area_weights[None, :]))


def derivatives(case):
    x, y = xx[:, :, None], yy[:, :, None]
    horizontal = density(case, x, y+point) - density(case, x+1, y+point)
    vertical = density(case, x+point, y) - density(case, x+point, y+1)
    return [np.sum(normal_flux*edge_weights, axis=2) for normal_flux in (horizontal,vertical)]


def shifted(case, axis, step):
    phase = list(case["phase"])
    phase[axis] += step
    return dict(case, phase=phase)


def covariance(columns):
    norm = np.linalg.norm(columns, axis=0)
    assert np.isfinite(norm).all() and (norm > 0).all()
    _, singular, vh = np.linalg.svd(columns/norm, full_matrices=False)
    assert singular[-1] > 1e-12*singular[0]
    unscaled = vh.T/singular[None, :]/norm[:, None]
    return unscaled @ unscaled.T


step = plan["phaseDerivativeCheckStepPixel"]
rows = []
for item in prior["cases"]:
    case = item["case"]
    expected_signal = edge(case, shape, flux, 0)
    shifts = derivatives(case)
    checks = []
    for axis, d in enumerate(shifts):
        left = edge(shifted(case, axis, -step), shape, flux, 0)
        right = edge(shifted(case, axis, step), shape, flux, 0)
        finite_difference = (right-left)/(2*step)
        rel = float(np.linalg.norm(d-finite_difference)/np.linalg.norm(d))
        checks.append(rel)
    independent_area_checks = []
    for axis, value in enumerate(checks):
        if value <= 1e-4:
            continue
        d = shifts[axis]
        indexes = np.argsort(np.abs(d).ravel())[-4:]
        locations = [np.unravel_index(index, d.shape) for index in indexes]
        actual = np.asarray([d[y,x] for y,x in locations])
        expected = np.asarray([area_derivative(case,y,x,axis) for y,x in locations])
        error = float(np.linalg.norm(actual-expected)/np.linalg.norm(expected))
        assert error <= 1e-4
        independent_area_checks.append(dict(axis=axis, selectedDerivativeRelativeL2Error=error,
                                            comparativeFiniteDifferenceRelativeL2Error=value,
                                            checkedPixels=len(locations)))
    jac = np.column_stack([j.ravel() for j in (*shifts,expected_signal,np.ones_like(expected_signal))])
    for background in plan["backgroundElectronsPerPixel"]:
        mu = expected_signal.ravel() + background
        assert np.isfinite(mu).all() and (mu > 0).all()
        weighted = jac/np.sqrt(mu[:, None])
        cov = covariance(weighted)
        known_center = covariance(weighted[:, 2:])
        assert cov[2, 2] >= known_center[0, 0] * (1-1e-8)
        eig = np.linalg.eigvalsh(cov[:2, :2])
        assert eig[0] > 0
        rows.append(dict(case=case, backgroundElectrons=background,
                         finiteDifferenceRelativeL2Error=checks, independentAreaChecks=independent_area_checks,
                         centerSigmaAxesLowerBoundsPx=np.sqrt(eig).tolist(),
                         marginalCenterSigmasPx=np.sqrt(np.diag(cov)[:2]).tolist(),
                         relativeFluxSigmaLowerBound=float(np.sqrt(cov[2,2])),
                         relativeFluxSigmaKnownCenterLowerBound=float(np.sqrt(known_center[0,0]))))

assert len(rows) == 144
result = dict(protocol="BKL046_POISSON_MOFFAT_PHASE_INFORMATION_V1", protocolSha256=pin,
              priorQuadratureSha256=plan["parentNumericalReportSha256"],
              knownShape=True, finiteGrid=True, expectationModel="Independent ideal Poisson counts",
              lowerBoundsOnly=True, estimatorAccuracyMeasured=False,
              rows=rows, nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(result, stream, indent=2, allow_nan=False)
    stream.write("\n")
