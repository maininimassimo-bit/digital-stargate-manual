const CATALOG_PATH = 'docs/data/scientific-session-catalog.json';
const SCHEMA_VERSION = '1.1';
const PROJECTION_TYPE = 'AI_POST_PROCESSING_ADVISORY_PROJECTION';
const PROJECTION_STATE = 'PRE_DECISION_READ_ONLY';
const IDENTITY_METHOD = 'BKL046-F4-CANONICAL-JSON-SHA256-1';
const PRODUCER = 'DSG.AiPostProcessingAdvisoryProjection';
const PRODUCER_VERSION = '1.0.0-f4b';
const METHOD_ID = 'BKL046-F3-CLOSED-RULES-1';
const PROVENANCE_PATH = /^docs\/architecture\/scientific-assets\/evidence\/BKL-045-F3B-PXP-\d{8}T\d{9}Z-[A-Z0-9][A-Z0-9_-]{0,31}\.json$/;
const DIGEST = /^[a-f0-9]{64}$/;
const CORRELATION_STATES = new Set([
  'PROVENANCE_MATCHED',
  'PROVENANCE_UNAVAILABLE',
  'CORRELATION_AMBIGUOUS',
  'CORRELATION_INVALID'
]);
const RULE_IDS = new Set(['GOVERNANCE_READINESS', 'PROCESSING_HISTORY_AVAILABILITY']);
const DECISIONS = new Set(['PASS', 'FAIL_CLOSED']);
const COMPLETENESS = new Set(['COMPLETE', 'PARTIAL', 'UNAVAILABLE']);
const FORBIDDEN_PUBLIC_KEYS = new Set([
  'actorRef', 'decisionRationale', 'decisionEdits', 'hostId', 'workspaceId', 'absolutePath',
  'localPath', 'imageData', 'imageUri', 'credential', 'secret'
]);
const PROJECTION_KEYS = [
  'schemaVersion', 'projectionType', 'projectionState', 'identityMethod', 'projectionId', 'generatedAt',
  'producer', 'producerVersion', 'methodId', 'sourceCatalog', 'sourceSet', 'records', 'summary',
  'authority', 'limitations', 'projectionDigest'
];
const CATALOG_KEYS = ['path', 'digest', 'sessionCount', 'sessionIds'];
const SOURCE_SET_KEYS = ['validationMode', 'digest', 'entries'];
const SOURCE_ENTRY_KEYS = [
  'path', 'digest', 'sidecarId', 'exportedAt', 'sessionId', 'target', 'workflowId', 'completeness', 'limitations'
];
const RECORD_KEYS = [
  'recordId', 'sessionId', 'target', 'correlationState', 'sourceRefs', 'inputArtifactDigest', 'subject',
  'sourceBindings', 'recommendations', 'ruleEvaluations', 'decisionState', 'recordDigest'
];
const RULE_KEYS = ['ruleId', 'recommendationId', 'decision', 'reasonCodes'];
const SUMMARY_KEYS = [
  'totalSessions', 'provenanceMatched', 'provenanceUnavailable', 'correlationAmbiguous',
  'correlationInvalid', 'governancePass', 'governanceFailClosed', 'processingHistoryPass',
  'processingHistoryFailClosed', 'uncorrelatedSources'
];
const AUTHORITY_KEYS = [
  'consumerMode', 'advisoryOnly', 'acceptanceAuthority', 'actionAuthority', 'executionAuthority',
  'safetyAuthority', 'pixInsightApplyAuthorized', 'automaticAcceptanceAuthorized'
];
const SUBJECT_KEYS = ['subjectId', 'subjectType', 'assetRef', 'sessionRef', 'workflowRef', 'stepRef', 'correlationState'];
const BINDING_KEYS = [
  'bindingId', 'semanticType', 'evidenceClass', 'sourceAuthority', 'sourceRef', 'lifecycleState',
  'quality', 'completeness', 'citationRefs', 'limitations', 'bindingDigest'
];
const RECOMMENDATION_KEYS = [
  'recommendationId', 'semanticType', 'aiDerived', 'producer', 'producerVersion', 'methodId',
  'generatedAt', 'correlationId', 'subjectRef', 'category', 'lifecycleState', 'proposedAction',
  'rationale', 'sourceBindingRefs', 'citationRefs', 'provenanceRefs', 'parameterAdvice', 'conflicts',
  'unknowns', 'confidence', 'limitations', 'recommendationDigest'
];
const CONFIDENCE_KEYS = ['state', 'contractRef', 'value', 'limitations'];
const PARAMETER_ADVICE_KEYS = [
  'parameterId', 'mode', 'unit', 'categoricalValue', 'lowerBound', 'upperBound', 'applicability',
  'evidenceRefs', 'limitations'
];
const SUBJECT_TYPES = new Set(['SCIENTIFIC_ASSET', 'PIXINSIGHT_WORKFLOW', 'PIXINSIGHT_PROCESS_STEP']);
const SUBJECT_CORRELATION_STATES = new Set(['RESOLVED', 'PARTIAL', 'UNRESOLVED']);
const SEMANTIC_TYPES = new Set(['observation', 'evidence', 'claim', 'recommendation']);
const EVIDENCE_CLASSES = new Set(['OBSERVED', 'DECLARED', 'SUGGESTED']);
const SOURCE_AUTHORITIES = new Set([
  'repository_authority', 'scientific_catalog', 'analytics_product', 'session_projection',
  'processing_evidence', 'projection', 'unknown'
]);
const LIFECYCLE_STATES = new Set(['incomplete', 'unknown', 'draft', 'validated', 'superseded', 'rejected']);
const QUALITY_STATES = new Set(['VALID', 'STALE', 'UNKNOWN', 'INVALID']);
const RECOMMENDATION_CATEGORIES = new Set([
  'PROCESS_ORDER', 'PARAMETER_RANGE', 'QUALITY_CHECK', 'WORKFLOW_ALTERNATIVE', 'STOP_AND_REVIEW'
]);
const PARAMETER_MODES = new Set(['CATEGORICAL', 'BOUNDED_INTERVAL', 'UNKNOWN_NOT_RECOMMENDED']);

const F5_SCHEMA_VERSION = '2.0';
const F5_EVALUATION_TYPE = 'BKL046_F5_REAL_EVIDENCE_EVALUATION';
const F5_EVALUATION_STATE = 'F5C_CLOSURE_EVALUATED';
const F5_IDENTITY_METHOD = 'BKL046-F5-CANONICAL-JSON-SHA256-1';
const F5_PRODUCER = 'DSG.AiPostProcessingRealEvidenceEvaluator';
const F5_PRODUCER_VERSION = '2.0.0-f5c';
const F5_METHOD_ID = 'BKL046-F5C-CLOSED-EVALUATION-1';
const F5_PROJECTION_PATH = 'docs/data/ai-post-processing-advisory-projection.json';
const F5_HUMAN_DIRECTORY = 'docs/data/ai-post-processing-human-decisions';
const F5_EXECUTION_DIRECTORY = 'docs/data/ai-post-processing-execution-evidence';
const F5_HUMAN_PATTERN = '^docs\\/data\\/ai-post-processing-human-decisions\\/BKL-046-F2-HDR-\\d{8}T\\d{6}Z-[A-Z0-9][A-Z0-9_-]{0,31}\\.json$';
const F5_EXECUTION_PATTERN = '^docs\\/data\\/ai-post-processing-execution-evidence\\/BKL-046-F5-EXE-\\d{8}T\\d{6}Z-[A-Z0-9][A-Z0-9_-]{0,31}\\.json$';
const F5_HUMAN_PATH = new RegExp(F5_HUMAN_PATTERN);
const F5_EXECUTION_PATH = new RegExp(F5_EXECUTION_PATTERN);
const F5_METHOD_REGISTRY = Object.freeze({
  registryId: 'BKL046-F5C-CLOSED-REGISTRY-1',
  cohortIds: ['ALL-CANONICAL-SESSIONS-F5', 'EXACT-PROVENANCE-MATCHED-F5', 'HUMAN-DECISION-RECEIPTS-F5', 'EXECUTION-EVIDENCE-F5'],
  selectionRuleIds: ['ALL-CANONICAL-SESSIONS-EXACT-SET-1', 'F4-PROVENANCE-MATCHED-EXACT-1', 'F2-HUMAN-DECISION-EXACT-CORRELATION-1', 'F5-EXECUTION-EVIDENCE-EXACT-CORRELATION-1'],
  technicalGateIds: ['CATALOG_SNAPSHOT_INTEGRITY', 'F4_PROJECTION_INTEGRITY', 'FULL_POPULATION_COVERAGE', 'HUMAN_DECISION_SOURCE_CONTRACT', 'EXECUTION_EVIDENCE_SOURCE_CONTRACT', 'CLOSED_METHOD_REGISTRY', 'F5A_REPORT_DETERMINISM', 'F5B_DYNAMIC_UPDATE', 'F5B_CONSUMER'],
  technicalStates: ['READY_FOR_F5_EVALUATION', 'NOT_ACCEPTED', 'REJECTED', 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS'],
  scientificStates: ['NOT_EVALUABLE_CURRENT_EVIDENCE', 'EVALUATION_REQUIRED', 'INVALID'],
  humanDecisionStates: ['NOT_AVAILABLE', 'AVAILABLE'],
  productionStates: ['NOT_READY_FOR_PRODUCTION', 'REJECTED_FOR_PRODUCTION'],
  capabilityOutcomes: ['F5A_EVALUATION_FOUNDATION_READY', 'NOT_ACCEPTED', 'REJECTED', 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS'],
  closureRecommendations: ['KEEP_OPEN', 'DO_NOT_CLOSE', 'CLOSE_DETERMINISTIC_CAPABILITY'],
  gateStates: ['PASS', 'FAIL_CLOSED', 'NOT_EXECUTED'],
  evidenceStates: ['AVAILABLE', 'NOT_AVAILABLE', 'NOT_EVALUABLE'],
  reasonCodes: ['FULL_CANONICAL_POPULATION', 'NO_EXACT_PROVENANCE_MATCHES', 'EXACT_PROVENANCE_AVAILABLE', 'NO_HUMAN_DECISION_RECEIPTS', 'HUMAN_DECISION_RECEIPTS_AVAILABLE', 'NO_EXECUTION_EVIDENCE', 'EXECUTION_EVIDENCE_AVAILABLE', 'NO_APPROVED_GROUND_TRUTH_METHOD', 'F5A_FOUNDATION_IMPLEMENTED', 'F5B_DYNAMIC_UPDATE_VERIFIED', 'F5B_CONSUMER_VERIFIED', 'PRODUCTION_AUTHORITY_NOT_GRANTED', 'SCIENTIFIC_EFFECTIVENESS_NOT_ESTABLISHED']
});
const F5_TOP_LEVEL_KEYS = ['schemaVersion', 'evaluationType', 'evaluationState', 'identityMethod', 'evaluationId', 'generatedAt', 'producer', 'producerVersion', 'methodId', 'sourceSnapshots', 'methodRegistry', 'cohorts', 'technicalGates', 'outcomes', 'summary', 'authority', 'limitations', 'evaluationDigest'];
const F5_SOURCE_SNAPSHOT_KEYS = ['catalog', 'f4Projection', 'humanDecisionSourceSet', 'executionEvidenceSourceSet'];
const F5_CATALOG_SNAPSHOT_KEYS = ['path', 'digest', 'sessionCount', 'sessionIds'];
const F5_F4_SNAPSHOT_KEYS = ['path', 'digest', 'projectionId', 'generatedAt', 'sourceSetDigest', 'recordCount'];
const F5_SOURCE_SET_KEYS = ['directory', 'pathPattern', 'validationMode', 'digest', 'entries'];
const F5_DECISION_ENTRY_KEYS = ['path', 'digest', 'receiptId', 'recommendationId', 'sessionId', 'presentedAt', 'decidedAt', 'disposition', 'correlationId', 'executionState', 'actionAuthority'];
const F5_EXECUTION_ENTRY_KEYS = ['path', 'digest', 'evidenceId', 'sessionId', 'recommendationId', 'decisionReceiptId', 'processingEvidenceRef', 'observedAt', 'executionState', 'actionAuthority'];
const F5_COHORT_KEYS = ['cohortId', 'selectionRuleId', 'populationCount', 'eligibleCount', 'memberRefs', 'evidenceState', 'reasonCodes', 'limitations'];
const F5_GATE_KEYS = ['gateId', 'state', 'reasonCodes'];
const F5_OUTCOMES_KEYS = ['technical', 'scientific', 'humanDecision', 'production', 'capabilityOutcome', 'closureRecommendation', 'aiModelImplemented'];
const F5_OUTCOME_KEYS = ['state', 'reasonCodes'];
const F5_SUMMARY_KEYS = ['canonicalSessions', 'provenanceEligible', 'humanDecisionReceipts', 'executionEvidence', 'uncorrelatedProcessingSources', 'targetDistribution'];
const F5_TARGET_COUNT_KEYS = ['target', 'count'];

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const nonEmpty = value => typeof value === 'string' && value.trim().length > 0;
const sorted = values => [...values].sort((left, right) => left.localeCompare(right));
const same = (left, right) => canonicalJson(left) === canonicalJson(right);

function exactKeys(value, expected, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} non valido`);
  assert(same(sorted(Object.keys(value)), sorted(expected)), `${label} contiene proprietà mancanti o sconosciute`);
}

function validateStringArray(value, label, { minItems = 0 } = {}) {
  assert(Array.isArray(value) && value.length >= minItems, `${label} non valido`);
  assert(value.every(nonEmpty) && new Set(value).size === value.length, `${label} contiene valori vuoti o duplicati`);
}

function assertNoForbiddenPublicFields(value, location = '$') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoForbiddenPublicFields(item, `${location}[${index}]`));
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_PUBLIC_KEYS.has(key), `${location}.${key} non è pubblicabile`);
    assertNoForbiddenPublicFields(child, `${location}.${key}`);
  }
}

function validateAuthority(authority) {
  exactKeys(authority, AUTHORITY_KEYS, 'authority');
  assert(authority.consumerMode === 'READ_ONLY', 'consumer mode non read-only');
  assert(authority.advisoryOnly === true, 'advisory boundary non valido');
  assert(authority.acceptanceAuthority === 'HUMAN_ONLY', 'acceptance authority drift');
  assert(authority.actionAuthority === 'NONE', 'action authority drift');
  assert(authority.executionAuthority === 'NONE', 'execution authority drift');
  assert(authority.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'Safety Authority drift');
  assert(authority.pixInsightApplyAuthorized === false, 'PixInsight apply authority drift');
  assert(authority.automaticAcceptanceAuthorized === false, 'automatic acceptance authority drift');
}

function validateSourceEntry(entry, index) {
  exactKeys(entry, SOURCE_ENTRY_KEYS, `sourceSet.entries[${index}]`);
  assert(PROVENANCE_PATH.test(entry.path ?? ''), `source path non autorizzato: ${entry.path ?? 'missing'}`);
  assert(DIGEST.test(entry.digest ?? ''), `source digest non valido: ${entry.path}`);
  assert(nonEmpty(entry.sidecarId) && entry.sidecarId.startsWith('PXP-'), `sidecarId non valido: ${entry.path}`);
  assert(Number.isFinite(Date.parse(entry.exportedAt)), `exportedAt non valido: ${entry.path}`);
  assert(nonEmpty(entry.sessionId), `sessionId source mancante: ${entry.path}`);
  assert(entry.target === null || nonEmpty(entry.target), `target source non valido: ${entry.path}`);
  assert(nonEmpty(entry.workflowId), `workflowId source mancante: ${entry.path}`);
  assert(COMPLETENESS.has(entry.completeness), `completeness source non valida: ${entry.path}`);
  assert(Array.isArray(entry.limitations), `limitations source non valide: ${entry.path}`);
}

function validateSubject(subject, sessionId) {
  exactKeys(subject, SUBJECT_KEYS, `subject.${sessionId}`);
  assert(nonEmpty(subject.subjectId), `subjectId mancante: ${sessionId}`);
  assert(SUBJECT_TYPES.has(subject.subjectType), `subjectType non valido: ${sessionId}`);
  for (const key of ['assetRef', 'sessionRef', 'workflowRef', 'stepRef']) {
    assert(subject[key] === null || typeof subject[key] === 'string', `${key} non valido: ${sessionId}`);
  }
  assert(SUBJECT_CORRELATION_STATES.has(subject.correlationState), `subject correlation non valida: ${sessionId}`);
}

function validateSourceBinding(binding, sessionId) {
  exactKeys(binding, BINDING_KEYS, `sourceBinding.${sessionId}`);
  assert(nonEmpty(binding.bindingId), `bindingId mancante: ${sessionId}`);
  assert(SEMANTIC_TYPES.has(binding.semanticType), `binding semanticType non valido: ${sessionId}`);
  assert(EVIDENCE_CLASSES.has(binding.evidenceClass), `evidenceClass non valida: ${sessionId}`);
  assert(SOURCE_AUTHORITIES.has(binding.sourceAuthority), `sourceAuthority non valida: ${sessionId}`);
  assert(nonEmpty(binding.sourceRef), `sourceRef mancante: ${sessionId}`);
  assert(LIFECYCLE_STATES.has(binding.lifecycleState), `binding lifecycle non valido: ${sessionId}`);
  assert(QUALITY_STATES.has(binding.quality), `binding quality non valida: ${sessionId}`);
  assert(COMPLETENESS.has(binding.completeness), `binding completeness non valida: ${sessionId}`);
  validateStringArray(binding.citationRefs, `binding citationRefs.${sessionId}`, { minItems: 1 });
  validateStringArray(binding.limitations, `binding limitations.${sessionId}`);
  assert(DIGEST.test(binding.bindingDigest ?? ''), `binding digest non valido: ${sessionId}`);
}

function validateParameterAdvice(item, sessionId) {
  exactKeys(item, PARAMETER_ADVICE_KEYS, `parameterAdvice.${sessionId}`);
  assert(item.parameterId === null || typeof item.parameterId === 'string', `parameterId non valido: ${sessionId}`);
  assert(PARAMETER_MODES.has(item.mode), `parameter mode non valido: ${sessionId}`);
  assert(item.unit === null || typeof item.unit === 'string', `parameter unit non valida: ${sessionId}`);
  assert(item.categoricalValue === null || typeof item.categoricalValue === 'string', `categorical value non valido: ${sessionId}`);
  assert(item.lowerBound === null || Number.isFinite(item.lowerBound), `lower bound non valido: ${sessionId}`);
  assert(item.upperBound === null || Number.isFinite(item.upperBound), `upper bound non valido: ${sessionId}`);
  assert(nonEmpty(item.applicability), `parameter applicability mancante: ${sessionId}`);
  validateStringArray(item.evidenceRefs, `parameter evidenceRefs.${sessionId}`);
  validateStringArray(item.limitations, `parameter limitations.${sessionId}`, { minItems: 1 });
  if (item.mode === 'UNKNOWN_NOT_RECOMMENDED') {
    assert(item.parameterId === null && item.unit === null && item.categoricalValue === null && item.lowerBound === null && item.upperBound === null, `unknown parameter advice contiene valori: ${sessionId}`);
  }
}

function validateRecommendation(recommendation, record, bindingIds) {
  exactKeys(recommendation, RECOMMENDATION_KEYS, `recommendation.${record.sessionId}`);
  assert(recommendation?.semanticType === 'recommendation', `semanticType recommendation non valido: ${record.sessionId}`);
  assert(recommendation.aiDerived === false, `AI-derived state non autorizzato: ${record.sessionId}`);
  assert(recommendation.producer === 'DSG.DeterministicAdvisoryDemonstrator', `producer recommendation non autorizzato: ${record.sessionId}`);
  assert(recommendation.methodId === METHOD_ID, `method recommendation non autorizzato: ${record.sessionId}`);
  assert(recommendation.generatedAt === record.generatedAt, `timestamp recommendation non allineato: ${record.sessionId}`);
  assert(recommendation.subjectRef === record.subject.subjectId, `subject recommendation non allineato: ${record.sessionId}`);
  assert(LIFECYCLE_STATES.has(recommendation.lifecycleState), `lifecycle recommendation non valido: ${record.sessionId}`);
  assert(RECOMMENDATION_CATEGORIES.has(recommendation.category), `category recommendation non valida: ${record.sessionId}`);
  assert(nonEmpty(recommendation.proposedAction) && nonEmpty(recommendation.rationale), `recommendation incompleta: ${record.sessionId}`);
  validateStringArray(recommendation.sourceBindingRefs, `recommendation sourceBindingRefs.${record.sessionId}`, { minItems: 1 });
  assert(recommendation.sourceBindingRefs.every(ref => bindingIds.has(ref)), `source binding sconosciuto: ${record.sessionId}`);
  validateStringArray(recommendation.citationRefs, `recommendation citationRefs.${record.sessionId}`, { minItems: 1 });
  validateStringArray(recommendation.provenanceRefs, `recommendation provenanceRefs.${record.sessionId}`, { minItems: 1 });
  validateStringArray(recommendation.conflicts, `recommendation conflicts.${record.sessionId}`);
  validateStringArray(recommendation.unknowns, `recommendation unknowns.${record.sessionId}`);
  validateStringArray(recommendation.limitations, `recommendation limitations.${record.sessionId}`, { minItems: 1 });
  exactKeys(recommendation.confidence, CONFIDENCE_KEYS, `confidence.${record.sessionId}`);
  assert(recommendation.confidence?.state === 'UNAVAILABLE_F2', `confidence state non autorizzato: ${record.sessionId}`);
  assert(recommendation.confidence?.contractRef === null, `confidence contract non autorizzato: ${record.sessionId}`);
  assert(recommendation.confidence?.value === null, `confidence numerica non autorizzata: ${record.sessionId}`);
  validateStringArray(recommendation.confidence.limitations, `confidence limitations.${record.sessionId}`, { minItems: 1 });
  assert(Array.isArray(recommendation.parameterAdvice), `parameter advice non valido: ${record.sessionId}`);
  recommendation.parameterAdvice.forEach(item => validateParameterAdvice(item, record.sessionId));
  assert(DIGEST.test(recommendation.recommendationDigest ?? ''), `recommendation digest non valido: ${record.sessionId}`);
}

function validateF5ReasonCodes(value, label) {
  assert(Array.isArray(value), `${label} non valido`);
  assert(value.every(code => F5_METHOD_REGISTRY.reasonCodes.includes(code)), `${label} contiene reason code sconosciuti`);
  assert(new Set(value).size === value.length, `${label} contiene duplicati`);
}

function validateF5SourceSet(value, { directory, pathPattern, pathExpression, entryKeys, type }) {
  exactKeys(value, F5_SOURCE_SET_KEYS, `sourceSnapshots.${type}`);
  assert(value.directory === directory, `${type} directory non autorizzata`);
  assert(value.pathPattern === pathPattern, `${type} pathPattern non autorizzato`);
  assert(value.validationMode === 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT', `${type} validationMode non supportato`);
  assert(DIGEST.test(value.digest ?? ''), `${type} digest non valido`);
  assert(Array.isArray(value.entries), `${type} entries non valide`);
  const paths = value.entries.map(entry => entry?.path);
  assert(paths.every(nonEmpty) && same(paths, sorted(paths)) && new Set(paths).size === paths.length, `${type} paths non canonici`);
  value.entries.forEach((entry, index) => {
    exactKeys(entry, entryKeys, `${type}.entries[${index}]`);
    assert(pathExpression.test(entry.path), `${type} path non autorizzato`);
    assert(DIGEST.test(entry.digest ?? ''), `${type} entry digest non valido`);
    assert(nonEmpty(entry.sessionId) && nonEmpty(entry.recommendationId), `${type} correlazione incompleta`);
    assert(entry.actionAuthority === 'NONE', `${type} action authority drift`);
    if (type === 'humanDecisionSourceSet') {
      assert(nonEmpty(entry.receiptId) && nonEmpty(entry.correlationId), `${type} identity incompleta`);
      assert(Number.isFinite(Date.parse(entry.presentedAt)) && Number.isFinite(Date.parse(entry.decidedAt)), `${type} timestamp non valido`);
      assert(Date.parse(entry.decidedAt) >= Date.parse(entry.presentedAt), `${type} sequenza temporale non valida`);
      assert(['ACCEPTED_FOR_MANUAL_APPLICATION', 'EDITED_FOR_MANUAL_APPLICATION', 'REJECTED', 'DEFERRED'].includes(entry.disposition), `${type} disposition non valida`);
      assert(entry.executionState === 'NOT_OBSERVED', `${type} execution state non autorizzato`);
    } else {
      assert(nonEmpty(entry.evidenceId) && nonEmpty(entry.decisionReceiptId), `${type} identity incompleta`);
      assert(PROVENANCE_PATH.test(entry.processingEvidenceRef ?? ''), `${type} processing evidence non autorizzata`);
      assert(Number.isFinite(Date.parse(entry.observedAt)), `${type} observedAt non valido`);
      assert(entry.executionState === 'OBSERVED_MANUAL_EXECUTION', `${type} execution state non autorizzato`);
    }
  });
}

export function validateRealEvidenceEvaluationContract(evaluation) {
  exactKeys(evaluation, F5_TOP_LEVEL_KEYS, 'evaluation');
  assert(evaluation.schemaVersion === F5_SCHEMA_VERSION, 'F5_SCHEMA_VERSION_UNSUPPORTED');
  assert(evaluation.evaluationType === F5_EVALUATION_TYPE, 'F5_EVALUATION_TYPE_UNSUPPORTED');
  assert(evaluation.evaluationState === F5_EVALUATION_STATE, 'F5_EVALUATION_STATE_UNSUPPORTED');
  assert(evaluation.identityMethod === F5_IDENTITY_METHOD, 'F5_IDENTITY_METHOD_UNSUPPORTED');
  assert(evaluation.producer === F5_PRODUCER && evaluation.producerVersion === F5_PRODUCER_VERSION, 'F5_PRODUCER_UNSUPPORTED');
  assert(evaluation.methodId === F5_METHOD_ID, 'F5_METHOD_UNSUPPORTED');
  assert(/^BKL046-F5C-[A-F0-9]{24}$/.test(evaluation.evaluationId ?? ''), 'F5_EVALUATION_ID_INVALID');
  assert(Number.isFinite(Date.parse(evaluation.generatedAt)), 'F5_GENERATED_AT_INVALID');
  assert(DIGEST.test(evaluation.evaluationDigest ?? ''), 'F5_EVALUATION_DIGEST_INVALID');

  exactKeys(evaluation.sourceSnapshots, F5_SOURCE_SNAPSHOT_KEYS, 'sourceSnapshots');
  exactKeys(evaluation.sourceSnapshots.catalog, F5_CATALOG_SNAPSHOT_KEYS, 'sourceSnapshots.catalog');
  assert(evaluation.sourceSnapshots.catalog.path === CATALOG_PATH, 'F5_CATALOG_PATH_UNSUPPORTED');
  assert(DIGEST.test(evaluation.sourceSnapshots.catalog.digest ?? ''), 'F5_CATALOG_DIGEST_INVALID');
  validateStringArray(evaluation.sourceSnapshots.catalog.sessionIds, 'F5 catalog sessionIds');
  assert(same(evaluation.sourceSnapshots.catalog.sessionIds, sorted(evaluation.sourceSnapshots.catalog.sessionIds)), 'F5_CATALOG_SESSION_ORDER_INVALID');
  assert(evaluation.sourceSnapshots.catalog.sessionCount === evaluation.sourceSnapshots.catalog.sessionIds.length, 'F5_CATALOG_COUNT_INVALID');

  exactKeys(evaluation.sourceSnapshots.f4Projection, F5_F4_SNAPSHOT_KEYS, 'sourceSnapshots.f4Projection');
  const f4 = evaluation.sourceSnapshots.f4Projection;
  assert(f4.path === F5_PROJECTION_PATH, 'F5_F4_PATH_UNSUPPORTED');
  assert(DIGEST.test(f4.digest ?? '') && DIGEST.test(f4.sourceSetDigest ?? ''), 'F5_F4_DIGEST_INVALID');
  assert(/^BKL046-F4-[A-F0-9]{24}$/.test(f4.projectionId ?? ''), 'F5_F4_ID_INVALID');
  assert(Number.isFinite(Date.parse(f4.generatedAt)), 'F5_F4_GENERATED_AT_INVALID');
  assert(Number.isInteger(f4.recordCount) && f4.recordCount >= 0, 'F5_F4_RECORD_COUNT_INVALID');

  validateF5SourceSet(evaluation.sourceSnapshots.humanDecisionSourceSet, {
    directory: F5_HUMAN_DIRECTORY, pathPattern: F5_HUMAN_PATTERN, pathExpression: F5_HUMAN_PATH,
    entryKeys: F5_DECISION_ENTRY_KEYS, type: 'humanDecisionSourceSet'
  });
  validateF5SourceSet(evaluation.sourceSnapshots.executionEvidenceSourceSet, {
    directory: F5_EXECUTION_DIRECTORY, pathPattern: F5_EXECUTION_PATTERN, pathExpression: F5_EXECUTION_PATH,
    entryKeys: F5_EXECUTION_ENTRY_KEYS, type: 'executionEvidenceSourceSet'
  });

  assert(same(evaluation.methodRegistry, F5_METHOD_REGISTRY), 'F5_METHOD_REGISTRY_DRIFT');
  assert(Array.isArray(evaluation.cohorts) && evaluation.cohorts.length === F5_METHOD_REGISTRY.cohortIds.length, 'F5_COHORTS_INCOMPLETE');
  evaluation.cohorts.forEach((cohort, index) => {
    exactKeys(cohort, F5_COHORT_KEYS, `cohorts[${index}]`);
    assert(cohort.cohortId === F5_METHOD_REGISTRY.cohortIds[index], `F5_COHORT_ID_MISMATCH:${index}`);
    assert(cohort.selectionRuleId === F5_METHOD_REGISTRY.selectionRuleIds[index], `F5_SELECTION_RULE_MISMATCH:${index}`);
    assert(Number.isInteger(cohort.populationCount) && cohort.populationCount >= 0, `F5_COHORT_POPULATION_INVALID:${index}`);
    assert(Number.isInteger(cohort.eligibleCount) && cohort.eligibleCount >= 0, `F5_COHORT_ELIGIBLE_INVALID:${index}`);
    validateStringArray(cohort.memberRefs, `cohorts[${index}].memberRefs`);
    assert(same(cohort.memberRefs, sorted(cohort.memberRefs)), `F5_COHORT_ORDER_INVALID:${index}`);
    assert(cohort.eligibleCount === cohort.memberRefs.length && cohort.eligibleCount <= cohort.populationCount, `F5_COHORT_COUNT_MISMATCH:${index}`);
    assert(F5_METHOD_REGISTRY.evidenceStates.includes(cohort.evidenceState), `F5_EVIDENCE_STATE_UNKNOWN:${index}`);
    if (cohort.eligibleCount === 0) assert(cohort.evidenceState !== 'AVAILABLE', `F5_EMPTY_COHORT_AVAILABLE:${index}`);
    validateF5ReasonCodes(cohort.reasonCodes, `cohorts[${index}].reasonCodes`);
    validateStringArray(cohort.limitations, `cohorts[${index}].limitations`, { minItems: 1 });
  });

  assert(Array.isArray(evaluation.technicalGates) && evaluation.technicalGates.length === F5_METHOD_REGISTRY.technicalGateIds.length, 'F5_TECHNICAL_GATES_INCOMPLETE');
  evaluation.technicalGates.forEach((gate, index) => {
    exactKeys(gate, F5_GATE_KEYS, `technicalGates[${index}]`);
    assert(gate.gateId === F5_METHOD_REGISTRY.technicalGateIds[index], `F5_GATE_ID_MISMATCH:${index}`);
    assert(F5_METHOD_REGISTRY.gateStates.includes(gate.state), `F5_GATE_STATE_UNKNOWN:${index}`);
    validateF5ReasonCodes(gate.reasonCodes, `technicalGates[${index}].reasonCodes`);
  });

  exactKeys(evaluation.outcomes, F5_OUTCOMES_KEYS, 'outcomes');
  for (const axis of ['technical', 'scientific', 'humanDecision', 'production']) {
    exactKeys(evaluation.outcomes[axis], F5_OUTCOME_KEYS, `outcomes.${axis}`);
    validateF5ReasonCodes(evaluation.outcomes[axis].reasonCodes, `outcomes.${axis}.reasonCodes`);
  }
  assert(F5_METHOD_REGISTRY.technicalStates.includes(evaluation.outcomes.technical.state), 'F5_TECHNICAL_STATE_UNKNOWN');
  assert(F5_METHOD_REGISTRY.scientificStates.includes(evaluation.outcomes.scientific.state), 'F5_SCIENTIFIC_STATE_UNKNOWN');
  assert(F5_METHOD_REGISTRY.humanDecisionStates.includes(evaluation.outcomes.humanDecision.state), 'F5_HUMAN_STATE_UNKNOWN');
  assert(F5_METHOD_REGISTRY.productionStates.includes(evaluation.outcomes.production.state), 'F5_PRODUCTION_STATE_UNKNOWN');
  assert(F5_METHOD_REGISTRY.capabilityOutcomes.includes(evaluation.outcomes.capabilityOutcome), 'F5_CAPABILITY_OUTCOME_UNKNOWN');
  assert(F5_METHOD_REGISTRY.closureRecommendations.includes(evaluation.outcomes.closureRecommendation), 'F5_CLOSURE_UNKNOWN');
  assert(evaluation.outcomes.aiModelImplemented === false, 'F5_AI_MODEL_CLAIM_FORBIDDEN');
  assert(evaluation.technicalGates.every(gate => gate.state === 'PASS' && gate.reasonCodes.length === 0), 'F5_TECHNICAL_GATES_NOT_ACCEPTED');
  assert(evaluation.outcomes.technical.state === 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS', 'F5_TECHNICAL_ACCEPTANCE_INVALID');
  assert(evaluation.outcomes.scientific.state === 'NOT_EVALUABLE_CURRENT_EVIDENCE', 'F5_SCIENTIFIC_EFFECTIVENESS_CLAIM_FORBIDDEN');
  assert(evaluation.outcomes.production.state === 'NOT_READY_FOR_PRODUCTION', 'F5_PRODUCTION_READINESS_CLAIM_FORBIDDEN');
  assert(evaluation.outcomes.capabilityOutcome === 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS', 'F5_CAPABILITY_OUTCOME_INVALID');
  assert(evaluation.outcomes.closureRecommendation === 'CLOSE_DETERMINISTIC_CAPABILITY', 'F5_CAPABILITY_CLOSURE_INVALID');

  exactKeys(evaluation.summary, F5_SUMMARY_KEYS, 'F5 summary');
  for (const key of F5_SUMMARY_KEYS.slice(0, 5)) assert(Number.isInteger(evaluation.summary[key]) && evaluation.summary[key] >= 0, `F5_SUMMARY_INVALID:${key}`);
  assert(Array.isArray(evaluation.summary.targetDistribution), 'F5_TARGET_DISTRIBUTION_INVALID');
  evaluation.summary.targetDistribution.forEach((item, index) => {
    exactKeys(item, F5_TARGET_COUNT_KEYS, `targetDistribution[${index}]`);
    assert(nonEmpty(item.target) && Number.isInteger(item.count) && item.count > 0, `F5_TARGET_COUNT_INVALID:${index}`);
  });
  validateAuthority(evaluation.authority);
  validateStringArray(evaluation.limitations, 'F5 limitations', { minItems: 1 });
  assertNoForbiddenPublicFields(evaluation);
  return true;
}

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

export async function sha256(value, cryptoProvider = globalThis.crypto) {
  assert(cryptoProvider?.subtle && globalThis.TextEncoder, 'WEB_CRYPTO_SHA256_UNAVAILABLE');
  const bytes = new TextEncoder().encode(canonicalJson(value));
  const digest = await cryptoProvider.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
}

export function validateAdvisoryProjectionContract(projection) {
  exactKeys(projection, PROJECTION_KEYS, 'projection');
  assert(projection.schemaVersion === SCHEMA_VERSION, 'SCHEMA_VERSION_UNSUPPORTED');
  assert(projection.projectionType === PROJECTION_TYPE, 'PROJECTION_TYPE_UNSUPPORTED');
  assert(projection.projectionState === PROJECTION_STATE, 'PROJECTION_STATE_UNSUPPORTED');
  assert(projection.identityMethod === IDENTITY_METHOD, 'IDENTITY_METHOD_UNSUPPORTED');
  assert(projection.producer === PRODUCER && projection.producerVersion === PRODUCER_VERSION, 'PRODUCER_UNSUPPORTED');
  assert(projection.methodId === METHOD_ID, 'METHOD_UNSUPPORTED');
  assert(Number.isFinite(Date.parse(projection.generatedAt)), 'GENERATED_AT_INVALID');
  assert(/^BKL046-F4-[A-F0-9]{24}$/.test(projection.projectionId ?? ''), 'PROJECTION_ID_INVALID');
  assert(DIGEST.test(projection.projectionDigest ?? ''), 'PROJECTION_DIGEST_INVALID');
  assert(Array.isArray(projection.limitations) && projection.limitations.length > 0, 'PROJECTION_LIMITATIONS_MISSING');

  exactKeys(projection.sourceCatalog, CATALOG_KEYS, 'sourceCatalog');
  assert(projection.sourceCatalog.path === CATALOG_PATH, 'SOURCE_CATALOG_PATH_UNSUPPORTED');
  assert(DIGEST.test(projection.sourceCatalog.digest ?? ''), 'SOURCE_CATALOG_DIGEST_INVALID');
  assert(Number.isInteger(projection.sourceCatalog.sessionCount) && projection.sourceCatalog.sessionCount >= 0, 'SOURCE_CATALOG_COUNT_INVALID');
  assert(Array.isArray(projection.sourceCatalog.sessionIds), 'SOURCE_CATALOG_SESSION_IDS_INVALID');

  exactKeys(projection.sourceSet, SOURCE_SET_KEYS, 'sourceSet');
  assert(projection.sourceSet.validationMode === 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT', 'SOURCE_VALIDATION_MODE_UNSUPPORTED');
  assert(DIGEST.test(projection.sourceSet.digest ?? ''), 'SOURCE_SET_DIGEST_INVALID');
  assert(Array.isArray(projection.sourceSet.entries), 'SOURCE_SET_ENTRIES_INVALID');
  projection.sourceSet.entries.forEach(validateSourceEntry);
  const sourcePaths = projection.sourceSet.entries.map(entry => entry.path);
  assert(same(sourcePaths, sorted(sourcePaths)) && new Set(sourcePaths).size === sourcePaths.length, 'SOURCE_SET_ORDER_OR_IDENTITY_INVALID');

  exactKeys(projection.summary, SUMMARY_KEYS, 'summary');
  SUMMARY_KEYS.forEach(key => assert(Number.isInteger(projection.summary[key]) && projection.summary[key] >= 0, `summary.${key} non valido`));
  validateAuthority(projection.authority);
  assert(Array.isArray(projection.records), 'RECORDS_INVALID');

  const sourcePathSet = new Set(sourcePaths);
  const sessionIds = projection.records.map(record => record?.sessionId);
  assert(sessionIds.every(nonEmpty), 'RECORD_SESSION_ID_MISSING');
  assert(same(sessionIds, sorted(sessionIds)) && new Set(sessionIds).size === sessionIds.length, 'RECORD_ORDER_OR_IDENTITY_INVALID');
  projection.records.forEach(record => {
    exactKeys(record, RECORD_KEYS, `record.${record?.sessionId ?? 'unknown'}`);
    assert(/^F4-[A-F0-9]{24}$/.test(record.recordId ?? ''), `recordId non valido: ${record.sessionId}`);
    assert(record.target === null || nonEmpty(record.target), `target non valido: ${record.sessionId}`);
    assert(CORRELATION_STATES.has(record.correlationState), `correlation state non valido: ${record.sessionId}`);
    assert(Array.isArray(record.sourceRefs) && same(record.sourceRefs, sorted(record.sourceRefs)), `source refs non ordinati: ${record.sessionId}`);
    assert(record.sourceRefs.every(ref => sourcePathSet.has(ref)), `source ref sconosciuto: ${record.sessionId}`);
    assert(DIGEST.test(record.inputArtifactDigest ?? '') && DIGEST.test(record.recordDigest ?? ''), `record digest non valido: ${record.sessionId}`);
    assert(record.decisionState === 'NOT_PRESENT_PRE_DECISION', `human decision implicita: ${record.sessionId}`);
    validateSubject(record.subject, record.sessionId);
    assert(Array.isArray(record.sourceBindings) && record.sourceBindings.length > 0, `source bindings mancanti: ${record.sessionId}`);
    record.sourceBindings.forEach(binding => validateSourceBinding(binding, record.sessionId));
    const bindingIds = new Set(record.sourceBindings.map(binding => binding?.bindingId));
    assert(bindingIds.size === record.sourceBindings.length && [...bindingIds].every(nonEmpty), `source binding identity non valida: ${record.sessionId}`);
    assert(Array.isArray(record.recommendations) && record.recommendations.length === 2, `recommendations non bounded: ${record.sessionId}`);
    const recommendationIds = new Set(record.recommendations.map(item => item?.recommendationId));
    assert(recommendationIds.size === 2 && [...recommendationIds].every(nonEmpty), `recommendation identity non valida: ${record.sessionId}`);
    const context = { ...record, generatedAt: projection.generatedAt };
    record.recommendations.forEach(item => validateRecommendation(item, context, bindingIds));
    assert(Array.isArray(record.ruleEvaluations) && record.ruleEvaluations.length === 2, `rule evaluations non bounded: ${record.sessionId}`);
    const ruleIds = new Set();
    record.ruleEvaluations.forEach(item => {
      exactKeys(item, RULE_KEYS, `ruleEvaluation.${record.sessionId}`);
      assert(RULE_IDS.has(item.ruleId) && !ruleIds.has(item.ruleId), `rule identity non valida: ${record.sessionId}`);
      ruleIds.add(item.ruleId);
      assert(DECISIONS.has(item.decision), `rule decision non valida: ${record.sessionId}`);
      assert(recommendationIds.has(item.recommendationId), `rule recommendation ref non valida: ${record.sessionId}`);
      assert(Array.isArray(item.reasonCodes), `rule reason codes non validi: ${record.sessionId}`);
      assert((item.decision === 'PASS') === (item.reasonCodes.length === 0), `rule decision/reason mismatch: ${record.sessionId}`);
    });
  });
  assertNoForbiddenPublicFields(projection);
  return true;
}

export async function validateAdvisoryProjectionFreshness(projection, catalog, cryptoProvider = globalThis.crypto) {
  validateAdvisoryProjectionContract(projection);
  assert(catalog?.catalogStatus === 'VERSIONED_ANALYTICS_PROJECTION', 'SOURCE_CATALOG_STATUS_UNSUPPORTED');
  assert(Array.isArray(catalog.sessions), 'SOURCE_CATALOG_SESSIONS_MISSING');

  const catalogIds = sorted(catalog.sessions.map(session => session?.sessionId));
  assert(catalogIds.every(nonEmpty) && new Set(catalogIds).size === catalogIds.length, 'SOURCE_CATALOG_SESSION_ID_INVALID');
  assert(await sha256(catalog, cryptoProvider) === projection.sourceCatalog.digest, 'STALE_SOURCE_CATALOG_DIGEST_MISMATCH');
  assert(same(catalogIds, projection.sourceCatalog.sessionIds), 'STALE_SESSION_SET_MISMATCH');
  assert(catalogIds.length === projection.sourceCatalog.sessionCount, 'STALE_SESSION_COUNT_MISMATCH');

  assert(await sha256(projection.sourceSet.entries, cryptoProvider) === projection.sourceSet.digest, 'SOURCE_SET_DIGEST_MISMATCH');
  const expectedProjectionId = `BKL046-F4-${(await sha256({
    catalogDigest: projection.sourceCatalog.digest,
    methodId: projection.methodId,
    sourceSetDigest: projection.sourceSet.digest
  }, cryptoProvider)).slice(0, 24).toUpperCase()}`;
  assert(projection.projectionId === expectedProjectionId, 'PROJECTION_ID_MISMATCH');

  for (const record of projection.records) {
    const expectedRecordId = `F4-${(await sha256({ sessionId: record.sessionId, sourceRefs: record.sourceRefs }, cryptoProvider)).slice(0, 24).toUpperCase()}`;
    assert(record.recordId === expectedRecordId, `RECORD_ID_MISMATCH:${record.sessionId}`);
    assert(await sha256({ correlationState: record.correlationState, sourceBindings: record.sourceBindings, subject: record.subject }, cryptoProvider) === record.inputArtifactDigest, `INPUT_ARTIFACT_DIGEST_MISMATCH:${record.sessionId}`);
    for (const binding of record.sourceBindings) {
      const preimage = structuredClone(binding);
      const digest = preimage.bindingDigest;
      delete preimage.bindingDigest;
      assert(DIGEST.test(digest ?? '') && await sha256(preimage, cryptoProvider) === digest, `SOURCE_BINDING_DIGEST_MISMATCH:${record.sessionId}`);
    }
    for (const recommendation of record.recommendations) {
      const preimage = structuredClone(recommendation);
      const digest = preimage.recommendationDigest;
      delete preimage.recommendationDigest;
      assert(await sha256(preimage, cryptoProvider) === digest, `RECOMMENDATION_DIGEST_MISMATCH:${record.sessionId}`);
    }
    const preimage = structuredClone(record);
    delete preimage.recordDigest;
    assert(await sha256(preimage, cryptoProvider) === record.recordDigest, `RECORD_DIGEST_MISMATCH:${record.sessionId}`);
  }

  const recordIds = projection.records.map(record => record.sessionId);
  assert(same(recordIds, projection.sourceCatalog.sessionIds), 'PROJECTION_SESSION_SET_MISMATCH');
  assert(projection.records.length === projection.summary.totalSessions, 'SUMMARY_TOTAL_MISMATCH');
  const countCorrelation = state => projection.records.filter(record => record.correlationState === state).length;
  assert(projection.summary.provenanceMatched === countCorrelation('PROVENANCE_MATCHED'), 'SUMMARY_MATCHED_MISMATCH');
  assert(projection.summary.provenanceUnavailable === countCorrelation('PROVENANCE_UNAVAILABLE'), 'SUMMARY_UNAVAILABLE_MISMATCH');
  assert(projection.summary.correlationAmbiguous === countCorrelation('CORRELATION_AMBIGUOUS'), 'SUMMARY_AMBIGUOUS_MISMATCH');
  assert(projection.summary.correlationInvalid === countCorrelation('CORRELATION_INVALID'), 'SUMMARY_INVALID_MISMATCH');
  const countRule = (ruleId, decision) => projection.records.reduce((total, record) => total + Number(record.ruleEvaluations.some(item => item.ruleId === ruleId && item.decision === decision)), 0);
  assert(projection.summary.governancePass === countRule('GOVERNANCE_READINESS', 'PASS'), 'SUMMARY_GOVERNANCE_PASS_MISMATCH');
  assert(projection.summary.governanceFailClosed === countRule('GOVERNANCE_READINESS', 'FAIL_CLOSED'), 'SUMMARY_GOVERNANCE_FAIL_MISMATCH');
  assert(projection.summary.processingHistoryPass === countRule('PROCESSING_HISTORY_AVAILABILITY', 'PASS'), 'SUMMARY_HISTORY_PASS_MISMATCH');
  assert(projection.summary.processingHistoryFailClosed === countRule('PROCESSING_HISTORY_AVAILABILITY', 'FAIL_CLOSED'), 'SUMMARY_HISTORY_FAIL_MISMATCH');
  const catalogSet = new Set(catalogIds);
  assert(projection.summary.uncorrelatedSources === projection.sourceSet.entries.filter(entry => !catalogSet.has(entry.sessionId)).length, 'SUMMARY_UNCORRELATED_SOURCE_MISMATCH');

  const projectionPreimage = structuredClone(projection);
  delete projectionPreimage.projectionDigest;
  assert(await sha256(projectionPreimage, cryptoProvider) === projection.projectionDigest, 'PROJECTION_DIGEST_MISMATCH');
  return true;
}

export async function validateRealEvidenceEvaluationFreshness(evaluation, projection, catalog, cryptoProvider = globalThis.crypto) {
  validateRealEvidenceEvaluationContract(evaluation);
  await validateAdvisoryProjectionFreshness(projection, catalog, cryptoProvider);

  const snapshots = evaluation.sourceSnapshots;
  const catalogIds = sorted(catalog.sessions.map(session => session.sessionId));
  assert(await sha256(catalog, cryptoProvider) === snapshots.catalog.digest, 'STALE_F5_CATALOG_DIGEST_MISMATCH');
  assert(same(catalogIds, snapshots.catalog.sessionIds), 'STALE_F5_CATALOG_SESSION_SET_MISMATCH');
  assert(catalogIds.length === snapshots.catalog.sessionCount, 'STALE_F5_CATALOG_SESSION_COUNT_MISMATCH');

  assert(snapshots.f4Projection.digest === projection.projectionDigest, 'STALE_F5_PROJECTION_DIGEST_MISMATCH');
  assert(snapshots.f4Projection.projectionId === projection.projectionId, 'STALE_F5_PROJECTION_ID_MISMATCH');
  assert(snapshots.f4Projection.generatedAt === projection.generatedAt, 'STALE_F5_PROJECTION_TIMESTAMP_MISMATCH');
  assert(snapshots.f4Projection.sourceSetDigest === projection.sourceSet.digest, 'STALE_F5_PROJECTION_SOURCE_SET_MISMATCH');
  assert(snapshots.f4Projection.recordCount === projection.records.length, 'STALE_F5_PROJECTION_RECORD_COUNT_MISMATCH');

  const humanSet = snapshots.humanDecisionSourceSet;
  const executionSet = snapshots.executionEvidenceSourceSet;
  assert(await sha256(humanSet.entries, cryptoProvider) === humanSet.digest, 'F5_HUMAN_SOURCE_SET_DIGEST_MISMATCH');
  assert(await sha256(executionSet.entries, cryptoProvider) === executionSet.digest, 'F5_EXECUTION_SOURCE_SET_DIGEST_MISMATCH');

  const expectedEvaluationId = `BKL046-F5C-${(await sha256({
    catalogDigest: snapshots.catalog.digest,
    executionEvidenceDigest: executionSet.digest,
    f4ProjectionDigest: snapshots.f4Projection.digest,
    humanDecisionDigest: humanSet.digest,
    methodId: evaluation.methodId
  }, cryptoProvider)).slice(0, 24).toUpperCase()}`;
  assert(evaluation.evaluationId === expectedEvaluationId, 'F5_EVALUATION_ID_MISMATCH');

  const recommendationMap = new Map();
  for (const record of projection.records) {
    for (const recommendation of record.recommendations) {
      assert(!recommendationMap.has(recommendation.recommendationId), `F5_DUPLICATE_RECOMMENDATION:${recommendation.recommendationId}`);
      recommendationMap.set(recommendation.recommendationId, { sessionId: record.sessionId, correlationId: recommendation.correlationId });
    }
  }
  const receiptMap = new Map();
  const decisionRecommendationIds = new Set();
  for (const entry of humanSet.entries) {
    const recommendation = recommendationMap.get(entry.recommendationId);
    assert(recommendation, `F5_HUMAN_UNKNOWN_RECOMMENDATION:${entry.receiptId}`);
    assert(recommendation.sessionId === entry.sessionId && recommendation.correlationId === entry.correlationId, `F5_HUMAN_CORRELATION_MISMATCH:${entry.receiptId}`);
    assert(!receiptMap.has(entry.receiptId), `F5_DUPLICATE_RECEIPT:${entry.receiptId}`);
    assert(!decisionRecommendationIds.has(entry.recommendationId), `F5_DUPLICATE_RECOMMENDATION_DECISION:${entry.recommendationId}`);
    receiptMap.set(entry.receiptId, entry);
    decisionRecommendationIds.add(entry.recommendationId);
  }
  const processingMap = new Map(projection.sourceSet.entries.map(entry => [entry.path, entry]));
  const executionIds = new Set();
  for (const entry of executionSet.entries) {
    assert(!executionIds.has(entry.evidenceId), `F5_DUPLICATE_EXECUTION_EVIDENCE:${entry.evidenceId}`);
    executionIds.add(entry.evidenceId);
    const receipt = receiptMap.get(entry.decisionReceiptId);
    assert(receipt && receipt.recommendationId === entry.recommendationId && receipt.sessionId === entry.sessionId, `F5_EXECUTION_DECISION_MISMATCH:${entry.evidenceId}`);
    const processing = processingMap.get(entry.processingEvidenceRef);
    assert(processing?.sessionId === entry.sessionId, `F5_EXECUTION_PROCESSING_MISMATCH:${entry.evidenceId}`);
    assert(Date.parse(entry.observedAt) >= Date.parse(receipt.decidedAt), `F5_EXECUTION_TIME_MISMATCH:${entry.evidenceId}`);
  }

  const provenanceMembers = projection.records.filter(record => record.correlationState === 'PROVENANCE_MATCHED').map(record => record.sessionId).sort();
  const expectedCohortMembers = [
    catalogIds,
    provenanceMembers,
    humanSet.entries.map(entry => entry.receiptId).sort(),
    executionSet.entries.map(entry => entry.evidenceId).sort()
  ];
  const expectedPopulations = [catalogIds.length, catalogIds.length, recommendationMap.size, humanSet.entries.length];
  evaluation.cohorts.forEach((cohort, index) => {
    assert(same(cohort.memberRefs, expectedCohortMembers[index]), `F5_COHORT_MEMBERSHIP_MISMATCH:${index}`);
    assert(cohort.populationCount === expectedPopulations[index], `F5_COHORT_POPULATION_MISMATCH:${index}`);
  });

  const expectedGates = [
    ['CATALOG_SNAPSHOT_INTEGRITY', 'PASS', []],
    ['F4_PROJECTION_INTEGRITY', 'PASS', []],
    ['FULL_POPULATION_COVERAGE', 'PASS', []],
    ['HUMAN_DECISION_SOURCE_CONTRACT', 'PASS', []],
    ['EXECUTION_EVIDENCE_SOURCE_CONTRACT', 'PASS', []],
    ['CLOSED_METHOD_REGISTRY', 'PASS', []],
    ['F5A_REPORT_DETERMINISM', 'PASS', []],
    ['F5B_DYNAMIC_UPDATE', 'PASS', []],
    ['F5B_CONSUMER', 'PASS', []]
  ].map(([gateId, state, reasonCodes]) => ({ gateId, state, reasonCodes }));
  assert(same(evaluation.technicalGates, expectedGates), 'F5_TECHNICAL_GATES_STATE_MISMATCH');
  const expectedOutcomes = {
    technical: { state: 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS', reasonCodes: ['F5A_FOUNDATION_IMPLEMENTED', 'F5B_CONSUMER_VERIFIED', 'F5B_DYNAMIC_UPDATE_VERIFIED'] },
    scientific: { state: 'NOT_EVALUABLE_CURRENT_EVIDENCE', reasonCodes: ['NO_APPROVED_GROUND_TRUTH_METHOD', ...(provenanceMembers.length ? [] : ['NO_EXACT_PROVENANCE_MATCHES'])].sort() },
    humanDecision: { state: humanSet.entries.length ? 'AVAILABLE' : 'NOT_AVAILABLE', reasonCodes: [humanSet.entries.length ? 'HUMAN_DECISION_RECEIPTS_AVAILABLE' : 'NO_HUMAN_DECISION_RECEIPTS'] },
    production: { state: 'NOT_READY_FOR_PRODUCTION', reasonCodes: ['PRODUCTION_AUTHORITY_NOT_GRANTED', 'SCIENTIFIC_EFFECTIVENESS_NOT_ESTABLISHED'] },
    capabilityOutcome: 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS',
    closureRecommendation: 'CLOSE_DETERMINISTIC_CAPABILITY',
    aiModelImplemented: false
  };
  assert(same(evaluation.outcomes, expectedOutcomes), 'F5_OUTCOMES_STATE_MISMATCH');

  const targetCounts = new Map();
  for (const session of catalog.sessions) {
    const target = nonEmpty(session.target) ? session.target : 'UNKNOWN';
    targetCounts.set(target, (targetCounts.get(target) ?? 0) + 1);
  }
  const targetDistribution = [...targetCounts.entries()].sort(([left], [right]) => left.localeCompare(right)).map(([target, count]) => ({ target, count }));
  const expectedSummary = {
    canonicalSessions: catalogIds.length,
    provenanceEligible: provenanceMembers.length,
    humanDecisionReceipts: humanSet.entries.length,
    executionEvidence: executionSet.entries.length,
    uncorrelatedProcessingSources: projection.summary.uncorrelatedSources,
    targetDistribution
  };
  assert(same(evaluation.summary, expectedSummary), 'F5_SUMMARY_MISMATCH');

  const evaluationPreimage = structuredClone(evaluation);
  delete evaluationPreimage.evaluationDigest;
  assert(await sha256(evaluationPreimage, cryptoProvider) === evaluation.evaluationDigest, 'F5_EVALUATION_DIGEST_MISMATCH');
  return true;
}
