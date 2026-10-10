"""Synthetic retained declarations; no native launch, cloud or science acceptance."""
import hashlib
import json
import unittest
import zipfile
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_local_report as fixtures
from tools.scientific_transients.report_bundle import export_bundle


class ReportBundleTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.LocalReportTests(); self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.journal, self.sha, self.output = self.fixture.journal, self.fixture.sha, self.fixture.output

    def test_archive_reopens_independently_with_exact_bytes_and_no_extra_files(self):
        f = self.fixture.fixture
        before = (f.starts, len(f.transport.posts))
        (self.journal.directory / 'UNREFERENCED-secret.txt').write_text('must not be copied')
        directory = export_bundle(self.journal, self.sha, self.output)
        raw = (directory / 'retained-report.zip').read_bytes()
        receipt = json.loads((directory / 'bundle-receipt.json').read_text())
        self.assertEqual(receipt['archive'], {'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()})
        with zipfile.ZipFile(directory / 'retained-report.zip') as bundle:
            self.assertIsNone(bundle.testzip())
            manifest = json.loads(bundle.read('manifest.json'))
            self.assertEqual(set(bundle.namelist()), {e['path'] for e in manifest['entries']} | {'manifest.json'})
            for entry in manifest['entries']:
                data = bundle.read(entry['path'])
                self.assertEqual(len(data), entry['bytes'])
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'])
                self.assertNotIn(f.claim['leaseToken'].encode(), data)
            self.assertIn('attempt/attempt.json', bundle.namelist())
            self.assertIn('attempt/events/005.json', bundle.namelist())
            self.assertNotIn('attempt/UNREFERENCED-secret.txt', bundle.namelist())
            report = json.loads(bundle.read('report.json'))
            self.assertFalse(manifest['completeDependencyArchive'])
            self.assertEqual(report['scienceValidation'], 'NOT_VALIDATED')
            self.assertIsNone(report['measurements'][0]['rows'][0]['fullVariance'])
        self.assertEqual((f.starts, len(f.transport.posts)), before)

    def test_wrong_seal_changed_evidence_and_output_overlap_refuse(self):
        with self.assertRaises(ProtocolError): export_bundle(self.journal, 'f'*64, self.output)
        with self.assertRaises(ProtocolError): export_bundle(self.journal, self.sha, self.journal.directory)
        self.assertEqual(list(self.output.iterdir()), [])
        path = self.journal.directory / self.journal.anchor['snapshot'][0]['path']
        path.write_bytes(b'changed')
        with self.assertRaises(ProtocolError): export_bundle(self.journal, self.sha, self.output)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_archive_and_receipt_are_never_overwritten(self):
        directory = export_bundle(self.journal, self.sha, self.output)
        before = {p.name:p.read_bytes() for p in directory.iterdir()}
        with self.assertRaises(FileExistsError): export_bundle(self.journal, self.sha, self.output)
        self.assertEqual({p.name:p.read_bytes() for p in directory.iterdir()}, before)

    def test_size_bound_refuses_before_creating_output(self):
        with patch('tools.scientific_transients.report_bundle.MAX_BYTES', 1):
            with self.assertRaisesRegex(ProtocolError, 'SIZE_LIMIT'):
                export_bundle(self.journal, self.sha, self.output)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_changed_source_after_archive_preserves_failure_without_success_receipt(self):
        from tools.scientific_transients.local_report import inspect
        calls = 0
        def unstable(journal, sha):
            nonlocal calls
            calls += 1
            if calls == 2: raise ProtocolError('BUNDLE_SOURCE_CHANGED')
            return inspect(journal, sha)
        with patch('tools.scientific_transients.report_bundle.inspect', side_effect=unstable):
            with self.assertRaises(ProtocolError): export_bundle(self.journal, self.sha, self.output)
        directory = self.output / self.journal.anchor['identity']['attemptId']
        self.assertTrue((directory / 'failed.json').exists())
        self.assertTrue((directory / 'retained-report.zip').exists())
        self.assertFalse((directory / 'bundle-receipt.json').exists())
        with self.assertRaises(FileExistsError): export_bundle(self.journal, self.sha, self.output)


if __name__ == '__main__': unittest.main()
