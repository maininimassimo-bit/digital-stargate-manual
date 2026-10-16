/* Consumer regression: synthetic projections, no provider or scientific writes. */
const assert=require('node:assert/strict'), fs=require('node:fs'), http=require('node:http');
const {chromium}=require('playwright');
const fields=['current-package','current-detail','latest-session','latest-detail','session-count','session-totals','session-records','freshness','latest-freshness','refresh-status'];
const html=`<!doctype html><meta charset="utf-8"><section data-dsg-home-snapshot><button data-home-refresh>Aggiorna riepilogo</button>${fields.map(x=>`<p data-home-${x}></p>`).join('')}<a data-home-latest-link></a></section><script src="/homepage-effects.js"></script>`;
const row=(sessionId,target,lightStarted,lightCompleted,integrationHours)=>({sessionId,target,lightStarted,lightCompleted,integrationHours});
const id='2026-10-14_2026-10-15';
const initial={
 'roadmap.json':{updatedAt:'2026-10-13',currentPackage:'BKL-051',summary:{percentCompleted:90},waves:[{items:[{id:'BKL-051',title:'Ricerca'}]}]},
 'scientific-session-catalog.json':{sessions:[row(id,'NGC 281',58,58,9.67),row('2026-09-19_2026-09-20','M27',16,16,2),row('2026-10-15_2026-10-16','UNKNOWN',0,0,0),row('2026-08-10_2026-08-11','M27',0,0,0)]},
 'latest-observation.json':{session_id:id,generated_at:'2026-10-16T13:15:05+02:00',target:{name:'NGC 281'},metrics:{}}
};
(async()=>{
 let server,browser,payload=structuredClone(initial),fail=false,requests=0;
 try{
  server=http.createServer((req,res)=>{
   if(req.url.startsWith('/data/')){requests++;res.writeHead(fail?503:200,{'Content-Type':'application/json'});res.end(JSON.stringify(payload[req.url.split('/').at(-1)]));}
   else if(req.url==='/homepage-effects.js'){res.setHeader('Content-Type','text/javascript');res.end(fs.readFileSync('docs/javascripts/homepage-effects.js'));}
   else {res.setHeader('Content-Type','text/html');res.end(html);}
  });
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
  const p=await browser.newPage(), errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.clock.install();await p.goto(`http://127.0.0.1:${server.address().port}`);
  const wait=()=>p.waitForFunction(()=>document.querySelector('[data-dsg-home-snapshot]').dataset.homeSnapshotLoading==='false');
  const text=k=>p.locator(`[data-home-${k}]`).textContent();
  const refresh=async()=>{await p.getByRole('button',{name:'Aggiorna riepilogo'}).click();await wait();};
  await wait();
  assert.equal(await text('session-count'),'2 sessioni con LIGHT');
  assert.equal(await text('session-records'),'Catalogo: 4 registrazioni · 2 senza LIGHT');
  assert.equal(await text('session-totals'),'11,67 h · 74 light · 2 target identificati');
  assert.equal(await text('freshness'),'Roadmap aggiornata: 13/10/2026');
  assert.match(await text('latest-freshness'),/Acquisizione: 14\/10\/2026–15\/10\/2026 · Aggiornamento dati: 16\/10\/26, 13:15/);
  // New import must update the entire summary on its timer, without reloading.
  const next='2026-10-16_2026-10-17';
  payload['scientific-session-catalog.json'].sessions.push(row(next,'LDN1320',2,0,0));
  payload['latest-observation.json']={...payload['latest-observation.json'],session_id:next};
  payload['roadmap.json'].updatedAt='2026-10-17';
  await p.clock.runFor(60001);await wait();
  assert.equal(await text('latest-session'),next);
  assert.equal(await text('session-count'),'3 sessioni con LIGHT'); // Failed LIGHT attempts are acquisitions.
  assert.match(await text('session-totals'),/3 target identificati/);
  assert.match(await text('freshness'),/17\/10\/2026/);
  assert.match(await p.locator('[data-home-latest-link]').getAttribute('href'),new RegExp(next));
  // Unknown counters are neither zero nor acquisitions, and totals are explicitly partial.
  payload['scientific-session-catalog.json'].sessions.push(row('2026-10-17_2026-10-18','N/A',null,null,null));
  payload['roadmap.json'].updatedAt=null;payload['latest-observation.json'].generated_at=null;
  await refresh();assert.match(await text('session-records'),/1 con acquisizione non determinabile/);
  assert.match(await text('session-totals'),/3 target identificati · totali parziali/);
  assert.equal(await text('freshness'),'Roadmap aggiornata: —');
  assert.match(await text('latest-freshness'),/Aggiornamento dati: non disponibile/);
  fail=true;await refresh();assert.equal(await text('latest-session'),'UNKNOWN');
  assert.equal(await text('session-count'),'—');assert.match(await p.locator('[data-home-latest-link]').getAttribute('href'),/scientific-session-catalog\/$/);
  fail=false;await refresh();assert.equal(await text('latest-session'),next);
  payload['scientific-session-catalog.json'].sessions[0].lightCompleted=false;
  await refresh();assert.equal(await text('session-count'),'—');
  payload=structuredClone(initial);await refresh();
  // Visibility return refreshes; hidden tabs skip their periodic requests.
  await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));});
  const before=requests;await p.clock.runFor(60001);assert.equal(requests,before);
  await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'));});
  await wait();assert.equal(requests,before+3);
  assert.deepEqual(errors,[]);
  console.log('PASS: acquisition/technical/unknown counts, known targets, separate source dates, timer/manual/visibility refresh, partial totals, failure/recovery and invalid counters.');
 }finally{await browser?.close();if(server)await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
