"""Synthetic plan lifecycle, exclusive storage and real existing journal verifier."""
import copy
import base64
import hashlib
import datetime as dt
import tempfile
import unittest
from pathlib import Path

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.attempt_journal import read_json
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.test_plan import PlanVersion, validate_draft


def ref(n):
    return format(n, '032x')


def draft():
    return {'schema': 'BKL051_TEST_PLAN_DRAFT_V1', 'planRef': ref(1), 'mode': 'PRELIMINARY_DRAFT',
            'falsePositiveMaximum': .05, 'confidence': .95, 'requiredControls': 59, 'algorithmRef': None,
            'cases': [{'caseRef': ref(2), 'clusterRef': ref(3), 'qualification': 'CANDIDATE',
                       'truth': 'UNVERIFIED', 'execution': 'NOT_RUN',
                       'frames': [{'frameRef': ref(i), 'sha256': format(i, '064x')} for i in (4, 5, 6)]}]}


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.versions = self.root / 'versions'; self.versions.mkdir()
        self.algorithm = self.root / 'algorithm'; self.algorithm.write_bytes(b'synthetic algorithm')
        self.rules = self.root / 'rules'; self.rules.write_bytes(b'synthetic rules, no science acceptance')
        self.rationale = self.root / 'rationale'; self.rationale.write_bytes(b'synthetic declared evidence')
        self.actor = {'actorRef': ref(8), 'recordedUTC': '2026-10-14T00:00:00+00:00'}
        self.plan = PlanVersion.create(self.versions, draft(), self.actor, self.algorithm, self.rules)

    def append(self, kind='QUALIFICATION', data=None, sources=None, head=None):
        return self.plan.append(ref(2), kind, data or {'state': 'NON_EVALUABLE'}, self.actor,
                                sources or {'RATIONALE': self.rationale}, head or self.plan.events()[1])

    def test_freeze_snapshots_bytes_and_keeps_original_draft(self):
        self.assertIsNone(draft()['algorithmRef'])
        value = self.plan.read()
        self.assertEqual(value['draft']['algorithmRef'], fingerprint(self.algorithm)['sha256'])
        self.algorithm.write_bytes(b'changed original')
        self.assertEqual(self.plan.read(), value)
        self.assertEqual(self.plan.view()['qualified'], 0)

    def test_new_version_preserves_predecessor(self):
        before = (self.plan.directory / 'plan.json').read_bytes()
        new = PlanVersion.create(self.versions, draft(), self.actor, self.algorithm, self.rules, self.plan)
        self.assertEqual(new.read()['previous']['sha256'], self.plan.sha)
        self.assertEqual((self.plan.directory / 'plan.json').read_bytes(), before)
        self.assertNotEqual(new.sha, self.plan.sha)

    def test_wrong_hash_and_changed_evidence_block(self):
        with self.assertRaisesRegex(ProtocolError, 'PLAN_CHANGED'):
            PlanVersion(self.plan.directory, 'f' * 64)
        (self.plan.directory / 'evidence-00.dat').write_bytes(b'changed')
        with self.assertRaisesRegex(ProtocolError, 'EVIDENCE_CHANGED'):
            self.plan.view()

    def test_failed_freeze_is_retained(self):
        value = draft(); value['algorithmRef'] = 'f' * 64
        with self.assertRaisesRegex(ProtocolError, 'ALGORITHM_CHANGED'):
            PlanVersion.create(self.versions, value, self.actor, self.algorithm, self.rules)
        self.assertEqual(len(list(self.versions.glob('*/failed.json'))), 1)

    def test_duplicate_frames_and_unknown_fields_rejected(self):
        for change in (lambda v: v.update(path='F:/private'),
                       lambda v: v['cases'][0]['frames'][1].update(sha256=v['cases'][0]['frames'][0]['sha256']),
                       lambda v: v['cases'][0].update(qualification='QUALIFIED'),
                       lambda v: v.update(requiredControls=True)):
            value = draft(); change(value)
            with self.assertRaises(ProtocolError): validate_draft(value)

    def test_documented_evidence_never_counts_as_qualified(self):
        self.append(data={'state': 'DOCUMENTED_PENDING_REVIEW'}, sources={
            k: self.rationale for k in ('NULL_REFERENCE', 'INDEPENDENCE', 'RATIONALE')})
        v = self.plan.view()
        self.assertEqual(v['cases'][0]['qualification'], 'DOCUMENTED_PENDING_REVIEW')
        self.assertEqual(v['qualified'], 0); self.assertIsNone(v['statisticalResult'])

    def test_missing_independence_and_false_qualification_rejected_without_event(self):
        for data in ({'state': 'QUALIFIED'}, {'state': 'DOCUMENTED_PENDING_REVIEW'}):
            with self.assertRaises(ProtocolError): self.append(data=data)
        self.assertEqual(self.plan.events()[0], [])

    def test_stale_head_does_not_overwrite(self):
        self.append()
        with self.assertRaisesRegex(ProtocolError, 'HEAD_CONFLICT'):
            self.append(head=self.plan.sha)
        self.assertEqual(len(self.plan.events()[0]), 1)

    def test_changed_event_evidence_invalidates_view(self):
        self.append()
        (self.plan.directory / 'events' / '0000' / 'evidence-00.dat').write_bytes(b'bad')
        with self.assertRaisesRegex(ProtocolError, 'EVIDENCE_CHANGED'): self.plan.view()

    def test_partial_event_is_not_repaired(self):
        (self.plan.directory / 'events' / '0000').mkdir()
        with self.assertRaises(FileNotFoundError): self.append()
        self.assertFalse((self.plan.directory / 'events' / '0000' / 'event.json').exists())

    def test_outcome_needs_completed_attempt(self):
        with self.assertRaisesRegex(ProtocolError, 'OUTCOME_TARGET'):
            self.append('OUTCOME_REVIEW', {'outcome': 'NO_SIGNAL_DECLARED', 'targetAttemptHeadSha256': '1'*64},
                        {'SCIENTIFIC_OUTCOME': self.rationale})

    def test_owner_review_targets_current_hash_and_does_not_accept_science(self):
        self.append('OWNER_REVIEW', {'action': 'KEEP_FOR_REVIEW', 'targetHeadSha256': self.plan.sha})
        self.assertEqual(self.plan.view()['scienceValidation'], 'NOT_VALIDATED')
        with self.assertRaisesRegex(ProtocolError, 'REVIEW_TARGET'):
            self.append('OWNER_REVIEW', {'action': 'KEEP_FOR_REVIEW', 'targetHeadSha256': self.plan.sha})

    def test_minimised_view_omits_paths_actors_evidence_and_identity(self):
        import json
        self.append(); raw = json.dumps(self.plan.view())
        for token in ('actorRef', 'recordedUTC', 'path', str(self.root), 'identity'):
            self.assertNotIn(token, raw)

    def test_empty_or_malformed_actor_refused(self):
        for actor in ({'actorRef': ref(8), 'recordedUTC': '2026-10-14'},
                      {'actorRef': 'owner', 'recordedUTC': self.actor['recordedUTC']}):
            with self.assertRaises(ProtocolError):
                PlanVersion.create(self.versions, draft(), actor, self.algorithm, self.rules)

    def package(self):
        raw = b'synthetic rationale'
        return {'schema': 'BKL051_PLAN_REVIEW_REQUEST_V1', 'packageRef': ref(20),
                'planSha256': self.plan.sha, 'expectedHeadSha256': self.plan.events()[1], 'caseRef': ref(2),
                'kind': 'QUALIFICATION', 'data': {'state': 'NON_EVALUABLE'}, 'declaration': self.actor,
                'attachments': [{'role': 'RATIONALE', 'sha256': hashlib.sha256(raw).hexdigest(),
                                 'base64': base64.b64encode(raw).decode()}]}

    def test_browser_package_archives_evidence_and_rejects_replay(self):
        inbox = self.root / 'inbox'; inbox.mkdir(); request = self.package()
        self.plan.apply_package(request, inbox)
        self.assertEqual(self.plan.view()['cases'][0]['qualification'], 'NON_EVALUABLE')
        self.assertTrue((inbox / ref(20) / 'receipt.json').exists())
        with self.assertRaises(FileExistsError): self.plan.apply_package(request, inbox)
        self.assertEqual(len(self.plan.events()[0]), 1)

    def test_package_tampered_attachment_and_unknown_roles_rejected(self):
        inbox = self.root / 'inbox'; inbox.mkdir()
        for mutate in (lambda p: p['attachments'][0].update(sha256='f'*64),
                       lambda p: p['attachments'][0].update(base64='not base64!'),
                       lambda p: p['attachments'][0].update(role='QUALIFIED'),
                       lambda p: p.update(kind='ATTEMPT')):
            p = self.package(); mutate(p)
            with self.assertRaises(ProtocolError): self.plan.apply_package(p, inbox)
        self.assertEqual(list(inbox.iterdir()), [])

    def test_stale_package_retains_request_and_failure(self):
        inbox = self.root / 'inbox'; inbox.mkdir(); p = self.package(); self.append()
        with self.assertRaisesRegex(ProtocolError, 'HEAD_CONFLICT'): self.plan.apply_package(p, inbox)
        self.assertTrue((inbox / ref(20) / 'request.json').exists())
        self.assertTrue((inbox / ref(20) / 'failed.json').exists())

    def test_later_event_makes_owner_review_historical(self):
        self.append('OWNER_REVIEW', {'action': 'KEEP_FOR_REVIEW', 'targetHeadSha256': self.plan.sha})
        self.append()
        self.assertEqual(self.plan.view()['cases'][0]['ownerReview'], 'HISTORICAL')


class AttemptLinkTests(unittest.TestCase):
    append = PlanTests.append

    def setUp(self):
        PlanTests.setUp(self)
        from tools.scientific_transients.test_native_supervisor import SupervisorTests
        self.fixture = SupervisorTests(); self.fixture.setUp(); self.addCleanup(self.fixture.doCleanups)
        self.journal = self.fixture.journal
        value = draft(); value['cases'][0]['frames'][0]['sha256'] = next(
            r['sha256'] for r in self.journal.anchor['snapshot'] if r['role'] == 'INPUT')
        algorithm = next(r for r in self.journal.anchor['snapshot'] if r['role'] == 'ALGORITHM')
        self.plan = PlanVersion.create(self.versions, value, self.actor,
                                      self.journal.directory / algorithm['path'], self.rules)

    def complete(self):
        supervisor = self.fixture.supervisor(); supervisor.start()
        self.fixture.native('COMPLETED'); supervisor.tick()
        return read_json(self.journal.directory / 'report.json')[1]

    def link(self, sha=None):
        return self.plan.link_attempt(ref(2), self.journal, sha, self.actor, self.rationale, self.plan.events()[1])

    def test_completed_journal_partial_coverage_does_not_pass_science(self):
        self.link(self.complete())
        v = self.plan.view(); attempt = v['cases'][0]['attempts'][0]
        self.assertEqual(attempt['coverage'], 'PARTIAL')
        self.assertEqual(attempt['technicalState'], 'COMPLETED')
        self.assertEqual(v['qualified'], 0); self.assertIsNone(v['statisticalResult'])
        self.assertEqual(v['cases'][0]['scientificOutcome'], 'NOT_EVALUATED')

    def test_preexisting_journal_is_diagnostic(self):
        sha = self.complete()
        actor = dict(self.actor, recordedUTC=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)).isoformat())
        old = self.plan.read(); algorithm = next(r for r in old['evidence'] if r['role'] == 'ALGORITHM')
        self.plan = PlanVersion.create(self.versions, old['draft'], actor,
                                      self.plan.directory / algorithm['path'], self.rules)
        self.link(sha)
        self.assertEqual(self.plan.view()['cases'][0]['attempts'][0]['chronology'], 'PREEXISTING')

    def test_wrong_report_hash_and_duplicate_attempt_refused(self):
        sha = self.complete()
        with self.assertRaises(ProtocolError): self.link('f'*64)
        self.link(sha)
        with self.assertRaisesRegex(ProtocolError, 'DUPLICATE'): self.link(sha)

    def test_failed_attempt_stays_failure_and_cannot_receive_no_signal(self):
        self.journal.terminal('FAILED'); self.link()
        row = self.plan.view()['cases'][0]
        self.assertEqual(row['attempts'][0]['technicalState'], 'FAILED')
        head = row['attempts'][0]['journalHeadSha256']
        with self.assertRaisesRegex(ProtocolError, 'OUTCOME_TARGET'):
            self.append('OUTCOME_REVIEW', {'outcome': 'NO_SIGNAL_DECLARED', 'targetAttemptHeadSha256': head},
                        {'SCIENTIFIC_OUTCOME': self.rationale})

    def test_changed_checkpoint_blocks_attempt_link(self):
        sha = self.complete()
        event = self.journal._events()[-2]
        (self.journal.directory / event['data']['files'][0]['path']).write_bytes(b'changed')
        with self.assertRaises(ProtocolError): self.link(sha)

    def test_wrong_case_input_and_active_attempt_refused(self):
        with self.assertRaisesRegex(ProtocolError, 'ACTIVE'): self.link()
        sha = self.complete()
        self.plan = PlanVersion.create(self.versions, draft(), self.actor, self.algorithm, self.rules)
        with self.assertRaisesRegex(ProtocolError, 'INPUT_MISMATCH'): self.link(sha)

    def test_scientific_and_owner_declarations_still_not_validation(self):
        self.link(self.complete()); head = self.plan.view()['cases'][0]['attempts'][0]['journalHeadSha256']
        self.append('OUTCOME_REVIEW', {'outcome': 'NO_SIGNAL_DECLARED', 'targetAttemptHeadSha256': head},
                    {'SCIENTIFIC_OUTCOME': self.rationale})
        self.append('OWNER_REVIEW', {'action': 'KEEP_FOR_REVIEW', 'targetHeadSha256': self.plan.events()[1]})
        v = self.plan.view()
        self.assertEqual(v['cases'][0]['scientificOutcome'], 'NO_SIGNAL_DECLARED')
        self.assertEqual(v['qualified'], 0); self.assertIsNone(v['statisticalResult'])


if __name__ == '__main__':
    unittest.main()
