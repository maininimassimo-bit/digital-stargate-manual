"""Compare disjoint GD153 blank-sky apertures with their diagonal FLC ERR null."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

PIN = "ae1bd626a019545d0775f0fff78328ff95fa2777e5f2446a46c6e07537e10c8d"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def checked(path, pin):
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == pin, f"Source SHA-256 differs: {path.name}")
    return raw


def archived(path, spec):
    zip_sha, name, sha = spec
    with ZipFile(BytesIO(checked(path, zip_sha))) as bundle:
        need(bundle.namelist().count(name) == 1, "Ambiguous report")
        raw = bundle.read(name)
    need(sha256(raw).hexdigest() == sha, "Report SHA-256 differs")
    return json.loads(raw)


def stats(np, values):
    array = np.array(values)
    if not len(array):
        return dict(count=0)
    median = float(np.median(array))
    return dict(count=len(array), median=median, rms=float(np.sqrt(np.mean(array**2))),
                normalizedMad=float(1.4826 * np.median(abs(array - median))),
                absoluteAbove1p96=int((abs(array) > 1.96).sum()),
                interval90=np.quantile(array, [.05, .95]).tolist())


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("protocol", "source", "natural", "clean", "err", "dependencies", "report"):
        cli.add_argument(name, type=Path)
    args = cli.parse_args()
    p = json.loads(checked(args.protocol, PIN))
    inputs = json.loads(checked(args.source / "protocollo.json", p["poseProtocol"]))
    natural, clean, err = (archived(getattr(args, key), p[key]) for key in ("natural", "clean", "err"))

    sys.path.insert(0, str(args.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits

    need((np.__version__, astropy.__version__) == ("2.3.5", "7.2.0"), "Dependency versions differ")
    pose = args.source / "source"
    pam_name = "UVIS1wfc3_map.fits"
    pam = fits.getdata(BytesIO(checked(pose / pam_name, inputs["inputs"][pam_name])))
    centers = {r["file"]: tuple(r["center"]) for r in natural["cases"] if "center" in r}
    centers.update({r["file"]: tuple(r["center"]) for r in clean["rows"] if "center" in r})
    pairs = [r for r in err["cases"] if r["state"] == "MEASURED"]
    names = {r[role]: r["band"] for r in pairs for role in ("target", "reference")}
    need(len(pairs) == 12 and all(name in centers for name in names), "Formal study linkage differs")
    inner, outer = p["skyAnnulus"]
    grid = p["centers"]
    need(grid["spacing"] > 2 * outer and grid["margin"] >= outer, "Patch supports overlap")
    coord = np.arange(-outer, outer + 1)
    radius2 = coord[:, None]**2 + coord**2
    ap_geometry = radius2 <= p["apertureRadius"]**2
    sky_geometry = (radius2 >= inner**2) & (radius2 <= outer**2)
    output_rows = []

    for name, band in sorted(names.items()):
        with fits.open(BytesIO(checked(pose / name, inputs["inputs"][name])), memmap=False) as h:
            sci, err_image, dq = (h[name, 1] for name in ("SCI", "ERR", "DQ"))
            height, width = sci.data.shape
            oy, ox = (abs(float(sci.header[k])) for k in ("LTV2", "LTV1"))
            need((int(oy), int(ox)) == (oy, ox) and h[0].header["FILTER"] == band
                 and sci.header["CCDCHIP"] == 1 and sci.header["BUNIT"] == err_image.header["BUNIT"] == "ELECTRONS"
                 and sci.data.shape == err_image.data.shape == dq.data.shape, "FLC input structure differs")
            oy, ox = int(oy), int(ox)
            gain = pam[oy:oy + height, ox:ox + width]
            values = sci.data.astype(float) * gain
            errors = err_image.data.astype(float) * gain
            valid = (dq.data == 0) & np.isfinite(values)
        seed = sha256(f'{p["rngSeed"]}:{name}'.encode()).digest()
        rng = np.random.default_rng(int.from_bytes(seed[:8], "big"))
        cx, cy = centers[name]
        for y in range(grid["margin"], height - grid["margin"], grid["spacing"]):
            for x in range(grid["margin"], width - grid["margin"], grid["spacing"]):
                row = dict(file=name, band=band, center=[x, y])
                output_rows.append(row)
                if (x - cx)**2 + (y - cy)**2 < grid["excludeWithinTarget"]**2:
                    row["state"] = "SOURCE_BUFFER"
                    continue
                window = np.s_[y - outer:y + outer + 1, x - outer:x + outer + 1]
                ap_mask, sky_mask = (valid[window] & mask for mask in (ap_geometry, sky_geometry))
                n, m = int(ap_mask.sum()), int(sky_mask.sum())
                row.update(apertureSamples=n, skySamples=m)
                if n < p["minimumApertureFraction"] * ap_geometry.sum() or m < p["minimumSkyFraction"] * sky_geometry.sum():
                    row["state"] = "INSUFFICIENT_DQ_SUPPORT"
                    continue
                source = values[window]
                sigma = errors[window]
                ap_vals, sky_vals = source[ap_mask], source[sky_mask]
                ap_std, sky_std = sigma[ap_mask], sigma[sky_mask]
                retained = sigma[ap_mask | sky_mask]
                if not (np.isfinite(retained).all() and (retained > 0).all()):
                    row["state"] = "INVALID_RETAINED_ERR"
                    continue
                sky_center = float(np.median(sky_vals))
                observed = float(np.sum(ap_vals - sky_center))
                largest = float(np.max(abs((source[ap_mask | sky_mask] - sky_center) / retained)))
                # The linear aperture sum is Gaussian under the independent-pixel null.
                ap_null = rng.normal(0., np.linalg.norm(ap_std), size=p["draws"])
                sky_null = np.median(rng.normal(0., sky_std, size=(p["draws"], m)), axis=1)
                aperture_noise = float(np.sqrt(np.square(ap_std).sum() + n*n*np.var(sky_null, ddof=1)))
                empirical_null_noise = float(np.std(ap_null - n*sky_null, ddof=1))
                row.update(state="MEASURED", apertureResidualElectrons=observed,
                           modelStdElectrons=aperture_noise, nullCheckStdElectrons=empirical_null_noise,
                           standardizedResidual=observed / aperture_noise, maxPixelResidualStd=largest,
                           belowFixedOutlierScreen=largest <= p["screenAbsSigma"])
    measured = [row for row in output_rows if row["state"] == "MEASURED"]
    need(measured and all(any(r["file"] == name for r in measured) for name in names),
         "Incomplete blank-sky coverage")
    def group(rowset):
        return dict(allSupported=stats(np, [r["standardizedResidual"] for r in rowset]),
                    fixedScreen=stats(np, [r["standardizedResidual"] for r in rowset if r["belowFixedOutlierScreen"]]))

    summary = dict(pooled=group(measured), byBand={band: group([r for r in measured if r["band"] == band])
                                                   for band in sorted(set(names.values()))},
                   byExposure={name: group([r for r in measured if r["file"] == name]) for name in sorted(names)})
    summary["centeredWithinExposure"] = {}
    for label, selected in (
        ("allSupported", measured),
        ("fixedScreen", [row for row in measured if row["belowFixedOutlierScreen"]]),
    ):
        distribution = []
        for filename in sorted(names):
            residuals = np.array([r["standardizedResidual"] for r in selected if r["file"] == filename])
            if len(residuals):
                distribution.extend(residuals - np.median(residuals))
        summary["centeredWithinExposure"][label] = stats(np, distribution)
    output = dict(schema=p["schema"] + "_RESULT", protocolSha256=PIN,
                  programSha256=sha256(Path(__file__).read_bytes()).hexdigest(), exposedFiles=len(names),
                  targetComparisons=len(pairs), patches=output_rows, summary=summary, independentTargets=1,
                  signalDependentCovarianceVerified=False, scientificClosures=0, nativeExecutions=0)
    with args.report.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(output, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()