'use strict';
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');

const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const [parser,runner,data]=process.argv.slice(2);
const source=fs.readFileSync(parser);
assert.equal(sha(source),'4e6bd49fa089c19e4c4688d0e2c11eab96503b7534fb40e9f2873e6e7cd04897');
const expected=JSON.parse(fs.readFileSync(path.join(data,'riscontro.json')));
const names=['compact-shuffled','compact-zones','tailed-shuffled','compact-wide-psf'];
const op='a'.repeat(32),nonce='b'.repeat(32);
const reservation='fd211b22-eace-482b-b353-c88ed80ba6b3';
const root='O:/PJSR-TEST/'+op;
const cols=['Path','FWHMpx','Eccentricity','Noise','Stars','PSFSignalWeight','PSFSNR','SNR','Median','Sigma','MStar'];

function test(mode) {
  const start=Date.parse('2026-11-25T12:00:00.000Z');
  const files=new Map();
  const logs=[];
  let now=start, callCount=0, abortRequested=false;
  const plan={operationRef:op,version:'1.9.6 build 1719',inputRoot:root+'/inputs',
    inputs:names.map(id=>{
      const prior=expected.files.find(row=>row.name===id+'.fits');
      const inputPath=root+'/inputs/'+id+'.fits';
      const raw=fs.readFileSync(path.join(data,prior.name));
      assert.equal(sha(raw),prior.sha256);
      files.set(inputPath,raw);
      return {id,path:inputPath,sha256:prior.sha256,byteLength:prior.bytes};
    })};
  const config=Buffer.from(JSON.stringify({protocol:'BKL046_IMAGEANALYSIS_PJSR_CONFIG_V1',
    operationRef:op,requestNonce:nonce,deadlineUTC:new Date(start+1000).toISOString(),plan}));
  files.set(root+'/runtime-config.json',config);
  files.set(root+'/entry.js',Buffer.from('fixture entry bytes'));
  if(mode==='existing') files.set(root+'/measurements.json',Buffer.from('preserved'));
  const File=class {
    static exists(key){return files.has(key);}
    static writeFile(key,raw){
      assert(!files.has(key),'unexpected overwrite');
      files.set(key,mode==='readback' && key.endsWith('/return.json')?Buffer.from('corrupt'):Buffer.from(raw));
    }
    openForReading(key){this.raw=files.get(key); if(!this.raw)throw Error('Missing '+key);this.isOpen=true;}
    get size(){return this.raw.length;}
    read(_mode,n){const bytes=this.raw.subarray(0,n);bytes.toUint8Array=()=>new Uint8Array(bytes);return bytes;}
    close(){this.isOpen=false;}
  };
  const ImageAnalysis=class {
    executeGlobal(){
      callCount++;
      if(mode==='ackAltered') files.set(root+'/start-ack.json',Buffer.from('altered acknowledgement'));
      this.measurements=this.frames.map(row=>[row[1],3.3,.2,.001,35,12,5,4,.018,.002,.03]);
      return true;
    }
  };
  ImageAnalysis.Task_Measure=1; ImageAnalysis.OnError_Continue=2;
  cols.forEach((name,i)=>ImageAnalysis['measurements_measurement'+name]=i);
  const ctx=vm.createContext({
    File,ImageAnalysis,Uint8Array,ByteArray:{stringToUTF8:value=>Buffer.from(value)},
    CryptographicHash:class {hash(bytes){return {toHex:()=>sha(bytes)};}},
    ElapsedTime:class {get value(){return (now-start)/1000;}},
    Date:class extends Date {static now(){return now;}},
    CoreApplication:{versionMajor:1,versionMinor:9,versionRelease:6,versionBuild:1719},
    ImageWindow:{windows:mode==='windows'?[{}]:[]},
    console:{get abortRequested(){return abortRequested;},writeln:line=>logs.push(line)},
    msleep:millis=>{now+=millis;},
    processEvents(){
      const request=files.get(root+'/start-request.json');
      if(mode==='timeout') return;
      if(mode==='abort'){abortRequested=true;return;}
      const acknowledgement={protocol:'BKL046_IMAGEANALYSIS_START_ACK_V1',operationRef:op,
        requestNonce:nonce,requestSha256:mode==='wrongDigest'?'0'.repeat(64):sha(request),
        reservation,decision:mode==='denied'?'DENIED':'ADMITTED'};
      files.set(root+'/start-ack.json',Buffer.from(JSON.stringify(acknowledgement)));
    },
  });
  for(const code of [source,fs.readFileSync(runner),fs.readFileSync(path.join(__dirname,'ImageAnalysis-adapter.jsh'))])
    vm.runInContext(code.toString(),ctx);
  const negatives={existing:['DIR_NOT_FRESH',0],wrongDigest:['ACK_BINDING',0],denied:['ACK_BINDING',0],
    timeout:['BUDGET',0],abort:['ABORT',0],windows:['NONEMPTY_WORKSPACE',2],readback:['OUTPUT_READBACK',2],
    configHash:['CONFIG_HASH',0],ackAltered:['ACK_CHANGED',2]};
  const run=()=>ctx.DSGRunImageAnalysisControls(root,op,mode==='configHash'?'0'.repeat(64):sha(config));
  if(mode in negatives){
    const [error,count]=negatives[mode];
    assert.throws(run,new RegExp('DSG_IA_ADAPTER_'+error));
    assert.deepEqual(logs,[]);
    assert.equal(callCount,count);
    if(mode==='existing')assert.equal(files.get(root+'/measurements.json').toString(),'preserved');
  }else{
    const receipt=run();
    const result=files.get(root+'/measurements.json');
    const rawReceipt=files.get(root+'/return.json');
    assert.equal(receipt.resultSha256,sha(result));
    assert.equal(receipt.startAckSha256,sha(files.get(root+'/start-ack.json')));
    assert.equal(receipt.reservation,reservation);
    assert.equal(callCount,2);
    assert.equal(logs[0],'DSG_BKL046_IMAGEANALYSIS_RETURNED_V1 '+op+' '+sha(rawReceipt));
  }
}
const denied=['existing','wrongDigest','denied','timeout','abort','windows','readback','configHash','ackAltered'];
test('positive');
for(const mode of denied)test(mode);
console.log(JSON.stringify({nativePjsrSimulated:true,actualFitsFilesReread:4,exactParser:true,
  positive:1,rejected:denied,coordinatorAdmissionRequested:false,scientificClosures:0},null,2));
