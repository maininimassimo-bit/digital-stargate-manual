"""Synthetic application-port tests: metadata fixtures do not qualify real controls."""
import copy
import datetime as dt
import json
import unittest
from decimal import Decimal, localcontext

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode
from tools.scientific_registry.ingestion_storage import MemoryStore, Conflict
from tools.scientific_transients.confirmatory_campaign import ConfirmatoryCampaigns, fingerprint


def ref(n): return format(n, '032x')
def sha(n): return format(n, '064x')


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.now=dt.datetime(2026,10,15,tzinfo=dt.timezone.utc)
        self.store=MemoryStore();self.jobs={}
        self.service=ConfirmatoryCampaigns(self.store,ref(1),ref(2),ref(3),
                                          lambda key:copy.deepcopy(self.jobs[key]),lambda:self.now)
        self.inputs=[]
        for i in range(59):
            frames=[{'frameRef':ref(1000+3*i+j),'sha256':sha(1000+3*i+j),
                     'exposureRef':ref(2000+3*i+j),'role':'SCIENCE',
                     'acquiredUTC':(self.now-dt.timedelta(days=90-i,seconds=600-10*j)).isoformat(),
                     'metadataSha256':sha(3000+3*i+j),'bandpassSha256':sha(4000),
                     'calibration':'VERIFIED_FOR_DECLARED_MODEL',
                     'uncertainty':'COMPLETE_FOR_DECLARED_MODEL','timeStatus':'ACQUIRED_VERIFIED'} for j in range(3)]
            request={'witnessRef':ref(100+i),'reportSha256':sha(5000+i),
                     'purpose':'CONFIRMATORY_RESERVED_REAL','correlationRef':ref(6000+i),'frames':frames}
            # REAL is protocol-shaped test metadata, not a real observation or scientific assertion.
            self.inputs.append(request);self.service.register_inputs(request)
        self.request={'planRef':ref(10),'algorithmRef':ref(20),'algorithmSha256':sha(20),
                      'contractRef':ref(30),'contractSha256':sha(30),
                      'inputWitnessRefs':[r['witnessRef'] for r in self.inputs],
                      'falsePositiveMaximum':.05,'confidence':.95,'requiredControls':59}
        self.plan=self.service.create(self.request)

    def review(self,i):
        r=self.inputs[i]
        request={'decisionId':ref(7000+i),'witnessSha256':fingerprint(r),
                 'nullReferenceSha256':sha(8000+i),'independenceSha256':sha(9000+i),
                 'modelReviewSha256':sha(10000+i),'separationEvidenceSha256':sha(11000+i),
                 'algorithmSha256':sha(20),'contractSha256':sha(30),
                 'acceptNullReference':True,'acceptIndependence':True,
                 'acceptScienceModel':True,'acceptDevelopmentSeparation':True}
        return self.service.review_input(r['witnessRef'],request)

    def freeze_request(self, plan_ref=None):
        value=self.service.view(plan_ref or ref(10))
        return {'decisionId':ref(12000),'planHeadSha256':value['headSha256'],
                'approveAlgorithm':True,'approveRules':True,
                'expectedInputReviewSha256':value['inputReviewSnapshotSha256'],
                'independenceReviewSha256':sha(12001),'developmentSeparationReviewSha256':sha(12002),
                'approveSampleIndependence':True,'approveDevelopmentSeparation':True}

    def freeze(self):
        for i in range(59):self.review(i)
        request=self.freeze_request()
        self.service.freeze(ref(10),request);self.now+=dt.timedelta(seconds=1)
        return request

    def execution(self,i,outcome='NO_ALERT'):
        r=self.inputs[i];jobs=[]
        for j,f in enumerate(r['frames']):
            jid='TRN_'+ref(13000+3*i+j);attempt=ref(14000+3*i+j);report=sha(15000+3*i+j)
            self.jobs[jid]={'jobId':jid,'attemptId':attempt,'state':'COMPLETED',
                           'binding':{'bindingRef':ref(16000+3*i+j),'inputRef':f['frameRef'],
                                      'algorithmRef':ref(20),'contractRef':ref(30)},
                           'createdAt':self.now.isoformat(),'updatedAt':self.now.isoformat(),
                           'result':{'reportSha256':report,'bindingRef':ref(16000+3*i+j),
                                     'qualityCounts':{'measured':1,'excluded':0,'incomplete':0}}}
            jobs.append({'jobId':jid,'attemptId':attempt,'frameRef':f['frameRef'],
                         'inputSha256':f['sha256'],'reportSha256':report})
        return {'executionRef':ref(17000+i),'planSha256':self.plan['planSha256'],
                'witnessRef':r['witnessRef'],'algorithmSha256':sha(20),'contractSha256':sha(30),
                'scienceEvidenceSha256':sha(18000+i),'pipelineStatus':'COMPLETE_UNDER_FROZEN_RULES',
                'outcome':outcome,'jobs':jobs}

    def completed(self,i,outcome='NO_ALERT'):
        request=self.execution(i,outcome);record=self.service.record_execution(ref(10),request)
        self.service.review_outcome(ref(10),{'decisionId':ref(19000+i),
                    'executionSha256':record['sha256'],'acceptRecordedOutcome':True})
        return request

    def replace_input_for_new_plan(self,index,**changes):
        request=copy.deepcopy(self.inputs[index]);request.update(changes)
        request['witnessRef']=ref(30000+index);self.service.register_inputs(request)
        new=copy.deepcopy(self.request);new['planRef']=ref(11)
        new['inputWitnessRefs'][index]=request['witnessRef'];self.service.create(new)
        return request

    def test_preliminary_or_unreviewed_inputs_cannot_freeze(self):
        self.assertEqual(self.service.view(ref(10))['qualifiedControls'],0)
        with self.assertRaisesRegex(ProtocolError,'FREEZE_BLOCKED'):
            self.service.freeze(ref(10),self.freeze_request())

    def test_59_completed_owner_reviews_produce_conditional_bound_then_final_review(self):
        self.freeze()
        for i in range(59):self.completed(i)
        value=self.service.view(ref(10));self.assertEqual(value['qualifiedControls'],59)
        self.assertEqual(value['status'],'READY_FOR_OWNER_FINAL_REVIEW')
        with localcontext() as context:
            context.prec=50;expected=1-(Decimal('0.05').ln()/59).exp()
        self.assertAlmostEqual(value['statisticalResult']['oneSidedUpperBound'],float(expected),15)
        self.assertLess(value['statisticalResult']['oneSidedUpperBound'],.05)
        self.service.finalize(ref(10),{'decisionId':ref(20000),'planHeadSha256':value['headSha256'],
                                    'acceptDeclaredCampaign':True})
        final=self.service.view(ref(10));self.assertEqual(final['status'],'OWNER_ACCEPTED_CAMPAIGN_SCOPE_ONLY')
        self.assertFalse(final['implicitDispatch']);self.assertEqual(final['publication'],'NONE')

    def test_58_reviewed_controls_do_not_pass_or_disappear(self):
        self.freeze()
        for i in range(58):self.completed(i)
        value=self.service.view(ref(10));self.assertEqual(value['qualifiedControls'],58)
        self.assertIsNone(value['statisticalResult']);self.assertEqual(value['status'],'BLOCKED')

    def test_one_false_alert_fails_zero_event_rule(self):
        self.freeze()
        for i in range(59):self.completed(i,'FALSE_ALERT' if i==58 else 'NO_ALERT')
        value=self.service.view(ref(10));self.assertEqual(value['qualifiedControls'],59)
        self.assertEqual(value['falseAlertRecords'],1);self.assertIsNone(value['statisticalResult'])
        self.assertIn('ZERO_EVENT_CRITERION_FAILED',value['blockers'])

    def test_three_planes_same_exposure_cannot_be_qualified(self):
        r=copy.deepcopy(self.inputs[0]);r['witnessRef']=ref(30000)
        r['frames'][1]['role']='TEMPLATE';r['frames'][2]['role']='DIFFERENCE'
        for f in r['frames']:f['exposureRef']=ref(123)
        self.service.register_inputs(r);self.inputs[0]=r
        with self.assertRaisesRegex(ProtocolError,'INPUT_NOT_ELIGIBLE'):self.review(0)

    def test_missing_uncertainty_or_acquisition_time_not_overridable(self):
        for index,(key,value) in enumerate([('uncertainty','UNKNOWN'),('timeStatus','UNKNOWN'),('acquiredUTC',None)]):
            r=copy.deepcopy(self.inputs[0]);r['witnessRef']=ref(31000+index);r['frames'][0][key]=value
            self.service.register_inputs(r);old=self.inputs[0];self.inputs[0]=r
            with self.assertRaisesRegex(ProtocolError,'INPUT_NOT_ELIGIBLE'):self.review(0)
            self.inputs[0]=old

    def test_development_or_synthetic_not_real_control(self):
        for i,purpose in enumerate(('DEVELOPMENT','SYNTHETIC')):
            r=copy.deepcopy(self.inputs[i]);r['witnessRef']=ref(32000+i);r['purpose']=purpose
            self.service.register_inputs(r);self.inputs[i]=r
            with self.assertRaisesRegex(ProtocolError,'INPUT_NOT_ELIGIBLE'):self.review(i)

    def test_reused_correlation_groups_block_freeze(self):
        r=self.replace_input_for_new_plan(0,correlationRef=self.inputs[1]['correlationRef'])
        self.inputs[0]=r
        for i in range(59):self.review(i)
        p=self.service.view(ref(11));self.assertIn('DEPENDENCY_GROUP_REUSED',p['blockers'])
        with self.assertRaisesRegex(ProtocolError,'FREEZE_BLOCKED'):
            self.service.freeze(ref(11),self.freeze_request(ref(11)))

    def test_development_overlap_blocks_original_reserved_alias(self):
        r=copy.deepcopy(self.inputs[0]);r['witnessRef']=ref(33000);r['purpose']='DEVELOPMENT'
        self.service.register_inputs(r)
        self.assertIn('DEVELOPMENT_INPUT_OVERLAP',self.service.view(ref(10))['blockers'])

    def development_identity_alias(self, identity):
        r=copy.deepcopy(self.inputs[0]);r['witnessRef']=ref(33001);r['purpose']='DEVELOPMENT'
        for j,f in enumerate(r['frames']):
            f['sha256']=sha(50000+j)
            f['frameRef']=ref(51000+j)
            f['exposureRef']=ref(52000+j)
        # Only one stable identity matches; every file hash and other identity differs.
        r['frames'][0][identity]=self.inputs[0]['frames'][0][identity]
        self.service.register_inputs(r)
        for i in range(59):self.review(i)
        self.assertIn('DEVELOPMENT_INPUT_OVERLAP',self.service.view(ref(10))['blockers'])
        with self.assertRaisesRegex(ProtocolError,'FREEZE_BLOCKED'):
            self.service.freeze(ref(10),self.freeze_request())

    def test_changed_hash_development_exposure_identity_blocks_freeze(self):
        self.development_identity_alias('exposureRef')

    def test_changed_hash_development_frame_identity_blocks_freeze(self):
        self.development_identity_alias('frameRef')

    def earlier_campaign_identity_alias(self, identity):
        self.freeze();old=copy.deepcopy(self.inputs)
        original_frozen_utc=self.service.view(ref(10))['frozenUTC']
        for i,r in enumerate(self.inputs):
            r=copy.deepcopy(r);r['witnessRef']=ref(40000+i);r['correlationRef']=ref(41000+i)
            for j,f in enumerate(r['frames']):
                f['sha256']=sha(50000+3*i+j)
                f['frameRef']=ref(51000+3*i+j)
                f['exposureRef']=ref(52000+3*i+j)
            if i==0 and identity is not None:r['frames'][0][identity]=old[0]['frames'][0][identity]
            self.service.register_inputs(r);self.inputs[i]=r;self.review(i)
        request=copy.deepcopy(self.request);request['planRef']=ref(11)
        request['inputWitnessRefs']=[r['witnessRef'] for r in self.inputs]
        self.service.create(request)
        if identity is None:
            self.service.freeze(ref(11),self.freeze_request(ref(11)))
            self.assertEqual(self.service.view(ref(11))['blockers'],['COMPLETE_REVIEWED_SAMPLE_MISSING'])
            self.assertEqual(self.service.view(ref(10))['frozenUTC'],original_frozen_utc)
            self.assertEqual(self.service.view(ref(10))['blockers'],['COMPLETE_REVIEWED_SAMPLE_MISSING'])
            return
        self.assertIn('EARLIER_FROZEN_SAMPLE_REUSED',self.service.view(ref(11))['blockers'])
        with self.assertRaisesRegex(ProtocolError,'FREEZE_BLOCKED'):
            self.service.freeze(ref(11),self.freeze_request(ref(11)))
        self.assertEqual(self.service.view(ref(10))['frozenUTC'],original_frozen_utc)

    def test_changed_hash_earlier_campaign_exposure_identity_blocks_freeze(self):
        self.earlier_campaign_identity_alias('exposureRef')

    def test_changed_hash_earlier_campaign_frame_identity_blocks_freeze(self):
        self.earlier_campaign_identity_alias('frameRef')

    def test_disjoint_second_campaign_freezes_without_invalidating_first_snapshot(self):
        self.earlier_campaign_identity_alias(None)

    def test_later_development_use_does_not_rewrite_frozen_registry_snapshot(self):
        self.freeze();r=copy.deepcopy(self.inputs[0]);r['witnessRef']=ref(33000);r['purpose']='DEVELOPMENT'
        self.service.register_inputs(r)
        self.assertNotIn('DEVELOPMENT_INPUT_OVERLAP',self.service.view(ref(10))['blockers'])

    def test_failed_inconclusive_execution_retained_but_not_success(self):
        self.freeze();r=self.execution(0,'INCONCLUSIVE');r['pipelineStatus']='INCOMPLETE'
        self.jobs[r['jobs'][0]['jobId']]['state']='FAILED'
        record=self.service.record_execution(ref(10),r)
        self.assertFalse(record['technicalCompleted'])
        with self.assertRaisesRegex(ProtocolError,'OUTCOME_INELIGIBLE'):
            self.service.review_outcome(ref(10),{'decisionId':ref(1),'executionSha256':record['sha256'],
                                               'acceptRecordedOutcome':True})
        value=self.service.view(ref(10));self.assertEqual(value['executionRecords'],1)
        self.assertEqual(value['qualifiedControls'],0)

    def test_failed_job_cannot_be_reported_as_no_alert(self):
        self.freeze();r=self.execution(0);self.jobs[r['jobs'][0]['jobId']]['state']='FAILED'
        with self.assertRaisesRegex(ProtocolError,'INCOMPLETE_NOT_SUCCESS'):self.service.record_execution(ref(10),r)
        self.assertEqual(self.service.view(ref(10))['executionRecords'],0)

    def test_pre_freeze_job_and_input_or_algorithm_mismatch_refused(self):
        self.freeze()
        for mode in ('time','input','algorithm','report'):
            r=self.execution(0)
            if mode=='time':self.jobs[r['jobs'][0]['jobId']]['createdAt']=(self.now-dt.timedelta(seconds=1)).isoformat()
            if mode=='input':r['jobs'][0]['inputSha256']=sha(99999)
            if mode=='algorithm':r['algorithmSha256']=sha(99999)
            if mode=='report':r['jobs'][0]['reportSha256']=sha(99999)
            with self.assertRaises(ProtocolError):self.service.record_execution(ref(10),r)

    def test_replay_is_idempotent_conflict_or_second_execution_refused(self):
        self.freeze();r=self.execution(0);first=self.service.record_execution(ref(10),r)
        self.assertEqual(first,self.service.record_execution(ref(10),r))
        r['scienceEvidenceSha256']=sha(99999)
        with self.assertRaisesRegex(ProtocolError,'EXECUTION_CONFLICT'):self.service.record_execution(ref(10),r)
        r['executionRef']=ref(99999)
        with self.assertRaisesRegex(ProtocolError,'ALREADY_RECORDED'):self.service.record_execution(ref(10),r)

    def test_current_head_required_and_revocation_preserves_history(self):
        self.freeze();self.completed(0);value=self.service.view(ref(10))
        r={'decisionId':ref(21000),'planHeadSha256':self.plan['headSha256'],
           'evidenceSha256':sha(21000),'reason':'OWNER_WITHDRAWAL'}
        with self.assertRaisesRegex(ProtocolError,'REVOCATION_HEAD'):self.service.revoke(ref(10),r)
        r['planHeadSha256']=value['headSha256'];self.service.revoke(ref(10),r)
        revoked=self.service.view(ref(10));self.assertEqual(revoked['executionRecords'],1)
        self.assertEqual(revoked['qualifiedControls'],0);self.assertIn('PLAN_REVOKED',revoked['blockers'])

    def test_clock_rollback_and_storage_mutation_or_foreign_owner_refused(self):
        self.now-=dt.timedelta(seconds=1)
        with self.assertRaisesRegex(ProtocolError,'CLOCK_ROLLBACK'):self.service.view(ref(10))
        self.now+=dt.timedelta(seconds=1)
        other=ConfirmatoryCampaigns(self.store,ref(1),ref(2),ref(999),self.jobs.get,lambda:self.now)
        with self.assertRaisesRegex(ProtocolError,'IDENTITY_OR_INTEGRITY'):other.view(ref(10))
        raw,generation=self.store.get(self.service.key);value=decode(raw);value['plans'][0]['revoked']=True
        self.store.put(self.service.key,encode(value),generation)
        with self.assertRaisesRegex(ProtocolError,'IDENTITY_OR_INTEGRITY'):self.service.view(ref(10))

    def test_untrusted_actor_fields_or_unhashable_values_rejected_cleanly(self):
        r=copy.deepcopy(self.inputs[0]);r['actorRef']=ref(3)
        with self.assertRaises(ProtocolError):self.service.register_inputs(r)
        r=copy.deepcopy(self.inputs[0]);r['purpose']=[]
        with self.assertRaises(ProtocolError):self.service.register_inputs(r)
        r=copy.deepcopy(self.request);r['inputWitnessRefs'][0]={}
        with self.assertRaises(ProtocolError):self.service.create(r)

    def test_input_review_for_another_algorithm_cannot_qualify_the_new_plan(self):
        for i in range(59):self.review(i)
        request=copy.deepcopy(self.request);request.update(planRef=ref(11),algorithmSha256=sha(99999))
        self.service.create(request)
        self.assertIn('INPUT_REVIEW_DIFFERENT_ALGORITHM_OR_RULES',self.service.view(ref(11))['blockers'])
        with self.assertRaisesRegex(ProtocolError,'FREEZE_BLOCKED'):
            self.service.freeze(ref(11),self.freeze_request(ref(11)))

    def test_changed_input_review_snapshot_refuses_freeze_without_state_mutation(self):
        for i in range(59):self.review(i)
        request=self.freeze_request();request['expectedInputReviewSha256']=sha(99999)
        before=self.store.get(self.service.key)
        with self.assertRaisesRegex(ProtocolError,'FREEZE_BLOCKED'):self.service.freeze(ref(10),request)
        self.assertEqual(before,self.store.get(self.service.key))

    def test_lost_metadata_ack_is_reconciled_idempotently_without_job_replay(self):
        for i in range(59):self.review(i)
        request=self.freeze_request();original=self.store.put;failed=[False]
        def lost_ack(*args,**kwargs):
            result=original(*args,**kwargs)
            if not failed[0]:failed[0]=True;raise OSError('SYNTHETIC_LOST_ACK')
            return result
        self.store.put=lost_ack
        with self.assertRaises(OSError):self.service.freeze(ref(10),request)
        self.store.put=original;receipt=self.service.freeze(ref(10),request)
        self.assertEqual(receipt['kind'],'FREEZE')
        state,_=self.service._read();self.assertEqual(sum(e['kind']=='FREEZE' for e in state['plans'][0]['events']),1)
        self.assertEqual(self.jobs,{})

    def test_cas_conflict_retries_only_the_metadata_transaction(self):
        for i in range(59):self.review(i)
        request=self.freeze_request();original=self.store.put;failed=[False]
        def conflict(*args,**kwargs):
            if not failed[0]:failed[0]=True;raise Conflict('SYNTHETIC_CAS_CONFLICT')
            return original(*args,**kwargs)
        self.store.put=conflict;self.service.freeze(ref(10),request);self.store.put=original
        state,_=self.service._read();self.assertEqual(sum(e['kind']=='FREEZE' for e in state['plans'][0]['events']),1)
        self.assertEqual(self.jobs,{})

    def test_state_is_separate_and_no_job_dispatch_interface(self):
        self.assertNotIn('control/transient-analysis-state-v1.json',self.store.items)
        self.assertFalse(hasattr(self.service,'dispatch'));self.assertFalse(hasattr(self.service,'launch'))
        self.assertEqual(len(self.jobs),0)


if __name__=='__main__':unittest.main()
