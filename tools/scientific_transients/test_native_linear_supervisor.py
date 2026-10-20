"""Original opaque fixtures, fake Popen/locks/Win32 queries. Never starts native code."""
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import encode
from tools.scientific_transients import native_linear_supervisor as lifecycle
from tools.scientific_transients import native_owned_closure as owned
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients import test_native_run_records as fixtures
from tools.scientific_transients import test_native_state_metadata as state_fixture
from tools.scientific_transients.native_read_locks import NativeReadLocks
from tools.scientific_transients.native_supervision_signals import NativeSupervisionSignals


def fake_locks(rows,guard=None):
    group=object.__new__(NativeReadLocks); group._released=False
    group._held=[(object(),Path(row['path']),dict(row),()) for row in rows]
    return group


class LinearSupervisorTests(unittest.TestCase):
    def setUp(self):
        self.case=fixtures.NativeRunRecordsTests(); self.case.setUp(); self.addCleanup(self.case.doCleanups)
        self.f=self.case.fixture; self.records=self.case.records(); self.signals=NativeSupervisionSignals(self.records)
        self.code=None
        patches=[patch.object(NativeReadLocks,'verify',return_value=None),
            patch.object(lifecycle,'_spawn_native',return_value=self.case.holder.process),
            patch.object(lifecycle,'_acquire_owner_locks',side_effect=fake_locks),
            patch.object(self.case.holder.Queries,'poll',side_effect=lambda handle:self.code),
            patch.object(owned,'_WindowsOwnedExit',side_effect=AssertionError('NO_REAL_WAIT_OR_TERMINATION'))]
        self.mocks=[]
        for item in patches: self.mocks.append(item.start()); self.addCleanup(item.stop)
        self.spawn=self.mocks[1]
        rows=[dict(path=p.as_posix(),sha256=row['sha256'],byteLength=row['byteLength'])
              for p,row,_ in self.records._pins if p.parent==self.f.work]
        for role in ['ENTRY','LAUNCHER']:
            row=self.f.fixed[role]; rows.append({k:row[k] for k in ['path','sha256','byteLength']})
        self.static=fake_locks(rows)

    def supervisor(self): return lifecycle.LinearNativeSupervisor(self.records,self.signals,[self.static])

    def native_products(self):
        """Create declared synthetic products after the fake Owner handshake."""
        f=self.f; r=self.records
        pins={p.name:row for p,row,_ in r._pins if p.parent==f.work}
        m=state_fixture.NativeStateMetadataTests(); m.setUp()
        m.expected.update(operationRef=f.operation,parametersSha256=pins['parameters.json']['sha256'],
            sealSha256=f.binding['sealSha256'],sourceSha256=pins['source.fits']['sha256'],
            kernelSpecSha256=pins['kernel-spec.json']['sha256'],lineageSha256=pins['source-lineage.json']['sha256'],
            dependencies={key:f.fixed[role]['sha256'] for role,key in [('CORE','coreSha256'),('PARSER','parserSha256'),
                ('PRIMARY','primarySha256'),('WRAPPER','wrapperSha256')]},pixInsightVersion=f.control['expectedPixInsightVersion'],
            processSessionRef=f.control['processSessionRef'],ownerSha256=pins['native-owner.json']['sha256'],
            ownerReadySha256=pins['native-owner-ready.json']['sha256'])
        m.started.update(**{k:m.expected[k] for k in ['operationRef','parametersSha256','sealSha256','pixInsightVersion']})
        m.evidence.update(**{k:copy.deepcopy(v) for k,v in m.expected.items() if k!='sealSha256'})
        f.terminal['products']=[]
        for name in sorted(pub.REQUIRED):
            raw=encode(m.started) if name=='started-native.json' else (
                encode(m.evidence) if name=='native-evidence.json' else ('SYNTHETIC_OPAQUE_'+name).encode('ascii'))
            (f.work/name).write_bytes(raw)
            f.terminal['products'].append(dict(role=name,name=name,sha256=fixtures.fixtures.sha(raw),byteLength=len(raw)))
        f.write_terminal()

    def test_constructor_does_not_spawn_and_checks_original_static_lock_coverage(self):
        supervisor=self.supervisor()
        self.spawn.assert_not_called()
        self.assertEqual(supervisor.diagnostic()['state'],'PREPARED_LIVE')

    def test_missing_lock_blocks_before_spawn(self):
        self.static._held.pop()
        with self.assertRaisesRegex(Exception,'LINEAR_SUPERVISOR_LOCK_COVERAGE'): self.supervisor()
        self.spawn.assert_not_called()
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])

    def test_consumed_record_precedes_sole_spawn_and_owner_commits_after_capture(self):
        supervisor=self.supervisor()
        def spawn(*args):
            self.assertTrue((self.f.journal/'start-consumed.json').exists())
            self.assertFalse((self.f.work/'native-owner-ready.json').exists())
            return self.case.holder.process
        self.spawn.side_effect=spawn
        value=supervisor.start()
        self.assertEqual(value['state'],'RUNNING_HELD')
        self.assertTrue((self.f.work/'native-owner-ready.json').exists())
        self.assertIs(supervisor._process,self.case.holder.process)
        self.assertIs(supervisor._held,self.records._held)
        with self.assertRaisesRegex(Exception,'LINEAR_SUPERVISOR_START_REPLAY'): supervisor.start()
        self.spawn.assert_called_once()

    def test_popen_exception_preserves_fence_and_never_retries(self):
        supervisor=self.supervisor(); self.spawn.side_effect=OSError('SYNTHETIC_AMBIGUOUS_START')
        with self.assertRaises(OSError): supervisor.start()
        self.assertTrue((self.f.journal/'start-consumed.json').exists())
        self.assertEqual(supervisor.diagnostic()['state'],'UNCERTAIN_HELD')
        supervisor.tick(); supervisor.tick()
        self.spawn.assert_called_once()

    def test_capture_failure_keeps_exact_popen_and_adopted_held_before_diagnostics(self):
        supervisor=self.supervisor(); self.case.holder.failure=True
        with self.assertRaises(Exception): supervisor.start()
        self.assertIs(supervisor._process,self.case.holder.process)
        self.assertIs(supervisor._held,self.signals._held)
        self.assertFalse((self.f.work/'native-owner-ready.json').exists())
        self.spawn.assert_called_once()

    def test_memory_uncertainty_after_consumption_still_prevents_popen(self):
        supervisor=self.supervisor(); original=self.f.session.assert_intact
        def attest():
            result=original()
            if supervisor._state=='START_CONSUMED': self.signals._fail()
            return result
        with patch.object(self.f.session,'assert_intact',side_effect=attest):
            with self.assertRaises(Exception): supervisor.start()
        self.assertTrue((self.f.journal/'start-consumed.json').exists())
        self.spawn.assert_not_called()
        self.assertEqual(supervisor.diagnostic()['state'],'UNCERTAIN_HELD')

    def test_missing_return_while_running_is_observation_not_completion(self):
        supervisor=self.supervisor(); supervisor.start()
        self.assertEqual(supervisor.tick()['state'],'RUNNING_HELD')
        self.assertFalse(supervisor.diagnostic()['publicationAttemptConsumed'])
        self.assertEqual(list(self.f.archive.iterdir()),[])

    def test_deadline_cancel_is_exclusive_and_does_not_prove_stop(self):
        supervisor=self.supervisor(); supervisor.start(); self.case.mono=181
        self.assertEqual(supervisor.tick()['state'],'RETENTION_ONLY')
        path=self.f.work/'cancel.json'; before=path.stat()
        supervisor.tick()
        self.assertEqual(path.stat().st_ino,before.st_ino)
        self.assertFalse(supervisor.diagnostic()['processExitObserved'])
        self.assertFalse(supervisor.diagnostic()['closureReceiptCommitted'])

    def test_cancel_before_start_blocks_any_spawn(self):
        supervisor=self.supervisor(); supervisor.tick(cancel=True)
        with self.assertRaisesRegex(Exception,'LINEAR_SUPERVISOR_START_REPLAY'): supervisor.start()
        self.spawn.assert_not_called()

    def test_memory_uncertainty_before_start_is_reported_by_tick(self):
        supervisor=self.supervisor(); self.signals._fail()
        with self.assertRaisesRegex(Exception,'LINEAR_SUPERVISOR_OBSERVED_UNCERTAINTY'): supervisor.tick()
        self.assertEqual(supervisor.diagnostic()['state'],'UNCERTAIN_HELD')
        self.spawn.assert_not_called()

    def test_last_budget_callback_uncertainty_blocks_running_tick(self):
        supervisor=self.supervisor(); supervisor.start(); original=self.records._budget.check; calls=0
        def check():
            nonlocal calls
            result=original(); calls+=1
            # First tick observation, runtime guard start, runtime guard end.
            if calls==3: self.signals._fail()
            return result
        with patch.object(self.records._budget,'check',side_effect=check):
            with self.assertRaisesRegex(Exception,'LINEAR_SUPERVISOR_OBSERVED_UNCERTAINTY'): supervisor.tick()
        self.assertFalse(supervisor.diagnostic()['publicationAttemptConsumed'])
        self.assertEqual(supervisor.diagnostic()['state'],'UNCERTAIN_HELD')

    def test_exit_without_return_is_truthfully_exited_and_evidence_uncertain(self):
        supervisor=self.supervisor(); supervisor.start(); self.code=7
        with self.assertRaisesRegex(Exception,'LINEAR_SUPERVISOR_RETURN_MISSING_AFTER_EXIT'): supervisor.tick()
        value=supervisor.diagnostic()
        self.assertEqual(value['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertEqual(value['exitCode'],7)
        self.assertTrue(value['processExitObserved'])

    def test_partial_return_fails_once_without_publication_or_close_retry(self):
        supervisor=self.supervisor(); supervisor.start()
        (self.f.work/'native-return.json').write_bytes(b'SYNTHETIC_PARTIAL')
        with self.assertRaises(Exception): supervisor.tick()
        self.assertTrue(supervisor.diagnostic()['publicationAttemptConsumed'])
        before={p.name:(p.stat().st_ino,p.stat().st_size,p.stat().st_mtime_ns) for p in self.f.journal.iterdir()}
        supervisor.tick(); supervisor.tick()
        self.assertEqual(before,{p.name:(p.stat().st_ino,p.stat().st_size,p.stat().st_mtime_ns) for p in self.f.journal.iterdir()})
        self.assertFalse(supervisor.diagnostic()['closureReceiptCommitted'])
        self.spawn.assert_called_once()

    def test_complete_fake_native_path_retains_actual_opaque_bytes_and_s7_exit_receipt(self):
        supervisor=self.supervisor(); supervisor.start(); self.native_products(); self.code=0
        value=supervisor.tick()
        self.assertEqual(value['state'],'CLOSED_RETAINED')
        self.assertTrue(value['closureReceiptCommitted'])
        self.assertTrue(value['processExitObserved'])
        self.assertEqual(value['scientificValidation'],'NOT_VALIDATED')
        self.assertEqual(value['qualifiedControls'],0)
        self.assertTrue((self.f.journal/'owned-closure.json').exists())
        supervisor.tick(); self.spawn.assert_called_once()
        self.assertFalse(self.static._released)

    def test_owner_lock_failure_retains_static_locks_process_and_uncertainty(self):
        supervisor=self.supervisor()
        with patch.object(lifecycle,'_acquire_owner_locks',side_effect=OSError('SYNTHETIC_OWNER_LOCK_FAILURE')):
            with self.assertRaises(OSError): supervisor.start()
        self.assertEqual(supervisor.diagnostic()['state'],'UNCERTAIN_HELD')
        self.assertIs(supervisor._process,self.case.holder.process)
        self.assertFalse(self.static._released)
        self.assertTrue((self.f.work/'native-owner-ready.json').exists())
        self.assertFalse(supervisor.diagnostic()['closureReceiptCommitted'])

    def test_receipt_failure_after_exit_is_propagated_without_inventing_alive(self):
        supervisor=self.supervisor(); supervisor.start(); self.native_products(); self.code=0
        original=pub._write_control
        def write(path,value):
            if path==self.f.journal/'owned-closure.json': raise OSError('SYNTHETIC_CLOSURE_IO')
            return original(path,value)
        with patch.object(pub,'_write_control',side_effect=write):
            with self.assertRaises(OSError): supervisor.tick()
        value=supervisor.diagnostic()
        self.assertEqual(value['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertTrue(value['processExitObserved'])
        self.assertEqual(value['exitCode'],0)
        self.assertFalse(value['closureReceiptCommitted'])
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])
        supervisor.tick(); self.spawn.assert_called_once()

    def test_reconstruction_with_same_live_records_is_forbidden(self):
        self.supervisor()
        with self.assertRaisesRegex(Exception,'LINEAR_SUPERVISOR_RECONSTRUCTION'): self.supervisor()


class HiddenSpawnContractTests(unittest.TestCase):
    def test_exact_hidden_argv_shell_false_and_no_unbounded_pipe(self):
        class Startup:
            dwFlags=0
            wShowWindow=99
        with patch.object(lifecycle.os,'name','nt'), patch.object(lifecycle.subprocess,'STARTUPINFO',Startup,create=True), \
                patch.object(lifecycle.subprocess,'STARTF_USESHOWWINDOW',1,create=True), \
                patch.object(lifecycle.subprocess,'SW_HIDE',0,create=True), \
                patch.object(lifecycle.subprocess,'Popen') as popen:
            lifecycle._spawn_native('F:/synthetic.exe','F:/entry.js','F:/work')
        args,kwargs=popen.call_args
        self.assertEqual(args[0],['F:/synthetic.exe','-n','--automation-mode','--no-startup-scripts',
            '--no-startup-check-updates','-r=F:/entry.js'])
        self.assertIs(kwargs['shell'],False)
        self.assertEqual(kwargs['startupinfo'].wShowWindow,0)
        for key in ['stdin','stdout','stderr']: self.assertEqual(kwargs[key],lifecycle.subprocess.DEVNULL)


if __name__=='__main__': unittest.main()
