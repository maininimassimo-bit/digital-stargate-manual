import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { buildPixInsightProvenanceReadModel } from './pixinsight-provenance-read-model.mjs';

const realEvidencePath = 'docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260909T212858612Z-OAT.json';
const realEvidence = JSON.parse(fs.readFileSync(realEvidencePath, 'utf8'));

test('real F3-B evidence remains UNAVAILABLE and read-only', () => {
  const model = buildPixInsightProvenanceReadModel({ sidecar: realEvidence });
  assert.equal(model.consumerMode, 'READ_ONLY');
  assert.equal(model.provenanceState, 'UNAVAILABLE');
  assert.equal(model.capture.completeness, 'UNAVAILABLE');
  assert.equal(model.workflow.observedStepCount, 0);
  assert.equal(model.workflow.declaredStepCount, 0);
  assert.equal(model.authority.acceptanceAuthority, false);
  assert.equal(model.authority.actionAuthority, 'NONE');
  assert.deepEqual(model.capture.limitations, realEvidence.capture.limitations);
});

test('declared steps remain declared in the read model', () => {
  const sidecar = structuredClone(realEvidence);
  sidecar.capture.completeness = 'PARTIAL';
  sidecar.workflow.steps = [{
    stepId: 'DECLARED-1', ordinal: 1, processId: 'ManualOperation', displayName: 'Manual operation',
    processVersion: null, evidenceClass: 'DECLARED', capturedAt: null, parameters: {}, sourceLocators: [],
    notes: 'operator declared', declaredBy: 'operator', declaredAt: sidecar.exportedAt,
    inputRefs: [], outputRefs: [], maskRefs: []
  }];
  sidecar.capture.declaredStepCount = 1;
  const model = buildPixInsightProvenanceReadModel({ sidecar });
  assert.equal(model.provenanceState, 'PARTIAL');
  assert.equal(model.workflow.declaredStepCount, 1);
  assert.equal(model.workflow.observedStepCount, 0);
  assert.equal(model.workflow.steps[0].evidenceClass, 'DECLARED');
});

test('rejects any action authority escalation', () => {
  const sidecar = structuredClone(realEvidence);
  sidecar.actionAuthority = 'APPLY';
  assert.throws(() => buildPixInsightProvenanceReadModel({ sidecar }), /action authority/i);
});

test('rejects mismatched processing projection linkage', () => {
  const projection = {
    projectionId: 'PXP-PROJECTION',
    reconciliationState: 'matched',
    catalogItemId: 'CAT-1',
    processing: { parameters: { provenanceSidecarId: 'PXP-OTHER' } },
    authority: { acceptanceAuthority: false }
  };
  assert.throws(() => buildPixInsightProvenanceReadModel({ sidecar: realEvidence, processingProjection: projection }), /does not reference/i);
});

test('rejects processing projection with acceptance authority', () => {
  const projection = {
    projectionId: 'PXP-PROJECTION',
    reconciliationState: 'matched',
    catalogItemId: 'CAT-1',
    processing: { parameters: { provenanceSidecarId: realEvidence.sidecarId } },
    authority: { acceptanceAuthority: true }
  };
  assert.throws(() => buildPixInsightProvenanceReadModel({ sidecar: realEvidence, processingProjection: projection }), /acceptance authority/i);
});
