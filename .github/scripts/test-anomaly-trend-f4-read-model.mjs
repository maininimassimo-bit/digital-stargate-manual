import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { buildAnomalyTrendReadModel, F3B_ACCEPTED_MERGE } from './generate-anomaly-trend-read-model.mjs';

const replay = JSON.parse(await readFile(new URL('../../docs/data/night-timeline-replay-f3.json', import.meta.url), 'utf8'));
const clone = value => structuredClone(value);

test('F4 consumer is deterministic, read-only and descriptive', () => {
  const a = buildAnomalyTrendReadModel(replay);
  const b = buildAnomalyTrendReadModel(replay);
  assert.deepEqual(a, b);
  assert.equal(a.baseline_commit, F3B_ACCEPTED_MERGE);
  assert.equal(a.authority, 'projection');
  assert.equal(a.action_authority, 'NONE');
  assert.equal(a.interaction_mode, 'READ_ONLY');
  assert.equal(a.advisory_mode, 'DESCRIPTIVE_ONLY');
  assert.equal(a.safety_authority, 'UNCHANGED_LOCAL_AUTHORITY');
  assert.deepEqual(a.command_actions, []);
  assert.deepEqual(a.summary, { total_records: 5, observations: 3, trend_measurements: 2, anomaly_candidates: 0, correlation_candidates: 0, recommendations: 0 });
  assert.ok(a.limitations.includes('NO_ANOMALY_THRESHOLD_AUTHORIZED'));
  assert.ok(a.limitations.includes('NO_COMMAND_OR_REMEDIATION_AUTHORITY'));
  for (const record of a.records) {
    assert.equal(record.authority, 'projection');
    assert.equal(record.action_authority, 'NONE');
    assert.ok(record.source_record_refs.length > 0);
    assert.ok(record.citation_refs.length > 0);
    assert.ok(record.provenance_refs.length > 0);
  }
});

test('source evidence mutations still fail closed through the F4 adapter', () => {
  const authority = clone(replay); authority.authority = 'command';
  assert.throws(() => buildAnomalyTrendReadModel(authority), /input authority must be projection/);
  const citation = clone(replay); citation.events[0].citation_refs = [];
  assert.throws(() => buildAnomalyTrendReadModel(citation), /citation_refs must not be empty/);
  const quality = clone(replay); quality.events[0].quality_state = 'HEALTHY';
  assert.throws(() => buildAnomalyTrendReadModel(quality), /unsupported quality_state/);
});

test('F4 never converts descriptive deltas into anomaly or causal claims', () => {
  const model = buildAnomalyTrendReadModel(replay);
  const trends = model.records.filter(record => record.semantic_type === 'TREND_MEASUREMENT');
  assert.deepEqual(trends.map(record => record.measurement.value), [6163877.6, 5300122.4]);
  assert.ok(trends.every(record => record.measurement.descriptive_only === true));
  assert.ok(trends.every(record => record.candidate_state === null && record.rule_id === null));
  assert.ok(trends.every(record => record.explanation_codes.includes('CAUSATION_NOT_INFERRED')));
});
