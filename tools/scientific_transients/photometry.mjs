// PROPOSED OFFLINE arithmetic, not provider semantics or an operating policy.
import {conditionalCovarianceSigma} from './covariance.mjs';
export const PHOTOMETRY = 'BKL051_PHOTOMETRIC_CALIBRATION_PROPOSED_V1';
const finite = v => typeof v === 'number' && Number.isFinite(v);
const known = v => v === null || finite(v);
const keys = (v, names) => v && typeof v === 'object' && !Array.isArray(v)
  && Object.keys(v).length === names.length && names.every(k => Object.hasOwn(v, k));
const fail = () => {throw new Error('INVALID_PHOTOMETRIC_CALIBRATION');};
const sha = v => typeof v === 'string' && /^[a-f0-9]{64}$/.test(v);
const vector = (v, n) => Array.isArray(v) && v.length === n
  && Array.from({length: n}, (_, i) => Object.hasOwn(v, i) && known(v[i])).every(Boolean);
export function inspectPhotometricCalibration(input) {
  if (!keys(input, ['kind', 'classification', 'origin', 'evidenceSha256', 'product', 'estimates', 'budget'])
      || input.kind !== PHOTOMETRY || input.classification !== 'PRIVATE'
      || !['SYNTHETIC_TEST', 'PRIVATE_MEASUREMENT_BUDGET'].includes(input.origin)
      || !sha(input.evidenceSha256)) fail();
  const p = input.product;
  if (!keys(p, ['measurement', 'uncertaintySemantics', 'colorDefinition', 'passbandCompatibility'])
      || !['INSTRUMENTAL_PSF_MAGNITUDE', 'ALREADY_CALIBRATED', 'APERTURE_UNCORRECTED', 'UNKNOWN'].includes(p.measurement)
      || !['VARIANCES_DECLARED', 'UNRESOLVED'].includes(p.uncertaintySemantics)
      || !(p.colorDefinition === null || typeof p.colorDefinition === 'string' && p.colorDefinition.trim().length > 0 && p.colorDefinition.length <= 80)
      || !['COMPATIBLE_DECLARED', 'UNKNOWN', 'INCOMPATIBLE'].includes(p.passbandCompatibility)) fail();
  const e = input.estimates;
  if (!keys(e, ['instrumentalMagnitude', 'zeroPoint', 'colorCoefficient', 'sourceColor'])
      || !Object.values(e).every(known)) fail();
  const b = input.budget;
  // Variances: [instrumental magnitude, zero point, color coefficient, source color].
  // Covariances: [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)].
  if (!keys(b, ['variances', 'covariances', 'omittedComponents'])
      || !vector(b.variances, 4)
      || b.variances.some(v => v !== null && v < 0)
      || !vector(b.covariances, 6)
      || !Array.isArray(b.omittedComponents) || b.omittedComponents.length < 1
      || b.omittedComponents.length > 6 || new Set(b.omittedComponents).size !== b.omittedComponents.length
      || !Array.from(b.omittedComponents).every(v => ['PSF_FIT', 'CALIBRATION_SYSTEMATICS', 'PASSBAND_RESPONSE', 'SOURCE_COLOR', 'MASTER_CALIBRATION', 'UNKNOWN'].includes(v))) fail();
  conditionalCovarianceSigma(b.variances, b.covariances, [0, 0, 0, 0], fail);
  const reasons = ['DECLARATIONS_NOT_INDEPENDENTLY_VERIFIED', 'FULL_UNCERTAINTY_NOT_VALIDATED'];
  if (input.origin === 'SYNTHETIC_TEST') reasons.push('SYNTHETIC_NOT_REAL_EVIDENCE');
  if (p.measurement !== 'INSTRUMENTAL_PSF_MAGNITUDE') reasons.push('PRODUCT_NOT_ELIGIBLE_FOR_THIS_CALIBRATION');
  if (p.uncertaintySemantics !== 'VARIANCES_DECLARED') reasons.push('CALIBRATION_UNCERTAINTY_SEMANTICS_UNRESOLVED');
  if (p.colorDefinition === null) reasons.push('COLOR_DEFINITION_UNKNOWN');
  if (p.passbandCompatibility !== 'COMPATIBLE_DECLARED') reasons.push('PASSBAND_NOT_COMPARABLE');
  if (Object.values(e).includes(null)) reasons.push('CALIBRATION_ESTIMATE_UNKNOWN');
  if (b.variances.includes(null)) reasons.push('UNKNOWN_VARIANCE_NOT_REPLACED_WITH_ZERO');
  if (b.covariances.includes(null)) reasons.push('UNKNOWN_COVARIANCE_NOT_REPLACED_WITH_ZERO');
  let magnitude = null, sigma = null;
  const eligible = p.measurement === 'INSTRUMENTAL_PSF_MAGNITUDE' && p.colorDefinition !== null
    && p.passbandCompatibility === 'COMPATIBLE_DECLARED' && !Object.values(e).includes(null);
  if (eligible) {
    magnitude = e.instrumentalMagnitude + e.zeroPoint + e.colorCoefficient * e.sourceColor;
    if (!finite(magnitude)) fail();
    if (p.uncertaintySemantics === 'VARIANCES_DECLARED') {
      sigma = conditionalCovarianceSigma(b.variances, b.covariances, [1, 1, e.sourceColor, e.colorCoefficient], fail);
      if (sigma === 0) reasons.push('DEGENERATE_CONDITIONAL_VARIANCE');
    }
  }
  return Object.freeze({kind: 'BKL051_PHOTOMETRIC_INSPECTION_PROPOSED_V1',
    conditionalMagnitude: magnitude, conditionalSigma: sigma, unit: 'MAG',
    propagation: 'FIRST_ORDER_DELTA_METHOD', arithmeticOnly: true,
    scientificValidation: 'NOT_VALIDATED', scientificClassification: 'NOT_EVALUATED',
    significance: null, nondetectionLimit: null, operatingPolicy: 'NOT_ACCEPTED_BY_THIS_INSPECTOR',
    externalRequests: 0, reviewRequired: true, reasons: Object.freeze(reasons),
    omittedComponents: Object.freeze([...b.omittedComponents])});
}
