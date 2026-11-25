'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const {spawn}=require('node:child_process');
const {once}=require('node:events');
const {createHash}=require('node:crypto');
const {runInNewContext}=require('node:vm');
const {observeOriginal}=require('./supervisore.cjs');
const {readBound,dispatchBound}=require('./dispatcher.cjs');
const [python,kit,deps,scratch,h,report]=process.argv.slice(2);
const sha=raw=>createHash('sha256').update(raw).digest('hex');
const op='BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001';
const old='348eaf20-c65c-438c-b808-eb1c163f9a31';
const auth=path.join(kit,'autorita');
const authority={verifier:path.join(kit,'verifica-batch.py'),plan:auth,
  oracle:path.join(auth,'oracoli-prova'),comparator:path.join(auth,'verifica-v4.py'),dependencies:deps};
const listener=process=>{
  process.stdin.on('error',()=>{});
  const stopped=once(process,'close');
  stopped.catch(()=>{});
  return stopped;
};

async function test(mode,entry,archiveRoot){
  const state=await fs.mkdtemp(path.join(scratch,'reg-'));
  let guard,guardExit,parent,parentExit,channel,stderr='';
  const fakeRequire=specifier=>{
    if(specifier!=='node:child_process'){
      assert.equal(specifier,'node:path');
      return path;
    }
    return {spawn:(file,cmd,options)=>{
      assert(!guard);
      const args=[...cmd.slice(0,4),scratch,...cmd.slice(4)];
      guard=spawn(file,args,{...options,env:{...process.env,DSG_ORIGIN_TEST_STATE:state}});
      guardExit=listener(guard);
      return guard;
    }};
  };
  const module={exports:{}};
  runInNewContext(entry,{module,require:fakeRequire,Buffer,process,setTimeout,clearTimeout});
  try{
    const owned=await module.exports.startOriginal({identityProtocol:'DSG_PARENT_IDENTITY_FD3_V2',
      python,milestone:'BKL-046',operation:op,start(){
        parent=spawn(python,['-I','-B','-S',path.join(__dirname,'parent-test.py'),state],
          {windowsHide:true,stdio:['pipe','pipe','pipe','pipe']});
        // Register one close observation, reused during cleanup.
        channel=observeOriginal(parent);
        parentExit=channel.exit;
        parent.stdin.on('error',()=>{});
        parent.stderr.on('data',b=>{stderr+=b.toString();});
        return parent;
      }});
    const bound=await readBound(state,owned);
    const rid=bound.reservation;
    const run=path.join(state,rid);
    await fs.cp(path.join(kit,'fixture','use-declared'),run,{recursive:true,errorOnExist:true,force:false});
    for(const n of ['events.txt','batch.done.json']){
      const file=path.join(run,n);
      const raw=await fs.readFile(file,'utf8');
      assert(raw.includes(old));
      await fs.writeFile(file,raw.replaceAll(old,rid));
    }
    const target=path.join(archiveRoot,rid);
    if(mode==='bad-log'){
      const file=path.join(run,'events.txt');
      const raw=await fs.readFile(file,'utf8');
      await fs.writeFile(file,raw.replace('"dropShrink":0.7','"dropShrink":0.65'));
    }
    if(mode==='archive-collision'){
      await fs.mkdir(target);
      await fs.writeFile(path.join(target,'untouched.txt'),'old',{flag:'wx'});
    }
    let releases=0;
    const observed={...owned,async release(){
      await assert.rejects(fs.open(path.join(target,'window.bmp'),'r+'),{code:'EBUSY'});
      releases++;
      return owned.release();
    }};
    const dispatch=()=>dispatchBound({owned:observed,channel,python,registry:state,run,archiveRoot,
      authority,holdArgs:['-I','-B','-S',path.join(__dirname,'custodia.py')]});
    if(mode==='valid'){
      assert.equal((await dispatch()).status,'LEASE_RELEASED');
      assert.equal(releases,1);
      assert.equal((await fs.readdir(target)).length,17);
      const release=JSON.parse(await fs.readFile(path.join(state,rid+'-released.json')));
      assert.equal(release.reservation,rid);
      assert.equal(release.parentExitCode,0);
      await assert.rejects(fs.access(path.join(state,'active.json')),{code:'ENOENT'});
      assert.deepEqual(await parentExit,[0,null],stderr);
      assert.deepEqual(await guardExit,[0,null]);
    }else{
      await assert.rejects(dispatch, mode==='bad-log' ? /SETTINGS_DIFFERS/ : {code:'EEXIST'});
      assert.equal(releases,0);
      guard.stdin.end();
      await assert.rejects(fs.access(path.join(state,rid+'-released.json')),{code:'ENOENT'});
      assert.deepEqual(await fs.readFile(path.join(state,'active.json')),bound.acquired);
      assert.deepEqual(await guardExit,[1,null]);
      const [code]=await parentExit;
      assert.equal(code,mode==='bad-log'?1:0,stderr);
      if(mode==='archive-collision')assert.deepEqual(await fs.readdir(target),['untouched.txt']);
    }
    return {mode,releases,retained:mode!=='valid'};
  }finally{
    parent?.stdin.end();
    guard?.stdin.end();
    await Promise.allSettled([parentExit,guardExit]);
  }
}
async function main(){
  const source=await fs.readFile('K:/DigitalStarGate/pixinsight-coordination-20261114-r1/original-parent-adapter.cjs');
  assert.equal(sha(source),'2fe08ef35c126f97b9fce3e382070acf21070ebe8c76fcf5519dc393024464a2');
  const text=source.toString('utf8');
  const anchor="const ENTRY='K:/DigitalStarGate/pixinsight-coordination-20261114-r1/coordinator.py';";
  assert.equal(text.split(anchor).length,2);
  const entry=text.replace(anchor,'const ENTRY='+JSON.stringify(path.join(__dirname,'custode.py'))+';');
  await fs.mkdir(scratch);
  const archiveRoot=await fs.mkdtemp(path.join(h,'collaudo-origine-dispatcher-'));
  const tests=[];
  for(const name of ['valid','bad-log','archive-collision'])tests.push(await test(name,entry,archiveRoot));
  const data={schema:'BKL046_CFA_ORIGIN_DISPATCHER_R4_SCRATCH_V1',tests,witnessWindows:true,
    actualComparator:true,installedR4Code:true,isolatedRegistry:true,fixturesNotNative:true,nativeExecutions:0};
  await fs.writeFile(report,JSON.stringify(data,null,2)+'\n',{flag:'wx'});
  console.log(JSON.stringify(data));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
