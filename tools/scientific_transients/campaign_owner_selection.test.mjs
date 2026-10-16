import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';
const generated=spawnSync('python',['-c',[
'import json',
'from tools.scientific_transients.test_campaign_triplet import TripletTests',
'from tools.scientific_transients.owner_operation_stager import operation_key',
'f=TripletTests();f.setUp()',
't=f.prepare();t.register_all(f.worker);p=t.owner_proposal()',
"print(json.dumps({'proposal':p,'context':f.context,'receipt':f.f.service.review_receipt(p['planRef']),'key':operation_key(p,'DISPATCH_INTENT')}))",
'f.doCleanups()'].join('\n')],{encoding:'utf8',maxBuffer:8*1024*1024});
assert.equal(generated.status,0,generated.stderr);const fixtures=JSON.parse(generated.stdout);
const context=vm.createContext({crypto:webcrypto,TextEncoder,structuredClone});
for(const name of ['scientific-campaign-dispatch-contract.js','scientific-campaign-contract.js'])vm.runInContext(readFileSync('docs/javascripts/'+name,'utf8'),context);
const api=context.DSGCampaignContract;
const canonical=v=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):Array.isArray(v)?v.map(canonical):v;
const digest=async v=>Buffer.from(await webcrypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(canonical(v))))).toString('hex');
test('actual synthetic registered proposal binds authenticated frozen context and Python semantic key',async()=>{
  const view=await api.receipt(fixtures.receipt),selection=await api.dispatchProposal(view,fixtures.proposal,fixtures.context);
  assert.equal(selection.operationKeySha256,fixtures.key);assert.equal(selection.action,'DISPATCH_INTENT');
  assert.equal(selection.request.jobs.length,3);assert.equal(Object.isFrozen(selection.request),true);
});
test('unvalidated receipt cannot authorize proposal selection',async()=>{
  await assert.rejects(api.dispatchProposal(fixtures.receipt,fixtures.proposal,fixtures.context));
});
test('different context and altered binding fail even with rehashed proposal',async()=>{
  const view=await api.receipt(fixtures.receipt),p=structuredClone(fixtures.proposal);
  p.request.jobs[0].binding.inputRef='f'.repeat(32);
  const {proposalSha256,...rest}=p;p.proposalSha256=await digest(rest);
  await assert.rejects(api.dispatchProposal(view,p,fixtures.context));
  const c=structuredClone(fixtures.context);c.algorithmSha256='f'.repeat(64);
  await assert.rejects(api.dispatchProposal(view,fixtures.proposal,c));
});
test('unknown proposal fields rejected instead of exporting private metadata',async()=>{
  const view=await api.receipt(fixtures.receipt),p=structuredClone(fixtures.proposal);p.privatePath='synthetic';
  await assert.rejects(api.dispatchProposal(view,p,fixtures.context));
});

test('proposal and context are snapshotted before the first asynchronous hash',async()=>{
  const view=await api.receipt(fixtures.receipt),p=structuredClone(fixtures.proposal),c=structuredClone(fixtures.context);
  const original=p.request.decisionId;
  const pending=api.dispatchProposal(view,p,c);
  p.request.decisionId='f'.repeat(32);c.algorithmSha256='f'.repeat(64);
  const selection=await pending;
  assert.equal(selection.request.decisionId,original);
  assert.equal(selection.proposalSha256,fixtures.proposal.proposalSha256);
});
