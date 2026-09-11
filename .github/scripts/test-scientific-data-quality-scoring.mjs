import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import {
  buildScientificDataQualityAssessment,
  canonicalJson,
  contentDigest,
  validateScoringProfile
} from './scientific-data-quality-scoring.mjs';

const source = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f3-fixture.json', 'utf8'));
const clone = () => structuredClone(source);

function resealProfile(profile) {
  delete profile.profileDigest;
  profile.profileDigest = contentDigest(profile);
}

function build(fixture = clone()) {
  return buildScientificDataQualityAssessment(fixture);
}

test('canonical JSON identity remains compatible with F2', () => {
  assert.equal(canonicalJson({ b: 2, a: 1 }), '{"a":1,"b":2}');
  assert.equal(contentDigest({ b: 2, a: 1 }), '43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777');
});

test('synthetic demonstrator profile and known answer validate', () => {
  assert.equal(validateScoringProfile(clone().profile), true);
  const result = build();
  assert.equal(result.assessmentState, source.expected.assessmentState);
  assert.equal(result.score.value, source.expected.scoreValue);
  assert.equal(result.confidence.value, source.expected.confidenceValue);
  assert.equal(result.evidenceCoverage, source.expected.evidenceCoverage);
  assert.equal(result.assessmentDigest, source.expected.assessmentDigest);
});

test('assessment is deterministic and deeply immutable', () => {
  const first = build();
  const second = build();
  assert.deepEqual(first, second);
  assert.equal(Object.isFrozen(first), true);
  assert.equal(Object.isFrozen(first.decomposition), true);
});

test('input order does not affect identity or result', () => {
  const fixture = clone();
  fixture.dimensions.reverse();
  assert.deepEqual(build(fixture), build());
});

test('required weights must sum exactly to one', () => {
  const fixture = clone();
  fixture.profile.dimensions[0].weight = 0.19;
  resealProfile(fixture.profile);
  assert.throws(() => build(fixture), /weights must sum to 1/);
});

test('negative weights are rejected', () => {
  const fixture = clone();
  fixture.profile.dimensions[0].weight = -0.1;
  resealProfile(fixture.profile);
  assert.throws(() => build(fixture), /must be within \[0,1\]/);
});

test('out-of-range observations are rejected, never clamped', () => {
  const fixture = clone();
  fixture.dimensions.find((item) => item.dimension === 'GUIDING_STABILITY').value = 3.1;
  assert.throws(() => build(fixture), /outside \[0.5,3\].*REJECT/);
});

test('missing required evidence fails closed without silent reweighting', () => {
  const fixture = clone();
  fixture.dimensions = fixture.dimensions.filter((item) => item.dimension !== 'GUIDING_STABILITY');
  const result = build(fixture);
  assert.equal(result.assessmentState, 'UNAVAILABLE');
  assert.equal(result.score, null);
  assert.equal(result.confidence, null);
  assert.equal(result.evidenceCoverage, 0.725);
  assert.equal(result.decomposition.find((item) => item.dimension === 'GUIDING_STABILITY').exclusionReason, 'REQUIRED_EVIDENCE_MISSING');
});

test('optional evidence remains visible and has zero scoring effect', () => {
  const fixture = clone();
  fixture.dimensions.push({
    dimension: 'OPTICAL_IMAGE_QUALITY', value: 0.5, unit: 'arcsec', evidenceClass: 'OBSERVED',
    quality: 'VALID', completeness: 'COMPLETE', coverage: 1, calibrationState: 'PROVEN',
    eligibility: 'ELIGIBLE_FOR_FUTURE_NORMALIZATION', evidenceRefs: ['SYN-EV-OPTICAL']
  });
  const result = build(fixture);
  assert.equal(result.score.value, source.expected.scoreValue);
  assert.equal(result.confidence.value, source.expected.confidenceValue);
  assert.equal(result.exclusions.find((item) => item.dimension === 'OPTICAL_IMAGE_QUALITY').reason, 'OPTIONAL_ZERO_WEIGHT_F3');
});

test('worse lower-is-better guiding decreases the score predictably', () => {
  const fixture = clone();
  fixture.dimensions.find((item) => item.dimension === 'GUIDING_STABILITY').value = 2.25;
  assert.equal(build(fixture).score.value, 67.86);
});

test('improved higher-is-better acquisition increases the score predictably', () => {
  const fixture = clone();
  fixture.dimensions.find((item) => item.dimension === 'ACQUISITION_COMPLETION').value = 1;
  assert.equal(build(fixture).score.value, 85.36);
});

test('all required dimensions preserve their declared monotonic direction', () => {
  const scenarios = [
    ['METADATA_LINEAGE_INTEGRITY', 0.5, 67.86],
    ['ACQUISITION_COMPLETION', 0.5, 70.36],
    ['GUIDING_STABILITY', 2.25, 67.86],
    ['SKY_QUALITY_COVERAGE', 19.8, 72.86]
  ];
  for (const [dimension, value, expected] of scenarios) {
    const fixture = clone();
    fixture.dimensions.find((item) => item.dimension === dimension).value = value;
    assert.equal(build(fixture).score.value, expected, dimension);
  }
});

test('evidence support changes confidence without changing scientific score', () => {
  const fixture = clone();
  fixture.dimensions.forEach((item) => { item.evidenceClass = 'OBSERVED'; });
  const result = build(fixture);
  assert.equal(result.score.value, source.expected.scoreValue);
  assert.equal(result.confidence.value, 92.5);
});

test('SUGGESTED required evidence makes the assessment unavailable', () => {
  const fixture = clone();
  fixture.dimensions[0].evidenceClass = 'SUGGESTED';
  const result = build(fixture);
  assert.equal(result.assessmentState, 'UNAVAILABLE');
  assert.equal(result.decomposition[0].exclusionReason, 'SUGGESTED_NOT_OBSERVED_OR_DECLARED');
});

test('incompatible units make the assessment unavailable', () => {
  const fixture = clone();
  fixture.dimensions.find((item) => item.dimension === 'SKY_QUALITY_COVERAGE').unit = 'lux';
  const result = build(fixture);
  assert.equal(result.assessmentState, 'UNAVAILABLE');
  assert.equal(result.decomposition.find((item) => item.dimension === 'SKY_QUALITY_COVERAGE').exclusionReason, 'UNIT_INCOMPATIBLE');
});

test('authority escalation is rejected', () => {
  const fixture = clone();
  fixture.authority.actionAuthority = 'DEVICE_COMMAND';
  assert.throws(() => build(fixture), /actionAuthority must be NONE/);
});

test('tampered profile identity fails closed', () => {
  const fixture = clone();
  fixture.profile.limitations[0] = 'Tampered but structurally valid limitation.';
  assert.throws(() => build(fixture), /profileDigest does not match canonical content/);
});

test('alternate profile identity is rejected even when correctly resealed', () => {
  const fixture = clone();
  fixture.profile.profileId = 'UNREVIEWED-PRODUCTION-PROFILE';
  resealProfile(fixture.profile);
  assert.throws(() => build(fixture), /Only the DSG-SCIENTIFIC-QUALITY-SYNTHETIC-DEMONSTRATOR profile is authorized/);
});

test('unknown properties are rejected fail-closed', () => {
  const fixture = clone();
  fixture.profile.legacyThreshold = 70;
  assert.throws(() => build(fixture), /legacyThreshold is not allowed/);
});
