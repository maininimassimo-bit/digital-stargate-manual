import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import '../../docs/javascripts/scientific-test-plan-review.js';
import '../../docs/javascripts/scientific-astrometry-context.js';
import '../../docs/javascripts/scientific-covariance.js';
import '../../docs/javascripts/scientific-multi-epoch.js';
const r=spawnSync('python',['-c',[
  'import json','from tools.scientific_transients.test_multi_epoch import MultiEpochTests',
  'f=MultiEpochTests();f.setUp()',
  'try: print(json.dumps([f.inspect(),f.f.plan.view()]))','finally:f.doCleanups()'
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(r.status,0,r.stderr);const data=JSON.parse(r.stdout),sample=()=>structuredClone(data);
test('three actual Python mock journals yield browser-rechecked differences and covariance',()=>{
  const [v,p]=sample(),s=DSGMultiEpoch.inspect(v,p);assert.equal(s.attempts,3);assert.equal(s.algebraicPairs,2);
  assert.equal(s.significance,null);assert.equal(s.qualified,0);
});
test('wrong plan, stale head, omitted failed attempt and private fields rejected',()=>{
  for(const change of [v=>v.planSha256='f'.repeat(64),v=>v.headSha256='f'.repeat(64),v=>v.attempts.pop(),
    v=>v.path='F:/private',v=>v.attempts[0].path='F:/private',v=>v.attempts[0].reportSha256=null]){
    const [v,p]=sample();change(v);assert.throws(()=>DSGMultiEpoch.inspect(v,p));
  }
});
test('altered difference, sigma, blockers and invalid matrix cannot masquerade as calculation',()=>{
  for(const change of [v=>v.pairs[0].algebraicDifference=9,v=>v.pairs[0].conditionalSigma=0,
    v=>v.pairs[0].blockers.push('FAKE'),v=>v.pairs[0].covariances=[.9,.9,-.9],
    v=>v.pairs[0].variances=[0,9,.04],v=>v.pairs[0].frameRef=v.referenceFrameRef]){
    const [v,p]=sample();change(v);assert.throws(()=>DSGMultiEpoch.inspect(v,p));
  }
});
test('unknown covariance permits algebraic difference but no conditional sigma',()=>{
  const [v,p]=sample();v.pairs[0].covariances[0]=null;v.pairs[0].conditionalSigma=null;
  v.pairs[0].blockers=['UNKNOWN_COVARIANCE_NOT_ZERO'];assert.equal(DSGMultiEpoch.inspect(v,p).algebraicPairs,2);
  v.pairs[1].rightToReferenceScale=null;v.pairs[1].algebraicDifference=null;v.pairs[1].conditionalSigma=null;
  v.pairs[1].blockers=['SCALE_UNKNOWN_NOT_REPLACED_WITH_ONE'];assert.equal(DSGMultiEpoch.inspect(v,p).algebraicPairs,1);
});
test('incompatible filters and changed aperture require unavailable comparison',()=>{
  for(const change of [v=>v.attempts[1].band='Red',v=>v.attempts[1].apertureParameters.apertureRadius=9]){
    const [v,p]=sample();change(v);assert.throws(()=>DSGMultiEpoch.inspect(v,p));
  }
});
test('negative flux remains signed; zero conditional sigma grants no significance',()=>{
  const [v,p]=sample();v.attempts[0].flux=-.3;
  for(const pair of v.pairs){pair.algebraicDifference=-.9;pair.variances=[1,1,0];pair.covariances=[1,0,0];
    pair.rightToReferenceScale=1;pair.algebraicDifference=-.6;pair.conditionalSigma=0;}
  assert.equal(DSGMultiEpoch.inspect(v,p).algebraicPairs,2);
  v.significance=Infinity;assert.throws(()=>DSGMultiEpoch.inspect(v,p));
});
test('no scientific promotion or duplicate read noise',()=>{
  for(const change of [v=>v.photometricComparability='VALIDATED',v=>v.variabilityClassification='VARIABLE',v=>v.fullVariance=1,
    v=>v.qualifiedControls=1,v=>v.confirmatoryEligible=true,v=>{v.skyIncludesReadNoise=true;v.readNoiseAddedSeparately=true;}]){
    const [v,p]=sample();change(v);assert.throws(()=>DSGMultiEpoch.inspect(v,p));
  }
});
function ui(){
  class Element{constructor(tag){this.tag=tag;this.children=[];this.textContent='';this.files=[];this.handlers={};this.style={};this.attrs={};}
    append(...x){this.children.push(...x);}replaceChildren(){this.children=[];}setAttribute(k,v){this.attrs[k]=v;}
    addEventListener(k,fn){this.handlers[k]=fn;}}
  const inputs=[new Element('input'),new Element('input')],status=new Element('p'),output=new Element('div');
  const root={dataset:{},isConnected:true,querySelector:s=>s==='[data-plan]'?inputs[0]:s==='[data-comparison]'?inputs[1]:s==='[role="status"]'?status:output};
  const document={readyState:'complete',querySelector:()=>root,createElement:t=>new Element(t)};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-multi-epoch.js',import.meta.url),'utf8'),
    {document,DSGTestPlanReview,DSGAstrometryContext,DSGCovariance});
  const [v,p]=sample();inputs[0].files=[{size:100,text:async()=>JSON.stringify(p)}];inputs[1].files=[{size:100,text:async()=>JSON.stringify(v)}];
  return {inputs,status,output,root,load:()=>inputs[1].handlers.change()};
}
test('UI table is keyboard reachable and explicitly synthetic/partial',async()=>{
  const u=ui();await u.load();assert.equal(u.output.children.length,5);const region=u.output.children[1];
  assert.equal(region.attrs.tabindex,'0');assert.equal(region.children[0].children[0].tag,'caption');
  assert.match(u.output.children[0].textContent,/Prova sintetica dichiarata/);assert.match(JSON.stringify(u.output.children),/non è incertezza completa/);
});
test('UI clears invalid pair, rejects oversized files and ignores late results',async()=>{
  const u=ui();await u.load();u.inputs[0].files=[{size:1,text:async()=>'{'}];await u.load();assert.equal(u.output.children.length,0);
  let read=false;u.inputs[0].files=[{size:1048577,text:async()=>{read=true;return '{}';}}];await u.load();assert.equal(read,false);
  let resolve;u.inputs[0].files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.load();
  u.inputs[0].files=[];await u.load();resolve(JSON.stringify(data[1]));await old;assert.equal(u.output.children.length,0);
});
