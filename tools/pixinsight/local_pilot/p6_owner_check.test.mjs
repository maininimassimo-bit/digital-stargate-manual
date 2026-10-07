import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {webcrypto} from 'node:crypto';
const source=readFileSync(new URL('../../../docs/javascripts/pixinsight-pilot-p6-check.js',import.meta.url),'utf8');
const ORIGIN='https://dsg-piai-p6-oat-cfjug35c6q-ew.a.run.app';
function harness({loseCreate=false,loseSecondRecovery=false,healthRequests=0,leakLease=false}={}) {
  const controls=Object.fromEntries(['connect','signin','message','probe','prepare','status','result'].map(name=>[name,{disabled:true,textContent:'',callbacks:{},
    addEventListener(type,callback){this.callbacks[type]=callback;},replaceChildren(){}}]));
  const root={dataset:{},querySelector(selector){return controls[selector.match(/data-p6-(.+)\]/)[1]];}};
  const jobs=new Map(),requests=[];let login,losing=loseCreate,failedSecond=false;
  const google={accounts:{id:{initialize(x){login=x.callback;},renderButton(){}}}};
  const context={document:{readyState:'complete',querySelector:()=>root},window:{google},google,URL,TextEncoder,crypto:webcrypto,AbortController,setTimeout,clearTimeout,
    async fetch(url,options) {
      assert(url.startsWith(ORIGIN+'/'));assert.equal(options.redirect,'error');assert.equal(options.credentials,'omit');requests.push({url,options});
      if(url.endsWith('/health'))return {ok:true,json:async()=>({protocol:'DSG_PIAI_QUEUE_V1',aiMode:'SESSION_ASSISTED',providerRequests:healthRequests})};
      assert.equal(options.headers.Authorization,'Bearer PRIVATE_SYNTHETIC_TOKEN');
      let value;
      if(url.endsWith('/v1/jobs')) {
        const request=JSON.parse(options.body);const id='PIAI_'+request.requestId;
        if(!jobs.has(id))jobs.set(id,{jobId:id,state:'QUEUED',request});value={...jobs.get(id)};
        if(losing){losing=false;throw new Error('deliberate lost response after commit');}
        if(loseSecondRecovery&&jobs.size===2&&!failedSecond){failedSecond=true;throw new Error('second create acknowledgement lost');}
      } else if(url.endsWith('/cancel')) {
        const id=url.split('/').at(-2);jobs.get(id).state='CANCELLED';value={...jobs.get(id)};
      } else {
        const id=url.split('/').at(-1);value={job:{...jobs.get(id)},publication:'NONE',connection:'RECENT_CONTACT'};
      }
      if(leakLease)value.leaseToken='SYNTHETIC_LEASE';
      return {ok:true,json:async()=>value};
    }};
  vm.runInNewContext(source,context);
  return {controls,jobs,requests,async click(name){controls[name].callbacks.click();await new Promise(r=>setTimeout(r,20));},
    async connect(){await this.click('connect');if(login)login({credential:'PRIVATE_SYNTHETIC_TOKEN'});}};
}
test('two client creates/cancels are launched concurrently for the same identity without production or credential output',async()=>{
  const h=harness();await h.connect();await h.click('probe');const result=JSON.parse(h.controls.result.textContent);
  assert.equal(h.jobs.size,1);assert.equal(result.state,'CANCELLED');assert.equal(result.serverInterleavedCasAttested,false);
  assert.equal(h.requests.filter(x=>x.url.endsWith('/v1/jobs')).length,2);
  assert.equal(new Set(h.requests.filter(x=>x.url.endsWith('/v1/jobs')).map(x=>x.options.body)).size,1);
  assert(!h.controls.result.textContent.includes('PRIVATE_SYNTHETIC_TOKEN'));
});
test('committed create with lost response retries same request and never creates another job',async()=>{
  const h=harness({loseCreate:true});await h.connect();await h.click('probe');assert.equal(h.controls.result.textContent,'');
  await h.click('probe');assert.equal(h.jobs.size,1);assert.equal(JSON.parse(h.controls.result.textContent).state,'CANCELLED');
});
test('partial recovery creation retries both immutable requests and preserves two jobs',async()=>{
  const h=harness({loseSecondRecovery:true});await h.connect();await h.click('prepare');assert.equal(h.controls.result.textContent,'');
  await h.click('prepare');assert.equal(h.jobs.size,2);assert.equal(JSON.parse(h.controls.result.textContent).jobs.length,2);
  await h.click('status');assert.equal(JSON.parse(h.controls.result.textContent).jobs.length,2);
  assert.equal(h.requests.filter(x=>x.url.endsWith('/cancel')).length,0);
});
test('health outside approved no-provider session mode blocks authentication and mutations',async()=>{
  const h=harness({healthRequests:1});await h.connect();assert.equal(h.requests.length,1);assert.equal(h.controls.prepare.disabled,true);
});
test('a lease leaked through an Owner response cannot produce a PASS receipt',async()=>{
  const h=harness({leakLease:true});await h.connect();await h.click('probe');assert.equal(h.controls.result.textContent,'');
});
