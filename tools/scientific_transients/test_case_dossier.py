"""Frozen scientific case + existing review ledger, synthetic jobs/actors only."""
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_multi_epoch as fixtures
from tools.scientific_transients.case_dossier import freeze,CaseDossier
from tools.scientific_transients.test_test_plan import ref
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.attempt_journal import read_json
from tools.scientific_transients.attempt_journal import write_new
from unittest.mock import patch

class CaseDossierTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.MultiEpochTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.root=self.f.f.root/'dossiers';self.root.mkdir();self.ledgers=self.f.f.root/'dossier-ledgers';self.ledgers.mkdir()
    def prepare(self,**kwargs):
        return freeze(self.f.f.plan,ref(2),self.f.f.journals,self.root,budget_path=self.f.path,
            budget_sha=self.f.sha,origin='SYNTHETIC_TEST',**kwargs)
    def request(self,pkg,ledger,head,action='KEEP_FOR_REVIEW',target=None,event=ref(501)):
        return {'schema':'BKL051_DOSSIER_REVIEW_REQUEST_V1','packageSha256':pkg.sha,'ledgerAnchorSha256':ledger.anchor_sha,
            'expectedHeadSha256':head,'decision':{'eventRef':event,'actorRef':ref(9),'recordedUTC':'2026-10-14T00:00:00Z',
                'action':action,'targetEventRef':target,'note':'SYNTHETIC review; no Owner acceptance'}}
    def test_freeze_verifies_retained_plan_and_case_without_submission(self):
        pkg=self.prepare();v,content=pkg.verify();ledger=pkg.prepare_review(self.ledgers,ref(500))
        view=pkg.view(ledger,ledger.anchor_sha,self.f.f.plan)
        self.assertEqual(view['packageStatus'],'RETAINED_PACKAGE_VERIFIED');self.assertEqual(view['planStatus'],'LIVE_PLAN_MATCHES')
        self.assertEqual(view['attempts'],3);self.assertTrue(view['comparisonPresent']);self.assertEqual(view['evidenceGaps'],0)
        self.assertEqual(view['decisions'],[]);self.assertFalse(view['submissionAuthorized'])
        self.assertFalse(view['scientificAcceptance']);self.assertNotIn(str(self.root),str(view))
    def test_review_and_revocation_preserve_original_event(self):
        pkg=self.prepare();ledger=pkg.prepare_review(self.ledgers,ref(500))
        first=pkg.apply_review(ledger,self.request(pkg,ledger,ledger.anchor_sha))
        before=fingerprint(ledger.directory/'events/0000.json')
        last=pkg.apply_review(ledger,self.request(pkg,ledger,first['headSha256'],'REVOKE_REVIEW',ref(501),ref(502)))
        view=pkg.view(ledger,last['headSha256']);self.assertTrue(view['decisions'][0]['revoked'])
        self.assertEqual(len(view['decisions']),2);self.assertEqual(fingerprint(ledger.directory/'events/0000.json'),before)
        self.assertFalse(view['actorIdentityAttested'])
    def test_retained_file_mutation_blocks_new_review_but_history_survives(self):
        pkg=self.prepare();ledger=pkg.prepare_review(self.ledgers,ref(500))
        first=pkg.apply_review(ledger,self.request(pkg,ledger,ledger.anchor_sha))
        receipt,_=read_json(pkg.directory/'package.json');target=pkg.directory/receipt['records'][0]['path'];target.write_bytes(b'changed')
        with self.assertRaises(ProtocolError):pkg.verify()
        view=pkg.view(ledger,first['headSha256']);self.assertEqual(view['packageStatus'],'RETAINED_PACKAGE_UNAVAILABLE_OR_CHANGED')
        self.assertEqual(len(view['decisions']),1)
        with self.assertRaises(ProtocolError):pkg.apply_review(ledger,self.request(pkg,ledger,first['headSha256'],event=ref(503)))
        restarted=CaseDossier.review_reference(pkg.directory,pkg.sha)
        revoked=restarted.apply_review(ledger,self.request(pkg,ledger,first['headSha256'],'REVOKE_REVIEW',ref(501),ref(505)))
        self.assertTrue(restarted.view(ledger,revoked['headSha256'])['decisions'][0]['revoked'])
    def test_live_plan_revision_does_not_rewrite_frozen_dossier(self):
        pkg=self.prepare();ledger=pkg.prepare_review(self.ledgers,ref(500));before=pkg.sha
        plan=self.f.f.plan
        plan.append(ref(2),'QUALIFICATION',{'state':'NON_EVALUABLE'},self.f.f.actor,{'RATIONALE':self.f.f.rationale},plan.events()[1])
        view=pkg.view(ledger,ledger.anchor_sha,plan);self.assertEqual(view['planStatus'],'HISTORICAL_PLAN_REVISION')
        self.assertEqual(pkg.sha,before);pkg.verify()
    def test_stale_head_wrong_package_and_scientific_approval_rejected(self):
        pkg=self.prepare();ledger=pkg.prepare_review(self.ledgers,ref(500))
        request=self.request(pkg,ledger,ledger.anchor_sha);pkg.apply_review(ledger,request)
        with self.assertRaises(ProtocolError):pkg.apply_review(ledger,self.request(pkg,ledger,ledger.anchor_sha,event=ref(504)))
        request=self.request(pkg,ledger,ledger.anchor_sha);request['packageSha256']='f'*64
        with self.assertRaises(ProtocolError):pkg.apply_review(ledger,request)
        with self.assertRaises(ProtocolError):pkg.apply_review(ledger,self.request(pkg,ledger,ledger.anchor_sha,'APPROVE_SUBMISSION'))
    def test_missing_journal_preserved_as_gap_without_success_declaration(self):
        self.f.f.journals.pop(next(iter(self.f.f.journals)))
        pkg=self.prepare();_,content=pkg.verify();self.assertGreater(content['evidenceGaps'],0)
        self.assertEqual(content['attempts'],3);self.assertEqual(content['technicalCoverage'],'INCOMPLETE')
        self.assertFalse(content['submissionAuthorized'])
    def test_another_package_ledger_cannot_be_used_as_this_dossier(self):
        a=self.prepare();b=self.prepare();ledger=b.prepare_review(self.ledgers,ref(500))
        with self.assertRaises(ProtocolError):a.view(ledger,ledger.anchor_sha)
        with self.assertRaises(ProtocolError):a.apply_review(ledger,self.request(a,ledger,ledger.anchor_sha))
    def test_browser_request_round_trip_records_only_internal_synthetic_review(self):
        import subprocess,json
        pkg=self.prepare();ledger=pkg.prepare_review(self.ledgers,ref(500));view=pkg.view(ledger,ledger.anchor_sha,self.f.f.plan)
        code="""import {readFileSync} from 'node:fs';
import './docs/javascripts/scientific-astrometry-context.js';
import './docs/javascripts/scientific-case-dossier.js';
const v=JSON.parse(readFileSync(0,'utf8'));
console.log(JSON.stringify(DSGCaseDossier.request(v,{eventRef:'000000000000000000000000000001f5',actorRef:'00000000000000000000000000000009',recordedUTC:'2026-10-15T00:00:00Z',action:'FOLLOW_UP',targetEventRef:null,note:'SYNTHETIC browser request; no Owner acceptance'})));
"""
        result=subprocess.run(['node','--input-type=module','-e',code],input=json.dumps(view),text=True,capture_output=True,check=True)
        changed=pkg.apply_review(ledger,json.loads(result.stdout))
        self.assertEqual(changed['events'][0]['decision']['action'],'FOLLOW_UP')
        self.assertFalse(changed['scientificAcceptance']);self.assertFalse(changed['submissionAuthorized'])
    def contextual_fixture(self):
        directory=self.f.f.root/'contextual-experiment';directory.mkdir()
        data=directory/'native-log.txt';data.write_text('SYNTHETIC archive fixture, no native execution')
        score={'sourceSha256':'a'*64,'scientificAcceptance':False}
        result_sha=write_new(directory/'Risultato-minimizzato-portale-v2.json',score)
        seal_sha=write_new(directory/'Sigillo-archivio-post-run.json',{'files':[{'path':data.name,**fingerprint(data)}]})
        return {'directory':str(directory),'prelaunchSha256':'b'*64,'sealSha256':seal_sha,'resultSha256':result_sha},score
    def test_context_archive_is_retained_without_changing_case_coverage_or_outcomes(self):
        descriptor,score=self.contextual_fixture();before=self.f.f.plan.events()[1]
        with patch('tools.scientific_transients.case_dossier.inspect_recovery',return_value=score) as verifier:
            pkg=self.prepare(recovery=descriptor)
        verifier.assert_called_once();_,content=pkg.verify()
        binding,_=read_json(pkg.directory/'retained/contextual-recovery.json')
        self.assertEqual(binding['relationship'],'CONTEXT_ONLY_NOT_CASE_RECOVERY_OR_VALIDATION')
        self.assertEqual(binding['qualifiedNullControlsAdded'],0)
        self.assertEqual(content['attempts'],3);self.assertEqual(self.f.f.plan.events()[1],before)
        self.assertIn('NON dimostra recupero',(pkg.directory/'preview/preview.txt').read_text(encoding='utf8'))
    def test_context_mutation_blocks_package_review(self):
        descriptor,score=self.contextual_fixture()
        with patch('tools.scientific_transients.case_dossier.inspect_recovery',return_value=score):pkg=self.prepare(recovery=descriptor)
        (pkg.directory/'retained/contextual-recovery/native-log.txt').write_text('changed')
        with self.assertRaises(ProtocolError):pkg.verify()
    def test_context_source_can_be_offline_after_snapshot(self):
        descriptor,score=self.contextual_fixture()
        with patch('tools.scientific_transients.case_dossier.inspect_recovery',return_value=score):pkg=self.prepare(recovery=descriptor)
        from pathlib import Path
        (Path(descriptor['directory'])/'native-log.txt').unlink();pkg.verify()
    def test_context_wrong_result_digest_rejected(self):
        descriptor,score=self.contextual_fixture();descriptor['resultSha256']='f'*64
        with patch('tools.scientific_transients.case_dossier.inspect_recovery',return_value=score):
            with self.assertRaises(ProtocolError):self.prepare(recovery=descriptor)
    def test_context_recomputed_result_must_equal_retained_result(self):
        descriptor,score=self.contextual_fixture()
        with patch('tools.scientific_transients.case_dossier.inspect_recovery',return_value={**score,'sourceSha256':'c'*64}):
            with self.assertRaises(ProtocolError):self.prepare(recovery=descriptor)
    def test_context_unpinned_descriptor_rejected_before_inspection(self):
        descriptor,score=self.contextual_fixture();descriptor['prelaunchSha256']=None
        with patch('tools.scientific_transients.case_dossier.inspect_recovery') as verifier:
            with self.assertRaises(ProtocolError):self.prepare(recovery=descriptor)
        verifier.assert_not_called()
    def test_unexecuted_plan_with_empty_event_directory_reopens_in_dossier_and_workspace(self):
        from tools.scientific_transients.test_plan import PlanVersion
        from tools.scientific_transients.case_workspace import assemble
        f=self.f.f;old=f.plan.read();roots=f.root/'unexecuted-plans';roots.mkdir()
        algorithm=f.plan.directory/next(r['path'] for r in old['evidence'] if r['role']=='ALGORITHM')
        rules=f.plan.directory/next(r['path'] for r in old['evidence'] if r['role']=='RULES')
        plan=PlanVersion.create(roots,old['draft'],f.actor,algorithm,rules)
        pkg=freeze(plan,ref(2),{},self.root,origin='SYNTHETIC_TEST')
        copied=PlanVersion(pkg.directory/'retained/plan'/plan.directory.name,plan.sha)
        self.assertEqual(copied.events()[0],[]);self.assertTrue((copied.directory/'events').is_dir())
        ledger=pkg.prepare_review(self.ledgers,ref(500));v=assemble(plan,pkg,ledger,ledger.anchor_sha)
        self.assertEqual(v['triplet']['attempts'],[]);self.assertEqual(v['triplet']['status'],'INCOMPLETE')
        self.assertFalse(v['scientificAcceptance']);self.assertEqual(v['qualifiedControls'],0)

if __name__=='__main__':unittest.main()
