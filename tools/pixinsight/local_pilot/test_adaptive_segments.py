"""Single-use native permits do not authorize replay, V1 or cancellation bypass."""
import copy
import unittest
from concurrent.futures import ThreadPoolExecutor

from . import test_adaptive_flow as flow_fixture
from .adaptive_segments import SegmentPermits
from .broker import ProtocolError
from .intake import sha


class SegmentPermitTests(unittest.TestCase):
    def setUp(self):
        flow_fixture.AdaptiveFlowTests.setUp(self)
        self.body = lambda: flow_fixture.AdaptiveFlowTests.body(self)
        state = self.portal.generate_adaptive(self.request_id, self.body())
        self.portal.approve_adaptive(self.request_id, {'proposalSha256':state['proposalSha256'],
            'adaptationScope':'NEXT_STEP_PARAMETERS_ONLY', 'nativeExecutionConfirmed':True})
        self.state = self.portal.adaptive_state(self.request_id)
        self.permits = SegmentPermits(self.portal)

    def send(self, payload):
        return flow_fixture.AdaptiveFlowTests.send(self, payload)

    def reserve(self):
        return self.permits.reserve(self.request_id, self.broker.worker_id, '2'*32,
            sha(self.state['executionPolicy']), self.state['cursor']['resultSha256'])

    def test_lost_permit_or_start_never_allows_another_attempt(self):
        permit = self.reserve()['permit']
        self.assertFalse(self.reserve()['nativeStartAllowed'])
        self.assertTrue(self.permits.start(self.request_id, self.broker.worker_id, permit)['executeAllowed'])
        self.assertFalse(self.permits.start(self.request_id, self.broker.worker_id, permit)['executeAllowed'])
        self.assertFalse(self.reserve()['nativeStartAllowed'])
        self.assertIsNone(self.broker.claim(self.broker.worker_id, '2'*32))

    def test_concurrent_reserve_and_start_have_only_one_winner(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            values = list(pool.map(lambda _: self.reserve(), range(4)))
        self.assertEqual(sum(v['nativeStartAllowed'] for v in values), 1)
        permit = next(v['permit'] for v in values if v['nativeStartAllowed'])
        with ThreadPoolExecutor(max_workers=4) as pool:
            values = list(pool.map(lambda _: self.permits.start(self.request_id, self.broker.worker_id, permit), range(4)))
        self.assertEqual(sum(v['executeAllowed'] for v in values), 1)

    def test_owner_views_omit_native_authority_nonce(self):
        permit = self.reserve()['permit']
        for state in (self.portal.adaptive_state(self.request_id)['job'],
                      self.broker.status('PIAI_'+self.request_id)['job']):
            self.assertNotIn('owner', state['adaptiveSegmentPermits']['0'])
            self.assertNotIn(permit['owner'], str(state))

    def test_cancel_between_reservation_and_start_blocks_native(self):
        permit = self.reserve()['permit']
        self.broker.cancel('PIAI_'+self.request_id)
        with self.assertRaises(ProtocolError):
            self.permits.start(self.request_id, self.broker.worker_id, permit)
        with self.assertRaises(ProtocolError):
            self.reserve()

    def test_changed_permit_and_unapproved_graph_do_not_start(self):
        permit = self.reserve()['permit']
        for field, value in (('owner','5'*64),('ordinal',True),('graphSha256','6'*64),
                             ('step',{'process':'STRETCH','parameters':{'targetBackground':.05}})):
            changed=copy.deepcopy(permit);changed[field]=value
            with self.assertRaises(ProtocolError):
                self.permits.start(self.request_id, self.broker.worker_id, changed)
        self.assertTrue(self.permits.start(self.request_id, self.broker.worker_id, permit)['executeAllowed'])

    def test_foreign_root_and_legacy_active_job_prevent_permit(self):
        def busy(state, now):
            state['jobs'].append({'jobId':'PIAI_'+'b'*32, 'state':'RUNNING',
                'request':{'aiMode':'SESSION_ASSISTED'}, 'cancelRequested':False})
        self.broker._mutate(busy)
        with self.assertRaises(ProtocolError):
            self.reserve()

    def test_foreign_root_and_removed_owner_authority_are_refused(self):
        def change_root(state, now):
            state['rootId'] = '3'*32
        self.broker._mutate(change_root)
        with self.assertRaises(ProtocolError):
            self.reserve()
        def remove_approval(state, now):
            state['rootId'] = None
            state['jobs'][0].pop('adaptiveExecutionApprovalSha256')
        self.broker._mutate(remove_approval)
        with self.assertRaises(ProtocolError):
            self.reserve()
