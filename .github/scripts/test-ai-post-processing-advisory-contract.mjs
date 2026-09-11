import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { canonicalJson, contentDigest, validateAdvisoryContractFixture } from './ai-post-processing-advisory-contract.mjs';

const source = JSON.parse(fs.readFileSync('docs/data/ai-post-processing-assistant-f2-fixture.json', 'utf8'));
const clone = () => structuredClone(source);

function reseal(record, field) {
  delete record[field];
  record[field] = contentDigest(record);
}

function resealFixture(fixture, { sources = [], recommendations = [], receipts = [] } = {}) {
  for (const index of sources) reseal(fixture.sourceBindings[index], 'bindingDigest');
  for (const index of recommendations) reseal(fixture.recommendations[index], 'recommendationDigest');
  for (const index of receipts) reseal(fixture.humanDecisionReceipts[index], 'receiptDigest');
  reseal(fixture, 'artifactDigest');
  return fixture;
}

test('canonical JSON and known-answer digest are deterministic', () => {
  assert.equal(canonicalJson({ b: 2, a: 1 }), '{"a":1,"b":2}');
  assert.equal(contentDigest({ b: 2, a: 1 }), '43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777');
});

test('bounded synthetic fixture passes with separate recommendation and decision receipt', () => {
  assert.equal(validateAdvisoryContractFixture(clone()), true);
  assert.equal(source.humanDecisionReceipts[0].executionState, 'NOT_OBSERVED');
  assert.deepEqual(source.humanDecisionReceipts[0].executionEvidenceRefs, []);
});

test('unknown properties are rejected fail-closed', () => {
  const fixture = clone();
  fixture.recommendations[0].legacyState = 'APPROVED';
  resealFixture(fixture, { recommendations: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /legacyState is not allowed/);
});

test('tampered recommendation identity fails closed', () => {
  const fixture = clone();
  fixture.recommendations[0].rationale = 'TAMPERED';
  resealFixture(fixture);
  assert.throws(() => validateAdvisoryContractFixture(fixture), /digest does not match canonical content/);
});

test('stale evidence cannot validate a recommendation', () => {
  const fixture = clone();
  fixture.sourceBindings[0].quality = 'STALE';
  resealFixture(fixture, { sources: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /cannot be validated from stale/);
});

test('suggested evidence cannot validate a recommendation', () => {
  const fixture = clone();
  fixture.sourceBindings[0].evidenceClass = 'SUGGESTED';
  resealFixture(fixture, { sources: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /suggested evidence/);
});

test('unresolved subject correlation blocks validated state', () => {
  const fixture = clone();
  fixture.subject.correlationState = 'UNRESOLVED';
  resealFixture(fixture);
  assert.throws(() => validateAdvisoryContractFixture(fixture), /unresolved subject correlation/);
});

test('conflicts and unknowns block validated state', () => {
  const fixture = clone();
  fixture.recommendations[0].unknowns = ['Synthetic unresolved fact'];
  resealFixture(fixture, { recommendations: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /resolved conflicts and unknowns/);
});

test('ungoverned confidence value is rejected', () => {
  const fixture = clone();
  fixture.recommendations[0].confidence.value = 0.9;
  resealFixture(fixture, { recommendations: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /must not carry ungoverned confidence/);
});

test('unknown parameter advice cannot invent a value', () => {
  const fixture = clone();
  fixture.recommendations[1].parameterAdvice[0].lowerBound = 0.2;
  resealFixture(fixture, { recommendations: [1] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /must not invent a parameter or value/);
});

test('bounded parameter interval cannot be inverted', () => {
  const fixture = clone();
  Object.assign(fixture.recommendations[1].parameterAdvice[0], {
    parameterId: 'SyntheticProcess.strength', mode: 'BOUNDED_INTERVAL', unit: 'ratio', lowerBound: 0.8, upperBound: 0.2
  });
  resealFixture(fixture, { recommendations: [1] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /interval must not be inverted/);
});

test('authority escalation and PixInsight apply authorization are rejected', () => {
  for (const [field, value, expected] of [
    ['actionAuthority', 'PIXINSIGHT_APPLY', /actionAuthority must be NONE/],
    ['pixInsightApplyAuthorized', true, /PixInsight apply is not authorized/],
    ['automaticAcceptanceAuthorized', true, /Automatic acceptance is not authorized/]
  ]) {
    const fixture = clone();
    fixture.authority[field] = value;
    resealFixture(fixture);
    assert.throws(() => validateAdvisoryContractFixture(fixture), expected);
  }
});

test('human decision receipt cannot claim execution', () => {
  const fixture = clone();
  fixture.humanDecisionReceipts[0].executionState = 'EXECUTED';
  fixture.humanDecisionReceipts[0].executionEvidenceRefs = ['PXP-OBSERVED-001'];
  resealFixture(fixture, { receipts: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /must not claim execution/);
});

test('human decision receipt must preserve recommendation correlation', () => {
  const fixture = clone();
  fixture.humanDecisionReceipts[0].correlationId = 'CORR-MISMATCH';
  resealFixture(fixture, { receipts: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /correlationId does not match/);
});

test('edited disposition requires explicit human edits', () => {
  const fixture = clone();
  fixture.humanDecisionReceipts[0].disposition = 'EDITED_FOR_MANUAL_APPLICATION';
  resealFixture(fixture, { receipts: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /requires decision edits/);
});

test('model/provider and executable channels are forbidden in F2', () => {
  const fixture = clone();
  fixture.recommendations[0].provider = 'UNAUTHORIZED';
  resealFixture(fixture, { recommendations: [0] });
  assert.throws(() => validateAdvisoryContractFixture(fixture), /provider is forbidden in BKL-046 F2/);
});
