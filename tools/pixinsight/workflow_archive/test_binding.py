"""Synthetic identity/association negatives; never opens scientific images."""
from copy import deepcopy
import unittest

from .archive import ArchiveError, digest, encode
from .binding import build_binding, compare_retained
from .test_provenance import sample


def fixture():
    packet, declaration = sample()
    declaration.update(sessionId='SYNTHETIC_SESSION', target='SYNTHETIC_TARGET')
    original = {'imageId': 'img:synthetic-original', 'objectRef': 'obj:synthetic-v1',
                'sha256': digest(b'synthetic original bytes'), 'byteSize': len(b'synthetic original bytes')}
    preview = {'imageId': 'img:synthetic-preview', 'objectRef': 'obj:synthetic-preview-v1',
               'sha256': digest(b'synthetic preview bytes'), 'byteSize': len(b'synthetic preview bytes')}
    common = {'archiveState': 'CATALOGED', 'metadataState': 'COMPLETE',
              'sessionRef': 'session:SYNTHETIC_SESSION', 'targetRef': 'target:SYNTHETIC_TARGET'}
    snapshot = {'kind': 'BKL049_PRIVATE_BINDING_SNAPSHOT_V1', 'revision': 'SYNTHETIC-R1',
                'catalogAuthority': 'AP-014', 'assetAuthority': 'AP-013',
                'catalogItems': [{'entityId': 'SYNTHETIC_SESSION', 'catalogItemId': 'CAT-SYNTHETIC',
                                  'qualityState': 'ACCEPTED', 'targetRef': 'target:SYNTHETIC_TARGET'}],
                'assets': [{**original, **common, 'derivativeRefs': [preview['objectRef']]},
                           {**preview, **common, 'derivativeRefs': []}]}
    measurements = {'kind': 'BKL049_PRIVATE_MEASUREMENTS_V1', 'measuredAt': '2026-09-30T18:01:00Z',
                    'items': [original, preview]}
    association = {'kind': 'BKL049_PRIVATE_ASSOCIATION_V1', 'bindingId': 'BKL049-SYNTHETIC-BINDING',
                   'declaredBy': 'SYNTHETIC_OPERATOR', 'declaredAt': '2026-09-30T18:01:00Z',
                   'evidenceClass': 'DECLARED', 'scope': 'WORKFLOW_TO_ORIGINAL_AND_PREVIEW',
                   'packetSha256': digest(encode(packet)), 'sourceSha256': packet['source']['sha256'],
                   'workflowId': 'archive:' + packet['receiptId'], 'snapshotSha256': digest(encode(snapshot)),
                   'original': original, 'preview': preview}
    return tuple(deepcopy(value) for value in (packet, declaration, snapshot, measurements, association))


def invoke(parts, **overrides):
    packet, declaration, snapshot, measurements, association = parts
    args = {'exported_at': '2026-09-30T18:02:00Z',
            'snapshot_bytes': encode(snapshot), 'snapshot_digest': digest(encode(snapshot)),
            'current_snapshot_digest': digest(encode(snapshot)),
            'measurement_bytes': encode(measurements), 'measurement_digest': digest(encode(measurements)),
            'association_bytes': encode(association), 'association_digest': digest(encode(association))}
    args.update(overrides)
    return build_binding(encode(packet), digest(encode(packet)), declaration, **args)


def reattest_snapshot(parts):
    parts[4]['snapshotSha256'] = digest(encode(parts[2]))


class BindingTests(unittest.TestCase):
    def test_exact_binding_preserves_partial_declared_private(self):
        parts = fixture(); before = deepcopy(parts)
        result = invoke(parts)
        self.assertEqual(parts, before)
        self.assertEqual(result['receipt']['evidenceClass'], 'DECLARED')
        self.assertEqual(result['receipt']['captureCompleteness'], 'PARTIAL')
        self.assertEqual(result['receipt']['publicationState'], 'PRIVATE_NOT_APPROVED')
        self.assertEqual(result['sidecar']['capture']['observedStepCount'], 0)
        self.assertEqual(result['sidecar']['workflow']['inputs'], [])
        self.assertEqual(result['sidecar']['workflow']['outputs'][0]['assetId'], 'img:synthetic-original')
        limitations = ' '.join(result['sidecar']['capture']['limitations'])
        self.assertIn('mandatory original output is verified against the selected snapshot', limitations)
        self.assertIn('step-level outputs and masks remain unresolved', limitations)
        self.assertNotIn('No authoritative image/version binding', limitations)
        self.assertNotIn('Inputs, outputs and mask associations are unresolved.', limitations)

    def test_retry_identical_and_changed_declaration_conflict(self):
        parts = fixture(); receipt = invoke(parts)['receipt']; raw = encode(receipt)
        self.assertEqual(compare_retained(invoke(parts)['receipt'], raw, digest(raw)), 'DUPLICATE_NOOP')
        parts[4]['declaredAt'] = '2026-09-30T18:01:30Z'
        with self.assertRaisesRegex(ArchiveError, 'BINDING_RECEIPT_CONFLICT'):
            compare_retained(invoke(parts)['receipt'], raw, digest(raw))

    def test_changed_export_or_context_cannot_overwrite_receipt(self):
        parts = fixture(); raw = encode(invoke(parts)['receipt'])
        with self.assertRaisesRegex(ArchiveError, 'BINDING_RECEIPT_CONFLICT'):
            compare_retained(invoke(parts, exported_at='2026-09-30T18:03:00Z')['receipt'], raw, digest(raw))
        with self.assertRaises(ArchiveError):
            compare_retained(invoke(parts)['receipt'], raw, '0' * 64)

    def test_missing_or_wrong_independent_trust_anchors(self):
        for key in ('snapshot_digest', 'measurement_digest', 'association_digest'):
            for value in (None, '', '0' * 64):
                with self.subTest(key=key, value=value), self.assertRaises(ArchiveError):
                    invoke(fixture(), **{key: value})

    def test_duplicates_rejected_before_maps(self):
        for where, key in ((2, 'assets'), (2, 'catalogItems'), (3, 'items')):
            parts = fixture(); parts[where][key].append(deepcopy(parts[where][key][0])); reattest_snapshot(parts)
            with self.subTest(key=key), self.assertRaisesRegex(ArchiveError, 'BINDING_DUPLICATE_ID'):
                invoke(parts)
        parts = fixture(); parts[2]['assets'][1]['objectRef'] = parts[2]['assets'][0]['objectRef']; reattest_snapshot(parts)
        with self.assertRaisesRegex(ArchiveError, 'BINDING_DUPLICATE_ID'):
            invoke(parts)

    def test_wrong_measured_size_digest_version_or_missing_original(self):
        for field, value in (('byteSize', 999), ('sha256', '0'*64), ('objectRef', 'obj:wrong-version'),
                             ('imageId', 'img:other')):
            parts = fixture(); parts[3]['items'][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ArchiveError, 'BINDING_IDENTITY_MISMATCH'):
                invoke(parts)

    def test_wrong_expected_version_even_when_name_matches(self):
        parts = fixture(); parts[2]['assets'][0]['objectRef'] = 'obj:changed'; reattest_snapshot(parts)
        with self.assertRaisesRegex(ArchiveError, 'BINDING_IDENTITY_MISMATCH'):
            invoke(parts)

    def test_unrelated_workflow_source_or_packet(self):
        for field, value in (('workflowId', 'archive:unrelated'), ('sourceSha256', '0'*64),
                             ('packetSha256', '0'*64), ('snapshotSha256', '0'*64)):
            parts = fixture(); parts[4][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ArchiveError, 'BINDING_UNRELATED_SOURCE'):
                invoke(parts)

    def test_unknown_or_different_context_rejected(self):
        for field in ('sessionId', 'target'):
            for value in ('unknown', 'WRONG'):
                parts = fixture(); parts[1][field] = value
                with self.subTest(field=field, value=value), self.assertRaisesRegex(ArchiveError, 'BINDING_SIDECAR_CONTEXT'):
                    invoke(parts)

    def test_catalog_withdrawal_and_snapshot_change_revoke(self):
        parts = fixture(); parts[2]['catalogItems'][0]['qualityState'] = 'WITHDRAWN'; reattest_snapshot(parts)
        with self.assertRaisesRegex(ArchiveError, 'BINDING_CATALOG_INELIGIBLE'):
            invoke(parts)
        with self.assertRaisesRegex(ArchiveError, 'BINDING_STALE_SNAPSHOT'):
            invoke(fixture(), current_snapshot_digest='0'*64)

    def test_quarantine_and_partial_asset_metadata_fail(self):
        for field, value in (('archiveState', 'QUARANTINED'), ('metadataState', 'PARTIAL')):
            for index in (0, 1):
                parts = fixture(); parts[2]['assets'][index][field] = value; reattest_snapshot(parts)
                with self.subTest(field=field, index=index), self.assertRaisesRegex(ArchiveError, 'BINDING_ASSET_INELIGIBLE'):
                    invoke(parts)

    def test_missing_preview_relation_or_preview_identity_mismatch(self):
        parts = fixture(); parts[2]['assets'][0]['derivativeRefs'] = []; reattest_snapshot(parts)
        with self.assertRaisesRegex(ArchiveError, 'BINDING_DERIVATIVE_MISSING'):
            invoke(parts)
        parts = fixture(); parts[3]['items'][1]['sha256'] = '0'*64
        with self.assertRaisesRegex(ArchiveError, 'BINDING_IDENTITY_MISMATCH'):
            invoke(parts)

    def test_preview_different_context_or_original_as_preview(self):
        parts = fixture(); parts[2]['assets'][1]['targetRef'] = 'target:OTHER'; reattest_snapshot(parts)
        with self.assertRaisesRegex(ArchiveError, 'BINDING_DERIVATIVE_CONTEXT'):
            invoke(parts)
        parts = fixture(); parts[4]['preview'] = deepcopy(parts[4]['original'])
        with self.assertRaisesRegex(ArchiveError, 'BINDING_DERIVATIVE_IDENTITY'):
            invoke(parts)

    def test_missing_owner_declaration_not_replaced_by_hashes(self):
        for field in ('declaredBy', 'declaredAt', 'scope'):
            parts = fixture(); del parts[4][field]
            with self.subTest(field=field), self.assertRaises(ArchiveError):
                invoke(parts)
        parts = fixture(); parts[4]['evidenceClass'] = 'OBSERVED'
        with self.assertRaisesRegex(ArchiveError, 'BINDING_DECLARATION_SCOPE'):
            invoke(parts)

    def test_boundaries_and_fixed_errors(self):
        parts = fixture(); parts[3]['items'][0]['byteSize'] = True
        with self.assertRaisesRegex(ArchiveError, '^BINDING_BYTE_SIZE$'):
            invoke(parts)
        parts = fixture(); parts[4]['declaredAt'] = '2026-09-30T19:00:00Z'
        with self.assertRaisesRegex(ArchiveError, '^BINDING_TIME_ORDER$'):
            invoke(parts)
        raw = b' ' * (256 * 1024 + 1)
        with self.assertRaisesRegex(ArchiveError, '^BINDING_RECORD_INTEGRITY$'):
            invoke(fixture(), association_bytes=raw, association_digest=digest(raw))

    def test_malformed_state_types_return_only_fixed_diagnostics(self):
        for collection, field, code in (('catalogItems', 'qualityState', 'BINDING_CATALOG_STATE'),
                                        ('assets', 'archiveState', 'BINDING_ASSET_STATE'),
                                        ('assets', 'metadataState', 'BINDING_ASSET_STATE')):
            for value in ([], {}, None, True, 1):
                parts = fixture(); parts[2][collection][0][field] = value; reattest_snapshot(parts)
                with self.subTest(field=field, value=value), self.assertRaisesRegex(ArchiveError, '^'+code+'$'):
                    invoke(parts)
        raw = b'{"a":1,"a":2}'
        with self.assertRaises(ArchiveError):
            invoke(fixture(), association_bytes=raw, association_digest=digest(raw))


if __name__ == '__main__':
    unittest.main()
