import assert from 'node:assert/strict';
import test from 'node:test';
import { PixInsightReconciliationService } from './pixinsight-reconciliation.mjs';

const catalogItems = () => ([
  {
    catalogItemId: 'CAT-SESSION-2026-07-15-2026-07-16',
    entityId: '2026-07-15_2026-07-16',
    qualityState: 'ACCEPTED'
  }
]);

const assets = () => ([
  { assetId: 'asset:raw-001', integrityState: 'VERIFIED' },
  { assetId: 'asset:raw-002', integrityState: 'VERIFIED' },
  { assetId: 'candidate:master-light-001', integrityState: 'VERIFIED' },
  { assetId: 'asset:conflicted-001', integrityState: 'CONFLICT' }
]);

const manifest = () => ({
  observationContext: {
    sessionId: '2026-07-15_2026-07-16'
  },
  processingRun: {
    inputs: ['asset:raw-001', 'asset:raw-002'],
    outputs: ['candidate:master-light-001']
  }
});

test('classifies a fully correlated manifest as matched', () => {
  const service = new PixInsightReconciliationService({ catalogItems: catalogItems(), assets: assets() });
  const result = service.reconcile(manifest(), { reconciledAt: '2026-08-05T22:10:00Z' });

  assert.equal(result.state, 'matched');
  assert.equal(result.session.matched, true);
  assert.equal(result.inputs.matched, 2);
  assert.equal(result.outputs.matched, 1);
  assert.deepEqual(result.inputs.missing, []);
  assert.deepEqual(result.outputs.missing, []);
  assert.deepEqual(result.authority, {
    catalog: 'AP-014',
    assetsAndProvenance: 'AP-013',
    mode: 'read-only'
  });
});

test('classifies missing catalog or asset references as partially-matched', () => {
  const service = new PixInsightReconciliationService({ catalogItems: catalogItems(), assets: assets() });
  const value = manifest();
  value.processingRun.outputs.push('candidate:missing-001');
  const result = service.reconcile(value);

  assert.equal(result.state, 'partially-matched');
  assert.equal(result.session.matched, true);
  assert.deepEqual(result.outputs.missing, ['candidate:missing-001']);
});

test('classifies an empty unmatched candidate as unresolved', () => {
  const service = new PixInsightReconciliationService({ catalogItems: catalogItems(), assets: assets() });
  const result = service.reconcile({
    observationContext: { sessionId: 'unknown-session' },
    processingRun: { inputs: [], outputs: [] }
  });

  assert.equal(result.state, 'unresolved');
  assert.equal(result.session.matched, false);
});

test('classifies authoritative asset conflicts as conflict', () => {
  const service = new PixInsightReconciliationService({ catalogItems: catalogItems(), assets: assets() });
  const value = manifest();
  value.processingRun.inputs = ['asset:conflicted-001'];
  const result = service.reconcile(value);

  assert.equal(result.state, 'conflict');
  assert.deepEqual(result.authoritativeConflicts, ['asset:conflicted-001']);
});

test('does not mutate authoritative catalog, assets or manifest inputs', () => {
  const catalog = catalogItems();
  const assetRegistry = assets();
  const value = manifest();
  const catalogBefore = structuredClone(catalog);
  const assetsBefore = structuredClone(assetRegistry);
  const manifestBefore = structuredClone(value);
  const service = new PixInsightReconciliationService({ catalogItems: catalog, assets: assetRegistry });

  service.reconcile(value);

  assert.deepEqual(catalog, catalogBefore);
  assert.deepEqual(assetRegistry, assetsBefore);
  assert.deepEqual(value, manifestBefore);
});

test('returns immutable reconciliation snapshots', () => {
  const service = new PixInsightReconciliationService({ catalogItems: catalogItems(), assets: assets() });
  const result = service.reconcile(manifest());

  assert.equal(Object.isFrozen(result), true);
  assert.equal(Object.isFrozen(result.session), true);
  assert.equal(Object.isFrozen(result.inputs), true);
  assert.equal(Object.isFrozen(result.outputs), true);
  assert.equal(Object.isFrozen(result.authority), true);
  assert.throws(() => result.inputs.missing.push('asset:new'), TypeError);
});
