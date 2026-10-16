"""Synthetic Popen-shaped objects and mocked Win32 queries; no process starts."""
import subprocess
import os
import unittest
from unittest.mock import patch, Mock

from tools.scientific_transients import native_held_process as held


class Handle:
    def __init__(self, value=123): self.value=value
    def __int__(self): return self.value


class HeldNativeProcessTests(unittest.TestCase):
    def setUp(self):
        self.process=object.__new__(subprocess.Popen)
        self.process._child_created=False  # Prevent Popen destructor from polling a synthetic handle.
        self.process._handle=Handle(); self.process.pid=4242
        self.value=(4242,'0123456789abcdef')
        case=self
        class Queries:
            def identity(self, handle):
                case.handles.append(handle)
                if case.failure: raise OSError('SYNTHETIC_QUERY_FAILURE')
                return case.value
            def poll(self, handle): raise AssertionError('poll must be mocked')
        self.failure=False; self.handles=[]
        self.Queries=Queries
        self.patch=patch.object(held,'_WindowsProcessQueries',Queries); self.patch.start(); self.addCleanup(self.patch.stop)
        self.held=held.HeldNativeProcess(self.process)

    def observe(self, code):
        with patch.object(self.Queries,'poll',return_value=code) as poll:
            outcome=self.held.observe(); poll.assert_called_once_with(123)
            return outcome

    def test_capture_uses_same_handle_and_exports_copy(self):
        identity=self.held.capture()
        self.assertEqual(identity,dict(nativeProcessId='4242',processCreationFileTime='0123456789abcdef'))
        identity['nativeProcessId']='1'
        self.assertEqual(self.held.identity()['nativeProcessId'],'4242')
        self.assertEqual(set(self.handles),{123})
        self.assertTrue(self.observe(None)['identityTrusted'])

    def test_persisted_pid_or_dictionary_cannot_be_adopted(self):
        for value in [4242,dict(pid=4242),None]:
            with self.assertRaisesRegex(Exception,'HELD_PROCESS_POPEN_REQUIRED'): held.HeldNativeProcess(value)

    def test_capture_failure_keeps_original_for_observation_and_never_rearms(self):
        self.failure=True
        with self.assertRaises(OSError): self.held.capture()
        self.failure=False
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_CAPTURE_REPLAY'): self.held.capture()
        outcome=self.observe(None)
        self.assertEqual(outcome['processObservation'],'HELD_RUNNING')
        self.assertFalse(outcome['identityTrusted'])
        self.assertFalse(outcome['processClosureAuthorized'])

    def test_pid_disagreement_rejected(self):
        self.process.pid=4243
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_PID'): self.held.capture()
        self.assertFalse(self.observe(0)['identityTrusted'])

    def test_replaced_equal_handle_object_is_uncertain(self):
        self.held.capture(); self.process._handle=Handle()
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_HANDLE_CHANGED'): self.held.verify()
        self.assertFalse(self.observe(None)['identityTrusted'])

    def test_foreign_popen_handle_is_never_polled_for_exit(self):
        self.held.capture(); original=self.process._handle
        self.process._handle=Handle(456)
        with patch.object(subprocess.Popen,'poll',side_effect=AssertionError('FOREIGN_POLL')):
            outcome=self.observe(7)
        self.assertIs(self.held._handle,original)
        self.assertEqual(outcome['exitCode'],7)
        self.assertFalse(outcome['identityTrusted'])

    def test_changed_handle_value_is_uncertain(self):
        self.held.capture(); self.process._handle.value=124
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_NO_CAPTURED_HANDLE'): self.observe(None)

    def test_creation_time_change_is_sticky(self):
        self.held.capture(); self.value=(4242,'0123456789abcdee')
        self.assertFalse(self.observe(None)['identityTrusted'])
        self.value=(4242,'0123456789abcdef')
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_IDENTITY_UNCERTAIN'): self.held.identity()
        self.assertEqual(self.observe(0)['processObservation'],'HELD_EXITED')

    def test_exit_observation_is_stable_and_never_grants_restart(self):
        self.held.capture()
        for code in [None,7,7]:
            outcome=self.observe(code); self.assertFalse(outcome['newNativeStartAllowed'])
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_EXIT_CHANGED'): self.observe(None)

    def test_non_integer_exit_is_rejected(self):
        self.held.capture()
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_EXIT_CODE'): self.observe(True)

    def test_query_failure_does_not_hide_confirmed_exit(self):
        self.held.capture(); self.failure=True
        outcome=self.observe(9)
        self.assertEqual(outcome['exitCode'],9)
        self.assertEqual(outcome['processObservation'],'HELD_EXITED')
        self.assertFalse(outcome['identityTrusted'])

    def test_poll_exception_does_not_drop_process(self):
        self.held.capture()
        with patch.object(self.Queries,'poll',side_effect=OSError('SYNTHETIC_POLL')):
            with self.assertRaises(OSError): self.held.observe()
        self.assertIs(self.held._process,self.process)
        self.assertFalse(self.observe(None)['identityTrusted'])

    def test_handle_replacement_during_poll_is_not_trusted(self):
        self.held.capture()
        def changed(handle):
            self.assertEqual(handle,123); self.process._handle=Handle(456); return 0
        with patch.object(self.Queries,'poll',side_effect=changed):
            outcome=self.held.observe()
        self.assertEqual(outcome['exitCode'],0)
        self.assertFalse(outcome['identityTrusted'])


@unittest.skipUnless(os.name=='nt','Win32 current-process query only')
class WindowsQueryTests(unittest.TestCase):
    def test_ctypes_binding_on_current_process_without_start_or_reopen(self):
        # Windows pseudo handle for this test process only; public capture rejects it.
        pid,creation=held._WindowsProcessQueries().identity(-1)
        self.assertEqual(pid,os.getpid())
        self.assertRegex(creation,'^[0-9a-f]{16}$')
        self.assertIsNone(held._WindowsProcessQueries().poll(-1))


class QueryPollTests(unittest.TestCase):
    def query(self,status):
        query=object.__new__(held._WindowsProcessQueries); query.dll=Mock()
        query.dll.WaitForSingleObject.return_value=status
        return query

    def test_timeout_does_not_read_an_exit_code(self):
        query=self.query(258)
        self.assertIsNone(query.poll(123))
        query.dll.WaitForSingleObject.assert_called_once_with(123,0)
        query.dll.GetExitCodeProcess.assert_not_called()

    def test_signaled_exit_259_is_not_running(self):
        query=self.query(0)
        def exit_code(handle,pointer):
            self.assertEqual(handle,123); pointer._obj.value=259; return 1
        query.dll.GetExitCodeProcess.side_effect=exit_code
        self.assertEqual(query.poll(123),259)

    def test_unknown_wait_status_is_not_completion(self):
        query=self.query(128)
        with self.assertRaisesRegex(Exception,'HELD_PROCESS_WAIT_RESULT'): query.poll(123)
        query.dll.GetExitCodeProcess.assert_not_called()


if __name__=='__main__': unittest.main()
