import test from 'node:test';
import assert from 'node:assert/strict';
import { canonicalIdentitySerialization, deriveRecordId, ID_METHOD, ID_METHOD_VERSION } from './anomaly-trend-id.mjs';

const record = {
  semantic_type: 'TREND_MEASUREMENT',
  method_id: 'BKL038-F2-EXACT-EVENT-DELTA-1',
  method_version: '1.0',
  source_record_refs: [
    'replay-event:RPL-20260815-CLOUDWATCHER-FIRST',
    'replay-event:RPL-20260815-NINA-DOME-OPEN'
  ],
  analysis_window: {
    start_utc: '2026-08-15T17:00:09Z',
    end_utc: '2026-08-15T18:42:52.8776Z'
  }
};

const expected = 'AT-SHA256-5cd67d6b57a15e9359077c9ab179bbb039ad29c2ee584a280aa80682163fa238';

test('method identity is versioned', () => {
  assert.equal(ID_METHOD, 'BKL038-F3-DERIVED-ID-SHA256-1');
  assert.equal(ID_METHOD_VERSION, '1.0');
});

test('canonical serialization is explicit and stable', () => {
  assert.equal(canonicalIdentitySerialization(record), '{"semantic_type":"TREND_MEASUREMENT","method_id":"BKL038-F2-EXACT-EVENT-DELTA-1","method_version":"1.0","source_record_refs":["replay-event:RPL-20260815-CLOUDWATCHER-FIRST","replay-event:RPL-20260815-NINA-DOME-OPEN"],"analysis_window":{"start_utc":"2026-08-15T17:00:09Z","end_utc":"2026-08-15T18:42:52.8776Z"}}');
});

test('same identity tuple is idempotent', () => {
  assert.equal(deriveRecordId(record), expected);
  assert.equal(deriveRecordId(structuredClone(record)), expected);
});

test('non-identity fields cannot perturb derived id', () => {
  assert.equal(deriveRecordId({...record, measurement:{value:6163877.6, unit:'ms'}, quality:'CURRENT_AT_OBSERVATION'}), expected);
});

test('ordered source references are identity-significant', () => {
  const changed = structuredClone(record); changed.source_record_refs.reverse();
  assert.notEqual(deriveRecordId(changed), expected);
});

test('semantic type, method version and window are identity-significant', () => {
  for (const mutate of [
    r => { r.semantic_type='CORRELATION_CANDIDATE'; },
    r => { r.method_version='1.1'; },
    r => { r.analysis_window.end_utc='2026-08-15T18:42:52.8777Z'; }
  ]) {
    const changed=structuredClone(record); mutate(changed); assert.notEqual(deriveRecordId(changed), expected);
  }
});

test('missing identity fields fail closed', () => {
  for (const changed of [
    {...record, semantic_type:''},
    {...record, source_record_refs:[]},
    {...record, analysis_window:null}
  ]) assert.throws(() => deriveRecordId(changed), /BKL-038 F3 ID FAILED/);
});
