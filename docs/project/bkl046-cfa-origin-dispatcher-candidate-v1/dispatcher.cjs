'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const {createHash} = require('node:crypto');
const {setTimeout: sleep} = require('node:timers/promises');
const {finishCfaOriginal} = require('./supervisore.cjs');
const {verifierFor} = require('./verificatore.cjs');
const {publish}=require('./archivia.cjs');
const {holdDuring} = require('./archive_hold.cjs');

const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');
const operation = 'BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001';
const reservationId = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

async function readBound(registry, owned) {
  const active = await fs.readFile(path.join(registry, 'active.json'));
  const record = JSON.parse(active);
  const reservation = record.reservation;
  assert.match(reservation, reservationId);
  assert.equal(record.protocol, 'DSG_PI_SERIAL_V1');
  assert.equal(record.milestone, 'BKL-046');
  assert.equal(record.operation, operation);
  const prefix = path.join(registry, reservation);
  const acquired = await fs.readFile(prefix + '-acquired.json');
  const original = await fs.readFile(prefix + '-original.json');
  assert.deepEqual(acquired, active);
  const identity = JSON.parse(original.toString('utf8').replace(
    /("creationFiletime"\s*:\s*)([1-9][0-9]{0,19})(?=\s*[,}])/, '$1"$2"'));
  assert.deepEqual(identity, {pid: owned.child.pid, creationFiletime: owned.identity.creationFiletime,
    callerPid: process.pid});
  assert.equal(owned.identity.pid, owned.child.pid);
  assert.equal(owned.identity.callerPid, process.pid);
  return {reservation, acquired, original};
}

function continuation(owned, bound) {
  return {
    protocol: 'BKL046_CFA_XDRZ_ORIGIN_START_BOUND_PARENT_V1', operation, reservation: bound.reservation,
    manifestSha256: '61d38f0160ba2650cea167e7e1a5fbe5af1d4b448ddc085f2f8845f36e7a4150',
    pid: owned.child.pid, callerPid: process.pid, creationFiletime: owned.identity.creationFiletime,
    activeSha256: digest(bound.acquired), originalSha256: digest(bound.original),
    planSha256: 'ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a',
    subjectSha256: '4aa98f614ab6e53c520662659ce91ce1a352b6d78291a20f2dd6cd9e0f0d9b3e',
    caseId: 'all-four-origin-cases'
  };
}

async function dispatchBound({owned, channel, python, registry, run, archiveRoot, holdArgs, authority}) {
  const {child} = owned;
  assert.equal(child, channel.child);
  const bound = await readBound(registry, owned);
  const {reservation} = bound;
  const control = path.join(run, 'control');
  const verifier = verifierFor(python,run,authority);
  let index = 0, window, capture, comparison, publication;

  async function send(message) {
    const frame = JSON.stringify(message) + '\n';
    assert(Buffer.byteLength(frame) <= 4096, 'parent command too large');
    await new Promise((resolve, reject) => child.stdin.write(frame, (error) => error ? reject(error) : resolve()));
  }

  async function request(action, context, fields = {}) {
    const reply = 'reply-' + ++index;
    await send({action, context, reply, ...fields});
    const deadline = Date.now() + 32000;
    const file = path.join(control, reply + '.json');
    while (Date.now() < deadline) {
      try {
        const bytes = await fs.readFile(file);
        assert(bytes.length > 0 && bytes.length <= 4096, 'parent response size differs');
        return JSON.parse(bytes);
      } catch (error) {
        if (error.code !== 'ENOENT') throw error;
        if (child.exitCode !== null || child.signalCode !== null) throw Error('CFA parent exited before reply');
        await sleep(20);
      }
    }
    throw Error('CFA parent reply timed out');
  }

  async function revalidateR4() {
    const current = await readBound(registry, owned);
    assert.deepEqual(current, bound, 'R4 acquisition changed during supervision');
  }

  const deadline = setTimeout(() => child.stdin.end(), 480000);
  try {
    await send(continuation(owned, bound));
    const custody = {child, release: () => holdDuring(python, publication, async () => {
      await revalidateR4();
      return owned.release();
    }, holdArgs)};
    return await finishCfaOriginal({owned: custody, channel, reservation,
      checkpoint: async (phase, context) => {
        await revalidateR4();
        if (phase !== 'before-capture') await verifier.revalidate(context, comparison);
        if (phase === 'before-release') await publication.verify();
      },
      findWindow: async (context) => {
        window = (await request('find', context)).window;
        return window;
      },
      capture: async (context, expected) => {
        const result = await request('capture', context, {window: expected});
        const bytes = await fs.readFile(path.join(control, 'frame.bmp'));
        capture = digest(bytes);
        assert.equal(result.sha256, capture);
        return {window: result.window, bytes};
      },
      compare: async (context) => {
        const scored = await verifier.compare(context);
        comparison = scored.receiptSha256;
        assert.deepEqual(await request('arm', context, {window, capture, comparison}), {armed: true});
        return scored;
      },
      publish: async (name, bytes) => {
        assert(['window-capture', 'normal-close'].includes(name));
        const file = path.join(control, name + '.bin');
        const handle = await fs.open(file, 'wx');
        try {
          await handle.writeFile(bytes);
          await handle.sync();
        } finally {
          await handle.close();
        }
        return {sha256: digest(await fs.readFile(file))};
      },
      close: async (context, expected) => {
        const result = await request('close', context, {window: expected, capture, comparison});
        assert.deepEqual(result, {context, window: expected, nativeExit: 0, capture, comparison});
        return {window: result.window, requested: true, bytes: Buffer.from(JSON.stringify(result))};
      },
      verifyFinal: async (context, evidence) => {
        await verifier.revalidate(context, evidence.comparison);
        publication=await publish({root:archiveRoot,run,acquired:bound.acquired,original:bound.original,
          receipt:verifier.receipt,receiptSha256:evidence.comparison,reservation,
          capturePin:evidence.screenshot,closePin:evidence.closed,
          entryFile:path.join(run,'batch-entry.js'),entryPin:context.entryScriptSha256,
          windowFile:path.join(control,'window-capture.bin'),closeFile:path.join(control,'normal-close.bin')});
        return {verified: true, reservation, originalWindowClosed: true, originalNativeExitCode: 0,
          outputsReadBack: true};
      }
    });
  } finally {
    clearTimeout(deadline);
    child.stdin.end();
  }
}

module.exports = {dispatchBound, readBound};