import unittest
from tools.scientific_transients import test_case_dossier as fixtures
from tools.scientific_transients.case_workspace import assemble
from tools.pixinsight.local_pilot.broker import ProtocolError

class WorkspaceTests(unittest.TestCase):
 def setUp(self):
  self.f=fixtures.CaseDossierTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
  self.p=self.f.prepare();self.l=self.p.prepare_review(self.f.ledgers,'c'*32)
 def export(self):return assemble(self.f.f.f.plan,self.p,self.l,self.l.anchor_sha)
 def test_actual_frozen_components_share_plan_head_and_case(self):
  v=self.export();self.assertEqual(v['caseRef'],v['dossier']['caseRef']);self.assertEqual(v['plan']['headSha256'],v['triplet']['headSha256'])
  self.assertEqual(v['dossier']['planHeadSha256'],v['plan']['headSha256']);self.assertFalse(v['scientificAcceptance']);self.assertEqual(v['qualifiedControls'],0)
  self.assertNotIn(str(self.f.root),str(v));self.assertIsNone(v['contextualRecovery']);self.assertIsNotNone(v['comparison'])
 def test_changed_live_plan_cannot_be_combined_with_historical_dossier(self):
  f=self.f.f.f
  f.plan.append(fixtures.ref(2),'QUALIFICATION',{'state':'NON_EVALUABLE'},f.actor,{'RATIONALE':f.rationale},f.plan.events()[1])
  with self.assertRaisesRegex(ProtocolError,'WORKSPACE_CURRENT_BINDING'):self.export()
 def test_corrupted_retained_evidence_blocks_workspace_export(self):
  (self.p.directory/'retained/triplet.json').write_bytes(b'{}')
  with self.assertRaises(ProtocolError):self.export()
 def test_stale_ledger_head_not_exported_as_current(self):
  self.p.apply_review(self.l,self.f.request(self.p,self.l,self.l.anchor_sha))
  with self.assertRaises(ProtocolError):self.export()

if __name__=='__main__':unittest.main()
