"""Synthetic private CBAT preview controls. No provider call or real report."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, decode
from tools.scientific_transients.local_registry import LocalRegistry, ROLES, fingerprint
from tools.scientific_transients import cbat_preview as cbat


class CBATPreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.artifacts, self.registry, self.output = [self.root / n for n in ('artifacts', 'registry', 'output')]
        for p in (self.artifacts, self.registry, self.output): p.mkdir()
        self.local = LocalRegistry(self.artifacts, self.registry)
        binding = {k: str(i) * 32 for i, k in enumerate(
            ('bindingRef', 'inputRef', 'referenceRef', 'algorithmRef', 'contractRef'), 1)}
        manifest = {'protocol': 'DSG_TRANSIENT_LOCAL_BINDING_V1', 'binding': binding, 'files': []}
        for role in sorted(ROLES):
            p = self.artifacts / (role + '.dat'); p.write_bytes(b'synthetic-not-astronomical-data')
            manifest['files'].append({'role': role, 'path': p.name, **fingerprint(p)})
        receipt = self.local.register(encode(manifest))
        self.request = {'protocol': cbat.PROTOCOL, 'exportRef': 'a' * 32, 'candidateRef': 'b' * 32,
            'bindingRef': binding['bindingRef'], 'manifestSha256': receipt['manifestSha256'],
            'categoryDeclared': 'GALACTIC_NOVA_CANDIDATE', 'sourceOriginDeclared': 'SYNTHETIC',
            'author': {'name': 'Synthetic Observer', 'contactEmail': 'observer@example.invalid',
                       'address': 'Synthetic address', 'experience': None},
            'siteDeclared': 'Synthetic site', 'noveltyNote': 'Synthetic fixture only; no discovery claim.',
            'instrument': {'methodDeclared': 'CCD', 'description': 'Synthetic reflector detector',
                           'apertureMeters': '0.50', 'fRatio': '5.0'},
            'position': {'raDegrees': '359.999999999', 'decDegrees': '-89.123456789', 'equinoxDeclared': 'J2000',
                         'rmsRaCosDecArcsec': None, 'rmsDecArcsec': None},
            'observations': [{'obsTime': '2026-10-09T01:02:03.120000Z', 'timeMeaningDeclared': 'MID_EXPOSURE_UTC',
                'exposureSeconds': '30.000', 'magnitude': '12.345600', 'magnitudeError': '0.1200',
                'uncertaintyConventionDeclared': 'RANDOM_1SIGMA_MAG', 'bandpassDeclared': 'ZTF_r',
                'imagePath': 'INPUT.dat', 'reductionPath': 'ALGORITHM.dat'}],
            'referenceImages': [{'obsTime': '2026-10-08T01:02:03Z', 'timeMeaningDeclared': 'MID_EXPOSURE_UTC',
                'bandpassDeclared': 'ZTF_r', 'limitingMagnitude': None, 'presenceDeclared': 'NOT_ASSESSED',
                'imagePath': 'REFERENCE.dat', 'reductionPath': 'ALGORITHM.dat'}],
            'catalogChecks': [{'kind': 'VARIABLE', 'catalogDeclared': 'Synthetic variable catalogue',
                              'checkedUTC': None, 'outcomeDeclared': 'NOT_CHECKED', 'evidencePath': None}]}
        self.path = self.root / 'request.json'

    def pin(self):
        raw = encode(self.request); self.path.write_bytes(raw); return hashlib.sha256(raw).hexdigest()

    def export(self): return cbat.export(self.local, self.path, self.pin(), self.output)

    def test_ascii_precision_provenance_and_no_network_or_authority(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')): directory = self.export()
        raw = (directory / 'preview.txt').read_bytes(); text = raw.decode('ascii')
        self.assertTrue(text.startswith('PRIVATE PREVIEW - NOT A DISCOVERY REPORT - NOT SENT\n'))
        for value in ['359.999999999', '-89.123456789', '12.345600', '0.1200', '30.000', '2026-10-09T01:02:03.120000Z']:
            self.assertIn(value, text)
        self.assertNotIn('INPUT.dat', text); self.assertNotIn('REFERENCE.dat', text)
        self.assertFalse((directory / 'preview.eml').exists())
        value = decode((directory / 'preview.json').read_bytes())
        self.assertEqual(value['scienceValidation'], 'NOT_VALIDATED'); self.assertFalse(value['submissionAuthorized'])
        self.assertFalse(value['declarationsAttested']); self.assertEqual(value['externalSubmission'], 'NONE')
        self.assertEqual(value['providerReadiness'], 'NOT_EVALUATED'); self.assertEqual(len(value['selectedEvidence']), 3)
        self.assertIn('possible Galactic nova - CCD - ', value['subjectPreview'])
        receipt = decode((directory / 'export.json').read_bytes())
        for name, record in receipt['files'].items(): self.assertEqual(fingerprint(directory / name), record)

    def test_unknown_measurements_contact_and_checks_are_not_zero_or_nondetection(self):
        row = self.request['observations'][0]
        for key in ('magnitude', 'magnitudeError', 'exposureSeconds', 'bandpassDeclared'): row[key] = None
        self.request['author']['contactEmail'] = None
        directory = self.export(); text = (directory / 'preview.txt').read_text()
        self.assertIn('Magnitude (declared): UNKNOWN', text)
        self.assertIn('Limiting magnitude (declared): UNKNOWN', text)
        self.assertIn('Reference presence (declared): Not assessed', text)
        self.assertNotIn('Nondetection declared, not validated', text)
        value = decode((directory / 'preview.json').read_bytes())
        self.assertIn('author.contactEmail', value['unknownFields'])
        self.assertIn('observations[0].magnitudeError', value['unknownFields'])
        self.assertIn('CURRENT_DUPLICATE_VARIABLE_AND_MOVING_OBJECT_CHECKS', value['missingGates'])

    def test_null_position_and_empty_reference_and_check_lists_remain_private(self):
        for key in ('raDegrees', 'decDegrees'): self.request['position'][key] = None
        self.request['referenceImages'] = []; self.request['catalogChecks'] = []
        value = decode((self.export() / 'preview.json').read_bytes())
        self.assertIn('position.raDegrees', value['unknownFields']); self.assertFalse(value['submissionAuthorized'])
        self.assertIn('MULTI_EXPOSURE_AND_REFERENCE_VALIDATION', value['missingGates'])

    def test_single_line_ascii_and_contact_injection_rejected(self):
        for value in ['Observer\r\nBcc: victim@example.invalid', 'Observer\tName', 'Observer\x00', 'Obs\u00e9rver', '\ud800', ' padded ']:
            self.request['author']['name'] = value
            with self.subTest(value=repr(value)), self.assertRaises(ProtocolError): self.export()
        self.request['author']['name'] = 'Synthetic Observer'
        for value in ['a@example.invalid,b@example.invalid', 'a@', 'a..b@example.invalid', 'a@example..invalid', 'a@exam_ple.invalid']:
            self.request['author']['contactEmail'] = value
            with self.assertRaises(ProtocolError): self.export()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_decimal_ranges_precision_and_types_rejected_without_rounding(self):
        position = self.request['position']; row = self.request['observations'][0]
        for section, key, values in [(position, 'raDegrees', ['360', '-0.1', 'NaN', 12, True, '0.1234567890']),
            (position, 'decDegrees', ['90.000000001', '-90.000000001']),
            (row, 'magnitude', ['1e2', 'Infinity', '01', [], '0.1234567890']),
            (row, 'magnitudeError', ['0', '-0.01'])]:
            old = section[key]
            for value in values:
                section[key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ProtocolError): self.export()
            section[key] = old

    def test_errors_require_corresponding_position_or_magnitude(self):
        self.request['observations'][0]['magnitude'] = None
        with self.assertRaisesRegex(ProtocolError, 'CBAT_ERROR_WITHOUT_MAGNITUDE'): self.export()
        self.request['observations'][0]['magnitudeError'] = None
        self.request['position']['raDegrees'] = None
        with self.assertRaisesRegex(ProtocolError, 'CBAT_POSITION_PAIR'): self.export()
        self.request['position']['decDegrees'] = None; self.request['position']['rmsDecArcsec'] = '0.1'
        with self.assertRaisesRegex(ProtocolError, 'CBAT_POSITION_ERROR_WITHOUT_POSITION'): self.export()

    def test_time_semantics_and_invalid_calendar_not_inferred(self):
        row = self.request['observations'][0]
        for value in ['2026-02-30T01:00:00Z', '2026-10-09T01:00:00+02:00', '2016-12-31T23:59:60Z', '2026-10-09', '2026-10-09T01:00:00.1234567Z']:
            row['obsTime'] = value
            with self.assertRaises(ProtocolError): self.export()
        row['obsTime'] = '2026-10-09T01:00:00Z'; row['timeMeaningDeclared'] = 'OBSJD'
        with self.assertRaisesRegex(ProtocolError, 'CBAT_CONVENTIONS'): self.export()

    def test_checked_catalog_is_only_a_declaration_and_requires_bound_evidence(self):
        row = self.request['catalogChecks'][0]
        row.update(outcomeDeclared='NO_MATCH_DECLARED', checkedUTC='2026-10-09T01:00:00Z', evidencePath='REFERENCE.dat')
        directory = self.export(); value = decode((directory / 'preview.json').read_bytes())
        self.assertFalse(value['declarationsAttested']); self.assertEqual(value['providerReadiness'], 'NOT_EVALUATED')
        row['evidencePath'] = 'missing.dat'
        with self.assertRaisesRegex(ProtocolError, 'CBAT_UNREGISTERED_EVIDENCE'): cbat.inspect(self.local, self.path, self.pin())

    def test_unchecked_catalog_cannot_claim_timestamp_or_evidence_and_duplicates_rejected(self):
        row = self.request['catalogChecks'][0]; row['checkedUTC'] = '2026-10-09T01:00:00Z'
        with self.assertRaisesRegex(ProtocolError, 'CBAT_UNCHECKED_CONTRADICTION'): self.export()
        row['checkedUTC'] = None; self.request['catalogChecks'].append(copy.deepcopy(row))
        with self.assertRaisesRegex(ProtocolError, 'CBAT_DUPLICATE_CHECK'): self.export()

    def test_repeated_image_and_reference_overlap_do_not_count_as_new_observation(self):
        self.request['observations'].append(copy.deepcopy(self.request['observations'][0]))
        with self.assertRaisesRegex(ProtocolError, 'CBAT_DUPLICATE_IMAGE'): self.export()
        self.request['observations'].pop(); self.request['referenceImages'][0]['imagePath'] = 'INPUT.dat'
        with self.assertRaisesRegex(ProtocolError, 'CBAT_DUPLICATE_REFERENCE'): self.export()

    def test_scopes_and_caller_authority_injection_rejected(self):
        for key, value in [('categoryDeclared', 'EXTRAGALACTIC_TRANSIENT_CANDIDATE'), ('sourceOriginDeclared', [])]:
            old = self.request[key]; self.request[key] = value
            with self.assertRaises(ProtocolError): self.export()
            self.request[key] = old
        for key in ('recipient', 'api_key', 'submissionAuthorized', 'scienceValidation'):
            self.request[key] = 'claim'
            with self.assertRaises(ProtocolError): self.export()
            del self.request[key]

    def test_raw_duplicate_keys_stale_request_and_changed_registered_bytes_rejected(self):
        raw = encode(self.request)[:-1] + b',"sourceOriginDeclared":"REAL"}'
        self.path.write_bytes(raw)
        with self.assertRaises(ProtocolError): cbat.inspect(self.local, self.path, hashlib.sha256(raw).hexdigest())
        pinned = self.pin(); self.path.write_bytes(b'{}')
        with self.assertRaisesRegex(ProtocolError, 'CBAT_REQUEST_CHANGED'): cbat.export(self.local, self.path, pinned, self.output)
        (self.artifacts / 'INPUT.dat').write_bytes(b'changed')
        with self.assertRaisesRegex(ProtocolError, 'LOCAL_BYTES_MISMATCH'): self.export()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_unregistered_and_traversal_evidence_rejected(self):
        for path in ('../INPUT.dat', 'missing.dat', []):
            self.request['observations'][0]['imagePath'] = path
            with self.assertRaises(ProtocolError): self.export()

    def test_root_overlap_and_retry_never_overwrite(self):
        pinned = self.pin()
        for root in (self.root, self.artifacts, self.registry):
            with self.assertRaises(ProtocolError): cbat.export(self.local, self.path, pinned, root)
        directory = self.export(); before = {p.name: p.read_bytes() for p in directory.iterdir()}
        with self.assertRaises(FileExistsError): self.export()
        self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})

    def test_mid_export_mutation_preserves_failure_and_blocks_retry(self):
        original = cbat.render
        def mutate(value):
            (self.artifacts / 'INPUT.dat').write_bytes(b'changed-during-export'); return original(value)
        with patch.object(cbat, 'render', side_effect=mutate), self.assertRaises(ProtocolError): self.export()
        directory = self.output / self.request['exportRef']
        self.assertTrue((directory / 'failed.json').exists()); self.assertFalse((directory / 'export.json').exists())
        (self.artifacts / 'INPUT.dat').write_bytes(b'synthetic-not-astronomical-data')
        with self.assertRaises(FileExistsError): self.export()


if __name__ == '__main__': unittest.main()
