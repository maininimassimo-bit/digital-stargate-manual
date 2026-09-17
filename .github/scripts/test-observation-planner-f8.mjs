import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {validateF8} from './verify-observation-planner-f8.mjs';
const p='docs/data/observation-planner-f8-current-astronomy-suitability.json';const d=JSON.parse(fs.readFileSync(p,'utf8'));
test('known answer passes',()=>assert.deepEqual(validateF8(d),[]));
test('privacy fails closed',()=>{const x=structuredClone(d);x.site.latitude=42;assert(validateF8(x).some(v=>v.includes('protected coordinates')))});
test('authority fails closed',()=>{const x=structuredClone(d);x.boundaries.readinessAuthority=true;assert(validateF8(x).some(v=>v.includes('advisory boundaries')))});
test('F7 lineage fails closed',()=>{const x=structuredClone(d);x.sourceBindings.forecastWorkflowRunId='0';assert(validateF8(x).some(v=>v.includes('workflow lineage')))});
test('ranking has both governed targets per setup',()=>{for(const r of d.rankings){assert.equal(r.targets.length,2);assert(r.targets.every(t=>t.bestWindows.length>0))}});
