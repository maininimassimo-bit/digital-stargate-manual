"""Lifecycle with mock owned process, synthetic receipt bytes and MemoryStore. Not cloud/native OAT."""
import datetime as dt
import unittest
from unittest.mock import patch, Mock

from tools.pixinsight.local_pilot.broker import ProtocolError, encode
from tools.scientific_registry.ingestion_storage import MemoryStore
from tools.scientific_transients.local_registry import LocalRegistry, fingerprint
from tools.scientific_transients.attempt_journal import AttemptJournal
from tools.scientific_transients.receipt_coordinator import ReceiptOutbox
from tools.scientific_transients.native_supervisor import NativeSupervisor, NativeProcess
from tools.scientific_transients import test_native_aperture as native_fixtures
from tools.scientific_transients.test_receipt_coordinator import MemoryTransport
from tools.scientific_transients.queue import TransientQueue


class OwnedMock:
    pid = 12345
    def __init__(self): self.closed = False
    def close_after_retained_terminal(self): self.closed = True; return 0


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.fixture = native_fixtures.NativeReceiptTests(); self.fixture.setUp(); self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        self.artifacts = f.root / 'artifacts'; self.artifacts.mkdir()
        f.runs = self.artifacts / 'runs'; f.runs.mkdir(); self.directory = f.prepare()
        for name in ['reference.json','contract.json','provenance.json']:
            (self.artifacts / name).write_bytes(encode({'scope':'SYNTHETIC_NOT_NATIVE_OR_SCIENTIFIC_EVIDENCE'}))
        binding = {k:c*32 for k,c in zip(['bindingRef','inputRef','referenceRef','algorithmRef','contractRef'],'12345')}
        paths = {'INPUT':self.directory/'input.xisf','PARAMETERS':self.directory/'parameters.json',
                 'ALGORITHM':self.directory/'native_aperture.jsh','REFERENCE':self.artifacts/'reference.json',
                 'CONTRACT':self.artifacts/'contract.json','PROVENANCE':self.artifacts/'provenance.json'}
        registry_root = f.root / 'registry'; registry_root.mkdir()
        self.local = LocalRegistry(self.artifacts,registry_root)
        registered = self.local.register(encode({'protocol':'DSG_TRANSIENT_LOCAL_BINDING_V1','binding':binding,
                    'files':[{'role':k,'path':p.relative_to(self.artifacts).as_posix(),**fingerprint(p)} for k,p in paths.items()]}))
        self.now = dt.datetime(2026,10,8,tzinfo=dt.timezone.utc)
        self.queue = TransientQueue(MemoryStore(),'a'*32,clock=lambda:self.now)
        self.queue.register(binding); self.queue.create({'requestId':'6'*32,'bindingRef':binding['bindingRef']})
        self.claim = self.queue.claim({'workerId':'a'*32,'rootId':'8'*32})['job']
        value = {k:self.claim[k] for k in ['jobId','attemptId','rootId','binding']};value['manifestSha256']=registered['manifestSha256']
        journals=f.root/'journals';journals.mkdir();self.journal=AttemptJournal.prepare(self.local,journals,value)
        outboxes=f.root/'outboxes';outboxes.mkdir();self.outbox=ReceiptOutbox.prepare(outboxes,self.journal)
        self.transport=MemoryTransport(self.queue);self.process=OwnedMock();self.starts=0;self.elapsed=0

    def spawn(self,directory):
        self.assertEqual(directory,self.directory);self.starts+=1;return self.process

    def supervisor(self,**kwargs):
        return NativeSupervisor(self.local,self.journal,self.outbox,self.directory,self.fixture.operation,
                    self.transport,self.claim['leaseToken'],spawn=kwargs.pop('spawn',self.spawn),clock=lambda:self.elapsed,
                    timeout=10,engine=self.fixture.engine,catalog=self.fixture.catalog,**kwargs)

    def native(self,state):
        if state=='COMPLETED':return self.fixture.terminal(self.directory)
        value={'protocol':'DSG_NATIVE_APERTURE_V1','operationRef':self.fixture.operation,'state':state,
               'rows':[],'retained':[],'error':'synthetic terminal fixture before image opened','scienceValidation':'NOT_VALIDATED'}
        (self.directory/'terminal.json').write_bytes(encode(value));return value

    def cancel(self):self.queue.cancel(self.claim['jobId'])

    def test_complete_only_after_verified_receipt_and_checkpoint_acks(self):
        s=self.supervisor();self.assertEqual(s.start()['state'],'RUNNING');self.assertEqual(self.starts,1)
        self.assertEqual(len(self.transport.posts),2);self.assertFalse(self.process.closed)
        self.native('COMPLETED');self.assertEqual(s.tick()['state'],'COMPLETED')
        self.assertTrue(self.process.closed);self.assertEqual(len(self.transport.posts),4)
        result=self.queue.status(self.claim['jobId'])['result'];self.assertEqual(result['qualityCounts']['measured'],0)
        self.assertEqual(len(self.journal._events()),5)
        for p in self.fixture.root.rglob('*.json'):
            self.assertNotIn(self.claim['leaseToken'].encode(),p.read_bytes());self.assertNotIn(b'leaseToken',p.read_bytes())
        with self.assertRaises(ProtocolError):s.start()
        with self.assertRaises(ProtocolError):s.tick()

    def test_cancel_before_start_never_launches_and_terminal_is_acknowledged(self):
        s=self.supervisor();self.cancel();self.assertEqual(s.start()['state'],'CANCELLED')
        self.assertEqual(self.starts,0);self.assertEqual(self.queue.status(self.claim['jobId'])['state'],'CANCELLED')

    def test_cancel_at_operation_ack_prevents_launch(self):
        original=self.transport.post
        def post(path,value):
            result=original(path,value)
            if value['sequence']==2:self.cancel()
            return result
        self.transport.post=post;s=self.supervisor();self.assertEqual(s.start()['state'],'CANCELLED')
        self.assertEqual(self.starts,0);self.assertEqual(len(self.transport.posts),3)

    def test_cancel_during_native_requests_safe_point_without_early_termination(self):
        s=self.supervisor();s.start();self.cancel()
        self.assertTrue(s.tick()['stopRequested']);self.assertTrue((self.directory/'cancel.json').exists())
        self.assertFalse(self.process.closed);self.native('CANCELLED')
        self.assertEqual(s.tick()['state'],'CANCELLED');self.assertTrue(self.process.closed)
        self.assertEqual(self.queue.status(self.claim['jobId'])['state'],'CANCELLED')

    def test_completed_native_and_owner_cancel_preserve_checkpoint_without_success(self):
        s=self.supervisor();s.start();self.native('COMPLETED');self.cancel()
        self.assertEqual(s.tick()['state'],'CANCELLED');self.assertTrue((self.directory/'history-bundle.json').exists())
        self.assertEqual(self.queue.status(self.claim['jobId'])['result'],None)
        self.assertEqual(self.journal._events()[-2]['kind'],'CHECKPOINT')

    def test_native_failure_retained_before_owned_handle_close(self):
        s=self.supervisor();s.start();self.native('FAILED');self.assertEqual(s.tick()['state'],'FAILED')
        self.assertTrue((s.records/'native-terminal.json').exists());self.assertTrue(self.process.closed)

    def test_lost_start_ack_freezes_without_native_or_second_receipt(self):
        self.transport.lose=True;s=self.supervisor();self.assertEqual(s.start()['state'],'RECOVERY_REQUIRED')
        self.assertEqual(self.starts,0);self.assertEqual(len(self.outbox._records()),1)
        with self.assertRaises(ProtocolError):s.start()

    def test_timeout_keeps_owned_process_and_requests_native_safe_point(self):
        s=self.supervisor();s.start();self.elapsed=11
        self.assertEqual(s.tick()['state'],'RECOVERY_REQUIRED');self.assertFalse(self.process.closed)
        self.assertTrue((self.directory/'cancel.json').exists());self.assertEqual(len(self.transport.posts),3)
        self.assertEqual(self.queue.status(self.claim['jobId'])['state'],'RECOVERY_REQUIRED')

    def test_invalid_terminal_never_grants_process_close(self):
        s=self.supervisor();s.start();t=self.native('FAILED');t['operationRef']='f'*32
        (self.directory/'terminal.json').write_bytes(encode(t));self.assertEqual(s.tick()['state'],'RECOVERY_REQUIRED')
        self.assertFalse(self.process.closed)

    def test_expired_remote_retains_complete_native_but_never_claims_success(self):
        s=self.supervisor();s.start();self.now+=dt.timedelta(hours=1);self.native('COMPLETED')
        self.assertEqual(s.tick()['state'],'RECOVERY_REQUIRED');self.assertTrue(self.process.closed)
        self.assertEqual(self.queue.status(self.claim['jobId'])['state'],'RECOVERY_REQUIRED')
        self.assertEqual(len(self.transport.posts),2)

    def test_lost_remote_read_waits_for_safe_point_then_recovery(self):
        s=self.supervisor();s.start()
        def broken(path):raise ProtocolError('SYNTHETIC_LOST_TRANSPORT')
        self.transport.request=broken;self.assertTrue(s.tick()['stopRequested']);self.assertFalse(self.process.closed)
        self.native('CANCELLED');self.assertEqual(s.tick()['state'],'RECOVERY_REQUIRED');self.assertTrue(self.process.closed)

    def test_launch_exception_is_ambiguous_and_never_replayed(self):
        def fail(directory):raise OSError('synthetic launch exception')
        s=self.supervisor(spawn=fail);self.assertEqual(s.start()['state'],'RECOVERY_REQUIRED')
        self.assertTrue((s.records/'launch-intent.json').exists())
        with self.assertRaises(ProtocolError):s.start()

    def test_parameter_mutation_before_start_never_launches(self):
        s=self.supervisor();p=self.directory/'parameters.json';p.write_bytes(p.read_bytes()+b' ')
        self.assertEqual(s.start()['state'],'RECOVERY_REQUIRED');self.assertEqual(self.starts,0)

    def test_reopened_outbox_and_duplicate_supervisor_refuse_start(self):
        s=self.supervisor()
        with self.assertRaises(FileExistsError):self.supervisor()
        self.outbox=ReceiptOutbox(self.outbox.directory,self.journal)
        with self.assertRaisesRegex(ProtocolError,'SAME_SESSION'):self.supervisor()

    def test_cancel_after_checkpoint_ack_keeps_local_complete_and_remote_recovery_separate(self):
        s=self.supervisor();s.start();self.native('COMPLETED');original=self.transport.post
        def post(path,value):
            result=original(path,value)
            if value['sequence']==3:self.cancel()
            return result
        self.transport.post=post
        self.assertEqual(s.tick()['state'],'RECOVERY_REQUIRED')
        self.assertEqual(self.journal._events()[-1]['kind'],'COMPLETED')
        self.assertTrue((self.journal.directory/'report.json').exists())
        self.assertEqual(len(self.transport.posts),3);self.assertIsNotNone(self.outbox._records()[-1][4])
        self.assertIsNone(self.queue.status(self.claim['jobId'])['result'])

    def test_failed_checkpoint_save_never_terminates_owned_process(self):
        s=self.supervisor();s.start();t=self.native('FAILED');t['retained']=['NOT_SAVED']
        (self.directory/'terminal.json').write_bytes(encode(t));self.assertEqual(s.tick()['state'],'RECOVERY_REQUIRED')
        self.assertFalse(self.process.closed);self.assertTrue((s.records/'native-terminal.json').exists())

    def test_conflicting_cancel_marker_preserved_with_recovery_no_process_close(self):
        s=self.supervisor();s.start();bad=encode({'operationRef':'f'*32,'requested':True})
        (self.directory/'cancel.json').write_bytes(bad);self.cancel()
        self.assertEqual(s.tick()['state'],'RECOVERY_REQUIRED');self.assertFalse(self.process.closed)
        self.assertEqual((self.directory/'cancel.json').read_bytes(),bad)

    def test_native_factory_uses_fixed_executable_argv_no_shell_and_current_handle_only(self):
        child=Mock(pid=54321);child.poll.return_value=0;child.returncode=0
        with patch('tools.scientific_transients.native_supervisor.safe_path',return_value=self.fixture.input), \
             patch('tools.scientific_transients.native_supervisor.subprocess.Popen',return_value=child) as popen:
            p=NativeProcess(self.directory)
            args,kwargs=popen.call_args
            self.assertEqual(args[0][-1],'-r='+str(self.directory/'entry.js'))
            self.assertEqual(len(args[0]),6);self.assertIs(kwargs['shell'],False)
            self.assertEqual(p.close_after_retained_terminal(),0);child.terminate.assert_not_called()


if __name__=='__main__':unittest.main()
