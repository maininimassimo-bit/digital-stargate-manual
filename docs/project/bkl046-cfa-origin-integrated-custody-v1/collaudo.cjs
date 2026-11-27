'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const {spawn,execFile}=require('node:child_process');
const {once}=require('node:events');
const {promisify}=require('node:util');
const {createHash}=require('node:crypto');
const {runInNewContext}=require('node:vm');

const {publish}=require('./archivia.cjs');
const {startCustody}=require('./ingressi.cjs');
const [python, authorities, inputAuthority, barrier, deps, scratch, archiveParent, report]=process.argv.slice(2);
const exec=promisify(execFile);
const sha=raw=>createHash('sha256').update(raw).digest('hex');
const canonical='K:/DigitalStarGate/pixinsight-coordination-20261114-r1';
const operation='BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001';
const fixtureId='348eaf20-c65c-438c-b808-eb1c163f9a31';
const verifier=path.join(authorities,'verifica-batch.py');
async function pinned(file, pin){
  const data=await fs.readFile(file);
  assert.equal(sha(data),pin,file);
  return data;
}
function done(child){
  const received=once(child,'close');
  received.catch(()=>{});
  child.stdin.on('error',()=>{});
  return received;
}
async function test(mode, adapter, archiveRoot, holdDuring){
  const state=await fs.mkdtemp(path.join(scratch,'reg-'));
  const run=path.join(state,'measure');
  const copy=path.join(state,'pinned-inputs');
  await fs.cp(inputAuthority,copy,{recursive:true,errorOnExist:true,force:false});
  const probe=path.join(copy,'fits','shear-a-cfa.fits');
  if(mode==='changed-before-start')await fs.appendFile(probe,'changed');
  const holdArgs=[path.join(inputAuthority,'..','trattieni.py'),path.join(copy,'batch-manifest.json'),
    path.join(copy,'archive_hold.py'),path.join(copy,'xdrz'),path.join(copy,'fits')];
  if(mode==='changed-before-start'){
    await assert.rejects(startCustody(python,holdArgs),/INPUT_CUSTODIAN_FAILED.*MEMBER_DIFFERS/s);
    await assert.rejects(fs.access(path.join(state,'active.json')),{code:'ENOENT'});
    return {mode,parentStarted:false,releaseCalls:0,reservationCreated:false};
  }
  const inputHold=await startCustody(python,holdArgs);
  let custodyLost=false, inputClosed=false;
  async function stopInputs(){
    if(inputClosed)return;
    await inputHold.stop();
    inputClosed=true;
  }
  let supervisor, parent, supervisorExit, parentExit, parentOutput='';
  const fakeRequire=specifier=>{
    if(specifier!=='node:child_process'){
      assert.equal(specifier,'node:path');
      return path;
    }
    return {spawn:(python,cmd,options)=>{
      assert(!supervisor);
      assert.equal(path.normalize(cmd[3]),path.join(__dirname,'custode.py'));
      const args=[...cmd.slice(0,4),scratch,...cmd.slice(4)];
      supervisor=spawn(python,args,{...options,env:{...process.env,DSG_ORIGIN_TEST_STATE:state}});
      supervisorExit=done(supervisor);
      return supervisor;
    }};
  };
  const module={exports:{}};
  runInNewContext(adapter,{module,require:fakeRequire,Buffer,process,setTimeout,clearTimeout});
  try{
    const owned=await module.exports.startOriginal({identityProtocol:'DSG_PARENT_IDENTITY_FD3_V2',
      python,milestone:'BKL-046',operation,start(){
        inputHold.checkAlive();
        parent=spawn(python,['-I','-B','-S',path.join(__dirname,'testimone.py'),state,barrier,mode],
          {windowsHide:true,stdio:['pipe','pipe','pipe','pipe']});
        parentExit=done(parent);
        parent.stdout.on('data',c=>{parentOutput+=c.toString();});
        return parent;
      }});
    const activePath=path.join(state,'active.json');
    const active=await fs.readFile(activePath);
    const acquired=JSON.parse(active);
    const prefix=path.join(state,acquired.reservation);
    const original=await fs.readFile(prefix+'-original.json');
    assert.deepEqual(await fs.readFile(prefix+'-acquired.json'),active);
    assert.equal(acquired.operation,operation);
    assert.equal(owned.child,parent);
    assert.equal(owned.identity.pid,parent.pid);
    await assert.rejects(fs.open(probe,'r+'),{code:'EBUSY'});
    if(mode==='custodian-stops-early'){
      assert.equal(parent.exitCode,null);
      await stopInputs();
      assert.throws(inputHold.checkAlive,/input custodian exited early/);
      custodyLost=true;
    }

    parent.stdin.end(JSON.stringify({reservation:acquired.reservation,acquired:sha(active),original:sha(original)})+'\n');
    const [parentCode,signal]=await parentExit;
    assert.equal(signal,null);
    assert.equal(parentCode,mode==='parent-failed'?7:0);
    assert.deepEqual(JSON.parse(parentOutput),{reservation:acquired.reservation,boundParent:true});

    if(!custodyLost){
      inputHold.checkAlive();
      await assert.rejects(fs.open(probe,'r+'),{code:'EBUSY'});
      await stopInputs();
    }
    const opened=await fs.open(probe,'r+');
    await opened.close();

    await fs.cp(path.join(authorities,'fixture','use-declared'),run,{recursive:true,errorOnExist:true,force:false});
    for(const name of ['events.txt','batch.done.json']){
      const f=path.join(run,name);
      const bytes=await fs.readFile(f,'utf8');
      assert(bytes.includes(fixtureId));
      await fs.writeFile(f,bytes.replaceAll(fixtureId,acquired.reservation));
    }
    if(mode==='bad-transcript'){
      const f=path.join(run,'events.txt');
      const bytes=await fs.readFile(f,'utf8');
      assert(bytes.includes('"dropShrink":0.7'));
      await fs.writeFile(f,bytes.replace('"dropShrink":0.7','"dropShrink":0.65'));
    }
    const auth=path.join(authorities,'autorita');
    if(mode==='unmodeled'){
      for(const name of (await fs.readdir(path.join(run,'outputs')))){
        const kind=name.endsWith('-rgb.fits')?'rgb':'weight';
        await fs.copyFile(path.join(auth,'oracoli-prova','oracoli','baseline-'+kind+'.fits'),path.join(run,'outputs',name));
      }
    }
    const receipt=path.join(run,'receipt.json');
    const verify=()=>exec(python,['-I','-B','-S',verifier,acquired.reservation,auth,
      path.join(auth,'oracoli-prova'),path.join(auth,'verifica-v4.py'),deps,run,receipt],{windowsHide:true,timeout:15000});
    let evidenceStatus=null;
    if(mode==='bad-transcript'){
      await assert.rejects(verify,e=>e.stderr?.includes('SETTINGS_DIFFERS'));
      evidenceStatus='REJECTED_TRANSCRIPT';
    }else{
      await verify();
      const result=JSON.parse(await fs.readFile(receipt));
      assert.equal(result.reservation,acquired.reservation);
      evidenceStatus=result.classification.status;
      assert.equal(evidenceStatus,mode==='unmodeled'?'UNMODELED_SEQUENCE':'MATCHED_TESTED_HYPOTHESIS');
    }
    let releases=0, archiveEntries=0, denyWriteObserved=false;
    async function preserveThenRelease(){
      const archive=await publish({root:archiveRoot,run,acquired:active,original,receipt,
        receiptSha256:sha(await fs.readFile(receipt)),reservation:acquired.reservation});
      archiveEntries=archive.holdEntries.length;
      const archivedLog=path.join(archive.directory,'events.txt');
      if(mode==='archive-changed')await fs.appendFile(archivedLog,'changed');
      await holdDuring(python,archive,async()=>{
        await assert.rejects(fs.open(archivedLog,'r+'),{code:'EBUSY'});
        denyWriteObserved=true;
        assert.deepEqual(await fs.readFile(activePath),active);
        assert.deepEqual(await fs.readFile(prefix+'-original.json'),original);
        releases++;
        assert.equal((await owned.release()).status,'LEASE_RELEASED');
      },['-I','-B','-S',path.join(__dirname,'custodia.py')]);
      const after=await fs.open(archivedLog,'r+');
      await after.close();
    }
    if(!custodyLost && parentCode===0 && evidenceStatus==='MATCHED_TESTED_HYPOTHESIS'){
      if(mode==='archive-collision'){
        const existing=path.join(archiveRoot,acquired.reservation);
        await fs.mkdir(existing);
        await fs.writeFile(path.join(existing,'previous.txt'),'preserved',{flag:'wx'});
        await assert.rejects(preserveThenRelease(),{code:'EEXIST'});
        assert.deepEqual(await fs.readdir(existing),['previous.txt']);
        assert.equal(await fs.readFile(path.join(existing,'previous.txt'),'utf8'),'preserved');
      }else if(mode==='archive-changed'){
        await assert.rejects(preserveThenRelease(),/archive hold readback differs/);
      }else{
        assert.equal(mode,'valid');
        await preserveThenRelease();
      }
    }
    if(mode!=='valid')supervisor.stdin.end();
    const [code,endSignal]=await supervisorExit;
    assert.equal(endSignal,null);
    assert.equal(code,mode==='valid'?0:1);
    assert.deepEqual(await fs.readFile(prefix+'-acquired.json'),active);
    assert.deepEqual(await fs.readFile(prefix+'-original.json'),original);
    if(mode==='valid'){
      const release=JSON.parse(await fs.readFile(prefix+'-released.json'));
      assert.equal(release.parentExitCode,0);
      assert.equal(release.reservation,acquired.reservation);
      await assert.rejects(fs.access(activePath),{code:'ENOENT'});
    }else{
      assert.deepEqual(await fs.readFile(activePath),active);
      await assert.rejects(fs.access(prefix+'-released.json'),{code:'ENOENT'});
    }
    return {mode,parentStarted:true,custodyLost,parentCode,evidenceStatus,releaseCalls:releases,archiveEntries,denyWriteObserved,reservationRetained:mode!=='valid'};
  }finally{
    parent?.stdin.end();
    supervisor?.stdin.end();
    await Promise.allSettled([parentExit,supervisorExit]);
    await stopInputs();
  }
}
async function main(){
  await fs.mkdir(scratch);
  const adapter=await pinned(path.join(canonical,'original-parent-adapter.cjs'),
    '2fe08ef35c126f97b9fce3e382070acf21070ebe8c76fcf5519dc393024464a2');
  const marker="const ENTRY='K:/DigitalStarGate/pixinsight-coordination-20261114-r1/coordinator.py';";
  const code=adapter.toString('utf8');
  assert.equal(code.split(marker).length,2);
  const scratchAdapter=code.replace(marker,'const ENTRY='+JSON.stringify(path.join(__dirname,'custode.py'))+';');
  await pinned(verifier,'1a2036157bb31e4bf7a09408e7bef25051d19ff0e8fe891ab513690f7483aa06');
  await pinned(path.join(inputAuthority,'..','trattieni.py'),'b6f39a2b4dd2e56455d9a0ceaed79a974e17206a77036aceb5b233d0cdc7077b');
  const archiveRoot=await fs.mkdtemp(path.join(archiveParent,'collaudo-origine-custodia-'));
  const holdModule=path.join(path.dirname(barrier),'archive_hold.cjs');
  await pinned(holdModule,'72fc5698d1db62cde879c2e6188940dccbfc5c69220dad43d52c40a37466391d');
  const {holdDuring}=require(holdModule);
  const cases=[];
  for(const mode of ['valid','bad-transcript','unmodeled','parent-failed','archive-collision','archive-changed','custodian-stops-early','changed-before-start']){
    cases.push(await test(mode,scratchAdapter,archiveRoot,holdDuring));
  }
  const r={schema:'BKL046_CFA_ORIGIN_R4_INPUT_ARCHIVE_SCRATCH_V1',cases,adapterSha256:sha(adapter),
    isolatedRegistry:true,nativeOutputsSimulated:true,processInventorySimulated:true,nativeExecutions:0,scientificClosures:0};
  await fs.writeFile(report,JSON.stringify(r,null,2)+'\n',{flag:'wx'});
  console.log(JSON.stringify(r));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
