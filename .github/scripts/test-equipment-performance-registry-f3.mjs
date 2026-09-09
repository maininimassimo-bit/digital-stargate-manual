import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';import os from 'node:os';import path from 'node:path';import {spawnSync} from 'node:child_process';
const root=process.cwd(),source=JSON.parse(fs.readFileSync(path.join(root,'docs/data/equipment-performance-registry-f3.json'),'utf8')),validator=path.join(root,'.github/scripts/verify-equipment-performance-registry-f3.mjs');
function rejected(mutator){const p=structuredClone(source);mutator(p);const d=fs.mkdtempSync(path.join(os.tmpdir(),'bkl039-f3-')),f=path.join(d,'projection.json');fs.writeFileSync(f,JSON.stringify(p));const r=spawnSync(process.execPath,[validator],{cwd:root,env:{...process.env,BKL039_F3_PROJECTION:f},encoding:'utf8'});fs.rmSync(d,{recursive:true,force:true});return r.status!==0;}
test('rejects angular unit overclaim',()=>assert.equal(rejected(p=>{p.records[0].unit='arcsec';}),true));
test('rejects calibrated-state overclaim',()=>assert.equal(rejected(p=>{p.records[0].angular_calibration_state='PROVEN';}),true));
test('rejects authority escalation',()=>assert.equal(rejected(p=>{p.records[0].action_authority='COMMAND';}),true));
test('rejects health semantics',()=>assert.equal(rejected(p=>{p.records[0].health_state='GOOD';}),true));
test('rejects ranking semantics',()=>assert.equal(rejected(p=>{p.records[19].ranking=1;}),true));
test('rejects changed source value',()=>assert.equal(rejected(p=>{p.records[0].value=1;}),true));
test('rejects wrong sample count',()=>assert.equal(rejected(p=>{p.records[19].sample_count=18;}),true));
test('rejects wrong statistic',()=>assert.equal(rejected(p=>{p.records[19].value=99;}),true));
test('rejects changed method',()=>assert.equal(rejected(p=>{p.records[19].method_id='UNVERSIONED';}),true));
test('rejects incomplete coverage claim',()=>assert.equal(rejected(p=>{p.records[19].coverage='PARTIAL_FOR_DECLARED_POPULATION';}),true));
test('rejects unresolved provenance',()=>assert.equal(rejected(p=>{p.records[0].provenance_refs=['does/not/exist'];}),true));
test('rejects duplicate record id',()=>assert.equal(rejected(p=>{p.records[1].record_id=p.records[0].record_id;}),true));
test('rejects extra record',()=>assert.equal(rejected(p=>{p.records.push(structuredClone(p.records[0]));}),true));
test('rejects changed bounded session',()=>assert.equal(rejected(p=>{p.records[0].session_id='2099-01-01_2099-01-02';}),true));
