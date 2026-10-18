const assert=require('node:assert/strict'),fs=require('node:fs'),http=require('node:http');
const {chromium}=require('playwright');
const actual=JSON.parse(fs.readFileSync('docs/data/scientific-session-catalog.json','utf8'));
const base=actual.sessions.find(s=>s.lightCompleted>0);
const id='2026-10-17_2026-10-18';
const rows=[{...base,sessionId:id,observationDate:'2026-10-17',target:'NGC 281',rmsTotalArcsec:null,exposureSeconds:null,raDeg:null,decDeg:null},{...base,sessionId:'2026-10-16_2026-10-17',target:'M 27',rmsTotalArcsec:0},{...base,sessionId:'2026-10-15_2026-10-16',target:'UNKNOWN',lightStarted:0,lightCompleted:0,completionPct:null,qualityState:'METADATA_INCOMPLETE',integrationHours:0}];
const receipt={sessionId:id,scope:'SESSION_DOCUMENT_PACKAGE',state:'VERIFIED',manifestRef:`data/sessions/2026/10/${id}/manifest.json`,fileCount:6,verifiedFileCount:6};
const html='<!doctype html><meta charset="utf-8">'+fs.readFileSync('docs/scientific-session-catalog/index.md','utf8').replace(/<link[^>]+>/g,'');
(async()=>{let server,browser,fail=false,transferFail=false,requests=0,catalog={...actual,sessions:structuredClone(rows)};
 try{
  server=http.createServer((req,res)=>{
   if(req.url.endsWith('scientific-session-catalog.json')){requests++;res.writeHead(fail?503:200,{'Content-Type':'application/json'});res.end(JSON.stringify(catalog));}
   else if(req.url.endsWith('session-package-transfer.json')){res.writeHead(transferFail?503:200,{'Content-Type':'application/json'});res.end(JSON.stringify({schemaVersion:'1.0',kind:'SESSION_PACKAGE_TRANSFER_PROJECTION',authority:'projection',scope:'SESSION_DOCUMENT_PACKAGE',records:[receipt]}));}
   else if(req.url.startsWith('/javascripts/')){res.setHeader('Content-Type','text/javascript');res.end(fs.readFileSync('docs'+req.url));}
   else {res.setHeader('Content-Type','text/html');res.end(html);}
  });await new Promise(r=>server.listen(0,'127.0.0.1',r));
  browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
  const p=await browser.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.clock.install();
  await p.goto(`http://127.0.0.1:${server.address().port}/scientific-session-catalog/`);
  const wait=()=>p.waitForFunction(()=>!document.querySelector('[data-session-refresh]').disabled);
  const refresh=async()=>{await p.getByRole('button',{name:'Aggiorna catalogo'}).click();await wait();};
  await wait();assert.equal(await p.locator('.dsg-session-card').count(),3);
  const kpis=await p.locator('[data-session-kpis] strong').allTextContents();assert.equal(kpis[0],'3');assert.equal(kpis[1],'2');
  assert.equal(await p.locator('[data-session-acquisition-count]').textContent(),'2 con LIGHT · 1 senza LIGHT');
  const card=p.locator('.dsg-session-card').filter({hasText:id});
  assert.match(await card.textContent(),/RMSNon disponibile/);assert(!/RA \(J2000\)/.test(await card.textContent()));
  assert.match(await card.textContent(),/VERIFIED · 6\/6 file/);
  assert.match(await p.locator('.dsg-session-card').filter({hasText:'2026-10-16_2026-10-17'}).textContent(),/0,000″/);
  assert.match(await p.locator('.dsg-session-card').filter({hasText:'2026-10-15_2026-10-16'}).textContent(),/Pacchetto senza LIGHT/);
  await p.getByRole('combobox',{name:'Qualità',exact:true}).selectOption('METADATA_INCOMPLETE');assert.equal(await p.locator('.dsg-session-card').count(),1);
  await p.getByRole('button',{name:'Reimposta'}).click();
  await p.getByRole('combobox',{name:'Target',exact:true}).selectOption('M 27');
  catalog.sessions.push({...base,sessionId:'2026-10-18_2026-10-19',target:'LDN 1320'});
  await p.clock.runFor(60001);await wait();assert.equal(await p.getByRole('combobox',{name:'Target',exact:true}).getAttribute('value'),null);
  assert.equal(await p.locator('.dsg-session-card').count(),1);assert.equal(await p.locator('[data-session-kpis] strong').nth(0).textContent(),'4');
  await refresh();assert.equal(await p.getByRole('option',{name:'M 27',exact:true}).count(),1);
  fail=true;await refresh();assert.equal(await p.locator('.dsg-session-card').count(),0);assert.equal(await p.locator('[data-session-kpis] strong').nth(0).textContent(),'—');
  await p.getByRole('searchbox',{name:'Ricerca',exact:true}).fill('M 27');assert.equal(await p.locator('.dsg-session-card').count(),0);
  fail=false;transferFail=true;await refresh();assert.match(await p.locator('[data-session-grid]').textContent(),/Transfer pacchetto: Non disponibile/);
  transferFail=false;await p.getByRole('button',{name:'Reimposta'}).click();await refresh();
  await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));});
  const before=requests;await p.clock.runFor(60001);assert.equal(requests,before);
  await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'));});await wait();assert.equal(requests,before+1);
  assert.deepEqual(errors,[]);console.log('PASS catalog: null vs real zero, known targets, acquisition/package counts, scoped receipts, filters, timer/manual/visibility refresh, failure and recovery.');
 }finally{await browser?.close();if(server)await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
