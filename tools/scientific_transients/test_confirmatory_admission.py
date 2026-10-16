"""Synthetic CAS admission tests, not a queue/native runner or scientific trial."""
import copy
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError,decode
from tools.scientific_registry.ingestion_storage import Conflict
from tools.scientific_transients import test_confirmatory_campaign as fixtures
ref,sha=fixtures.ref,fixtures.sha

class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.CampaignTests();self.f.setUp();self.f.freeze();self.s=self.f.service
        self.request=self.intent_request(0)
        self.intent=self.s.prepare_dispatch(ref(10),self.request)

    def intent_request(self,case):
        context=self.s.dispatch_context(ref(10),ref(100+case))
        jobs=[{'requestId':ref(60000+case*3+i),'binding':{'bindingRef':ref(61000+case*3+i),
            'inputRef':f['frameRef'],'referenceRef':ref(62000),'algorithmRef':ref(20),'contractRef':ref(30)}}
            for i,f in enumerate(context['frames'])]
        return {'decisionId':ref(63000+case),'contextSha256':context['contextSha256'],
            'witnessRef':ref(100+case),'jobs':jobs,'workerId':ref(2),'rootId':ref(64000),'archiveSha256':sha(65000+case)}

    def admission_request(self,ordinal=0):
        return {'decisionId':ref(66000+ordinal),'dispatchIntentSha256':self.intent['sha256'],
            'ordinal':ordinal,'workerId':ref(2),'rootId':ref(64000)}

    def admit(self,ordinal=0):return self.s.admit_frame(ref(10),self.admission_request(ordinal))['admission']

    def closure(self,admission,state='COMPLETED'):
        ordinal=admission['request']['ordinal'];binding=self.request['jobs'][ordinal]['binding']
        result={'reportSha256':sha(67000+ordinal),'bindingRef':binding['bindingRef'],
            'qualityCounts':{'incomplete':0,'measured':1}}
        job={'jobId':admission['facts']['jobId'],'attemptId':ref(68000+ordinal),'rootId':ref(64000),
            'binding':copy.deepcopy(binding),'state':state,'result':result if state=='COMPLETED' else None,
            'createdAt':self.f.now.isoformat(),'updatedAt':self.f.now.isoformat()}
        self.f.jobs[job['jobId']]=job
        return {'decisionId':ref(69000+ordinal),'admissionSha256':admission['sha256'],'jobId':job['jobId'],
            'attemptId':job['attemptId'],'reportSha256':None if job['result'] is None else result['reportSha256'],
            'nativeStopEvidenceSha256':sha(70000+ordinal),'technicalState':state,'processStoppedReported':True}

    def revoke(self):
        return self.s.revoke(ref(10),{'decisionId':ref(71000),'planHeadSha256':self.s.view(ref(10))['headSha256'],
            'evidenceSha256':sha(71000),'reason':'OWNER_WITHDRAWAL'})

    def receipt(self):return self.s.dispatch_receipt(ref(10),self.intent['sha256'])

    def test_intent_is_exact_and_has_no_queue_side_effect(self):
        self.assertEqual(self.intent['facts']['context']['contextSha256'],self.request['contextSha256'])
        self.assertFalse(self.intent['facts']['launchAuthorized']);self.assertEqual(self.f.jobs,{})
        self.assertEqual(self.s.prepare_dispatch(ref(10),self.request),self.intent)

    def test_changed_context_is_rejected_before_intent(self):
        request=self.intent_request(1);request['contextSha256']=sha(999)
        with self.assertRaisesRegex(ProtocolError,'CONTEXT_CHANGED'):self.s.prepare_dispatch(ref(10),request)
        self.assertEqual(self.f.jobs,{})

    def test_reordered_triplet_is_rejected(self):
        request=self.intent_request(1);request['jobs'].reverse()
        with self.assertRaisesRegex(ProtocolError,'JOB_BINDING'):self.s.prepare_dispatch(ref(10),request)

    def test_duplicate_case_and_global_request_reuse_are_rejected(self):
        request=copy.deepcopy(self.request);request['decisionId']=ref(72000)
        with self.assertRaisesRegex(ProtocolError,'CASE_ALREADY_PREPARED'):self.s.prepare_dispatch(ref(10),request)
        request=self.intent_request(1)
        for a,b in zip(request['jobs'],self.request['jobs']):a['requestId']=b['requestId']
        with self.assertRaisesRegex(ProtocolError,'REQUEST_REUSED'):self.s.prepare_dispatch(ref(10),request)

    def test_same_admission_ack_lost_returns_no_grant(self):
        self.admit()
        self.assertEqual(self.s.admit_frame(ref(10),self.admission_request()),
            {'disposition':'RECONCILIATION_REQUIRED','admission':None})
        self.assertEqual(len(self.receipt()['admissions']),1)

    def test_new_decision_cannot_readmit_same_frame(self):
        self.admit();request=self.admission_request();request['decisionId']=ref(72000)
        with self.assertRaisesRegex(ProtocolError,'FRAME_ALREADY_ADMITTED'):self.s.admit_frame(ref(10),request)

    def test_frame_order_and_bool_ordinal_rejected(self):
        with self.assertRaisesRegex(ProtocolError,'PREVIOUS_FRAME'):self.admit(1)
        request=self.admission_request();request['ordinal']=False
        with self.assertRaisesRegex(ProtocolError,'START_ADMISSION'):self.s.admit_frame(ref(10),request)

    def test_in_flight_blocks_every_next_frame_and_other_case(self):
        self.admit()
        with self.assertRaisesRegex(ProtocolError,'IN_FLIGHT_OR_UNCERTAIN'):self.admit(1)
        intent=self.s.prepare_dispatch(ref(10),self.intent_request(1));request=self.admission_request()
        request.update(decisionId=ref(73000),dispatchIntentSha256=intent['sha256'])
        with self.assertRaisesRegex(ProtocolError,'IN_FLIGHT_OR_UNCERTAIN'):self.s.admit_frame(ref(10),request)

    def test_closed_completed_frames_allow_only_next_in_order(self):
        for i in range(3):
            admission=self.admit(i);closure=self.closure(admission)
            self.s.close_frame(ref(10),closure)
        receipt=self.receipt();self.assertEqual(len(receipt['closures']),3)
        self.assertEqual(receipt['pendingAdmissionSha256'],[])
        self.assertFalse(receipt['launchAuthorized']);self.assertEqual(self.s.view(ref(10))['qualifiedControls'],0)

    def test_failed_closed_frame_prevents_next_frame(self):
        self.s.close_frame(ref(10),self.closure(self.admit(),'FAILED'))
        with self.assertRaisesRegex(ProtocolError,'PREVIOUS_FRAME'):self.admit(1)

    def test_cancel_requested_is_not_stop_evidence(self):
        admission=self.admit();closure=self.closure(admission)
        self.f.jobs[closure['jobId']].update(state='RUNNING',cancelRequested=True)
        with self.assertRaisesRegex(ProtocolError,'CLOSURE_JOB_MISMATCH'):self.s.close_frame(ref(10),closure)
        self.assertEqual(self.receipt()['pendingAdmissionSha256'],[admission['sha256']])

    def test_false_stop_and_recovery_do_not_close_fence(self):
        closure=self.closure(self.admit());closure['processStoppedReported']=False
        with self.assertRaisesRegex(ProtocolError,'FRAME_CLOSURE'):self.s.close_frame(ref(10),closure)
        closure['processStoppedReported']=True;closure['technicalState']='RECOVERY_REQUIRED'
        with self.assertRaisesRegex(ProtocolError,'FRAME_CLOSURE'):self.s.close_frame(ref(10),closure)

    def test_incomplete_report_is_not_completed_closure(self):
        closure=self.closure(self.admit());self.f.jobs[closure['jobId']]['result']['qualityCounts']['incomplete']=1
        with self.assertRaisesRegex(ProtocolError,'RESULT_INCOMPLETE'):self.s.close_frame(ref(10),closure)

    def test_wrong_root_or_attempt_does_not_close_fence(self):
        closure=self.closure(self.admit());closure['attemptId']=ref(99999)
        with self.assertRaisesRegex(ProtocolError,'CLOSURE_JOB_MISMATCH'):self.s.close_frame(ref(10),closure)

    def test_revocation_before_admission_prevents_grant(self):
        self.revoke()
        with self.assertRaisesRegex(ProtocolError,'CONTEXT_BLOCKED'):self.admit()
        self.assertEqual(self.receipt()['admissions'],[])

    def test_revocation_after_admission_keeps_stop_pending_fence(self):
        admission=self.admit();self.revoke();receipt=self.receipt()
        self.assertTrue(receipt['revoked']);self.assertEqual(receipt['pendingDisposition'],'STOP_PENDING_RECONCILIATION')
        self.assertEqual(receipt['pendingAdmissionSha256'],[admission['sha256']])
        self.assertIsNone(self.s.admit_frame(ref(10),self.admission_request())['admission'])
        self.s.close_frame(ref(10),self.closure(admission))
        self.assertEqual(self.receipt()['pendingAdmissionSha256'],[])
        with self.assertRaisesRegex(ProtocolError,'CONTEXT_BLOCKED'):self.admit(1)

    def test_revocation_wins_in_forced_cas_interleaving(self):
        original=self.f.store.put;fired=[]
        def intercept(key,raw,generation):
            state=decode(raw)
            if not fired and any(e['kind']=='START_ADMISSION' for p in state['plans'] for e in p['events']):
                fired.append(True);self.revoke();raise Conflict('synthetic concurrent revoke')
            return original(key,raw,generation)
        self.f.store.put=intercept
        with self.assertRaisesRegex(ProtocolError,'CONTEXT_BLOCKED'):self.admit()
        self.assertEqual(self.receipt()['admissions'],[]);self.assertEqual(self.f.jobs,{})

    def test_cas_retry_has_one_admission_and_no_external_call(self):
        original=self.f.store.put;fired=[]
        def intercept(key,raw,generation):
            if not fired:fired.append(True);raise Conflict('synthetic conflict')
            return original(key,raw,generation)
        self.f.store.put=intercept
        self.admit();self.assertEqual(len(self.receipt()['admissions']),1);self.assertEqual(self.f.jobs,{})

    def test_closure_cas_retry_reads_job_once_outside_callback(self):
        closure=self.closure(self.admit());original=self.f.store.put;calls=[];fired=[]
        self.s.job_reader=lambda job_id:(calls.append(job_id) or copy.deepcopy(self.f.jobs[job_id]))
        def intercept(key,raw,generation):
            if not fired:fired.append(True);raise Conflict('synthetic conflict')
            return original(key,raw,generation)
        self.f.store.put=intercept
        self.s.close_frame(ref(10),closure);self.assertEqual(len(calls),1)
        self.assertEqual(len(self.receipt()['closures']),1)

    def test_full_59_triplet_event_history_fits_storage_limit(self):
        # Protocol-shaped fixtures only: these are not real observations or
        # native executions and do not increment scientific qualification.
        for case in range(59):
            if case:
                self.request=self.intent_request(case)
                self.intent=self.s.prepare_dispatch(ref(10),self.request)
            for ordinal in range(3):
                index=case*3+ordinal
                request=self.admission_request(ordinal);request['decisionId']=ref(86000+index)
                admission=self.s.admit_frame(ref(10),request)['admission']
                closure=self.closure(admission);closure.update(decisionId=ref(89000+index),attemptId=ref(92000+index))
                self.f.jobs[closure['jobId']]['attemptId']=closure['attemptId']
                self.s.close_frame(ref(10),closure)
        raw,_=self.f.store.get(self.s.key);state=decode(raw)
        self.assertLess(len(raw),8*1024*1024)
        self.assertEqual(len(state['plans'][0]['events']),415)
        self.assertEqual(self.receipt()['pendingAdmissionSha256'],[])
        self.assertEqual(self.s.view(ref(10))['qualifiedControls'],0)

    def test_recovery_requires_exact_owner_closure_and_stays_failed_case(self):
        admission=self.admit();closure=self.closure(admission,'RECOVERY_REQUIRED')
        job=self.f.jobs[closure['jobId']]
        with self.assertRaisesRegex(ProtocolError,'OWNER_RECOVERY_CLOSURE_REQUIRED'):
            self.s.close_frame(ref(10),closure)
        self.assertEqual(self.receipt()['pendingAdmissionSha256'],[admission['sha256']])
        job['recoveryClosure']={'request':{'decisionId':ref(97000),'attemptId':closure['attemptId'],
            'rootId':job['rootId'],'bindingRef':job['binding']['bindingRef'],
            'evidenceSha256':closure['nativeStopEvidenceSha256'],'quiescenceConfirmed':True},
            'recordedAt':self.f.now.isoformat(),'authority':'OWNER_DECLARED'}
        self.s.close_frame(ref(10),closure)
        self.assertEqual(self.receipt()['pendingAdmissionSha256'],[])
        self.assertEqual(self.receipt()['closures'][0]['request']['technicalState'],'RECOVERY_REQUIRED')
        with self.assertRaisesRegex(ProtocolError,'PREVIOUS_FRAME'):self.admit(1)
        other=self.s.prepare_dispatch(ref(10),self.intent_request(1))
        request=self.admission_request();request.update(decisionId=ref(97001),dispatchIntentSha256=other['sha256'])
        self.assertEqual(self.s.admit_frame(ref(10),request)['disposition'],'CREATED')

    def test_recovery_owner_evidence_mismatch_preserves_fence(self):
        admission=self.admit();closure=self.closure(admission,'RECOVERY_REQUIRED');job=self.f.jobs[closure['jobId']]
        job['recoveryClosure']={'request':{'decisionId':ref(97000),'attemptId':closure['attemptId'],
            'rootId':job['rootId'],'bindingRef':job['binding']['bindingRef'],
            'evidenceSha256':sha(99999),'quiescenceConfirmed':True},
            'recordedAt':self.f.now.isoformat(),'authority':'OWNER_DECLARED'}
        with self.assertRaisesRegex(ProtocolError,'RECOVERY_EVIDENCE_MISMATCH'):
            self.s.close_frame(ref(10),closure)
        self.assertEqual(self.receipt()['pendingAdmissionSha256'],[admission['sha256']])

if __name__=='__main__':unittest.main()
