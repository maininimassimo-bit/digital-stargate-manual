'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const [candidate, batchPath, controls, python, root, output] = process.argv.slice(2);
const hash = raw => crypto.createHash('sha256').update(raw).digest('hex');
function pinned(file, expected) {
  const raw = fs.readFileSync(file);
  assert.equal(hash(raw), expected, path.basename(file));
  return raw;
}
const subjectSHA = '3ad86ab652dbe80b08fc6b939dd2b10fb3038563784598f08c10ada3a545b072';
const batchSHA = '0b91c52cc63eb0196f1e9ba5ac6774ebb7a9d28478392358976ae8f7138a87ec';
const subject = JSON.parse(pinned(path.join(candidate,'launcher-subject.json'),subjectSHA));
const batch = pinned(batchPath,batchSHA).toString('utf8');
const plan = JSON.parse(pinned(path.join(controls,'piano-controllo.json'),subject.inputPlanSha256));
const fixtures = path.join(controls,'fixture');
const manifest = JSON.parse(pinned(path.join(fixtures,'manifest.json'),subject.fixtureManifestSha256));
const comparator = path.join(candidate,'comparator.cjs');
pinned(comparator,subject.memberSha256['comparator.cjs']);
pinned(process.execPath,subject.nodeSha256);
pinned(python,subject.pythonSha256);
const {verifierFor} = require(comparator);

const reservation='52d471bc-3d3d-42ea-ad47-29146dbd36a5';
const virtualRoot='O:/BKL046-CFA-XDRZ-esecuzioni-v1/'+reservation;
const virtualInputs='O:/BKL046-CFA-XDRZ-tre-ingressi-v1/fixture/';
const binding={operation:subject.operation,planSha256:subject.inputPlanSha256,
  subjectSha256:subject.syntheticSubjectSha256,reservation};
const outputsByScene = {};
for (const scene of ['detector','reference','unmasked','wrong-channel','shear']) {
  outputsByScene[scene]={};
  for (const kind of ['rgb','weight']) {
    const name=scene+'-expected-'+kind+'.fits';
    outputsByScene[scene][kind]=pinned(path.join(fixtures,name),manifest.files[name]);
  }
}

function prepare(directory,mask,shear,mode) {
  const out=path.join(directory,'outputs');
  fs.mkdirSync(out,{recursive:true});
  const events=[];
  let executions=0;
  const windows=[{mainView:{id:'pre-existing'}}];
  const outputPath = virtual => {
    assert.equal(path.posix.dirname(virtual),virtualRoot);
    return path.join(out,path.posix.basename(virtual));
  };
  function window(id,bytes) {
    return {isNull:false,mainView:{id,image:{width:32,height:28,numberOfChannels:3,bytes}},
      forceClose(){const i=windows.indexOf(this);assert(i>0);windows.splice(i,1);}};
  }
  class DrizzleIntegration {
    constructor() {
      for (const key of ['inputData','onError','enableCFA','cfaPattern','scale','dropShrink','kernelFunction',
        'useLUT','enableRejection','enableImageWeighting','enableSurfaceSplines','enableLocalNormalization',
        'enableAdaptiveNormalization','truncateOnOutOfRange','closePreviousImages','showImages']) this[key]=null;
    }
    toSource(){return '// Fixture: process state supplied by JavaScript test double';}
    executeGlobal(){
      const ctl=plan.cases[executions++];
      assert.deepEqual(Array.from(this.inputData, row=>path.posix.basename(row[1])),ctl.files);
      if (mode==='incomplete' && executions===3) return false;
      let scene=ctl.expected[0];
      if (ctl.id==='integer-green-mask') scene=mask;
      if (ctl.id.startsWith('shear-') && ctl.id!==shear && mode!=='ambiguous') scene='unmasked';
      this.integrationImageId='rgb_'+executions;
      this.weightImageId='weight_'+executions;
      const {rgb,weight}=outputsByScene[scene];
      const selected = mode==='incorrect-frame' && executions===2 ? outputsByScene.unmasked.weight : weight;
      windows.push(window(this.integrationImageId,rgb),window(this.weightImageId,selected));
      return true;
    }
  }
  Object.assign(DrizzleIntegration,{Abort:0,Auto:0,Kernel_Square:1});
  class FileFormat{
    constructor(ext,read,write){assert.deepEqual([ext,read,write],['.fits',false,true]);}
  }
  class FileFormatInstance{
    create(virtual){this.filename=outputPath(virtual);this.isOpen=true;return true;}
    setOptions(o){return o.bitsPerSample===64 && o.ieeefpSampleFormat;}
    writeImage(image){fs.writeFileSync(this.filename,image.bytes,{flag:'wx'});return true;}
    close(){this.isOpen=false;return true;}
  }
  const File={
    directoryExists: v=>v===virtualRoot,
    exists(v){
      if (!v.startsWith(virtualInputs)) return fs.existsSync(outputPath(v));
      const name=v.slice(virtualInputs.length);
      pinned(path.join(fixtures,name),manifest.files[name]);
      return true;
    },
    writeTextFile:(v,bytes)=>fs.writeFileSync(outputPath(v),bytes,{flag:'wx'}),
    readTextFile:v=>fs.readFileSync(outputPath(v),'utf8')
  };
  const sandbox=vm.createContext({File,FileFormat,FileFormatInstance,DrizzleIntegration,
    ImageDescription:class{},
    ImageWindow:{windows,windowById:id=>windows.find(w=>w.mainView.id===id)},
    console:{writeln:line=>events.push(line)},binding});
  vm.runInContext(batch,sandbox,{timeout:2000});
  assert.equal(executions,0);
  const marker=path.join(out,'batch.done.json');
  const execute=()=>vm.runInContext('runCfaXdrzBatch(binding)',sandbox,{timeout:5000});
  return {out,execute,events,windows,marker,count:()=>executions};
}

async function main(){
  fs.mkdirSync(root);
  const result=[];
  for(const [mode,mask,shear,failure] of [
    ['detector','detector','shear-center0',null],
    ['reference','reference','shear-edge05',null],
    ['incorrect-frame','detector','shear-center0',/unexpected native comparison/],
    ['ambiguous','detector','shear-center0',/geometry convention missing or ambiguous/],
    ['incomplete','detector','shear-center0',/DrizzleIntegration returned failure/],
  ]){
    const state=path.join(root,mode);
    const t=prepare(state,mask,shear,mode);
    if(mode==='incomplete'){
      assert.throws(t.execute,failure);
      assert.equal(t.count(),3);
      assert.equal(fs.existsSync(t.marker),false);
      result.push({mode,marker:false,accepted:false});
      continue;
    }
    t.execute();
    assert.equal(t.count(),5);
    assert.deepEqual(t.windows.map(w=>w.mainView.id),['pre-existing']);
    assert.equal(fs.readFileSync(path.join(t.out,'events.txt'),'utf8'),t.events.slice(0,10).join('\n')+'\n');
    assert.equal(t.events.length,11);
    const context={reservation,operation:binding.operation,plan:binding.planSha256,subject:binding.subjectSha256,
      batchMarkerSha256:hash(fs.readFileSync(t.marker))};
    const v=verifierFor(python,state,t.out);
    if(failure) {
      await assert.rejects(v.compare(context), e=>e.message==='CFA comparator failed' && failure.test(e.cause?.stderr??''));
      assert.equal(fs.existsSync(path.join(state,'comparison.json')),false);
      result.push({mode,marker:true,accepted:false});
    } else {
      const verified=await v.compare(context);
      await v.revalidate(context,verified.receiptSha256);
      const receipt=JSON.parse(fs.readFileSync(path.join(state,'comparison.json')));
      assert.equal(receipt.evidence.maskCoordinates,mask);
      assert.equal(receipt.evidence.shearAgreement,shear);
      result.push({mode,marker:true,accepted:true,mask,shear});
    }
  }
  const r={schema:'BKL046_CFA_PJSR_COMPARATOR_BOUNDARY_V1',subjectSHA,batchSHA,
    comparatorSHA:subject.memberSha256['comparator.cjs'],cases:result,simulatedPjsrRuntime:true,
    nativeExecutions:0,scientificClosures:0,admissionRequested:false};
  fs.writeFileSync(output,JSON.stringify(r,null,2)+'\n',{flag:'wx'});
  console.log(JSON.stringify(r));
}
main().catch(error=>{console.error(error);process.exitCode=1});
