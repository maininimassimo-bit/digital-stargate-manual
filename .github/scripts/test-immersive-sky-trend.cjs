const {chromium}=require('playwright');const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});try{
 const base=process.env.DSG_TEST_BASE_URL||'http://127.0.0.1:8766/digital-stargate-manual/';
 const page=await browser.newPage({viewport:{width:1157,height:900}});await page.clock.install();
 await page.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
 await page.goto(base+'session-comparison/');const chart=page.locator('.dsg-sky-chart');await chart.waitFor();
 const data=await(await page.request.get(base+'data/session-comparison-projection.json')).json();
 assert.equal(await chart.locator('[data-sky-point]').count(),data.includedSessions.length);
 await chart.locator('[data-sky-point]').first().focus();assert((await chart.locator('[data-sky-point]').first().getAttribute('aria-label')).includes('mag/arcsec'));
 for(const width of [1157,390]){await page.setViewportSize({width,height:900});for(const theme of ['dark','light']){await page.evaluate(t=>window.DSGThemeService.setTheme(t),theme);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}}
 if(process.env.DSG_SKY_SCREENSHOT){await page.setViewportSize({width:1157,height:900});await page.evaluate(()=>window.DSGThemeService.setTheme('dark'));await chart.screenshot({path:process.env.DSG_SKY_SCREENSHOT});}
 await page.route('**/data/session-comparison-projection.json',r=>r.fulfill({status:503,body:'unavailable'}));await page.clock.fastForward(300001);await page.locator('.dsg-sc-fail').waitFor();assert.equal(await chart.count(),0);
 console.log('PASS sky chart values, focus, responsive themes and automatic refresh failure');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
