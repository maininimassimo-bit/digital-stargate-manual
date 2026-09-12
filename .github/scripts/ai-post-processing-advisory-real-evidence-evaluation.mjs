import { createHash } from 'node:crypto';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

export const F5_SCHEMA_VERSION = '1.0';
export const F5_EVALUATION_TYPE = 'BKL046_F5_REAL_EVIDENCE_EVALUATION';
export const F5_EVALUATION_STATE = 'F5A_FOUNDATION_EVALUATED';
export const F5_IDENTITY_METHOD = 'BKL046-F5-CANONICAL-JSON-SHA256-1';
export const F5_PRODUCER = 'DSG.AiPostProcessingRealEvidenceEvaluator';
export const F5_PRODUCER_VERSION = '1.0.0-f5a';
export const F5_METHOD_ID = 'BKL046-F5A-CLOSED-EVALUATION-1';

export const CATALOG_PATH = 'docs/data/scientific-session-catalog.json';
export const F4_PROJECTION_PATH = 'docs/data/ai-post-processing-advisory-projection.json';
export const HUMAN_DECISION_DIRECTORY = 'docs/data/ai-post-processing-human-decisions';
export const EXECUTION_EVIDENCE_DIRECTORY = 'docs/data/ai-post-processing-execution-evidence';

const HUMAN_DECISION_PATH = /^docs\/data\/ai-post-processing-human-decisions\/BKL-046-F2-HDR-\d{8}T\d{6}Z-[A-Z0-9][A-Z0-9_-]{0,31}\.json$/;
const EXECUTION_EVIDENCE_PATH = /^docs\/data\/ai-post-processing-execution-evidence\/BKL-046-F5-EXE-\d{8}T\d{6}Z-[A-Z0-9][A-Z0-9_-]{0,31}\.json$/;
const PROCESSING_EVIDENCE_PATH = /^docs\/architecture\/scientific-assets\/evidence\/BKL-045-F3B-PXP-\d{8}T\d{9}Z-[A-Z0-9][A-Z0-9_-]{0,31}\.json$/;

const DISPOSITIONS = new Set([
  'ACCEPTED_FOR_MANUAL_APPLICATION',
  'EDITED_FOR_MANUAL_APPLICATION',
  'REJECTED',
  'DEFERRED'
]);

const AUTHORITY = Object.freeze({
  consumerMode: 'READ_ONLY',
  advisoryOnly: true,
  acceptanceAuthority: 'HUMAN_ONLY',
  actionAuthority: 'NONE',
  executionAuthority: 'NONE',
  safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS',
  pixInsightApplyAuthorized: false,
  automaticAcceptanceAuthorized: false
});

export const F5_METHOD_REGISTRY = Object.freeze({
  registryId: 'BKL046-F5A-CLOSED-REGISTRY-1',
  cohortIds: [
    'ALL-CANONICAL-SESSIONS-F5',
    'EXACT-PROVENANCE-MATCHED-F5',
    'HUMAN-DECISION-RECEIPTS-F5',
    'EXECUTION-EVIDENCE-F5'
  ],
  selectionRuleIds: [
    'ALL-CANONICAL-SESSIONS-EXACT-SET-1',
    'F4-PROVENANCE-MATCHED-EXACT-1',
    'F2-HUMAN-DECISION-EXACT-CORRELATION-1',
    'F5-EXECUTION-EVIDENCE-EXACT-CORRELATION-1'
  ],
  technicalGateIds: [
    'CATALOG_SNAPSHOT_INTEGRITY',
    'F4_PROJECTION_INTEGRITY',
    'FULL_POPULATION_COVERAGE',
    'HUMAN_DECISION_SOURCE_CONTRACT',
    'EXECUTION_EVIDENCE_SOURCE_CONTRACT',
    'CLOSED_METHOD_REGISTRY',
    'F5A_REPORT_DETERMINISM',
    'F5B_DYNAMIC_UPDATE',
    'F5B_CONSUMER'
  ],
  technicalStates: [
    'READY_FOR_F5_EVALUATION',
    'NOT_ACCEPTED',
    'REJECTED',
    'ACCEPTED_READ_ONLY_WITH_LIMITATIONS'
  ],
  scientificStates: [
    'NOT_EVALUABLE_CURRENT_EVIDENCE',
    'EVALUATION_REQUIRED',
    'INVALID'
  ],
  humanDecisionStates: [
    'NOT_AVAILABLE',
    'AVAILABLE'
  ],
  productionStates: [
    'NOT_READY_FOR_PRODUCTION',
    'REJECTED_FOR_PRODUCTION'
  ],
  capabilityOutcomes: [
    'F5A_EVALUATION_FOUNDATION_READY',
    'NOT_ACCEPTED',
    'REJECTED',
    'ACCEPTED_READ_ONLY_WITH_LIMITATIONS'
  ],
  closureRecommendations: [
    'KEEP_OPEN',
    'DO_NOT_CLOSE',
    'CLOSE_DETERMINISTIC_CAPABILITY'
  ],
  gateStates: [
    'PASS',
    'FAIL_CLOSED',
    'NOT_EXECUTED'
  ],
  evidenceStates: [
    'AVAILABLE',
    'NOT_AVAILABLE',
    'NOT_EVALUABLE'
  ],
  reasonCodes: [
    'FULL_CANONICAL_POPULATION',
    'NO_EXACT_PROVENANCE_MATCHES',
    'EXACT_PROVENANCE_AVAILABLE',
    'NO_HUMAN_DECISION_RECEIPTS',
    'HUMAN_DECISION_RECEIPTS_AVAILABLE',
    'NO_EXECUTION_EVIDENCE',
    'EXECUTION_EVIDENCE_AVAILABLE',
    'NO_APPROVED_GROUND_TRUTH_METHOD',
    'F5A_FOUNDATION_IMPLEMENTED',
    'F5B_DYNAMIC_UPDATE_NOT_EXECUTED',
    'F5B_CONSUMER_NOT_EXECUTED',
    'PRODUCTION_AUTHORITY_NOT_GRANTED',
    'SCIENTIFIC_EFFECTIVENESS_NOT_ESTABLISHED'
  ]
});

const TOP_LEVEL_KEYS = new Set([
  'schemaVersion', 'evaluationType', 'evaluationState', 'identityMethod', 'evaluationId',
  'generatedAt', 'producer', 'producerVersion', 'methodId', 'sourceSnapshots',
  'methodRegistry', 'cohorts', 'technicalGates', 'outcomes', 'summary',
  'authority', 'limitations', 'evaluationDigest'
]);
const SOURCE_SNAPSHOT_KEYS = new Set(['catalog', 'f4Projection', 'humanDecisionSourceSet', 'executionEvidenceSourceSet']);
const CATALOG_SNAPSHOT_KEYS = new Set(['path', 'digest', 'sessionCount', 'sessionIds']);
const F4_SNAPSHOT_KEYS = new Set(['path', 'digest', 'projectionId', 'generatedAt', 'sourceSetDigest', 'recordCount']);
const SOURCE_SET_KEYS = new Set(['directory', 'pathPattern', 'validationMode', 'digest', 'entries']);
const DECISION_ENTRY_KEYS = new Set([
  'path', 'digest', 'receiptId', 'recommendationId', 'sessionId', 'presentedAt',
  'decidedAt', 'disposition', 'correlationId', 'executionState', 'actionAuthority'
]);
const EXECUTION_ENTRY_KEYS = new Set([
  'path', 'digest', 'evidenceId', 'sessionId', 'recommendationId',
  'decisionReceiptId', 'processingEvidenceRef', 'observedAt',
  'executionState', 'actionAuthority'
]);
const COHORT_KEYS = new Set([
  'cohortId', 'selectionRuleId', 'populationCount', 'eligibleCount',
  'memberRefs', 'evidenceState', 'reasonCodes', 'limitations'
]);
const TECHNICAL_GATE_KEYS = new Set(['gateId', 'state', 'reasonCodes']);
const OUTCOMES_KEYS = new Set([
  'technical', 'scientific', 'humanDecision', 'production',
  'capabilityOutcome', 'closureRecommendation', 'aiModelImplemented'
]);
const OUTCOME_KEYS = new Set(['state', 'reasonCodes']);
const SUMMARY_KEYS = new Set([
  'canonicalSessions', 'provenanceEligible', 'humanDecisionReceipts',
  'executionEvidence', 'uncorrelatedProcessingSources', 'targetDistribution'
]);
const TARGET_COUNT_KEYS = new Set(['target', 'count']);
const RAW_DECISION_KEYS = new Set([
  'schemaVersion', 'sourceType', 'authority', 'sessionId',
  'recommendationId', 'receipt', 'artifactDigest'
]);
const RAW_RECEIPT_KEYS = new Set([
  'receiptId', 'recommendationId', 'presentedAt', 'decidedAt', 'actorRef',
  'disposition', 'decisionEdits', 'decisionRationale', 'correlationId',
  'executionState', 'executionEvidenceRefs', 'actionAuthority', 'receiptDigest'
]);
const RAW_EXECUTION_KEYS = new Set([
  'schemaVersion', 'sourceType', 'authority', 'evidenceId', 'sessionId',
  'recommendationId', 'decisionReceiptId', 'processingEvidenceRef',
  'observedAt', 'executionState', 'actionAuthority', 'artifactDigest'
]);
const FORBIDDEN_PUBLIC_KEYS = new Set([
  'actorRef', 'decisionRationale', 'decisionEdits', 'hostId', 'workspaceId',
  'absolutePath', 'localPath', 'imageData', 'imageUri', 'credential', 'secret'
]);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function assertExactKeys(value, allowed, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object.`);
  for (const key of Object.keys(value)) assert(allowed.has(key), `${label}.${key} is not allowed.`);
  for (const key of allowed) assert(Object.hasOwn(value, key), `${label}.${key} is required.`);
}

const nonEmpty = (value) => typeof value === 'string' && value.trim().length > 0;
const validDigest = (value) => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
const validDateTime = (value) => typeof value === 'string'
  && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$/.test(value)
  && Number.isFinite(Date.parse(value));

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

export function contentDigest(value) {
  return createHash('sha256').update(canonicalJson(value)).digest('hex');
}

function deepFreeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    Object.freeze(value);
    Object.values(value).forEach(deepFreeze);
  }
  return value;
}

function assertSortedUnique(values, label) {
  assert(Array.isArray(values), `${label} must be an array.`);
  assert(values.every(nonEmpty), `${label} must contain non-empty strings.`);
  assert(new Set(values).size === values.length, `${label} must be unique.`);
  assert(canonicalJson(values) === canonicalJson([...values].sort()), `${label} must be sorted.`);
}

function assertAllowedPath(repositoryPath, expression, label) {
  assert(nonEmpty(repositoryPath), `${label} path is required.`);
  assert(!path.isAbsolute(repositoryPath), `Absolute ${label} paths are forbidden.`);
  assert(!repositoryPath.includes('\\'), `Backslash ${label} paths are forbidden.`);
  assert(!repositoryPath.split('/').includes('..'), `${label} path traversal is forbidden.`);
  assert(expression.test(repositoryPath), `${label} path is outside the closed allowlist: ${repositoryPath}`);
  return true;
}

export function assertAllowedHumanDecisionPath(repositoryPath) {
  return assertAllowedPath(repositoryPath, HUMAN_DECISION_PATH, 'Human Decision');
}

export function assertAllowedExecutionEvidencePath(repositoryPath) {
  return assertAllowedPath(repositoryPath, EXECUTION_EVIDENCE_PATH, 'Execution evidence');
}

function validateDigestProtected(value, digestKey, label) {
  assert(validDigest(value?.[digestKey]), `${label} has an invalid ${digestKey}.`);
  const preimage = structuredClone(value);
  delete preimage[digestKey];
  assert(value[digestKey] === contentDigest(preimage), `${label} ${digestKey} mismatch.`);
}

export function validateRawHumanDecisionSource(repositoryPath, payload) {
  assertAllowedHumanDecisionPath(repositoryPath);
  assertExactKeys(payload, RAW_DECISION_KEYS, repositoryPath);
  assert(payload.schemaVersion === '1.0', `${repositoryPath} has an unsupported schemaVersion.`);
  assert(payload.sourceType === 'BKL046_HUMAN_DECISION_RECEIPT', `${repositoryPath} has an unsupported sourceType.`);
  assert(payload.authority === 'human_decision', `${repositoryPath} has unsupported authority.`);
  assert(nonEmpty(payload.sessionId) && nonEmpty(payload.recommendationId), `${repositoryPath} requires exact session and recommendation IDs.`);
  assertExactKeys(payload.receipt, RAW_RECEIPT_KEYS, `${repositoryPath}.receipt`);
  const receipt = payload.receipt;
  assert(nonEmpty(receipt.receiptId) && receipt.recommendationId === payload.recommendationId, `${repositoryPath} receipt identity mismatch.`);
  assert(validDateTime(receipt.presentedAt) && validDateTime(receipt.decidedAt), `${repositoryPath} has invalid receipt timestamps.`);
  assert(Date.parse(receipt.decidedAt) >= Date.parse(receipt.presentedAt), `${repositoryPath} decidedAt precedes presentedAt.`);
  assert(nonEmpty(receipt.actorRef) && nonEmpty(receipt.correlationId), `${repositoryPath} requires actorRef and correlationId.`);
  assert(DISPOSITIONS.has(receipt.disposition), `${repositoryPath} has unsupported disposition.`);
  assert(Array.isArray(receipt.decisionEdits), `${repositoryPath} decisionEdits must be an array.`);
  assert(receipt.decisionRationale === null || typeof receipt.decisionRationale === 'string', `${repositoryPath} decisionRationale is invalid.`);
  assert(receipt.executionState === 'NOT_OBSERVED', `${repositoryPath} cannot claim execution.`);
  assert(Array.isArray(receipt.executionEvidenceRefs) && receipt.executionEvidenceRefs.length === 0, `${repositoryPath} receipt cannot embed execution evidence.`);
  assert(receipt.actionAuthority === 'NONE', `${repositoryPath} escalates action authority.`);
  validateDigestProtected(receipt, 'receiptDigest', `${repositoryPath}.receipt`);
  validateDigestProtected(payload, 'artifactDigest', repositoryPath);
  return true;
}

export function validateRawExecutionEvidenceSource(repositoryPath, payload) {
  assertAllowedExecutionEvidencePath(repositoryPath);
  assertExactKeys(payload, RAW_EXECUTION_KEYS, repositoryPath);
  assert(payload.schemaVersion === '1.0', `${repositoryPath} has an unsupported schemaVersion.`);
  assert(payload.sourceType === 'BKL046_RECOMMENDATION_EXECUTION_EVIDENCE', `${repositoryPath} has an unsupported sourceType.`);
  assert(payload.authority === 'processing_execution_evidence', `${repositoryPath} has unsupported authority.`);
  for (const key of ['evidenceId', 'sessionId', 'recommendationId', 'decisionReceiptId']) {
    assert(nonEmpty(payload[key]), `${repositoryPath} requires ${key}.`);
  }
  assert(PROCESSING_EVIDENCE_PATH.test(payload.processingEvidenceRef ?? ''), `${repositoryPath} processingEvidenceRef is outside the BKL-045 allowlist.`);
  assert(validDateTime(payload.observedAt), `${repositoryPath} has invalid observedAt.`);
  assert(payload.executionState === 'OBSERVED_MANUAL_EXECUTION', `${repositoryPath} has unsupported executionState.`);
  assert(payload.actionAuthority === 'NONE', `${repositoryPath} escalates action authority.`);
  validateDigestProtected(payload, 'artifactDigest', repositoryPath);
  return true;
}

async function discoverSources(repositoryRoot, directory, prefix, validator) {
  const absoluteDirectory = path.join(repositoryRoot, directory);
  let entries;
  try {
    entries = await readdir(absoluteDirectory, { withFileTypes: true });
  } catch (error) {
    if (error?.code === 'ENOENT') return [];
    throw error;
  }
  for (const entry of entries) {
    assert(entry.isFile(), `Unknown non-file entry in governed source directory ${directory}: ${entry.name}`);
    assert(entry.name.startsWith(prefix) && entry.name.endsWith('.json'), `Unknown file in governed source directory ${directory}: ${entry.name}`);
  }
  const files = entries.map((entry) => entry.name).sort();
  const sources = [];
  for (const name of files) {
    const repositoryPath = `${directory}/${name}`;
    const payload = JSON.parse(await readFile(path.join(repositoryRoot, repositoryPath), 'utf8'));
    validator(repositoryPath, payload);
    sources.push({ path: repositoryPath, payload });
  }
  return sources;
}

export function discoverHumanDecisionSources(repositoryRoot = '.') {
  return discoverSources(repositoryRoot, HUMAN_DECISION_DIRECTORY, 'BKL-046-F2-HDR-', validateRawHumanDecisionSource);
}

export function discoverExecutionEvidenceSources(repositoryRoot = '.') {
  return discoverSources(repositoryRoot, EXECUTION_EVIDENCE_DIRECTORY, 'BKL-046-F5-EXE-', validateRawExecutionEvidenceSource);
}

function validateCatalog(catalog) {
  assert(catalog?.catalogStatus === 'VERSIONED_ANALYTICS_PROJECTION', 'Unsupported scientific catalog status.');
  assert(Array.isArray(catalog.sessions), 'Scientific catalog sessions are required.');
  const ids = catalog.sessions.map((session) => session?.sessionId);
  assert(ids.every(nonEmpty), 'Every catalog session requires a sessionId.');
  assert(new Set(ids).size === ids.length, 'Scientific catalog session IDs must be unique.');
}

function validateF4Projection(catalog, projection) {
  assert(projection?.schemaVersion === '1.1', 'Unsupported F4 projection schemaVersion.');
  assert(projection.projectionType === 'AI_POST_PROCESSING_ADVISORY_PROJECTION', 'Unsupported F4 projection type.');
  assert(projection.projectionState === 'PRE_DECISION_READ_ONLY', 'Unsupported F4 projection state.');
  validateDigestProtected(projection, 'projectionDigest', 'F4 projection');
  assert(projection.authority?.consumerMode === 'READ_ONLY' && projection.authority?.acceptanceAuthority === 'HUMAN_ONLY', 'F4 authority is not read-only/human-only.');
  assert(projection.authority?.actionAuthority === 'NONE' && projection.authority?.executionAuthority === 'NONE', 'F4 action or execution authority escalated.');
  assert(projection.authority?.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'F4 Safety Authority is invalid.');
  assert(projection.authority?.pixInsightApplyAuthorized === false && projection.authority?.automaticAcceptanceAuthorized === false, 'F4 apply or auto-accept escalation is forbidden.');
  assert(Array.isArray(projection.records) && Array.isArray(projection.sourceSet?.entries), 'F4 records and source entries are required.');
  const catalogIds = catalog.sessions.map((session) => session.sessionId).sort();
  const recordIds = projection.records.map((record) => record.sessionId).sort();
  assert(new Set(recordIds).size === recordIds.length, 'F4 record session IDs must be unique.');
  assert(canonicalJson(catalogIds) === canonicalJson(recordIds), 'F4 record set does not match the canonical catalog.');
  assert(projection.sourceCatalog?.path === CATALOG_PATH, 'F4 source catalog path is invalid.');
  assert(projection.sourceCatalog?.digest === contentDigest(catalog), 'F4 source catalog digest does not match the canonical catalog.');
  assert(canonicalJson([...projection.sourceCatalog.sessionIds].sort()) === canonicalJson(catalogIds), 'F4 source catalog session set mismatch.');
  assert(projection.sourceCatalog.sessionCount === catalogIds.length, 'F4 source catalog count mismatch.');
}

function sanitizeHumanDecision(source) {
  const { payload, path: repositoryPath } = source;
  const receipt = payload.receipt;
  return {
    path: repositoryPath,
    digest: contentDigest(payload),
    receiptId: receipt.receiptId,
    recommendationId: payload.recommendationId,
    sessionId: payload.sessionId,
    presentedAt: receipt.presentedAt,
    decidedAt: receipt.decidedAt,
    disposition: receipt.disposition,
    correlationId: receipt.correlationId,
    executionState: receipt.executionState,
    actionAuthority: receipt.actionAuthority
  };
}

function sanitizeExecutionEvidence(source) {
  const { payload, path: repositoryPath } = source;
  return {
    path: repositoryPath,
    digest: contentDigest(payload),
    evidenceId: payload.evidenceId,
    sessionId: payload.sessionId,
    recommendationId: payload.recommendationId,
    decisionReceiptId: payload.decisionReceiptId,
    processingEvidenceRef: payload.processingEvidenceRef,
    observedAt: payload.observedAt,
    executionState: payload.executionState,
    actionAuthority: payload.actionAuthority
  };
}

function sourceSet(directory, expression, entries) {
  return {
    directory,
    pathPattern: expression.source,
    validationMode: 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT',
    digest: contentDigest(entries),
    entries
  };
}

function cohort(cohortId, selectionRuleId, populationCount, memberRefs, evidenceState, reasonCodes, limitations) {
  const sortedMembers = [...memberRefs].sort();
  return {
    cohortId,
    selectionRuleId,
    populationCount,
    eligibleCount: sortedMembers.length,
    memberRefs: sortedMembers,
    evidenceState,
    reasonCodes: [...reasonCodes].sort(),
    limitations
  };
}

function outcome(state, reasonCodes) {
  return { state, reasonCodes: [...reasonCodes].sort() };
}

function validateCorrelatedSources(f4Projection, humanEntries, executionEntries) {
  const recommendations = new Map();
  for (const record of f4Projection.records) {
    assert(Array.isArray(record.recommendations), `F4 record ${record.sessionId} recommendations are required.`);
    for (const recommendation of record.recommendations) {
      assert(nonEmpty(recommendation.recommendationId), `F4 record ${record.sessionId} has invalid recommendation identity.`);
      assert(!recommendations.has(recommendation.recommendationId), `Duplicate F4 recommendationId: ${recommendation.recommendationId}`);
      recommendations.set(recommendation.recommendationId, {
        sessionId: record.sessionId,
        correlationId: recommendation.correlationId
      });
    }
  }

  const receipts = new Map();
  const decisionByRecommendation = new Set();
  for (const entry of humanEntries) {
    const recommendation = recommendations.get(entry.recommendationId);
    assert(recommendation, `Human Decision receipt ${entry.receiptId} references an unknown recommendation.`);
    assert(recommendation.sessionId === entry.sessionId, `Human Decision receipt ${entry.receiptId} session mismatch.`);
    assert(recommendation.correlationId === entry.correlationId, `Human Decision receipt ${entry.receiptId} correlation mismatch.`);
    assert(!receipts.has(entry.receiptId), `Duplicate Human Decision receiptId: ${entry.receiptId}`);
    assert(!decisionByRecommendation.has(entry.recommendationId), `Multiple Human Decision receipts for recommendation ${entry.recommendationId} are forbidden.`);
    receipts.set(entry.receiptId, entry);
    decisionByRecommendation.add(entry.recommendationId);
  }

  const processingEntries = new Map(f4Projection.sourceSet.entries.map((entry) => [entry.path, entry]));
  const evidenceIds = new Set();
  for (const entry of executionEntries) {
    assert(!evidenceIds.has(entry.evidenceId), `Duplicate execution evidenceId: ${entry.evidenceId}`);
    evidenceIds.add(entry.evidenceId);
    const receipt = receipts.get(entry.decisionReceiptId);
    assert(receipt, `Execution evidence ${entry.evidenceId} references an unknown decision receipt.`);
    assert(receipt.recommendationId === entry.recommendationId && receipt.sessionId === entry.sessionId, `Execution evidence ${entry.evidenceId} decision correlation mismatch.`);
    const processing = processingEntries.get(entry.processingEvidenceRef);
    assert(processing, `Execution evidence ${entry.evidenceId} references unknown BKL-045 processing evidence.`);
    assert(processing.sessionId === entry.sessionId, `Execution evidence ${entry.evidenceId} processing session mismatch.`);
    assert(Date.parse(entry.observedAt) >= Date.parse(receipt.decidedAt), `Execution evidence ${entry.evidenceId} predates the Human Decision.`);
  }

  return recommendations.size;
}

function assertNoForbiddenPublicFields(value, location = '$') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) return value.forEach((item, index) => assertNoForbiddenPublicFields(item, `${location}[${index}]`));
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_PUBLIC_KEYS.has(key), `${location}.${key} is forbidden in the public F5 report.`);
    assertNoForbiddenPublicFields(child, `${location}.${key}`);
  }
}

export function buildRealEvidenceEvaluation({
  catalog,
  f4Projection,
  humanDecisionSources = [],
  executionEvidenceSources = [],
  generatedAt
}) {
  validateCatalog(catalog);
  validateF4Projection(catalog, f4Projection);
  assert(validDateTime(generatedAt), 'generatedAt must be an ISO date-time.');
  assert(Array.isArray(humanDecisionSources) && Array.isArray(executionEvidenceSources), 'F5 source collections must be arrays.');

  const decisionPaths = humanDecisionSources.map((source) => source?.path);
  const executionPaths = executionEvidenceSources.map((source) => source?.path);
  assert(new Set(decisionPaths).size === decisionPaths.length, 'Duplicate Human Decision source paths are forbidden.');
  assert(new Set(executionPaths).size === executionPaths.length, 'Duplicate execution evidence source paths are forbidden.');

  const humanEntries = humanDecisionSources.map((source) => {
    validateRawHumanDecisionSource(source.path, source.payload);
    return sanitizeHumanDecision(source);
  }).sort((a, b) => a.path.localeCompare(b.path));
  const executionEntries = executionEvidenceSources.map((source) => {
    validateRawExecutionEvidenceSource(source.path, source.payload);
    return sanitizeExecutionEvidence(source);
  }).sort((a, b) => a.path.localeCompare(b.path));

  const recommendationCount = validateCorrelatedSources(f4Projection, humanEntries, executionEntries);
  const catalogIds = catalog.sessions.map((session) => session.sessionId).sort();
  const f4SourcePaths = new Set(f4Projection.sourceSet.entries.map((entry) => entry.path));
  const provenanceMembers = f4Projection.records
    .filter((record) => {
      if (record.correlationState !== 'PROVENANCE_MATCHED') return false;
      assert(record.sourceRefs.length > 0 && record.sourceRefs.every((sourceRef) => f4SourcePaths.has(sourceRef)), `F4 matched record ${record.sessionId} lacks exact processing evidence.`);
      return true;
    })
    .map((record) => record.sessionId);

  const humanSourceSet = sourceSet(HUMAN_DECISION_DIRECTORY, HUMAN_DECISION_PATH, humanEntries);
  const executionSourceSet = sourceSet(EXECUTION_EVIDENCE_DIRECTORY, EXECUTION_EVIDENCE_PATH, executionEntries);
  const catalogDigest = contentDigest(catalog);
  const sourceSnapshots = {
    catalog: {
      path: CATALOG_PATH,
      digest: catalogDigest,
      sessionCount: catalogIds.length,
      sessionIds: catalogIds
    },
    f4Projection: {
      path: F4_PROJECTION_PATH,
      digest: f4Projection.projectionDigest,
      projectionId: f4Projection.projectionId,
      generatedAt: f4Projection.generatedAt,
      sourceSetDigest: f4Projection.sourceSet.digest,
      recordCount: f4Projection.records.length
    },
    humanDecisionSourceSet: humanSourceSet,
    executionEvidenceSourceSet: executionSourceSet
  };

  const cohorts = [
    cohort(
      F5_METHOD_REGISTRY.cohortIds[0],
      F5_METHOD_REGISTRY.selectionRuleIds[0],
      catalogIds.length,
      catalogIds,
      'AVAILABLE',
      ['FULL_CANONICAL_POPULATION'],
      ['This cohort proves complete governed population coverage only; it is not scientific-effectiveness evidence.']
    ),
    cohort(
      F5_METHOD_REGISTRY.cohortIds[1],
      F5_METHOD_REGISTRY.selectionRuleIds[1],
      catalogIds.length,
      provenanceMembers,
      provenanceMembers.length ? 'AVAILABLE' : 'NOT_EVALUABLE',
      [provenanceMembers.length ? 'EXACT_PROVENANCE_AVAILABLE' : 'NO_EXACT_PROVENANCE_MATCHES'],
      ['Only exact F4/BKL-045 session correlation is eligible; similarity and imputation are forbidden.']
    ),
    cohort(
      F5_METHOD_REGISTRY.cohortIds[2],
      F5_METHOD_REGISTRY.selectionRuleIds[2],
      recommendationCount,
      humanEntries.map((entry) => entry.receiptId),
      humanEntries.length ? 'AVAILABLE' : 'NOT_AVAILABLE',
      [humanEntries.length ? 'HUMAN_DECISION_RECEIPTS_AVAILABLE' : 'NO_HUMAN_DECISION_RECEIPTS'],
      ['Human disposition is not execution proof and is not scientific ground truth.']
    ),
    cohort(
      F5_METHOD_REGISTRY.cohortIds[3],
      F5_METHOD_REGISTRY.selectionRuleIds[3],
      humanEntries.length,
      executionEntries.map((entry) => entry.evidenceId),
      executionEntries.length ? 'AVAILABLE' : 'NOT_AVAILABLE',
      [executionEntries.length ? 'EXECUTION_EVIDENCE_AVAILABLE' : 'NO_EXECUTION_EVIDENCE'],
      ['Execution evidence proves a governed manual execution link only; it does not prove outcome quality.']
    )
  ];

  const technicalGates = [
    ['CATALOG_SNAPSHOT_INTEGRITY', 'PASS', []],
    ['F4_PROJECTION_INTEGRITY', 'PASS', []],
    ['FULL_POPULATION_COVERAGE', 'PASS', []],
    ['HUMAN_DECISION_SOURCE_CONTRACT', 'PASS', []],
    ['EXECUTION_EVIDENCE_SOURCE_CONTRACT', 'PASS', []],
    ['CLOSED_METHOD_REGISTRY', 'PASS', []],
    ['F5A_REPORT_DETERMINISM', 'PASS', []],
    ['F5B_DYNAMIC_UPDATE', 'NOT_EXECUTED', ['F5B_DYNAMIC_UPDATE_NOT_EXECUTED']],
    ['F5B_CONSUMER', 'NOT_EXECUTED', ['F5B_CONSUMER_NOT_EXECUTED']]
  ].map(([gateId, state, reasonCodes]) => ({ gateId, state, reasonCodes }));

  const targetCounts = new Map();
  for (const session of catalog.sessions) {
    const target = nonEmpty(session.target) ? session.target : 'UNKNOWN';
    targetCounts.set(target, (targetCounts.get(target) ?? 0) + 1);
  }
  const targetDistribution = [...targetCounts.entries()]
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([target, count]) => ({ target, count }));

  const report = {
    schemaVersion: F5_SCHEMA_VERSION,
    evaluationType: F5_EVALUATION_TYPE,
    evaluationState: F5_EVALUATION_STATE,
    identityMethod: F5_IDENTITY_METHOD,
    evaluationId: `BKL046-F5A-${contentDigest({
      catalogDigest,
      executionEvidenceDigest: executionSourceSet.digest,
      f4ProjectionDigest: f4Projection.projectionDigest,
      humanDecisionDigest: humanSourceSet.digest,
      methodId: F5_METHOD_ID
    }).slice(0, 24).toUpperCase()}`,
    generatedAt,
    producer: F5_PRODUCER,
    producerVersion: F5_PRODUCER_VERSION,
    methodId: F5_METHOD_ID,
    sourceSnapshots,
    methodRegistry: structuredClone(F5_METHOD_REGISTRY),
    cohorts,
    technicalGates,
    outcomes: {
      technical: outcome('READY_FOR_F5_EVALUATION', [
        'F5A_FOUNDATION_IMPLEMENTED',
        'F5B_DYNAMIC_UPDATE_NOT_EXECUTED',
        'F5B_CONSUMER_NOT_EXECUTED'
      ]),
      scientific: outcome('NOT_EVALUABLE_CURRENT_EVIDENCE', [
        'NO_APPROVED_GROUND_TRUTH_METHOD',
        ...(provenanceMembers.length ? [] : ['NO_EXACT_PROVENANCE_MATCHES'])
      ]),
      humanDecision: outcome(humanEntries.length ? 'AVAILABLE' : 'NOT_AVAILABLE', [
        humanEntries.length ? 'HUMAN_DECISION_RECEIPTS_AVAILABLE' : 'NO_HUMAN_DECISION_RECEIPTS'
      ]),
      production: outcome('NOT_READY_FOR_PRODUCTION', [
        'PRODUCTION_AUTHORITY_NOT_GRANTED',
        'SCIENTIFIC_EFFECTIVENESS_NOT_ESTABLISHED'
      ]),
      capabilityOutcome: 'F5A_EVALUATION_FOUNDATION_READY',
      closureRecommendation: 'KEEP_OPEN',
      aiModelImplemented: false
    },
    summary: {
      canonicalSessions: catalogIds.length,
      provenanceEligible: provenanceMembers.length,
      humanDecisionReceipts: humanEntries.length,
      executionEvidence: executionEntries.length,
      uncorrelatedProcessingSources: f4Projection.summary.uncorrelatedSources,
      targetDistribution
    },
    authority: structuredClone(AUTHORITY),
    limitations: [
      'F5-A implements deterministic evaluation foundations only; dynamic workflow integration and consumer delivery remain not executed.',
      'Scientific effectiveness is not evaluable without exact eligible evidence and an independently governed ground-truth method.',
      'Human decisions and execution evidence are separate from scientific outcome quality.',
      'No AI model, provider, confidence score, automatic acceptance, PixInsight apply, device command, production authority or Safety Authority is implemented.'
    ],
    evaluationDigest: ''
  };
  delete report.evaluationDigest;
  report.evaluationDigest = contentDigest(report);
  validateRealEvidenceEvaluation(report);
  return deepFreeze(report);
}

function validateSourceSet(value, entryKeys, pathValidator, label) {
  assertExactKeys(value, SOURCE_SET_KEYS, label);
  assert(nonEmpty(value.directory) && nonEmpty(value.pathPattern), `${label} directory and pattern are required.`);
  assert(value.validationMode === 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT', `${label} validationMode is unsupported.`);
  assert(Array.isArray(value.entries), `${label}.entries must be an array.`);
  const paths = value.entries.map((entry) => entry.path);
  assertSortedUnique(paths, `${label}.paths`);
  value.entries.forEach((entry, index) => {
    assertExactKeys(entry, entryKeys, `${label}.entries[${index}]`);
    pathValidator(entry.path);
    assert(validDigest(entry.digest), `${label}.entries[${index}].digest is invalid.`);
  });
  assert(value.digest === contentDigest(value.entries), `${label} digest mismatch.`);
}

export function validateRealEvidenceEvaluation(report) {
  assertExactKeys(report, TOP_LEVEL_KEYS, 'report');
  assert(report.schemaVersion === F5_SCHEMA_VERSION, 'Unsupported F5 schemaVersion.');
  assert(report.evaluationType === F5_EVALUATION_TYPE && report.evaluationState === F5_EVALUATION_STATE, 'Unsupported F5 evaluation type or state.');
  assert(report.identityMethod === F5_IDENTITY_METHOD, 'Unsupported F5 identity method.');
  assert(report.producer === F5_PRODUCER && report.producerVersion === F5_PRODUCER_VERSION, 'Unsupported F5 producer.');
  assert(report.methodId === F5_METHOD_ID, 'Unsupported F5 method.');
  assert(validDateTime(report.generatedAt), 'Invalid F5 generatedAt.');
  assertExactKeys(report.sourceSnapshots, SOURCE_SNAPSHOT_KEYS, 'sourceSnapshots');
  assertExactKeys(report.sourceSnapshots.catalog, CATALOG_SNAPSHOT_KEYS, 'sourceSnapshots.catalog');
  assert(report.sourceSnapshots.catalog.path === CATALOG_PATH && validDigest(report.sourceSnapshots.catalog.digest), 'F5 catalog snapshot is invalid.');
  assertSortedUnique(report.sourceSnapshots.catalog.sessionIds, 'F5 catalog sessionIds');
  assert(report.sourceSnapshots.catalog.sessionCount === report.sourceSnapshots.catalog.sessionIds.length, 'F5 catalog snapshot count mismatch.');
  assertExactKeys(report.sourceSnapshots.f4Projection, F4_SNAPSHOT_KEYS, 'sourceSnapshots.f4Projection');
  assert(report.sourceSnapshots.f4Projection.path === F4_PROJECTION_PATH, 'F5 F4 projection path is invalid.');
  assert(validDigest(report.sourceSnapshots.f4Projection.digest) && validDigest(report.sourceSnapshots.f4Projection.sourceSetDigest), 'F5 F4 projection digests are invalid.');
  assert(validDateTime(report.sourceSnapshots.f4Projection.generatedAt), 'F5 F4 generatedAt is invalid.');
  validateSourceSet(report.sourceSnapshots.humanDecisionSourceSet, DECISION_ENTRY_KEYS, assertAllowedHumanDecisionPath, 'humanDecisionSourceSet');
  validateSourceSet(report.sourceSnapshots.executionEvidenceSourceSet, EXECUTION_ENTRY_KEYS, assertAllowedExecutionEvidencePath, 'executionEvidenceSourceSet');

  assert(canonicalJson(report.methodRegistry) === canonicalJson(F5_METHOD_REGISTRY), 'F5 method registry drift.');
  assert(Array.isArray(report.cohorts) && report.cohorts.length === F5_METHOD_REGISTRY.cohortIds.length, 'F5 cohorts are incomplete.');
  report.cohorts.forEach((item, index) => {
    assertExactKeys(item, COHORT_KEYS, `cohorts[${index}]`);
    assert(item.cohortId === F5_METHOD_REGISTRY.cohortIds[index], `cohorts[${index}] identity/order mismatch.`);
    assert(item.selectionRuleId === F5_METHOD_REGISTRY.selectionRuleIds[index], `cohorts[${index}] selection rule mismatch.`);
    assert(Number.isInteger(item.populationCount) && item.populationCount >= 0, `cohorts[${index}] populationCount is invalid.`);
    assert(Number.isInteger(item.eligibleCount) && item.eligibleCount >= 0, `cohorts[${index}] eligibleCount is invalid.`);
    assertSortedUnique(item.memberRefs, `cohorts[${index}].memberRefs`);
    assert(item.eligibleCount === item.memberRefs.length && item.eligibleCount <= item.populationCount, `cohorts[${index}] counts are inconsistent.`);
    assert(F5_METHOD_REGISTRY.evidenceStates.includes(item.evidenceState), `cohorts[${index}] evidenceState is unknown.`);
    assert(Array.isArray(item.reasonCodes) && item.reasonCodes.every((code) => F5_METHOD_REGISTRY.reasonCodes.includes(code)), `cohorts[${index}] contains unknown reason codes.`);
    assert(Array.isArray(item.limitations) && item.limitations.length > 0, `cohorts[${index}] limitations are required.`);
    if (item.eligibleCount === 0) assert(item.evidenceState !== 'AVAILABLE', `cohorts[${index}] cannot treat an empty cohort as available.`);
  });

  assert(Array.isArray(report.technicalGates) && report.technicalGates.length === F5_METHOD_REGISTRY.technicalGateIds.length, 'F5 technical gates are incomplete.');
  report.technicalGates.forEach((gate, index) => {
    assertExactKeys(gate, TECHNICAL_GATE_KEYS, `technicalGates[${index}]`);
    assert(gate.gateId === F5_METHOD_REGISTRY.technicalGateIds[index], `technicalGates[${index}] identity/order mismatch.`);
    assert(F5_METHOD_REGISTRY.gateStates.includes(gate.state), `technicalGates[${index}] state is unknown.`);
    assert(Array.isArray(gate.reasonCodes) && gate.reasonCodes.every((code) => F5_METHOD_REGISTRY.reasonCodes.includes(code)), `technicalGates[${index}] has unknown reason codes.`);
  });

  assertExactKeys(report.outcomes, OUTCOMES_KEYS, 'outcomes');
  for (const axis of ['technical', 'scientific', 'humanDecision', 'production']) assertExactKeys(report.outcomes[axis], OUTCOME_KEYS, `outcomes.${axis}`);
  assert(F5_METHOD_REGISTRY.technicalStates.includes(report.outcomes.technical.state), 'Unknown technical outcome.');
  assert(F5_METHOD_REGISTRY.scientificStates.includes(report.outcomes.scientific.state), 'Unknown scientific outcome.');
  assert(F5_METHOD_REGISTRY.humanDecisionStates.includes(report.outcomes.humanDecision.state), 'Unknown Human Decision outcome.');
  assert(F5_METHOD_REGISTRY.productionStates.includes(report.outcomes.production.state), 'Unknown production outcome.');
  for (const axis of ['technical', 'scientific', 'humanDecision', 'production']) {
    assert(Array.isArray(report.outcomes[axis].reasonCodes) && report.outcomes[axis].reasonCodes.every((code) => F5_METHOD_REGISTRY.reasonCodes.includes(code)), `outcomes.${axis} has unknown reason codes.`);
  }
  assert(F5_METHOD_REGISTRY.capabilityOutcomes.includes(report.outcomes.capabilityOutcome), 'Unknown capability outcome.');
  assert(F5_METHOD_REGISTRY.closureRecommendations.includes(report.outcomes.closureRecommendation), 'Unknown closure recommendation.');
  assert(report.outcomes.aiModelImplemented === false, 'F5-A cannot claim an implemented AI model.');
  assert(report.outcomes.technical.state === 'READY_FOR_F5_EVALUATION', 'F5-A technical outcome must remain evaluation-ready, not accepted.');
  assert(report.outcomes.scientific.state === 'NOT_EVALUABLE_CURRENT_EVIDENCE', 'F5-A cannot claim scientific effectiveness.');
  assert(report.outcomes.production.state === 'NOT_READY_FOR_PRODUCTION', 'F5-A cannot claim production readiness.');
  assert(report.outcomes.closureRecommendation === 'KEEP_OPEN', 'F5-A cannot close the capability.');

  assertExactKeys(report.summary, SUMMARY_KEYS, 'summary');
  for (const key of ['canonicalSessions', 'provenanceEligible', 'humanDecisionReceipts', 'executionEvidence', 'uncorrelatedProcessingSources']) {
    assert(Number.isInteger(report.summary[key]) && report.summary[key] >= 0, `summary.${key} is invalid.`);
  }
  assert(Array.isArray(report.summary.targetDistribution), 'summary.targetDistribution must be an array.');
  report.summary.targetDistribution.forEach((item, index) => {
    assertExactKeys(item, TARGET_COUNT_KEYS, `summary.targetDistribution[${index}]`);
    assert(nonEmpty(item.target) && Number.isInteger(item.count) && item.count > 0, `summary.targetDistribution[${index}] is invalid.`);
  });
  assert(report.summary.targetDistribution.reduce((total, item) => total + item.count, 0) === report.summary.canonicalSessions, 'Target distribution does not cover the canonical population.');
  assert(report.summary.canonicalSessions === report.cohorts[0].eligibleCount, 'Canonical summary/cohort mismatch.');
  assert(report.summary.provenanceEligible === report.cohorts[1].eligibleCount, 'Provenance summary/cohort mismatch.');
  assert(report.summary.humanDecisionReceipts === report.cohorts[2].eligibleCount, 'Human Decision summary/cohort mismatch.');
  assert(report.summary.executionEvidence === report.cohorts[3].eligibleCount, 'Execution summary/cohort mismatch.');

  assert(canonicalJson(report.authority) === canonicalJson(AUTHORITY), 'F5 authority drift.');
  assert(Array.isArray(report.limitations) && report.limitations.length > 0, 'F5 limitations are required.');
  assertNoForbiddenPublicFields(report);
  assert(/^BKL046-F5A-[A-F0-9]{24}$/.test(report.evaluationId), 'F5 evaluationId is invalid.');
  const identity = contentDigest({
    catalogDigest: report.sourceSnapshots.catalog.digest,
    executionEvidenceDigest: report.sourceSnapshots.executionEvidenceSourceSet.digest,
    f4ProjectionDigest: report.sourceSnapshots.f4Projection.digest,
    humanDecisionDigest: report.sourceSnapshots.humanDecisionSourceSet.digest,
    methodId: report.methodId
  }).slice(0, 24).toUpperCase();
  assert(report.evaluationId === `BKL046-F5A-${identity}`, 'F5 evaluation identity mismatch.');
  validateDigestProtected(report, 'evaluationDigest', 'F5 evaluation');
  return true;
}
