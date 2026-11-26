'use strict';
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const [candidate,planPath,contractPath,out]=process.argv.slice(2);
const pin=raw=>crypto.createHash('sha256').update(raw).digest('hex');
const code=fs.readFileSync(candidate,'utf8');
const planRaw=fs.readFileSync(planPath);
const contractRaw=fs.readFileSync(contractPath);
const contract=JSON.parse(contractRaw);
assert.equal(contract.fixtureReceiptSha256,pin(planRaw));
const cases=JSON.parse(planRaw).arms;
const reservation='52d471bc-3d3d-42ea-ad47-29146dbd36a5';
const root='O:/BKL046-CFA-XDRZ-weight-window-runs-v1/'+reservation;
const binding={
    operation:'BKL046_CFA_XDRZ_WEIGHT_WINDOW_DSG_SHARED_001',
    planSha256:pin(planRaw),
    componentContractSha256:pin(contractRaw),
    reservation
};
function make(mode) {
   const stats={calls:0,lines:[],removed:[],processed:[]};
   const files=new Map();
   if (mode==='prior-transcript') files.set(root+'/events.txt','old');
   if (mode==='prior-product') files.set(root+'/zero-reference-weight.fits','old');
   const windows=[{mainView:{id:'externally-open'}}];
   function window(id) {
      return {isNull:false, mainView:{id,image:{width:32,height:28,numberOfChannels:3}},
         forceClose() {
            if(mode==='leaked-window'&&id.startsWith('weight_')) return;
            const i=windows.indexOf(this);
            assert.ok(i>0,'attempted to close an old window');
            windows.splice(i,1);
            stats.removed.push(id);
            this.isNull=true;
         }};
   }
   class DrizzleIntegration {
      constructor(){
         for(const key of ['inputData','onError','enableCFA','cfaPattern','scale','dropShrink',
          'kernelFunction','useLUT','enableRejection','enableImageWeighting','enableSurfaceSplines',
          'enableLocalNormalization','enableAdaptiveNormalization','truncateOnOutOfRange',
          'closePreviousImages','showImages']) this[key]=null;
      }
      toSource(){return 'fixed effective state';}
      executeGlobal(){
         stats.calls++;
         stats.processed.push(this.inputData.map(row=>path.basename(row[1])));
         if(mode==='third-case-failed' && stats.calls===3) return false;
         this.integrationImageId='rgb_'+stats.calls;
         this.weightImageId='weight_'+stats.calls;
         windows.push(window(this.integrationImageId),window(this.weightImageId));
         return true;
      }
   }
   Object.assign(DrizzleIntegration,{Auto:0,Abort:0,Kernel_Square:1});
   class FileFormat{}
   class FileFormatInstance {
      create(file){this.file=file;this.isOpen=true;return true;}
      setOptions(o){return o.bitsPerSample===64&&o.ieeefpSampleFormat;}
      writeImage(){
         if(mode==='write-failure'&&this.file.includes('mask-green-weight')) return false;
         files.set(this.file,'test FITS');
         return true;
      }
      close(){this.isOpen=false;return true;}
   }
   const File={
      exists(f){return f.endsWith('.xdrz')?fs.existsSync(path.join(path.dirname(planPath),path.basename(f))):files.has(f);},
      directoryExists(f){return mode!=='no-directory'&&f===root;},
      writeTextFile(f,v){assert.equal(files.has(f),false);files.set(f,v);},
      readTextFile(f){return files.get(f)+(mode==='damaged-transcript'&&f.endsWith('events.txt')?'altered':'');}
   };
   const env=vm.createContext({DrizzleIntegration, ImageWindow:{windows,
      windowById:id=>windows.find(w=>w.mainView.id===id)},FileFormat,FileFormatInstance,
      ImageDescription:class {},File,console:{writeln:line=>stats.lines.push(line)}});
   vm.runInContext(code,env);
   assert.equal(stats.calls,0);
   return {env,stats,files,windows};
}
const positive=make('positive');
positive.env.runCfaXdrzBatch(binding);
assert.equal(positive.stats.calls,5);
assert.equal(positive.stats.removed.length,10);
assert.deepEqual(positive.windows.map(w=>w.mainView.id),['externally-open']);
assert.deepEqual(JSON.parse(JSON.stringify(positive.stats.processed)),cases.map(c=>c.xdrz));
const events=positive.files.get(root+'/events.txt').trimEnd().split('\n');
assert.deepEqual(events,positive.stats.lines.slice(0,10));
assert.equal(positive.stats.lines.length,11);
const declarations=events.filter(line=>line.startsWith("DSG_CFA_EXPORT ")).map(line=>JSON.parse(line.slice(15)));
assert.equal(declarations.length,5);
assert.ok(declarations.every(row=>row.weightMeaning==="NATIVE_WEIGHT_WINDOW_UNCLASSIFIED" && /^weight_/.test(row.weightWindowId)));
const complete=JSON.parse(positive.files.get(root+'/batch.done.json'));
assert.equal(complete.reservation,reservation);
assert.deepEqual(complete.cases,cases.map(c=>c.id));
assert.equal(complete.scope,'OUTPUT_MARKER_NOT_ADMISSION');
const modes={'no-directory':0,'prior-transcript':0,'prior-product':0,'bad-reservation':0,'foreign-plan':0,'foreign-component':0,
   'third-case-failed':3,'leaked-window':1,'write-failure':2,'damaged-transcript':5};
for(const [mode,expected] of Object.entries(modes)){
   const h=make(mode);
   const observed={...binding};
   if(mode==='foreign-component') observed.componentContractSha256='0'.repeat(64);
   if(mode==='bad-reservation') observed.reservation='../outside';
   if(mode==='foreign-plan') observed.planSha256='0'.repeat(64);
   assert.throws(()=>h.env.runCfaXdrzBatch(observed),undefined,mode);
   assert.equal(h.stats.calls,expected,mode);
   assert.equal(h.files.has(root+'/batch.done.json'),false,mode);
   assert.ok(h.windows.some(w=>w.mainView.id==='externally-open'));
}
const result={schema:'BKL046_CFA_XDRZ_BATCH_CANDIDATE_MOCK_TEST_V1',
   planSha256:binding.planSha256,scriptSha256:pin(code), componentContractSha256:pin(contractRaw), declaredWeightMeaning:contract.weightOutput,observedOrder:complete.cases,
   caseEventCount:events.length,ownedWindowsClosed:positive.stats.removed.length,
   rejectedModes:Object.keys(modes),nativeExecutions:0,scientificClosures:0};
const resultText=JSON.stringify(result,null,2)+'\n';
fs.writeFileSync(out,resultText,{flag:'wx'});
process.stdout.write(JSON.stringify(result)+'\n');
