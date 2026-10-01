"""Synthetic DSDM asset checks; never access real image payloads."""
import copy
import unittest

from tools.pixinsight.workflow_archive.archive import ArchiveError, digest, encode
from .asset_metadata import KIND, MEASUREMENTS, REQUIRED, COMMON, check_asset_metadata
from .registration_validation import KIND as REGISTRATION_KIND, check_registration_metadata
from .test_catalog_context import fixture as catalog_fixture


def fixture():
    data = dict(kind=KIND, originalAssetId='SYN-ORIGINAL', previewAssetId='SYN-PREVIEW',
        assets=[dict(assetId='SYN-ORIGINAL', assetClass='FINAL_SCIENTIFIC', originalFileName='synthetic.xisf',
                     format='XISF', sizeBytes=120, immutabilityStatus='NOT_ASSESSED',
                     integrityStatus='NOT_VERIFIED', registrationStatus='DISCOVERED',
                     canonicalHashAlgorithm='SHA-256', canonicalContentHash='a' * 64),
                dict(assetId='SYN-PREVIEW', assetClass='FINAL_PUBLICATION', originalFileName='synthetic.jpg',
                     format='JPEG', sizeBytes=60, immutabilityStatus='NOT_ASSESSED',
                     integrityStatus='NOT_VERIFIED', registrationStatus='DISCOVERED',
                     canonicalHashAlgorithm='SHA-256', canonicalContentHash='b' * 64)],
        volumes=[dict(storageVolumeId='SYN-VOLUME', logicalName='Synthetic', storageType='LOCAL_DISK',
                      role='STAGING', healthStatus='UNKNOWN', availabilityStatus='UNKNOWN',
                      encryptionStatus='UNKNOWN', backupStatus='UNKNOWN')],
        locators=[dict(locatorId='SYN-LOC-1', assetId='SYN-ORIGINAL', storageVolumeId='SYN-VOLUME',
                       relativePath='original/synthetic.xisf', locatorType='SOURCE', availabilityStatus='SYN-UNRESOLVED',
                       firstSeenAtUtc='2026-01-01T12:00:00Z', sanitizedForPublication=False),
                  dict(locatorId='SYN-LOC-2', assetId='SYN-PREVIEW', storageVolumeId='SYN-VOLUME',
                       relativePath='preview/synthetic.jpg', locatorType='SOURCE', availabilityStatus='SYN-UNRESOLVED',
                       firstSeenAtUtc='2026-01-01T12:00:00Z', sanitizedForPublication=False)],
        integrityRecords=[dict(integrityRecordId='SYN-HASH-1', assetId='SYN-ORIGINAL', locatorId='SYN-LOC-1',
                               algorithm='SHA-256', hashValue='a' * 64, computedAtUtc='2026-01-01T12:00:00Z',
                               computedBy='SYN-ACTOR', verificationType='INITIAL', result='COMPUTED'),
                          dict(integrityRecordId='SYN-HASH-2', assetId='SYN-PREVIEW', locatorId='SYN-LOC-2',
                               algorithm='SHA-256', hashValue='b' * 64, computedAtUtc='2026-01-01T12:00:00Z',
                               computedBy='SYN-ACTOR', verificationType='INITIAL', result='COMPUTED')],
        relations=[dict(assetRelationId='SYN-REL-1', sourceAssetId='SYN-PREVIEW', targetAssetId='SYN-ORIGINAL',
                        relationType='PUBLICATION_VARIANT_OF', confidence='SYN-UNRESOLVED')])
    for collection in REQUIRED:
        for row in data[collection]:
            row.update(createdAtUtc='2026-01-01T12:00:00Z', createdBy='SYN-ACTOR',
                       updatedAtUtc='2026-01-01T12:00:00Z', updatedBy='SYN-ACTOR', recordVersion=1,
                       lifecycleStatus='SYN-UNRESOLVED', sourceSystem='MANUAL')
    measured = dict(kind=MEASUREMENTS, items=[dict(assetId=row['assetId'], sha256=row['canonicalContentHash'],
                        sizeBytes=row['sizeBytes'], scope='FULL_FILE_BYTES', measuredAtUtc='2026-01-01T12:00:00Z',
                        evidenceRef='SYN-EVIDENCE') for row in data['assets']])
    return data, measured


def check(data, measured):
    raw = encode(data)
    kwargs = {}
    if measured is not None:
        measurement_raw = encode(measured)
        kwargs = dict(measurement_source=measurement_raw, measurement_digest=digest(measurement_raw))
    return check_asset_metadata(raw, digest(raw), **kwargs)


class AssetMetadataTests(unittest.TestCase):
    def test_matching_selected_metadata_never_confers_acceptance(self):
        data, measured = fixture()
        before = copy.deepcopy((data, measured))
        result = check(data, measured)
        self.assertEqual(result['findings'], [])
        self.assertTrue(result['vocabularyGaps'])
        self.assertEqual(result['eligibilityFindings'], [])
        self.assertFalse(result['acceptanceEligible'])
        self.assertFalse(result['catalogWritePerformed'])
        self.assertEqual(result['state'], 'DRAFT_NOT_ACCEPTED')
        self.assertEqual(before, (data, measured))
        self.assertEqual(result, check(data, measured))

    def test_each_mandatory_field_is_required_without_defaults(self):
        for collection, fields in REQUIRED.items():
            for field in (*COMMON, *fields):
                data, measured = fixture()
                del data[collection][0][field]
                with self.subTest(collection=collection, field=field):
                    self.assertIn(dict(collection=collection, index=0, field=field, code='REQUIRED'),
                                  check(data, measured)['findings'])
                    self.assertNotIn(field, data[collection][0])

    def test_same_id_duplicate_ids_and_missing_selection(self):
        for mutation in ('same', 'duplicate', 'missing'):
            data, measured = fixture()
            if mutation == 'same':
                data['previewAssetId'] = data['originalAssetId']
            elif mutation == 'duplicate':
                data['assets'].append(copy.deepcopy(data['assets'][0]))
            else:
                data['originalAssetId'] = 'SYN-ABSENT'
            self.assertTrue(check(data, measured)['findings'])

    def test_duplicate_unselected_identity_is_not_ignored(self):
        data, measured = fixture()
        extra = copy.deepcopy(data['assets'][0])
        extra['assetId'] = 'SYN-EXTRA'
        data['assets'] += [extra, copy.deepcopy(extra)]
        self.assertIn('DUPLICATE_ID', [f['code'] for f in check(data, measured)['findings']])

    def test_all_references_are_exact(self):
        for collection, field in (('locators', 'assetId'), ('locators', 'storageVolumeId'),
                ('integrityRecords', 'assetId'), ('integrityRecords', 'locatorId'),
                ('integrityRecords', 'previousIntegrityRecordId'), ('relations', 'sourceAssetId'),
                ('relations', 'targetAssetId')):
            data, measured = fixture()
            data[collection][0][field] = 'SYN-ABSENT'
            self.assertIn('UNRESOLVED_REFERENCE', [f['code'] for f in check(data, measured)['findings']])

    def test_missing_locator_or_integrity_record(self):
        for collection, code in (('locators', 'MISSING_LOCATOR'), ('integrityRecords', 'MISSING_INTEGRITY_RECORD')):
            data, measured = fixture()
            data[collection] = data[collection][1:]
            self.assertIn(code, [f['code'] for f in check(data, measured)['findings']])

    def test_relative_path_cannot_be_absolute_or_escape_root(self):
        for path in ('../private', 'C:\\private', '/private', '\\\\host\\share', 'a/../b', 'a//b', 'a:b', ''):
            data, measured = fixture()
            data['locators'][0]['relativePath'] = path
            self.assertTrue(check(data, measured)['findings'])

    def test_duplicate_active_location_ignores_separator_spelling(self):
        data, measured = fixture()
        data['locators'][1]['relativePath'] = 'original\\synthetic.xisf'
        self.assertIn('DUPLICATE_ACTIVE_LOCATION', [f['code'] for f in check(data, measured)['findings']])
        data['locators'][1]['supersededAtUtc'] = '2026-01-02T12:00:00Z'
        self.assertNotIn('DUPLICATE_ACTIVE_LOCATION', [f['code'] for f in check(data, measured)['findings']])

    def test_volume_logical_names_are_unique_and_checksums_do_not_merge_assets(self):
        data, measured = fixture()
        volume = copy.deepcopy(data['volumes'][0])
        volume['storageVolumeId'] = 'SYN-VOLUME-2'
        data['volumes'].append(volume)
        self.assertIn('DUPLICATE_LOGICAL_NAME', [f['code'] for f in check(data, measured)['findings']])
        data, measured = fixture()
        data['assets'][1]['canonicalContentHash'] = 'a' * 64
        data['integrityRecords'][1]['hashValue'] = 'a' * 64
        measured['items'][1]['sha256'] = 'a' * 64
        self.assertEqual(check(data, measured)['findings'], [])
        self.assertNotEqual(data['assets'][0]['assetId'], data['assets'][1]['assetId'])

    def test_integrity_locator_must_belong_to_same_asset(self):
        data, measured = fixture()
        data['integrityRecords'][0]['locatorId'] = 'SYN-LOC-2'
        self.assertIn('LOCATOR_ASSET_MISMATCH', [f['code'] for f in check(data, measured)['findings']])

    def test_positive_integrity_hash_cannot_contradict_asset(self):
        data, measured = fixture()
        data['integrityRecords'][0]['hashValue'] = 'c' * 64
        self.assertIn('INTEGRITY_IDENTITY_MISMATCH', [f['code'] for f in check(data, measured)['findings']])

    def test_integrity_predecessor_cycles_and_cross_asset_links(self):
        data, measured = fixture()
        data['integrityRecords'][0]['previousIntegrityRecordId'] = 'SYN-HASH-2'
        data['integrityRecords'][1]['previousIntegrityRecordId'] = 'SYN-HASH-1'
        codes = [f['code'] for f in check(data, measured)['findings']]
        self.assertIn('PREDECESSOR_MISMATCH', codes)
        self.assertIn('PREDECESSOR_CYCLE', codes)

    def test_preview_relation_is_explicit_and_directional(self):
        for mode in ('self', 'reverse', 'unrelated'):
            data, measured = fixture()
            relation = data['relations'][0]
            if mode == 'self':
                relation['sourceAssetId'] = relation['targetAssetId']
            elif mode == 'reverse':
                relation['sourceAssetId'], relation['targetAssetId'] = relation['targetAssetId'], relation['sourceAssetId']
            else:
                relation['relationType'] = 'RELATED_TO'
            self.assertIn('MISSING_SELECTED_DERIVATIVE_RELATION', [f['code'] for f in check(data, measured)['findings']])

    def test_measurements_are_required_and_header_hash_is_not_full_file_hash(self):
        data, measured = fixture()
        self.assertIn('MEASUREMENTS_UNAVAILABLE', [f['code'] for f in check(data, None)['findings']])
        measured['items'][0]['scope'] = 'PRIMARY_HEADER_ONLY'
        codes = [f['code'] for f in check(data, measured)['findings']]
        self.assertIn('FULL_FILE_SCOPE_REQUIRED', codes)
        self.assertIn('FULL_FILE_MEASUREMENT_MISSING', codes)

    def test_measured_hash_size_and_identity_are_compared_exactly(self):
        for field, value in (('sha256', 'c' * 64), ('sizeBytes', 121), ('assetId', 'SYN-OTHER')):
            data, measured = fixture()
            measured['items'][0][field] = value
            self.assertTrue(check(data, measured)['findings'])

    def test_duplicate_measurement_cannot_select_last_writer(self):
        data, measured = fixture()
        measured['items'].append(copy.deepcopy(measured['items'][0]))
        codes = [f['code'] for f in check(data, measured)['findings']]
        self.assertIn('DUPLICATE_ID', codes)
        self.assertIn('FULL_FILE_MEASUREMENT_MISSING', codes)

    def test_unsafe_states_remain_blockers_not_cleansed_by_matching_hashes(self):
        data, measured = fixture()
        data['assets'][0]['registrationStatus'] = 'WITHDRAWN'
        data['integrityRecords'][0]['result'] = 'PARTIAL'
        codes = [f['code'] for f in check(data, measured)['eligibilityFindings']]
        self.assertIn('ASSET_INELIGIBLE', codes)
        self.assertIn('NEGATIVE_OR_PARTIAL_INTEGRITY', codes)

    def test_hash_pair_optional_nulls_and_typed_bounds(self):
        for field, value in (('sizeBytes', True), ('sizeBytes', -1), ('sizeBytes', 2**63),
                ('metadataCompleteness', 101), ('registrationStatus', []), ('canonicalHashAlgorithm', None)):
            data, measured = fixture()
            data['assets'][0][field] = value
            self.assertTrue(check(data, measured)['findings'])
        data, measured = fixture()
        data['assets'][0]['metadataCompleteness'] = None
        self.assertEqual(check(data, measured)['findings'], [])

    def test_dates_not_inferred_and_unordered_dates_reject(self):
        data, measured = fixture()
        data['locators'][0]['lastVerifiedAtUtc'] = '2026-01-01T11:00:00Z'
        self.assertIn('TIME_ORDER', [f['code'] for f in check(data, measured)['findings']])
        data['locators'][0]['lastVerifiedAtUtc'] = '2026-01-01'
        self.assertIn('INVALID_VALUE', [f['code'] for f in check(data, measured)['findings']])

    def test_malformed_collections_and_measurements_are_bounded(self):
        for value in (None, [], {}, 'private', True, [None], [{}] * 9):
            data, measured = fixture()
            data['assets'] = value
            self.assertTrue(check(data, measured)['findings'])
            data, measured = fixture()
            measured['items'] = value
            self.assertTrue(check(data, measured)['findings'])

    def test_private_values_and_unknown_keys_not_reflected(self):
        data, measured = fixture()
        secret = 'PRIVATE-SENTINEL'
        data[secret] = secret
        data['assets'][0][secret] = secret
        measured['items'][0]['assetId'] = secret
        self.assertNotIn(secret, encode(check(data, measured)).decode())

    def test_independent_input_anchors_and_json_limits(self):
        data, measured = fixture()
        raw, evidence = encode(data), encode(measured)
        with self.assertRaises(ArchiveError):
            check_asset_metadata(raw, digest(raw), measurement_source=evidence, measurement_digest='0' * 64)
        with self.assertRaises(ArchiveError):
            check_asset_metadata(raw, '0' * 64)
        for raw in (b'{"assets":[],"assets":[]}', b'{"x":NaN}', b'[]', b' ' * (256*1024+1)):
            with self.assertRaises(ArchiveError):
                check_asset_metadata(raw, digest(raw))

    def test_composed_candidate_is_not_an_authoritative_binding(self):
        assets, measured = fixture()
        selection = dict(kind=REGISTRATION_KIND, catalogContext=catalog_fixture(), assetSelection=assets,
                         sessionId='SYN-SESSION', targetId='TGT-SYN-001')
        raw, evidence = encode(selection), encode(measured)
        result = check_registration_metadata(raw, digest(raw), measurement_source=evidence,
                                             measurement_digest=digest(evidence))
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['reports']['assetSelection']['findings'], [])
        self.assertFalse(result['acceptanceEligible'])
        self.assertIn('EXACT_F4_WORKFLOW_BINDING', result['unverified'])
        selection['targetId'] = 'TGT-SYN-OTHER'
        raw = encode(selection)
        self.assertIn('SELECTED_CONTEXT_UNRESOLVED', check_registration_metadata(raw, digest(raw))['findings'])

    def test_composed_context_rejects_target_mismatch_and_ambiguous_catalog(self):
        assets, _ = fixture()
        catalog = catalog_fixture()
        target = copy.deepcopy(catalog['targets'][0])
        target['targetId'] = 'TGT-SYN-OTHER'
        catalog['targets'].append(target)
        catalog['catalogItems'].append(copy.deepcopy(catalog['catalogItems'][0]))
        selection = dict(kind=REGISTRATION_KIND, catalogContext=catalog, assetSelection=assets,
                         sessionId='SYN-SESSION', targetId='TGT-SYN-OTHER')
        raw = encode(selection)
        result = check_registration_metadata(raw, digest(raw))
        self.assertIn('SELECTED_TARGET_MISMATCH', result['findings'])
        self.assertIn('SELECTED_CATALOG_ITEM_UNRESOLVED', result['findings'])

    def test_composed_malformed_fields_fail_closed(self):
        for value in (None, [], {}, True):
            raw = encode(dict(kind=REGISTRATION_KIND, catalogContext=value, assetSelection=value,
                              sessionId=value, targetId=value))
            result = check_registration_metadata(raw, digest(raw))
            self.assertTrue(result['findings'])
            self.assertFalse(result['acceptanceEligible'])


if __name__ == '__main__':
    unittest.main()
