import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import '../../docs/javascripts/scientific-test-plan.js';
const ref=n=>n.toString(16).padStart(32,'0');
const sample=()=>({schema:'BKL051_TEST_PLAN_DRAFT_V1',planRef:ref(1),mode:'PRELIMINARY_DRAFT',falsePositiveMaximum:.05,confidence:.95,requiredControls:59,algorithmRef:null,cases:[{caseRef:ref(2),clusterRef:ref(3),frames:[4,5,6].map(n=>({frameRef:ref(n),sha256:n.toString(16).padStart(64,'0')})),qualification:'CANDIDATE',truth:'UNVERIFIED',execution:'NOT_RUN'}]});
test('candidates never count as qualified or executed',()=>assert.deepEqual(DSGTestPlan.inspect(sample()),{candidates:1,frames:3,clusters:1,qualified:0,executed:0,statisticalResult:null}));
test('duplicate image across cases is rejected',()=>{const v=sample();v.cases.push({...v.cases[0],caseRef:ref(7)});assert.throws(()=>DSGTestPlan.inspect(v));});
test('private path fields rejected',()=>{const v=sample();v.cases[0].frames[0].path='F:/private';assert.throws(()=>DSGTestPlan.inspect(v));});
test('unattested qualification cannot be imported as accepted',()=>{const v=sample();v.cases[0].qualification='QUALIFIED';assert.throws(()=>DSGTestPlan.inspect(v));});
test('executed outcome cannot be smuggled into candidate draft',()=>{const v=sample();v.cases[0].execution='PASS';assert.throws(()=>DSGTestPlan.inspect(v));});
test('old target and malformed identity rejected',()=>{const v=sample();v.falsePositiveMaximum=.001;assert.throws(()=>DSGTestPlan.inspect(v));v.falsePositiveMaximum=.05;v.planRef='unknown';assert.throws(()=>DSGTestPlan.inspect(v));});
test('incomplete triplet rejected',()=>{const v=sample();v.cases[0].frames.pop();assert.throws(()=>DSGTestPlan.inspect(v));});
test('duplicate case identity rejected',()=>{const v=sample();v.cases.push(structuredClone(v.cases[0]));assert.throws(()=>DSGTestPlan.inspect(v));});
test('same bytes under different image IDs rejected',()=>{const v=sample();v.cases[0].frames[1].sha256=v.cases[0].frames[0].sha256;assert.throws(()=>DSGTestPlan.inspect(v));});
test('revision leaves original untouched and excludes only explicit known cases',()=>{const original=sample();const revised=DSGTestPlan.revise(original,'f'.repeat(64),[ref(2)]);assert.equal(original.cases.length,1);assert.equal(original.algorithmRef,null);assert.equal(revised.cases.length,0);assert.equal(revised.algorithmRef,'f'.repeat(64));assert.throws(()=>DSGTestPlan.revise(original,null,[ref(20)]));assert.throws(()=>DSGTestPlan.revise(original,null,[ref(2),ref(2)]));assert.throws(()=>DSGTestPlan.revise(original,'not-a-hash'));});
function ui(){
  const input={value:'selected',files:[],addEventListener:(name,fn)=>{input.change=fn;}},status={textContent:''},output={textContent:''};
  const root={dataset:{},isConnected:true,querySelector:s=>s==='input'?input:s==='[role="status"]'?status:output};
  const document={readyState:'complete',querySelector:()=>root};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-test-plan.js',import.meta.url),'utf8'),{document});
  return {input,status,output,root};
}
test('UI displays candidate counters and clears prior result on invalid import',async()=>{const u=ui();u.input.files=[{size:200,text:async()=>JSON.stringify(sample())}];await u.input.change();assert.match(u.output.textContent,/Sequenze candidate: 1/);assert.match(u.output.textContent,/Controlli qualificati: 0/);assert.equal(u.input.value,'');u.input.files=[{size:5,text:async()=>'{bad'}];await u.input.change();assert.equal(u.output.textContent,'');assert.match(u.status.textContent,/non valido/);});
test('UI rejects oversized input before reading contents',async()=>{const u=ui();let read=false;u.input.files=[{size:1048577,text:async()=>{read=true;return '{}';}}];await u.input.change();assert.equal(read,false);assert.equal(u.output.textContent,'');});
test('late file read cannot replace newer imported plan',async()=>{const u=ui();let resolve;u.input.files=[{size:200,text:()=>new Promise(r=>{resolve=r;})}];const old=u.input.change();u.input.files=[{size:5,text:async()=>'{bad'}];await u.input.change();resolve(JSON.stringify(sample()));await old;assert.equal(u.output.textContent,'');assert.match(u.status.textContent,/non valido/);});
