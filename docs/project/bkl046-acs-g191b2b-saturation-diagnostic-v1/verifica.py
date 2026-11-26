import hashlib
import json
from pathlib import Path
import sys

sys.path.append(sys.argv[1])
import numpy as np
from astropy.io import fits


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def checked(path, expected):
    require(digest(path) == expected, f"Hash changed: {path.name}")
    return path


def stamp(image, x, y, radius):
    result = image[y-radius:y+radius+1, x-radius:x+radius+1]
    require(result.shape == (2 * radius + 1,) * 2, "Stamp crosses image boundary")
    return result


def raw_diagnostic(path, sci, dq, x, y, cfg, flt_header):
    with fits.open(path, memmap=False) as hdus:
        raw = hdus["SCI"].data.astype(float)
        header = hdus[0].header
        require(header["ROOTNAME"] == flt_header["ROOTNAME"], "RAW/FLT mismatch")
        require(header["CCDGAIN"] == 2 and hdus["SCI"].header["CCDCHIP"] == cfg["chip"], "RAW detector mismatch")
        require(hdus["SCI"].header["BUNIT"] == "COUNTS", "Unexpected RAW units")
    half = cfg["registrationHalfSize"]
    search = cfg["registrationSearch"]
    mask = np.isin(stamp(dq, x, y, half), cfg["allowedDQ"])
    reference = stamp(sci, x, y, half)[mask]
    candidates = []
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            sample = stamp(raw, x + dx, y + dy, half)[mask]
            candidates.append((float(np.corrcoef(reference, sample)[0, 1]), dx, dy))
    candidates.sort(reverse=True)
    corr, dx, dy = candidates[0]
    raw_peak = int(raw[y+dy, x+dx])
    require(corr > 0.98 and corr - candidates[1][0] > 1e-4 and raw_peak == raw.max(), "Ambiguous RAW registration")
    return {
        "offsetXY": [dx, dy], "correlation": corr, "nextCorrelation": candidates[1][0],
        "samples": int(mask.sum()), "centerDN": raw_peak,
        "adcHeadroomDN": cfg["nominalAdcMaxDN"] - raw_peak,
        "satufile": flt_header["SATUFILE"],
    }


def measure(entry, cfg, dirs, pam):
    star, obs = entry["star"], entry["id"]
    path = checked(dirs[star] / (obs + "_flt.fits"), entry["flt"])
    with fits.open(path, memmap=False) as hdus:
        header = hdus[0].header
        plane = hdus["SCI"]
        require(
            header["PROPOSID"] == cfg["program"]
            and cfg["filter"] in (header["FILTER1"], header["FILTER2"])
            and header["APERTURE"] == cfg["aperture"]
            and header["CCDAMP"] == cfg["amp"]
            and plane.header["CCDCHIP"] == cfg["chip"]
            and plane.header["BUNIT"] == "ELECTRONS",
            f"Unexpected detector configuration: {obs}",
        )
        sci = plane.data.astype(float)
        dq = hdus["DQ"].data.astype(int)
        origin_x, origin_y = (-int(plane.header[key]) for key in ("LTV1", "LTV2"))
    y, x = (int(v) for v in np.unravel_index(sci.argmax(), sci.shape))
    radius = cfg["skyAnnulus"][1]
    dy, dx = np.mgrid[-radius:radius+1, -radius:radius+1]
    distance = np.hypot(dx, dy)
    quality = stamp(dq, x, y, radius)
    valid = np.isin(quality, cfg["allowedDQ"])
    center = distance == 0
    count_full = int(np.count_nonzero(dq & cfg["fullWellBit"]))
    count_adc = int(np.count_nonzero(dq & cfg["adcBit"]))
    center_dq = int(dq[y, x])
    require(count_full == int("raw" in entry) and count_adc == 0, f"Unexpected saturation flags: {obs}")
    require(center_dq == cfg["fullWellBit"] if "raw" in entry else center_dq in cfg["allowedDQ"], f"Unexpected center quality: {obs}")
    corrected = stamp(sci, x, y, radius) * stamp(pam, origin_x + x, origin_y + y, radius)
    require(np.isfinite(corrected).all(), "Non-finite samples")
    sky = valid & (distance >= cfg["skyAnnulus"][0]) & (distance <= radius)
    require(sky.sum() > 100, "Too few usable sky pixels")
    background = float(np.median(corrected[sky]))
    corrected -= background

    apertures = {}
    for aperture in cfg["apertureRadii"]:
        selected = (distance <= aperture) & valid & ~center
        excluded = float(corrected[selected].sum())
        included = excluded + float(corrected[center][0])
        require(included > 0, "Nonpositive aperture sum")
        apertures[str(aperture)] = {
            "recordedIncludingCenterE": included, "excludingCenterE": excluded,
            "removedPercentOfRecorded": 100 * (included - excluded) / included,
            "otherMaskedPixels": int(((distance <= aperture) & ~valid & ~center).sum()),
        }
    wing = (distance >= cfg["wingAnnulus"][0]) & (distance <= cfg["wingAnnulus"][1])
    # Reject asymmetric coverage instead of imputing any detector pixels.
    wing_stripes = {}
    masked_wing = int((wing & ~valid).sum())
    wing_flux = None
    if masked_wing == 0:
        wing_flux = float(corrected[wing].sum())
        require(wing_flux > 0, "Nonpositive wing sum")
        for width in cfg["stripeHalfWidths"]:
            x_stripe = float(corrected[wing & (np.abs(dy) <= width)].sum()) / wing_flux
            y_stripe = float(corrected[wing & (np.abs(dx) <= width)].sum()) / wing_flux
            wing_stripes[str(width)] = {"alongXFraction": x_stripe, "alongYFraction": y_stripe}
    row = {
        "id": obs, "star": star, "peakXYZeroBased": [x, y], "centerRecordedE": float(sci[y, x]),
        "centerDQ": center_dq, "fullWellFlags": count_full, "adcFlags": count_adc,
        "skyPixels": int(sky.sum()), "skyCorrectedE": background, "apertures": apertures,
        "wingE": wing_flux, "wingStripes": wing_stripes, "maskedWingPixels": masked_wing,
    }
    if "raw" in entry:
        raw_path = checked(dirs["raw"] / (obs + "_raw.fits"), entry["raw"])
        row["raw"] = raw_diagnostic(raw_path, sci, dq, x, y, cfg, header)
    return row


def main():
    _, _, protocol, raw, saturated, gd71, gd153, pam_path, output = sys.argv
    cfg = json.loads(Path(protocol).read_bytes())
    directories = dict(zip(("raw", "G191B2B", "GD71", "GD153"), map(Path, (raw, saturated, gd71, gd153))))
    pam = fits.getdata(checked(Path(pam_path), cfg["pam"]["sha256"]))
    rows = [measure(entry, cfg, directories, pam) for entry in cfg["exposures"]]
    report = {
        "schema": cfg["schema"], "protocolSha256": digest(Path(protocol)),
        "results": rows, "coreRecovered": False, "scientificClosures": 0,
    }
    with Path(output).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
