"""Owner recovery declarations: synthetic storage and HTTP only, no native/cloud OAT."""
import concurrent.futures
import datetime as dt
import unittest
from unittest.mock import patch
from tools.scientific_transients import test_queue as fixtures
from tools.scientific_registry.ingestion_storage import Conflict
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.queue import STATE_KEY, LEASE_SECONDS

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.QueueTests();self.f.setUp();self.job=self.f.claim()
        self.f.now+=dt.timedelta(seconds=LEASE_SECONDS)
        self.f.queue.status(self.job['jobId'])
        self.request={'decisionId':'d'*32,'attemptId':self.job['attemptId'],'rootId':self.job['rootId'],
          'bindingRef':self.job['binding']['bindingRef'],'evidenceSha256':'e'*64,'quiescenceConfirmed':True}

    def close(self, changes=None):
        return self.f.queue.close_recovery(self.job['jobId'], {**self.request,**(changes or {})})

    def next_job(self):
        return self.f.queue.create({'requestId':'f'*32,'bindingRef':fixtures.BINDING['bindingRef']})

    def test_closure_preserves_entire_attempt_state_and_prior_evidence(self):
        before=self.f.queue.status(self.job['jobId']);after=self.close()
        closure=after.pop('recoveryClosure');self.assertEqual(before,after)
        self.assertEqual(closure['authority'],'OWNER_DECLARED');self.assertEqual(closure['request'],self.request)
        self.assertEqual(after['state'],'RECOVERY_REQUIRED');self.assertEqual(after['scientificValidation'],'NOT_VALIDATED')
        self.assertNotIn('recoveryClosure',self.f.queue.worker_receipt(self.job['jobId']))

    def test_identical_repeat_returns_same_declaration_without_rewrite(self):
        first=self.close();raw=self.f.primary.get(STATE_KEY)
        self.f.now+=dt.timedelta(seconds=20);self.assertEqual(self.close(),first)
        self.assertEqual(self.f.primary.get(STATE_KEY),raw)
        with self.assertRaises(ProtocolError):self.close({'evidenceSha256':'a'*64})
        with self.assertRaises(ProtocolError):self.close({'decisionId':'a'*32})

    def test_old_attempt_cannot_report_or_reserve_after_closure(self):
        self.close()
        with self.assertRaises(ProtocolError):
            self.f.queue.report(self.job['jobId'],self.f.report(self.job,'RECOVERY_REQUIRED'))
        with self.assertRaises(ProtocolError):
            self.f.queue.reserve_once({'workerId':fixtures.WORKER,'rootId':fixtures.ROOT,
              'jobId':self.job['jobId'],'bindingRef':fixtures.BINDING['bindingRef'],'reservationRef':'a'*32})
        next_job=self.next_job()
        fresh=self.f.queue.reserve_once({'workerId':fixtures.WORKER,'rootId':fixtures.ROOT,
              'jobId':next_job['jobId'],'bindingRef':fixtures.BINDING['bindingRef'],'reservationRef':'a'*32})['job']
        self.assertNotEqual(fresh['attemptId'],self.job['attemptId'])
        self.assertEqual(self.f.queue.status(self.job['jobId'])['state'],'RECOVERY_REQUIRED')

    def test_legacy_claim_can_only_get_a_distinct_queued_job(self):
        self.close();next_job=self.next_job()
        self.assertEqual(self.f.queue.claim({'workerId':fixtures.WORKER,'rootId':fixtures.ROOT})['job']['jobId'],next_job['jobId'])

    def test_missing_quiescence_and_wrong_identity_never_close(self):
        raw=self.f.primary.get(STATE_KEY)
        for changes in [{'quiescenceConfirmed':False},{'quiescenceConfirmed':1},{'attemptId':'a'*32},
                        {'rootId':'a'*32},{'bindingRef':'a'*32},{'evidenceSha256':'missing'},{'path':'F:/private'}]:
            with self.assertRaises(ProtocolError):self.close(changes)
        self.assertEqual(raw,self.f.primary.get(STATE_KEY))

    def test_queued_and_live_attempts_cannot_be_closed(self):
        next_job=self.next_job()
        with self.assertRaises(ProtocolError):self.f.queue.close_recovery(next_job['jobId'],self.request)
        self.close();live=self.f.queue.claim({'workerId':fixtures.WORKER,'rootId':fixtures.ROOT})['job']
        with self.assertRaises(ProtocolError):
            self.f.queue.close_recovery(live['jobId'],{**self.request,'attemptId':live['attemptId']})

    def test_decision_reference_cannot_be_reused_for_another_attempt(self):
        self.close();self.next_job();live=self.f.queue.claim({'workerId':fixtures.WORKER,'rootId':fixtures.ROOT})['job']
        self.f.now+=dt.timedelta(seconds=LEASE_SECONDS)
        with self.assertRaises(ProtocolError):
            self.f.queue.close_recovery(live['jobId'],{**self.request,'attemptId':live['attemptId']})
        self.assertNotIn('recoveryClosure',self.f.queue.status(live['jobId']))

    def test_backup_failure_does_not_clear_block(self):
        before=self.f.primary.get(STATE_KEY)
        with patch.object(self.f.backup,'put',side_effect=OSError('synthetic failure')):
            with self.assertRaises(OSError):self.close()
        self.assertEqual(self.f.primary.get(STATE_KEY),before)
        self.next_job()
        self.assertEqual(self.f.queue.claim({'workerId':fixtures.WORKER,'rootId':fixtures.ROOT})['job']['jobId'],self.job['jobId'])

    def test_cas_conflict_retries_without_multiple_declarations(self):
        original=self.f.primary.put;counter=[0]
        def conflict(*args):
            counter[0]+=1
            if counter[0]==1:raise Conflict('synthetic')
            return original(*args)
        with patch.object(self.f.primary,'put',side_effect=conflict):self.close()
        self.assertEqual(counter[0],2)
        self.assertEqual(self.f.queue.status(self.job['jobId'])['recoveryClosure']['request'],self.request)

    def test_corrupt_retained_closure_never_releases_new_claim(self):
        self.close();self.next_job()
        from tools.pixinsight.local_pilot.broker import decode,encode
        raw,generation=self.f.primary.get(STATE_KEY);state=decode(raw)
        state['jobs'][0]['recoveryClosure']['request']['quiescenceConfirmed']=False
        self.f.primary.put(STATE_KEY,encode(state),generation)
        with self.assertRaises(ProtocolError):self.f.queue.claim({'workerId':fixtures.WORKER,'rootId':fixtures.ROOT})

    def test_clock_regression_cannot_record_an_earlier_closure(self):
        self.f.now-=dt.timedelta(seconds=1)
        with self.assertRaises(ProtocolError):self.close()
        self.assertNotIn('recoveryClosure',self.f.queue.status(self.job['jobId']))

    def test_concurrent_identical_declarations_are_one_immutable_record(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(lambda _:self.close(),range(4)))
        self.assertTrue(all(r==results[0] for r in results))

class RecoveryHttpTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.HttpTests();self.f.setUp();self.addCleanup(self.f.tearDown)

    def test_only_owner_origin_can_close_exact_recovery(self):
        f=self.f;base='/v1/transient-analysis'
        f.request(base+'/worker/register',fixtures.BINDING,fixtures.TOKEN)
        _,job=f.request(base+'/jobs',fixtures.REQUEST,'synthetic-owner',True)
        _,claimed=f.request(base+'/worker/claim',{'workerId':fixtures.WORKER,'rootId':fixtures.ROOT},fixtures.TOKEN)
        attempt=claimed['job']
        f.queue.report(job['jobId'],{'attemptId':attempt['attemptId'],'leaseToken':attempt['leaseToken'],
          'sequence':1,'stage':'RECOVERY_REQUIRED','result':None})
        request={'decisionId':'d'*32,'attemptId':attempt['attemptId'],'rootId':fixtures.ROOT,
          'bindingRef':fixtures.BINDING['bindingRef'],'evidenceSha256':'e'*64,'quiescenceConfirmed':True}
        path=base+'/jobs/'+job['jobId']+'/close-recovery'
        for token,origin in [(None,False),(fixtures.TOKEN,False),(fixtures.LEGACY_TOKEN,False),('synthetic-owner',False)]:
            self.assertEqual(f.request(path,request,token,origin)[0],403)
        code,response=f.request(path,request,'synthetic-owner',True)
        self.assertEqual(code,200);self.assertEqual(response['state'],'RECOVERY_REQUIRED')
        self.assertEqual(f.request(path,request,'synthetic-owner',True)[1],response)
        self.assertEqual(f.request(base+'/worker/jobs/'+job['jobId']+'/close-recovery',request,fixtures.TOKEN)[0],404)

if __name__=='__main__':unittest.main()
