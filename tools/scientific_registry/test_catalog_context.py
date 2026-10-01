"""Synthetic selected-context checks: no scientific acceptance or image access."""
import copy
import unittest

from tools.pixinsight.workflow_archive.archive import ArchiveError, digest, encode
from .catalog_context import KIND, REQUIRED, COMMON, check_catalog_context
from .test_configuration_preflight import fixture as configuration_fixture


def fixture():
    data = dict(kind=KIND, configurationSelection=configuration_fixture(),
        projects=[dict(projectId='PRJ-2026-001', projectName='Synthetic', projectType='UNRESOLVED-SYNTHETIC',
                       priority=3, status='PLANNED')],
        campaigns=[dict(campaignId='CAM-2026-001', projectId='PRJ-2026-001', campaignName='Synthetic',
                        status='UNRESOLVED-SYNTHETIC')],
        targets=[dict(targetId='TGT-SYN-001', canonicalName='Synthetic', targetType='UNKNOWN')],
        observations=[dict(observationId='OBS-20260101-001', campaignId='CAM-2026-001',
                           targetId='TGT-SYN-001', observationTitle='Synthetic', observationMode='ENGINEERING',
                           priority=3, status='UNRESOLVED-SYNTHETIC', completionState='UNRESOLVED-SYNTHETIC')],
        sessions=[dict(sessionId='SYN-SESSION', observationId='OBS-20260101-001',
                       localObservingDate='2026-01-01', observatoryId='SYN-SITE',
                       instrumentConfigurationId='SYN-CONFIG', sessionStatus='PLANNED', qualityState='PENDING')],
        catalogItems=[dict(catalogItemId='CAT-SESSION-SYN-001', entityType='OBSERVATION_SESSION',
                           entityId='SYN-SESSION', catalogState='DISCOVERED', qualityState='PENDING',
                           reconciliationState='MATCHED')])
    for collection in REQUIRED:
        for row in data[collection]:
            row.update(schemaVersion='1.0', recordVersion=1, createdAtUtc='2026-10-01T10:00:00Z',
                       updatedAtUtc='2026-10-01T10:00:00Z', sourceSystem='MANUAL',
                       sourceVersion='SYN-1', sourceDigest='sha256:' + 'a' * 64)
    return data


def check(data):
    raw = encode(data)
    return check_catalog_context(raw, digest(raw))


class CatalogContextTests(unittest.TestCase):
    def test_structurally_clean_still_has_unresolved_vocabulary_and_no_acceptance(self):
        data = fixture()
        original = copy.deepcopy(data)
        report = check(data)
        self.assertEqual(report['findings'], [])
        self.assertEqual(report['configurationReport']['findings'], [])
        self.assertEqual(len(report['vocabularyGaps']), 4)
        self.assertFalse(report['acceptanceEligible'])
        self.assertFalse(report['catalogWritePerformed'])
        self.assertEqual(report['state'], 'DRAFT_NOT_ACCEPTED')
        self.assertEqual(data, original)
        self.assertEqual(report, check(data))

    def test_all_required_fields_report_missing_without_defaults(self):
        for collection, fields in REQUIRED.items():
            for field in (*COMMON, *fields):
                with self.subTest(collection=collection, field=field):
                    data = fixture()
                    del data[collection][0][field]
                    result = check(data)
                    self.assertIn(dict(collection=collection, index=0, field=field, code='REQUIRED'),
                                  result['findings'])
                    self.assertNotIn(field, data[collection][0])

    def test_priorities_are_never_invented_or_coerced(self):
        for value in (None, True, '3', 0, 6, 3.0, [], {}):
            with self.subTest(value=value):
                data = fixture()
                data['observations'][0]['priority'] = value
                self.assertTrue(any(f['field'] == 'priority' for f in check(data)['findings']))

    def test_supported_enums_and_malformed_types(self):
        for field in ('observationMode', 'status', 'completionState'):
            for value in ([], {}, True, 4):
                data = fixture()
                data['observations'][0][field] = value
                self.assertTrue(check(data)['findings'])
        data = fixture()
        data['sessions'][0]['qualityState'] = 'GREEN'
        self.assertIn('INVALID_VALUE', [f['code'] for f in check(data)['findings']])

    def test_unknown_fields_and_private_values_are_not_reflected(self):
        data = fixture()
        private = 'PRIVATE-DO-NOT-REFLECT'
        data[private] = private
        data['sessions'][0][private] = private
        data['sessions'][0]['observationId'] = private
        result = check(data)
        self.assertTrue(result['findings'])
        self.assertNotIn(private, encode(result).decode())

    def test_duplicate_ids_never_resolve_by_last_writer(self):
        data = fixture()
        other = copy.deepcopy(data['observations'][0])
        other['targetId'] = 'TGT-SYN-OTHER'
        data['observations'].append(other)
        codes = [f['code'] for f in check(data)['findings']]
        self.assertIn('DUPLICATE_ID', codes)
        self.assertIn('UNRESOLVED_REFERENCE', codes)

    def test_every_foreign_key_chain_is_checked(self):
        for collection, field, value in (
                ('campaigns', 'projectId', 'PRJ-2026-002'),
                ('observations', 'campaignId', 'CAM-2026-002'),
                ('observations', 'targetId', 'TGT-SYN-002'),
                ('sessions', 'observationId', 'OBS-20260101-002'),
                ('catalogItems', 'entityId', 'SYN-OTHER')):
            with self.subTest(collection=collection, field=field):
                data = fixture()
                data[collection][0][field] = value
                self.assertIn('UNRESOLVED_REFERENCE', [f['code'] for f in check(data)['findings']])

    def test_duplicate_catalog_entity_version_and_target_name(self):
        data = fixture()
        other = copy.deepcopy(data['catalogItems'][0])
        other['catalogItemId'] = 'CAT-SESSION-SYN-002'
        data['catalogItems'].append(other)
        target = copy.deepcopy(data['targets'][0])
        target.update(targetId='TGT-SYN-002', canonicalName='SYNTHETIC')
        data['targets'].append(target)
        codes = [f['code'] for f in check(data)['findings']]
        self.assertIn('DUPLICATE_ENTITY_VERSION', codes)
        self.assertIn('DUPLICATE_NAME', codes)

    def test_conflict_cannot_be_indexed_and_self_supersession_rejects(self):
        data = fixture()
        item = data['catalogItems'][0]
        item.update(catalogState='INDEXED', reconciliationState='CONFLICT',
                    supersedesCatalogItemId=item['catalogItemId'])
        codes = [f['code'] for f in check(data)['findings']]
        self.assertIn('CONFLICT_INDEXED', codes)
        self.assertIn('SELF_REFERENCE', codes)

    def test_configuration_and_observatory_references_must_match(self):
        for field in ('observatoryId', 'instrumentConfigurationId'):
            data = fixture()
            data['sessions'][0][field] = 'SYN-WRONG'
            self.assertIn('CONFIGURATION_REFERENCE_MISMATCH',
                          [f['code'] for f in check(data)['findings']])

    def test_known_session_instants_outside_configuration_interval(self):
        data = fixture()
        data['sessions'][0]['startedAtUtc'] = '2026-01-01T11:59:59Z'
        self.assertIn('OUTSIDE_CONFIGURATION_INTERVAL', [f['code'] for f in check(data)['findings']])
        data['sessions'][0]['startedAtUtc'] = None
        result = check(data)
        self.assertEqual(result['findings'], [])
        self.assertIn('HISTORICAL_CONFIGURATION_VALIDITY', result['unverified'])

    def test_day_precision_stays_day_precision_and_calendar_is_checked(self):
        data = fixture()
        self.assertEqual(check(data)['findings'], [])
        self.assertNotIn('startedAtUtc', data['sessions'][0])
        for value in ('2026-02-30', '2026-01-01T00:00:00Z', '2026-1-1'):
            data['sessions'][0]['localObservingDate'] = value
            self.assertTrue(check(data)['findings'])

    def test_utc_naive_times_reject_and_fractional_order_uses_instants(self):
        data = fixture()
        data['sessions'][0].update(startedAtUtc='2026-01-01T12:00:00.1Z',
                                    completedAtUtc='2026-01-01T12:00:00.01Z')
        self.assertIn('TIME_ORDER', [f['code'] for f in check(data)['findings']])
        data['sessions'][0].update(startedAtUtc='2026-01-01T12:00:00', completedAtUtc=None)
        self.assertIn('INVALID_VALUE', [f['code'] for f in check(data)['findings']])

    def test_bounds_bad_records_and_bad_configuration_never_crash(self):
        for value in (None, [], {}, 'private', True, [None], [{}] * 9):
            data = fixture()
            data['sessions'] = value
            self.assertTrue(check(data)['findings'])
        for value in (None, [], True, {'configuration': []}):
            data = fixture()
            data['configurationSelection'] = value
            self.assertEqual(check(data)['structuralState'], 'FINDINGS')

    def test_optional_nulls_and_unsupported_complex_contracts(self):
        data = fixture()
        data['campaigns'][0]['completionCriteria'] = None
        data['targets'][0]['catalogReferences'] = None
        self.assertEqual(check(data)['findings'], [])
        data['campaigns'][0]['completionCriteria'] = {'claim': 'ACCEPTED'}
        self.assertIn('UNSUPPORTED_DETAIL', [f['code'] for f in check(data)['findings']])

    def test_numeric_and_text_constraints(self):
        for collection, field, value in (
                ('targets', 'rightAscensionDeg', 360), ('targets', 'declinationDeg', True),
                ('targets', 'alternativeNames', ['same', 'same']),
                ('observations', 'requiredIntegrationByFilter', {'L': -1}),
                ('projects', 'projectName', 'a' * 201), ('projects', 'sourceDigest', 'sha256:example'),
                ('projects', 'projectId', 'name-from-file.xisf')):
            data = fixture()
            data[collection][0][field] = value
            self.assertTrue(check(data)['findings'])

    def test_forged_acceptance_does_not_change_envelope(self):
        data = fixture()
        data['sessions'][0]['qualityState'] = 'ACCEPTED'
        data['catalogItems'][0]['qualityState'] = 'ACCEPTED'
        result = check(data)
        self.assertFalse(result['acceptanceEligible'])
        self.assertEqual(result['scientificAuthority'], 'NONE')
        self.assertIn('CATALOG_ACCEPTANCE_DECISION', result['unverified'])

    def test_integrity_duplicate_keys_and_input_resource_limits(self):
        raw = encode(fixture())
        with self.assertRaises(ArchiveError):
            check_catalog_context(raw, 'b' * 64)
        for raw in (b'{"kind":1,"kind":2}', b'{"n":1e999}', b'[]',
                    b' ' * (256 * 1024 + 1)):
            with self.assertRaises(ArchiveError):
                check_catalog_context(raw, digest(raw))


if __name__ == '__main__':
    unittest.main()
