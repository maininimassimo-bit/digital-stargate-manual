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
  'hostId', 'workspaceId', 'absolutePath', 'localPath', 'imageData', 'imageUri', 'credential', 'secret'
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

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const nonEmpty = value => typeof value === 'string' && value.trim().length > 0;
const sorted = values => [...values].sort((left, right) => left.localeCompare(right));
const same = (left, right) => canonicalJson(left) === canonicalJson(right);

function exactKeys(value, expected, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} non valido`);
  assert(same(sorted(Object.keys(value)), sorted(expected)), `${label} contiene proprietà mancanti o sconosciute`);
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

function validateRecommendation(recommendation, record, bindingIds) {
  assert(recommendation?.semanticType === 'recommendation', `semanticType recommendation non valido: ${record.sessionId}`);
  assert(recommendation.aiDerived === false, `AI-derived state non autorizzato: ${record.sessionId}`);
  assert(recommendation.producer === 'DSG.DeterministicAdvisoryDemonstrator', `producer recommendation non autorizzato: ${record.sessionId}`);
  assert(recommendation.methodId === METHOD_ID, `method recommendation non autorizzato: ${record.sessionId}`);
  assert(recommendation.generatedAt === record.generatedAt, `timestamp recommendation non allineato: ${record.sessionId}`);
  assert(recommendation.subjectRef === record.subject.subjectId, `subject recommendation non allineato: ${record.sessionId}`);
  assert(['validated', 'incomplete'].includes(recommendation.lifecycleState), `lifecycle recommendation non valido: ${record.sessionId}`);
  assert(nonEmpty(recommendation.proposedAction) && nonEmpty(recommendation.rationale), `recommendation incompleta: ${record.sessionId}`);
  assert(Array.isArray(recommendation.sourceBindingRefs), `source binding refs non valide: ${record.sessionId}`);
  assert(recommendation.sourceBindingRefs.every(ref => bindingIds.has(ref)), `source binding sconosciuto: ${record.sessionId}`);
  assert(recommendation.confidence?.state === 'UNAVAILABLE_F2', `confidence state non autorizzato: ${record.sessionId}`);
  assert(recommendation.confidence?.value === null, `confidence numerica non autorizzata: ${record.sessionId}`);
  assert(Array.isArray(recommendation.parameterAdvice), `parameter advice non valido: ${record.sessionId}`);
  assert(DIGEST.test(recommendation.recommendationDigest ?? ''), `recommendation digest non valido: ${record.sessionId}`);
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
    assert(Array.isArray(record.sourceBindings) && record.sourceBindings.length > 0, `source bindings mancanti: ${record.sessionId}`);
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
