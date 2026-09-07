import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const repo = process.cwd();
const validator = path.join(repo, '.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs');
const manifestPath = path.join(repo, 'docs/data/knowledge-ai-seed-reconciliation.json');
const contractPath = path.join(repo, 'docs/data/knowledge-ai-evidence-contract.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));

function run(mutator) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dsg-f3-'));
  fs.mkdirSync(path.join(tmp, '.github/scripts'), { recursive: true });
  fs.mkdirSync(path.join(tmp, 'docs/data'), { recursive: true });
  for (const source of manifest.sources) {
    const src = path.join(repo, source.path);
    const dst = path.join(tmp, source.path);
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
  }
  const m = structuredClone(manifest);
  const c = structuredClone(contract);
  mutator?.(m, c, tmp);
  fs.writeFileSync(path.join(tmp, 'docs/data/knowledge-ai-seed-reconciliation.json'), JSON.stringify(m, null, 2));
  fs.writeFileSync(path.join(tmp, 'docs/data/knowledge-ai-evidence-contract.json'), JSON.stringify(c, null, 2));
  fs.copyFileSync(validator, path.join(tmp, '.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs'));
  return spawnSync(process.execPath, ['.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs'], { cwd: tmp, encoding: 'utf8' });
}

test('accepts the bounded governed F3 seed set', () => {
  const r = run();
  assert.equal(r.status, 0, r.stderr + r.stdout);
});

test('fails closed when a source assertion drifts', () => {
  const r = run((m) => { m.seeds[0].required_fragments[0] = 'THIS AUTHORITATIVE ASSERTION DOES NOT EXIST'; });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /source drifted/);
});

test('fails closed on unresolved knowledge item', () => {
  const r = run((m) => { m.seeds[0].knowledge_item_ref = 'EVD-DOES-NOT-EXIST'; });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /unresolved knowledge_item_ref/);
});

test('fails closed when semantic type is flattened', () => {
  const r = run((m) => { m.seeds[0].semantic_type = 'claim'; });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /semantic_type differs/);
});

test('fails closed when governed bounds are exceeded', () => {
  const r = run((m) => { m.bounds.max_seeds = 2; });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /seed count exceeds governed bound/);
});

test('fails closed when source authority is downgraded', () => {
  const r = run((m) => { m.sources[0].source_authority = 'projection'; });
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /source must be repository_authority/);
});
