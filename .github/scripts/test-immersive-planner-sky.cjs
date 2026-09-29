const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require('playwright');
const base = process.env.DSG_TEST_BASE_URL || 'http://127.0.0.1:8766/digital-stargate-manual/';
const original = JSON.parse(fs.readFileSync('docs/data/observation-planner-f9-current-night.json', 'utf8'));
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.DSG_BROWSER_CHANNEL ? {channel:process.env.DSG_BROWSER_CHANNEL} : {})});
  const page = await browser.newPage({viewport:{width:1157,height:828}});
  const errors = []; page.on('pageerror', e => errors.push(e.message));
  // Use the governed fixture's own run time so scheduled data refreshes cannot stale this test.
  const now = Date.parse(original.generatedAtUtc);
  await page.clock.install({time:now});
  let fixture, unavailable=false, imageError=false, requests=0;
  await page.route('**/*', route => {
    const url = route.request().url();
    if(url.includes('/data/observation-planner-f9-current-night.json')) {
      requests++; return unavailable ? route.fulfill({status:503,body:'unavailable'}) : route.fulfill({json:fixture});
    }
    if(imageError && url.includes('/assets/images/planner-sky/')) return route.fulfill({status:404,body:''});
    return new URL(url).origin === new URL(base).origin ? route.continue() : route.abort();
  });
  const sky = page.locator('[data-weather-sky]');
  async function scenario(state, mutate=()=>{}) {
    fixture=structuredClone(original);
    fixture.hourly.forEach(row=>{row.weather.cloudCoverPct=0;row.weather.precipitationMm=0;});
    mutate(fixture); requests=0;
    await page.goto(base+'observation-planner/');
    await page.waitForFunction(s=>document.querySelector('[data-weather-sky]')?.dataset.skyState===s,state);
    if(state==='unknown') await page.waitForFunction(()=>document.querySelector('[data-sky-title]').textContent.includes('non disponibile'));
    else if(!imageError) await page.waitForFunction(()=>document.querySelector('[data-weather-sky] img').naturalWidth>0);
    assert.equal(requests,1,'no second forecast fetch');
    if(process.env.DSG_SKY_SCREENSHOTS && state!=='unknown' && !imageError) await sky.screenshot({path:process.env.DSG_SKY_SCREENSHOTS+'/planner-sky-'+state+'.png'});
  }
  try {
    await scenario('clear');
    assert.match(await sky.innerText(),/Nuvole medie 0,0%/);
    await scenario('clear', d=>d.hourly.forEach(r=>r.weather.cloudCoverPct=20));
    await scenario('cloudy', d=>d.hourly.forEach(r=>r.weather.cloudCoverPct=75));
    await scenario('rain', d=>d.hourly[0].weather.precipitationMm=0.01);
    assert.match(await sky.innerText(),/Pioggia totale 0,010 mm/);
    assert.match(await sky.innerText(),new RegExp(`1/${original.hourly.length} campioni`));
    await page.setViewportSize({width:390,height:844});
    assert(await sky.isVisible()); assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
    await scenario('unknown', d=>d.hourly.pop());
    await scenario('unknown', d=>d.hourly[1].validAtUtc=d.hourly[0].validAtUtc);
    await scenario('unknown', d=>d.hourly[0].weather.cloudCoverPct=null);
    await scenario('unknown', d=>d.hourly[0].weather.precipitationMm=-1);
    await scenario('unknown', d=>d.forecast.freshnessState='STALE');
    unavailable=true; await scenario('unknown'); unavailable=false;
    imageError=true; await scenario('clear');
    await page.waitForFunction(()=>document.querySelector('[data-weather-sky]').dataset.skyImage==='unavailable');
    assert(await sky.locator('img').isHidden()); assert.match(await sky.innerText(),/Nuvole medie/); imageError=false;
    await scenario('clear');
    const expiry = Math.min(Date.parse(fixture.nightWindow.toUtcExclusive), Date.parse(fixture.forecast.runInitialisationUtc)+18*3600000+1);
    await page.clock.fastForward(expiry-now+10);
    assert.equal(await sky.getAttribute('data-sky-state'),'unknown');
    assert.equal(await sky.locator('img').getAttribute('src'),null);
    assert.deepEqual(errors,[]);
    console.log('PASS planner sky: clear/cloud/rain, average boundary, precipitation priority, single fetch, mobile, missing/duplicate/invalid/stale data, unavailable image, expiry.');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
