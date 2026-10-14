const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require('playwright');
const base = process.env.DSG_TEST_BASE_URL || 'http://127.0.0.1:8766/';
const camera = 'https://digitalstargate.freeddns.it:23232/dome-camera/';
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.DSG_BROWSER_CHANNEL ? {channel:process.env.DSG_BROWSER_CHANNEL} : {})});
  const page = await browser.newPage({viewport:{width:1007,height:828}});
  const errors = []; page.on('pageerror', error => errors.push(error.message));
  let available = true, badUrl = false, requests = 0, dome = 'UNKNOWN';
  await page.clock.install({time:Date.now()});
  await page.route('**/*', async route => {
    const url = route.request().url();
    if (url === camera + 'status.json') {
      requests++; const now = await page.evaluate(() => Date.now());
      return route.fulfill({json:{schemaVersion:'1.0',kind:'DSG_DOME_CAMERA_PUBLIC_V1',
        state:available ? 'CURRENT' : 'UNAVAILABLE', receivedAt:available ? new Date(now).toISOString() : null,
        freshUntil:available ? new Date(now + 8000).toISOString() : null, sequence:requests,
        frameUrl:camera+'frame.jpg', streamUrl:badUrl ? 'https://example.com/secret' : camera+'live.mjpg',
        commandAuthority:false,safetyAuthority:false,audio:false}});
    }
    if (url.startsWith(camera+'live.mjpg')) return route.fulfill({contentType:'image/png', body:fs.readFileSync('docs/assets/images/dsg-brand-mark.png')});
    if (url.endsWith('/v1/observatory-status') || url.endsWith('/data/realtime/observatory-status.json')) {
      const now = await page.evaluate(() => Date.now());
      return route.fulfill({json:{quality:'CURRENT',fresh_until_utc:new Date(now+3600000).toISOString(),
        systems:{dome:{state:dome,quality:'CURRENT',fresh_until_utc:new Date(now+3600000).toISOString()}}}});
    }
    return new URL(url).origin === new URL(base).origin ? route.continue() : route.abort();
  });
  const stage = page.locator('[data-dsg-dome-camera]');
  const image = stage.locator('[data-dsg-camera-image]');
  const state = expected => page.waitForFunction(value => document.querySelector('[data-dsg-dome-camera]')?.dataset.dsgCameraState === value, expected);
  try {
    await page.goto(base+'status/'); await stage.scrollIntoViewIfNeeded();
    assert.equal(requests,0); // Unknown badge does not select or request the camera.
    await stage.locator('[data-dsg-scene-view="section"]').click();
    await state('ready'); assert(await image.isVisible());
    assert.match(await stage.getAttribute('aria-label'),/TVCC/);
    assert.match(await stage.locator('.dsg-scene__status').innerText(),/senza audio/);
    const badge = await page.locator('[data-observatory-status="dome-state"]').first().innerText();
    available = false; await page.clock.fastForward(2001); await state('unavailable');
    assert(!(await image.isVisible())); assert.equal(await image.getAttribute('src'),null);
    assert.equal(await page.locator('[data-observatory-status="dome-state"]').first().innerText(),badge);
    available = true; await page.clock.fastForward(2001); await state('ready');
    badUrl = true; await page.clock.fastForward(2001); await state('unavailable');
    badUrl = false; await page.clock.fastForward(2001); await state('ready');
    await stage.locator('[data-dsg-scene-view="top"]').click();
    const count = requests; await page.clock.fastForward(6001); assert.equal(requests,count);
    assert.equal(await image.getAttribute('src'),null);
    dome = 'OPEN'; await stage.locator('[data-dsg-follow-dome]').click();
    await page.clock.fastForward(15001); await state('ready');
    assert.equal(await stage.getAttribute('data-dsg-view-mode'),'auto');
    await stage.locator('[data-dsg-scene-mode]').click();
    await state('unavailable'); const paused = requests;
    await page.clock.fastForward(6001); assert.equal(requests,paused);
    await stage.locator('[data-dsg-scene-mode]').click(); await state('ready');
    await page.setViewportSize({width:390,height:844});
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth+2));
    await page.goto(base+'operations/'); const left = requests;
    await page.clock.fastForward(6001); assert.equal(requests,left);
    assert.deepEqual(errors,[]);
    console.log('PASS public dome camera: manual/automatic view, privacy contract, withdrawal/recovery, no badge authority, pause, mobile, navigation.');
  } finally { await browser.close(); }
})().catch(error => {console.error(error);process.exitCode=1;});
