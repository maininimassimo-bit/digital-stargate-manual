"""Mock process and MemoryStore integration; no native or cloud execution."""
import datetime as dt
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_native_supervisor as fixtures
from tools.scientific_transients.attempt_journal import AttemptJournal
from tools.scientific_transients.receipt_coordinator import ReceiptOutbox
from tools.scientific_transients.local_driver import LocalDriver, reconcile_retained


class DriverTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.SupervisorTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.jroot = self.f.fixture.root / 'driver-journals'; self.jroot.mkdir()
        self.oroot = self.f.fixture.root / 'driver-outboxes'; self.oroot.mkdir()
        self.time = 0

    def prepare(self, **kwargs):
        f = self.f
        return LocalDriver.prepare(f.local, self.jroot, self.oroot, f.journal.anchor['identity'],
            f.directory, f.fixture.operation, f.transport, f.claim['leaseToken'],
            supervisor_options={'spawn': f.spawn, 'clock': lambda: self.time,
                'timeout': 10, 'engine': f.fixture.engine, 'catalog': f.fixture.catalog},
            clock=lambda: self.time, **kwargs)

    def reopened(self, driver):
        journal = AttemptJournal(driver.journal.directory, driver.journal.anchor['identity'])
        return journal, ReceiptOutbox(driver.outbox.directory, journal)

    def test_explicit_polling_completion_and_no_second_start(self):
        d = self.prepare(); self.assertEqual(d.start()['state'], 'RUNNING')
        posts = len(self.f.transport.posts)
        self.assertEqual(d.step()['state'], 'POLL_NOT_DUE')
        self.assertEqual(len(self.f.transport.posts), posts)
        self.f.native('COMPLETED'); self.time = 2
        self.assertEqual(d.step()['state'], 'COMPLETED')
        self.assertEqual(self.f.starts, 1)
        with self.assertRaises(ProtocolError): d.start()
        with self.assertRaises(ProtocolError): d.step()
        for path in self.f.fixture.root.rglob('*.json'):
            self.assertNotIn(self.f.claim['leaseToken'].encode(), path.read_bytes())

    def test_cancel_observed_before_start_never_launches(self):
        self.f.cancel(); d = self.prepare()
        self.assertEqual(d.start()['state'], 'CANCELLED'); self.assertEqual(self.f.starts, 0)

    def test_lost_ack_freezes_and_restart_does_not_post(self):
        d = self.prepare(); self.f.transport.lose = True
        self.assertEqual(d.start()['state'], 'RECOVERY_REQUIRED')
        journal, outbox = self.reopened(d); posts = len(self.f.transport.posts)
        result = reconcile_retained(journal, outbox, self.f.transport)
        self.assertTrue(result['currentRemoteMatchesLastReceipt'])
        self.assertEqual(result['receiptDisposition'], 'ACKNOWLEDGED')
        self.assertEqual(result['localState'], 'RECOVERY_REQUIRED')
        self.assertFalse(result['serverRecoveryCleared'])
        self.assertEqual(len(self.f.transport.posts), posts); self.assertEqual(self.f.starts, 0)

    def test_historical_ack_not_current_remote_state(self):
        d = self.prepare(); d.start()
        self.f.now += dt.timedelta(seconds=901)
        journal, outbox = self.reopened(d); posts = len(self.f.transport.posts)
        result = reconcile_retained(journal, outbox, self.f.transport)
        self.assertEqual(result['remoteState'], 'RECOVERY_REQUIRED')
        self.assertEqual(result['receiptDisposition'], 'ACKNOWLEDGED')
        self.assertFalse(result['currentRemoteMatchesLastReceipt'])
        self.assertEqual(len(self.f.transport.posts), posts); self.assertFalse(self.f.process.closed)

    def test_restart_prepared_or_alternate_roots_never_reuses_run(self):
        d = self.prepare()
        with self.assertRaises(ProtocolError): self.prepare()
        self.jroot = self.f.fixture.root / 'alternative-journals'; self.jroot.mkdir()
        self.oroot = self.f.fixture.root / 'alternative-outboxes'; self.oroot.mkdir()
        with self.assertRaises(FileExistsError): self.prepare()
        journal, outbox = self.reopened(d)
        result = reconcile_retained(journal, outbox, self.f.transport)
        self.assertEqual(result['receiptDisposition'], 'NO_RETAINED_RECEIPT')
        self.assertEqual(self.f.starts, 0)

    def test_invalid_cadence_and_clock_regression(self):
        for value in [True, float('nan'), float('inf'), 0, 31]:
            with self.assertRaises(ProtocolError): self.prepare(poll_interval=value)
        d = self.prepare(); d.start(); self.time = -1
        with self.assertRaises(ProtocolError): d.step()
        self.assertFalse(self.f.process.closed)
        self.time = 2
        with self.assertRaises(ProtocolError): d.step()

    def test_corrupt_local_or_remote_evidence_refuses_reconciliation(self):
        d = self.prepare(); d.start(); journal, outbox = self.reopened(d)
        snapshot = journal.directory / journal.anchor['snapshot'][0]['path']
        snapshot.write_bytes(b'altered')
        with self.assertRaises(ProtocolError): reconcile_retained(journal, outbox, self.f.transport)
        self.assertFalse(self.f.process.closed)

    def test_corrupt_registry_refused_before_prepare(self):
        (self.f.directory / 'parameters.json').write_bytes(b'altered')
        with self.assertRaises(ProtocolError): self.prepare()
        self.assertFalse((self.f.directory / 'driver-reservation.json').exists())
        self.assertEqual(self.f.starts, 0)

    def test_partial_prepare_preserved_and_reuse_refused(self):
        with patch('tools.scientific_transients.local_driver.NativeSupervisor', side_effect=OSError('synthetic')):
            with self.assertRaises(OSError): self.prepare()
        attempt = self.jroot / self.f.claim['attemptId']
        self.assertTrue((attempt / 'driver' / 'prepare-failed.json').is_file())
        self.assertTrue((self.f.directory / 'driver-reservation.json').is_file())
        with self.assertRaises(ProtocolError): self.prepare()
        self.assertEqual(self.f.starts, 0)

    def test_timeout_freezes_driver_and_preserves_process(self):
        d = self.prepare(); d.start(); self.time = 10
        self.assertEqual(d.step()['state'], 'RECOVERY_REQUIRED')
        with self.assertRaises(ProtocolError): d.step()
        self.assertFalse(self.f.process.closed)
        self.assertTrue((self.f.directory / 'cancel.json').exists())

    def test_remote_identity_mismatch_and_live_outbox_refused(self):
        d = self.prepare()
        with self.assertRaises(ProtocolError): reconcile_retained(d.journal, d.outbox, self.f.transport)
        journal, outbox = self.reopened(d)
        original = self.f.transport.request
        def mismatch(path):
            remote = original(path); remote['rootId'] = 'f' * 32; return remote
        self.f.transport.request = mismatch
        with self.assertRaises(ProtocolError): reconcile_retained(journal, outbox, self.f.transport)
        self.assertEqual(self.f.starts, 0)

    def test_unexpected_start_exception_freezes_without_replay_or_tick(self):
        d = self.prepare()
        with patch.object(d.supervisor, 'start', side_effect=OSError('synthetic persistence failure')):
            with self.assertRaises(OSError): d.start()
        with self.assertRaises(ProtocolError): d.start()
        self.time = 2
        with self.assertRaises(ProtocolError): d.step()
        self.assertEqual(self.f.starts, 0)


if __name__ == '__main__':
    unittest.main()
