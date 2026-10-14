import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const sandbox = {URL, window:{}, document:{currentScript:null}};
vm.runInNewContext(fs.readFileSync('docs/javascripts/scientific-session-publication.js','utf8'),sandbox);
vm.runInNewContext(fs.readFileSync('docs/javascripts/scientific-data-engine.js','utf8'),sandbox);
const publication=sandbox.window.DSGSessionPublication, engine=sandbox.window.DSGScientificDataEngine;
const evidence=JSON.parse(fs.readFileSync('docs/project/evidence/BKL-049-M27-PUBLIC-2026-10-05.json','utf8'));
const sessionId='2026-09-19_2026-09-20';
const record={...evidence, title:'M27',workflowId:'WF-'+evidence.imageVersionId.slice(4), steps:Array.from({length:evidence.processCount},()=>({processId:'Script'}))};
const session={sessionId,lightCompleted:16,manifestState:'VERSIONED',transferState:'NOT_REPRESENTED',evidenceState:'SOURCE_METRICS_AVAILABLE'};

test('published M27 joins by exact declared session, with its version and partial workflow',()=>{
  const records=publication.select(sessionId,{records:[record]});
  assert.equal(records.length,1);
  const lineage=engine.getLineage(session,publication.describe(records));
  assert.equal(lineage[5].state,'partial');
  assert.match(lineage[5].detail,/80 passaggi disponibili.*parziale.*esecuzione non verificata/);
  assert.match(lineage[5].detail,/WF-5e5dd49a62f90e349e2931f3d143b941/);
  assert.equal(lineage[6].state,'represented');
  assert.match(lineage[6].detail,/VER-5e5dd49a62f90e349e2931f3d143b941.*dichiarata/);
});
test('same target, substring IDs and historical declarations do not establish an association',()=>{
  assert.equal(publication.select(sessionId,{records:[{...record,sessionIds:[sessionId+'-other']},{...record,associationEvidence:'HISTORICAL_OWNER_DECLARATION',sessionIds:[]}]}).length,0);
});
test('every associated version is retained, including unavailable workflows',()=>{
  const description=publication.describe([record,{...record,imageVersionId:'VER-second',workflowId:'WF-second',steps:[],captureCompleteness:'UNAVAILABLE'}]);
  assert.match(description.publication.detail,/VER-second/);
  assert.match(description.processing.detail,/WF-second: 0 passaggi disponibili; workflow non disponibile/);
});
test('withdrawal clears publication on the next fresh collection',()=>{
  assert.equal(publication.describe(publication.select(sessionId,{records:[record]})).publication.state,'represented');
  const description=publication.describe(publication.select(sessionId,{records:[]}));
  assert.equal(description.publication.state,'missing');
  assert.match(description.processing.detail,/Nessun workflow pubblico/);
});
test('failed or pending reads remain unknown rather than asserting absence',()=>{
  for(const state of ['loading','unavailable']){
    const description=publication.describe([],state);
    assert.equal(description.publication.state,'partial');
    assert.doesNotMatch(description.publication.detail,/Nessuna immagine/);
  }
});
test('gallery links bind the session and exact image version',()=>{
  const url=new URL(publication.galleryUrl('https://example.test/digital-stargate-manual/',sessionId,record.imageVersionId));
  assert.equal(url.pathname,'/digital-stargate-manual/scientific-image-gallery/');
  assert.equal(url.searchParams.get('sessionId'),sessionId);
  assert.equal(url.hash,'#'+record.imageVersionId);
});
test('canonical metrics link points to repository evidence and rejects malformed paths',()=>{
  const path=`data/sessions/2026/09/${sessionId}/normalized/session-metrics.json`;
  assert.equal(publication.metricsUrl(path),'https://github.com/maininimassimo-bit/digital-stargate-manual/blob/main/'+path);
  for(const path of [null,'https://evil.test','data/../secret','data/sessions/2026/09/id/normalized/session-metrics.json?token=x']) assert.equal(publication.metricsUrl(path),null);
});


test('scientific assets follow exact associated versions without claiming RAW inventory',()=>{
  const view=engine.getLineage(session,publication.describe(publication.select(sessionId,{records:[record]})))[2];
  assert.equal(view.state,'partial');
  assert.match(view.detail,/1 immagine pubblicata associata.*M27.*VER-5e5dd49a62f90e349e2931f3d143b941/);
  assert.match(view.detail,/dichiarata.*inventario RAW fotografici non esposto/);
  const withdrawn=engine.getLineage(session,publication.describe([]))[2];
  assert.doesNotMatch(withdrawn.detail,/VER-/);
  assert.match(withdrawn.detail,/Nessuna immagine pubblicata associata/);
  for(const state of ['loading','unavailable']){
    const failed=engine.getLineage(session,publication.describe([],state))[2];
    assert.equal(failed.state,'partial');assert.doesNotMatch(failed.detail,/Nessuna immagine|VER-/);
  }
});

test('unavailable catalog clears catalog lineage claims independently of gallery and transfer',()=>{
  const view=engine.getLineage(session,publication.describe([record]),{state:'represented',detail:'6/6 verified'},'unavailable');
  for(const index of [0,1,3]){assert.equal(view[index].state,'partial');assert.match(view[index].detail,/Catalogo non disponibile/);}
  assert.match(view[2].detail,/M27/);assert.equal(view[4].state,'represented');assert.equal(view[6].state,'represented');
  const graph=engine.getKnowledgeGraph(session,null,'unavailable');
  assert.equal(graph.outputs[0].available,false);assert.equal(graph.outputs[1].available,false);
});

async function freshReader(catalog,requests=[]){
  const context={window:{},document:{currentScript:null},location:{href:'https://portal.test/detail/',origin:'https://portal.test'},URL,AbortController,setTimeout,clearTimeout,TextDecoder,crypto: (await import('node:crypto')).webcrypto,
    fetch:async(url,options)=>{requests.push(options);return {ok:true,url,body:new Response(JSON.stringify(catalog)).body};}};
  vm.runInNewContext(fs.readFileSync('docs/javascripts/scientific-data-engine.js','utf8'),context);
  return context.window.DSGScientificDataEngine.getCurrentSession('../data/catalog.json',sessionId);
}
const catalog=records=>({schemaVersion:'1.5',catalogStatus:'VERSIONED_ANALYTICS_PROJECTION',sessions:records});
test('current catalog reader bypasses cached metrics and rejects removed or ambiguous identity',async()=>{
  const requests=[];
  assert.equal((await freshReader(catalog([{...session,lightCompleted:20}]),requests)).lightCompleted,20);
  assert.equal(requests[0].cache,'no-store');assert.equal(requests[0].credentials,'omit');assert.equal(requests[0].redirect,'error');
  for(const records of [[],[session,session],[null],[{...session,sessionId:sessionId+'-other'}]])await assert.rejects(freshReader(catalog(records)));
});

test('visible minute, visibility return and manual refresh reread all sources and remove withdrawn assets',async()=>{
  class Element{
    constructor(){this.dataset={};this.classList={add(){},remove(){}};this.listeners={};this.innerHTML='';this.textContent='';this.children=[];this.disabled=false;this.hidden=false;}
    addEventListener(name,fn){this.listeners[name]=fn;}
    append(...items){this.children.push(...items);}
    replaceChildren(){this.children=[];}
  }
  const nodes=new Map(),root=new Element();root.isConnected=true;root.dataset.sessionCatalog='../data/catalog.json';root.querySelector=key=>{if(!nodes.has(key))nodes.set(key,new Element());return nodes.get(key);};
  let initialize,timer,visibility,current={...session,target:'M27',weather:{},guiding:{}},records=[record],failed=false,reads=0;
  const document={currentScript:null,visibilityState:'visible',querySelector:()=>root,createElement:()=>new Element(),addEventListener:(name,fn)=>{if(name==='visibilitychange')visibility=fn;},removeEventListener(){}};
  const liveEngine={...engine,getSessions:async()=>[current],getSession:async()=>current,
    getCurrentSession:async()=>{reads++;if(failed)throw Error('catalog unavailable');return current;},
    getSessionPhotoCollection:async()=>({records}),getSessionTransferCollection:async()=>({records:[]})};
  const context={document,window:{DSGScientificDataEngine:liveEngine,DSGSessionPublication:publication,DSGSessionTransfer:{describe:()=>({state:'partial',detail:'transfer unknown'})},DSGPhotoApi:{base:'https://portal.test/'},DSGScientificSessionDetailRouting:{resolve:()=>({sessionId,source:'explicit'}),withSessionId:()=>''},DSG:{components:{register:component=>initialize=component.initialize}},location:{search:'?sessionId='+sessionId}},URLSearchParams,URL,console,setInterval:fn=>{timer=fn;return 1;},clearInterval(){}};
  vm.runInNewContext(fs.readFileSync('docs/javascripts/scientific-session-detail.js','utf8'),context);
  const flush=()=>new Promise(resolve=>setImmediate(resolve));await initialize();await flush();
  const lineage=nodes.get('[data-detail-lineage]'),button=nodes.get('[data-detail-publication-refresh]');
  assert.match(lineage.innerHTML,/16 completed light frames.*M27.*VER-/);assert.equal(reads,1);
  current={...current,lightCompleted:20};records=[];timer();await flush();
  assert.match(lineage.innerHTML,/20 completed light frames/);assert.doesNotMatch(lineage.innerHTML,/VER-/);assert.match(lineage.innerHTML,/Nessuna immagine/);
  document.visibilityState='hidden';timer();await flush();assert.equal(reads,2);
  document.visibilityState='visible';visibility();await flush();assert.equal(reads,3);
  failed=true;button.listeners.click();await flush();assert.match(lineage.innerHTML,/Catalogo non disponibile/);assert.doesNotMatch(lineage.innerHTML,/20 completed light frames/);assert.equal(button.disabled,false);
  failed=false;records=[record];button.listeners.click();await flush();assert.match(lineage.innerHTML,/20 completed light frames.*M27.*VER-/);assert.equal(reads,5);
});


const missionSandbox={window:{}};
vm.runInNewContext(fs.readFileSync('docs/javascripts/mission-control-lineage.js','utf8'),missionSandbox);
const mission=missionSandbox.window.DSGMissionLineage;
const completeSession={...session,target:'M27',telescope:'C8',camera:'QHY',filter:'L-Pro',observationDate:'2026-09-19',integrationHours:2,qualityState:'VALIDATED_ANALYTICS'};
const otherSession={...completeSession,sessionId:'2026-09-20_2026-09-21',target:'UNKNOWN',manifestState:'NOT_REPRESENTED',evidenceState:'UNAVAILABLE'};
test('mission coverage aggregates exact catalog identities without conflating documents and photographic assets',()=>{
  const rows=mission.describe([completeSession,otherSession],{records:[record,{...record,associationEvidence:'HISTORICAL_OWNER_DECLARATION',sessionIds:[]},{...record,sessionIds:[sessionId+'-other']}]},{records:[{sessionId,state:'VERIFIED'}]});
  const byLabel=label=>rows.find(row=>row.label===label);
  assert.equal(byLabel('Target').state,'partial');assert.match(byLabel('Target').detail,/1\/2/);
  assert.equal(byLabel('Metrics').state,'partial');assert.match(byLabel('Metrics').detail,/1\/2/);
  assert.match(byLabel('Scientific assets').detail,/1 versioni pubblicate.*1\/2.*inventario RAW fotografici non esposto/);
  assert.equal(byLabel('Scientific assets').state,'partial');
  assert.match(byLabel('Manifest · catalogo').detail,/1\/2/);
  assert.match(byLabel('Transfer · pacchetto sessione').detail,/1\/2.*SHA-256.*non RAW/);
  assert.equal(byLabel('Processing').state,'partial');assert.match(byLabel('Processing').detail,/esecuzione non verificata/);
  assert.equal(byLabel('Publication').state,'represented');assert.match(byLabel('Publication').detail,/1\/2/);
});
test('mission withdrawal, empty catalog and unavailable sources cannot retain positive coverage',()=>{
  const published=mission.describe([completeSession],{records:[record]},{records:[]});assert.equal(published[8].state,'represented');
  for(const sessions of [[completeSession],[]]){
    const rows=mission.describe(sessions,{records:[]},{records:[]});assert.equal(rows[8].state,'missing');assert.match(rows[4].detail,/0 versioni/);assert.notEqual(rows[4].state,'represented');
  }
  const galleryFailed=mission.describe([completeSession],null,{records:[{sessionId,state:'VERIFIED'}]});
  assert.equal(galleryFailed[8].state,'partial');assert.match(galleryFailed[8].detail,/non verificabile/);assert.equal(galleryFailed[6].state,'represented');
  const catalogFailed=mission.describe(null,{records:[record]},{records:[{sessionId,state:'VERIFIED'}]});
  assert(catalogFailed.every(row=>row.state==='partial'));assert.match(catalogFailed[8].detail,/associazioni non calcolabili/);
});

test('mission controller refreshes catalog, gallery and transfer on every trigger with independent failures',async()=>{
  class Element{constructor(){this.dataset={};this.listeners={};this.innerHTML='';this.textContent='';this.disabled=false;this.strongs=Array.from({length:4},()=>({textContent:''}));}addEventListener(name,fn){this.listeners[name]=fn;}querySelectorAll(){return this.strongs;}}
  const root=new Element(),nodes=new Map();root.isConnected=true;root.dataset.sessionCatalog='../data/catalog.json';root.querySelector=key=>{if(!nodes.has(key))nodes.set(key,new Element());return nodes.get(key);};
  let initialize,timer,visibility,catalogReads=0,galleryReads=0,transferReads=0,platformReads=0,platformFailed=false,sessions=[completeSession],records=[record],galleryFailed=false,catalogFailed=false;
  const document={querySelector:()=>root,visibilityState:'visible',addEventListener:(name,fn)=>{if(name==='visibilitychange')visibility=fn;},removeEventListener(){}};
  const context={document,window:{DSGMissionLineage:mission,DSG:{components:{register:c=>initialize=c.initialize}},DSGScientificDataEngine:{
    getCurrentSessions:async()=>{catalogReads++;if(catalogFailed)throw Error('unavailable');return sessions;},getSessionPhotoCollection:async()=>{galleryReads++;if(galleryFailed)throw Error('unavailable');return {records};},getSessionTransferCollection:async()=>{transferReads++;return {records:[{sessionId,state:'VERIFIED'}]};},getMissionPlatformState:async()=>{platformReads++;if(platformFailed)throw Error('unavailable');return platformFixture;}}},console,setInterval:fn=>{timer=fn;return 1;},clearInterval(){}};
  vm.runInNewContext(fs.readFileSync('docs/javascripts/mission-control.js','utf8'),context);initialize();
  const flush=()=>new Promise(resolve=>setImmediate(resolve));await flush();
  const knowledge=nodes.get('[data-mission-knowledge]'),kpis=nodes.get('[data-mission-kpis]'),button=nodes.get('[data-mission-refresh]');
  assert.match(knowledge.innerHTML,/1 versioni pubblicate.*1\/1/);assert.equal(kpis.strongs[0].textContent,'1');
  records=[];sessions=[completeSession,otherSession];timer();await flush();assert.match(knowledge.innerHTML,/0 versioni pubblicate/);assert.equal(kpis.strongs[0].textContent,'2');
  document.visibilityState='hidden';timer();await flush();assert.equal(catalogReads,2);
  document.visibilityState='visible';galleryFailed=true;visibility();await flush();assert.match(knowledge.innerHTML,/Gallery corrente non verificabile/);assert.match(knowledge.innerHTML,/1\/2 pacchetti verificati/);
  catalogFailed=true;platformFailed=true;button.listeners.click();await flush();assert.match(knowledge.innerHTML,/associazioni non calcolabili/);assert.equal(kpis.strongs[0].textContent,'—');assert.equal(button.disabled,false);
  catalogFailed=false;galleryFailed=false;platformFailed=false;records=[record];button.listeners.click();await flush();assert.match(knowledge.innerHTML,/1 versioni pubblicate/);
  assert.equal(catalogReads,5);assert.equal(galleryReads,5);assert.equal(transferReads,5);assert.equal(platformReads,5);
  assert.match(nodes.get('[data-mission-pipeline]').innerHTML,/203.*2026|203.*ago/);
  assert.match(nodes.get('[data-mission-pipeline]').innerHTML,/30 file \/ run/);
  assert.match(nodes.get('[data-mission-boundary]').innerHTML,/evidenza storica.*Non disponibile/);
  assert.doesNotMatch(nodes.get('[data-mission-boundary]').innerHTML,/07:30–08:15/);
});


const platformFixture=JSON.parse(fs.readFileSync('docs/data/scientific-platform-status.json','utf8'));
async function platformReader(value,requests=[]){
  const context={window:{},document:{currentScript:{src:'https://portal.test/javascripts/scientific-data-engine.js'}},location:{origin:'https://portal.test'},URL,AbortController,setTimeout,clearTimeout,TextDecoder,
    fetch:async(url,options)=>{requests.push(options);return {ok:true,url,body:new Response(JSON.stringify(value)).body};}};
  vm.runInNewContext(fs.readFileSync('docs/javascripts/scientific-data-engine.js','utf8'),context);
  return context.window.DSGScientificDataEngine.getMissionPlatformState();
}
test('operational projection reader preserves document-only authority and rejects contradictory or malformed evidence',async()=>{
  const requests=[];const value=await platformReader(platformFixture,requests);
  assert.equal(value.transfer.maxFilesPerRun,30);assert.equal(value.historicalDiscovery.asOf,'2026-08-04');
  assert.equal(requests[0].cache,'no-store');assert.equal(requests[0].credentials,'omit');assert.equal(requests[0].redirect,'error');
  const clone=()=>JSON.parse(JSON.stringify(platformFixture));
  const unsafe=clone();unsafe.safety.commandAuthority=true;
  const cleanup=clone();cleanup.transfer.sourceCleanupAuthorized=true;
  const live=clone();live.authorityBoundary.runtimeTelemetry=true;
  const count=clone();count.historicalDiscovery.parsed=202;
  for(const invalid of [null,{},unsafe,cleanup,live,count])await assert.rejects(platformReader(invalid));
});
