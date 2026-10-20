"""Synthetic private bundles and fake held queries; no process or cloud actions."""
import json
import unittest
from unittest.mock import patch

from tools.scientific_transients import native_publication as pub
from tools.scientific_transients import test_native_run_records as fixtures
from tools.scientific_transients.native_supervision_signals import NativeSupervisionSignals
from tools.scientific_transients.native_held_process import HeldNativeProcess


class NativeSupervisionSignalsTests(unittest.TestCase):
    def setUp(self):
        self.case=fixtures.NativeRunRecordsTests(); self.case.setUp(); self.addCleanup(self.case.doCleanups)
        self.records=self.case.records(); self.signals=NativeSupervisionSignals(self.records)
        self.fixture=self.case.fixture

    def consume_and_adopt(self):
        self.case.consume(self.records); self.signals.adopt_held(self.case.holder.held)

    def mark(self,code=None):
        with patch.object(self.case.holder.Queries,'poll',return_value=code):
            return self.signals.mark_uncertain('SYNTHETIC_FAILURE')

    def test_cancel_is_exclusive_and_never_proves_stop(self):
        result=self.signals.request_cancel()
        value=json.loads((self.fixture.work/'cancel.json').read_bytes())
        self.assertEqual(value,dict(protocol='DSG_NATIVE_LINEAR_CANCEL_V1',operationRef=self.fixture.operation,requested=True))
        self.assertFalse(result['processStopVerified'])
        before=(self.fixture.work/'cancel.json').read_bytes()
        with self.assertRaisesRegex(Exception,'SUPERVISION_CANCEL_REPLAY'): self.signals.request_cancel()
        self.assertEqual((self.fixture.work/'cancel.json').read_bytes(),before)

    def test_signals_cannot_be_reconstructed_from_same_context(self):
        with self.assertRaisesRegex(Exception,'SUPERVISION_SIGNALS_RECONSTRUCTION'): NativeSupervisionSignals(self.records)

    def test_preexisting_partial_cancel_is_preserved_and_latches_uncertainty(self):
        path=self.fixture.work/'cancel.json'; path.write_bytes(b'{partial')
        with self.assertRaises(FileExistsError): self.signals.request_cancel()
        self.assertEqual(path.read_bytes(),b'{partial')
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])
        self.assertTrue(self.records.diagnostic()['failed'])
        self.mark()
        self.assertTrue((self.fixture.journal/'supervision-uncertain.json').exists())

    def test_no_handle_uncertainty_has_no_fabricated_exit_or_start_hash(self):
        self.mark()
        value=json.loads((self.fixture.journal/'supervision-uncertain.json').read_bytes())
        self.assertEqual(value['processObservation'],'NO_HANDLE_AMBIGUOUS')
        self.assertIsNone(value['exitCode']); self.assertIsNone(value['startConsumedSha256'])
        self.assertFalse(value['newNativeStartAllowed']); self.assertEqual(value['launchCountBound'],1)

    def test_held_running_observation_is_bound_to_consumed_start(self):
        self.consume_and_adopt(); self.mark()
        value=json.loads((self.fixture.journal/'supervision-uncertain.json').read_bytes())
        self.assertEqual(value['processObservation'],'HELD_RUNNING')
        self.assertEqual(value['startConsumedSha256'],self.records._start_sha)
        self.assertIsNone(value['exitCode'])

    def test_actual_held_exit_is_not_hidden_by_identity_uncertainty(self):
        self.consume_and_adopt(); self.case.holder.failure=True; self.mark(7)
        value=json.loads((self.fixture.journal/'supervision-uncertain.json').read_bytes())
        self.assertEqual(value['processObservation'],'HELD_EXITED'); self.assertEqual(value['exitCode'],7)
        self.assertTrue(self.signals.diagnostic()['processReferenceRetained'])
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])

    def test_poll_failure_does_not_invent_observation_or_release_reference(self):
        self.consume_and_adopt()
        with patch.object(self.case.holder.Queries,'poll',side_effect=OSError('SYNTHETIC_POLL')):
            with self.assertRaises(OSError): self.signals.mark_uncertain('SYNTHETIC_FAILURE')
        self.assertFalse((self.fixture.journal/'supervision-uncertain.json').exists())
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])
        self.assertIs(self.signals._held,self.case.holder.held)
        with self.assertRaisesRegex(Exception,'SUPERVISION_UNCERTAINTY_REPLAY'): self.mark()

    def test_uncertainty_io_failure_stays_live_and_monouse(self):
        with patch.object(pub,'_write_control',side_effect=OSError('SYNTHETIC_IO')):
            with self.assertRaises(OSError): self.mark()
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])
        self.assertFalse(self.signals.diagnostic()['uncertaintyCommitted'])
        with self.assertRaisesRegex(Exception,'SUPERVISION_UNCERTAINTY_REPLAY'): self.mark()

    def test_known_expiry_and_clock_failure_do_not_block_stop_only_writes(self):
        self.case.mono=181
        with self.assertRaises(Exception): self.case.budget.require_running()
        self.case.mono=0
        with self.assertRaises(Exception): self.case.budget.check()
        self.signals.request_cancel(); self.mark()
        self.assertTrue(self.signals.diagnostic()['uncertaintyCommitted'])

    def test_existing_uncertainty_is_never_replaced(self):
        path=self.fixture.journal/'supervision-uncertain.json'; path.write_bytes(b'PARTIAL_ORIGINAL')
        with self.assertRaises(FileExistsError): self.mark()
        self.assertEqual(path.read_bytes(),b'PARTIAL_ORIGINAL')
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])

    def test_changed_cancel_can_be_reported_without_becoming_a_valid_cancel(self):
        self.signals.request_cancel()
        (self.fixture.work/'cancel.json').write_bytes(b'CHANGED_SYNTHETIC')
        with self.assertRaises(Exception): self.signals.verify_records()
        self.mark()
        self.assertTrue(self.signals.diagnostic()['uncertaintyCommitted'])
        self.assertFalse(self.signals.diagnostic()['newNativeStartAllowed'])

    def test_parent_metadata_cap_checked_before_uncertainty_write(self):
        (self.fixture.journal/'synthetic-padding.dat').write_bytes(b'x'*(16*pub.MIB))
        with self.assertRaisesRegex(Exception,'SUPERVISION_METADATA_AGGREGATE'): self.mark()
        self.assertFalse((self.fixture.journal/'supervision-uncertain.json').exists())
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])

    def test_failed_identity_capture_still_retains_and_observes_original_handle(self):
        self.case.consume(self.records)
        held=HeldNativeProcess(self.case.holder.process); self.case.holder.failure=True
        self.signals.adopt_held(held)
        with self.assertRaises(OSError): held.capture()
        self.mark()
        value=json.loads((self.fixture.journal/'supervision-uncertain.json').read_bytes())
        self.assertEqual(value['processObservation'],'HELD_RUNNING')
        self.assertTrue(self.signals.diagnostic()['processReferenceRetained'])

    def test_invalid_reason_is_not_serialized_and_still_blocks_reconstruction(self):
        with self.assertRaisesRegex(Exception,'SUPERVISION_UNCERTAINTY_REASON'):
            self.signals.mark_uncertain('not a machine code')
        self.assertTrue(self.signals.diagnostic()['liveUncertain'])
        self.assertFalse((self.fixture.journal/'supervision-uncertain.json').exists())
        with self.assertRaisesRegex(Exception,'SUPERVISION_SIGNALS_RECONSTRUCTION'): NativeSupervisionSignals(self.records)

    def test_cancel_is_available_after_failed_poll_without_fabricating_receipt(self):
        self.consume_and_adopt()
        with patch.object(self.case.holder.Queries,'poll',side_effect=OSError('SYNTHETIC_POLL')):
            with self.assertRaises(OSError): self.signals.mark_uncertain('SYNTHETIC_FAILURE')
        self.signals.request_cancel()
        self.assertTrue((self.fixture.work/'cancel.json').exists())
        self.assertFalse((self.fixture.journal/'supervision-uncertain.json').exists())

    def test_cancel_failure_without_file_still_consumes_same_context(self):
        with patch.object(pub,'_write_control',side_effect=OSError('SYNTHETIC_OPEN')):
            with self.assertRaises(OSError): self.signals.request_cancel()
        self.assertFalse((self.fixture.work/'cancel.json').exists())
        with self.assertRaisesRegex(Exception,'SUPERVISION_CANCEL_REPLAY'): self.signals.request_cancel()
        with self.assertRaisesRegex(Exception,'SUPERVISION_SIGNALS_RECONSTRUCTION'): NativeSupervisionSignals(self.records)


if __name__=='__main__': unittest.main()
