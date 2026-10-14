"""Byte-bound derived associations do not grant dispatch or scientific qualification."""
import hashlib
import json
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_input_lineage as lineage_fixtures
from tools.scientific_transients import test_operator_run as operator_fixtures
from tools.scientific_transients.local_registry import relative
from tools.scientific_transients.test_plan import PlanVersion
from tools.scientific_transients.test_test_plan import ref
from tools.scientific_transients.derived_input_preflight import preflight


class DerivedPreflightTests(unittest.TestCase):
    def setUp(self):
        self.lineage=lineage_fixtures.LineageTests();self.lineage.setUp();self.addCleanup(self.lineage.doCleanups)
        self.f=operator_fixtures.OperatorTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.operator=self.f.load();self.manifest=self.operator.registry.verify(
            self.operator.value['binding']['bindingRef'],self.operator.value['manifestSha256'])
        l=self.lineage;l.output.write_bytes(self.source('INPUT').read_bytes())
        l.receipt['products']['out.xisf']=hashlib.sha256(l.output.read_bytes()).hexdigest()
        (l.directory/'receipt.json').write_text(json.dumps(l.receipt))
        l.receipt_sha=hashlib.sha256((l.directory/'receipt.json').read_bytes()).hexdigest()
        root=self.f.f.f.fixture.root/'plans';root.mkdir()
        self.plan=PlanVersion.create(root,l.draft,{'actorRef':ref(8),'recordedUTC':'2026-10-14T00:00:00Z'},
                                     self.source('ALGORITHM'),self.source('CONTRACT'))

    def source(self,role):
        row=next(r for r in self.manifest['files'] if r['role']==role)
        return self.operator.registry.artifacts/relative(row['path'])

    def inspect(self,frame=ref(4)):
        l=self.lineage
        return preflight(self.plan,ref(2),frame,self.operator,l.directory,l.receipt_sha,l.draft_path,l.draft_sha)

    def test_matching_derived_input_still_blocked_no_dispatch(self):
        v=self.inspect();self.assertEqual(v['status'],'BLOCKED')
        self.assertTrue(v['matches']['originalInSelectedCase']);self.assertTrue(v['matches']['derivedMatchesPreparedInput'])
        self.assertTrue(v['matches']['currentSignedReadImplementation'])
        self.assertIn('DERIVED_ATTEMPT_ARCHIVE_LINK_REQUIRED',v['blockers'])
        self.assertFalse(v['executionAuthorized']);self.assertEqual(v['qualifiedControls'],0)
        self.assertEqual(self.f.f.transport.calls,[]);self.assertEqual(self.f.f.f.starts,0)

    def test_different_original_and_outside_sample_do_not_attach(self):
        v=self.inspect(ref(5));self.assertFalse(v['matches']['originalInSelectedCase'])
        self.assertIn('ORIGINAL_NOT_IN_SELECTED_CASE',v['blockers']);self.assertIsNone(v['derivedSha256'])

    def test_corrupted_derived_or_candidate_manifest_rejected(self):
        self.lineage.output.write_bytes(b'changed')
        with self.assertRaises(ProtocolError):self.inspect()
        self.assertEqual(self.f.f.transport.calls,[])

    def test_private_paths_not_exposed_and_no_uncertainty_invented(self):
        v=self.inspect();raw=json.dumps(v)
        self.assertNotIn(str(self.lineage.root),raw);self.assertNotIn('leaseToken',raw)
        self.assertIsNone(v['completeUncertainty']);self.assertIsNone(v['significance'])


if __name__=='__main__':unittest.main()
