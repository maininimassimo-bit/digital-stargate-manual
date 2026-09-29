const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('playwright');
const base=process.env.DSG_TEST_BASE_URL||'http://127.0.0.1:8766/digital-stargate-manual/';
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage(),original=JSON.parse(fs.readFileSync('docs/data/observation-planner-f9-current-night.json'));
  const run=Date.parse(original.forecast.runInitialisationUtc), now=run+18*3600000-120000;
  await page.clock.install({time:now});let fixture=structuredClone(original), requests=0;
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',r=>{
   if(r.request().url().includes('/data/observation-planner-f9-current-night.json')){requests++;return r.fulfill({json:fixture});}
   return new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort();
  });
  await page.goto(base+'observation-planner/');await page.waitForSelector('#dsg-f9-status');
  assert.match(await page.locator('.dsg-op-refresh-status').innerText(),/valido fino/);
  await page.clock.fastForward(120001);
  await page.waitForFunction(()=>document.querySelector('[data-observation-planner-f9]').textContent.includes('non disponibile'));
  assert.equal(await page.locator('#dsg-f9-results').count(),0,'stale advisory removed');
  assert.equal(await page.locator('[data-weather-sky]').getAttribute('data-sky-state'),'unknown');
  // New publication becomes available without reload; clock/fixtures never reach production.
  fixture=structuredClone(original);
  fixture.forecast.runInitialisationUtc=new Date(run+12*3600000).toISOString();
  fixture.forecast.retrievedAtUtc=fixture.generatedAtUtc=new Date(now+120001).toISOString();
  await page.clock.fastForward(300001);await page.waitForSelector('#dsg-f9-status');
  assert.notEqual(await page.locator('[data-weather-sky]').getAttribute('data-sky-state'),'unknown');
  await page.selectOption('#dsg-f9-status','NOT_YET_ACQUIRED');
  const before=requests;await page.clock.fastForward(300001);
  await page.waitForFunction(()=>document.querySelector('#dsg-f9-status')?.value==='NOT_YET_ACQUIRED');
  assert(requests>before,'poll checked the published projection');
  assert.deepEqual(errors,[]);
  console.log('PASS: exact expiry removes stale panels/sky, automatic recovery after publication, displayed validity, filter preservation.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
