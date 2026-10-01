"""Synthetic end-to-end external admission, revocation and private PXP tests."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from tools.pixinsight.workflow_archive.archive import ArchiveError, digest, encode
from tools.pixinsight.workflow_archive.external_delivery import (
    build_external_delivery, verify_external_delivery, retain_external_delivery, load_external_delivery)
from tools.pixinsight.workflow_archive.provenance import validate_emitted_profile
from tools.pixinsight.workflow_archive.test_provenance import sample
from .external_registry import (PROFILE, FACTS, OPERATIONS, candidate, measurements,
    build_event, replay, load_events, retain_event, export_snapshot)

NOW = '2026-10-01T10:00:00Z'


def fixture():
    packet, declaration = sample()
    facts = {name: dict(value=None, evidenceClass='UNAVAILABLE', evidenceRefs=[],
                       reason='Synthetic unavailable historical evidence') for name in FACTS}
    for name, value in dict(author='Synthetic Author', subject='Synthetic Subject',
                            acquisitionDate='2026-01-02', site='Synthetic External Site',
                            telescope='Synthetic Telescope', camera='Synthetic Camera').items():
        facts[name] = dict(value=value, evidenceClass='DECLARED', evidenceRefs=['SYNTHETIC-DOC'], reason=None)
    def asset(role):
        return dict(imageId='img:synthetic-' + role, objectRef='obj:synthetic-' + role,
                    sha256=digest(role.encode()), byteSize=len(role))
    selected = dict(kind='DSG_EXTERNAL_CANDIDATE_V1', profile=PROFILE,
                    acquisitionId='EXT-SYNTHETIC', revision=1, facts=facts,
                    evidence=[dict(evidenceId='SYNTHETIC-DOC', sha256=digest(b'synthetic document'),
                                   scope='OWNER_DECLARATION')],
                    original=asset('original'), preview=asset('preview'),
                    workflow=dict(packetSha256=digest(encode(packet)), sourceSha256=packet['source']['sha256'],
                                  workflowId='archive:' + packet['receiptId']),
                    metadataState='PARTIAL', qualityState='UNKNOWN')
    measured = dict(kind='DSG_EXTERNAL_MEASUREMENTS_V1', scope='FULL_FILE_BYTES', measuredAtUtc=NOW,
                    items=[deepcopy(selected['original']), deepcopy(selected['preview'])])
    return selected, measured, packet, declaration


def event_for(events, selected, measured, op, **changes):
    head = digest(events[-1]) if events else None
    state = replay(events, head).get(selected['acquisitionId'])
    act = dict(kind='DSG_EXTERNAL_OWNER_DECISION_V1', decisionId='SYNTHETIC-ACT-' + str(len(events) + 1),
               operation=op, authority=OPERATIONS[op][0], scope=OPERATIONS[op][1],
               actor='SYNTHETIC_OPERATOR', decidedAtUtc=NOW, acquisitionId=selected['acquisitionId'],
               candidateSha256=digest(encode(selected)), previousRecordSha256=state['eventSha256'] if state else None,
               measurementSha256=digest(encode(measured)) if op == 'REGISTER' else None,
               rationale='Synthetic explicit decision only')
    act.update(changes)
    args = {}
    if op == 'REGISTER':
        args = dict(candidate_bytes=encode(selected), candidate_digest=digest(encode(selected)),
                    measurement_bytes=encode(measured), measurement_digest=digest(encode(measured)))
    return build_event(encode(act), digest(encode(act)), sequence=len(events) + 1, previous_digest=head, **args)


def admitted():
    parts = fixture()
    events = []
    for op in ('REGISTER', 'ADMIT'):
        events.append(encode(event_for(events, *parts[:2], op)))
    return parts, events


def delivery(parts, events):
    selected, measured, packet, declaration = parts
    return build_external_delivery(encode(packet), digest(encode(packet)), declaration,
            events=events, current_head=digest(events[-1]), acquisition_id=selected['acquisitionId'],
            measurement_bytes=encode(measured), measurement_digest=digest(encode(measured)), exported_at=NOW)


class ExternalRegistryTests(unittest.TestCase):
    def test_null_history_retains_declared_date_and_separate_quality(self):
        selected, *_ = fixture()
        result = candidate(encode(selected), digest(encode(selected)))
        self.assertIsNone(result['facts']['validFromUtc']['value'])
        self.assertEqual(result['facts']['acquisitionDate']['value'], '2026-01-02')
        self.assertEqual(result['qualityState'], 'UNKNOWN')
        self.assertNotIn('sessionId', result)

    def test_each_required_fact_cannot_be_unknown_or_suggested(self):
        for name in FACTS[:6]:
            for mutation in ('unknown', 'suggested'):
                with self.subTest(name=name, mutation=mutation):
                    selected, *_ = fixture()
                    selected['facts'][name]['evidenceClass'] = 'SUGGESTED' if mutation == 'suggested' else 'UNAVAILABLE'
                    if mutation == 'unknown':
                        selected['facts'][name]['value'] = None
                    with self.assertRaises(ArchiveError):
                        candidate(encode(selected), digest(encode(selected)))

    def test_candidate_closed_fields_provenance_and_states(self):
        mutations = [lambda c: c.update(sessionId='fake'), lambda c: c.update(qualityState='ACCEPTED'),
                     lambda c: c.update(metadataState='COMPLETE'),
                     lambda c: c['facts']['camera'].update(evidenceRefs=[]),
                     lambda c: c['facts']['camera'].update(evidenceRefs=['missing']),
                     lambda c: c['evidence'].append(deepcopy(c['evidence'][0])),
                     lambda c: c['facts']['validFromUtc'].update(reason=None),
                     lambda c: c['facts']['acquisitionDate'].update(value='2026-02-30'),
                     lambda c: c.update(preview=deepcopy(c['original']))]
        for change in mutations:
            with self.subTest(change=change):
                selected, *_ = fixture(); change(selected)
                with self.assertRaises(ArchiveError):
                    candidate(encode(selected), digest(encode(selected)))

    def test_temporal_evidence_no_midnight_conversion_or_invalid_interval(self):
        selected, *_ = fixture()
        for name in ('validFromUtc', 'validToUtc'):
            selected['facts'][name] = dict(value=NOW, evidenceClass='DECLARED',
                                          evidenceRefs=['SYNTHETIC-DOC'], reason=None)
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_VALIDITY_ORDER'):
            candidate(encode(selected), digest(encode(selected)))
        selected['facts']['validToUtc']['value'] = '2026-10-02T10:00:00Z'
        self.assertEqual(candidate(encode(selected), digest(encode(selected)))['facts'], selected['facts'])
        selected['facts']['validFromUtc']['value'] = '2026-10-01'
        with self.assertRaises(ArchiveError):
            candidate(encode(selected), digest(encode(selected)))

    def test_full_bytes_required_not_headers_or_forged_measurement(self):
        for change in (lambda m: m.update(scope='HEADER_ONLY'),
                       lambda m: m['items'][0].update(sha256='0' * 64),
                       lambda m: m['items'].reverse(), lambda m: m['items'].pop()):
            selected, measured, *_ = fixture(); change(measured)
            with self.assertRaises(ArchiveError):
                measurements(encode(measured), digest(encode(measured)), selected)

    def test_register_alone_not_admitted_and_roles_not_interchangeable(self):
        selected, measured, *_ = fixture()
        events = [encode(event_for([], selected, measured, 'REGISTER'))]
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_NOT_ADMITTED'):
            export_snapshot(events, digest(events[-1]), selected['acquisitionId'], exported_at=NOW)
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_DECISION_SCOPE'):
            event_for(events, selected, measured, 'ADMIT', authority='AP-013')
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_DECISION_SOURCE'):
            event_for([], selected, measured, 'REGISTER', candidateSha256='0' * 64)

    def test_admission_without_registration_and_stale_decision_rejected(self):
        selected, measured, *_ = fixture()
        raw = encode(event_for([], selected, measured, 'ADMIT'))
        with self.assertRaises(ArchiveError):
            replay([raw], digest(raw))
        parts, events = admitted()
        raw = encode(event_for(events, *parts[:2], 'WITHDRAW', previousRecordSha256='0' * 64))
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_STALE_RECORD'):
            replay(events + [raw], digest(raw))

    def test_admitted_snapshot_keeps_partial_quality_unknown(self):
        parts, events = admitted()
        snap = export_snapshot(events, digest(events[-1]), parts[0]['acquisitionId'], exported_at=NOW)
        self.assertEqual(snap['metadataState'], 'PARTIAL')
        self.assertEqual(snap['qualityState'], 'UNKNOWN')
        self.assertEqual(snap['admissionState'], 'ADMITTED')
        self.assertNotIn('sessionRef', encode(snap).decode())
        self.assertEqual(snap['candidate'], parts[0])

    def test_withdrawal_quarantine_and_stale_export_fail_closed(self):
        for operation in ('WITHDRAW', 'QUARANTINE'):
            parts, events = admitted(); old_head = digest(events[-1])
            bundle = delivery(parts, events)
            events.append(encode(event_for(events, *parts[:2], operation)))
            with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_NOT_ADMITTED'):
                export_snapshot(events, digest(events[-1]), parts[0]['acquisitionId'], exported_at=NOW)
            with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_DELIVERY_STALE'):
                verify_external_delivery(encode(bundle), digest(encode(bundle)), digest(events[-1]))
            with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_STALE_HEAD'):
                replay(events, old_head)
            raw = encode(event_for(events, *parts[:2], 'ADMIT'))
            with self.assertRaises(ArchiveError):
                replay(events + [raw], digest(raw))

    def test_new_revision_invalidates_admission_requires_new_decision(self):
        parts, events = admitted(); selected, measured = parts[:2]
        selected['revision'] = 2
        selected['facts']['subject']['value'] = 'Revised synthetic subject'
        events.append(encode(event_for(events, selected, measured, 'REGISTER')))
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_NOT_ADMITTED'):
            export_snapshot(events, digest(events[-1]), selected['acquisitionId'], exported_at=NOW)
        events.append(encode(event_for(events, selected, measured, 'ADMIT')))
        self.assertEqual(replay(events, digest(events[-1]))[selected['acquisitionId']]['candidate']['revision'], 2)

    def test_global_identity_collision_and_changed_immutable_bytes_rejected(self):
        for mutation in ('other-record', 'changed-bytes'):
            parts, events = admitted(); selected, measured = parts[:2]
            if mutation == 'other-record':
                selected['acquisitionId'] = 'EXT-OTHER'
            else:
                selected['revision'] = 2
                selected['original']['sha256'] = '0' * 64
                measured['items'][0] = deepcopy(selected['original'])
            raw = encode(event_for(events, selected, measured, 'REGISTER'))
            with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_ID_COLLISION'):
                replay(events + [raw], digest(raw))

    def test_decision_reuse_and_time_reversal(self):
        parts, events = admitted()
        for changes in (dict(decisionId='SYNTHETIC-ACT-1'), dict(decidedAtUtc='2026-09-30T00:00:00Z')):
            raw = encode(event_for(events, *parts[:2], 'WITHDRAW', **changes))
            with self.assertRaises(ArchiveError):
                replay(events + [raw], digest(raw))

    def test_retention_restore_missing_file_tamper_and_concurrent_conflict(self):
        parts, events = admitted()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'journal'; root.mkdir()
            backup = Path(temporary) / 'backup'
            first, second = map(json.loads, events)
            receipt = retain_event(first, root, expected_head=None)
            self.assertEqual(receipt['outcome'], 'CREATED')
            self.assertEqual(retain_event(first, root, expected_head=receipt['sha256'])['outcome'], 'DUPLICATE_NOOP')
            competing = event_for(events[:1], *parts[:2], 'QUARANTINE')
            retain_event(second, root, expected_head=receipt['sha256'])
            with self.assertRaises(ArchiveError):
                retain_event(competing, root, expected_head=receipt['sha256'])
            shutil.copytree(root, backup)
            head = digest(events[-1])
            self.assertEqual(load_events(backup, head), events)
            (backup / '0001.external.json').unlink()
            with self.assertRaises(ArchiveError):
                load_events(backup, head)
            (root / '0002.external.json').write_bytes(events[1] + b' ')
            with self.assertRaises(ArchiveError):
                load_events(root, head)

    def test_private_delivery_rebuild_rejects_forgery_and_legacy_profile(self):
        parts, events = admitted(); before = deepcopy(parts)
        bundle = delivery(parts, events); raw = encode(bundle); head = digest(events[-1])
        self.assertEqual(verify_external_delivery(raw, digest(raw), head), bundle)
        self.assertEqual(parts, before)
        sidecar = bundle['result']['sidecar']
        self.assertEqual(sidecar['capture']['observedStepCount'], 0)
        self.assertEqual(sidecar['capture']['completeness'], 'PARTIAL')
        with self.assertRaises(ArchiveError):
            validate_emitted_profile(sidecar)
        for change in (lambda b: b['result']['snapshot'].update(qualityState='ACCEPTED'),
                       lambda b: b.update(publicationState='PUBLIC'),
                       lambda b: b['result']['sidecar']['observationContext'].update(sessionId='fake')):
            modified = deepcopy(bundle); change(modified)
            with self.assertRaises(ArchiveError):
                verify_external_delivery(encode(modified), digest(encode(modified)), head)

    def test_unrelated_workflow_and_session_alias_fail(self):
        parts, events = admitted()
        parts[3]['sessionId'] = 'FAKE'
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_NO_SESSION_ALIAS'):
            delivery(parts, events)
        parts, events = admitted()
        parts[0]['workflow']['packetSha256'] = '0' * 64
        events = []
        for op in ('REGISTER', 'ADMIT'):
            events.append(encode(event_for(events, *parts[:2], op)))
        with self.assertRaisesRegex(ArchiveError, 'EXTERNAL_WORKFLOW_IDENTITY'):
            delivery(parts, events)

    def test_delivery_immutable_restore_and_independent_anchor(self):
        parts, events = admitted(); bundle = delivery(parts, events); head = digest(events[-1])
        with tempfile.TemporaryDirectory() as temporary:
            receipt = retain_external_delivery(bundle, temporary, head)
            self.assertEqual(retain_external_delivery(bundle, temporary, head)['outcome'], 'DUPLICATE_NOOP')
            result = load_external_delivery(Path(temporary) / receipt['filename'], receipt['sha256'], head)
            self.assertEqual(result, bundle['result'])
            with self.assertRaises(ArchiveError):
                load_external_delivery(Path(temporary) / receipt['filename'], '0' * 64, head)

    def test_source_byte_anchors_duplicates_and_size_are_enforced(self):
        selected, *_ = fixture(); raw = encode(selected)
        with self.assertRaises(ArchiveError):
            candidate(raw, '0' * 64)
        raw = b'{"kind":"one","kind":"two"}'
        with self.assertRaises(ArchiveError):
            candidate(raw, digest(raw))
        raw = b' ' * (256 * 1024 + 1)
        with self.assertRaises(ArchiveError):
            candidate(raw, digest(raw))


if __name__ == '__main__':
    unittest.main()
