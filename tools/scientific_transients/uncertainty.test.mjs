import test from 'node:test';
import assert from 'node:assert/strict';
import {UNCERTAINTY, inspectPairUncertainty} from './uncertainty.mjs';
const sha = x => x.repeat(64);
function fixture() {
  return {kind: UNCERTAINTY, classification: 'PRIVATE', origin: 'SYNTHETIC_TEST',
    images: [{sha256: sha('a'), imageIndex: 0, unit: 'ADU'}, {sha256: sha('b'), imageIndex: 0, unit: 'ADU'}],
    estimates: {leftFlux: 100, rightFlux: 40, rightToLeftScale: 2},
    budget: {variances: [9, 16, 0], covariances: [6, 0, 0], omittedComponents: ['UNKNOWN'],
      skyIncludesReadNoise: true, readNoiseAddedSeparately: false, evidenceSha256: sha('c')},
    comparability: {band: 'EQUIVALENT_DECLARED', astrometry: 'VERIFIED_DECLARED', psf: 'COMPATIBLE_DECLARED', quality: 'LOCAL_CHECKS_ONLY', epochs: 'DISTINCT_EPOCHS_DECLARED'}};
}
const close = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-10 * Math.max(1, Math.abs(expected)), `${actual} != ${expected}`);
test('known covariance changes first-order variance; no scientific significance manufactured', () => {
  const r = inspectPairUncertainty(fixture()); close(r.algebraicDifference, 20); close(r.conditionalSigma, 7);
  assert.equal(r.significance, null); assert.equal(r.scientificClassification, 'NOT_EVALUATED'); assert.equal(r.scientificComparison, 'NOT_VALIDATED');
  const f = fixture(); f.budget.covariances[0] = 0; close(inspectPairUncertainty(f).conditionalSigma, Math.sqrt(73));
});
test('scale-estimation correlations enter with correct gradient signs', () => {
  const f = fixture(); f.estimates = {leftFlux: 20, rightFlux: 10, rightToLeftScale: 2};
  f.budget.variances = [4, 9, 0.01]; f.budget.covariances = [1, 0.1, 0.2];
  close(inspectPairUncertainty(f).conditionalSigma, Math.sqrt(43));
});
test('unknown covariance never silently assumes independence', () => {
  const f = fixture(); f.budget.covariances[0] = null;
  const r = inspectPairUncertainty(f); assert.equal(r.conditionalSigma, null); assert.equal(r.algebraicDifference, 20);
  assert.ok(r.reasons.includes('UNKNOWN_COVARIANCE_NOT_REPLACED_WITH_ZERO'));
});
test('unknown variance or scale produces explicitly incomplete arithmetic', () => {
  const f = fixture(); f.budget.variances[2] = null; assert.equal(inspectPairUncertainty(f).conditionalSigma, null);
  f.estimates.rightToLeftScale = null; assert.equal(inspectPairUncertainty(f).algebraicDifference, null);
});
test('negative measured flux remains signed and never becomes a nondetection limit', () => {
  const f = fixture(); f.estimates.leftFlux = -4; close(inspectPairUncertainty(f).algebraicDifference, -84);
  assert.equal(inspectPairUncertainty(f).nondetectionLimit, null);
});
test('same-image singular covariance yields zero conditional variance, never infinite significance', () => {
  const f = fixture(); f.images[1] = {...f.images[0]}; f.estimates.rightToLeftScale = 1;
  f.budget.variances = [4, 4, 0]; f.budget.covariances = [4, 0, 0];
  const r = inspectPairUncertainty(f); close(r.conditionalSigma, 0); assert.equal(r.significance, null);
  assert.ok(r.reasons.includes('SAME_IMAGE_NOT_INDEPENDENT'));
});
test('anti-correlated errors increase difference variance', () => {
  const f = fixture(); f.estimates.rightToLeftScale = 1; f.budget.variances = [4, 4, 0]; f.budget.covariances = [-4, 0, 0];
  close(inspectPairUncertainty(f).conditionalSigma, 4);
});
test('non-PSD covariance is rejected even when every pair passes Cauchy bound', () => {
  const f = fixture(); f.budget.variances = [1, 1, 1]; f.budget.covariances = [0.9, 0.9, -0.9];
  assert.throws(() => inspectPairUncertainty(f), /INVALID_PAIR_UNCERTAINTY/);
});
test('known covariance violates zero variance or Cauchy bound even in partial budget', () => {
  for (const covariance of [13, -13]) {const f = fixture(); f.budget.covariances[0] = covariance; assert.throws(() => inspectPairUncertainty(f), /INVALID_PAIR_UNCERTAINTY/);}
  const f = fixture(); f.budget.variances = [0, null, null]; f.budget.covariances = [1, null, null];
  assert.throws(() => inspectPairUncertainty(f), /INVALID_PAIR_UNCERTAINTY/);
});
test('read noise cannot be added again when already included in background variance', () => {
  const f = fixture(); f.budget.readNoiseAddedSeparately = true;
  assert.throws(() => inspectPairUncertainty(f), /INVALID_PAIR_UNCERTAINTY/);
});
test('impossible complete covariance still rejects when estimates are unknown', () => {
  const f = fixture(); f.estimates.leftFlux = null;
  f.budget.variances = [1, 1, 1]; f.budget.covariances = [0.9, 0.9, -0.9];
  assert.throws(() => inspectPairUncertainty(f), /INVALID_PAIR_UNCERTAINTY/);
});
test('palette/incompatible band, crowded PSF and saturation remain reasons for no valid comparison', () => {
  const f = fixture(); f.comparability.band = 'INCOMPATIBLE'; f.comparability.psf = 'CROWDED_OR_UNVERIFIED'; f.comparability.quality = 'SATURATED_OR_DEFECTIVE';
  const r = inspectPairUncertainty(f); assert.equal(r.scientificComparison, 'NOT_VALIDATED');
  for (const reason of ['BAND_NOT_COMPARABLE', 'PSF_OR_CROWDING_UNVERIFIED', 'QUALITY_BLOCKED_OR_UNKNOWN']) assert.ok(r.reasons.includes(reason));
});
test('nonfinite values, numeric overflow, false full-model claims and consent/threshold additions reject', () => {
  for (const mutate of [f => f.estimates.leftFlux = Infinity, f => f.budget.variances[0] = NaN,
    f => f.budget.variances[1] = -1, f => f.estimates.rightToLeftScale = 0,
    f => f.estimates.rightToLeftScale = 1e308, f => f.budget.omittedComponents = [],
    f => f.ownerApproved = true, f => f.threshold = 5]) {
    const f = fixture(); mutate(f); assert.throws(() => inspectPairUncertainty(f), /INVALID_PAIR_UNCERTAINTY/);
  }
});
