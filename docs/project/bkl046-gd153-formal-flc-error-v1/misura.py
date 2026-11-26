"""Propagate the diagonal FLC ERR model through exact GD153 aperture estimators."""
import argparse
from functools import lru_cache
from hashlib import sha256
from io import BytesIO
import json
from math import isclose, log10
from pathlib import Path
import sys
from zipfile import ZipFile

PIN = "b99596c0825d19cdee2351aa72cee8f0a555c58f979175a315a69485da150bf9"


def expect(condition, message):
    if not condition:
        raise ValueError(message)


def verified(path, pin):
    data = path.read_bytes()
    expect(sha256(data).hexdigest() == pin, f"Input changed: {path.name}")
    return data


def extract(path, pin, member, report_pin):
    with ZipFile(BytesIO(verified(path, pin))) as archive:
        expect(archive.namelist().count(member) == 1, "Ambiguous report")
        raw = archive.read(member)
    expect(sha256(raw).hexdigest() == report_pin, "Input report changed")
    return json.loads(raw)


def estimators(np, samples, sky_pixels, rings, missing_rings, pixels):
    sky = np.median(sky_pixels, axis=-1)
    centered = samples - sky[..., None]
    total = centered.sum(axis=-1)
    median_fill = total.copy()
    for k, missing in missing_rings.items():
        supported = rings == k
        if not supported.any():
            median_fill = None
            break
        median_fill += missing * np.median(centered[..., supported], axis=-1)
    return dict(zero=total, area=total * pixels / samples.shape[-1], annularMedian=median_fill)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for arg in ("protocol", "source", "naturalZip", "cleanZip", "dependencies", "report"):
        cli.add_argument(arg, type=Path)
    args = cli.parse_args()
    p = json.loads(verified(args.protocol, PIN))
    pose = json.loads(verified(args.source / "protocollo.json", p["sourceProtocolSha256"]))
    natural = extract(args.naturalZip, p["naturalArchiveSha256"], "riscontro.json", p["naturalReportSha256"])
    clean = extract(args.cleanZip, p["cleanArchiveSha256"], "riscontro-verificato.json", p["cleanReportSha256"])

    sys.path.insert(0, str(args.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits

    expect((np.__version__, astropy.__version__) == ("2.3.5", "7.2.0"), "Dependency versions differ")
    folder = args.source / "source"
    pam_name = "UVIS1wfc3_map.fits"
    pam = fits.getdata(BytesIO(verified(folder / pam_name, pose["inputs"][pam_name])))
    clean_rows = {row["file"]: row for row in clean["rows"]}
    rows = [row for row in natural["cases"] if row["family"] in p["targetFamilies"]]
    eligible = [row for row in rows if row["state"] == "MEASURED"]
    expect(len(rows) == 24 and len(eligible) == 12 and all(row["referenceCount"] == 1 for row in eligible),
           "Comparison coverage differs")
    inner, outer = p["skyAnnulus"]

    @lru_cache(maxsize=None)
    def propagate(filename, center):
        x, y = center
        with fits.open(BytesIO(verified(folder / filename, pose["inputs"][filename])), memmap=False) as h:
            science, error, quality = (h[name, 1] for name in ("SCI", "ERR", "DQ"))
            values, sigmas, flags = science.data.astype(float), error.data.astype(float), quality.data
            expect(values.shape == sigmas.shape == flags.shape and science.header["CCDCHIP"] == 1
                   and science.header["BUNIT"] == error.header["BUNIT"] == "ELECTRONS", "SCI/ERR units or shape differ")
            oy, ox = (abs(float(science.header[k])) for k in ("LTV2", "LTV1"))
            expect((int(ox), int(oy)) == (ox, oy), "Non-integral PAM offset")
            ox, oy = int(ox), int(oy)
            sy, sx = values.shape
            scale = pam[oy:oy + sy, ox:ox + sx]
            values *= scale
            sigmas *= scale
            rate = float(science.header["PHOTFLAM"]) / float(h[0].header["EXPTIME"])
        yy, xx = np.ogrid[:sy, :sx]
        r2 = (xx - x)**2 + (yy - y)**2
        aperture = r2 <= p["radius"]**2
        sky_geom = (r2 >= inner**2) & (r2 <= outer**2)
        valid = (flags == 0) & np.isfinite(values)
        used = aperture & valid
        sky = sky_geom & valid
        expect(used.any() and sky.sum() >= p["minSkyFraction"] * sky_geom.sum(), "Aperture or sky support differs")
        expect(np.isfinite(sigmas[used | sky]).all() and (sigmas[used | sky] > 0).all(), "Invalid retained ERR")
        sky_vals, sky_sig = values[sky], sigmas[sky]
        ap_vals, ap_sig = values[used], sigmas[used]
        rings = np.floor(np.sqrt(r2[used])).astype(int)
        keys, counts = np.unique(np.floor(np.sqrt(r2[aperture & ~valid])).astype(int), return_counts=True)
        missing = dict(zip(keys, counts, strict=True))
        full = int(aperture.sum())
        nominal = estimators(np, ap_vals, sky_vals, rings, missing, full)
        chunks = {key: [] for key, val in nominal.items() if val is not None}
        flag = sha256(json.dumps([p["baseSeed"], filename, center]).encode()).digest()
        rng = np.random.default_rng(int.from_bytes(flag[:8], "big"))
        sky_draws, zero_draws = [], []
        for index in range(0, p["samples"], p["chunkSize"]):
            take = min(p["chunkSize"], p["samples"] - index)
            draw_ap = rng.normal(ap_vals, ap_sig, size=(take, len(ap_vals)))
            draw_sky = rng.normal(sky_vals, sky_sig, size=(take, len(sky_vals)))
            draw = estimators(np, draw_ap, draw_sky, rings, missing, full)
            for key in chunks:
                chunks[key].append(draw[key] * rate)
            sky_draws.append(np.median(draw_sky, axis=1))
            zero_draws.append(draw_ap.sum(axis=1))
        draws = {key: np.concatenate(parts) for key, parts in chunks.items()}
        var_ap = float(np.square(ap_sig).sum())
        var_sky = float(np.var(np.concatenate(sky_draws), ddof=1))
        diagonal_flux_std = float(np.sqrt(var_ap + len(ap_vals)**2 * var_sky) * rate)
        empirical_flux_std = float(np.std(draws["zero"], ddof=1))
        expect(isclose(float(np.var(np.concatenate(zero_draws), ddof=1)), var_ap, rel_tol=.06)
               and isclose(empirical_flux_std, diagonal_flux_std, rel_tol=.06), "Monte Carlo variance check differs")
        counts = dict(aperture=full, missing=full - len(ap_vals), sky=len(sky_vals))
        return {k: float(v * rate) for k, v in nominal.items() if v is not None}, draws, counts

    cases = []
    for row in rows:
        if row["state"] != "MEASURED":
            cases.append(dict(target=row["file"], family=row["family"], state=row["state"]))
            continue
        target = row["file"]
        reference, = row["referenceFiles"]
        ref_row = clean_rows[reference]
        target_flux, target_draw, target_counts = propagate(target, tuple(row["center"]))
        ref_flux, ref_draw, ref_counts = propagate(reference, tuple(ref_row["center"]))
        need_nominal = ref_row["measurements"][p["aperture"]]["rate"] * ref_row["flam"]
        expect(ref_counts["missing"] == 0 and isclose(ref_flux["zero"], need_nominal, rel_tol=1e-10),
               "Clean reference replay differs")
        old = row["phases"][0]
        expect(old["offsetPx"] == [0, 0] and target_counts["missing"] == old["missing"], "Target geometry differs")
        methods = {}
        for method in p["methods"]:
            delta = -2500 * log10(target_flux[method] / ref_flux["zero"])
            expect(isclose(delta, old["withinVisitDifferenceMillimag"][method], abs_tol=1e-9),
                   "Nominal observed difference differs")
            numerator, denominator = target_draw[method], ref_draw["zero"]
            good = (numerator > 0) & (denominator > 0)
            expect(good.all(), "Invalid perturbation draws")
            result = -2500 * np.log10(numerator / denominator)
            noise = float(np.std(result, ddof=1))
            methods[method] = dict(observedDifferenceMillimag=delta, formalStdMillimag=noise,
                                   observedToFormalStd=delta / noise,
                                   perturbationCentral95Millimag=np.quantile(result, [.025, .975]).tolist())
        cases.append(dict(target=target, reference=reference, band=row["band"], visit=row["visit"],
                          family=row["family"], state=row["state"], targetCounts=target_counts,
                          referenceCounts=ref_counts, methods=methods))
    paired_controls = {tuple(sorted((row["target"], row["reference"]))) for row in cases
                       if row["state"] == "MEASURED" and row["family"] == "clean"}
    output = dict(schema=p["schema"] + "_RESULT", protocolSha256=PIN,
                  programSha256=sha256(Path(__file__).read_bytes()).hexdigest(), cases=cases,
                  distinctUnorderedCleanPairs=len(paired_controls), perturbationsPerAperture=p["samples"],
                  covarianceVerified=False, independentTargets=1, scientificClosures=0, nativeExecutions=0)
    with args.report.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()