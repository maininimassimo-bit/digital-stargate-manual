import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';
const source=readFileSync(new URL('./native_aperture.jsh',import.meta.url),'utf8');
function fixture() {
 const hash='a'.repeat(64), root='F:/test/'+'b'.repeat(32);
 const m={protocol:'DSG_NATIVE_APERTURE_V1',runDirectory:root,operationRef:'b'.repeat(32),
  input:{sha256:hash,imageIndex:0,width:64,height:64,channels:1,linearity:'DECLARED_LINEAR_NOT_ATTESTED'},
  parameters:{coordinateConvention:'PI_NATIVE_GEOMETRIC',apertureRadius:4,annulusInner:2,annulusOuter:3},
  runtime:{librarySha256:hash,engineSha256:hash,catalogSha256:hash,pixInsightVersion:'1.9.5 build 1706'},
  targets:[{sourceRef:'c'.repeat(32),x:32.5,y:32.5}]};
 const files=new Map(), pixels=new Float64Array([.01,.31]), window={mainView:{image:{width:64,height:64,numberOfNominalChannels:1,isComplex:false},initialProcessing:{toSource:()=> 'native initial'},processing:{toSource:()=> 'native current'}},saveAs:(p)=>{files.set(p,'checkpoint');return true;},forceClose:()=>{window.closed=true;}};
 files.set(root+'/parameters.json',JSON.stringify(m));files.set(root+'/input.xisf','source');
 const context={File:{exists:p=>files.has(p),writeTextFile:(p,v)=>files.set(p,v),readTextFile:p=>files.get(p),readFile:p=>files.get(p)},
  CryptographicHash:class {hash(){return {toHex:()=>hash};}},
  CoreApplication:{versionMajor:1,versionMinor:9,versionRelease:5,versionBuild:1706},
  ImageWindow:{open:()=>[window]},PhotometryPixels:{FromImage:()=>({data:pixels}),Measure:()=>({clipped:false,flux:.3,area:50.4,background:.01,peak:.31,noise:0,localCount:248})}};
 context.CryptographicHash.SHA256=1;vm.createContext(context);vm.runInContext(source,context);
 return {m,root,files,pixels,window,context,run:()=>context.DSGNativeAperture(m)};
}
test('native adapter keeps normalized units and unknown uncertainty, preserves exports',()=>{
 const f=fixture(), result=f.run();assert.equal(result.state,'COMPLETED');assert.equal(result.unit,'NORMALIZED_SAMPLE_SUM');
 assert.equal(result.rows[0].fullVariance,null);assert.equal(result.rows[0].significance,null);assert.equal(result.changedPixels,0);
 assert.equal(result.fullAperturePhotometryWorkflowExecuted,false);assert.equal(f.window.closed,true);
 for(const name of ['input-initial.js','input-current.js','checkpoint-initial.js','checkpoint-current.js','measurement-00001.json','terminal.json'])assert(f.files.has(f.root+'/'+name));
});
test('completed native reservation refuses replay without rewriting',()=>{
 const f=fixture();f.run();const old=f.files.get(f.root+'/terminal.json');assert.throws(f.run,/REPLAY_REFUSED/);assert.equal(f.files.get(f.root+'/terminal.json'),old);
});
test('native cancellation before open is terminal with no checkpoint',()=>{
 const f=fixture();f.files.set(f.root+'/cancel.json',JSON.stringify({operationRef:f.m.operationRef,requested:true}));const r=f.run();assert.equal(r.state,'CANCELLED');assert.equal(f.files.has(f.root+'/checkpoint.xisf'),false);
});
test('wrong cancellation identity is failure, not authorised cancellation',()=>{
 const f=fixture();f.files.set(f.root+'/cancel.json',JSON.stringify({operationRef:'d'.repeat(32),requested:true}));assert.equal(f.run().state,'FAILED');
});
test('pixel mutation fails and retains failed checkpoint and History',()=>{
 const f=fixture();f.context.PhotometryPixels.Measure=()=>{f.pixels[0]=.2;return {clipped:false,flux:.3,area:50,background:.01,peak:.31,noise:0,localCount:10};};
 const r=f.run();assert.equal(r.state,'FAILED');assert(f.files.has(f.root+'/failed-checkpoint.xisf'));assert(f.files.has(f.root+'/failed-current.js'));
});
test('missing background never manufactures a corrected flux',()=>{
 const f=fixture();f.context.PhotometryPixels.Measure=()=>({clipped:false,flux:.5,area:50,background:0,peak:.31,noise:0,localCount:0});
 const r=f.run();assert.equal(r.rows[0].backgroundAvailable,false);assert.equal(r.rows[0].fluxNormalizedSampleSum,null);
});
test('clipped source remains an explicit excluded row',()=>{
 const f=fixture();f.context.PhotometryPixels.Measure=()=>({clipped:true,backgroundRect:null});const row=f.run().rows[0];assert.equal(row.clipped,true);assert.equal(row.fluxNormalizedSampleSum,null);
});
test('malformed scientific parameters and secret extras rejected before opening',()=>{
 for(const modify of [m=>m.parameters.coordinateConvention='UNKNOWN',m=>m.input.linearity='NONLINEAR',m=>m.input.channels=3,m=>m.leaseToken='d'.repeat(64),m=>m.targets[0].x=Infinity,m=>m.targets.push(m.targets[0]),m=>m.parameters.apertureRadius=0]) {
  const f=fixture();modify(f.m);assert.throws(f.run);assert.equal(f.window.closed,undefined);
 }
});
test('runtime or parameter mismatch fails before reading pixels',()=>{
 const f=fixture();f.m.runtime.librarySha256='d'.repeat(64);assert.equal(f.run().state,'FAILED');assert.equal(f.files.has(f.root+'/started.json'),false);
 const g=fixture();g.files.set(g.root+'/parameters.json','{}');assert.equal(g.run().state,'FAILED');assert.equal(g.files.has(g.root+'/started.json'),false);
});
test('nonfinite measurement and missing image index retain failure',()=>{
 const f=fixture();f.context.PhotometryPixels.Measure=()=>({clipped:false,flux:NaN,area:50,background:.01,peak:.31,noise:0,localCount:1});assert.equal(f.run().state,'FAILED');
 const g=fixture();g.context.ImageWindow.open=()=>[];assert.equal(g.run().state,'FAILED');
});
