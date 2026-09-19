import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import assert from 'node:assert/strict';

const root = process.cwd();
const script = path.join(root, '.github/scripts/verify-bkl-036-f2-evidence-envelope.mjs');
const fixturePath = path.join(root, 'docs/data/bkl-036-f2-descriptive-health-fixture.json');

const run = (fixture) => {
  const dir = mkdtemp(path.join(os.tmpdir(), 'dsg-bkl036-f2-'));
  return dir.then(async (tmp) => {
    const file = path.join(tmp, 'fixture.json');
    await writeFile(file, JSON.stringify(fixture));
    const result = spawnSync(process.execPath, [script, file], { cwd: root, encoding: 'utf8' });
    await rm(tmp, { recursive: true, force: true });
    return result;
  });
};

test('accepts the bounded offline descriptive fixture', async () => {
  const fixture = JSON.parse(await readFile(fixturePath, 'utf8'));
  const result = await run(fixture);
  assert.equal(result.status, 0, result.stderr);
});

for (const [name, mutate] of [
  ['rejects score promotion', f => { f.descriptive_projection.score_available = true; }],
  ['rejects missing mandatory domain', f => { f.evidence = f.evidence.filter(x => x.domain !== 'mount'); }],
  ['rejects comparable incomplete evidence', f => { f.evidence.find(x => x.domain === 'weather').compatibility = 'COMPARABLE'; }],
  ['rejects runtime acceptance', f => { f.evidence[0].runtime_disposition = 'LIVE_RUNTIME_ACCEPTED'; }],
  ['rejects operational key', f => { f.score = 0.5; }]
]) {
  test(name, async () => {
    const fixture = JSON.parse(await readFile(fixturePath, 'utf8'));
    const result = await run(mutate(fixture));
    assert.notEqual(result.status, 0, result.stdout || result.stderr || 'expected validator failure');
  });
}
