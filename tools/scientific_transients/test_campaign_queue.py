"""Synthetic guarded queue integration; no HTTP/cloud/native execution."""
import copy
import datetime as dt
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError,decode,encode
from tools.scientific_registry.ingestion_storage import Conflict
from tools.scientific_transients.queue import TransientQueue,CAMPAIGN_PROFILE
from tools.scientific_transients.confirmatory_campaign import ConfirmatoryCampaigns
from tools.scientific_transients.campaign_queue import CampaignQueue
from tools.scientific_transients.reservation_intent import JOB_FIELDS
from tools.scientific_transients import test_confirmatory_admission as fixtures
ref,sha=fixtures.ref,fixtures.sha

class CampaignQueueTests(unittest.TestCase):
    def setUp(self):
        self.fixture=fixtures.AdmissionTests();self.fixture.setUp();self.f=self.fixture.f;self.s=self.fixture.s
        self.q=TransientQueue(self.f.store,ref(2),lambda:self.f.now,state_ref=ref(95000),capacity_profile=CAMPAIGN_PROFILE)
        self.s.job_reader=self.q.status;self.bridge=CampaignQueue(self.s,self.q)
        self.intent=self.fixture.intent;self.owner=self.fixture.request
        for item in self.owner['jobs']:self.q.register(item['binding'])
        self.job=self.bridge.project(ref(10),self.intent['sha256'],0)
        self.request={'workerId':ref(2),'rootId':self.owner['rootId'],'jobId':self.job['jobId'],
            'bindingRef':self.job['binding']['bindingRef'],'reservationRef':ref(96000)}

    def reserve(self):
        return self.bridge.admit_and_reserve(ref(10),self.intent['sha256'],0,self.request,ref(96001))

    def receipt(self):return self.s.dispatch_receipt(ref(10),self.intent['sha256'])

    def report_running(self,job):
        self.q.report(job['jobId'],{'attemptId':job['attemptId'],'leaseToken':job['leaseToken'],
            'sequence':1,'stage':'RUNNING','result':None})

    def test_exact_projection_is_private_and_no_admission(self):
        self.assertEqual(self.job['state'],'QUEUED');self.assertNotIn('campaignOrigin',self.job)
        self.assertEqual(self.bridge.project(ref(10),self.intent['sha256'],0),self.job)
        self.assertEqual(self.receipt()['admissions'],[])
        raw,_=self.q.store.get(self.q.state_key);origin=decode(raw)['jobs'][0]['campaignOrigin']
        self.assertEqual(origin['contextSha256'],self.owner['contextSha256'])
        self.assertEqual(origin['intentSha256'],self.intent['sha256'])
        self.assertEqual(origin['namespaceSha256'],self.bridge.namespace_sha)

    def test_untrusted_json_cannot_call_projection_or_reserve(self):
        origin=self.bridge._origin(self.intent,self.intent['facts']['context'],0)
        with self.assertRaisesRegex(ProtocolError,'TRUSTED_COMPOSITION_REQUIRED'):
            self.q._create_campaign(self.job['request'],self.job['binding'],origin,guard={})
        with self.assertRaisesRegex(ProtocolError,'TRUSTED_COMPOSITION_REQUIRED'):
            self.q._reserve_campaign_once(self.request,origin,sha(96002),guard=None)

    def test_legacy_queued_claim_and_selected_reserve_fail_closed(self):
        with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_PROTECTED'):
            self.q.claim({'workerId':ref(2),'rootId':self.owner['rootId']})
        with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_PROTECTED'):self.q.reserve_once(self.request)
        with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_PROTECTED'):self.q.create(self.job['request'])
        self.assertEqual(self.q.status(self.job['jobId'])['state'],'QUEUED')

    def test_fresh_lease_has_unchanged_exact_operator_schema(self):
        response=self.reserve();self.assertEqual(response['disposition'],'CREATED')
        self.assertEqual(set(response['job']),JOB_FIELDS)
        self.assertNotIn('campaignOrigin',response['job']);self.assertNotIn('campaignReservation',response['job'])
        self.assertEqual(len(response['job']['leaseToken']),64)
        self.assertEqual(len(self.receipt()['pendingAdmissionSha256']),1)

    def test_active_legacy_claim_never_returns_campaign_lease(self):
        job=self.reserve()['job']
        for running in (False,True):
            if running:self.report_running(job)
            with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_PROTECTED'):
                self.q.claim({'workerId':ref(2),'rootId':self.owner['rootId']})
            with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_PROTECTED'):self.q.reserve_once(self.request)

    def test_reads_and_reprojection_never_disclose_lease_or_marker(self):
        job=self.reserve()['job'];self.report_running(job)
        for value in (self.q.status(job['jobId']),self.q.worker_receipt(job['jobId']),
                      self.bridge.project(ref(10),self.intent['sha256'],0)):
            text=str(value)
            self.assertNotIn(job['leaseToken'],text);self.assertNotIn('campaignOrigin',text)
            self.assertNotIn('campaignReservation',text);self.assertNotIn('archiveSha256',text)

    def test_same_admission_and_changed_reservation_do_not_emit_lease(self):
        self.reserve()
        self.assertEqual(self.reserve(),{'disposition':'RECONCILIATION_REQUIRED','job':None})
        self.request['reservationRef']=ref(96003)
        self.assertEqual(self.reserve(),{'disposition':'RECONCILIATION_REQUIRED','job':None})
        self.assertEqual(len(self.receipt()['admissions']),1)

    def test_wrong_root_or_job_rejected_before_admission(self):
        for key,value in [('rootId',ref(99999)),('jobId','TRN_'+ref(99999)),('bindingRef',ref(99999))]:
            request=copy.deepcopy(self.request);request[key]=value
            with self.assertRaisesRegex(ProtocolError,'RESERVATION_BINDING'):
                self.bridge.admit_and_reserve(ref(10),self.intent['sha256'],0,request,ref(96001))
        self.assertEqual(self.receipt()['admissions'],[])

    def test_revocation_prevents_new_admission(self):
        self.fixture.revoke()
        with self.assertRaisesRegex(ProtocolError,'REVOKED'):self.reserve()
        self.assertEqual(self.receipt()['admissions'],[])

    def test_queue_write_failure_retains_consumed_fence_and_no_replay(self):
        original=self.q.store.put
        def fail(key,raw,generation):
            if key==self.q.state_key:raise OSError('synthetic lost queue storage')
            return original(key,raw,generation)
        self.q.store.put=fail
        with self.assertRaises(OSError):self.reserve()
        self.q.store.put=original
        self.assertEqual(len(self.receipt()['pendingAdmissionSha256']),1)
        self.assertEqual(self.q.status(self.job['jobId'])['state'],'QUEUED')
        self.assertEqual(self.reserve(),{'disposition':'RECONCILIATION_REQUIRED','job':None})

    def test_lost_queue_ack_retains_attempt_and_never_recovers_lease(self):
        original=self.q.store.put
        def commit_then_fail(key,raw,generation):
            result=original(key,raw,generation)
            if key==self.q.state_key:raise OSError('synthetic lost acknowledgement')
            return result
        self.q.store.put=commit_then_fail
        with self.assertRaises(OSError):self.reserve()
        self.q.store.put=original
        self.assertEqual(self.q.status(self.job['jobId'])['state'],'RESERVED')
        self.assertEqual(self.reserve(),{'disposition':'RECONCILIATION_REQUIRED','job':None})
        self.assertNotIn('leaseToken',str(self.q.worker_receipt(self.job['jobId'])))

    def test_forced_queue_cas_conflict_emits_exactly_one_lease(self):
        admission=self.s.admit_frame(ref(10),self.fixture.admission_request())['admission']
        origin=self.bridge._origin(self.intent,self.intent['facts']['context'],0)
        original=self.q.store.put;fired=[];winner=[]
        def intercept(key,raw,generation):
            if key==self.q.state_key and not fired:
                fired.append(True)
                winner.append(self.q._reserve_campaign_once(self.request,origin,admission['sha256'],guard=self.bridge._guard))
                raise Conflict('synthetic concurrent winner')
            return original(key,raw,generation)
        self.q.store.put=intercept
        loser=self.q._reserve_campaign_once(self.request,origin,admission['sha256'],guard=self.bridge._guard)
        self.assertEqual(loser,{'disposition':'RECONCILIATION_REQUIRED','job':None})
        self.assertEqual(winner[0]['disposition'],'CREATED')
        self.assertEqual(self.q.worker_receipt(self.job['jobId'])['attemptId'],winner[0]['job']['attemptId'])

    def test_foreign_namespace_origin_is_not_adopted(self):
        other=ConfirmatoryCampaigns(self.f.store,ref(98000),ref(2),ref(3),self.q.status,lambda:self.f.now)
        raw,_=self.f.store.get(self.s.key);self.f.store.put(other.key,raw,0)
        q2=TransientQueue(self.f.store,ref(2),lambda:self.f.now,state_ref=ref(95000),capacity_profile=CAMPAIGN_PROFILE)
        bridge=CampaignQueue(other,q2)
        with self.assertRaisesRegex(ProtocolError,'PROJECTION_CONFLICT'):bridge.project(ref(10),self.intent['sha256'],0)
        with self.assertRaisesRegex(ProtocolError,'ORIGIN_MISMATCH'):
            bridge.admit_and_reserve(ref(10),self.intent['sha256'],0,self.request,ref(96001))

    def test_existing_unmarked_job_is_never_upgraded(self):
        raw,generation=self.q.store.get(self.q.state_key);state=decode(raw)
        del state['jobs'][0]['campaignOrigin'];self.q.store.put(self.q.state_key,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'PROJECTION_CONFLICT'):
            self.bridge.project(ref(10),self.intent['sha256'],0)
        self.assertNotIn('campaignOrigin',decode(self.q.store.get(self.q.state_key)[0])['jobs'][0])

    def test_unknown_or_missing_marker_fails_closed(self):
        self.reserve();raw,generation=self.q.store.get(self.q.state_key);state=decode(raw)
        state['jobs'][0]['campaignOrigin']['protocol']='UNKNOWN'
        self.q.store.put(self.q.state_key,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_ORIGIN'):self.q.status()
        raw,generation=self.q.store.get(self.q.state_key);state=decode(raw);del state['jobs'][0]['campaignOrigin']
        self.q.store.put(self.q.state_key,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'RESERVATION_WITHOUT_ORIGIN'):self.q.status()

    def test_expired_campaign_attempt_and_owner_recovery_never_disclose_lease(self):
        job=self.reserve()['job'];self.f.now+=dt.timedelta(seconds=901)
        with self.assertRaisesRegex(ProtocolError,'CAMPAIGN_PROTECTED'):
            self.q.claim({'workerId':ref(2),'rootId':self.owner['rootId']})
        self.assertEqual(self.q.status(job['jobId'])['state'],'RECOVERY_REQUIRED')
        self.q.close_recovery(job['jobId'],{'decisionId':ref(99000),'attemptId':job['attemptId'],
            'rootId':job['rootId'],'bindingRef':job['binding']['bindingRef'],'evidenceSha256':sha(99000),
            'quiescenceConfirmed':True})
        self.assertEqual(self.q.claim({'workerId':ref(2),'rootId':self.owner['rootId']}),{'job':None})
        self.assertNotIn(job['leaseToken'],str(self.q.status(job['jobId'])))
        self.assertEqual(len(self.receipt()['pendingAdmissionSha256']),1)

    def test_reports_remain_existing_protocol_and_do_not_qualify_science(self):
        job=self.reserve()['job'];self.report_running(job)
        self.q.report(job['jobId'],{'attemptId':job['attemptId'],'leaseToken':job['leaseToken'],
            'sequence':2,'stage':'COMPLETED','result':{'reportSha256':sha(99001),
            'bindingRef':job['binding']['bindingRef'],'qualityCounts':{'measured':1,'excluded':0,'incomplete':0}}})
        self.assertEqual(self.q.status(job['jobId'])['state'],'COMPLETED')
        self.assertEqual(self.s.view(ref(10))['qualifiedControls'],0)
        self.assertEqual(len(self.receipt()['pendingAdmissionSha256']),1)

    def test_full_synthetic_59_triplets_fit_queue_and_campaign_limits(self):
        # These stop/report digests are declared fixtures, never OS evidence.
        for case in range(59):
            owner=self.owner if case==0 else self.fixture.intent_request(case)
            intent=self.intent if case==0 else self.s.prepare_dispatch(ref(10),owner)
            for ordinal,item in enumerate(owner['jobs']):
                index=3*case+ordinal
                self.q.register(item['binding'])
                projected=self.bridge.project(ref(10),intent['sha256'],ordinal)
                request={'workerId':ref(2),'rootId':owner['rootId'],'jobId':projected['jobId'],
                    'bindingRef':item['binding']['bindingRef'],'reservationRef':ref(120000+index)}
                reserved=self.bridge.admit_and_reserve(ref(10),intent['sha256'],ordinal,request,ref(100000+index))
                self.assertEqual(reserved['disposition'],'CREATED');job=reserved['job']
                self.report_running(job)
                self.q.report(job['jobId'],{'attemptId':job['attemptId'],'leaseToken':job['leaseToken'],
                    'sequence':2,'stage':'COMPLETED','result':{'reportSha256':sha(130000+index),
                    'bindingRef':item['binding']['bindingRef'],
                    'qualityCounts':{'measured':1,'excluded':0,'incomplete':0}}})
                receipt=self.s.dispatch_receipt(ref(10),intent['sha256'])
                admission=receipt['admissions'][-1]
                self.s.close_frame(ref(10),{'decisionId':ref(110000+index),'admissionSha256':admission['sha256'],
                    'jobId':job['jobId'],'attemptId':job['attemptId'],'reportSha256':sha(130000+index),
                    'nativeStopEvidenceSha256':sha(140000+index),'technicalState':'COMPLETED',
                    'processStoppedReported':True})
        queue_raw,_=self.q.store.get(self.q.state_key);campaign_raw,_=self.s.store.get(self.s.key)
        self.assertLess(len(queue_raw),8*1024*1024);self.assertLess(len(campaign_raw),8*1024*1024)
        self.assertEqual(len(decode(queue_raw)['jobs']),177)
        self.assertEqual(len(decode(campaign_raw)['plans'][0]['events']),415)
        self.assertEqual(self.s.view(ref(10))['qualifiedControls'],0)

if __name__=='__main__':unittest.main()
