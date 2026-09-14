import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { loadRepositorySources, validateObservationPlannerContext } from './verify-observation-planner-context-f2.mjs';

const fixture = JSON.parse(fs.readFileSync('docs/data/observation-planner-context-f2-fixture.json', 'utf8'));
const repositorySources = loadRepositorySources();
const clone = value => structuredClone(value);
const errorsFor = (mutate, sourceMutate = () => {}) => {
  const doc = clone(fixture); const sources = clone(repositorySources);
  mutate(doc); sourceMutate(sources);
  return validateObservationPlannerContext(doc, sources).join('\n');
};
const rejects = (name, mutate, pattern, sourceMutate) => test(name, () => assert.match(errorsFor(mutate, sourceMutate), pattern));
const dimension = (doc, type) => doc.evidence_dimensions.find(item => item.dimension_type === type);
const explanation = doc => doc.ranking_explanations[0];

test('accepted bounded fixture validates', () => assert.deepEqual(validateObservationPlannerContext(fixture, repositorySources), []));

rejects('N01 candidate without source Citation and Provenance fails closed', doc => {
  const item = doc.target_candidates[0]; item.source_refs = []; item.citation_refs = []; item.provenance_refs = [];
}, /candidate.*(?:source_refs|Citation|Provenance)/i);

rejects('N02 conflicted BKL-035 identity cannot be reported as validated', () => {}, /identity state conflict|cannot be validated/i, sources => {
  sources.targetKnowledgeReadModel.targets.find(item => item.target_key === 'dsg-target:m-27').identity_state = 'conflicted';
});

rejects('N03 unknown target is not fuzzy-matched', doc => {
  const item = doc.target_candidates[0]; item.target_key = 'dsg-target:m27'; item.canonical_name = 'M27'; item.target_id = null;
}, /no exact BKL-035 identity; fuzzy matching prohibited/);

rejects('N04 historical configuration cannot become current', doc => {
  doc.planning_contexts[0].active_setup_ref = 'configuration:C8_QHY695A_BIN1';
}, /historical configuration cannot become current/);

rejects('N05 missing site keeps celestial and lunar evidence unavailable', doc => {
  const item = dimension(doc, 'CELESTIAL_GEOMETRY'); item.availability_state = 'AVAILABLE'; item.evidence_kind = 'DECLARED';
}, /missing site requires unavailable celestial\/lunar evidence|usable evidence requires/);

rejects('N06 target coordinates require epoch', doc => {
  const item = dimension(doc, 'CELESTIAL_GEOMETRY');
  item.availability_state = 'AVAILABLE'; item.evidence_kind = 'DECLARED';
  item.citation_refs = ['CIT-OP-M27-IDENTITY@1.0']; item.provenance_refs = ['PRV-OP-M27-IDENTITY-DIM@1.0'];
  item.facts = [
    fact('FACT-RA','TARGET_RA_DEG',299.9017,'DEG','BKL031-S01','CIT-OP-M27-IDENTITY@1.0','PRV-OP-M27-IDENTITY-DIM@1.0','DECLARED'),
    fact('FACT-DEC','TARGET_DEC_DEG',22.7211,'DEG','BKL031-S01','CIT-OP-M27-IDENTITY@1.0','PRV-OP-M27-IDENTITY-DIM@1.0','DECLARED')
  ];
  item.source_refs = ['BKL031-S01'];
}, /target coordinates require epoch/);

rejects('N07 ephemeris output requires governed source and method version', doc => {
  const item = dimension(doc, 'CELESTIAL_GEOMETRY');
  item.availability_state = 'AVAILABLE'; item.evidence_kind = 'DECLARED';
  item.citation_refs = ['CIT-OP-M27-IDENTITY@1.0']; item.provenance_refs = ['PRV-OP-M27-IDENTITY-DIM@1.0'];
  item.source_refs = ['BKL031-S10'];
  item.facts = [fact('FACT-ALT','ALTITUDE_DEG',45,'DEG','BKL031-S10','CIT-OP-M27-IDENTITY@1.0','PRV-OP-M27-IDENTITY-DIM@1.0','DECLARED')];
}, /ephemeris output requires governed source and method\/version/);

rejects('N08 forecast requires provider run issue validity and spatial applicability', doc => {
  const item = dimension(doc, 'FORECAST');
  item.availability_state = 'AVAILABLE'; item.evidence_kind = 'DECLARED';
  item.citation_refs = ['CIT-OP-M27-IDENTITY@1.0']; item.provenance_refs = ['PRV-OP-M27-IDENTITY-DIM@1.0'];
  item.facts = [fact('FACT-CLOUD','FORECAST_CLOUD_PCT',10,'PERCENT','BKL031-S11','CIT-OP-M27-IDENTITY@1.0','PRV-OP-M27-IDENTITY-DIM@1.0','DECLARED')];
}, /forecast requires provider run, issue time, valid interval and spatial applicability/);

rejects('N09 historical weather cannot substitute forecast', doc => {
  const item = dimension(doc, 'FORECAST');
  item.availability_state = 'AVAILABLE'; item.evidence_kind = 'OBSERVED';
  item.source_refs = ['BKL031-S05']; item.citation_refs = ['CIT-OP-M27-SQM-20260913@1.0']; item.provenance_refs = ['PRV-OP-M27-SQM-DIM@1.0'];
  item.facts = [fact('FACT-HIST-CLOUD','FORECAST_CLOUD_PCT',10,'PERCENT','BKL031-S05','CIT-OP-M27-SQM-20260913@1.0','PRV-OP-M27-SQM-DIM@1.0','OBSERVED')];
}, /historical weather cannot substitute forecast/);

rejects('N10 expired realtime evidence becomes stale and excludes the value', doc => {
  const item = dimension(doc, 'OBSERVED_WEATHER_SQM'); const value = item.facts[0];
  item.source_refs = ['BKL031-S07']; value.source_ref = 'BKL031-S07'; value.temporal_scope = 'CURRENT';
  value.observed_at_utc = '2026-09-13T20:00:00Z';
  value.valid_interval = {start_utc:'2026-09-13T20:00:00Z',end_utc:'2026-09-13T21:00:00Z'};
}, /realtime evidence expired and must be STALE/);

rejects('N11 null zero or empty source value is rejected', doc => {
  dimension(doc, 'OBSERVED_WEATHER_SQM').facts[0].value = 0;
}, /null, zero, empty or semantically invalid value/);

rejects('N12 analytics cannot override target identity authority', doc => {
  const item = dimension(doc, 'TARGET_IDENTITY'); item.source_refs = ['BKL031-S05']; item.facts[0].source_ref = 'BKL031-S05';
}, /analytics\/read model cannot override BKL-035 target authority/);

rejects('N13 numeric weight score threshold normalization or ordering is prohibited', doc => {
  doc.ranking_factors[0].weight = 0.5;
}, /prohibited F2 field weight/);

rejects('N14 explanation cannot omit excluded or stale dimensions', doc => {
  explanation(doc).excluded_dimension_refs = [];
}, /explanation must enumerate every excluded dimension/);

rejects('N15 operational conclusion vocabulary is prohibited', doc => {
  explanation(doc).message = 'Target is safe and ready to go.';
}, /operational conclusion vocabulary is prohibited/);

rejects('N16 command or sequence-edit path is prohibited', doc => {
  doc.command = {device:'NINA',operation:'edit_sequence'};
}, /prohibited F2 field command/);

rejects('N17 EAGLE compute or external-call workload is prohibited', doc => {
  doc.execution_zone = 'EAGLE';
}, /EAGLE workload is prohibited/);

rejects('N18 suggested result cannot be re-ingested as observed evidence', doc => {
  const value = dimension(doc, 'TARGET_IDENTITY').facts[0];
  value.evidence_kind = 'OBSERVED'; value.provenance_refs = ['PRV-OP-M27-EXPLANATION@1.0'];
}, /suggested result cannot be re-ingested as observed evidence/);

rejects('N19 raw operational locator or credential cannot enter public projection', doc => {
  doc.citations[0].locator.path = 'data/sessions/2026/09/raw/nina/operator-token.log';
}, /raw operational locator or credential is prohibited/);

rejects('N20 conflict cannot be silently resolved by recency file order or UI text', doc => {
  doc.target_candidates[0].resolution_basis = 'RECENCY_ONLY';
}, /prohibited conflict resolution basis/);


test('M01 validator is total for non-object JSON roots', () => {
  assert.deepEqual(validateObservationPlannerContext(null, repositorySources), ['observation planner contract must be an object']);
  assert.deepEqual(validateObservationPlannerContext([], repositorySources), ['observation planner contract must be an object']);
});

rejects('M01 wrong root collection type returns deterministic errors without throwing', doc => {
  doc.sources = {};
}, /source inventory must contain exactly|missing source BKL031-S01/);

rejects('M01 missing nested collection returns deterministic structural error', doc => {
  delete doc.sources[0].reason_codes;
}, /required property reason_codes missing|reason_codes must be unique refs/);

rejects('M01 null nested object returns deterministic structural error', doc => {
  doc.citations[0].locator = null;
}, /locator: must be an object|locator.*must be non-empty/);

rejects('M02 SQM value must equal its cited source field', doc => {
  dimension(doc, 'OBSERVED_WEATHER_SQM').facts[0].value = 19.99;
}, /value does not equal cited sqm_median_mag_arcsec2/);

rejects('M02 identity fact cannot reuse a valid Citation for a different value', doc => {
  dimension(doc, 'TARGET_IDENTITY').facts[0].value = 'dsg-target:ldn-1320';
}, /value does not equal (?:the cited BKL-035 target_key|its Citation record_value)/);

rejects('M02 Provenance output_ref must bind to the exact dimension', doc => {
  doc.provenance_records.find(item => item.id === 'PRV-OP-M27-SQM-DIM').output_ref = 'DIM-OTHER';
}, /Provenance (?:must bind exactly|output)|dimension Provenance input\/output\/Citation binding mismatch/i);

rejects('M02 session fact cannot reuse another existing session Citation', doc => {
  const item = dimension(doc, 'SCIENTIFIC_HISTORY').facts[0];
  item.citation_refs = ['CIT-OP-M27-SESSION-20260815@1.0'];
}, /value does not equal cited session reference|dimension Citation set/);

rejects('M03 readiness semantic smuggling is rejected inside a fact', doc => {
  const item = dimension(doc, 'TARGET_IDENTITY').facts[0];
  item.semantic_type = 'READINESS'; item.value = 'READY';
}, /readiness\/safety\/authorization\/score\/threshold\/normalization\/ordering semantics are prohibited|closed vocabulary/);

rejects('M03 operational value smuggling is rejected even with an allowed semantic type', doc => {
  dimension(doc, 'TARGET_IDENTITY').facts[0].value = 'AUTHORIZED';
}, /readiness\/safety\/authorization\/score\/threshold\/normalization\/ordering semantics are prohibited/);

test('M04 exact governed S02 coordinate triplet is accepted in a synthetic governed-site context', () => {
  const doc = clone(fixture); addCoordinateEvidence(doc);
  assert.deepEqual(validateObservationPlannerContext(doc, repositorySources), []);
});

rejects('M04 coordinate fact rejects the wrong source class', doc => {
  addCoordinateEvidence(doc);
  const item = dimension(doc, 'CELESTIAL_GEOMETRY');
  item.source_refs.push('BKL031-S01');
  item.facts[0].source_ref = 'BKL031-S01';
}, /source class is not authorized|coordinate Citation must resolve to eligible S02\/S04/);

rejects('M04 coordinate range is validated', doc => {
  addCoordinateEvidence(doc);
  dimension(doc, 'CELESTIAL_GEOMETRY').facts.find(item => item.semantic_type === 'TARGET_RA_DEG').value = 360;
}, /RA must be in \[0,360\) degrees/);

rejects('M04 coordinate values must match governed S02 evidence', doc => {
  addCoordinateEvidence(doc);
  dimension(doc, 'CELESTIAL_GEOMETRY').facts.find(item => item.semantic_type === 'TARGET_DEC_DEG').value = 21;
}, /coordinate value conflicts with governed S02 evidence/);

rejects('M04 conflicting governed coordinate evidence cannot be published as available', doc => {
  addCoordinateEvidence(doc);
}, /conflicting governed S02 coordinate evidence must remain CONFLICTED or UNAVAILABLE/, sources => {
  sources.scientificMetadataCsv = sources.scientificMetadataCsv.replace(
    ',M 27,TGT-MESSIER-M27,299.9017,22.7211,C8_QHY695A_BIN1',
    ',M 27,TGT-MESSIER-M27,300.0000,22.7211,C8_QHY695A_BIN1'
  );
});

function addCoordinateEvidence(doc) {
  const citationRef = 'CIT-OP-M27-COORD-20260814@1.0';
  const provenanceRef = 'PRV-OP-M27-COORD-DIM@1.0';
  const item = dimension(doc, 'CELESTIAL_GEOMETRY');
  item.availability_state = 'AVAILABLE';
  item.evidence_kind = 'DECLARED';
  item.source_refs = ['BKL031-S02'];
  item.citation_refs = [citationRef];
  item.provenance_refs = [provenanceRef];
  item.reason_codes = ['HISTORICAL_ONLY'];
  item.facts = [
    fact('FACT-M27-RA','TARGET_RA_DEG',299.9017,'DEG','BKL031-S02',citationRef,provenanceRef,'DECLARED'),
    fact('FACT-M27-DEC','TARGET_DEC_DEG',22.7211,'DEG','BKL031-S02',citationRef,provenanceRef,'DECLARED'),
    fact('FACT-M27-EPOCH','COORDINATE_EPOCH','J2000',null,'BKL031-S02',citationRef,provenanceRef,'DECLARED')
  ];
  item.facts.forEach(value => { value.temporal_scope = 'HISTORICAL'; });
  doc.citations.push({
    id:'CIT-OP-M27-COORD-20260814', version:'1.0', source_ref:'BKL031-S02',
    locator:{
      path:'data/analytics/metadata/session-scientific-metadata.csv',
      record_key:'session_id',
      record_value:'2026-08-14_2026-08-15'
    },
    public_safe:true
  });
  doc.provenance_records.push({
    id:'PRV-OP-M27-COORD-DIM', version:'1.0',
    method_id:'BKL031-F2-EVIDENCE-BINDING-1',
    input_refs:['session:2026-08-14_2026-08-15','BKL031-S02'],
    output_ref:item.dimension_id,
    citation_refs:[citationRef],
    evidence_kind:'DECLARED'
  });
  const context = doc.planning_contexts[0];
  context.site_ref = 'site:synthetic-governed-test';
  context.unavailable_dimension_refs = context.unavailable_dimension_refs.filter(value => value !== item.dimension_id);
  const result = explanation(doc);
  result.excluded_dimension_refs = result.excluded_dimension_refs.filter(value => value !== item.dimension_id);
  result.citation_refs.push(citationRef);
  result.missing_reason_codes = [...new Set(
    doc.evidence_dimensions
      .filter(value => value.candidate_ref === result.candidate_ref && value.availability_state !== 'AVAILABLE')
      .flatMap(value => value.reason_codes)
  )];
  doc.provenance_records.find(value => value.id === 'PRV-OP-M27-EXPLANATION').citation_refs.push(citationRef);
}

function fact(id, semanticType, value, unit, sourceRef, citationRef, provenanceRef, evidenceKind) {
  return {
    fact_id:id, semantic_type:semanticType, value, unit, temporal_scope:'STATIC',
    observed_at_utc:null, issue_at_utc:null, valid_interval:null,
    spatial_scope_ref:null, method_ref:null, source_ref:sourceRef,
    citation_refs:[citationRef], provenance_refs:[provenanceRef],
    evidence_kind:evidenceKind
  };
}
