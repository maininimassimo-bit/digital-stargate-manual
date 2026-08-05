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

const createConflict = (ledger) => {
  const accepted = ledger.append(manifest(), { receivedAt: '2026-08-05T21:01:00Z' });
  const changed = manifest();
  changed.processingRun.outputs.push('candidate:master-light-002');
  const conflict = ledger.append(changed, { receivedAt: '2026-08-05T21:02:00Z' });
  return { accepted, conflict };
};

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
  const { accepted, conflict } = createConflict(ledger);
  assert.equal(accepted.outcome, 'accepted');
  assert.equal(conflict.outcome, 'conflict');
  assert.equal(conflict.previousSequence, 1);
  assert.equal(ledger.records.length, 2);
  assert.equal(ledger.findByManifestId(conflict.manifestId).sequence, 1);
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

test('returns frozen snapshots of records and audit events', () => {
  const ledger = new PixInsightSynchronizationLedger();
  ledger.append(manifest());
  const records = ledger.records;
  const audit = ledger.auditTrail;
  assert.equal(Object.isFrozen(records), true);
  assert.equal(Object.isFrozen(audit), true);
  assert.equal(Object.isFrozen(audit[0]), true);
  assert.throws(() => records.push({}), TypeError);
  assert.throws(() => audit.push({}), TypeError);
});

test('audits accepted, duplicate, conflict and rejected attempts in order', () => {
  const ledger = new PixInsightSynchronizationLedger();
  ledger.append(manifest(), { receivedAt: '2026-08-05T21:01:00Z' });
  ledger.append(manifest(), { receivedAt: '2026-08-05T21:02:00Z' });
  const changed = manifest();
  changed.processingRun.outputs.push('candidate:master-light-002');
  ledger.append(changed, { receivedAt: '2026-08-05T21:03:00Z' });
  const invalid = manifest();
  invalid.schemaVersion = '9.9';
  ledger.append(invalid, { receivedAt: '2026-08-05T21:04:00Z' });

  assert.deepEqual(
    ledger.auditTrail.map((entry) => entry.eventType),
    ['manifest-accepted', 'manifest-duplicate', 'manifest-conflict', 'manifest-rejected']
  );
  assert.deepEqual(ledger.auditTrail.map((entry) => entry.auditSequence), [1, 2, 3, 4]);
});

test('resolves a conflict without replacing the authoritative accepted record', () => {
  const ledger = new PixInsightSynchronizationLedger();
  const { accepted, conflict } = createConflict(ledger);
  const resolution = ledger.resolveConflict(conflict.sequence, {
    decision: 'retain-authoritative',
    reason: 'AP-013 provenance remains authoritative.',
    operatorId: 'operator-001',
    resolvedAt: '2026-08-05T21:05:00Z'
  });

  assert.equal(resolution.outcome, 'conflict-resolved');
  assert.equal(resolution.authoritativeSequence, accepted.sequence);
  assert.equal(ledger.findByManifestId(accepted.manifestId), accepted);
  assert.equal(ledger.records.length, 3);
  assert.equal(ledger.auditTrail.at(-1).eventType, 'conflict-resolved');
});

test('rejects unsupported, incomplete or duplicate conflict resolutions', () => {
  const ledger = new PixInsightSynchronizationLedger();
  const { conflict } = createConflict(ledger);

  assert.throws(() => ledger.resolveConflict(conflict.sequence, {
    decision: 'promote-candidate',
    reason: 'Not allowed.',
    operatorId: 'operator-001'
  }), /Unsupported conflict resolution decision/);

  assert.throws(() => ledger.resolveConflict(conflict.sequence, {
    decision: 'reject-candidate',
    reason: '',
    operatorId: 'operator-001'
  }), /reason is required/);

  ledger.resolveConflict(conflict.sequence, {
    decision: 'reject-candidate',
    reason: 'Candidate contradicts authoritative provenance.',
    operatorId: 'operator-001'
  });

  assert.throws(() => ledger.resolveConflict(conflict.sequence, {
    decision: 'reject-candidate',
    reason: 'Repeated decision.',
    operatorId: 'operator-001'
  }), /already been resolved/);
});
