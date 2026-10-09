import test from 'node:test';
import assert from 'node:assert/strict';
import {PHOTOMETRY, inspectPhotometricCalibration} from './photometry.mjs';
const close = (a, b) => assert.ok(Math.abs(a - b) < 1e-11 * Math.max(1, Math.abs(b)), `${a} != ${b}`);
function fixture() {
  return {kind: PHOTOMETRY, classification: 'PRIVATE', origin: 'SYNTHETIC_TEST', evidenceSha256: 'a'.repeat(64),
    product: {measurement: 'INSTRUMENTAL_PSF_MAGNITUDE', uncertaintySemantics: 'VARIANCES_DECLARED', colorDefinition: 'g-r', passbandCompatibility: 'COMPATIBLE_DECLARED'},
    estimates: {instrumentalMagnitude: -8, zeroPoint: 25, colorCoefficient: 0.1, sourceColor: 0.5},
    budget: {variances: [0.01, 0.04, 0.0025, 0.09], covariances: [0, 0, 0, 0, 0, 0], omittedComponents: ['CALIBRATION_SYSTEMATICS']}};
}
test('explicit source color enters magnitude and all four variance sensitivities', () => {
  const r = inspectPhotometricCalibration(fixture()); close(r.conditionalMagnitude, 17.05); close(r.conditionalSigma, Math.sqrt(0.051525));
  assert.equal(r.significance, null); assert.equal(r.scientificValidation, 'NOT_VALIDATED');
  assert.equal(r.operatingPolicy, 'NOT_ACCEPTED_BY_THIS_INSPECTOR'); assert.ok(Object.isFrozen(r));
});
test('zero-point / color-coefficient covariance contributes with its sign', () => {
  for (const sign of [-1, 1]) {
    const f = fixture(); f.budget.covariances[3] = sign * 0.005;
    close(inspectPhotometricCalibration(f).conditionalSigma, Math.sqrt(0.051525 + sign * 0.005));
  }
});
test('all six cross terms use the declared ordering and gradients', () => {
  const f = fixture(); f.budget.variances = [1, 1, 1, 1];
  f.budget.covariances = [0.1, 0.2, 0.1, 0.15, 0.1, 0.2];
  close(inspectPhotometricCalibration(f).conditionalSigma, Math.sqrt(2.87));
});
test('unknown source color stays unknown; no flat-spectrum default', () => {
  const f = fixture(); f.estimates.sourceColor = null;
  const r = inspectPhotometricCalibration(f); assert.equal(r.conditionalMagnitude, null); assert.equal(r.conditionalSigma, null);
});
test('zero coefficient does not manufacture a missing source color', () => {
  const f = fixture(); f.estimates.colorCoefficient = 0; f.estimates.sourceColor = null;
  assert.equal(inspectPhotometricCalibration(f).conditionalMagnitude, null);
});
test('unresolved provider semantics blocks sigma even with numerical declarations', () => {
  const f = fixture(); f.product.uncertaintySemantics = 'UNRESOLVED';
  const r = inspectPhotometricCalibration(f); assert.equal(r.conditionalSigma, null);
  assert.ok(r.reasons.includes('CALIBRATION_UNCERTAINTY_SEMANTICS_UNRESOLVED'));
});
test('missing variance or covariance never silently becomes zero', () => {
  for (const name of ['variances', 'covariances']) {
    const f = fixture(); f.budget[name][0] = null;
    assert.equal(inspectPhotometricCalibration(f).conditionalSigma, null);
  }
});
test('already-calibrated, aperture-uncorrected and unknown products do not receive PSF zero point', () => {
  for (const measurement of ['ALREADY_CALIBRATED', 'APERTURE_UNCORRECTED', 'UNKNOWN']) {
    const f = fixture(); f.product.measurement = measurement;
    const r = inspectPhotometricCalibration(f); assert.equal(r.conditionalMagnitude, null); assert.equal(r.conditionalSigma, null);
  }
});
test('missing color definition and incompatible passband block conditional calibration', () => {
  for (const change of [f => f.product.colorDefinition = null, f => f.product.passbandCompatibility = 'INCOMPATIBLE']) {
    const f = fixture(); change(f); assert.equal(inspectPhotometricCalibration(f).conditionalMagnitude, null);
  }
});
test('non-PSD complete declarations reject even with unknown estimates', () => {
  const f = fixture(); f.estimates.sourceColor = null; f.budget.variances = [1, 1, 1, 1];
  f.budget.covariances = [0.9, 0.9, 0, -0.9, 0, 0];
  assert.throws(() => inspectPhotometricCalibration(f), /INVALID_PHOTOMETRIC_CALIBRATION/);
});
test('partial budget still rejects impossible known covariance and zero-variance correlation', () => {
  for (const variance of [0, 0.01]) {
    const f = fixture(); f.budget.variances = [variance, 0.04, null, null]; f.budget.covariances = [1, null, null, null, null, null];
    assert.throws(() => inspectPhotometricCalibration(f), /INVALID_PHOTOMETRIC_CALIBRATION/);
  }
  const f = fixture(); f.budget.omittedComponents = Array(1);
  assert.throws(() => inspectPhotometricCalibration(f), /INVALID_PHOTOMETRIC_CALIBRATION/);
});
test('singular zero budget is arithmetic only and has no infinite significance', () => {
  const f = fixture(); f.budget.variances = [0, 0, 0, 0];
  const r = inspectPhotometricCalibration(f); assert.equal(r.conditionalSigma, 0); assert.equal(r.significance, null);
});
test('negative source color and coefficient preserve signs', () => {
  const f = fixture(); f.estimates.sourceColor = -0.5; f.estimates.colorCoefficient = -0.1;
  close(inspectPhotometricCalibration(f).conditionalMagnitude, 17.05);
});
test('rank-one covariance preserves cancellations in a singular four-variable budget', () => {
  const f = fixture(); f.budget.variances = [1, 1, 1, 1];
  f.budget.covariances = [-1, 1, -1, -1, 1, -1];
  close(inspectPhotometricCalibration(f).conditionalSigma, 0.4);
});
test('sparse vectors are not unknown values or complete budgets', () => {
  for (const name of ['variances', 'covariances']) {
    const f = fixture(); delete f.budget[name][0];
    assert.throws(() => inspectPhotometricCalibration(f), /INVALID_PHOTOMETRIC_CALIBRATION/);
  }
});
test('overflow, nonfinite data, unqualified full budgets and operational additions reject', () => {
  for (const change of [f => f.estimates.sourceColor = NaN, f => f.budget.variances[0] = -1,
    f => {f.estimates.sourceColor = 1e308; f.estimates.colorCoefficient = 1e308;}, f => f.budget.omittedComponents = [],
    f => f.threshold = 5, f => f.ownerApproved = true, f => f.product.uncertaintySemantics = 'STANDARD_DEVIATIONS']) {
    const f = fixture(); change(f);
    assert.throws(() => inspectPhotometricCalibration(f), /INVALID_PHOTOMETRIC_CALIBRATION/);
  }
});
