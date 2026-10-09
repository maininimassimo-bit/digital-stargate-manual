/* Browser integration regression: same origin assets, no calls to live providers. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require('playwright');
const base = process.env.DSG_TEST_BASE_URL || 'http://127.0.0.1:8766/digital-stargate-manual/';
const routes = Object.keys(JSON.parse(fs.readFileSync('overrides/main.html', 'utf8').match(/set scenes = (.+) %}/)[1]));

(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.DSG_BROWSER_CHANNEL ? { channel: process.env.DSG_BROWSER_CHANNEL } : {}) });
  const errors = [];
  async function page(options = {}) {
    const p = await browser.newPage(options);
    p.on('pageerror', error => errors.push(error.message));
    await p.route('**/*', route => new URL(route.request().url()).origin === new URL(base).origin ? route.continue() : route.abort());
    await p.route('https://digitalstargate.freeddns.it:23232/current/image.jpg*', route => route.fulfill({ contentType: 'image/jpeg', body: fs.readFileSync('docs/assets/images/osservatorio-hero.jpg') }));
    return p;
  }
  try {
    for (const viewport of [{ width: 1440, height: 1000 }, { width: 390, height: 844 }]) {
      const p = await page({ viewport, colorScheme: 'dark' });
      for (const route of routes) {
        console.log(`Checking ${route} / ${viewport.width}`);
        await p.goto(base + route.replace(/index\.md$/, ''));
        const stage = p.locator('[data-dsg-scene]');
        await stage.scrollIntoViewIfNeeded();
        try { await p.waitForFunction(() => document.querySelector('[data-dsg-scene]').dataset.dsgSceneState === 'ready'); }
        catch (error) { console.error(await stage.getAttribute('data-dsg-scene-state'), await stage.locator('.dsg-scene__status').textContent(), await stage.evaluate(e=>e.getBoundingClientRect().toJSON()), errors); fs.mkdirSync('artifacts',{recursive:true}); await p.screenshot({path:'artifacts/portal-test-failure.png'}); throw error; }
        assert.equal(await p.locator('.md-content h1').count(), 1, route);
        assert(await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Horizontal overflow: ${route} at ${viewport.width}`);
        assert.equal(await stage.locator('canvas').count(), 1);
      }
      await p.close();
      console.log(`PASS: ${routes.length} scene routes at ${viewport.width}px`);
    }
    const p = await page({ viewport: { width: 1440, height: 1000 }, colorScheme: 'light' });
    await p.goto(base + 'status/');
    const stage = p.locator('[data-dsg-scene]');await stage.scrollIntoViewIfNeeded();
    await p.waitForFunction(() => document.querySelector('[data-dsg-scene]').dataset.dsgSceneState === 'ready');
    const bindingSnapshot = () => p.locator('[data-observatory-status], [data-eagle-health], [data-bkl036-score]').allTextContents();
    const before = await bindingSnapshot();
    for (const view of ['exterior', 'top', 'section']) {
      await p.locator(`[data-dsg-scene-view="${view}"]`).click();
      assert.equal(await p.locator(`[data-dsg-scene-view="${view}"]`).getAttribute('aria-pressed'), 'true');
    }
    assert.deepEqual(await bindingSnapshot(), before, 'Visual controls must not change telemetry.');
    await p.locator('[data-dsg-scene-mode]').click();
    assert.equal(await stage.getAttribute('data-dsg-scene-state'), 'essential');
    await p.reload();assert.equal(await p.locator('[data-dsg-scene]').getAttribute('data-dsg-scene-state'), 'essential');
    await p.locator('[data-dsg-scene-mode]').click();await p.waitForFunction(() => document.querySelector('[data-dsg-scene]').dataset.dsgSceneState === 'ready');
    // Rapid teardown/remount must not leave multiple canvases or stale async mounts.
    for(let i=0;i<4;i++) await p.locator('[data-dsg-scene-mode]').click();
    await p.waitForFunction(() => document.querySelector('[data-dsg-scene]').dataset.dsgSceneState === 'ready');
    assert.equal(await p.locator('[data-dsg-scene] canvas').count(),1);
    await p.goto(base+'chapters/01-introduzione/');assert.equal(await p.locator('[data-dsg-scene]').count(),0);
    assert.equal(await p.locator('.dsg-breadcrumb').count(),1);
    await p.locator('[data-dsg-search]').click();await p.locator('.md-search__input').fill('cupola');
    await p.waitForFunction(()=>document.querySelector('#__search').checked);await p.keyboard.press('Escape');
    assert.equal(await p.locator('#__search').isChecked(),false);
    const reduced=await page({reducedMotion:'reduce'});const requests=[];reduced.on('request',r=>requests.push(r.url()));
    await reduced.goto(base);await reduced.waitForTimeout(500);
    assert(!requests.some(url=>url.includes('/vendor/three-')||url.includes('immersive-renderer')), 'Reduced motion must not download WebGL.');
    const offline=await page();await offline.route('**/assets/vendor/three-*/**',r=>r.abort());await offline.goto(base);
    await offline.goto(base+'mission-control/');await offline.locator('[data-dsg-scene]').scrollIntoViewIfNeeded();
    await offline.waitForFunction(()=>document.querySelector('[data-dsg-scene]').dataset.dsgSceneState==='unavailable');
    assert(await offline.locator('.dsg-domain-card').count()===6);
    const nojs=await page({javaScriptEnabled:false});await nojs.goto(base+'status/');
    assert((await nojs.locator('[data-observatory-status="quality"]').innerText()).includes('UNKNOWN'));
    assert.equal(await nojs.locator('[data-dsg-scene-mode]').isVisible(),false);
    assert.deepEqual([...new Set(errors)],[]);
    console.log('PASS: light theme, data invariance, view controls, essential preference/remount, document mode, search/Escape, reduced-motion, blocked WebGL and no-JS fallback.');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
