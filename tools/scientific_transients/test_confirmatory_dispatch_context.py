"""Synthetic frozen-triplet context tests; no job submission or native execution."""
import copy
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.confirmatory_campaign import fingerprint
from tools.scientific_transients import test_confirmatory_campaign as fixtures
ref=fixtures.ref

class DispatchContextTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.CampaignTests();self.f.setUp();self.service=self.f.service

    def test_frozen_context_binds_exact_triplet_without_mutation(self):
        self.f.freeze();before=self.service.store.get(self.service.key)
        context=self.service.dispatch_context(ref(10),ref(100))
        self.assertEqual(context['contextSha256'],fingerprint({k:v for k,v in context.items() if k!='contextSha256'}))
        self.assertEqual(context['planSha256'],self.f.plan['planSha256'])
        self.assertEqual(context['witnessSha256'],fingerprint(self.f.inputs[0]))
        self.assertEqual(context['frames'],self.f.inputs[0]['frames'])
        self.assertEqual(context['algorithmSha256'],self.f.request['algorithmSha256'])
        self.assertEqual(context['contractSha256'],self.f.request['contractSha256'])
        self.assertFalse(context['launchAuthorized']);self.assertEqual(context['scientificValidation'],'NOT_VALIDATED')
        self.assertEqual(before,self.service.store.get(self.service.key))
        context['frames'][0]['sha256']='f'*64
        self.assertNotEqual(context,self.service.dispatch_context(ref(10),ref(100)))

    def test_unfrozen_plan_rejected(self):
        with self.assertRaisesRegex(ProtocolError,'DISPATCH_CONTEXT_BLOCKED'):
            self.service.dispatch_context(ref(10),ref(100))

    def test_revoked_plan_rejected(self):
        self.f.freeze();head=self.service.view(ref(10))['headSha256']
        self.service.revoke(ref(10),{'decisionId':ref(50000),'planHeadSha256':head,'evidenceSha256':'e'*64,'reason':'OWNER_WITHDRAWAL'})
        with self.assertRaisesRegex(ProtocolError,'DISPATCH_CONTEXT_BLOCKED'):
            self.service.dispatch_context(ref(10),ref(100))

    def test_nonselected_witness_rejected(self):
        self.f.freeze()
        with self.assertRaisesRegex(ProtocolError,'DISPATCH_CONTEXT_WITNESS'):
            self.service.dispatch_context(ref(10),ref(99999))

    def test_recorded_case_cannot_prepare_replacement(self):
        self.f.freeze();self.service.record_execution(ref(10),self.f.execution(0))
        with self.assertRaisesRegex(ProtocolError,'DISPATCH_CONTEXT_ALREADY_EXECUTED'):
            self.service.dispatch_context(ref(10),ref(100))

    def test_other_case_record_does_not_change_frozen_context(self):
        self.f.freeze();context=self.service.dispatch_context(ref(10),ref(100))
        self.service.record_execution(ref(10),self.f.execution(1))
        self.assertEqual(context,self.service.dispatch_context(ref(10),ref(100)))

if __name__=='__main__':unittest.main()
