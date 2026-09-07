import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const validator = '.github/scripts/verify-knowledge-ai-evidence-contract.mjs';
const base = {
  schema_version: '1.0', component: 'DSG.KnowledgeAIEvidenceContract', authority: 'projection',
  citations: [{ id:'CIT-TEST', version:'1.0', source_authority:'repository_authority', locator:{kind:'repository_path', value:'docs/test.md'}, producer:'test-suite', produced_at_utc:'2026-09-07T12:00:00Z' }],
  provenance_records: [],
  confidence_contracts: [{ id: 'CONF-TEST', version: '1.0', scale: '0..1', method: 'test', producer: 'test-suite' }],
  items: []
};
const run = async (doc) => {
  const dir = await mkdtemp(path.join(tmpdir(), 'dsg-bkl044-'));
  const file = path.join(dir, 'fixture.json');
  await writeFile(file, JSON.stringify(doc));
  const result = spawnSync(process.execPath, [validator, file], { encoding: 'utf8' });
  await rm(dir, { recursive: true, force: true });
  return result;
};
const evidence = (id='E-1') => ({ id, semantic_type:'evidence', producer:'engine', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'repository_authority', lifecycle_state:'validated', ai_derived:false, citation_refs:['CIT-TEST@1.0'] });

test('accepts incomplete AI inference without evidence', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'INF-1', semantic_type:'inference', producer:'AI', producer_version:'1', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'projection', lifecycle_state:'incomplete', ai_derived:true, method_id:'M-1' });
  assert.equal((await run(doc)).status, 0);
});

test('rejects validated AI inference without evidence and citations', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'INF-2', semantic_type:'inference', producer:'AI', producer_version:'1', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'projection', lifecycle_state:'validated', ai_derived:true, method_id:'M-1' });
  const result = await run(doc); assert.notEqual(result.status, 0); assert.match(result.stderr, /requires evidence_refs/);
});

test('rejects validated evidence without governed citation locator', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'E-1', semantic_type:'evidence', producer:'engine', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'repository_authority', lifecycle_state:'validated', ai_derived:false });
  const result = await run(doc); assert.notEqual(result.status, 0); assert.match(result.stderr, /validated evidence requires citation_refs/);
});

test('rejects unresolved citation reference', async () => {
  const doc = structuredClone(base); const item = evidence(); item.citation_refs=['CIT-MISSING@1.0']; doc.items.push(item);
  const result = await run(doc); assert.notEqual(result.status, 0); assert.match(result.stderr, /unresolved citation/);
});

test('rejects unresolved provenance reference on validated derived item', async () => {
  const doc = structuredClone(base); doc.items.push(evidence());
  doc.items.push({ id:'CLM-1', semantic_type:'claim', producer:'engine', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'analytics_product', lifecycle_state:'validated', ai_derived:false, method_id:'M-2', evidence_refs:['E-1'], citation_refs:['CIT-TEST@1.0'], provenance_refs:['PROV-MISSING@1.0'] });
  const result = await run(doc); assert.notEqual(result.status, 0); assert.match(result.stderr, /unresolved provenance/);
});

test('rejects unsupported source authority', async () => {
  const doc = structuredClone(base); const item = evidence(); item.source_authority='invented_authority'; doc.items.push(item);
  const result = await run(doc); assert.notEqual(result.status, 0); assert.match(result.stderr, /unsupported source_authority/);
});

test('rejects confidence without a stable versioned contract reference', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'CLM-DRAFT', semantic_type:'claim', producer:'engine', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'projection', lifecycle_state:'draft', ai_derived:false, method_id:'M-2', confidence:{ contract_ref:'CONF-MISSING@1.0', value:0.92 } });
  const result = await run(doc); assert.notEqual(result.status, 0); assert.match(result.stderr, /unresolved confidence contract/);
});

test('accepts validated derived item with resolvable evidence citation provenance and confidence', async () => {
  const doc = structuredClone(base); doc.items.push(evidence());
  doc.items.push({ id:'CLM-2', semantic_type:'claim', producer:'engine', produced_at_utc:'2026-09-07T12:01:00Z', source_authority:'analytics_product', lifecycle_state:'validated', ai_derived:false, method_id:'M-2', evidence_refs:['E-1'], citation_refs:['CIT-TEST@1.0'], provenance_refs:['PROV-TEST@1.0'], confidence:{ contract_ref:'CONF-TEST@1.0', value:0.92 } });
  doc.provenance_records.push({ id:'PROV-TEST', version:'1.0', producer:'engine', produced_at_utc:'2026-09-07T12:01:00Z', method_id:'M-2', input_refs:['E-1'], output_ref:'CLM-2', citation_refs:['CIT-TEST@1.0'] });
  assert.equal((await run(doc)).status, 0);
});
