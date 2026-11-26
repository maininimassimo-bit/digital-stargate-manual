"""Classify a complete five-arm CFA FITS set against the frozen geometric controls."""
from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys

parser = ArgumentParser()
parser.add_argument("packages", type=Path)
parser.add_argument("fixture", type=Path)
parser.add_argument("output", type=Path)
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument("--exports", type=Path)
mode.add_argument("--self-test", action="store_true")
args = parser.parse_args()
sys.path.insert(0, str(args.packages))
import numpy as np
from astropy.io import fits

PIN = "a64038a4901d93bf6973e55f1fc888afbb5cd221ec9c8c5a0a94a2359eaaaf8d"
ARMS = ("unmasked", "mask-green", "mask-wrong-channel", "zero-detector", "zero-reference")
SHAPE = (3, 28, 32)
TOLERANCE = 1e-6
SUPPORT = 1e-8


def raw_file(path, limit=262144):
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if not 0 < len(raw) <= limit:
        raise ValueError(f"Unexpected file size: {path.name}")
    return raw


def sha(raw):
    return sha256(raw).hexdigest()


def fits_map(raw):
    with fits.open(BytesIO(raw), memmap=False) as hdus:
        if len(hdus) != 1 or hdus[0].data is None or hdus[0].data.shape != SHAPE:
            raise ValueError("Expected one RGB FITS plane stack")
        data = hdus[0].data
        if data.dtype.kind != "f":
            raise ValueError("Expected linear floating-point export")
        for key, verify in (("CHECKSUM", hdus[0].verify_checksum), ("DATASUM", hdus[0].verify_datasum)):
            if key in hdus[0].header and verify() != 1:
                raise ValueError(f"Invalid FITS {key}")
        return np.asarray(data, dtype=np.float64)


def load_models():
    raw = raw_file(args.fixture / "riscontro.json")
    if sha(raw) != PIN:
        raise ValueError("Frozen fixture receipt mismatch")
    receipt = json.loads(raw)

    def oracle(filename):
        data = raw_file(args.fixture / filename)
        if receipt["outputs"][filename] != sha(data):
            raise ValueError(f"Frozen oracle mismatch: {filename}")
        return fits_map(data)

    models = {
        model: tuple(oracle(f"{model}-expected-{kind}.fits") for kind in ("rgb", "weight"))
        for model in ("unmasked", "detector", "reference")
    }
    for label in ("detector", "reference"):
        models[f"zero-{label}-retained"] = (
            oracle(f"zero-{label}-retained-expected-rgb.fits"), models["unmasked"][1]
        )
    return models


def classify_map(value, weight, choices, models):
    if value.shape != SHAPE or weight.shape != SHAPE:
        raise ValueError("Unexpected RGB map shape")
    if not np.isfinite(weight).all() or (weight < 0).any():
        return dict(status="INVALID_RAW_WEIGHT", matches=[])
    measured = weight > SUPPORT
    if not np.isfinite(value[measured]).all():
        return dict(status="INVALID_SUPPORTED_INTENSITY", matches=[])
    hits = []
    for name in choices:
        prediction, predicted_weight = models[name]
        support = predicted_weight > SUPPORT
        if (np.array_equal(measured, support)
                and np.allclose(weight, predicted_weight, atol=TOLERANCE, rtol=0)
                and np.allclose(value[support], prediction[support], atol=TOLERANCE, rtol=0)):
            hits.append(name)
    status = {0: "OUTSIDE_FROZEN_MODELS", 1: "UNIQUE_MODEL"}.get(len(hits), "AMBIGUOUS_MODEL")
    return dict(status=status, matches=hits)


def classify_set(pairs, models):
    choices = {
        "unmasked": ("unmasked",),
        "mask-green": ("unmasked", "detector", "reference"),
        "mask-wrong-channel": ("unmasked",),
        "zero-detector": ("zero-detector-retained", "detector", "unmasked"),
        "zero-reference": ("zero-reference-retained", "reference", "unmasked"),
    }
    arms = {key: classify_map(*pairs[key], choices[key], models) for key in ARMS}
    if any(row["status"] != "UNIQUE_MODEL" for row in arms.values()):
        return dict(status="INCOMPLETE_OR_UNMATCHED", arms=arms)
    selected = {key: row["matches"][0] for key, row in arms.items()}
    landed = selected["mask-green"]
    if landed == "unmasked":
        return dict(status="GREEN_MASK_NO_EFFECT", arms=arms)
    zeros = (selected["zero-detector"], selected["zero-reference"])
    if zeros == ("zero-detector-retained", "zero-reference-retained"):
        mode = "ZERO_WEIGHT_RETAINED"
    elif zeros == ("detector", "reference"):
        mode = "ZERO_SAMPLE_EXCLUDED"
    else:
        mode = "ZERO_BEHAVIOR_UNRESOLVED"
    return dict(status=mode, greenMaskCoordinateModel=landed, arms=arms)


models = load_models()
report = dict(schema="BKL046_CFA_XDRZ_ZERO_COMPARISON_V1", fixtureSha256=PIN,
              absoluteTolerance=TOLERANCE, supportThreshold=SUPPORT,
              nativeProvenanceVerified=False, scientificClosures=0)
if args.self_test:
    expected = {
        "unmasked": "unmasked", "mask-green": "detector", "mask-wrong-channel": "unmasked",
        "zero-detector": "zero-detector-retained", "zero-reference": "zero-reference-retained",
    }

    def derive(overrides):
        return {key: models[name] for key, name in (expected | overrides).items()}

    cases = {}
    for name, changes, status in (
        ("detector_retained", {}, "ZERO_WEIGHT_RETAINED"),
        ("reference_retained", {"mask-green": "reference"}, "ZERO_WEIGHT_RETAINED"),
        ("detector_excluded", {"zero-detector": "detector", "zero-reference": "reference"}, "ZERO_SAMPLE_EXCLUDED"),
        ("reference_excluded", {"mask-green": "reference", "zero-detector": "detector",
                                "zero-reference": "reference"}, "ZERO_SAMPLE_EXCLUDED"),
        ("mixed_zero", {"zero-detector": "detector"}, "ZERO_BEHAVIOR_UNRESOLVED"),
        ("unapplied_mask", {"mask-green": "unmasked"}, "GREEN_MASK_NO_EFFECT"),
        ("wrong_channel_changed", {"mask-wrong-channel": "detector"}, "INCOMPLETE_OR_UNMATCHED"),
        ("swapped_zero", {"zero-detector": "zero-reference-retained"}, "INCOMPLETE_OR_UNMATCHED"),
    ):
        checked = classify_set(derive(changes), models)
        if checked["status"] != status:
            raise ValueError(f"Self-test failed: {name}")
        cases[name] = status
    value, weight = models["unmasked"]
    scaled = classify_map(value, weight * 0.5, ("unmasked",), models)
    if scaled["status"] != "OUTSIDE_FROZEN_MODELS":
        raise ValueError("Renormalized weights accepted")
    altered = value.copy()
    altered[0, 10, 10] = np.nan
    if weight[0, 10, 10] <= SUPPORT:
        raise ValueError("Invalid test anchor")
    if classify_map(altered, weight, ("unmasked",), models)["status"] != "INVALID_SUPPORTED_INTENSITY":
        raise ValueError("Nonfinite supported pixel accepted")
    changed = weight.copy()
    changed[0, 10, 10] = 0
    if classify_map(value, changed, ("unmasked",), models)["status"] != "OUTSIDE_FROZEN_MODELS":
        raise ValueError("Changed support outside probes accepted")
    report.update(mode="OFFLINE_SELF_TEST", cases=cases, auxiliaryChecks=[
        "renormalized_weight_rejected", "nonfinite_supported_intensity_rejected", "remote_pixel_support_change_rejected"
    ])
else:
    exports, pins = {}, {}
    for arm in ARMS:
        hashes, arrays = {}, []
        for kind in ("rgb", "weight"):
            filename = f"{arm}-{kind}.fits"
            raw = raw_file(args.exports / filename)
            arrays.append(fits_map(raw))
            hashes[filename] = sha(raw)
        exports[arm], pins[arm] = tuple(arrays), hashes
    report.update(mode="FITS_COMPARISON", inputHashes=pins, comparison=classify_set(exports, models))

with args.output.open("x", encoding="utf-8", newline="\n") as target:
    json.dump(report, target, indent=2, allow_nan=False)
    target.write("\n")
