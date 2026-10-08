import test from 'node:test';
import assert from 'node:assert/strict';
import {MEASUREMENT, inspectMeasurement} from './measurement.mjs';
const sha = c => c.repeat(64);
function fixture() {
  return {kind: MEASUREMENT, classification: 'PRIVATE', origin: 'SYNTHETIC_TEST',
    image: {sha256: sha('a'), imageIndex: 0, width: 600, height: 400},
    measurement: {method: 'KNOWN_POSITION_FORCED_APERTURE', band: 'TEST_R', acquisitionUtc: '2026-01-01T00:00:00.123Z',
      fluxADU: 1234, uncertaintyModel: 'CONDITIONAL_SKY_SOURCE_POISSON', evidenceSha256: sha('b')},
    quality: {apertureDefectPixels: 0, saturation: 'NOT_DETECTED', confusion: 'NOT_ESTABLISHED',
      skyContamination: 'NOT_ESTABLISHED', maskEvidenceSha256: sha('c')},
    detection: {knownCoordinateUsed: true, baseline: {sourceCount: 100, nearestKnownPositionDistancePixels: 20, receiptSha256: sha('d')},
      allowClusteredSources: {sourceCount: 120, nearestKnownPositionDistancePixels: 0.05, receiptSha256: sha('e')}}};
}
test('nearby detection and complete declarations never create a transient or acceptance', () => {
  const r = inspectMeasurement(fixture());
  assert.equal(r.scientificClassification, 'NOT_EVALUATED');
  assert.equal(r.operatingPolicy, 'NOT_ACCEPTED_BY_THIS_INSPECTOR');
  assert.equal(r.measurementUse, 'EXPLORATORY_NOT_VALIDATED');
  assert.equal(r.numericAssociationThreshold, null); assert.equal(r.falsePositiveRate, null);
  assert.equal(r.externalRequests, 0); assert.equal(r.declarationsIndependentlyVerified, false);
  assert.ok(r.reasons.includes('SYNTHETIC_NOT_REAL_EVIDENCE'));
});
test('saturated detection is rejected even with a very close centroid', () => {
  const f = fixture(); f.quality.saturation = 'CONFIRMED';
  const r = inspectMeasurement(f); assert.equal(r.measurementUse, 'REJECTED_BY_REPORTED_LOCAL_QUALITY');
  assert.ok(r.reasons.includes('SATURATED_MEASUREMENT'));
});
test('defective aperture rejected separately from saturation', () => {
  const f = fixture(); f.quality.apertureDefectPixels = 1;
  assert.equal(inspectMeasurement(f).measurementUse, 'REJECTED_BY_REPORTED_LOCAL_QUALITY');
});
test('crowding diagnostic requires measurement review without accepting deblending', () => {
  const f = fixture(); f.origin = 'PUBLIC_KNOWN_EVENT_CONTROL'; f.quality.confusion = 'MULTIPLE_MAXIMA_DIAGNOSTIC';
  const r = inspectMeasurement(f);
  assert.ok(r.reasons.includes('CROWDED_SOURCE_REQUIRES_SEPARATE_MEASUREMENT'));
  assert.equal(r.reviewRequired, true); assert.equal(r.scientificClassification, 'NOT_EVALUATED');
});
test('missing and nonpositive flux retain unknown limit instead of claiming absence', () => {
  for (const flux of [null, 0, -42]) {
    const f = fixture(); f.measurement.fluxADU = flux; f.detection.baseline = {sourceCount: 0, nearestKnownPositionDistancePixels: null, receiptSha256: sha('d')};
    const r = inspectMeasurement(f); assert.equal(r.nondetectionLimit, null); assert.equal(r.scientificClassification, 'NOT_EVALUATED');
    assert.ok(r.reasons.includes(flux === null ? 'FLUX_NOT_MEASURED' : 'NONPOSITIVE_FLUX_IS_NOT_A_NONDETECTION_LIMIT'));
  }
});
test('unknown epoch, masks, saturation and contaminated sky remain explicit', () => {
  const f = fixture(); f.measurement.acquisitionUtc = null; f.quality.maskEvidenceSha256 = null;
  f.quality.saturation = 'UNKNOWN'; f.quality.skyContamination = 'KNOWN_OR_POSSIBLE';
  const r = inspectMeasurement(f);
  for (const c of ['ACQUISITION_EPOCH_UNKNOWN', 'MASK_EVIDENCE_MISSING', 'SATURATION_UNKNOWN', 'SKY_OR_HOST_CONTAMINATION']) assert.ok(r.reasons.includes(c));
});
test('unsafe numbers, geometry, wrong quality enums and impossible detector counts reject', () => {
  for (const mutate of [f => f.measurement.fluxADU = NaN, f => f.measurement.fluxADU = Infinity,
    f => f.image.width = 0, f => f.image.imageIndex = -1, f => f.quality.apertureDefectPixels = 240001,
    f => f.detection.baseline.sourceCount = 0, f => f.detection.baseline.nearestKnownPositionDistancePixels = null,
    f => f.quality.saturation = 'CERTIFIED_GOOD', f => f.measurement.uncertaintyModel = 'FULLY_VALIDATED']) {
    const f = fixture(); mutate(f); assert.throws(() => inspectMeasurement(f), /INVALID_MEASUREMENT_EVIDENCE/);
  }
});
test('invalid calendar dates and invented times reject', () => {
  for (const v of ['2026-02-30T00:00:00Z', '2026-01-01', '2026-01-01T00:00:00+01:00']) {
    const f = fixture(); f.measurement.acquisitionUtc = v; assert.throws(() => inspectMeasurement(f), /INVALID_MEASUREMENT_EVIDENCE/);
  }
});
test('closed proposed schema rejects paths, endpoints, consent and blind-search claims', () => {
  for (const k of ['localPath', 'endpoint', 'ownerApproved', 'threshold', 'candidateClassification']) {
    const f = fixture(); f[k] = 'UNAUTHORIZED'; assert.throws(() => inspectMeasurement(f), /INVALID_MEASUREMENT_EVIDENCE/);
  }
  const f = fixture(); f.detection.knownCoordinateUsed = false; assert.throws(() => inspectMeasurement(f), /INVALID_MEASUREMENT_EVIDENCE/);
});
