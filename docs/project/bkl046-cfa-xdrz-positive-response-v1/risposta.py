from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

parser = ArgumentParser()
for key in ("parent", "packages", "output"):
    parser.add_argument(key, type=Path)
parser.add_argument("--exports", type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np
from astropy.io import fits

PIN = "677460604bd564285b0571a7149f22f7ae6ea7aed27e5badc1d71b42b0474a0f"
ROOT = Path("O:/BKL046-CFA-XDRZ-risposta-relativa-v1/fixture")
NS = "http://www.pixinsight.com/xdrz"
ET.register_namespace("", NS)
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
CASE_ORDER = ("baseline", "first", "second")
POINTS = [(14, 7, 13, 8), (15, 6, 14, 7)]
TOL = 1e-6


def sha(raw):
    return sha256(raw).hexdigest()


def read(path):
    with path.open("rb") as stream:
        raw = stream.read(262145)
    if not 0 < len(raw) <= 262144:
        raise ValueError(f"Unexpected size: {path.name}")
    return raw


raw_receipt = read(args.parent / "riscontro.json")
if sha(raw_receipt) != PIN:
    raise ValueError("Changed parent kit")
parent = json.loads(raw_receipt)


def pinned(name):
    raw = read(args.parent / name)
    if sha(raw) != parent["outputs"][name]:
        raise ValueError(f"Changed member: {name}")
    return raw


def fits_data(raw, shape):
    with fits.open(BytesIO(raw), memmap=False) as hdus:
        if len(hdus) != 1 or hdus[0].data is None or hdus[0].data.shape != shape:
            raise ValueError("Unexpected FITS shape")
        if hdus[0].data.dtype.kind != "f" or not np.isfinite(hdus[0].data).all():
            raise ValueError("Floating finite pixels required")
        for key, verify in (("CHECKSUM", hdus[0].verify_checksum), ("DATASUM", hdus[0].verify_datasum)):
            if key in hdus[0].header and verify() != 1:
                raise ValueError(f"Changed FITS {key}")
        return hdus[0].data.copy(), hdus[0].header.copy()


mosaic, header = fits_data(pinned("integer-b-cfa.fits"), (28, 32))
baseline, image_header = fits_data(pinned("unmasked-expected-rgb.fits"), (3, 28, 32))
weights, _ = fits_data(pinned("unmasked-expected-weight.fits"), (3, 28, 32))
source_levels = [[float(mosaic[sy, sx]) for sx, sy, _, _ in POINTS], [0.25, 0.30], [0.50, 0.55]]
source_levels = np.asarray(source_levels, dtype=mosaic.dtype).astype(np.float64)
if not np.all((0 < source_levels) & (source_levels < 1)):
    raise ValueError("Expected strictly positive unclipped control values")


def assess(maps):
    ordered = [maps[name] for name in CASE_ORDER]
    allowed = np.zeros(baseline.shape, dtype=bool)
    signals = []
    for sx, sy, x, y in POINTS:
        if (sx - 1, sy + 1) != (x, y) or not np.isclose(weights[1, y, x], 2, atol=1e-12, rtol=0):
            raise ValueError("Invalid probe anchor")
        allowed[1, y, x] = True
        signals.append([float(image[1, y, x]) for image in ordered])
    supported_other = (weights > 1e-8) & ~allowed
    outside = max(float(np.max(np.abs((image - ordered[0])[supported_other]))) for image in ordered[1:])
    rows = []
    for index, (_, _, x, y) in enumerate(POINTS):
        dy = np.asarray(signals[index][1:]) - signals[index][0]
        dx = source_levels[1:, index] - source_levels[0, index]
        slope = (dy / dx).tolist()
        rows.append(dict(referenceXY=[x, y], input=source_levels[:, index].tolist(),
                         output=signals[index], secantSlopesFromBaseline=slope))
    linear = all(abs(row["secantSlopesFromBaseline"][0] - row["secantSlopesFromBaseline"][1]) <= TOL
                 and all(-TOL <= k <= 1 + TOL for k in row["secantSlopesFromBaseline"])
                 for row in rows)
    return dict(status="COMPATIBLE_LOCAL_LINEAR_RESPONSE" if linear and outside <= TOL else "RESPONSE_UNRESOLVED",
                probes=rows, maxChangeOutsideProbesOnModeledSupport=outside,
                modeledHalfShareMatched=outside <= TOL and all(
                    abs(k - 0.5) <= TOL for row in rows for k in row["secantSlopesFromBaseline"]),
                absoluteWeightEstablished=False)


def save_fit(destination, data, hdr):
    hdu = fits.PrimaryHDU(data, header=hdr)
    hdu.add_checksum(when="2026-01-01T00:00:00")
    hdu.writeto(destination)
    stored, _ = fits_data(read(destination), data.shape)
    np.testing.assert_array_equal(stored, data)


def write_xdrz(source, output, cfa):
    xml = ET.fromstring(pinned(source))
    if xml.find(f"{{{NS}}}RejectionMap") is not None:
        raise ValueError("Unexpected rejection")
    for kind, filename in (("CFASourceImage", cfa), ("SourceImage", source.split(".")[0].replace("-unmasked","") + "-rgb.fits")):
        node = xml.find(f"{{{NS}}}{kind}")
        node.text = (ROOT / filename).as_posix()
    (args.output / output).write_bytes(ET.tostring(xml, encoding="utf-8", xml_declaration=True) + b"\n")


def build():
    args.output.mkdir()
    for stem in ("integer-a", "integer-b", "integer-c"):
        for kind in ("cfa", "rgb"):
            name = f"{stem}-{kind}.fits"
            (args.output / name).write_bytes(pinned(name))
    for stem in ("integer-a", "integer-c"):
        write_xdrz(f"{stem}.xdrz", f"{stem}.xdrz", f"{stem}-cfa.fits")
    write_xdrz("integer-b-unmasked.xdrz", "integer-b-baseline.xdrz", "integer-b-cfa.fits")
    maps = {"baseline": baseline}
    save_fit(args.output / "baseline-rgb.fits", baseline, image_header)
    for case, levels in zip(CASE_ORDER[1:], source_levels[1:], strict=True):
        frame = mosaic.copy()
        expected = baseline.copy()
        for (sx, sy, x, y), level in zip(POINTS, levels, strict=True):
            frame[sy, sx] = level
            expected[1, y, x] += (float(frame[sy, sx]) - float(mosaic[sy, sx])) / 2
        if np.count_nonzero(frame != mosaic) != 2:
            raise ValueError("Unexpected CFA changes")
        filename = f"integer-b-{case}-cfa.fits"
        save_fit(args.output / filename, frame, header)
        write_xdrz("integer-b-unmasked.xdrz", f"integer-b-{case}.xdrz", filename)
        save_fit(args.output / f"{case}-rgb.fits", expected, image_header)
        maps[case] = expected
    positive = assess(maps)
    if not positive["modeledHalfShareMatched"] or positive["absoluteWeightEstablished"]:
        raise ValueError("Expected half contribution not recovered")
    nonlinear = {**maps, "first": maps["first"].copy()}
    nonlinear["first"][1, 8, 13] += .04
    leaked = {**maps, "first": maps["first"].copy()}
    if weights[0, 10, 10] <= 1e-8:
        raise ValueError("Invalid leakage test anchor")
    leaked["first"][0, 10, 10] += .01
    if any(assess(bad)["status"] != "RESPONSE_UNRESOLVED" for bad in (nonlinear, leaked)):
        raise ValueError("Incorrect response accepted")
    return positive, {p.name: sha(read(p)) for p in sorted(args.output.iterdir())}


if args.exports:
    inputs = {case: read(args.exports / f"{case}-rgb.fits") for case in CASE_ORDER}
    result = assess({key: fits_data(raw, baseline.shape)[0] for key, raw in inputs.items()})
    hashes = {f"{key}-rgb.fits": sha(raw) for key, raw in inputs.items()}
    output = args.output
    mode = "FITS_COMPARISON"
else:
    result, hashes = build()
    output = args.output / "riscontro.json"
    mode = "OFFLINE_MODEL_SELF_TEST"
report = dict(schema="BKL046_CFA_POSITIVE_RESPONSE_V1", parentFixtureSha256=PIN,
              mode=mode, cases={case: ["integer-a.xdrz",f"integer-b-{case}.xdrz","integer-c.xdrz"]
                               for case in CASE_ORDER},
              result=result, sha256=hashes, nativeProvenanceVerified=False, scientificClosures=0)
with output.open("x", encoding="utf-8", newline="\n") as handle:
    json.dump(report, handle, indent=2, allow_nan=False)
    handle.write("\n")
