import { createHash } from 'node:crypto';

export const SCHEMA_VERSION = '1.0';
export const CONTRACT_TYPE = 'SCIENTIFIC_DATA_QUALITY_F2_FIXTURE';
export const IDENTITY_METHOD = 'BKL041-F2-CANONICAL-JSON-SHA256-1';

export const DIMENSIONS = Object.freeze([
  'METADATA_LINEAGE_INTEGRITY',
  'ACQUISITION_COMPLETION',
  'GUIDING_STABILITY',
  'SKY_QUALITY_COVERAGE',
  'WEATHER_CONTEXT',
  'OPTICAL_IMAGE_QUALITY',
  'PROCESSING_PROVENANCE_COMPLETENESS',
  'ERROR_EVIDENCE',
  'FINAL_SCIENTIFIC_OUTCOME'
]);

const ASSESSMENT_STATES = new Set(['AVAILABLE', 'PARTIAL', 'UNAVAILABLE', 'NOT_APPLICABLE', 'INVALID']);
const ELIGIBILITY = new Set(['ELIGIBLE_FOR_FUTURE_NORMALIZATION', 'CONDITIONAL', 'CONTEXT_ONLY', 'UNAVAILABLE', 'INVALID']);
const EVIDENCE_CLASSES = new Set(['OBSERVED', 'DECLARED', 'SUGGESTED']);
const QUALITY = new Set(['VALID', 'STALE', 'UNKNOWN', 'INVALID']);
const COMPLETENESS = new Set(['COMPLETE', 'PARTIAL', 'UNAVAILABLE']);
const CALIBRATION = new Set(['PROVEN', 'NOT_PROVEN', 'NOT_APPLICABLE', 'UNKNOWN']);
const FORBIDDEN_KEYS = new Set(['score', 'scoreValue', 'scoreScale', 'weight', 'weights', 'normalizedValue', 'contribution', 'confidence']);

const present = (value) => value !== null && value !== undefined;
const nonEmpty = (value) => typeof value === 'string' && value.trim().length > 0;

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

export function contentDigest(value) {
  return createHash('sha256').update(canonicalJson(value), 'utf8').digest('hex');
}

export function withDigest(value, digestField) {
  const clone = structuredClone(value);
  delete clone[digestField];
  return Object.freeze({ ...clone, [digestField]: contentDigest(clone) });
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function assertStringArray(value, field, { min = 0 } = {}) {
  assert(Array.isArray(value), `${field} must be an array.`);
  assert(value.length >= min, `${field} must contain at least ${min} item(s).`);
  assert(value.every(nonEmpty), `${field} must contain non-empty strings.`);
  assert(new Set(value).size === value.length, `${field} must not contain duplicates.`);
}

function assertNoForbiddenFields(value, path = '$') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoForbiddenFields(item, `${path}[${index}]`));
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_KEYS.has(key), `${path}.${key} is forbidden in BKL-041 F2.`);
    assertNoForbiddenFields(child, `${path}.${key}`);
  }
}

function assertRepositoryRelative(sourceRef) {
  assert(nonEmpty(sourceRef), 'sourceRef is required.');
  assert(!sourceRef.startsWith('/') && !sourceRef.startsWith('\\\\'), 'sourceRef must be repository-relative.');
  assert(!/^[A-Za-z]:[\\/]/.test(sourceRef), 'sourceRef must not expose a local drive path.');
  assert(!sourceRef.split('/').includes('..'), 'sourceRef must not traverse outside the repository.');
}

function assertDigest(record, digestField, label) {
  assert(/^[a-f0-9]{64}$/.test(record[digestField] ?? ''), `${label} must carry a SHA-256 digest.`);
  const clone = structuredClone(record);
  delete clone[digestField];
  assert(record[digestField] === contentDigest(clone), `${label} digest does not match canonical content.`);
}

function validateProfile(profile) {
  assert(profile && typeof profile === 'object', 'assessmentProfile is required.');
  for (const field of ['profileId', 'profileVersion', 'intendedUse', 'eligibleCohort']) {
    assert(nonEmpty(profile[field]), `assessmentProfile.${field} is required.`);
  }
  assert(profile.profileState === 'DRAFT_F2', 'assessmentProfile.profileState must be DRAFT_F2.');
  for (const field of ['requiredDimensions', 'optionalDimensions', 'contextDimensions', 'excludedDimensions']) {
    assertStringArray(profile[field], `assessmentProfile.${field}`);
    assert(profile[field].every((dimension) => DIMENSIONS.includes(dimension)), `assessmentProfile.${field} contains an unsupported dimension.`);
  }
  const allDimensions = [...profile.requiredDimensions, ...profile.optionalDimensions, ...profile.contextDimensions, ...profile.excludedDimensions];
  assert(new Set(allDimensions).size === allDimensions.length, 'Profile dimension sets must be disjoint.');
  assert(profile.weightSetState === 'NOT_ASSIGNED_F2', 'Numeric weights are not authorized in F2.');
  assert(profile.scoreState === 'NOT_IMPLEMENTED_F2', 'Aggregated score is not authorized in F2.');
  assert(profile.confidenceMethodState === 'NOT_ASSIGNED_F2', 'Confidence computation is not authorized in F2.');
  assertStringArray(profile.minimumEvidenceRules, 'assessmentProfile.minimumEvidenceRules', { min: 1 });
  assertStringArray(profile.limitations, 'assessmentProfile.limitations', { min: 1 });
  assertDigest(profile, 'profileDigest', 'assessmentProfile');
}

function validateEvidence(evidence, sessionId) {
  for (const field of ['evidenceId', 'sessionId', 'dimension', 'methodId', 'methodVersion']) {
    assert(nonEmpty(evidence[field]), `qualityEvidence.${field} is required.`);
  }
  assert(evidence.sessionId === sessionId, `Evidence ${evidence.evidenceId} belongs to a different session.`);
  assert(DIMENSIONS.includes(evidence.dimension), `Evidence ${evidence.evidenceId} has an unsupported dimension.`);
  assert(EVIDENCE_CLASSES.has(evidence.evidenceClass), `Evidence ${evidence.evidenceId} has an invalid evidenceClass.`);
  assert(QUALITY.has(evidence.quality), `Evidence ${evidence.evidenceId} has an invalid quality.`);
  assert(COMPLETENESS.has(evidence.completeness), `Evidence ${evidence.evidenceId} has invalid completeness.`);
  assert(CALIBRATION.has(evidence.calibrationState), `Evidence ${evidence.evidenceId} has invalid calibrationState.`);
  assertRepositoryRelative(evidence.sourceRef);
  assert(evidence.value === null || ['number', 'string', 'boolean'].includes(typeof evidence.value), `Evidence ${evidence.evidenceId} has an unsupported value.`);
  assert(evidence.unit === null || nonEmpty(evidence.unit), `Evidence ${evidence.evidenceId} has an invalid unit.`);
  assert(evidence.coverage === null || (typeof evidence.coverage === 'number' && evidence.coverage >= 0 && evidence.coverage <= 1), `Evidence ${evidence.evidenceId} coverage must be null or within [0,1].`);
  assertStringArray(evidence.limitations, `qualityEvidence.${evidence.evidenceId}.limitations`);

  if (evidence.dimension === 'GUIDING_STABILITY' && present(evidence.value)) {
    assert(evidence.unit === 'arcsec', 'GUIDING_STABILITY requires unit arcsec.');
  }
  if (evidence.dimension === 'SKY_QUALITY_COVERAGE' && present(evidence.value)) {
    assert(evidence.unit === 'mag/arcsec2', 'SKY_QUALITY_COVERAGE requires unit mag/arcsec2.');
  }
  assertDigest(evidence, 'evidenceDigest', `qualityEvidence.${evidence.evidenceId}`);
}

function validateDimensionAssessment(assessment, evidenceById, profile) {
  assert(nonEmpty(assessment.dimension) && DIMENSIONS.includes(assessment.dimension), 'DimensionAssessment.dimension is invalid.');
  assert(ASSESSMENT_STATES.has(assessment.assessmentState), `Dimension ${assessment.dimension} has invalid assessmentState.`);
  assert(ELIGIBILITY.has(assessment.eligibility), `Dimension ${assessment.dimension} has invalid eligibility.`);
  assertStringArray(assessment.evidenceRefs, `dimensionAssessment.${assessment.dimension}.evidenceRefs`);
  assertStringArray(assessment.exclusionReasons, `dimensionAssessment.${assessment.dimension}.exclusionReasons`);
  assertStringArray(assessment.limitations, `dimensionAssessment.${assessment.dimension}.limitations`);
  assert(assessment.normalizationState === 'NOT_IMPLEMENTED_F2', 'Normalization is not authorized in F2.');
  assert(assessment.weightState === 'NOT_ASSIGNED_F2', 'Weights are not authorized in F2.');
  assert(assessment.contributionState === 'NOT_COMPUTED_F2', 'Dimension contribution is not authorized in F2.');

  const evidence = assessment.evidenceRefs.map((ref) => {
    assert(evidenceById.has(ref), `Dimension ${assessment.dimension} references unknown evidence ${ref}.`);
    return evidenceById.get(ref);
  });
  assert(evidence.every((item) => item.dimension === assessment.dimension), `Dimension ${assessment.dimension} references evidence from another dimension.`);

  const usable = evidence.filter((item) => item.value !== null && item.quality === 'VALID' && item.completeness === 'COMPLETE');
  if (profile.requiredDimensions.includes(assessment.dimension) && usable.length === 0) {
    assert(assessment.assessmentState === 'UNAVAILABLE' && assessment.eligibility === 'UNAVAILABLE', `Required dimension ${assessment.dimension} without usable evidence must be UNAVAILABLE.`);
    assert(assessment.exclusionReasons.includes('REQUIRED_EVIDENCE_MISSING'), `Required dimension ${assessment.dimension} must expose REQUIRED_EVIDENCE_MISSING.`);
  }
  if (assessment.dimension === 'WEATHER_CONTEXT' || assessment.dimension === 'ERROR_EVIDENCE') {
    assert(assessment.eligibility === 'CONTEXT_ONLY', `${assessment.dimension} must remain CONTEXT_ONLY in F2.`);
  }
  if (assessment.dimension === 'FINAL_SCIENTIFIC_OUTCOME') {
    assert(assessment.eligibility === 'UNAVAILABLE', 'FINAL_SCIENTIFIC_OUTCOME must remain UNAVAILABLE in F2.');
  }
  if (assessment.dimension === 'OPTICAL_IMAGE_QUALITY' && assessment.eligibility === 'ELIGIBLE_FOR_FUTURE_NORMALIZATION') {
    assert(usable.length > 0 && usable.every((item) => item.unit === 'arcsec' && item.unitSemantics === 'ANGULAR_CALIBRATED' && item.calibrationState === 'PROVEN'), 'Optical evidence is eligible only with proven angular calibration in arcsec.');
  }
  if (assessment.dimension === 'PROCESSING_PROVENANCE_COMPLETENESS' && assessment.eligibility === 'ELIGIBLE_FOR_FUTURE_NORMALIZATION') {
    assert(usable.length > 0, 'Processing provenance is eligible only when evidence is complete and valid.');
  }
  if (usable.some((item) => item.evidenceClass === 'SUGGESTED')) {
    assert(assessment.eligibility === 'CONTEXT_ONLY' || assessment.eligibility === 'UNAVAILABLE', 'SUGGESTED evidence cannot become eligible evidence.');
  }
  assertDigest(assessment, 'assessmentDigest', `dimensionAssessment.${assessment.dimension}`);
}

export function validateQualityContractFixture(fixture) {
  assert(fixture && typeof fixture === 'object' && !Array.isArray(fixture), 'Contract fixture must be an object.');
  assertNoForbiddenFields(fixture);
  assert(fixture.schemaVersion === SCHEMA_VERSION, `Unsupported schemaVersion ${fixture.schemaVersion}.`);
  assert(fixture.contractType === CONTRACT_TYPE, `Unsupported contractType ${fixture.contractType}.`);
  assert(fixture.identityMethod === IDENTITY_METHOD, `Unsupported identityMethod ${fixture.identityMethod}.`);
  assert(nonEmpty(fixture.fixtureId), 'fixtureId is required.');
  assert(nonEmpty(fixture.sessionId), 'sessionId is required.');
  assert(fixture.fixtureMode === 'BOUNDED_SYNTHETIC_FIXTURE', 'fixtureMode must be BOUNDED_SYNTHETIC_FIXTURE.');
  assert(fixture.authority?.consumerMode === 'READ_ONLY', 'consumerMode must be READ_ONLY.');
  assert(fixture.authority?.acceptanceAuthority === false, 'acceptanceAuthority must be false.');
  assert(fixture.authority?.actionAuthority === 'NONE', 'actionAuthority must be NONE.');
  assert(fixture.authority?.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'safetyAuthority must remain LOCAL_PHYSICAL_INTERLOCKS.');
  validateProfile(fixture.assessmentProfile);

  assert(Array.isArray(fixture.qualityEvidence), 'qualityEvidence must be an array.');
  const evidenceById = new Map();
  for (const evidence of fixture.qualityEvidence) {
    validateEvidence(evidence, fixture.sessionId);
    assert(!evidenceById.has(evidence.evidenceId), `Duplicate evidenceId ${evidence.evidenceId}.`);
    evidenceById.set(evidence.evidenceId, evidence);
  }

  assert(Array.isArray(fixture.dimensionAssessments), 'dimensionAssessments must be an array.');
  const dimensions = new Set();
  for (const assessment of fixture.dimensionAssessments) {
    assert(!dimensions.has(assessment.dimension), `Duplicate DimensionAssessment ${assessment.dimension}.`);
    dimensions.add(assessment.dimension);
    validateDimensionAssessment(assessment, evidenceById, fixture.assessmentProfile);
  }
  for (const dimension of fixture.assessmentProfile.requiredDimensions) {
    assert(dimensions.has(dimension), `Required dimension ${dimension} has no explicit assessment.`);
  }
  assertDigest(fixture, 'artifactDigest', 'fixture');
  return true;
}
