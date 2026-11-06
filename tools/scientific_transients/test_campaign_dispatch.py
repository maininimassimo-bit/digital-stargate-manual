"""Synthetic protected dispatch, real durable files and mock owned process only."""
import copy
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import campaign_dispatch as module
from tools.scientific_transients import test_campaign_queue as fixtures
from tools.scientific_transients import test_operator_run as operator_fixtures
from tools.scientific_transients import test_campaign_queue_http as http_fixtures
from tools.scientific_transients.attempt_journal import read_json


class MemoryCampaignTransport:
    def __init__(self, fixture):
        self.fixture, self.calls, self.lose = fixture, [], False

    def request(self, path, value=None):
        self.calls.append((path, copy.deepcopy(value)))
        if path.endswith('/reserve-once'):
            f = self.fixture
            response = f.bridge.reserve_envelope(fixtures.ref(10),f.intent['sha256'],0,
                                                value['reservation'],value['decisionId'])
            if self.lose: raise OSError('synthetic private error')
            return response
        return self.fixture.q.worker_receipt(path.rsplit('/',1)[-1])

    def post(self,path,value):
        self.calls.append((path, copy.deepcopy(value)))
        return self.fixture.q.report(path.split('/')[-2],value)


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.CampaignQueueTests();self.f.setUp()
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.transport=MemoryCampaignTransport(self.f)

    def prepare(self,**changes):
        args=dict(root=self.root,transport=self.transport,plan_ref=fixtures.ref(10),
                  intent_sha=self.f.intent['sha256'],ordinal=0,decision_id=fixtures.ref(96001),
                  request=self.f.request,binding=self.f.job['binding'],manifest_sha='a'*64,operation_ref='a'*32)
        args.update(changes)
        return module.CampaignReservationAdapter.prepare(**args)

    def reserve(self,adapter):return adapter.request(module.RESERVE,self.f.request)

    def test_real_guarded_queue_consumed_once_mapping_has_no_lease(self):
        adapter=self.prepare();result=self.reserve(adapter);mapping=adapter.mapping()
        self.assertEqual(set(result),{'disposition','job'})
        self.assertEqual(mapping['admissionSha256'],self.f.receipt()['admissions'][0]['sha256'])
        self.assertEqual(mapping['attemptId'],result['job']['attemptId'])
        self.assertEqual(mapping['manifestSha256'],'a'*64)
        for path in self.root.rglob('*.json'):
            self.assertNotIn(result['job']['leaseToken'].encode(),path.read_bytes())
            self.assertNotIn(b'leaseToken',path.read_bytes())
        with self.assertRaises(ProtocolError):self.reserve(adapter)
        self.assertEqual(len(self.transport.calls),1)
        with self.assertRaises(FileExistsError):self.prepare()

    def test_wrong_request_path_and_selection_rejected_without_network(self):
        adapter=self.prepare()
        with self.assertRaises(ProtocolError):adapter.request(module.RESERVE,dict(self.f.request,rootId='e'*32))
        for path in ('/v1/transient-analysis/worker/claim','/v1/transient-analysis/worker/register'):
            with self.assertRaises(ProtocolError):adapter.request(path,self.f.request)
        for ordinal in (True,-1,3):
            with self.assertRaises(ProtocolError):self.prepare(ordinal=ordinal)
        self.assertEqual(self.transport.calls,[])

    def test_lost_ack_never_resumes_from_get_or_restarts(self):
        self.transport.lose=True;adapter=self.prepare()
        with self.assertRaisesRegex(ProtocolError,'UNCONFIRMED_NO_REPLAY'):self.reserve(adapter)
        self.assertEqual(self.f.q.status(self.f.job['jobId'])['state'],'RESERVED')
        for action in (lambda:self.reserve(adapter),lambda:adapter.mapping(),
                       lambda:adapter.request('/v1/transient-analysis/worker/jobs/'+self.f.job['jobId'])):
            with self.assertRaises(ProtocolError):action()
        with self.assertRaises(FileExistsError):self.prepare()
        self.assertEqual(len(self.transport.calls),1)

    def test_dispatch_fsync_failure_never_sends(self):
        adapter=self.prepare()
        with patch('tools.scientific_transients.attempt_journal.os.fsync',side_effect=OSError('synthetic fsync')):
            with self.assertRaises(ProtocolError):self.reserve(adapter)
        self.assertEqual(self.transport.calls,[])
        self.assertEqual(adapter.phase,'RECONCILIATION_REQUIRED')

    def test_mapping_retention_failure_keeps_reserved_job_but_no_driver_grant(self):
        adapter=self.prepare();original=module.write_new
        def write(path,value):
            if path.name=='admission.json':raise OSError('synthetic retention failure')
            return original(path,value)
        with patch.object(module,'write_new',side_effect=write):
            with self.assertRaises(ProtocolError):self.reserve(adapter)
        self.assertEqual(adapter.phase,'RECONCILIATION_REQUIRED')
        self.assertEqual(self.f.q.status(self.f.job['jobId'])['state'],'RESERVED')
        with self.assertRaises(ProtocolError):adapter.mapping()
        self.assertFalse((adapter.directory/'admission.json').exists())

    def test_mapping_fsync_failure_after_response_preserves_file_without_driver_grant(self):
        adapter=self.prepare();original=os.fsync;calls=[]
        def fsync(fd):
            calls.append(fd)
            if len(calls)==2:raise OSError('synthetic mapping fsync failure')
            return original(fd)
        with patch('tools.scientific_transients.attempt_journal.os.fsync',side_effect=fsync):
            with self.assertRaises(ProtocolError):self.reserve(adapter)
        self.assertEqual(len(self.transport.calls),1)
        self.assertTrue((adapter.directory/'admission.json').exists())
        self.assertEqual(adapter.phase,'RECONCILIATION_REQUIRED')
        with self.assertRaises(ProtocolError):adapter.mapping()
        self.assertEqual(self.f.q.status(self.f.job['jobId'])['state'],'RESERVED')

    def test_unknown_envelope_and_binding_or_time_mismatch_refuse_mapping(self):
        mutations=[lambda r:r.update(protocol='unknown'),lambda r:r.update(admissionSha256=None),
                   lambda r:r.update(extra='unexpected'),lambda r:r['job'].update(rootId='e'*32),
                   lambda r:r['job'].update(leaseExpiresAt=r['job']['leaseIssuedAt'])]
        # Each subcase has independent synthetic authority and durable root.
        for mutate in mutations:
            f=fixtures.CampaignQueueTests();f.setUp()
            transport=MemoryCampaignTransport(f)
            with tempfile.TemporaryDirectory() as root:
                request=transport.request
                def changed(path,value=None):
                    response=request(path,value);mutate(response);return response
                transport.request=changed
                adapter=self.prepare(root=Path(root),transport=transport,intent_sha=f.intent['sha256'])
                with self.assertRaises(ProtocolError):self.reserve(adapter)
                self.assertFalse((adapter.directory/'admission.json').exists())

    def test_changed_mapping_blocks_report_and_read_before_network(self):
        adapter=self.prepare();self.reserve(adapter);calls=len(self.transport.calls)
        path=adapter.directory/'admission.json';path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaises(ProtocolError):adapter.request('/v1/transient-analysis/worker/jobs/'+self.f.job['jobId'])
        with self.assertRaises(ProtocolError):adapter.post('/v1/transient-analysis/worker/jobs/'+self.f.job['jobId']+'/report',{})
        self.assertEqual(len(self.transport.calls),calls)

    def test_changed_selection_consumes_adapter_before_any_dispatch(self):
        adapter=self.prepare();path=adapter.directory/'selection.json';original=path.read_bytes()
        path.write_bytes(original+b' ')
        with self.assertRaises(ProtocolError):self.reserve(adapter)
        self.assertEqual(adapter.phase,'RECONCILIATION_REQUIRED')
        path.write_bytes(original)
        with self.assertRaises(ProtocolError):self.reserve(adapter)
        self.assertEqual(self.transport.calls,[])

    def test_already_consumed_server_admission_returns_no_mapping_or_lease(self):
        self.f.reserve();adapter=self.prepare()
        self.assertEqual(self.reserve(adapter),{'disposition':'RECONCILIATION_REQUIRED','job':None})
        self.assertEqual(adapter.phase,'RECONCILIATION_REQUIRED')
        self.assertFalse((adapter.directory/'admission.json').exists())

    def test_owner_durable_projection_and_lost_ack_block_repeat(self):
        f=self.f;calls=[]
        class OwnerTransport:
            lose=False
            def request(self,path,body):
                calls.append((path,body))
                if path.endswith('/dispatch-intents'):return f.bridge.prepare_dispatch(fixtures.ref(10),body)
                result=f.bridge.project(fixtures.ref(10),f.intent['sha256'],0)
                if self.lose:raise OSError('synthetic lost ack')
                return result
        transport=OwnerTransport();owner=module.CampaignOwnerOperations(self.root,transport,fixtures.ref(10))
        self.assertEqual(owner.prepare_intent('1'*32,f.owner),f.intent)
        transport.lose=True
        with self.assertRaises(ProtocolError):owner.project('2'*32,f.intent['sha256'],0,f.owner['jobs'][0]['requestId'],f.job['binding'])
        with self.assertRaises(FileExistsError):owner.project('2'*32,f.intent['sha256'],0,f.owner['jobs'][0]['requestId'],f.job['binding'])
        self.assertEqual(len(calls),2)
        self.assertTrue((self.root/('2'*32)/'unconfirmed.json').exists())

    def test_owner_bad_body_or_fsync_failure_has_no_network(self):
        class Transport:
            def request(self,*args):raise AssertionError('network forbidden')
        owner=module.CampaignOwnerOperations(self.root,Transport(),fixtures.ref(10))
        with self.assertRaises(ProtocolError):owner.prepare_intent('1'*32,dict(self.f.owner,token='private'))
        with patch('tools.scientific_transients.attempt_journal.os.fsync',side_effect=OSError('synthetic fsync')):
            with self.assertRaises(ProtocolError):owner.prepare_intent('2'*32,self.f.owner)

    def test_actual_protected_http_transport_and_adapter_preserve_one_shot_contract(self):
        f=http_fixtures.ProtectedCampaignHttpTests();f.setUp();self.addCleanup(f.doCleanups)
        transport=module.CampaignWorkerTransport('http://127.0.0.1:'+str(f.server.server_port),
                                                http_fixtures.TOKEN,test_loopback=True)
        adapter=module.CampaignReservationAdapter.prepare(self.root,transport,f.ref,f.intent,0,'e'*32,
            f.f.request,f.f.job['binding'],'a'*64,'b'*32)
        response=adapter.request(module.RESERVE,f.f.request)
        self.assertEqual(response['disposition'],'CREATED')
        self.assertEqual(adapter.mapping()['admissionSha256'],f.f.receipt()['admissions'][0]['sha256'])
        observed=adapter.request('/v1/transient-analysis/worker/jobs/'+f.f.job['jobId'])
        self.assertNotIn('leaseToken',observed)
        with self.assertRaises(ProtocolError):adapter.request(module.RESERVE,f.f.request)
        for path in (module.BASE+f.ref+'/executions',module.BASE+f.ref+'/dispatch-intents/'+f.intent+'/jobs/3/reserve-once'):
            with self.assertRaises(ProtocolError):transport.request(path,{})
        with self.assertRaises(ProtocolError):transport.request(module.BASE+f.ref+'/frame-closures')


class OperatorAdapterTests(unittest.TestCase):
    def setUp(self):
        self.f=operator_fixtures.OperatorTests();self.f.setUp();self.addCleanup(self.f.doCleanups)

    def test_actual_operator_and_reservation_intent_use_adapter_without_contract_change(self):
        f=self.f;plan=f.load();root=f.f.f.fixture.root/'campaign-adapter';root.mkdir();calls=[]
        # Synthetic envelope source tests existing OperatorPlan/ReservationIntent/
        # driver contracts. Real campaign authority is tested separately above.
        class ProtectedTransport:
            def request(self,path,value=None):
                calls.append(path)
                if path.endswith('/reserve-once'):
                    result=f.f.transport.request(module.RESERVE,value['reservation'])
                    return dict(protocol=module.PROTOCOL,admissionSha256='a'*64,**result)
                return f.f.transport.request(path,value)
            def post(self,path,value):return f.f.transport.post(path,value)
        value=plan.value
        request={k:value[k] for k in ('workerId','rootId','jobId','reservationRef')}
        request['bindingRef']=value['binding']['bindingRef']
        adapter=module.CampaignReservationAdapter.prepare(root,ProtectedTransport(),'1'*32,'2'*64,0,
            '3'*32,request,value['binding'],value['manifestSha256'],value['operationRef'])
        result=plan.run_selected(adapter,native_launch_authorized=True,spawn=f.f.f.spawn,
                                clock=lambda:f.f.elapsed,sleep=f.advance_complete)
        self.assertEqual(result['state'],'COMPLETED');self.assertEqual(f.f.f.starts,1)
        self.assertTrue(f.f.f.process.closed)
        self.assertTrue(calls[0].endswith('/jobs/0/reserve-once'))
        self.assertNotIn(module.RESERVE,calls)
        self.assertEqual(adapter.mapping()['jobId'],value['jobId'])
        self.assertIs(read_json(adapter.directory/'admission.json')[0]['leasePersisted'],False)


if __name__=='__main__':unittest.main()
