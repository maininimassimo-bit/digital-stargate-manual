const freeze = (value) => Object.freeze(value);

const clone = (value) => structuredClone(value);

export function buildPixInsightProvenanceReadModel({ sidecar, processingProjection = null } = {}) {
  if (!sidecar || sidecar.schemaVersion !== '1.0') throw new Error('A supported PixInsight provenance sidecar is required.');
  if (sidecar.authority !== 'processing_evidence') throw new Error('Unsupported provenance authority.');
  if (sidecar.actionAuthority !== 'NONE') throw new Error('Consumer cannot expose action authority.');

  const steps = Array.isArray(sidecar.workflow?.steps) ? sidecar.workflow.steps : [];
  const observed = steps.filter((step) => step?.evidenceClass === 'OBSERVED');
  const declared = steps.filter((step) => step?.evidenceClass === 'DECLARED');
  const limitations = Array.isArray(sidecar.capture?.limitations) ? [...sidecar.capture.limitations] : [];

  if (processingProjection) {
    const projectedSidecarId = processingProjection.processing?.parameters?.provenanceSidecarId;
    if (projectedSidecarId && projectedSidecarId !== sidecar.sidecarId) {
      throw new Error('Processing projection does not reference the supplied provenance sidecar.');
    }
    if (processingProjection.authority?.acceptanceAuthority !== false) {
      throw new Error('Processing projection must not carry acceptance authority.');
    }
  }

  const captureCompleteness = sidecar.capture?.completeness ?? 'UNAVAILABLE';
  const state = captureCompleteness === 'COMPLETE'
    ? 'AVAILABLE'
    : captureCompleteness === 'PARTIAL'
      ? 'PARTIAL'
      : 'UNAVAILABLE';

  return freeze({
    schemaVersion: '1.0',
    readModelType: 'PIXINSIGHT_PROVENANCE_READ_MODEL',
    consumerMode: 'READ_ONLY',
    provenanceState: state,
    sidecarId: sidecar.sidecarId,
    exportedAt: sidecar.exportedAt,
    source: freeze({
      product: sidecar.source?.product ?? 'PixInsight',
      productVersion: sidecar.source?.productVersion ?? 'unknown',
      workspaceId: sidecar.source?.workspaceId ?? 'unknown',
      captureMethod: sidecar.source?.captureMethod ?? 'unknown'
    }),
    observationContext: freeze({
      sessionId: sidecar.observationContext?.sessionId ?? null,
      target: sidecar.observationContext?.target ?? null,
      projectId: sidecar.observationContext?.projectId ?? null,
      campaignId: sidecar.observationContext?.campaignId ?? null
    }),
    workflow: freeze({
      workflowId: sidecar.workflow?.workflowId ?? null,
      runId: sidecar.workflow?.runId ?? null,
      startedAt: sidecar.workflow?.startedAt ?? null,
      completedAt: sidecar.workflow?.completedAt ?? null,
      environment: freeze(clone(sidecar.workflow?.environment ?? {})),
      steps: freeze(steps.map((step) => freeze(clone(step)))),
      observedStepCount: observed.length,
      declaredStepCount: declared.length
    }),
    capture: freeze({
      completeness: captureCompleteness,
      limitations: freeze(limitations)
    }),
    reconciliation: processingProjection ? freeze({
      projectionId: processingProjection.projectionId ?? null,
      state: processingProjection.reconciliationState ?? null,
      catalogItemId: processingProjection.catalogItemId ?? null
    }) : null,
    authority: freeze({
      sourceEvidence: 'BKL-045-PROCESSING-EVIDENCE',
      catalogProjection: processingProjection ? 'AP-014-DERIVED' : null,
      assetsAndProvenance: 'AP-013',
      acceptanceAuthority: false,
      actionAuthority: 'NONE'
    })
  });
}
