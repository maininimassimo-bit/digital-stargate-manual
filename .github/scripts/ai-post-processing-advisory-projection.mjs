import { createHash } from 'node:crypto';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { validateRecommendationRecord } from './ai-post-processing-advisory-contract.mjs';
import {
  buildDeterministicAdvisoryRecords,
  F3_CONTEXTS
} from './ai-post-processing-advisory-demonstrator.mjs';

export const F4A_SCHEMA_VERSION = '1.0';
export const F4A_PROJECTION_TYPE = 'AI_POST_PROCESSING_ASSISTANT_F4_SOURCE_PROJECTION';
export const F4A_PROJECTION_STATE = 'SOURCE_MAPPED_PRE_ADVISORY';
export const F4A_IDENTITY_METHOD = 'BKL046-F4-CANONICAL-JSON-SHA256-1';
export const F4A_PRODUCER = 'DSG.AiPostProcessingAdvisorySourceProjection';
export const F4A_PRODUCER_VERSION = '1.0.0-f4a';
export const F4A_METHOD_ID = 'BKL046-F4A-EXACT-CORRELATION-1';
export const F3_METHOD_ID = 'BKL046-F3-CLOSED-RULES-1';
export const F4_SCHEMA_VERSION = '1.1';
export const F4_PROJECTION_TYPE = 'AI_POST_PROCESSING_ADVISORY_PROJECTION';
export const F4_PROJECTION_STATE = 'PRE_DECISION_READ_ONLY';
export const F4_PRODUCER = 'DSG.AiPostProcessingAdvisoryProjection';
export const F4_PRODUCER_VERSION = '1.0.0-f4b';
export const CATALOG_PATH = 'docs/data/scientific-session-catalog.json';
export const PROVENANCE_DIRECTORY = 'docs/architecture/scientific-assets/evidence';

const PROVENANCE_PATH = /^docs\/architecture\/scientific-assets\/evidence\/BKL-045-F3B-PXP-\d{8}T\d{9}Z-[A-Z0-9][A-Z0-9_-]{0,31}\.json$/;
const COMPLETENESS = new Set(['COMPLETE', 'PARTIAL', 'UNAVAILABLE']);
const CORRELATION_STATES = new Set(['PROVENANCE_MATCHED', 'PROVENANCE_UNAVAILABLE', 'CORRELATION_AMBIGUOUS', 'CORRELATION_INVALID']);
const FORBIDDEN_PUBLIC_KEYS = new Set(['hostId', 'workspaceId', 'absolutePath', 'localPath', 'imageData', 'imageUri', 'credential', 'secret']);
const PROJECTION_KEYS = new Set(['schemaVersion', 'projectionType', 'projectionState', 'identityMethod', 'projectionId', 'generatedAt', 'producer', 'producerVersion', 'methodId', 'downstreamRuleMethodId', 'sourceCatalog', 'sourceSet', 'records', 'summary', 'authority', 'limitations', 'projectionDigest']);
const RECORD_KEYS = new Set(['recordId', 'sessionId', 'target', 'correlationState', 'sourceRefs', 'advisoryInput', 'gateState', 'reasonCodes', 'recommendationState', 'recordDigest']);
const SOURCE_ENTRY_KEYS = new Set(['path', 'digest', 'sidecarId', 'exportedAt', 'sessionId', 'target', 'workflowId', 'completeness', 'limitations']);
const FINAL_PROJECTION_KEYS = new Set(['schemaVersion', 'projectionType', 'projectionState', 'identityMethod', 'projectionId', 'generatedAt', 'producer', 'producerVersion', 'methodId', 'sourceCatalog', 'sourceSet', 'records', 'summary', 'authority', 'limitations', 'projectionDigest']);
const FINAL_RECORD_KEYS = new Set(['recordId', 'sessionId', 'target', 'correlationState', 'sourceRefs', 'inputArtifactDigest', 'subject', 'sourceBindings', 'recommendations', 'ruleEvaluations', 'decisionState', 'recordDigest']);

const authority = Object.freeze({
  consumerMode: 'READ_ONLY',
  advisoryOnly: true,
  acceptanceAuthority: 'HUMAN_ONLY',
  actionAuthority: 'NONE',
  executionAuthority: 'NONE',
  safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS',
  pixInsightApplyAuthorized: false,
  automaticAcceptanceAuthorized: false
});

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function assertExactKeys(value, allowed, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object.`);
  for (const key of Object.keys(value)) assert(allowed.has(key), `${label}.${key} is not allowed.`);
  for (const key of allowed) assert(Object.hasOwn(value, key), `${label}.${key} is required.`);
}

const nonEmpty = (value) => typeof value === 'string' && value.trim().length > 0;

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

function assertNoForbiddenPublicFields(value, location = '$') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) return value.forEach((item, index) => assertNoForbiddenPublicFields(item, `${location}[${index}]`));
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_PUBLIC_KEYS.has(key), `${location}.${key} is forbidden in the public F4 projection.`);
    assertNoForbiddenPublicFields(child, `${location}.${key}`);
  }
}

export function assertAllowedProvenancePath(repositoryPath) {
  assert(nonEmpty(repositoryPath), 'Provenance path is required.');
  assert(!path.isAbsolute(repositoryPath), 'Absolute provenance paths are forbidden.');
  assert(!repositoryPath.includes('\\'), 'Backslash provenance paths are forbidden.');
  assert(!repositoryPath.split('/').includes('..'), 'Provenance path traversal is forbidden.');
  assert(PROVENANCE_PATH.test(repositoryPath), `Provenance path is outside the BKL-045 allowlist: ${repositoryPath}`);
  return true;
}

export function validateRawProvenanceSource(repositoryPath, payload) {
  assertAllowedProvenancePath(repositoryPath);
  assert(payload && typeof payload === 'object' && !Array.isArray(payload), `${repositoryPath} must contain a JSON object.`);
  assert(payload.schemaVersion === '1.0', `${repositoryPath} has an unsupported schemaVersion.`);
  assert(payload.authority === 'processing_evidence', `${repositoryPath} has unsupported authority.`);
  assert(payload.actionAuthority === 'NONE', `${repositoryPath} escalates action authority.`);
  assert(nonEmpty(payload.sidecarId) && payload.sidecarId.startsWith('PXP-'), `${repositoryPath} has an invalid sidecarId.`);
  assert(Number.isFinite(Date.parse(payload.exportedAt)), `${repositoryPath} has an invalid exportedAt.`);
  assert(nonEmpty(payload.observationContext?.sessionId), `${repositoryPath} has no exact sessionId.`);
  assert(nonEmpty(payload.workflow?.workflowId), `${repositoryPath} has no workflowId.`);
  assert(COMPLETENESS.has(payload.capture?.completeness), `${repositoryPath} has unsupported completeness.`);
  assert(Array.isArray(payload.capture?.limitations), `${repositoryPath} has invalid capture limitations.`);
  return true;
}

function sanitizeSource(repositoryPath, payload) {
  return {
    path: repositoryPath,
    digest: contentDigest(payload),
    sidecarId: payload.sidecarId,
    exportedAt: payload.exportedAt,
    sessionId: payload.observationContext.sessionId,
    target: payload.observationContext.target ?? null,
    workflowId: payload.workflow.workflowId,
    completeness: payload.capture.completeness,
    limitations: [...payload.capture.limitations].sort()
  };
}

export async function discoverProvenanceSources(repositoryRoot = '.') {
  const absoluteDirectory = path.join(repositoryRoot, PROVENANCE_DIRECTORY);
  const entries = await readdir(absoluteDirectory, { withFileTypes: true });
  const paths = entries
    .filter((entry) => entry.isFile() && entry.name.startsWith('BKL-045-F3B-PXP-'))
    .map((entry) => `${PROVENANCE_DIRECTORY}/${entry.name}`)
    .sort();
  const sources = [];
  for (const repositoryPath of paths) {
    assertAllowedProvenancePath(repositoryPath);
    const payload = JSON.parse(await readFile(path.join(repositoryRoot, repositoryPath), 'utf8'));
    validateRawProvenanceSource(repositoryPath, payload);
    sources.push({ path: repositoryPath, payload });
  }
  return sources;
}

function validateCatalog(catalog) {
  assert(catalog?.catalogStatus === 'VERSIONED_ANALYTICS_PROJECTION', 'Unsupported scientific catalog status.');
  assert(Array.isArray(catalog.sessions), 'Scientific catalog sessions are required.');
  const ids = catalog.sessions.map((session) => session?.sessionId);
  assert(ids.every(nonEmpty), 'Every catalog session requires a sessionId.');
  assert(new Set(ids).size === ids.length, 'Scientific catalog session IDs must be unique.');
}

function recordFor(session, candidates) {
  let correlationState = 'PROVENANCE_UNAVAILABLE';
  let selected = null;
  let reasonCodes = ['PROCESSING_EVIDENCE_UNAVAILABLE'];
  if (candidates.length > 1) {
    correlationState = 'CORRELATION_AMBIGUOUS';
    reasonCodes = ['MULTIPLE_PROCESSING_EVIDENCE_CANDIDATES'];
  } else if (candidates.length === 1) {
    [selected] = candidates;
    if (selected.target !== null && nonEmpty(session.target) && selected.target !== session.target) {
      correlationState = 'CORRELATION_INVALID';
      reasonCodes = ['SOURCE_TARGET_MISMATCH'];
    } else {
      correlationState = 'PROVENANCE_MATCHED';
      reasonCodes = selected.completeness === 'COMPLETE' ? [] : [`SOURCE_COMPLETENESS_${selected.completeness}`];
    }
  }
  const sourceRefs = candidates.map((item) => item.path).sort();
  const seed = { sessionId: session.sessionId, sourceRefs };
  const record = {
    recordId: `F4A-${contentDigest(seed).slice(0, 24).toUpperCase()}`,
    sessionId: session.sessionId,
    target: session.target ?? null,
    correlationState,
    sourceRefs,
    advisoryInput: {
      subject: {
        subjectId: `SESSION-${contentDigest(session.sessionId).slice(0, 24).toUpperCase()}`,
        subjectType: 'PIXINSIGHT_WORKFLOW',
        sessionRef: `${CATALOG_PATH}#${session.sessionId}`,
        workflowRef: selected?.workflowId ?? null,
        correlationState: ['PROVENANCE_MATCHED', 'PROVENANCE_UNAVAILABLE'].includes(correlationState) ? 'RESOLVED' : 'PARTIAL'
      },
      repositoryAuthority: {
        sourceAuthority: 'repository_authority',
        sourceRef: CATALOG_PATH,
        lifecycleState: 'validated',
        quality: 'VALID',
        completeness: 'COMPLETE'
      },
      processingEvidence: selected ? {
        sourceAuthority: 'processing_evidence',
        sourceRef: selected.path,
        lifecycleState: 'validated',
        quality: selected.completeness === 'COMPLETE' ? 'VALID' : 'UNKNOWN',
        completeness: selected.completeness
      } : null
    },
    gateState: reasonCodes.length === 0 ? 'SOURCE_READY' : 'FAIL_CLOSED',
    reasonCodes: [...reasonCodes].sort(),
    recommendationState: 'NOT_GENERATED_F4A',
    recordDigest: ''
  };
  delete record.recordDigest;
  record.recordDigest = contentDigest(record);
  return record;
}

export function buildAdvisorySourceProjection({ catalog, provenanceSources, generatedAt }) {
  validateCatalog(catalog);
  assert(Number.isFinite(Date.parse(generatedAt)), 'generatedAt must be an ISO date-time.');
  assert(Array.isArray(provenanceSources), 'provenanceSources must be an array.');
  const paths = provenanceSources.map((source) => source?.path);
  assert(new Set(paths).size === paths.length, 'Duplicate provenance paths are forbidden.');
  const sidecarIds = new Set();
  const sanitized = provenanceSources.map(({ path: repositoryPath, payload }) => {
    validateRawProvenanceSource(repositoryPath, payload);
    assert(!sidecarIds.has(payload.sidecarId), `Duplicate provenance sidecarId: ${payload.sidecarId}`);
    sidecarIds.add(payload.sidecarId);
    return sanitizeSource(repositoryPath, payload);
  }).sort((a, b) => a.path.localeCompare(b.path));
  const bySession = new Map();
  for (const source of sanitized) {
    const current = bySession.get(source.sessionId) ?? [];
    current.push(source);
    bySession.set(source.sessionId, current);
  }
  const records = [...catalog.sessions]
    .sort((a, b) => a.sessionId.localeCompare(b.sessionId))
    .map((session) => recordFor(session, bySession.get(session.sessionId) ?? []));
  const catalogDigest = contentDigest(catalog);
  const sourceSetDigest = contentDigest(sanitized);
  const counts = (state) => records.filter((record) => record.correlationState === state).length;
  const projection = {
    schemaVersion: F4A_SCHEMA_VERSION,
    projectionType: F4A_PROJECTION_TYPE,
    projectionState: F4A_PROJECTION_STATE,
    identityMethod: F4A_IDENTITY_METHOD,
    projectionId: `BKL046-F4A-${contentDigest({ catalogDigest, sourceSetDigest }).slice(0, 24).toUpperCase()}`,
    generatedAt,
    producer: F4A_PRODUCER,
    producerVersion: F4A_PRODUCER_VERSION,
    methodId: F4A_METHOD_ID,
    downstreamRuleMethodId: F3_METHOD_ID,
    sourceCatalog: {
      path: CATALOG_PATH,
      digest: catalogDigest,
      sessionCount: records.length,
      sessionIds: records.map((record) => record.sessionId)
    },
    sourceSet: {
      validationMode: 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT',
      digest: sourceSetDigest,
      entries: sanitized
    },
    records,
    summary: {
      totalSessions: records.length,
      provenanceMatched: counts('PROVENANCE_MATCHED'),
      provenanceUnavailable: counts('PROVENANCE_UNAVAILABLE'),
      correlationAmbiguous: counts('CORRELATION_AMBIGUOUS'),
      correlationInvalid: counts('CORRELATION_INVALID'),
      sourceReady: records.filter((record) => record.gateState === 'SOURCE_READY').length,
      failClosed: records.filter((record) => record.gateState === 'FAIL_CLOSED').length,
      uncorrelatedSources: sanitized.filter((source) => !catalog.sessions.some((session) => session.sessionId === source.sessionId)).length
    },
    authority: structuredClone(authority),
    limitations: [
      'F4-A maps governed sources and missingness only; it does not generate or publish recommendations.',
      'Raw BKL-045 sidecars are validated at build time; the public snapshot excludes host and workspace identifiers.',
      'No human decision, PixInsight execution, automatic acceptance, device command or Safety Authority is represented.'
    ],
    projectionDigest: ''
  };
  delete projection.projectionDigest;
  projection.projectionDigest = contentDigest(projection);
  validateAdvisorySourceProjection(projection);
  return deepFreeze(projection);
}

export function validateAdvisorySourceProjection(projection) {
  assertExactKeys(projection, PROJECTION_KEYS, 'projection');
  assert(projection?.schemaVersion === F4A_SCHEMA_VERSION, 'Unsupported F4-A schemaVersion.');
  assert(projection.projectionType === F4A_PROJECTION_TYPE && projection.projectionState === F4A_PROJECTION_STATE, 'Unsupported F4-A projection type or state.');
  assert(projection.identityMethod === F4A_IDENTITY_METHOD, 'Unsupported F4-A identity method.');
  assert(projection.producer === F4A_PRODUCER && projection.producerVersion === F4A_PRODUCER_VERSION, 'Unsupported F4-A producer.');
  assert(projection.methodId === F4A_METHOD_ID && projection.downstreamRuleMethodId === F3_METHOD_ID, 'Unsupported F4-A/F3 method binding.');
  assert(Number.isFinite(Date.parse(projection.generatedAt)), 'Invalid F4-A generatedAt.');
  assert(Array.isArray(projection.records) && Array.isArray(projection.sourceSet?.entries), 'F4-A records and source entries are required.');
  const sessionIds = projection.records.map((record) => record.sessionId);
  assert(canonicalJson(sessionIds) === canonicalJson([...sessionIds].sort()), 'F4-A records must be sorted by sessionId.');
  assert(new Set(sessionIds).size === sessionIds.length, 'F4-A records must have unique session IDs.');
  const sourcePaths = projection.sourceSet.entries.map((entry) => entry.path);
  assert(canonicalJson(sourcePaths) === canonicalJson([...sourcePaths].sort()), 'F4-A source entries must be sorted by path.');
  projection.sourceSet.entries.forEach((entry, index) => {
    assertExactKeys(entry, SOURCE_ENTRY_KEYS, `sourceSet.entries[${index}]`);
    assertAllowedProvenancePath(entry.path);
    assert(/^[a-f0-9]{64}$/.test(entry.digest ?? ''), `Invalid source digest for ${entry.path}.`);
  });
  assert(projection.sourceSet.validationMode === 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT', 'Unsupported F4-A source validation mode.');
  assert(projection.sourceSet.digest === contentDigest(projection.sourceSet.entries), 'F4-A source-set digest mismatch.');
  const sourcePathSet = new Set(sourcePaths);
  for (const record of projection.records) {
    assertExactKeys(record, RECORD_KEYS, `record.${record?.sessionId ?? 'unknown'}`);
    assert(CORRELATION_STATES.has(record.correlationState), `Unsupported correlation state for ${record.sessionId}.`);
    assert(record.sourceRefs.every((sourceRef) => sourcePathSet.has(sourceRef)), `Record ${record.sessionId} references an unknown source.`);
    assert(canonicalJson(record.sourceRefs) === canonicalJson([...record.sourceRefs].sort()), `Record ${record.sessionId} sourceRefs must be sorted.`);
    assert(record.recordId === `F4A-${contentDigest({ sessionId: record.sessionId, sourceRefs: record.sourceRefs }).slice(0, 24).toUpperCase()}`, `Record identity mismatch for ${record.sessionId}.`);
    assert((record.gateState === 'SOURCE_READY') === (record.reasonCodes.length === 0), `Record ${record.sessionId} gate and reason codes disagree.`);
    assert(record.recommendationState === 'NOT_GENERATED_F4A', 'F4-A cannot contain generated recommendations.');
    const preimage = structuredClone(record);
    delete preimage.recordDigest;
    assert(record.recordDigest === contentDigest(preimage), `Record digest mismatch for ${record.sessionId}.`);
  }
  assert(projection.sourceCatalog.sessionCount === projection.records.length, 'F4-A catalog count does not match records.');
  assert(projection.sourceCatalog.path === CATALOG_PATH && /^[a-f0-9]{64}$/.test(projection.sourceCatalog.digest ?? ''), 'F4-A catalog snapshot is invalid.');
  assert(canonicalJson(projection.sourceCatalog.sessionIds) === canonicalJson(sessionIds), 'F4-A catalog session set does not match records.');
  assert(projection.projectionId === `BKL046-F4A-${contentDigest({ catalogDigest: projection.sourceCatalog.digest, sourceSetDigest: projection.sourceSet.digest }).slice(0, 24).toUpperCase()}`, 'F4-A projection identity mismatch.');
  assert(projection.summary.totalSessions === projection.records.length, 'F4-A summary total does not match records.');
  assert(projection.summary.sourceReady + projection.summary.failClosed === projection.records.length, 'F4-A gate summary is inconsistent.');
  for (const state of CORRELATION_STATES) {
    const key = {
      PROVENANCE_MATCHED: 'provenanceMatched',
      PROVENANCE_UNAVAILABLE: 'provenanceUnavailable',
      CORRELATION_AMBIGUOUS: 'correlationAmbiguous',
      CORRELATION_INVALID: 'correlationInvalid'
    }[state];
    assert(projection.summary[key] === projection.records.filter((record) => record.correlationState === state).length, `F4-A summary ${key} is inconsistent.`);
  }
  assert(projection.summary.sourceReady === projection.records.filter((record) => record.gateState === 'SOURCE_READY').length, 'F4-A sourceReady summary is inconsistent.');
  assert(projection.authority.consumerMode === 'READ_ONLY' && projection.authority.acceptanceAuthority === 'HUMAN_ONLY', 'F4-A authority must remain read-only and human-only.');
  assert(projection.authority.actionAuthority === 'NONE' && projection.authority.executionAuthority === 'NONE', 'F4-A action and execution authority must be NONE.');
  assert(projection.authority.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'F4-A Safety Authority is invalid.');
  assert(projection.authority.pixInsightApplyAuthorized === false && projection.authority.automaticAcceptanceAuthorized === false, 'F4-A apply or auto-accept escalation is forbidden.');
  assertNoForbiddenPublicFields(projection);
  const preimage = structuredClone(projection);
  delete preimage.projectionDigest;
  assert(projection.projectionDigest === contentDigest(preimage), 'F4-A projection digest mismatch.');
  return true;
}

function sealBinding(binding) {
  const sealed = structuredClone(binding);
  delete sealed.bindingDigest;
  sealed.bindingDigest = contentDigest(sealed);
  return sealed;
}

function repositoryBinding(sessionId) {
  return sealBinding({
    bindingId: `SRC-F4-CATALOG-${contentDigest(sessionId).slice(0, 20).toUpperCase()}`,
    semanticType: 'evidence',
    evidenceClass: 'DECLARED',
    sourceAuthority: 'repository_authority',
    sourceRef: CATALOG_PATH,
    lifecycleState: 'validated',
    quality: 'VALID',
    completeness: 'COMPLETE',
    citationRefs: [CATALOG_PATH],
    limitations: ['The catalog establishes governed session identity; it does not establish PixInsight processing completeness.'],
    bindingDigest: ''
  });
}

function processingBinding(source) {
  return sealBinding({
    bindingId: `SRC-F4-PROVENANCE-${contentDigest({ path: source.path, digest: source.digest }).slice(0, 20).toUpperCase()}`,
    semanticType: 'evidence',
    evidenceClass: 'OBSERVED',
    sourceAuthority: 'processing_evidence',
    sourceRef: source.path,
    lifecycleState: 'validated',
    quality: source.completeness === 'COMPLETE' ? 'VALID' : 'UNKNOWN',
    completeness: source.completeness,
    citationRefs: [source.path],
    limitations: [...source.limitations],
    bindingDigest: ''
  });
}

function finalRecord(sourceRecord, sourceByPath, generatedAt) {
  const resolvedSubject = ['PROVENANCE_MATCHED', 'PROVENANCE_UNAVAILABLE'].includes(sourceRecord.correlationState);
  const candidateSources = sourceRecord.sourceRefs.map((sourceRef) => sourceByPath.get(sourceRef));
  assert(candidateSources.every(Boolean), `Source mapping missing for ${sourceRecord.sessionId}.`);
  const subject = {
    subjectId: `SESSION-${contentDigest(sourceRecord.sessionId).slice(0, 24).toUpperCase()}`,
    subjectType: 'PIXINSIGHT_WORKFLOW',
    assetRef: null,
    sessionRef: `${CATALOG_PATH}#${sourceRecord.sessionId}`,
    workflowRef: candidateSources.length === 1 ? candidateSources[0].workflowId : null,
    stepRef: null,
    correlationState: resolvedSubject ? 'RESOLVED' : 'PARTIAL'
  };
  const sourceBindings = [
    repositoryBinding(sourceRecord.sessionId),
    ...candidateSources.map(processingBinding)
  ].sort((a, b) => a.bindingId.localeCompare(b.bindingId));
  const inputArtifactDigest = contentDigest({
    correlationState: sourceRecord.correlationState,
    sourceBindings,
    subject
  });
  const rules = buildDeterministicAdvisoryRecords({
    inputArtifactDigest,
    generatedAt,
    subject,
    sourceBindings,
    contextMode: F3_CONTEXTS.SESSION_PROVENANCE_READ_ONLY
  });
  const record = {
    recordId: `F4-${contentDigest({ sessionId: sourceRecord.sessionId, sourceRefs: sourceRecord.sourceRefs }).slice(0, 24).toUpperCase()}`,
    sessionId: sourceRecord.sessionId,
    target: sourceRecord.target,
    correlationState: sourceRecord.correlationState,
    sourceRefs: [...sourceRecord.sourceRefs],
    inputArtifactDigest,
    subject,
    sourceBindings: structuredClone(rules.sourceBindings),
    recommendations: structuredClone(rules.recommendations),
    ruleEvaluations: structuredClone(rules.ruleEvaluations),
    decisionState: 'NOT_PRESENT_PRE_DECISION',
    recordDigest: ''
  };
  delete record.recordDigest;
  record.recordDigest = contentDigest(record);
  return record;
}

export function buildAdvisoryProjection({ catalog, provenanceSources, generatedAt }) {
  const sourceProjection = buildAdvisorySourceProjection({ catalog, provenanceSources, generatedAt });
  const sourceByPath = new Map(sourceProjection.sourceSet.entries.map((source) => [source.path, source]));
  const records = sourceProjection.records.map((record) => finalRecord(record, sourceByPath, generatedAt));
  const ruleCount = (ruleId, decision) => records.reduce(
    (count, record) => count + Number(record.ruleEvaluations.some((item) => item.ruleId === ruleId && item.decision === decision)),
    0
  );
  const projection = {
    schemaVersion: F4_SCHEMA_VERSION,
    projectionType: F4_PROJECTION_TYPE,
    projectionState: F4_PROJECTION_STATE,
    identityMethod: F4A_IDENTITY_METHOD,
    projectionId: `BKL046-F4-${contentDigest({
      catalogDigest: sourceProjection.sourceCatalog.digest,
      methodId: F3_METHOD_ID,
      sourceSetDigest: sourceProjection.sourceSet.digest
    }).slice(0, 24).toUpperCase()}`,
    generatedAt,
    producer: F4_PRODUCER,
    producerVersion: F4_PRODUCER_VERSION,
    methodId: F3_METHOD_ID,
    sourceCatalog: structuredClone(sourceProjection.sourceCatalog),
    sourceSet: structuredClone(sourceProjection.sourceSet),
    records,
    summary: {
      totalSessions: records.length,
      provenanceMatched: records.filter((record) => record.correlationState === 'PROVENANCE_MATCHED').length,
      provenanceUnavailable: records.filter((record) => record.correlationState === 'PROVENANCE_UNAVAILABLE').length,
      correlationAmbiguous: records.filter((record) => record.correlationState === 'CORRELATION_AMBIGUOUS').length,
      correlationInvalid: records.filter((record) => record.correlationState === 'CORRELATION_INVALID').length,
      governancePass: ruleCount('GOVERNANCE_READINESS', 'PASS'),
      governanceFailClosed: ruleCount('GOVERNANCE_READINESS', 'FAIL_CLOSED'),
      processingHistoryPass: ruleCount('PROCESSING_HISTORY_AVAILABILITY', 'PASS'),
      processingHistoryFailClosed: ruleCount('PROCESSING_HISTORY_AVAILABILITY', 'FAIL_CLOSED'),
      uncorrelatedSources: sourceProjection.summary.uncorrelatedSources
    },
    authority: structuredClone(authority),
    limitations: [
      'Deterministic session/provenance-driven read-only projection; it is not an AI model output or scientific acceptance.',
      'Missing, partial, ambiguous or invalid processing evidence remains explicit and produces fail-closed rule outcomes.',
      'Raw BKL-045 sidecars are validated at build time; the published projection excludes host and workspace identifiers.',
      'No human decision, PixInsight execution, automatic acceptance, device command or Safety Authority is represented.'
    ],
    projectionDigest: ''
  };
  delete projection.projectionDigest;
  projection.projectionDigest = contentDigest(projection);
  validateAdvisoryProjection(projection);
  return deepFreeze(projection);
}

export function validateAdvisoryProjection(projection) {
  assertExactKeys(projection, FINAL_PROJECTION_KEYS, 'projection');
  assert(projection.schemaVersion === F4_SCHEMA_VERSION, 'Unsupported F4 schemaVersion.');
  assert(projection.projectionType === F4_PROJECTION_TYPE && projection.projectionState === F4_PROJECTION_STATE, 'Unsupported F4 projection type or state.');
  assert(projection.identityMethod === F4A_IDENTITY_METHOD, 'Unsupported F4 identity method.');
  assert(projection.producer === F4_PRODUCER && projection.producerVersion === F4_PRODUCER_VERSION, 'Unsupported F4 producer.');
  assert(projection.methodId === F3_METHOD_ID, 'F4 must reuse the accepted F3 method.');
  assert(Number.isFinite(Date.parse(projection.generatedAt)), 'Invalid F4 generatedAt.');
  assert(Array.isArray(projection.records) && Array.isArray(projection.sourceSet?.entries), 'F4 records and source entries are required.');
  const sourcePaths = projection.sourceSet.entries.map((entry) => entry.path);
  assert(canonicalJson(sourcePaths) === canonicalJson([...sourcePaths].sort()), 'F4 source entries must be sorted by path.');
  assert(new Set(sourcePaths).size === sourcePaths.length, 'F4 source entries must be unique.');
  projection.sourceSet.entries.forEach((entry, index) => {
    assertExactKeys(entry, SOURCE_ENTRY_KEYS, `sourceSet.entries[${index}]`);
    assertAllowedProvenancePath(entry.path);
    assert(/^[a-f0-9]{64}$/.test(entry.digest ?? ''), `Invalid source digest for ${entry.path}.`);
  });
  assert(projection.sourceSet.validationMode === 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT', 'Unsupported F4 source validation mode.');
  assert(projection.sourceSet.digest === contentDigest(projection.sourceSet.entries), 'F4 source-set digest mismatch.');
  const sourcePathSet = new Set(sourcePaths);
  const sessionIds = projection.records.map((record) => record.sessionId);
  assert(canonicalJson(sessionIds) === canonicalJson([...sessionIds].sort()), 'F4 records must be sorted by sessionId.');
  assert(new Set(sessionIds).size === sessionIds.length, 'F4 records must have unique session IDs.');
  for (const record of projection.records) {
    assertExactKeys(record, FINAL_RECORD_KEYS, `record.${record?.sessionId ?? 'unknown'}`);
    assert(CORRELATION_STATES.has(record.correlationState), `Unsupported correlation state for ${record.sessionId}.`);
    assert(canonicalJson(record.sourceRefs) === canonicalJson([...record.sourceRefs].sort()), `Record ${record.sessionId} sourceRefs must be sorted.`);
    assert(record.sourceRefs.every((sourceRef) => sourcePathSet.has(sourceRef)), `Record ${record.sessionId} references an unknown source.`);
    assert(record.recordId === `F4-${contentDigest({ sessionId: record.sessionId, sourceRefs: record.sourceRefs }).slice(0, 24).toUpperCase()}`, `Record identity mismatch for ${record.sessionId}.`);
    assert(record.inputArtifactDigest === contentDigest({ correlationState: record.correlationState, sourceBindings: record.sourceBindings, subject: record.subject }), `Input digest mismatch for ${record.sessionId}.`);
    assert(record.decisionState === 'NOT_PRESENT_PRE_DECISION', `Record ${record.sessionId} must remain pre-decision.`);
    assert(Array.isArray(record.recommendations) && record.recommendations.length === 2, `Record ${record.sessionId} must contain two F3 recommendations.`);
    record.recommendations.forEach((recommendation) => validateRecommendationRecord(recommendation, record.subject, record.sourceBindings));
    const expected = buildDeterministicAdvisoryRecords({
      inputArtifactDigest: record.inputArtifactDigest,
      generatedAt: projection.generatedAt,
      subject: record.subject,
      sourceBindings: record.sourceBindings,
      contextMode: F3_CONTEXTS.SESSION_PROVENANCE_READ_ONLY
    });
    assert(canonicalJson(record.recommendations) === canonicalJson(expected.recommendations), `F3 recommendations drift for ${record.sessionId}.`);
    assert(canonicalJson(record.ruleEvaluations) === canonicalJson(expected.ruleEvaluations), `F3 rule evaluations drift for ${record.sessionId}.`);
    const recordPreimage = structuredClone(record);
    delete recordPreimage.recordDigest;
    assert(record.recordDigest === contentDigest(recordPreimage), `Record digest mismatch for ${record.sessionId}.`);
  }
  assert(projection.sourceCatalog.path === CATALOG_PATH && /^[a-f0-9]{64}$/.test(projection.sourceCatalog.digest ?? ''), 'F4 catalog snapshot is invalid.');
  assert(projection.sourceCatalog.sessionCount === projection.records.length, 'F4 catalog count does not match records.');
  assert(canonicalJson(projection.sourceCatalog.sessionIds) === canonicalJson(sessionIds), 'F4 catalog session set does not match records.');
  assert(projection.projectionId === `BKL046-F4-${contentDigest({ catalogDigest: projection.sourceCatalog.digest, methodId: F3_METHOD_ID, sourceSetDigest: projection.sourceSet.digest }).slice(0, 24).toUpperCase()}`, 'F4 projection identity mismatch.');
  const count = (ruleId, decision) => projection.records.reduce(
    (total, record) => total + Number(record.ruleEvaluations.some((item) => item.ruleId === ruleId && item.decision === decision)),
    0
  );
  assert(projection.summary.totalSessions === projection.records.length, 'F4 summary total does not match records.');
  assert(projection.summary.governancePass === count('GOVERNANCE_READINESS', 'PASS'), 'F4 governance PASS summary is inconsistent.');
  assert(projection.summary.governanceFailClosed === count('GOVERNANCE_READINESS', 'FAIL_CLOSED'), 'F4 governance FAIL_CLOSED summary is inconsistent.');
  assert(projection.summary.processingHistoryPass === count('PROCESSING_HISTORY_AVAILABILITY', 'PASS'), 'F4 processing PASS summary is inconsistent.');
  assert(projection.summary.processingHistoryFailClosed === count('PROCESSING_HISTORY_AVAILABILITY', 'FAIL_CLOSED'), 'F4 processing FAIL_CLOSED summary is inconsistent.');
  assert(projection.authority.consumerMode === 'READ_ONLY' && projection.authority.acceptanceAuthority === 'HUMAN_ONLY', 'F4 authority must remain read-only and human-only.');
  assert(projection.authority.actionAuthority === 'NONE' && projection.authority.executionAuthority === 'NONE', 'F4 action and execution authority must be NONE.');
  assert(projection.authority.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'F4 Safety Authority is invalid.');
  assert(projection.authority.pixInsightApplyAuthorized === false && projection.authority.automaticAcceptanceAuthorized === false, 'F4 apply or auto-accept escalation is forbidden.');
  assertNoForbiddenPublicFields(projection);
  const preimage = structuredClone(projection);
  delete preimage.projectionDigest;
  assert(projection.projectionDigest === contentDigest(preimage), 'F4 projection digest mismatch.');
  return true;
}
