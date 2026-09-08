import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const source = JSON.parse(fs.readFileSync(path.join(root, 'docs/data/anomaly-trend-f2-fixture.json'), 'utf8'));
const validator = path.join(root, '.github/scripts/verify-anomaly-trend-f2.mjs');

function mutated(mutator) {
  const doc = structuredClone(source); mutator(doc);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'dsg-bkl038-f2-'));
  const fixture = path.join(dir, 'fixture.json'); fs.writeFileSync(fixture, JSON.stringify(doc));
  const r = spawnSync(process.execPath, [validator], { cwd: root, env: {...process.env, DSG_ANOMALY_TREND_FIXTURE: fixture}, encoding:'utf8' });
  fs.rmSync(dir, {recursive:true, force:true}); return r;
}
function rejects(name, mutator, expected) {
  test(name, () => { const r=mutated(mutator); assert.notEqual(r.status,0); assert.match(`${r.stdout}\n${r.stderr}`, expected); });
}

test('accepted bounded fixture passes', () => {
  const r=spawnSync(process.execPath,[validator],{cwd:root,encoding:'utf8'}); assert.equal(r.status,0,`${r.stdout}\n${r.stderr}`);
});
rejects('descriptive trend cannot self-promote', d=>{const r=d.records.find(x=>x.semantic_type==='TREND_MEASUREMENT');r.candidate_state='OBSERVED_RULE_MATCH';r.rule_id='UNAPPROVED';}, /descriptive trend cannot self-promote/);
rejects('rule match requires governed rule id', d=>{const r=d.records[0];r.semantic_type='ANOMALY_CANDIDATE';r.candidate_state='OBSERVED_RULE_MATCH';r.rule_id=null;}, /governed rule_id required/);
rejects('correlation must remain not assessed', d=>{const r=d.records.find(x=>x.semantic_type==='CORRELATION_CANDIDATE');r.candidate_state='OBSERVED_RULE_MATCH';r.rule_id='UNAPPROVED';}, /must remain NOT_ASSESSED/);
rejects('correlation requires causation guard', d=>{const r=d.records.find(x=>x.semantic_type==='CORRELATION_CANDIDATE');r.explanation_codes=['SEQUENTIAL_RELATIONSHIP_ONLY'];}, /causation guard missing/);
rejects('unresolved source fails closed', d=>{d.records[0].source_record_refs=['replay-event:DOES-NOT-EXIST'];}, /unresolved source/);
rejects('unresolved citation fails closed', d=>{d.records[0].citation_refs=['CIT-DOES-NOT-EXIST@1.0'];}, /unresolved citation/);
rejects('unresolved provenance fails closed', d=>{d.records[0].provenance_refs=['PRV-DOES-NOT-EXIST@1.0'];}, /unresolved provenance/);
rejects('projection authority is immutable', d=>{d.records[0].authority='runtime';}, /const mismatch/);
rejects('action authority is none', d=>{d.records[0].action_authority='COMMAND';}, /const mismatch/);
