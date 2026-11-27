from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

p = ArgumentParser()
for argument in ("parent_fixture", "parent_plan", "packages", "output"):
    p.add_argument(argument, type=Path)
args = p.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np
import astropy
from astropy.io import fits

if (np.__version__, astropy.__version__) != ("2.3.5", "7.2.0"):
    raise ValueError("Changed numerical environment")

BASE = args.parent_fixture
RUN = Path("O:/BKL046-CFA-XDRZ-valor-zero-tre-ingressi-v1/fixture")
MANIFEST_PIN = "6fd2da645650a19f4654276607612c0af5ba193734a0087fc221058aab4fe16b"
raw = (BASE / "manifest.json").read_bytes()
if sha256(raw).hexdigest() != MANIFEST_PIN:
    raise ValueError("Changed original manifest")
manifest = json.loads(raw)
if manifest["scale"] != 1 or manifest["dropShrink"] != 0.70 or manifest["pattern"] != "RGGB":
    raise ValueError("Changed acquisition geometry")
NS = "http://www.pixinsight.com/xdrz"
ET.register_namespace("", NS)
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")


def pinned(name):
    raw = (BASE / name).read_bytes()
    if sha256(raw).hexdigest() != manifest["files"][name]:
        raise ValueError(f"Changed source {name}")
    return raw


def image(name):
    pinned(name)
    with fits.open(BASE / name, memmap=False) as hdus:
        if hdus[0].verify_checksum() != 1 or hdus[0].verify_datasum() != 1:
            raise ValueError(f"Bad FITS checksum {name}")
        return hdus[0].data.copy(), hdus[0].header.copy()


def write_fits(name, values, header):
    target = out / name
    hdu = fits.PrimaryHDU(values, header=header)
    hdu.add_checksum(when="2026-01-01T00:00:00", override_datasum=False)
    hdu.writeto(target)
    with fits.open(target, memmap=False) as hdus:
        if hdus[0].verify_checksum() != 1 or hdus[0].verify_datasum() != 1:
            raise ValueError(f"Bad output FITS checksum {name}")
        np.testing.assert_array_equal(hdus[0].data, values)


def xdrz(source, output, stem, native_cfa):
    xml = ET.fromstring(pinned(source))
    cfa = xml.find(f"{{{NS}}}CFASourceImage")
    if cfa.get("pattern") != "RGGB":
        raise ValueError("Changed Bayer phase")
    xml.find(f"{{{NS}}}SourceImage").text = (RUN / f"{stem}-rgb.fits").as_posix()
    cfa.text = (RUN / native_cfa).as_posix()
    (out / output).write_bytes(ET.tostring(xml, encoding="utf-8", xml_declaration=True) + b"\n")


out = args.output
out.mkdir()
for stem in ("integer-a", "integer-b", "integer-c"):
    for kind in ("cfa", "rgb"):
        name = f"{stem}-{kind}.fits"
        (out / name).write_bytes(pinned(name))
xdrz("integer-a-center0.xdrz", "integer-a.xdrz", "integer-a", "integer-a-cfa.fits")
xdrz("integer-c-center0.xdrz", "integer-c.xdrz", "integer-c", "integer-c-cfa.fits")
xdrz("integer-b-center0.xdrz", "integer-b-unmasked.xdrz", "integer-b", "integer-b-cfa.fits")
for suffix in ("mask-green", "mask-wrong-channel"):
    name = f"integer-b-{suffix}.xdrz"
    xdrz(name, name, "integer-b", "integer-b-cfa.fits")
xml = ET.parse(out / "integer-b-unmasked.xdrz").getroot()
if xml.find(f"{{{NS}}}AlignmentMatrix").text != "1,0,1,0,1,-1,0,0,1":
    raise ValueError("Changed native alignment")

mosaic, header = image("integer-b-cfa.fits")
baseline, image_header = image("unmasked-expected-rgb.fits")
weights, _ = image("unmasked-expected-weight.fits")
records = []
for label, (sx, sy), (x, y) in (
    ("detector", (14, 7), (13, 8)),
    ("reference", (15, 6), (14, 7)),
):
    if (sx - 1, sy + 1) != (x, y) or (sx + sy) % 2 != 1 or not np.isclose(weights[1, y, x], 2, atol=1e-12, rtol=0):
        raise ValueError("Invalid green control anchor")
    value = float(mosaic[sy, sx])
    if not 0 < value < 1:
        raise ValueError("Degenerate control value")
    variant = mosaic.copy()
    variant[sy, sx] = 0
    if np.count_nonzero(variant != mosaic) != 1:
        raise ValueError("More than one pixel changed")
    fname = f"integer-b-zero-{label}-cfa.fits"
    write_fits(fname, variant, header)
    xdrz("integer-b-center0.xdrz", f"integer-b-zero-{label}.xdrz", "integer-b", fname)

    predicted = baseline.copy()
    predicted[1, y, x] -= value / 2
    excluded, _ = image(f"{label}-expected-rgb.fits")
    excluded_weight, _ = image(f"{label}-expected-weight.fits")
    if not np.isclose(excluded_weight[1, y, x], 1, atol=1e-12, rtol=0) or not np.isclose(
        excluded[1, y, x], 2 * predicted[1, y, x], atol=2e-8, rtol=0
    ):
        raise ValueError("Reference exclusion model does not match zeroed input")
    if abs(excluded[1, y, x] - predicted[1, y, x]) < 1e-3:
        raise ValueError("Zero and rejection predictions are not separated")
    write_fits(f"zero-{label}-retained-expected-rgb.fits", predicted, image_header)
    records.append(dict(model=label, detectorXY=[sx, sy], referenceXY=[x, y],
                        originalSample=value, included=[float(baseline[1, y, x]), 2],
                        zeroWeightRetained=[float(predicted[1, y, x]), 2],
                        sampleExcluded=[float(excluded[1, y, x]), 1]))

for name in ("unmasked-expected-rgb.fits", "unmasked-expected-weight.fits",
             "detector-expected-rgb.fits", "detector-expected-weight.fits",
             "reference-expected-rgb.fits", "reference-expected-weight.fits"):
    (out / name).write_bytes(pinned(name))
plan_raw = args.parent_plan.read_bytes()
plan_pin = "377aea9a4decbf470a95c92f7f85852bc59f5e056b76a8c7ae110e842fcfd6e7"
if sha256(plan_raw).hexdigest() != plan_pin:
    raise ValueError("Changed parent plan")
parent_plan = json.loads(plan_raw)
if parent_plan["fixtureManifestSha256"] != MANIFEST_PIN:
    raise ValueError("Changed plan-fixture relation")

records_for_plan = []
third, _ = image("integer-c-cfa.fits")
c_xml = ET.parse(out / "integer-c.xdrz").getroot()
if c_xml.find(f"{{{NS}}}AlignmentMatrix").text != "1,0,1,0,1,0,0,0,1":
    raise ValueError("Changed third exposure alignment")
for item in records:
    x, y = item["referenceXY"]
    if (x + 1 + y) % 2 != 0 or not np.isfinite(third[y, x + 1]):
        raise ValueError("Third exposure intrudes on discriminating green probes")
for arm in ("unmasked", "mask-green", "mask-wrong-channel", "zero-detector", "zero-reference"):
    filenames = ("integer-a.xdrz", f"integer-b-{arm}.xdrz", "integer-c.xdrz")
    paths = []
    for name in filenames:
        tree = ET.parse(out / name).getroot()
        if (tree.find(f"{{{NS}}}RejectionMap") is not None) != (
            name == filenames[1] and arm.startswith("mask-")
        ):
            raise ValueError("Unexpected rejection map")
        for tag in ("SourceImage", "CFASourceImage"):
            source = Path(tree.find(f"{{{NS}}}{tag}").text)
            if source.parent != RUN or not (out / source.name).is_file():
                raise ValueError("Unbound source")
            if tag == "CFASourceImage":
                paths.append(source.name)
    if len(set(paths)) != 3 or len({sha256((out / name).read_bytes()).hexdigest() for name in paths}) != 3:
        raise ValueError("Non-unique exposures")
    records_for_plan.append(dict(id=arm, xdrz=filenames, cfa=paths, rejection=arm.startswith("mask-")))

record = dict(schema="BKL046_CFA_XDRZ_ZERO_THREE_INPUT_V1", fixtureManifestSha256=MANIFEST_PIN,
              parentPlanSha256=plan_pin, runtimeFiles=parent_plan["runtimeFiles"],
              settings=parent_plan["settings"], arms=records_for_plan,
              requiredExports=["effective parameters", "console and exit", "linear RGB", "raw RGB weights"],
              nativeExecutions=0, scientificClosures=0, predictions=records,
              outputs={f.name: sha256(f.read_bytes()).hexdigest() for f in sorted(out.iterdir())})
(out / "riscontro.json").write_text(json.dumps(record, indent=2, allow_nan=False) + "\n",
                                   encoding="utf-8", newline="\n")
