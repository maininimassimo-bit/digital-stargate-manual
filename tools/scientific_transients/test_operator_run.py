"""Bounded explicit operator caller: synthetic queue and owned mock process only."""
import contextlib
import hashlib
import io
import json
import os
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode, ProtocolError
from tools.scientific_transients import test_reservation_intent as fixtures
from tools.scientific_transients.operator_run import OperatorPlan, ORIGIN, main


class OperatorTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.ReservationTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        f=self.f;identity=f.f.journal.anchor['identity']
        self.value={'protocol':'DSG_TRANSIENT_OPERATOR_PLAN_V1','serviceOrigin':ORIGIN,
                    'workerId':'a'*32,'rootId':'8'*32,'jobId':f.job['jobId'],
                    'reservationRef':'e'*32,'binding':identity['binding'],
                    'manifestSha256':identity['manifestSha256'],'operationRef':f.f.fixture.operation,
                    'paths':{k:str(v) for k,v in {'artifacts':f.f.artifacts,'registry':f.f.local.registry,
                    'run':f.f.directory,'intents':f.root,'journals':f.jroot,'outboxes':f.oroot}.items()},
                    'timeoutSeconds':10}
        self.path=f.f.fixture.root/'operator-plan.json';self.persist()

    def persist(self):
        raw=encode(self.value);self.path.write_bytes(raw);self.sha=hashlib.sha256(raw).hexdigest()

    def load(self):
        return OperatorPlan.load(self.path,self.sha,engine=self.f.f.fixture.engine,catalog=self.f.f.fixture.catalog)

    def run_plan(self,plan=None,sleep=None):
        return (plan or self.load()).run_selected(self.f.transport,native_launch_authorized=True,
                  spawn=self.f.f.spawn,clock=lambda:self.f.elapsed,sleep=sleep or self.advance_complete)

    def advance_complete(self,seconds):
        self.f.elapsed+=seconds;self.f.f.native('COMPLETED')

    def test_mock_completion_one_selected_job_and_no_secret_persistence(self):
        result=self.run_plan();self.assertEqual(result['state'],'COMPLETED');self.assertEqual(self.f.f.starts,1)
        self.assertEqual(self.f.f.queue.status(self.f.job['jobId'])['scientificValidation'],'NOT_VALIDATED')
        # Explicitly test duplicate invocation before any further remote request or launch.
        calls=len(self.f.transport.calls)
        with self.assertRaises((FileExistsError,ProtocolError)):self.run_plan()
        self.assertEqual(len(self.f.transport.calls),calls);self.assertEqual(self.f.f.starts,1)
        for path in self.f.f.fixture.root.rglob('*.json'):
            self.assertNotIn(b'leaseToken',path.read_bytes())

    def test_preflight_is_offline_and_launch_requires_explicit_boolean(self):
        plan=self.load();plan.verify()
        for flag in [False,1,None]:
            with self.assertRaises(ProtocolError):plan.run_selected(self.f.transport,native_launch_authorized=flag)
        self.assertEqual(self.f.transport.calls,[]);self.assertEqual(self.f.f.starts,0)

    def test_missing_selected_job_refused_before_network(self):
        self.value['jobId']=None;self.persist();plan=self.load()
        with self.assertRaises(ProtocolError):self.run_plan(plan)
        self.assertEqual(self.f.transport.calls,[])

    def test_plan_mutation_and_private_fields_refused_before_network(self):
        plan=self.load();self.path.write_bytes(self.path.read_bytes()+b' ')
        with self.assertRaises(ProtocolError):self.run_plan(plan)
        self.persist();plan=self.load();plan.value['jobId']='TRN_'+'d'*32
        with self.assertRaises(ProtocolError):self.run_plan(plan)
        self.value['token']='synthetic-private';self.persist()
        with self.assertRaises(ProtocolError):self.load()
        self.assertEqual(self.f.transport.calls,[])

    def test_wrong_origin_digest_relative_path_overlap_and_timeout_refused(self):
        original=json.loads(json.dumps(self.value))
        cases=[('serviceOrigin','https://example.invalid'),('timeoutSeconds',True),('timeoutSeconds',901)]
        for key,value in cases:
            self.value=json.loads(json.dumps(original));self.value[key]=value;self.persist()
            with self.assertRaises(ProtocolError):self.load()
        self.value=original;self.value['paths']['intents']='relative';self.persist()
        with self.assertRaises(ProtocolError):self.load()
        self.value['paths']['intents']=self.value['paths']['artifacts'];self.persist()
        with self.assertRaises(ProtocolError):self.load()
        self.assertEqual(self.f.transport.calls,[])

    def test_lost_reservation_and_reentry_never_start_or_repeat_post(self):
        self.f.transport.lose=True
        with self.assertRaises(ProtocolError):self.run_plan()
        self.assertEqual(self.f.f.starts,0);self.assertEqual(len(self.f.transport.calls),1)
        with self.assertRaises(FileExistsError):self.run_plan()
        self.assertEqual(len(self.f.transport.calls),1)
        self.assertTrue((self.f.root/('e'*32)/'operator-unconfirmed.json').is_file())

    def test_plan_changed_after_reserve_never_launches(self):
        original=self.f.transport.request
        def request(path,value=None):
            result=original(path,value)
            if value is not None:self.path.write_bytes(self.path.read_bytes()+b' ')
            return result
        self.f.transport.request=request
        with self.assertRaises(ProtocolError):self.run_plan()
        self.assertEqual(self.f.f.starts,0)

    def test_timeout_retains_process_and_requests_safe_point(self):
        def advance(seconds):self.f.elapsed+=seconds
        self.assertEqual(self.run_plan(sleep=advance)['state'],'RECOVERY_REQUIRED')
        self.assertFalse(self.f.f.process.closed)
        self.assertTrue((self.f.f.directory/'cancel.json').exists())

    def test_cancel_after_reservation_before_launch_never_starts(self):
        original=self.f.transport.request
        def request(path,value=None):
            result=original(path,value)
            if value is not None:self.f.f.queue.cancel(self.f.job['jobId'])
            return result
        self.f.transport.request=request
        self.assertEqual(self.run_plan()['state'],'CANCELLED');self.assertEqual(self.f.f.starts,0)

    def test_cancel_during_native_preserves_terminal_before_owned_close(self):
        def cancel(seconds):
            self.f.elapsed+=seconds
            self.f.f.queue.cancel(self.f.job['jobId'])
            self.f.f.native('CANCELLED')
        self.assertEqual(self.run_plan(sleep=cancel)['state'],'CANCELLED')
        self.assertTrue(self.f.f.process.closed)

    def test_outcome_write_failure_preserves_remote_terminal_without_replay(self):
        from tools.scientific_transients import operator_run
        original=operator_run.write_new
        def write(path,value):
            if path.name=='operator-outcome.json':raise OSError('synthetic private failure')
            return original(path,value)
        with patch.object(operator_run,'write_new',side_effect=write):
            with self.assertRaises(ProtocolError):self.run_plan()
        self.assertEqual(self.f.f.queue.status(self.f.job['jobId'])['state'],'COMPLETED')
        self.assertTrue((self.f.root/('e'*32)/'operator-unconfirmed.json').exists())
        self.assertEqual(self.f.f.starts,1)

    def test_interrupt_retains_uncertainty_without_stop_attestation_or_replay(self):
        def interrupted(seconds):raise KeyboardInterrupt('synthetic secret must not escape')
        with self.assertRaisesRegex(ProtocolError,'OPERATOR_UNCONFIRMED_KEEP_EVIDENCE_NO_REPLAY'):
            self.run_plan(sleep=interrupted)
        record=json.loads((self.f.root/('e'*32)/'operator-unconfirmed.json').read_text())
        self.assertIs(record['nativeStoppedAttested'],False);self.assertFalse(self.f.f.process.closed)
        with self.assertRaises(FileExistsError):self.run_plan()
        self.assertEqual(self.f.f.starts,1)

    def test_register_exact_binding_only_no_native_or_queue_selection(self):
        plan=self.load();calls=[]
        class Transport:
            def request(self,path,value):calls.append((path,value));return dict(value)
        self.assertTrue(plan.register_binding(Transport())['bindingRegistered'])
        self.assertEqual(calls,[('/v1/transient-analysis/worker/register',self.value['binding'])])
        self.assertEqual(self.f.f.starts,0)
        class Wrong:
            def request(self,path,value):return {**value,'bindingRef':'d'*32}
        with self.assertRaises(ProtocolError):plan.register_binding(Wrong())

    def test_cli_missing_authorization_or_credential_never_constructs_transport(self):
        plan=self.load()
        for mode,extra in [('run-selected',[]),('register-binding',[])]:
            with patch('tools.scientific_transients.operator_run.OperatorPlan.load',return_value=plan), \
                 patch('tools.scientific_transients.operator_run.TransientTransport') as transport, \
                 patch.dict(os.environ,{},clear=True),contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main([mode,'--plan',str(self.path),'--plan-sha256',self.sha]+extra),2)
                transport.assert_not_called();self.assertNotIn(str(self.path),output.getvalue())

    def test_cli_offline_preflight_never_reads_credentials_or_constructs_transport(self):
        with patch('tools.scientific_transients.operator_run.OperatorPlan.load',return_value=self.load()), \
             patch('tools.scientific_transients.operator_run.TransientTransport') as transport, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(['preflight','--plan',str(self.path),'--plan-sha256',self.sha]),0)
            transport.assert_not_called();self.assertIs(json.loads(output.getvalue())['networkRequested'],False)


if __name__=='__main__':unittest.main()
