const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('playwright');
const base=process.env.DSG_TEST_BASE_URL || 'http://127.0.0.1:8766/digital-stargate-manual/';
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:1157,height:900}}); const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.clock.install();
  await page.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
  await page.goto(base+'scientific-data-quality/');
  const chart=page.locator('[data-quality-trend]');
  await chart.locator('svg').waitFor();
  const catalog=JSON.parse(fs.readFileSync('site/data/scientific-session-catalog.json','utf8'));
  const projection=JSON.parse(fs.readFileSync('site/data/scientific-data-quality-projection.json','utf8'));
  const known=new Map(catalog.sessions.filter(s=>s.configurationId && s.configurationId!=='UNKNOWN').map(s=>[s.sessionId,s.configurationId]));
  const represented=projection.assessments.filter(a=>known.has(a.sessionId));
  const published=represented.filter(a=>a.projectionRecordState==='AVAILABLE');
  assert.equal(await chart.locator('[data-toggle]').count(),new Set(represented.map(a=>known.get(a.sessionId))).size);
  const plottedIds=await chart.locator('svg a').evaluateAll(links=>links.map(link=>new URL(link.href.baseVal || link.getAttribute('href'),document.baseURI).searchParams.get('sessionId')));
  assert.deepEqual(plottedIds.sort(),published.map(a=>a.sessionId).sort());
  assert.equal(await chart.locator('tbody tr').count(),represented.length);
  const first=chart.locator('svg a').first();await first.focus();
  assert((await chart.locator('.dsg-trend-readout').textContent()).includes('score'));
  await chart.locator('[data-toggle="0"]').click();
  assert.equal(await chart.locator('[data-toggle="0"]').getAttribute('aria-pressed'),'false');
  assert.equal(await chart.locator('[data-series="0"]').isVisible(),false);
  await chart.locator('[data-toggle="0"]').click();
  for(const width of [1440,1157,768,390]){
   await page.setViewportSize({width,height:900});
   for(const theme of ['dark','light']){
    await page.evaluate(t=>window.DSGThemeService.setTheme(t),theme);
    const a=await chart.boundingBox(),b=await page.locator('.dsg-dq-hero>.dsg-scene').boundingBox();
    if(width>700){assert(Math.abs(a.y-b.y)<2);assert(Math.abs(a.height-b.height)<2);}
    else assert(b.y>=a.y+a.height);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   }
  }
  if(process.env.DSG_TREND_SCREENSHOT){await page.setViewportSize({width:1157,height:1000});await page.evaluate(()=>window.DSGThemeService.setTheme('dark'));await page.locator('.dsg-dq-hero').screenshot({path:process.env.DSG_TREND_SCREENSHOT});}
  await page.route('**/data/scientific-data-quality-projection.json',r=>r.fulfill({status:503,body:'unavailable'}));
  await page.clock.fastForward(300001);await chart.locator('[role=alert]').waitFor();assert.equal(await chart.locator('svg').count(),0);
  assert.deepEqual(errors,[]);console.log('PASS quality trend: values, controls, keyboard, alignment, mobile, light/dark, fail-closed.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
