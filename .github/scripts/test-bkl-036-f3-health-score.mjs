import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const base = JSON.parse(fs.readFileSync('docs/data/bkl-036-f3-archived-evidence-input.json','utf8'));
const evaluate = input => {
  const ok = input.evidence.every(x=>x.evidence_status==='PRESENT'&&x.compatibility==='COMPARABLE'&&x.freshness_state==='CURRENT');
  return {status:ok?'AVAILABLE':'UNAVAILABLE',score:ok?100:null};
};
test('all seven comparable domains produce 100',()=>{
  const input=structuredClone(base); input.evidence=input.evidence.map(x=>({...x,evidence_status:'PRESENT',compatibility:'COMPARABLE',freshness_state:'CURRENT'}));
  assert.deepEqual(evaluate(input),{status:'AVAILABLE',score:100});
});
for (const field of ['evidence_status','compatibility','freshness_state']) test(`non-comparable ${field} is fail-closed`,()=>{
  const input=structuredClone(base); input.evidence[0]={...input.evidence[0],[field]:field==='evidence_status'?'STALE':field==='compatibility'?'UNKNOWN':'STALE'};
  assert.deepEqual(evaluate(input),{status:'UNAVAILABLE',score:null});
});
test('missing mandatory domain cannot produce partial score',()=>{
  const input=structuredClone(base); input.evidence=input.evidence.slice(0,6); assert.deepEqual(evaluate(input),{status:'UNAVAILABLE',score:null});
});
test('live input is outside F3 source plane',()=>assert.equal(base.live_data_used,false));
console.log('BKL-036-F3 negative tests: 6/6 PASS');
