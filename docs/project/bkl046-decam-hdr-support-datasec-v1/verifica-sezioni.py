"""Verify DECam cutout origins and restrict short-exposure support to CCD DATASEC."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import re
import runpy
import sys


def sha(path):
    with path.open("rb") as f:
        return file_digest(f, "sha256").hexdigest()


def section(text):
    values = [int(value) for value in re.fullmatch(r"\[(\d+):(\d+),(\d+):(\d+)\]", text).groups()]
    x, x1, y, y1 = values
    assert x <= x1 and y <= y1
    return (x-1, x1, y-1, y1)


def inside(np, x, y, rect):
    left, right, bottom, top = rect
    return (x >= left) & (x < right) & (y >= bottom) & (y < top)


def main():
    parser = argparse.ArgumentParser()
    for name in ("root", "sourceKit", "dependencies", "report"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    file = a.root / "protocollo-sezioni.json"
    p = json.loads(file.read_bytes())
    source_report = a.sourceKit / "riscontro.json"
    assert sha(source_report) == p["sourceReportSha256"]
    old = json.loads(source_report.read_bytes())
    assert sha(a.root / "misura.py") == p["supersetProgram"]
    assert sha(a.root / "riscontro.json") == p["supersetReport"]
    support = runpy.run_path(str(a.root / "misura.py"))["supported"]

    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    frames = {}
    results = []
    for item in old["fields"]["M8"]["frames"]:
        original = a.sourceKit / item["file"]
        wide = "wide-" + item["file"]
        full = a.root / wide
        assert sha(original) == item["sha256"] and sha(full) == p["wideSha256"][wide]
        with fits.open(full, memmap=False) as f, fits.open(original, memmap=False) as s:
            full_hdu, = f
            small, = s
            assert full_hdu.data.shape == (4146, 2160) and small.data.dtype == np.uint16
            f_h, s_h = full_hdu.header, small.header
            needed = ("DATASEC", "DATASECA", "DATASECB", "SATURATA", "SATURATB")
            for k in (*needed, "CCDNUM", "DATE-OBS", "EXPTIME"):
                assert f_h[k] == s_h[k]
            x0, y0 = [round(f_h[key] - s_h[key]) for key in ("CRPIX1", "CRPIX2")]
            assert np.array_equal(small.data, full_hdu.data[y0:y0+small.data.shape[0], x0:x0+small.data.shape[1]])
            # Both headers agree on the absolute sky coordinates of the subarray corners.
            small_wcs, full_wcs = WCS(s_h).celestial, WCS(f_h).celestial
            ys, xs = np.array([[0, 0], [small.data.shape[0]-1, small.data.shape[1]-1]]).T
            np.testing.assert_allclose(small_wcs.pixel_to_world_values(xs, ys),
                                       full_wcs.pixel_to_world_values(x0+xs, y0+ys), atol=1e-10, rtol=0)
            yy, xx = np.indices(small.data.shape)
            sci = inside(np, x0+xx, y0+yy, section(f_h["DATASEC"]))
            amp = [inside(np, x0+xx, y0+yy, section(f_h["DATASEC"+key])) for key in "AB"]
            assert np.array_equal(amp[0] | amp[1], sci) and not (amp[0] & amp[1]).any()
            values = small.data.copy()
            clipped, by_amp = np.zeros(sci.shape, dtype=bool), {}
            for key, mask in zip("AB", amp, strict=True):
                threshold = f_h["SATURAT"+key]
                high = mask & (values >= threshold)
                clipped |= high
                by_amp[key] = {"headerLevelADU": threshold, "scienceSamples": int(mask.sum()),
                               "atOrAboveLevel": int(high.sum())}
            x, y = item["centerXY"]
            center_in_sci = bool(inside(np, x+x0, y+y0, section(f_h["DATASEC"])))
            results.append({
                "seconds": item["exposureSeconds"], "source": item["source"], "rawSubarrayOriginXY": [x0, y0],
                "archiveFullCcdCutout": wide,
                "centerInDataSection": center_in_sci, "scienceSamples": int(sci.sum()),
                "nonScienceSamples": int((~sci).sum()), "zerosInScience": int(np.count_nonzero(sci & (values == 0))),
                "zerosOutsideScience": int(np.count_nonzero(~sci & (values == 0))), "amplifiers": by_amp,
                "samplesAtOrAboveAmplifierLevel": int(clipped.sum()),
            })
            frames[item["exposureSeconds"]] = (small_wcs, np.where(sci, values, 0), clipped,
                                               min(item["headerAmplifierLevelsADU"]))
    reports = []
    for long, short in ((100, 45), (100, 30), (45, 30)):
        w_l, _, clipped, _ = frames[long]
        w_s, values, _, low = frames[short]
        y, x = np.nonzero(clipped)
        a_1, a_2 = w_l.pixel_to_world_values(x, y)
        mapped = np.stack(w_s.world_to_pixel_values(a_1, a_2), axis=1)
        assert np.isfinite(mapped).all()
        details, _ = support(np, values, mapped, low, p["guardLevels"])
        reports.append({"longSeconds": long, "shortSeconds": short,
                        "sourceScienceSamplesAtOrAboveAmplifierLevel": len(x), **details})
    out = {"schema": "BKL046_DECAM_HDR_M8_DATASEC_RESULT_V1", "protocolSha256": sha(file),
           "programSha256": sha(Path(__file__)), "frames": results, "comparisons": reports,
           "fluxReferenceQualified": False, "nativeExecutions": 0, "scientificClosures": 0}
    with a.report.open("x", encoding="utf-8", newline="\n") as dst:
        json.dump(out, dst, indent=2, sort_keys=True, allow_nan=False)
        dst.write("\n")


if __name__ == "__main__":
    main()
