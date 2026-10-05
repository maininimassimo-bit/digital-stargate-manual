import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';

const source=readFileSync(new URL('./executor.jsh',import.meta.url),'utf8');
const digest='a'.repeat(64),token='b'.repeat(32),root='/worker/Job_1';
function fixture(){
  const m={schemaVersion:'1.0',jobId:'Job_1',recipe:'LRGB_LINEAR_PREP_V1',workerRoot:'/worker',jobDirectory:root,token,
    runtimeLibrary:root+'/executor.jsh',runtimeSha256:digest,
    background:{polyDegree:1,boxSize:12,boxSeparation:16},
    inputs:['R','G','B','L'].map(role=>({role,path:`${root}/inputs/${role}.xisf`,sourcePath:`/source/${role}.xisf`,sha256:digest,imageIndex:0,width:10,height:12}))};
  const files=new Map([['/worker/active-job.json',JSON.stringify({jobId:m.jobId,token})]]);
  files.set(m.runtimeLibrary,'trusted snapshot');
  for(const i of m.inputs){files.set(i.path,'pixels');files.set(i.sourcePath,'pixels');}
  let leased=false,operations=0,cancelAfter=false,failProcess=false,leaseEnforced=true,cancelAt=0,failAt=0;
  class File {
    static exists(p){return files.has(p);}
    static readFile(p){return {digest:files.get(p)==='corrupt'?'c'.repeat(64):digest};}
    static readTextFile(p){return files.get(p);}
    openForReadWrite(p){if(leased && leaseEnforced)throw Error('exclusive');leased=true;this.isOpen=true;this.path=p;this.size=files.get(p).length;}
    createForWriting(p){this.path=p;this.isOpen=true;}
    read(){return {utf8ToString:()=>files.get(this.path)};}
    write(data){files.set(this.path,data);}
    close(){this.isOpen=false;if(this.path==='/worker/active-job.json')leased=false;}
  }
  const views=new Map();
  function window(channels=1,id='source'){
    const w={isNull:false,isModified:false,keywords:[],hasAstrometricSolution:false,show(){},bringToFront(){},removeMask(){},regenerateAstrometricSolution(){},
      saveAs(path){files.set(path,'pixels');return true;},
      mainView:{id,historyIndex:0,properties:[],setPropertyValue(){},setPropertyAttributes(){},deleteProperty(){},
        computeOrFetchProperty(){return {at:()=>0.002};},beginProcess(){},endProcess(){},image:{width:m.inputs[0].width,height:m.inputs[0].height,numberOfNominalChannels:channels,isColor:channels===3,isReal:true,bitsPerSample:32,assign(){}}}};
    views.set(id,w);return w;
  }
  function ImageWindow(width,height,channels,bits,float,color,id){return window(channels,id);}
  ImageWindow.windowById=id=>views.get(id)||{isNull:true};
  ImageWindow.open=()=>[window(m.recipe==='OSC_FIELD_NONLINEAR_V1'?3:1)];ImageWindow.activeWindow={isNull:true};
  Object.defineProperty(ImageWindow,'windows',{get:()=>[...views.values()]});
  function process(){operations++;if(cancelAfter || operations===cancelAt)files.set(root+'/cancel.json',JSON.stringify({jobId:m.jobId,token,requested:true}));if(failProcess || operations===failAt)return false;return true;}
  class ABE{toSource(){return 'synthetic-native-ABE';}executeOn(){return process();}}
  class CC{toSource(){return 'synthetic-native-CC';}executeGlobal(){nativeCalls.push({...this});if(!process())return false;ImageWindow.activeWindow=window(3,'rgb');return true;}}
  const nativeCalls=[];
  class Native{toSource(){return 'synthetic-native-instance';}executeOn(){nativeCalls.push({...this});return process();}}
  class SXT extends Native{executeOn(v){if(!process())return false;window(v.image.numberOfNominalChannels,'stars'+operations);return true;}}
  const context={File,ImageWindow,FITSKeyword:class{constructor(name,value,comment){Object.assign(this,{name,value,comment});}},AutomaticBackgroundExtractor:ABE,ChannelCombination:CC,
    DataType:{ByteArray:0},ByteArray:{stringToUTF8:s=>s},Console:{show(){},writeln(){},criticalln(){}},
    BlurXTerminator:Native,NoiseXTerminator:Native,StarXTerminator:SXT,BackgroundNeutralization:Native,
    ColorCalibration:Native,MaskedStretch:Native,PixelMath:Native,LocalHistogramEqualization:Native,
    CurvesTransformation:Native,LRGBCombination:Native,ArcsinhStretch:Native,
    CoreApplication:{versionMajor:1,versionMinor:9,versionRelease:5,versionBuild:1706},
    CryptographicHash:class{hash(data){return {toHex:()=>data.digest};}}};
  vm.createContext(context);vm.runInContext(source,context);
  return {m,context,files,nativeCalls,run:()=>context.DSGExecuteLocalPilot(m),operations:()=>operations,leased:()=>leased,
    cancelAfter:()=>{cancelAfter=true;},cancelAt:n=>{cancelAt=n;},failAt:n=>{failAt=n;},failProcess:()=>{failProcess=true;},disableLease:()=>{leaseEnforced=false;}};
}
test('fixed recipe completes five native operations and five separate checkpoints',()=>{
  const f=fixture(),r=f.run();assert.equal(r.status,'COMPLETED');assert.equal(r.processCount,5);
  assert.equal(r.outputs.length,5);assert.equal(r.originalViewsUnmodified,true);assert.equal(f.leased(),false);
  assert.ok([...f.files.keys()].some(k=>k.endsWith('process-started.json')));
});
test('pre-cancel executes no pixel operation and retains terminal receipt',()=>{
  const f=fixture();f.files.set(root+'/cancel.json',JSON.stringify({jobId:f.m.jobId,token,requested:true}));const r=f.run();
  assert.equal(r.status,'CANCELLED');assert.equal(f.operations(),0);assert.ok(f.files.has(root+'/terminal.json'));
});
test('cancel between processes retains completed action and stops next operation',()=>{
  const f=fixture();f.cancelAfter();const r=f.run();assert.equal(r.status,'CANCELLED');assert.equal(r.processCount,1);assert.equal(f.operations(),1);
});
test('mismatched cancellation identity fails without classifying another job cancellation',()=>{
  const f=fixture();f.files.set(root+'/cancel.json',JSON.stringify({jobId:'Other',token,requested:true}));
  const r=f.run();assert.equal(r.status,'FAILED');assert.match(r.error,/Cancellation identity mismatch/);assert.equal(f.operations(),0);
});
test('native false result becomes failure without success checkpoint',()=>{
  const f=fixture();f.failProcess();const r=f.run();assert.equal(r.status,'FAILED');assert.equal(r.outputs.length,0);
});
test('module missing fails without pixel operation',()=>{
  const f=fixture();delete f.context.ChannelCombination;assert.equal(f.run().status,'FAILED');assert.equal(f.operations(),0);
});
test('source or scratch corruption fails before any native operation',()=>{
  const f=fixture();f.files.set(f.m.inputs[2].sourcePath,'corrupt');assert.equal(f.run().status,'FAILED');assert.equal(f.operations(),0);
});
test('same job replay is refused before any lease or operation',()=>{
  const f=fixture();f.run();assert.throws(f.run,/Job already executed/);assert.equal(f.operations(),5);
});
test('unproven platform lease fails closed',()=>{
  const f=fixture();f.disableLease();assert.equal(f.run().status,'FAILED');assert.equal(f.operations(),0);
});
for(const [label,mutate] of [
  ['unapproved recipe',m=>m.recipe='IMPORTED_JS'],
  ['target outside job',m=>m.inputs[0].path='/source/R.xisf'],
  ['unsafe job name',m=>m.jobId='../escape'],
  ['out-of-bounds parameter',m=>m.background.polyDegree=6],
  ['unexpected parameter',m=>m.background.script='eval()'],
  ['unspecified container selection',m=>delete m.inputs[0].imageIndex]
])test(`rejects ${label}`,()=>{const f=fixture();mutate(f.m);assert.throws(f.run);assert.equal(f.operations(),0);});

function nonlinearFixture(){const f=fixture();f.m.recipe='M27_LRGB_NONLINEAR_V1';for(const i of f.m.inputs){i.width=1000;i.height=800;}return f;}

function fieldFixture(mode){
  const f=fixture();f.m.recipe=mode+'_FIELD_NONLINEAR_V1';
  const roles=mode==='OSC'?['RGB']:mode==='SHO'?['SII','Ha','OIII']:mode==='HOO'?['Ha','OIII']:['R','G','B','L'];
  f.m.inputs=roles.map(role=>({role,path:`${root}/inputs/${role}.xisf`,sourcePath:`/source/${role}.xisf`,sha256:digest,imageIndex:0,width:1000,height:800}));
  for(const i of f.m.inputs){f.files.set(i.path,'pixels');f.files.set(i.sourcePath,'pixels');}
  f.m.processing={sharpenL:.4,sharpenRGB:.3,denoiseL:.6,denoiseRGB:.6,contrastLarge:.2,contrastSmall:.15,targetBackground:.07};
  f.m.field={target:'NGC 281',backgroundROI:[.05,.1,.15,.2],maskLow:.08,maskHigh:.5,contrastLargeRadius:64,contrastSmallRadius:24,starsStretch:80,saturation:.1};
  return f;
}

for(const [mode,count,outputs] of [['LRGB',29,15],['OSC',26,12],['SHO',27,15],['HOO',26,14]]) {
  test(`${mode} field recipe has bound channels, reviewed scene parameters and complete checkpoints`,()=>{
    const f=fieldFixture(mode),r=f.run();assert.equal(r.status,'COMPLETED',r.error);assert.equal(r.processCount,count);assert.equal(r.outputs.length,outputs);
    assert.equal(r.originalViewsUnmodified,true);assert.equal(f.leased(),false);
    const events=[...f.files.entries()].filter(([k])=>k.includes('/events/')).map(([,v])=>JSON.parse(v));
    const completed=events.filter(e=>e.event==='process-completed').map(e=>e.data.label);
    assert.equal(completed.includes('calibrate-RGB'),mode==='LRGB'||mode==='OSC');
    const neutralize=f.nativeCalls.find(p=>p.roiX0!==undefined);assert.equal(neutralize.roiX0,50);assert.equal(neutralize.roiY0,80);
    const contrast=f.nativeCalls.filter(p=>p.radius!==undefined);assert.deepEqual(contrast.map(p=>p.radius),[64,24]);
    if(mode==='OSC'){assert.equal(completed.includes('RGB-composition'),false);assert.ok(f.nativeCalls.some(p=>p.expression?.includes('0.2126*DSG_Job_1_RGB[0]')));}
    else {const combination=f.nativeCalls.find(p=>p.channels);const channelIds=Array.from(combination.channels,row=>row[1]);
      if(mode==='SHO')assert.deepEqual(channelIds,['DSG_Job_1_SII','DSG_Job_1_Ha','DSG_Job_1_OIII']);
      if(mode==='HOO')assert.deepEqual(channelIds,['DSG_Job_1_Ha','DSG_Job_1_OIII','DSG_Job_1_OIII']);}
  });
}

test('missing or unsafe reviewed field stops before pixel operations',()=>{
  for(const mutation of [m=>delete m.field,m=>m.field.backgroundROI=[0,0,0,0],m=>m.field.starsStretch=999,m=>m.field.script='eval()']){
    const f=fieldFixture('OSC');mutation(f.m);assert.throws(f.run);assert.equal(f.operations(),0);
  }
});
test('M27 recipe completes 29 native operations, saves 15 checkpoints and journals masks',()=>{
  const f=nonlinearFixture(),r=f.run();assert.equal(r.status,'COMPLETED');assert.equal(r.processCount,29);
  assert.equal(r.outputs.length,15);assert.equal(r.outputs.at(-1).nonLinear,true);assert.equal(r.outputs.at(-1).channels,3);
  const events=[...f.files.entries()].filter(([k])=>k.includes('/events/')).map(([,v])=>JSON.parse(v));
  assert.equal(events.filter(e=>e.event==='mask-attached').length,3);
  assert.equal(events.filter(e=>e.event==='mask-detached').length,3);
  assert.equal(events.filter(e=>e.event==='secondary-output').length,2);
});
test('M27 missing licensed module fails before processing or checkpoints',()=>{
  const f=nonlinearFixture();delete f.context.StarXTerminator;const r=f.run();assert.equal(r.status,'FAILED');assert.equal(f.operations(),0);assert.equal(r.outputs.length,0);
});
test('M27 undersized image fails before pixel operation',()=>{
  const f=fixture();f.m.recipe='M27_LRGB_NONLINEAR_V1';assert.equal(f.run().status,'FAILED');assert.equal(f.operations(),0);
});
test('M27 cancellation after masked processing removes mask and never saves final',()=>{
  const f=nonlinearFixture();f.cancelAt(20);const r=f.run();assert.equal(r.status,'CANCELLED');assert.equal(r.processCount,20);
  assert.ok(!r.outputs.some(o=>o.name==='LRGB-nonlinear.xisf'));
  const events=[...f.files.entries()].filter(([k])=>k.includes('/events/')).map(([,v])=>JSON.parse(v));
  assert.equal(events.filter(e=>e.event==='mask-attached').length,events.filter(e=>e.event==='mask-detached').length);
  assert.equal(f.leased(),false);
});
test('M27 native masked process failure removes mask and retains partial checkpoints',()=>{
  const f=nonlinearFixture();f.failAt(21);const r=f.run();assert.equal(r.status,'FAILED');assert.equal(r.processCount,20);
  assert.ok(r.outputs.length>5);assert.ok(!r.outputs.some(o=>o.name==='LRGB-nonlinear.xisf'));
  const events=[...f.files.entries()].filter(([k])=>k.includes('/events/')).map(([,v])=>JSON.parse(v));
  assert.equal(events.filter(e=>e.event==='mask-attached').length,events.filter(e=>e.event==='mask-detached').length);
});


test('reviewed processing parameters reach native process instances within the fixed M27 order',()=>{
 const f=nonlinearFixture();f.m.processing={sharpenL:0.58,sharpenRGB:0.35,denoiseL:0.5,denoiseRGB:0.6,contrastLarge:0.3,contrastSmall:0.32,targetBackground:0.07};
 const r=f.run();assert.equal(r.status,'COMPLETED');assert.equal(r.processCount,29);
 assert.deepEqual(f.nativeCalls.filter(p=>'sharpen_nonstellar' in p).map(p=>p.sharpen_nonstellar),[0.35,0.58]);
 assert.deepEqual(f.nativeCalls.filter(p=>'denoise' in p).map(p=>p.denoise),[0.6,0.5]);
 assert.deepEqual(f.nativeCalls.filter(p=>'targetBackground' in p).map(p=>p.targetBackground),[0.07,0.07]);
 assert.deepEqual(f.nativeCalls.filter(p=>'amount' in p).map(p=>p.amount),[0.3,0.32]);
});
test('unsafe or unknown processing parameters stop before any native pixel operation',()=>{
 for(const change of [{sharpenL:0.9},{targetBackground:0.001},{script:'alert(1)'},{denoiseL:true}]){
  const f=nonlinearFixture();f.m.processing={sharpenL:0.5,sharpenRGB:0.45,denoiseL:0.65,denoiseRGB:0.7,contrastLarge:0.22,contrastSmall:0.28,targetBackground:0.085,...change};
  assert.throws(()=>f.run(),/processing|Processing/);assert.equal(f.operations(),0);
 }
});
