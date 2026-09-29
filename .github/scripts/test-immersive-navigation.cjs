const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base=process.env.DSG_TEST_BASE_URL||'http://127.0.0.1:8766/digital-stargate-manual/';
(async()=>{
 const b=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
 try{
  const p=await b.newPage({viewport:{width:1157,height:828},colorScheme:'dark'}), errors=[];
  p.on('pageerror',e=>errors.push(e.message));
  await p.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
  await p.goto(base+'scientific-platform/');
  const links=p.locator('.dsg-section-nav');
  for(const label of ['Observation Planner','Report delle sessioni']) assert(await links.getByRole('link',{name:label,exact:true}).isVisible());
  await links.getByRole('link',{name:'Observation Planner',exact:true}).click();
  const stage=p.locator('[data-dsg-scene]');await stage.scrollIntoViewIfNeeded();await p.waitForSelector('.dsg-scene.is-ready');
  for(const width of [1157,1440,768,390]){
   await p.setViewportSize({width,height:900});await stage.scrollIntoViewIfNeeded();await p.waitForTimeout(1000);
   const metrics=await stage.evaluate(e=>{const c=e.querySelector('canvas').getBoundingClientRect(),h=e.querySelector('.dsg-scene__heading').getBoundingClientRect(),t=e.querySelector('.dsg-scene__toolbar').getBoundingClientRect();return {top:c.top,heading:h.bottom,bottom:c.bottom,toolbar:t.top,height:c.height};});
   assert(metrics.top>=metrics.heading && metrics.bottom<=metrics.toolbar && metrics.height>100,'Dedicated atlas viewport avoids headings and controls');
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   await p.locator('[data-dsg-scene-view="top"]').click();await p.locator('[data-dsg-scene-view="section"]').click();
   await p.waitForTimeout(1000);
   if(process.env.DSG_NAV_SCREENSHOTS)await stage.screenshot({path:process.env.DSG_NAV_SCREENSHOTS+`/atlas-fit-${width}.png`});
  }
  await p.goto(base+'portal-map/');
  const map=p.locator('#dsg-portal-directory');
  assert(await map.locator('a').count()>800);
  await map.getByText('Scienza e Analytics',{exact:true}).click();
  assert(await map.getByRole('link',{name:'Observation Planner',exact:true}).isVisible());
  await map.getByRole('link',{name:'Observation Planner',exact:true}).click();assert(p.url().includes('/observation-planner/'));
  const plain=await b.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});
  await plain.goto(base+'scientific-platform/');assert(await plain.locator('.dsg-section-nav').getByRole('link',{name:'Observation Planner',exact:true}).isVisible());
  await plain.locator('.dsg-section-nav').getByRole('link',{name:'Mappa completa del portale →',exact:true}).click();
  await plain.locator('#dsg-portal-directory').getByText('Osservatorio',{exact:true}).click();
  assert(await plain.locator('#dsg-portal-directory').getByRole('link',{name:'Report delle sessioni',exact:true}).isVisible());
  assert.deepEqual(errors,[]);console.log('PASS: section links, atlas desktop/tablet/mobile viewport, directory navigation, no-JS navigation.');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
