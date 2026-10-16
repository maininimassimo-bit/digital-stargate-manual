"""Synthetic metadata/handoff tests; no native start, cloud or Google token."""
import copy
import datetime as dt
import unittest

from tools.pixinsight.local_pilot.broker import ProtocolError, decode, encode
from tools.scientific_transients import campaign_handoff as module
from tools.scientific_transients import test_campaign_queue as fixtures
from tools.scientific_transients import test_campaign_queue_http as http_fixtures
from tools.scientific_transients.campaign_dispatch import CampaignWorkerTransport, BASE


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.CampaignQueueTests();self.f.setUp()
        for ordinal in (1,2):self.f.bridge.project(fixtures.ref(10),self.f.intent['sha256'],ordinal)

    def technical(self,ordinal=0):
        return self.f.bridge.technical_context(fixtures.ref(10),self.f.intent['sha256'],ordinal)

    def handoff(self):
        rows=[self.technical(i) for i in range(3)]
        common={key:rows[0][key] for key in module.COMMON}
        jobs=[{key:row[key] for key in module.JOB} for row in rows]
        return module.make_handoff(common,jobs)

    def test_roundtrip_correlates_three_jobs_but_never_grants_launch(self):
        handoff=self.handoff()
        self.assertEqual(module.validate_handoff(decode(encode(handoff))),handoff)
        calls=[];test=self
        class Transport:
            def request(self,path):
                calls.append(path);return test.technical(int(path.split('/')[-2]))
        result=module.inspect_remote(handoff,Transport())
        self.assertEqual(len(calls),3);self.assertEqual(result['matchedJobs'],3)
        self.assertFalse(result['launchAuthorized'])
        self.assertNotIn('decisionId',str(handoff));self.assertNotIn('leaseToken',str(handoff))
        self.assertNotIn('context',handoff);self.assertNotIn('binding',handoff['jobs'][0])

    def test_forged_self_consistent_file_is_not_server_authority(self):
        handoff=self.handoff();common={key:handoff[key] for key in module.COMMON}
        common['archiveSha256']='f'*64
        forged=module.make_handoff(common,[{key:j[key] for key in module.JOB} for j in handoff['jobs']])
        with self.assertRaisesRegex(ProtocolError,'REMOTE_MISMATCH'):module.compare_technical(forged,self.technical(),0)

    def test_unknown_fields_versions_wrong_order_and_duplicates_are_rejected(self):
        handoff=self.handoff()
        mutations=[lambda h:h.update(token='private'),lambda h:h.update(protocol='unknown'),
            lambda h:h.update(launchAuthorized=True),lambda h:h['jobs'].reverse(),
            lambda h:h['jobs'][0].update(ordinal=True),lambda h:h['jobs'][0].update(path='F:/private'),
            lambda h:h['jobs'][0].update(requestSelectionSha256='f'*64)]
        for mutate in mutations:
            changed=copy.deepcopy(handoff);mutate(changed)
            with self.assertRaises(ProtocolError):module.validate_handoff(changed)
        common={key:handoff[key] for key in module.COMMON};jobs=[{key:j[key] for key in module.JOB} for j in handoff['jobs']]
        jobs[1]['inputSha256']=jobs[0]['inputSha256']
        with self.assertRaisesRegex(ProtocolError,'DUPLICATE'):module.make_handoff(common,jobs)

    def test_read_only_even_after_lease_expiry_does_not_mutate_queue_or_campaign(self):
        self.f.reserve();self.f.f.now+=dt.timedelta(seconds=901)
        before=[self.f.f.store.get(key) for key in (self.f.q.state_key,self.f.s.key)]
        row=self.technical()
        self.assertTrue(row['reservationConsumed']);self.assertEqual(row['projectionState'],'RESERVED')
        self.assertFalse(row['launchAuthorized'])
        self.assertEqual(before,[self.f.f.store.get(key) for key in (self.f.q.state_key,self.f.s.key)])
        self.assertEqual(self.technical(),row)

    def test_consumed_or_cancelled_projection_cannot_be_used_as_fresh_handoff(self):
        handoff=self.handoff();self.f.reserve()
        with self.assertRaisesRegex(ProtocolError,'NOT_FRESH'):module.compare_technical(handoff,self.technical(),0)
        job=self.f.owner['jobs'][1];self.f.q.cancel('TRN_'+job['requestId'])
        with self.assertRaisesRegex(ProtocolError,'NOT_FRESH'):module.compare_technical(handoff,self.technical(1),1)

    def test_admission_without_queue_reservation_already_blocks_freshness(self):
        handoff=self.handoff()
        self.f.s.admit_frame(fixtures.ref(10),self.f.fixture.admission_request(),queue_guard=self.f.bridge._guard)
        row=self.technical();self.assertEqual(row['projectionState'],'QUEUED');self.assertTrue(row['reservationConsumed'])
        with self.assertRaisesRegex(ProtocolError,'NOT_FRESH'):module.compare_technical(handoff,row,0)

    def test_revoked_intent_denied_without_queue_read(self):
        self.f.fixture.revoke();calls=[]
        self.f.q._campaign_technical_snapshot=lambda *a,**k:calls.append(True)
        with self.assertRaisesRegex(ProtocolError,'REVOKED'):self.technical()
        self.assertEqual(calls,[])

    def test_foreign_origin_and_unmarked_generic_job_are_not_adopted(self):
        raw,generation=self.f.f.store.get(self.f.q.state_key);state=decode(raw)
        state['jobs'][0]['campaignOrigin']['namespaceSha256']='f'*64
        self.f.f.store.put(self.f.q.state_key,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'ORIGIN_MISMATCH'):self.technical()
        raw,generation=self.f.f.store.get(self.f.q.state_key);state=decode(raw);del state['jobs'][0]['campaignOrigin']
        self.f.f.store.put(self.f.q.state_key,encode(state),generation)
        with self.assertRaisesRegex(ProtocolError,'PROTECTED_JOB_REQUIRED'):self.technical()

    def test_stale_read_cannot_override_revocation_at_fresh_admission(self):
        handoff=self.handoff();row=self.technical();self.f.fixture.revoke()
        self.assertFalse(module.compare_technical(handoff,row,0)['launchAuthorized'])
        with self.assertRaisesRegex(ProtocolError,'REVOKED'):self.f.reserve()
        self.assertEqual(self.f.q._campaign_technical_snapshot(self.f.job['jobId'],guard=self.f.bridge._guard)['state'],'QUEUED')

    def test_technical_response_has_strict_allowlist_and_rejects_owner_proof(self):
        row=self.technical()
        self.assertEqual(set(row),module.SELECTION|{'protocol','requestSelectionSha256','projectionState',
            'revoked','reservationConsumed','launchAuthorized','scientificValidation'})
        for key in ('leaseToken','ownerRecoveryClosure','admissionSha256','attemptId','decisionId'):
            with self.assertRaises(ProtocolError):module.validate_technical(dict(row,**{key:'f'*64}))


class HandoffHttpTests(unittest.TestCase):
    def setUp(self):
        self.f=http_fixtures.ProtectedCampaignHttpTests();self.f.setUp();self.addCleanup(self.f.doCleanups)

    def path(self):return self.f.path(True,'jobs/0/technical-context')

    def test_separate_owner_worker_reads_and_bounded_worker_transport(self):
        f=self.f
        self.assertEqual(f.request(self.path(),token='synthetic-owner',owner=True)[0],403)
        self.assertEqual(f.request(self.path(),token=http_fixtures.LEGACY_TOKEN)[0],403)
        self.assertEqual(f.request(self.path())[0],403)
        transport=CampaignWorkerTransport('http://127.0.0.1:'+str(f.server.server_port),http_fixtures.TOKEN,test_loopback=True)
        row=transport.request(self.path());self.assertFalse(row['launchAuthorized'])
        self.assertEqual(row,module.validate_technical(row))
        self.assertEqual(f.request(f.path(False,'jobs/0/technical-context'),token='synthetic-owner',owner=True)[0],200)
        self.assertEqual(f.request(self.path(),{},http_fixtures.TOKEN)[0],404)
        with self.assertRaises(ProtocolError):transport.request(self.path(),{})

    def test_disabled_and_invalid_selection_have_no_state_changes(self):
        f=self.f;before=[f.f.f.store.get(k) for k in (f.f.q.state_key,f.f.s.key)]
        self.assertEqual(f.request(f.path(True,'jobs/3/technical-context'),token=http_fixtures.TOKEN)[0],404)
        f.server.RequestHandlerClass=f.handler(False)
        self.assertEqual(f.request(self.path(),token=http_fixtures.TOKEN)[0],404)
        self.assertEqual(before,[f.f.f.store.get(k) for k in (f.f.q.state_key,f.f.s.key)])

    def test_owner_read_is_exact_nonmutating_and_does_not_expire_or_admit(self):
        from unittest.mock import patch
        f=self.f;before=[f.f.f.store.get(k) for k in (f.f.q.state_key,f.f.s.key)]
        path=f.path(False,'jobs/0/technical-context')
        with patch.object(f.f.q,'_mutate',side_effect=AssertionError('read mutated queue')):
            code,row=f.request(path,token='synthetic-owner',owner=True)
        self.assertEqual(code,200);self.assertEqual(row,module.validate_technical(row))
        self.assertEqual(row['jobId'],f.f.job['jobId']);self.assertFalse(row['reservationConsumed'])
        self.assertFalse(row['launchAuthorized']);self.assertEqual(row['projectionState'],'QUEUED')
        self.assertEqual(before,[f.f.f.store.get(k) for k in (f.f.q.state_key,f.f.s.key)])
        self.assertEqual(f.request(path,{},'synthetic-owner',True)[0],404)
        self.assertEqual(f.request(path,token=http_fixtures.TOKEN)[0],403)
        self.assertEqual(f.request(path,token=http_fixtures.LEGACY_TOKEN)[0],403)

    def test_owner_read_reconciles_already_consumed_projection_without_reserving(self):
        f=self.f;job=f.f.reserve()['job']
        before=[f.f.f.store.get(k) for k in (f.f.q.state_key,f.f.s.key)]
        code,row=f.request(f.path(False,'jobs/0/technical-context'),token='synthetic-owner',owner=True)
        self.assertEqual(code,200);self.assertTrue(row['reservationConsumed'])
        self.assertEqual(row['projectionState'],'RESERVED');self.assertFalse(row['launchAuthorized'])
        for key in ('attemptId','leaseToken','admissionSha256'):self.assertNotIn(key,row)
        self.assertNotIn(job['leaseToken'],str(row))
        self.assertEqual(before,[f.f.f.store.get(k) for k in (f.f.q.state_key,f.f.s.key)])

    def test_owner_revoked_or_missing_projection_never_confirms_another_job(self):
        f=self.f;path=f.path(False,'jobs/0/technical-context')
        missing=path.replace(f.intent,'f'*64)
        self.assertNotEqual(f.request(missing,token='synthetic-owner',owner=True)[0],200)
        f.f.fixture.revoke()
        self.assertNotEqual(f.request(path,token='synthetic-owner',owner=True)[0],200)


if __name__=='__main__':unittest.main()
