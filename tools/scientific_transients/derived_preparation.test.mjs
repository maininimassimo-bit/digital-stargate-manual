import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import '../../docs/javascripts/scientific-test-plan-review.js';
import '../../docs/javascripts/scientific-input-lineage.js';
import '../../docs/javascripts/scientific-derived-preparation.js';
const run=spawnSync('python',['-m','tools.scientific_transients.derived_preparation_fixture'],
  {encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(run.status,0,run.stderr);
const fixture=JSON.parse(run.stdout),sample=()=>structuredClone(fixture);
const inspect=({preparation:v,plan,lineage})=>DSGDerivedPreparation.inspect(v,plan,lineage);

test('actual synthetic Python producer pairs with both existing browser contracts',()=>{
  assert.deepEqual(inspect(sample()),{prepared:3,selectedJobs:0,nativeStarts:0,attempts:0,qualified:0});
  for(const p of fixture.preparation.preflights){assert.equal(p.status,'BLOCKED');assert.equal(p.blockers.length,4);}
});
test('foreign version/head/case/family and lineage receipt/draft/pair reject',()=>{
  for(const change of [x=>x.preparation.versionRef='f'.repeat(32),x=>x.preparation.headSha256='f'.repeat(64),
    x=>x.preparation.planSha256='f'.repeat(64),x=>x.preparation.caseRef='f'.repeat(32),x=>x.lineage.candidatePlanRef='f'.repeat(32),
    x=>x.lineage.receiptSha256='f'.repeat(64),x=>x.lineage.candidateDraftSha256='f'.repeat(64),
    x=>x.preparation.preflights[0].derivedSha256='f'.repeat(64),x=>x.preparation.preflights[0].frameRef='INVALID',
    x=>x.lineage.inputs[0].sampleMembership='OUTSIDE_CANDIDATE_MANIFEST']){
    const x=sample();change(x);assert.throws(()=>inspect(x));
  }
});
test('missing duplicate and mixed preflights cannot describe a prepared triplet',()=>{
  for(const change of [v=>v.preflights.pop(),v=>v.preflights.push(v.preflights[0]),
    v=>v.preflights[1]=structuredClone(v.preflights[0]),v=>v.preflights[1].frameRef=v.preflights[0].frameRef,
    v=>v.preflights[1].rawSha256=v.preflights[0].rawSha256,v=>v.preflights[1].derivedSha256=v.preflights[0].derivedSha256,
    v=>v.preflights[1].caseRef='f'.repeat(32),v=>v.preflights[1].headSha256='f'.repeat(64),
    v=>v.preflights[1].signedReadEvidenceSha256='f'.repeat(64)]){
    const x=sample();change(x.preparation);assert.throws(()=>inspect(x));
  }
});
test('all eight literal flags and four unchanged blockers remain mandatory',()=>{
  for(const key of Object.keys(fixture.preparation.preflights[0].matches))for(const value of [false,1,'true',null]){
    const x=sample();x.preparation.preflights[0].matches[key]=value;assert.throws(()=>inspect(x));
  }
  for(const change of [p=>p.blockers.pop(),p=>p.blockers.push('READY'),p=>p.blockers.reverse(),p=>p.matches.newAuthority=true]){
    const x=sample();change(x.preparation.preflights[0]);assert.throws(()=>inspect(x));
  }
});
test('private fields and scientific/execution/count promotion reject at both levels',()=>{
  for(const change of [v=>v.path='F:/PRIVATE',v=>v.status='READY',v=>v.selectedJobs=1,v=>v.nativeStarts=1,
    v=>v.attempts=1,v=>v.executionAuthorized=true,v=>v.scienceValidation='VALIDATED',v=>v.qualifiedControls=1,
    v=>v.completeUncertainty=0,v=>v.significance=5]){
    const x=sample();change(x.preparation);assert.throws(()=>inspect(x));
  }
  for(const change of [p=>p.operatorPath='F:/PRIVATE',p=>p.status='READY',p=>p.executionAuthorized=true,
    p=>p.scienceValidation='VALIDATED',p=>p.qualifiedControls=1,p=>p.completeUncertainty=0,p=>p.significance=5]){
    const x=sample();change(x.preparation.preflights[0]);assert.throws(()=>inspect(x));
  }
});
test('zero attempt claim is scoped to the selected case, not unrelated cases',()=>{
  const attempt={journalHeadSha256:'f'.repeat(64),technicalState:'COMPLETED',coverage:'PARTIAL',
    algorithmMatches:true,chronology:'AFTER_DECLARED_FREEZE'};
  const x=sample();x.plan.cases[0].attempts.push(attempt);assert.throws(()=>inspect(x));
  const y=sample();y.plan.cases.push({...structuredClone(y.plan.cases[0]),caseRef:'f'.repeat(32),
    clusterRef:'e'.repeat(32),attempts:[attempt]});assert.equal(inspect(y).attempts,0);
});

function ui(){
  class Element{
    constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.files=[];this.handlers={};this.listeners=0;}
    append(...items){this.children.push(...items);}replaceChildren(){this.children=[];this.textContent='';}
    addEventListener(key,fn){this.handlers[key]=fn;this.listeners++;}
  }
  function controls(){
    const inputs=[new Element('input'),new Element('input'),new Element('input')],status=new Element('p'),output=new Element('div');
    const map={'[data-plan]':inputs[0],'[data-lineage]':inputs[1],'[data-preparation]':inputs[2],
      '[role="status"]':status,'[data-result]':output};
    const root={dataset:{},isConnected:true,querySelector:s=>map[s]};
    const values=[fixture.plan,fixture.lineage,fixture.preparation];
    inputs.forEach((input,i)=>{const text=JSON.stringify(values[i]);input.files=[{size:Buffer.byteLength(text),text:async()=>text}];});
    return {inputs,status,output,root,load:()=>inputs[2].handlers.change()};
  }
  let current=controls(),subscribe,pagehide;
  const document={readyState:'complete',querySelector:()=>current.root,createElement:t=>new Element(t)};
  const forbidden=()=>assert.fail('network/storage/process unavailable to passive reader');
  const context={document,TextEncoder,DSGTestPlanReview,DSGInputLineage,fetch:forbidden,
    window:{addEventListener(key,fn){assert.equal(key,'pagehide');pagehide=fn;}},
    localStorage:new Proxy({},{get:forbidden}),sessionStorage:new Proxy({},{get:forbidden}),
    document$:{subscribe(fn){subscribe=fn;}}};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-derived-preparation.js',import.meta.url),'utf8'),context);
  return {get current(){return current;},mount(){current=controls();subscribe();return current;},subscribe:()=>subscribe(),pagehide:()=>pagehide()};
}
test('UI shows prepared declarations and blockers without remote or storage actions',async()=>{
  const h=ui(),u=h.current;await u.load();const text=JSON.stringify(u.output.children);
  assert.match(text,/copie preparate per questo caso: 3/);assert.match(text,/Job selezionati: 0/);
  assert.match(text,/non rilegge i file privati/);assert.match(text,/quattro blocchi|Incertezza completa mancante/);
  assert.equal(u.output.children.filter(c=>c.tag==='article').length,3);
  assert.equal(u.output.children.some(c=>['button','a','form'].includes(c.tag)),false);
});
test('every changed/missing/invalid input clears a previous combined result immediately',async()=>{
  const h=ui(),u=h.current;await u.load();assert.ok(u.output.children.length);
  u.inputs[0].files=[];const missing=u.inputs[0].handlers.change();assert.equal(u.output.children.length,0);await missing;
  u.inputs[0].files=[{size:1,text:async()=>'{'}];await u.load();assert.equal(u.output.children.length,0);
  assert.match(u.status.textContent,/non valide/);
});
test('declared oversize rejects before reads and actual UTF8 bytes are also bounded',async()=>{
  const h=ui(),u=h.current;let reads=0;
  u.inputs[0].files=[{size:1048577,text:async()=>{reads++;return '{}';}}];await u.load();assert.equal(reads,0);
  u.inputs[0].files=[{size:1,text:async()=>'é'.repeat(524289)}];await u.load();assert.equal(u.output.children.length,0);
  assert.match(u.status.textContent,/non valide/);
});
test('a late import cannot restore success after a newer invalid selection',async()=>{
  const h=ui(),u=h.current;let finish;
  u.inputs[0].files=[{size:100,text:()=>new Promise(resolve=>finish=resolve)}];const old=u.load();
  u.inputs[0].files=[{size:1,text:async()=>'{'}];await u.load();finish(JSON.stringify(fixture.plan));await old;
  assert.equal(u.output.children.length,0);assert.match(u.status.textContent,/non valide/);
});
test('detached and replaced roots cannot receive delayed results; remount initializes once',async()=>{
  for(const detach of [true,false]){
    const h=ui(),u=h.current;let finish;
    u.inputs[0].files=[{size:100,text:()=>new Promise(resolve=>finish=resolve)}];const old=u.load();
    if(detach)u.root.isConnected=false;
    const next=h.mount();h.subscribe();assert.equal(next.inputs[0].listeners,1);
    finish(JSON.stringify(fixture.plan));await old;assert.equal(u.output.children.length,0);
    await next.load();assert.equal(next.output.children.filter(c=>c.tag==='article').length,3);
  }
});
test('navigation invalidates already rendered declarations and leaving the page clears files',async()=>{
  const h=ui(),old=h.current;await old.load();assert.ok(old.output.children.length);
  const next=h.mount();assert.equal(old.output.children.length,0);await next.load();assert.ok(next.output.children.length);
  h.pagehide();assert.equal(next.output.children.length,0);
  assert.ok(next.inputs.every(input=>input.value===''));assert.match(next.status.textContent,/Nessuna preparazione/);
});
