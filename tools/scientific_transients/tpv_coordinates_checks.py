"""Synthetic known-answer TPV geometry and rejection tests, no network/native processing."""
import hashlib
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from astropy.io import fits
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.tpv_coordinates import transform_local_tpv


class TpvTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "synthetic.fits"
        self.header = fits.Header({"CTYPE1": "RA---TPV", "CTYPE2": "DEC--TPV",
            "CUNIT1": "deg", "CUNIT2": "deg", "CRPIX1": 32.5, "CRPIX2": 32.5,
            "CRVAL1": 120., "CRVAL2": 30., "CD1_1": -.001, "CD1_2": 0.,
            "CD2_1": 0., "CD2_2": .001, "PV1_1": 1., "PV2_1": 1., "RADESYS": "ICRS"})
        self.geometry = {"width": 64, "height": 64}
        self.targets = [{"sourceRef": "a" * 32, "x": 31.5, "y": 31.5}]
        self.write()

    def write(self, extension=False):
        hdu = fits.PrimaryHDU(np.zeros((64, 64), dtype=np.float32), header=self.header)
        fits.HDUList([hdu] + ([fits.ImageHDU()] if extension else [])).writeto(self.path, overwrite=True)
        self.sha = hashlib.sha256(self.path.read_bytes()).hexdigest()

    def run_transform(self, convention="FITS_SAMPLE_INDEX_ZERO", targets=None):
        return transform_local_tpv(self.path, self.sha, self.geometry, convention,
                                   self.targets if targets is None else targets)

    def test_center_and_unknown_scientific_state(self):
        result = self.run_transform()
        self.assertAlmostEqual(result["rows"][0]["raDegreesInHeaderFrame"], 120., places=11)
        self.assertAlmostEqual(result["rows"][0]["decDegreesInHeaderFrame"], 30., places=11)
        self.assertEqual(result["scientificValidation"], "NOT_VALIDATED")
        self.assertIsNone(result["positionalCovariance"])
        self.assertIsNone(result["observationEpoch"])
        self.assertFalse(result["associationAccepted"])
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(), self.sha)

    def test_half_pixel_conversion_same_world_position(self):
        geometric = [{"sourceRef": "a" * 32, "x": 32., "y": 32.}]
        self.assertEqual(self.run_transform()["rows"], self.run_transform("PI_NATIVE_GEOMETRIC", geometric)["rows"])

    def test_polynomial_against_independent_tangent_plane_formula(self):
        self.header["PV1_4"], self.header["PV2_4"] = .1, -.2
        self.write()
        target = [{"sourceRef": "a" * 32, "x": 40., "y": 20.}]
        row = self.run_transform(targets=target)["rows"][0]
        xi, eta = -.001 * (41 - 32.5), .001 * (21 - 32.5)
        xi, eta = math.radians(xi + .1 * xi**2), math.radians(eta - .2 * eta**2)
        d0, a0 = math.radians(30), math.radians(120)
        denominator = math.cos(d0) - eta * math.sin(d0)
        ra = a0 + math.atan2(xi, denominator)
        dec = math.atan2(math.sin(d0) + eta * math.cos(d0), math.hypot(denominator, xi))
        self.assertAlmostEqual(row["raDegreesInHeaderFrame"], math.degrees(ra), places=10)
        self.assertAlmostEqual(row["decDegreesInHeaderFrame"], math.degrees(dec), places=10)

    def test_unknown_frame_not_invented(self):
        del self.header["RADESYS"]
        self.write()
        result = self.run_transform()
        self.assertIsNone(result["frameDeclared"])
        self.assertFalse(result["frameAttested"])

    def test_digest_and_geometry_mismatch(self):
        with self.assertRaises(ProtocolError):
            transform_local_tpv(self.path, "0" * 64, self.geometry, "FITS_SAMPLE_INDEX_ZERO", self.targets)
        self.geometry["width"] = 63
        with self.assertRaises(ProtocolError): self.run_transform()

    def test_unsafe_targets(self):
        for values in [[True, 1], [float("nan"), 1], [-1, 1], [64, 1], [1, float("inf")]]:
            with self.subTest(values=values), self.assertRaises(ProtocolError):
                self.run_transform(targets=[{"sourceRef": "a" * 32, "x": values[0], "y": values[1]}])
        with self.assertRaises(ProtocolError): self.run_transform(targets=self.targets * 2)
        with self.assertRaises(ProtocolError): self.run_transform("PI_NATIVE_GEOMETRIC", [{"sourceRef": "a" * 32, "x": 0., "y": .5}])

    def test_duplicate_and_unsupported_wcs(self):
        for field, value in [("PC1_1", 1.), ("A_ORDER", 2), ("PV1_40", 1.),
                             ("CTYPE1A", "RA---TAN"), ("RADECSYS", "ICRS"),
                             ("CROTA1", 1.), ("CD1_3", 0.), ("CD1_1", 0.), ("CRVAL2", 91.)]:
            original = self.header.copy()
            self.header[field] = value
            self.write()
            with self.subTest(field=field), self.assertRaises(ProtocolError): self.run_transform()
            self.header = original
        self.header.append(("CRVAL1", 120.))
        self.write()
        with self.assertRaises(ProtocolError): self.run_transform()

    def test_projection_units_missing_distortion(self):
        for key, value in [("CTYPE1", "RA---TAN"), ("CUNIT1", "rad")]:
            original = self.header.copy()
            self.header[key] = value
            self.write()
            with self.subTest(key=key), self.assertRaises(ProtocolError): self.run_transform()
            self.header = original
        del self.header["PV2_1"]
        self.write()
        with self.assertRaises(ProtocolError): self.run_transform()

    def test_extension_and_truncated_image(self):
        self.write(extension=True)
        with self.assertRaises(ProtocolError): self.run_transform()
        self.write()
        raw = self.path.read_bytes()[:-2880]
        self.path.write_bytes(raw)
        self.sha = hashlib.sha256(raw).hexdigest()
        with self.assertRaises(ProtocolError): self.run_transform()

    def test_version_and_size_fail_closed(self):
        with patch("numpy.__version__", "unapproved"), self.assertRaises(ProtocolError): self.run_transform()
        with patch("tools.scientific_transients.tpv_coordinates.MAX_BYTES", 10), self.assertRaises(ProtocolError): self.run_transform()


if __name__ == "__main__":
    unittest.main()
