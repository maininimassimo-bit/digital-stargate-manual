"""Selected-job reservation: MemoryStore/mock native only, no cloud/credentials/native launch."""
import concurrent.futures
import datetime as dt
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_native_supervisor as fixtures
from tools.scientific_transients import test_queue as queue_fixtures
from tools.scientific_transients.reservation_intent import ReservationIntent
from tools.scientific_transients.queue import TransientQueue, STATE_KEY


class ReserveTransport:
    def __init__(self, queue):
        self.queue, self.calls, self.posts, self.lose = queue, [], [], False

    def request(self, path, value=None):
        self.calls.append((path, value))
        if value is not None:
            result = self.queue.reserve_once(value)
            if self.lose:
                self.lose = False; raise ProtocolError('SYNTHETIC_LOST_RESERVATION_RESPONSE')
            return result
        return self.queue.worker_receipt(path.rsplit('/', 1)[-1])

    def post(self, path, value):
        self.posts.append(value)
        return self.queue.report(path.split('/')[-2], value)


class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.SupervisorTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        f = self.f
        f.queue.report(f.claim['jobId'], {'attemptId':f.claim['attemptId'], 'leaseToken':f.claim['leaseToken'],
                       'sequence':1, 'stage':'CANCELLED', 'result':None})
        self.job = f.queue.create({'requestId':'f'*32, 'bindingRef':f.journal.anchor['identity']['binding']['bindingRef']})
        self.root = f.fixture.root / 'reservation-intents'; self.root.mkdir()
        self.jroot = f.fixture.root / 'reservation-journals'; self.jroot.mkdir()
        self.oroot = f.fixture.root / 'reservation-outboxes'; self.oroot.mkdir()
        self.transport, self.elapsed = ReserveTransport(f.queue), 0

    def prepare(self, ref='e'*32):
        f = self.f; value = f.journal.anchor['identity']
        return ReservationIntent.prepare(f.local, self.root, 'a'*32, '8'*32, self.job['jobId'], ref,
                   value['binding'], value['manifestSha256'], f.directory, f.fixture.operation,
                   engine=f.fixture.engine, catalog=f.fixture.catalog)

    def request(self, ref='e'*32):
        return {'workerId':'a'*32, 'rootId':'8'*32, 'jobId':self.job['jobId'],
                'bindingRef':self.job['binding']['bindingRef'], 'reservationRef':ref}

    def driver(self, intent):
        return intent.prepare_driver(self.jroot, self.oroot, self.transport,
                    supervisor_options={'spawn':self.f.spawn, 'clock':lambda:self.elapsed, 'timeout':10},
                    clock=lambda:self.elapsed)

    def test_explicit_selected_job_to_native_mock_completion_without_secret_persistence(self):
        intent = self.prepare(); result = intent.reserve(self.transport)
        self.assertEqual(result['state'], 'RESERVED'); lease = intent.lease
        self.assertEqual(self.f.starts, 0); driver = self.driver(intent)
        self.assertIsNone(intent.lease); self.assertEqual(self.f.starts, 0)
        self.assertEqual(driver.start()['state'], 'RUNNING')
        self.f.native('COMPLETED'); self.elapsed = 2
        self.assertEqual(driver.step()['state'], 'COMPLETED')
        self.assertEqual(self.f.queue.status(self.job['jobId'])['scientificValidation'], 'NOT_VALIDATED')
        for path in self.f.fixture.root.rglob('*.json'):
            self.assertNotIn(lease.encode(), path.read_bytes())
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        with self.assertRaises(ProtocolError): self.driver(intent)

    def test_existing_server_intent_never_returns_lease_or_renews(self):
        first = self.f.queue.reserve_once(self.request()); previous = self.f.queue.status(self.job['jobId'])
        self.f.now += dt.timedelta(seconds=10)
        self.assertEqual(self.f.queue.reserve_once(self.request()), {'disposition':'RECONCILIATION_REQUIRED','job':None})
        self.assertEqual(self.f.queue.status(self.job['jobId']), previous)
        self.assertNotIn('reservationIntent', previous)
        self.assertNotIn('reservationIntent', first['job'])

    def test_lost_response_preserved_and_never_retried_or_launched(self):
        intent = self.prepare(); self.transport.lose = True
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        self.assertEqual(self.f.queue.status(self.job['jobId'])['state'], 'RESERVED')
        self.assertTrue((intent.records / 'failed.json').is_file()); self.assertIsNone(intent.lease)
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        with self.assertRaises(ProtocolError): self.driver(intent)
        self.assertEqual(len(self.transport.calls), 1); self.assertEqual(self.f.starts, 0)
        with self.assertRaises(FileExistsError): self.prepare()

    def test_existing_intent_response_freezes_client_without_driver(self):
        self.f.queue.reserve_once(self.request()); intent = self.prepare()
        self.assertEqual(intent.reserve(self.transport)['state'], 'RECONCILIATION_REQUIRED')
        self.assertIsNone(intent.lease)
        with self.assertRaises(ProtocolError): self.driver(intent)
        self.assertEqual(self.f.starts, 0)

    def test_concurrent_same_intent_has_one_created_response(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _:self.f.queue.reserve_once(self.request()), range(4)))
        self.assertEqual(sum(r['disposition'] == 'CREATED' for r in results), 1)
        self.assertTrue(all(r['job'] is None for r in results if r['disposition'] != 'CREATED'))

    def test_different_nonce_or_job_cannot_adopt_active_attempt(self):
        self.f.queue.reserve_once(self.request())
        with self.assertRaises(ProtocolError): self.f.queue.reserve_once(self.request('d'*32))
        next_job = self.f.queue.create({'requestId':'c'*32,'bindingRef':self.job['binding']['bindingRef']})
        with self.assertRaises(ProtocolError):
            self.f.queue.reserve_once({**self.request('d'*32), 'jobId':next_job['jobId']})
        with self.assertRaises(ProtocolError):
            self.f.queue.reserve_once({**self.request(), 'jobId':next_job['jobId']})

    def test_legacy_reserved_attempt_and_cancelled_job_never_look_fresh(self):
        self.f.queue.cancel(self.job['jobId'])
        with self.assertRaises(ProtocolError): self.f.queue.reserve_once(self.request())
        next_job = self.f.queue.create({'requestId':'c'*32,'bindingRef':self.job['binding']['bindingRef']})
        self.f.queue.claim({'workerId':'a'*32,'rootId':'8'*32})
        with self.assertRaises(ProtocolError):
            self.f.queue.reserve_once({**self.request(), 'jobId':next_job['jobId']})

    def test_wrong_binding_root_worker_and_extra_payload_rejected(self):
        before = self.f.queue.store.get(STATE_KEY)[0]
        for changes in [{'bindingRef':'0'*32}, {'rootId':'0'*32}, {'workerId':'0'*32}, {'path':'F:/private'}, {'reservationRef':'http://invalid'}]:
            with self.assertRaises(ProtocolError): self.f.queue.reserve_once({**self.request(), **changes})
        self.assertEqual(self.f.queue.store.get(STATE_KEY)[0], before)

    def test_expiry_keeps_recovery_and_never_issues_new_lease(self):
        self.f.queue.reserve_once(self.request()); self.f.now += dt.timedelta(seconds=901)
        restarted = TransientQueue(self.f.queue.store, 'a'*32, lambda:self.f.now)
        self.assertEqual(restarted.reserve_once(self.request()), {'disposition':'RECONCILIATION_REQUIRED','job':None})
        self.assertEqual(restarted.status(self.job['jobId'])['state'], 'RECOVERY_REQUIRED')

    def test_altered_intent_refused_before_dispatch(self):
        intent = self.prepare(); (intent.records / 'request.json').write_bytes(b'altered')
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        self.assertEqual(self.transport.calls, []); self.assertEqual(self.f.starts, 0)

    def test_altered_response_identity_or_secret_echo_freezes(self):
        intent = self.prepare(); original = self.transport.request
        def altered(path, value=None):
            response = original(path, value); response['job']['unexpected'] = 'secret-echo'; return response
        self.transport.request = altered
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        self.assertIsNone(intent.lease); self.assertEqual(self.f.starts, 0)
        self.assertNotIn(b'secret-echo', (intent.records / 'failed.json').read_bytes())

    def test_changed_reservation_receipt_refuses_driver(self):
        intent = self.prepare(); intent.reserve(self.transport)
        (intent.records / 'reserved.json').write_bytes(b'altered')
        with self.assertRaises(ProtocolError): self.driver(intent)
        self.assertEqual(self.f.starts, 0)


    def test_mutated_in_memory_request_refuses_dispatch(self):
        intent = self.prepare(); intent.request['reservationRef'] = 'b'*32
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        self.assertEqual(self.transport.calls, [])
        self.assertEqual(self.f.starts, 0)

    def test_input_changed_after_intent_prevents_dispatch(self):
        intent = self.prepare()
        (self.f.directory / 'input.xisf').write_bytes(b'changed scientific input')
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        self.assertEqual(self.transport.calls, [])
        self.assertEqual(self.f.starts, 0)

    def test_overlapping_driver_root_freezes_without_native_launch(self):
        intent = self.prepare(); intent.reserve(self.transport)
        with self.assertRaises(ProtocolError):
            intent.prepare_driver(self.root, self.oroot, self.transport)
        self.assertIsNone(intent.lease)
        self.assertEqual(self.f.starts, 0)

    def test_response_persistence_failure_after_commit_never_retries(self):
        intent = self.prepare()
        from tools.scientific_transients.reservation_intent import write_new
        def fail(path, value):
            if path.name == 'reserved.json': raise OSError('synthetic-secret-must-not-be-retained')
            return write_new(path, value)
        with patch('tools.scientific_transients.reservation_intent.write_new', side_effect=fail):
            with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        self.assertEqual(self.f.queue.status(self.job['jobId'])['state'], 'RESERVED')
        self.assertIsNone(intent.lease)
        with self.assertRaises(ProtocolError): intent.reserve(self.transport)
        self.assertEqual(len(self.transport.calls), 1)
        self.assertNotIn(b'synthetic-secret', (intent.records / 'failed.json').read_bytes())
        self.assertEqual(self.f.starts, 0)

    def test_driver_marker_failure_retains_partial_driver_without_launch_or_retry(self):
        intent = self.prepare(); intent.reserve(self.transport)
        from tools.scientific_transients.reservation_intent import write_new
        def fail(path, value):
            if path.name == 'driver-prepared.json': raise OSError('synthetic interruption')
            return write_new(path, value)
        with patch('tools.scientific_transients.reservation_intent.write_new', side_effect=fail):
            with self.assertRaises(ProtocolError): self.driver(intent)
        self.assertTrue(list(self.jroot.iterdir()))
        self.assertTrue(list(self.oroot.iterdir()))
        self.assertIsNone(intent.lease)
        with self.assertRaises(ProtocolError): self.driver(intent)
        self.assertEqual(self.f.starts, 0)


class ReserveHttpTests(unittest.TestCase):
    def setUp(self):
        self.f = queue_fixtures.HttpTests(); self.f.setUp(); self.addCleanup(self.f.tearDown)

    def test_dedicated_worker_only_explicit_reservation(self):
        f = self.f; base = '/v1/transient-analysis'
        f.request(base + '/worker/register', queue_fixtures.BINDING, queue_fixtures.TOKEN)
        _, job = f.request(base + '/jobs', queue_fixtures.REQUEST, 'synthetic-owner', True)
        value = {'workerId':queue_fixtures.WORKER, 'rootId':queue_fixtures.ROOT, 'jobId':job['jobId'],
                 'bindingRef':queue_fixtures.BINDING['bindingRef'], 'reservationRef':'9'*32}
        for token, owner in [(None,False),(queue_fixtures.LEGACY_TOKEN,False),('synthetic-owner',True)]:
            self.assertEqual(f.request(base + '/worker/reserve', value, token, owner)[0], 403)
        from tools.scientific_transients.receipt_coordinator import TransientTransport
        transport = TransientTransport('http://127.0.0.1:' + str(f.server.server_port), queue_fixtures.TOKEN, test_loopback=True)
        with self.assertRaises(ProtocolError): transport.request(base + '/worker/reserve')
        response = transport.request(base + '/worker/reserve', value)
        self.assertEqual(response['disposition'], 'CREATED')
        _, repeated = f.request(base + '/worker/reserve', value, queue_fixtures.TOKEN)
        self.assertEqual(repeated, {'disposition':'RECONCILIATION_REQUIRED','job':None})


if __name__ == '__main__':
    unittest.main()
