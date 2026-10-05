import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {webcrypto} from 'node:crypto';
const source=readFileSync(new URL('../../../docs/javascripts/pixinsight-pilot.js',import.meta.url),'utf8');
const tick=async()=>{for(let i=0;i<12;i++)await new Promise(resolve=>setTimeout(resolve,3));};
function harness({lostCreate=false,denied=false,rejected=false,unknownStatus=false}={}) {
  function node(){return {dataset:{},children:[],callbacks:{},value:'',checked:false,isConnected:true,
    addEventListener(type,callback){this.callbacks[type]=callback;},append(...items){this.children.push(...items);},
    replaceChildren(){this.children=[];},querySelectorAll(){return this.children.flatMap(label=>label.children).filter(x=>x.type==='checkbox'&&x.checked);},
    click(){this.callbacks.click?.();},remove(){}};}
  const controls=Object.fromEntries(['message','connect','signin','form','fields','input','parent','title','date','sessions','attest','create','pending','retry','refresh','jobs','review','summary','preview','steps','workflow','correlations','receipt','accept','reject'].map(name=>[name,node()]));
  controls.title.value='M27 test';controls.date.value='2026-10-05';controls.attest.checked=true;
  const root=node();root.querySelector=selector=>controls[selector.match(/data-p5-(.+)\]/)[1]];
  const stored=new Map(),requests=[];let callback,job,first=lostCreate;
  const google={accounts:{id:{initialize(value){callback=value.callback;},renderButton(){}}}};
  const context={document:{readyState:'complete',querySelector:()=>root,createElement:node,createTextNode:text=>({textContent:text})},
    window:{google},google,crypto:webcrypto,Blob,URL,AbortController,setTimeout,clearTimeout,
    sessionStorage:{getItem:key=>stored.get(key)||null,setItem:(key,value)=>stored.set(key,value),removeItem:key=>stored.delete(key)},
    async fetch(url,options){
      requests.push({url,options});assert.equal(options.redirect,'error');assert.equal(options.credentials,'omit');
      assert.equal(options.headers.Authorization,'Bearer PRIVATE_OWNER_TOKEN');
      if(denied)return {ok:false,status:403,json:async()=>({error:'ACCESS_DENIED'})};
      if(url.endsWith('/options'))return {ok:true,json:async()=>({inputs:[{inputRef:'b'.repeat(32),target:'M27'}],images:[],catalogSha256:'a'.repeat(64),sessions:[{sessionId:'SESSION-M27',target:'M27'}]})};
      if(url.endsWith('/science/jobs')){
        if(options.method==='POST'){
          if(rejected)return {ok:false,status:400,json:async()=>({error:'CATALOG_CHANGED_REFRESH'})};
          const request=JSON.parse(options.body);job ||= {jobId:'PIAI_'+request.requestId,state:'QUEUED',request};
          if(first){first=false;throw new Error('lost response');}
          return {ok:true,json:async()=>job};
        }
        return {ok:true,json:async()=>({jobs:job?[job]:[]})};
      }
      if(url.endsWith('/cancel')){job.state='CANCELLED';return {ok:true,json:async()=>job};}
      if(!job)return {ok:false,status:unknownStatus?503:400,json:async()=>({error:unknownStatus?'UNAVAILABLE':'JOB_NOT_FOUND'})};
      return {ok:true,json:async()=>({job,connection:'OFFLINE',publication:'NONE'})};
    }};
  vm.runInNewContext(source,context);
  return {controls,stored,requests,async login(){controls.connect.click();await tick();callback({credential:'PRIVATE_OWNER_TOKEN'});await tick();
      controls.input.value='b'.repeat(32);controls.sessions.children[0]?.children.forEach(x=>{if(x.type==='checkbox')x.checked=true;});},
    async submit(){controls.form.callbacks.submit({preventDefault(){}});await tick();},async retry(){controls.retry.click();await tick();}};
}
test('Owner scientific request freezes exact selection and sends no code/path/token in storage',async()=>{
  const h=harness();await h.login();await h.submit();
  const posts=h.requests.filter(x=>x.url.endsWith('/science/jobs')&&x.options.method==='POST');
  assert.equal(posts.length,1);const body=JSON.parse(posts[0].options.body);
  assert.deepEqual(body.sessionIds,['SESSION-M27']);assert.equal(body.associationConfirmed,true);
  assert.equal(body.parent,null);assert.equal('script' in body,false);assert.equal('path' in body,false);
  assert.equal(h.stored.size,0);assert.match(h.controls.message.textContent,/conservata/);
  assert.equal(h.requests.some(x=>/worker|decision|commit/.test(x.url)),false);
});
test('lost create response retains exact request and retry cannot duplicate or change it',async()=>{
  const h=harness({lostCreate:true});await h.login();await h.submit();
  assert.equal(h.stored.size,1);assert.equal(h.controls.fields.disabled,true);
  assert.equal([...h.stored.values()].some(x=>x.includes('PRIVATE_OWNER_TOKEN')),false);
  h.controls.title.value='Changed after ambiguous response';await h.retry();
  const posts=h.requests.filter(x=>x.url.endsWith('/science/jobs')&&x.options.method==='POST');
  assert.equal(posts.length,2);assert.equal(posts[0].options.body,posts[1].options.body);
  assert.equal(h.stored.size,0);
});
test('denied authentication does not enable scientific commands',async()=>{
  const h=harness({denied:true});await h.login();
  assert.equal(h.controls.fields.disabled,true);assert.equal(h.controls.refresh.disabled,true);
  assert.equal(h.requests.some(x=>x.options.method==='POST'),false);
  assert.match(h.controls.message.textContent,/Accedi di nuovo/);
});
test('Owner refresh reports offline without automatic cancel/reassignment',async()=>{
  const h=harness();await h.login();await h.submit();
  const text=JSON.stringify(h.controls.jobs.children.map(card=>card.children.map(x=>x.textContent)));
  assert.match(text,/prenotazione conservata/);
  assert.equal(h.requests.some(x=>/cancel/.test(x.url)),false);
});

test('catalog rejection clears frozen request only after verified job absence and reloads options',async()=>{
  const h=harness({rejected:true});await h.login();await h.submit();
  assert.equal(h.stored.size,0);assert.equal(h.controls.fields.disabled,false);
  assert.equal(h.requests.filter(x=>x.url.endsWith('/options')).length,2);
  assert.match(h.controls.message.textContent,/assenza del job verificata/);
});
test('definitive rejection with uncertain job status retains frozen request',async()=>{
  const h=harness({rejected:true,unknownStatus:true});await h.login();await h.submit();
  assert.equal(h.stored.size,1);assert.equal(h.controls.fields.disabled,true);
  assert.equal(h.requests.filter(x=>x.url.endsWith('/options')).length,1);
});
