import argparse
import hashlib
import json
from pathlib import Path
import sys

PINS = {
    "j8f866kdq_flc.fits": "63f72aebcbfbbda4aff3f19542478354f6ffc6cf6449701f54cb9e5dd4e620b7",
    "j8f866kfq_flc.fits": "884be6b89a9b843302ca1862609f5aceaf8d2ae2dd7ffe53bdfc9eb0478e6b9a",
    "j8f866khq_flc.fits": "dab5801808c25eee20b1579a3d1932db6858e9761c72b1d95f1fd87a1d7719f7",
}

parser = argparse.ArgumentParser()
for key in ("fits_root", "site_packages", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.site_packages))

import astropy
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np

assert (astropy.__version__, np.__version__) == ("7.2.0", "2.3.5")


def tangent(sky, center):
    ra, dec = np.deg2rad(sky.T)
    ra0, dec0 = np.deg2rad(center)
    delta = ra - ra0
    denominator = np.sin(dec0) * np.sin(dec) + np.cos(dec0) * np.cos(dec) * np.cos(delta)
    assert np.all(denominator > 0)
    x = np.cos(dec) * np.sin(delta) / denominator
    y = (np.cos(dec0) * np.sin(dec) - np.sin(dec0) * np.cos(dec) * np.cos(delta)) / denominator
    return np.rad2deg(np.column_stack((x, y)))


def design(pixel, center):
    return np.column_stack((pixel - center, np.ones(len(pixel))))


def mesh(x, y):
    return np.column_stack([component.ravel() for component in np.meshgrid(x, y)])


def fit(pixel, projection, center):
    coeff, _, rank, _ = np.linalg.lstsq(design(pixel, center), projection, rcond=None)
    assert rank == 3
    return coeff


def errors_px(pixel, projection, coeff, center):
    residual = design(pixel, center) @ coeff - projection
    pixel_residual = np.linalg.solve(coeff[:2].T, residual.T).T
    distance = np.linalg.norm(pixel_residual, axis=1)
    assert np.isfinite(distance).all()
    return dict(n=len(pixel), median=float(np.median(distance)),
                p90=float(np.quantile(distance, 0.9)), maximum=float(distance.max()))


def grid(axis_length):
    nodes = np.linspace(32, axis_length - 33, 9)
    return nodes, (nodes[1:] + nodes[:-1]) / 2


training = mesh(np.linspace(0, 399, 9), np.linspace(0, 199, 9))
test = mesh(np.linspace(0.5, 398.5, 8), np.linspace(0.5, 198.5, 8))
origin = np.array([199.5, 99.5])
true_coeff = np.array([[0.000012, -0.000001], [0.000002, -0.000011], [0.001, -0.002]])
calibration = fit(training, design(training, origin) @ true_coeff, origin)
control = errors_px(test, design(test, origin) @ true_coeff, calibration, origin)
assert control["maximum"] < 1e-8

reports = []
for name, pin in PINS.items():
    path = args.fits_root / name
    with path.open("rb") as stream:
        assert hashlib.file_digest(stream, "sha256").hexdigest() == pin
    with fits.open(path, mode="readonly", memmap=True) as image:
        for extension in (1, 2):
            header = image["SCI", extension].header
            wcs = WCS(header, image, key="A")
            assert wcs.wcs.name == "IDC_4bb1536oj" and wcs.has_distortion
            x, hx = grid(header["NAXIS1"])
            y, hy = grid(header["NAXIS2"])
            training = mesh(x, y)
            holdout = mesh(hx, hy)
            assert not set(map(tuple, training)) & set(map(tuple, holdout))
            center = (np.asarray([header["NAXIS1"], header["NAXIS2"]]) - 1) / 2
            positions = np.vstack((center, training, holdout))
            sky = wcs.all_pix2world(positions, 0, ra_dec_order=True)
            projected = tangent(sky[1:], sky[0])
            reference = WCS(naxis=2)
            reference.wcs.ctype = ["RA---TAN", "DEC--TAN"]
            reference.wcs.crval = sky[0]
            reference.wcs.crpix = [1, 1]
            reference.wcs.cdelt = [1, 1]
            ref_projected = reference.all_world2pix(sky[1:], 0, ra_dec_order=True)
            assert np.allclose(projected, ref_projected, rtol=0, atol=2e-12)
            projected_train, projected_holdout = np.split(projected, [len(training)])
            coeff = fit(training, projected_train, center)
            reports.append(dict(fits=name, fitsSha256=pin, scienceExtension=extension,
                                chip=header["CCDCHIP"], wcs=wcs.wcs.name,
                                rank=3, determinant=float(np.linalg.det(coeff[:2])),
                                trainingErrorsPx=errors_px(training, projected_train, coeff, center),
                                holdoutErrorsPx=errors_px(holdout, projected_holdout, coeff, center)))

assert len(reports) == 6
report = dict(protocol="BKL046_INSTRUMENTAL_WCS_AFFINE_HOLDOUT_V1",
              versions=dict(astropy=astropy.__version__, numpy=np.__version__),
              independentAffineOnlyModel=True, idealAffineControl=control,
              trainingGrid="9x9 with 32 px edge inset", holdoutGrid="8x8 cell midpoints",
              wcsSource="Instrumental WCS A; no stellar measurements or identity matching",
              rows=reports, nativeExecutions=0, scientificClosures=0)
with args.output.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write("\n")
