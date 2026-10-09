const assert=require('node:assert/strict'),fs=require('node:fs'),{chromium}=require('playwright');
const base=process.env.DSG_TEST_BASE_URL||'http://127.0.0.1:8766/';
(async()=>{
 const b=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
 try{
  const p=await b.newPage();let requests=0,unavailable=false;const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
  await p.route('https://digitalstargate.freeddns.it:23232/current/image.jpg*',r=>{requests++;return unavailable?r.abort():r.fulfill({contentType:'image/jpeg',body:fs.readFileSync('docs/assets/images/osservatorio-hero.jpg')});});
  await p.clock.install();await p.goto(base);const s=p.locator('[data-dsg-allsky-live]');await p.waitForSelector('[data-dsg-scene-state="ready"]');
  assert.equal(await s.getByRole('button',{name:'Dall’alto'}).count(),0);
  assert.equal(await s.getByRole('link',{name:/Allsky/}).getAttribute('href'),'https://digitalstargate.freeddns.it:23232/allsky/');
  for(const width of [1440,1007,768,390]){
   await p.setViewportSize({width,height:900});const f=await s.evaluate(e=>{const i=e.querySelector('img'),b=i.getBoundingClientRect(),h=e.querySelector('.dsg-scene__heading').getBoundingClientRect(),t=e.querySelector('.dsg-scene__toolbar').getBoundingClientRect();return {fit:getComputedStyle(i).objectFit,top:b.top,bottom:b.bottom,heading:h.bottom,toolbar:t.top,height:b.height,natural:i.naturalWidth};});
   assert.equal(f.fit,'contain');assert(f.top>=f.heading&&f.bottom<=f.toolbar&&f.height>100&&f.natural>0,JSON.stringify(f));
  }
  const refreshed=p.waitForResponse(r=>r.url().startsWith('https://digitalstargate.freeddns.it:23232/current/image.jpg'));
  await p.clock.runFor(31000);await refreshed;await p.waitForFunction(()=>document.querySelector("[data-dsg-scene-state]").dataset.dsgSceneState==="ready");assert(requests>=2);
  await s.getByRole('button',{name:'Vista essenziale',exact:true}).click();const frozen=requests;await p.clock.runFor(61000);assert.equal(requests,frozen);
  await p.reload();assert.equal(await s.getAttribute('data-dsg-scene-state'),'essential');assert.equal(requests,frozen);
  await s.getByRole('button',{name:'Attiva il live',exact:true}).click();await p.waitForSelector('[data-dsg-scene-state="ready"]');
  unavailable=true;await p.clock.runFor(31000);await p.waitForSelector('[data-dsg-scene-state="unavailable"]');assert(await s.locator('img').isHidden());
  unavailable=false;await p.clock.runFor(31000);await p.waitForSelector('[data-dsg-scene-state="ready"]');
  await p.goto(base+'mission-control/');const away=requests;await p.clock.runFor(61000);assert.equal(requests,away);assert.deepEqual(errors,[]);
  console.log('PASS: preview fit, refresh, essential persistence, error/recovery and teardown.');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
