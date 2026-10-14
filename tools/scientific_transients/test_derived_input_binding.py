"""Synthetic proof bytes and owned MOCK process; no native execution."""
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_derived_input_preflight as fixtures
from tools.scientific_transients.test_test_plan import ref
from tools.scientific_transients.attempt_journal import write_new, read_json
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.derived_input_binding import DerivedInputBinding, archived_binding
from tools.scientific_transients.plan_execution import PlanExecution
from tools.scientific_transients.plan_readiness import assess
from tools.scientific_transients.triplet_report import inspect_triplet


class DerivedBindingTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.DerivedPreflightTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.plan, self.operator, self.l = self.f.plan, self.f.operator, self.f.lineage
        self.root = self.f.f.f.f.fixture.root
        self.signed = self.root / 'synthetic-signed-proof'; self.signed.mkdir()
        w = write_new(self.signed / 'wrapper-terminal.json', {'fixture': 'SYNTHETIC'})
        t = write_new(self.signed / 'terminal.json', {'fixture': 'SYNTHETIC'})
        for name in ('input.xisf', 'checkpoint.xisf'):
            (self.signed / name).write_bytes(b'SYNTHETIC proof fixture, not actual XISF')
        (self.signed / 'native_aperture.jsh').write_bytes(self.f.source('ALGORITHM').read_bytes())
        self.signed_sha = write_new(self.signed / 'verification.json', {
            'scope':'NEW_NATIVE_SYNTHETIC_SIGNED_READ_REGRESSION',
            'sourceLibrarySha256':fingerprint(self.f.source('ALGORITHM'))['sha256'],
            'scienceValidation':'NOT_VALIDATED','qualifiedControls':0,
            'engineMaxAbsoluteError':0,'checkpointMaxAbsoluteError':0,
            'negativePixels':1,'aboveOnePixels':1,'ownedInstanceStopped':True,'userInstancesTouched':False,
            'wrapperTerminalSha256':w,'nativeTerminalSha256':t,
            'inputSha256':fingerprint(self.signed/'input.xisf')['sha256'],
            'checkpointSha256':fingerprint(self.signed/'checkpoint.xisf')['sha256']})
        self.bindings = self.root / 'execution-bindings'; self.bindings.mkdir()
        self.reason = self.root / 'derived-reason.txt'; self.reason.write_bytes(b'SYNTHETIC DERIVED DIAGNOSTIC')
        self.actor = {'actorRef':ref(8),'recordedUTC':'2026-10-14T00:00:00Z'}

    def prepare(self, frame=ref(4)):
        return DerivedInputBinding.prepare(self.plan, ref(2), frame, self.operator,
            self.root/'derived-proof.json', self.l.directory, self.l.receipt_sha,
            self.l.draft_path, self.l.draft_sha, self.signed, self.signed_sha)

    def execution(self, proof):
        return PlanExecution.prepare(self.plan,ref(2),ref(4),self.operator,self.bindings,
            self.plan.events()[1],self.actor,self.reason,derived=proof)

    def run_mock(self, execution, sleep=None):
        f=self.f.f
        return execution.run_selected(f.f.transport,native_launch_authorized=True,
            spawn=f.f.f.spawn,clock=lambda:f.f.elapsed,sleep=sleep or f.advance_complete)

    def test_offline_preparation_preserves_two_hashes_no_launch(self):
        proof=self.prepare();execution=self.execution(proof);execution.verify()
        self.assertNotEqual(proof.value['rawSha256'],proof.value['derivedSha256'])
        self.assertEqual(execution.value['inputSha256'],proof.value['derivedSha256'])
        self.assertEqual(self.f.f.f.transport.calls,[])

    def test_mock_completion_archives_proof_and_audits_original_coverage(self):
        proof=self.prepare();execution=self.execution(proof)
        self.assertEqual(self.run_mock(execution)['planLinkage'],'LINKED')
        event=self.plan.events()[0][0]
        self.assertEqual(event['data']['inputDerivationSha256'],proof.sha)
        archived_binding(self.plan,event).verify(self.plan,ref(2))
        view=self.plan.view();self.assertEqual(view['schema'],'BKL051_TEST_PLAN_REVIEW_V2')
        self.assertEqual(view['qualified'],0)
        root=self.operator.roots['journals']
        audit=assess(self.plan,root)
        self.assertEqual(audit['cases'][0]['attempts'][0]['byteIntegrity'],'RECHECKED_BYTE_INTEGRITY_ONLY')
        report=inspect_triplet(self.plan,ref(2),{event['data']['identity']['attemptId']:root/event['data']['identity']['attemptId']})
        self.assertEqual(report['attempts'][0]['frameRefs'],[ref(4)])
        self.assertEqual(report['status'],'INCOMPLETE');self.assertEqual(report['qualifiedControls'],0)
        proof.path.unlink()  # The event owns a verified copy, not this scratch file.
        self.assertEqual(assess(self.plan,root)['cases'][0]['attempts'][0]['byteIntegrity'],'RECHECKED_BYTE_INTEGRITY_ONLY')
        self.l.raw.write_bytes(b'changed after retained completion')
        self.assertEqual(assess(self.plan,root)['cases'][0]['attempts'][0]['byteIntegrity'],'UNAVAILABLE_OR_CHANGED')
        self.assertEqual(self.plan.view()['cases'][0]['attempts'][0]['technicalState'],'COMPLETED')

    def test_wrong_frame_or_missing_native_evidence_refused_before_dispatch(self):
        with self.assertRaises(ProtocolError):self.prepare(ref(5))
        (self.signed/'checkpoint.xisf').write_bytes(b'changed')
        with self.assertRaises(ProtocolError):self.prepare()
        self.assertEqual(self.f.f.f.transport.calls,[])

    def test_changed_parent_before_dispatch_consumes_execution_without_launch(self):
        proof=self.prepare();execution=self.execution(proof)
        self.l.raw.write_bytes(b'changed')
        with self.assertRaises(ProtocolError):self.run_mock(execution)
        self.assertEqual(self.f.f.f.transport.calls,[])
        with self.assertRaisesRegex(ProtocolError,'REPLAY'):self.run_mock(execution)

    def test_changed_private_proof_and_case_are_rejected(self):
        proof=self.prepare()
        with self.assertRaises(ProtocolError):proof.verify(self.plan,ref(22))
        proof.path.write_bytes(b'{}')
        with self.assertRaises(ProtocolError):self.execution(proof)

    def test_archive_evidence_change_detected_without_losing_technical_result(self):
        proof=self.prepare();execution=self.execution(proof);self.run_mock(execution)
        event=self.plan.events()[0][0]
        archived=archived_binding(self.plan,event);archived.path.write_bytes(b'{}')
        with self.assertRaises(ProtocolError):self.plan.events()
        self.assertEqual(read_json(execution.directory/'technical-outcome.json')[0]['state'],'COMPLETED')

    def test_source_changes_during_run_preserve_result_require_reconciliation(self):
        proof=self.prepare();execution=self.execution(proof)
        def changed_sleep(seconds):
            self.f.f.advance_complete(seconds)
            self.l.raw.write_bytes(b'changed during execution')
        result=self.run_mock(execution,changed_sleep)
        self.assertEqual(result['state'],'COMPLETED')
        self.assertEqual(result['planLinkage'],'RECONCILIATION_REQUIRED')
        self.assertEqual(self.plan.events()[0],[])


if __name__=='__main__':unittest.main()
