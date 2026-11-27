"""Independently integrate archived elliptical Moffat profiles along pixel edges."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

parser = argparse.ArgumentParser()
for key in ("archive", "refinement", "packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np

assert np.__version__ == "2.3.5"
PINS = {
    "archive": "6b2ae3dcffe752300c35786b45dc3e1d7eb2751913e731d91868634cd27969bd",
    "protocol": "c68ae1bf0727e888e507710c2e10ecb194ffdbbfa8349223e011c3839e3e5a92",
    "failed": "a7d2913094b47cfdda4132b8d006ecdefd3419c4bd432f9bcf449037cb197a86",
    "refinement": "9d548de943e17811d30b803e5d08ae1a556375e7a1ffbb851c86fdc7209595aa",
}


def checked(raw, key):
    if sha256(raw).hexdigest() != PINS[key]:
        raise ValueError(f"Unexpected digest for {key}")
    return raw


quad = {n: np.polynomial.legendre.leggauss(n) for n in (32, 64, 128)}


def integrate_edges(case, geometry, electrons, order):
    height, width = geometry
    theta = np.deg2rad(case["angleDegrees"])
    cos, sin = np.cos(theta), np.sin(theta)
    alpha, ratio, beta = case["alpha"], case["axisRatio"], case["beta"]
    assert alpha > 0 and 0 < ratio <= 1 and beta > 1
    transform = np.asarray([[cos/alpha, sin/alpha], [-sin/(alpha*ratio), cos/(alpha*ratio)]])
    assert np.linalg.det(transform) > 0
    origin = np.asarray([12.5, 12.5]) + np.asarray(case["phase"])
    corners = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    yy, xx = np.mgrid[:height, :width]
    positions = np.stack((xx, yy), axis=-1)
    vertices = (positions[:, :, None, :] + corners - origin) @ transform.T
    edge = np.roll(vertices, -1, axis=2) - vertices
    nodes, weights = quad[order]
    points = vertices[:, :, :, None, :] + (nodes[None, None, None, :, None] + 1) / 2 * edge[:, :, :, None, :]
    radius2 = np.sum(points * points, axis=-1)
    numerator = -np.expm1((1-beta) * np.log1p(radius2))
    density_scale = np.full_like(radius2, beta-1)
    np.divide(numerator, radius2, out=density_scale, where=radius2 != 0)
    # The normalized line flux uses outward normal times edge length.
    normal = np.stack((edge[:, :, :, 1], -edge[:, :, :, 0]), axis=-1)
    normal_flux = np.sum(points * normal[:, :, :, None, :], axis=-1) * density_scale
    return np.sum(normal_flux * weights, axis=(2, 3)) * electrons / (4*np.pi)


def circular_exact(case, geometry, electrons):
    # For beta=3/2 and a circular profile the normalized rectangular
    # integral is the solid angle of the rectangle divided by 2*pi.
    height, width = geometry
    origin = np.asarray([12.5, 12.5]) + np.asarray(case["phase"])
    yy, xx = np.mgrid[:height+1, :width+1]
    x, y = (xx-origin[0])/case["alpha"], (yy-origin[1])/case["alpha"]
    corner = np.arctan2(x*y, np.sqrt(1+x*x+y*y))
    return np.diff(np.diff(corner, axis=0), axis=1) * electrons / (2*np.pi)


def differences(first, second):
    return dict(maxPixelElectrons=float(np.max(np.abs(first-second))),
                finiteFieldElectrons=float(abs(first.sum()-second.sum())))


refinement = json.loads(checked(args.refinement.read_bytes(), "refinement"))
assert refinement["originalFailuresPreserved"] == 8 and refinement["selectedPixelsExactlyRecomputed"] == 108
with ZipFile(BytesIO(checked(args.archive.read_bytes(), "archive"))) as bundle:
    protocol = json.loads(checked(bundle.read(
        "moffat-pixel-integration-protocol-v1/Protocollo-integrazione-pixel-Moffat-v1.json"), "protocol"))
    failed = json.loads(checked(bundle.read(
        "moffat-pixel-integration-development-v1/Studio-integrazione-pixel-Moffat-v1.json"), "failed"))
    profile = bundle.read("moffat-pixel-integration-development-v1/integrated-profiles.npz")
assert sha256(profile).hexdigest() == failed["arraySha256"]
assert len(failed["failures"]) == 8
tolerance = protocol["absolutePixelToleranceElectrons"]
sum_tolerance = protocol["absoluteFiniteFieldSumToleranceElectrons"]
geometry = protocol["geometry"]
electrons = protocol["totalElectronsInfinitePlane"]
controls = []
records = []
with np.load(BytesIO(profile), allow_pickle=False) as stored:
    for case in protocol["cases"]:
        order32, order64, order128 = (integrate_edges(case, geometry, electrons, n) for n in quad)
        assert np.isfinite(order128).all() and np.min(order128) >= -1e-11
        base = stored[case["id"]+"_order128"]
        comparisons = dict(edge32To128=differences(order32, order128),
                           edge64To128=differences(order64, order128),
                           edge128ToArchivedGauss128=differences(order128, base))
        for key in ("edge64To128", "edge128ToArchivedGauss128"):
            assert comparisons[key]["maxPixelElectrons"] <= tolerance
            assert comparisons[key]["finiteFieldElectrons"] <= sum_tolerance
        if case["beta"] == 1.5 and case["axisRatio"] == 1:
            exact = circular_exact(case, geometry, electrons)
            relative = differences(order128, exact)
            assert relative["maxPixelElectrons"] <= tolerance and relative["finiteFieldElectrons"] <= sum_tolerance
            controls.append(dict(id=case["id"], edge128ToSolidAngle=relative))
        records.append(dict(id=case["id"], parameters=case, comparisons=comparisons))
assert len(records) == 36 and len(controls) > 0
report = dict(protocol="BKL046_MOFFAT_PIXEL_EDGE_QUADRATURE_V1", sourcePins=PINS,
              previousFailedChecksPreserved=failed["failures"], evaluatedPixels=len(records)*int(np.prod(geometry)),
              edgeQuadratureOrders=[32,64,128], archivedGaussComparisonOrder=128, checks=records,
              independentAnalyticControls=controls, fluxRenormalized=False,
              numericalAgreementOnly=True, nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write("\n")
