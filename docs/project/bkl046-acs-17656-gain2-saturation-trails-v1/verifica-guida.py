import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.append(sys.argv[1])
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.time import Time
import astropy.units as u


def sha(p):
    with p.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def checked(root, name, expected):
    path = root / name
    if sha(path) != expected:
        raise ValueError(f"Changed input {name}")
    return path


def utc(value):
    return datetime.strptime(value, "%Y.%j:%H:%M:%S").replace(tzinfo=timezone.utc)


def xy(ra, dec):
    return SkyCoord(ra * u.deg, dec * u.deg)


def measure(root, photos, row):
    obs = row["obs"]
    log = obs[:-1] + "j"
    sci = fits.getheader(checked(photos, obs+"_flt.fits", row["flt"]))
    disp = checked(root, row["log"]+"_jif.fits", row["jif"])
    samples = checked(root, row["log"]+"_jit.fits", row["jit"])
    with fits.open(disp) as hdr, fits.open(samples) as tab:
        hh = [hdu for hdu in hdr[1:] if hdu.header.get("EXPNAME") == log]
        jj = [hdu for hdu in tab[1:] if hdu.header.get("EXPNAME") == log]
        if len(hh) != 1 or len(jj) != 1:
            raise ValueError("Ambiguous telemetry extension")
        d, h, j = hdr[0].header, hh[0].header, jj[0].header
        if not (sci["ROOTNAME"] == obs and sci["EXPTIME"] == row["exptime"] and sci["PROPOSID"] == row["program"]
                and h["EXPNAME"] == log and j["EXPNAME"] == log and h["ROOTNAME"] == row["log"]):
            raise ValueError("Science/telemetry identity mismatch")
        start = Time(sci["EXPSTART"], format="mjd", scale="utc").to_datetime(timezone=timezone.utc)
        stop = Time(sci["EXPEND"], format="mjd", scale="utc").to_datetime(timezone=timezone.utc)
        delta_start = (start-utc(h["STARTIME"])).total_seconds()
        delta_stop = (stop-utc(h["ENDTIME"])).total_seconds()
        if max(abs(delta_start), abs(delta_stop)) > 2:
            raise ValueError("Science window does not match telemetry")
        data = jj[0].data
        point = xy(np.asarray(data["RA"]), np.asarray(data["DEC"]))
        median = xy(float(np.median(data["RA"])), float(np.median(data["DEC"])))
        target = xy(sci["RA_TARG"], sci["DEC_TARG"])
        take = np.asarray(data["TakeData"], dtype=int)
        seconds = np.asarray(data["Seconds"])
        if np.any(np.diff(seconds) <= 0) or not np.isin(take, [0, 1]).all():
            raise ValueError("Invalid samples")
        rms = [float(h[key]) if h[key] >= 0 else None for key in ("V2_RMS", "V3_RMS")]
        return {"obs": obs, "telemetryRoot": log, "startDifferenceSeconds": delta_start,
                "endDifferenceSeconds": delta_stop, "expFlag": sci["EXPFLAG"],
                "commandedMode": d["GUIDECMD"], "actualMode": h["GUIDEACT"],
                "guideAcquisitionFailed": bool(d["T_GSFAIL"]), "guideFailure": h.get("GSFAIL"),
                "takeDataFlagDown": bool(d["T_TDFDWN"]), "takeDataOnSamples": int(take.sum()),
                "totalJitSamples": len(take), "guideRmsMas": rms,
                "medianPointingDeg": [float(median.ra.deg), float(median.dec.deg)],
                "medianPointingToTargetArcsec": float(median.separation(target).arcsec),
                "firstToLastReconstructedArcsec": float(point[0].separation(point[-1]).arcsec)}


def main():
    root, photos, protocol, dest = map(Path, sys.argv[2:])
    cfg = json.loads(protocol.read_bytes())
    rows = [measure(root, photos, row) for row in cfg["inputs"]]
    pointing = [xy(*row["medianPointingDeg"]) for row in rows]
    summary = {"schema": cfg["schema"], "protocolSha256": sha(protocol), "rows": rows,
               "separationBetweenReconstructedMedianPointingsArcsec": float(pointing[0].separation(pointing[1]).arcsec),
               "scientificClosures": 0}
    with dest.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(summary, sort_keys=True, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
