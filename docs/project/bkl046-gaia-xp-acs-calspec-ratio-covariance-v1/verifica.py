"""Propagate coefficient covariance to the pinned ACS standards and compare diagnostic bounds."""
import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import runpy
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import numpy as np

PIN = "e003c02ce90a3087660986c8ce28c3c44c4ae6835fc5a1a34486d9ad4900e727"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pinned(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected, "Input digest differs")
    return raw


def basis_model(capsule, spec, n):
    with ZipFile(BytesIO(pinned(capsule, spec["archiveSha256"]))) as parent:
        with ZipFile(BytesIO(parent.read("objects/Prove-GaiaXPy-campionamento-reale-v3.zip"))) as child:
            raw = child.read("real/Source-GaiaXPy-real-XpFilter_v375wiv142r.xml")
    require(sha256(raw).hexdigest() == spec["modelSha256"], "GaiaXPy model differs")
    model = ET.fromstring(raw)
    bands = {}
    for band in ("bp", "rp"):
        values = model.find(f"XpSampling/{band}SampledBases")
        require(int(values.attrib["dimension"]) == 55, "Unexpected basis dimension")
        x = np.array([float(item.text) for item in values]).reshape(n, 55)
        w = np.array([float(item.text) for item in model.find(f"XpMerge/{band}Weights")])
        require(w.shape == (n,), "Unexpected merge weight dimensions")
        bands[band] = (x, w)
    require(np.allclose(bands["bp"][1] + bands["rp"][1], 1., atol=1e-12, rtol=0.),
            "Merge weights do not sum to one")
    return model.findtext("solutionId"), bands


def decode(row, band, design, weights, basis_id):
    coefficient, sigma, packed = [
        np.array(json.loads(row[band+"_"+key]), dtype=float)
        for key in ("coefficients", "coefficient_errors", "coefficient_correlations")]
    n = int(row[band+"_n_parameters"])
    stdev = float(row[band+"_standard_deviation"])
    require(n == 55 and int(row[band+"_basis_function_id"]) == basis_id and stdev > 0
            and packed.shape == (1485,) and coefficient.shape == sigma.shape == (n,),
            "Coefficient metadata differs")
    corr = np.eye(n)
    i, j = np.tril_indices(n, -1)
    corr[i,j] = corr[j,i] = packed
    coefficient_cov = corr * np.outer(sigma, sigma)
    require(np.linalg.eigvalsh(corr)[0] > 0, "Coefficient correlation is not positive definite")
    single = design @ coefficient_cov @ design.T
    spectral = weights[:, None] * design
    return spectral @ coefficient, spectral @ coefficient_cov @ spectral.T, single * weights / stdev**2


def design_weights(chain, grid, order):
    edges = np.unique(np.concatenate([grid, *(x for x, _ in chain)]))
    half = np.diff(edges) / 2
    nodes, quadrature = np.polynomial.legendre.leggauss(order)
    x = (edges[:-1] + half)[:, None] + half[:, None] * nodes
    w = half[:, None] * quadrature * x
    for wave, response in chain:
        w *= np.interp(x, wave, response, left=0., right=0.)
    include = (x >= grid[0]) & (x < grid[-1])
    left = np.searchsorted(grid, x[include], side="right") - 1
    t = (x[include] - grid[left]) / (grid[left+1] - grid[left])
    out = np.bincount(left, w[include]*(1-t), minlength=len(grid))
    out += np.bincount(left+1, w[include]*t, minlength=len(grid))
    return out


def relative_sigmas(design, flux, bp, rp, i, j):
    means = design @ flux
    g = design[i]/means[i] - design[j]/means[j]
    s = np.array([np.sqrt(g @ c @ g) for c in (bp, rp)])
    conditional = float(np.linalg.norm(s))
    require(conditional > 0, "Nonpositive formal uncertainty")
    return dict(conditional=conditional, lowerUnknownCross=float(abs(s[0]-s[1])),
                upperUnknownCross=float(s.sum()),
                diagonalOnly=float(np.sqrt(np.sum(g*g*np.diag(bp+rp)))))


def main():
    protocol, continuo, sampled_path, prior_dir, acs_path, gd71_path, gd153_path, capsule, out = map(Path, sys.argv[1:])
    plan = json.loads(pinned(protocol, PIN))
    source_receipt = json.loads(pinned(continuo / "riscontro.json", plan["continuousReceiptSha256"]))
    catalogue = json.loads(pinned(sampled_path, plan["sampledSha256"]))
    prior_plan = json.loads(pinned(prior_dir / "protocollo.json", plan["photometryProtocolSha256"]))
    prior_result = json.loads(pinned(prior_dir / "riscontro.json", plan["photometryReceiptSha256"]))
    codes = pinned(prior_dir / "verifica.py", plan["priorPhotometryRunnerSha256"])
    env = {"__name__":"verified_photometry"}
    exec(compile(codes, "verified_photometry.py", "exec"), env)
    acs = json.loads(pinned(acs_path, prior_plan["acsProtocolSha256"]))
    sys.path.insert(0, acs["packages"])
    from astropy.io import fits
    helper = Path(acs["helper"])
    pinned(helper, acs["helperSha256"])
    throughput = runpy.run_path(str(helper))["throughput"]
    capture = Path(acs["capture"])
    captures = json.loads(pinned(capture, acs["captureSha256"]))
    require(captures["routes"] == acs["routes"], "Capture route differs")
    for item in sorted({name for route in acs["routes"].values() for name in route}):
        pinned(capture.parent / item, captures["components"][item]["sha256"])
    grid = np.array(catalogue["gridNm"], dtype=float)
    require(np.array_equal(grid, np.arange(336.,1021.,2.)), "Wavelength grid differs")
    solution, model = basis_model(capsule, plan, len(grid))
    reports = {}
    for star, exposure_path in (("GD71", gd71_path), ("GD153", gd153_path)):
        raw = pinned(continuo / (star+"-continuous-row.csv"), plan["continuousRows"][star])
        header, marker, content = raw.partition(b"\n")
        require(marker and sha256(content).hexdigest() == source_receipt["targets"][star]["originalRowSha256"],
                "Original row digest differs")
        row, = csv.DictReader(raw.decode().splitlines())
        observed = catalogue["spectra"][star]
        require(row["source_id"] == observed["sourceId"] and row["solution_id"] == observed["solutionId"],
                "Catalogue products disagree")
        products = [decode(row, band, *model[band], plan["basisIds"][band]) for band in ("bp", "rp")]
        flux = products[0][0] + products[1][0]
        bp, rp = [item[1] for item in products]
        formal = bp + rp
        gaia_flux, errors = [np.array(observed[key]) for key in ("flux", "fluxError")]
        checks = {"flux":float(np.max(abs(flux/gaia_flux-1))),
                  "error":float(np.max(abs(np.sqrt(np.diag(formal))/errors-1)))}
        require(all(checks[key] <= limit for key, limit in plan["relativeReplayTolerance"].items()),
                f"Published Gaia replay exceeds tolerance for {star}: {checks}")
        source = products[0][2] + products[1][2]
        sd = np.sqrt(np.diag(source))
        lower = np.tril(source/np.outer(sd,sd),-1)
        history_corr = lower + lower.T + np.eye(len(grid))
        minimum = float(np.linalg.eigvalsh(history_corr)[0])
        exposure = json.loads(pinned(exposure_path, prior_plan["targets"][star]["exposures"]))
        mean = []
        for label in prior_plan["bands"]:
            vectors = []
            for image in exposure["rows"]:
                if image["band"] != label:
                    continue
                throughput.__globals__["EPOCH"] = image["startMjd"]
                chain = [throughput(np, fits, item) for item in acs["routes"][label.lower()]]
                a, b = [design_weights(chain,grid*10.,order) for order in prior_plan["quadratureOrders"]]
                np.testing.assert_allclose(a,b,rtol=1e-9,atol=1e-12)
                vectors.append(a)
            require(len(vectors)==2, "Missing repeated exposure")
            mean.append(np.mean(vectors,axis=0))
        design = np.stack(mean)
        predicted = design @ (gaia_flux * prior_plan["gaiaToFlamFactor"]) * env["RATE_FACTOR"]
        base = prior_result["comparisons"][star]
        np.testing.assert_allclose(predicted,
            [base["averageRates"][label]["gaiaFullGridRate"] for label in prior_plan["bands"]],
            rtol=1e-10,atol=0.)
        masked = design.copy()
        a, b = prior_plan["maskNm"]
        masked[:, (grid >= a) & (grid <= b)] = 0.
        results = {}
        for ratio in prior_plan["ratios"]:
            i, j = [prior_plan["bands"].index(label) for label in ratio.split("/")]
            s = relative_sigmas(design, flux, bp, rp, i, j)
            delta = base["ratios"][ratio]
            results[ratio] = dict(full=s, masked=relative_sigmas(masked,flux,bp,rp,i,j),
                    sampledGaiaVersusCalspecSameGrid=delta["gaiaVersusCalspecSameGridFraction"],
                    observedApertureVersusSampledGaia=delta["observedVersusGaiaFraction"],
                    observedResidualDividedByUpperGaiaFormalSigma=abs(delta["observedVersusGaiaFraction"])/s["upperUnknownCross"])
        reports[star] = dict(catalogueSolutionId=row["solution_id"], numericalReplay=checks,
                             historicalCorrelationMinimum=minimum,
                             historicalCorrelationFailsTolerance=minimum < -plan["normalizedCorrelationNegativeModeTolerance"],
                             ratios=results)
    receipt = dict(schema="BKL046_GAIAXP_ACS_STANDARD_COVARIANCE_RESULT_V1", protocolSha256=PIN,
                   modelSolutionId=solution, formalConditionalAssumesIndependentBpRp=True,
                   crossBlockBoundsHoldWithFixedPublishedMarginals=True,
                   instrumentSystematicsIncluded=False, observedUncertaintyCombined=False,
                   scientificClosures=0, nativeExecutions=0, targets=reports)
    with out.open("x",encoding="utf-8",newline="\n") as file:
        json.dump(receipt,file,sort_keys=True,indent=2,allow_nan=False)
        file.write("\n")


if __name__=="__main__":
    main()
