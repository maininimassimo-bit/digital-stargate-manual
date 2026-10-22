const assert=require('node:assert/strict'),fs=require('node:fs'),http=require('node:http');
const {chromium}=require('playwright');
(async()=>{
 let browser,server;
 try{
  server=http.createServer((req,res)=>{res.setHeader('Content-Type','text/html');res.end('<textarea id="bkl042-chat-question"></textarea><div id="bkl042-chat-answer"></div><button id="bkl042-chat-live">Invia ad IA</button><p id="bkl042-chat-auth-status"></p><div id="bkl042-google-signin"></div>');});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  browser=await chromium.launch({headless:true,...(process.env.DSG_BROWSER_CHANNEL?{channel:process.env.DSG_BROWSER_CHANNEL}:{})});
  const page=await browser.newPage();let code='SOURCE_TOO_LARGE';
  await page.route('https://dsg-bkl042-portal-gateway-183451329061.europe-west1.run.app/**',r=>r.fulfill({status:503,contentType:'application/json',headers:{'Access-Control-Allow-Origin':'*'},body:JSON.stringify({error:code})}));
  await page.goto(`http://127.0.0.1:${server.address().port}`);
  await page.evaluate(()=>{window.google={accounts:{id:{initialize(){},renderButton(){}}}};});
  await page.addScriptTag({content:fs.readFileSync('docs/javascripts/bkl042-chat.js','utf8')});
  await page.evaluate(()=>window.handleBkl042GoogleCredential({credential:'synthetic'}));
  await page.locator('#bkl042-chat-question').fill('test');
  for(const [next,expected] of [['SOURCE_TOO_LARGE','supera il limite'],['PILOT_REQUEST_LIMIT_REACHED','limite di richieste'],['SOURCE_UNAVAILABLE','fonte documentale'],['UNKNOWN','Richiesta non completata (503)']]){
   code=next;await page.getByRole('button',{name:'Invia ad IA'}).click();
   await page.waitForFunction(()=>!document.querySelector('#bkl042-chat-live').disabled);
   assert.match(await page.locator('#bkl042-chat-auth-status').textContent(),new RegExp(expected.replace(/[()]/g,'\\$&')));
  }
  console.log('PASS BKL042 public diagnostic messages and safe fallback');
 }finally{await browser?.close();if(server)await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
