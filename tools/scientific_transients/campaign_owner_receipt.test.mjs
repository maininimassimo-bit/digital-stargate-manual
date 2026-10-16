import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';
const generated=spawnSync('python',['-c',[
'import json',
'from tools.scientific_transients.test_campaign_triplet import TripletTests,ref',
'from tools.scientific_transients import owner_operation_stager as m',
'from tools.scientific_transients.confirmatory_campaign import fingerprint',
'f=TripletTests();f.setUp();t=f.prepare();t.register_all(f.worker);p=t.owner_proposal()',
"before=f.f.service.review_receipt(p['planRef'])",
"event=f.owner.request('/v1/transient-analysis/campaigns/'+p['planRef']+'/dispatch-intents',p['request'])",
"raw=f.f.service.review_receipt(p['planRef'])",
"[f.bridge.project(p['planRef'],event['sha256'],i) for i in range(3)]",
"technical=[f.bridge.technical_context(p['planRef'],event['sha256'],i) for i in range(3)]",
"receipt=dict(protocol=m.INTENT_RECEIPT,planRef=p['planRef'],intentSha256=event['sha256'],contextSha256=p['request']['contextSha256'],archiveSha256=p['request']['archiveSha256'],queueNamespaceSha256=event['request']['queueNamespaceSha256'],orderedJobSelectionDigests=[fingerprint(j) for j in p['request']['jobs']],operationKeySha256=m.operation_key(p,'DISPATCH_INTENT'),requestSha256=m.request_sha(p['request']),launchAuthorized=False,scientificValidation='NOT_VALIDATED')",
"receipt['receiptSha256']=fingerprint(receipt);m.validate_intent_receipt(receipt,p)",
"selections=[dict(key=m.operation_key(p,'PROJECT_JOB',receipt,i),selection=m.projection_selection_sha(p,receipt,i)) for i in range(3)]",
"f.f.service.revoke(p['planRef'],dict(decisionId=ref(99999),planHeadSha256=f.f.service.view(p['planRef'])['headSha256'],evidenceSha256='f'*64,reason='OWNER_WITHDRAWAL'))",
"print(json.dumps(dict(proposal=p,before=before,raw=raw,technical=technical,receipt=receipt,selections=selections,revoked=f.f.service.review_receipt(p['planRef']))))",
'f.doCleanups()'].join('\n')],{encoding:'utf8',maxBuffer:8*1024*1024});
assert.equal(generated.status,0,generated.stderr);const fixtures=JSON.parse(generated.stdout);
const context=vm.createContext({crypto:webcrypto,TextEncoder,structuredClone});
for(const name of ['scientific-campaign-dispatch-contract.js','scientific-campaign-contract.js','scientific-campaign-owner-receipt.js'])vm.runInContext(readFileSync('docs/javascripts/'+name,'utf8'),context);
const api=context.DSGCampaignOwnerReceipt;
test('recorded intent receipt matches offline Python schema and digests exactly',async()=>{
  const receipt=await api.intent(fixtures.raw,fixtures.proposal);
  assert.deepEqual(JSON.parse(JSON.stringify(receipt)),fixtures.receipt);
});
test('three projection selections match Python and retain ordinal distinctions',async()=>{
  for(let i=0;i<3;i++){
    const selected=await api.projection(fixtures.raw,fixtures.proposal,fixtures.receipt,i);
    assert.equal(selected.operationKeySha256,fixtures.selections[i].key);
    assert.equal(selected.proposalSha256,fixtures.selections[i].selection);
    assert.ok(selected.relativePath.endsWith('/jobs/'+i+'/project'));
  }
});
test('unobserved intent does not become permission to retry',async()=>{
  await assert.rejects(api.intent(fixtures.before,fixtures.proposal));
});
test('revoked campaign can be reconciled historically but cannot authorize projection',async()=>{
  const receipt=await api.intent(fixtures.revoked,fixtures.proposal);
  assert.equal(receipt.intentSha256,fixtures.receipt.intentSha256);
  await assert.rejects(api.projection(fixtures.revoked,fixtures.proposal,fixtures.receipt,0));
});
test('changed receipt, invalid ordinal and changed proposal are rejected',async()=>{
  const receipt=structuredClone(fixtures.receipt);receipt.queueNamespaceSha256='f'.repeat(64);
  await assert.rejects(api.projection(fixtures.raw,fixtures.proposal,receipt,0));
  for(const i of [-1,3,true])await assert.rejects(api.projection(fixtures.raw,fixtures.proposal,fixtures.receipt,i));
  const proposal=structuredClone(fixtures.proposal);proposal.request.decisionId='f'.repeat(32);
  await assert.rejects(api.intent(fixtures.raw,proposal));
});
test('caller mutations during reads cannot change retained receipt selection',async()=>{
  const proposal=structuredClone(fixtures.proposal),raw=structuredClone(fixtures.raw);
  const pending=api.intent(raw,proposal);proposal.request.decisionId='f'.repeat(32);raw.events=[];
  assert.deepEqual(JSON.parse(JSON.stringify(await pending)),fixtures.receipt);
});

test('exact projection existence is verifiable for all three jobs without launch authority',async()=>{
  for(let i=0;i<3;i++){
    const receipt=await api.projected(fixtures.raw,fixtures.proposal,fixtures.receipt,i,fixtures.technical[i]);
    assert.equal(receipt.jobId,fixtures.technical[i].jobId);assert.equal(receipt.launchAuthorized,false);
    assert.equal(receipt.requestSelectionSha256,fixtures.technical[i].requestSelectionSha256);
  }
});
test('consumed projection remains historical existence without permission to reserve again',async()=>{
  const technical=structuredClone(fixtures.technical[0]);technical.projectionState='RUNNING';technical.reservationConsumed=true;
  const receipt=await api.projected(fixtures.raw,fixtures.proposal,fixtures.receipt,0,technical);
  assert.equal(receipt.projectionObserved,true);assert.equal(receipt.reservationFreshness,'NOT_ATTESTED');
  assert.equal(receipt.launchAuthorized,false);
  const earlier=await api.projected(fixtures.raw,fixtures.proposal,fixtures.receipt,0,fixtures.technical[0]);
  assert.equal(receipt.receiptSha256,earlier.receiptSha256);
});
test('wrong namespace, job order or private lease data cannot confirm a projection',async()=>{
  const technical=structuredClone(fixtures.technical[0]);technical.queueNamespaceSha256='f'.repeat(64);
  await assert.rejects(api.projected(fixtures.raw,fixtures.proposal,fixtures.receipt,0,technical));
  await assert.rejects(api.projected(fixtures.raw,fixtures.proposal,fixtures.receipt,1,fixtures.technical[0]));
  await assert.rejects(api.projected(fixtures.raw,fixtures.proposal,fixtures.receipt,0,{...fixtures.technical[0],leaseToken:'synthetic-private'}));
  await assert.rejects(api.projected(fixtures.revoked,fixtures.proposal,fixtures.receipt,0,fixtures.technical[0]));
});
