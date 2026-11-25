'use strict';
const assert=require('node:assert/strict');
const {spawn}=require('node:child_process');
const {once}=require('node:events');
const {createInterface}=require('node:readline');

async function startCustody(python,params){
  const child=spawn(python,['-I','-B','-S',...params],{windowsHide:true,stdio:['pipe','pipe','pipe']});
  child.stdin.on('error',()=>{});
  let diagnostic='';
  child.stderr.on('data',d=>{diagnostic=(diagnostic+d.toString()).slice(-4096);});
  const exit=once(child,'close');
  exit.catch(()=>{});
  const lines=[];
  const reader=createInterface({input:child.stdout,crlfDelay:Infinity});
  reader.on('line',line=>lines.push(line));
  let timer;
  async function close(){
    child.stdin.end();
    const stopTimer=setTimeout(()=>child.kill(),5000);
    try{
      const [code,signal]=await exit;
      return {code,signal,closedLine:lines[1],lineCount:lines.length};
    }finally{
      clearTimeout(stopTimer);
    }
  }
  function checkAlive(){
    assert.equal(child.exitCode,null,'input custodian exited early');
    assert.equal(child.signalCode,null,'input custodian was signaled');
  }
  try{
    const ready=await Promise.race([
      once(reader,'line').then(([line])=>line),
      exit.then(()=>{throw new Error('INPUT_CUSTODIAN_FAILED: '+diagnostic);}),
      new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error('INPUT_CUSTODY_READY_TIMEOUT')),8000);})
    ]);
    assert.deepEqual(JSON.parse(ready),{status:'HELD',xdrz:12,fits:6});
    checkAlive();
    return {checkAlive,async stop(){
      const state=await close();
      assert.deepEqual(state,{code:0,signal:null,closedLine:'{"status": "CLOSED"}',lineCount:2});
    }};
  }catch(error){
    await close();
    throw error;
  }finally{
    clearTimeout(timer);
  }
}
module.exports={startCustody};
