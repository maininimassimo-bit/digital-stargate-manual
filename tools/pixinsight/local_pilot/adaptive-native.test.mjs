import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import fs from 'node:fs';

const source=fs.readFileSync(new URL('./adaptive_native.jsh',import.meta.url),'utf8');
function fixture() {
  const calls=[];
  const windows=[];
  function window(id,channels=3) {
    const value={isNull:false,mainView:{id,image:{width:64,height:64,numberOfNominalChannels:channels},
      computeOrFetchProperty(){return {at(){return .01;}};}},removeMask(){delete this.mask;}};
    windows.push(value);return value;
  }
  const context={ImageWindow:{windows},Number,Object,Array,Error};
  for(const name of ['AutomaticBackgroundExtractor','BlurXTerminator','NoiseXTerminator','StarXTerminator',
      'BackgroundNeutralization','ColorCalibration','MaskedStretch','PixelMath','ArcsinhStretch',
      'LocalHistogramEqualization','LRGBCombination','ChannelCombination']) {
    context[name]=function(){this.kind=name;};
  }
  context.AutomaticBackgroundExtractor.Correction_Subtract=1;
  context.MaskedStretch.MaskType_Intensity=1;
  context.ChannelCombination.RGB=0;
  vm.createContext(context);vm.runInContext(source,context);
  const tracks={RGB:window('DSG_RGB'),L:window('DSG_L',1)};
  const settings={mode:'LRGB',domain:'LINEAR_ATTESTED',branch:'DIRECT',
    models:{BLURX:4,NOISEX:3.1,STARX:11},backgroundROI:[0,0,32,32]};
  const callbacks={cancel(){},clone(w,role){return window('DSG_'+role,1);},secondary(){},
    apply(p,w,role){calls.push({p,w,role});if(p.kind==='StarXTerminator')window('stars_'+role,role==='L'?1:3);return true;}};
  return {calls,tracks,settings,callbacks,run(step){return context.DSGAdaptiveNativeStep(step,tracks,settings,callbacks);}};
}
test('selected ML parameters reach both native tracks with explicit version selectors',()=>{
  const f=fixture();f.run({process:'DENOISE',parameters:{denoiseL:.4,denoiseRGB:.3}});
  assert.deepEqual(f.calls.map(c=>[c.role,c.p.ml_version,c.p.denoise]),[['RGB',3.1,.3],['L',3.1,.4]]);
  assert.equal(f.tracks.RGB.mask,undefined);
});
test('unknown process, code fields, booleans and domain mismatch cannot execute',()=>{
  for(const step of [{process:'ExecuteScript',parameters:{}},
    {process:'DENOISE',parameters:{denoiseL:true,denoiseRGB:.3}},
    {process:'DENOISE',parameters:{denoiseL:.4,denoiseRGB:.3},expression:'$T'},
    {process:'COMBINE',parameters:{}}]) {
    const f=fixture();assert.throws(()=>f.run(step));assert.equal(f.calls.length,0);
  }
});
test('stretch refuses missing background and missing stars before changing pixels',()=>{
  for(const missing of ['region','stars']) {
    const f=fixture();if(missing==='region')f.settings.backgroundROI=null;else f.settings.branch='STARLESS';
    assert.throws(()=>f.run({process:'STRETCH',parameters:{targetBackground:.08}}));
    assert.equal(f.calls.length,0);
  }
});
test('native false result and cancellation stop later track execution',()=>{
  let f=fixture();f.callbacks.apply=()=>false;
  assert.throws(()=>f.run({process:'DENOISE',parameters:{denoiseL:.4,denoiseRGB:.3}}));
  f=fixture();f.callbacks.cancel=()=>{if(f.calls.length)throw Error('cancel');};
  assert.throws(()=>f.run({process:'DENOISE',parameters:{denoiseL:.4,denoiseRGB:.3}}));
  assert.equal(f.calls.length,1);
});
test('mask dependencies survive and are detached after native contrast failure',()=>{
  const f=fixture();f.settings.domain='NONLINEAR_ATTESTED';
  f.run({process:'MASK_BUILD',parameters:{maskLow:.1,maskHigh:.6}});
  assert.equal(f.calls[0].role,'MASK');
  f.callbacks.apply=()=>{assert.equal(f.tracks.L.mask,f.tracks.MASK);throw Error('native failure');};
  assert.throws(()=>f.run({process:'LOCAL_CONTRAST',parameters:{contrastLarge:.2,contrastSmall:.1}}));
  assert.equal(f.tracks.L.mask,undefined);assert.ok(f.tracks.MASK);
});
test('SHO and HOO cannot invoke empirical broadband color calibration',()=>{
  for(const mode of ['SHO','HOO']) {
    const f=fixture();f.settings.mode=mode;assert.throws(()=>f.run({process:'COLOR',parameters:{}}));
    assert.equal(f.calls.length,0);
  }
});
test('narrowband ML operates on independent monochrome channels before recombination',()=>{
  for(const mode of ['SHO','HOO']) {
    const f=fixture();f.settings.mode=mode;
    f.callbacks.extract=(w,c,role)=>({isNull:false,mainView:{id:'DSG_'+role,
      image:{width:64,height:64,numberOfNominalChannels:1}}});
    f.run({process:'DENOISE',parameters:{denoiseL:.4,denoiseRGB:.3}});
    const ml=f.calls.filter(c=>c.p.kind==='NoiseXTerminator');
    assert.equal(ml.length,4);
    assert.ok(ml.every(c=>c.w.mainView.image.numberOfNominalChannels===1));
    assert.equal(f.calls.filter(c=>c.p.kind==='ChannelCombination').length,1);
    assert.equal(ml.at(-1).role,'L');
  }
});
test('narrowband requires a compatible independent channel adapter before ML',()=>{
  const f=fixture();f.settings.mode='SHO';
  assert.throws(()=>f.run({process:'DENOISE',parameters:{denoiseL:.4,denoiseRGB:.3}}));
  assert.equal(f.calls.length,0);
  f.callbacks.extract=()=>({isNull:false,mainView:{image:{width:32,height:64,numberOfNominalChannels:1}}});
  assert.throws(()=>f.run({process:'DENOISE',parameters:{denoiseL:.4,denoiseRGB:.3}}));
  assert.equal(f.calls.length,0);
});
test('starless secondary tracks are retained with selected model and screened recombination',()=>{
  const f=fixture();f.settings.branch='STARLESS';f.run({process:'SEPARATE',parameters:{}});
  assert.ok(f.tracks.RGB_STARS);assert.ok(f.tracks.L_STARS);
  assert.ok(f.calls.every(c=>c.p.ml_version===11));
  f.run({process:'STRETCH',parameters:{targetBackground:.08}});
  f.settings.domain='NONLINEAR_ATTESTED';f.run({process:'RECOMBINE',parameters:{}});
  assert.match(f.calls.at(-1).p.expression,/^1-\(1-\$T\)\*\(1-stars_RGB\)$/);
});
test('factory does not evaluate source, run a shell or dispatch network requests',()=>{
  assert.doesNotMatch(source,/\beval\s*\(|new\s+Function|\.executeExternal\s*\(|\.download\s*\(|\bfetch\s*\(/);
});
