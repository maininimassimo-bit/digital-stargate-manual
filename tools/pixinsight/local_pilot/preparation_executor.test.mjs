import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const kernel=fs.readFileSync(new URL('./source_preparation.jsh',import.meta.url),'utf8');
const executor=fs.readFileSync(new URL('./preparation_executor.jsh',import.meta.url),'utf8');
const sha='a'.repeat(64),token='b'.repeat(32);
function fixture(mode='OSC',layout='PANELS'){
  const roles=mode==='LRGB'?['R','G','B','L']:mode==='SHO'?['SII','Ha','OIII']:mode==='HOO'?['Ha','OIII']:mode==='OSC'?['RGB']:['CFA'];
  const panels=layout==='PANELS'?['P1','P2']:['P1'];
  const m={schemaVersion:'1.0',jobId:'Prep_1',mode,layout,bayerPattern:mode==='OSC_CFA'?'RGGB':null,
    canvas:layout==='PANELS'?{centerRA:10,centerDec:40,resolution:.0003,rotation:0,width:1000,height:800}:null,
    shrink:layout==='PANELS'?1:0,feather:layout==='PANELS'?10:0,workerRoot:'/worker',jobDirectory:'/worker/Prep_1',token,
    authority:'LOCAL_SOURCE_PREPARATION_NOT_OWNER_PORTAL_JOB',requestSha256:sha,
    runtimeHashes:{'source_preparation.jsh':sha,'preparation_executor.jsh':sha},enginePath:'/installed/MosaicByCoordinatesEngine.js',engineSha256:sha,
    inputs:panels.flatMap(panelId=>roles.map(role=>({panelId,role,path:`/worker/Prep_1/inputs/${role}-${panelId}.xisf`,sourcePath:`/source/${role}-${panelId}.xisf`,sha256:sha,imageIndex:0,width:1000,height:800}))),expectedOutputs:{},
    nativeProcessCount:(mode==='OSC_CFA'?panels.length:0)+(layout==='PANELS'?(mode==='OSC_CFA'?1:roles.length):0)};
  const resultRoles=mode==='OSC_CFA'?['RGB']:roles;
  if(mode==='OSC_CFA')for(const p of panels)m.expectedOutputs[`RGB-${p}-debayer.xisf`]=3;
  if(layout==='PANELS')for(const role of resultRoles){for(const p of panels)m.expectedOutputs[`${role}-${p}-registered.xisf`]=role==='RGB'?3:1;m.expectedOutputs[`${role}-mosaic-linear.xisf`]=role==='RGB'?3:1;}
  else m.expectedOutputs['RGB-linear.xisf']=3;
  const request=Object.fromEntries(['schemaVersion','jobId','mode','layout','bayerPattern','canvas','shrink','feather'].map(k=>[k,m[k]]));
  request.inputs=m.inputs.map(r=>Object.fromEntries(['panelId','role','sha256','imageIndex','width','height'].map(k=>[k,r[k]]).concat([['path',r.sourcePath]])));
  const files=new Map([['/worker/active-job.json',JSON.stringify({jobId:m.jobId,token,authority:m.authority,requestSha256:sha})],[m.jobDirectory+'/request.json',JSON.stringify(request)]]);
  for(const name of Object.keys(m.runtimeHashes))files.set(m.jobDirectory+'/'+name,'trusted');
  files.set(m.enginePath,'installed');for(const row of m.inputs){files.set(row.path,'pixels');files.set(row.sourcePath,'pixels');}
  let leased=false,operationCount=0,opened=0,unsolved=false;
  class File{
    static exists(p){return files.has(p);}static readFile(p){return {hash:files.get(p)==='corrupt'?'c'.repeat(64):sha};}static readTextFile(p){return files.get(p);}
    openForReadWrite(p){if(leased)throw Error('exclusive');leased=true;this.path=p;this.isOpen=true;this.size=files.get(p).length;}
    read(){return {utf8ToString:()=>files.get(this.path)};}createForWriting(p){this.path=p;this.isOpen=true;}
    write(value){files.set(this.path,value);}close(){this.isOpen=false;if(this.path==='/worker/active-job.json')leased=false;}
  }
  const windows=[];
  function window(channels,id,bits=32){
    const w={isNull:false,isModified:false,hasAstrometricSolution:!unsolved,box:{x0:0,y0:0,x1:1000,y1:800},
      mainView:{id,historyIndex:0,image:{width:1000,height:800,numberOfNominalChannels:channels,isReal:true,bitsPerSample:bits}},
      forceClose(){this.isNull=true;windows.splice(windows.indexOf(this),1);},saveAs(path){files.set(path,'pixels');return true;},
      setSampleFormat(bits,real){this.mainView.image.bitsPerSample=bits;this.mainView.image.isReal=real;},regenerateAstrometricSolution(){this.hasAstrometricSolution=true;}};
    windows.push(w);return w;
  }
  const ImageWindow={get windows(){return windows;},windowById(id){return windows.find(w=>w.mainView.id===id)||{isNull:true};},
    open(){const channels=mode==='OSC'?3:1;return [window(channels,'source'+(++opened)),window(channels,'reject'+opened)];}};
  class Metadata{ExtractMetadata(w){this.box=w.box;}SaveKeywords(){}SaveProperties(){}}
  class Engine{CreateMetadata(){return new Metadata;}}
  class Reprojection{reprojectedImage(_reference,w){return window(w.mainView.image.numberOfNominalChannels,'warped'+(++opened));}static reprojectedBounds(_reference,m){return m.box;}}
  class Mosaic{static Average=0;executeGlobal(){++operationCount;window(mode==='OSC'||mode==='OSC_CFA'?3:1,'merged'+operationCount,64);return true;}toSource(){return 'var P = new GradientMergeMosaic;';}}
  class Debayer{static RGGB=0;static BGGR=1;static GBRG=2;static GRBG=3;static VNG=0;executeOn(){++operationCount;this.outputImage=window(3,'debayer'+operationCount).mainView.id;return true;}toSource(){return 'var P = new Debayer;';}}
  const ctx={File,ImageWindow,AstrometricMetadata:Metadata,MosaicByCoordinatesEngine:Engine,ImageReprojection:Reprojection,
    GradientMergeMosaic:Mosaic,Debayer,Projection:{Gnomonic:0},InterpolationAlgorithm:{Auto:0},DataType:{ByteArray:0},
    ByteArray:{stringToUTF8:s=>s},Console:{show(){},criticalln(){}},CryptographicHash:class{hash(v){return {toHex:()=>v.hash};}}};
  vm.createContext(ctx);vm.runInContext(kernel+'\n'+executor,ctx);
  return {m,ctx,files,windows,run:()=>ctx.DSGExecuteMasterPreparation(m),operationCount:()=>operationCount,leased:()=>leased,unsolved:()=>{unsolved=true;}};
}

for(const mode of ['LRGB','OSC','SHO','HOO','OSC_CFA'])test(`preparation ${mode} has exact native instances/checkpoints and closes owned views`,()=>{
  const f=fixture(mode),receipt=f.run();assert.equal(receipt.status,'COMPLETED',receipt.error);
  assert.equal(receipt.processCount,f.m.nativeProcessCount);assert.equal(receipt.outputs.length,Object.keys(f.m.expectedOutputs).length);
  assert.equal(receipt.originalIntegrity,'UNCHANGED');assert.equal(f.leased(),false);assert.equal(f.windows.length,0);
});
test('single CFA preserves explicit debayer checkpoint and prepared RGB without mosaic',()=>{
  const f=fixture('OSC_CFA','SINGLE'),receipt=f.run();assert.equal(receipt.status,'COMPLETED',receipt.error);
  assert.equal(receipt.processCount,1);assert.equal(receipt.outputs.length,2);
});
test('changed immutable request, source binding, runtime, canvas or missing module cannot process pixels',()=>{
  for(const mutate of [f=>f.files.set(f.m.jobDirectory+'/request.json','corrupt'),f=>f.m.inputs[0].sourcePath='/other/master.xisf',
      f=>f.files.set(f.m.jobDirectory+'/source_preparation.jsh','corrupt'),f=>f.m.canvas.width=999,f=>delete f.ctx.Debayer]){
    const f=fixture('OSC_CFA');mutate(f);assert.equal(f.run().status,'FAILED');assert.equal(f.operationCount(),0);
  }
});
test('unsolved mosaic preflight and identity-bound pre-cancel execute no native process',()=>{
  const f=fixture();f.unsolved();assert.equal(f.run().status,'FAILED');assert.equal(f.operationCount(),0);
  const cancelled=fixture();cancelled.files.set(cancelled.m.jobDirectory+'/cancel.json',JSON.stringify({jobId:cancelled.m.jobId,token,requested:true}));
  assert.equal(cancelled.run().status,'CANCELLED');assert.equal(cancelled.operationCount(),0);
  assert.equal(cancelled.windows.length,0);
});
test('same preparation cannot replay or overwrite terminal artifacts',()=>{
  const f=fixture();f.run();const count=f.operationCount();assert.throws(f.run,/scope\/replay/);assert.equal(f.operationCount(),count);
});
