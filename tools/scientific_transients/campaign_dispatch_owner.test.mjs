import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';
const generated=spawnSync('python',['-c',[
'import json',
'from tools.scientific_transients.test_campaign_triplet import TripletTests',
'f=TripletTests();f.setUp();t=f.prepare();t.register_all(f.worker);p=t.owner_proposal()',
"before=f.f.service.review_receipt(p['planRef'])",
"event=f.owner.request('/v1/transient-analysis/campaigns/'+p['planRef']+'/dispatch-intents',p['request'])",
"after=f.f.service.review_receipt(p['planRef'])",
"[f.bridge.project(p['planRef'],event['sha256'],i) for i in range(3)]",
"technical=[f.bridge.technical_context(p['planRef'],event['sha256'],i) for i in range(3)]",
"print(json.dumps(dict(proposal=p,before=before,after=after,context=f.context,technical=technical)))",
'f.doCleanups()'].join('\n')],{encoding:'utf8',maxBuffer:8*1024*1024});
assert.equal(generated.status,0,generated.stderr);const fixtures=JSON.parse(generated.stdout);
function node(){return {value:'',files:[],checked:false,disabled:false,isConnected:true,textContent:'',callbacks:{},
  addEventListener(type,fn){this.callbacks[type]=fn;},click(){return this.disabled?undefined:this.callbacks.click?.();}};}
const canonical=v=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):Array.isArray(v)?v.map(canonical):v;
const digest=async v=>Buffer.from(await webcrypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(canonical(v))))).toString('hex');
function harness({storage=new Map(),recorded=false,lost=false}={}){
  const controls=Object.fromEntries(['proposal','intent-receipt','saved-receipt','action','ordinal','prepare','envelope','confirmed','send','reconcile','complete','status','pending','preview'].map(k=>[k,node()]));
  controls.action.value='DISPATCH_INTENT';controls.ordinal.value='0';
  const root=node();root.querySelector=s=>controls[s.match(/data-dispatch-(.+)\]/)[1]];
  const calls=[],downloads=[];let module,authorized=false,busy=false,blocked=false,fail=lost;
  const context=vm.createContext({crypto:webcrypto,TextEncoder,structuredClone,Blob,
    URL:{createObjectURL(blob){downloads.push(blob);return 'blob:synthetic';},revokeObjectURL(){}},setTimeout:fn=>fn(),
    document:{createElement:()=>({click(){}})},sessionStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)}});
  for(const file of ['scientific-campaign-dispatch-contract','scientific-campaign-contract','scientific-campaign-owner-operation','scientific-campaign-owner-receipt','scientific-campaign-dispatch-owner'])
    vm.runInContext(readFileSync('docs/javascripts/'+file+'.js','utf8'),context);
  const update=()=>module?.update({authorized,busy,blocked});
  const host={planRef:()=>fixtures.proposal.planRef,canAct:()=>authorized,canMutate:()=>authorized&&!blocked,changed:update,
    async run(fn){if(busy)return;busy=true;update();try{await fn();}finally{busy=false;update();}},
    async request(path,method='GET',request){calls.push({path,method,request});assert.equal(authorized,true);
      if(method==='POST'){recorded=true;if(fail)throw Error('synthetic lost acknowledgement');return {};}
      if(path.endsWith('/review-receipt'))return structuredClone(recorded?fixtures.after:fixtures.before);
      if(path.endsWith('/dispatch-context'))return structuredClone(fixtures.context);
      if(path.endsWith('/technical-context'))return structuredClone(fixtures.technical[Number(path.match(/jobs\/([0-2])/)[1])]);
      throw Error('unexpected synthetic route');}};
  module=context.DSGCampaignDispatchOwner.mount(root,host);update();
  async function load(name,value){const text=JSON.stringify(value);controls[name].files=[{size:Buffer.byteLength(text),text:async()=>text}];await controls[name].callbacks.change();}
  return {module,controls,calls,storage,downloads,context,load,
    login(){authorized=true;update();},logout(){authorized=false;update();},setBlocked(v){blocked=v;update();},
    setLost(v){fail=v;},async download(){return JSON.parse(await downloads.at(-1).text());},
    confirm(){controls.confirmed.checked=true;controls.confirmed.callbacks.change();}};
}
async function stage(h){
  await h.controls.prepare.click();const challenge=await h.download();
  const request=h.controls.action.value==='DISPATCH_INTENT'?fixtures.proposal.request:{};
  const selection=h.controls.action.value==='DISPATCH_INTENT'?
    await h.context.DSGCampaignContract.dispatchProposal(await h.context.DSGCampaignContract.receipt(fixtures.before),fixtures.proposal,fixtures.context):
    await h.context.DSGCampaignOwnerReceipt.projection(fixtures.after,fixtures.proposal,await h.context.DSGCampaignOwnerReceipt.intent(fixtures.after,fixtures.proposal),Number(h.controls.ordinal.value));
  const envelope={protocol:'DSG_CAMPAIGN_OWNER_DURABLE_OPERATION_V1',action:selection.action,planRef:selection.planRef,
    operationKeySha256:selection.operationKeySha256,challenge,request,requestSha256:challenge.requestSha256,
    relativePath:selection.relativePath,launchAuthorized:false,scientificValidation:'NOT_VALIDATED'};
  envelope.envelopeSha256=await digest(envelope);await h.load('envelope',envelope);h.confirm();
}
test('mount and login are passive; actual synthetic intent flow uses explicit actions and saved receipt',async()=>{
  const h=harness();assert.equal(h.controls.prepare.disabled,true);h.login();assert.equal(h.calls.length,0);
  await h.load('proposal',fixtures.proposal);await stage(h);assert.equal(h.controls.send.disabled,false);
  await h.controls.send.click();assert.equal(h.module.hasPending(),true);
  assert.equal(h.calls.filter(c=>c.method==='POST').length,1);
  await h.controls.reconcile.click();const receipt=await h.download();assert.equal(receipt.protocol,'DSG_CAMPAIGN_OWNER_INTENT_RECEIPT_V1');
  assert.equal(h.module.hasPending(),true);await h.load('saved-receipt',receipt);await h.controls.complete.click();
  assert.equal(h.module.hasPending(),false);assert.equal(h.calls.filter(c=>c.method==='POST').length,1);
});
test('lost acknowledgement survives reload and reconciles through reads without another POST',async()=>{
  const h=harness({lost:true});h.login();await h.load('proposal',fixtures.proposal);await stage(h);await h.controls.send.click();
  assert.equal(h.module.hasPending(),true);
  const next=harness({storage:h.storage,recorded:true});next.login();await next.load('proposal',fixtures.proposal);
  await next.controls.reconcile.click();const receipt=await next.download();await next.load('saved-receipt',receipt);await next.controls.complete.click();
  assert.equal(next.module.hasPending(),false);assert.equal(next.calls.filter(c=>c.method==='POST').length,0);
});
test('actual projection flow binds chosen ordinal and receipt with no native authority',async()=>{
  const h=harness({recorded:true});h.login();await h.load('proposal',fixtures.proposal);
  const receipt=await h.context.DSGCampaignOwnerReceipt.intent(fixtures.after,fixtures.proposal);
  await h.load('intent-receipt',receipt);h.controls.action.value='PROJECT_JOB';h.controls.action.callbacks.change();
  h.controls.ordinal.value='2';h.controls.ordinal.callbacks.change();await stage(h);await h.controls.send.click();
  const posted=h.calls.find(c=>c.method==='POST');assert.ok(posted.path.endsWith('/jobs/2/project'));
  await h.controls.reconcile.click();const saved=await h.download();assert.equal(saved.ordinal,2);assert.equal(saved.launchAuthorized,false);
  await h.load('saved-receipt',saved);await h.controls.complete.click();assert.equal(h.module.hasPending(),false);
});
test('logout and queue interlock invalidate or block prepared commands',async()=>{
  const h=harness();h.login();await h.load('proposal',fixtures.proposal);await stage(h);
  h.setBlocked(true);assert.equal(h.controls.send.disabled,true);h.logout();h.login();h.setBlocked(false);
  assert.equal(h.controls.send.disabled,true);assert.equal(h.calls.filter(c=>c.method==='POST').length,0);
});
