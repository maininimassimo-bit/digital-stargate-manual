const freeze = (value) => Object.freeze(value);

const textOrUnknown = (value) => typeof value === 'string' && value.trim() ? value.trim() : 'unknown';
const assetRefs = (items) => Array.isArray(items)
  ? items.map((item) => item?.assetId || item?.reference).filter((value) => typeof value === 'string' && value.trim()).map((value) => value.trim())
  : [];

export function provenanceSidecarToManifest(sidecar) {
  if (!sidecar || sidecar.schemaVersion !== '1.0') throw new Error('Unsupported provenance sidecar schemaVersion');
  if (sidecar.authority !== 'processing_evidence') throw new Error('Invalid provenance authority');
  if (sidecar.actionAuthority !== 'NONE') throw new Error('PixInsight provenance must not carry action authority');

  const observedSteps = Array.isArray(sidecar.workflow?.steps)
    ? sidecar.workflow.steps.filter((step) => step?.evidenceClass === 'OBSERVED')
    : [];
  const declaredSteps = Array.isArray(sidecar.workflow?.steps)
    ? sidecar.workflow.steps.filter((step) => step?.evidenceClass === 'DECLARED')
    : [];

  return freeze({
    schemaVersion: '1.0',
    manifestId: `PXM-${textOrUnknown(sidecar.sidecarId).replace(/^PXP-/, '')}`,
    exportedAt: sidecar.exportedAt,
    source: freeze({
      product: 'PixInsight',
      productVersion: textOrUnknown(sidecar.source?.productVersion),
      hostId: textOrUnknown(sidecar.source?.hostId),
      workspaceId: textOrUnknown(sidecar.source?.workspaceId)
    }),
    observationContext: freeze({
      sessionId: textOrUnknown(sidecar.observationContext?.sessionId),
      target: textOrUnknown(sidecar.observationContext?.target),
      projectId: textOrUnknown(sidecar.observationContext?.projectId),
      campaignId: textOrUnknown(sidecar.observationContext?.campaignId)
    }),
    processingRun: freeze({
      externalRunId: textOrUnknown(sidecar.workflow?.runId),
      startedAt: sidecar.workflow?.startedAt ?? null,
      completedAt: sidecar.workflow?.completedAt ?? null,
      processes: freeze(observedSteps.map((step) => step.processId)),
      inputs: freeze(assetRefs(sidecar.workflow?.inputs)),
      outputs: freeze(assetRefs(sidecar.workflow?.outputs)),
      parameters: freeze({
        provenanceSidecarId: sidecar.sidecarId,
        workflowId: textOrUnknown(sidecar.workflow?.workflowId),
        captureMethod: textOrUnknown(sidecar.source?.captureMethod),
        captureCompleteness: textOrUnknown(sidecar.capture?.completeness),
        observedStepCount: observedSteps.length,
        declaredStepCount: declaredSteps.length,
        limitations: freeze(Array.isArray(sidecar.capture?.limitations) ? [...sidecar.capture.limitations] : [])
      })
    })
  });
}
