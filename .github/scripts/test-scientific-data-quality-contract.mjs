import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { canonicalJson, contentDigest, validateQualityContractFixture } from './scientific-data-quality-contract.mjs';

const source = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f2-fixture.json', 'utf8'));
const clone = () => structuredClone(source);

function reseal(record, field) {
  delete record[field];
  record[field] = contentDigest(record);
}

function resealFixture(fixture, { profile = false, evidence = [], dimensions = [] } = {}) {
  if (profile) reseal(fixture.assessmentProfile, 'profileDigest');
  for (const index of evidence) reseal(fixture.qualityEvidence[index], 'evidenceDigest');
  for (const index of dimensions) reseal(fixture.dimensionAssessments[index], 'assessmentDigest');
  reseal(fixture, 'artifactDigest');
  return fixture;
}

test('canonical JSON and known-answer digest are deterministic', () => {
  assert.equal(canonicalJson({ b: 2, a: 1 }), '{"a":1,"b":2}');
  assert.equal(contentDigest({ b: 2, a: 1 }), '43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777');
});

test('accepted bounded fixture passes and preserves missing required evidence explicitly', () => {
  assert.equal(validateQualityContractFixture(clone()), true);
  const guiding = source.dimensionAssessments.find((item) => item.dimension === 'GUIDING_STABILITY');
  assert.equal(guiding.assessmentState, 'UNAVAILABLE');
  assert.ok(guiding.exclusionReasons.includes('REQUIRED_EVIDENCE_MISSING'));
});

test('required dimension without an explicit assessment fails closed', () => {
  const fixture = clone();
  fixture.dimensionAssessments = fixture.dimensionAssessments.filter((item) => item.dimension !== 'GUIDING_STABILITY');
  resealFixture(fixture);
  assert.throws(() => validateQualityContractFixture(fixture), /has no explicit assessment/);
});

test('missing required evidence cannot be reported as available', () => {
  const fixture = clone();
  const index = fixture.dimensionAssessments.findIndex((item) => item.dimension === 'GUIDING_STABILITY');
  fixture.dimensionAssessments[index].assessmentState = 'AVAILABLE';
  fixture.dimensionAssessments[index].eligibility = 'CONDITIONAL';
  resealFixture(fixture, { dimensions: [index] });
  assert.throws(() => validateQualityContractFixture(fixture), /must be UNAVAILABLE/);
});

test('incompatible SQM unit is rejected', () => {
  const fixture = clone();
  const index = fixture.qualityEvidence.findIndex((item) => item.dimension === 'SKY_QUALITY_COVERAGE');
  fixture.qualityEvidence[index].unit = 'lux';
  resealFixture(fixture, { evidence: [index] });
  assert.throws(() => validateQualityContractFixture(fixture), /requires unit mag\/arcsec2/);
});

test('uncalibrated optical evidence cannot become eligible', () => {
  const fixture = clone();
  const evidenceIndex = fixture.qualityEvidence.findIndex((item) => item.dimension === 'OPTICAL_IMAGE_QUALITY');
  const dimensionIndex = fixture.dimensionAssessments.findIndex((item) => item.dimension === 'OPTICAL_IMAGE_QUALITY');
  Object.assign(fixture.qualityEvidence[evidenceIndex], { value: 2.1, unit: 'px', quality: 'VALID', completeness: 'COMPLETE', coverage: 1 });
  Object.assign(fixture.dimensionAssessments[dimensionIndex], { assessmentState: 'AVAILABLE', eligibility: 'ELIGIBLE_FOR_FUTURE_NORMALIZATION' });
  resealFixture(fixture, { evidence: [evidenceIndex], dimensions: [dimensionIndex] });
  assert.throws(() => validateQualityContractFixture(fixture), /proven angular calibration/);
});

test('partial PixInsight provenance cannot become eligible', () => {
  const fixture = clone();
  const evidenceIndex = fixture.qualityEvidence.findIndex((item) => item.dimension === 'PROCESSING_PROVENANCE_COMPLETENESS');
  const dimensionIndex = fixture.dimensionAssessments.findIndex((item) => item.dimension === 'PROCESSING_PROVENANCE_COMPLETENESS');
  Object.assign(fixture.qualityEvidence[evidenceIndex], { value: 'PARTIAL', quality: 'VALID', completeness: 'PARTIAL', coverage: 0.5 });
  Object.assign(fixture.dimensionAssessments[dimensionIndex], { assessmentState: 'PARTIAL', eligibility: 'ELIGIBLE_FOR_FUTURE_NORMALIZATION' });
  resealFixture(fixture, { evidence: [evidenceIndex], dimensions: [dimensionIndex] });
  assert.throws(() => validateQualityContractFixture(fixture), /only when evidence is complete and valid/);
});

test('SUGGESTED evidence cannot become eligible evidence', () => {
  const fixture = clone();
  const evidenceIndex = fixture.qualityEvidence.findIndex((item) => item.dimension === 'METADATA_LINEAGE_INTEGRITY');
  const dimensionIndex = fixture.dimensionAssessments.findIndex((item) => item.dimension === 'METADATA_LINEAGE_INTEGRITY');
  fixture.qualityEvidence[evidenceIndex].evidenceClass = 'SUGGESTED';
  fixture.dimensionAssessments[dimensionIndex].eligibility = 'ELIGIBLE_FOR_FUTURE_NORMALIZATION';
  resealFixture(fixture, { evidence: [evidenceIndex], dimensions: [dimensionIndex] });
  assert.throws(() => validateQualityContractFixture(fixture), /SUGGESTED evidence cannot become eligible/);
});

test('authority escalation is rejected', () => {
  const fixture = clone();
  fixture.authority.actionAuthority = 'DEVICE_COMMAND';
  resealFixture(fixture);
  assert.throws(() => validateQualityContractFixture(fixture), /actionAuthority must be NONE/);
});

test('numeric scores and weights are forbidden in F2', () => {
  for (const [field, value] of [['scoreValue', 81], ['weight', 0.25]]) {
    const fixture = clone();
    fixture.assessmentProfile[field] = value;
    resealFixture(fixture, { profile: true });
    assert.throws(() => validateQualityContractFixture(fixture), /forbidden in BKL-041 F2/);
  }
});

test('unknown properties are rejected fail-closed', () => {
  const fixture = clone();
  fixture.qualityEvidence[0].legacyQuality = 'GOOD';
  resealFixture(fixture, { evidence: [0] });
  assert.throws(() => validateQualityContractFixture(fixture), /legacyQuality is not allowed/);
});

test('tampered evidence identity fails closed', () => {
  const fixture = clone();
  fixture.qualityEvidence[0].value = 'TAMPERED';
  resealFixture(fixture);
  assert.throws(() => validateQualityContractFixture(fixture), /digest does not match canonical content/);
});
