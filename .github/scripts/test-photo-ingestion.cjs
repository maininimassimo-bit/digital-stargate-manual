const assert=require('node:assert/strict');
const {createHash,randomBytes}=require('node:crypto');
const fs=require('node:fs'), path=require('node:path'), http=require('node:http');
const {spawn}=require('node:child_process');
const {chromium}=require('playwright');
const {SHA256}=require('../../docs/javascripts/photo-file-hash.js');
for(const length of [0,1,55,56,63,64,65,127,128,1000,4194305]){
  const bytes=randomBytes(length), expected=createHash('sha256').update(bytes).digest('hex');
  for(const size of [1,63,127,4194304]){
    if(length>100000 && size<127)continue;
    const hash=new SHA256();for(let i=0;i<bytes.length;i+=size)hash.update(bytes.subarray(i,i+size));assert.equal(hash.finish(),expected,`SHA256 size ${length} chunk ${size}`);
  }
}
(async()=>{
  const root=path.resolve(process.env.DSG_TEST_SITE || 'site');let child,browser,server;
  try{
    server=http.createServer((req,res)=>{try{let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep))throw Error();if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml'};res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');fs.createReadStream(file).pipe(res);}catch{res.writeHead(404);res.end();}});
    await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin=`http://127.0.0.1:${server.address().port}`;
    child=spawn(process.env.DSG_TEST_PYTHON || 'python',['.github/scripts/run-photo-ingestion-test-server.py'],{env:{...process.env,DSG_TEST_ORIGIN:origin},stdio:['ignore','pipe','pipe']});let stderr='';child.stderr.on('data',chunk=>stderr+=chunk);
    const fixture=await new Promise((resolve,reject)=>{let output='';const timer=setTimeout(()=>reject(Error('HTTP test server timed out: '+stderr)),15000);child.on('exit',code=>reject(Error('HTTP fixture exited '+code+stderr)));child.stdout.on('data',chunk=>{output+=chunk;if(output.includes('\n')){clearTimeout(timer);resolve(JSON.parse(output.split('\n')[0]));}});});
    const local=`http://127.0.0.1:${fixture.port}`;
    const unauthenticated=await fetch(local+'/v1/uploads',{method:'POST',headers:{Origin:origin,'Content-Type':'application/json'},body:'{}'});assert.equal(unauthenticated.status,403);
    const badOrigin=await fetch(local+'/v1/uploads',{method:'POST',headers:{Origin:'https://attacker.example',Authorization:'Bearer synthetic-owner-token','Content-Type':'application/json'},body:'{}'});assert.equal(badOrigin.status,403);
    browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
    const page=await browser.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
    await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
    await page.route('**/photo-ingestion-config.json',route=>route.fulfill({json:{schemaVersion:'1.0',serviceUrl:'https://photo-test.run.app',deploymentState:'SYNTHETIC_TEST'}}));
    await page.route('https://photo-test.run.app/**',async route=>{
      const request=route.request(),headers={...request.headers(),origin};delete headers.host;
      const response=await fetch(local+new URL(request.url()).pathname,{method:request.method(),headers,body:['GET','HEAD'].includes(request.method())?undefined:request.postDataBuffer()});
      await route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});
    });
    await page.route('https://accounts.google.com/gsi/client',route=>route.fulfill({contentType:'text/javascript',body:`window.google={accounts:{id:{initialize(value){window.testSignIn=value.callback;},renderButton(host){const button=document.createElement('button');button.textContent='Synthetic owner login';button.addEventListener('click',()=>window.testSignIn({credential:'synthetic-owner-token'}));host.append(button);}}}};`}));
    const catalog=JSON.parse(fs.readFileSync('docs/data/scientific-session-catalog.json'));const session=catalog.sessions[0];
    await page.goto(`${origin}/scientific-photo-upload/?sessionId=${encodeURIComponent(session.sessionId)}`);
    await page.getByText('Synthetic owner login',{exact:true}).click();try{await page.waitForFunction(()=>!document.querySelector('[data-photo-fields]').disabled);}catch(error){throw Error(error.message+' status: '+await page.locator('[data-photo-status]').textContent()+' errors: '+errors.join(';'));}
    assert.equal(await page.locator('[data-photo-sessions] input:checked').inputValue(),session.sessionId);
    await page.locator('[data-photo-title]').fill('Synthetic image <script>private</script>');await page.locator('[data-photo-date]').fill('2026-10-02');
    await page.locator('[data-photo-original]').setInputFiles({name:'synthetic.xisf',mimeType:'application/octet-stream',buffer:Buffer.from('XISF0100synthetic original')});
    await page.locator('[data-photo-preview]').setInputFiles({name:'synthetic.png',mimeType:'image/png',buffer:Buffer.from(fixture.preview,'base64')});
    await page.locator('[data-photo-workflow]').setInputFiles({name:'synthetic.js',mimeType:'text/plain',buffer:Buffer.from('var P = new PixelMath; P.expression = "private-path"; P.n = 0.25;')});
    await page.locator('[data-photo-attest]').check();await page.getByRole('button',{name:'Carica e verifica',exact:true}).focus();await page.keyboard.press('Enter');
    await page.locator('[data-photo-review]').waitFor({state:'visible'});await page.waitForFunction(()=>!document.querySelector('[data-photo-save]').disabled);
    assert.equal(await page.locator('[data-photo-steps] input[data-param]:checked').count(),0);
    assert.equal(await page.locator('[data-photo-review-image]').evaluate(image=>image.complete&&image.naturalWidth>0),true);
    await page.locator('[data-photo-save]').click();await page.getByText('Immagine e workflow salvati privatamente.',{exact:true}).waitFor();
    assert.equal((await (await fetch(local+'/v1/gallery')).json()).records.length,0);
    await page.locator('[data-photo-rights]').check();await page.locator('[data-photo-publish]').click();await page.getByText('Immagine e workflow pubblicati.',{exact:true}).waitFor();
    const collection=await (await fetch(local+'/v1/gallery')).json();assert.equal(collection.records.length,1);assert.equal(collection.records[0].steps[0].parameters.length,0);assert.equal(collection.records[0].validUntil,null);
    const previewUrl=collection.records[0].previewUrl;
    await page.goto(origin+'/scientific-image-gallery/');await page.locator('[data-session-photo-gallery] article').waitFor();
    assert.equal(await page.locator('[data-session-photo-gallery] article').count(),1);assert.equal(await page.locator('[data-session-photo-gallery] script').count(),0);
    assert.equal(await page.locator('[data-bkl034-gallery]').count(),0);
    await page.clock.setFixedTime(Date.now()+2*86400000);await page.locator('[data-gallery-reset]').click();await page.locator('[data-session-photo-gallery] article').waitFor();
    await page.evaluate(()=>document.body.setAttribute('data-md-color-scheme','slate'));
    if(process.env.DSG_TEST_OUTPUT)await page.screenshot({path:path.join(process.env.DSG_TEST_OUTPUT,'photo-ingestion-gallery-synthetic.png'),fullPage:true});
    await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    await page.goto(origin+'/scientific-photo-upload/');await page.getByText('Synthetic owner login',{exact:true}).click();await page.getByRole('button',{name:'Ritira pubblicazione',exact:true}).click();await page.getByText('Pubblicazione ritirata. I file privati restano conservati.',{exact:true}).waitFor();
    assert.equal((await (await fetch(local+'/v1/gallery')).json()).records.length,0);
    assert.equal((await fetch(local+new URL(previewUrl).pathname)).status,400);
    await page.goto(origin+'/scientific-image-gallery/');await page.getByText('Nessuna immagine ancora pubblicata dalle sessioni importate.',{exact:true}).waitFor();
    const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();await staticPage.goto(origin+'/scientific-photo-upload/');assert.equal(await staticPage.getByRole('button',{name:'Carica e verifica',exact:true}).isDisabled(),true);await nojs.close();
    assert.deepEqual(errors,[]);console.log('Photo ingestion PASS: SHA256, owner/origin gates, real synthetic HTTP upload, private save, minimization, publication, mobile, XSS, withdrawal.');
  }finally{await browser?.close();child?.kill();if(server)await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
