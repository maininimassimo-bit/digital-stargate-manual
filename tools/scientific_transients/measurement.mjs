// Proposed offline evidence inspection, not a detector or operational policy.
export const MEASUREMENT = 'BKL051_MEASUREMENT_EVIDENCE_PROPOSED_V1';
const keys = (v, expected) => v && typeof v === 'object' && !Array.isArray(v)
  && Object.keys(v).length === expected.length && expected.every(k => Object.hasOwn(v, k));
const finite = v => typeof v === 'number' && Number.isFinite(v);
const count = v => Number.isSafeInteger(v) && v >= 0;
const sha = v => typeof v === 'string' && /^[a-f0-9]{64}$/.test(v);
const maybeSha = v => v === null || sha(v);
const member = (v, allowed) => allowed.includes(v);
const fail = () => { throw new Error('INVALID_MEASUREMENT_EVIDENCE'); };
function utc(v) {
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(v)) return false;
  const d = new Date(v);
  return Number.isFinite(d.getTime()) && d.toISOString() === (v.includes('.') ? v : v.replace('Z', '.000Z'));
}
function detector(v) {
  return keys(v, ['sourceCount', 'nearestKnownPositionDistancePixels', 'receiptSha256']) && count(v.sourceCount)
    && sha(v.receiptSha256) && (v.sourceCount === 0 ? v.nearestKnownPositionDistancePixels === null
      : finite(v.nearestKnownPositionDistancePixels) && v.nearestKnownPositionDistancePixels >= 0);
}
export function inspectMeasurement(input) {
  if (!keys(input, ['kind', 'classification', 'origin', 'image', 'measurement', 'quality', 'detection'])
      || input.kind !== MEASUREMENT || input.classification !== 'PRIVATE'
      || !member(input.origin, ['OBSERVATORY', 'PUBLIC_KNOWN_EVENT_CONTROL', 'SYNTHETIC_TEST'])) fail();
  const image = input.image;
  if (!keys(image, ['sha256', 'imageIndex', 'width', 'height']) || !sha(image.sha256)
      || !count(image.imageIndex) || !count(image.width) || !count(image.height)
      || image.width === 0 || image.height === 0 || !Number.isSafeInteger(image.width * image.height)) fail();
  const m = input.measurement;
  if (!keys(m, ['method', 'band', 'acquisitionUtc', 'fluxADU', 'uncertaintyModel', 'evidenceSha256'])
      || m.method !== 'KNOWN_POSITION_FORCED_APERTURE'
      || typeof m.band !== 'string' || !/^[A-Za-z0-9_-]{1,96}$/.test(m.band)
      || !(m.acquisitionUtc === null || utc(m.acquisitionUtc))
      || !(m.fluxADU === null || finite(m.fluxADU))
      || !member(m.uncertaintyModel, ['CONDITIONAL_SKY_SOURCE_POISSON', 'PARTIAL', 'UNKNOWN'])
      || !sha(m.evidenceSha256)) fail();
  const q = input.quality;
  if (!keys(q, ['apertureDefectPixels', 'saturation', 'confusion', 'skyContamination', 'maskEvidenceSha256'])
      || !count(q.apertureDefectPixels) || q.apertureDefectPixels > image.width * image.height
      || !member(q.saturation, ['CONFIRMED', 'NOT_DETECTED', 'UNKNOWN'])
      || !member(q.confusion, ['MULTIPLE_MAXIMA_DIAGNOSTIC', 'NOT_ESTABLISHED'])
      || !member(q.skyContamination, ['KNOWN_OR_POSSIBLE', 'NOT_ESTABLISHED']) || !maybeSha(q.maskEvidenceSha256)) fail();
  const d = input.detection;
  if (!keys(d, ['knownCoordinateUsed', 'baseline', 'allowClusteredSources']) || d.knownCoordinateUsed !== true
      || !detector(d.baseline) || !detector(d.allowClusteredSources)) fail();

  const reasons = ['KNOWN_POSITION_CONTROL_NOT_BLIND_SEARCH', 'FULL_UNCERTAINTY_NOT_VALIDATED',
    'ASTROMETRY_AND_BAND_COMPARABILITY_NOT_ATTESTED_BY_THIS_INSPECTOR', 'INDEPENDENT_CONFIRMATION_NOT_ATTESTED'];
  if (input.origin === 'SYNTHETIC_TEST') reasons.push('SYNTHETIC_NOT_REAL_EVIDENCE');
  if (m.acquisitionUtc === null) reasons.push('ACQUISITION_EPOCH_UNKNOWN');
  if (m.fluxADU === null) reasons.push('FLUX_NOT_MEASURED');
  else if (m.fluxADU <= 0) reasons.push('NONPOSITIVE_FLUX_IS_NOT_A_NONDETECTION_LIMIT');
  if (q.apertureDefectPixels > 0) reasons.push('DEFECTIVE_APERTURE');
  if (q.saturation === 'CONFIRMED') reasons.push('SATURATED_MEASUREMENT');
  else if (q.saturation === 'UNKNOWN') reasons.push('SATURATION_UNKNOWN');
  if (q.maskEvidenceSha256 === null) reasons.push('MASK_EVIDENCE_MISSING');
  reasons.push(q.confusion === 'MULTIPLE_MAXIMA_DIAGNOSTIC' ? 'CROWDED_SOURCE_REQUIRES_SEPARATE_MEASUREMENT' : 'SOURCE_ISOLATION_NOT_ESTABLISHED');
  reasons.push(q.skyContamination === 'KNOWN_OR_POSSIBLE' ? 'SKY_OR_HOST_CONTAMINATION' : 'SKY_CONTAMINATION_NOT_ESTABLISHED');
  const rejected = q.apertureDefectPixels > 0 || q.saturation === 'CONFIRMED';
  return Object.freeze({kind: 'BKL051_MEASUREMENT_INSPECTION_PROPOSED_V1', state: 'NO_NEW_ANALYSIS_EXECUTED',
    measurementUse: rejected ? 'REJECTED_BY_REPORTED_LOCAL_QUALITY' : 'EXPLORATORY_NOT_VALIDATED',
    scientificClassification: 'NOT_EVALUATED', reviewRequired: true, operatingPolicy: 'NOT_ACCEPTED_BY_THIS_INSPECTOR',
    numericAssociationThreshold: null, nondetectionLimit: null, falsePositiveRate: null,
    externalRequests: 0, declarationsIndependentlyVerified: false, reasons: Object.freeze(reasons)});
}
