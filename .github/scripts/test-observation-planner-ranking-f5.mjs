import assert from 'node:assert/strict';
import test from 'node:test';
import fs from 'node:fs';
import { rankFixture, validateFixture, canonicalJson } from './observation-planner-ranking-f5.mjs';

const load=()=>JSON.parse(fs.readFileSync('docs/data/observation-planner-ranking-f5-fixture.json','utf8'));

test('known-answer ranking is deterministic and immutable by input order',()=>{
  const a=load();
  const b=structuredClone(a); b.candidates.reverse();
  const ra=rankFixture(a); const rb=rankFixture(b);
  assert.equal(canonicalJson(ra),canonicalJson(rb));
  assert.deepEqual(ra.results.map(x=>x.targetKey),['dsg-target:ldn-1320','dsg-target:m-27']);
});

test('improved altitude increases score while preserving boundaries',()=>{
  const f=load();
  const before=rankFixture(f).results.find(x=>x.targetKey==='dsg-target:m-27').score;
  f.candidates.find(x=>x.targetKey==='dsg-target:m-27').evidence.astronomicalAltitudeDeg=45;
  const after=rankFixture(f).results.find(x=>x.targetKey==='dsg-target:m-27').score;
  assert.ok(after>before);
});

test('out-of-range evidence fails closed',()=>{
  const f=load(); f.candidates[0].evidence.astronomicalAltitudeDeg=91;
  assert.throws(()=>rankFixture(f),/out of range/);
});

test('unknown fixture property fails closed',()=>{
  const f=load(); f.hiddenRecommendation='LDN 1320';
  assert.throws(()=>validateFixture(f),/unknown property/);
});

test('unknown candidate evidence property fails closed',()=>{
  const f=load(); f.candidates[0].evidence.readiness=true;
  assert.throws(()=>validateFixture(f),/unknown property/);
});

test('duplicate target identity fails closed',()=>{
  const f=load(); f.candidates[1].targetKey=f.candidates[0].targetKey;
  assert.throws(()=>validateFixture(f),/duplicate targetKey/);
});

test('unvalidated identity fails closed',()=>{
  const f=load(); f.candidates[0].identityState='conflicted';
  assert.throws(()=>validateFixture(f),/identity must be validated/);
});

test('authority escalation fails closed',()=>{
  const f=load(); f.method.readinessAuthority=true;
  assert.throws(()=>validateFixture(f),/authority escalation/);
});

test('identity factor cannot be silently weakened',()=>{
  const f=load(); f.candidates[0].evidence.targetIdentityValidation=0.5;
  assert.throws(()=>validateFixture(f),/identity validation must equal 1/);
});

test('forecast completeness cannot be imputed above one',()=>{
  const f=load(); f.candidates[0].evidence.forecastEvidenceCompleteness=1.01;
  assert.throws(()=>validateFixture(f),/out of range/);
});
