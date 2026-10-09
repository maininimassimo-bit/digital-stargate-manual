"""Synthetic, offline review worksheet controls; no provider or scientific acceptance."""
import copy
import hashlib
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, decode
from tools.scientific_transients.local_registry import LocalRegistry, ROLES, fingerprint
from tools.scientific_transients import channel_review as review


class ChannelReviewTests(unittest.TestCase):
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
        self.request = {'protocol': review.PROTOCOL, 'reviewRef': 'a' * 32, 'candidateRef': 'b' * 32,
            'bindingRef': binding['bindingRef'], 'manifestSha256': receipt['manifestSha256'],
            'channelDeclared': 'TNS', 'categoryDeclared': 'EXTRAGALACTIC_TRANSIENT_CANDIDATE',
            'originDeclared': 'SYNTHETIC', 'reporterDeclared': 'Osservatore sintetico é',
            'position': {'raDegrees': '359.999999999', 'decDegrees': '-89.123456789', 'frameDeclared': 'ICRS',
                         'equinoxDeclared': 'NOT_APPLICABLE', 'coordinateEpochJulianYear': '2016.0',
                         'epochTimeScaleDeclared': 'TCB', 'evidencePath': 'PROVENANCE.dat'},
            'observations': [{'obsTime': '2026-10-09T01:02:03.120000Z', 'timeMeaningDeclared': 'MID_EXPOSURE_UTC',
                'exposureSeconds': '30.000', 'magnitude': '12.345600', 'magnitudeError': '0.1200',
                'uncertaintyConventionDeclared': 'RANDOM_1SIGMA_MAG', 'magnitudeSystemDeclared': 'AB_MAG',
                'bandpassDeclared': 'ZTF_r', 'imagePath': 'INPUT.dat', 'reductionPath': 'ALGORITHM.dat'}],
            'catalogChecks': [{'kind': 'PREVIOUS_REPORT', 'catalogDeclared': 'Synthetic catalogue',
                              'checkedUTC': None, 'outcomeDeclared': 'NOT_CHECKED', 'evidencePath': None}],
            'channelData': {'internalNameDeclared': 'Synthetic transient', 'reportingGroupDeclared': None,
                'discoveryDataSourceDeclared': None, 'discoveryImagePath': 'INPUT.dat',
                'priorImages': [{'obsTime': '2026-10-08T01:02:03Z', 'timeMeaningDeclared': 'MID_EXPOSURE_UTC',
                    'presenceDeclared': 'NOT_ASSESSED', 'limitingMagnitude': '20.1000', 'limitSigmaDeclared': None,
                    'magnitudeSystemDeclared': 'AB_MAG', 'bandpassDeclared': 'ZTF_r',
                    'imagePath': 'REFERENCE.dat', 'reductionPath': 'ALGORITHM.dat'}],
                'archivalContext': {'noteDeclared': None, 'evidencePath': None},
                'hostDeclared': {'name': None, 'redshift': None, 'evidencePath': None}}}
        self.path = self.root / 'request.json'

    def vsx(self):
        self.request.update(channelDeclared='VSX', categoryDeclared='VARIABLE_STAR_CANDIDATE',
            channelData={'primaryNameDeclared': 'Synthetic variable', 'crossIds': [], 'variabilityTypeDeclared': None,
                'rangeDeclared': {'brightMagnitude': '12.3000', 'faintMagnitude': '12.9000',
                                  'bandpassDeclared': 'V', 'evidencePath': 'PROVENANCE.dat'},
                'periodDeclared': {'days': '1.234567890', 'epochHjd': '2461310.123456789',
                    'epochTimeScaleDeclared': 'UTC', 'epochEventDeclared': 'PRIMARY_MINIMUM', 'evidencePath': 'PARAMETERS.dat'},
                'plots': [{'kindDeclared': 'PHASE', 'sourceDeclared': 'OWNER_GENERATED', 'evidencePath': 'REFERENCE.dat'}]})

    def pin(self):
        raw = encode(self.request); self.path.write_bytes(raw); return hashlib.sha256(raw).hexdigest()

    def export(self): return review.export(self.local, self.path, self.pin(), self.output)

    def test_tns_precision_utf8_nondetection_and_no_network(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')): directory = self.export()
        txt = (directory / 'worksheet.txt').read_text(encoding='utf-8')
        for token in ['359.999999999', '12.345600', '2026-10-09T01:02:03.120000Z', 'Osservatore sintetico é']:
            self.assertIn(token, txt)
        self.assertIn('NOT_ASSESSED', txt); self.assertNotIn('NON_DETECTION_DECLARED', txt)
        self.assertNotIn('INPUT.dat', txt); self.assertNotIn('PROVENANCE.dat', txt)
        value = decode((directory / 'worksheet.json').read_bytes())
        self.assertFalse(value['submissionAuthorized']); self.assertFalse(value['providerPayload'])
        self.assertFalse(value['providerSchemaValidated']); self.assertFalse(value['declarationsAttested'])
        self.assertEqual(value['externalSubmission'], 'NONE'); self.assertEqual(value['scienceValidation'], 'NOT_VALIDATED')
        self.assertIn('channelData.reportingGroupDeclared', value['unknownFields'])
        receipt = decode((directory / 'export.json').read_bytes())
        for name, record in receipt['files'].items(): self.assertEqual(fingerprint(directory / name), record)

    def test_vsx_period_hjd_preserved_without_conversion_or_classification(self):
        self.vsx(); directory = self.export(); txt = (directory / 'worksheet.txt').read_text(encoding='utf-8')
        self.assertIn('1.234567890', txt); self.assertIn('2461310.123456789', txt)
        self.assertIn('Epoch time scale: UTC', txt); self.assertIn('Variability type: UNKNOWN', txt)
        self.assertIn('no JD/HJD conversion', txt)
        value = decode((directory / 'worksheet.json').read_bytes())
        self.assertEqual(value['declarations']['channelData']['plots'][0]['sourceDeclared'], 'OWNER_GENERATED')
        self.assertFalse(value['declarationsAttested']); self.assertEqual(value['providerReadiness'], 'NOT_EVALUATED')

    def test_all_missing_optional_values_remain_unknown(self):
        p = self.request['position']; p.update(raDegrees=None, decDegrees=None, coordinateEpochJulianYear=None,
            epochTimeScaleDeclared='NOT_ATTESTED', frameDeclared='NOT_ATTESTED', equinoxDeclared='NOT_ATTESTED', evidencePath=None)
        row = self.request['observations'][0]
        row.update(magnitude=None, magnitudeError=None, bandpassDeclared=None, exposureSeconds=None, magnitudeSystemDeclared='NOT_ATTESTED')
        self.request['reporterDeclared'] = None; self.request['catalogChecks'] = []
        self.request['channelData'].update(priorImages=[], discoveryImagePath=None)
        value = decode((self.export() / 'worksheet.json').read_bytes())
        self.assertIn('observations[0].magnitudeError', value['unknownFields'])
        self.assertIn('position.coordinateEpochJulianYear', value['unknownFields']); self.assertFalse(value['submissionAuthorized'])

    def test_wrong_category_or_channel_and_forged_authority_rejected(self):
        saved = copy.deepcopy(self.request)
        for updates in [{'categoryDeclared': 'GALACTIC_NOVA_CANDIDATE'}, {'channelDeclared': 'CBAT'},
                        {'channelDeclared': []}, {'submissionAuthorized': True}, {'api_key': 'synthetic-secret'}]:
            self.request = {**saved, **updates}
            with self.subTest(updates=updates), self.assertRaises(ProtocolError): self.export()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_single_line_controls_bidi_surrogates_and_empty_rejected(self):
        for value in ['line\nsecond', 'line\rsecond', 'line\tsecond', 'x\x00', 'x\u202e', 'x\u2028', '\ud800', '', ' padded ']:
            self.request['reporterDeclared'] = value
            with self.subTest(value=repr(value)), self.assertRaises(ProtocolError): self.export()

    def test_decimal_overprecision_nonfinite_types_and_ra_wrap_rejected(self):
        position = self.request['position']; row = self.request['observations'][0]
        for obj, key, values in [(position, 'raDegrees', ['360', '-1', 'NaN', '1e2', 12, True, '1.1234567890']),
            (position, 'decDegrees', ['90.1', '-90.1']), (row, 'magnitudeError', ['0', '-1', 'Infinity']),
            (row, 'magnitude', ['01', {}, '1.1234567890'])]:
            original = obj[key]
            for value in values:
                obj[key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ProtocolError): self.export()
            obj[key] = original

    def test_frame_equinox_epoch_and_magnitude_conventions_rejected(self):
        saved = copy.deepcopy(self.request)
        for section, updates in [('position', {'equinoxDeclared': 'J2000'}),
            ('position', {'coordinateEpochJulianYear': None}), ('position', {'epochTimeScaleDeclared': 'UTC'}),
            ('position', {'decDegrees': None}), ('observations', {'magnitudeSystemDeclared': 'FLUX'}),
            ('observations', {'magnitude': None}), ('observations', {'timeMeaningDeclared': 'START'}),
            ('observations', {'uncertaintyConventionDeclared': 'FULL_ERROR'})]:
            self.request = copy.deepcopy(saved)
            target = self.request[section][0] if section == 'observations' else self.request[section]
            target.update(updates)
            with self.subTest(updates=updates), self.assertRaises(ProtocolError): self.export()

    def test_invalid_dates_and_leap_seconds_not_silently_normalized(self):
        for value in ['2026-02-30T00:00:00Z', '2026-10-09T01:02:03+01:00', '2016-12-31T23:59:60Z', '2026-10-09T01:02:03.1234567Z']:
            self.request['observations'][0]['obsTime'] = value
            with self.assertRaises(ProtocolError): self.export()

    def test_catalogue_declarations_require_evidence_but_are_not_attested(self):
        row = self.request['catalogChecks'][0]; row.update(outcomeDeclared='NO_MATCH_DECLARED', checkedUTC='2026-10-09T00:00:00Z')
        with self.assertRaises(ProtocolError): self.export()
        row['evidencePath'] = 'PROVENANCE.dat'
        value = review.inspect(self.local, self.path, self.pin())
        self.assertFalse(value['declarationsAttested']); self.assertEqual(value['declarations']['catalogChecks'][0]['outcomeDeclared'], 'NO_MATCH_DECLARED')
        self.request['catalogChecks'].append(copy.deepcopy(row))
        with self.assertRaises(ProtocolError): self.export()

    def test_tns_unassessed_limit_and_declared_nondetection_remain_distinct(self):
        row = self.request['channelData']['priorImages'][0]
        row.update(presenceDeclared='NON_DETECTION_DECLARED', limitingMagnitude=None)
        value = review.inspect(self.local, self.path, self.pin())
        self.assertIn('channelData.priorImages[0].limitingMagnitude', value['unknownFields'])
        self.assertEqual(value['scienceValidation'], 'NOT_VALIDATED')
        row['limitSigmaDeclared'] = '5'
        with self.assertRaises(ProtocolError): self.export()

    def test_discovery_and_prior_images_must_be_registered_and_distinct(self):
        self.request['channelData']['discoveryImagePath'] = 'REFERENCE.dat'
        with self.assertRaises(ProtocolError): self.export()
        self.request['channelData']['discoveryImagePath'] = 'INPUT.dat'
        self.request['channelData']['priorImages'][0]['imagePath'] = 'INPUT.dat'
        with self.assertRaises(ProtocolError): self.export()

    def test_archival_context_requires_paired_registered_evidence(self):
        row = self.request['channelData']['archivalContext']; row['noteDeclared'] = 'Synthetic archive context'
        with self.assertRaises(ProtocolError): self.export()
        row['evidencePath'] = 'PROVENANCE.dat'
        value = review.inspect(self.local, self.path, self.pin())
        self.assertFalse(value['providerPayload']); self.assertFalse(value['submissionAuthorized'])

    def test_vsx_range_order_and_hjd_time_scale_remain_explicit(self):
        self.vsx(); data = self.request['channelData']; data['rangeDeclared']['brightMagnitude'] = '13'
        with self.assertRaises(ProtocolError): self.export()
        data['rangeDeclared']['brightMagnitude'] = '12.3'; data['periodDeclared']['epochHjd'] = None
        with self.assertRaises(ProtocolError): self.export()
        data['periodDeclared'].update(epochTimeScaleDeclared='NOT_ATTESTED', epochEventDeclared='NOT_ATTESTED')
        value = review.inspect(self.local, self.path, self.pin())
        self.assertIn('channelData.periodDeclared.epochHjd', value['unknownFields'])

    def test_vsx_identifiers_and_plot_paths_are_unique_and_registered(self):
        self.vsx(); data = self.request['channelData']
        row = {'catalogDeclared': 'Synthetic catalog', 'idDeclared': '1234567890123456789', 'evidencePath': 'PROVENANCE.dat'}
        data['crossIds'] = [row, copy.deepcopy(row)]
        with self.assertRaises(ProtocolError): self.export()
        data['crossIds'] = [row]; data['plots'].append(copy.deepcopy(data['plots'][0]))
        with self.assertRaises(ProtocolError): self.export()
        data['plots'] = []; value = review.inspect(self.local, self.path, self.pin())
        self.assertEqual(value['declarations']['channelData']['crossIds'][0]['idDeclared'], '1234567890123456789')
        self.assertIn('INDEPENDENT_SCIENTIFIC_VALIDATION', value['missingGates'])

    def test_unregistered_traversal_changed_bytes_and_stale_request_rejected(self):
        saved = copy.deepcopy(self.request)
        for value in ['missing.dat', '../INPUT.dat', 'C:/INPUT.dat', 'INPUT\\dat']:
            self.request['observations'][0]['imagePath'] = value
            with self.assertRaises(ProtocolError): self.export()
        self.request = saved; sha = self.pin(); self.request['reporterDeclared'] = 'Changed'; self.pin()
        with self.assertRaises(ProtocolError): review.export(self.local, self.path, sha, self.output)
        (self.artifacts / 'INPUT.dat').write_bytes(b'changed')
        with self.assertRaises(ProtocolError): self.export()

    def test_duplicate_json_keys_fail_before_creating_export(self):
        raw = encode(self.request).replace(b'"protocol":', b'"protocol":"wrong","protocol":', 1)
        self.path.write_bytes(raw)
        with self.assertRaises(ProtocolError): review.export(self.local, self.path, hashlib.sha256(raw).hexdigest(), self.output)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_create_only_preserves_previous_export_and_blocks_retries(self):
        directory = self.export(); before = fingerprint(directory / 'worksheet.json')
        with self.assertRaises(FileExistsError): self.export()
        self.assertEqual(fingerprint(directory / 'worksheet.json'), before)

    def test_second_verification_failure_preserves_partial_without_success_receipt(self):
        original = self.local.verify; calls = []
        def changed(*args):
            calls.append(1)
            if len(calls) == 2: (self.artifacts / 'INPUT.dat').write_bytes(b'changed')
            return original(*args)
        with patch.object(self.local, 'verify', side_effect=changed), self.assertRaises(ProtocolError): self.export()
        directory = self.output / self.request['reviewRef']
        self.assertTrue((directory / 'failed.json').is_file()); self.assertTrue((directory / 'worksheet.txt').is_file())
        self.assertFalse((directory / 'export.json').exists())

    def test_output_overlap_rejected_before_any_export(self):
        for root in (self.artifacts, self.registry, self.root):
            with self.assertRaises(ProtocolError): review.export(self.local, self.path, self.pin(), root)

    def test_explicit_local_cli_exports_and_stale_digest_returns_conservative_error(self):
        args = [sys.executable, '-m', 'tools.scientific_transients.channel_review',
            '--artifacts', str(self.artifacts), '--registry', str(self.registry), '--request', str(self.path),
            '--request-sha256', self.pin(), '--output-root', str(self.output)]
        success = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertIn('NO_SUBMISSION_OR_SCIENCE_ACCEPTANCE', success.stdout)
        self.request['reviewRef'] = 'c' * 32; self.pin()
        failed = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(failed.returncode, 2)
        self.assertIn('Nessun invio effettuato', failed.stderr)
        self.assertNotIn(str(self.artifacts), failed.stderr)
        self.assertFalse((self.output / ('c' * 32)).exists())


if __name__ == '__main__': unittest.main()
