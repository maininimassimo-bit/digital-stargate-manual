import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
const root = path.resolve(import.meta.dirname, '../..');
const fixture = JSON.parse(fs.readFileSync(path.join(root,'docs/data/night-timeline-replay.json'),'utf8'));
function run(mutator) {
  const d=structuredClone(fixture); mutator(d);
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'dsg-rpl-')); const f=path.join(dir,'fixture.json'); fs.writeFileSync(f,JSON.stringify(d));
  return spawnSync(process.execPath,[path.join(root,'.github/scripts/verify-night-timeline-replay.mjs')],{cwd:root,env:{...process.env,DSG_NIGHT_TIMELINE_REPLAY:f},encoding:'utf8'});
}
test('accepted bounded fixture passes',()=>assert.equal(run(()=>{}).status,0));
test('authority promotion rejected',()=>assert.notEqual(run(d=>d.authority='authority').status,0));
test('invented UTC instant rejected',()=>assert.notEqual(run(d=>d.sessions[0].events[0].event_time_utc='2026-08-15T17:01:00Z').status,0));
test('source timestamp substitution rejected',()=>assert.notEqual(run(d=>d.sessions[0].events[0].source_timestamp_raw='2026-08-15T19:01:00+02:00').status,0));
test('source order promotion rejected',()=>assert.notEqual(run(d=>d.sessions[0].events[0].source_order=10).status,0));
test('missing citation rejected',()=>assert.notEqual(run(d=>d.sessions[0].events[0].citation_refs=['CIT-MISSING@1.0']).status,0));
test('missing provenance rejected',()=>assert.notEqual(run(d=>d.sessions[0].events[0].provenance_refs=['PRV-MISSING@1.0']).status,0));
test('UNPLACED cannot carry timestamps',()=>assert.notEqual(run(d=>d.sessions[0].events[0].temporal_state='UNPLACED').status,0));
test('bounded event overflow rejected',()=>assert.notEqual(run(d=>{d.bounds.max_events=1}).status,0));
