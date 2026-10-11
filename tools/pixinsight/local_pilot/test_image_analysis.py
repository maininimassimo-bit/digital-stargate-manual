"""Independent synthetic fixtures; no native execution or scientific acceptance."""
import hashlib
import copy
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from . import image_analysis as candidate


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'fixture.xisf'

    def write(self, values, width=None, channels=1, extra=''):
        width = width or len(values) // channels
        raw = struct.pack('<' + 'f' * len(values), *values)
        header = (f'<xisf><Image geometry="{width}:1:{channels}" sampleFormat="Float32" '
                  f'colorSpace="{"Gray" if channels == 1 else "RGB"}" '
                  f'location="attachment:4096:{len(raw)}" {extra}/></xisf>').encode()
        data = b'XISF0100' + struct.pack('<II', len(header), 0) + header
        self.path.write_bytes(data + bytes(4096 - len(data)) + raw)
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

    def test_linear_values_outside_normalized_range_are_diagnostic_not_rejected(self):
        digest = self.write([-2, -1, 0, 1, 2])
        result = candidate.analyze(self.path, expected_sha256=digest)
        row = result['channels'][0]
        self.assertEqual((row['minimum'], row['maximum'], row['mean'], row['populationVariance']), (-2, 2, 0, 2))
        self.assertEqual((row['belowZeroSamples'], row['aboveOneSamples']), (2, 1))
        self.assertEqual((row['zeroSamples'], row['oneSamples']), (1, 1))
        self.assertEqual(result['backgroundNoise']['status'], 'UNAVAILABLE')
        self.assertEqual(result['linearity'], 'NOT_ESTABLISHED')
        self.assertEqual(result['acceptance'], 'DIAGNOSTIC_ONLY')

    def test_each_rgb_channel_is_measured_separately(self):
        digest = self.write([0, 1, -1, 1, 2, 2], width=2, channels=3)
        rows = candidate.analyze(self.path, expected_sha256=digest)['channels']
        self.assertEqual([r['mean'] for r in rows], [.5, 0, 2])
        self.assertEqual([r['constant'] for r in rows], [False, False, True])

    def test_multi_image_requires_explicit_index_and_measures_selected_attachment(self):
        header = b'<xisf><Image geometry="2:1:1" sampleFormat="Float32" colorSpace="Gray" location="attachment:4096:8"/><Image geometry="2:1:1" sampleFormat="Float32" colorSpace="Gray" location="attachment:4104:8"/></xisf>'
        prefix = b'XISF0100' + struct.pack('<II', len(header), 0) + header
        self.path.write_bytes(prefix + bytes(4096 - len(prefix)) + struct.pack('<4f', -1, 1, 6, 10))
        digest = hashlib.sha256(self.path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'Single output image required'):
            candidate.analyze(self.path, expected_sha256=digest)
        result = candidate.analyze(self.path, expected_sha256=digest, image_index=1)
        self.assertEqual(result['imageIndex'], 1)
        self.assertEqual(result['channels'][0]['mean'], 8)
        for invalid in [-1, 2, True]:
            with self.assertRaisesRegex(ValueError, 'ANALYSIS_IMAGE_INDEX'):
                candidate.analyze(self.path, expected_sha256=digest, image_index=invalid)

    def test_named_auxiliary_rejection_map_is_not_a_master(self):
        digest = self.write([0, 1], extra='id="rejection_low"')
        with self.assertRaisesRegex(ValueError, 'ANALYSIS_AUXILIARY_IMAGE'):
            candidate.analyze(self.path, expected_sha256=digest, image_index=0)

    def test_stream_boundary_moments_and_sparse_sampling(self):
        # 12000x6 crosses the 65536-sample block boundary.
        values = [float(n % 2) for n in range(72000)]
        header = b'<xisf><Image geometry="12000:6:1" sampleFormat="Float32" colorSpace="Gray" location="attachment:4096:288000"/></xisf>'
        data = b'XISF0100' + struct.pack('<II', len(header), 0) + header
        self.path.write_bytes(data + bytes(4096 - len(data)) + struct.pack('<72000f', *values))
        digest = hashlib.sha256(self.path.read_bytes()).hexdigest()
        row = candidate.analyze(self.path, expected_sha256=digest)['channels'][0]
        self.assertEqual((row['sampleCount'], row['mean'], row['populationVariance']), (72000, .5, .25))
        self.assertEqual(row['sampledDistribution']['count'], 384)

    def test_nonfinite_samples_rejected_even_outside_sample_grid(self):
        for value in (float('nan'), float('inf'), -float('inf')):
            with self.subTest(value=value):
                # Index1 is outside the 64-cell-center sample of a 100px row.
                values = [0] * 100; values[1] = value
                digest = self.write(values)
                with self.assertRaisesRegex(ValueError, 'ANALYSIS_NONFINITE'):
                    candidate.analyze(self.path, expected_sha256=digest)

    def test_unsupported_compression_requires_native_export(self):
        digest = self.write([0, 1], extra='compression="zlib"')
        with self.assertRaisesRegex(ValueError, 'NATIVE_EXPORT_REQUIRED'):
            candidate.analyze(self.path, expected_sha256=digest)

    def test_truncated_attachment_rejected(self):
        self.write([0, 1]); self.path.write_bytes(self.path.read_bytes()[:-1])
        digest = hashlib.sha256(self.path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'ATTACHMENT_BOUNDS'):
            candidate.analyze(self.path, expected_sha256=digest)

    def test_expected_digest_and_changed_source_refused(self):
        digest = self.write([0, 1])
        with self.assertRaisesRegex(ValueError, 'INPUT_CHANGED'):
            candidate.analyze(self.path, expected_sha256='e' * 64)
        with patch.object(candidate, 'fingerprint', side_effect=[digest, 'e' * 64]):
            with self.assertRaisesRegex(ValueError, 'INPUT_CHANGED'):
                candidate.analyze(self.path, expected_sha256=digest)

    def test_comparison_reports_deltas_without_quality_or_domain_promotion(self):
        before = candidate.analyze(self.path, expected_sha256=self.write([0, 1]))
        after = candidate.analyze(self.path, expected_sha256=self.write([.5, .5]))
        result = candidate.compare(before, after)
        self.assertEqual(result['channels'][0]['populationVarianceDelta'], -.25)
        self.assertEqual(result['channels'][0]['zeroSamplesDelta'], -1)
        self.assertEqual(result['scientificComparison'], 'NOT_ESTABLISHED')
        self.assertNotIn('improved', result)
        changed = copy.deepcopy(after); changed['width'] += 1
        with self.assertRaisesRegex(ValueError, 'COMPARISON_GEOMETRY'):
            candidate.compare(before, changed)

    def test_cli_preserves_existing_output_and_writes_no_paths(self):
        digest = self.write([0, 1]); output = Path(self.tmp.name) / 'diagnostics.json'
        argv = ['analysis', '--input', str(self.path), '--sha256', digest, '--output', str(output)]
        with patch('sys.argv', argv), patch('builtins.print'):
            candidate.main()
        raw = output.read_bytes()
        self.assertNotIn(str(self.path).encode(), raw)
        with patch('sys.argv', argv), self.assertRaises(SystemExit):
            candidate.main()
        self.assertEqual(output.read_bytes(), raw)


if __name__ == '__main__': unittest.main()
