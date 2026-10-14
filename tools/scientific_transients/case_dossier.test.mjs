import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import vm from 'node:vm';
import '../../docs/javascripts/scientific-astrometry-context.js';
import '../../docs/javascripts/scientific-case-dossier.js';
const ref=n=>n.toString(16).padStart(32,'0');
const r=spawnSync('python',['-c',[
  'import json','from tools.scientific_transients.test_case_dossier import CaseDossierTests',
  'f=CaseDossierTests();f.setUp()',
  'try:',
  ' p=f.prepare();l=p.prepare_review(f.ledgers,"0"*31+"1");before=p.view(l,l.anchor_sha,f.f.f.plan)',
  ' first=p.apply_review(l,f.request(p,l,l.anchor_sha));middle=p.view(l,first["headSha256"],f.f.f.plan)',
  ' last=p.apply_review(l,f.request(p,l,first["headSha256"],"REVOKE_REVIEW",format(501,"032x"),format(502,"032x")))',
  ' print(json.dumps([before,middle,p.view(l,last["headSha256"],f.f.f.plan)]))',
  'finally:f.doCleanups()'
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(r.status,0,r.stderr);const views=JSON.parse(r.stdout),sample=(i=0)=>structuredClone(views[i]);
const decision=(action='FOLLOW_UP',targetEventRef=null)=>({eventRef:ref(600),actorRef:ref(9),recordedUTC:'2026-10-15T00:00:01Z',action,targetEventRef,note:'SYNTHETIC test, not Owner approval'});
test('contextual experiment view permits review without treating attachment as case recovery',()=>{
 const v={...sample(),schema:'BKL051_CASE_DOSSIER_REVIEW_V2',contextualRecoveryRelationship:'CONTEXT_ONLY_NOT_CASE_RECOVERY_OR_VALIDATION'};
 assert.equal(DSGCaseDossier.inspect(v).submissionAuthorized,false);
 assert.equal(DSGCaseDossier.request(v,decision()).packageSha256,v.packageSha256);
});
test('context attachment cannot be relabelled as case validation',()=>{
 const v={...sample(),schema:'BKL051_CASE_DOSSIER_REVIEW_V2',contextualRecoveryRelationship:'VALIDATED_CASE_RECOVERY'};
 assert.throws(()=>DSGCaseDossier.inspect(v));
});
test('contextual field cannot be smuggled into a V1 view',()=>{
 const v={...sample(),contextualRecoveryRelationship:'CONTEXT_ONLY_NOT_CASE_RECOVERY_OR_VALIDATION'};
 assert.throws(()=>DSGCaseDossier.inspect(v));
});
test('actual frozen case and ledger export keep reviews separate from scientific acceptance',()=>{
  assert.equal(DSGCaseDossier.inspect(sample()).decisions,0);assert.equal(DSGCaseDossier.inspect(sample(1)).decisions,1);
  assert.equal(DSGCaseDossier.inspect(sample(2)).revoked,1);
  assert.equal(sample().comparisonPresent,true);assert.equal(sample().submissionAuthorized,false);
});
test('request binds exact package, ledger anchor and observed head without mutating receipt',()=>{
  const v=sample(),before=JSON.stringify(v),p=DSGCaseDossier.request(v,decision());
  assert.equal(p.packageSha256,v.packageSha256);assert.equal(p.expectedHeadSha256,v.ledgerHeadSha256);
  assert.equal(p.decision.action,'FOLLOW_UP');assert.equal(JSON.stringify(v),before);
});
test('revocation requires previous unrevoked review and preserves its history',()=>{
  assert.throws(()=>DSGCaseDossier.request(sample(),decision('REVOKE_REVIEW',ref(501))));
  assert.equal(DSGCaseDossier.request(sample(1),decision('REVOKE_REVIEW',ref(501))).decision.targetEventRef,ref(501));
  assert.throws(()=>DSGCaseDossier.request(sample(2),decision('REVOKE_REVIEW',ref(501))));
});
test('changed retained package blocks new review but permits revoking old decision',()=>{
  const v=sample(1);v.packageStatus='RETAINED_PACKAGE_UNAVAILABLE_OR_CHANGED';
  assert.throws(()=>DSGCaseDossier.request(v,decision()));
  assert.equal(DSGCaseDossier.request(v,decision('REVOKE_REVIEW',ref(501))).decision.action,'REVOKE_REVIEW');
});
test('invented approval, malformed history and private fields rejected',()=>{
  for(const mutate of [v=>v.scientificAcceptance=true,v=>v.actorIdentityAttested=true,v=>v.submissionAuthorized=true,
    v=>v.externalSubmission='SENT',v=>v.path='F:/private',v=>v.ledgerHeadSha256=v.ledgerAnchorSha256,
    v=>v.decisions[0].revoked=true,v=>v.decisions[0].action='APPROVE',v=>v.decisions[0].recordedUTC='2026-02-30T00:00:00Z']){
    const v=sample(1);mutate(v);assert.throws(()=>DSGCaseDossier.inspect(v));
  }
  assert.throws(()=>DSGCaseDossier.request(sample(),decision('APPROVE_SUBMISSION')));
  assert.throws(()=>DSGCaseDossier.request(sample(),{...decision(),note:'two\nlines'}));
});
function ui(){
  class Element{constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.value='';this.files=[];this.handlers={};this.style={};this.disabled=false;}
    append(...x){this.children.push(...x);}replaceChildren(){this.children=[];}addEventListener(k,fn){this.handlers[k]=fn;}click(){this.clicked=true;}}
  const input=new Element('input'),status=new Element('p'),output=new Element('div');
  const controls=Object.fromEntries(['actor','action','target','note','save','new-actor','request-status'].map(k=>[k,new Element(k)]));
  controls.action.value='KEEP_FOR_REVIEW';
  const form={querySelector:s=>controls[s.slice(6,-1)]};
  const root={dataset:{},isConnected:true,querySelector:s=>s==='[data-view]'?input:s==='[data-view-status]'?status:s==='[data-result]'?output:form};
  const document={readyState:'complete',querySelector:()=>root,createElement:t=>new Element(t)},blobs=[];
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-case-dossier.js',import.meta.url),'utf8'),{
    document,DSGAstrometryContext,crypto:{randomUUID:()=>ref(700)},Blob:class{constructor(parts){this.parts=parts;}},
    URL:{createObjectURL:b=>{blobs.push(b);return 'blob:local';},revokeObjectURL:()=>{}},setTimeout:fn=>fn()});
  const load=async(v=sample())=>{input.files=[{size:100,text:async()=>JSON.stringify(v)}];await input.handlers.change();};
  return {input,status,output,controls,root,blobs,load};
}
test('UI renders exact hashes and historical-plan warning, download is an unrecorded request',async()=>{
  const u=ui(),v=sample();v.planStatus='HISTORICAL_PLAN_REVISION';await u.load(v);
  assert.equal(u.output.children.length,5);assert.match(u.output.children[1].textContent,/versione storica/);
  assert.match(JSON.stringify(u.output.children),new RegExp(v.packageSha256));
  u.controls.actor.value=ref(9);u.controls.note.value='Synthetic local request';u.controls.action.value='FOLLOW_UP';
  u.controls.save.handlers.click();assert.equal(u.blobs.length,1);
  const request=JSON.parse(u.blobs[0].parts[0]);assert.equal(request.expectedHeadSha256,v.ledgerHeadSha256);
  assert.match(u.controls['request-status'].textContent,/Nessuna revisione già registrata/);
});
test('new dossier clears prior target/action/note; invalid view disables request',async()=>{
  const u=ui();await u.load(sample(1));u.controls.note.value='stale';u.controls.action.value='REVOKE_REVIEW';
  await u.load();assert.equal(u.controls.note.value,'');assert.equal(u.controls.action.value,'KEEP_FOR_REVIEW');
  assert.equal(u.controls.target.children.length,0);
  u.input.files=[{size:1,text:async()=>'{'}];await u.input.handlers.change();assert.equal(u.controls.save.disabled,true);assert.equal(u.output.children.length,0);
});
test('oversize/late imports never leave a stale requestable dossier',async()=>{
  const u=ui();await u.load();let read=false;
  u.input.files=[{size:1048577,text:async()=>{read=true;return '{}';}}];await u.input.handlers.change();assert.equal(read,false);assert.equal(u.controls.save.disabled,true);
  let resolve;u.input.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.input.handlers.change();
  u.input.files=[{size:1,text:async()=>'{'}];await u.input.handlers.change();resolve(JSON.stringify(sample()));await old;
  assert.equal(u.controls.save.disabled,true);assert.equal(u.output.children.length,0);
});
