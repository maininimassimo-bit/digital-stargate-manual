// PROPOSED OFFLINE CONTRACT. Arithmetic on declarations; no scientific operating policy.
export const UNCERTAINTY = 'BKL051_PAIR_UNCERTAINTY_PROPOSED_V1';
const finite = v => typeof v === 'number' && Number.isFinite(v);
const knownNumber = v => v === null || finite(v);
const keys = (v, k) => v && typeof v === 'object' && !Array.isArray(v)
  && Object.keys(v).length === k.length && k.every(n => Object.hasOwn(v, n));
const sha = v => typeof v === 'string' && /^[a-f0-9]{64}$/.test(v);
const member = (v, k) => k.includes(v);
const fail = () => { throw new Error('INVALID_PAIR_UNCERTAINTY'); };
const vector = v => Array.isArray(v) && v.length === 3 && v.every(knownNumber);
const pairIndices = [[0, 1], [0, 2], [1, 2]];
const omissions = ['MASTER_CALIBRATION', 'RESAMPLING_COVARIANCE', 'SKY_ESTIMATOR', 'CROWDED_PSF', 'SCALE_ESTIMATION', 'PASSBAND_RESPONSE', 'UNKNOWN'];

function validateKnownCovariances(variances, covariances) {
  for (let k = 0; k < 3; k++) {
    const [i, j] = pairIndices[k], c = covariances[k];
    if (c === null) continue;
    if ((variances[i] === 0 || variances[j] === 0) && c !== 0) fail();
    if (variances[i] !== null && variances[j] !== null
        && Math.abs(c) > Math.sqrt(variances[i]) * Math.sqrt(variances[j])) fail();
  }
}
function conditionalSigma(variances, covariances, gradient) {
  if (variances.includes(null) || covariances.includes(null)) return null;
  // Factor a normalized covariance matrix, including singular cases.
  // This tolerance handles floating point rounding, not source acceptance.
  const tolerance = 64 * Number.EPSILON;
  const std = variances.map(Math.sqrt), corr = variances.map((v, i) => [0, 0, 0].map((_, j) => i === j && v > 0 ? 1 : 0));
  for (let k = 0; k < 3; k++) {
    const [i, j] = pairIndices[k];
    corr[i][j] = corr[j][i] = std[i] === 0 || std[j] === 0 ? 0 : covariances[k] / (std[i] * std[j]);
  }
  const lower = Array.from({length: 3}, () => [0, 0, 0]);
  for (let i = 0; i < 3; i++) for (let j = 0; j <= i; j++) {
    let residual = corr[i][j];
    for (let k = 0; k < j; k++) residual -= lower[i][k] * lower[j][k];
    if (i === j) {
      if (residual < -tolerance) fail();
      lower[i][j] = Math.sqrt(Math.max(0, residual));
    } else if (lower[j][j] === 0) {
      if (Math.abs(residual) > tolerance) fail();
    } else lower[i][j] = residual / lower[j][j];
  }
  const weights = gradient.map((g, i) => g * std[i]);
  if (!weights.every(finite)) fail();
  const transformed = [0, 1, 2].map(j => weights.reduce((sum, w, i) => sum + w * lower[i][j], 0));
  const sigma = Math.hypot(...transformed);
  if (!finite(sigma)) fail();
  return sigma;
}
export function inspectPairUncertainty(input) {
  if (!keys(input, ['kind', 'classification', 'origin', 'images', 'estimates', 'budget', 'comparability'])
      || input.kind !== UNCERTAINTY || input.classification !== 'PRIVATE'
      || !member(input.origin, ['SYNTHETIC_TEST', 'PRIVATE_MEASUREMENT_BUDGET'])
      || !Array.isArray(input.images) || input.images.length !== 2) fail();
  for (const i of input.images) if (!keys(i, ['sha256', 'imageIndex', 'unit']) || !sha(i.sha256)
    || !Number.isSafeInteger(i.imageIndex) || i.imageIndex < 0 || !member(i.unit, ['ADU', 'NORMALIZED_SAMPLE'])) fail();
  const e = input.estimates;
  if (!keys(e, ['leftFlux', 'rightFlux', 'rightToLeftScale']) || !knownNumber(e.leftFlux)
      || !knownNumber(e.rightFlux) || !knownNumber(e.rightToLeftScale)
      || (e.rightToLeftScale !== null && e.rightToLeftScale <= 0)) fail();
  const b = input.budget;
  if (!keys(b, ['variances', 'covariances', 'omittedComponents', 'skyIncludesReadNoise', 'readNoiseAddedSeparately', 'evidenceSha256'])
      || !vector(b.variances) || !vector(b.covariances) || b.variances.some(v => v !== null && v < 0)
      || !Array.isArray(b.omittedComponents) || b.omittedComponents.length < 1 || b.omittedComponents.length > omissions.length
      || new Set(b.omittedComponents).size !== b.omittedComponents.length || !b.omittedComponents.every(v => member(v, omissions))
      || !member(b.skyIncludesReadNoise, [true, false, null]) || !member(b.readNoiseAddedSeparately, [true, false, null])
      || !sha(b.evidenceSha256)) fail();
  if (b.skyIncludesReadNoise === true && b.readNoiseAddedSeparately === true) fail();
  const c = input.comparability;
  if (!keys(c, ['band', 'astrometry', 'psf', 'quality', 'epochs'])
      || !member(c.band, ['EQUIVALENT_DECLARED', 'INCOMPATIBLE', 'UNKNOWN'])
      || !member(c.astrometry, ['VERIFIED_DECLARED', 'UNKNOWN'])
      || !member(c.psf, ['COMPATIBLE_DECLARED', 'CROWDED_OR_UNVERIFIED'])
      || !member(c.quality, ['LOCAL_CHECKS_ONLY', 'SATURATED_OR_DEFECTIVE', 'UNKNOWN'])
      || !member(c.epochs, ['DISTINCT_EPOCHS_DECLARED', 'SAME_ACQUISITION', 'UNKNOWN'])) fail();
  validateKnownCovariances(b.variances, b.covariances);
  // A complete but impossible matrix is invalid even if flux/scale is unknown.
  if (!b.variances.includes(null) && !b.covariances.includes(null)) conditionalSigma(b.variances, b.covariances, [0, 0, 0]);
  const reasons = ['DECLARATIONS_NOT_INDEPENDENTLY_VERIFIED', 'FULL_UNCERTAINTY_NOT_VALIDATED', 'NO_BLIND_SEARCH_OR_INDEPENDENT_CONFIRMATION'];
  if (input.origin === 'SYNTHETIC_TEST') reasons.push('SYNTHETIC_NOT_REAL_EVIDENCE');
  if (b.variances.includes(null)) reasons.push('UNKNOWN_VARIANCE_NOT_REPLACED_WITH_ZERO');
  if (b.covariances.includes(null)) reasons.push('UNKNOWN_COVARIANCE_NOT_REPLACED_WITH_ZERO');
  if (b.skyIncludesReadNoise === null || b.readNoiseAddedSeparately === null) reasons.push('READ_NOISE_BOOKKEEPING_UNKNOWN');
  if (c.band !== 'EQUIVALENT_DECLARED') reasons.push('BAND_NOT_COMPARABLE');
  if (c.astrometry !== 'VERIFIED_DECLARED') reasons.push('ASTROMETRY_UNVERIFIED');
  if (c.psf !== 'COMPATIBLE_DECLARED') reasons.push('PSF_OR_CROWDING_UNVERIFIED');
  if (c.quality !== 'LOCAL_CHECKS_ONLY') reasons.push('QUALITY_BLOCKED_OR_UNKNOWN');
  if (c.epochs !== 'DISTINCT_EPOCHS_DECLARED') reasons.push('DISTINCT_EPOCHS_NOT_ESTABLISHED');
  if (input.images[0].sha256 === input.images[1].sha256 && input.images[0].imageIndex === input.images[1].imageIndex) reasons.push('SAME_IMAGE_NOT_INDEPENDENT');
  let difference = null, sigma = null;
  if ([e.leftFlux, e.rightFlux, e.rightToLeftScale].includes(null)) reasons.push('DIFFERENCE_INPUT_UNKNOWN');
  else {
    difference = e.leftFlux - e.rightToLeftScale * e.rightFlux;
    if (!finite(difference)) fail();
    sigma = conditionalSigma(b.variances, b.covariances, [1, -e.rightToLeftScale, -e.rightFlux]);
    if (sigma === 0) reasons.push('DEGENERATE_CONDITIONAL_VARIANCE_NOT_SIGNIFICANCE');
  }
  return Object.freeze({kind: 'BKL051_PAIR_UNCERTAINTY_INSPECTION_PROPOSED_V1',
    algebraicDifference: difference, leftUnitDeclared: input.images[0].unit, conditionalSigma: sigma,
    propagation: 'FIRST_ORDER_DELTA_METHOD', arithmeticOnly: true, scientificComparison: 'NOT_VALIDATED',
    scientificClassification: 'NOT_EVALUATED', operatingPolicy: 'NOT_ACCEPTED_BY_THIS_INSPECTOR',
    significance: null, nondetectionLimit: null, externalRequests: 0, reviewRequired: true,
    reasons: Object.freeze(reasons), omittedComponents: Object.freeze([...b.omittedComponents])});
}
