import assert from 'node:assert/strict';
import test from 'node:test';
import { canonicalize, digestManifest, idempotencyKey, validateManifest } from './pixinsight-manifest.mjs';

const manifest = () => ({
  schemaVersion: '1.0',
  manifestId: 'PXM-20260805T210000Z-001',
  exportedAt: '2026-08-05T21:00:00Z',
  source: {
    product: 'PixInsight',
    productVersion: '1.9.3',
    hostId: 'EAGLE-MANCIANO',
    workspaceId: 'WS-M31-001'
  },
  observationContext: {
    sessionId: 'SESSION-20260805-M31',
    target: 'M31',
    projectId: 'PROJECT-ANDROMEDA',
    campaignId: 'CAMPAIGN-2026'
  },
  processingRun: {
    externalRunId: 'RUN-001',
    startedAt: '2026-08-05T20:00:00Z',
    completedAt: '2026-08-05T20:30:00Z',
    processes: ['WeightedBatchPreprocessing', 'ImageIntegration'],
    inputs: ['asset:raw-001', 'asset:raw-002'],
    outputs: ['candidate:master-light-001'],
    parameters: { rejection: { algorithm: 'WinsorizedSigmaClipping' }, drizzle: false }
  }
});

test('accepts a valid governed PixInsight manifest', () => {
  const result = validateManifest(manifest());
  assert.equal(result.valid, true);
  assert.deepEqual(result.errors, []);
});

test('rejects unsupported schema and non-PixInsight source', () => {
  const value = manifest();
  value.schemaVersion = '2.0';
  value.source.product = 'OtherProduct';
  const result = validateManifest(value);
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((error) => error.code === 'unsupported-schema'));
  assert.ok(result.errors.some((error) => error.path === '$.source.product'));
});

test('rejects unexpected properties without mutating the payload', () => {
  const value = manifest();
  value.secret = 'must-not-pass';
  value.processingRun.execute = true;
  const before = structuredClone(value);
  const result = validateManifest(value);
  assert.equal(result.valid, false);
  assert.deepEqual(value, before);
  assert.equal(result.errors.filter((error) => error.code === 'additional-property').length, 2);
});

test('canonicalization is stable across object key order', () => {
  const first = manifest();
  const second = {
    processingRun: first.processingRun,
    observationContext: first.observationContext,
    source: first.source,
    exportedAt: first.exportedAt,
    manifestId: first.manifestId,
    schemaVersion: first.schemaVersion
  };
  assert.equal(canonicalize(first), canonicalize(second));
  assert.equal(digestManifest(first), digestManifest(second));
  assert.equal(idempotencyKey(first), idempotencyKey(second));
});

test('digest and idempotency key change when payload changes', () => {
  const first = manifest();
  const second = structuredClone(first);
  second.processingRun.outputs.push('candidate:master-light-002');
  assert.notEqual(digestManifest(first), digestManifest(second));
  assert.notEqual(idempotencyKey(first), idempotencyKey(second));
});

test('idempotency key is a lowercase SHA-256 value', () => {
  assert.match(idempotencyKey(manifest()), /^[a-f0-9]{64}$/);
});
