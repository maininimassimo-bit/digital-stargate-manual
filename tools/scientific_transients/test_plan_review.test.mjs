import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {webcrypto} from 'node:crypto';
import '../../docs/javascripts/scientific-test-plan-review.js';
const ref=n=>n.toString(16).padStart(32,'0');
const sample=()=>({schema:'BKL051_TEST_PLAN_REVIEW_V1',planRef:ref(1),versionRef:ref(2),planSha256:'1'.repeat(64),headSha256:'2'.repeat(64),state:'FROZEN_PRELIMINARY',attestation:'LOCAL_DECLARATION_ONLY',scienceValidation:'NOT_VALIDATED',qualified:0,statisticalResult:null,cases:[{caseRef:ref(3),clusterRef:ref(4),qualification:'CANDIDATE',attempts:[],scientificOutcome:'NOT_EVALUATED',outcomeAttemptHeadSha256:null,ownerReview:'PENDING'}]});
const attempt=()=>({journalHeadSha256:'3'.repeat(64),technicalState:'COMPLETED',coverage:'PARTIAL',algorithmMatches:true,chronology:'PREEXISTING'});
test('derived attempt requires V2 and a pinned archive digest',()=>{
  const v=sample();v.cases[0].attempts=[{...attempt(),inputDerivationSha256:'4'.repeat(64)}];
  assert.throws(()=>DSGTestPlanReview.inspect(v));v.schema='BKL051_TEST_PLAN_REVIEW_V2';
  assert.equal(DSGTestPlanReview.inspect(v).qualified,0);
  v.cases[0].attempts[0].inputDerivationSha256='unbound';assert.throws(()=>DSGTestPlanReview.inspect(v));
});
test('V2 refuses private derivation paths and invented validation',()=>{
  const v=sample();v.schema='BKL051_TEST_PLAN_REVIEW_V2';
  v.cases[0].attempts=[{...attempt(),inputDerivationSha256:'4'.repeat(64),calibrationValidated:true}];
  assert.throws(()=>DSGTestPlanReview.inspect(v));delete v.cases[0].attempts[0].calibrationValidated;
  v.cases[0].attempts[0].path='F:/private';assert.throws(()=>DSGTestPlanReview.inspect(v));
});
test('actual Python derived mock archive imports with audit and raw-frame coverage',()=>{
  const r=spawnSync('python',['-c',[
    'import json',
    'from tools.scientific_transients.test_derived_input_binding import DerivedBindingTests',
    'from tools.scientific_transients.plan_readiness import assess',
    'from tools.scientific_transients.triplet_report import inspect_triplet',
    'f=DerivedBindingTests();f.setUp()',
    'try:',
    ' p=f.prepare();e=f.execution(p);f.run_mock(e)',
    ' event=f.plan.events()[0][0];i=event["data"]["identity"]["attemptId"];root=f.operator.roots["journals"]',
    ' print(json.dumps([f.plan.view(),assess(f.plan,root),inspect_triplet(f.plan,event["caseRef"],{i:root/i})]))',
    'finally:f.doCleanups()'
  ].join('\n')],{encoding:'utf8'});
  assert.equal(r.status,0,r.stderr);const [view,audit,triplet]=JSON.parse(r.stdout);
  assert.equal(DSGTestPlanReview.inspect(view).executed,1);
  assert.equal(DSGTestPlanReview.inspectAudit(audit,view).rechecked,1);
  DSGTestPlanReview.inspectTriplet(triplet,view);
  assert.equal(triplet.frames.filter(f=>f.attemptHeads.length).length,1);
});
test('preliminary versions never count as qualified',()=>assert.equal(DSGTestPlanReview.inspect(sample()).qualified,0));
test('documented case and completed technical run are distinct',()=>{const v=sample();v.cases[0].qualification='DOCUMENTED_PENDING_REVIEW';v.cases[0].attempts=[attempt()];const s=DSGTestPlanReview.inspect(v);assert.equal(s.documented,1);assert.equal(s.executed,1);assert.equal(s.qualified,0);assert.equal(s.statisticalResult,null);});
test('failed attempts do not count as completed and cannot carry no-signal outcome',()=>{const v=sample();v.cases[0].attempts=[{...attempt(),technicalState:'FAILED'}];assert.equal(DSGTestPlanReview.inspect(v).failed,1);v.cases[0].scientificOutcome='NO_SIGNAL_DECLARED';assert.throws(()=>DSGTestPlanReview.inspect(v));});
test('invented qualification, scientific acceptance and numeric statistics refused',()=>{for(const change of [v=>v.qualified=59,v=>v.statisticalResult=.0495,v=>v.scienceValidation='VALIDATED',v=>v.cases[0].qualification='QUALIFIED',v=>v.cases[0].ownerReview='APPROVED']){const v=sample();change(v);assert.throws(()=>DSGTestPlanReview.inspect(v));}});
test('private paths, duplicate cases and duplicate journal heads refused',()=>{let v=sample();v.path='F:/private';assert.throws(()=>DSGTestPlanReview.inspect(v));v=sample();v.cases.push(structuredClone(v.cases[0]));assert.throws(()=>DSGTestPlanReview.inspect(v));v=sample();v.cases[0].attempts=[attempt(),attempt()];assert.throws(()=>DSGTestPlanReview.inspect(v));});
test('unknown enum values and nonboolean algorithm match refused',()=>{const v=sample();v.cases[0].attempts=[{...attempt(),algorithmMatches:'yes'}];assert.throws(()=>DSGTestPlanReview.inspect(v));});
test('local request binds evidence, case and expected head without paths',()=>{const v=sample(),a={role:'RATIONALE',sha256:'4'.repeat(64),base64:'eA=='};const p=DSGTestPlanReview.request(v,ref(8),ref(3),'QUALIFICATION','NON_EVALUABLE',ref(9),'2026-10-14T00:00:00Z',[a]);assert.equal(p.expectedHeadSha256,v.headSha256);assert.equal(p.planSha256,v.planSha256);assert.equal(p.data.state,'NON_EVALUABLE');assert.equal(JSON.stringify(p).includes('path'),false);});
test('documented qualification requires all three roles and never QUALIFIED',()=>{const v=sample(),a={role:'RATIONALE',sha256:'4'.repeat(64),base64:'eA=='};assert.throws(()=>DSGTestPlanReview.request(v,ref(8),ref(3),'QUALIFICATION','DOCUMENTED_PENDING_REVIEW',ref(9),'2026-10-14T00:00:00Z',[a]));assert.throws(()=>DSGTestPlanReview.request(v,ref(8),ref(3),'QUALIFICATION','QUALIFIED',ref(9),'2026-10-14T00:00:00Z',[a]));});
test('outcome request must target this case completed attempt',()=>{const v=sample(),a={role:'SCIENTIFIC_OUTCOME',sha256:'4'.repeat(64),base64:'eA=='};assert.throws(()=>DSGTestPlanReview.request(v,ref(8),ref(3),'OUTCOME_REVIEW','NO_SIGNAL_DECLARED',ref(9),'2026-10-14T00:00:00Z',[a],'3'.repeat(64)));v.cases[0].attempts=[attempt()];assert.equal(DSGTestPlanReview.request(v,ref(8),ref(3),'OUTCOME_REVIEW','NO_SIGNAL_DECLARED',ref(9),'2026-10-14T00:00:00Z',[a],'3'.repeat(64)).data.targetAttemptHeadSha256,'3'.repeat(64));});
const auditSample=()=>({schema:'BKL051_CONFIRMATORY_BLOCKERS_V1',planRef:ref(1),versionRef:ref(2),planSha256:'1'.repeat(64),headSha256:'2'.repeat(64),status:'BLOCKED',scope:'READ_ONLY_LOCAL_PREREQUISITES_AUDIT',
  globalBlockers:['PRELIMINARY_PLAN_ONLY','ALGORITHM_AND_RULES_SCIENTIFIC_APPROVAL_MISSING','FREEZE_CHRONOLOGY_NOT_ATTESTED','SCIENTIFIC_PIPELINE_NOT_VALIDATED','QUALIFIED_INDEPENDENT_CONTROLS_MISSING','OWNER_ACCEPTANCE_NOT_GRANTED'],
  requiredIndependentControls:59,falsePositiveMaximum:.05,confidence:.95,candidateCases:1,declaredDependencyGroups:1,qualifiedControls:0,confirmatoryEligibleCases:0,statisticalResult:null,scienceValidation:'NOT_VALIDATED',
  cases:[{caseRef:ref(3),clusterRef:ref(4),qualification:'CANDIDATE',attempts:[],scientificOutcome:'NOT_EVALUATED',ownerReview:'MISSING',confirmatoryEligible:false,
    blockers:['NULL_REFERENCE_NOT_ATTESTED','INDEPENDENCE_NOT_ATTESTED','QUALIFICATION_MISSING','ATTEMPT_MISSING','SCIENTIFIC_OUTCOME_MISSING','OWNER_REVIEW_MISSING']}]});
test('audit must match exact plan and event head and cannot grant pass',()=>{
  assert.equal(DSGTestPlanReview.inspectAudit(auditSample(),sample()).cases,1);
  for(const mutate of [a=>a.headSha256='f'.repeat(64),a=>a.planSha256='e'.repeat(64),a=>a.status='PASS',a=>a.qualifiedControls=59,a=>a.statisticalResult=.0495,a=>a.cases[0].confirmatoryEligible=true]){const a=auditSample();mutate(a);assert.throws(()=>DSGTestPlanReview.inspectAudit(a,sample()));}
});
test('audit cannot omit blockers or invent counts and private fields',()=>{
  for(const mutate of [a=>a.globalBlockers.pop(),a=>a.cases[0].blockers.pop(),a=>a.candidateCases=59,a=>a.path='F:/private',a=>a.cases[0].caseRef=ref(8),a=>a.cases[0].blockers.push('<script>')]){const a=auditSample();mutate(a);assert.throws(()=>DSGTestPlanReview.inspectAudit(a,sample()));}
});
const tripletSample=()=>({schema:'BKL051_TRIPLET_TECHNICAL_V1',planRef:ref(1),versionRef:ref(2),planSha256:'1'.repeat(64),headSha256:'2'.repeat(64),caseRef:ref(3),status:'INCOMPLETE',
  frames:[20,21,22].map(n=>({frameRef:ref(n),sha256:n.toString(16).padStart(64,'0'),attemptHeads:[]})),attempts:[],
  blockers:['EXACTLY_THREE_LINKED_ATTEMPTS_REQUIRED','ONE_ATTEMPT_PER_DISTINCT_FRAME_REQUIRED'],scope:'THREE_SINGLE_FRAME_DIAGNOSTIC_RUNS_ONLY',qualifiedControls:0,
  scienceValidation:'NOT_VALIDATED',photometricComparability:'NOT_VALIDATED',crossEpochResult:null,fullVariance:null,significance:null,statisticalResult:null,confirmatoryEligible:false});
test('triplet receipt cannot invent significance, duplicate images or grant complete coverage',()=>{
  assert.equal(DSGTestPlanReview.inspectTriplet(tripletSample(),sample()).complete,false);
  for(const mutate of [t=>t.significance=5,t=>t.qualifiedControls=1,t=>t.status='TECHNICAL_COVERAGE_COMPLETE',t=>t.frames[1].sha256=t.frames[0].sha256,t=>t.headSha256='f'.repeat(64),t=>t.blockers.pop()]){const t=tripletSample();mutate(t);assert.throws(()=>DSGTestPlanReview.inspectTriplet(t,sample()));}
});
function ui(withForm=false,withAudit=false,withTriplet=false){
  class Element{
    constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.attrs={};this.style={};this.value='';this.files=[];this.handlers={};}
    addEventListener(name,fn){this.handlers[name]=fn;}
    click(){this.clicked=true;}
    append(...items){this.children.push(...items);}
    replaceChildren(...items){this.children=items;this.textContent='';}
    setAttribute(k,v){this.attrs[k]=v;}
  }
  const input={value:'selected',files:[],addEventListener:(name,fn)=>{input.change=fn;}},status=new Element('p'),output=new Element('div');
  const controls=Object.fromEntries(['[data-case]','[data-action]','[data-actor]','[data-attempt]','button','[role="status"]',
    '[data-evidence="NULL_REFERENCE"]','[data-evidence="INDEPENDENCE"]','[data-evidence="RATIONALE"]','[data-evidence="SCIENTIFIC_OUTCOME"]'].map(k=>[k,new Element('control')]));
  const form={querySelector:s=>controls[s]},blobs=[],auditInput=new Element('input'),auditStatus=new Element('p'),auditOutput=new Element('div');
  const auditRoot={querySelector:s=>s==='input'?auditInput:s==='[role="status"]'?auditStatus:auditOutput};
  const tripletInput=new Element('input'),tripletStatus=new Element('p'),tripletOutput=new Element('div');
  const tripletRoot={querySelector:s=>s==='input'?tripletInput:s==='[role="status"]'?tripletStatus:tripletOutput};
  const root={dataset:{},isConnected:true,querySelector:s=>s==='input'?input:s==='[role="status"]'?status:s==='[data-dsg-triplet]'?(withTriplet?tripletRoot:null):s==='[data-dsg-readiness]'?(withAudit?auditRoot:null):s==='[data-dsg-plan-request]'?(withForm?form:null):output};
  const document={readyState:'complete',querySelector:()=>root,createElement:t=>new Element(t)};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-test-plan-review.js',import.meta.url),'utf8'),{document,crypto:webcrypto,Blob,
    URL:{createObjectURL:b=>{blobs.push(b);return 'blob:test';},revokeObjectURL:()=>{}},setTimeout:fn=>fn(),btoa:s=>Buffer.from(s,'binary').toString('base64')});
  return {input,status,output,root,controls,blobs,auditInput,auditStatus,auditOutput,tripletInput,tripletStatus,tripletOutput};
}
test('UI labels archived derived provenance and pending calibration',async()=>{
  const u=ui(),v=sample();v.schema='BKL051_TEST_PLAN_REVIEW_V2';
  v.cases[0].attempts=[{...attempt(),inputDerivationSha256:'4'.repeat(64)}];
  u.input.files=[{size:100,text:async()=>JSON.stringify(v)}];await u.input.change();
  assert.match(JSON.stringify(u.output.children),/derivato con prova archiviata, calibrazione scientifica non attestata/);
});
test('UI table has caption and named keyboard region and clears invalid import',async()=>{const u=ui();u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();assert.equal(u.output.children.length,3);const region=u.output.children[2];assert.equal(region.tabIndex,0);assert.equal(region.attrs.role,'region');assert.equal(region.children[0].children[0].tag,'caption');assert.match(u.output.children[0].textContent,/Controlli qualificati: 0/);u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();assert.equal(u.output.children.length,0);assert.match(u.status.textContent,/non valida/);});
test('UI no read above 1 MiB',async()=>{const u=ui();u.input.files=[{size:1048577,text:()=>{throw Error('should not read');}}];await u.input.change();assert.equal(u.output.children.length,0);});
test('UI late read cannot overwrite latest input',async()=>{const u=ui();let resolve;u.input.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.input.change();u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();resolve(JSON.stringify(sample()));await old;assert.equal(u.output.children.length,0);assert.match(u.status.textContent,/non valida/);});
test('UI ignores result after page disconnected',async()=>{const u=ui();let resolve;u.input.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.input.change();u.root.isConnected=false;resolve(JSON.stringify(sample()));await old;assert.equal(u.output.children.length,0);});
test('UI request saves only selected evidence with digest and disables after invalid import',async()=>{
  const u=ui(true);u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();
  const c=u.controls;c['[data-case]'].value=ref(3);c['[data-action]'].value='QUALIFICATION:NON_EVALUABLE';c['[data-actor]'].value=ref(9);
  c['[data-evidence="RATIONALE"]'].files=[{size:1,arrayBuffer:async()=>new Uint8Array([120]).buffer}];
  await c.button.handlers.click();assert.equal(u.blobs.length,1);const request=JSON.parse(await u.blobs[0].text());
  assert.equal(request.attachments.length,1);assert.equal(request.attachments[0].base64,'eA==');assert.equal(request.attachments[0].sha256,'2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881');
  assert.equal(request.expectedHeadSha256,sample().headSha256);assert.match(c['[role="status"]'].textContent,/Nessun evento/);
  u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();assert.equal(c.button.disabled,true);
});
test('UI request missing evidence produces no downloadable package',async()=>{
  const u=ui(true);u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();
  u.controls['[data-action]'].value='QUALIFICATION:DOCUMENTED_PENDING_REVIEW';await u.controls.button.handlers.click();
  assert.equal(u.blobs.length,0);assert.match(u.controls['[role="status"]'].textContent,/non preparata/);
});
test('UI audit requires plan first, then clears on invalid or newer plan import',async()=>{
  const u=ui(false,true);const loadAudit=async()=>{u.auditInput.files=[{size:100,text:async()=>JSON.stringify(auditSample())}];await u.auditInput.handlers.change();};
  await loadAudit();assert.equal(u.auditOutput.children.length,0);
  u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();await loadAudit();
  assert.equal(u.auditOutput.children.length,2);assert.match(u.auditOutput.children[0].textContent,/bloccato/);
  u.auditInput.files=[{size:1,text:async()=>'{'}];await u.auditInput.handlers.change();assert.equal(u.auditOutput.children.length,0);
  await loadAudit();u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();assert.equal(u.auditOutput.children.length,0);
});
test('UI late audit cannot overwrite newer plan',async()=>{
  const u=ui(false,true);u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();
  let resolve;u.auditInput.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.auditInput.handlers.change();
  u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();resolve(JSON.stringify(auditSample()));await old;
  assert.equal(u.auditOutput.children.length,0);assert.match(u.auditStatus.textContent,/Nessun controllo/);
});
test('UI audit rejects oversized file without reading',async()=>{
  const u=ui(false,true);u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();let read=false;
  u.auditInput.files=[{size:1048577,text:async()=>{read=true;return '{}';}}];await u.auditInput.handlers.change();assert.equal(read,false);assert.equal(u.auditOutput.children.length,0);
});
test('UI triplet receipt clears invalid input and changed plan',async()=>{
  const u=ui(false,false,true);u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();
  const load=async()=>{u.tripletInput.files=[{size:100,text:async()=>JSON.stringify(tripletSample())}];await u.tripletInput.handlers.change();};
  await load();assert.equal(u.tripletOutput.children.length,2);assert.match(u.tripletOutput.children[0].textContent,/incompleta/);
  u.tripletInput.files=[{size:1,text:async()=>'{'}];await u.tripletInput.handlers.change();assert.equal(u.tripletOutput.children.length,0);
  await load();u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();assert.equal(u.tripletOutput.children.length,0);
});
test('late triplet read cannot restore result after plan change',async()=>{
  const u=ui(false,false,true);u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();
  let resolve;u.tripletInput.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.tripletInput.handlers.change();
  u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();resolve(JSON.stringify(tripletSample()));await old;
  assert.equal(u.tripletOutput.children.length,0);
});
test('UI triplet rejects oversized file before read',async()=>{
  const u=ui(false,false,true);u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();let read=false;
  u.tripletInput.files=[{size:1048577,text:async()=>{read=true;return '{}';}}];await u.tripletInput.handlers.change();assert.equal(read,false);
});
test('three distinct plan-bound jobs produce a complete technical receipt compatible with portal',()=>{
  const result=spawnSync('python',['-c',[
    'import json',
    'from tools.scientific_transients.test_triplet_report import TripletTests',
    'from tools.scientific_transients.triplet_report import inspect_triplet',
    'from tools.scientific_transients.test_test_plan import ref',
    't=TripletTests(); t.setUp()',
    'try:',
    ' for index in range(3): t.execute(index)',
    " print(json.dumps({'plan':t.plan.view(),'triplet':inspect_triplet(t.plan,ref(2),t.journals)}))",
    'finally: t.doCleanups()',
  ].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
  assert.equal(result.status,0,result.stderr);const {plan,triplet}=JSON.parse(result.stdout);
  assert.equal(DSGTestPlanReview.inspectTriplet(triplet,plan).complete,true);assert.equal(triplet.qualifiedControls,0);
  triplet.attempts[0].verification='UNAVAILABLE_OR_CHANGED';assert.throws(()=>DSGTestPlanReview.inspectTriplet(triplet,plan));
});
test('audit exported by Python matches browser plan and rechecked journal facts',()=>{
  const result=spawnSync('python',['-c',[
    'import json',
    'from tools.scientific_transients.test_test_plan import AttemptLinkTests',
    'from tools.scientific_transients.plan_readiness import assess',
    't=AttemptLinkTests(); t.setUp()',
    'try:',
    ' t.link(t.complete())',
    " print(json.dumps({'plan':t.plan.view(),'audit':assess(t.plan,t.journal.directory.parent)}))",
    'finally: t.doCleanups()',
  ].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
  assert.equal(result.status,0,result.stderr);const {plan,audit}=JSON.parse(result.stdout);
  assert.equal(DSGTestPlanReview.inspectAudit(audit,plan).rechecked,1);
  audit.cases[0].attempts[0].blockers=[];assert.throws(()=>DSGTestPlanReview.inspectAudit(audit,plan));
});
test('plan-bound selected-job mock produces a portal-compatible linked attempt',()=>{
  const result=spawnSync('python',['-c',[
    'import json',
    'from tools.scientific_transients.test_plan_execution import PlanExecutionTests',
    't=PlanExecutionTests(); t.setUp()',
    'try:',
    ' result=t.run_binding(t.prepare())',
    " assert result['planLinkage']=='LINKED'",
    ' print(json.dumps(t.plan.view()))',
    'finally: t.doCleanups()',
  ].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
  assert.equal(result.status,0,result.stderr);const view=JSON.parse(result.stdout),summary=DSGTestPlanReview.inspect(view);
  assert.equal(summary.executed,1);assert.equal(summary.qualified,0);assert.equal(summary.statisticalResult,null);
  assert.equal(view.cases[0].attempts[0].coverage,'PARTIAL');assert.equal(view.cases[0].scientificOutcome,'NOT_EVALUATED');
});
test('browser accepts view from actual Python plan, journal, evidence and report integration',()=>{
  const result=spawnSync('python',['-c',[
    'import json',
    'from tools.scientific_transients.test_test_plan import AttemptLinkTests',
    't=AttemptLinkTests(); t.setUp()',
    'try:',
    ' t.link(t.complete())',
    " t.append(data={'state':'DOCUMENTED_PENDING_REVIEW'}, sources={k:t.rationale for k in ('NULL_REFERENCE','INDEPENDENCE','RATIONALE')})",
    ' print(json.dumps(t.plan.view()))',
    'finally: t.doCleanups()',
  ].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
  assert.equal(result.status,0,result.stderr);const v=JSON.parse(result.stdout),s=DSGTestPlanReview.inspect(v);
  assert.equal(s.cases,1);assert.equal(s.documented,1);assert.equal(s.executed,1);assert.equal(s.qualified,0);
  assert.equal(v.cases[0].attempts[0].coverage,'PARTIAL');assert.equal(v.scienceValidation,'NOT_VALIDATED');
});
