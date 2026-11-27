from contextlib import ExitStack
from pathlib import Path
import hashlib
import json
import runpy
import sys

sys.path.extend(sys.argv[1:3])
import numpy as np
from astropy.io import fits


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def checked(path, expected):
    if digest(path) != expected:
        raise ValueError(f"Changed evidence: {path.name}")
    return path


def load_json(path, expected):
    return json.loads(checked(path, expected).read_bytes())


def component(image, ops, old, center):
    choices = [row for row in ops["connected_long"](image, old) if
               [np.median(row[0]), np.median(row[1])] == center]
    if len(choices) != 1:
        raise ValueError("Component identity is ambiguous")
    return choices[0]


def allowed(stamp, cap, center=None, item=None):
    quality = stamp[1]
    valid = np.isin(quality, [0, 64])
    if item is not None:
        x, y = center
        xx, yy, flags = item
        if not np.isin(flags, [256, 320]).all():
            raise ValueError("Mixed quality in trail")
        valid[yy-y+cap, xx-x+cap] |= np.isin(quality[yy-y+cap, xx-x+cap], [256, 320])
    return valid


def estimate(samples, bg, support):
    fluxes = [float((signal[support]-level).sum()/seconds)
              for (signal, _), level, seconds in zip(samples, bg, (150, 150, 40, 40))]
    if min(fluxes) <= 0:
        raise ValueError("Nonpositive diagnostic flux")
    a, b, c, d = fluxes
    return {"rates": fluxes, "primaryVsShortMeanPercent": 100*(2*a/(c+d)-1),
            "replicaVsShortMeanPercent": 100*(2*b/(c+d)-1),
            "longPairDifferencePercent": 200*(b-a)/(a+b),
            "shortPairDifferencePercent": 200*(d-c)/(d+c)}


def main():
    original, sensitivity, protocol, out = map(Path, sys.argv[3:])
    cfg = json.loads(protocol.read_bytes())
    sens_ops = runpy.run_path(str(checked(sensitivity/"verifica.py", cfg["sensitivityCode"])))
    sens_cfg = load_json(sensitivity/"protocollo.json", cfg["sensitivityProtocol"])
    prior = load_json(sensitivity/"riscontro.json", cfg["sensitivityReport"])
    spec_a = load_json(original/"protocollo-jfdp02vfq.json", sens_cfg["primaryProtocol"])
    spec_b = load_json(original/"protocollo-jfdp02vdq.json", sens_cfg["siblingProtocol"])
    ops = runpy.run_path(str(checked(original/"verifica.py", sens_cfg["parentCode"])))
    receipt = load_json(original/"riscontro-jfdp02vfq.json", sens_cfg["primaryReport"])
    qualified = [row for row in receipt["rows"] if row["status"] == "MEASURED"]
    if len(qualified) != 1 or prior["replica"]["assessment"]["status"] != "UNUSABLE_COMMON_APERTURE":
        raise ValueError("Unexpected original qualification state")

    cap = max(bounds[-1] for bounds in cfg["skyAnnuli"])
    coord = np.arange(-cap, cap+1)
    distance = np.hypot(coord[:, None], coord)
    aperture = distance <= cfg["radiusPx"]
    pam = fits.getdata(checked(original/"wfc1_newpam.fits", spec_a["pam"]["1"]))
    with ExitStack() as stack:
        def frame(row):
            return ops["read_frame"](ops["open_input"](original/row["file"], row["sha256"], stack), row)[1]
        first, *short = [frame(row) for row in spec_a["inputs"]]
        second = frame(spec_b["inputs"][0])
        one = component(first, ops, spec_a, qualified[0]["centerXY"])
        two = component(second, ops, spec_b, prior["replica"]["assessment"]["centerXY"])
        center, refs, _ = sens_ops["positions"](ops, first, short, one, spec_a)
        center2, duplicate_refs, _ = sens_ops["positions"](ops, second, short, two, spec_b)
        if refs != duplicate_refs:
            raise ValueError("Short-reference centers do not match")
        centers = [center, center2, *refs]
        samples = [ops["stamp"](im, c, cap, pam) for im, c in zip([first, second, *short], centers)]
        if any(row is None for row in samples):
            raise ValueError("Clipped image window")
        keep = [allowed(samples[0], cap, center, one), allowed(samples[1], cap, center2, two)]
        keep.extend(allowed(sample, cap) for sample in samples[2:])
        full = aperture & keep[0] & keep[2] & keep[3]
        shared = full & keep[1]
        removed = full & ~shared
        strict = np.logical_and.reduce([np.isin(row[1], [0,64]) for row in samples])
        full_count, shared_count = (int(m.sum()) for m in (full, shared))
        if shared_count != prior["replica"]["apertureSupport"]["commonPixels"]:
            raise ValueError("Replica mask does not reproduce prior count")
        results = []
        for inner, outer in cfg["skyAnnuli"]:
            sky = strict & (distance >= inner) & (distance <= outer)
            if sky.sum() < 400:
                raise ValueError("Insufficient shared background")
            background = [float(np.median(signal[sky])) for signal, _ in samples]
            shared_fit = estimate(samples, background, shared)
            clean_fraction = []
            for i in (0,2,3):
                signal = samples[i][0]-background[i]
                clean_fraction.append(100*float(signal[removed].sum()/signal[full].sum()))
            clean_flux = [float((samples[i][0][full]-background[i]).sum()/time)
                          for i, time in ((0,150),(2,40),(3,40))]
            baseline = 100*(2*clean_flux[0]/(clean_flux[1]+clean_flux[2])-1)
            results.append({"skyPx": [inner,outer], "primaryVsShortMeanOriginalSupportPercent": baseline,
                            "sharedFit": shared_fit, "removedFluxPercentPrimaryShort1Short2": clean_fraction,
                            "primaryChangeFromMaskPercentagePoints": shared_fit["primaryVsShortMeanPercent"]-baseline})
    coverage = shared_count/int(aperture.sum())
    report = {"schema": cfg["schema"], "protocolSha256": digest(protocol), "centersXY": centers,
              "aperturePixels": int(aperture.sum()), "primaryAndShortSupportPixels": full_count,
              "sharedFourExposurePixels": shared_count, "maskedByReplica": int(removed.sum()),
              "originalCoverageAccepted": coverage >= cfg["originalMinimumCoverage"],
              "diagnosticOnly": True, "results": results, "scientificClosures": 0}
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, indent=2, sort_keys=True, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
