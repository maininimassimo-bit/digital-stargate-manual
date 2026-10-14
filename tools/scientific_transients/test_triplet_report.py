"""Distinct synthetic inputs and three independent MOCK selected-job calls."""
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_native_aperture as native_fixtures
from tools.scientific_transients import test_operator_run as operator_fixtures
from tools.scientific_transients.test_test_plan import draft, ref
from tools.scientific_transients.plan_execution import PlanExecution
from tools.scientific_transients.test_plan import PlanVersion
from tools.scientific_transients.triplet_report import inspect_triplet
from tools.scientific_transients.attempt_journal import read_json
from tools.scientific_transients.local_registry import relative


class TripletTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = []; self.operators = []; self.manifests = []
        original = native_fixtures.NativeReceiptTests.setUp
        for index in range(3):
            def distinct(instance, index=index):
                original(instance)
                instance.input.write_bytes(b'DISTINCT_SYNTHETIC_XISF_NOT_REAL_' + str(index).encode())
                instance.operation = ref(200 + index)
            with patch.object(native_fixtures.NativeReceiptTests, 'setUp', distinct):
                fixture = operator_fixtures.OperatorTests(); fixture.setUp()
            self.addCleanup(fixture.doCleanups)
            fixture.f.job = fixture.f.f.queue.create({'requestId':ref(300+index),
                'bindingRef':fixture.value['binding']['bindingRef']})
            fixture.value['jobId'] = fixture.f.job['jobId']
            fixture.value['reservationRef'] = ref(400+index);fixture.persist()
            operator = fixture.load(); manifest = operator.registry.verify(
                operator.value['binding']['bindingRef'], operator.value['manifestSha256'])
            self.fixtures.append(fixture); self.operators.append(operator); self.manifests.append(manifest)
        self.root = self.fixtures[0].f.f.fixture.root
        self.versions=self.root/'plans';self.versions.mkdir()
        self.bindings=self.root/'bindings';self.bindings.mkdir()
        self.rationale=self.root/'rationale';self.rationale.write_bytes(b'SYNTHETIC triple technical coverage only')
        self.actor={'actorRef':ref(8),'recordedUTC':'2026-10-14T00:00:00Z'}
        value=draft()
        for index,manifest in enumerate(self.manifests):
            value['cases'][0]['frames'][index]['sha256']=next(r['sha256'] for r in manifest['files'] if r['role']=='INPUT')
        self.plan=PlanVersion.create(self.versions,value,self.actor,self.source(0,'ALGORITHM'),self.source(0,'CONTRACT'))
        self.journals={};self.bindings_created=[]

    def source(self,index,role):
        row=next(r for r in self.manifests[index]['files'] if r['role']==role)
        return self.operators[index].registry.artifacts/relative(row['path'])

    def execute(self,index,completion=None):
        fixture=self.fixtures[index];operator=self.operators[index]
        binding=PlanExecution.prepare(self.plan,ref(2),ref(4+index),operator,self.bindings,
            self.plan.events()[1],self.actor,self.rationale)
        result=binding.run_selected(fixture.f.transport,native_launch_authorized=True,spawn=fixture.f.f.spawn,
            clock=lambda:fixture.f.elapsed,sleep=completion or fixture.advance_complete)
        self.assertEqual(result['planLinkage'],'LINKED');self.bindings_created.append(binding)
        receipt,_=read_json(operator.roots['intents']/operator.value['reservationRef']/'reserved.json')
        attempt=receipt['identity']['attemptId'];self.journals[attempt]=operator.roots['journals']/attempt
        return attempt

    def test_no_attempts_incomplete_and_no_measurement_invented(self):
        value=inspect_triplet(self.plan,ref(2),{})
        self.assertEqual(value['status'],'INCOMPLETE');self.assertEqual(len(value['frames']),3)
        for key in ('crossEpochResult','fullVariance','significance','statisticalResult'):self.assertIsNone(value[key])

    def test_one_or_two_completions_cannot_cover_three_frames(self):
        for index in (0,1):
            self.execute(index)
            self.assertEqual(inspect_triplet(self.plan,ref(2),self.journals)['status'],'INCOMPLETE')

    def test_three_distinct_verified_jobs_cover_triplet_but_not_science(self):
        for index in range(3):self.execute(index)
        value=inspect_triplet(self.plan,ref(2),self.journals)
        self.assertEqual(value['status'],'TECHNICAL_COVERAGE_COMPLETE');self.assertEqual(value['blockers'],[])
        self.assertEqual(value['qualifiedControls'],0);self.assertFalse(value['confirmatoryEligible'])
        self.assertEqual(value['scienceValidation'],'NOT_VALIDATED');self.assertIsNone(value['significance'])
        self.assertEqual(len({f['sha256'] for f in value['frames']}),3)

    def test_missing_or_changed_journal_invalidates_complete_coverage(self):
        for index in range(3):self.execute(index)
        missing=dict(self.journals);missing.pop(next(iter(missing)))
        self.assertEqual(inspect_triplet(self.plan,ref(2),missing)['status'],'INCOMPLETE')
        path=next(iter(self.journals.values()))/'report.json';path.write_bytes(b'changed')
        self.assertEqual(inspect_triplet(self.plan,ref(2),self.journals)['status'],'INCOMPLETE')

    def test_unknown_case_and_changed_plan_refused(self):
        with self.assertRaises(ProtocolError):inspect_triplet(self.plan,ref(100),self.journals)
        (self.plan.directory/'evidence-00.dat').write_bytes(b'altered')
        with self.assertRaises(ProtocolError):inspect_triplet(self.plan,ref(2),self.journals)

    def test_failed_attempt_remains_visible_and_never_completes_triplet(self):
        self.execute(0);self.execute(1)
        fixture=self.fixtures[2]
        def failed(seconds):
            fixture.f.elapsed+=seconds;fixture.f.f.native('FAILED')
        self.execute(2,completion=failed)
        value=inspect_triplet(self.plan,ref(2),self.journals)
        self.assertEqual(value['status'],'INCOMPLETE');self.assertEqual(len(value['attempts']),3)
        self.assertEqual(value['attempts'][2]['verification'],'RETAINED_TECHNICAL_FAILURE')
        self.assertEqual(value['qualifiedControls'],0)

    def test_same_journal_cannot_substitute_another_frame_attempt(self):
        for index in range(3):self.execute(index)
        attempts=list(self.journals);self.journals[attempts[1]]=self.journals[attempts[0]]
        value=inspect_triplet(self.plan,ref(2),self.journals)
        self.assertEqual(value['status'],'INCOMPLETE')
        self.assertEqual(len(value['attempts']),3)


if __name__=='__main__':unittest.main()
