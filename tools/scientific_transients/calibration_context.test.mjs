import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import '../../docs/javascripts/scientific-input-lineage.js';
import '../../docs/javascripts/scientific-calibration-context.js';
const run=spawnSync('python',['-c',[
  'import json','from tools.scientific_transients.test_calibration_context import CalibrationContextTests',
  'f=CalibrationContextTests();f.setUp()',
  'try: print(json.dumps([f.inspect(),f.l.inspect()]))','finally: f.doCleanups()'
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(run.status,0,run.stderr);const pair=JSON.parse(run.stdout),sample=()=>structuredClone(pair);
test('actual Python context pairs with byte-verified input lineage and preserves unknowns',()=>{
  const [v,l]=sample(),s=DSGCalibrationContext.inspect(v,l);assert.equal(s.inputs,1);assert.equal(s.maps,1);
  assert.equal(s.significance,null);assert.equal(s.completeUncertainty,null);assert.equal(s.qualified,0);
});
test('different lineage receipt, candidate or derived identity cannot be paired',()=>{
  for(const change of [v=>v.lineageReceiptSha256='f'.repeat(64),v=>v.candidatePlanRef='f'.repeat(32),
    v=>v.candidateDraftSha256='f'.repeat(64),v=>v.inputs[0].derivedSha256='f'.repeat(64),
    v=>v.inputs[0].inputRef='f'.repeat(32),v=>v.inputs[0].filter='Red']){
    const [v,l]=sample();change(v);assert.throws(()=>DSGCalibrationContext.inspect(v,l));
  }
});
test('no promotion of partial evidence, unknown covariance or map application',()=>{
  for(const change of [v=>v.completeUncertainty=0,v=>v.significance=4,v=>v.qualifiedControls=1,
    v=>v.executionAuthorized=true,v=>v.scienceValidation='VALIDATED',v=>v.components[1].status='COMPLETE',
    v=>v.inputs[0].association='APPLIED',v=>v.maps[0].scope='FULL_NOISE']){
    const [v,l]=sample();change(v);assert.throws(()=>DSGCalibrationContext.inspect(v,l));
  }
});
test('private fields, incomplete budgets, duplicated maps and wrong units rejected',()=>{
  for(const change of [v=>v.path='F:/private',v=>v.inputs[0].path='F:/private',v=>v.components.pop(),
    v=>v.components[1]={...v.components[0]},v=>v.maps.push({...v.maps[0]}),
    v=>v.maps[0].unit='ADU',v=>v.maps[0].varianceMinimum=Infinity,v=>v.maps[0].varianceMean=0,
    v=>v.maps[0].varianceMaximum=v.maps[0].varianceMinimum/2,v=>v.camera.sourceCells='B5:C5',
    v=>v.camera.readNoiseADUConditional=1,v=>v.inputs.push({...v.inputs[0]})]){
    const [v,l]=sample();change(v);assert.throws(()=>DSGCalibrationContext.inspect(v,l));
  }
});
function ui(){
  class Element{constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.files=[];this.handlers={};}
    append(...items){this.children.push(...items);}replaceChildren(){this.children=[];this.textContent='';}
    addEventListener(k,fn){this.handlers[k]=fn;}}
  const inputs=[new Element('input'),new Element('input')],status=new Element('p'),output=new Element('div');
  const root={dataset:{},isConnected:true,querySelector:s=>s==='[data-lineage]'?inputs[0]:s==='[data-calibration]'?inputs[1]:s==='[role="status"]'?status:output};
  const document={readyState:'complete',querySelector:()=>root,createElement:t=>new Element(t)};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-calibration-context.js',import.meta.url),'utf8'),
    {document,DSGInputLineage});
  const [v,l]=sample();inputs[0].files=[{size:100,text:async()=>JSON.stringify(l)}];inputs[1].files=[{size:100,text:async()=>JSON.stringify(v)}];
  return {inputs,status,output,root,load:()=>inputs[1].handlers.change()};
}
test('UI renders units and missing terms, clears stale output on invalid pair',async()=>{
  const u=ui();await u.load();assert.equal(u.output.children.length,5);
  assert.match(JSON.stringify(u.output.children),/Covarianze mancanti non sono poste a zero/);
  assert.match(JSON.stringify(u.output.children),/M5:N5/);
  assert.match(JSON.stringify(u.output.children),/Non è la varianza di un flusso/);
  u.inputs[0].files=[{size:1,text:async()=>'{'}];await u.load();assert.equal(u.output.children.length,0);
});
test('UI waits for both files and clears result when a file is removed',async()=>{
  const u=ui();await u.load();u.inputs[0].files=[];await u.load();assert.equal(u.output.children.length,0);
  assert.match(u.status.textContent,/entrambe/);
});
test('UI refuses oversize files without reading either',async()=>{
  const u=ui();let reads=0;u.inputs[0].files=[{size:1048577,text:async()=>{reads++;return '{}';}}];
  u.inputs[1].files=[{size:100,text:async()=>{reads++;return '{}';}}];await u.load();assert.equal(reads,0);
});
test('late pair import cannot overwrite a newer invalid pair',async()=>{
  const u=ui();let resolve;u.inputs[0].files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.load();
  u.inputs[0].files=[{size:1,text:async()=>'{'}];await u.load();resolve(JSON.stringify(pair[1]));await old;
  assert.equal(u.output.children.length,0);assert.match(u.status.textContent,/non valide/);
});
test('UI ignores pair read after page removal',async()=>{
  const u=ui();let resolve;u.inputs[0].files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.load();
  u.root.isConnected=false;resolve(JSON.stringify(pair[1]));await old;assert.equal(u.output.children.length,0);
});
