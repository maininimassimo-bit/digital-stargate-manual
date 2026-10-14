"""Synthetic audit cases; no launch, cloud, attestations or scientific acceptance."""
import json
import unittest

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.plan_readiness import assess
from tools.scientific_transients import test_test_plan as fixtures


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.PlanTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)

    def test_draft_controls_and_missing_attempts_never_ready(self):
        value = assess(self.f.plan)
        self.assertEqual(value['status'], 'BLOCKED')
        self.assertEqual(value['qualifiedControls'], 0)
        self.assertEqual(value['confirmatoryEligibleCases'], 0)
        self.assertIsNone(value['statisticalResult'])
        self.assertIn('ATTEMPT_MISSING', value['cases'][0]['blockers'])

    def test_documented_qualification_still_needs_attestation(self):
        self.f.append(data={'state': 'DOCUMENTED_PENDING_REVIEW'}, sources={
            k:self.f.rationale for k in ('NULL_REFERENCE', 'INDEPENDENCE', 'RATIONALE')})
        value = assess(self.f.plan)
        self.assertIn('QUALIFICATION_REVIEW_PENDING', value['cases'][0]['blockers'])
        self.assertIn('INDEPENDENCE_NOT_ATTESTED', value['cases'][0]['blockers'])
        self.assertEqual(value['qualifiedControls'], 0)

    def test_non_evaluable_explicit_and_no_private_data(self):
        self.f.append()
        value = assess(self.f.plan); raw = json.dumps(value)
        self.assertIn('CASE_NON_EVALUABLE', value['cases'][0]['blockers'])
        for item in (str(self.f.root), 'actorRef', 'recordedUTC', 'leaseToken'):
            self.assertNotIn(item, raw)

    def test_modified_plan_evidence_refuses_entire_assessment(self):
        (self.f.plan.directory / 'evidence-00.dat').write_bytes(b'altered')
        with self.assertRaises(ProtocolError): assess(self.f.plan)


class JournalReadinessTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.AttemptLinkTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)

    def test_completed_attempt_rechecked_but_partial_not_confirmatory(self):
        self.f.link(self.f.complete())
        value = assess(self.f.plan, self.f.journal.directory.parent)
        attempt = value['cases'][0]['attempts'][0]
        self.assertEqual(attempt['byteIntegrity'], 'RECHECKED_BYTE_INTEGRITY_ONLY')
        self.assertIn('INPUT_COVERAGE_PARTIAL', attempt['blockers'])
        self.assertIn('CHRONOLOGY_NOT_ATTESTED', attempt['blockers'])
        self.assertFalse(attempt['confirmatoryEligible'])

    def test_original_journal_mutation_after_link_is_detected(self):
        self.f.link(self.f.complete())
        event = self.f.journal._events()[-2]
        (self.f.journal.directory / event['data']['files'][0]['path']).write_bytes(b'changed after link')
        value = assess(self.f.plan, self.f.journal.directory.parent)
        attempt = value['cases'][0]['attempts'][0]
        self.assertEqual(attempt['byteIntegrity'], 'UNAVAILABLE_OR_CHANGED')
        self.assertIn('JOURNAL_UNAVAILABLE_OR_CHANGED', attempt['blockers'])

    def test_no_journal_root_is_explicitly_unverified(self):
        self.f.link(self.f.complete())
        value = assess(self.f.plan)
        self.assertEqual(value['cases'][0]['attempts'][0]['byteIntegrity'], 'NOT_RECHECKED')

    def test_failed_attempt_never_success(self):
        self.f.journal.terminal('FAILED'); self.f.link()
        value = assess(self.f.plan, self.f.journal.directory.parent)
        self.assertIn('TECHNICAL_NOT_COMPLETED', value['cases'][0]['attempts'][0]['blockers'])
        self.assertIsNone(value['statisticalResult'])

    def test_false_alert_and_later_change_keep_review_historical(self):
        self.f.link(self.f.complete())
        head = self.f.plan.view()['cases'][0]['attempts'][0]['journalHeadSha256']
        self.f.append('OUTCOME_REVIEW', {'outcome': 'FALSE_ALERT_DECLARED', 'targetAttemptHeadSha256': head},
                      {'SCIENTIFIC_OUTCOME': self.f.rationale})
        self.f.append('OWNER_REVIEW', {'action':'KEEP_FOR_REVIEW', 'targetHeadSha256':self.f.plan.events()[1]})
        self.f.append()
        value = assess(self.f.plan, self.f.journal.directory.parent)
        self.assertIn('FALSE_ALERT_DECLARED', value['cases'][0]['blockers'])
        self.assertIn('OWNER_REVIEW_HISTORICAL', value['cases'][0]['blockers'])
        self.assertEqual(value['status'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
