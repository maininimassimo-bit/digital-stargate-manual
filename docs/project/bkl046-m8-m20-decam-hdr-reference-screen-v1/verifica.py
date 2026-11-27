"""Qualify provenance and conservative saturation screening in NOIRLab cutouts."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlsplit
from xml.etree import ElementTree


def digest(data):
    return sha256(data).hexdigest()


def rows(path, expected):
    data = path.read_bytes()
    assert digest(data) == expected
    root = ElementTree.fromstring(data)
    table = root.find(".//{*}TABLE")
    columns = [node.get("name") for node in table.findall("{*}FIELD")]
    return [dict(zip(columns, [cell.text for cell in row], strict=True))
            for row in table.findall(".//{*}TR")]


def main():
    cli = argparse.ArgumentParser()
    for name in ("root", "dependencies", "report"):
        cli.add_argument(name, type=Path)
    a = cli.parse_args()
    raw = (a.root / "protocollo.json").read_bytes()
    p = json.loads(raw)
    sys.path.insert(0, str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    expected_hashes = json.loads((a.root / "impronte-fits.json").read_bytes())
    reports = {}
    verified = set()
    for field, target in p["targets"].items():
        catalog = rows(a.root / f"{field}-votable.xml", target["catalogSha256"])
        seen = set()
        frames = []
        for row in catalog:
            url = urlsplit(row["access_url"])
            source, = parse_qs(url.query)["siaRef"]
            if source not in target["selected"]:
                continue
            assert source not in seen
            assert url.scheme == "https" and url.netloc == "datalab.noirlab.edu"
            assert row["proctype"] == "Raw" and row["obs_bandpass"] == "r" and row["instrument_name"] == "DECam"
            seen.add(source)
            name = target["selected"][source]
            file = a.root / name
            raw_fits = file.read_bytes()
            assert digest(raw_fits) == expected_hashes[name]
            verified.add(name)
            with fits.open(file, memmap=False) as hdus:
                assert len(hdus) == 1
                header, data = hdus[0].header, hdus[0].data
                assert data.dtype == np.uint16 and data.ndim == 2
                assert header["DATE-OBS"] == row["date_obs"]
                assert header["INSTRUME"] == "DECam" and header["FILTER"].startswith("r DECam")
                assert float(header["EXPTIME"]) == float(row["exptime"])
                assert header["BUNIT"].lower() == "adu"
                levels = [float(header[key]) for key in ("SATURATA", "SATURATB")]
                wcs = WCS(header).celestial
                x, y = wcs.world_to_pixel_values(target["ra"], target["dec"])
                assert np.isfinite([x, y]).all()
                inside = bool(0 <= x < data.shape[1] and 0 <= y < data.shape[0])
                low, high = min(levels), max(levels)
                frames.append({
                    "source": source, "file": name, "sha256": expected_hashes[name], "bytes": len(raw_fits),
                    "archiveCutoutUrl": row["access_url"], "archiveProgram": row["project_code"],
                    "dateObs": header["DATE-OBS"], "exposureSeconds": float(header["EXPTIME"]),
                    "CCDNUM": int(header["CCDNUM"]), "filter": header["FILTER"],
                    "shapeYX": list(data.shape), "centerXY": [round(float(x), 6), round(float(y), 6)],
                    "catalogCenterInside": inside, "minimumCode": int(data.min()), "maximumCode": int(data.max()),
                    "headerAmplifierLevelsADU": levels, "zeroCodes": int(np.count_nonzero(data == 0)),
                    "nonzeroBelowBoth": int(np.count_nonzero((data > 0) & (data < low))),
                    "atOrAboveLowerLevelOnly": int(np.count_nonzero((data >= low) & (data < high))),
                    "atOrAboveBoth": int(np.count_nonzero(data >= high)),
                })
        assert seen == set(target["selected"])
        for frame in frames:
            assert sum(frame[k] for k in ("zeroCodes", "nonzeroBelowBoth", "atOrAboveLowerLevelOnly",
                                          "atOrAboveBoth")) == int(np.prod(frame["shapeYX"]))
        reports[field] = {"catalogRows": len(catalog), "frames": sorted(frames, key=lambda row: row["exposureSeconds"])}
    assert verified == set(expected_hashes)
    out = {"schema": "BKL046_M8M20_DECAM_REFERENCE_CHECK_RESULT_V1",
           "programSha256": digest(Path(__file__).read_bytes()), "protocolSha256": digest(raw),
           "fields": reports, "filesVerified": len(verified), "fluxReferenceQualified": False,
           "nativeExecutions": 0, "scientificClosures": 0}
    with a.report.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(out, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
