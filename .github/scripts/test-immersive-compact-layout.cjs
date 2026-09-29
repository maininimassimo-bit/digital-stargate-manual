const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const base = process.env.DSG_TEST_BASE_URL || 'http://127.0.0.1:8766/digital-stargate-manual/';
(async () => {
 const browser = await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL ? {channel:process.env.DSG_BROWSER_CHANNEL} : {})});
 try {
  const page = await browser.newPage({viewport:{width:1157,height:900},colorScheme:'dark'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',route=>new URL(route.request().url()).origin===new URL(base).origin?route.continue():route.abort());
  const data=await (await page.request.get(base+'data/roadmap.json')).json();
  await page.goto(base+'roadmap/');
  const meter=page.getByRole('meter',{name:'Avanzamento roadmap'});await meter.waitFor();
  assert.equal(await meter.getAttribute('aria-valuenow'),String(data.summary.percentCompleted));
  assert((await meter.getAttribute('aria-valuetext')).includes(`${data.summary.completed} completati`));
  const full=page.locator('.dsg-roadmap-summary__long');
  assert.equal(await full.nth(0).locator('p').textContent(),data.projectStatus);
  assert.equal(await full.nth(1).locator('p').textContent(),data.target);
  await full.nth(0).locator('summary').focus();await page.keyboard.press('Enter');
  assert(await full.nth(0).locator('p').isVisible(),'Full project status is keyboard accessible');
  await full.nth(0).locator('summary').press('Enter');
  const items=data.waves.flatMap(w=>w.items), cards=page.locator('.dsg-roadmap-card');
  assert.equal(await cards.count(),items.length);
  for(let i=0;i<items.length;i++){
   const card=cards.nth(i),item=items[i];
   assert.equal(await card.locator('h3').textContent(),item.title);
   assert((await card.getAttribute('class')).includes(`is-${item.status}`));
   if(item.note)assert.equal(await card.locator('details p').textContent(),item.note);
  }
  for(const width of [1440,1157,768,390]){
   await page.setViewportSize({width,height:900});
   for(const scheme of ['slate','default']){
    await page.evaluate(s=>window.DSGThemeService.setTheme(s==='slate'?'dark':'light'),scheme);
    await page.waitForFunction(s=>document.body.dataset.mdColorScheme===s,scheme);
    await page.waitForTimeout(200);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`No overflow ${width} ${scheme}`);
    const hero=await page.locator('.dsg-roadmap-hero').boundingBox();assert(hero.height<900,'Collapsed summary remains compact');
    if(process.env.DSG_COMPACT_SCREENSHOTS)await page.locator('.dsg-roadmap-overview').screenshot({path:`${process.env.DSG_COMPACT_SCREENSHOTS}/roadmap-${width}-${scheme}.png`});
   }
  }
  // Empty governed summary must not invent a visible completed segment.
  await page.route('**/data/roadmap.json',r=>r.fulfill({json:{...data,summary:{total:0,completed:0,active:0,planned:0,percentCompleted:0}}}));
  await page.reload();await meter.waitFor();assert.equal(await meter.getAttribute('aria-valuenow'),'0');
  const widths=await page.locator('.dsg-roadmap-meter__rail i').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().width));
  assert(widths.every(w=>w===0),'Zero values have zero graphical width');
  await page.goto(base+'observation-planner/');
  for(const width of [1157,768,390]){
   await page.setViewportSize({width,height:900});await page.locator('.dsg-scene').scrollIntoViewIfNeeded();await page.waitForTimeout(600);
   const sky=await page.locator('.dsg-weather-sky').boundingBox(),atlas=await page.locator('.dsg-scene').boundingBox();
   if(width>700){assert(Math.abs(sky.y-atlas.y)<2,'Aligned top');assert(Math.abs(sky.height-atlas.height)<2,'Aligned bottom');}
   else assert(atlas.y>=sky.y+sky.height,'Stacked mobile cards');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  }
  assert.deepEqual(errors,[]);console.log('PASS: governed roadmap values and full text retained, keyboard details, responsive light/dark, aligned Planner.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
