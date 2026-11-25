'use strict';
// Candidate operator only: dependencies supplied by the reviewed launcher.
const assert=require('node:assert/strict');
const {createHash}=require('node:crypto');
const {once}=require('node:events');

const OPERATION='BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001';
const PLAN='ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a';
const SUBJECT='4aa98f614ab6e53c520662659ce91ce1a352b6d78291a20f2dd6cd9e0f0d9b3e';
const IMAGE='76d2339130b58be3d112b66cafc578d9f859d80c96842b2ba2dfbbdcdc8b2943';
const HEX=/^[0-9a-f]{64}$/;
const UUID=/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const digest=bytes=>createHash('sha256').update(bytes).digest('hex');

function exact(record, keys, label){
  assert(record && typeof record==='object' && !Array.isArray(record),label);
  assert.deepEqual(Object.keys(record).sort(),[...keys].sort(),label);
}

async function* records(stdout){
  const bound=65536;
  let pending=Buffer.alloc(0);
  for await(const chunk of stdout.iterator({destroyOnReturn:false})){
    assert(Buffer.isBuffer(chunk),'INVALID_CHILD_STDOUT_CHUNK');
    let cursor=0;
    for(let i=chunk.indexOf(10);i!==-1;i=chunk.indexOf(10,cursor)){
      assert(pending.length+i-cursor<=bound,'EVIDENCE_LINE_TOO_LARGE');
      const frame=Buffer.concat([pending,chunk.subarray(cursor,i)]);
      yield JSON.parse(frame.toString('utf8'));
      pending=Buffer.alloc(0);
      cursor=i+1;
    }
    assert(pending.length+chunk.length-cursor<=bound,'EVIDENCE_LINE_TOO_LARGE');
    pending=Buffer.concat([pending,chunk.subarray(cursor)]);
  }
  assert.equal(pending.length,0,'INCOMPLETE_EVIDENCE_LINE');
}

function observeOriginal(child){
  const exit=once(child,'close');
  exit.catch(()=>{});
  return Object.freeze({child,stdout:child.stdout,pid:child.pid,exit});
}

async function finishCfaOriginal({owned,channel,reservation,findWindow,capture,publish,
  compare,close,verifyFinal,checkpoint}){
  assert(owned.child===channel.child&&channel.child.pid===channel.pid&&
    channel.child.stdout===channel.stdout,'ORIGINAL_PARENT_CHANNEL_CHANGED');
  assert.match(reservation,UUID);
  let context, window, screenshot, comparison, closed, terminal;
  let phase='capture';
  for await(const message of records(channel.stdout)){
    if(phase==='capture'){
      exact(message,['status','context'],'UNEXPECTED_BEGIN_EVENT');
      assert.equal(message.status,'CFA_BATCH_READY_CAPTURE','UNEXPECTED_BEGIN_STATUS');
      context=Object.freeze({...message.context});
      exact(context,['operation','reservation','plan','subject','pid','creationFiletime',
        'imageSha256','entryScriptSha256','batchMarkerSha256'],'INVALID_CFA_CONTEXT');
      assert.equal(context.operation,OPERATION);
      assert.equal(context.reservation,reservation);
      assert.equal(context.plan,PLAN);
      assert.equal(context.subject,SUBJECT);
      assert.equal(context.imageSha256,IMAGE);
      assert(Number.isSafeInteger(context.pid)&&context.pid>0&&context.pid!==channel.pid);
      assert.match(context.creationFiletime,/^[1-9][0-9]{0,19}$/);
      assert.match(context.entryScriptSha256,HEX);
      assert.match(context.batchMarkerSha256,HEX);
      await checkpoint('before-capture',context);
      window=Object.freeze(await findWindow(context));
      exact(window,['pid','creationFiletime','session','hwnd'],'INVALID_CFA_HWND');
      assert.equal(window.pid,context.pid);
      assert.equal(window.creationFiletime,context.creationFiletime);
      assert(Number.isSafeInteger(window.session)&&window.session>0);
      assert.match(window.hwnd,/^[1-9][0-9]{0,19}$/);
      const captureResult=await capture(context,window);
      assert.deepEqual(captureResult.window,window,'CAPTURE_FOREIGN_HWND');
      assert(Buffer.isBuffer(captureResult.bytes)&&captureResult.bytes.length>0,'MISSING_CAPTURE');
      screenshot=digest(captureResult.bytes);
      const saved=await publish('window-capture',captureResult.bytes,context);
      assert.equal(saved.sha256,screenshot,'CAPTURE_READBACK_DIFFERS');
      const scored=await compare(context);
      assert(scored.verified===true&&scored.reservation===reservation&&
             scored.batchMarkerSha256===context.batchMarkerSha256,'CFA_OUTPUTS_NOT_VERIFIED');
      assert.match(scored.receiptSha256,HEX);
      comparison=scored.receiptSha256;
      phase='close';
    }else if(phase==='close'){
      exact(message,['status','context','captureSha256','comparisonSha256'],'UNEXPECTED_ARM_EVENT');
      assert.equal(message.status,'CFA_CLOSE_ARMED','UNEXPECTED_ARM_STATUS');
      assert.deepEqual(message.context,context,'ARM_CONTEXT_CHANGED');
      assert.equal(message.captureSha256,screenshot,'ARM_CAPTURE_CHANGED');
      assert.equal(message.comparisonSha256,comparison,'ARM_COMPARISON_CHANGED');
      await checkpoint('before-close',context);
      assert.deepEqual(await findWindow(context),window,'ARM_WINDOW_CHANGED');
      const closeResult=await close(context,window);
      assert.deepEqual(closeResult.window,window,'CLOSE_FOREIGN_HWND');
      assert(closeResult.requested===true&&Buffer.isBuffer(closeResult.bytes)&&
             closeResult.bytes.length>0,'NORMAL_CLOSE_RECEIPT_MISSING');
      closed=digest(closeResult.bytes);
      const saved=await publish('normal-close',closeResult.bytes,context);
      assert.equal(saved.sha256,closed,'CLOSE_READBACK_DIFFERS');
      phase='finish';
    }else if(phase==='finish'){
      exact(message,['status','context','nativeExitCode','scientificClosures'],'UNEXPECTED_TERMINAL_EVENT');
      assert.equal(message.status,'CFA_NATIVE_EXIT_OBSERVED','UNEXPECTED_TERMINAL_STATUS');
      assert.deepEqual(message.context,context,'TERMINAL_CONTEXT_CHANGED');
      assert.equal(message.nativeExitCode,0,'ORIGINAL_PIXINSIGHT_EXIT_NONZERO');
      assert.equal(message.scientificClosures,0,'UNSUPPORTED_SCIENCE_CLAIM');
      terminal=message;
      phase='eof';
    }else{
      throw Error('EXTRA_PARENT_EVENT');
    }
  }
  assert.equal(phase,'eof','MISSING_ORIGINAL_PARENT_EVIDENCE');
  const [code,signal]=await channel.exit;
  assert(code===0&&signal===null&&owned.child===channel.child&&
         channel.child.pid===channel.pid&&channel.child.stdout===channel.stdout,'ORIGINAL_PARENT_DID_NOT_EXIT_ZERO');
  const final=await verifyFinal(context,{screenshot,comparison,closed,terminal});
  assert(final.verified===true&&final.reservation===reservation&&final.originalWindowClosed===true&&
         final.originalNativeExitCode===0&&final.outputsReadBack===true,'FINAL_EVIDENCE_NOT_VERIFIED');
  await checkpoint('before-release',context);
  const result=await owned.release();
  assert.equal(result.status,'LEASE_RELEASED');
  return {status:result.status,reservation,scientificClosures:0};
}

module.exports={observeOriginal,finishCfaOriginal};
