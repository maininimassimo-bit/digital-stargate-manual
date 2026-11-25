'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const path = require('node:path');
const vm = require('node:vm');

const installed = process.argv[2] || 'C:/Program Files/PixInsight';
const script = path.join(installed, 'src/scripts/BatchPreprocessing/BPP-SubframeAnalyzer.js');
const cache = path.join(installed, 'src/scripts/BatchPreprocessing/BPP-ExecutionCache.js');
const moduleFile = path.join(installed, 'bin/ImageAnalysis-pxm.dll');
const pins = [
  [script,'2e238f66ec3e0aa31cb791b1be9190ce55e8321f6d8023694b289f10c33d4620'],
  [cache,'324e6df1c7430f16c2849fccba483b2e003046e9cfe770a595e559250ce2edc9'],
  [moduleFile,'fd421a2d4abe392a72ca9fd02c365716c202aaf3df8a61eabc7a8214893d16bc'],
];
for (const [file,digest] of pins) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),digest);
}
function method(file, signature) {
  const source=fs.readFileSync(file,'utf8').replace(/\r\n/g,'\n');
  const start=source.indexOf('\n   '+signature+'\n');
  const end=source.indexOf('\n   }\n',start)+5;
  assert(start>=0 && end>start);
  return source.slice(start,end).trim();
}
const columns=['Path','FWHMpx','Eccentricity','Noise','Stars','PSFSignalWeight','PSFSNR','SNR','Median','Sigma','MStar'];
const goodRow=(image) => [image,2.3,.4,.012,40,12,9,2,.14,.04,.18];
let rows,success,settings,executeCount,lastInstance;
class ImageAnalysis {
  constructor() { lastInstance=this; }
  toSource() { return JSON.stringify([this.task,this.onError,this.fileCache,this.extendedMeasurements,settings]); }
  executeGlobal() { executeCount++; this.executed=true; return success; }
  get measurements() { return this.executed ? rows : []; }
}
Object.assign(ImageAnalysis,{Task_Measure:1,OnError_Continue:2});
columns.forEach((name,index) => ImageAnalysis['measurements_measurement'+name]=index);
const empty=()=>{};
const log={writeln:empty,noteln:empty,warningln:empty,flush:empty};
const dateByPath=new Map();
const context={
  ImageAnalysis, BPP:{Constants:{CACHE_VERSION:'cache_v3'}}, console:log,
  WBPPUtils:{enableTargetFrames:(paths)=>paths.map(image=>[true,image]),
             paddedStringNumber:(value)=>value,getLastModifiedDate:(file)=>dateByPath.get(file)},
  CoreApplication:{processEvents:empty}, format:()=>'', File:{extractNameAndExtension:path.basename},
};
const readMethod=(file,signature)=>{
  return vm.runInNewContext('({'+method(file,signature)+'}).'+signature.split('(')[0].trim(),context);
};
const compute=readMethod(script,'computeDescriptors( fileItems )');
const unmodified=readMethod(cache,'isFileUnmodified( key, filePath )');
const cacheByKey=new Map(), stamp=new Map();
const engine={
  executionCache:{
    keyFor:key=>crypto.createHash('sha1').update(key).digest('hex'),
    hasCacheForKey:key=>cacheByKey.has(key), cacheForKey:key=>cacheByKey.get(key),
    isFileUnmodified:unmodified, _lmdPrefix:'time:',
    _get:key=>stamp.get(key), _log:empty,
    cacheFileLMD(key,file){ stamp.set(this._lmdPrefix+key+file,dateByPath.get(file)); },
    setCache(key,value){ cacheByKey.set(key,value); },
  },
  processContainer:{add:empty},processLogger:{addWarning:empty},
};
function run(files, returned, {ok=true, configuration='default'}={}) {
  rows=returned; success=ok; settings=configuration; executeCount=0;
  const items=files.map(current=>({current,setDescriptor(d){this.d=d;}, processingFailed(_,why){this.error=why;}}));
  const counts=JSON.parse(JSON.stringify(compute.call({engine},items)));
  return {counts,reportedFailures:items.filter(x=>x.error).map(x=>x.current),
          measurements:items.map(x=>x.d||null),executes:executeCount};
}

dateByPath.set('A','2026-11-25T15:00');
const measured=run(['A'],[goodRow('A')]);
assert.equal(measured.measurements[0].mad,.04);
assert.equal(measured.measurements[0].noise,.012);
assert.equal(lastInstance.task,ImageAnalysis.Task_Measure);
assert.equal(lastInstance.onError,ImageAnalysis.OnError_Continue);
assert.equal(lastInstance.extendedMeasurements,false);
assert.equal(lastInstance.fileCache,true);
let changed=goodRow('A'); changed[1]=9;
const sameStamp=run(['A'],[changed]);
assert.equal(sameStamp.executes,0);
assert.equal(sameStamp.measurements[0].FWHM,2.3);
dateByPath.set('A','2026-11-25T15:02');
const newStamp=run(['A'],[changed]);
assert.equal(newStamp.executes,1);
assert.equal(newStamp.measurements[0].FWHM,9);
const newConfig=run(['A'],[goodRow('A')],{configuration:'other'});
assert.equal(newConfig.executes,1);

const missing=run(['absent'],[]);
assert.deepEqual(missing.counts,{nCached:0,nMeasured:0,nFailed:0});
assert.deepEqual(missing.reportedFailures,['absent']);
const duplicate=run(['repeat'],[goodRow('repeat'),goodRow('repeat')]);
assert.equal(duplicate.counts.nMeasured,2);
assert.equal(duplicate.measurements.length,1);
const unknown=run(['expected'],[goodRow('unknown')]);
assert.equal(unknown.counts.nFailed,1);
assert.deepEqual(unknown.reportedFailures,['expected']);
const invalid=goodRow('nonfinite-noise'); invalid[3]=NaN;
const uncheckedNoise=run(['nonfinite-noise'],[invalid]);
assert.equal(uncheckedNoise.counts.nMeasured,1);
assert.equal(uncheckedNoise.reportedFailures.length,0);
assert.equal(Number.isNaN(uncheckedNoise.measurements[0].noise),true);
const rejected=run(['execution-fails'],[goodRow('execution-fails')],{ok:false});
assert.equal(rejected.counts.nFailed,1);
assert.deepEqual(rejected.reportedFailures,['execution-fails']);

console.log(JSON.stringify({
  protocol:'BKL046_WBPP_IMAGEANALYSIS_WRAPPER_V1',target:'PixInsight 1.9.6 build 1719 / WBPP 3.2.2',
  sources:pins.map(([file, sha256])=>({file:path.basename(file),sha256})),
  methodSimulation:'Exact installed methods with mock native ImageAnalysis, frame paths, and timestamps',
  mapping:{madSource:'measurements_measurementSigma',sampleMad:measured.measurements[0].mad,
           noiseSource:'measurements_measurementNoise',nonfiniteNoiseAccepted:true},
  cache:{sameTimestampReused:sameStamp.counts.nCached,changedTimestampRemeasured:newStamp.executes,
         changedSettingsRemeasured:newConfig.executes},
  bookkeeping:{absentRow:missing.counts,absentFrameMarkedFailed:true,mockDuplicateRowsMeasured:duplicate.counts.nMeasured,
               mockUnknownRowFailed:unknown.counts.nFailed,globalFailureCount:rejected.counts.nFailed},
  nativeExecutions:0,scientificClosures:0
},null,2));
