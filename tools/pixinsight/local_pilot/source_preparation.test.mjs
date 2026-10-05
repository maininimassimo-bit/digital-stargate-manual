import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('./source_preparation.jsh',import.meta.url),'utf8');
function fixture(outputBits=32){
  const windows=[],calls=[],events=[],saves=[];
  function window(id,channels=3){const w={isNull:false,hasAstrometricSolution:true,mainView:{id,historyIndex:0,image:{width:1000,height:800,numberOfNominalChannels:channels,isReal:true,bitsPerSample:32}},setSampleFormat(bits,real){calls.push(['format',bits,real]);this.mainView.image.bitsPerSample=bits;this.mainView.image.isReal=real;},forceClose(){this.isNull=true;windows.splice(windows.indexOf(this),1);},regenerateAstrometricSolution(){}};windows.push(w);return w;}
  const first=window('first'),second=window('second');
  first.box={x0:0,y0:0,x1:700,y1:800};second.box={x0:300,y0:0,x1:1000,y1:800};
  class Metadata{ExtractMetadata(w){this.box=w.box;}SaveKeywords(){}SaveProperties(){}}
  class Engine{CreateMetadata(){return new Metadata;}}
  class Reprojection{reprojectedImage(_r,w){calls.push(['warp',w.mainView.id]);return window('warp_'+w.mainView.id,w.mainView.image.numberOfNominalChannels);}static reprojectedBounds(_r,m){return m.box;}}
  class Mosaic{static Average=0;executeGlobal(){calls.push(['merge',this.targetFrames,this.nShrinkCount,this.nFeatherRadius]);window('merged',first.mainView.image.numberOfNominalChannels).mainView.image.bitsPerSample=outputBits;return true;}toSource(){return 'var P = new GradientMergeMosaic;';}}
  class Debayer{static RGGB=0;static BGGR=1;static GBRG=2;static GRBG=3;static VNG=0;executeOn(v){calls.push(['debayer',this.cfaPattern]);this.outputImage=window('debayer',3).mainView.id;return true;}toSource(){return 'var P = new Debayer;';}}
  const ctx={ImageWindow:{get windows(){return windows;},windowById(id){return windows.find(w=>w.mainView.id===id)||{isNull:true};}},AstrometricMetadata:Metadata,MosaicByCoordinatesEngine:Engine,ImageReprojection:Reprojection,GradientMergeMosaic:Mosaic,Debayer,Projection:{Gnomonic:0},InterpolationAlgorithm:{Auto:0}};
  vm.createContext(ctx);vm.runInContext(source,ctx);
  const spec={role:'RGB',shrink:1,feather:10,canvas:{width:1000,height:800,centerRA:10,centerDec:40,resolution:0.0003,rotation:0},inputs:[{panelId:'P1',window:first},{panelId:'P2',window:second}]};
  const record=(name,data)=>events.push({name,data});
  const save=(w,name)=>{saves.push(name);return '/scoped/outputs/'+name;};
  return {ctx,spec,calls,events,saves,windows,record,save};
}
test('mosaic reprojects every solved selected panel before merging, saves bound checkpoints',()=>{
  const f=fixture();const out=f.ctx.DSGPrepareMosaicGroup(f.spec,f.record,f.save,()=>{});
  assert.equal(out.mainView.id,'merged');
  assert.deepEqual(f.calls.map(c=>c[0]),['warp','warp','merge']);
  assert.deepEqual(f.saves,['RGB-P1-registered.xisf','RGB-P2-registered.xisf','RGB-mosaic-linear.xisf']);
  assert.equal(f.events.filter(e=>e.name==='astrometric-reprojection').length,2);
  assert.equal(f.windows.some(w=>w.mainView.id.startsWith('warp_')),false);
});
test('unknown parameters, canvas clipping, unsolved and disconnected panels fail before warp',()=>{
  for(const mutate of [f=>f.spec.code='run()',f=>f.spec.feather=101,f=>f.spec.inputs[1].window.hasAstrometricSolution=false,f=>f.spec.inputs[1].window.box.x1=1002,f=>{f.spec.inputs[0].window.box.x1=200;f.spec.inputs[1].window.box.x0=300;}]){
    const f=fixture();mutate(f);assert.throws(()=>f.ctx.DSGPrepareMosaicGroup(f.spec,f.record,f.save,()=>{}));assert.equal(f.calls.length,0);
  }
});
test('native Float64 mosaic is explicitly converted and recorded before saving',()=>{
  const f=fixture(64);const out=f.ctx.DSGPrepareMosaicGroup(f.spec,f.record,f.save,()=>{});
  assert.equal(out.mainView.image.bitsPerSample,32);
  assert.deepEqual(f.calls.at(-1),['format',32,true]);
  const conversion=f.events.find(e=>e.name==='sample-format-conversion');
  assert.equal(conversion.data.fromBits,64);assert.equal(conversion.data.toBits,32);
  assert.equal(f.events.find(e=>e.name==='process-completed').data.bitsPerSample,64);
  const invalid=fixture(16);
  assert.throws(()=>invalid.ctx.DSGPrepareMosaicGroup(invalid.spec,invalid.record,invalid.save,()=>{}),/Mosaic output format/);
  assert.equal(invalid.saves.includes('RGB-mosaic-linear.xisf'),false);
});
test('monochrome LRGB and narrowband mosaic groups retain one physical channel',()=>{
  for(const role of ['R','G','B','L','Ha','OIII','SII']){
    const f=fixture(64);f.spec.role=role;
    for(const input of f.spec.inputs)input.window.mainView.image.numberOfNominalChannels=1;
    const out=f.ctx.DSGPrepareMosaicGroup(f.spec,f.record,f.save,()=>{});
    assert.equal(out.mainView.image.numberOfNominalChannels,1);
    assert.equal(out.mainView.image.bitsPerSample,32);
    assert.equal(f.saves.at(-1),role+'-mosaic-linear.xisf');
  }
});
test('cancellation after first registration cannot execute mosaic merge',()=>{
  const f=fixture();let count=0;
  assert.throws(()=>f.ctx.DSGPrepareMosaicGroup(f.spec,f.record,f.save,()=>{if(++count===2)throw Error('cancel');}),/cancel/);
  assert.deepEqual(f.calls.map(c=>c[0]),['warp']);assert.equal(f.windows.some(w=>w.mainView.id.startsWith('warp_')),false);
});
test('CFA uses only declared native Bayer pattern and retains source geometry',()=>{
  const f=fixture();f.spec.inputs[0].window.mainView.image.numberOfNominalChannels=1;
  const out=f.ctx.DSGDebayerSelectedMaster(f.spec.inputs[0].window,'GBRG',f.record,()=>{});
  assert.equal(out.mainView.image.numberOfNominalChannels,3);assert.deepEqual(f.calls,[['debayer',2]]);
  assert.equal(f.events[0].data.pattern,'GBRG');
});
test('missing CFA pattern and already RGB input execute no Debayer operation',()=>{
  const f=fixture();assert.throws(()=>f.ctx.DSGDebayerSelectedMaster(f.spec.inputs[0].window,'AUTO',f.record,()=>{}));
  assert.throws(()=>f.ctx.DSGDebayerSelectedMaster(f.spec.inputs[0].window,'RGGB',f.record,()=>{}));assert.equal(f.calls.length,0);
});
