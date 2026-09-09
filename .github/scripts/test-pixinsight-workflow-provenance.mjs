import assert from 'node:assert/strict';
import test from 'node:test';
import { canonicalJson, digest, validatePixInsightWorkflowProvenance } from './pixinsight-workflow-provenance.mjs';

const sample = () => ({
  schemaVersion: '1.0', sidecarId: 'PXP-20260909T204500Z-001', exportedAt: '2026-09-09T20:45:00Z',
  authority: 'processing_evidence', actionAuthority: 'NONE',
  source: { product: 'PixInsight', productVersion: '1.9.3', hostId: 'WORKSTATION', workspaceId: 'M51-Processing', captureMethod: 'HYBRID', sourceLocators: ['project:M51'] },
  observationContext: { sessionId: 'SESSION-M51-001', target: 'M51', projectId: 'M51', campaignId: null },
  workflow: {
    workflowId: 'WF-M51-001', runId: 'RUN-M51-001', startedAt: null, completedAt: null,
    environment: { pixInsightVersion: '1.9.3', platform: 'Windows', modules: [] },
    steps: [
      { stepId: 'STEP-001', ordinal: 1, processId: 'DynamicCrop', displayName: 'DynamicCrop', processVersion: null, evidenceClass: 'OBSERVED', capturedAt: '2026-09-09T20:40:00Z', parameters: { example: true }, sourceLocators: ['history:1'], notes: null, declaredBy: null, declaredAt: null, inputRefs: ['input.xisf'], outputRefs: ['crop.xisf'], maskRefs: [] },
      { stepId: 'STEP-002', ordinal: 2, processId: 'ManualNote', displayName: 'Manual adjustment', processVersion: null, evidenceClass: 'DECLARED', capturedAt: null, parameters: {}, sourceLocators: [], notes: 'User-declared operation not observable in source history', declaredBy: 'operator', declaredAt: '2026-09-09T20:44:00Z', inputRefs: [], outputRefs: [], maskRefs: [] }
    ],
    inputs: [{ reference: 'input.xisf', resolutionState: 'UNRESOLVED', assetId: null }],
    outputs: [{ reference: 'crop.xisf', resolutionState: 'UNRESOLVED', assetId: null }]
  },
  capture: { completeness: 'PARTIAL', limitations: ['Manual operation declared by operator'], observedStepCount: 1, declaredStepCount: 1 }
});

test('accepts mixed OBSERVED and DECLARED provenance', () => assert.equal(validatePixInsightWorkflowProvenance(sample()).valid, true));
test('canonical digest is deterministic', () => { const a=sample(); const b=JSON.parse(JSON.stringify(a)); b.workflow = { outputs:b.workflow.outputs, inputs:b.workflow.inputs, steps:b.workflow.steps, environment:b.workflow.environment, completedAt:b.workflow.completedAt, startedAt:b.workflow.startedAt, runId:b.workflow.runId, workflowId:b.workflow.workflowId }; assert.equal(digest(a), digest(b)); assert.equal(canonicalJson(a), canonicalJson(b)); });
test('rejects observed provenance without evidence locator', () => { const x=sample(); x.workflow.steps[0].sourceLocators=[]; assert.throws(() => validatePixInsightWorkflowProvenance(x), /requires source evidence/); });
test('rejects declared provenance without declaration identity', () => { const x=sample(); x.workflow.steps[1].declaredBy=null; assert.throws(() => validatePixInsightWorkflowProvenance(x), /requires declaration provenance/); });
test('rejects suggested provenance as executed step', () => { const x=sample(); x.workflow.steps[0].evidenceClass='SUGGESTED'; assert.throws(() => validatePixInsightWorkflowProvenance(x), /unsupported evidenceClass/); });
test('requires explicit limitations for partial capture', () => { const x=sample(); x.capture.limitations=[]; assert.throws(() => validatePixInsightWorkflowProvenance(x), /requires explicit limitations/); });
test('rejects non-contiguous workflow order', () => { const x=sample(); x.workflow.steps[1].ordinal=3; assert.throws(() => validatePixInsightWorkflowProvenance(x), /ordinals must be contiguous/); });
test('enforces no action authority', () => { const x=sample(); x.actionAuthority='APPLY'; assert.throws(() => validatePixInsightWorkflowProvenance(x), /actionAuthority must be NONE/); });
