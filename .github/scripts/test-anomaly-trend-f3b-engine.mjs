import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { projectAnomalyTrend } from './anomaly-trend-engine.mjs';

const replay = JSON.parse(await readFile(new URL('../../docs/data/night-timeline-replay-f3.json', import.meta.url), 'utf8'));
const clone = value => structuredClone(value);

test('accepted replay produces bounded deterministic read-only projection', () => {
  const a = projectAnomalyTrend(replay);
  const b = projectAnomalyTrend(replay);
  assert.deepEqual(a, b);
  assert.equal(a.authority, 'projection');
  assert.equal(a.action_authority, 'NONE');
  assert.equal(a.records.length, 5);
  assert.deepEqual(a.records.map(r => r.derived_record_id), [
    'AT-SHA256-121a9a7dbe3da345927c4e6771adc32ce2a0922b2fbeb05ffbffbb49873a784a',
    'AT-SHA256-53faeb7bf2f490d7aa19807326f008ffa9c7de0d02bb04e8f583f21671840d0a',
    'AT-SHA256-49ba5ed38f94628e0e6bcd3cdc065e3a0075655881fde4934e75e480e3d1c752',
    'AT-SHA256-6963401289521af98fc2605dcc00628c38b7d25b7a0ac477dc509c9850b3a60f',
    'AT-SHA256-bf2e27ec398f08dc3d78c273580feb910cc79a4b8907f34ce5eaefaf1bad2526'
  ]);
  for (const r of a.records) {
    assert.equal(r.authority, 'projection');
    assert.equal(r.action_authority, 'NONE');
    assert.ok(r.citation_refs.length > 0);
    assert.ok(r.provenance_refs.length > 0);
  }
  const trends = a.records.filter(r => r.semantic_type === 'TREND_MEASUREMENT');
  assert.deepEqual(trends.map(r => r.measurement.value), [6163877.6, 5300122.4]);
  assert.ok(trends.every(r => r.measurement.descriptive_only === true && r.candidate_state === null && r.rule_id === null));
});

test('non-projection input authority fails closed', () => {
  const x = clone(replay); x.authority = 'command';
  assert.throws(() => projectAnomalyTrend(x), /input authority must be projection/);
});

test('unplaced event fails closed instead of inventing temporal placement', () => {
  const x = clone(replay); x.events[0].temporal_state = 'UNPLACED';
  assert.throws(() => projectAnomalyTrend(x), /is not PLACED/);
});

test('source-declared stale quality remains stale at observation', () => {
  const x = clone(replay); x.events[0].quality_state = 'STALE';
  const projection = projectAnomalyTrend(x);
  assert.equal(projection.records[0].quality_state, 'STALE_AT_OBSERVATION');
  const dependentTrend = projection.records.find(r => r.semantic_type === 'TREND_MEASUREMENT' && r.source_record_refs.includes(`replay-event:${x.events[0].replay_event_id}`));
  assert.equal(dependentTrend.quality_state, 'STALE_AT_OBSERVATION');
});

test('unsupported source quality fails closed instead of collapsing to unknown', () => {
  const x = clone(replay); x.events[0].quality_state = 'HEALTHY';
  assert.throws(() => projectAnomalyTrend(x), /unsupported quality_state/);
});

test('unsupported correlation method fails closed', () => {
  const x = clone(replay); x.correlations[0].classification_method_id = 'INVENTED-THRESHOLD';
  assert.throws(() => projectAnomalyTrend(x), /unsupported method/);
});

test('analytically classified upstream correlation fails closed', () => {
  const x = clone(replay); x.correlations[0].classification_state = 'ANOMALOUS';
  assert.throws(() => projectAnomalyTrend(x), /attempts analytical classification/);
});

test('unresolved source reference fails closed', () => {
  const x = clone(replay); x.correlations[0].left_event_ref = 'replay-event:DOES-NOT-EXIST';
  assert.throws(() => projectAnomalyTrend(x), /unresolved source refs/);
});

test('empty Citation or Provenance refs fail closed', () => {
  const citation = clone(replay); citation.events[0].citation_refs = [];
  assert.throws(() => projectAnomalyTrend(citation), /citation_refs must not be empty/);
  const provenance = clone(replay); provenance.correlations[0].provenance_refs = [];
  assert.throws(() => projectAnomalyTrend(provenance), /provenance_refs must not be empty/);
});

test('unresolved Citation or Provenance refs fail closed', () => {
  const citation = clone(replay); citation.events[0].citation_refs = ['DOES-NOT-EXIST@1.0'];
  assert.throws(() => projectAnomalyTrend(citation), /citation_refs contains unresolved reference/);
  const provenance = clone(replay); provenance.correlations[0].provenance_refs = ['DOES-NOT-EXIST@1.0'];
  assert.throws(() => projectAnomalyTrend(provenance), /provenance_refs contains unresolved reference/);
});

test('negative or non-numeric delta fails closed', () => {
  const negative = clone(replay); negative.correlations[0].delta_ms = -1;
  assert.throws(() => projectAnomalyTrend(negative), /invalid delta_ms/);
  const text = clone(replay); text.correlations[0].delta_ms = '6163877.6';
  assert.throws(() => projectAnomalyTrend(text), /invalid delta_ms/);
});
