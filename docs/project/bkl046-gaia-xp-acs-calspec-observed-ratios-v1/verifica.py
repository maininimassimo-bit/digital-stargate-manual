"""Compare Gaia XP band synthesis with pinned CALSPEC and ACS observations."""
from hashlib import sha256
import json
from pathlib import Path
import runpy
import sys

import numpy as np

PLAN_PIN = "35d55a18a4a102d855210e5f5e19c3f0edef364b651a84546c1888cb4928bed7"
RATE_FACTOR = 45238.93416 / (6.62607015e-27 * 2.99792458e18)


def require(ok, label):
    if not ok:
        raise ValueError(label)


def pinned(path, digest):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == digest, "Pinned input changed")
    return raw


def integral(chain, wave, spectra, order):
    edges = np.unique(np.concatenate([wave, *(grid for grid, _ in chain)]))
    half = np.diff(edges) / 2
    nodes, node_weights = np.polynomial.legendre.leggauss(order)
    coords = (edges[:-1] + half)[:, None] + half[:, None] * nodes
    w = half[:, None] * node_weights * coords
    for grid, response in chain:
        w *= np.interp(coords, grid, response, left=0., right=0.)
    inside = (coords >= wave[0]) & (coords <= wave[-1])
    values = np.array([np.sum(w[inside] * np.interp(coords[inside], wave, flux)) for flux in spectra])
    return values, float(np.sum(w)), float(np.sum(w[~inside]) / np.sum(w))


def synthesize(chain, wave, spectra, plan):
    results = [integral(chain, wave, spectra, order) for order in plan["quadratureOrders"]]
    np.testing.assert_allclose(np.r_[results[0][0], results[0][1:]],
                               np.r_[results[1][0], results[1][1:]], rtol=1e-9, atol=1e-15)
    return results[0]


def calspec(path, pin, fits):
    pinned(path, pin)
    with fits.open(path, memmap=False) as hdus:
        hdus.verify("exception")
        table = hdus[1]
        require(table.columns["WAVELENGTH"].unit.lower() in ("angstrom", "angstroms")
                and table.columns["FLUX"].unit.lower() == "flam", "Unexpected CALSPEC units")
        wave = table.data["WAVELENGTH"].astype(float)
        flux = table.data["FLUX"].astype(float)
    require(np.all(np.diff(wave) > 0) and np.isfinite(flux).all(), "CALSPEC samples malformed")
    return wave, flux


def compare(star, spectra, grid_nm, exposure, history, spec, plan, acs, throughput, capture, fits):
    wavelengths, ref = spec
    grid = grid_nm * 10.
    gaia = np.array(spectra["flux"]) * plan["gaiaToFlamFactor"]
    require(gaia.shape == grid.shape and np.isfinite(gaia).all()
            and wavelengths[0] <= grid[0] < grid[-1] <= wavelengths[-1],
            "Spectra wavelength support changed")
    mask = (grid_nm >= plan["maskNm"][0]) & (grid_nm <= plan["maskNm"][1])
    require(np.count_nonzero(mask) == 8, "Mask changed")
    gaia_masked = np.where(mask, 0., gaia)
    ref_grid = np.interp(grid, wavelengths, ref)
    low, high = plan["bands"], plan["fixedAperturePixels"]
    bands = {name: [] for name in low}
    require(len(exposure["rows"]) == 6, "Exposure coverage changed")
    for row in exposure["rows"]:
        throughput.__globals__["EPOCH"] = row["startMjd"]
        name = row["band"]
        route = acs["routes"][name.lower()]
        chain = [throughput(np, fits, str(item)) for item in route]
        physical, response, tail_ref = synthesize(chain, wavelengths, [ref], plan)
        common, common_response, tail_grid = synthesize(chain, grid, [gaia, ref_grid, gaia_masked], plan)
        require(tail_ref <= 1e-10 and tail_grid <= 1 and
                abs(common_response / response - 1) < 1e-9
                and abs((1 / (response * RATE_FACTOR)) / row["flam"] - 1) < 1e-4
                and min(*physical, *common) > 0, "ACS exposure calibration check failed")
        bands[name].append(dict(calspecFullRate=float(physical[0] * RATE_FACTOR),
                                calspecGaiaGridRate=float(common[1] * RATE_FACTOR),
                                gaiaFullGridRate=float(common[0] * RATE_FACTOR),
                                gaiaMaskedRate=float(common[2] * RATE_FACTOR),
                                throughputOutsideGaiaGrid=tail_grid,
                                observedApertureRate=row["apertures"][str(high)]["rate"]))
    require(all(len(items) == 2 for items in bands.values()), "Coverage per band changed")
    means = {band:{key:float(np.mean([row[key] for row in items])) for key in items[0]}
             for band, items in bands.items()}
    methods = ("observedApertureRate", "calspecFullRate", "calspecGaiaGridRate",
               "gaiaFullGridRate", "gaiaMaskedRate")
    ratios = {}
    for ratio in plan["ratios"]:
        a, b = ratio.split("/")
        out = {key:means[a][key]/means[b][key] for key in methods}
        expected = (history["comparisons"][str(high)]["ratios"][ratio] if star == "GD71"
                    else history["ratios"][ratio])
        observed, calspec_exact = ((expected["observed"], expected["predicted"]["stis"]) if star == "GD71"
                                   else (expected["observedThreePixelRate"], expected["calspecInfiniteRate"]))
        np.testing.assert_allclose([out["observedApertureRate"], out["calspecFullRate"]],
                                   [observed, calspec_exact], rtol=1e-10, atol=0)
        out["gaiaVersusCalspecSameGridFraction"] = out["gaiaFullGridRate"]/out["calspecGaiaGridRate"] - 1
        out["observedVersusGaiaFraction"] = out["observedApertureRate"]/out["gaiaFullGridRate"] - 1
        out["gaiaMaskedVersusFullFraction"] = out["gaiaMaskedRate"]/out["gaiaFullGridRate"] - 1
        ratios[ratio] = out
    return dict(verifiedExposures=6, averageRates=means, ratios=ratios)


def main():
    protocol, spectra_path, acs_path, gd71obs, gd71hist, gd71spec, gd153obs, gd153hist, gd153spec, out = map(Path, sys.argv[1:])
    plan = json.loads(pinned(protocol, PLAN_PIN))
    data = json.loads(pinned(spectra_path, plan["gaiaSpectraSha256"]))
    acs = json.loads(pinned(acs_path, plan["acsProtocolSha256"]))
    sys.path.insert(0, acs["packages"])
    from astropy.io import fits
    helper = Path(acs["helper"])
    pinned(helper, acs["helperSha256"])
    throughput = runpy.run_path(str(helper))["throughput"]
    capture = Path(acs["capture"])
    captures = json.loads(pinned(capture, acs["captureSha256"]))
    require(captures["routes"] == acs["routes"], "ACS capture paths differ")
    for name in sorted({item for route in acs["routes"].values() for item in route}):
        pinned(capture.parent / name, captures["components"][name]["sha256"])
    grid = np.array(data["gridNm"], dtype=float)
    require(np.array_equal(grid, np.arange(336., 1021., 2.)), "Gaia grid changed")
    uniform = [(np.array([1., 2.]), np.ones(2))]
    check, sensitivity, tail = integral(uniform, np.array([1., 2.]), [np.ones(2)*3.], 4)
    require(abs(check[0] - 4.5) < 1e-13 and abs(sensitivity - 1.5) < 1e-13 and tail == 0.,
            "Uniform integration control failed")
    result = {}
    for star, files in (("GD71", (gd71obs,gd71hist,gd71spec)), ("GD153", (gd153obs,gd153hist,gd153spec))):
        spec = plan["targets"][star]
        exposure = json.loads(pinned(files[0], spec["exposures"]))
        history = json.loads(pinned(files[1], spec["historicalComparison"]))
        result[star] = compare(star, data["spectra"][star], grid, exposure, history,
                               calspec(files[2], spec["stis"], fits), plan, acs, throughput, capture, fits)
    report = dict(schema="BKL046_GAIAXP_ACS_STANDARD_PHOTOMETRY_RESULT_V1", protocolSha256=PLAN_PIN,
                  comparisons=result, observedAperturePixels=plan["fixedAperturePixels"],
                  filterResponseAtEachExposure=True, gaiaLineSpreadFunctionModelled=False,
                  calibratedCovarianceAvailable=False, independentAbsoluteCalibrationEstablished=False,
                  independentInstrumentObservedComparisons=2, scientificClosures=0, nativeExecutions=0)
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
