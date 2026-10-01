const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const contract = require('../../docs/javascripts/bkl049-workflow-contract.js');
let base = process.env.DSG_TEST_BASE_URL || 'http://127.0.0.1:8766/';
const result = spawnSync('python', ['-c', 'import json; from tools.pixinsight.workflow_archive.test_public_projection import candidate,selection_for,project; b=candidate(); print(json.dumps(project(b,selection_for(b))))'], {encoding:'utf8',timeout:10000,maxBuffer:1024*1024});
assert.equal(result.status,0,result.stderr);
const record = JSON.parse(result.stdout);
const attack = '</pre><img src=x onerror="globalThis.__bkl049Executed=true">';
record.steps[0].parameters[0].lexicalJson = JSON.stringify(attack);
const makeCollection = () => {
  const now = Math.floor(Date.now()/1000)*1000;
  return {schemaVersion:'1.0',kind:'BKL049_PUBLIC_COLLECTION',authority:'processing_evidence',actionAuthority:'NONE',
    publishedAt:new Date(now-1000).toISOString().replace('.000Z','Z'),
    validUntil:new Date(now+60000).toISOString().replace('.000Z','Z'),records:[structuredClone(record)]};
};
(async()=>{
  let server, browser;
  try {
    if (process.env.DSG_TEST_SITE) {
      const root=path.resolve(process.env.DSG_TEST_SITE);
      server=http.createServer((request,response)=>{
        let file;
        try {
          file=path.resolve(root,'.'+decodeURIComponent(new URL(request.url,'http://localhost').pathname));
          if (!file.startsWith(root+path.sep) && file!==root) throw new Error('outside');
          if(fs.statSync(file).isDirectory()) file=path.join(file,'index.html');
          const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png'};
          response.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');
          fs.createReadStream(file).on('error',()=>response.destroy()).pipe(response);
        } catch {response.writeHead(404);response.end();}
      });
      await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
      base=`http://127.0.0.1:${server.address().port}/`;
    }
    browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
    const page=await browser.newPage(), errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    let collection=makeCollection(), unavailable=false, requests=0;
    await page.route('**/*',route=>{
      const url=new URL(route.request().url());
      if(url.pathname.endsWith('/data/bkl049-public-workflows.json')) {
        requests++;return unavailable?route.abort():route.fulfill({contentType:'application/json',body:contract.canonical(collection)});
      }
      return url.origin===new URL(base).origin?route.continue():route.abort();
    });
    const panel=page.locator('[data-bkl049-workflows]');
    const status=panel.locator('[data-workflow-status]');
    const waitRecord=async()=>{await page.waitForFunction(()=>document.querySelectorAll('.dsg-workflow-card').length===1);};
    const waitUnavailable=async()=>{await page.waitForFunction(()=>document.querySelector('[data-workflow-status]')?.textContent.startsWith('Workflow non disponibile'));assert.equal(await panel.locator('.dsg-workflow-card').count(),0);};
    await page.goto(base+'scientific-image-gallery/');await waitRecord();
    assert.match(await status.innerText(),/Ordine esportato/);
    assert.match(await panel.innerText(),/DECLARED \/ PARTIAL/);
    await panel.locator('summary').focus();await page.keyboard.press('Enter');
    assert.equal(await panel.locator('details').getAttribute('open'),'');
    assert.equal(await panel.locator('pre').textContent(),JSON.stringify(attack));
    assert.equal(await panel.locator('img').count(),0);
    assert.equal(await page.evaluate(()=>globalThis.__bkl049Executed),undefined);
    const exact=await panel.getByRole('link',{name:/Collegamento esatto/}).getAttribute('href');
    await page.goto(exact);await waitRecord();
    await page.reload();await waitRecord();
    await page.goto(exact.replace('version=VER-synthetic-1','version=VER-wrong'));await waitUnavailable();
    await page.goto(exact+'&workflow=WF-duplicate');await waitUnavailable();
    await page.goto(base+'scientific-image-gallery/');await waitRecord();
    const before=requests;
    await page.evaluate(()=>window.DSG.components.run('synthetic-instant-navigation'));
    await waitRecord();assert.ok(requests>before);
    await panel.locator('summary').focus();await page.keyboard.press('Enter');
    for (const width of [390,1440]) {
      await page.setViewportSize({width,height:900});
      assert.ok(await panel.evaluate(node=>node.scrollWidth<=node.clientWidth+2),'no horizontal panel overflow');
      if(width===390 && process.env.DSG_TEST_SCREENSHOT) await panel.screenshot({path:process.env.DSG_TEST_SCREENSHOT.replace('.png','-mobile.png')});
    }
    await page.evaluate(()=>document.body.setAttribute('data-md-color-scheme','slate'));
    await panel.locator('summary').focus();
    assert.notEqual(await panel.locator('summary').evaluate(node=>getComputedStyle(node).outlineStyle),'none');
    if(process.env.DSG_TEST_SCREENSHOT) await page.screenshot({path:process.env.DSG_TEST_SCREENSHOT,fullPage:true});
    unavailable=true;await panel.locator('[data-workflow-refresh]').click();await waitUnavailable();
    unavailable=false;collection=makeCollection();collection.records.push(structuredClone(record));
    await panel.locator('[data-workflow-refresh]').click();await waitUnavailable();
    collection={...makeCollection(),publishedAt:null,validUntil:null,records:[]};
    await panel.locator('[data-workflow-refresh]').click();await waitUnavailable();
    collection=makeCollection();await page.clock.install({time:Date.now()});
    await panel.locator('[data-workflow-refresh]').click();await waitRecord();
    await page.clock.fastForward(61000);await waitUnavailable();
    assert.deepEqual(errors,[]);
    const nojs=await browser.newPage({javaScriptEnabled:false});
    await nojs.route('**/*',route=>new URL(route.request().url()).origin===new URL(base).origin?route.continue():route.abort());
    await nojs.goto(base+'scientific-image-gallery/');
    assert.equal(await nojs.locator('.dsg-workflow-card').count(),0);
    assert.match(await nojs.locator('[data-bkl049-workflows]').innerText(),/occorre JavaScript/);
    console.log('PASS BKL049 browser: exact triple/deep refresh, wrong/duplicate refs, text-only XSS, keyboard, mobile/dark, lifecycle, offline/withdrawal/expiry and no-JS.');
  } finally {await browser?.close();if(server){server.closeAllConnections();await new Promise(resolve=>server.close(resolve));}}
})().catch(error=>{console.error(error);process.exitCode=1;});
