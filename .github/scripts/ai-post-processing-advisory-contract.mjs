import { createHash } from 'node:crypto';

export const SCHEMA_VERSION = '1.0';
export const CONTRACT_TYPE = 'AI_POST_PROCESSING_ASSISTANT_F2_FIXTURE';
export const IDENTITY_METHOD = 'BKL046-F2-CANONICAL-JSON-SHA256-1';

const ROOT_KEYS = new Set(['schemaVersion', 'contractType', 'identityMethod', 'fixtureId', 'fixtureMode', 'generatedAt', 'subject', 'sourceBindings', 'recommendations', 'humanDecisionReceipts', 'authority', 'limitations', 'artifactDigest']);
const SUBJECT_KEYS = new Set(['subjectId', 'subjectType', 'assetRef', 'sessionRef', 'workflowRef', 'stepRef', 'correlationState']);
const SOURCE_KEYS = new Set(['bindingId', 'semanticType', 'evidenceClass', 'sourceAuthority', 'sourceRef', 'lifecycleState', 'quality', 'completeness', 'citationRefs', 'limitations', 'bindingDigest']);
const RECOMMENDATION_KEYS = new Set(['recommendationId', 'semanticType', 'aiDerived', 'producer', 'producerVersion', 'methodId', 'generatedAt', 'correlationId', 'subjectRef', 'category', 'lifecycleState', 'proposedAction', 'rationale', 'sourceBindingRefs', 'citationRefs', 'provenanceRefs', 'parameterAdvice', 'conflicts', 'unknowns', 'confidence', 'limitations', 'recommendationDigest']);
const CONFIDENCE_KEYS = new Set(['state', 'contractRef', 'value', 'limitations']);
const PARAMETER_KEYS = new Set(['parameterId', 'mode', 'unit', 'categoricalValue', 'lowerBound', 'upperBound', 'applicability', 'evidenceRefs', 'limitations']);
const RECEIPT_KEYS = new Set(['receiptId', 'recommendationId', 'presentedAt', 'decidedAt', 'actorRef', 'disposition', 'decisionEdits', 'decisionRationale', 'correlationId', 'executionState', 'executionEvidenceRefs', 'actionAuthority', 'receiptDigest']);
const EDIT_KEYS = new Set(['parameterId', 'selectedValue', 'unit', 'reason']);
const AUTHORITY_KEYS = new Set(['consumerMode', 'advisoryOnly', 'acceptanceAuthority', 'actionAuthority', 'executionAuthority', 'safetyAuthority', 'pixInsightApplyAuthorized', 'automaticAcceptanceAuthorized']);

const SUBJECT_TYPES = new Set(['SCIENTIFIC_ASSET', 'PIXINSIGHT_WORKFLOW', 'PIXINSIGHT_PROCESS_STEP']);
const CORRELATION_STATES = new Set(['RESOLVED', 'PARTIAL', 'UNRESOLVED']);
const SEMANTIC_TYPES = new Set(['observation', 'evidence', 'claim', 'recommendation']);
const EVIDENCE_CLASSES = new Set(['OBSERVED', 'DECLARED', 'SUGGESTED']);
const SOURCE_AUTHORITIES = new Set(['repository_authority', 'scientific_catalog', 'analytics_product', 'session_projection', 'processing_evidence', 'projection', 'unknown']);
const LIFECYCLES = new Set(['incomplete', 'unknown', 'draft', 'validated', 'superseded', 'rejected']);
const QUALITY = new Set(['VALID', 'STALE', 'UNKNOWN', 'INVALID']);
const COMPLETENESS = new Set(['COMPLETE', 'PARTIAL', 'UNAVAILABLE']);
const CATEGORIES = new Set(['PROCESS_ORDER', 'PARAMETER_RANGE', 'QUALITY_CHECK', 'WORKFLOW_ALTERNATIVE', 'STOP_AND_REVIEW']);
const PARAMETER_MODES = new Set(['CATEGORICAL', 'BOUNDED_INTERVAL', 'UNKNOWN_NOT_RECOMMENDED']);
const DISPOSITIONS = new Set(['ACCEPTED_FOR_MANUAL_APPLICATION', 'EDITED_FOR_MANUAL_APPLICATION', 'REJECTED', 'DEFERRED']);
const FORBIDDEN_KEYS = new Set(['command', 'script', 'applyPath', 'execute', 'autoAccept', 'deviceCommand', 'provider', 'modelId', 'imageData', 'imageUri', 'secret', 'credential', 'absolutePath']);

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

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function assertExactKeys(value, allowed, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object.`);
  for (const key of Object.keys(value)) assert(allowed.has(key), `${label}.${key} is not allowed by schemaVersion ${SCHEMA_VERSION}.`);
  for (const key of allowed) assert(Object.hasOwn(value, key), `${label}.${key} is required.`);
}

function assertStringArray(value, label, { min = 0 } = {}) {
  assert(Array.isArray(value), `${label} must be an array.`);
  assert(value.length >= min, `${label} must contain at least ${min} item(s).`);
  assert(value.every(nonEmpty), `${label} must contain non-empty strings.`);
  assert(new Set(value).size === value.length, `${label} must not contain duplicates.`);
}

function assertDateTime(value, label) {
  assert(nonEmpty(value) && Number.isFinite(Date.parse(value)), `${label} must be an ISO date-time.`);
}

function assertRepositoryRelative(value, label) {
  assert(nonEmpty(value), `${label} is required.`);
  assert(!value.startsWith('/') && !value.startsWith('\\\\'), `${label} must be repository-relative.`);
  assert(!/^[A-Za-z]:[\\/]/.test(value), `${label} must not expose a local drive path.`);
  assert(!value.split('/').includes('..'), `${label} must not traverse outside the repository.`);
}

function assertDigest(record, digestField, label) {
  assert(/^[a-f0-9]{64}$/.test(record[digestField] ?? ''), `${label} must carry a SHA-256 digest.`);
  const clone = structuredClone(record);
  delete clone[digestField];
  assert(record[digestField] === contentDigest(clone), `${label} digest does not match canonical content.`);
}

function assertNoForbiddenFields(value, path = '$') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoForbiddenFields(item, `${path}[${index}]`));
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_KEYS.has(key), `${path}.${key} is forbidden in BKL-046 F2.`);
    assertNoForbiddenFields(child, `${path}.${key}`);
  }
}

function validateSubject(subject) {
  assertExactKeys(subject, SUBJECT_KEYS, 'subject');
  assert(nonEmpty(subject.subjectId), 'subject.subjectId is required.');
  assert(SUBJECT_TYPES.has(subject.subjectType), 'subject.subjectType is invalid.');
  assert(CORRELATION_STATES.has(subject.correlationState), 'subject.correlationState is invalid.');
  for (const field of ['assetRef', 'sessionRef', 'workflowRef', 'stepRef']) {
    assert(subject[field] === null || nonEmpty(subject[field]), `subject.${field} must be null or non-empty.`);
  }
  assert([subject.assetRef, subject.sessionRef, subject.workflowRef, subject.stepRef].some(present), 'subject must carry at least one reference.');
}

function validateSourceBinding(binding) {
  assertExactKeys(binding, SOURCE_KEYS, `sourceBinding.${binding?.bindingId ?? 'unknown'}`);
  assert(nonEmpty(binding.bindingId), 'sourceBinding.bindingId is required.');
  assert(SEMANTIC_TYPES.has(binding.semanticType), `Source ${binding.bindingId} semanticType is invalid.`);
  assert(EVIDENCE_CLASSES.has(binding.evidenceClass), `Source ${binding.bindingId} evidenceClass is invalid.`);
  assert(SOURCE_AUTHORITIES.has(binding.sourceAuthority), `Source ${binding.bindingId} sourceAuthority is invalid.`);
  assertRepositoryRelative(binding.sourceRef, `Source ${binding.bindingId} sourceRef`);
  assert(LIFECYCLES.has(binding.lifecycleState), `Source ${binding.bindingId} lifecycleState is invalid.`);
  assert(QUALITY.has(binding.quality), `Source ${binding.bindingId} quality is invalid.`);
  assert(COMPLETENESS.has(binding.completeness), `Source ${binding.bindingId} completeness is invalid.`);
  assertStringArray(binding.citationRefs, `Source ${binding.bindingId} citationRefs`, { min: 1 });
  binding.citationRefs.forEach((ref) => assertRepositoryRelative(ref, `Source ${binding.bindingId} citationRef`));
  assertStringArray(binding.limitations, `Source ${binding.bindingId} limitations`);
  assertDigest(binding, 'bindingDigest', `Source ${binding.bindingId}`);
}

function validateParameterAdvice(advice, sourceById, label) {
  assertExactKeys(advice, PARAMETER_KEYS, label);
  assert(PARAMETER_MODES.has(advice.mode), `${label}.mode is invalid.`);
  assert(nonEmpty(advice.applicability), `${label}.applicability is required.`);
  assertStringArray(advice.evidenceRefs, `${label}.evidenceRefs`);
  assertStringArray(advice.limitations, `${label}.limitations`, { min: 1 });
  advice.evidenceRefs.forEach((ref) => assert(sourceById.has(ref), `${label} references unknown source ${ref}.`));

  if (advice.mode === 'UNKNOWN_NOT_RECOMMENDED') {
    assert(advice.parameterId === null && advice.unit === null && advice.categoricalValue === null && advice.lowerBound === null && advice.upperBound === null, `${label} unknown advice must not invent a parameter or value.`);
    return;
  }
  assert(nonEmpty(advice.parameterId), `${label}.parameterId is required for actionable advice.`);
  assert(advice.evidenceRefs.length > 0, `${label} actionable advice requires evidence.`);
  if (advice.mode === 'CATEGORICAL') {
    assert(nonEmpty(advice.categoricalValue), `${label} categorical advice requires a value.`);
    assert(advice.lowerBound === null && advice.upperBound === null, `${label} categorical advice cannot carry numeric bounds.`);
  }
  if (advice.mode === 'BOUNDED_INTERVAL') {
    assert(typeof advice.lowerBound === 'number' && Number.isFinite(advice.lowerBound), `${label}.lowerBound must be finite.`);
    assert(typeof advice.upperBound === 'number' && Number.isFinite(advice.upperBound), `${label}.upperBound must be finite.`);
    assert(advice.lowerBound <= advice.upperBound, `${label} interval must not be inverted.`);
    assert(nonEmpty(advice.unit), `${label} bounded interval requires a unit.`);
    assert(advice.categoricalValue === null, `${label} bounded interval cannot carry a categorical value.`);
  }
}

function validateRecommendation(recommendation, subject, sourceById) {
  const label = `recommendation.${recommendation?.recommendationId ?? 'unknown'}`;
  assertExactKeys(recommendation, RECOMMENDATION_KEYS, label);
  for (const field of ['recommendationId', 'producer', 'producerVersion', 'methodId', 'correlationId', 'subjectRef', 'proposedAction', 'rationale']) {
    assert(nonEmpty(recommendation[field]), `${label}.${field} is required.`);
  }
  assert(recommendation.semanticType === 'recommendation', `${label}.semanticType must be recommendation.`);
  assert(typeof recommendation.aiDerived === 'boolean', `${label}.aiDerived must be boolean.`);
  assertDateTime(recommendation.generatedAt, `${label}.generatedAt`);
  assert(recommendation.subjectRef === subject.subjectId, `${label} references another subject.`);
  assert(CATEGORIES.has(recommendation.category), `${label}.category is invalid.`);
  assert(LIFECYCLES.has(recommendation.lifecycleState), `${label}.lifecycleState is invalid.`);
  assertStringArray(recommendation.sourceBindingRefs, `${label}.sourceBindingRefs`, { min: 1 });
  assertStringArray(recommendation.citationRefs, `${label}.citationRefs`, { min: 1 });
  assertStringArray(recommendation.provenanceRefs, `${label}.provenanceRefs`, { min: 1 });
  assertStringArray(recommendation.conflicts, `${label}.conflicts`);
  assertStringArray(recommendation.unknowns, `${label}.unknowns`);
  assertStringArray(recommendation.limitations, `${label}.limitations`, { min: 1 });
  const sources = recommendation.sourceBindingRefs.map((ref) => {
    assert(sourceById.has(ref), `${label} references unknown source ${ref}.`);
    return sourceById.get(ref);
  });
  assert(Array.isArray(recommendation.parameterAdvice), `${label}.parameterAdvice must be an array.`);
  recommendation.parameterAdvice.forEach((advice, index) => validateParameterAdvice(advice, sourceById, `${label}.parameterAdvice[${index}]`));
  assertExactKeys(recommendation.confidence, CONFIDENCE_KEYS, `${label}.confidence`);
  assert(recommendation.confidence.state === 'UNAVAILABLE_F2', `${label} confidence must remain unavailable in F2.`);
  assert(recommendation.confidence.contractRef === null && recommendation.confidence.value === null, `${label} must not carry ungoverned confidence.`);
  assertStringArray(recommendation.confidence.limitations, `${label}.confidence.limitations`, { min: 1 });

  const eligible = sources.every((source) => source.lifecycleState === 'validated' && source.quality === 'VALID' && source.completeness === 'COMPLETE' && source.evidenceClass !== 'SUGGESTED');
  if (recommendation.lifecycleState === 'validated') {
    assert(subject.correlationState === 'RESOLVED', `${label} cannot be validated with unresolved subject correlation.`);
    assert(eligible, `${label} cannot be validated from stale, incomplete, invalid or suggested evidence.`);
    assert(recommendation.conflicts.length === 0 && recommendation.unknowns.length === 0, `${label} validated state requires resolved conflicts and unknowns.`);
  }
  if (!eligible || subject.correlationState !== 'RESOLVED' || recommendation.conflicts.length > 0 || recommendation.unknowns.length > 0) {
    assert(['incomplete', 'unknown', 'rejected'].includes(recommendation.lifecycleState), `${label} must fail closed when evidence or correlation is insufficient.`);
  }
  assertDigest(recommendation, 'recommendationDigest', label);
}

function validateReceipt(receipt, recommendationById) {
  const label = `humanDecisionReceipt.${receipt?.receiptId ?? 'unknown'}`;
  assertExactKeys(receipt, RECEIPT_KEYS, label);
  for (const field of ['receiptId', 'recommendationId', 'actorRef', 'correlationId']) assert(nonEmpty(receipt[field]), `${label}.${field} is required.`);
  assertDateTime(receipt.presentedAt, `${label}.presentedAt`);
  assertDateTime(receipt.decidedAt, `${label}.decidedAt`);
  assert(Date.parse(receipt.presentedAt) <= Date.parse(receipt.decidedAt), `${label} decision cannot precede presentation.`);
  assert(DISPOSITIONS.has(receipt.disposition), `${label}.disposition is invalid.`);
  assert(recommendationById.has(receipt.recommendationId), `${label} references unknown recommendation ${receipt.recommendationId}.`);
  const recommendation = recommendationById.get(receipt.recommendationId);
  assert(receipt.correlationId === recommendation.correlationId, `${label} correlationId does not match recommendation.`);
  assert(Array.isArray(receipt.decisionEdits), `${label}.decisionEdits must be an array.`);
  receipt.decisionEdits.forEach((edit, index) => {
    assertExactKeys(edit, EDIT_KEYS, `${label}.decisionEdits[${index}]`);
    assert(nonEmpty(edit.parameterId) && present(edit.selectedValue) && nonEmpty(edit.reason), `${label}.decisionEdits[${index}] is incomplete.`);
    assert(edit.unit === null || nonEmpty(edit.unit), `${label}.decisionEdits[${index}].unit is invalid.`);
  });
  if (receipt.disposition === 'EDITED_FOR_MANUAL_APPLICATION') assert(receipt.decisionEdits.length > 0, `${label} edited disposition requires decision edits.`);
  if (receipt.disposition !== 'EDITED_FOR_MANUAL_APPLICATION') assert(receipt.decisionEdits.length === 0, `${label} decision edits require edited disposition.`);
  assert(receipt.decisionRationale === null || nonEmpty(receipt.decisionRationale), `${label}.decisionRationale is invalid.`);
  assert(receipt.executionState === 'NOT_OBSERVED', `${label} must not claim execution.`);
  assert(Array.isArray(receipt.executionEvidenceRefs) && receipt.executionEvidenceRefs.length === 0, `${label} execution evidence belongs to BKL-045, not the decision receipt.`);
  assert(receipt.actionAuthority === 'NONE', `${label} actionAuthority must be NONE.`);
  assertDigest(receipt, 'receiptDigest', label);
}

export function validateAdvisoryContractFixture(fixture) {
  assertExactKeys(fixture, ROOT_KEYS, 'fixture');
  assertNoForbiddenFields(fixture);
  assert(fixture.schemaVersion === SCHEMA_VERSION, `Unsupported schemaVersion ${fixture.schemaVersion}.`);
  assert(fixture.contractType === CONTRACT_TYPE, `Unsupported contractType ${fixture.contractType}.`);
  assert(fixture.identityMethod === IDENTITY_METHOD, `Unsupported identityMethod ${fixture.identityMethod}.`);
  assert(nonEmpty(fixture.fixtureId), 'fixture.fixtureId is required.');
  assert(fixture.fixtureMode === 'BOUNDED_SYNTHETIC_FIXTURE', 'fixtureMode must be BOUNDED_SYNTHETIC_FIXTURE.');
  assertDateTime(fixture.generatedAt, 'fixture.generatedAt');
  validateSubject(fixture.subject);

  assert(Array.isArray(fixture.sourceBindings) && fixture.sourceBindings.length >= 1 && fixture.sourceBindings.length <= 32, 'sourceBindings must contain 1..32 records.');
  const sourceById = new Map();
  for (const source of fixture.sourceBindings) {
    validateSourceBinding(source);
    assert(!sourceById.has(source.bindingId), `Duplicate source binding ${source.bindingId}.`);
    sourceById.set(source.bindingId, source);
  }

  assert(Array.isArray(fixture.recommendations) && fixture.recommendations.length >= 1 && fixture.recommendations.length <= 16, 'recommendations must contain 1..16 records.');
  const recommendationById = new Map();
  for (const recommendation of fixture.recommendations) {
    validateRecommendation(recommendation, fixture.subject, sourceById);
    assert(!recommendationById.has(recommendation.recommendationId), `Duplicate recommendation ${recommendation.recommendationId}.`);
    recommendationById.set(recommendation.recommendationId, recommendation);
  }

  assert(Array.isArray(fixture.humanDecisionReceipts) && fixture.humanDecisionReceipts.length >= 1 && fixture.humanDecisionReceipts.length <= 16, 'humanDecisionReceipts must contain 1..16 records.');
  const receiptIds = new Set();
  for (const receipt of fixture.humanDecisionReceipts) {
    validateReceipt(receipt, recommendationById);
    assert(!receiptIds.has(receipt.receiptId), `Duplicate human decision receipt ${receipt.receiptId}.`);
    receiptIds.add(receipt.receiptId);
  }

  assertExactKeys(fixture.authority, AUTHORITY_KEYS, 'authority');
  assert(fixture.authority.consumerMode === 'READ_ONLY', 'consumerMode must be READ_ONLY.');
  assert(fixture.authority.advisoryOnly === true, 'advisoryOnly must be true.');
  assert(fixture.authority.acceptanceAuthority === 'HUMAN_ONLY', 'acceptanceAuthority must be HUMAN_ONLY.');
  assert(fixture.authority.actionAuthority === 'NONE', 'actionAuthority must be NONE.');
  assert(fixture.authority.executionAuthority === 'NONE', 'executionAuthority must be NONE.');
  assert(fixture.authority.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'safetyAuthority must remain LOCAL_PHYSICAL_INTERLOCKS.');
  assert(fixture.authority.pixInsightApplyAuthorized === false, 'PixInsight apply is not authorized in F2.');
  assert(fixture.authority.automaticAcceptanceAuthorized === false, 'Automatic acceptance is not authorized in F2.');
  assertStringArray(fixture.limitations, 'fixture.limitations', { min: 1 });
  assertDigest(fixture, 'artifactDigest', 'fixture');
  return true;
}
