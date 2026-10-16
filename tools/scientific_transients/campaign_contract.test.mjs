import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';

const context=vm.createContext({crypto:webcrypto,TextEncoder,structuredClone});
vm.runInContext(readFileSync('docs/javascripts/scientific-campaign-contract.js','utf8'),context);
const api=context.DSGCampaignContract;
const generated=spawnSync('python',['-c',[
  'import json,datetime as dt',
  'from tools.scientific_transients.test_confirmatory_campaign import CampaignTests,ref,sha',
  'f=CampaignTests();f.setUp()',
  'draft=f.service.review_receipt(ref(10))',
  'freeze=f.freeze();f.now=f.now-dt.timedelta(seconds=1)+dt.timedelta(microseconds=1);f.completed(0)',
  'partial=f.service.review_receipt(ref(10))',
  'for i in range(1,59):f.completed(i)',
  'ready=f.service.review_receipt(ref(10))',
  "f.service.finalize(ref(10),{'decisionId':ref(22000),'planHeadSha256':ready['campaign']['headSha256'],'acceptDeclaredCampaign':True})",
  'accepted=f.service.review_receipt(ref(10))',
  "f.service.revoke(ref(10),{'decisionId':ref(22001),'planHeadSha256':accepted['campaign']['headSha256'],'evidenceSha256':sha(22002),'reason':'REFERENCE_INVALID'})",
  'revoked=f.service.review_receipt(ref(10))',
  "print(json.dumps({'draft':draft,'partial':partial,'ready':ready,'accepted':accepted,'revoked':revoked,'freeze':freeze}))"
].join('\n')],{encoding:'utf8',maxBuffer:8*1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(generated.status,0,generated.stderr);
const fixtures=JSON.parse(generated.stdout);

test('actual Python receipts preserve draft, partial, conditional result, acceptance and revocation',async()=>{
  for(const [name,qualified] of [['draft',0],['partial',1],['ready',59],['accepted',59],['revoked',0]]){
    const value=await api.receipt(fixtures[name]);assert.equal(value.campaign.qualifiedControls,qualified);
    assert.equal(value.localBytesVerified,false);assert.equal(value.implicitDispatch,false);
  }
});
test('only exact decision identity and request acknowledge a lost metadata response',async()=>{
  const value=await api.receipt(fixtures.partial);
  assert.equal(api.reconcile(value,fixtures.freeze),'CONFIRMED');
  assert.equal(api.reconcile(value,{...fixtures.freeze,approveAlgorithm:false}),'CONFLICT');
  assert.equal(api.reconcile(value,{...fixtures.freeze,decisionId:'f'.repeat(32)}),'NOT_OBSERVED');
  assert.throws(()=>api.reconcile(fixtures.partial,fixtures.freeze));
});
test('validated snapshot is detached and immutable during later reconciliation',async()=>{
  const source=structuredClone(fixtures.partial),value=await api.receipt(source);
  source.events.length=0;assert.equal(api.reconcile(value,fixtures.freeze),'CONFIRMED');
  assert.throws(()=>{value.events[1].request.approveAlgorithm=false;});
});
for(const [name,source,change] of [
  ['private root field','partial',v=>v.privatePath='secret'],
  ['invented qualification','draft',v=>v.campaign.qualifiedControls=59],
  ['qualified without input reviews','partial',v=>{v.campaign.cases[0].inputReviewedByOwner=false;v.campaign.ownerReviewedInputs=58;}],
  ['altered plan','partial',v=>v.plan.algorithmSha256='f'.repeat(64)],
  ['reordered cases','partial',v=>v.campaign.cases.reverse()],
  ['event body changed','partial',v=>v.events[1].request.approveAlgorithm=false],
  ['actor changed','partial',v=>v.events[1].actorRef='f'.repeat(32)],
  ['private lease field','partial',v=>v.executions[0].jobSnapshots[0].leaseToken='private'],
  ['execution science proof changed','partial',v=>v.executions[0].request.scienceEvidenceSha256='f'.repeat(64)],
  ['unlogged review','partial',v=>v.executions[0].review.request.decisionId='f'.repeat(32)],
  ['pre-freeze job','partial',v=>v.executions[0].jobSnapshots[0].createdAt=v.campaign.frozenUTC],
  ['false bound','ready',v=>v.campaign.statisticalResult.oneSidedUpperBound=0],
  ['unrecorded final acceptance','ready',v=>{v.campaign.status='OWNER_ACCEPTED_CAMPAIGN_SCOPE_ONLY';v.campaign.scientificValidation='OWNER_ACCEPTED_DECLARED_CAMPAIGN_ONLY';}],
  ['revocation hidden','revoked',v=>{v.campaign.blockers=v.campaign.blockers.filter(r=>r!=='PLAN_REVOKED');}],
  ['unknown blocker','draft',v=>v.campaign.blockers.push('<script>')]
])test(name+' rejected',async()=>{const value=structuredClone(fixtures[source]);change(value);await assert.rejects(api.receipt(value));});
