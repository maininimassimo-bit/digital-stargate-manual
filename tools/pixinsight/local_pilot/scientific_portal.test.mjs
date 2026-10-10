import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {webcrypto} from 'node:crypto';
const source=readFileSync(new URL('../../../docs/javascripts/pixinsight-pilot.js',import.meta.url),'utf8');
const tick=async()=>{for(let i=0;i<12;i++)await new Promise(resolve=>setTimeout(resolve,3));};
function harness({lostCreate=false,denied=false,rejected=false,unknownStatus=false,plansReady=false,sourcePlanReady=false,preparationReady=false,completedRevision=false,legacyRevisions=false,openaiEnabled=false}={}) {
  function node(){return {dataset:{},children:[],callbacks:{},value:'',checked:false,isConnected:true,
    addEventListener(type,callback){this.callbacks[type]=callback;},append(...items){this.children.push(...items);},
    replaceChildren(){this.children=[];},querySelectorAll(){return this.children.flatMap(label=>label.children).filter(x=>x.type==='checkbox'&&x.checked);},
    click(){this.callbacks.click?.();},remove(){}};}
  const controls=Object.fromEntries(['planning-mode','openai-option','openai-consent','openai-consent-label','origin','catalog-label','parent-label','session-fields','historical-fields','historical-target','provenance','historical-attest','message','connect','signin','form','fields','input','directory','prompt','target','mode','layout','bayer','bayer-label','additional','additional-label','plans','parent','title','date','sessions','attest','create','pending','retry','refresh','jobs','review','summary','preview','steps','workflow','correlations','receipt','accept','reject'].map(name=>[name,node()]));
  controls.title.value='M27 test';controls.date.value='2026-10-05';controls.attest.checked=true;
  controls.mode.value='LRGB';controls.layout.value='SINGLE';controls.additional.value='';controls.directory.value='F:\\Astro\\M27\\Master';controls.prompt.value='Dettaglio interno, fondo naturale';
  const root=node();root.querySelector=selector=>controls[selector.match(/data-p5-(.+)\]/)[1]];
  const stored=new Map(),requests=[];let callback,job,intake,first=lostCreate;
  if(completedRevision)job={jobId:'PIAI_'+'1'.repeat(32),state:'COMPLETED'};
  const revision={revisionId:'8'.repeat(32),imageVersionId:'VER-'+'8'.repeat(32),label:'M31 colore approvato',processingDate:'2026-10-06',reviewSha256:'9'.repeat(64)};
  const google={accounts:{id:{initialize(value){callback=value.callback;},renderButton(){}}}};
  const context={document:{readyState:'complete',querySelector:()=>root,createElement:node,createTextNode:text=>({textContent:text})},
    window:{google},google,crypto:webcrypto,Blob,URL,AbortController,setTimeout,clearTimeout,
    sessionStorage:{getItem:key=>stored.get(key)||null,setItem:(key,value)=>stored.set(key,value),removeItem:key=>stored.delete(key)},
    async fetch(url,options){
      requests.push({url,options});assert.equal(options.redirect,'error');assert.equal(options.credentials,'omit');
      assert.equal(options.headers.Authorization,'Bearer PRIVATE_OWNER_TOKEN');
      if(denied)return {ok:false,status:403,json:async()=>({error:'ACCESS_DENIED'})};
      if(url.endsWith('/revisions'))return legacyRevisions ? {ok:false,status:404,json:async()=>({error:'NOT_FOUND'})} : {ok:true,json:async()=>({revisions:completedRevision?[revision]:[]})};
      if(completedRevision&&url.includes('/revisions/'+revision.revisionId+'/')){
        if(url.endsWith('/result'))return {ok:true,json:async()=>({...revision,jobId:job.jobId,imageId:'IMG-test',workflowId:'WF-'+revision.revisionId,
          context:{selection:{title:'M31',sessionIds:[]}},original:{width:1000,height:800},steps:[{ordinal:1,processId:'PixelMath'}],decision:null})};
        if(url.endsWith('/decision'))return {ok:true,json:async()=>({publication:'NONE'})};
        return {ok:true,blob:async()=>new Blob(['private fixture'])};
      }
      if(url.endsWith('/options'))return {ok:true,json:async()=>({openaiPlanningEnabled:openaiEnabled,inputs:[{inputRef:'b'.repeat(32),target:'M27'}],images:[],catalogSha256:'a'.repeat(64),sessions:[{sessionId:'SESSION-M27',target:'M27'}]})};
      if(url.endsWith('/science/intakes')){
        if(options.method==='POST'){
          if(rejected)return {ok:false,status:400,json:async()=>({error:'CATALOG_CHANGED_REFRESH'})};
          const selection=JSON.parse(options.body);intake ||= {selection,state:'AWAITING_ASSISTANT_PLAN'};
          if(first){first=false;throw new Error('lost response');}
          return {ok:true,json:async()=>({requestId:selection.requestId,state:intake.state})};
        }
        if(intake&&plansReady&&intake.state!=='WITHDRAWN'){intake.state='PLAN_READY';intake.proposalSha256='d'.repeat(64);intake.plan={rationale:'Piano per il prompt',limitations:'M27 soltanto',masters:[{role:'R',width:1000,height:800,imageIndex:0}],background:{polyDegree:1,boxSize:16,boxSeparation:32},steps:['ChannelCombination'],checkpointCount:15,processing:{sharpenL:0.5,sharpenRGB:0.45,denoiseL:0.65,denoiseRGB:0.7,contrastLarge:0.22,contrastSmall:0.28,targetBackground:0.085}};}
        if(intake&&sourcePlanReady){intake.sourcePlanSha256='e'.repeat(64);intake.sourcePlan={rationale:'Selezione esplicita',limitations:'Astrometria da verificare',panels:[{panelId:'P1',directory:'F:\\Astro',sessionIds:['SESSION-M27'],masters:{RGB:{filename:'<img src=x>.xisf',imageIndex:0}}},{panelId:'P2',directory:'F:\\Astro',sessionIds:['SESSION-M27'],masters:{RGB:{filename:'Panel2.xisf',imageIndex:0}}}]};}
        if(intake&&preparationReady){intake.preparationPlanSha256='f'.repeat(64);intake.preparationPlan={rationale:'Preparazione CFA verificata',limitations:'Piano finale separato',masters:[{panelId:'P1',role:'CFA',filename:'<img src=x>.xisf',width:1000,height:800,imageIndex:0}],bayerPattern:'RGGB',canvas:null,nativeProcessCount:1,checkpointCount:2};}
        return {ok:true,json:async()=>({intakes:intake?[intake]:[]})};
      }
      if(/\/science\/intakes\/[a-f0-9]+\/approve-sources$/.test(url)){
        assert.equal(JSON.parse(options.body).sourcePlanSha256,intake.sourcePlanSha256);
        intake.sourceSelectionApproved=true;
        return {ok:true,json:async()=>({requestId:intake.selection.requestId,state:'SOURCE_SELECTION_APPROVED',nativeStarted:false})};
      }
      if(/\/science\/intakes\/[a-f0-9]+\/approve-preparation$/.test(url)){
        assert.equal(JSON.parse(options.body).preparationPlanSha256,intake.preparationPlanSha256);
        intake.preparationApproved=true;
        return {ok:true,json:async()=>({requestId:intake.selection.requestId,state:'LOCAL_PREPARATION_APPROVED',nativeStarted:false})};
      }
      if(/\/science\/intakes\/[a-f0-9]+\/approve$/.test(url)){
        const request=JSON.parse(options.body);assert.equal(request.proposalSha256,intake.proposalSha256);
        job={jobId:'PIAI_'+intake.selection.requestId,state:'QUEUED'};intake.state='JOB_CREATED';
        return {ok:true,json:async()=>job};
      }
      if(url.endsWith('/withdraw')){
        assert.deepEqual(JSON.parse(options.body),{});intake.state='WITHDRAWN';
        return {ok:true,json:async()=>({requestId:intake.selection.requestId,state:'WITHDRAWN',nativeStarted:false})};
      }
      if(/\/science\/intakes\/[a-f0-9]+$/.test(url))return intake?{ok:true,json:async()=>intake}:{ok:false,status:unknownStatus?503:400,json:async()=>({error:unknownStatus?'UNAVAILABLE':'INTAKE_NOT_FOUND'})};
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

test('derived review and downloads use exact revision, preserving the first delivery',async()=>{
  const h=harness({completedRevision:true});await h.login();
  const card=h.controls.jobs.children[0];
  const revised=card.children.find(x=>x.textContent==='M31 colore approvato · 2026-10-06');
  assert.ok(revised);revised.click();await tick();
  assert.match(h.controls.summary.children[0].textContent,/VER-8888/);
  h.controls.workflow.click();await tick();h.controls.correlations.click();await tick();
  h.controls.accept.click();await tick();
  const revisionRequests=h.requests.filter(x=>/\/(result|preview|workflow|correlations|decision)$/.test(x.url));
  assert.ok(revisionRequests.length>=6);
  assert.ok(revisionRequests.every(x=>x.url.includes('/revisions/'+'8'.repeat(32)+'/')));
  const decision=revisionRequests.find(x=>x.url.endsWith('/decision'));
  assert.deepEqual(JSON.parse(decision.options.body),{reviewSha256:'9'.repeat(64),decision:'ACCEPT_PRIVATE'});
});

test('previous delivery remains reachable when revision API is rolled back',async()=>{
  const h=harness({completedRevision:true,legacyRevisions:true});await h.login();
  const card=h.controls.jobs.children[0];
  assert.ok(card.children.some(x=>x.textContent==='Apri anteprima e workflow'));
  assert.equal(card.children.some(x=>x.textContent==='M31 colore approvato · 2026-10-06'),false);
  assert.equal(h.controls.refresh.disabled,false);
  assert.doesNotMatch(h.controls.message.textContent,/Operazione non completata/);
});
test('folder and prompt create planning intake only, no native queue or code evaluation',async()=>{
  const h=harness();await h.login();await h.submit();
  const posts=h.requests.filter(x=>x.url.endsWith('/science/intakes')&&x.options.method==='POST');
  assert.equal(posts.length,1);const body=JSON.parse(posts[0].options.body);
  assert.deepEqual(body.sessionIds,['SESSION-M27']);assert.equal(body.associationConfirmed,true);
  assert.equal(body.parent,null);assert.equal('script' in body,false);assert.equal('path' in body,false);
  assert.equal(body.masterDirectory,'F:\\Astro\\M27\\Master');assert.equal(body.prompt,'Dettaglio interno, fondo naturale');
  assert.equal(h.stored.size,0);assert.match(h.controls.message.textContent,/conservat/);
  assert.equal(h.requests.some(x=>/worker|decision|commit/.test(x.url)),false);
  assert.equal(h.requests.some(x=>x.url.endsWith('/science/jobs')&&x.options.method==='POST'),false);
});

test('OpenAI requires runtime availability and explicit transfer consent, no browser provider call',async()=>{
  const h=harness({openaiEnabled:true});await h.login();
  assert.equal(h.controls['openai-option'].disabled,false);
  h.controls['planning-mode'].value='OPENAI_API';h.controls['planning-mode'].callbacks.change();
  await h.submit();assert.equal(h.requests.some(r=>r.options.method==='POST'),false);
  h.controls['openai-consent'].checked=true;await h.submit();
  const post=h.requests.find(r=>r.url.endsWith('/science/intakes')&&r.options.method==='POST');
  assert.deepEqual(JSON.parse(post.options.body).openaiPlanning,{dataTransferConfirmed:true});
  assert.equal(h.requests.some(r=>r.url.includes('api.openai.com')||r.url.includes('/worker/')),false);
  h.controls['planning-mode'].value='SESSION_ASSISTED';h.controls['planning-mode'].callbacks.change();
  assert.equal(h.controls['openai-consent'].checked,false);
});

test('disabled backend refuses OpenAI choice without freezing or sending a request',async()=>{
  const h=harness();await h.login();assert.equal(h.controls['openai-option'].disabled,true);
  h.controls['planning-mode'].value='OPENAI_API';h.controls['openai-consent'].checked=true;
  await h.submit();assert.equal(h.requests.some(r=>r.options.method==='POST'),false);
  assert.equal(h.stored.size,0);
});

test('historical mosaic clears catalog choices and sends declared target without fake sessions',async()=>{
  const h=harness();await h.login();h.controls.origin.value='HISTORICAL';
  h.controls.origin.callbacks.change();
  assert.equal(h.controls.sessions.children.length,0);assert.equal(h.controls.attest.required,false);
  h.controls['historical-target'].value='M31';h.controls.provenance.value='Riprese anteriori al portale';
  h.controls['historical-attest'].checked=true;h.controls.mode.value='OSC';h.controls.layout.value='PANELS';
  await h.submit();
  const body=JSON.parse(h.requests.find(r=>r.url.endsWith('/science/intakes')&&r.options.method==='POST').options.body);
  assert.deepEqual(body.sessionIds,[]);assert.equal(body.catalogSha256,null);assert.equal(body.parent,null);
  assert.equal(body.associationConfirmed,false);assert.equal(body.historicalSource.target,'M31');
  assert.equal(body.historicalSource.attested,true);assert.equal(body.sourceProfile.layout,'PANELS');
  assert.equal(h.requests.some(r=>r.url.endsWith('/approve')||r.url.includes('/worker/')),false);
});

test('historical provenance requires a separate human declaration and switching resets attestations',async()=>{
  const h=harness();await h.login();h.controls.origin.value='HISTORICAL';h.controls.origin.callbacks.change();
  h.controls['historical-target'].value='M31';h.controls.provenance.value='Riprese storiche';await h.submit();
  assert.equal(h.requests.some(r=>r.options.method==='POST'),false);
  assert.match(h.controls.message.textContent,/conferma la dichiarazione/);
  h.controls['historical-attest'].checked=true;h.controls.origin.value='CATALOG';h.controls.origin.callbacks.change();
  assert.equal(h.controls['historical-attest'].checked,false);assert.equal(h.controls.attest.checked,false);
  assert.equal(h.controls.attest.required,true);
});

test('withdrawal preserves the visible receipt and removes all plan approval controls',async()=>{
  const h=harness({plansReady:true});await h.login();await h.submit();
  h.controls.plans.children[0].children.find(n=>n.textContent==='Ritira richiesta').click();await tick();
  assert.equal(h.requests.filter(r=>r.url.endsWith('/withdraw')).length,1);
  const card=h.controls.plans.children[0];assert.match(JSON.stringify(card.children),/Richiesta ritirata/);
  assert.equal(card.children.some(n=>n.textContent==='Conferma piano e richiedi elaborazione'),false);
  assert.equal(h.requests.some(r=>r.url.endsWith('/approve')||r.url.endsWith('/cancel')),false);
});
test('lost create response retains exact request and retry cannot duplicate or change it',async()=>{
  const h=harness({lostCreate:true});await h.login();await h.submit();
  assert.equal(h.stored.size,1);assert.equal(h.controls.fields.disabled,true);
  assert.equal([...h.stored.values()].some(x=>x.includes('PRIVATE_OWNER_TOKEN')),false);
  h.controls.title.value='Changed after ambiguous response';await h.retry();
  const posts=h.requests.filter(x=>x.url.endsWith('/science/intakes')&&x.options.method==='POST');
  assert.equal(posts.length,2);assert.equal(posts[0].options.body,posts[1].options.body);
  assert.equal(h.stored.size,0);
});
test('denied authentication does not enable scientific commands',async()=>{
  const h=harness({denied:true});await h.login();
  assert.equal(h.controls.fields.disabled,true);assert.equal(h.controls.refresh.disabled,true);
  assert.equal(h.requests.some(x=>x.options.method==='POST'),false);
  assert.match(h.controls.message.textContent,/Accedi di nuovo/);
});
test('planning intake stays pending without automatic cancel, approval or reassignment',async()=>{
  const h=harness();await h.login();await h.submit();
  const text=JSON.stringify(h.controls.plans.children.map(card=>card.children.map(x=>x.textContent)));
  assert.match(text,/Nessuna elaborazione avviata/);
  assert.equal(h.requests.some(x=>/cancel/.test(x.url)),false);
});

test('mosaic selection renders literal filenames and confirms its exact digest without queueing',async()=>{
  const h=harness({sourcePlanReady:true});await h.login();
  h.controls.mode.value='OSC';h.controls.layout.value='PANELS';await h.submit();
  const card=h.controls.plans.children[0];
  const files=card.children.filter(x=>x.children?.some(child=>child.textContent?.includes('<img src=x>')));
  assert.equal(files.length,1);
  const button=card.children.find(x=>x.textContent==='Conferma selezione dei pannelli');
  assert.ok(button);assert.equal(h.requests.some(x=>x.url.endsWith('/approve-sources')),false);
  button.click();await tick();
  assert.equal(h.requests.filter(x=>x.url.endsWith('/approve-sources')).length,1);
  assert.match(h.controls.message.textContent,/nessuna elaborazione avviata/);
  assert.equal(h.requests.some(x=>x.options.method==='POST'&&/\/science\/jobs|\/approve$/.test(x.url)),false);
});

test('catalog rejection clears frozen request only after verified job absence and reloads options',async()=>{
  const h=harness({rejected:true});await h.login();await h.submit();
  assert.equal(h.stored.size,0);assert.equal(h.controls.fields.disabled,false);
  assert.equal(h.requests.filter(x=>x.url.endsWith('/options')).length,2);
  assert.match(h.controls.message.textContent,/assenza della richiesta di piano verificata/);
});

test('preparation confirmation binds exact plan and cannot queue final processing',async()=>{
  const h=harness({preparationReady:true});await h.login();h.controls.mode.value='OSC_CFA';h.controls.bayer.value='RGGB';await h.submit();
  const card=h.controls.plans.children[0];
  assert.match(JSON.stringify(card.children.map(x=>x.textContent)),/Preparazione dei master|pattern RGGB/);
  const confirm=card.children.find(x=>x.textContent==='Conferma preparazione dei master');assert.ok(confirm);
  assert.equal(h.requests.some(x=>x.url.endsWith('/approve-preparation')),false);
  confirm.click();await tick();
  const posts=h.requests.filter(x=>x.url.endsWith('/approve-preparation'));
  assert.equal(posts.length,1);assert.deepEqual(JSON.parse(posts[0].options.body),{preparationPlanSha256:'f'.repeat(64)});
  assert.equal(h.requests.some(x=>x.options.method==='POST'&&/\/science\/jobs|\/approve$|worker/.test(x.url)),false);
  assert.match(h.controls.message.textContent,/supervisionato/);
});

test('reviewed plan enters queue only on explicit Owner approval of exact proposal hash',async()=>{
  const h=harness({plansReady:true});await h.login();await h.submit();
  assert.equal(h.requests.some(x=>x.url.endsWith('/approve')),false);
  const approve=h.controls.plans.children[0].children.find(x=>x.textContent==='Conferma piano e richiedi elaborazione');
  assert.ok(approve);approve.click();await tick();
  const posts=h.requests.filter(x=>x.url.endsWith('/approve'));
  assert.equal(posts.length,1);assert.deepEqual(JSON.parse(posts[0].options.body),{proposalSha256:'d'.repeat(64)});
});
test('definitive rejection with uncertain job status retains frozen request',async()=>{
  const h=harness({rejected:true,unknownStatus:true});await h.login();await h.submit();
  assert.equal(h.stored.size,1);assert.equal(h.controls.fields.disabled,true);
  assert.equal(h.requests.filter(x=>x.url.endsWith('/options')).length,1);
});
