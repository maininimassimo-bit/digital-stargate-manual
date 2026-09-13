import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { buildF5Decision, buildRealEvidenceValidation } from './scientific-data-quality-real-evidence-validation.mjs';
import { validateRealEvidenceFreshness } from '../../docs/javascripts/scientific-data-quality-core.mjs';

const catalog = JSON.parse(fs.readFileSync('docs/data/scientific-session-catalog.json', 'utf8'));
const projection = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-projection.json', 'utf8'));

function projectionStateCounts(assessments) {
  return Object.fromEntries(
    ['AVAILABLE', 'UNAVAILABLE', 'INVALID'].map(state => [
      state.toLowerCase(),
      assessments.filter(item => item.projectionRecordState === state).length
    ])
  );
}

test('real full catalog produces a deterministic non-production decision', () => {
  const a = buildRealEvidenceValidation(catalog, projection);
  const b = buildRealEvidenceValidation(structuredClone(catalog), structuredClone(projection));
  assert.deepEqual(a, b);
  assert.equal(a.cohort.sessionCount, catalog.sessions.length);
  assert.equal(a.decision.productionReadiness, 'NOT_READY_FOR_PRODUCTION');
  assert.equal(a.decision.capabilityAcceptance, 'ACCEPTED_AS_READ_ONLY_EXPERIMENTAL_WITH_RETAINED_LIMITATIONS');
});

test('cohort includes every catalog session without outcome filtering', () => {
  const result = buildRealEvidenceValidation(catalog, projection);
  assert.deepEqual(result.sourceCatalog.sessionIds, catalog.sessions.map(x => x.sessionId).sort());
  assert.deepEqual(result.cohort.assessmentStates, projectionStateCounts(projection.assessments));
  assert.equal(
    Object.values(result.cohort.assessmentStates).reduce((sum, count) => sum + count, 0),
    catalog.sessions.length
  );
});

test('bias and evidence gaps remain explicit', () => {
  const result = buildRealEvidenceValidation(catalog, projection);
  assert.deepEqual(result.cohort.knownTargets, ['LDN 1320', 'M 27']);
  assert.equal(result.cohort.evidenceAvailability.guidingTemporalCoverage, 0);
  assert.ok(result.biasDisclosure.includes('AVAILABLE_ASSESSMENTS_ARE_ONLY_FOR_M27_IN_THE_CURRENT_COHORT'));
  assert.ok(result.decision.reasonCodes.includes('REFERENCE_GROUND_TRUTH'));
});

test('readiness criteria are governance gates and never quality thresholds', () => {
  const result = buildRealEvidenceValidation(catalog, projection);
  assert.equal(result.acceptancePolicy.purpose, 'PRODUCTION_CALIBRATION_READINESS_NOT_SCIENTIFIC_QUALITY_THRESHOLD');
  assert.ok(result.acceptancePolicy.requirements.every(item => Object.keys(item).sort().join(',') === 'criterionId,requiredState'));
  assert.doesNotMatch(
    JSON.stringify(result.acceptancePolicy),
    /minimumImportedSessions|minimumKnownTargets|minimumAvailableAssessmentRatio|maximumInvalidAssessmentCount|minimumSqmEvidenceRatio/
  );
  assert.equal(result.authority.acceptanceAuthority, false);
  assert.equal(result.authority.actionAuthority, 'NONE');
  assert.equal(result.authority.productionUseAuthorized, false);
});

test('even complete calibration inputs never grant production readiness automatically', () => {
  const decision = buildF5Decision([{ criterionId: 'SYNTHETIC_FUTURE_INPUT', status: 'PASS' }]);
  assert.equal(decision.calibrationInputReadiness, 'ELIGIBLE_FOR_CALIBRATION_REVIEW');
  assert.equal(decision.productionReadiness, 'NOT_READY_FOR_PRODUCTION');
  assert.equal(decision.productionProfileAuthorized, false);
  assert.equal(decision.productionUseAuthorized, false);
});

test('stale projection fails closed', () => {
  const changed = structuredClone(catalog);
  changed.sessions[0].target = 'CHANGED';
  assert.throws(() => buildRealEvidenceValidation(changed, projection), /stale/);
});

test('session identity mismatch fails closed', () => {
  const changed = structuredClone(projection);
  changed.assessments[0].sessionId = 'OTHER';
  assert.throws(() => buildRealEvidenceValidation(catalog, changed), /identity mismatch/);
});

test('production authority escalation is rejected', () => {
  const changed = structuredClone(projection);
  changed.authority.productionUseAuthorized = true;
  assert.throws(() => buildRealEvidenceValidation(catalog, changed), /escalation/);
});

test('result is deeply immutable', () => {
  const result = buildRealEvidenceValidation(catalog, projection);
  assert.ok(Object.isFrozen(result));
  assert.ok(Object.isFrozen(result.results));
  assert.throws(() => result.results.push({}), TypeError);
});

test('browser contract accepts the aligned persisted validation', async () => {
  const validation = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f5-validation.json', 'utf8'));
  assert.equal(await validateRealEvidenceFreshness(validation, projection, catalog), true);
});

test('browser contract rejects a tampered production decision', async () => {
  const validation = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f5-validation.json', 'utf8'));
  validation.decision.productionUseAuthorized = true;
  await assert.rejects(validateRealEvidenceFreshness(validation, projection, catalog), /production use authority drift/);
});

test('browser contract rejects unknown nested properties', async () => {
  const validation = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f5-validation.json', 'utf8'));
  validation.cohort.legacyThreshold = 0.8;
  await assert.rejects(validateRealEvidenceFreshness(validation, projection, catalog), /proprietà mancanti o sconosciute/);
});
