import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import vm from 'node:vm';
import '../../docs/javascripts/scientific-motion-hypotheses.js';
const result=spawnSync('python',['-c',[
  'import json','from tools.scientific_transients.test_motion_hypotheses import MotionTests',
  'f=MotionTests();f.setUp()','try:print(json.dumps(f.inspect()))','finally:f.doCleanups()'
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(result.status,0,result.stderr);const source=JSON.parse(result.stdout),sample=()=>structuredClone(source);
test('all Python hypotheses independently recomputed, including two perfect ambiguous paths',()=>{
  const v=sample(),s=DSGMotionHypotheses.inspect(v);assert.equal(s.hypotheses,8);assert.equal(s.selected,null);assert.equal(s.qualified,0);
  assert.equal(v.hypotheses.filter(h=>h.radialRMSArcsec===0).length,2);
});
test('missing combination, altered residual, false motion and automatic acceptance rejected',()=>{
  for(const change of [v=>v.hypotheses.pop(),v=>v.hypotheses[1].radialRMSArcsec=0,v=>v.hypotheses[0].velocityArcsecPerHour[0]=9,
    v=>v.hypotheses[0].detectionRefs.reverse(),v=>v.selectedHypothesis=v.hypotheses[0].hypothesisRef,
    v=>v.trackletAccepted=true,v=>v.movingObjectClassification='ASTEROID',v=>v.submissionAuthorized=true,
    v=>v.blindRecovery=true,v=>v.qualifiedControls=1]){const v=sample();change(v);assert.throws(()=>DSGMotionHypotheses.inspect(v));}
});
test('private fields, reused exposure, invented covariance and inconsistent nominal times rejected',()=>{
  for(const change of [v=>v.path='F:/private',v=>v.pool.frames[0].path='F:/private',
    v=>v.pool.frames[1].imageSha256=v.pool.frames[0].imageSha256,v=>v.pool.frames[1].elapsedSeconds++,
    v=>v.pool.frames[1].recordedJD='2450000',v=>v.hypotheses[0].velocityCovariance=0,
    v=>v.pool.frames[0].candidates[0].positionCovariance=0]){const v=sample();change(v);assert.throws(()=>DSGMotionHypotheses.inspect(v));}
});
test('empty pool keeps explicit non-nondetection status',()=>{
  const v=sample();v.pool.frames[1].candidates=[];v.expectedHypotheses=0;v.hypotheses=[];v.status='EMPTY_POOL_NOT_NONDETECTION';
  assert.equal(DSGMotionHypotheses.inspect(v).hypotheses,0);v.status='NO_MOVING_OBJECTS';assert.throws(()=>DSGMotionHypotheses.inspect(v));
});
test('resource ceiling preserves count and never permits partial top list',()=>{
  const v=sample();for(const [i,f] of v.pool.frames.entries()){
    f.retainedCatalogSourceCount=17;f.candidates=Array.from({length:17},(_,j)=>({detectionRef:(1000+i*100+j).toString(16).padStart(32,'0'),positionArcsec:[j,i],positionCovariance:null}));}
  v.expectedHypotheses=4913;v.hypotheses=[];v.status='RESOURCE_LIMIT_NO_PARTIAL_SELECTION';
  assert.equal(DSGMotionHypotheses.inspect(v).expectedHypotheses,4913);
  v.hypotheses=[sample().hypotheses[0]];assert.throws(()=>DSGMotionHypotheses.inspect(v));
});
test('retained ephemeris distance is reported without accepting a match',()=>{
  const v=sample();v.pool.frames[1].candidates[0].referenceDistanceArcsec=15;
  assert.equal(DSGMotionHypotheses.inspect(v).selected,null);
  v.pool.frames[1].candidates[0].referenceDistanceArcsec=-1;assert.throws(()=>DSGMotionHypotheses.inspect(v));
});
function ui(){
  class Element{constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.style={};this.attrs={};}
    append(...x){this.children.push(...x);}replaceChildren(){this.children=[];}setAttribute(k,v){this.attrs[k]=v;}}
  const input={files:[],value:'selected',addEventListener:(_,fn)=>input.change=fn},status=new Element('p'),output=new Element('div');
  const root={dataset:{},isConnected:true,querySelector:s=>s==='input'?input:s==='[role="status"]'?status:output};
  const document={readyState:'complete',querySelector:()=>root,createElement:t=>new Element(t)};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-motion-hypotheses.js',import.meta.url),'utf8'),{document});
  return {input,status,output,root};
}
test('UI retains all rows, accessible table and non-orbital limitation',async()=>{
  const u=ui();u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();
  const region=u.output.children[2],table=region.children[0];assert.equal(region.attrs.tabindex,'0');assert.equal(table.children[0].tag,'caption');
  assert.equal(table.children[2].children.length,8);assert.match(JSON.stringify(u.output.children),/non soluzione orbitale/);
  assert.match(u.output.children[0].textContent,/Nessuna ipotesi scelta automaticamente/);
});
test('UI invalid/oversize reads clear results and never read excess payload',async()=>{
  const u=ui();u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();
  u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();assert.equal(u.output.children.length,0);
  let read=false;u.input.files=[{size:4194305,text:async()=>{read=true;return '{}';}}];await u.input.change();assert.equal(read,false);
});
test('late result cannot replace newer import or disconnected page',async()=>{
  const u=ui();let resolve;u.input.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.input.change();
  u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();resolve(JSON.stringify(sample()));await old;assert.equal(u.output.children.length,0);
  u.input.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const pending=u.input.change();u.root.isConnected=false;
  resolve(JSON.stringify(sample()));await pending;assert.equal(u.output.children.length,0);
});
