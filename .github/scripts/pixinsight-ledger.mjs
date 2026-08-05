import { digestManifest, idempotencyKey, validateManifest } from './pixinsight-manifest.mjs';

const freezeRecord = (record) => Object.freeze({ ...record });

export class PixInsightSynchronizationLedger {
  #records = [];
  #auditTrail = [];
  #byManifestId = new Map();
  #byIdempotencyKey = new Map();

  #audit(event) {
    const entry = freezeRecord({ auditSequence: this.#auditTrail.length + 1, ...event });
    this.#auditTrail.push(entry);
    return entry;
  }

  append(manifest, { receivedAt = new Date().toISOString(), adapterVersion = '1.0.0' } = {}) {
    const validation = validateManifest(manifest);
    if (!validation.valid) {
      const rejected = freezeRecord({
        outcome: 'rejected',
        manifestId: manifest?.manifestId ?? null,
        receivedAt,
        adapterVersion,
        errors: Object.freeze([...validation.errors])
      });
      this.#audit({ eventType: 'manifest-rejected', occurredAt: receivedAt, manifestId: rejected.manifestId, outcome: rejected.outcome });
      return rejected;
    }

    const payloadDigest = digestManifest(manifest);
    const key = idempotencyKey(manifest);
    const sameKey = this.#byIdempotencyKey.get(key);
    if (sameKey) {
      const duplicate = freezeRecord({
        outcome: 'duplicate-noop',
        manifestId: manifest.manifestId,
        idempotencyKey: key,
        payloadDigest,
        receivedAt,
        previousSequence: sameKey.sequence
      });
      this.#audit({ eventType: 'manifest-duplicate', occurredAt: receivedAt, manifestId: duplicate.manifestId, outcome: duplicate.outcome, previousSequence: duplicate.previousSequence });
      return duplicate;
    }

    const sameManifest = this.#byManifestId.get(manifest.manifestId);
    if (sameManifest && sameManifest.payloadDigest !== payloadDigest) {
      const conflict = freezeRecord({
        sequence: this.#records.length + 1,
        outcome: 'conflict',
        manifestId: manifest.manifestId,
        idempotencyKey: key,
        payloadDigest,
        receivedAt,
        adapterVersion,
        previousSequence: sameManifest.sequence,
        previousPayloadDigest: sameManifest.payloadDigest
      });
      this.#records.push(conflict);
      this.#audit({ eventType: 'manifest-conflict', occurredAt: receivedAt, manifestId: conflict.manifestId, outcome: conflict.outcome, recordSequence: conflict.sequence, previousSequence: conflict.previousSequence });
      return conflict;
    }

    const accepted = freezeRecord({
      sequence: this.#records.length + 1,
      outcome: 'accepted',
      manifestId: manifest.manifestId,
      idempotencyKey: key,
      payloadDigest,
      receivedAt,
      adapterVersion
    });
    this.#records.push(accepted);
    this.#byManifestId.set(manifest.manifestId, accepted);
    this.#byIdempotencyKey.set(key, accepted);
    this.#audit({ eventType: 'manifest-accepted', occurredAt: receivedAt, manifestId: accepted.manifestId, outcome: accepted.outcome, recordSequence: accepted.sequence });
    return accepted;
  }

  resolveConflict(conflictSequence, {
    decision,
    reason,
    operatorId,
    resolvedAt = new Date().toISOString()
  } = {}) {
    const conflict = this.#records.find((record) => record.sequence === conflictSequence && record.outcome === 'conflict');
    if (!conflict) throw new Error('Conflict record not found.');
    if (!['retain-authoritative', 'reject-candidate'].includes(decision)) throw new Error('Unsupported conflict resolution decision.');
    if (typeof reason !== 'string' || reason.trim().length === 0) throw new Error('Conflict resolution reason is required.');
    if (typeof operatorId !== 'string' || operatorId.trim().length === 0) throw new Error('Conflict resolution operatorId is required.');
    if (this.#records.some((record) => record.outcome === 'conflict-resolved' && record.conflictSequence === conflictSequence)) {
      throw new Error('Conflict has already been resolved.');
    }

    const resolution = freezeRecord({
      sequence: this.#records.length + 1,
      outcome: 'conflict-resolved',
      conflictSequence,
      manifestId: conflict.manifestId,
      decision,
      reason: reason.trim(),
      operatorId: operatorId.trim(),
      resolvedAt,
      authoritativeSequence: conflict.previousSequence
    });
    this.#records.push(resolution);
    this.#audit({
      eventType: 'conflict-resolved',
      occurredAt: resolvedAt,
      manifestId: conflict.manifestId,
      outcome: resolution.outcome,
      recordSequence: resolution.sequence,
      conflictSequence,
      decision,
      operatorId: resolution.operatorId
    });
    return resolution;
  }

  get records() {
    return Object.freeze([...this.#records]);
  }

  get auditTrail() {
    return Object.freeze([...this.#auditTrail]);
  }

  findByManifestId(manifestId) {
    return this.#byManifestId.get(manifestId) ?? null;
  }

  findByIdempotencyKey(key) {
    return this.#byIdempotencyKey.get(key) ?? null;
  }
}
