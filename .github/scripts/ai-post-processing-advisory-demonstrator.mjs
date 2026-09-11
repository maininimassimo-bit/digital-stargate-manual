import {
  canonicalJson,
  contentDigest,
  validateAdvisoryContractFixture,
  validateRecommendationRecord
} from './ai-post-processing-advisory-contract.mjs';

export const F3_SCHEMA_VERSION = '1.0';
export const F3_CONTRACT_TYPE = 'AI_POST_PROCESSING_ASSISTANT_F3_DEMONSTRATOR_OUTPUT';
export const F3_MODE = 'BOUNDED_SYNTHETIC_READ_ONLY';
export const F3_PRODUCER = 'DSG.DeterministicAdvisoryDemonstrator';
export const F3_PRODUCER_VERSION = '1.0.0-f3';
export const F3_METHOD_ID = 'BKL046-F3-CLOSED-RULES-1';
export const F3_CONTEXTS = Object.freeze({
  BOUNDED_SYNTHETIC: 'BOUNDED_SYNTHETIC',
  SESSION_PROVENANCE_READ_ONLY: 'SESSION_PROVENANCE_READ_ONLY'
});

const OUTPUT_KEYS = new Set(['schemaVersion', 'contractType', 'demonstratorMode', 'producer', 'producerVersion', 'methodId', 'inputFixtureId', 'inputArtifactDigest', 'generatedAt', 'subject', 'sourceBindings', 'recommendations', 'ruleEvaluations', 'decisionState', 'authority', 'limitations', 'artifactDigest']);
const EVALUATION_KEYS = new Set(['ruleId', 'recommendationId', 'decision', 'reasonCodes']);
const FORBIDDEN_KEYS = new Set(['humanDecisionReceipts', 'command', 'script', 'applyPath', 'execute', 'autoAccept', 'deviceCommand', 'provider', 'modelId', 'imageData', 'imageUri', 'secret', 'credential', 'absolutePath']);

const RULES = Object.freeze([
  Object.freeze({ ruleId: 'GOVERNANCE_READINESS', sourceAuthority: 'repository_authority' }),
  Object.freeze({ ruleId: 'PROCESSING_HISTORY_AVAILABILITY', sourceAuthority: 'processing_evidence' })
]);

const nonEmpty = (value) => typeof value === 'string' && value.trim().length > 0;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function assertExactKeys(value, allowed, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object.`);
  for (const key of Object.keys(value)) assert(allowed.has(key), `${label}.${key} is not allowed in F3.`);
  for (const key of allowed) assert(Object.hasOwn(value, key), `${label}.${key} is required.`);
}

function assertNoForbiddenFields(value, path = '$') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoForbiddenFields(item, `${path}[${index}]`));
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_KEYS.has(key), `${path}.${key} is forbidden in BKL-046 F3.`);
    assertNoForbiddenFields(child, `${path}.${key}`);
  }
}

function deepFreeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    Object.freeze(value);
    for (const child of Object.values(value)) deepFreeze(child);
  }
  return value;
}

function eligibilityReasonCodes(subject, sources) {
  const reasons = [];
  if (subject.correlationState !== 'RESOLVED') reasons.push(`SUBJECT_CORRELATION_${subject.correlationState}`);
  if (sources.length === 0) reasons.push('REQUIRED_SOURCE_AUTHORITY_MISSING');
  for (const source of sources) {
    if (source.lifecycleState !== 'validated') reasons.push(`SOURCE_LIFECYCLE_${source.lifecycleState.toUpperCase()}`);
    if (source.quality !== 'VALID') reasons.push(`SOURCE_QUALITY_${source.quality}`);
    if (source.completeness !== 'COMPLETE') reasons.push(`SOURCE_COMPLETENESS_${source.completeness}`);
    if (source.evidenceClass === 'SUGGESTED') reasons.push('SOURCE_CLASS_SUGGESTED');
  }
  return [...new Set(reasons)].sort();
}

function makeRecommendation({ inputArtifactDigest, generatedAt, subject, sourceBindings, contextMode, rule, sources, reasonCodes }) {
  const sourceBindingRefs = sources.length > 0
    ? sources.map((source) => source.bindingId).sort()
    : sourceBindings.map((source) => source.bindingId).sort();
  const citationRefs = [...new Set((sources.length > 0 ? sources : sourceBindings).flatMap((source) => source.citationRefs))].sort();
  const seed = {
    inputArtifactDigest,
    methodId: F3_METHOD_ID,
    ruleId: rule.ruleId,
    sourceBindingRefs,
    subjectRef: subject.subjectId
  };
  const suffix = contentDigest(seed).slice(0, 24).toUpperCase();
  const eligible = reasonCodes.length === 0;
  const governanceRule = rule.ruleId === 'GOVERNANCE_READINESS';
  const recommendation = {
    recommendationId: `REC-BKL046-F3-${suffix}`,
    semanticType: 'recommendation',
    aiDerived: false,
    producer: F3_PRODUCER,
    producerVersion: F3_PRODUCER_VERSION,
    methodId: F3_METHOD_ID,
    generatedAt,
    correlationId: `CORR-BKL046-F3-${suffix}`,
    subjectRef: subject.subjectId,
    category: eligible ? 'QUALITY_CHECK' : 'STOP_AND_REVIEW',
    lifecycleState: eligible ? 'validated' : 'incomplete',
    proposedAction: eligible
      ? (governanceRule
        ? 'Confirm the governed advisory boundary before requesting subject-specific PixInsight guidance.'
        : 'Review the complete governed PixInsight process history before requesting subject-specific parameter guidance.')
      : (governanceRule
        ? 'Stop advisory generation and review the governance evidence manually.'
        : 'Stop subject-specific parameter recommendation and review the PixInsight workflow evidence manually.'),
    rationale: eligible
      ? (governanceRule
        ? (contextMode === F3_CONTEXTS.BOUNDED_SYNTHETIC
          ? 'The repository authority source is validated, complete and correlated to the bounded synthetic subject.'
          : 'The repository authority source is validated, complete and correlated to the governed session subject.')
        : (contextMode === F3_CONTEXTS.BOUNDED_SYNTHETIC
          ? 'The processing evidence source is validated, complete and correlated to the bounded synthetic subject.'
          : 'The processing evidence source is validated, complete and correlated to the governed session subject.'))
      : `The closed F3 eligibility gate failed: ${reasonCodes.join(', ')}.`,
    sourceBindingRefs,
    citationRefs,
    provenanceRefs: [`PRV-BKL046-F3-${rule.ruleId}-${suffix}`],
    parameterAdvice: eligible ? [] : [{
      parameterId: null,
      mode: 'UNKNOWN_NOT_RECOMMENDED',
      unit: null,
      categoricalValue: null,
      lowerBound: null,
      upperBound: null,
      applicability: 'Subject-specific PixInsight parameters while the deterministic evidence gate is not satisfied.',
      evidenceRefs: sourceBindingRefs,
      limitations: ['No parameter or value may be inferred from incomplete, stale, invalid, suggested or uncorrelated evidence.']
    }],
    conflicts: [],
    unknowns: eligible ? [] : reasonCodes,
    confidence: {
      state: 'UNAVAILABLE_F2',
      contractRef: null,
      value: null,
      limitations: ['F3 does not introduce a calibrated recommendation-confidence method.']
    },
    limitations: [
      eligible
        ? (contextMode === F3_CONTEXTS.BOUNDED_SYNTHETIC
          ? 'Validated means contract-valid deterministic guidance over a bounded synthetic fixture; it is not scientific acceptance, human approval or execution.'
          : 'Validated means contract-valid deterministic guidance over governed session evidence; it is not scientific acceptance, human approval or execution.')
        : 'This recommendation is fail-closed and cannot be promoted while any reason code remains.'
    ],
    recommendationDigest: ''
  };
  delete recommendation.recommendationDigest;
  recommendation.recommendationDigest = contentDigest(recommendation);
  return recommendation;
}

export function buildDeterministicAdvisoryRecords({
  inputArtifactDigest,
  generatedAt,
  subject,
  sourceBindings: inputSourceBindings,
  contextMode = F3_CONTEXTS.SESSION_PROVENANCE_READ_ONLY
}) {
  assert(/^[a-f0-9]{64}$/.test(inputArtifactDigest ?? ''), 'inputArtifactDigest must be a SHA-256 digest.');
  assert(Number.isFinite(Date.parse(generatedAt)), 'generatedAt must be an ISO date-time.');
  assert(Object.values(F3_CONTEXTS).includes(contextMode), 'Unsupported F3 rule context.');
  assert(Array.isArray(inputSourceBindings) && inputSourceBindings.length >= 1 && inputSourceBindings.length <= 32, 'sourceBindings must contain 1..32 records.');
  const sourceBindings = structuredClone(inputSourceBindings).sort((a, b) => a.bindingId.localeCompare(b.bindingId));
  const recommendations = [];
  const ruleEvaluations = [];

  for (const rule of RULES) {
    const sources = sourceBindings.filter((source) => source.sourceAuthority === rule.sourceAuthority);
    const reasonCodes = eligibilityReasonCodes(subject, sources);
    const recommendation = makeRecommendation({ inputArtifactDigest, generatedAt, subject, sourceBindings, contextMode, rule, sources, reasonCodes });
    validateRecommendationRecord(recommendation, subject, sourceBindings);
    recommendations.push(recommendation);
    ruleEvaluations.push({
      ruleId: rule.ruleId,
      recommendationId: recommendation.recommendationId,
      decision: reasonCodes.length === 0 ? 'PASS' : 'FAIL_CLOSED',
      reasonCodes
    });
  }

  recommendations.sort((a, b) => a.recommendationId.localeCompare(b.recommendationId));
  ruleEvaluations.sort((a, b) => a.ruleId.localeCompare(b.ruleId));
  return deepFreeze({ sourceBindings, recommendations, ruleEvaluations });
}

export function buildDeterministicAdvisoryDemonstration(fixture) {
  validateAdvisoryContractFixture(fixture);
  const { sourceBindings, recommendations, ruleEvaluations } = buildDeterministicAdvisoryRecords({
    inputArtifactDigest: fixture.artifactDigest,
    generatedAt: fixture.generatedAt,
    subject: fixture.subject,
    sourceBindings: fixture.sourceBindings,
    contextMode: F3_CONTEXTS.BOUNDED_SYNTHETIC
  });
  const output = {
    schemaVersion: F3_SCHEMA_VERSION,
    contractType: F3_CONTRACT_TYPE,
    demonstratorMode: F3_MODE,
    producer: F3_PRODUCER,
    producerVersion: F3_PRODUCER_VERSION,
    methodId: F3_METHOD_ID,
    inputFixtureId: fixture.fixtureId,
    inputArtifactDigest: fixture.artifactDigest,
    generatedAt: fixture.generatedAt,
    subject: structuredClone(fixture.subject),
    sourceBindings,
    recommendations,
    ruleEvaluations,
    decisionState: 'NOT_PRESENT_PRE_DECISION',
    authority: structuredClone(fixture.authority),
    limitations: [
      'Deterministic read-only demonstration over a bounded synthetic F2 fixture; not a production assistant or model output.',
      'No human decision, PixInsight execution, automatic acceptance, device command or Safety Authority is represented.'
    ],
    artifactDigest: ''
  };
  delete output.artifactDigest;
  output.artifactDigest = contentDigest(output);
  validateDeterministicAdvisoryOutput(output);
  return deepFreeze(output);
}

export function validateDeterministicAdvisoryOutput(output) {
  assertExactKeys(output, OUTPUT_KEYS, 'output');
  assertNoForbiddenFields(output);
  assert(output.schemaVersion === F3_SCHEMA_VERSION, 'Unsupported F3 schemaVersion.');
  assert(output.contractType === F3_CONTRACT_TYPE, 'Unsupported F3 contractType.');
  assert(output.demonstratorMode === F3_MODE, 'Only bounded synthetic read-only mode is authorized in F3.');
  assert(output.producer === F3_PRODUCER && output.producerVersion === F3_PRODUCER_VERSION, 'Unsupported F3 producer.');
  assert(output.methodId === F3_METHOD_ID, 'Unsupported F3 method.');
  assert(nonEmpty(output.inputFixtureId), 'output.inputFixtureId is required.');
  assert(/^[a-f0-9]{64}$/.test(output.inputArtifactDigest ?? ''), 'output.inputArtifactDigest must be a SHA-256 digest.');
  assert(Number.isFinite(Date.parse(output.generatedAt)), 'output.generatedAt must be an ISO date-time.');
  assert(Array.isArray(output.sourceBindings) && output.sourceBindings.length >= 1 && output.sourceBindings.length <= 32, 'output.sourceBindings must contain 1..32 records.');
  assert(Array.isArray(output.recommendations) && output.recommendations.length === RULES.length, `output.recommendations must contain exactly ${RULES.length} records.`);
  output.recommendations.forEach((recommendation) => validateRecommendationRecord(recommendation, output.subject, output.sourceBindings));
  assert(Array.isArray(output.ruleEvaluations) && output.ruleEvaluations.length === RULES.length, `output.ruleEvaluations must contain exactly ${RULES.length} records.`);
  const recommendationById = new Map(output.recommendations.map((item) => [item.recommendationId, item]));
  assert(recommendationById.size === output.recommendations.length, 'output.recommendations must have unique IDs.');
  const sourceById = new Map(output.sourceBindings.map((item) => [item.bindingId, item]));
  const ruleIds = new Set();
  const evaluatedRecommendationIds = new Set();
  for (const evaluation of output.ruleEvaluations) {
    assertExactKeys(evaluation, EVALUATION_KEYS, `ruleEvaluation.${evaluation?.ruleId ?? 'unknown'}`);
    assert(RULES.some((rule) => rule.ruleId === evaluation.ruleId), `Unknown rule ${evaluation.ruleId}.`);
    assert(!ruleIds.has(evaluation.ruleId), `Duplicate rule ${evaluation.ruleId}.`);
    ruleIds.add(evaluation.ruleId);
    assert(recommendationById.has(evaluation.recommendationId), `Rule ${evaluation.ruleId} references an unknown recommendation.`);
    assert(!evaluatedRecommendationIds.has(evaluation.recommendationId), `Recommendation ${evaluation.recommendationId} is evaluated more than once.`);
    evaluatedRecommendationIds.add(evaluation.recommendationId);
    assert(['PASS', 'FAIL_CLOSED'].includes(evaluation.decision), `Rule ${evaluation.ruleId} decision is invalid.`);
    assert(Array.isArray(evaluation.reasonCodes) && new Set(evaluation.reasonCodes).size === evaluation.reasonCodes.length, `Rule ${evaluation.ruleId} reasonCodes must be unique.`);
    assert(evaluation.reasonCodes.every(nonEmpty), `Rule ${evaluation.ruleId} reasonCodes must be non-empty strings.`);
    assert((evaluation.decision === 'PASS') === (evaluation.reasonCodes.length === 0), `Rule ${evaluation.ruleId} decision and reasonCodes disagree.`);
    const recommendation = recommendationById.get(evaluation.recommendationId);
    const rule = RULES.find((item) => item.ruleId === evaluation.ruleId);
    const actualAuthorities = new Set(recommendation.sourceBindingRefs.map((ref) => sourceById.get(ref)?.sourceAuthority));
    if (evaluation.reasonCodes.includes('REQUIRED_SOURCE_AUTHORITY_MISSING')) {
      assert(!actualAuthorities.has(rule.sourceAuthority), `Rule ${evaluation.ruleId} reports a missing authority that is present.`);
    } else {
      assert(actualAuthorities.size === 1 && actualAuthorities.has(rule.sourceAuthority), `Rule ${evaluation.ruleId} references the wrong source authority.`);
    }
    if (evaluation.decision === 'PASS') {
      assert(recommendation.lifecycleState === 'validated' && recommendation.category === 'QUALITY_CHECK', `Rule ${evaluation.ruleId} PASS must reference a validated QUALITY_CHECK.`);
      assert(recommendation.unknowns.length === 0, `Rule ${evaluation.ruleId} PASS cannot carry unknowns.`);
    } else {
      assert(recommendation.lifecycleState === 'incomplete' && recommendation.category === 'STOP_AND_REVIEW', `Rule ${evaluation.ruleId} FAIL_CLOSED must reference an incomplete STOP_AND_REVIEW.`);
      assert(canonicalJson(recommendation.unknowns) === canonicalJson(evaluation.reasonCodes), `Rule ${evaluation.ruleId} reasonCodes must match recommendation unknowns.`);
    }
  }
  assert(output.decisionState === 'NOT_PRESENT_PRE_DECISION', 'F3 output must remain pre-decision.');
  assert(output.authority.consumerMode === 'READ_ONLY', 'consumerMode must be READ_ONLY.');
  assert(output.authority.advisoryOnly === true, 'advisoryOnly must be true.');
  assert(output.authority.acceptanceAuthority === 'HUMAN_ONLY', 'acceptanceAuthority must be HUMAN_ONLY.');
  assert(output.authority.actionAuthority === 'NONE' && output.authority.executionAuthority === 'NONE', 'Action and execution authority must be NONE.');
  assert(output.authority.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'Safety Authority must remain LOCAL_PHYSICAL_INTERLOCKS.');
  assert(output.authority.pixInsightApplyAuthorized === false && output.authority.automaticAcceptanceAuthorized === false, 'Apply and automatic acceptance are not authorized.');
  assert(Array.isArray(output.limitations) && output.limitations.length >= 1 && output.limitations.every(nonEmpty), 'output.limitations are required.');
  assert(/^[a-f0-9]{64}$/.test(output.artifactDigest ?? ''), 'output.artifactDigest must be a SHA-256 digest.');
  const preimage = structuredClone(output);
  delete preimage.artifactDigest;
  assert(output.artifactDigest === contentDigest(preimage), 'output.artifactDigest does not match canonical content.');
  return true;
}

export { canonicalJson, contentDigest };
