"""Count exact raw detector-coordinate overlap with a frozen dark series."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


PARITIES = {"R": (0, 0), "G1": (0, 1), "G2": (1, 0), "B": (1, 1)}


def pinned_json(path, expected):
    data = path.read_bytes()
    assert sha256(data).hexdigest() == expected, path
    return json.loads(data)


def read_series(np, fits, path, rows, member, date, image_type, shape):
    with ZipFile(path) as archive:
        for row in rows:
            data = archive.read(row[member])
            assert sha256(data).hexdigest() == row["sha256"]
            with fits.open(BytesIO(data), memmap=False, uint=True) as hdus:
                header = hdus[0].header
                assert header["BITPIX"] == 16 and header["BZERO"] == 32768
                assert header["BSCALE"] == 1 and header["BAYERPAT"] == "RGGB"
                assert header["IMAGETYP"] == image_type and header["DATE-OBS"] == row[date]
                assert header["EXPTIME"] == 180 and header["GAIN"] == 100
                image = hdus[0].data
                assert image.shape == shape and image.dtype == np.uint16
                yield row, image


def tail_cutoff(np, values, size):
    counts = np.bincount(values.ravel(), minlength=65536)
    index = np.searchsorted(np.cumsum(counts[::-1]), size, side="left")
    return 65535 - int(index)


def rows_by_recurrence(np, light, dark_peak, ceiling, near, tail):
    populations = (
        ("allSites", np.ones(light.shape, dtype=bool)),
        ("darkCeiling", dark_peak == ceiling),
        ("darkNearCeiling", dark_peak >= near),
        ("darkUpperTail", dark_peak >= tail),
    )
    return {
        label: np.bincount(light[mask], minlength=16).tolist()
        for label, mask in populations
    }


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "light_archive", "light_receipt", "dark_archive",
                 "dark_receipt", "prior", "dependencies", "report"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    lights = pinned_json(a.light_receipt, p["lightReceipt"])["rows"]
    darks = pinned_json(a.dark_receipt, p["darkReceipt"])["sourceMembers"]["dark"]
    prior = pinned_json(a.prior, p["prior"])
    prev = {row["frameSha256"]: row for row in prior["frames"]}
    size = p["framesPerSeries"]
    assert len(lights) == len(darks) == len(prev) == size == 15
    for path, key in ((a.light_archive, "lightArchive"), (a.dark_archive, "darkArchive")):
        with path.open("rb") as f:
            assert file_digest(f, "sha256").hexdigest() == p[key]

    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    assert tail_cutoff(np, np.array([1, 10, 10, 20], np.uint16), 2) == 10
    shape = tuple(p["shape"])
    ceiling, near = p["ceiling"], p["nearCeiling"]
    dark_peak = np.zeros(shape, np.uint16)
    dark_events = []
    for row, image in read_series(np, fits, a.dark_archive, darks, "file", "date", "Dark", shape):
        np.maximum(dark_peak, image, out=dark_peak)
        dark_events.append({"sha256": row["sha256"], "ceiling": int(np.count_nonzero(image == ceiling))})
    occupancy = np.zeros(shape, np.uint8)
    for row, image in read_series(np, fits, a.light_archive, lights, "member", "dateObs", "Light", shape):
        clipped = image == ceiling
        for parity, (y, x) in PARITIES.items():
            expected = prev[row["sha256"]]["parities"][parity]["atDigitalCeiling"]
            assert np.count_nonzero(clipped[y::2, x::2]) == expected
        occupancy += clipped

    bands = {}
    denominator = p["darkUpperTailDenominator"]
    assert p["darkUpperTailNumerator"] == 1
    for parity, (y, x) in PARITIES.items():
        count, peak = occupancy[y::2, x::2], dark_peak[y::2, x::2]
        cutoff = tail_cutoff(np, peak, (peak.size + denominator - 1) // denominator)
        hist = rows_by_recurrence(np, count, peak, ceiling, near, cutoff)
        bands[parity] = {
            "darkPeakMaximum": int(peak.max()),
            "darkTailCutoff": cutoff,
            "siteHistogramsByLightRecurrence": hist,
            "sites": {name: sum(pop) for name, pop in hist.items()},
            "clippedLightSites": {name: sum(pop[1:]) for name, pop in hist.items()},
            "clippedLightEvents": {
                name: sum(n * frequency for n, frequency in enumerate(pop))
                for name, pop in hist.items()
            },
        }

    report = {"schema": "BKL046_M8M20_DETECTOR_CLIP_DARK_OVERLAP_RESULT_V1",
              "protocolSha256": sha256(raw).hexdigest(),
              "programSha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "lightFramesRead": len(lights), "darkFramesRead": len(darks),
              "lightDates": sorted(row["dateObs"] for row in lights),
              "darkDates": sorted(row["date"] for row in darks),
              "darkEventsByFrame": dark_events, "bands": bands,
              "nativeExecutions": 0, "scientificClosures": 0}
    with a.report.open("x", encoding="utf-8", newline="\n") as dst:
        json.dump(report, dst, indent=2, sort_keys=True, allow_nan=False)
        dst.write("\n")


if __name__ == "__main__":
    main()
