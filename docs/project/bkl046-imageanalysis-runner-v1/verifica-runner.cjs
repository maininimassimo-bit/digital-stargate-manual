'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const crypto=require('node:crypto');

const controls=process.argv[2];
const WBPP=process.argv[3] || 'C:/Program Files/PixInsight/src/scripts/BatchPreprocessing';
const helper=fs.readFileSync(path.join(WBPP,'BPP-helper.js'));
assert.equal(crypto.createHash('sha256').update(helper).digest('hex'),
             '8578aeae1173cb94b5362acfba121b826cd78db69dae6f0757276064f9728ef7');
const expected=JSON.parse(fs.readFileSync(path.join(controls,'riscontro.json')));
const code=fs.readFileSync(path.join(__dirname,'ImageAnalysis-controls.jsh'),'utf8');
const context=vm.createContext({});
vm.runInContext(code,context);
const source=helper.toString('utf8').replace(/\r\n/g,'\n');
const start=source.indexOf('   enableTargetFrames: function(');
const end=source.indexOf('\n   },',start)+5;
assert(start>0 && end>start);
const WBPPFrames=vm.runInNewContext('({'+source.slice(start,end)+'}).enableTargetFrames');
const clean=value=>JSON.parse(JSON.stringify(value));

const order=['compact-shuffled','compact-zones','tailed-shuffled','compact-wide-psf'];
const inputRoot=controls.replace(/\\/g,'/');
const plan={inputRoot,operationRef:'8'.repeat(32),version:'1.9.6 build 1719',
  inputs:order.map(id=>{
    const row=expected.files.find(record=>record.name===id+'.fits');
    return {id,path:inputRoot+'/'+row.name,sha256:row.sha256,byteLength:row.bytes};
  })};
const names=['Path','FWHMpx','Eccentricity','Noise','Stars','PSFSignalWeight','PSFSNR','SNR','Median','Sigma','MStar'];
function setup(mode) {
  let executions=0;
  class Fake {
    executeGlobal() {
      executions++;
      assert.equal(this.fileCache,false);
      assert.equal(this.extendedMeasurements,false);
      assert.equal(this.task,Fake.Task_Measure);
      assert.equal(this.onError,Fake.OnError_Continue);
      const paths=this.frames.map(row=>row[1]);
      assert.deepEqual(clean(this.frames),clean(WBPPFrames(paths,2)));
      this.measurements=paths.slice().reverse().map(file=>{
        const expectedRow=expected.files.find(row=>file.endsWith('/'+row.name));
        return [file.replace(/\//g,'\\'),expectedRow.gaussianFwhmPixels,.2,.001,36,12,5,4,.018,.002,.03];
      });
      if(mode==='missing') this.measurements.pop();
      if(mode==='duplicate') this.measurements[0]=this.measurements[1];
      if(mode==='foreign') this.measurements[0][0]='C:/other/alien.fits';
      if(mode==='badNoise') this.measurements[0][3]=null;
      if(mode==='invalidStars') this.measurements[0][4]=40.5;
      if(mode==='orderSensitive' && executions===2) this.measurements[0][1]+=.5;
      return mode!=='executionFailure';
    }
  }
  Fake.Task_Measure=1;
  Fake.OnError_Continue=2;
  names.forEach((name,i)=>Fake['measurements_measurement'+name]=i);
  if(mode==='missingColumn') delete Fake.measurements_measurementSigma;
  const host={ImageAnalysis:Fake,currentVersion:()=>plan.version,guard:()=>{},
    fingerprint(file){
      const raw=fs.readFileSync(file);
      const sha=crypto.createHash('sha256').update(raw).digest('hex');
      return {sha256:(mode==='postExecutionChanged' && executions>0)?'0'.repeat(64):sha,byteLength:raw.length};
    }};
  return {host,executions:()=>executions};
}
const equal=setup();
const first=clean(context.DSGImageAnalysisControls(plan,equal.host));
assert.equal(equal.executions(),2);
assert.deepEqual(first.forward.inputOrder,order);
assert.deepEqual(first.reverse.inputOrder,order.slice().reverse());
assert(first.deltas.every(row=>Object.values(row.byMetric).every(x=>x===0)));
const changed=setup('orderSensitive');
const second=clean(context.DSGImageAnalysisControls(plan,changed.host));
assert.equal(second.deltas[0].byMetric.fwhmPx,.5);
assert.equal(second.scientificAcceptance,false);
const negatives={
  missing:/ROW_COUNT/,duplicate:/ROW_IDENTITY/,foreign:/ROW_IDENTITY/,badNoise:/MEASUREMENT_VALUES/,
  invalidStars:/MEASUREMENT_VALUES/,executionFailure:/MEASUREMENT_FAILED/,
  missingColumn:/MISSING_OR_AMBIGUOUS_COLUMN/,postExecutionChanged:/INPUT_CHANGED/
};
for(const [mode,error] of Object.entries(negatives)) {
  assert.throws(()=>context.DSGImageAnalysisControls(plan,setup(mode).host),error);
}
console.log(JSON.stringify({protocol:'BKL046_IMAGEANALYSIS_RUNNER_OFFLINE_V1',
  fitsBytesRead:plan.inputs.map(row=>({id:row.id,sha256:row.sha256,bytes:row.byteLength})),
  exactWbppFourColumnHelper:true,orderIndependentControl:true,injectedOrderSensitivityPx:.5,
  rejected:Object.keys(negatives),nativeObjectsMocked:true,scientificClosures:0},null,2));
