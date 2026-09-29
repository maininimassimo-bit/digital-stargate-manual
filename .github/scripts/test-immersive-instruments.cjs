const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const base = process.env.DSG_TEST_BASE_URL || 'http://127.0.0.1:8766/digital-stargate-manual/';
const now = Date.now(), fresh = new Date(now + 3600000).toISOString(), past = new Date(now - 3600000).toISOString();
const signal = data => ({quality:'CURRENT',state:'OBSERVED',fresh_until_utc:fresh,data});
const eagle = {component:'DSG.EagleHealthPortalProjection',quality:'CURRENT',fresh_until_utc:fresh,summary:{state:'HEALTHY',reason:'TEST_FIXTURE'},signals:{cpu:signal({load_pct:10}),memory:signal({available_ratio:.664}),storage:signal({logical_disks:[{device_id:'C:',free_pct:20},{device_id:'D:',free_pct:47}]}),uptime:signal({}),time_sync:signal({last_successful_sync_utc:new Date(now).toISOString()})}};
const observatory = {quality:'CURRENT',fresh_until_utc:fresh,systems:{weather:{quality:'CURRENT',fresh_until_utc:fresh,temperature_c:20,dew_point_c:6.2,wind_speed_kmh:1.3,wind_gust_kmh:3.8,humidity_pct:43.7,cloud_cover_pct:0,rain_rate_mm_h:0},dome:{state:'CLOSED',quality:'CURRENT',fresh_until_utc:fresh},mount:{state:'UNKNOWN',quality:'CURRENT',fresh_until_utc:fresh},camera:{state:'UNKNOWN',quality:'CURRENT',fresh_until_utc:fresh},power:{state:'MAINS_PRESENT',quality:'CURRENT',fresh_until_utc:fresh},network:{state:'ONLINE',quality:'CURRENT',fresh_until_utc:fresh}}};
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
 const errors=[];let e=structuredClone(eagle),o=structuredClone(observatory),offline=false;
 const p=await browser.newPage({viewport:{width:1157,height:828},colorScheme:'dark'});
 await p.clock.install({time:now});
 p.on('pageerror',error=>errors.push(error.message));
 await p.route('**/*',route=>{
  const url=route.request().url();
  if(/\/v1\/(eagle-health|observatory-status)$|\/data\/realtime\/(eagle-health|observatory-status)\.json$/.test(url)) return offline?route.abort():route.fulfill({json:url.includes('eagle-health')?e:o});
  return new URL(url).origin===new URL(base).origin?route.continue():route.abort();
 });
 const card=name=>p.locator('.dsg-instrument').filter({has:p.getByRole('heading',{name,exact:true})});
 async function load(){await p.goto(base+'status/');await p.waitForFunction(()=>document.querySelectorAll('.dsg-instrument').length===17);}
 try {
  await load();
  assert.equal(await card('CPU load').getAttribute('data-instrument-value'),'10');
  assert.equal(await card('Memoria disponibile').getAttribute('data-instrument-ratio'),'0.664');
  assert.equal(await card('Storage C:').getAttribute('data-instrument-tone'),'good');
  assert.equal(await card('Nuvolosità').getAttribute('data-instrument-value'),'0');
  assert.equal(await card('Montatura').getAttribute('data-instrument-tone'),'unknown');
  assert.equal(await card('Montatura').getAttribute('data-instrument-ratio'),null);
  for(const panel of await p.locator('.dsg-instrument-panel').all()) {await panel.scrollIntoViewIfNeeded();await panel.waitFor({state:'visible'});await p.waitForFunction(el=>el.dataset.instrumentsState==='ready',await panel.elementHandle());assert.equal(await panel.locator('canvas').count(),1);}
  const before=await p.locator('.dsg-instrument__value').allTextContents();
  await p.locator('[data-instruments-mode]').click();assert.equal(await p.locator('.dsg-instrument-panel canvas').count(),0);assert.deepEqual(await p.locator('.dsg-instrument__value').allTextContents(),before);
  await p.locator('[data-instruments-mode]').click();
  for(let n=0;n<4;n++)await p.locator('[data-instruments-mode]').click();
  await p.locator('.dsg-instrument-panel').first().scrollIntoViewIfNeeded();await p.waitForSelector('.dsg-instrument-panel.is-instruments-ready');
  assert(await p.locator('.dsg-instrument-panel canvas').count()<=3);
  e.signals.cpu.data.load_pct=11;await p.clock.fastForward(15001);await p.waitForFunction(()=>document.querySelector('[data-instrument-type="dial"]').dataset.instrumentValue==='11');
  assert(await p.locator('.dsg-instrument-panel canvas').count()<=3);
  offline=true;await p.clock.fastForward(15001);await p.waitForFunction(()=>document.querySelector('[data-instrument-type="dial"]').dataset.instrumentValue==='');offline=false;
  await p.setViewportSize({width:390,height:844});await p.waitForTimeout(100);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
  await p.emulateMedia({colorScheme:'light'});
  // Boundary and missing values: null must never become zero/green.
  e.signals.cpu.data.load_pct=90;e.signals.memory.data.available_ratio=null;o.systems.weather.rain_rate_mm_h=.1;o.systems.weather.temperature_c=9.2;o.systems.weather.dew_point_c=6.2;
  await load();assert.equal(await card('CPU load').getAttribute('data-instrument-tone'),'good');assert.equal(await card('Memoria disponibile').getAttribute('data-instrument-tone'),'unknown');assert.match(await card('Memoria disponibile').innerText(),/UNKNOWN/);assert.equal(await card('Pioggia').getAttribute('data-instrument-tone'),'bad');assert.equal(await card('Margine dew point').getAttribute('data-instrument-tone'),'bad');
  e.signals.cpu.data.load_pct=91;e.signals.storage.data.logical_disks[0].free_pct=19.9;o.systems.weather.wind_speed_kmh=40;
  await load();assert.equal(await card('CPU load').getAttribute('data-instrument-tone'),'bad');assert.equal(await card('Storage C:').getAttribute('data-instrument-tone'),'bad');assert.match(await card('Vento medio').innerText(),/fuori scala/);
  // Expired signals and envelope must suppress state and fill.
  e.fresh_until_utc=past;o.systems.dome.fresh_until_utc=past;o.systems.weather.fresh_until_utc=past;
  await load();assert.equal(await card('Uptime').getAttribute('data-instrument-state'),'UNKNOWN');assert.equal(await card('Cupola').getAttribute('data-instrument-state'),'UNKNOWN');assert.equal(await card('CPU load').getAttribute('data-instrument-value'),'');assert.equal(await card('Vento medio').getAttribute('data-instrument-value'),'');
  o=structuredClone(observatory);o.fresh_until_utc=past;await load();assert.equal(await card('Cupola').getAttribute('data-instrument-state'),'UNKNOWN');assert.equal(await card('Vento medio').getAttribute('data-instrument-value'),'');
  offline=true;await load();assert.equal(await card('CPU load').getAttribute('data-instrument-tone'),'unknown');
  // Static fallback survives renderer failure with all values accessible.
  offline=false;e=structuredClone(eagle);o=structuredClone(observatory);await p.route('**/immersive-instruments.mjs',route=>route.abort());await load();await p.locator('.dsg-instrument-panel').first().scrollIntoViewIfNeeded();await p.waitForFunction(()=>document.querySelector('.dsg-instrument-panel').dataset.instrumentsState==='unavailable');assert.equal(await card('CPU load').getAttribute('data-instrument-value'),'10');
  await p.emulateMedia({reducedMotion:'reduce'});await load();assert.equal(await p.locator('.dsg-instrument-panel canvas').count(),0);assert.equal(await card('CPU load').getAttribute('data-instrument-value'),'10');
  await p.emulateMedia({reducedMotion:'no-preference'});await p.addInitScript(()=>{ const get=Storage.prototype.getItem,set=Storage.prototype.setItem; Storage.prototype.getItem=function(key){if(key==='dsg-immersive-essential')throw new Error('Preference storage disabled');return get.call(this,key);};Storage.prototype.setItem=function(key,value){if(key==='dsg-immersive-essential')throw new Error('Preference storage disabled');return set.call(this,key,value);}; });await load();await p.locator('[data-instruments-mode]').click();assert.equal(await p.locator('[data-instruments-mode]').getAttribute('aria-pressed'),'true');assert.equal(await p.locator('[data-dsg-scene-mode]').getAttribute('aria-pressed'),'true');
  assert.deepEqual(errors,[]);console.log('PASS instruments: 17 values, policy boundaries, null/zero, stale, offline, 3D, essential/remount, mobile, fallback.');
 } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
