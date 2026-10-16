/* Isolated browser contract: no remote survey/provider or scientific mutation. */
const assert=require('node:assert/strict'),fs=require('node:fs'),http=require('node:http');
const {chromium}=require('playwright');
const imported=JSON.parse(fs.readFileSync('docs/data/realtime/latest-observation.json','utf8'));
const complete={...imported,target:{name:"Target non disponibile",ra_deg:null,dec_deg:null,epoch:null,coordinate_source:"unavailable"}};
const observed={...complete,session_id:'2026-10-14_2026-10-15',target:{name:'NGC 281',ra_deg:13.10416667,dec_deg:56.565,epoch:'J2000',coordinate_source:'nina-log'}};
const markup=`<!doctype html><html><head><meta charset="utf-8"></head><body><section class="dsg-latest-observation"><button data-latest-sky-refresh>Aggiorna vista astronomica</button><p data-latest-sky-note role="status"></p><div class="dsg-showcase__media"></div><div class="dsg-showcase__content"><h2></h2></div><div class="dsg-showcase__metrics"><strong></strong><strong></strong><strong></strong></div><span data-sky-session></span><span data-sky-survey></span><span data-sky-fov></span><span data-sky-ra></span><span data-sky-dec></span><span data-sky-source></span></section><script src="/latest-observation.js"></script></body></html>`;
(async()=>{
 let payload=structuredClone(complete),httpError=false,server,browser;
 try{
  server=http.createServer((req,res)=>{
   if(req.url.startsWith('/data/')){res.writeHead(httpError?503:200,{'Content-Type':'application/json'});res.end(JSON.stringify(payload));}
   else if(req.url==='/latest-observation.js'){res.setHeader('Content-Type','text/javascript');res.end(fs.readFileSync('docs/javascripts/latest-observation.js'));}
   else {res.setHeader('Content-Type','text/html');res.end(markup);}
  });
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const origin=`http://127.0.0.1:${server.address().port}`;
  browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
  const p=await browser.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.route('**/*',r=>new URL(r.request().url()).origin===origin?r.continue():r.abort());
  await p.addInitScript(()=>{
   window.skyCalls=[];
   window.A={init:Promise.resolve(),aladin(selector,options){window.skyCalls.push(['create',options.target]);document.querySelector(selector).textContent='Synthetic survey';return {gotoRaDec(ra,dec){window.skyCalls.push(['goto',ra,dec]);},setFoV(){},setBaseImageLayer(){}};}};
  });
  await p.clock.install();
  await p.goto(origin);
  const wait=()=>p.waitForFunction(()=>!document.querySelector('[data-latest-sky-refresh]').disabled);
  await wait();
  // Missing-coordinate fixture stays valid when future imports contain coordinates.
  assert.equal(await p.locator('[data-sky-ra]').textContent(),'Non disponibile');
  assert.equal(await p.locator('[data-sky-dec]').textContent(),'Non disponibile');
  assert.equal(await p.locator('#dsg-latest-sky-canvas').isVisible(),false);
  assert.deepEqual(await p.evaluate(()=>window.skyCalls),[]);
  assert((await p.locator('[data-latest-sky-note]').textContent()).includes(complete.session_id));
  payload=structuredClone(observed);
  await p.getByRole('button',{name:'Aggiorna vista astronomica'}).click();await wait();
  assert.deepEqual(await p.evaluate(()=>window.skyCalls),[['create','13.10416667 56.565']]);
  assert.equal(await p.locator('[data-sky-ra]').textContent(),'13,1042°');
  assert.equal(await p.locator('[data-sky-session]').textContent(),observed.session_id);
  // Same identity does not undo user panning; numeric zero is a legitimate coordinate.
  await p.getByRole('button',{name:'Aggiorna vista astronomica'}).click();await wait();
  assert.equal((await p.evaluate(()=>window.skyCalls)).length,1);
  payload={...observed,session_id:'2026-10-16_2026-10-17',target:{...observed.target,ra_deg:0,dec_deg:0}};
  await p.clock.runFor(60001);await wait();
  assert.deepEqual((await p.evaluate(()=>window.skyCalls)).at(-1),['goto',0,0]);
  assert.equal(await p.locator('[data-sky-ra]').textContent(),'0,0000°');
  assert.equal(await p.locator('[data-sky-session]').textContent(),payload.session_id);
  for(const target of [{ra_deg:null},{ra_deg:''},{ra_deg:false},{ra_deg:'13.1'},{ra_deg:360},{dec_deg:91},{epoch:null}]){
   payload={...observed,target:{...observed.target,...target}};
   const before=await p.evaluate(()=>window.skyCalls.length);
   await p.getByRole('button',{name:'Aggiorna vista astronomica'}).click();await wait();
   assert.equal(await p.locator('[data-sky-ra]').textContent(),'Non disponibile');
   assert.equal(await p.locator('#dsg-latest-sky-canvas').isVisible(),false);
   assert.equal(await p.evaluate(()=>window.skyCalls.length),before);
  }
  payload=structuredClone(observed);await p.getByRole('button',{name:'Aggiorna vista astronomica'}).click();await wait();
  assert.equal(await p.locator('#dsg-latest-sky-canvas').isVisible(),true);
  httpError=true;await p.getByRole('button',{name:'Aggiorna vista astronomica'}).click();await wait();
  assert.equal(await p.locator('[data-sky-ra]').textContent(),'Non disponibile');
  assert.equal(await p.locator('#dsg-latest-sky-canvas').isVisible(),false);
  assert.deepEqual(errors,[]);
  console.log('PASS: real missing latest coordinates, exact numeric target, manual and automatic refresh, unchanged-view preservation, real zero, invalid coordinate/epoch rejection, recovery and HTTP failure.');
 }finally{await browser?.close();await new Promise(r=>server?.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
