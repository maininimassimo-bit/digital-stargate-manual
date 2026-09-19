import { readFile, writeFile, mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import assert from 'node:assert/strict';

const root = process.cwd();
const script = path.join(root, '.github/scripts/verify-bkl-036-f4-archived-telemetry.mjs');
const fixture = path.join(root, 'docs/data/bkl-036-f4-telemetry-ingest-fixture.json');
const run = async value => {
  const dir = await mkdtemp(path.join(os.tmpdir(), 'dsg-bkl036-f4-'));
  const file = path.join(dir, 'input.json');
  await writeFile(file, JSON.stringify(value));
  const result = spawnSync(process.execPath, [script, file], {cwd: root, encoding: 'utf8'});
  await rm(dir, {recursive:true, force:true});
  return result;
};

test('accepts a bounded archived snapshot', async () => {
  const result = await run(JSON.parse(await readFile(fixture, 'utf8')));
  assert.equal(result.status, 0, result.stderr);
});

for (const [name, mutate] of [
  ['rejects live transport', value => { value.safety_boundary.live_transport_used = true; }],
  ['rejects a missing domain', value => { value.domains = value.domains.slice(1); }],
  ['rejects comparable stale evidence', value => { value.domains[0].evidence_status = 'STALE'; value.domains[0].compatibility = 'COMPARABLE'; }],
  ['rejects present evidence without timestamps', value => { value.domains[0].evidence_status = 'PRESENT'; value.domains[0].compatibility = 'COMPARABLE'; }]
]) {
  test(name, async () => {
    const value = JSON.parse(await readFile(fixture, 'utf8'));
    const result = await run(mutate(value) || value);
    assert.notEqual(result.status, 0, result.stdout || result.stderr);
  });
}
