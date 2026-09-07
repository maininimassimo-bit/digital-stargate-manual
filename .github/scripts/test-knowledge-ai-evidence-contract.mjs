import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const validator = '.github/scripts/verify-knowledge-ai-evidence-contract.mjs';
const base = {
  schema_version: '1.0', component: 'DSG.KnowledgeAIEvidenceContract', authority: 'projection',
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

test('accepts incomplete AI inference without evidence', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'INF-1', semantic_type:'inference', producer:'AI', producer_version:'1', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'projection', lifecycle_state:'incomplete', ai_derived:true, method_id:'M-1' });
  assert.equal((await run(doc)).status, 0);
});

test('rejects validated AI inference without evidence and citations', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'INF-2', semantic_type:'inference', producer:'AI', producer_version:'1', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'projection', lifecycle_state:'validated', ai_derived:true, method_id:'M-1' });
  const result = await run(doc);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /requires evidence_refs/);
});

test('rejects confidence without a stable versioned contract reference', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'CLM-1', semantic_type:'claim', producer:'engine', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'projection', lifecycle_state:'draft', ai_derived:false, method_id:'M-2', confidence:{ contract_ref:'CONF-MISSING@1.0', value:0.92 } });
  const result = await run(doc);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /unresolved confidence contract/);
});

test('accepts validated derived item with evidence, citation and confidence contract', async () => {
  const doc = structuredClone(base);
  doc.items.push({ id:'CLM-2', semantic_type:'claim', producer:'engine', produced_at_utc:'2026-09-07T12:00:00Z', source_authority:'analytics_product', lifecycle_state:'validated', ai_derived:false, method_id:'M-2', evidence_refs:['E-1'], citation_refs:['C-1'], confidence:{ contract_ref:'CONF-TEST@1.0', value:0.92 } });
  assert.equal((await run(doc)).status, 0);
});
