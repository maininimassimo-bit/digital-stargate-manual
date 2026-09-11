import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import {
  buildDeterministicAdvisoryDemonstration,
  contentDigest,
  validateDeterministicAdvisoryOutput
} from './ai-post-processing-advisory-demonstrator.mjs';
import { validateRecommendationRecord } from './ai-post-processing-advisory-contract.mjs';

const source = JSON.parse(fs.readFileSync('docs/data/ai-post-processing-assistant-f2-fixture.json', 'utf8'));
const knownAnswer = JSON.parse(fs.readFileSync('docs/data/ai-post-processing-assistant-f3-output.json', 'utf8'));
const clone = () => structuredClone(source);

function reseal(record, field) {
  delete record[field];
  record[field] = contentDigest(record);
}

function resealFixture(fixture, { sources = [], recommendations = [] } = {}) {
  for (const index of sources) reseal(fixture.sourceBindings[index], 'bindingDigest');
  for (const index of recommendations) reseal(fixture.recommendations[index], 'recommendationDigest');
  reseal(fixture, 'artifactDigest');
  return fixture;
}

function evaluation(result, ruleId) {
  return result.ruleEvaluations.find((item) => item.ruleId === ruleId);
}

test('accepted F2 bounded fixture produces the F3 known answer', () => {
  assert.deepEqual(buildDeterministicAdvisoryDemonstration(clone()), knownAnswer);
  assert.equal(validateDeterministicAdvisoryOutput(knownAnswer), true);
});

test('generation is deterministic, idempotent and deeply immutable', () => {
  const first = buildDeterministicAdvisoryDemonstration(clone());
  const second = buildDeterministicAdvisoryDemonstration(clone());
  assert.deepEqual(first, second);
  assert.equal(Object.isFrozen(first), true);
  assert.equal(Object.isFrozen(first.recommendations), true);
  assert.equal(Object.isFrozen(first.recommendations[0].confidence), true);
});

test('the demonstrator does not mutate its F2 input', () => {
  const fixture = clone();
  const before = structuredClone(fixture);
  buildDeterministicAdvisoryDemonstration(fixture);
  assert.deepEqual(fixture, before);
});

test('generated records reuse the accepted F2 Recommendation contract', () => {
  const result = buildDeterministicAdvisoryDemonstration(clone());
  for (const recommendation of result.recommendations) {
    assert.equal(validateRecommendationRecord(recommendation, result.subject, result.sourceBindings), true);
  }
});

test('output is explicitly pre-decision and contains no decision receipts', () => {
  const result = buildDeterministicAdvisoryDemonstration(clone());
  assert.equal(result.decisionState, 'NOT_PRESENT_PRE_DECISION');
  assert.equal(Object.hasOwn(result, 'humanDecisionReceipts'), false);
});

test('processing history missingness emits stable fail-closed reason codes', () => {
  const result = buildDeterministicAdvisoryDemonstration(clone());
  const gate = evaluation(result, 'PROCESSING_HISTORY_AVAILABILITY');
  assert.equal(gate.decision, 'FAIL_CLOSED');
  assert.deepEqual(gate.reasonCodes, ['SOURCE_COMPLETENESS_UNAVAILABLE', 'SOURCE_QUALITY_UNKNOWN']);
  const recommendation = result.recommendations.find((item) => item.recommendationId === gate.recommendationId);
  assert.equal(recommendation.category, 'STOP_AND_REVIEW');
  assert.equal(recommendation.lifecycleState, 'incomplete');
  assert.equal(recommendation.parameterAdvice[0].mode, 'UNKNOWN_NOT_RECOMMENDED');
});

test('complete valid processing evidence passes without inventing parameters', () => {
  const fixture = clone();
  fixture.sourceBindings[1].quality = 'VALID';
  fixture.sourceBindings[1].completeness = 'COMPLETE';
  resealFixture(fixture, { sources: [1] });
  const result = buildDeterministicAdvisoryDemonstration(fixture);
  const gate = evaluation(result, 'PROCESSING_HISTORY_AVAILABILITY');
  assert.equal(gate.decision, 'PASS');
  const recommendation = result.recommendations.find((item) => item.recommendationId === gate.recommendationId);
  assert.equal(recommendation.lifecycleState, 'validated');
  assert.deepEqual(recommendation.parameterAdvice, []);
});

test('missing required source authority produces an explicit fail-closed result', () => {
  const fixture = clone();
  fixture.sourceBindings[1].sourceAuthority = 'projection';
  resealFixture(fixture, { sources: [1] });
  const result = buildDeterministicAdvisoryDemonstration(fixture);
  const gate = evaluation(result, 'PROCESSING_HISTORY_AVAILABILITY');
  assert.equal(gate.decision, 'FAIL_CLOSED');
  assert.deepEqual(gate.reasonCodes, ['REQUIRED_SOURCE_AUTHORITY_MISSING']);
});

test('stale governance evidence fails closed', () => {
  const fixture = clone();
  fixture.sourceBindings[0].quality = 'STALE';
  fixture.recommendations[0].lifecycleState = 'incomplete';
  fixture.recommendations[0].unknowns = ['SOURCE_QUALITY_STALE'];
  resealFixture(fixture, { sources: [0], recommendations: [0] });
  const gate = evaluation(buildDeterministicAdvisoryDemonstration(fixture), 'GOVERNANCE_READINESS');
  assert.equal(gate.decision, 'FAIL_CLOSED');
  assert.deepEqual(gate.reasonCodes, ['SOURCE_QUALITY_STALE']);
});

test('suggested governance evidence fails closed', () => {
  const fixture = clone();
  fixture.sourceBindings[0].evidenceClass = 'SUGGESTED';
  fixture.recommendations[0].lifecycleState = 'incomplete';
  fixture.recommendations[0].unknowns = ['SOURCE_CLASS_SUGGESTED'];
  resealFixture(fixture, { sources: [0], recommendations: [0] });
  const gate = evaluation(buildDeterministicAdvisoryDemonstration(fixture), 'GOVERNANCE_READINESS');
  assert.deepEqual(gate.reasonCodes, ['SOURCE_CLASS_SUGGESTED']);
});

test('unresolved subject correlation fails every rule closed', () => {
  const fixture = clone();
  fixture.subject.correlationState = 'UNRESOLVED';
  fixture.recommendations[0].lifecycleState = 'incomplete';
  fixture.recommendations[0].unknowns = ['SUBJECT_CORRELATION_UNRESOLVED'];
  resealFixture(fixture, { recommendations: [0] });
  const result = buildDeterministicAdvisoryDemonstration(fixture);
  assert(result.ruleEvaluations.every((item) => item.decision === 'FAIL_CLOSED'));
  assert(result.ruleEvaluations.every((item) => item.reasonCodes.includes('SUBJECT_CORRELATION_UNRESOLVED')));
});

test('tampered F2 fixture is rejected before rule execution', () => {
  const fixture = clone();
  fixture.sourceBindings[0].limitations[0] = 'Tampered without resealing.';
  assert.throws(() => buildDeterministicAdvisoryDemonstration(fixture), /digest does not match canonical content/);
});

test('unsupported F2 envelope is rejected', () => {
  const fixture = clone();
  fixture.contractType = 'LEGACY_ASSISTANT_FIXTURE';
  reseal(fixture, 'artifactDigest');
  assert.throws(() => buildDeterministicAdvisoryDemonstration(fixture), /Unsupported contractType/);
});

test('numeric confidence remains unavailable', () => {
  const result = buildDeterministicAdvisoryDemonstration(clone());
  for (const recommendation of result.recommendations) {
    assert.equal(recommendation.confidence.state, 'UNAVAILABLE_F2');
    assert.equal(recommendation.confidence.value, null);
    assert.equal(recommendation.confidence.contractRef, null);
  }
});

test('authority remains read-only, human-only and non-executing', () => {
  const authority = buildDeterministicAdvisoryDemonstration(clone()).authority;
  assert.equal(authority.consumerMode, 'READ_ONLY');
  assert.equal(authority.acceptanceAuthority, 'HUMAN_ONLY');
  assert.equal(authority.actionAuthority, 'NONE');
  assert.equal(authority.executionAuthority, 'NONE');
  assert.equal(authority.pixInsightApplyAuthorized, false);
  assert.equal(authority.automaticAcceptanceAuthorized, false);
  assert.equal(authority.safetyAuthority, 'LOCAL_PHYSICAL_INTERLOCKS');
});

test('output tampering is detected', () => {
  const result = structuredClone(knownAnswer);
  result.recommendations[0].rationale = 'Tampered output.';
  assert.throws(() => validateDeterministicAdvisoryOutput(result), /digest does not match canonical content/);
});

test('unknown output properties are rejected', () => {
  const result = structuredClone(knownAnswer);
  result.legacyStatus = 'READY';
  reseal(result, 'artifactDigest');
  assert.throws(() => validateDeterministicAdvisoryOutput(result), /legacyStatus is not allowed/);
});

test('model, provider, execution and decision-receipt channels are forbidden', () => {
  for (const key of ['modelId', 'provider', 'command', 'humanDecisionReceipts']) {
    const result = structuredClone(knownAnswer);
    result[key] = key === 'humanDecisionReceipts' ? [] : 'UNAUTHORIZED';
    reseal(result, 'artifactDigest');
    assert.throws(() => validateDeterministicAdvisoryOutput(result), /not allowed|forbidden/);
  }
});

test('rule decision and reason codes cannot disagree', () => {
  const result = structuredClone(knownAnswer);
  result.ruleEvaluations[0].decision = 'FAIL_CLOSED';
  reseal(result, 'artifactDigest');
  assert.throws(() => validateDeterministicAdvisoryOutput(result), /decision and reasonCodes disagree/);
});

test('rule evaluation cannot be rebound to another recommendation', () => {
  const result = structuredClone(knownAnswer);
  result.ruleEvaluations[0].recommendationId = result.ruleEvaluations[1].recommendationId;
  reseal(result, 'artifactDigest');
  assert.throws(() => validateDeterministicAdvisoryOutput(result), /wrong source authority|evaluated more than once/);
});

test('fail-closed reason codes must match Recommendation unknowns', () => {
  const result = structuredClone(knownAnswer);
  result.ruleEvaluations[1].reasonCodes = ['SOURCE_QUALITY_UNKNOWN'];
  reseal(result, 'artifactDigest');
  assert.throws(() => validateDeterministicAdvisoryOutput(result), /reasonCodes must match recommendation unknowns/);
});
