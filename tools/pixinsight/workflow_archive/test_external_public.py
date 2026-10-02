"""Synthetic public consent/currentness/atomic replacement tests, no cloud calls."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.scientific_registry.test_external_registry import admitted, delivery, event_for
from .archive import ArchiveError, digest, encode
from .external_public import (build_external_projection, build_external_collection,
                              publish_external_collection, SCHEMA)
from .provenance import validate_emitted_profile

NOW = '2026-10-01T11:00:00Z'
END = '2026-10-01T12:00:00Z'


def fixture():
    parts, events = admitted()
    bundle = delivery(parts, events)
    first = bundle['result']['sidecar']['workflow']['steps'][0]
    selection = dict(kind='BKL049_EXTERNAL_PUBLIC_SELECTION_V2', scope='EXACT_EXTERNAL_PREVIEW_AND_WORKFLOW',
                     deliverySha256=digest(encode(bundle)), approvedBy='SYNTHETIC_APPROVER', approvedAt=NOW,
                     validUntil=END, rightsConfirmed=True, imageId='IMG-external-test',
                     imageVersionId='VER-external-test', workflowId='WF-external-test',
                     title='Synthetic public title', attribution='Synthetic attribution',
                     preview=dict(url='https://storage.googleapis.com/synthetic-public-preview/preview.jpg',
                                  alt='Synthetic preview', sha256=bundle['result']['preview']['sha256']),
                     steps=[dict(stepId=first['stepId'], processId=first['processId'], parameters=[])])
    return bundle, selection, parts, events


def entry(bundle, selection):
    return dict(delivery_bytes=encode(bundle), delivery_digest=digest(encode(bundle)),
                current_head=bundle['journalHeadSha256'], selection_bytes=encode(selection),
                selection_digest=digest(encode(selection)), current_selection_digest=digest(encode(selection)))


def projection():
    bundle, selected, *_ = fixture()
    return build_external_projection(**entry(bundle, selected), now=NOW)


class ExternalPublicTests(unittest.TestCase):
    def test_until_withdrawal_requires_new_current_exact_approval(self):
        bundle, selected, parts, events = fixture()
        with self.assertRaises(ArchiveError):
            build_external_collection([entry(bundle, selected)], published_at=NOW, valid_until=None, now=NOW)
        selected['validUntil'] = None
        with self.assertRaises(ArchiveError):
            build_external_projection(**entry(bundle, selected), now=NOW)
        selected['kind'] = 'BKL049_EXTERNAL_PUBLIC_SELECTION_V3'
        future = '2027-10-01T11:00:00Z'
        item = entry(bundle, selected)
        value = build_external_collection([item], published_at=NOW, valid_until=None, now=future)
        self.assertEqual(value['schemaVersion'], '2.0')
        self.assertIsNone(value['validUntil'])
        self.assertEqual(len(value['records']), 1)
        for changed in ({**item, 'current_selection_digest':'0'*64},
                        {**item, 'current_head':'0'*64}):
            with self.assertRaises(ArchiveError):
                build_external_collection([changed], published_at=NOW, valid_until=None, now=future)
        events.append(encode(event_for(events, *parts[:2], 'WITHDRAW')))
        with self.assertRaises(ArchiveError):
            build_external_projection(**{**item, 'current_head':digest(events[-1])}, now=future)
        with self.assertRaises(ArchiveError):
            build_external_collection([item, item], published_at=NOW, valid_until=None, now=NOW)
        with self.assertRaises(ArchiveError):
            build_external_collection([item], published_at=NOW, valid_until=END, now=NOW)
        selected['validUntil'] = END
        with self.assertRaises(ArchiveError):
            build_external_projection(**entry(bundle, selected), now=NOW)
        selected['validUntil'] = None
        with self.assertRaises(ArchiveError):
            build_external_projection(**entry(bundle, selected), now='2026-10-01T10:59:59Z')

    def test_persistent_local_publication_and_explicit_withdrawal(self):
        bundle, selected, *_ = fixture()
        selected.update(kind='BKL049_EXTERNAL_PUBLIC_SELECTION_V3', validUntil=None)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'bkl049-public-workflows.json'
            empty = encode(build_external_collection([], published_at=None, valid_until=None, now=NOW)) + b'\n'
            target.write_bytes(empty)
            result = publish_external_collection([entry(bundle, selected)], target,
                expected_previous_digest=digest(empty), published_at=NOW, valid_until=None, now=NOW)
            self.assertEqual(json.loads(target.read_bytes())['schemaVersion'], '2.0')
            publish_external_collection([], target, expected_previous_digest=result['sha256'],
                published_at=None, valid_until=None, now='2027-10-01T11:00:00Z')
            self.assertEqual(target.read_bytes(), empty)

    def test_minimized_profile_and_no_private_identifiers(self):
        bundle, selected, *_ = fixture()
        result = build_external_projection(**entry(bundle, selected), now=NOW)
        self.assertEqual(result['scientificContext']['qualityState'], 'UNKNOWN')
        self.assertEqual(result['scientificContext']['metadataState'], 'PARTIAL')
        self.assertEqual(result['preview'], {k:v for k,v in selected['preview'].items() if k != 'sha256'})
        raw = encode(result)
        for secret in ('SYNTHETIC_APPROVER', 'Synthetic Subject', 'Synthetic Telescope',
                       bundle['journalHeadSha256'], bundle['packetSha256'], bundle['acquisitionId'],
                       bundle['result']['original']['sha256'], bundle['result']['preview']['sha256']):
            self.assertNotIn(secret.encode(), raw)

    def test_existing_registration_is_not_publication_approval(self):
        bundle, selected, *_ = fixture()
        for change in (dict(rightsConfirmed=False), dict(scope='REGISTER_EXACT_EXTERNAL_ASSETS'),
                       dict(kind='DSG_EXTERNAL_OWNER_DECISION_V1'), dict(privateExtra='unapproved')):
            with self.subTest(change=change), self.assertRaises(ArchiveError):
                build_external_projection(**entry(bundle, {**selected, **change}), now=NOW)

    def test_exact_preview_delivery_selection_and_current_authority_required(self):
        bundle, selected, parts, events = fixture()
        for key in ('current_head', 'current_selection_digest', 'delivery_digest', 'selection_digest'):
            args = entry(bundle, selected); args[key] = '0' * 64
            with self.subTest(key=key), self.assertRaises(ArchiveError):
                build_external_projection(**args, now=NOW)
        changed = deepcopy(selected); changed['preview']['sha256'] = '0' * 64
        with self.assertRaises(ArchiveError):
            build_external_projection(**entry(bundle, changed), now=NOW)
        events.append(encode(event_for(events, *parts[:2], 'WITHDRAW')))
        args = entry(bundle, selected); args['current_head'] = digest(events[-1])
        with self.assertRaises(ArchiveError):
            build_external_projection(**args, now=NOW)

    def test_url_boundary_rejects_credentials_queries_and_unreviewed_hosts(self):
        bundle, selected, *_ = fixture()
        for url in ('javascript:alert(1)', 'https://evil.example/a.jpg',
                    'https://storage.googleapis.com@evil.example/b/a.jpg',
                    selected['preview']['url'] + '?token=private', selected['preview']['url'] + '#x',
                    selected['preview']['url'] + '\n', 'https://storage.googleapis.com/bucket/../x.jpg',
                    'https://storage.googleapis.com/bucket/%2e%2e/x.jpg'):
            changed = deepcopy(selected); changed['preview']['url'] = url
            with self.subTest(url=url), self.assertRaises(ArchiveError):
                build_external_projection(**entry(bundle, changed), now=NOW)

    def test_approval_and_release_expiry_cannot_be_extended(self):
        bundle, selected, *_ = fixture()
        for instant in ('2026-10-01T10:59:59Z', END):
            with self.assertRaises(ArchiveError):
                build_external_projection(**entry(bundle, selected), now=instant)
        selected['validUntil'] = '2026-10-03T11:00:00Z'
        with self.assertRaises(ArchiveError):
            build_external_projection(**entry(bundle, selected), now=NOW)
        selected['validUntil'] = END
        with self.assertRaises(ArchiveError):
            build_external_collection([entry(bundle, selected)], published_at=NOW,
                                      valid_until='2026-10-01T13:00:00Z', now=NOW)

    def test_schema_rejects_scientific_promotion_and_private_fields(self):
        schema = json.loads(SCHEMA.read_text())
        for change in (lambda p: p['scientificContext'].update(qualityState='ACCEPTED'),
                       lambda p: p['scientificContext'].update(metadataState='COMPLETE'),
                       lambda p: p.update(privateHash='0' * 64),
                       lambda p: p['preview'].update(sha256='0' * 64)):
            value = projection(); change(value)
            with self.assertRaises(ArchiveError):
                validate_emitted_profile(value, schema)

    def test_closed_steps_and_omissions_preserve_partial_unavailable(self):
        bundle, selected, *_ = fixture()
        selected['steps'] = []
        value = build_external_projection(**entry(bundle, selected), now=NOW)
        self.assertEqual(value['captureCompleteness'], 'UNAVAILABLE')
        self.assertEqual(value['omittedStepCount'], 2)
        selected['steps'] = [dict(stepId='missing', processId='PixelMath', parameters=[])]
        with self.assertRaises(ArchiveError):
            build_external_projection(**entry(bundle, selected), now=NOW)

    def test_collection_duplicates_empty_withdrawal_and_limits(self):
        bundle, selected, *_ = fixture(); item = entry(bundle, selected)
        for entries in ([item, item], [item] * 9):
            with self.assertRaises(ArchiveError):
                build_external_collection(entries, published_at=NOW, valid_until=END, now=NOW)
        empty = build_external_collection([], published_at=None, valid_until=None, now=NOW)
        self.assertEqual(empty['records'], [])
        with self.assertRaises(ArchiveError):
            build_external_collection([], published_at=NOW, valid_until=END, now=NOW)

    def test_local_publisher_stale_predecessor_lock_failure_and_withdrawal(self):
        bundle, selected, *_ = fixture(); item = entry(bundle, selected)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'bkl049-public-workflows.json'
            empty = encode(build_external_collection([], published_at=None, valid_until=None, now=NOW)) + b'\n'
            target.write_bytes(empty)
            args = dict(expected_previous_digest=digest(empty), published_at=NOW, valid_until=END, now=NOW)
            with self.assertRaises(ArchiveError):
                publish_external_collection([item], target, **{**args, 'expected_previous_digest':'0'*64})
            lock = target.with_name('.bkl049-publication.lock'); lock.write_text('held')
            with self.assertRaises(ArchiveError):
                publish_external_collection([item], target, **args)
            lock.unlink()
            with patch('tools.pixinsight.workflow_archive.external_public.os.replace', side_effect=OSError):
                with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_PUBLICATION_IO'):
                    publish_external_collection([item], target, **args)
            self.assertEqual(target.read_bytes(), empty)
            self.assertEqual(list(Path(directory).iterdir()), [target])
            result = publish_external_collection([item], target, **args)
            self.assertEqual(result['outcome'], 'LOCAL_COLLECTION_REPLACED')
            result = publish_external_collection([item], target, **{**args, 'expected_previous_digest':result['sha256']})
            self.assertEqual(result['outcome'], 'DUPLICATE_NOOP')
            publish_external_collection([], target, expected_previous_digest=result['sha256'],
                                        published_at=None, valid_until=None, now=NOW)
            self.assertEqual(target.read_bytes(), empty)


if __name__ == '__main__':
    unittest.main()
