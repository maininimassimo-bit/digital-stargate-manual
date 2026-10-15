"""Synthetic campaign capacity; no GCS, OAuth, native work or qualified controls."""
import copy
import datetime as dt
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError, encode, decode
from tools.scientific_registry.ingestion_storage import MemoryStore, BackedUpStore, Conflict
from tools.scientific_transients.queue import (
    TransientQueue, STATE_KEY, CAMPAIGN_PROFILE, CAMPAIGN_LIMIT)

WORKER, ROOT, REF = 'a'*32, 'b'*32, 'c'*32


def binding(i):
    return {key:format(10000+i*16+n,'032x') for n,key in enumerate(
        ('bindingRef','inputRef','referenceRef','algorithmRef','contractRef'))}


def campaign(store):
    return TransientQueue(store,WORKER,
        clock=lambda:dt.datetime(2026,10,15,tzinfo=dt.timezone.utc),
        state_ref=REF,capacity_profile=CAMPAIGN_PROFILE)


class CampaignCapacityTests(unittest.TestCase):
    def test_177_distinct_lifecycles_reopen_without_scientific_promotion(self):
        store=MemoryStore();q=campaign(store);attempts=[]
        for i in range(177):
            b=binding(i);q.register(b)
            request={'requestId':format(1000+i,'032x'),'bindingRef':b['bindingRef']}
            job=q.create(request)
            intent={'workerId':WORKER,'rootId':ROOT,'jobId':job['jobId'],
                    'bindingRef':b['bindingRef'],'reservationRef':format(5000+i,'032x')}
            a=q.reserve_once(intent)['job'];attempts.append(a['attemptId'])
            report={'attemptId':a['attemptId'],'leaseToken':a['leaseToken'],
                    'sequence':1,'stage':'RUNNING','result':None}
            q.report(job['jobId'],report)
            report.update(sequence=2,stage='COMPLETED',result={'reportSha256':'e'*64,
                'bindingRef':b['bindingRef'],'qualityCounts':{'measured':0,'excluded':0,'incomplete':1}})
            q.report(job['jobId'],report)
            q.review(job['jobId'],{'decisionId':format(9000+i,'032x'),
                'reportSha256':'e'*64,'decision':'KEEP_FOR_REVIEW'})
            self.assertEqual(q.create(request)['jobId'],job['jobId'])
            self.assertEqual(q.reserve_once(intent),{'disposition':'RECONCILIATION_REQUIRED','job':None})
        reopened=campaign(store);rows=reopened.status()['jobs']
        self.assertEqual(len(rows),177);self.assertEqual(len(set(attempts)),177)
        self.assertEqual(len({r['jobId'] for r in rows}),177)
        self.assertEqual(len(reopened.options()['bindings']),177)
        self.assertTrue(all(r['state']=='COMPLETED' and len(r['reviews'])==1
            and r['scientificValidation']=='NOT_VALIDATED' and 'leaseToken' not in r for r in rows))
        self.assertNotIn(STATE_KEY,store.items)

    def test_default_and_historical_bytes_and_backups_keep_legacy_capacity(self):
        primary,backup=MemoryStore(),MemoryStore();store=BackedUpStore(primary,backup)
        legacy=TransientQueue(store,WORKER)
        for i in range(32):legacy.register(binding(i))
        for i in range(32):legacy.create({'requestId':format(1000+i,'032x'),
                                        'bindingRef':binding(0)['bindingRef']})
        before=copy.deepcopy((primary.items,backup.items))
        with self.assertRaisesRegex(ProtocolError,'BINDING_CAPACITY'):legacy.register(binding(32))
        with self.assertRaisesRegex(ProtocolError,'JOB_CAPACITY'):
            legacy.create({'requestId':'d'*32,'bindingRef':binding(0)['bindingRef']})
        self.assertEqual((primary.items,backup.items),before)
        self.assertEqual((legacy.capacity,legacy.state_limit),(32,1048576))
        extended=campaign(store);extended.register(binding(40))
        self.assertEqual(primary.items[STATE_KEY],before[0][STATE_KEY])
        self.assertTrue(all(backup.items[k]==value for k,value in before[1].items()))
        self.assertNotIn('capacityProfile',decode(primary.items[STATE_KEY][0]))

    def test_profile_is_explicit_and_requires_isolated_reference(self):
        store=MemoryStore()
        for value in ('','unknown',False,32,{},[]):
            with self.subTest(value=value),self.assertRaisesRegex(ProtocolError,'CAPACITY_PROFILE'):
                TransientQueue(store,WORKER,state_ref=REF,capacity_profile=value)
        with self.assertRaisesRegex(ProtocolError,'ISOLATED_STATE_REQUIRED'):
            TransientQueue(store,WORKER,capacity_profile=CAMPAIGN_PROFILE)
        self.assertEqual(store.items,{})

    def test_extended_recovery_keeps_identity_and_quiescence_guards(self):
        store=MemoryStore();q=campaign(store);jobs=[];intents=[]
        for i in range(2):
            b=binding(i);q.register(b)
            job=q.create({'requestId':format(1000+i,'032x'),'bindingRef':b['bindingRef']});jobs.append(job)
            intents.append({'workerId':WORKER,'rootId':ROOT,'jobId':job['jobId'],
                'bindingRef':b['bindingRef'],'reservationRef':format(5000+i,'032x')})
        a=q.reserve_once(intents[0])['job']
        with self.assertRaisesRegex(ProtocolError,'WORKER_ID'):q.claim({'workerId':'f'*32,'rootId':ROOT})
        with self.assertRaisesRegex(ProtocolError,'ROOT_MISMATCH'):q.claim({'workerId':WORKER,'rootId':'f'*32})
        with self.assertRaisesRegex(ProtocolError,'STALE_WORKER'):
            q.report(a['jobId'],{'attemptId':a['attemptId'],'leaseToken':'f'*64,
                'sequence':1,'stage':'RUNNING','result':None})
        q.cancel(a['jobId'])
        q.report(a['jobId'],{'attemptId':a['attemptId'],'leaseToken':a['leaseToken'],
            'sequence':1,'stage':'RECOVERY_REQUIRED','result':None})
        with self.assertRaisesRegex(ProtocolError,'ATTEMPT_ACTIVE'):q.reserve_once(intents[1])
        closure={'decisionId':'9'*32,'attemptId':a['attemptId'],'rootId':ROOT,
            'bindingRef':binding(0)['bindingRef'],'evidenceSha256':'e'*64,'quiescenceConfirmed':False}
        with self.assertRaises(ProtocolError):q.close_recovery(a['jobId'],closure)
        closure['quiescenceConfirmed']=True;q.close_recovery(a['jobId'],closure)
        self.assertEqual(q.reserve_once(intents[1])['disposition'],'CREATED')
        retained=q.status(a['jobId'])
        self.assertEqual(retained['attemptId'],a['attemptId'])
        self.assertEqual(retained['state'],'RECOVERY_REQUIRED')
        self.assertEqual(retained['recoveryClosure']['authority'],'OWNER_DECLARED')

    def test_extended_conflict_retry_retains_one_immutable_backup(self):
        class OneConflict(MemoryStore):
            armed=True
            def put(self,key,raw,generation=0):
                if self.armed:self.armed=False;raise Conflict('synthetic')
                return super().put(key,raw,generation)
        primary,backup=OneConflict(),MemoryStore();q=campaign(BackedUpStore(primary,backup))
        q.register(binding(0));q.register(binding(0))
        self.assertEqual(primary.serial,1);self.assertEqual(backup.serial,1)
        self.assertEqual(q.options()['bindings'],[binding(0)])

    def test_profile_marker_rejects_adoption_and_downgrade_without_writing(self):
        for extended_first in (False,True):
            store=MemoryStore()
            old=campaign(store) if extended_first else TransientQueue(store,WORKER,state_ref=REF)
            old.register(binding(0));before=copy.deepcopy(store.items)
            other=TransientQueue(store,WORKER,state_ref=REF) if extended_first else campaign(store)
            with self.assertRaisesRegex(ProtocolError,'CAPACITY_STATE_MISMATCH'):other.options()
            self.assertEqual(store.items,before)
        raw,generation=store.get(old.state_key);state=decode(raw);state['capacityProfile']=None
        store.put(old.state_key,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'CAPACITY_STATE_MISMATCH'):
            TransientQueue(store,WORKER,state_ref=REF).options()

    def test_512_readable_and_513_rejected_atomically(self):
        store=MemoryStore();q=campaign(store);q.register(binding(0))
        q.create({'requestId':'d'*32,'bindingRef':binding(0)['bindingRef']})
        raw,generation=store.get(q.state_key);state=decode(raw)
        # Controlled queued-state fixture for the boundary, not 512 executions.
        base=state['jobs'][0];state['bindings']=[binding(i) for i in range(512)];state['jobs']=[]
        for i,b in enumerate(state['bindings']):
            job=copy.deepcopy(base);job['jobId']='TRN_'+format(1000+i,'032x')
            job['request']={'requestId':job['jobId'][4:],'bindingRef':b['bindingRef']};job['binding']=b
            state['jobs'].append(job)
        store.put(q.state_key,encode(state),generation);before=copy.deepcopy(store.items)
        self.assertEqual(len(q.options()['bindings']),512);self.assertEqual(len(q.status()['jobs']),512)
        with self.assertRaisesRegex(ProtocolError,'BINDING_CAPACITY'):q.register(binding(512))
        with self.assertRaisesRegex(ProtocolError,'JOB_CAPACITY'):
            q.create({'requestId':'e'*32,'bindingRef':binding(0)['bindingRef']})
        self.assertEqual(store.items,before)

    def test_byte_limit_rejects_read_and_write_without_new_generation(self):
        store=MemoryStore();q=campaign(store);q.register(binding(0))
        before=copy.deepcopy(store.items)
        with patch.object(q,'state_limit',1):
            with self.assertRaisesRegex(ProtocolError,'STATE_LIMIT'):q.options()
        # Large controlled state, padding is not an allowed public request field.
        def oversized(state,now):state['syntheticPadding']='x'*CAMPAIGN_LIMIT
        with self.assertRaisesRegex(ProtocolError,'STATE_LIMIT'):q._mutate(oversized)
        self.assertEqual(store.items,before)
        _,generation=store.get(q.state_key)
        store.put(q.state_key,b'x'*(CAMPAIGN_LIMIT+1),generation)
        corrupt=store.get(q.state_key)
        with self.assertRaisesRegex(ProtocolError,'STATE_LIMIT'):q.options()
        self.assertEqual(store.get(q.state_key),corrupt)

    def test_512_completed_rows_with_max_reviews_fit_and_remain_readable(self):
        store=MemoryStore();q=campaign(store);b=binding(0);q.register(b)
        job=q.create({'requestId':'d'*32,'bindingRef':b['bindingRef']})
        a=q.reserve_once({'workerId':WORKER,'rootId':ROOT,'jobId':job['jobId'],
            'bindingRef':b['bindingRef'],'reservationRef':'8'*32})['job']
        report={'attemptId':a['attemptId'],'leaseToken':a['leaseToken'],
            'sequence':1,'stage':'RUNNING','result':None};q.report(job['jobId'],report)
        report.update(sequence=2,stage='COMPLETED',result={'reportSha256':'e'*64,
            'bindingRef':b['bindingRef'],'qualityCounts':dict.fromkeys(('measured','excluded','incomplete'),10000000)})
        q.report(job['jobId'],report)
        for i in range(32):q.review(job['jobId'],{'decisionId':format(9000+i,'032x'),
            'reportSha256':'e'*64,'decision':'REJECT_CANDIDATE'})
        raw,generation=store.get(q.state_key);state=decode(raw);base=state['jobs'][0]
        # Maximum-shape snapshot fixture, not a claim of 512 executed jobs.
        state['bindings']=[binding(i) for i in range(512)];state['jobs']=[]
        for i,b in enumerate(state['bindings']):
            j=copy.deepcopy(base);j['jobId']='TRN_'+format(1000+i,'032x');j['binding']=b
            j['request']={'requestId':j['jobId'][4:],'bindingRef':b['bindingRef']}
            j['attemptId']=format(5000+i,'032x');j['leaseToken']=format(6000+i,'064x')
            j['result']['bindingRef']=b['bindingRef']
            j['lastEvent'].update(attemptId=j['attemptId'],leaseToken=j['leaseToken'])
            j['lastEvent']['result']['bindingRef']=b['bindingRef']
            j['reservationIntent'].update(jobId=j['jobId'],bindingRef=b['bindingRef'],reservationRef=format(7000+i,'032x'))
            state['jobs'].append(j)
        raw=encode(state);self.assertGreater(len(raw),1048576);self.assertLess(len(raw),CAMPAIGN_LIMIT)
        store.put(q.state_key,raw,generation);rows=campaign(store).status()['jobs']
        self.assertEqual(len(rows),512)
        self.assertTrue(all(len(j['reviews'])==32 and 'leaseToken' not in j and 'lastEvent' not in j for j in rows))

    def test_trusted_deployment_profile_does_not_activate_service(self):
        path=Path(__file__).resolve().parents[2]/'infrastructure/pixinsight-pilot/app.py'
        spec=importlib.util.spec_from_file_location('capacity_candidate',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        env={'DSG_TRANSIENT_CAPACITY_PROFILE':CAMPAIGN_PROFILE,'DSG_TRANSIENT_STATE_REF':REF}
        store=MemoryStore()
        with patch.dict(os.environ,env,clear=True):
            self.assertEqual(module.transient_component(store,'1'*32,'2'*64),(None,None))
        env.update(DSG_TRANSIENT_ACTIVATION='OWNER_AUTHORIZED',DSG_TRANSIENT_WORKER_ID=WORKER,
                   DSG_TRANSIENT_WORKER_SHA256='f'*64)
        with patch.dict(os.environ,env,clear=True):
            q,_=module.transient_component(store,'1'*32,'2'*64)
            self.assertEqual((q.capacity,q.state_limit),(512,CAMPAIGN_LIMIT))
        self.assertEqual(store.items,{})


if __name__=='__main__':unittest.main()
