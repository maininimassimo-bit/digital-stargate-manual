'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {execFileSync} = require('node:child_process');
const [batchDir, planDir, oracleDir, comparator, dependencies, python, work, report] = process.argv.slice(2);
const digest = raw => crypto.createHash('sha256').update(raw).digest('hex');
const parse = file => JSON.parse(fs.readFileSync(file));
const manifest = parse(path.join(batchDir,'batch-manifest.json'));
const code = fs.readFileSync(path.join(batchDir,'batch-origine.js'),'utf8');
assert.equal(digest(code),manifest.candidateSha256);
const planRaw=fs.readFileSync(path.join(planDir,'piano.json'));
assert.equal(digest(planRaw),manifest.planSha256);
const plan=JSON.parse(planRaw);
const oracle=parse(path.join(oracleDir,'riscontro.json'));
const oracleBytes = (scene,kind) => {
  const name=scene+'-'+kind+'.fits';
  const raw=fs.readFileSync(path.join(oracleDir,'oracoli',name));
  assert.equal(digest(raw),oracle.fixtureSha256['oracoli/'+name]);
  return raw;
};

const reservation='348eaf20-c65c-438c-b808-eb1c163f9a31';
const root='O:/BKL046-CFA-origine-nativa-v1/'+reservation;
const xdrzRoot='O:/BKL046-CFA-origine-fattoriale-v1/prodotti/xdrz/';
const binding={operation:manifest.operation,planSha256:manifest.planSha256,reservation};
const outputNames=plan.cases.flatMap(c=>plan.fitsKinds.map(k=>c.id+'-'+k+'.fits')).sort();
fs.mkdirSync(work);

function prepare(id, sequence, mode) {
  const dir=path.join(work,id);
  const output=path.join(dir,'outputs');
  fs.mkdirSync(output,{recursive:true});
  const console=[], windows=[{mainView:{id:'untouched'}}];
  const paths = virtual => {
    assert(virtual.startsWith(root+'/'));
    const parts=virtual.slice(root.length+1).split('/');
    assert(parts.length===1 || (parts.length===2&&parts[0]==='outputs'));
    assert(parts.every(p=>/^[a-z0-9.-]+$/.test(p) && p!=='.' && p!=='..'));
    return path.join(dir,...parts);
  };
  let calls=0;
  function makeWindow(id,bytes){
    return {isNull:false,mainView:{id,image:{width:32,height:28,numberOfChannels:3,bytes}},
      forceClose(){const i=windows.indexOf(this);assert(i>0);windows.splice(i,1);}};
  }
  class DrizzleIntegration{
    constructor(){
      for(const key of ['inputData','onError','enableCFA','cfaPattern','scale','dropShrink','kernelFunction','useLUT',
        'enableRejection','enableImageWeighting','enableSurfaceSplines','enableLocalNormalization',
        'enableAdaptiveNormalization','truncateOnOutOfRange','closePreviousImages','showImages'])this[key]=null;
    }
    toSource(){return '// synthetic controls';}
    executeGlobal(){
      const index=calls++;
      const {matrix,origin}=plan.cases[index];
      const expected=['a','b','c'].map(x=>xdrzRoot+'shear-'+x+'-'+matrix+'-origin'+origin.toFixed(1)+'.xdrz');
      assert.deepEqual(Array.from(this.inputData,r=>r[1]),expected);
      assert.equal(this.enableRejection,false);
      if(mode==='failed-case'&&index===2)return false;
      this.integrationImageId='rgb_'+index;
      this.weightImageId='weight_'+index;
      windows.push(makeWindow(this.integrationImageId,oracleBytes(sequence[index],'rgb')),
                   makeWindow(this.weightImageId,oracleBytes(sequence[index],'weight')));
      return true;
    }
  }
  Object.assign(DrizzleIntegration,{Abort:0,Auto:0,Kernel_Square:1});
  const File={
    directoryExists:v=>v===root||v===root+'/outputs',
    exists(v){
      if(!v.startsWith(xdrzRoot))return fs.existsSync(paths(v));
      const name=v.slice(xdrzRoot.length);
      const raw=fs.readFileSync(path.join(oracleDir,'xdrz',name));
      assert.equal(digest(raw),manifest.xdrzSha256[name]);
      return true;
    },
    writeTextFile:(v,text)=>fs.writeFileSync(paths(v),text,{flag:'wx'}),
    readTextFile:v=>fs.readFileSync(paths(v),'utf8')
  };
  class FileFormatInstance{
    create(file){this.file=paths(file);this.isOpen=true;return true;}
    writeImage(image){fs.writeFileSync(this.file,image.bytes,{flag:'wx'});return true;}
    setOptions(o){return o.bitsPerSample===64&&o.ieeefpSampleFormat;}
    close(){this.isOpen=false;return true;}
  }
  const env=vm.createContext({binding,File,DrizzleIntegration,FileFormatInstance,FileFormat:class{},
    ImageDescription:class{},ImageWindow:{windows,windowById:id=>windows.find(w=>w.mainView.id===id)},
    console:{writeln:line=>console.push(line)}});
  vm.runInContext(code,env,{timeout:2000});
  assert.equal(calls,0);
  return {dir,output,console,windows,run:()=>vm.runInContext('runOriginBatch(binding)',env,{timeout:5000})};
}
const results=[];
for(const [name,sequence] of Object.entries(oracle.predictedSignatures)){
  const t=prepare(name,sequence,'complete');
  t.run();
  assert.deepEqual(fs.readdirSync(t.output).sort(),outputNames);
  assert.deepEqual(t.windows.map(w=>w.mainView.id),['untouched']);
  assert.equal(t.console.length,8);
  const marker=parse(path.join(t.dir,'batch.done.json'));
  assert.deepEqual(marker,{schema:'BKL046_CFA_ORIGIN_BATCH_MARKER_V1',scope:'OUTPUT_MARKER_NOT_ADMISSION',
    operation:manifest.operation,planSha256:manifest.planSha256,reservation,cases:manifest.caseOrder});
  assert.equal(fs.readFileSync(path.join(t.dir,'events.txt'),'utf8'),t.console.join('\n')+'\n');
  const receipt=path.join(t.dir,'classificazione.json');
  execFileSync(python,['-I','-B','-S',path.join(planDir,'classifica.py'),planDir,oracleDir,comparator,dependencies,t.output,receipt]);
  const r=parse(receipt);
  assert.equal(r.status,'MATCHED_TESTED_HYPOTHESIS');
  assert.deepEqual(r.hypotheses,[name]);
  results.push({case:name,outputCount:8,matched:name,marker:true});
}
const failed=prepare('failed-case',oracle.predictedSignatures['use-declared'],'failed-case');
assert.throws(failed.run,/DrizzleIntegration returned failure/);
assert.equal(fs.existsSync(path.join(failed.dir,'batch.done.json')),false);
results.push({case:'third-case-failed',marker:false});
const reportData={schema:'BKL046_CFA_ORIGIN_BATCH_CLASSIFIER_FIXTURE_V1',batchSha256:manifest.candidateSha256,
  planSha256:manifest.planSha256,results,nativeExecutions:0,admissionRequested:false};
fs.writeFileSync(report,JSON.stringify(reportData,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify(reportData));
