import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { validateReadModel } from './verify-knowledge-ai-read-model.mjs';

const source = JSON.parse(fs.readFileSync('docs/data/knowledge-ai-evidence-contract.json', 'utf8'));
const fixture = JSON.parse(fs.readFileSync('docs/data/knowledge-ai-read-model.json', 'utf8'));
const clone = x => structuredClone(x);
const errorsFor = x => validateReadModel(x, source);
const find = (x, ref) => x.items.find(i => i.source_item_ref === ref);

test('accepts governed F4 consumer projection', () => assert.deepEqual(errorsFor(fixture), []));

test('rejects semantic flattening', () => {
  const x = clone(fixture); find(x, 'CLM-BKL044-F3-NEXT-INCREMENT').semantic_type = 'observation';
  assert.ok(errorsFor(x).some(e => e.includes('semantic_type')));
});

test('rejects authority escalation', () => {
  const x = clone(fixture); find(x, 'INF-BKL044-F2-INCOMPLETE').source_authority = 'repository_authority';
  assert.ok(errorsFor(x).some(e => e.includes('source_authority')));
});

test('rejects lifecycle promotion', () => {
  const x = clone(fixture); find(x, 'INF-BKL044-F2-INCOMPLETE').lifecycle_state = 'validated';
  assert.ok(errorsFor(x).some(e => e.includes('lifecycle_state')));
});

test('rejects Citation loss', () => {
  const x = clone(fixture); find(x, 'CLM-BKL044-F3-NEXT-INCREMENT').citations = [];
  assert.ok(errorsFor(x).some(e => e.includes('Citation identities')));
});

test('rejects Citation locator mutation', () => {
  const x = clone(fixture); find(x, 'CLM-BKL044-F3-NEXT-INCREMENT').citations[0].locator.value = 'docs/project/OTHER.md';
  assert.ok(errorsFor(x).some(e => e.includes('Citation locator mismatch')));
});

test('rejects Provenance loss', () => {
  const x = clone(fixture); find(x, 'CLM-BKL044-F3-NEXT-INCREMENT').provenance = [];
  assert.ok(errorsFor(x).some(e => e.includes('Provenance identities')));
});

test('rejects Provenance chain mutation', () => {
  const x = clone(fixture); find(x, 'CLM-BKL044-F3-NEXT-INCREMENT').provenance[0].input_refs = [];
  assert.ok(errorsFor(x).some(e => e.includes('Provenance input_refs mismatch')));
});

test('rejects Confidence contract loss', () => {
  const x = clone(fixture); delete find(x, 'CLM-BKL044-F3-NEXT-INCREMENT').confidence;
  assert.ok(errorsFor(x).some(e => e.includes('Confidence must not be dropped')));
});

test('rejects AI marker loss', () => {
  const x = clone(fixture); find(x, 'INF-BKL044-F2-INCOMPLETE').ai_derived = false;
  assert.ok(errorsFor(x).some(e => e.includes('ai_derived') || e.includes('AI-derived marker')));
});
