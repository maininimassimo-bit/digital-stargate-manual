"""Synthetic pixel rejection tests; these are not native PixInsight tests."""
import json
from pathlib import Path
import struct
import tempfile
import unittest

from tools.pixinsight.local_pilot.quality import inspect_pixels


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "synthetic.xisf"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, values=(0, 0.5, 1), extra="", location="attachment:4096:12", padding=True):
        header = f'<xisf><Image geometry="1:1:3" sampleFormat="Float32" colorSpace="RGB" location="{location}" {extra}/></xisf>'.encode()
        data = b"XISF0100" + struct.pack("<II", len(header), 0) + header
        if padding:
            data += bytes(max(0, 4096 - len(data)))
        data += struct.pack("<" + "f" * len(values), *values)
        self.path.write_bytes(data)

    def test_reports_finite_range_and_clipping_without_acceptance(self):
        self.write()
        r = inspect_pixels(self.path)
        self.assertTrue(r["allFinite"])
        self.assertEqual(r["channels"][0]["zeroSamples"], 1)
        self.assertEqual(r["channels"][2]["saturatedSamples"], 1)
        self.assertEqual(r["acceptance"], "OWNER_REVIEW_REQUIRED")
        json.dumps(r, allow_nan=False)

    def test_monochrome_preparation_requires_explicit_channel_contract(self):
        header=b'<xisf><Image geometry="2:1:1" sampleFormat="Float32" colorSpace="Gray" location="attachment:4096:8"/></xisf>'
        data=b'XISF0100'+struct.pack('<II',len(header),0)+header
        self.path.write_bytes(data+bytes(4096-len(data))+struct.pack('<ff',.1,.7))
        with self.assertRaises(ValueError):inspect_pixels(self.path)
        result=inspect_pixels(self.path,expected_channels=1)
        self.assertEqual(len(result['channels']),1)
        self.assertTrue(result['normalizedRange'])
        self.path.write_bytes(data+bytes(4096-len(data))+struct.pack('<ff',.1,float('nan')))
        with self.assertRaisesRegex(ValueError,'Nonfinite'):inspect_pixels(self.path,expected_channels=1)

    def test_rejects_nonfinite_and_out_of_range(self):
        for bad in (float("nan"), float("inf"), -0.01, 1.01):
            with self.subTest(bad=bad):
                self.write((0, bad, 1))
                with self.assertRaises(ValueError):
                    inspect_pixels(self.path)

    def test_rejects_unsupported_layouts(self):
        for extra in ('compression="zlib"', 'pixelStorage="normal"', 'byteOrder="big"'):
            with self.subTest(extra=extra):
                self.write(extra=extra)
                with self.assertRaises(ValueError):
                    inspect_pixels(self.path)

    def test_rejects_truncated_or_overlapping_attachment(self):
        for location, values in (("attachment:4096:12", (0,)), ("attachment:12:12", (0, 0.5, 1)), ("attachment:4096:16", (0, 0.5, 1))):
            with self.subTest(location=location, values=values):
                self.write(values, location=location)
                with self.assertRaises(ValueError):
                    inspect_pixels(self.path)

    def test_rejects_constant_channel_even_when_finite_and_normalized(self):
        self.write((0, 0, 0))
        data = self.path.read_bytes().replace(b'geometry="1:1:3"', b'geometry="2:1:3"').replace(b'attachment:4096:12', b'attachment:4096:24')
        self.path.write_bytes(data + bytes(12))
        with self.assertRaisesRegex(ValueError, "Constant output channel"):
            inspect_pixels(self.path)


if __name__ == "__main__":
    unittest.main()
