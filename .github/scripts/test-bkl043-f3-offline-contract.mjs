import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const schema = JSON.parse(await readFile(
  new URL('../../contracts/telemetry/bkl-043-reliability-observation-v1.schema.json', import.meta.url),
  'utf8',
));

const digest = 'a'.repeat(64);
const base = {
  schema_version: '1.0',
  record_id: 'synthetic-record-001',
  record_type: 'SOURCE_OBSERVATION',
  component_id: 'synthetic-component',
  source_id: 'synthetic-source',
  source_observed_at_utc: '2026-09-24T10:00:00Z',
  received_at_utc: '2026-09-24T10:00:01Z',
  clock_quality: 'SYNCHRONIZED',
  source_quality: 'CURRENT',
  coverage_state: 'COVERED',
  source_sequence: 1,
  host_boot_id: 'synthetic-boot-1',
  process_run_id: 'synthetic-run-1',
  reason_code: null,
  payload_digest: digest,
  command_authority: 'NONE',
  execution_authority: 'NONE',
  safety_authority: 'NONE',
};

function validateEnvelope(record) {
  const errors = [];
  const properties = schema.properties;

  for (const key of schema.required) {
    if (!Object.hasOwn(record, key)) errors.push(`missing:${key}`);
  }
  for (const key of Object.keys(record)) {
    if (!Object.hasOwn(properties, key)) errors.push(`extra:${key}`);
  }
  for (const [key, rule] of Object.entries(properties)) {
    if (!Object.hasOwn(record, key)) continue;
    const value = record[key];
    if (rule.const !== undefined && value !== rule.const) errors.push(`const:${key}`);
    if (rule.enum && !rule.enum.includes(value)) errors.push(`enum:${key}`);
    if (rule.type === 'string' && typeof value !== 'string') errors.push(`type:${key}`);
    if (rule.type === 'integer' && !Number.isInteger(value)) errors.push(`type:${key}`);
    if (Array.isArray(rule.type)) {
      const acceptable = rule.type.includes('null') && value === null
        || rule.type.includes('string') && typeof value === 'string'
        || rule.type.includes('integer') && Number.isInteger(value);
      if (!acceptable) errors.push(`type:${key}`);
    }
    if (typeof value === 'string' && rule.minLength && value.length < rule.minLength) errors.push(`minLength:${key}`);
    if (typeof value === 'string' && rule.maxLength && value.length > rule.maxLength) errors.push(`maxLength:${key}`);
    if (typeof value === 'string' && rule.pattern && !new RegExp(rule.pattern).test(value)) errors.push(`pattern:${key}`);
    if (typeof value === 'number' && rule.minimum !== undefined && value < rule.minimum) errors.push(`minimum:${key}`);
    if (typeof value === 'string' && rule.format === 'date-time'
      && (!/^\d{4}-\d\d-\d\dT.*Z$/.test(value) || !Number.isFinite(Date.parse(value)))) errors.push(`format:${key}`);
  }

  if (record.record_type === 'SOURCE_OBSERVATION' && typeof record.source_observed_at_utc !== 'string') {
    errors.push('source-observation-requires-source-time');
  }
  if (record.record_type === 'WITNESS_RECEIPT' && typeof record.received_at_utc !== 'string') {
    errors.push('witness-receipt-requires-receive-time');
  }
  if (record.coverage_state === 'COVERED' && record.source_quality !== 'CURRENT') {
    errors.push('non-current-cannot-be-covered');
  }
  if (record.source_quality === 'CONFLICTING' && record.coverage_state !== 'UNKNOWN_GAP') {
    errors.push('conflict-requires-unknown-gap');
  }

  return errors;
}

function coverageEligible(record) {
  return validateEnvelope(record).length === 0
    && record.coverage_state === 'COVERED'
    && record.source_quality === 'CURRENT'
    && record.clock_quality === 'SYNCHRONIZED'
    && typeof record.source_observed_at_utc === 'string'
    && typeof record.received_at_utc === 'string'
    && Date.parse(record.received_at_utc) >= Date.parse(record.source_observed_at_utc);
}

function reconcileById(records) {
  const seen = new Map();
  const duplicates = [];
  const conflicts = new Map();
  for (const record of records) {
    const previous = seen.get(record.record_id);
    if (!previous) {
      seen.set(record.record_id, record);
    } else if (previous.payload_digest === record.payload_digest) {
      duplicates.push(record.record_id);
    } else {
      const lineage = conflicts.get(record.record_id) ?? [previous];
      lineage.push(record);
      conflicts.set(record.record_id, lineage);
    }
  }
  return { duplicates, conflicts: [...conflicts.values()] };
}

test('synthetic current observation qualifies only with ordered synchronized evidence', () => {
  assert.deepEqual(validateEnvelope(base), []);
  assert.equal(coverageEligible(base), true);
});

test('stale, unknown, unavailable, excluded, and unsynchronized data never qualify as covered exposure', () => {
  for (const source_quality of ['STALE', 'UNKNOWN', 'UNAVAILABLE']) {
    const record = { ...base, source_quality, coverage_state: 'UNKNOWN_GAP' };
    assert.deepEqual(validateEnvelope(record), []);
    assert.equal(coverageEligible(record), false);
  }
  assert.equal(coverageEligible({ ...base, coverage_state: 'EXCLUDED' }), false);
  assert.equal(coverageEligible({ ...base, clock_quality: 'UNKNOWN' }), false);
  assert.equal(coverageEligible({ ...base, clock_quality: 'UNSYNCHRONIZED' }), false);
});

test('absent source time and backwards receipt time remain unknown, not healthy', () => {
  const absent = { ...base, source_quality: 'UNKNOWN', coverage_state: 'UNKNOWN_GAP', source_observed_at_utc: null };
  assert.ok(validateEnvelope(absent).includes('source-observation-requires-source-time'));
  assert.equal(coverageEligible(absent), false);

  const backwards = { ...base, received_at_utc: '2026-09-24T09:59:59Z' };
  assert.deepEqual(validateEnvelope(backwards), []);
  assert.equal(coverageEligible(backwards), false);
});

test('conflicting source values require an explicit unknown gap', () => {
  const conflict = { ...base, source_quality: 'CONFLICTING', coverage_state: 'UNKNOWN_GAP', reason_code: 'SOURCE_CONFLICT' };
  assert.deepEqual(validateEnvelope(conflict), []);
  assert.equal(coverageEligible(conflict), false);
  assert.ok(validateEnvelope({ ...conflict, coverage_state: 'COVERED' }).includes('non-current-cannot-be-covered'));
});

test('identical replay is deduplicated; identity reuse with changed digest remains a conflict', () => {
  const changed = { ...base, payload_digest: 'b'.repeat(64) };
  assert.deepEqual(reconcileById([base, { ...base }]), { duplicates: [base.record_id], conflicts: [] });
  assert.deepEqual(reconcileById([base, changed]), { duplicates: [], conflicts: [[base, changed]] });
});

test('reordered source sequence preserves original timestamps and does not create inferred exposure', () => {
  const later = { ...base, record_id: 'synthetic-record-002', source_sequence: 2, source_observed_at_utc: '2026-09-24T10:00:02Z', received_at_utc: '2026-09-24T10:00:03Z' };
  const earlier = { ...base, source_sequence: 1 };
  const arrivalOrder = [later, earlier];
  assert.equal(coverageEligible(arrivalOrder[0]), true);
  assert.equal(arrivalOrder[0].source_observed_at_utc, '2026-09-24T10:00:02Z');
  assert.equal(arrivalOrder[1].source_observed_at_utc, '2026-09-24T10:00:00Z');
});

test('witness receipts require receiver time and never replace source observation time', () => {
  const receipt = { ...base, record_type: 'WITNESS_RECEIPT' };
  assert.deepEqual(validateEnvelope(receipt), []);
  assert.equal(coverageEligible(receipt), true);
  assert.ok(validateEnvelope({ ...receipt, received_at_utc: null }).includes('witness-receipt-requires-receive-time'));
  assert.equal(receipt.source_observed_at_utc, base.source_observed_at_utc);
});

test('clock jumps, missing timestamps, and malformed timestamps fail closed', () => {
  assert.equal(coverageEligible({ ...base, source_observed_at_utc: 'bad-time' }), false);
  assert.ok(validateEnvelope({ ...base, source_observed_at_utc: '2026-99-99T10:00:00Z' }).includes('format:source_observed_at_utc'));
  assert.equal(coverageEligible({ ...base, received_at_utc: null }), false);
  assert.equal(coverageEligible({ ...base, received_at_utc: '2026-09-24T09:00:00Z' }), false);
});

test('raw bodies, credentials, control fields, and authority escalation are rejected', () => {
  for (const forbidden of [
    { ...base, raw_payload: 'synthetic-only' },
    { ...base, api_key: 'synthetic-only' },
    { ...base, command: 'synthetic-only' },
    { ...base, safety_authority: 'ENABLED' },
  ]) {
    assert.notDeepEqual(validateEnvelope(forbidden), []);
    assert.equal(coverageEligible(forbidden), false);
  }
});

test('schema requires a closed object and permanently NONE authority', () => {
  assert.equal(schema.additionalProperties, false);
  assert.equal(schema.properties.command_authority.const, 'NONE');
  assert.equal(schema.properties.execution_authority.const, 'NONE');
  assert.equal(schema.properties.safety_authority.const, 'NONE');
});
