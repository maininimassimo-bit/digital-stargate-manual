import { deriveRecordId } from './anomaly-trend-id.mjs';

export const ENGINE_METHOD_VERSION = '1.0';
export const OBSERVATION_METHOD = 'BKL038-F3B-SOURCE-OBSERVATION-1';
export const TREND_METHOD = 'BKL038-F3B-EXACT-DELTA-PROJECTION-1';

const fail = message => { throw new Error(`BKL-038 F3-B FAILED: ${message}`); };
const requiredArray = (value, field) => {
  if (!Array.isArray(value)) fail(`${field} must be an array`);
  return value;
};
const requiredNonEmptyArray = (value, field) => {
  const result = requiredArray(value, field);
  if (result.length === 0) fail(`${field} must not be empty`);
  return result;
};
const requiredString = (value, field) => {
  if (typeof value !== 'string' || value.length === 0) fail(`${field} is required`);
  return value;
};

function refs(event) {
  return [`replay-event:${requiredString(event.replay_event_id, 'event.replay_event_id')}`];
}

function qualityState(sourceQuality, field) {
  switch (sourceQuality) {
    case 'CURRENT': return 'CURRENT_AT_OBSERVATION';
    case 'STALE': return 'STALE_AT_OBSERVATION';
    case 'UNKNOWN': return 'UNKNOWN';
    default: fail(`${field} has unsupported quality_state ${String(sourceQuality)}`);
  }
}

function combinedQuality(leftQuality, rightQuality) {
  const left = qualityState(leftQuality, 'left event');
  const right = qualityState(rightQuality, 'right event');
  if (left === 'STALE_AT_OBSERVATION' || right === 'STALE_AT_OBSERVATION') return 'STALE_AT_OBSERVATION';
  if (left === 'UNKNOWN' || right === 'UNKNOWN') return 'UNKNOWN';
  return 'CURRENT_AT_OBSERVATION';
}

function buildEvidenceSets(replay) {
  const citations = requiredArray(replay.citations, 'citations');
  const provenance = requiredArray(replay.provenance_records, 'provenance_records');
  const citationSet = new Set(citations.map((item, index) => `${requiredString(item?.id, `citations[${index}].id`)}@${requiredString(item?.version, `citations[${index}].version`)}`));
  const provenanceSet = new Set(provenance.map((item, index) => `${requiredString(item?.id, `provenance_records[${index}].id`)}@${requiredString(item?.version, `provenance_records[${index}].version`)}`));
  return { citationSet, provenanceSet };
}

function resolvedRefs(value, field, acceptedRefs) {
  const refs = requiredNonEmptyArray(value, field).map((item, index) => requiredString(item, `${field}[${index}]`));
  for (const ref of refs) if (!acceptedRefs.has(ref)) fail(`${field} contains unresolved reference ${ref}`);
  return refs;
}

function observation(event, evidence) {
  if (event.temporal_state !== 'PLACED') fail(`event ${event.replay_event_id ?? '<unknown>'} is not PLACED`);
  const time = requiredString(event.event_time_utc, 'event.event_time_utc');
  const record = {
    semantic_type: 'OBSERVATION', method_id: OBSERVATION_METHOD, method_version: ENGINE_METHOD_VERSION,
    source_record_refs: refs(event), citation_refs: resolvedRefs(event.citation_refs, 'event.citation_refs', evidence.citationSet),
    provenance_refs: resolvedRefs(event.provenance_refs, 'event.provenance_refs', evidence.provenanceSet),
    analysis_window: { start_utc: time, end_utc: time }, measurement: null, candidate_state: null, rule_id: null,
    quality_state: qualityState(event.quality_state, `event ${event.replay_event_id}`),
    explanation_codes: ['SOURCE_OBSERVATION_PRESERVED'], authority: 'projection', action_authority: 'NONE'
  };
  return { derived_record_id: deriveRecordId(record), ...record };
}

function trend(correlation, byRef, evidence) {
  if (correlation.relationship_type !== 'SEQUENTIAL') fail(`correlation ${correlation.correlation_id ?? '<unknown>'} is not SEQUENTIAL`);
  if (correlation.classification_method_id !== 'BKL040-F3-EXACT-DELTA-1') fail(`correlation ${correlation.correlation_id} has unsupported method`);
  if (correlation.classification_state !== 'NOT_ASSESSED') fail(`correlation ${correlation.correlation_id} attempts analytical classification`);
  if (typeof correlation.delta_ms !== 'number' || !Number.isFinite(correlation.delta_ms) || correlation.delta_ms < 0) fail(`correlation ${correlation.correlation_id} has invalid delta_ms`);
  const left = byRef.get(requiredString(correlation.left_event_ref, 'correlation.left_event_ref'));
  const right = byRef.get(requiredString(correlation.right_event_ref, 'correlation.right_event_ref'));
  if (!left || !right) fail(`correlation ${correlation.correlation_id} has unresolved source refs`);
  const source_record_refs = [correlation.left_event_ref, correlation.right_event_ref];
  const record = {
    semantic_type: 'TREND_MEASUREMENT', method_id: TREND_METHOD, method_version: ENGINE_METHOD_VERSION,
    source_record_refs, citation_refs: resolvedRefs(correlation.citation_refs, 'correlation.citation_refs', evidence.citationSet),
    provenance_refs: resolvedRefs(correlation.provenance_refs, 'correlation.provenance_refs', evidence.provenanceSet),
    analysis_window: { start_utc: left.event_time_utc, end_utc: right.event_time_utc },
    measurement: { value: correlation.delta_ms, unit: 'ms', descriptive_only: true }, candidate_state: null, rule_id: null,
    quality_state: combinedQuality(left.quality_state, right.quality_state),
    explanation_codes: ['EXACT_TEMPORAL_DELTA', 'DESCRIPTIVE_ONLY_NO_ANOMALY_RULE', 'CAUSATION_NOT_INFERRED'],
    authority: 'projection', action_authority: 'NONE'
  };
  return { derived_record_id: deriveRecordId(record), ...record };
}

export function projectAnomalyTrend(replay) {
  if (!replay || typeof replay !== 'object' || Array.isArray(replay)) fail('replay must be an object');
  if (replay.authority !== 'projection') fail('input authority must be projection');
  const events = requiredArray(replay.events, 'events');
  const correlations = requiredArray(replay.correlations, 'correlations');
  const evidence = buildEvidenceSets(replay);
  const byRef = new Map(events.map(event => [`replay-event:${event.replay_event_id}`, event]));
  if (byRef.size !== events.length) fail('duplicate replay_event_id');
  const records = [...events.map(event => observation(event, evidence)), ...correlations.map(item => trend(item, byRef, evidence))];
  if (new Set(records.map(record => record.derived_record_id)).size !== records.length) fail('duplicate derived_record_id');
  return {
    schema_version: '1.0', component: 'DSG.AnomalyTrendCenter.F3B', authority: 'projection', action_authority: 'NONE',
    source_component: replay.component, source_baseline_commit: replay.baseline_commit, session_id: replay.session_id,
    method_version: ENGINE_METHOD_VERSION, records
  };
}
