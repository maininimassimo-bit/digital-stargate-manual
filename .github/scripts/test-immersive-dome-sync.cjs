const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base=process.env.DSG_TEST_BASE_URL||'http://127.0.0.1:8766/digital-stargate-manual/';
(async()=>{
 const b=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
 const p=await b.newPage({viewport:{width:1157,height:828}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 let state='CLOSED',stale=false;const now=Date.now();await p.clock.install({time:now});
 await p.route('**/*',r=>{
  const url=r.request().url();
  if(url.endsWith('/v1/observatory-status')||url.endsWith('/data/realtime/observatory-status.json'))return r.fulfill({json:{quality:'CURRENT',fresh_until_utc:new Date(now+3600000).toISOString(),systems:{dome:{state,quality:'CURRENT',fresh_until_utc:new Date(now+(stale?-3600000:3600000)).toISOString()}}}});
  return new URL(url).origin===new URL(base).origin?r.continue():r.abort();
 });
 const stage=p.locator('[data-dsg-dome-sync]');
 async function view(expected){await p.waitForFunction(v=>document.querySelector('[data-dsg-dome-sync]')?.dataset.dsgRenderedView===v,expected);assert.equal(await stage.getAttribute('data-dsg-selected-view'),expected);}
 async function refresh(){await p.clock.fastForward(15001);}
 try{
  await p.goto(base+'status/');await stage.scrollIntoViewIfNeeded();await view('exterior');
  assert.match(await p.locator('[data-observatory-status="dome-state"]').first().innerText(),/CLOSED/);
  if(process.env.DSG_DOME_SCREENSHOTS)await stage.screenshot({path:process.env.DSG_DOME_SCREENSHOTS+'/cupola-closed.png'});
  state='OPEN';await refresh();await view('section');assert.equal(await stage.getAttribute('data-dsg-view-mode'),'auto');
  if(process.env.DSG_DOME_SCREENSHOTS)await stage.screenshot({path:process.env.DSG_DOME_SCREENSHOTS+'/cupola-open.png'});
  await p.locator('[data-dsg-scene-view="top"]').click();await view('top');assert.match(await stage.locator('.dsg-scene__status').innerText(),/Vista libera/);
  await refresh();await view('top'); // Unchanged snapshots do not cancel manual inspection.
  await p.locator('[data-dsg-follow-dome]').click();await view('section');
  state='CLOSED';await refresh();await view('exterior');
  stale=true;await refresh();await view('neutral');assert.match(await p.locator('[data-observatory-status="dome-state"]').first().innerText(),/UNKNOWN/);
  if(process.env.DSG_DOME_SCREENSHOTS)await stage.screenshot({path:process.env.DSG_DOME_SCREENSHOTS+'/cupola-unknown.png'});
  await p.locator('[data-dsg-scene-mode]').click();state='OPEN';stale=false;await refresh();
  await p.waitForFunction(()=>document.querySelector('[data-dsg-dome-sync]').dataset.dsgObservedDome==='OPEN');
  await p.locator('[data-dsg-scene-mode]').click();await view('section');assert.equal(await stage.locator('canvas').count(),1);
  state='OPENING';await refresh();await view('neutral');
  await p.setViewportSize({width:390,height:844});assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
  await p.goto(base+'operations/');assert.equal(await p.locator('[data-dsg-follow-dome]').count(),0);
  await p.goto(base+'status/');await stage.scrollIntoViewIfNeeded();await view('neutral');assert.equal(await stage.locator('canvas').count(),1);
  assert.deepEqual(errors,[]);console.log('PASS dome badge sync: CLOSED/OPEN/stale/UNKNOWN, manual/auto, unchanged refresh, essential resume, navigation/mobile.');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
