"""Offline journal crash/concurrency tests. No adaptive production job exists."""
from concurrent.futures import ThreadPoolExecutor
import copy
import unittest
from unittest.mock import patch

from .adaptive_ledger import DecisionJournal, VERSION, NATIVE_RECEIPT_VERSION
from .broker import Broker, ProtocolError, encode, decode
from .intake import sha
from tools.scientific_registry.ingestion_storage import MemoryStore, immutable, Conflict

JOB = 'PIAI_' + 'd' * 32


class JournalTests(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.broker = Broker(self.store, 'a' * 32)
        self.journal = DecisionJournal(self.broker)
        self.policy = {'version': VERSION, 'catalogSha256': 'a' * 64, 'runtimeSha256': 'b' * 64,
                       'inputSetSha256': 'c' * 64, 'mode': 'LRGB', 'model': 'test-model',
                       'dataTransferConfirmed': True, 'pixelStatisticsConfirmed': True}
        self.policy_sha = sha(self.policy)
        immutable(self.store, 'science/adaptive-policies/' + self.policy_sha, encode(self.policy))
        # Future adapter authority is synthetic here. V1 Broker.create cannot
        # create this mode, and no new HTTP route or native dispatch is installed.
        self.broker._mutate(lambda state, now: state['jobs'].append(
            {'jobId': JOB, 'request': {'aiMode': 'OPENAI_API_ADAPTIVE'}, 'state': 'RUNNING',
             'cancelRequested': False, 'adaptivePolicySha256': self.policy_sha}))
        self.refs = {k: self.policy[k] for k in ('catalogSha256', 'runtimeSha256', 'inputSetSha256')}
        self.refs.update(policySha256=self.policy_sha, evidenceSha256='e' * 64)
        self.journal.open(JOB, self.policy_sha)

    def record(self, reservation, action='EXECUTE_GRAPH'):
        return self.journal.record(reservation, {'action': action, 'decisionSha256': 'f' * 64},
                                   {'input_tokens': 40, 'output_tokens': 60, 'total_tokens': 100})

    def receipt(self, cursor, **changes):
        value = {'version': NATIVE_RECEIPT_VERSION, 'jobId': JOB, 'ordinal': cursor['ordinal'], 'decisionResultSha256': cursor['resultSha256'],
                 'runtimeSha256': self.policy['runtimeSha256'], 'checkpointSha256': '1' * 64,
                 'historySha256': '2' * 64, 'status': 'CHECKPOINT_VERIFIED', **changes}
        digest = sha(value)
        immutable(self.store, 'science/adaptive-native/' + digest, encode(value))
        return digest

    def test_concurrent_reservation_has_exactly_one_sender(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: self.journal.reserve(JOB, self.refs), range(8)))
        self.assertEqual(sum(r['sendAllowed'] for r in results), 1)
        self.assertTrue(all(r['request']['ordinal'] == 0 for r in results))

    def test_restart_lost_response_never_resends_or_advances(self):
        self.journal.reserve(JOB, self.refs)
        restarted = DecisionJournal(Broker(self.store, 'a' * 32))
        replay = restarted.reserve(JOB, self.refs)
        self.assertFalse(replay['sendAllowed'])
        cursor = restarted.reconcile(JOB)
        self.assertEqual(cursor['state'], 'RESERVED')
        self.assertFalse(cursor['usageComplete'])
        self.assertEqual(cursor['ordinal'], 0)
        with self.assertRaises(Conflict):
            restarted.reserve(JOB, {**self.refs, 'evidenceSha256': '9' * 64})

    def test_crash_after_result_write_recovers_once_without_send(self):
        reservation = self.journal.reserve(JOB, self.refs)
        with patch.object(self.journal, 'reconcile', side_effect=RuntimeError('synthetic crash')):
            with self.assertRaises(RuntimeError):
                self.record(reservation)
        restarted = DecisionJournal(Broker(self.store, 'a' * 32))
        first = restarted.reconcile(JOB)
        self.assertEqual(first, restarted.reconcile(JOB))
        self.assertEqual(first['usage']['total_tokens'], 100)
        self.assertTrue(first['usageComplete'])
        self.assertEqual(first['state'], 'AWAITING_EXECUTION')
        with self.assertRaises(ProtocolError):
            restarted.reserve(JOB, self.refs)

    def test_decision_does_not_replace_native_receipt(self):
        cursor = self.record(self.journal.reserve(JOB, self.refs))
        with self.assertRaisesRegex(ProtocolError, 'NATIVE_RECEIPT_REQUIRED'):
            self.journal.checkpoint(JOB, cursor['resultSha256'], cursor['resultSha256'])
        wrong = self.receipt(cursor, runtimeSha256='0' * 64)
        with self.assertRaisesRegex(ProtocolError, 'RUNTIME_BINDING'):
            self.journal.checkpoint(JOB, wrong, cursor['resultSha256'])
        receipt = self.receipt(cursor)
        next_cursor = self.journal.checkpoint(JOB, receipt, cursor['resultSha256'])
        self.assertEqual(next_cursor['ordinal'], 1)
        self.assertEqual(next_cursor['parentReceiptSha256'], receipt)
        with self.assertRaisesRegex(ProtocolError, 'EXECUTION_BINDING'):
            self.journal.checkpoint(JOB, receipt, cursor['resultSha256'])
        next_reservation = self.journal.reserve(JOB, {**self.refs, 'evidenceSha256': '8' * 64})
        self.assertEqual(next_reservation['request']['parentReceiptSha256'], receipt)
        stopped = self.record(next_reservation, 'STOP_FOR_REVIEW')
        self.assertEqual(stopped['usage']['total_tokens'], 200)
        with self.assertRaisesRegex(ProtocolError, 'PHASE_CLOSED'):
            self.journal.reserve(JOB, self.refs)

    def test_source_runtime_catalog_policy_or_owner_cannot_be_changed(self):
        for key in ('inputSetSha256', 'runtimeSha256', 'catalogSha256', 'policySha256'):
            with self.subTest(key=key), self.assertRaises(ProtocolError):
                self.journal.reserve(JOB, {**self.refs, key: '9' * 64})
        reservation = self.journal.reserve(JOB, self.refs)
        forged = {**reservation, 'owner': '9' * 32}
        with self.assertRaisesRegex(ProtocolError, 'RESERVATION_BINDING'):
            self.record(forged)
        with self.assertRaisesRegex(ProtocolError, 'POLICY_REQUIRED'):
            self.journal.open(JOB, '9' * 64)

    def test_unknown_usage_not_zero_and_unsupported_actions_cannot_progress(self):
        reservation = self.journal.reserve(JOB, self.refs)
        for usage in (None, {'input_tokens': True, 'output_tokens': 1, 'total_tokens': 2},
                      {'input_tokens': 40, 'output_tokens': 60, 'total_tokens': 99}):
            with self.assertRaisesRegex(ProtocolError, 'USAGE'):
                self.journal.record(reservation, {'action': 'EXECUTE_GRAPH', 'decisionSha256': 'f' * 64}, usage)
        with self.assertRaisesRegex(ProtocolError, 'CHECKPOINT_ONLY'):
            self.record(reservation, 'CONTINUE')
        self.assertFalse(self.journal.reconcile(JOB)['usageComplete'])

    def test_cancel_or_withdrawal_blocks_new_reservation(self):
        self.broker._mutate(lambda state, now: state['jobs'][0].update(cancelRequested=True))
        with self.assertRaisesRegex(ProtocolError, 'JOB_INACTIVE'):
            self.journal.reserve(JOB, self.refs)
        self.broker._mutate(lambda state, now: state['jobs'][0].update(cancelRequested=False))
        self.broker._mutate(lambda state, now: state.update(withdrawnIntakes=[JOB.removeprefix('PIAI_')]))
        with self.assertRaisesRegex(ProtocolError, 'JOB_INACTIVE'):
            self.journal.reserve(JOB, self.refs)


if __name__ == '__main__':
    unittest.main()
