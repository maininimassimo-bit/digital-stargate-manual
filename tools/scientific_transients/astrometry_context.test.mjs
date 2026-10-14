import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import '../../docs/javascripts/scientific-input-lineage.js';
import '../../docs/javascripts/scientific-astrometry-context.js';
const run=spawnSync('python',['-c',[
  'import json','from tools.scientific_transients.test_astrometry_context import AstrometryContextTests',
  'f=AstrometryContextTests();f.setUp()',
  'try: print(json.dumps([f.inspect(),f.l.inspect()]))','finally:f.doCleanups()'
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(run.status,0,run.stderr);const pair=JSON.parse(run.stdout),sample=()=>structuredClone(pair);
test('Python candidate context imports exact seven-digit timing and bound lineage',()=>{
  const [v,l]=sample(),s=DSGAstrometryContext.inspect(v,l);assert.equal(s.matched,2);assert.equal(s.unmatched,1);
  assert.equal(v.timing.derivedStartMinusSourceSeconds,'-0.0004567');assert.equal(s.qualified,0);assert.equal(s.covariance,null);
});
test('wrong candidate, original, parent and output identities rejected',()=>{
  for(const change of [v=>v.lineageReceiptSha256='f'.repeat(64),v=>v.candidateDraftSha256='f'.repeat(64),
    v=>v.rawSha256='f'.repeat(64),v=>v.parentDerivedSha256='f'.repeat(64),v=>v.wcsDerivedSha256=v.parentDerivedSha256,
    v=>v.inputRef='f'.repeat(32),v=>v.filter='Red',v=>v.candidatePlanRef='f'.repeat(32)]){
    const [v,l]=sample();change(v);assert.throws(()=>DSGAstrometryContext.inspect(v,l));
  }
});
test('timestamp truncation, offset corruption and impossible calendar values rejected',()=>{
  for(const change of [v=>v.timing.sourceDateObs='2026-08-16T01:00:00.123',
    v=>v.timing.averageMinusStartHalfExposureSeconds='0',v=>v.timing.derivedStartMinusSourceSeconds='0',
    v=>v.timing.sourceDateAvg='2026-02-30T01:05:00',v=>v.timing.sourceDateObs='2026-08-16T01:00:60',
    v=>v.timing.exposureSeconds='NaN',v=>v.timing.averagePreserved=false]){
    const [v,l]=sample();change(v);assert.throws(()=>DSGAstrometryContext.inspect(v,l));
  }
});
test('no scientific promotion, invented covariance, radial gate or control count',()=>{
  for(const change of [v=>v.solutionState='VALIDATED',v=>v.significance=5,v=>v.qualifiedControls=59,
    v=>v.executionAuthorized=true,v=>v.holdout.fullCovariance=0,v=>v.holdout.independentScientificValidation=true,
    v=>v.holdout.searchGeometry='RADIAL_3_PIXELS',v=>v.timing.clockShutterUncertainty=0,
    v=>v.timing.timeScale='UTC_VERIFIED',v=>v.holdout.unmatchedOutsideRecheck='REMATCHED']){
    const [v,l]=sample();change(v);assert.throws(()=>DSGAstrometryContext.inspect(v,l));
  }
});
test('count inconsistency, impossible residual summary and private data rejected',()=>{
  for(const change of [v=>v.path='F:/private',v=>v.holdout.coordinates=[1,2],v=>v.holdout.heldOutReferences++,
    v=>v.holdout.centroidReuse=1,v=>v.holdout.radialRMSPixel=-1,v=>v.holdout.largestSquaredResidualShare=.01,
    v=>v.geometry=[64,64,0]]){
    const [v,l]=sample();change(v);assert.throws(()=>DSGAstrometryContext.inspect(v,l));
  }
});
function ui(){
  class Element{constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.files=[];this.handlers={};}
    append(...items){this.children.push(...items);}replaceChildren(){this.children=[];this.textContent='';}
    addEventListener(k,fn){this.handlers[k]=fn;}}
  const inputs=[new Element('input'),new Element('input')],status=new Element('p'),output=new Element('div');
  const root={dataset:{},isConnected:true,querySelector:s=>s==='[data-lineage]'?inputs[0]:s==='[data-astrometry]'?inputs[1]:s==='[role="status"]'?status:output};
  const document={readyState:'complete',querySelector:()=>root,createElement:t=>new Element(t)};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-astrometry-context.js',import.meta.url),'utf8'),
    {document,DSGInputLineage});
  const [v,l]=sample();inputs[0].files=[{size:100,text:async()=>JSON.stringify(l)}];inputs[1].files=[{size:100,text:async()=>JSON.stringify(v)}];
  return {inputs,status,output,root,load:()=>inputs[1].handlers.change()};
}
test('UI preserves seven-digit source time and distinguishes synthesized end and descriptive scatter',async()=>{
  const u=ui();await u.load();const text=JSON.stringify(u.output.children);
  assert.equal(u.output.children.length,4);assert.match(text,/01:00:00.1234567/);assert.match(text,/-0.0004567/);
  assert.match(text,/non è un tempo acquisito attestato/);assert.match(text,/dispersione descrittiva/);
  assert.match(text,/non sono stati riassociati/);
});
test('UI clears valid results on wrong file or missing pair',async()=>{
  const u=ui();await u.load();u.inputs[0].files=[{size:1,text:async()=>'{'}];await u.load();assert.equal(u.output.children.length,0);
  u.inputs[0].files=[];await u.load();assert.match(u.status.textContent,/Apri provenienza/);
});
test('UI refuses oversized input without reading',async()=>{
  const u=ui();let read=false;u.inputs[0].files=[{size:1048577,text:async()=>{read=true;return '{}';}}];
  await u.load();assert.equal(read,false);assert.equal(u.output.children.length,0);
});
test('UI ignores late pair after newer import or removal',async()=>{
  const u=ui();let resolve;u.inputs[0].files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.load();
  u.inputs[0].files=[];await u.load();resolve(JSON.stringify(pair[1]));await old;assert.equal(u.output.children.length,0);
  u.inputs[0].files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const next=u.load();u.root.isConnected=false;
  resolve(JSON.stringify(pair[1]));await next;assert.equal(u.output.children.length,0);
});
