"""Fake held process and Win32 exit calls; no native starts, waits or termination."""
import datetime as dt
import json
import inspect
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients import native_owned_closure as closure
from tools.scientific_transients import native_publication as pub
from tools.scientific_transients import test_native_held_process as held_fixture
from tools.scientific_transients import test_native_retained_verification as retained_fixture
from tools.scientific_transients.native_read_locks import NativeReadLocks
from tools.scientific_transients.native_retained_verification import RetainedRunVerification
from tools.scientific_transients.native_run_budget import LiveNativeBudget
from tools.scientific_transients.native_run_records import NativeRunRecords
from tools.scientific_transients.native_supervision_signals import NativeSupervisionSignals


class OwnedClosureTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root=Path(temporary.name).resolve(); op='a'*32
        self.holder=held_fixture.HeldNativeProcessTests(); self.holder.setUp(); self.addCleanup(self.holder.doCleanups)
        identity=self.holder.held.capture(); self.code=None; self.mono=1
        poll=patch.object(self.holder.Queries,'poll',side_effect=lambda handle:self.code)
        poll.start(); self.addCleanup(poll.stop)
        r=object.__new__(NativeRunRecords); self.records=r
        r._roots=[]
        for name in ['native-work','native-retained','native-supervision']:
            path=root/name/op; path.mkdir(parents=True); r._roots.append(pub._directory(path))
        r._work,r._retained,r._journal=[p for p,_ in r._roots]
        r._held=self.holder.held; r._held_identity=identity; r._failed=False; r._pins=[]; r._start_sha='e'*64
        r._binding=dict(operationRef=op,parentIntentSha256='1'*64,launchControlSha256='2'*64,
                       sealSha256='3'*64,grantSha256='4'*64)
        r._budget=LiveNativeBudget(monotonic=lambda:self.mono,
            wall=lambda:dt.datetime(2026,10,16,10,0,tzinfo=dt.timezone.utc))
        r._session=SimpleNamespace(assert_intact=lambda:None)
        self.signals=NativeSupervisionSignals(r); self.signals.adopt_held(r._held)
        self.proof=object.__new__(RetainedRunVerification)
        self.proof._records=r; self.proof._signals=self.signals; self.proof._failed=False
        self.proof._live=SimpleNamespace(verify=Mock())
        lock=object.__new__(NativeReadLocks); lock._released=False
        self.proof._locks=[lock]
        lock_patch=patch.object(NativeReadLocks,'verify',return_value=None)
        lock_patch.start(); self.addCleanup(lock_patch.stop)
        self.result=dict(conditionalComputationDeclaredComplete=True,nativeCooperativeDeadlineExceeded=False,
            markerSha256='5'*64,nativeReturnSha256='6'*64,processSessionRef='b'*32,**identity,
            parentCancelRequested=False,parentMonotonicDeadlineExceeded=False,parentWallDeadlineExceeded=False)
        self.proof._last=dict(self.result)
        self.fail_proof=False
        def verify():
            require(not self.fail_proof,'SYNTHETIC_PROOF_FAILURE')
            require(not (r._journal/'owned-closure.json').exists(),'SYNTHETIC_PRECLOSURE_GUARD')
            r._budget.check(); self.holder.held.identity()
            result=dict(self.result,parentCancelRequested=(r._work/'cancel.json').exists())
            self.proof._last=dict(result)
            return result
        proof_patch=patch.object(self.proof,'verify',side_effect=verify)
        proof_patch.start(); self.addCleanup(proof_patch.stop)
        self.wait_calls=[]; self.terminate_calls=[]; self.natural_exit_on_wait=None
        self.wait_hook=None; self.terminate_hook=None
        def wait(handle,milliseconds):
            self.wait_calls.append((handle,milliseconds))
            if self.wait_hook: self.wait_hook()
            if self.natural_exit_on_wait is not None: self.code=self.natural_exit_on_wait
            return self.code is not None
        def terminate(handle):
            self.terminate_calls.append(handle)
            if self.terminate_hook: self.terminate_hook()
            self.code=0
        self.api=SimpleNamespace(wait=wait,terminate=terminate)
        api_patch=patch.object(closure,'_WindowsOwnedExit',return_value=self.api)
        self.api_factory=api_patch.start(); self.addCleanup(api_patch.stop)

    def closer(self): return closure.OwnedNativeClosure(self.proof)

    def test_construction_does_not_wait_terminate_or_write(self):
        self.closer(); self.api_factory.assert_not_called()
        self.assertEqual(list(self.records._journal.iterdir()),[])

    def test_natural_exit_writes_exact_s7_receipt_and_never_calls_exit_api(self):
        self.code=0; owned=self.closer(); result=owned.close()
        self.api_factory.assert_not_called()
        record=json.loads((self.records._journal/'owned-closure.json').read_bytes())
        self.assertEqual(len(record),16)
        self.assertEqual(record['closeMethod'],'NATURAL_EXIT')
        self.assertTrue(record['technicalComputationAccepted'])
        self.assertEqual(record['scientificValidation'],'NOT_VALIDATED')
        self.assertEqual(record['qualifiedControls'],0)
        self.assertEqual(owned.diagnostic()['state'],'CLOSED_RETAINED')
        self.assertFalse(result['newNativeStartAllowed'])

    def test_owned_termination_uses_original_captured_handle_after_fresh_proof(self):
        owned=self.closer(); result=owned.close()
        self.assertEqual(self.wait_calls,[(123,1000),(123,30000)])
        self.assertEqual(self.terminate_calls,[123])
        self.assertEqual(self.proof.verify.call_count,3)
        self.assertEqual(result['closeMethod'],'OWNED_POST_RETAINED_TERMINATION')
        self.assertFalse(self.proof._locks[0]._released)

    def test_natural_exit_during_brief_wait_does_not_terminate(self):
        self.natural_exit_on_wait=0
        self.assertEqual(self.closer().close()['closeMethod'],'NATURAL_EXIT')
        self.assertEqual(self.terminate_calls,[])

    def test_preexisting_nonzero_exit_cannot_be_technical_success(self):
        self.code=7; value=self.closer().close()
        self.assertEqual(value['exitCode'],7)
        self.assertFalse(value['technicalComputationAccepted'])

    def test_failed_native_state_is_cleanup_only_even_with_zero_exit(self):
        self.code=0; self.result['conditionalComputationDeclaredComplete']=False
        self.assertFalse(self.closer().close()['technicalComputationAccepted'])

    def test_known_original_deadline_overrun_can_only_close_as_cleanup(self):
        self.mono=181; result=self.closer().close()
        self.assertTrue(result['parentMonotonicDeadlineExceeded'])
        self.assertFalse(result['technicalComputationAccepted'])

    def test_already_requested_cancel_cannot_be_technical_success(self):
        self.signals.request_cancel(); self.code=0
        self.assertFalse(self.closer().close()['technicalComputationAccepted'])

    def test_proof_failure_before_termination_preserves_live_reference_and_no_retry(self):
        self.wait_hook=lambda:setattr(self,'fail_proof',True)
        owned=self.closer()
        with self.assertRaisesRegex(Exception,'SYNTHETIC_PROOF_FAILURE'): owned.close()
        self.assertEqual(self.terminate_calls,[])
        self.assertEqual(owned.diagnostic()['state'],'UNCERTAIN_HELD')
        self.assertIs(owned._held,self.holder.held)
        with self.assertRaisesRegex(Exception,'OWNED_EXIT_REPLAY'): owned.close()

    def test_replaced_popen_handle_is_never_terminated(self):
        owned=self.closer(); self.holder.process._handle=held_fixture.Handle(456)
        with self.assertRaises(Exception): owned.close()
        self.assertEqual(self.terminate_calls,[])
        self.assertIs(owned._held._handle,self.holder.held._handle)

    def test_changed_record_held_reference_cannot_borrow_exit_from_original(self):
        self.code=0; owned=self.closer(); self.records._held=object()
        with self.assertRaisesRegex(Exception,'OWNED_EXIT_HELD_CHANGED'): owned.close()
        self.assertEqual(self.terminate_calls,[])
        self.assertFalse(owned.diagnostic()['receiptCommitted'])

    def test_exit_observed_before_receipt_io_failure_remains_truthfully_stopped(self):
        self.code=0; owned=self.closer()
        with patch.object(pub,'_write_control',side_effect=OSError('SYNTHETIC_IO_FAILURE')):
            with self.assertRaises(OSError): owned.close()
        diagnostic=owned.diagnostic()
        self.assertEqual(diagnostic['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertTrue(diagnostic['processExitObserved'])
        self.assertFalse(diagnostic['receiptCommitted'])

    def test_terminate_exception_after_actual_exit_never_invents_alive_or_retries(self):
        def fail(): self.code=0; raise OSError('SYNTHETIC_TERMINATE_FAILURE')
        self.terminate_hook=fail; owned=self.closer()
        with self.assertRaises(OSError): owned.close()
        self.assertEqual(owned.diagnostic()['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertEqual(self.terminate_calls,[123])

    def test_late_uncertainty_after_receipt_preserves_file_without_acceptance(self):
        self.code=0; owned=self.closer(); original=pub._write_control
        def write(path,value):
            result=original(path,value)
            (self.records._journal/'supervision-uncertain.json').write_bytes(b'SYNTHETIC_PARTIAL')
            return result
        with patch.object(pub,'_write_control',side_effect=write):
            with self.assertRaisesRegex(Exception,'OWNED_EXIT_FENCE'): owned.close()
        self.assertTrue((self.records._journal/'owned-closure.json').exists())
        self.assertFalse(owned.diagnostic()['receiptCommitted'])
        self.assertTrue(owned.diagnostic()['processExitObserved'])

    def test_receipt_deadline_crossing_preserves_uncertainty_and_historical_bytes(self):
        self.code=0; owned=self.closer(); original=pub._write_control
        def write(path,value):
            result=original(path,value); self.mono=181; return result
        with patch.object(pub,'_write_control',side_effect=write):
            with self.assertRaisesRegex(Exception,'OWNED_EXIT_DEADLINE_CROSSED_DURING_RECEIPT'): owned.close()
        self.assertEqual(owned.diagnostic()['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertFalse(owned.diagnostic()['receiptCommitted'])

    def test_final_identity_read_crossing_original_deadline_preserves_exit_not_acceptance(self):
        self.code=0; owned=self.closer(); original=Path.open; injected=False
        def read(path,*args,**kwargs):
            nonlocal injected
            result=original(path,*args,**kwargs)
            if path==self.records._journal/'owned-closure.json' and \
                    inspect.currentframe().f_back.f_code.co_name=='_post_receipt_verify':
                self.mono=182; injected=True
            return result
        with patch.object(Path,'open',read):
            with self.assertRaisesRegex(Exception,'OWNED_EXIT_DEADLINE_CROSSED_DURING_RECEIPT'):
                owned.close()
        self.assertTrue(injected)
        self.assertEqual(owned.diagnostic()['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertTrue(owned.diagnostic()['processExitObserved'])
        self.assertFalse(owned.diagnostic()['receiptCommitted'])
        historical=json.loads((self.records._journal/'owned-closure.json').read_bytes())
        self.assertTrue(historical['technicalComputationAccepted'])
        self.assertFalse(historical['parentMonotonicDeadlineExceeded'])
        with self.assertRaisesRegex(Exception,'OWNED_EXIT_REPLAY'): owned.close()

    def test_reconstruction_of_closer_on_same_records_is_rejected(self):
        self.closer()
        with self.assertRaisesRegex(Exception,'OWNED_EXIT_RECONSTRUCTION'): self.closer()

    def test_identical_receipt_replacement_in_last_publication_recheck_is_rejected(self):
        self.code=0; owned=self.closer(); calls=0
        def recheck():
            nonlocal calls
            calls+=1
            if calls==2:
                p=self.records._journal/'owned-closure.json'; replacement=p.with_name('replacement.json')
                replacement.write_bytes(p.read_bytes()); replacement.replace(p)
        self.proof._live.verify.side_effect=recheck
        with self.assertRaises(Exception): owned.close()
        self.assertEqual(owned.diagnostic()['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')

    def test_memory_uncertainty_during_last_receipt_readback_is_not_hidden(self):
        self.code=0; owned=self.closer(); original=pub._hash_bounded; calls=0
        def digest(path,size,info):
            nonlocal calls
            result=original(path,size,info)
            if path==self.records._journal/'owned-closure.json':
                calls+=1
                if calls==2: self.signals._fail()
            return result
        with patch.object(pub,'_hash_bounded',side_effect=digest):
            with self.assertRaisesRegex(Exception,'OWNED_EXIT_UNCERTAIN'): owned.close()
        self.assertFalse(owned.diagnostic()['receiptCommitted'])

    def test_fence_during_last_receipt_readback_is_rechecked(self):
        self.code=0; owned=self.closer(); original=pub._hash_bounded; calls=0
        def digest(path,size,info):
            nonlocal calls
            result=original(path,size,info)
            if path==self.records._journal/'owned-closure.json':
                calls+=1
                if calls==2: (self.records._journal/'supervision-uncertain.json').write_bytes(b'SYNTHETIC')
            return result
        with patch.object(pub,'_hash_bounded',side_effect=digest):
            with self.assertRaisesRegex(Exception,'OWNED_EXIT_FENCE'): owned.close()
        self.assertTrue(owned.diagnostic()['processExitObserved'])

    def pinned_start(self):
        path=self.records._journal/'start-consumed.json'; raw=b'SYNTHETIC_ORIGINAL_START'
        path.write_bytes(raw)
        row=dict(sha256=pub.hashlib.sha256(raw).hexdigest(),byteLength=len(raw))
        self.records._pins.append((path,row,pub._snapshot(path,row)))
        return path,raw

    def late_original_pin(self,replace=False):
        self.code=0; owned=self.closer(); path,raw=self.pinned_start()
        original=pub._hash_bounded; calls=0
        def digest(target,size,info):
            nonlocal calls
            result=original(target,size,info)
            if target==self.records._journal/'owned-closure.json':
                calls+=1
                if calls==2:
                    if replace:
                        other=path.with_name('replacement.json'); other.write_bytes(raw); other.replace(path)
                    else: path.write_bytes(b'X'*len(raw))
            return result
        with patch.object(pub,'_hash_bounded',side_effect=digest):
            with self.assertRaises(Exception): owned.close()
        self.assertEqual(owned.diagnostic()['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertTrue(owned.diagnostic()['processExitObserved'])
        self.assertFalse(owned.diagnostic()['receiptCommitted'])
        self.assertTrue((self.records._journal/'owned-closure.json').exists())
        with self.assertRaisesRegex(Exception,'OWNED_EXIT_REPLAY'): owned.close()

    def test_original_start_changed_during_last_receipt_readback_blocks_commit(self):
        self.late_original_pin()

    def test_identical_original_start_replacement_during_last_readback_blocks_commit(self):
        self.late_original_pin(replace=True)

    def test_cancel_bytes_changed_during_last_receipt_readback_block_commit(self):
        self.code=0; self.signals.request_cancel(); owned=self.closer()
        original=pub._hash_bounded; calls=0
        def digest(target,size,info):
            nonlocal calls
            result=original(target,size,info)
            if target==self.records._journal/'owned-closure.json':
                calls+=1
                if calls==2: (self.records._work/'cancel.json').write_bytes(b'SYNTHETIC_CHANGED_CANCEL')
            return result
        with patch.object(pub,'_hash_bounded',side_effect=digest):
            with self.assertRaises(Exception): owned.close()
        self.assertEqual(owned.diagnostic()['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertFalse(owned.diagnostic()['receiptCommitted'])

    def test_signal_read_after_final_pin_hash_cannot_hide_original_pin_change(self):
        self.code=0; self.signals.request_cancel(); owned=self.closer(); path,raw=self.pinned_start()
        original=pub._hash_bounded; receipt_reads=0
        def digest(target,size,info):
            nonlocal receipt_reads
            result=original(target,size,info)
            if target==self.records._journal/'owned-closure.json': receipt_reads+=1
            if target==self.records._work/'cancel.json' and receipt_reads==2:
                path.write_bytes(b'X'*len(raw))
            return result
        with patch.object(pub,'_hash_bounded',side_effect=digest):
            with self.assertRaisesRegex(Exception,'OWNED_EXIT_FINAL_IDENTITY_CHANGED'): owned.close()
        self.assertTrue(owned.diagnostic()['processExitObserved'])
        self.assertFalse(owned.diagnostic()['receiptCommitted'])

    def test_initial_cancel_outside_signals_changed_by_final_clock_callback_is_rejected(self):
        self.code=0; path=self.records._work/'cancel.json'
        pub._write_control(path,dict(protocol='DSG_NATIVE_LINEAR_CANCEL_V1',
            operationRef=self.records._binding['operationRef'],requested=True))
        self.assertEqual(self.signals._pins,[])
        owned=self.closer(); original_hash=pub._hash_bounded; original_clock=self.records._budget.check
        receipt_reads=0; changed=False
        def digest(target,size,info):
            nonlocal receipt_reads
            result=original_hash(target,size,info)
            if target==self.records._journal/'owned-closure.json': receipt_reads+=1
            return result
        def clock():
            nonlocal changed
            result=original_clock()
            if receipt_reads==2 and not changed:
                path.write_bytes(b'SYNTHETIC_CHANGED_INITIAL_CANCEL'); changed=True
            return result
        with patch.object(pub,'_hash_bounded',side_effect=digest), patch.object(
                self.records._budget,'check',side_effect=clock):
            with self.assertRaisesRegex(Exception,'OWNED_EXIT_FINAL_IDENTITY_CHANGED'): owned.close()
        self.assertEqual(owned.diagnostic()['state'],'EXIT_VERIFIED_EVIDENCE_UNCERTAIN')
        self.assertFalse(owned.diagnostic()['receiptCommitted'])


class OwnedClosureCompositionTests(unittest.TestCase):
    def test_real_opaque_byte_composition_and_natural_exit_receipt_with_fake_process_only(self):
        fixture=retained_fixture.RetainedVerificationTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        fixture.publish(); proof=fixture.proof()
        with patch.object(fixture.case.holder.Queries,'poll',return_value=0), patch.object(
                closure,'_WindowsOwnedExit',side_effect=AssertionError('NO_ACTUAL_WAIT_OR_TERMINATION')):
            owned=closure.OwnedNativeClosure(proof); result=owned.close()
        self.assertEqual(owned.diagnostic()['state'],'CLOSED_RETAINED')
        self.assertEqual(result['closeMethod'],'NATURAL_EXIT')
        self.assertEqual(result['scientificValidation'],'NOT_VALIDATED')
        self.assertEqual(result['qualifiedControls'],0)
        self.assertFalse(fixture.lock._released)


if __name__=='__main__': unittest.main()
