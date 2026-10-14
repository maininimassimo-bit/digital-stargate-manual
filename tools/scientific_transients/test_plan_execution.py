"""Plan/job binding with actual queue/journal code and an owned MOCK process only."""
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_operator_run as fixtures
from tools.scientific_transients.test_test_plan import draft, ref
from tools.scientific_transients.test_plan import PlanVersion
from tools.scientific_transients.plan_execution import PlanExecution
from tools.scientific_transients.local_registry import relative


class PlanExecutionTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.OperatorTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.operator = self.f.load(); registry = self.operator.registry
        self.manifest = registry.verify(self.operator.value['binding']['bindingRef'], self.operator.value['manifestSha256'])
        self.root = self.f.f.f.fixture.root
        self.versions = self.root / 'plans'; self.versions.mkdir()
        self.bindings = self.root / 'plan-execution-bindings'; self.bindings.mkdir()
        self.rationale = self.root / 'reason.txt'; self.rationale.write_bytes(b'SYNTHETIC diagnostic single-frame exercise')
        self.actor = {'actorRef':ref(8), 'recordedUTC':'2026-10-14T00:00:00Z'}
        value = draft(); value['cases'][0]['frames'][0]['sha256'] = self.role('INPUT')['sha256']
        self.plan = PlanVersion.create(self.versions, value, self.actor, self.source('ALGORITHM'), self.source('CONTRACT'))

    def role(self, name):
        return next(r for r in self.manifest['files'] if r['role'] == name)

    def source(self, name):
        return self.operator.registry.artifacts / relative(self.role(name)['path'])

    def prepare(self, **kwargs):
        return PlanExecution.prepare(self.plan, ref(2), kwargs.pop('frame',ref(4)), self.operator,
            self.bindings, self.plan.events()[1], self.actor, self.rationale, **kwargs)

    def run_binding(self, binding, **kwargs):
        return binding.run_selected(self.f.f.transport, native_launch_authorized=True,
            spawn=self.f.f.f.spawn, clock=lambda:self.f.f.elapsed,
            sleep=kwargs.pop('sleep', self.f.advance_complete), **kwargs)

    def change_head(self):
        self.plan.append(ref(2), 'QUALIFICATION', {'state':'NON_EVALUABLE'}, self.actor,
                         {'RATIONALE':self.rationale}, self.plan.events()[1])

    def test_offline_binding_has_no_reservation_or_launch(self):
        binding = self.prepare(); binding.verify()
        self.assertEqual(self.f.f.transport.calls, []); self.assertEqual(self.f.f.f.starts, 0)
        self.assertFalse(binding.value['confirmatoryEligible'])
        self.assertEqual(binding.value['coverage'], 'SINGLE_FRAME_OF_TRIPLET')

    def test_mock_run_links_verified_journal_as_partial_diagnostic(self):
        binding = self.prepare(); result = self.run_binding(binding)
        self.assertEqual(result['state'], 'COMPLETED'); self.assertEqual(result['planLinkage'], 'LINKED')
        view = self.plan.view()
        self.assertEqual(view['cases'][0]['attempts'][0]['coverage'], 'PARTIAL')
        self.assertEqual(view['qualified'], 0); self.assertIsNone(view['statisticalResult'])
        self.assertTrue((binding.directory / 'plan-linked.json').exists())

    def test_unknown_frame_and_confirmatory_mode_refused_before_dispatch(self):
        for options in ({'frame':ref(20)}, {'mode':'CONFIRMATORY'}):
            with self.assertRaises(ProtocolError): self.prepare(**options)
        self.assertEqual(self.f.f.transport.calls, [])

    def test_rules_mismatch_refused(self):
        value = self.plan.read()['draft']
        other = self.root / 'other-rules'; other.write_bytes(b'different rules')
        self.plan = PlanVersion.create(self.versions, value, self.actor, self.source('ALGORITHM'), other)
        with self.assertRaisesRegex(ProtocolError, 'RULES_MISMATCH'): self.prepare()

    def test_wrong_frame_input_and_algorithm_refused(self):
        with self.assertRaisesRegex(ProtocolError, 'INPUT_MISMATCH'): self.prepare(frame=ref(5))
        other = self.root / 'other-algorithm'; other.write_bytes(b'different algorithm')
        value = self.plan.read()['draft']; value['algorithmRef'] = None
        self.plan = PlanVersion.create(self.versions, value, self.actor, other, self.source('CONTRACT'))
        with self.assertRaisesRegex(ProtocolError, 'ALGORITHM_MISMATCH'): self.prepare()

    def test_authorization_and_replay_do_not_dispatch(self):
        binding = self.prepare()
        for flag in (False, None, 1):
            with self.assertRaises(ProtocolError): binding.run_selected(self.f.f.transport,native_launch_authorized=flag)
        self.assertEqual(self.f.f.transport.calls, [])
        self.run_binding(binding); calls=len(self.f.f.transport.calls)
        with self.assertRaisesRegex(ProtocolError,'REPLAY'): self.run_binding(binding)
        self.assertEqual(len(self.f.f.transport.calls),calls)

    def test_changed_plan_before_dispatch_and_before_spawn_never_launches(self):
        binding = self.prepare(); self.change_head()
        with self.assertRaises(ProtocolError): self.run_binding(binding)
        self.assertEqual(self.f.f.transport.calls, []);self.assertEqual(self.f.f.f.starts, 0)

    def test_lost_reservation_has_no_replay_or_launch(self):
        binding = self.prepare(); self.f.f.transport.lose=True
        with self.assertRaises(ProtocolError): self.run_binding(binding)
        calls=len(self.f.f.transport.calls)
        with self.assertRaises(ProtocolError): self.run_binding(binding)
        self.assertEqual(len(self.f.f.transport.calls),calls);self.assertEqual(self.f.f.f.starts,0)
        self.assertTrue((binding.directory / 'unconfirmed.json').exists())

    def test_changed_plan_after_reservation_never_launches(self):
        binding=self.prepare(); original=self.f.f.transport.request
        def changed(path,value=None):
            result=original(path,value)
            if value is not None:self.change_head()
            return result
        self.f.f.transport.request=changed
        with self.assertRaises(ProtocolError):self.run_binding(binding)
        self.assertEqual(self.f.f.f.starts,0)

    def test_plan_change_during_run_preserves_completed_job_with_pending_link(self):
        binding=self.prepare()
        def complete_and_change(seconds):
            self.f.advance_complete(seconds);self.change_head()
        result=self.run_binding(binding,sleep=complete_and_change)
        self.assertEqual(result['state'],'COMPLETED');self.assertEqual(result['planLinkage'],'RECONCILIATION_REQUIRED')
        self.assertTrue((binding.directory/'technical-outcome.json').exists())
        self.assertTrue((binding.directory/'link-pending.json').exists())
        self.assertEqual(len(self.plan.view()['cases'][0]['attempts']),0)
        self.assertEqual(self.f.f.f.starts,1)

    def test_no_credentials_persisted_and_no_automatic_second_job(self):
        binding=self.prepare();self.run_binding(binding)
        for path in binding.directory.iterdir():
            self.assertNotIn(b'leaseToken',path.read_bytes())
        with self.assertRaises((FileExistsError,ProtocolError)):self.prepare()
        self.assertEqual(self.f.f.f.starts,1)

    def test_binding_or_rationale_changes_block_before_dispatch(self):
        binding=self.prepare();(binding.directory/'rationale.dat').write_bytes(b'changed')
        with self.assertRaises(ProtocolError):self.run_binding(binding)
        self.assertEqual(self.f.f.transport.calls,[]);self.assertEqual(self.f.f.f.starts,0)

    def test_plan_change_after_operation_ack_still_blocks_spawn(self):
        binding=self.prepare();original=self.f.f.transport.post
        def change(path,value):
            result=original(path,value)
            if value['sequence']==2:self.change_head()
            return result
        self.f.f.transport.post=change
        result=self.run_binding(binding)
        self.assertEqual(result['state'],'RECOVERY_REQUIRED');self.assertEqual(self.f.f.f.starts,0)
        self.assertEqual(result['planLinkage'],'RECONCILIATION_REQUIRED')


if __name__=='__main__':unittest.main()
