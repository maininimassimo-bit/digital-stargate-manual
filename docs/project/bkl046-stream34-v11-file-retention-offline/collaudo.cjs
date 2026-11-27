'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const [source, protocolPath, output] = process.argv.slice(2);
const protocolBytes = fs.readFileSync(protocolPath);
const protocol = JSON.parse(protocolBytes);
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const read = (name, pin) => {
  const bytes = fs.readFileSync(path.join(source, name));
  assert.equal(sha(bytes), pin, name);
  return bytes;
};
const subject = JSON.parse(read('launcher-subject.json', protocol.subjectSha256));
const plan = JSON.parse(read('input-plan.json', subject.memberSha256['input-plan.json']));
const hashName = 'hash_primary2048_file_streaming_h_v2.js';
const bodyName = 'native_stream_hash_witness_body_h_v2.js';
const hashSource = read(hashName, subject.memberSha256[hashName]).toString('utf8');
const include = /^#include "[^"\r\n]+"\r?\n/;
assert.match(hashSource, include);
const program = new vm.Script(hashSource.replace(include, '') + '\n' +
  read(bodyName, subject.memberSha256[bodyName]).toString('utf8'));
const allowed = new Set(plan.files.map(row => row.path));

function createLab(fault = 'none', options = {}) {
  const events = {allocated: 0, opened: 0, closeCalls: 0, initialized: 0, updates: 0,
    finalized: 0, maximumReadRequest: 0, readCalls: 0};
  const handles = new Set();
  const windows = options.windows || [];
  class File {
    constructor() {
      this.fd = null;
      this.offset = fault === 'position-initial' ? 1 : 0;
      this.sizeReads = 0;
      handles.add(this);
      events.allocated++;
    }
    openForReading(filename) {
      assert.ok(allowed.has(filename), 'unplanned physical read');
      events.opened++;
      if (fault === 'open') throw new Error('MOCK_OPEN_ERROR');
      this.fd = fs.openSync(filename, 'r');
      this.initialSize = fs.fstatSync(this.fd).size;
    }
    get position() {
      return this.offset;
    }
    get size() {
      this.sizeReads++;
      if (fault === 'size-limit') return 100667393;
      return this.initialSize + Number(fault === 'size-changed' && this.sizeReads > 1);
    }
    read(type, length) {
      assert.equal(type, 15);
      events.readCalls++;
      events.maximumReadRequest = Math.max(events.maximumReadRequest, length);
      if (fault === 'read') throw new Error('MOCK_READ_ERROR');
      const chunk = Buffer.alloc(length);
      const amount = fs.readSync(this.fd, chunk, 0, length, this.offset);
      this.offset += amount;
      if (fault === 'position-after-read') this.offset--;
      if (fault === 'short-read') return chunk.subarray(0, amount - 1);
      if (fault === 'content-changed') chunk[0] ^= 1;
      return chunk.subarray(0, amount);
    }
    close() {
      events.closeCalls++;
      if (fault === 'close') throw new Error('MOCK_CLOSE_ERROR');
      fs.closeSync(this.fd);
      this.fd = null;
      if (fault === 'close-after-handle-exit') throw new Error('MOCK_CLOSE_AFTER_HANDLE_EXIT');
      if (fault === 'late-image') windows.push({});
    }
  }
  class CryptographicHash {
    constructor(bits) {
      assert.equal(bits, 256);
      this.hash = crypto.createHash('sha256');
    }
    initialize() {
      events.initialized++;
      if (fault === 'hash-init') throw new Error('MOCK_HASH_INIT_ERROR');
    }
    update(chunk) {
      events.updates++;
      if (fault === 'hash-update') throw new Error('MOCK_HASH_UPDATE_ERROR');
      this.hash.update(chunk);
    }
    finalize() {
      events.finalized++;
      if (fault === 'hash-finalize') throw new Error('MOCK_HASH_FINALIZE_ERROR');
      return {toHex: () => this.hash.digest('hex')};
    }
  }
  const context = vm.createContext({
    File, CryptographicHash, DataType_ByteArray: options.dataType ?? 15, ImageWindow: {windows}
  });
  program.runInContext(context);
  return {context, events, handles,
    cleanup() {
      for (const file of handles) {
        if (file.fd !== null) fs.closeSync(file.fd);
      }
    }};
}

function testComplete() {
  const lab = createLab();
  try {
    const state = {retainedIO: [], claimed: false};
    const actual = lab.context.runNativeStreamHashWitness(plan, state);
    assert.equal(actual.status, 'NATIVE_STREAM_HASH_BODY_COMPLETED_NOT_PARENT_ACCEPTANCE');
    assert.equal(actual.totalBytes, plan.totalBytes);
    assert.equal(actual.results.length, 8);
    assert.equal(actual.images, 0);
    assert.equal(actual.scientificProcessExecutions, 0);
    assert.equal(actual.actualNativeMemoryBoundAttested, false);
    assert.equal(state.phase, 'BODY_COMPLETE_NOT_PROCESS_EXIT');
    assert.equal(state.retainedIO.length, 0);
    assert.equal(lab.events.closeCalls, 8);
    const expectedReads = plan.files.reduce((total, row) => total + Math.ceil(row.bytes / 1048576), 0);
    assert.equal(lab.events.readCalls, expectedReads);
    assert.equal(lab.events.maximumReadRequest, 1048576);
    actual.results.forEach((row, i) => {
      assert.equal(row.index, i);
      assert.equal(row.path, plan.files[i].path);
      assert.equal(row.result.sha256, plan.files[i].sha256);
      assert.equal(row.result.bytes, plan.files[i].bytes);
      assert.equal(row.result.maximumChunkBytes, Math.min(row.result.bytes, 1048576));
      assert.equal(row.result.fileClosed, true);
      assert.equal(row.result.actualNativeMemoryBoundAttested, false);
    });
    assert.throws(() => lab.context.runNativeStreamHashWitness(plan, state), /NativeStreamWitnessPrecondition/);
    assert.equal(lab.events.opened, 8);
    return {totalBytes: actual.totalBytes, files: actual.results.length, ...lab.events, secondClaimRefused: true};
  } finally {
    lab.cleanup();
  }
}

const cases = [
  ['open', 'MOCK_OPEN_ERROR', 'OPEN_CALL_CLAIMED'],
  ['position-initial', 'StreamingHashFileSizeOrPosition', 'FILE_OPEN'],
  ['size-limit', 'StreamingHashFileSizeOrPosition', 'FILE_OPEN'],
  ['hash-init', 'MOCK_HASH_INIT_ERROR', 'FILE_OPEN'],
  ['read', 'MOCK_READ_ERROR', 'READ_CALL_CLAIMED'],
  ['short-read', 'StreamingHashShortReadOrPosition', 'CHUNK_READ'],
  ['position-after-read', 'StreamingHashShortReadOrPosition', 'CHUNK_READ'],
  ['hash-update', 'MOCK_HASH_UPDATE_ERROR', 'CHUNK_READ'],
  ['hash-finalize', 'MOCK_HASH_FINALIZE_ERROR', 'CHUNK_HASHED'],
  ['content-changed', 'StreamingHashDigestOrSizeChanged', 'HASH_FINALIZED'],
  ['size-changed', 'StreamingHashDigestOrSizeChanged', 'HASH_FINALIZED'],
  ['close', 'MOCK_CLOSE_ERROR', 'CLOSE_CALL_CLAIMED'],
  ['close-after-handle-exit', 'MOCK_CLOSE_AFTER_HANDLE_EXIT', 'CLOSE_CALL_CLAIMED'],
];
function testFaults() {
  const input = plan.files.find(row => row.bytes === 1048577);
  return cases.map(([fault, error, phase]) => {
    const lab = createLab(fault);
    try {
      const retained = [];
      const run = () => lab.context.hashPrimary2048FileStreamingImmutable(input.path, input.sha256, retained);
      assert.throws(run, {message: error});
      assert.equal(retained.length, 1);
      assert.ok(lab.handles.has(retained[0].file));
      assert.equal(retained[0].phase, phase);
      assert.equal(retained[0].closed, false);
      assert.equal(lab.events.closeCalls, phase === 'CLOSE_CALL_CLAIMED' ? 1 : 0);
      assert.throws(run, /StreamingHashInvalidPinnedPathOrRetainer/);
      assert.equal(lab.events.allocated, 1);
      return {fault, error, phase, reportedClosed: false, retryRefused: true, ...lab.events};
    } finally {
      lab.cleanup();
    }
  });
}

function testPlanGuards() {
  const duplicate = {...plan, files: [...plan.files.slice(0, 7), plan.files[0]]};
  const alteredPath = {...plan, files: [{...plan.files[0], path: plan.files[0].path + '/../foo'}, ...plan.files.slice(1)]};
  const budgets = {...plan, totalBytes: plan.totalBytes + 1};
  const guards = [
    ['duplicate', duplicate, {}, 'NativeStreamWitnessInvalidFilePlan'],
    ['traversal', alteredPath, {}, 'NativeStreamWitnessInvalidFilePlan'],
    ['aggregate-size', budgets, {}, 'NativeStreamWitnessInputBudget'],
    ['image-already-open', plan, {windows: [{}]}, 'NativeStreamWitnessPrecondition'],
    ['unexpected-byte-type', plan, {dataType: 16}, 'NativeStreamWitnessPrecondition'],
  ];
  return guards.map(([label, value, options, error]) => {
    const lab = createLab('none', options);
    try {
      const state = {retainedIO: [], claimed: false};
      assert.throws(() => lab.context.runNativeStreamHashWitness(value, state), {message: error});
      assert.equal(lab.events.allocated, 0);
      return {label, error, allocated: 0, claimed: state.claimed};
    } finally {
      lab.cleanup();
    }
  });
}

const report = {
  schema: 'BKL046_STREAM34_V11_PJSR_SHIM_RESULT_V1',
  subjectSha256: protocol.subjectSha256,
  inputPlanSha256: subject.memberSha256['input-plan.json'],
  protocolSha256: sha(protocolBytes), programSha256: sha(fs.readFileSync(__filename)),
  success: testComplete(), faultCases: testFaults(), planGuards: testPlanGuards(),
  pixInsightStarted: false, actualPjsrMemoryBoundAttested: false, admissionRequested: false,
  scientificClosures: 0
};
fs.writeFileSync(output, JSON.stringify(report, null, 2) + '\n', {flag: 'wx'});
