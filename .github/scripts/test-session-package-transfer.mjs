import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,rm,readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import vm from 'node:vm';
import {projectSessionPackage} from './session-package-transfer.mjs';
const id='2026-09-19_2026-09-20';
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
async function fixture(t){
  const root=await mkdtemp(join(tmpdir(),'dsg-package-'));t.after(()=>rm(root,{recursive:true,force:true}));
  const directory=join(root,'data/sessions/2026/09',id);await mkdir(join(directory,'raw/nina'),{recursive:true});
  const bytes=Buffer.from('actual received evidence\r\n');await writeFile(join(directory,'raw/nina/log.txt'),bytes);
  const manifest={schema_version:'1.0',session_id:id,report_status:'COMPLETE',files:[{path:'raw/nina/log.txt',size_bytes:bytes.length,sha256:sha(bytes)}]};
  const save=(value=manifest)=>writeFile(join(directory,'manifest.json'),JSON.stringify(value));await save();return {root,directory,manifest,save};
}
test('complete received bytes match every manifest size and SHA',async t=>{const f=await fixture(t);const r=await projectSessionPackage(f.root,id);assert.equal(r.state,'VERIFIED');assert.equal(r.fileCount,1);assert.equal(r.verifiedFileCount,1);assert.equal(r.scope,'SESSION_DOCUMENT_PACKAGE');assert.deepEqual(Object.keys(r).sort(),['sessionId','scope','state','manifestRef','fileCount','verifiedFileCount'].sort());});
test('same-size modified bytes do not verify and recover after restoration',async t=>{const f=await fixture(t);const path=join(f.directory,'raw/nina/log.txt');const original=await readFile(path);await writeFile(path,Buffer.alloc(original.length,65));assert.equal((await projectSessionPackage(f.root,id)).state,'INCOMPLETE');await writeFile(path,original);assert.equal((await projectSessionPackage(f.root,id)).state,'VERIFIED');});
test('missing file remains incomplete and missing manifest is unavailable',async t=>{const f=await fixture(t);await rm(join(f.directory,'raw/nina/log.txt'));assert.equal((await projectSessionPackage(f.root,id)).verifiedFileCount,0);await rm(join(f.directory,'manifest.json'));assert.equal((await projectSessionPackage(f.root,id)).state,'UNAVAILABLE');});
test('cross-session identity, incomplete status, duplicate and traversal paths are rejected',async t=>{const f=await fixture(t);for(const change of [m=>m.session_id='another',m=>m.report_status='PARTIAL',m=>m.files.push({...m.files[0]}),m=>m.files[0].path='raw/../../secret']){const original=JSON.stringify(f.manifest);change(f.manifest);await f.save(f.manifest);assert.equal((await projectSessionPackage(f.root,id)).state,'INVALID');f.manifest=JSON.parse(original);await writeFile(join(f.directory,'manifest.json'),original);}});
test('empty manifest cannot attest a transfer',async t=>{const f=await fixture(t);f.manifest.files=[];await f.save();assert.equal((await projectSessionPackage(f.root,id)).state,'INVALID');});
const sandbox={window:{}};vm.runInNewContext(await readFile('docs/javascripts/scientific-session-transfer.js','utf8'),sandbox);const describe=sandbox.window.DSGSessionTransfer.describe;
const record={sessionId:id,scope:'SESSION_DOCUMENT_PACKAGE',state:'VERIFIED',fileCount:6,verifiedFileCount:6,manifestRef:`data/sessions/2026/09/${id}/manifest.json`};
test('view distinguishes session documents from RAW photographic transfer',()=>{const v=describe(id,{records:[record]});assert.equal(v.state,'represented');assert.match(v.detail,/6\/6.*SHA-256.*non RAW/);assert.match(v.manifestUrl,/github.com\/maininimassimo-bit/);});
test('fresh invalid/unavailable/other-session input removes prior positive claim',()=>{for(const state of ['INVALID','INCOMPLETE','UNAVAILABLE'])assert.notEqual(describe(id,{records:[{...record,state}]}).state,'represented');assert.equal(describe('2026-09-20_2026-09-21',{records:[record]}).manifestUrl,null);assert.equal(describe(id,null,'unavailable').state,'partial');});

async function reader(value,requests=[]){
  const url='https://portal.test/javascripts/scientific-data-engine.js';
  const context={window:{},document:{currentScript:{src:url}},location:{origin:'https://portal.test'},URL,AbortController,setTimeout,clearTimeout,TextDecoder,fetch:async(source,options)=>{requests.push(options);return {ok:true,url:source,body:new Response(JSON.stringify(value)).body};}};
  vm.runInNewContext(await readFile('docs/javascripts/scientific-data-engine.js','utf8'),context);
  return context.window.DSGScientificDataEngine.getSessionTransferCollection();
}
const collection={schemaVersion:'1.0',kind:'SESSION_PACKAGE_TRANSFER_PROJECTION',authority:'projection',scope:'SESSION_DOCUMENT_PACKAGE',records:[record]};
test('reader fetches fresh same-origin projection without credentials',async()=>{const requests=[];assert.equal((await reader(collection,requests)).records[0].state,'VERIFIED');assert.equal(requests[0].cache,'no-store');assert.equal(requests[0].credentials,'omit');assert.equal(requests[0].redirect,'error');});
test('reader rejects duplicate identities, contradictory verification, altered scope and unsafe links',async()=>{for(const value of [{...collection,records:[record,record]},{...collection,records:[{...record,verifiedFileCount:3}]},{...collection,scope:'RAW_IMAGES'},{...collection,records:[{...record,manifestRef:'https://evil.test'}]}])await assert.rejects(reader(value));});
