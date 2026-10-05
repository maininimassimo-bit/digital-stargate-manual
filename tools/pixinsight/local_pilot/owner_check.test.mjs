import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {webcrypto} from 'node:crypto';
const source = readFileSync(new URL('../../../docs/javascripts/pixinsight-pilot-check.js', import.meta.url), 'utf8');
const ORIGIN = 'https://dsg-pixinsight-pilot-183451329061.europe-west1.run.app';
const tick = async () => { for (let i=0;i<10;i++) await new Promise(resolve => setTimeout(resolve, 5)); };
function harness({failCancel=false}={}) {
  const controls = Object.fromEntries(['origin','connect','signin','message','probe','result'].map(name=>[name, {
    value: ORIGIN, disabled: name==='probe', textContent:'', callbacks:{},
    addEventListener(type, callback){this.callbacks[type]=callback;}, replaceChildren(){}
  }]));
  const root={dataset:{},querySelector(selector){return controls[selector.match(/data-piai-(.+)\]/)[1]];}};
  const requests=[]; let signIn, job, firstCancel=failCancel;
  const google={accounts:{id:{initialize(value){signIn=value.callback;},renderButton(){}}}};
  const context={document:{readyState:'complete',querySelector:()=>root},window:{google},google,
    URL,TextEncoder,crypto:webcrypto,AbortController,setTimeout,clearTimeout,
    async fetch(url, options){
      requests.push({url,options});
      assert.equal(options.redirect,'error'); assert.equal(options.credentials,'omit');
      if(url.endsWith('/health'))return {ok:true,json:async()=>({protocol:'DSG_PIAI_QUEUE_V1',aiMode:'SESSION_ASSISTED',providerRequests:0})};
      assert.equal(options.headers.Authorization,'Bearer PRIVATE_TEST_TOKEN');
      if(url.endsWith('/cancel')){
        if(firstCancel){firstCancel=false;throw new Error('lost response');}
        job.state='CANCELLED';return {ok:true,json:async()=>({...job})};
      }
      if(options.method==='POST'){const request=JSON.parse(options.body);job ||= {jobId:'PIAI_'+request.requestId,state:'QUEUED',request};return {ok:true,json:async()=>({...job})};}
      return {ok:true,json:async()=>({job:{...job},publication:'NONE',executionEvidence:'WORKER_REPORTED_NOT_ATTESTED'})};
    }};
  vm.runInNewContext(source,context);
  return {controls,requests,async connect(){controls.connect.callbacks.click();await tick();},
    login(){signIn({credential:'PRIVATE_TEST_TOKEN'});},async probe(){controls.probe.callbacks.click();await tick();}};
}
test('credential stays in memory and synthetic Owner probe cancels before native',async()=>{
  const h=harness();await h.connect();h.login();await h.probe();
  assert.equal(JSON.parse(h.controls.result.textContent).state,'CANCELLED');
  assert.equal(h.requests.length,5);
  assert.equal(h.requests[0].options.headers.Authorization,undefined);
  assert(!h.controls.result.textContent.includes('PRIVATE_TEST_TOKEN'));
  assert.equal(h.controls.origin.disabled,true);
});
test('another valid run.app host receives no request or Google credential',async()=>{
  const h=harness();h.controls.origin.value='https://attacker.run.app';await h.connect();
  assert.equal(h.requests.length,0);assert.equal(h.controls.probe.disabled,true);
});
test('userinfo, query, non-TLS, path and port origins are refused',async()=>{
  for(const origin of ['http://example.run.app','https://user@example.run.app','https://example.run.app/path','https://example.run.app?q=1','https://example.run.app:444']){
    const h=harness();h.controls.origin.value=origin;await h.connect();assert.equal(h.requests.length,0);
  }
});
test('lost cancellation retries same opaque request and does not create a second job',async()=>{
  const h=harness({failCancel:true});await h.connect();h.login();await h.probe();
  assert.equal(h.controls.result.textContent,'');await h.probe();
  const creates=h.requests.filter(r=>r.url.endsWith('/v1/jobs'));
  assert.equal(creates.length,4);assert.equal(new Set(creates.map(r=>r.options.body)).size,1);
  assert.equal(JSON.parse(h.controls.result.textContent).cancelBeforeNative,'PASS');
});
