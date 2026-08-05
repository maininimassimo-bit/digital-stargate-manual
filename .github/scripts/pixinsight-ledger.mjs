import { digestManifest, idempotencyKey, validateManifest } from './pixinsight-manifest.mjs';

const freezeRecord = (record) => Object.freeze({ ...record });

export class PixInsightSynchronizationLedger {
  #records = [];
  #byManifestId = new Map();
  #byIdempotencyKey = new Map();

  append(manifest, { receivedAt = new Date().toISOString(), adapterVersion = '1.0.0' } = {}) {
    const validation = validateManifest(manifest);
    if (!validation.valid) {
      return freezeRecord({
        outcome: 'rejected',
        manifestId: manifest?.manifestId ?? null,
        receivedAt,
        adapterVersion,
        errors: Object.freeze([...validation.errors])
      });
    }

    const payloadDigest = digestManifest(manifest);
    const key = idempotencyKey(manifest);
    const sameKey = this.#byIdempotencyKey.get(key);
    if (sameKey) {
      return freezeRecord({
        outcome: 'duplicate-noop',
        manifestId: manifest.manifestId,
        idempotencyKey: key,
        payloadDigest,
        receivedAt,
        previousSequence: sameKey.sequence
      });
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
    return accepted;
  }

  get records() {
    return Object.freeze([...this.#records]);
  }

  findByManifestId(manifestId) {
    return this.#byManifestId.get(manifestId) ?? null;
  }

  findByIdempotencyKey(key) {
    return this.#byIdempotencyKey.get(key) ?? null;
  }
}
