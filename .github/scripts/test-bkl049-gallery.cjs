/* Synthetic producer/contract/SDE integration; no real image or remote request. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {spawnSync} = require('node:child_process');
const contract = require('../../docs/javascripts/bkl049-workflow-contract.js');
const child = spawnSync('python', ['-c', 'import json; from tools.pixinsight.workflow_archive.test_public_projection import candidate,selection_for,project; b=candidate(); print(json.dumps(project(b,selection_for(b))))'], {encoding:'utf8',timeout:10000,maxBuffer:1024*1024});
assert.equal(child.status, 0, child.stderr);
const workflow = JSON.parse(child.stdout);
const externalChild = spawnSync('python', ['-c', 'import json; from tools.pixinsight.workflow_archive.test_external_public import projection; print(json.dumps(projection()))'], {encoding:'utf8',timeout:10000,maxBuffer:1024*1024});
assert.equal(externalChild.status, 0, externalChild.stderr);
const externalWorkflow = JSON.parse(externalChild.stdout);
const current = () => {
  const now = Math.floor(Date.now()/1000)*1000;
  return {schemaVersion:'1.0',kind:'BKL049_PUBLIC_COLLECTION',authority:'processing_evidence',actionAuthority:'NONE',
    publishedAt:new Date(now-1000).toISOString().replace('.000Z','Z'),
    validUntil:new Date(now+60000).toISOString().replace('.000Z','Z'), records:[structuredClone(workflow)]};
};
const snapshot = contract.parseCollection(contract.canonical(current()));
const externalCollection = {...current(), records:[externalWorkflow]};
const persistent={...externalCollection,schemaVersion:'2.0',validUntil:null};
const later=Date.parse(persistent.publishedAt)+366*86400000;
assert.equal(contract.parseCollection(contract.canonical(persistent),later).records.length,1);
assert.equal(contract.resolve(persistent,externalWorkflow.imageId,externalWorkflow.imageVersionId,externalWorkflow.workflowId,later).workflowId,externalWorkflow.workflowId);
for(const change of [{schemaVersion:'1.0'},{validUntil:externalCollection.validUntil},
  {records:[workflow]},{records:[]},{publishedAt:'2099-01-01T00:00:00Z'},
  {records:[externalWorkflow,externalWorkflow]}]) {
  assert.throws(()=>contract.parseCollection(contract.canonical({...persistent,...change})));
}
assert.equal(contract.parseCollection(contract.canonical(externalCollection)).records[0].scientificContext.qualityState, 'UNKNOWN');
for (const mutate of [
  r => r.scientificContext.qualityState='ACCEPTED',
  r => r.scientificContext.metadataState='COMPLETE',
  r => delete r.scientificContext,
  r => r.preview.url='javascript:alert(1)',
  r => r.preview.url+='?token=secret',
  r => r.preview.url+='\n',
  r => r.preview.sha256='private',
  r => r.title='x'.repeat(201),
  r => r.attribution='\u0000secret',
  r => r.schemaVersion='1.0'
]) {
  const bad=structuredClone(externalWorkflow);mutate(bad);
  assert.throws(()=>contract.validateWorkflow(bad));
}
assert.equal(contract.resolve(externalCollection, externalWorkflow.imageId, externalWorkflow.imageVersionId, externalWorkflow.workflowId).kind, 'BKL049_PUBLIC_EXTERNAL_WORKFLOW');
assert.equal(contract.resolve(externalCollection, externalWorkflow.imageId, 'VER-wrong', externalWorkflow.workflowId), null);
assert.ok(Object.isFrozen(snapshot.records[0].steps));
assert.equal(contract.resolve(snapshot, workflow.imageId, workflow.imageVersionId, workflow.workflowId).workflowId, workflow.workflowId);
assert.equal(contract.resolve(snapshot, workflow.imageId, 'VER-wrong', workflow.workflowId), null);
assert.throws(() => contract.resolve(snapshot, workflow.imageId, workflow.imageVersionId, workflow.workflowId, Date.parse(snapshot.validUntil)));
const negative = [
  c => c.records.push(structuredClone(c.records[0])),
  c => {const other=structuredClone(c.records[0]);other.imageVersionId='VER-other';c.records.push(other);},
  c => c.records[0].imageId='IMG-x\r',
  c => c.records[0].imageId='IMG-x\n',
  c => c.records[0].imageVersionId='https://example.test',
  c => c.records[0].workflowId='WF-../x',
  c => c.records[0].captureCompleteness='COMPLETE',
  c => c.records[0].steps[0].evidenceClass='OBSERVED',
  c => c.records[0].steps[0].parameters.push(structuredClone(c.records[0].steps[0].parameters[0])),
  c => c.records[0].steps.push(structuredClone(c.records[0].steps[0])),
  c => c.records[0].methodCitation='javascript:alert(1)',
  c => c.records[0].privatePath='NEVER DISPLAY',
  c => c.records[0].gaps[0]='ARBITRARY',
  c => c.records[0].steps[0].parameters[0].lexicalJson='x'.repeat(4097),
  c => c.validUntil=c.publishedAt,
  c => c.publishedAt=c.validUntil,
  c => c.publishedAt='2026-02-30T00:00:00Z',
  c => c.validUntil='2099-01-01T00:00:00Z',
  c => c.records=[],
  c => c.records=Array(9).fill(c.records[0]),
];
negative.forEach(mutate => {const c=current();mutate(c);assert.throws(()=>contract.parseCollection(contract.canonical(c)));});
const raw=contract.canonical(current());
assert.throws(()=>contract.parseCollection('{"kind":"duplicate",'+raw.slice(1)));
assert.throws(()=>contract.parseCollection(raw+' garbage'));
assert.throws(()=>contract.parseCollection(' '.repeat(contract.MAX_BYTES+1)));
const committed=fs.readFileSync('docs/data/bkl049-public-workflows.json','utf8');
const committedShape=JSON.parse(committed);
// Validate a retained release at its publication instant, then enforce expiry.
// A historical artifact must not make unrelated CI fail after its live window.
const committedAt=committedShape.publishedAt ? Date.parse(committedShape.publishedAt) : Date.now();
contract.parseCollection(committed,committedAt);
if(committedShape.records.length && committedShape.validUntil !== null) {
  assert.throws(()=>contract.parseCollection(committed,Date.parse(committedShape.validUntil)));
} else if(committedShape.records.length) {
  assert.equal(contract.parseCollection(committed,committedAt+366*86400000).records.length,committedShape.records.length);
}
const empty=contract.canonical({schemaVersion:'1.0',kind:'BKL049_PUBLIC_COLLECTION',authority:'processing_evidence',
  actionAuthority:'NONE',publishedAt:null,validUntil:null,records:[]});
assert.equal(contract.parseCollection(empty).records.length,0);

const source='https://example.test/manual/data/bkl049-public-workflows.json';
const engineCode=fs.readFileSync('docs/javascripts/scientific-data-engine.js','utf8');
const response=(text,url=source)=>{const r=new Response(text);Object.defineProperty(r,'url',{value:url});return r;};
function engine(fetchImpl) {
  const context={URL,TextEncoder,TextDecoder,AbortController,setTimeout,clearTimeout,console,
    document:{currentScript:{src:'https://example.test/manual/javascripts/scientific-data-engine.js'}},
    location:{origin:'https://example.test'},fetch:fetchImpl,DSGBkl049WorkflowContract:contract};
  context.window=context;vm.runInNewContext(engineCode,context);return context.DSGScientificDataEngine;
}
(async()=>{
  let calls=0;
  const api=engine(async(url,options)=>{
    calls++;assert.equal(url,source);assert.equal(options.cache,'no-store');assert.equal(options.redirect,'error');assert.equal(options.credentials,'omit');
    return response(calls===1?contract.canonical(current()):empty);
  });
  assert.equal((await api.getPublicWorkflowCollection()).records.length,1);
  assert.equal((await api.getPublicWorkflowCollection()).records.length,0,'withdrawal replaces prior records without cache fallback');
  for (const fake of [async()=>response(raw,'https://other.test/private'),async()=>response('{'),
                     async()=>response(' '.repeat(contract.MAX_BYTES+1)),async()=>{throw new Error('PRIVATE TRANSPORT DETAIL');}]) {
    await assert.rejects(engine(fake).getPublicWorkflowCollection(), /WORKFLOW_UNAVAILABLE/);
  }
  const cancel=new AbortController();
  const aborted=engine(async(url,{signal})=>{assert.equal(signal.aborted,true);throw new Error('cancel');});
  cancel.abort();await assert.rejects(aborted.getPublicWorkflowCollection({signal:cancel.signal}),/WORKFLOW_UNAVAILABLE/);
  console.log('PASS BKL049: Python producer compatibility, exact identity, omissions, canonical/closed schema, uniqueness, expiry, bounded SDE, cancellation and withdrawal.');
})().catch(error=>{console.error(error);process.exitCode=1;});

module.exports={workflow,current};
