"""Synthetic command transport and fake lifecycle only; no native operations."""
import io
import json
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from tools.pixinsight.local_pilot.broker import encode, ProtocolError
from tools.scientific_transients import native_linear_driver as driver


def frame(name, **fields):
    return encode(dict(protocol=driver.PROTOCOL, command=name, **fields))+b'\n'


class LinearDriverTests(unittest.TestCase):
    def setUp(self):
        self.session=SimpleNamespace(assert_intact=Mock())
        self.d=driver.LinearNativeDriver(self.session)
        self.lock=SimpleNamespace(release=Mock())
        self.sup=SimpleNamespace(_start_attempted=False,_process=None,_held=None,
            _locks=[self.lock],_uncertain=Mock(),_observe=Mock(return_value=None),
            diagnostic=Mock(return_value=dict(state='PREPARED_LIVE')),start=Mock(),tick=Mock())
        self.prep=SimpleNamespace(_supervisor=self.sup,_locks=self.lock,
            prepare=Mock(return_value=self.sup),diagnostic=Mock(return_value=dict(state='PREPARED_LIVE')))
        self.factory=patch.object(driver,'LinearAttemptPreparation',return_value=self.prep).start()
        self.addCleanup(patch.stopall)

    def prepare(self):
        return self.d.dispatch(frame('PREPARE',planPath='F:/synthetic/plan.json',planSha256='a'*64,
            approvalPath='F:/synthetic/approval.json',approvalSha256='b'*64))

    def running(self, *, trusted=True, exited=False):
        self.prepare(); self.sup._start_attempted=True; self.sup._process=object(); self.sup._held=object()
        self.sup._observe.return_value=dict(identityTrusted=trusted,
            processObservation='HELD_EXITED' if exited else 'HELD_RUNNING',exitCode=0 if exited else None)

    def test_construction_and_status_never_prepare_or_start(self):
        self.d.dispatch(frame('STATUS'))
        self.factory.assert_not_called(); self.sup.start.assert_not_called()

    def test_prepare_keeps_original_objects_and_never_automatically_starts(self):
        self.prepare()
        self.assertIs(self.d._preparation,self.prep); self.assertIs(self.d._supervisor,self.sup)
        self.sup.start.assert_not_called(); self.sup.tick.assert_not_called()
        with self.assertRaisesRegex(ProtocolError,'PREPARE_REPLAY'): self.prepare()
        self.assertEqual(self.factory.call_count,1)

    def test_prepare_failure_is_consumed_and_original_context_retained(self):
        self.prep.prepare.side_effect=OSError('synthetic path must not leak')
        with self.assertRaises(OSError): self.prepare()
        self.assertIs(self.d._preparation,self.prep); self.assertIs(self.d._supervisor,self.sup)
        self.assertTrue(self.d.diagnostic()['failed'])
        self.assertEqual(self.d.diagnostic()['lastError'],'LINEAR_DRIVER_FAILURE')
        with self.assertRaisesRegex(ProtocolError,'PREPARE_REPLAY'): self.prepare()

    def test_driver_cannot_be_reconstructed_on_same_live_session(self):
        with self.assertRaisesRegex(ProtocolError,'RECONSTRUCTION'): driver.LinearNativeDriver(self.session)

    def test_start_only_on_explicit_command_and_no_replay(self):
        self.prepare(); self.d.dispatch(frame('START')); self.sup.start.assert_called_once()
        self.sup._start_attempted=True
        with self.assertRaisesRegex(ProtocolError,'START_REPLAY'): self.d.dispatch(frame('START'))
        self.assertEqual(self.sup.start.call_count,1)

    def test_observe_is_not_a_tick_or_closure(self):
        self.running(); self.d.dispatch(frame('OBSERVE'))
        self.sup._observe.assert_called_once(); self.sup.tick.assert_not_called()
        self.sup._uncertain.assert_not_called(); self.lock.release.assert_not_called()

    def test_tick_and_cancel_are_explicit_distinct_commands(self):
        self.running(); self.d.dispatch(frame('TICK')); self.d.dispatch(frame('CANCEL'))
        self.assertEqual(self.sup.tick.call_args_list, [unittest.mock.call(),unittest.mock.call(cancel=True)])

    def test_live_process_refuses_exit_and_file_release_without_cancelling(self):
        self.running()
        for name in ['EXIT','RELEASE_FILES']:
            with self.assertRaisesRegex(ProtocolError,'EXIT_NOT_VERIFIED'): self.d.dispatch(frame(name))
        self.lock.release.assert_not_called(); self.sup._uncertain.assert_not_called()
        self.assertFalse(self.d._failed); self.assertFalse(self.d._exited)

    def test_spawn_ambiguity_with_no_held_handle_refuses_release(self):
        self.prepare(); self.sup._start_attempted=True; self.sup._process=object()
        with self.assertRaisesRegex(ProtocolError,'EXIT_NOT_VERIFIED'): self.d.dispatch(frame('EXIT'))
        self.lock.release.assert_not_called()

    def test_untrusted_exit_is_observed_but_cannot_release(self):
        self.running(trusted=False,exited=True)
        with self.assertRaisesRegex(ProtocolError,'EXIT_NOT_VERIFIED'): self.d.dispatch(frame('RELEASE_FILES'))
        self.assertTrue(self.d._failed); self.sup._uncertain.assert_called_once()
        self.lock.release.assert_not_called()

    def test_trusted_exit_releases_unique_original_locks_only(self):
        self.running(exited=True); self.d.dispatch(frame('EXIT'))
        self.lock.release.assert_called_once(); self.assertTrue(self.d._exited)
        self.sup.tick.assert_not_called(); self.sup.start.assert_not_called()

    def test_never_started_preparation_can_release_but_cannot_start_after_release(self):
        self.prepare(); self.d.dispatch(frame('RELEASE_FILES'))
        with self.assertRaisesRegex(ProtocolError,'NOT_ACTIONABLE'): self.d.dispatch(frame('START'))
        self.sup.start.assert_not_called()

    def test_stream_eof_during_active_run_fences_without_termination_or_release(self):
        self.running()
        with self.assertRaisesRegex(ProtocolError,'INPUT_LOST'):
            driver.serve(self.d,io.BytesIO(),io.BytesIO())
        self.assertTrue(self.d._failed); self.sup._uncertain.assert_called_once()
        self.lock.release.assert_not_called(); self.sup.tick.assert_not_called()

    def test_oversized_frame_is_fatal_and_following_start_not_executed(self):
        self.prepare(); source=io.BytesIO(b' '*4097+b'\n'+frame('START'))
        with self.assertRaisesRegex(ProtocolError,'INPUT_LOST'): driver.serve(self.d,source,io.BytesIO())
        self.sup.start.assert_not_called()

    def test_invalid_frame_is_rejected_before_command_execution(self):
        for raw in [b'{"protocol":"x","command":"START"}\n',
                    frame('START',extra=True),b'{"command":"START","command":"START"}\n',
                    frame('PREPARE',planPath='F:/p',planSha256=True,approvalPath='F:/a',approvalSha256='a'*64)]:
            with self.assertRaises(ProtocolError): self.d.dispatch(raw)
        self.factory.assert_not_called(); self.sup.start.assert_not_called()

    def test_output_failure_keeps_context_and_marks_uncertainty(self):
        self.running(); destination=Mock(); destination.write.side_effect=BrokenPipeError('synthetic')
        with self.assertRaises(BrokenPipeError): driver.serve(self.d,io.BytesIO(frame('STATUS')),destination)
        self.assertTrue(self.d._failed); self.sup._uncertain.assert_called_once()
        self.lock.release.assert_not_called()

    def test_main_retains_driver_on_original_session_after_input_loss(self):
        with patch.object(driver.sys,'stdin',SimpleNamespace(buffer=io.BytesIO())), patch.object(
                driver.sys,'stdout',SimpleNamespace(buffer=io.BytesIO())):
            other=SimpleNamespace(assert_intact=Mock())
            with self.assertRaisesRegex(ProtocolError,'INPUT_LOST'): driver.main(other)
        self.assertIsInstance(other._linear_driver_context,driver.LinearNativeDriver)
        self.assertTrue(other._linear_driver_context._failed)
        self.factory.assert_not_called()

    def test_explicit_exit_before_any_prepare_finishes_transport(self):
        output=io.BytesIO(); result=driver.serve(self.d,io.BytesIO(frame('STATUS')+frame('EXIT')),output)
        self.assertTrue(result['driverExitCommitted'])
        replies=[json.loads(row) for row in output.getvalue().splitlines()]
        self.assertEqual(len(replies),2); self.assertTrue(all(row['ok'] for row in replies))
        self.factory.assert_not_called()


class LinearDriverCompositionTests(unittest.TestCase):
    def test_actual_opaque_preparation_and_cancel_before_start_keep_original_budget(self):
        from tools.scientific_transients import test_native_linear_preparation as fixture
        case=fixture.LinearPreparationTests(); case.setUp(); self.addCleanup(case.doCleanups)
        context=[]
        def factory(session,path,sha):
            self.assertIs(session,case.f.session)
            self.assertEqual((path,sha),(case.plan_path.as_posix(),case.plan_sha))
            result=case.context(); context.append(result); return result
        parent=driver.LinearNativeDriver(case.f.session)
        with patch.object(driver,'LinearAttemptPreparation',side_effect=factory):
            parent.dispatch(frame('PREPARE',planPath=case.plan_path.as_posix(),planSha256=case.plan_sha,
                approvalPath=case.approval_path.as_posix(),approvalSha256=case.approval_sha))
        original=context[0]; sup=parent._supervisor
        self.assertIs(parent._preparation,original)
        self.assertIs(sup._records._budget,original._budget)
        self.assertIs(sup,original._supervisor)
        self.assertFalse(sup.diagnostic()['startAttemptConsumed'])
        parent.dispatch(frame('CANCEL'))
        self.assertEqual(sup.diagnostic()['state'],'RETENTION_ONLY')
        self.assertTrue((sup._records._work/'cancel.json').is_file())
        with self.assertRaisesRegex(ProtocolError,'START_REPLAY'): parent.dispatch(frame('START'))
        case.spawn.assert_not_called()
        self.assertFalse(sup.diagnostic()['measurementAccepted'])
        self.assertEqual(parent.diagnostic()['qualifiedControls'],0)


if __name__=='__main__': unittest.main()
