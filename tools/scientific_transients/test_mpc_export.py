"""Synthetic local export and independent schema fixtures; no astronomical submission."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, decode
from tools.scientific_transients.local_registry import LocalRegistry, ROLES, fingerprint
from tools.scientific_transients import mpc_export as mpc


class MPCExportTests(unittest.TestCase):
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
        row = {'permID': '1', 'obsTime': '2026-10-09T01:02:03.120000Z',
               'timeMeaningDeclared': 'MID_EXPOSURE_UTC', 'coordinateMeaningDeclared': 'J2000_ASTROMETRIC_DEGREES',
               'uncertaintyConventionDeclared': 'RANDOM_1SIGMA_ARCSEC_RA_COSDEC_TIME_SECONDS',
               'ra': '359.999999999', 'dec': '-89.123456789', 'rmsRA': '0.25', 'rmsDec': '0.30',
               'rmsCorr': '-0.5', 'rmsTime': '0.01', 'astCat': 'Gaia3',
               'imagePath': 'INPUT.dat', 'reductionPath': 'ALGORITHM.dat'}
        self.request = {'protocol': mpc.PROTOCOL, 'exportRef': 'a' * 32, 'bindingRef': binding['bindingRef'],
                        'manifestSha256': receipt['manifestSha256'], 'sourceOriginDeclared': 'SYNTHETIC',
                        'context': {'mpcCode': '500', 'submitterName': 'A. Synthetic & Example',
                                    'observers': ['A. Synthetic'], 'measurers': ['B. Synthetic'],
                                    'telescope': {'design': 'Reflector', 'apertureMeters': '0.5', 'detector': 'CCD'}},
                        'observations': [row]}
        self.path = self.root / 'request.json'

    def pin(self):
        raw = encode(self.request); self.path.write_bytes(raw)
        return hashlib.sha256(raw).hexdigest()

    def export(self): return mpc.export(self.local, self.path, self.pin(), self.output)

    def test_precision_units_and_provenance_preserved_without_network(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')): directory = self.export()
        xml = ET.parse(directory / 'preview.xml'); node = xml.find('./obsBlock/obsData/optical')
        for name in ('permID', 'obsTime', 'ra', 'dec', 'rmsRA', 'rmsDec', 'rmsCorr', 'rmsTime', 'astCat'):
            self.assertEqual(node.findtext(name), self.request['observations'][0][name])
        value = decode((directory / 'preview.json').read_bytes())
        self.assertEqual(value['scienceValidation'], 'NOT_VALIDATED'); self.assertFalse(value['submissionAuthorized'])
        self.assertFalse(value['declarationsAttested']); self.assertEqual(value['externalSubmission'], 'NONE')
        self.assertFalse(value['observingNightOrAssociationValidated'])
        self.assertEqual(len(value['selectedEvidence']), 2)
        receipt = decode((directory / 'export.json').read_bytes())
        for name, record in receipt['files'].items(): self.assertEqual(fingerprint(directory / name), record)

    def test_unknown_uncertainties_omitted_and_retained_as_unknown(self):
        row = self.request['observations'][0]
        for key in ('rmsRA', 'rmsDec', 'rmsCorr', 'rmsTime'): row[key] = None
        directory = self.export(); xml = ET.parse(directory / 'preview.xml')
        for key in ('rmsRA', 'rmsDec', 'rmsCorr', 'rmsTime'): self.assertIsNone(xml.find('.//' + key))
        value = decode((directory / 'preview.json').read_bytes())
        self.assertEqual(set(value['unknownFieldsByObservation'][0]['unknownFields']), {'rmsRA', 'rmsDec', 'rmsCorr', 'rmsTime'})

    def test_same_instant_different_decimal_precision_rejected(self):
        row = copy.deepcopy(self.request['observations'][0]); row['obsTime'] = '2026-10-09T01:02:03.12Z'
        self.request['observations'].append(row)
        with self.assertRaisesRegex(ProtocolError, 'MPC_DUPLICATE_OBJECT_TIME'): self.export()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_distinct_object_at_same_time_supported(self):
        row = copy.deepcopy(self.request['observations'][0]); row['permID'] = '2'
        self.request['observations'].append(row)
        self.assertEqual(len(ET.parse(self.export() / 'preview.xml').findall('.//optical')), 2)

    def test_invalid_decimal_range_precision_and_types_rejected(self):
        row = self.request['observations'][0]
        for key, values in [('ra', ['360', '-0.1', 'NaN', '1e2', 12, True, '0.1234567890', '01']),
                            ('dec', ['-90.000000001', '90.000000001']),
                            ('rmsRA', ['0', '-0.1', '100000', '0.123456']), ('rmsCorr', ['1', '-1'])]:
            old = row[key]
            for value in values:
                row[key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ProtocolError): self.export()
            row[key] = old
        self.assertEqual(list(self.output.iterdir()), [])

    def test_correlation_requires_both_sigmas(self):
        self.request['observations'][0]['rmsRA'] = None
        with self.assertRaisesRegex(ProtocolError, 'MPC_CORRELATION_WITHOUT_SIGMAS'): self.export()

    def test_utc_and_conventions_not_inferred(self):
        row = self.request['observations'][0]
        for value in ['2026-02-30T01:00:00Z', '2026-10-09T01:00:00+02:00', '2016-12-31T23:59:60Z', '2026-10-09']:
            row['obsTime'] = value
            with self.assertRaises(ProtocolError): self.export()
        row['obsTime'] = '2026-10-09T01:00:00Z'; row['timeMeaningDeclared'] = 'OBSJD'
        with self.assertRaisesRegex(ProtocolError, 'MPC_CONVENTIONS'): self.export()

    def test_scope_rejects_unknown_object_catalog_mode_and_authority(self):
        for section, key, value in [(self.request['observations'][0], 'permID', 'new-object'),
                                    (self.request['observations'][0], 'astCat', 'GaiaDR3'),
                                    (self.request['context']['telescope'], 'detector', 'UNK'),
                                    (self.request, 'sourceOriginDeclared', [])]:
            old = section[key]; section[key] = value
            with self.assertRaises(ProtocolError): self.export()
            section[key] = old
        for key in ('endpoint', 'api_key', 'submissionAuthorized', 'scienceValidation'):
            self.request[key] = 'claim'
            with self.assertRaises(ProtocolError): self.export()
            del self.request[key]

    def test_hostile_text_escaped_and_illegal_xml_rejected(self):
        self.request['context']['submitterName'] = '<script>Example</script>'
        directory = self.export()
        self.assertNotIn(b'<script>', (directory / 'preview.xml').read_bytes())
        for text in ('bad\x00name', 'bad|name', '\ud800', 'bad\uffff'):
            self.request['context']['submitterName'] = text
            with self.assertRaises(ProtocolError): mpc.inspect(self.local, self.path, self.pin())

    def test_raw_duplicate_keys_and_stale_hash_rejected(self):
        raw = encode(self.request)[:-1] + b',"sourceOriginDeclared":"REAL"}'
        self.path.write_bytes(raw)
        with self.assertRaises(ProtocolError): mpc.inspect(self.local, self.path, hashlib.sha256(raw).hexdigest())
        pinned = self.pin(); self.path.write_bytes(b'{}')
        with self.assertRaisesRegex(ProtocolError, 'MPC_REQUEST_CHANGED'): mpc.export(self.local, self.path, pinned, self.output)

    def test_unregistered_and_changed_evidence_rejected(self):
        row = self.request['observations'][0]
        for path in ('../INPUT.dat', 'missing.dat'):
            row['imagePath'] = path
            with self.assertRaises(ProtocolError): self.export()
        row['imagePath'] = 'INPUT.dat'; (self.artifacts / 'INPUT.dat').write_bytes(b'changed')
        with self.assertRaisesRegex(ProtocolError, 'LOCAL_BYTES_MISMATCH'): self.export()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_root_overlap_and_reuse_do_not_overwrite(self):
        pinned = self.pin()
        for root in (self.root, self.artifacts, self.registry):
            with self.assertRaises(ProtocolError): mpc.export(self.local, self.path, pinned, root)
        directory = self.export(); before = {p.name: p.read_bytes() for p in directory.iterdir()}
        with self.assertRaises(FileExistsError): self.export()
        self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})

    def test_mid_export_mutation_preserves_partial_and_blocks_retry(self):
        original = mpc.render
        def mutate(value):
            (self.artifacts / 'INPUT.dat').write_bytes(b'changed-during-export'); return original(value)
        with patch.object(mpc, 'render', side_effect=mutate), self.assertRaises(ProtocolError): self.export()
        directory = self.output / self.request['exportRef']
        self.assertTrue((directory / 'failed.json').exists()); self.assertFalse((directory / 'export.json').exists())
        (self.artifacts / 'INPUT.dat').write_bytes(b'synthetic-not-astronomical-data')
        with self.assertRaises(FileExistsError): self.export()


def schema_fixtures(output):
    """Synthetic exporter output plus corrupted controls for an independent XSD engine."""
    output.mkdir()
    case = MPCExportTests(); case.setUp()
    try:
        for detector in ('CCD', 'CMO'):
            case.request['context']['telescope']['detector'] = detector
            case.request['exportRef'] = ('b' if detector == 'CMO' else 'a') * 32
            directory = case.export(); raw = (directory / 'preview.xml').read_bytes()
            (output / ('valid-' + detector + '.xml')).write_bytes(raw)
        for name, old, new in [('bad-version', b'version="2022"', b'version="2017"'),
                              ('bad-range', b'359.999999999', b'360.0'),
                              ('bad-order', b'<rmsTime>0.01</rmsTime>', b'<unexpected>0.01</unexpected>')]:
            (output / (name + '.xml')).write_bytes(raw.replace(old, new))
    finally: case.doCleanups()


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == '--schema-fixtures': schema_fixtures(Path(sys.argv[2]))
    else: unittest.main()
