import { canonicalJson, contentDigest } from './scientific-data-quality-contract.mjs';

export const F3_SCHEMA_VERSION = '1.0';
export const F3_ALGORITHM_ID = 'DSG-WEIGHTED-LINEAR-SCORE';
export const F3_ALGORITHM_VERSION = '1.0.0';

const PROFILE_KEYS = new Set(['profileId', 'profileVersion', 'profileState', 'algorithmId', 'algorithmVersion', 'scoreScale', 'confidenceMethod', 'dimensions', 'limitations', 'profileDigest']);
const SCALE_KEYS = new Set(['min', 'max', 'roundingDigits']);
const CONFIDENCE_KEYS = new Set(['methodId', 'methodVersion', 'semantic', 'evidenceClassFactors', 'qualityFactors', 'completenessFactors', 'calibrationFactors']);
const RULE_KEYS = new Set(['dimension', 'requirement', 'weight', 'unit', 'normalization']);
const NORMALIZATION_KEYS = new Set(['type', 'min', 'max', 'direction', 'outOfRangePolicy']);
const INPUT_KEYS = new Set(['dimension', 'value', 'unit', 'evidenceClass', 'quality', 'completeness', 'coverage', 'calibrationState', 'eligibility', 'evidenceRefs']);
const AUTHORITY_KEYS = new Set(['consumerMode', 'acceptanceAuthority', 'actionAuthority', 'safetyAuthority']);

const nonEmpty = (value) => typeof value === 'string' && value.trim().length > 0;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function exactKeys(value, allowed, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object.`);
  for (const key of Object.keys(value)) assert(allowed.has(key), `${label}.${key} is not allowed.`);
  for (const key of allowed) assert(Object.hasOwn(value, key), `${label}.${key} is required.`);
}

function stringArray(value, label, min = 0) {
  assert(Array.isArray(value) && value.length >= min, `${label} must contain at least ${min} item(s).`);
  assert(value.every(nonEmpty), `${label} must contain non-empty strings.`);
  assert(new Set(value).size === value.length, `${label} must not contain duplicates.`);
}

function finite(value, label) {
  assert(typeof value === 'number' && Number.isFinite(value), `${label} must be finite.`);
}

function round(value, digits) {
  const factor = 10 ** digits;
  return Math.round((value + Number.EPSILON) * factor) / factor;
}

function deepFreeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    Object.freeze(value);
    for (const child of Object.values(value)) deepFreeze(child);
  }
  return value;
}

function assertDigest(record, field, label) {
  assert(/^[a-f0-9]{64}$/.test(record[field] ?? ''), `${label}.${field} must be a SHA-256 digest.`);
  const copy = structuredClone(record);
  delete copy[field];
  assert(record[field] === contentDigest(copy), `${label}.${field} does not match canonical content.`);
}

function assertFactorMap(map, expected, label) {
  exactKeys(map, new Set(expected), label);
  for (const key of expected) {
    finite(map[key], `${label}.${key}`);
    assert(map[key] >= 0 && map[key] <= 1, `${label}.${key} must be within [0,1].`);
  }
}

export function validateScoringProfile(profile) {
  exactKeys(profile, PROFILE_KEYS, 'profile');
  for (const field of ['profileId', 'profileVersion', 'algorithmId', 'algorithmVersion']) assert(nonEmpty(profile[field]), `profile.${field} is required.`);
  assert(profile.profileState === 'SYNTHETIC_DEMONSTRATOR_F3', 'Only SYNTHETIC_DEMONSTRATOR_F3 profiles are authorized in F3.');
  assert(profile.algorithmId === F3_ALGORITHM_ID && profile.algorithmVersion === F3_ALGORITHM_VERSION, 'Unsupported scoring algorithm.');
  exactKeys(profile.scoreScale, SCALE_KEYS, 'profile.scoreScale');
  assert(profile.scoreScale.min === 0 && profile.scoreScale.max === 100, 'F3 score scale must be [0,100].');
  assert(Number.isInteger(profile.scoreScale.roundingDigits) && profile.scoreScale.roundingDigits >= 0 && profile.scoreScale.roundingDigits <= 6, 'Invalid score roundingDigits.');

  exactKeys(profile.confidenceMethod, CONFIDENCE_KEYS, 'profile.confidenceMethod');
  assert(profile.confidenceMethod.methodId === 'DSG-EVIDENCE-SUPPORT-PRODUCT', 'Unsupported confidence method.');
  assert(profile.confidenceMethod.methodVersion === '1.0.0', 'Unsupported confidence method version.');
  assert(profile.confidenceMethod.semantic === 'EVIDENCE_SUPPORT_NOT_PROBABILITY', 'Confidence semantic must remain non-probabilistic.');
  assertFactorMap(profile.confidenceMethod.evidenceClassFactors, ['OBSERVED', 'DECLARED', 'SUGGESTED'], 'profile.confidenceMethod.evidenceClassFactors');
  assertFactorMap(profile.confidenceMethod.qualityFactors, ['VALID', 'STALE', 'UNKNOWN', 'INVALID'], 'profile.confidenceMethod.qualityFactors');
  assertFactorMap(profile.confidenceMethod.completenessFactors, ['COMPLETE', 'PARTIAL', 'UNAVAILABLE'], 'profile.confidenceMethod.completenessFactors');
  assertFactorMap(profile.confidenceMethod.calibrationFactors, ['PROVEN', 'NOT_PROVEN', 'NOT_APPLICABLE', 'UNKNOWN'], 'profile.confidenceMethod.calibrationFactors');

  assert(Array.isArray(profile.dimensions) && profile.dimensions.length > 0, 'profile.dimensions is required.');
  const seen = new Set();
  let totalWeight = 0;
  for (const rule of profile.dimensions) {
    exactKeys(rule, RULE_KEYS, `profile.dimension.${rule?.dimension ?? 'unknown'}`);
    assert(nonEmpty(rule.dimension) && !seen.has(rule.dimension), 'Profile dimensions must be unique and named.');
    seen.add(rule.dimension);
    assert(['REQUIRED', 'OPTIONAL', 'CONTEXT_ONLY'].includes(rule.requirement), `Invalid requirement for ${rule.dimension}.`);
    finite(rule.weight, `profile.dimension.${rule.dimension}.weight`);
    assert(rule.weight >= 0 && rule.weight <= 1, `Weight for ${rule.dimension} must be within [0,1].`);
    if (rule.requirement === 'REQUIRED') {
      assert(rule.weight > 0, `Required dimension ${rule.dimension} must have positive weight.`);
      totalWeight += rule.weight;
    } else {
      assert(rule.weight === 0, `${rule.requirement} dimension ${rule.dimension} must have zero weight in F3.`);
    }
    assert(nonEmpty(rule.unit), `Unit is required for ${rule.dimension}.`);
    exactKeys(rule.normalization, NORMALIZATION_KEYS, `profile.dimension.${rule.dimension}.normalization`);
    assert(rule.normalization.type === 'LINEAR', `F3 supports only LINEAR normalization for ${rule.dimension}.`);
    finite(rule.normalization.min, `${rule.dimension}.normalization.min`);
    finite(rule.normalization.max, `${rule.dimension}.normalization.max`);
    assert(rule.normalization.max > rule.normalization.min, `Normalization bounds are invalid for ${rule.dimension}.`);
    assert(['HIGHER_IS_BETTER', 'LOWER_IS_BETTER'].includes(rule.normalization.direction), `Normalization direction is invalid for ${rule.dimension}.`);
    assert(rule.normalization.outOfRangePolicy === 'REJECT', `Out-of-range policy must be REJECT for ${rule.dimension}.`);
  }
  assert(Math.abs(totalWeight - 1) <= 1e-12, `Required dimension weights must sum to 1; received ${totalWeight}.`);
  stringArray(profile.limitations, 'profile.limitations', 1);
  assertDigest(profile, 'profileDigest', 'profile');
  return true;
}

function validateAuthority(authority) {
  exactKeys(authority, AUTHORITY_KEYS, 'authority');
  assert(authority.consumerMode === 'READ_ONLY', 'consumerMode must be READ_ONLY.');
  assert(authority.acceptanceAuthority === false, 'acceptanceAuthority must be false.');
  assert(authority.actionAuthority === 'NONE', 'actionAuthority must be NONE.');
  assert(authority.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'safetyAuthority must remain LOCAL_PHYSICAL_INTERLOCKS.');
}

function validateInput(input) {
  exactKeys(input, INPUT_KEYS, `input.${input?.dimension ?? 'unknown'}`);
  assert(nonEmpty(input.dimension), 'Input dimension is required.');
  finite(input.value, `input.${input.dimension}.value`);
  assert(nonEmpty(input.unit), `input.${input.dimension}.unit is required.`);
  assert(['OBSERVED', 'DECLARED', 'SUGGESTED'].includes(input.evidenceClass), `Invalid evidenceClass for ${input.dimension}.`);
  assert(['VALID', 'STALE', 'UNKNOWN', 'INVALID'].includes(input.quality), `Invalid quality for ${input.dimension}.`);
  assert(['COMPLETE', 'PARTIAL', 'UNAVAILABLE'].includes(input.completeness), `Invalid completeness for ${input.dimension}.`);
  finite(input.coverage, `input.${input.dimension}.coverage`);
  assert(input.coverage >= 0 && input.coverage <= 1, `Coverage for ${input.dimension} must be within [0,1].`);
  assert(['PROVEN', 'NOT_PROVEN', 'NOT_APPLICABLE', 'UNKNOWN'].includes(input.calibrationState), `Invalid calibrationState for ${input.dimension}.`);
  assert(['ELIGIBLE_FOR_FUTURE_NORMALIZATION', 'CONDITIONAL', 'CONTEXT_ONLY', 'UNAVAILABLE', 'INVALID'].includes(input.eligibility), `Invalid eligibility for ${input.dimension}.`);
  stringArray(input.evidenceRefs, `input.${input.dimension}.evidenceRefs`, 1);
}

function normalize(value, rule) {
  const { min, max, direction } = rule.normalization;
  assert(value >= min && value <= max, `${rule.dimension} value ${value} is outside [${min},${max}] and policy is REJECT.`);
  const ascending = (value - min) / (max - min);
  return direction === 'HIGHER_IS_BETTER' ? ascending : 1 - ascending;
}

function evidenceFactor(input, method) {
  return input.coverage
    * method.evidenceClassFactors[input.evidenceClass]
    * method.qualityFactors[input.quality]
    * method.completenessFactors[input.completeness]
    * method.calibrationFactors[input.calibrationState];
}

function ineligibilityReason(input, rule) {
  if (!input) {
    if (rule.requirement === 'REQUIRED') return 'REQUIRED_EVIDENCE_MISSING';
    if (rule.requirement === 'OPTIONAL') return 'OPTIONAL_EVIDENCE_MISSING';
    return 'CONTEXT_EVIDENCE_MISSING';
  }
  if (input.unit !== rule.unit) return 'UNIT_INCOMPATIBLE';
  if (input.eligibility !== 'ELIGIBLE_FOR_FUTURE_NORMALIZATION') return `ELIGIBILITY_${input.eligibility}`;
  if (input.evidenceClass === 'SUGGESTED') return 'SUGGESTED_NOT_OBSERVED_OR_DECLARED';
  if (input.quality !== 'VALID') return `QUALITY_${input.quality}`;
  if (input.completeness !== 'COMPLETE') return `COMPLETENESS_${input.completeness}`;
  if (!['PROVEN', 'NOT_APPLICABLE'].includes(input.calibrationState)) return `CALIBRATION_${input.calibrationState}`;
  return null;
}

export function buildScientificDataQualityAssessment({ profile, sessionId, dimensions = [], authority } = {}) {
  validateScoringProfile(profile);
  assert(nonEmpty(sessionId), 'sessionId is required.');
  validateAuthority(authority);
  assert(Array.isArray(dimensions), 'dimensions must be an array.');

  const inputByDimension = new Map();
  for (const input of dimensions) {
    validateInput(input);
    assert(!inputByDimension.has(input.dimension), `Duplicate input dimension ${input.dimension}.`);
    inputByDimension.set(input.dimension, structuredClone(input));
  }
  for (const dimension of inputByDimension.keys()) {
    assert(profile.dimensions.some((rule) => rule.dimension === dimension), `Input dimension ${dimension} is not declared by the profile.`);
  }

  const decomposition = [];
  const exclusions = [];
  let weightedScore = 0;
  let weightedConfidence = 0;
  let weightedCoverage = 0;
  let available = true;

  for (const rule of profile.dimensions) {
    const input = inputByDimension.get(rule.dimension);
    const exclusionReason = ineligibilityReason(input, rule);
    if (rule.requirement !== 'REQUIRED') {
      exclusions.push({ dimension: rule.dimension, requirement: rule.requirement, weight: 0, reason: exclusionReason ?? `${rule.requirement}_ZERO_WEIGHT_F3` });
      continue;
    }
    if (exclusionReason) {
      available = false;
      decomposition.push({ dimension: rule.dimension, state: 'UNAVAILABLE', rawValue: input?.value ?? null, unit: input?.unit ?? rule.unit, normalizedValue: null, weight: rule.weight, contribution: null, confidenceFactor: null, evidenceRefs: input?.evidenceRefs ?? [], exclusionReason });
      continue;
    }
    const normalizedValue = normalize(input.value, rule);
    const contribution = normalizedValue * rule.weight;
    const confidenceFactor = evidenceFactor(input, profile.confidenceMethod);
    weightedScore += contribution;
    weightedConfidence += confidenceFactor * rule.weight;
    weightedCoverage += input.coverage * rule.weight;
    decomposition.push({ dimension: rule.dimension, state: 'AVAILABLE', rawValue: input.value, unit: input.unit, normalizedValue: round(normalizedValue, 8), weight: rule.weight, contribution: round(contribution, 8), confidenceFactor: round(confidenceFactor, 8), evidenceRefs: [...input.evidenceRefs], exclusionReason: null });
  }

  const snapshot = [...inputByDimension.values()].sort((a, b) => a.dimension.localeCompare(b.dimension));
  const evidenceSnapshotDigest = contentDigest(snapshot);
  const assessmentId = `BKL041-F3-${contentDigest({ sessionId, profileDigest: profile.profileDigest, evidenceSnapshotDigest }).slice(0, 24)}`;
  const output = {
    schemaVersion: F3_SCHEMA_VERSION,
    assessmentType: 'SCIENTIFIC_DATA_QUALITY_ASSESSMENT',
    assessmentId,
    sessionId,
    profileId: profile.profileId,
    profileVersion: profile.profileVersion,
    profileDigest: profile.profileDigest,
    algorithmId: profile.algorithmId,
    algorithmVersion: profile.algorithmVersion,
    evidenceSnapshotDigest,
    assessmentState: available ? 'AVAILABLE' : 'UNAVAILABLE',
    score: available ? { value: round(weightedScore * 100, profile.scoreScale.roundingDigits), scaleMin: 0, scaleMax: 100, roundingDigits: profile.scoreScale.roundingDigits } : null,
    confidence: available ? { value: round(weightedConfidence * 100, profile.scoreScale.roundingDigits), scaleMin: 0, scaleMax: 100, semantic: profile.confidenceMethod.semantic } : null,
    evidenceCoverage: round(weightedCoverage, 8),
    decomposition,
    exclusions,
    limitations: [...profile.limitations, 'Synthetic demonstrator profile; not production scientific calibration or acceptance authority.'],
    authority: structuredClone(authority)
  };
  output.assessmentDigest = contentDigest(output);
  return deepFreeze(output);
}

export { canonicalJson, contentDigest };
