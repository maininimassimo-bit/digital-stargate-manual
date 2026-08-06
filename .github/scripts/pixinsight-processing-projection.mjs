import { createHash } from 'node:crypto';

const freeze = (value) => Object.freeze(value);
const sha256 = (value) => createHash('sha256').update(value, 'utf8').digest('hex');

const stableStringify = (value) => {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`;
  if (value !== null && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
};

export class PixInsightProcessingProjectionBuilder {
  build({ manifest, ledgerRecord, reconciliation, projectedAt = new Date().toISOString(), correlationId = null } = {}) {
    if (!manifest || !ledgerRecord || !reconciliation) throw new Error('manifest, ledgerRecord and reconciliation are required.');
    if (ledgerRecord.outcome !== 'accepted') throw new Error('Only accepted ledger records can produce a processing projection.');

    const effectiveCorrelationId = correlationId || `PXC-${ledgerRecord.idempotencyKey.slice(0, 16).toUpperCase()}`;
    const projectionBody = {
      schemaVersion: '1.0',
      projectionType: 'PIXINSIGHT_PROCESSING',
      manifestId: manifest.manifestId,
      externalRunId: manifest.processingRun.externalRunId,
      sessionId: manifest.observationContext.sessionId,
      catalogItemId: reconciliation.session.catalogItemId,
      reconciliationState: reconciliation.state,
      source: {
        product: manifest.source.product,
        productVersion: manifest.source.productVersion,
        workspaceId: manifest.source.workspaceId
      },
      processing: {
        startedAt: manifest.processingRun.startedAt,
        completedAt: manifest.processingRun.completedAt,
        processes: freeze([...manifest.processingRun.processes]),
        inputReferences: freeze([...manifest.processingRun.inputs]),
        outputReferences: freeze([...manifest.processingRun.outputs]),
        parameters: freeze(structuredClone(manifest.processingRun.parameters))
      },
      authority: {
        projection: 'AP-014-DERIVED',
        assetsAndProvenance: 'AP-013',
        acceptanceAuthority: false
      },
      correlationId: effectiveCorrelationId,
      projectedAt
    };

    const projectionDigest = `sha256:${sha256(stableStringify(projectionBody))}`;
    const projectionId = `PXP-${projectionDigest.slice(7, 23).toUpperCase()}`;
    const projection = freeze({ projectionId, projectionDigest, ...projectionBody });

    const events = freeze([
      freeze({
        eventType: 'PixInsightProjectionCreated',
        schemaVersion: '1.0',
        occurredAt: projectedAt,
        correlationId: effectiveCorrelationId,
        manifestId: manifest.manifestId,
        projectionId,
        reconciliationState: reconciliation.state,
        acceptanceAuthority: false
      }),
      freeze({
        eventType: 'PixInsightProjectionAvailable',
        schemaVersion: '1.0',
        occurredAt: projectedAt,
        correlationId: effectiveCorrelationId,
        projectionId,
        catalogItemId: reconciliation.session.catalogItemId,
        acceptanceAuthority: false
      })
    ]);

    return freeze({ projection, events });
  }
}
