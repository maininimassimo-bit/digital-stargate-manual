import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';

const key='dsg-bkl051-campaign-pending-v1';
const generated=spawnSync('python',['-c',[
  'import json,datetime as dt',
  'from tools.scientific_transients.test_confirmatory_campaign import CampaignTests,ref',
  'f=CampaignTests();f.setUp()',
  'for i in range(59):f.review(i)',
  'draft=f.service.review_receipt(ref(10));request=f.freeze_request()',
  'f.service.freeze(ref(10),request);frozen=f.service.review_receipt(ref(10))',
  'f.now+=dt.timedelta(seconds=1);f.completed(0);partial=f.service.review_receipt(ref(10))',
  "def action(kind,body,witness=None):return {'schema':'BKL051_OWNER_CAMPAIGN_ACTION_V1','action':kind,'planRef':ref(10),'witnessRef':witness,'request':body}",
  'row=f.service.input_view(ref(100))',
  "print(json.dumps({'draft':draft,'frozen':frozen,'partial':partial,'freeze':action('FREEZE',request),'create':action('CREATE',f.request),'input':row,'inputAction':action('INPUT_REVIEW',row['review']['request'],ref(100))}))"
].join('\n')],{encoding:'utf8',maxBuffer:1024*1024,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(generated.status,0,generated.stderr);const fixtures=JSON.parse(generated.stdout);

function node(tag='div'){
  return {tag,children:[],textContent:'',disabled:false,value:'',checked:false,files:[],isConnected:true,callbacks:{},
    append(...items){this.children.push(...items);},replaceChildren(){this.children=[];},setAttribute(){},
    addEventListener(type,callback){this.callbacks[type]=callback;},
    async click(){if(!this.disabled)return this.callbacks.click?.();}};
}
function harness({storage=new Map(),initial=fixtures.draft,postFailure='',storageFail=false,dispatchAdapter=null}={}){
  const controls=Object.fromEntries(['refresh','select','open','file','confirmed','send','retry','pending','status','preview','result'].map(k=>[k,node()]));
  if(dispatchAdapter)controls.dispatch=node();
  const root=node();root.querySelector=s=>controls[s.match(/data-campaign-(.+)\]/)[1]];
  let authorized=false,busy=false,queueBlocked=false,expired=false,module,current=structuredClone(initial),deferred=null;
  const requests=[];
  const context=vm.createContext({...(dispatchAdapter?{DSGCampaignDispatchOwner:dispatchAdapter}:{}),crypto:webcrypto,TextEncoder,structuredClone,document:{createElement:node},sessionStorage:{
    getItem:k=>storage.get(k)??null,
    setItem(k,v){if(storageFail)throw Error('PRIVATE_STORAGE_FAILURE');assert.equal(v.includes('Bearer'),false);storage.set(k,v);},
    removeItem(k){if(storageFail)throw Error('PRIVATE_STORAGE_FAILURE');storage.delete(k);}
  }});
  for(const file of ['scientific-campaign-contract','scientific-campaign-owner'])
    vm.runInContext(readFileSync('docs/javascripts/'+file+'.js','utf8'),context);
  const update=()=>module?.update({authorized,busy,queueBlocked});
  const host={changed:update,canMutate:()=>authorized&&!expired&&!queueBlocked,
    canAct(){if(expired){authorized=false;update();}return authorized;},
    async run(fn){if(busy)return;busy=true;update();try{await fn();}finally{busy=false;update();}},
    async request(path,method='GET',body){
      requests.push({path,method,body:structuredClone(body)});assert.ok(authorized);
      assert.match(path,/^\/campaigns(?:\/inputs\/[a-f0-9]{32}(?:\/review)?|\/[a-f0-9]{32}(?:\/(?:freeze|review-receipt))?)?$/);
      if(deferred?.path===path){const waiting=deferred;deferred=null;await waiting.promise;}
      if(method==='POST'){
        if(postFailure==='before')throw Error('PRIVATE_LOST_ACK');
        if(path==='/campaigns')current=structuredClone(fixtures.draft);
        else if(path.endsWith('/freeze'))current=structuredClone(fixtures.frozen);
        else assert.ok(path.endsWith('/review'));
        if(postFailure==='after')throw Error('PRIVATE_LOST_ACK');
        return {};
      }
      if(path==='/campaigns')return current===false?null:{campaigns:current?[structuredClone(current.campaign)]:[]};
      if(path.includes('/inputs/'))return structuredClone(fixtures.input);
      assert.ok(path.endsWith('/review-receipt'));return structuredClone(current);
    }};
  module=context.DSGCampaignOwner.mount(root,host);update();
  return {controls,requests,storage,module,
    login(){authorized=true;update();},logout(){authorized=false;update();},expire(){expired=true;},
    setQueueBlocked(value){queueBlocked=value;update();},setCurrent(value){current=structuredClone(value);},setPostFailure(value){postFailure=value;},
    async refresh(){await controls.refresh.click();},
    async open(){controls.select.value=fixtures.draft.plan.planRef;controls.select.callbacks.change();await controls.open.click();},
    async load(value=fixtures.freeze){const text=JSON.stringify(value);controls.file.files=[{size:Buffer.byteLength(text),text:async()=>text}];await controls.file.callbacks.change();},
    confirm(){controls.confirmed.checked=true;controls.confirmed.callbacks.change();},
    defer(path){let release;const promise=new Promise(r=>release=r);deferred={path,promise};return release;}
  };
}
const text=n=>n.textContent+n.children.map(text).join(' ');
const posts=h=>h.requests.filter(r=>r.method==='POST');
async function prepared(options){const h=harness(options);h.login();await h.refresh();await h.open();await h.load();h.confirm();return h;}

test('initialization/login do not read or write; private controls require Owner action',()=>{
  const h=harness();assert.equal(h.controls.refresh.disabled,true);assert.equal(h.requests.length,0);
  h.login();assert.equal(h.controls.refresh.disabled,false);assert.equal(h.requests.length,0);assert.equal(h.controls.send.disabled,true);
});
test('actual authenticated draft renders all59 cases without statistical promotion',async()=>{
  const h=harness();h.login();await h.refresh();await h.open();
  assert.match(text(h.controls.result),/Controlli qualificati nel piano: 0/);
  const table=h.controls.result.children.find(n=>n.tag==='div').children[0];
  assert.equal(table.children[1].children.length,59);assert.equal(posts(h).length,0);
});
test('partial result shows exact private science/report proofs without full-plan acceptance',async()=>{
  const h=harness({initial:fixtures.partial});h.login();await h.refresh();await h.open();const rendered=text(h.controls.result);
  assert.ok(rendered.includes(fixtures.partial.executions[0].request.scienceEvidenceSha256));
  assert.ok(rendered.includes(fixtures.partial.executions[0].sha256));
  assert.match(rendered,/Controlli qualificati nel piano: 1/);assert.match(rendered,/Risultato statistico non disponibile/);
});
test('explicit freeze is persisted before POST and cleared only after exact receipt',async()=>{
  const h=await prepared();assert.equal(h.controls.send.disabled,false);await h.controls.send.click();
  assert.equal(posts(h).length,1);assert.deepEqual(posts(h)[0].body,fixtures.freeze.request);
  assert.equal(h.storage.size,0);assert.equal(h.module.hasPending(),false);
  assert.match(text(h.controls.result),/Controlli qualificati nel piano: 0/);
});
test('lost successful acknowledgement survives logout and reconciles without second POST',async()=>{
  const h=await prepared({postFailure:'after'});await h.controls.send.click();assert.equal(h.storage.size,1);
  const retained=[...h.storage];h.logout();assert.equal(h.controls.result.children.length,0);assert.deepEqual([...h.storage],retained);
  const restored=harness({storage:h.storage,initial:fixtures.frozen});restored.login();assert.equal(restored.requests.length,0);
  await restored.refresh();assert.equal(restored.storage.size,0);assert.equal(posts(restored).length,0);
});
test('unobserved metadata request retries only exact body after manual read and confirmation',async()=>{
  const h=await prepared({postFailure:'before'});await h.controls.send.click();assert.equal(posts(h).length,1);
  await h.refresh();assert.equal(posts(h).length,1);assert.equal(h.controls.retry.disabled,true);
  h.confirm();assert.equal(h.controls.retry.disabled,false);h.setPostFailure('');await h.controls.retry.click();
  assert.equal(posts(h).length,2);assert.deepEqual(posts(h)[0].body,posts(h)[1].body);assert.equal(h.storage.size,0);
});
test('expired Owner access cannot persist or send a new decision',async()=>{
  const h=await prepared();h.expire();await h.controls.send.click();
  assert.equal(posts(h).length,0);assert.equal(h.storage.size,0);assert.equal(h.controls.result.children.length,0);
});
test('pending queue command blocks campaign mutation while allowing private reads',async()=>{
  const h=await prepared();h.setQueueBlocked(true);assert.equal(h.controls.send.disabled,true);
  await h.controls.send.callbacks.click();assert.equal(posts(h).length,0);assert.equal(h.storage.size,0);
});
test('unverifiable persisted action blocks commands and is preserved',async()=>{
  const storage=new Map([[key,'{"authority":"forged"}']]),h=harness({storage});h.login();await h.refresh();
  assert.equal(h.module.hasPending(),true);assert.equal(h.controls.file.disabled,true);assert.equal(storage.size,1);assert.equal(posts(h).length,0);
});
test('storage failure prevents POST and blocks both metadata and job mutation',async()=>{
  const h=await prepared({storageFail:true});await h.controls.send.click();
  assert.equal(posts(h).length,0);assert.equal(h.module.hasPending(),true);assert.equal(h.controls.send.disabled,true);
});
test('changed retained action blocks reconciliation and never resends automatically',async()=>{
  const h=await prepared({postFailure:'before'});await h.controls.send.click();h.storage.set(key,JSON.stringify(fixtures.create));
  await h.refresh();assert.equal(h.controls.retry.disabled,true);assert.equal(posts(h).length,1);assert.equal(h.controls.result.children.length,0);
});
test('unavailable registry is not proof that a pending command did not commit',async()=>{
  const h=await prepared({postFailure:'before'});await h.controls.send.click();h.setCurrent(false);await h.refresh();
  assert.equal(h.controls.retry.disabled,true);assert.equal(h.storage.size,1);assert.equal(h.controls.result.children.length,0);
});
test('malformed replacement clears old results and never displays server error details',async()=>{
  const h=await prepared(),bad=structuredClone(fixtures.draft);bad.campaign.qualifiedControls=59;h.setCurrent(bad);await h.refresh();
  assert.equal(h.controls.result.children.length,0);assert.doesNotMatch(text(h.controls.status),/PRIVATE_/);
});
test('authority-bearing imported action is rejected without POST or retained intent',async()=>{
  const h=await prepared();await h.load({...fixtures.freeze,authority:'AUTHENTICATED_OWNER'});
  assert.equal(h.controls.send.disabled,true);assert.equal(h.storage.size,0);assert.equal(posts(h).length,0);
});
test('late private response after logout cannot restore results',async()=>{
  const h=harness();h.login();await h.refresh();const release=h.defer('/campaigns/'+fixtures.draft.plan.planRef+'/review-receipt');
  const opening=h.open();h.logout();release();await opening;
  assert.equal(h.controls.result.children.length,0);assert.equal(h.controls.refresh.disabled,true);
});
test('new plan creation requires explicit action and exact plan readback',async()=>{
  const h=harness({initial:null});h.login();await h.refresh();await h.load(fixtures.create);h.confirm();await h.controls.send.click();
  assert.equal(posts(h).length,1);assert.equal(posts(h)[0].path,'/campaigns');assert.equal(h.storage.size,0);
});
test('input review uses Owner-only input receipt for exact acknowledgement',async()=>{
  const h=harness();h.login();await h.refresh();await h.open();await h.load(fixtures.inputAction);h.confirm();await h.controls.send.click();
  assert.equal(posts(h).length,1);assert.match(posts(h)[0].path,/\/inputs\/[a-f0-9]{32}\/review$/);
  assert.equal(h.storage.size,0);assert.ok(h.requests.some(r=>r.method==='GET'&&r.path.includes('/inputs/')));
});

test('dispatch child shares Owner host, interlocks metadata and invalidates on view or auth change',async()=>{
  let bridge,pending=false,invalidations=0,resets=0;const states=[];
  const h=harness({dispatchAdapter:{mount(root,host){bridge=host;return {
    hasPending:()=>pending,update:s=>states.push(s),invalidate(){invalidations++;},reset(){resets++;},dispose(){}};}}});
  h.login();await h.refresh();await h.open();await h.load();h.confirm();assert.equal(h.controls.send.disabled,false);
  assert.equal(bridge.planRef(),fixtures.draft.plan.planRef);assert.equal(bridge.canMutate(),true);
  pending=true;bridge.changed();assert.equal(h.module.hasPending(),true);assert.equal(h.controls.send.disabled,true);
  const before=invalidations;await h.refresh();assert.ok(invalidations>before);
  h.logout();assert.ok(resets>0);assert.equal(states.at(-1).authorized,false);
});
