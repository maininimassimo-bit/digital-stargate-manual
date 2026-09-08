import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
const root = path.resolve(import.meta.dirname, '../..');
const fixture = JSON.parse(fs.readFileSync(path.join(root,'docs/data/night-timeline-replay.json'),'utf8'));
function run(mutator, options={}) {
  const d=structuredClone(fixture); mutator(d);
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'dsg-rpl-')); const f=path.join(dir,'fixture.json');
  const json=JSON.stringify(d); fs.writeFileSync(f,options.bom ? `\uFEFF${json}` : json);
  return spawnSync(process.execPath,[path.join(root,'.github/scripts/verify-night-timeline-replay.mjs')],{cwd:root,env:{...process.env,DSG_NIGHT_TIMELINE_REPLAY:f},encoding:'utf8'});
}
const passes = mutator => assert.equal(run(mutator).status,0);
const rejects = mutator => assert.notEqual(run(mutator).status,0);
test('accepted bounded fixture passes',()=>passes(()=>{}));
test('UTF-8 BOM fixture passes',()=>assert.equal(run(()=>{},{bom:true}).status,0));
test('authority promotion rejected',()=>rejects(d=>d.authority='authority'));
test('invented UTC instant rejected',()=>rejects(d=>d.sessions[0].events[0].event_time_utc='2026-08-15T17:01:00Z'));
test('source timestamp substitution rejected',()=>rejects(d=>d.sessions[0].events[0].source_timestamp_raw='2026-08-15T19:01:00+02:00'));
test('source order promotion rejected',()=>rejects(d=>d.sessions[0].events[0].source_order=10));
test('missing citation rejected',()=>rejects(d=>d.sessions[0].events[0].citation_refs=['CIT-MISSING@1.0']));
test('missing provenance rejected',()=>rejects(d=>d.sessions[0].events[0].provenance_refs=['PRV-MISSING@1.0']));
test('UNPLACED cannot carry event_time_utc',()=>rejects(d=>d.sessions[0].events[0].temporal_state='UNPLACED'));
test('bounded event overflow rejected',()=>rejects(d=>{d.bounds.max_events=1}));
test('unexpected event property rejected by schema',()=>rejects(d=>{d.sessions[0].events[0].unexpected=true}));
test('missing required event field rejected by schema',()=>rejects(d=>{delete d.sessions[0].events[0].quality_state}));
test('invalid temporal state rejected by schema',()=>rejects(d=>{d.sessions[0].events[0].temporal_state='MAYBE'}));
test('malformed Citation locator rejected by schema',()=>rejects(d=>{d.citations[0].locator.json_pointer='start_local'}));
test('malformed Provenance structure rejected by schema',()=>rejects(d=>{delete d.provenance_records[0].method_id}));
test('reverse chronological replay order rejected',()=>rejects(d=>{d.sessions[0].events.reverse()}));
test('same-time source-order tie-break violation rejected',()=>rejects(d=>{
  const a=d.sessions[0].events[0], b=d.sessions[0].events[1];
  b.event_time_utc=a.event_time_utc; b.source_timestamp_raw=a.source_timestamp_raw;
  b.source_ref=a.source_ref; b.event_kind=a.event_kind;
  const c=d.citations.find(x=>`${x.id}@${x.version}`===b.citation_refs[0]); c.locator.json_pointer='/start_local';
  const p=d.provenance_records.find(x=>`${x.id}@${x.version}`===b.provenance_refs[0]); p.input_refs=[a.source_ref];
  a.source_type='SESSION_PROJECTION'; a.source_order=90; b.source_type='NINA'; b.source_order=10;
}));
test('valid UNPLACED evidence is representable',()=>passes(d=>{
  const e=d.sessions[0].events[1];
  e.temporal_state='UNPLACED'; e.event_time_utc=null; e.source_timestamp_raw=null;
  e.source_type='NINA'; e.source_order=10; e.source_authority='NINA raw evidence'; e.event_kind='SOURCE_TIMESTAMP_UNPLACED';
  e.source_ref='data/sessions/2026/08/2026-08-15_2026-08-16/raw/nina/';
  const c=d.citations.find(x=>`${x.id}@${x.version}`===e.citation_refs[0]); c.source_authority='NINA raw evidence'; c.locator.path=e.source_ref; c.locator.json_pointer='/unplaced';
  const p=d.provenance_records.find(x=>`${x.id}@${x.version}`===e.provenance_refs[0]); p.method_id='BKL040-F2-UNPLACED-REPRESENTATION-TEST-1'; p.input_refs=[e.source_ref];
}));
