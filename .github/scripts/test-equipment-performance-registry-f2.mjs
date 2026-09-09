import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const root=process.cwd();
const source=JSON.parse(fs.readFileSync(path.join(root,'docs/data/equipment-performance-registry-f2-fixture.json'),'utf8'));
const validator=path.join(root,'.github/scripts/verify-equipment-performance-registry-f2.mjs');
function clone(){ return structuredClone(source); }
function rejected(mutator){
  const value=clone(); mutator(value);
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bkl039-f2-'));
  const file=path.join(dir,'fixture.json'); fs.writeFileSync(file,JSON.stringify(value,null,2));
  const result=spawnSync(process.execPath,[validator],{cwd:root,env:{...process.env,BKL039_F2_FIXTURE:file},encoding:'utf8'});
  fs.rmSync(dir,{recursive:true,force:true});
  return result.status !== 0;
}

test('rejects authority escalation',()=>assert.equal(rejected(f=>{f.records[0].action_authority='COMMAND';}),true));
test('rejects synthetic configuration identity',()=>assert.equal(rejected(f=>{f.records[0].configuration_id='SYNTHETIC-CONFIG';}),true));
test('rejects unresolved session',()=>assert.equal(rejected(f=>{f.records[1].session_id='2099-01-01_2099-01-02';}),true));
test('rejects PARTIAL session',()=>assert.equal(rejected(f=>{f.records[1].session_id='2026-08-10_2026-08-11';}),true));
test('rejects equipment mismatch',()=>assert.equal(rejected(f=>{f.records[2].camera='Invented Camera';}),true));
test('rejects performance rating field',()=>assert.equal(rejected(f=>{f.records[0].performance_rating='GOOD';}),true));
test('rejects unresolved provenance',()=>assert.equal(rejected(f=>{f.records[0].provenance_refs=['does/not/exist'];}),true));
test('rejects duplicate record identity',()=>assert.equal(rejected(f=>{f.records[1].record_id=f.records[0].record_id;}),true));
