import assert from 'node:assert/strict';
import test from 'node:test';
import { PixInsightSynchronizationLedger } from './pixinsight-ledger.mjs';

const manifest = () => ({
  schemaVersion: '1.0',
  manifestId: 'PXM-20260805T210000Z-LEDGER01',
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
    externalRunId: 'RUN-LEDGER-001',
    startedAt: '2026-08-05T20:00:00Z',
    completedAt: '2026-08-05T20:30:00Z',
    processes: ['ImageIntegration'],
    inputs: ['asset:raw-001'],
    outputs: ['candidate:master-light-001'],
    parameters: { drizzle: false }
  }
});

test('accepts the first valid manifest and appends one immutable record', () => {
  const ledger = new PixInsightSynchronizationLedger();
  const result = ledger.append(manifest(), { receivedAt: '2026-08-05T21:01:00Z' });
  assert.equal(result.outcome, 'accepted');
  assert.equal(result.sequence, 1);
  assert.equal(ledger.records.length, 1);
  assert.equal(Object.isFrozen(result), true);
  assert.throws(() => { result.outcome = 'changed'; }, TypeError);
});

test('treats an identical retry as duplicate-noop without appending', () => {
  const ledger = new PixInsightSynchronizationLedger();
  const first = ledger.append(manifest());
  const retry = ledger.append(structuredClone(manifest()));
  assert.equal(first.outcome, 'accepted');
  assert.equal(retry.outcome, 'duplicate-noop');
  assert.equal(retry.previousSequence, 1);
  assert.equal(ledger.records.length, 1);
});

test('records a conflict for the same manifestId with a different payload', () => {
  const ledger = new PixInsightSynchronizationLedger();
  const first = ledger.append(manifest());
  const changed = manifest();
  changed.processingRun.outputs.push('candidate:master-light-002');
  const conflict = ledger.append(changed);
  assert.equal(first.outcome, 'accepted');
  assert.equal(conflict.outcome, 'conflict');
  assert.equal(conflict.previousSequence, 1);
  assert.equal(ledger.records.length, 2);
  assert.equal(ledger.findByManifestId(changed.manifestId).sequence, 1);
});

test('rejects invalid manifests without appending to the ledger', () => {
  const ledger = new PixInsightSynchronizationLedger();
  const invalid = manifest();
  invalid.schemaVersion = '9.9';
  const rejected = ledger.append(invalid);
  assert.equal(rejected.outcome, 'rejected');
  assert.equal(ledger.records.length, 0);
  assert.ok(rejected.errors.some((error) => error.code === 'unsupported-schema'));
});

test('supports lookup by manifestId and idempotency key', () => {
  const ledger = new PixInsightSynchronizationLedger();
  const accepted = ledger.append(manifest());
  assert.equal(ledger.findByManifestId(accepted.manifestId), accepted);
  assert.equal(ledger.findByIdempotencyKey(accepted.idempotencyKey), accepted);
  assert.equal(ledger.findByManifestId('missing'), null);
});

test('returns a frozen snapshot of records', () => {
  const ledger = new PixInsightSynchronizationLedger();
  ledger.append(manifest());
  const snapshot = ledger.records;
  assert.equal(Object.isFrozen(snapshot), true);
  assert.throws(() => snapshot.push({}), TypeError);
  assert.equal(ledger.records.length, 1);
});
