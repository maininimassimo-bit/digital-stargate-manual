import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const sandbox = {URL, window:{}, document:{currentScript:null}};
vm.runInNewContext(fs.readFileSync('docs/javascripts/scientific-session-publication.js','utf8'),sandbox);
vm.runInNewContext(fs.readFileSync('docs/javascripts/scientific-data-engine.js','utf8'),sandbox);
const publication=sandbox.window.DSGSessionPublication, engine=sandbox.window.DSGScientificDataEngine;
const evidence=JSON.parse(fs.readFileSync('docs/project/evidence/BKL-049-M27-PUBLIC-2026-10-05.json','utf8'));
const sessionId='2026-09-19_2026-09-20';
const record={...evidence, title:'M27',workflowId:'WF-'+evidence.imageVersionId.slice(4), steps:Array.from({length:evidence.processCount},()=>({processId:'Script'}))};
const session={sessionId,lightCompleted:16,manifestState:'VERSIONED',transferState:'NOT_REPRESENTED',evidenceState:'SOURCE_METRICS_AVAILABLE'};

test('published M27 joins by exact declared session, with its version and partial workflow',()=>{
  const records=publication.select(sessionId,{records:[record]});
  assert.equal(records.length,1);
  const lineage=engine.getLineage(session,publication.describe(records));
  assert.equal(lineage[5].state,'partial');
  assert.match(lineage[5].detail,/80 passaggi disponibili.*parziale.*esecuzione non verificata/);
  assert.match(lineage[5].detail,/WF-5e5dd49a62f90e349e2931f3d143b941/);
  assert.equal(lineage[6].state,'represented');
  assert.match(lineage[6].detail,/VER-5e5dd49a62f90e349e2931f3d143b941.*dichiarata/);
});
test('same target, substring IDs and historical declarations do not establish an association',()=>{
  assert.equal(publication.select(sessionId,{records:[{...record,sessionIds:[sessionId+'-other']},{...record,associationEvidence:'HISTORICAL_OWNER_DECLARATION',sessionIds:[]}]}).length,0);
});
test('every associated version is retained, including unavailable workflows',()=>{
  const description=publication.describe([record,{...record,imageVersionId:'VER-second',workflowId:'WF-second',steps:[],captureCompleteness:'UNAVAILABLE'}]);
  assert.match(description.publication.detail,/VER-second/);
  assert.match(description.processing.detail,/WF-second: 0 passaggi disponibili; workflow non disponibile/);
});
test('withdrawal clears publication on the next fresh collection',()=>{
  assert.equal(publication.describe(publication.select(sessionId,{records:[record]})).publication.state,'represented');
  const description=publication.describe(publication.select(sessionId,{records:[]}));
  assert.equal(description.publication.state,'missing');
  assert.match(description.processing.detail,/Nessun workflow pubblico/);
});
test('failed or pending reads remain unknown rather than asserting absence',()=>{
  for(const state of ['loading','unavailable']){
    const description=publication.describe([],state);
    assert.equal(description.publication.state,'partial');
    assert.doesNotMatch(description.publication.detail,/Nessuna immagine/);
  }
});
test('gallery links bind the session and exact image version',()=>{
  const url=new URL(publication.galleryUrl('https://example.test/digital-stargate-manual/',sessionId,record.imageVersionId));
  assert.equal(url.pathname,'/digital-stargate-manual/scientific-image-gallery/');
  assert.equal(url.searchParams.get('sessionId'),sessionId);
  assert.equal(url.hash,'#'+record.imageVersionId);
});
test('canonical metrics link points to repository evidence and rejects malformed paths',()=>{
  const path=`data/sessions/2026/09/${sessionId}/normalized/session-metrics.json`;
  assert.equal(publication.metricsUrl(path),'https://github.com/maininimassimo-bit/digital-stargate-manual/blob/main/'+path);
  for(const path of [null,'https://evil.test','data/../secret','data/sessions/2026/09/id/normalized/session-metrics.json?token=x']) assert.equal(publication.metricsUrl(path),null);
});
