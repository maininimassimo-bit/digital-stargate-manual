"""Synthetic structural failures cannot confer scientific acceptance."""
import copy
import unittest

from tools.pixinsight.workflow_archive.archive import ArchiveError, digest, encode
from .configuration_preflight import check_configuration


def fixture():
    rows = {
        'observatory': {'observatoryId': 'SYN-SITE', 'name': 'Synthetic',
                        'timezoneId': 'Etc/UTC', 'status': 'ACTIVE'},
        'telescope': {'telescopeId': 'SYN-OTA', 'model': 'Synthetic', 'status': 'ACTIVE'},
        'camera': {'cameraId': 'SYN-CAMERA', 'model': 'Synthetic', 'isColor': True,
                   'status': 'ACTIVE'},
        'configuration': {'instrumentConfigurationId': 'SYN-CONFIG',
                          'observatoryId': 'SYN-SITE', 'telescopeId': 'SYN-OTA',
                          'cameraId': 'SYN-CAMERA', 'configurationName': 'Synthetic',
                          'configurationVersion': 1, 'validFromUtc': '2026-01-01T12:00:00Z',
                          'status': 'DRAFT'},
    }
    for row in rows.values():
        row.update(createdAtUtc='2026-10-01T10:00:00Z', createdBy='SYN-ACTOR',
                   updatedAtUtc='2026-10-01T10:00:00Z', updatedBy='SYN-ACTOR',
                   recordVersion=1, lifecycleStatus='DRAFT', sourceSystem='MANUAL')
    return rows


def check(data):
    raw = encode(data)
    return check_configuration(raw, digest(raw))


class ConfigurationPreflightTests(unittest.TestCase):
    def test_no_findings_is_not_acceptance_or_historical_verification(self):
        data = fixture()
        before = copy.deepcopy(data)
        result = check(data)
        self.assertEqual(result['structuralState'], 'NO_STRUCTURAL_FINDINGS')
        self.assertFalse(result['acceptanceEligible'])
        self.assertFalse(result['catalogWritePerformed'])
        self.assertEqual(result['state'], 'DRAFT_NOT_ACCEPTED')
        self.assertIn('HISTORICAL_CONFIGURATION_VALIDITY', result['unverified'])
        self.assertEqual(data, before)
        self.assertEqual(result, check(data))

    def test_declared_models_cannot_replace_configuration(self):
        data = fixture()
        data['configuration'] = None
        result = check(data)
        self.assertIn({'section': 'configuration', 'field': None, 'code': 'MISSING_RECORD'},
                      result['findings'])

    def test_missing_historical_time_never_defaults_to_receipt_time(self):
        data = fixture()
        del data['configuration']['validFromUtc']
        result = check(data)
        self.assertIn({'section': 'configuration', 'field': 'validFromUtc', 'code': 'REQUIRED'},
                      result['findings'])
        self.assertNotIn('validFromUtc', data['configuration'])

    def test_invalid_calendar_naive_and_offset_times(self):
        for value in ('2026-02-30T12:00:00Z', '2026-04-08', '2026-04-08T11:24:19',
                      '2026-04-08T11:24:19+02:00', [], True):
            with self.subTest(value=value):
                data = fixture()
                data['configuration']['validFromUtc'] = value
                self.assertTrue(any(f['field'] == 'validFromUtc' for f in check(data)['findings']))

    def test_time_comparisons_use_instants(self):
        data = fixture()
        data['configuration']['validToUtc'] = '2026-01-01T12:00:00.000000Z'
        self.assertIn('TIME_ORDER', [f['code'] for f in check(data)['findings']])
        data['configuration']['validToUtc'] = '2026-01-01T12:00:00.000001Z'
        self.assertEqual(check(data)['findings'], [])
        data['camera']['updatedAtUtc'] = '2026-09-30T10:00:00Z'
        self.assertIn('TIME_ORDER', [f['code'] for f in check(data)['findings']])

    def test_reference_is_exact_not_model_or_filename(self):
        data = fixture()
        data['configuration']['cameraId'] = data['camera']['model']
        self.assertIn('REFERENCE_MISMATCH', [f['code'] for f in check(data)['findings']])

    def test_required_fields_and_optional_unknowns(self):
        data = fixture()
        data['telescope']['nativeFocalLengthMm'] = None
        self.assertEqual(check(data)['findings'], [])
        data['camera']['isColor'] = None
        self.assertIn('REQUIRED', [f['code'] for f in check(data)['findings']])

    def test_malformed_types_bool_as_number_and_enum(self):
        for field, value in (('configurationVersion', True), ('status', {}),
                             ('effectiveFocalLengthMm', False), ('recordVersion', 0),
                             ('configurationName', '   ')):
            with self.subTest(field=field):
                data = fixture()
                data['configuration'][field] = value
                self.assertTrue(check(data)['findings'])

    def test_unknown_fields_and_diagnostics_do_not_reflect_private_content(self):
        data = fixture()
        secret = 'PRIVATE-SENTINEL-DO-NOT-REFLECT'
        data[secret] = secret
        data['camera'][secret] = secret
        data['configuration']['cameraId'] = secret
        result = check(data)
        self.assertNotIn(secret, encode(result).decode())
        self.assertEqual(len(result['findings']), 3)

    def test_integrity_and_json_resource_boundaries(self):
        raw = encode(fixture())
        with self.assertRaises(ArchiveError):
            check_configuration(raw, '0' * 64)
        for raw in (b'{"camera":{},"camera":{}}', b'{"x":NaN}', b'[]',
                    b'{"x":' + b'[' * 40 + b'0' + b']' * 40 + b'}', b' ' * (256 * 1024 + 1)):
            with self.subTest(size=len(raw)), self.assertRaises(ArchiveError):
                check_configuration(raw, digest(raw))

    def test_bad_records_report_bounded_fixed_findings(self):
        for value in (None, [], True, 3, 'private'):
            result = check({key: value for key in fixture()})
            self.assertEqual(len(result['findings']), 4)
            self.assertFalse(result['acceptanceEligible'])


if __name__ == '__main__':
    unittest.main()
