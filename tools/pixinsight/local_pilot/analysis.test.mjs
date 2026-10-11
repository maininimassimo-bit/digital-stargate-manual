import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';
const source=readFileSync(new URL('./analysis.jsh',import.meta.url),'utf8');
function fixture({changedHistory=false,changedOriginal=false}={}) {
  const hashes={source:'a',copy:'a',measurement:'b',detector:'c'},written=new Map();let closed=0;
  const window={mainView:{historyIndex:0,image:{width:64,height:64,numberOfNominalChannels:1}},forceClose(){++closed;}};
  class File {
    createForWriting(path){assert.equal(written.has(path),false);this.path=path;}
    write(raw){written.set(this.path,raw);}close(){}
  }
  Object.assign(File,{exists:path=>written.has(path),readFile:path=>hashes[path]});
  class CryptographicHash {hash(raw){return {toHex:()=>raw};}}
  CryptographicHash.SHA256=0;
  const context=vm.createContext({File,CryptographicHash,ByteArray:{stringToUTF8:text=>text},
    ImageWindow:{open:()=>[window]},CoreApplication:{versionMajor:1,versionMinor:9,versionRelease:5,versionRevision:0,versionBuild:1706},
    console:{beginLog(){},endLog(){},writeln(){}},
    DSGMeasureNative(){if(changedHistory)window.mainView.historyIndex++;
      if(changedOriginal)hashes.source='changed';return {regions:[[0,0,64,64]]};}});
  vm.runInContext(source,context);
  const manifest={version:'DSG_PIAI_READ_ONLY_ANALYSIS_V2',measurementLibrary:'measurement',measurementSha256:'b',
    starDetectorLibrary:'detector',starDetectorSha256:'c',report:'report',log:'log',
    inputs:[{role:'L',source:'source',copy:'copy',sha256:'a',imageIndex:0,width:64,height:64,channels:1,regions:[[0,0,64,64]]}]};
  return {run:()=>context.DSGAnalyzeMasters(manifest),written,closed:()=>closed};
}
test('records only read-only measurement receipt and closes owned copies',()=>{
  const f=fixture();f.run();const report=JSON.parse(f.written.get('report'));
  assert.equal(report.status,'READ_ONLY_MEASURED');assert.equal(report.scientificAcceptance,'NOT_ESTABLISHED');
  assert.equal(report.measurements[0].report.sourceSha256,'a');assert.equal(f.closed(),1);
  assert.throws(()=>f.run(),/replay refused/);
});
test('history or original changes prevent positive receipt and preserve cleanup',()=>{
  for(const options of [{changedHistory:true},{changedOriginal:true}]){
    const f=fixture(options);assert.throws(()=>f.run(),/preserve originals/);assert.equal(f.written.size,0);assert.equal(f.closed(),1);
  }
});
test('read-only collector has no pixel process execution, eval or network dispatch',()=>{
  assert.doesNotMatch(source,/executeOn|beginProcess|eval\(|XMLHttpRequest|fetch\(/);
});
