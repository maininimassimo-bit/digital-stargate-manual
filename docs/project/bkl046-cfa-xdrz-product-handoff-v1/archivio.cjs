'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const {createHash} = require('node:crypto');
const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

async function writeNew(file, bytes) {
  const handle = await fs.open(file, 'wx');
  try {
    await handle.writeFile(bytes);
    await handle.sync();
  } finally {
    await handle.close();
  }
}

async function readPlain(file) {
  const info = await fs.lstat(file);
  assert(info.isFile() && !info.isSymbolicLink(), 'archive member is not a regular file');
  return fs.readFile(file);
}

function archiveTarget(root, reservation) {
  assert.match(reservation, uuid);
  return path.join(root, reservation);
}

async function publishEvidence({root, state, outputs, registry, context, evidence, acquired, original}) {
  const directory = archiveTarget(root, context.reservation);
  const parent = await fs.lstat(root);
  assert(parent.isDirectory() && !parent.isSymbolicLink(), 'archive root is not a regular directory');
  const markerPath = path.join(outputs, 'batch.done.json');
  const receiptPath = path.join(state, 'comparison.json');
  const comparisonBytes = await readPlain(receiptPath);
  assert.equal(digest(comparisonBytes), evidence.comparison, 'archive comparison source changed');
  const comparison = JSON.parse(comparisonBytes);
  assert.equal(comparison.resolved, true, 'archive comparison unresolved');
  assert.equal(comparison.reservation, context.reservation, 'archive foreign comparison');
  assert.equal(comparison.outputHashes['batch.done.json'], context.batchMarkerSha256);
  const specs = [
    ['comparison.json', receiptPath, evidence.comparison],
    ['batch.done.json', markerPath, context.batchMarkerSha256],
    ['events.txt', path.join(outputs, 'events.txt'), comparison.outputHashes['events.txt']],
    ['window.bmp', path.join(state, 'window-capture.bin'), evidence.screenshot],
    ['normal-close.json', path.join(state, 'normal-close.bin'), evidence.closed],
    ['r4-acquired.json', path.join(registry, context.reservation + '-acquired.json'), digest(acquired)],
    ['r4-original.json', path.join(registry, context.reservation + '-original.json'), digest(original)]
  ];
  const exports = Object.entries(comparison.outputHashes).filter(([name]) => name.endsWith(".fits")).sort(([a], [b]) => a.localeCompare(b, 'en'));
  assert.equal(exports.length, 10, 'archive export set differs');
  for (const [name, digest] of exports) {
    assert.match(name, /^[a-z0-9-]+-(rgb|weight)\.fits$/);
    specs.push([name, path.join(outputs, name), digest]);
  }
  // No retry can overwrite a directory or any named evidence member.
  await fs.mkdir(directory);
  const members = [];
  for (const [name, source, expected] of specs) {
    const bytes = await readPlain(source);
    assert.equal(digest(bytes), expected, 'archive source changed: ' + name);
    await writeNew(path.join(directory, name), bytes);
    members.push({name, length: bytes.length, sha256: expected});
  }
  const marker = Buffer.from(JSON.stringify({
    schema: 'BKL046_CFA_ARCHIVED_EVIDENCE_V1',
    state: 'EVIDENCE_ARCHIVED_NOT_RELEASED',
    context, terminal: evidence.terminal, members
  }) + '\n');

  async function verifyMembers(includeMarker) {
    const dir = await fs.lstat(directory);
    assert(dir.isDirectory() && !dir.isSymbolicLink(), 'archive directory changed');
    const expected = members.map(({name}) => name);
    if (includeMarker) expected.push('ARCHIVED.json');
    assert.deepEqual((await fs.readdir(directory)).sort(), expected.sort(), 'archive namespace changed');
    for (const {name, length, sha256} of members) {
      const bytes = await readPlain(path.join(directory, name));
      assert(bytes.length === length && digest(bytes) === sha256, 'archive readback differs: ' + name);
    }
    if (includeMarker) assert.deepEqual(await readPlain(path.join(directory, 'ARCHIVED.json')), marker);
  }

  await verifyMembers(false);
  await writeNew(path.join(directory, 'ARCHIVED.json'), marker);
  await verifyMembers(true);
  const holdEntries = [...members, {name: 'ARCHIVED.json', length: marker.length, sha256: digest(marker)}];
  return {directory, holdEntries, memberCount: members.length, verify: () => verifyMembers(true)};
}

module.exports = {archiveTarget, publishEvidence};