"""Preserve existing state when an explicitly configured campaign starts."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_registry.ingestion_storage import BackedUpStore, MemoryStore
from tools.scientific_transients.queue import STATE_KEY, TransientQueue
from tools.scientific_transients.test_queue import BINDING, REQUEST, WORKER, ROOT


class ControlNamespaceTests(unittest.TestCase):
    def setUp(self):
        self.primary, self.backup = MemoryStore(), MemoryStore()
        self.store = BackedUpStore(self.primary, self.backup)
        self.legacy = TransientQueue(self.store, WORKER)
        self.legacy.register(BINDING)
        self.job = self.legacy.create(REQUEST)
        self.legacy.claim({'workerId': WORKER, 'rootId': ROOT})
        self.legacy_bytes = self.primary.get(STATE_KEY)
        self.backup_before = dict(self.backup.items)

    def test_new_campaign_keeps_active_legacy_state_and_backups(self):
        new = TransientQueue(self.store, 'f' * 32, state_ref='7' * 32)
        new.register(BINDING)
        job = new.create(REQUEST)
        self.assertEqual(job['state'], 'QUEUED')
        self.assertEqual(new.state_key,
                         'control/transient-analysis/' + '7' * 32 + '/state-v1.json')
        self.assertEqual(self.primary.get(STATE_KEY), self.legacy_bytes)
        for key, value in self.backup_before.items():
            self.assertEqual(self.backup.items[key], value)
        self.assertEqual(self.legacy.status(self.job['jobId'])['state'], 'RESERVED')

    def test_restart_keeps_identity_and_request_idempotency_in_selected_campaign(self):
        new = TransientQueue(self.store, 'f' * 32, state_ref='7' * 32)
        new.register(BINDING)
        expected = new.create(REQUEST)
        restarted = TransientQueue(self.store, 'f' * 32, state_ref='7' * 32)
        self.assertEqual(restarted.create(REQUEST), expected)
        before = self.primary.get(new.state_key)
        with self.assertRaisesRegex(ProtocolError, 'TRANSIENT_STATE_IDENTITY'):
            TransientQueue(self.store, 'e' * 32, state_ref='7' * 32).register(BINDING)
        self.assertEqual(self.primary.get(new.state_key), before)

    def test_invalid_reference_cannot_select_legacy_or_arbitrary_storage_paths(self):
        before = dict(self.primary.items)
        for value in ('', '../piai-state', STATE_KEY, 'A' * 32, '7' * 31,
                      '7' * 33, True, 7, '7' * 31 + '/', '7' * 32 + '\n'):
            with self.subTest(value=value), self.assertRaises(ProtocolError):
                TransientQueue(self.store, 'f' * 32, state_ref=value)
        self.assertEqual(self.primary.items, before)

    def test_omitted_reference_preserves_legacy_identity_rejection(self):
        with self.assertRaisesRegex(ProtocolError, 'TRANSIENT_STATE_IDENTITY'):
            TransientQueue(self.store, 'f' * 32).register(BINDING)
        self.assertEqual(self.primary.get(STATE_KEY), self.legacy_bytes)

    def test_deployment_selects_only_explicit_reference_and_does_not_migrate(self):
        path = Path(__file__).resolve().parents[2] / 'infrastructure/pixinsight-pilot/app.py'
        spec = importlib.util.spec_from_file_location('transient_namespace_candidate', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        environment = {'DSG_TRANSIENT_ACTIVATION': 'OWNER_AUTHORIZED',
                       'DSG_TRANSIENT_WORKER_ID': 'f' * 32,
                       'DSG_TRANSIENT_WORKER_SHA256': 'b' * 64}
        with patch.dict(os.environ, environment, clear=True):
            queue, _ = module.transient_component(self.store, WORKER, 'c' * 64)
            self.assertEqual(queue.state_key, STATE_KEY)
        environment['DSG_TRANSIENT_STATE_REF'] = '7' * 32
        with patch.dict(os.environ, environment, clear=True):
            queue, _ = module.transient_component(self.store, WORKER, 'c' * 64)
            self.assertNotEqual(queue.state_key, STATE_KEY)
            queue.register(BINDING)
        self.assertEqual(self.primary.get(STATE_KEY), self.legacy_bytes)
        environment['DSG_TRANSIENT_STATE_REF'] = ''
        with patch.dict(os.environ, environment, clear=True), self.assertRaises(ProtocolError):
            module.transient_component(self.store, WORKER, 'c' * 64)


if __name__ == '__main__':
    unittest.main()
