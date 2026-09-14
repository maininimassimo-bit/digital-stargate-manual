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

function fact(id, semanticType, value, unit, sourceRef, citationRef, provenanceRef, evidenceKind) {
  return {
    fact_id:id, semantic_type:semanticType, value, unit, temporal_scope:'STATIC',
    observed_at_utc:null, issue_at_utc:null, valid_interval:null,
    spatial_scope_ref:null, method_ref:null, source_ref:sourceRef,
    citation_refs:[citationRef], provenance_refs:[provenanceRef],
    evidence_kind:evidenceKind
  };
}
