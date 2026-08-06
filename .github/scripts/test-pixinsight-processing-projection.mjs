import assert from 'node:assert/strict';
import test from 'node:test';
import { PixInsightProcessingProjectionBuilder } from './pixinsight-processing-projection.mjs';

const manifest = () => ({
  schemaVersion: '1.0',
  manifestId: 'PXM-20260806T140000Z-001',
  source: {
    product: 'PixInsight',
    productVersion: '1.9.3',
    workspaceId: 'WS-LDN1320-001'
  },
  observationContext: {
    sessionId: 'SESSION-20260709-LDN1320'
  },
  processingRun: {
    externalRunId: 'RUN-001',
    startedAt: '2026-08-06T13:00:00Z',
    completedAt: '2026-08-06T13:30:00Z',
    processes: ['WeightedBatchPreprocessing', 'ImageIntegration'],
    inputs: ['asset:raw-001', 'asset:raw-002'],
    outputs: ['candidate:master-light-001'],
    parameters: { rejection: 'WinsorizedSigmaClipping', drizzle: false }
  }
});

const ledgerRecord = (outcome = 'accepted') => ({
  outcome,
  idempotencyKey: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
});

const reconciliation = () => ({
  state: 'matched',
  session: { catalogItemId: 'CAT-SESSION-20260709-LDN1320' }
});

const projectedAt = '2026-08-06T14:00:00.000Z';

test('builds a deterministic derived processing projection', () => {
  const builder = new PixInsightProcessingProjectionBuilder();
  const first = builder.build({ manifest: manifest(), ledgerRecord: ledgerRecord(), reconciliation: reconciliation(), projectedAt });
  const second = builder.build({ manifest: manifest(), ledgerRecord: ledgerRecord(), reconciliation: reconciliation(), projectedAt });

  assert.equal(first.projection.projectionId, second.projection.projectionId);
  assert.equal(first.projection.projectionDigest, second.projection.projectionDigest);
  assert.match(first.projection.projectionDigest, /^sha256:[a-f0-9]{64}$/);
  assert.equal(first.projection.projectionType, 'PIXINSIGHT_PROCESSING');
  assert.equal(first.projection.catalogItemId, 'CAT-SESSION-20260709-LDN1320');
});

test('preserves the AP-013 authority boundary and never grants acceptance authority', () => {
  const builder = new PixInsightProcessingProjectionBuilder();
  const result = builder.build({ manifest: manifest(), ledgerRecord: ledgerRecord(), reconciliation: reconciliation(), projectedAt });

  assert.deepEqual(result.projection.authority, {
    projection: 'AP-014-DERIVED',
    assetsAndProvenance: 'AP-013',
    acceptanceAuthority: false
  });
  assert.ok(result.events.every((event) => event.acceptanceAuthority === false));
});

test('emits correlated immutable audit events', () => {
  const builder = new PixInsightProcessingProjectionBuilder();
  const result = builder.build({ manifest: manifest(), ledgerRecord: ledgerRecord(), reconciliation: reconciliation(), projectedAt });

  assert.equal(result.events.length, 2);
  assert.deepEqual(result.events.map((event) => event.eventType), [
    'PixInsightProjectionCreated',
    'PixInsightProjectionAvailable'
  ]);
  assert.ok(result.events.every((event) => event.correlationId === result.projection.correlationId));
  assert.equal(Object.isFrozen(result.projection), true);
  assert.equal(Object.isFrozen(result.events), true);
  assert.equal(Object.isFrozen(result.events[0]), true);
});

test('rejects ledger records that were not accepted', () => {
  const builder = new PixInsightProcessingProjectionBuilder();
  assert.throws(
    () => builder.build({ manifest: manifest(), ledgerRecord: ledgerRecord('conflict'), reconciliation: reconciliation(), projectedAt }),
    /Only accepted ledger records/
  );
});

test('copies processing collections so later source mutations do not change the projection', () => {
  const builder = new PixInsightProcessingProjectionBuilder();
  const source = manifest();
  const result = builder.build({ manifest: source, ledgerRecord: ledgerRecord(), reconciliation: reconciliation(), projectedAt });

  source.processingRun.processes.push('NoiseXTerminator');
  source.processingRun.inputs.push('asset:raw-003');
  source.processingRun.parameters.drizzle = true;

  assert.deepEqual(result.projection.processing.processes, ['WeightedBatchPreprocessing', 'ImageIntegration']);
  assert.deepEqual(result.projection.processing.inputReferences, ['asset:raw-001', 'asset:raw-002']);
  assert.equal(result.projection.processing.parameters.drizzle, false);
});
