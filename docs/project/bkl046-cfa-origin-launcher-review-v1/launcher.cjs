'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const {createHash}=require('node:crypto');
const {spawn,execFile}=require('node:child_process');
const {once}=require('node:events');
const {promisify}=require('node:util');
const {compileFunction}=require('node:vm');
const {dispatchBound, readBound}=require('./dispatcher.cjs');
const {observeOriginal}=require('./supervisore.cjs');
const hash=raw=>createHash('sha256').update(raw).digest('hex');
const exec=promisify(execFile);
const root='K:/DigitalStarGate/pixinsight-coordination-20261114-r1';
const registry=path.join(root,'state');
const operation='BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001';
const deps='O:/BKL046-ACS-WFC-runtime-7.2.0';

async function pinned(file,sha){
  assert.match(sha,/^[0-9a-f]{64}$/);
  const info=await fs.lstat(file);
  assert(info.isFile()&&!info.isSymbolicLink());
  const bytes=await fs.readFile(file);
  assert.equal(hash(bytes),sha,'pinned file changed: '+path.basename(file));
  return bytes;
}
function mapAuthority(relative,subject){
  assert(/^[A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*$/.test(relative)&&
         !relative.split('/').some(p=>p==='.'||p==='..'));
  assert(Object.hasOwn(subject.authoritySha256,relative));
  return path.join(__dirname,relative);
}
async function launch(subject,python){
  assert.equal(subject.operation,operation);
  const source=await pinned(path.join(root,'original-parent-adapter.cjs'),subject.r4['original-parent-adapter.cjs']);
  for(const [name,sha] of Object.entries(subject.r4)){
    await pinned(path.join(root,name),sha);
  }
  for(const [name,sha] of Object.entries(subject.authoritySha256)){
    await pinned(mapAuthority(name,subject),sha);
  }
  const authority={verifier:mapAuthority('autorita/verifica-batch.py',subject),plan:path.join(__dirname,'autorita'),
    oracle:path.join(__dirname,'autorita','oracoli-prova'),
    comparator:mapAuthority('autorita/verifica-v4.py',subject),dependencies:deps};
  const bootstrap=(await pinned(path.join(__dirname,'bootstrap.py'),subject.memberSha256['bootstrap.py'])).toString('utf8');
  const args=['-I','-B','-S','-c',bootstrap,__dirname,JSON.stringify(subject)];
  authority.compareArgs=[...args,'compare'];
  const preflight=await exec(python,[...args,'preflight'],{windowsHide:true,timeout:120000,maxBuffer:65536});
  assert.equal(preflight.stderr,'');
  assert.deepEqual(JSON.parse(preflight.stdout),{comparatorFilesVerified:3824,rootsVerified:true,pixInsightProcesses:0});
  const module={exports:{}};
  let guardian,guardianExit,child,channel;
  compileFunction(source.toString('utf8'),['module','require'],{filename:path.join(root,'original-parent-adapter.cjs')})
    (module,specifier=>{
      if(specifier==='node:path')return path;
      assert.equal(specifier,'node:child_process');
      return {spawn(...argv){
        assert(!guardian);
        guardian=spawn(...argv);
        guardianExit=once(guardian,'close');
        guardianExit.catch(()=>{});
        return guardian;
      }};
    });
  try{
    const owned=await module.exports.startOriginal({identityProtocol:'DSG_PARENT_IDENTITY_FD3_V2',
      python,milestone:'BKL-046',operation,start(){
        child=spawn(python,[...args,'parent'],{windowsHide:true,stdio:['pipe','pipe','pipe','pipe']});
        child.stdin.on('error',()=>{});
        child.stderr.on('data',d=>process.stderr.write(d));
        channel=observeOriginal(child);
        return child;
      }});
    const bound=await readBound(registry,owned);
    return await dispatchBound({owned,channel,python,registry,authority,run:path.join(subject.work,bound.reservation),
      archiveRoot:subject.archive,holdArgs:[...args,'hold']});
  }finally{
    child?.stdin.end();
    guardian?.stdin.end();
    // The parent keeps its input handles while observing the original application.
    await channel?.exit.catch(()=>{});
    await guardianExit?.catch(()=>{});
  }
}
module.exports={launch};
