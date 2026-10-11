import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import fs from 'node:fs';

const source=fs.readFileSync(new URL('./adaptive_native.jsh',import.meta.url),'utf8');
const controller=fs.readFileSync(new URL('./adaptive_executor.jsh',import.meta.url),'utf8');

test('controller claims stars once when native enumeration returns distinct window wrappers',()=>{
  const files=new Map([['ack',JSON.stringify({executeAllowed:true,ordinal:1})],['lease',''],['rgb','RGB'],['lum','L']]);
  const slots=[],closed=[];let leaseHeld=false;
  class File {
    static exists(p){return files.has(p);}
    static readFile(p){assert.ok(files.has(p));return p;}
    static readTextFile(p){return files.get(p);}
    createForWriting(p){this.path=p;files.set(p,'');}
    write(value){files.set(this.path,value);}
    openForReadWrite(){if(leaseHeld)throw Error('exclusive');leaseHeld=true;this.isOpen=true;}
    close(){if(this.isOpen){leaseHeld=false;this.isOpen=false;}}
  }
  function add(id,channels){
    const slot={closed:false,view:{id,image:{width:64,height:64,numberOfNominalChannels:channels,isReal:true,bitsPerSample:32},
      historyIndex:0,initialProcessing:{toSource(){return 'initial';}},processing:{toSource(){return 'history';}}}};
    slots.push(slot);return slot;
  }
  function wrap(slot){return {get isNull(){return slot.closed;},mainView:slot.view,
    saveAs(p){files.set(p,'native checkpoint');return true;},
    forceClose(){assert.equal(slot.closed,false);slot.closed=true;closed.push(slot.view.id);}};}
  const ImageWindow={get windows(){return slots.filter(s=>!s.closed).map(wrap);},
    open(p){return [wrap(add(p,files.get(p)==='RGB'?3:1))];},windowById(id){return {isNull:!slots.some(s=>s.view.id===id&&!s.closed)};}};
  function CryptographicHash(){}
  CryptographicHash.SHA256=1;CryptographicHash.prototype.hash=function(p){return {toHex(){return p;}};};
  const core={major:1,minor:9,release:5,revision:0,build:1706};
  const ctx={File,ImageWindow,CryptographicHash,ByteArray:{stringToUTF8:v=>v},
    console:{beginLog(){},endLog(){}},
    CoreApplication:{versionMajor:1,versionMinor:9,versionRelease:5,versionRevision:0,versionBuild:1706},
    DSGMeasureNative(w){return {width:64,height:64,channels:w.mainView.image.numberOfNominalChannels};},
    DSGAdaptiveNativeStep(step,tracks,context,callbacks){
      for(const role of ['RGB','L']){
        callbacks.apply({toSource(){return 'native StarX';},executeOn(view){view.historyIndex++;add('stars_'+role,role==='RGB'?3:1);return true;}},tracks[role],role);
        // Native API enumeration produces another JS wrapper for the same view.
        const stars=ImageWindow.windows.find(w=>w.mainView.id==='stars_'+role);
        tracks[role+'_STARS']=stars;callbacks.secondary(stars,role+'_STARS');
      }
    }};
  vm.createContext(ctx);vm.runInContext(controller,ctx);
  const m={version:'DSG_PIAI_ADAPTIVE_NATIVE_MANIFEST_V2',permit:{jobId:'PIAI_'+'a'.repeat(32),ordinal:1,step:{process:'SEPARATE',parameters:{}}},
    permitSha256:'permit',approvalSha256:'approval',sources:[],runtimeFiles:[],coreVersion:core,
    startAcknowledgement:'ack',startAcknowledgementSha256:'ack',nativeLease:'lease',
    inputs:[{role:'RGB',copy:'rgb',sha256:'rgb',width:64,height:64,channels:3,imageIndex:0},
            {role:'L',copy:'lum',sha256:'lum',width:64,height:64,channels:1,imageIndex:0}],
    parentArtifacts:[],context:{},regions:[[0,0,64,64]],measurementSha256:'measure',starDetectorSha256:'detector',
    outputDirectory:'outputs',report:'report',failure:'failure',events:'events',cancel:'cancel',log:'log',done:'done'};
  ctx.DSGAdaptiveExecute(m);
  const report=JSON.parse(files.get('report'));
  assert.deepEqual(report.intermediates,[]);
  assert.deepEqual(report.current.map(r=>r.role),['RGB','L','RGB_STARS','L_STARS']);
  assert.equal(closed.length,4);assert.equal(new Set(closed).size,4);
  assert.equal(files.has('failure'),false);assert.equal(leaseHeld,false);
});
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
