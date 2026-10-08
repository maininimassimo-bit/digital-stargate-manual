import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {webcrypto} from 'node:crypto';
const source=readFileSync(new URL('../../docs/javascripts/scientific-transients-portal.js',import.meta.url),'utf8');
const queueViews=JSON.parse(readFileSync(new URL('portal-queue-fixture.json',import.meta.url),'utf8'));
const tick=async()=>{for(let i=0;i<8;i++)await new Promise(resolve=>setTimeout(resolve,2));};
const fixture=()=>({jobId:'TRN_'+'6'.repeat(32),request:{requestId:'6'.repeat(32),bindingRef:'1'.repeat(32)},
  binding:{bindingRef:'1'.repeat(32),inputRef:'2'.repeat(32),referenceRef:'3'.repeat(32),algorithmRef:'4'.repeat(32),contractRef:'5'.repeat(32)},
  state:'COMPLETED',cancelRequested:false,sequence:4,result:{reportSha256:'7'.repeat(64),bindingRef:'1'.repeat(32),
    qualityCounts:{measured:0,excluded:0,incomplete:2}},reviews:[],createdAt:'2026-10-08T10:00:00+00:00',updatedAt:'2026-10-08T10:01:00.123456+00:00',
  rootId:'8'.repeat(32),attemptId:'9'.repeat(32),leaseIssuedAt:'2026-10-08T10:00:00+00:00',leaseExpiresAt:'2026-10-08T10:15:00+00:00',
  executionEvidence:'WORKER_REPORTED_NOT_ATTESTED',scientificValidation:'NOT_VALIDATED',detailsLocation:'OWNER_PC',publication:'NONE'});
function harness({jobs=[fixture()],status=200,fail=false,deferred=false,googleMissing=false,rawBody,media='application/json',contentLength=null,timeout=false,
  bindings=[fixture().binding],storage=new Map(),storageFail=false,removeFail=false,postFailure='',postDeferred=false}={}) {
  function node(tag='div'){return {tag,dataset:{},children:[],callbacks:{},disabled:false,isConnected:true,
    textContent:'',value:'',checked:false,setAttribute(){},addEventListener(type,callback){this.callbacks[type]=callback;},append(...items){this.children.push(...items);},
    replaceChildren(){this.children=[];},querySelectorAll(selector){return this.children.flatMap(n=>[...(n.tag===selector?[n]:[]),...n.querySelectorAll(selector)]);},
    click(){if(!this.disabled)this.callbacks.click?.();}};}
  const controls=Object.fromEntries(['message','connect','disconnect','signin','refresh','observed','jobs','group','verified','create','retry','pending','group-details'].map(key=>[key,node()]));
  const root=node();root.querySelector=selector=>controls[selector.match(/data-dsg-transients-(.+)\]/)[1]];
  let currentRoot=root,login,subscribe,release,abortByTimeout;
  const requests=[],blobs=[],revoked=[],created=[];
  const google={accounts:{id:{initialize(value){login=value.callback;},renderButton(){}}}};
  const context={document:{readyState:'complete',querySelector:()=>currentRoot,createElement:tag=>{const n=node(tag);created.push(n);return n;},head:node()},
    window:{google:googleMissing?undefined:google},google,document$:{subscribe(callback){subscribe=callback;}},
    Blob,TextDecoder,AbortController,crypto:webcrypto,Uint8Array,setTimeout(callback,delay){if(delay===30000)abortByTimeout=callback;return setTimeout(callback,delay);},clearTimeout,
    URL:{createObjectURL(blob){blobs.push(blob);return 'blob:'+blobs.length;},revokeObjectURL(url){revoked.push(url);}},
    localStorage:{setItem(){assert.fail('credential persistence forbidden');}},sessionStorage:{
      getItem:key=>storage.has(key)?storage.get(key):null,
      setItem(key,value){if(storageFail)throw Error('PRIVATE_STORAGE_ERROR');assert.equal(value.includes('OWNER_ONLY_IN_MEMORY'),false);storage.set(key,value);},
      removeItem(key){if(removeFail)throw Error('PRIVATE_STORAGE_ERROR');storage.delete(key);}},
    async fetch(url,options){
      requests.push({url,options});assert.match(url,/^https:\/\/dsg-pixinsight-pilot-183451329061.europe-west1.run.app\/v1\/transient-analysis\/(?:options|jobs(?:\/TRN_[a-f0-9]{32}\/(?:cancel|review))?)$/);
      assert.equal(options.cache,'no-store');
      assert.equal(options.redirect,'error');assert.equal(options.credentials,'omit');
      assert.equal(options.headers.Authorization,'Bearer OWNER_ONLY_IN_MEMORY');
      if(timeout)await new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(Error('ABORTED'))));
      if(deferred)await new Promise(resolve=>{release=resolve;});
      if(fail)throw Error('HOSTILE_PRIVATE_ERROR');
      let responseBody=url.endsWith('/options')?{bindings}:{jobs};
      if(options.method==='POST') {
        assert.equal(options.headers['Content-Type'],'application/json');
        if(postDeferred)await new Promise(resolve=>{release=resolve;});
        if(postFailure==='before')throw Error('LOST_ACK');
        const body=JSON.parse(options.body);
        if(url.endsWith('/jobs')) {
          let job=jobs.find(j=>j.jobId==='TRN_'+body.requestId);
          if(!job){job={...fixture(),jobId:'TRN_'+body.requestId,request:body,binding:bindings.find(b=>b.bindingRef===body.bindingRef),state:'QUEUED',sequence:0,result:null};
            for(const key of ['rootId','attemptId','leaseIssuedAt','leaseExpiresAt'])delete job[key];jobs.push(job);}
          responseBody=job;
        } else {
          const job=jobs.find(j=>url.includes(j.jobId));assert.ok(job);
          if(url.endsWith('/cancel')) {if(!['COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(job.state)){
            job.cancelRequested=true;if(job.state==='QUEUED')job.state='CANCELLED';}}
          else if(!job.reviews.some(r=>r.request.decisionId===body.decisionId))job.reviews.push({...structuredClone(queueViews.reviewResponse),request:body,recordedAt:job.updatedAt});
          responseBody=url.endsWith('/review')?job.reviews.find(r=>r.request.decisionId===body.decisionId):job;
        }
        if(postFailure==='after')throw Error('LOST_ACK');
      } else {assert.equal(options.method,'GET');assert.equal(options.body,undefined);}
      return {status,ok:status===200,headers:{get:key=>key==='Content-Length'?contentLength:media},
        body:new ReadableStream({start(controller){controller.enqueue(rawBody instanceof Uint8Array?rawBody:new TextEncoder().encode(rawBody??JSON.stringify(responseBody)));controller.close();}})};
    }};
  vm.runInNewContext(source,context);
  return {controls,root,requests,blobs,revoked,created,storage,
    async login(){controls.connect.click();await tick();login({credential:'OWNER_ONLY_IN_MEMORY'});await tick();},
    async refresh(){controls.refresh.click();await tick();},
    setStatus(value){status=value;},setJobs(value){jobs=value;},setBindings(value){bindings=value;},setPostFailure(value){postFailure=value;},release(){release?.();},fireTimeout(){abortByTimeout();},
    async create(){controls.group.value=bindings[0].bindingRef;controls.group.callbacks.change();controls.verified.checked=true;controls.verified.callbacks.change();controls.create.click();await tick();},
    navigate(){root.isConnected=false;currentRoot=null;subscribe();},
    repeatInitialize(){subscribe();},loginCallback(){return login;},context};
}
const text=h=>JSON.stringify(h.controls.jobs.children);

test('other portal pages do not initialize authentication or requests',()=>{
  let callback;
  vm.runInNewContext(source,{document:{readyState:'complete',querySelector:()=>null},
    document$:{subscribe(value){callback=value;}},fetch(){assert.fail('unrelated page fetch');}});
  callback();
});

test('no reads or commands before Owner action; initialization is idempotent',async()=>{
  const h=harness();assert.equal(h.requests.length,0);assert.equal(h.controls.refresh.disabled,true);
  h.repeatInitialize();await h.login();assert.equal(h.requests.length,2);await h.refresh();assert.equal(h.requests.length,4);
});
test('completion remains worker-reported, incomplete and scientifically unvalidated',async()=>{
  const h=harness();await h.login();assert.match(text(h),/Completamento tecnico/);assert.match(text(h),/incompleti 2/);
  assert.match(text(h),/Validazione scientifica non completata/);assert.match(text(h),/senza attestazione indipendente/);
  assert.equal(h.controls.jobs.querySelectorAll('button').length,2);
});
test('download contains a minimized snapshot with no token and no local-byte verification',async()=>{
  const h=harness();await h.login();h.controls.jobs.querySelectorAll('button')[0].click();
  const value=JSON.parse(await h.blobs[0].text());assert.equal(value.localBytesVerified,false);
  assert.equal(value.scientificValidation,'NOT_VALIDATED');assert.equal(value.publication,'NONE');
  assert.equal(JSON.stringify(value).includes('OWNER_ONLY_IN_MEMORY'),false);
  assert.equal(h.created.find(n=>n.tag==='a').download,fixture().jobId+'-ricevuta-stato.json');
  await h.refresh();assert.deepEqual(h.revoked,['blob:1']);
});
test('disabled backend is explicit, no fake result or automatic retry',async()=>{
  const h=harness({status:404});await h.login();assert.match(h.controls.message.textContent,/non è attivato/);
  assert.equal(h.controls.jobs.children.length,0);assert.equal(h.requests.length,1);
});
test('denied Owner access clears earlier private cards and disables refresh',async()=>{
  const h=harness();await h.login();h.setStatus(403);await h.refresh();
  assert.equal(h.controls.jobs.children.length,0);assert.equal(h.controls.refresh.disabled,true);
  assert.match(h.controls.message.textContent,/non autorizzato o scaduto/);
});
test('unavailable service clears a previous snapshot; manual read only',async()=>{
  const h=harness();await h.login();h.setStatus(503);await h.refresh();
  assert.equal(h.controls.jobs.children.length,0);assert.match(h.controls.message.textContent,/Nessun risultato mostrato/);
  assert.equal(h.requests.length,3);
});
test('empty state is explicit',async()=>{const h=harness({jobs:[]});await h.login();assert.match(text(h),/Nessuna analisi registrata/);});
test('pending cancel cannot be shown as a stopped native process',async()=>{
  const job=fixture();Object.assign(job,{state:'RUNNING',result:null,reviews:[],cancelRequested:true,sequence:2});
  const h=harness({jobs:[job]});await h.login();assert.match(text(h),/arresto del processo non è ancora confermato/);
  assert.equal(h.requests.some(r=>r.options.method!=='GET'),false);
});
test('recovery remains uncertain without relaunch or resolution commands',async()=>{
  const job=fixture();Object.assign(job,{state:'RECOVERY_REQUIRED',result:null,reviews:[]});
  const h=harness({jobs:[job]});await h.login();assert.match(text(h),/Stato incerto/);assert.match(text(h),/Conserva il tentativo/);
  assert.equal(h.controls.jobs.querySelectorAll('button').length,1);
});
test('queued cancellation without native attempt is a valid preserved receipt',async()=>{
  const job=fixture();Object.assign(job,{state:'CANCELLED',result:null,cancelRequested:true,sequence:0});
  for(const key of ['rootId','attemptId','leaseIssuedAt','leaseExpiresAt'])delete job[key];
  const h=harness({jobs:[job]});await h.login();assert.match(text(h),/Annullamento confermato/);
});
test('Owner review remains declared and bound to the exact report',async()=>{
  const job=fixture();job.reviews=[{request:{decisionId:'a'.repeat(32),reportSha256:job.result.reportSha256,decision:'FOLLOW_UP'},
    recordedAt:job.updatedAt,authority:'OWNER_DECLARED'}];
  const h=harness({jobs:[job]});await h.login();assert.match(text(h),/Owner dichiarata: Approfondire/);
  job.reviews[0].request.reportSha256='0'.repeat(64);h.setJobs([job]);await h.refresh();assert.equal(h.controls.jobs.children.length,0);
});
test('hostile HTML, credentials, added details and malformed claims fail closed',async()=>{
  const mutations=[j=>j.jobId='<img src=x>',j=>j.leaseToken='SECRET',j=>j.path='F:/private',j=>j.state='DISCOVERY',
    j=>j.scientificValidation='VALIDATED',j=>j.publication='PUBLISHED',j=>j.result.qualityCounts.measured=true,
    j=>j.result.bindingRef='0'.repeat(32),j=>j.binding.inputRef='https://untrusted.invalid',j=>j.updatedAt='2026-02-30T10:01:00Z',
    j=>j.result.significance=99,j=>j.cancelRequested=true,j=>delete j.attemptId];
  for(const mutate of mutations){const job=fixture();mutate(job);const h=harness({jobs:[job]});await h.login();
    assert.equal(h.controls.jobs.children.length,0);assert.match(h.controls.message.textContent,/Nessun risultato mostrato/);}
});
test('duplicate jobs, oversized collection and duplicate review IDs are rejected',async()=>{
  for(const jobs of [[fixture(),fixture()],Array.from({length:33},fixture)]){
    const h=harness({jobs});await h.login();assert.equal(h.controls.jobs.children.length,0);}
  const job=fixture(),review={request:{decisionId:'a'.repeat(32),reportSha256:job.result.reportSha256,decision:'KEEP_FOR_REVIEW'},recordedAt:job.updatedAt,authority:'OWNER_DECLARED'};
  job.reviews=[review,review];const h=harness({jobs:[job]});await h.login();assert.equal(h.controls.jobs.children.length,0);
});
test('disconnect during an in-flight read prevents late private rendering',async()=>{
  const h=harness({deferred:true});await h.login();h.controls.disconnect.click();h.release();await tick();
  assert.equal(h.controls.jobs.children.length,0);assert.equal(h.controls.refresh.disabled,true);
  assert.match(h.controls.message.textContent,/Accesso terminato/);
});
test('Instant Navigation clears token, cards, downloads and rejects old sign-in callbacks',async()=>{
  const h=harness();await h.login();h.controls.jobs.querySelectorAll('button')[0].click();const old=h.loginCallback();
  h.navigate();old({credential:'OWNER_ONLY_IN_MEMORY'});await tick();assert.equal(h.requests.length,2);
  assert.equal(h.controls.jobs.children.length,0);assert.deepEqual(h.revoked,['blob:1']);
});
test('late response after navigation cannot restore a removed private page',async()=>{
  const h=harness({deferred:true});await h.login();h.navigate();h.release();await tick();assert.equal(h.controls.jobs.children.length,0);
});
test('network errors are minimized and never reflect server diagnostics',async()=>{
  const h=harness({fail:true});await h.login();assert.match(h.controls.message.textContent,/Nessun risultato mostrato/);
  assert.equal(h.controls.message.textContent.includes('HOSTILE_PRIVATE_ERROR'),false);
});
test('failed Google script load exposes a usable error without network reads',async()=>{
  const h=harness({googleMissing:true});h.controls.connect.click();await tick();h.context.document.head.children[0].onerror();await tick();
  assert.match(h.controls.message.textContent,/Consultazione non riuscita/);assert.equal(h.requests.length,0);assert.equal(h.controls.connect.disabled,false);
});
test('bounded body, declared size, JSON media and UTF-8 reject malformed delivery',async()=>{
  for(const options of [{rawBody:'x'.repeat(1048577)},{contentLength:'1048577'},{contentLength:'-1'},
    {media:'text/html'},{rawBody:new Uint8Array([255])},{rawBody:'{"jobs":['}]){
    const h=harness(options);await h.login();assert.equal(h.controls.jobs.children.length,0);
    assert.match(h.controls.message.textContent,/Nessun risultato mostrato/);
  }
});
test('browser consumes actual Python queue Owner views in all lifecycle states',async()=>{
  assert.equal(queueViews.kind,'SYNTHETIC_QUEUE_OWNER_VIEWS_NOT_CLOUD_OAT');
  for(const item of queueViews.cases){const h=harness({jobs:item.response.jobs});await h.login();
    assert.equal(h.controls.jobs.children.length,1,item.stage);
    assert.match(h.controls.message.textContent,/Stato letto dal servizio privato/);
    assert.equal(text(h).includes('leaseToken'),false);}
});
test('operational read timeout clears results and exposes a manual retry error',async()=>{
  const h=harness({timeout:true});await h.login();h.fireTimeout();await tick();
  assert.equal(h.controls.jobs.children.length,0);assert.match(h.controls.message.textContent,/riprova manualmente/);
  assert.equal(h.controls.refresh.disabled,false);assert.equal(h.requests.length,1);
});

const posts=h=>h.requests.filter(r=>r.options.method==='POST');
test('create requires a selected group and explicit PC confirmation; no automatic commands',async()=>{
  const h=harness();await h.login();assert.equal(h.controls.create.disabled,true);assert.equal(posts(h).length,0);
  h.controls.group.value=fixture().binding.bindingRef;h.controls.group.callbacks.change();assert.equal(h.controls.create.disabled,true);
  await h.create();assert.equal(posts(h).length,1);const body=JSON.parse(posts(h)[0].options.body);
  assert.match(body.requestId,/^[a-f0-9]{32}$/);assert.equal(body.bindingRef,fixture().binding.bindingRef);
  assert.equal(h.storage.size,0);assert.match(h.controls.message.textContent,/Richiesta di analisi registrata/);
});
test('lost create acknowledgement is reconciled by read, without a second POST',async()=>{
  const h=harness({postFailure:'after'});await h.login();await h.create();assert.equal(h.storage.size,1);
  assert.equal(h.controls.create.disabled,true);await h.refresh();assert.equal(h.storage.size,0);assert.equal(posts(h).length,1);
});
test('uncommitted create retains immutable intent and retries only on explicit click',async()=>{
  const h=harness({postFailure:'before'});await h.login();await h.create();const body=posts(h)[0].options.body;
  await h.refresh();assert.equal(h.controls.retry.disabled,false);assert.equal(posts(h).length,1);
  h.setPostFailure('');h.controls.retry.click();await tick();assert.equal(posts(h).length,2);
  assert.equal(posts(h)[1].options.body,body);assert.equal(h.storage.size,0);
});
test('restored intent never sends automatically; changed immutable binding freezes retry',async()=>{
  const first=harness({postFailure:'before'});await first.login();await first.create();
  const changed={...fixture().binding,inputRef:'f'.repeat(32)};
  const h=harness({storage:first.storage,jobs:[],bindings:[changed]});await h.login();
  assert.equal(posts(h).length,0);assert.equal(h.controls.retry.disabled,true);assert.equal(h.controls.create.disabled,true);
  assert.equal(h.storage.size,1);
});
test('invalid stored intent is retained and blocks commands without reflecting contents',async()=>{
  const storage=new Map([['dsg-bkl051-owner-pending-v1','{"path":"PRIVATE_SECRET"}']]);
  const h=harness({storage});await h.login();assert.equal(h.controls.create.disabled,true);assert.equal(h.controls.retry.disabled,true);
  assert.equal(storage.size,1);assert.equal(h.controls.pending.textContent.includes('PRIVATE_SECRET'),false);assert.equal(posts(h).length,0);
});
test('storage failure prevents POST; removal failure blocks further commands',async()=>{
  const h=harness({storageFail:true});await h.login();await h.create();assert.equal(posts(h).length,0);assert.equal(h.controls.create.disabled,true);
  const other=harness({removeFail:true});await other.login();await other.create();assert.equal(posts(other).length,1);
  assert.equal(other.storage.size,1);assert.equal(other.controls.create.disabled,true);assert.equal(other.controls.retry.disabled,true);
});
test('queued cancellation retains job and acknowledges request, not native termination',async()=>{
  const queued=structuredClone(queueViews.cases.find(c=>c.stage==='QUEUED').response.jobs[0]);
  const h=harness({jobs:[queued]});await h.login();h.controls.jobs.querySelectorAll('button').find(b=>b.textContent==='Richiedi annullamento').click();await tick();
  assert.equal(posts(h).length,1);assert.equal(posts(h)[0].options.body,'{}');assert.match(text(h),/Annullamento confermato/);
  assert.match(h.controls.message.textContent,/PC va verificato separatamente/);assert.equal(h.storage.size,0);
});
test('review requires explicit local consultation and pins exact report hash',async()=>{
  const h=harness();await h.login();const button=h.controls.jobs.querySelectorAll('button').find(b=>b.textContent==='Registra valutazione dichiarata');
  button.click();await tick();assert.equal(posts(h).length,0);
  h.controls.jobs.querySelectorAll('input')[0].checked=true;h.controls.jobs.querySelectorAll('select')[0].value='FOLLOW_UP';
  button.click();await tick();assert.equal(posts(h).length,1);
  const body=JSON.parse(posts(h)[0].options.body);assert.equal(body.reportSha256,fixture().result.reportSha256);assert.equal(body.decision,'FOLLOW_UP');
  assert.match(text(h),/Owner dichiarata: Approfondire/);assert.equal(h.storage.size,0);
});
test('lost review acknowledgement reconciles exact declared decision without resubmission',async()=>{
  const h=harness({postFailure:'after'});await h.login();h.controls.jobs.querySelectorAll('input')[0].checked=true;
  h.controls.jobs.querySelectorAll('select')[0].value='KEEP_FOR_REVIEW';
  h.controls.jobs.querySelectorAll('button').find(b=>b.textContent==='Registra valutazione dichiarata').click();await tick();
  assert.equal(h.storage.size,1);await h.refresh();assert.equal(h.storage.size,0);assert.equal(posts(h).length,1);
});
test('disconnect during POST preserves intent and prevents later rendering or further requests',async()=>{
  const h=harness({postDeferred:true});await h.login();await h.create();const count=h.requests.length;
  h.controls.disconnect.click();h.release();await tick();assert.equal(h.requests.length,count);assert.equal(h.storage.size,1);
  assert.equal(h.controls.jobs.children.length,0);assert.match(h.controls.message.textContent,/Accesso terminato/);
});
test('restored valid create can only resend the same payload after fresh reads',async()=>{
  const first=harness({postFailure:'before'});await first.login();await first.create();
  const h=harness({storage:first.storage,jobs:[]});await h.login();assert.equal(posts(h).length,0);
  assert.equal(h.controls.retry.disabled,false);h.controls.retry.click();await tick();
  assert.equal(posts(h)[0].options.body,posts(first)[0].options.body);assert.equal(h.storage.size,0);
});
test('two rapid create clicks produce one intent and one POST',async()=>{
  const h=harness({postDeferred:true});await h.login();await h.create();h.controls.create.click();await tick();
  assert.equal(posts(h).length,1);h.release();await tick();assert.equal(h.storage.size,0);
});
test('a completed job before cancellation retry is reported as no effect',async()=>{
  const running=fixture();Object.assign(running,{state:'RUNNING',result:null,sequence:2});
  const h=harness({jobs:[running],postFailure:'before'});await h.login();
  h.controls.jobs.querySelectorAll('button').find(b=>b.textContent==='Richiedi annullamento').click();await tick();
  h.setJobs([fixture()]);await h.refresh();assert.equal(h.storage.size,0);assert.equal(posts(h).length,1);
  assert.match(h.controls.message.textContent,/nessun annullamento attribuito/);
});
test('review retry freezes when the report changes, without substituting the new digest',async()=>{
  const h=harness({postFailure:'before'});await h.login();h.controls.jobs.querySelectorAll('input')[0].checked=true;
  h.controls.jobs.querySelectorAll('select')[0].value='FOLLOW_UP';
  h.controls.jobs.querySelectorAll('button').find(b=>b.textContent==='Registra valutazione dichiarata').click();await tick();
  const changed=fixture();changed.result.reportSha256='e'.repeat(64);h.setJobs([changed]);await h.refresh();
  assert.equal(h.storage.size,1);assert.equal(h.controls.retry.disabled,true);assert.equal(posts(h).length,1);
});
test('duplicate review ID with a different declaration freezes reconciliation',async()=>{
  const h=harness({postFailure:'before'});await h.login();h.controls.jobs.querySelectorAll('input')[0].checked=true;
  h.controls.jobs.querySelectorAll('select')[0].value='FOLLOW_UP';
  h.controls.jobs.querySelectorAll('button').find(b=>b.textContent==='Registra valutazione dichiarata').click();await tick();
  const changed=fixture(),body=JSON.parse(posts(h)[0].options.body);
  changed.reviews=[{request:{...body,decision:'REJECT_CANDIDATE'},recordedAt:changed.updatedAt,authority:'OWNER_DECLARED'}];
  h.setJobs([changed]);await h.refresh();assert.equal(h.storage.size,1);assert.equal(h.controls.retry.disabled,true);
  assert.equal(posts(h).length,1);
});
test('changed persisted intent before acknowledgement is retained and blocks reconciliation',async()=>{
  const h=harness({postDeferred:true});await h.login();await h.create();
  const key='dsg-bkl051-owner-pending-v1',changed=JSON.parse(h.storage.get(key));changed.binding.inputRef='f'.repeat(32);
  const raw=JSON.stringify(changed);h.storage.set(key,raw);h.release();await tick();
  assert.equal(h.storage.get(key),raw);assert.equal(h.controls.create.disabled,true);assert.equal(h.controls.retry.disabled,true);
  assert.equal(posts(h).length,1);
});
test('removed persisted intent before acknowledgement freezes instead of creating a replacement',async()=>{
  const h=harness({postDeferred:true});await h.login();await h.create();h.storage.clear();h.release();await tick();
  assert.equal(h.storage.size,0);assert.equal(h.controls.create.disabled,true);assert.equal(h.controls.retry.disabled,true);
  assert.equal(posts(h).length,1);
});
