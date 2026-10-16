import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';

const context=vm.createContext({crypto:webcrypto,TextEncoder,structuredClone});
for(const file of ['scientific-campaign-dispatch-contract.js','scientific-campaign-contract.js'])
  vm.runInContext(readFileSync('docs/javascripts/'+file,'utf8'),context);
const api=context.DSGCampaignContract;
// Actual application ports and memory queue, all references/stop declarations
// and quality counts synthetic. This tests UI capacity/invariants, not science.
const generated=spawnSync('python',['-c',[
  'import json',
  'from tools.scientific_transients.test_campaign_queue import CampaignQueueTests,ref,sha',
  'from tools.scientific_transients.test_unreserved_reconciliation import UnreservedTests',
  'f=CampaignQueueTests();f.setUp()',
  'partial=None',
  'for case in range(59):',
  ' owner=f.owner if case==0 else f.fixture.intent_request(case)',
  " intent=f.intent if case==0 else f.bridge.prepare_dispatch(ref(10),owner)",
  ' jobs=[]',
  " for ordinal,item in enumerate(owner['jobs']):",
  '  index=3*case+ordinal',
  "  f.q.register(item['binding'])",
  "  projected=f.bridge.project(ref(10),intent['sha256'],ordinal)",
  "  req={'workerId':ref(2),'rootId':owner['rootId'],'jobId':projected['jobId'],'bindingRef':item['binding']['bindingRef'],'reservationRef':ref(120000+index)}",
  "  job=f.bridge.admit_and_reserve(ref(10),intent['sha256'],ordinal,req,ref(100000+index))['job']",
  '  f.report_running(job)',
  "  report=sha(130000+index)",
  "  f.q.report(job['jobId'],{'attemptId':job['attemptId'],'leaseToken':job['leaseToken'],'sequence':2,'stage':'COMPLETED','result':{'reportSha256':report,'bindingRef':item['binding']['bindingRef'],'qualityCounts':{'measured':1,'excluded':0,'incomplete':0}}})",
  "  admission=f.s.dispatch_receipt(ref(10),intent['sha256'])['admissions'][-1]",
  "  f.bridge.close_frame(ref(10),{'decisionId':ref(110000+index),'admissionSha256':admission['sha256'],'jobId':job['jobId'],'attemptId':job['attemptId'],'reportSha256':report,'nativeStopEvidenceSha256':sha(140000+index),'technicalState':'COMPLETED','processStoppedReported':True})",
  "  frame=f.f.inputs[case]['frames'][ordinal]",
  "  jobs.append({'jobId':job['jobId'],'attemptId':job['attemptId'],'frameRef':frame['frameRef'],'inputSha256':frame['sha256'],'reportSha256':report})",
  " record=f.s.record_execution(ref(10),{'executionRef':ref(17000+case),'planSha256':f.s.view(ref(10))['planSha256'],'witnessRef':owner['witnessRef'],'algorithmSha256':sha(20),'contractSha256':sha(30),'scienceEvidenceSha256':sha(18000+case),'pipelineStatus':'COMPLETE_UNDER_FROZEN_RULES','outcome':'NO_ALERT','jobs':jobs})",
  " f.s.review_outcome(ref(10),{'decisionId':ref(19000+case),'executionSha256':record['sha256'],'acceptRecordedOutcome':True})",
  ' if case==0:partial=f.s.review_receipt(ref(10))',
  "f.s.finalize(ref(10),{'decisionId':ref(22000),'planHeadSha256':f.s.view(ref(10))['headSha256'],'acceptDeclaredCampaign':True})",
  'full=f.s.review_receipt(ref(10))',
  'u=UnreservedTests();u.setUp();u.admit_only();u.close(u.fence())',
  'unreserved=u.s.review_receipt(ref(10))',
  'r=CampaignQueueTests();r.setUp();j=r.reserve()["job"]',
  "r.q.report(j['jobId'],{'attemptId':j['attemptId'],'leaseToken':j['leaseToken'],'sequence':1,'stage':'RECOVERY_REQUIRED','result':None})",
  "r.q.close_recovery(j['jobId'],{'decisionId':ref(23000),'attemptId':j['attemptId'],'rootId':j['rootId'],'bindingRef':j['binding']['bindingRef'],'evidenceSha256':sha(23000),'quiescenceConfirmed':True})",
  "r.bridge.close_frame(ref(10),{'decisionId':ref(23001),'admissionSha256':r.receipt()['admissions'][0]['sha256'],'jobId':j['jobId'],'attemptId':j['attemptId'],'reportSha256':None,'nativeStopEvidenceSha256':sha(23000),'technicalState':'RECOVERY_REQUIRED','processStoppedReported':True})",
  "print(json.dumps({'full':full,'partial':partial,'unreserved':unreserved,'recovery':r.s.review_receipt(ref(10))}))"
].join('\n')],{encoding:'utf8',maxBuffer:8*1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(generated.status,0,generated.stderr);
const fixtures=JSON.parse(generated.stdout);

const canonical=v=>v&&typeof v==='object'&&!Array.isArray(v)?
  Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):Array.isArray(v)?v.map(canonical):v;
const digest=async v=>Buffer.from(await webcrypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(canonical(v))))).toString('hex');
async function rehash(v){
  let previous=null;
  for(const event of v.events){event.previous=previous;const {sha256,...payload}=event;event.sha256=await digest(payload);previous=event.sha256;}
  v.campaign.headSha256=previous;
  return v;
}

test('full534-event lifecycle verifies every technical event without truncating chronology',async()=>{
  assert.equal(fixtures.full.events.length,534);
  assert.equal(fixtures.full.events.filter(e=>e.kind==='START_ADMISSION').length,177);
  const checked=await api.receipt(fixtures.full);
  assert.equal(checked.events.length,534);assert.equal(checked.localBytesVerified,false);
  assert.equal(checked.implicitDispatch,false);
});
test('partial, never-reserved fence and owner-declared recovery preserve technical authority',async()=>{
  for(const key of ['partial','unreserved','recovery']){
    const checked=await api.receipt(fixtures[key]);assert.equal(checked.events.length,fixtures[key].events.length);
  }
});
for(const [name,key,mutate] of [
  ['unknown event','recovery',v=>v.events.at(-1).kind='UNKNOWN'],
  ['worker claims Owner authority','recovery',v=>v.events.at(-1).authority='AUTHENTICATED_OWNER_SCIENTIFIC_DECISION'],
  ['recovery proof swapped','recovery',v=>v.events.at(-1).facts.ownerRecoveryClosure.request.evidenceSha256='f'.repeat(64)],
  ['recovery falsely attested','recovery',v=>v.events.at(-1).facts.stopEvidence='OS_ATTESTED'],
  ['unreserved falsely completed','unreserved',v=>v.events.at(-1).facts.status='COMPLETED'],
  ['unreserved unexpected lease','unreserved',v=>v.events.at(-1).facts.queueFenceSnapshot.leaseToken='f'.repeat(64)],
  ['launch inferred from intent','partial',v=>v.events.find(e=>e.kind==='DISPATCH_INTENT').facts.launchAuthorized=true],
  ['admission order altered','partial',v=>v.events.find(e=>e.kind==='START_ADMISSION').request.ordinal=2],
  ['context mismatched namespace','partial',v=>v.events.find(e=>e.kind==='DISPATCH_INTENT').request.queueNamespaceSha256='f'.repeat(64)],
])test(name+' rejected even after recomputing the outer event chain',async()=>{
  const value=structuredClone(fixtures[key]);mutate(value);await rehash(value);await assert.rejects(api.receipt(value));
});
test('unknown technical facts and unbounded event arrays fail closed',async()=>{
  const value=structuredClone(fixtures.recovery);value.events.at(-1).facts.extra='private';await rehash(value);
  await assert.rejects(api.receipt(value));
  const large=structuredClone(fixtures.partial);large.events=Array(1025).fill(large.events[0]);await assert.rejects(api.receipt(large));
});
test('bound execution must retain the selected jobs, inputs and all three exact closures',()=>{
  const h={check:v=>assert.ok(v),hash:v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v)};
  const inspect=context.DSGCampaignDispatchContract.execution,record=fixtures.full.executions[0];
  inspect(record,fixtures.full.events,h);
  for(const key of ['jobId','frameRef','inputSha256','attemptId','reportSha256']){
    const changed=structuredClone(record);changed.request.jobs[0][key]=key==='jobId'?'TRN_'+'f'.repeat(32):'f'.repeat(key.endsWith('Sha256')?64:32);
    assert.throws(()=>inspect(changed,fixtures.full.events,h));
  }
  const withoutClosure=fixtures.full.events.filter(e=>!(e.kind==='FRAME_CLOSURE'&&e.request.jobId===record.request.jobs[0].jobId));
  assert.throws(()=>inspect(record,withoutClosure,h));
});

for(const targetKind of ['DISPATCH_INTENT','START_ADMISSION','FRAME_CLOSURE'])
  test('execution before '+targetKind+' rejected with valid recomputed hashes and references',async()=>{
    const value=structuredClone(fixtures.partial);
    await api.receipt(value);
    const index=value.events.findIndex(e=>e.kind==='EXECUTION');
    const [execution]=value.events.splice(index,1);
    const target=value.events.findIndex(e=>e.kind===targetKind);
    assert.ok(target>=0);
    value.events.splice(target,0,execution);
    const remap=new Map();let previous=null;
    function references(item){
      if(Array.isArray(item))return item.map(references);
      if(item&&typeof item==='object')return Object.fromEntries(Object.entries(item).map(([key,v])=>[key,references(v)]));
      return remap.get(item)??item;
    }
    for(let i=0;i<value.events.length;i++){
      const old=value.events[i].sha256,event=references(value.events[i]);
      event.previous=previous;
      const {sha256,...payload}=event;
      event.sha256=await digest(payload);
      remap.set(old,event.sha256);previous=event.sha256;value.events[i]=event;
    }
    value.campaign.headSha256=previous;
    for(const record of value.executions)
      if(record.review)record.review=value.events.find(e=>e.kind==='OUTCOME_REVIEW'&&e.request.executionSha256===record.sha256);
    await assert.rejects(api.receipt(value));
  });
