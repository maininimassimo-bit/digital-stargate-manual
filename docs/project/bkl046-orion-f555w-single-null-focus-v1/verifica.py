"""Reproduce paired single/double PSF simulations on the archived pixel support."""
import hashlib
import io
import json
from pathlib import Path
import sys

root, runtime, previous, report = map(Path, sys.argv[1:])
sys.path.insert(0, str(runtime))
import astropy
from astropy.io import fits
import numpy as np


def pinned(path, sha):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise ValueError(f"Changed input: {path.name}")
    return data


def fit_support(obs, cfg):
    data = pinned(previous / "stamps" / obs["stampFile"], obs["stampSha256"])
    with np.load(io.BytesIO(data), allow_pickle=False) as z:
        sci, err, dq, lower = (z[key] for key in ("sci", "err", "dq", "lowerXY"))
    y, x = np.indices(sci.shape)
    x += lower[0] - obs["peakXY"][0]
    y += lower[1] - obs["peakXY"][1]
    usable = (dq == 0) & np.isfinite(sci) & np.isfinite(err) & (err > 0)
    usable &= x*x + y*y <= cfg["fitRadiusPx"]**2
    return np.column_stack((x[usable], y[usable])), err[usable].astype(float)


def run_case(engine, psfs, xy, err, values, cfg, spec):
    folds = []
    for fold in (0, 1):
        result = engine["fit_fold"](psfs, xy, values, err, (xy.sum(axis=1) % 2) == fold, cfg)
        if result["status"] != "MEASURED":
            folds.append({"status": result["status"]})
            continue
        measured = result["two"]["separationPx"] * cfg["nominalMasPerPixel"]
        ratio = result["two"]["secondaryToPrimaryFlux"]
        expected = spec["separationPx"] * cfg["nominalMasPerPixel"]
        tolerance = max(cfg["separationAbsoluteToleranceMas"], expected * cfg["separationRelativeTolerance"])
        folds.append(dict(status=result["status"], gain=result["heldoutGain"], separationMas=measured,
                          fluxRatio=ratio, focusSingle=result["one"]["focusIndex"], focusDouble=result["two"]["focusIndex"],
                          parametersPx=result["two"]["parametersPx"],
                          matchesInjectedPair=abs(measured-expected)<=tolerance and
                          abs(ratio/spec["secondaryFluxRatio"]-1)<=cfg["relativeFluxRatioTolerance"]))
    gains = all(fold.get("gain", 0) > 0 for fold in folds)
    return dict(bothGainsPositive=gains, bothGainsAndMatch=gains and
                all(fold.get("matchesInjectedPair", False) for fold in folds), folds=folds)


def main():
    raw = (root / "protocollo.json").read_bytes()
    spec = json.loads(raw)
    if (astropy.__version__, np.__version__) != ("7.2.0", "2.3.5"):
        raise ValueError("Runtime changed")
    engine_source = pinned(previous / "verifica-fit.py", spec["engineSha256"]).decode("utf-8")
    engine = {"__name__": "pinned_fit_engine"}
    boundary = engine_source.index('\nraw=(root/"protocollo.json")')
    exec(compile(engine_source[:boundary], "pinned_fit_engine.py", "exec"), engine)
    cfg = json.loads(pinned(previous / "protocollo-fit.json", spec["engineProtocolSha256"]))
    data = pinned(previous / "fit" / cfg["library"], spec["librarySha256"])
    with fits.open(io.BytesIO(data), memmap=False) as h:
        header, cube = h[0].header, h[0].data.astype(float)
    parent = json.loads(pinned(previous / "riscontro.json", spec["parentReportSha256"]))
    observations = [obs for obs in parent["observations"] if obs["status"] == "RECORDED"]
    results = []
    for i, obs in enumerate(observations):
        xy, err = fit_support(obs, cfg)
        psfs = engine["loc_psfs"](cube, header, obs["peakXY"], obs["chip"])
        index = spec["truthFocusLowerIndices"][i]
        truth = 0.5 * (psfs[index] + psfs[index + 1])
        primary = np.array(spec["primaryXY"])
        angle = np.deg2rad(spec["anglesDeg"][i])
        companion = primary + spec["separationPx"] * np.array([np.cos(angle), np.sin(angle)])
        one = engine["interp"](truth, *(xy-primary).T)
        two = engine["interp"](truth, *(xy-companion).T)
        support_noise = np.random.default_rng(spec["seedBase"] + i).standard_normal(len(err))*err
        background = 12 + 0.21*xy[:, 0] - 0.19*xy[:, 1]
        for snr in spec["peakSNR"]:
            scale = snr / (one/err).max()
            single = scale*one + background + support_noise
            double = single + scale*spec["secondaryFluxRatio"]*two
            pair = dict(root=obs["root"], pixels=len(err), nominalPeakSNR=snr, truthFocusBetween=[index,index+1],
                        null=run_case(engine, psfs, xy, err, single, cfg, spec),
                        injectedPair=run_case(engine, psfs, xy, err, double, cfg, spec))
            results.append(pair)
        print(obs["root"], "paired controls evaluated", flush=True)
    with report.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(dict(schema=spec["schema"], protocolSha256=hashlib.sha256(raw).hexdigest(), results=results,
                       nativeExecutions=0, scientificClosures=0), out, sort_keys=True, indent=2, allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
