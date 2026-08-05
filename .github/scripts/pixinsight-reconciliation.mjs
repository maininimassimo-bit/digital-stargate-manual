const freeze = (value) => Object.freeze(value);

const normalizeRef = (value) => typeof value === 'string' ? value.trim() : '';

export class PixInsightReconciliationService {
  constructor({ catalogItems = [], assets = [] } = {}) {
    this.catalogItems = freeze([...catalogItems]);
    this.assets = freeze([...assets]);
    this.catalogByEntityId = new Map(this.catalogItems.map((item) => [item.entityId, item]));
    this.assetsById = new Map(this.assets.map((asset) => [asset.assetId, asset]));
  }

  reconcile(manifest, { reconciledAt = new Date().toISOString() } = {}) {
    const sessionId = normalizeRef(manifest?.observationContext?.sessionId);
    const inputRefs = Array.isArray(manifest?.processingRun?.inputs)
      ? manifest.processingRun.inputs.map(normalizeRef).filter(Boolean)
      : [];
    const outputRefs = Array.isArray(manifest?.processingRun?.outputs)
      ? manifest.processingRun.outputs.map(normalizeRef).filter(Boolean)
      : [];

    const catalogItem = this.catalogByEntityId.get(sessionId) ?? null;
    const inputMatches = inputRefs.map((reference) => ({
      reference,
      asset: this.assetsById.get(reference) ?? null
    }));
    const outputMatches = outputRefs.map((reference) => ({
      reference,
      asset: this.assetsById.get(reference) ?? null
    }));

    const missingInputs = inputMatches.filter((match) => match.asset === null).map((match) => match.reference);
    const missingOutputs = outputMatches.filter((match) => match.asset === null).map((match) => match.reference);
    const authoritativeConflicts = [...inputMatches, ...outputMatches]
      .filter((match) => match.asset?.integrityState === 'CONFLICT')
      .map((match) => match.reference);

    let state = 'matched';
    if (!catalogItem && inputRefs.length === 0 && outputRefs.length === 0) state = 'unresolved';
    else if (authoritativeConflicts.length > 0) state = 'conflict';
    else if (!catalogItem || missingInputs.length > 0 || missingOutputs.length > 0) state = 'partially-matched';

    return freeze({
      state,
      reconciledAt,
      session: freeze({
        requestedId: sessionId || null,
        matched: catalogItem !== null,
        catalogItemId: catalogItem?.catalogItemId ?? null,
        qualityState: catalogItem?.qualityState ?? null
      }),
      inputs: freeze({
        requested: inputRefs.length,
        matched: inputRefs.length - missingInputs.length,
        missing: freeze([...missingInputs])
      }),
      outputs: freeze({
        requested: outputRefs.length,
        matched: outputRefs.length - missingOutputs.length,
        missing: freeze([...missingOutputs])
      }),
      authoritativeConflicts: freeze([...authoritativeConflicts]),
      authority: freeze({
        catalog: 'AP-014',
        assetsAndProvenance: 'AP-013',
        mode: 'read-only'
      })
    });
  }
}
