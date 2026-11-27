'use strict';

const assert = require('node:assert/strict');
const {createHash} = require('node:crypto');
const fs = require('node:fs/promises');
const path = require('node:path');
const {verifierFor} = require('./comparator.cjs');
const {publishEvidence} = require('./archivio.cjs');

const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const [python, packages, fixture, laboratory, scratch, report] = process.argv.slice(2);

async function main() {
  const original = path.join(laboratory, 'original');
  const markerBytes = await fs.readFile(path.join(original, 'batch.done.json'));
  const marker = JSON.parse(markerBytes);
  const context = {operation: marker.operation, reservation: marker.reservation, plan: marker.planSha256,
    subject: marker.componentContractSha256, batchMarkerSha256: digest(markerBytes)};
  const run = path.join(scratch, marker.reservation);
  const outputs = path.join(run, 'products');
  const state = path.join(run, 'control');
  const root = path.join(scratch, 'archive');
  const registry = path.join(scratch, 'simulated-registry');
  await fs.mkdir(scratch);
  await Promise.all([fs.mkdir(root), fs.mkdir(registry), fs.mkdir(state, {recursive: true})]);
  await fs.cp(original, outputs, {recursive: true, errorOnExist: true});
  await fs.writeFile(path.join(run, 'batch-entry.js'), 'test entry');
  const checker = verifierFor(python, packages, fixture, run);
  await assert.rejects(checker.compare({...context, subject: '0'.repeat(64)}));
  const comparison = await checker.compare(context);
  const scored = await checker.revalidate(context, comparison.receiptSha256);
  assert.equal(scored.comparison.weightProfile, 'RAW');

  const screenshot = Buffer.from('simulated capture');
  const closed = Buffer.from('simulated close');
  const acquired = Buffer.from('simulated acquisition');
  const originalParent = Buffer.from('simulated parent');
  await Promise.all([
    fs.writeFile(path.join(state, 'window-capture.bin'), screenshot),
    fs.writeFile(path.join(state, 'normal-close.bin'), closed),
    fs.writeFile(path.join(registry, context.reservation + '-acquired.json'), acquired),
    fs.writeFile(path.join(registry, context.reservation + '-original.json'), originalParent),
  ]);
  const evidence = {comparison: comparison.receiptSha256, screenshot: digest(screenshot), closed: digest(closed),
    terminal: {status: 'SIMULATED', nativeExitCode: 0, scientificClosures: 0}};
  const args = {root, state, outputs, registry, context, evidence, acquired, original: originalParent};
  const archive = await publishEvidence(args);
  assert.equal(archive.memberCount, 17);
  await archive.verify();
  await assert.rejects(publishEvidence(args), {code: 'EEXIST'});

  const product = path.join(outputs, 'zero-reference-weight.fits');
  await fs.appendFile(product, 'change after compare');
  await assert.rejects(checker.revalidate(context, comparison.receiptSha256), /Product changed/);
  const archived = path.join(archive.directory, 'events.txt');
  await fs.appendFile(archived, 'change after archival');
  await assert.rejects(archive.verify(), /archive readback differs/);

  await fs.writeFile(report, JSON.stringify({
    schema: 'BKL046_CFA_PRODUCT_HANDOFF_FIXTURE_TEST_V1',
    candidateFilesCompared: Object.keys(scored.outputHashes).length,
    archivedMembers: archive.memberCount,
    independentLauncherFilesOutsideProducts: true,
    rejected: ['foreign component', 'archive overwrite', 'post-comparison change', 'post-archive change'],
    gateAccessed: false, nativeExecutions: 0, scientificClosures: 0
  }, null, 2) + '\n', {flag: 'wx'});
}
main().catch(error => {console.error(error); process.exitCode = 1;});
