'use strict';

const assert = require('node:assert/strict');
const {execFile} = require('node:child_process');
const {createHash} = require('node:crypto');
const fs = require('node:fs/promises');
const path = require('node:path');
const {promisify} = require('node:util');

const exec = promisify(execFile);
const digest = raw => createHash('sha256').update(raw).digest('hex');
const component = 'd71f3a4dfc2ae411f4a7da212ef3fb37e4f04149c6b70f426e32f9ed3a20a9a2';
const plan = '677460604bd564285b0571a7149f22f7ae6ea7aed27e5badc1d71b42b0474a0f';
const comparisonPin = '10321edfe7218f9c3dd082d59148004b76303b774c7772b12f8f605f382c2423';
const classifierPin = '54615e810d86dc95ea3ad2ca9a2b94520b557c313cede84b80cf672524304be6';
const operation = 'BKL046_CFA_XDRZ_WEIGHT_WINDOW_DSG_SHARED_001';
const cases = ['unmasked', 'mask-green', 'mask-wrong-channel', 'zero-detector', 'zero-reference'];
const productNames = ['batch.done.json', 'events.txt',
  ...cases.flatMap(id => ['rgb', 'weight'].map(kind => id + '-' + kind + '.fits'))].sort();

async function read(file, limit = 262144) {
  const stat = await fs.lstat(file);
  assert(stat.isFile() && !stat.isSymbolicLink() && stat.size > 0 && stat.size <= limit,
    'Invalid comparison member: ' + path.basename(file));
  const bytes = await fs.readFile(file);
  assert.equal(bytes.length, stat.size, 'Member length changed while reading');
  return bytes;
}

function verifierFor(python, packages, fixture, run) {
  const outputs = path.join(run, 'products');
  const receipt = path.join(run, 'control', 'comparison.json');

  function contextMatches(context) {
    assert.equal(context.operation, operation);
    assert.equal(context.plan, plan);
    assert.equal(context.subject, component);
    assert.equal(path.basename(run), context.reservation);
    assert.match(context.reservation, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
    assert.match(context.batchMarkerSha256, /^[0-9a-f]{64}$/);
  }

  async function revalidate(context, expectedReceipt) {
    contextMatches(context);
    const raw = await read(receipt);
    assert.equal(digest(raw), expectedReceipt, 'Comparison receipt changed');
    const scored = JSON.parse(raw);
    assert.equal(scored.schema, 'BKL046_CFA_WEIGHT_WINDOW_OUTPUT_RECEIPT_V1');
    assert.equal(scored.reservation, context.reservation);
    assert.equal(scored.operation, context.operation);
    assert.equal(scored.planSha256, context.plan);
    assert.equal(scored.componentSha256, context.subject);
    assert.equal(scored.classifierSha256, classifierPin);
    assert.equal(scored.outputHashes['batch.done.json'], context.batchMarkerSha256);
    assert.equal(scored.provesCoordinatorAdmission, false);
    assert.equal(scored.nativeProvenanceVerified, false);
    assert.equal(scored.scientificClosures, 0);
    assert.equal(scored.resolved, true, 'Unresolved CFA comparison retained');
    assert.deepEqual(Object.keys(scored.outputHashes).sort(), productNames);
    assert.deepEqual((await fs.readdir(outputs)).sort(), productNames);
    for (const name of productNames) {
      assert.equal(digest(await read(path.join(outputs, name))), scored.outputHashes[name],
        'Product changed: ' + name);
    }
    assert.equal(digest(await read(receipt)), expectedReceipt, 'Receipt readback changed');
    return scored;
  }

  async function compare(context) {
    contextMatches(context);
    const raw = await read(path.join(__dirname, 'confronto.py'));
    assert.equal(digest(raw), comparisonPin, 'Comparison source changed');
    await exec(python, ['-I', '-B', '-S', '-c', raw.toString('utf8'),
      path.join(__dirname, 'piano-componenti.json'), path.join(__dirname, 'classifica.py'),
      packages, fixture, outputs, receipt, context.reservation, context.batchMarkerSha256],
    {windowsHide: true, timeout: 60000});
    const receiptSha256 = digest(await read(receipt));
    await revalidate(context, receiptSha256);
    return {verified: true, reservation: context.reservation,
      batchMarkerSha256: context.batchMarkerSha256, receiptSha256};
  }

  return {compare, revalidate};
}

module.exports = {verifierFor};
