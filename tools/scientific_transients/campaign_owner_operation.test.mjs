import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';
const canonical=v=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):Array.isArray(v)?v.map(canonical):v;
const digest=async v=>Buffer.from(await webcrypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(canonical(v))))).toString('hex');
function fixture(initial=null){
  const values=new Map(initial===null?[]:[['dsg-campaign-durable-owner-pending-v1',initial]]),calls=[];
  const storage={getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v),removeItem:k=>values.delete(k)};
  const host={storage,canAct:()=>true,canMutate:()=>true,request:async(...args)=>{calls.push(args);return {synthetic:true};}};
  const context=vm.createContext({crypto:webcrypto,TextEncoder,structuredClone});
  vm.runInContext(readFileSync('docs/javascripts/scientific-campaign-owner-operation.js','utf8'),context);
  const controller=context.DSGCampaignOwnerOperation.create(host);
  const selection={action:'DISPATCH_INTENT',planRef:'a'.repeat(32),proposalSha256:'b'.repeat(64),operationKeySha256:'c'.repeat(64),
    relativePath:'/v1/transient-analysis/campaigns/'+'a'.repeat(32)+'/dispatch-intents',request:{synthetic:true}};
  async function envelope(challenge){
    const value={protocol:'DSG_CAMPAIGN_OWNER_DURABLE_OPERATION_V1',action:selection.action,planRef:selection.planRef,
      operationKeySha256:selection.operationKeySha256,challenge,request:selection.request,requestSha256:challenge.requestSha256,
      relativePath:selection.relativePath,launchAuthorized:false,scientificValidation:'NOT_VALIDATED'};
    value.envelopeSha256=await digest(value);return value;
  }
  return {controller,selection,envelope,host,values,calls,context};
}
test('fresh challenge binds exact envelope; pending is retained before one POST',async()=>{
  const f=fixture(),c=await f.controller.prepare(f.selection),e=await f.envelope(c);
  f.host.request=async()=>{assert.equal(f.controller.hasPending(),true);f.calls.push('post');return {};};
  await f.controller.submit(e);assert.equal(f.calls.length,1);assert.equal(f.controller.hasPending(),true);
  await assert.rejects(f.controller.submit(e));assert.equal(f.calls.length,1);
});
test('concurrent double click consumes before first await',async()=>{
  const f=fixture(),e=await f.envelope(await f.controller.prepare(f.selection));
  const first=f.controller.submit(e),second=f.controller.submit(e);
  await assert.rejects(second);await first;assert.equal(f.calls.length,1);
});
test('invalidation during prepare cannot restore stale challenge',async()=>{
  const f=fixture(),p=f.controller.prepare(f.selection);f.controller.invalidate();await assert.rejects(p);
  assert.equal(f.calls.length,0);
});
test('invalidation during envelope hashing prevents POST',async()=>{
  const f=fixture(),e=await f.envelope(await f.controller.prepare(f.selection));
  const p=f.controller.submit(e);f.controller.invalidate();await assert.rejects(p);assert.equal(f.calls.length,0);
});
test('reload with pending record cannot prepare another challenge',async()=>{
  const f=fixture('{}');assert.equal(f.controller.hasPending(),true);await assert.rejects(f.controller.prepare(f.selection));
});
test('changed route with recomputed envelope hash fails closed',async()=>{
  const f=fixture(),e=await f.envelope(await f.controller.prepare(f.selection));e.relativePath+='/wrong';
  const {envelopeSha256,...rest}=e;e.envelopeSha256=await digest(rest);
  await assert.rejects(f.controller.submit(e));assert.equal(f.calls.length,0);
});
test('lost POST response retains pending and forbids replay',async()=>{
  const f=fixture(),e=await f.envelope(await f.controller.prepare(f.selection));
  f.host.request=async()=>{f.calls.push('post');throw Error('synthetic lost response');};
  await assert.rejects(f.controller.submit(e));assert.equal(f.controller.hasPending(),true);
  await assert.rejects(f.controller.prepare(f.selection));assert.equal(f.calls.length,1);
});
test('failed storage readback prevents POST',async()=>{
  const f=fixture(),e=await f.envelope(await f.controller.prepare(f.selection));
  f.host.storage.setItem=()=>{};await assert.rejects(f.controller.submit(e));assert.equal(f.calls.length,0);
});

test('logout while POST is pending ignores response and retains reconciliation record',async()=>{
  const f=fixture(),e=await f.envelope(await f.controller.prepare(f.selection));
  f.host.request=async()=>{f.calls.push('post');f.controller.invalidate();return {synthetic:true};};
  await assert.rejects(f.controller.submit(e));assert.equal(f.controller.hasPending(),true);assert.equal(f.calls.length,1);
});

async function reconcilable(){
  const f=fixture(),e=await f.envelope(await f.controller.prepare(f.selection));await f.controller.submit(e);
  const record=JSON.parse([...f.values.values()][0]);
  const receipt={planRef:record.planRef,operationKeySha256:record.operationKeySha256,requestSha256:record.requestSha256};
  f.context.DSGCampaignOwnerReceipt={intent:async()=>receipt};
  f.host.request=async(path,method)=>{assert.equal(method,undefined);assert.ok(path.endsWith('/review-receipt'));f.calls.push('get');return {};};
  return {...f,receipt};
}
test('read-only reconciliation retains pending until matching saved receipt is reimported',async()=>{
  const f=await reconcilable();
  assert.deepEqual(JSON.parse(JSON.stringify(await f.controller.reconcileIntent({}))),f.receipt);
  assert.equal(f.controller.hasPending(),true);
  await f.controller.reconcileIntent({},f.receipt);assert.equal(f.controller.hasPending(),false);
  assert.equal(f.calls.length,3); // one POST and two fresh GETs
});
test('wrong saved receipt cannot clear pending',async()=>{
  const f=await reconcilable();await assert.rejects(f.controller.reconcileIntent({},{...f.receipt,requestSha256:'f'.repeat(64)}));
  assert.equal(f.controller.hasPending(),true);
});
test('logout during reconciliation preserves pending',async()=>{
  const f=await reconcilable();f.host.request=async()=>{f.controller.invalidate();return {};};
  await assert.rejects(f.controller.reconcileIntent({},f.receipt));assert.equal(f.controller.hasPending(),true);
});
test('reload restores correlation record but never challenge or permission to submit',async()=>{
  const old=await reconcilable(),f=fixture([...old.values.values()][0]);
  f.context.DSGCampaignOwnerReceipt={intent:async()=>old.receipt};f.host.request=async()=>({});
  assert.equal(f.controller.hasPending(),true);
  await assert.rejects(f.controller.submit({}));await assert.rejects(f.controller.prepare(f.selection));
  await f.controller.reconcileIntent({},old.receipt);assert.equal(f.controller.hasPending(),false);
});
