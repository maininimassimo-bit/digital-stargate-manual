"""Synthetic queue-terminal fencing; never an assertion of native OS stop."""
import copy
import datetime as dt
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError,decode,encode
from tools.scientific_registry.ingestion_storage import Conflict
from tools.scientific_transients.confirmatory_campaign import ConfirmatoryCampaigns
from tools.scientific_transients.queue import TransientQueue,CAMPAIGN_PROFILE
from tools.scientific_transients.campaign_queue import CampaignQueue
from tools.scientific_transients import test_campaign_queue as fixtures
from tools.scientific_transients import test_confirmatory_admission as old_fixtures
ref,sha=fixtures.ref,fixtures.sha

class UnreservedTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.CampaignQueueTests();self.f.setUp()
        self.s,self.q,self.bridge=self.f.s,self.f.q,self.f.bridge

    def admit_only(self):
        request=self.f.fixture.admission_request()
        return self.s.admit_frame(ref(10),request,queue_guard=self.bridge._guard)['admission']

    def fence(self):
        self.q.cancel(self.f.job['jobId'])
        context=self.bridge.unreserved_context(ref(10),self.f.intent['sha256'],0)
        return {'decisionId':ref(160000),'admissionSha256':context['admissionSha256'],
            'jobId':context['jobId'],'fenceSnapshotSha256':context['fenceSnapshotSha256'],
            'cancellationEvidenceSha256':sha(160000)}

    def close(self,request):return self.bridge.close_unreserved(ref(10),self.f.intent['sha256'],0,request)

    def test_owner_fence_closes_only_as_not_started(self):
        admission=self.admit_only();request=self.fence();event=self.close(request)
        self.assertEqual(event['kind'],'UNRESERVED_FENCED_CLOSURE')
        self.assertEqual(event['facts']['status'],'NOT_STARTED_FENCED')
        self.assertFalse(event['facts']['nativeStoppedAttested'])
        self.assertEqual(self.f.receipt()['pendingAdmissionSha256'],[])
        self.assertEqual(self.f.receipt()['closures'][0]['request']['admissionSha256'],admission['sha256'])
        view=self.s.view(ref(10));self.assertEqual(view['qualifiedControls'],0);self.assertEqual(view['executionRecords'],0)

    def test_queued_is_not_a_fence(self):
        admission=self.admit_only()
        with self.assertRaisesRegex(ProtocolError,'NOT_FENCED_UNRESERVED'):
            self.bridge.unreserved_context(ref(10),self.f.intent['sha256'],0)
        self.assertEqual(self.f.receipt()['pendingAdmissionSha256'],[admission['sha256']])

    def test_missing_job_does_not_prove_no_pending_commit(self):
        self.admit_only();raw,generation=self.q.store.get(self.q.state_key);state=decode(raw);state['jobs']=[]
        self.q.store.put(self.q.state_key,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'JOB_NOT_FOUND'):
            self.bridge.unreserved_context(ref(10),self.f.intent['sha256'],0)
        self.assertEqual(len(self.f.receipt()['pendingAdmissionSha256']),1)

    def test_real_attempt_rejects_unreserved_even_after_reported_cancel(self):
        job=self.f.reserve()['job'];self.q.cancel(job['jobId'])
        with self.assertRaises(ProtocolError):self.bridge.unreserved_context(ref(10),self.f.intent['sha256'],0)
        self.q.report(job['jobId'],{'attemptId':job['attemptId'],'leaseToken':job['leaseToken'],
            'sequence':1,'stage':'CANCELLED','result':None})
        with self.assertRaises(ProtocolError):self.bridge.unreserved_context(ref(10),self.f.intent['sha256'],0)
        self.assertEqual(len(self.f.receipt()['pendingAdmissionSha256']),1)

    def test_cancel_wins_forced_queue_cas_race_and_old_reserve_never_emits_lease(self):
        admission=self.admit_only();origin=self.bridge._origin(self.f.intent,self.f.intent['facts']['context'],0)
        original=self.q.store.put;fired=[]
        def intercept(key,raw,generation):
            if key==self.q.state_key and not fired:
                fired.append(True);self.f.f.now+=dt.timedelta(seconds=1)
                self.q.cancel(self.f.job['jobId']);raise Conflict('synthetic earlier cancel')
            return original(key,raw,generation)
        self.q.store.put=intercept
        with self.assertRaisesRegex(ProtocolError,'NOT_FRESH'):
            self.q._reserve_campaign_once(self.f.request,origin,admission['sha256'],guard=self.bridge._guard)
        self.q.store.put=original
        self.assertNotIn('attemptId',self.q.status(self.f.job['jobId']))
        event=self.close(self.fence());self.assertEqual(event['facts']['status'],'NOT_STARTED_FENCED')

    def test_cancelled_barrier_before_admission_is_also_stable(self):
        self.q.cancel(self.f.job['jobId']);self.f.f.now+=dt.timedelta(seconds=1)
        with self.assertRaisesRegex(ProtocolError,'NOT_FRESH'):self.f.reserve()
        event=self.close(self.fence());self.assertEqual(event['facts']['status'],'NOT_STARTED_FENCED')

    def test_repeat_close_is_metadata_only_and_new_decision_cannot_close_twice(self):
        self.admit_only();request=self.fence();event=self.close(request)
        self.assertEqual(self.close(request),event)
        changed=copy.deepcopy(request);changed['decisionId']=ref(160001)
        with self.assertRaisesRegex(ProtocolError,'ALREADY_CLOSED'):self.close(changed)
        self.assertEqual(len(self.f.receipt()['closures']),1)
        self.assertFalse(self.f.receipt()['launchAuthorized'])

    def test_wrong_fence_hash_and_job_preserve_admission(self):
        admission=self.admit_only();request=self.fence()
        wrong=copy.deepcopy(request);wrong['fenceSnapshotSha256']=sha(99999)
        with self.assertRaisesRegex(ProtocolError,'UNRESERVED_PROOF'):self.close(wrong)
        wrong=copy.deepcopy(request);wrong['jobId']='TRN_'+ref(99999)
        with self.assertRaisesRegex(ProtocolError,'UNRESERVED_BINDING'):self.close(wrong)
        self.assertEqual(self.f.receipt()['pendingAdmissionSha256'],[admission['sha256']])

    def test_every_attempt_or_lease_field_presence_rejects_even_null(self):
        self.admit_only();self.q.cancel(self.f.job['jobId']);original,_=self.q.store.get(self.q.state_key)
        for key in ('attemptId','rootId','leaseToken','leaseIssuedAt','leaseExpiresAt',
                    'reservationIntent','campaignReservation','lastEvent','recoveryClosure'):
            with self.subTest(key=key):
                state=decode(original);state['jobs'][0][key]=None
                _,generation=self.q.store.get(self.q.state_key);self.q.store.put(self.q.state_key,encode(state),generation)
                with self.assertRaises(ProtocolError):self.bridge.unreserved_context(ref(10),self.f.intent['sha256'],0)
        _,generation=self.q.store.get(self.q.state_key);self.q.store.put(self.q.state_key,original,generation)
        self.assertEqual(len(self.f.receipt()['pendingAdmissionSha256']),1)

    def test_next_frame_of_same_case_stays_blocked_but_new_case_can_proceed(self):
        self.admit_only();self.close(self.fence())
        request=self.f.fixture.admission_request(1)
        with self.assertRaisesRegex(ProtocolError,'PREVIOUS_FRAME'):
            self.s.admit_frame(ref(10),request,queue_guard=self.bridge._guard)
        owner=self.f.fixture.intent_request(1);intent=self.bridge.prepare_dispatch(ref(10),owner)
        for item in owner['jobs']:self.q.register(item['binding'])
        job=self.bridge.project(ref(10),intent['sha256'],0)
        request={'workerId':ref(2),'rootId':owner['rootId'],'jobId':job['jobId'],
            'bindingRef':job['binding']['bindingRef'],'reservationRef':ref(160002)}
        self.assertEqual(self.bridge.admit_and_reserve(ref(10),intent['sha256'],0,request,ref(160003))['disposition'],'CREATED')
        self.assertEqual(self.s.view(ref(10))['qualifiedControls'],0)

    def test_revocation_allows_cleanup_but_no_new_admission(self):
        self.admit_only();request=self.fence();self.f.fixture.revoke();self.close(request)
        self.assertEqual(self.f.receipt()['pendingAdmissionSha256'],[])
        with self.assertRaisesRegex(ProtocolError,'REVOKED'):self.f.reserve()

    def test_queue_snapshot_is_read_once_outside_campaign_cas_retry(self):
        self.admit_only();request=self.fence();original_read=self.q._campaign_fenced_snapshot;reads=[]
        def read(*args,**kwargs):reads.append(True);return original_read(*args,**kwargs)
        self.q._campaign_fenced_snapshot=read;original_put=self.q.store.put;fired=[]
        def put(key,raw,generation):
            if key==self.s.key and not fired:fired.append(True);raise Conflict('synthetic campaign conflict')
            return original_put(key,raw,generation)
        self.q.store.put=put;self.close(request)
        self.assertEqual(len(reads),1);self.assertEqual(len(self.f.receipt()['closures']),1)

    def test_other_queue_key_cannot_prepare_project_admit_or_close(self):
        other=ConfirmatoryCampaigns(self.s.store,ref(1),ref(2),ref(3),lambda _:None,lambda:self.f.f.now)
        q2=TransientQueue(self.s.store,ref(2),lambda:self.f.f.now,state_ref=ref(170000),capacity_profile=CAMPAIGN_PROFILE)
        bridge=CampaignQueue(other,q2);request=self.f.fixture.intent_request(1)
        with self.assertRaisesRegex(ProtocolError,'NAMESPACE_MISMATCH'):bridge.prepare_dispatch(ref(10),request)
        for action in (lambda:bridge.project(ref(10),self.f.intent['sha256'],0),
                       lambda:bridge.admit_and_reserve(ref(10),self.f.intent['sha256'],0,self.f.request,ref(160000)),
                       lambda:bridge.unreserved_context(ref(10),self.f.intent['sha256'],0)):
            with self.assertRaisesRegex(ProtocolError,'NAMESPACE_MISMATCH'):action()
        self.assertEqual(self.f.receipt()['admissions'],[])

    def test_raw_namespace_hash_and_changed_job_reader_are_not_authority(self):
        request=self.f.fixture.intent_request(1)
        with self.assertRaisesRegex(ProtocolError,'TRUSTED_PREPARATION_REQUIRED'):self.s.prepare_dispatch(ref(10),request)
        request['queueNamespaceSha256']=self.bridge.namespace_sha
        with self.assertRaisesRegex(ProtocolError,'TRANSIENT_FIELDS'):self.bridge.prepare_dispatch(ref(10),request)
        with self.assertRaisesRegex(ProtocolError,'NAMESPACE_MISMATCH'):
            self.s.admit_frame(ref(10),self.f.fixture.admission_request())
        reader=self.s.job_reader;self.s.job_reader=lambda _:None
        with self.assertRaisesRegex(ProtocolError,'COMPOSITION_CHANGED'):
            self.bridge.project(ref(10),self.f.intent['sha256'],0)
        self.s.job_reader=reader;self.assertEqual(self.f.receipt()['admissions'],[])

    def test_historical_unbound_intent_is_preserved_without_adoption(self):
        old=old_fixtures.AdmissionTests();old.setUp()
        q=TransientQueue(old.f.store,ref(2),lambda:old.f.now,state_ref=ref(180000),capacity_profile=CAMPAIGN_PROFILE)
        bridge=CampaignQueue(old.s,q)
        with self.assertRaisesRegex(ProtocolError,'NAMESPACE_MISMATCH'):bridge.project(ref(10),old.intent['sha256'],0)
        with self.assertRaisesRegex(ProtocolError,'DECISION_CONFLICT'):bridge.prepare_dispatch(ref(10),old.request)
        receipt=old.s.dispatch_receipt(ref(10),old.intent['sha256'])
        self.assertNotIn('queueNamespaceSha256',receipt['intent']['request']);self.assertIsNone(receipt['queueNamespaceSha256'])

    def test_existing_execution_port_rejects_foreign_queue_before_any_read(self):
        other=ConfirmatoryCampaigns(self.s.store,ref(1),ref(2),ref(3),lambda _:None,lambda:self.f.f.now)
        q2=TransientQueue(self.s.store,ref(2),lambda:self.f.f.now,state_ref=ref(190000),capacity_profile=CAMPAIGN_PROFILE)
        reads=[];original=q2.status
        def reader(job_id):reads.append(job_id);return original(job_id)
        q2.status=reader;CampaignQueue(other,q2)
        with self.assertRaisesRegex(ProtocolError,'NAMESPACE_MISMATCH'):
            other.record_execution(ref(10),self.f.f.execution(0))
        self.assertEqual(reads,[]);self.assertEqual(self.s.view(ref(10))['executionRecords'],0)

    def test_existing_execution_port_requires_exact_owner_intent_jobs(self):
        for case in (0,1):
            with self.subTest(case=case), self.assertRaisesRegex(ProtocolError,'EXECUTION_DISPATCH_BINDING'):
                self.s.record_execution(ref(10),self.f.f.execution(case))
        self.assertEqual(self.s.view(ref(10))['executionRecords'],0)

    def test_frame_closure_rejects_foreign_reader_before_any_queue_read(self):
        admission=self.admit_only();request=self.f.fixture.closure(admission)
        other=ConfirmatoryCampaigns(self.s.store,ref(1),ref(2),ref(3),lambda _:None,lambda:self.f.f.now)
        q2=TransientQueue(self.s.store,ref(2),lambda:self.f.f.now,state_ref=ref(190001),capacity_profile=CAMPAIGN_PROFILE)
        reads=[];original=q2.status
        def reader(job_id):reads.append(job_id);return original(job_id)
        q2.status=reader;bridge=CampaignQueue(other,q2)
        with self.assertRaisesRegex(ProtocolError,'NAMESPACE_MISMATCH'):
            other.close_frame(ref(10),request,queue_guard=bridge._guard)
        self.assertEqual(reads,[]);self.assertEqual(len(self.f.receipt()['pendingAdmissionSha256']),1)

    def _completed_execution_request(self):
        request=self.f.f.execution(0);request['jobs']=[]
        for ordinal,item in enumerate(self.f.owner['jobs']):
            projected=self.bridge.project(ref(10),self.f.intent['sha256'],ordinal)
            reservation={'workerId':ref(2),'rootId':self.f.owner['rootId'],'jobId':projected['jobId'],
                'bindingRef':item['binding']['bindingRef'],'reservationRef':ref(191000+ordinal)}
            job=self.bridge.admit_and_reserve(ref(10),self.f.intent['sha256'],ordinal,reservation,ref(192000+ordinal))['job']
            self.f.report_running(job)
            self.q.report(job['jobId'],{'attemptId':job['attemptId'],'leaseToken':job['leaseToken'],
                'sequence':2,'stage':'COMPLETED','result':{'reportSha256':sha(193000+ordinal),
                'bindingRef':item['binding']['bindingRef'],'qualityCounts':{'measured':1,'excluded':0,'incomplete':0}}})
            request['jobs'].append({'jobId':job['jobId'],'attemptId':job['attemptId'],
                'frameRef':self.f.f.inputs[0]['frames'][ordinal]['frameRef'],
                'inputSha256':self.f.f.inputs[0]['frames'][ordinal]['sha256'],'reportSha256':sha(193000+ordinal)})
            if ordinal==2:
                with self.assertRaisesRegex(ProtocolError,'FRAME_CLOSURE_MISSING'):
                    self.s.record_execution(ref(10),request)
            admission=self.f.receipt()['admissions'][-1]
            self.bridge.close_frame(ref(10),{'decisionId':ref(194000+ordinal),
                'admissionSha256':admission['sha256'],'jobId':job['jobId'],'attemptId':job['attemptId'],
                'reportSha256':sha(193000+ordinal),'nativeStopEvidenceSha256':sha(195000+ordinal),
                'technicalState':'COMPLETED','processStoppedReported':True})
        return request

    def test_bound_execution_requires_all_closures_then_remains_worker_reported(self):
        record=self.s.record_execution(ref(10),self._completed_execution_request())
        self.assertTrue(record['technicalCompleted']);self.assertIsNone(record.get('review'))
        self.assertEqual(record['evidenceOrigin'],'AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED')
        self.assertEqual(self.s.view(ref(10))['qualifiedControls'],0)

    def test_execution_snapshots_read_three_times_outside_cas_and_never_on_repeat(self):
        request=self._completed_execution_request();original_get=self.q.store.get;reads=[]
        def get(key):
            if key==self.q.state_key:reads.append(key)
            return original_get(key)
        self.q.store.get=get;original_put=self.q.store.put;fired=[]
        def put(key,raw,generation):
            if key==self.s.key and not fired:fired.append(True);raise Conflict('synthetic execution CAS conflict')
            return original_put(key,raw,generation)
        self.q.store.put=put
        record=self.s.record_execution(ref(10),request)
        self.assertEqual(len(reads),3);self.assertEqual(len(fired),1)
        reads.clear();self.assertEqual(self.s.record_execution(ref(10),request),record)
        self.assertEqual(reads,[])

    def test_malformed_closure_request_rejected_before_private_snapshot(self):
        reads=[];original=self.q._campaign_fenced_snapshot
        def read(*args,**kwargs):reads.append(True);return original(*args,**kwargs)
        self.q._campaign_fenced_snapshot=read
        for request in (None,[],{}):
            with self.subTest(request=request), self.assertRaisesRegex(ProtocolError,'TRANSIENT_FIELDS'):
                self.close(request)
        self.assertEqual(reads,[])

if __name__=='__main__':unittest.main()
