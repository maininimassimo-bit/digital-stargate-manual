"""Explicit trusted-local TPV coordinate diagnostic. No network, native launch or acceptance."""
import hashlib
import io
import math
import re

from tools.pixinsight.local_pilot.broker import require, opaque
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.queue import fields

PROTOCOL = "DSG_LOCAL_TPV_COORDINATES_V1"
MAX_BYTES = 128 * 1024 * 1024  # Resource bound, not a scientific quality threshold.
MAX_POINTS = 1024
VERSIONS = {"astropy": "8.0.1", "numpy": "2.5.3"}
WCS_KEY = re.compile(r"^(CTYPE[12]|CRPIX[12]|CRVAL[12]|CUNIT[12]|CD[12]_[12]|"
                     r"PC[12]_[12]|CDELT[12]|PV[12]_\d+|RADESYS|RADECSYS|EQUINOX|"
                     r"LONPOLE|LATPOLE|NAXIS[12]?|BITPIX|SIMPLE|WCSAXES)$")


def finite(value):
    return type(value) in {int, float} and math.isfinite(value)


def transform_local_tpv(path, expected_sha256, geometry, convention, targets):
    """Read one bounded private snapshot; caller supplies a trusted local path, never a portal URL.

    The projection is computed in the header's declared frame. No frame/epoch conversion,
    proper motion, centroid covariance or catalog association is inferred.
    """
    require(type(expected_sha256) is str and re.fullmatch(r"[0-9a-f]{64}", expected_sha256),
            "TPV_DIGEST")
    fields(geometry, {"width", "height"})
    require(all(type(geometry[k]) is int and 0 < geometry[k] <= 100000 for k in geometry)
            and geometry["width"] * geometry["height"] <= 100000000, "TPV_GEOMETRY")
    require(type(convention) is str and convention in {"FITS_SAMPLE_INDEX_ZERO", "PI_NATIVE_GEOMETRIC"},
            "TPV_CONVENTION")
    require(type(targets) is list and 0 < len(targets) <= MAX_POINTS, "TPV_TARGET_COUNT")
    ids, points = set(), []
    for target in targets:
        fields(target, {"sourceRef", "x", "y"})
        require(opaque(target["sourceRef"]) and target["sourceRef"] not in ids
                and finite(target["x"]) and finite(target["y"]), "TPV_TARGET")
        ids.add(target["sourceRef"])
        shift = 0.5 if convention == "PI_NATIVE_GEOMETRIC" else 0
        x, y = target["x"] - shift, target["y"] - shift
        require(0 <= x <= geometry["width"] - 1 and 0 <= y <= geometry["height"] - 1,
                "TPV_TARGET_BOUNDS")
        points.append([x, y])

    source = safe_path(path)
    require(source.is_file() and 0 < source.stat().st_size <= MAX_BYTES, "TPV_LOCAL_FILE")
    with source.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(0 < len(raw) <= MAX_BYTES, "TPV_BYTE_LIMIT")
    require(hashlib.sha256(raw).hexdigest() == expected_sha256, "TPV_BYTES_MISMATCH")
    require(raw.startswith(b"SIMPLE  =") and len(raw) % 2880 == 0, "TPV_UNCOMPRESSED_FITS")
    require(any(raw[k:k+80] == b"END" + b" " * 77
                for k in range(0, min(len(raw), 64 * 2880), 80)), "TPV_HEADER_LIMIT")
    # All parsing/transformation uses these verified bytes, not a second path read.
    import astropy
    import numpy as np
    from astropy.io import fits
    from astropy.wcs import WCS
    require(astropy.__version__ == VERSIONS["astropy"] and np.__version__ == VERSIONS["numpy"],
            "TPV_RUNTIME_VERSION")
    with fits.open(io.BytesIO(raw), mode="readonly", memmap=False,
                   lazy_load_hdus=False, do_not_scale_image_data=True) as hdus:
        require(len(hdus) == 1 and type(hdus[0]) is fits.PrimaryHDU, "TPV_PRIMARY_ONLY")
        hdus.verify("exception")
        header = hdus[0].header
        require(header.get("NAXIS") == 2 and header.get("NAXIS1") == geometry["width"]
                and header.get("NAXIS2") == geometry["height"], "TPV_HEADER_GEOMETRY")
        require(header.get("BITPIX") in {8, 16, 32, 64, -32, -64}
                and header.get("WCSAXES", 2) == 2, "TPV_IMAGE_AXES")
        info = hdus[0].fileinfo()
        require(info is not None and info["datLoc"] + info["datSpan"] <= len(raw),
                "TPV_TRUNCATED_IMAGE")
        seen = set()
        for card in header.cards:
            if WCS_KEY.fullmatch(card.keyword):
                require(card.keyword not in seen, "TPV_DUPLICATE_WCS_CARD")
                seen.add(card.keyword)
                if card.keyword.startswith("PV"):
                    require(0 <= int(card.keyword.split("_")[1]) <= 39, "TPV_POLYNOMIAL_ORDER")
                if card.keyword.startswith(("CRPIX", "CRVAL", "CD", "PC", "PV")) \
                        or card.keyword in {"EQUINOX", "LONPOLE", "LATPOLE"}:
                    require(finite(card.value), "TPV_NONFINITE_WCS")
        require(header.get("CTYPE1") == "RA---TPV" and header.get("CTYPE2") == "DEC--TPV",
                "TPV_PROJECTION")
        require(all(header.get(k) == "deg" for k in ["CUNIT1", "CUNIT2"]), "TPV_UNITS")
        require(all(k in header for k in ["CRPIX1", "CRPIX2", "CRVAL1", "CRVAL2",
                                          "CD1_1", "CD1_2", "CD2_1", "CD2_2"]), "TPV_WCS_FIELDS")
        require(abs(header["CRVAL2"]) <= 90, "TPV_REFERENCE_DECLINATION")
        determinant = header["CD1_1"] * header["CD2_2"] - header["CD1_2"] * header["CD2_1"]
        require(finite(determinant) and determinant != 0, "TPV_SINGULAR_MATRIX")
        require(any(k.startswith("PV1_") for k in seen)
                and any(k.startswith("PV2_") for k in seen), "TPV_DISTORTION_FIELDS")
        # SIP/table/alternate WCS and mixed matrix representations are outside this adapter.
        require(not any(k.startswith(("A_", "B_", "AP_", "BP_", "CPDIS", "DP", "D2IM", "CROTA"))
                        or (re.fullmatch(r"(CD\d+_\d+|PV\d+_\d+)", k) and not WCS_KEY.fullmatch(k))
                        or re.fullmatch(r"(CTYPE[12]|CRPIX[12]|CRVAL[12]|CUNIT[12]|CD[12]_[12]|"
                                        r"PC[12]_[12]|CDELT[12]|PV[12]_\d+|RADESYS|EQUINOX)[A-Z]", k)
                        or re.fullmatch(r"PC[12]_[12]|CDELT[12]", k) for k in header),
                "TPV_UNSUPPORTED_WCS_FIELDS")
        require(not ("RADESYS" in header and "RADECSYS" in header), "TPV_AMBIGUOUS_FRAME")
        frame = header.get("RADESYS", header.get("RADECSYS"))
        require(frame is None or frame in {"ICRS", "FK5", "FK4", "FK4-NO-E", "GAPPT"},
                "TPV_FRAME_DECLARATION")
        wcs = WCS(header, naxis=2, relax=False)
        require(wcs.pixel_n_dim == 2 and wcs.world_n_dim == 2 and wcs.has_celestial,
                "TPV_DIMENSIONS")
        values = wcs.all_pix2world(np.asarray(points, dtype=np.float64), 0)
        require(values.shape == (len(points), 2) and np.isfinite(values).all()
                and np.all((values[:, 0] >= 0) & (values[:, 0] < 360))
                and np.all(np.abs(values[:, 1]) <= 90), "TPV_COORDINATES")
        equinox = header.get("EQUINOX")
    return {"protocol": PROTOCOL, "classification": "PRIVATE", "imageSha256": expected_sha256,
            "imageBytes": len(raw), "versions": dict(VERSIONS), "geometry": dict(geometry),
            "coordinateConvention": convention, "projection": "TPV_FROM_ORIGINAL_HEADER",
            "frameDeclared": frame, "equinoxDeclared": equinox,
            "frameAttested": False, "observationEpoch": None, "properMotionApplied": False,
            "positionalCovariance": None, "associationAccepted": False,
            "scientificValidation": "NOT_VALIDATED", "candidateClassification": "NOT_EVALUATED",
            "rows": [{"sourceRef": target["sourceRef"], "raDegreesInHeaderFrame": float(v[0]),
                      "decDegreesInHeaderFrame": float(v[1])}
                     for target, v in zip(targets, values, strict=True)]}
