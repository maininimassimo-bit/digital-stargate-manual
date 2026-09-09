import fs from 'node:fs';

const path = 'docs/data/equipment-performance-registry-f5-collection.json';
const fail = (message) => { throw new Error(`BKL-039 F5 collection validation failed: ${message}`); };
const assert = (condition, message) => { if (!condition) fail(message); };
const unique = (values) => new Set(values).size === values.length;

const doc = JSON.parse(fs.readFileSync(path, 'utf8'));
assert(doc.schema_version === '1.0', 'schema_version must be 1.0');
assert(doc.component === 'DSG.EquipmentPerformanceRegistry.F5.CollectionReadModel', 'component mismatch');
assert(doc.authority === 'projection', 'authority escalation is forbidden');
assert(doc.action_authority === 'NONE', 'action authority is forbidden');
assert(doc.source_contract?.f3_projection === 'docs/data/equipment-performance-registry-f3-multisession.json', 'F3 source contract mismatch');
assert(Array.isArray(doc.views) && doc.views.length >= 2, 'multi-session collection requires at least two views');
assert(doc.population_count === doc.views.length, 'population_count must equal views length');
assert(unique(doc.views.map((v) => v.population_id)), 'duplicate population_id');

const allowedStats = new Set(['MEAN', 'MINIMUM', 'MAXIMUM', 'SAMPLE_STDDEV']);
for (const view of doc.views) {
  assert(view.configuration_id && view.session_id && view.target_name && view.filter_name, `synthetic or incomplete identity in ${view.population_id}`);
  assert(view.frame_type === 'LIGHT' && view.metric_name === 'FWHM', `population boundary mismatch in ${view.population_id}`);
  assert(view.coverage === 'COMPLETE_FOR_DECLARED_POPULATION', `non-complete population included: ${view.population_id}`);
  assert(view.unit === 'NINA_FILENAME_FWHM_SOURCE_UNIT', `unit mismatch in ${view.population_id}`);
  assert(view.unit_semantics === 'SOURCE_NATIVE_UNCALIBRATED', `unit semantics mismatch in ${view.population_id}`);
  assert(view.angular_calibration_state === 'NOT_PROVEN', `angular calibration escalation in ${view.population_id}`);
  assert(view.authority === 'projection' && view.action_authority === 'NONE', `authority escalation in ${view.population_id}`);
  assert(Array.isArray(view.measurements) && view.measurements.length === view.measurement_count, `measurement count mismatch in ${view.population_id}`);
  assert(unique(view.measurements.map((m) => m.record_id)), `duplicate measurement record in ${view.population_id}`);
  assert(view.measurements.every((m) => typeof m.value === 'number' && m.value > 0 && m.source_record_ref), `invalid source-backed measurement in ${view.population_id}`);
  assert(Array.isArray(view.citation_refs) && view.citation_refs.length > 0, `missing Citation in ${view.population_id}`);
  assert(Array.isArray(view.provenance_refs) && view.provenance_refs.length > 0, `missing Provenance in ${view.population_id}`);
  assert(Array.isArray(view.statistics) && view.statistics.length >= 3, `missing descriptive statistics in ${view.population_id}`);
  assert(view.statistics.every((s) => allowedStats.has(s.statistic_type) && s.sample_count === view.measurement_count), `invalid statistic in ${view.population_id}`);
  assert(view.limitations?.includes('SOURCE_NATIVE_FWHM_UNIT_IS_NOT_PHYSICALLY_CALIBRATED'), `missing calibration limitation in ${view.population_id}`);
  assert(view.limitations?.includes('NO_EQUIPMENT_HEALTH_RANKING_THRESHOLD_OR_RECOMMENDATION'), `health/ranking boundary missing in ${view.population_id}`);
  assert(view.limitations?.includes('HISTORICAL_READ_ONLY_PROJECTION_NOT_SAFETY_AUTHORITY'), `safety authority boundary missing in ${view.population_id}`);
}

console.log(`BKL-039 F5 collection valid: ${doc.views.length} populations, projection-only authority.`);
