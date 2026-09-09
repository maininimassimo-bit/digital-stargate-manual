import test from 'node:test';
import assert from 'node:assert/strict';
import { provenanceSidecarToManifest } from './pixinsight-provenance-to-manifest.mjs';

const sidecar = {
  schemaVersion: '1.0', sidecarId: 'PXP-20260909T213316284Z-OAT', exportedAt: '2026-09-09T21:33:16.284Z',
  authority: 'processing_evidence', actionAuthority: 'NONE',
  source: { product: 'PixInsight', productVersion: '1.9.4 build 1695', hostId: 'WIN-QOOF3903TQS', workspaceId: 'PIXINSIGHT-OAT-20260909-231843', captureMethod: 'GOVERNED_PJSR_EXPORT' },
  observationContext: { sessionId: 'OAT-BKL045-F3B-20260909-231843', target: 'BKL-045-F3B-OAT', projectId: null, campaignId: null },
  workflow: { workflowId: 'WF-BKL045-F3B-20260909-231843', runId: 'RUN-BKL045-F3B-20260909-231843', startedAt: null, completedAt: null, steps: [], inputs: [], outputs: [] },
  capture: { completeness: 'UNAVAILABLE', limitations: ['NO_OBSERVED_PROCESSING_STEP_IS_EMITTED_BY_THIS_PROBE'], observedStepCount: 0, declaredStepCount: 0 }
};

test('maps real F3-B bounded evidence fail-closed', () => {
  const manifest = provenanceSidecarToManifest(sidecar);
  assert.equal(manifest.manifestId, 'PXM-20260909T213316284Z-OAT');
  assert.equal(manifest.observationContext.projectId, 'unknown');
  assert.deepEqual(manifest.processingRun.processes, []);
  assert.equal(manifest.processingRun.parameters.captureCompleteness, 'UNAVAILABLE');
  assert.equal(manifest.processingRun.parameters.observedStepCount, 0);
});

test('only OBSERVED steps enter manifest process evidence', () => {
  const manifest = provenanceSidecarToManifest({ ...sidecar, workflow: { ...sidecar.workflow, steps: [
    { processId: 'ObservedProcess', evidenceClass: 'OBSERVED' },
    { processId: 'DeclaredProcess', evidenceClass: 'DECLARED' }
  ] } });
  assert.deepEqual(manifest.processingRun.processes, ['ObservedProcess']);
  assert.equal(manifest.processingRun.parameters.declaredStepCount, 1);
});

test('rejects action authority', () => {
  assert.throws(() => provenanceSidecarToManifest({ ...sidecar, actionAuthority: 'APPLY' }), /action authority/);
});
