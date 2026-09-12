import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import {
  sha256,
  validateAdvisoryProjectionContract,
  validateAdvisoryProjectionFreshness,
  validateRealEvidenceEvaluationContract,
  validateRealEvidenceEvaluationFreshness
} from '../../docs/javascripts/ai-post-processing-assistant-core.mjs';

const catalogPath = 'docs/data/scientific-session-catalog.json';
const projectionPath = 'docs/data/ai-post-processing-advisory-projection.json';
const evaluationPath = 'docs/data/ai-post-processing-advisory-f5-evaluation.json';
const uiPath = 'docs/javascripts/ai-post-processing-assistant.js';
const pagePath = 'docs/ai-post-processing-assistant/index.md';
const cssPath = 'docs/styles/ai-post-processing-assistant.css';

const authority = {
  consumerMode: 'READ_ONLY',
  advisoryOnly: true,
  acceptanceAuthority: 'HUMAN_ONLY',
  actionAuthority: 'NONE',
  executionAuthority: 'NONE',
  safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS',
  pixInsightApplyAuthorized: false,
  automaticAcceptanceAuthorized: false
};

async function seal(value, digestKey) {
  const result = structuredClone(value);
  delete result[digestKey];
  result[digestKey] = await sha256(result);
  return result;
}

async function buildFixture() {
  const generatedAt = '2026-09-12T08:00:00.000Z';
  const sessionId = '2026-09-11_2026-09-12';
  const catalog = {
    schemaVersion: '1.5',
    catalogStatus: 'VERSIONED_ANALYTICS_PROJECTION',
    sessions: [{ sessionId, target: 'M 27' }]
  };
  const catalogDigest = await sha256(catalog);
  const sourceEntries = [];
  const sourceSetDigest = await sha256(sourceEntries);
  const subject = {
    subjectId: 'SESSION-TEST000000000000000001',
    subjectType: 'PIXINSIGHT_WORKFLOW',
    assetRef: null,
    sessionRef: `${catalogPath}#${sessionId}`,
    workflowRef: null,
    stepRef: null,
    correlationState: 'RESOLVED'
  };
  const binding = await seal({
    bindingId: 'SRC-F4-CATALOG-TEST000000000001',
    semanticType: 'evidence',
    evidenceClass: 'DECLARED',
    sourceAuthority: 'repository_authority',
    sourceRef: catalogPath,
    lifecycleState: 'validated',
    quality: 'VALID',
    completeness: 'COMPLETE',
    citationRefs: [catalogPath],
    limitations: ['Catalog identity only.'],
    bindingDigest: ''
  }, 'bindingDigest');
  const sourceBindings = [binding];
  const inputArtifactDigest = await sha256({
    correlationState: 'PROVENANCE_UNAVAILABLE',
    sourceBindings,
    subject
  });
  const recommendation = async ({ id, category, lifecycleState, action, rationale, unknowns }) => seal({
    recommendationId: id,
    semanticType: 'recommendation',
    aiDerived: false,
    producer: 'DSG.DeterministicAdvisoryDemonstrator',
    producerVersion: '1.0.0-f3',
    methodId: 'BKL046-F3-CLOSED-RULES-1',
    generatedAt,
    correlationId: `CORR-${id}`,
    subjectRef: subject.subjectId,
    category,
    lifecycleState,
    proposedAction: action,
    rationale,
    sourceBindingRefs: [binding.bindingId],
    citationRefs: [catalogPath],
    provenanceRefs: [`PRV-${id}`],
    parameterAdvice: [],
    conflicts: [],
    unknowns,
    confidence: { state: 'UNAVAILABLE_F2', contractRef: null, value: null, limitations: ['No calibrated confidence.'] },
    limitations: ['Read-only deterministic guidance.'],
    recommendationDigest: ''
  }, 'recommendationDigest');
  const governanceRecommendation = await recommendation({
    id: 'REC-BKL046-F3-TEST000000000001',
    category: 'QUALITY_CHECK',
    lifecycleState: 'validated',
    action: 'Confirm the governed advisory boundary.',
    rationale: 'Repository authority is present.',
    unknowns: []
  });
  const historyRecommendation = await recommendation({
    id: 'REC-BKL046-F3-TEST000000000002',
    category: 'STOP_AND_REVIEW',
    lifecycleState: 'incomplete',
    action: 'Stop and review PixInsight evidence manually.',
    rationale: 'Required processing evidence is unavailable.',
    unknowns: ['REQUIRED_SOURCE_AUTHORITY_MISSING']
  });
  const sourceRefs = [];
  const record = await seal({
    recordId: `F4-${(await sha256({ sessionId, sourceRefs })).slice(0, 24).toUpperCase()}`,
    sessionId,
    target: 'M 27',
    correlationState: 'PROVENANCE_UNAVAILABLE',
    sourceRefs,
    inputArtifactDigest,
    subject,
    sourceBindings,
    recommendations: [governanceRecommendation, historyRecommendation],
    ruleEvaluations: [
      { ruleId: 'GOVERNANCE_READINESS', recommendationId: governanceRecommendation.recommendationId, decision: 'PASS', reasonCodes: [] },
      { ruleId: 'PROCESSING_HISTORY_AVAILABILITY', recommendationId: historyRecommendation.recommendationId, decision: 'FAIL_CLOSED', reasonCodes: ['REQUIRED_SOURCE_AUTHORITY_MISSING'] }
    ],
    decisionState: 'NOT_PRESENT_PRE_DECISION',
    recordDigest: ''
  }, 'recordDigest');
  const projection = await seal({
    schemaVersion: '1.1',
    projectionType: 'AI_POST_PROCESSING_ADVISORY_PROJECTION',
    projectionState: 'PRE_DECISION_READ_ONLY',
    identityMethod: 'BKL046-F4-CANONICAL-JSON-SHA256-1',
    projectionId: `BKL046-F4-${(await sha256({ catalogDigest, methodId: 'BKL046-F3-CLOSED-RULES-1', sourceSetDigest })).slice(0, 24).toUpperCase()}`,
    generatedAt,
    producer: 'DSG.AiPostProcessingAdvisoryProjection',
    producerVersion: '1.0.0-f4b',
    methodId: 'BKL046-F3-CLOSED-RULES-1',
    sourceCatalog: { path: catalogPath, digest: catalogDigest, sessionCount: 1, sessionIds: [sessionId] },
    sourceSet: { validationMode: 'RAW_BUILD_TIME_SANITIZED_PUBLIC_SNAPSHOT', digest: sourceSetDigest, entries: sourceEntries },
    records: [record],
    summary: {
      totalSessions: 1,
      provenanceMatched: 0,
      provenanceUnavailable: 1,
      correlationAmbiguous: 0,
      correlationInvalid: 0,
      governancePass: 1,
      governanceFailClosed: 0,
      processingHistoryPass: 0,
      processingHistoryFailClosed: 1,
      uncorrelatedSources: 0
    },
    authority,
    limitations: ['Read-only test fixture.'],
    projectionDigest: ''
  }, 'projectionDigest');
  return { catalog, projection };
}

const repositoryDataAvailable = fs.existsSync(catalogPath) && fs.existsSync(projectionPath) && fs.existsSync(evaluationPath);

function readPersistedChain() {
  return {
    catalog: JSON.parse(fs.readFileSync(catalogPath, 'utf8')),
    projection: JSON.parse(fs.readFileSync(projectionPath, 'utf8')),
    evaluation: JSON.parse(fs.readFileSync(evaluationPath, 'utf8'))
  };
}

test('current persisted projection passes the browser freshness chain', { skip: !repositoryDataAvailable }, async () => {
  const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
  const projection = JSON.parse(fs.readFileSync(projectionPath, 'utf8'));
  assert.equal(await validateAdvisoryProjectionFreshness(projection, catalog), true);
});

test('F5-EVAL-013 current persisted evaluation passes the complete browser freshness chain', { skip: !repositoryDataAvailable }, async () => {
  const { catalog, projection, evaluation } = readPersistedChain();
  assert.equal(validateRealEvidenceEvaluationContract(evaluation), true);
  assert.equal(await validateRealEvidenceEvaluationFreshness(evaluation, projection, catalog), true);
});

test('F5-EVAL-013 stale F4 snapshot makes the evaluation unavailable', { skip: !repositoryDataAvailable }, async () => {
  const { catalog, projection, evaluation } = readPersistedChain();
  const changed = structuredClone(evaluation);
  changed.sourceSnapshots.f4Projection.digest = 'a'.repeat(64);
  await assert.rejects(validateRealEvidenceEvaluationFreshness(changed, projection, catalog), /STALE_F5_PROJECTION_DIGEST_MISMATCH/);
});

test('F5-EVAL-013 evaluation payload tampering fails the digest check', { skip: !repositoryDataAvailable }, async () => {
  const { catalog, projection, evaluation } = readPersistedChain();
  const changed = structuredClone(evaluation);
  changed.limitations[0] = 'Altered after publication.';
  await assert.rejects(validateRealEvidenceEvaluationFreshness(changed, projection, catalog), /F5_EVALUATION_DIGEST_MISMATCH/);
});

test('F5-EVAL-013 F5 authority and scientific claims cannot be escalated', { skip: !repositoryDataAvailable }, () => {
  const { evaluation } = readPersistedChain();
  const authority = structuredClone(evaluation);
  authority.authority.automaticAcceptanceAuthorized = true;
  assert.throws(() => validateRealEvidenceEvaluationContract(authority), /automatic acceptance authority drift/);
  const scientific = structuredClone(evaluation);
  scientific.outcomes.scientific.state = 'INVALID';
  assert.throws(() => validateRealEvidenceEvaluationContract(scientific), /F5_SCIENTIFIC_EFFECTIVENESS_CLAIM_FORBIDDEN/);
});

test('F5-EVAL-013 missing Web Crypto keeps the F5 chain fail-closed', { skip: !repositoryDataAvailable }, async () => {
  const { catalog, projection, evaluation } = readPersistedChain();
  await assert.rejects(validateRealEvidenceEvaluationFreshness(evaluation, projection, catalog, null), /WEB_CRYPTO_SHA256_UNAVAILABLE/);
});

test('aligned projection and catalog are accepted', async () => {
  const { catalog, projection } = await buildFixture();
  assert.equal(validateAdvisoryProjectionContract(projection), true);
  assert.equal(await validateAdvisoryProjectionFreshness(projection, catalog), true);
});

test('new session without regenerated projection fails closed as stale', async () => {
  const { catalog, projection } = await buildFixture();
  const changed = structuredClone(catalog);
  changed.sessions.push({ sessionId: '2026-09-12_2026-09-13', target: 'M 31' });
  await assert.rejects(validateAdvisoryProjectionFreshness(projection, changed), /STALE_SOURCE_CATALOG_DIGEST_MISMATCH/);
});

test('tampered sanitized source snapshot is rejected', async () => {
  const { catalog, projection } = await buildFixture();
  const changed = structuredClone(projection);
  changed.sourceSet.entries.push({
    path: 'docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260912T080000000Z-TEST.json',
    digest: 'a'.repeat(64), sidecarId: 'PXP-TEST', exportedAt: '2026-09-12T08:00:00.000Z',
    sessionId: 'UNMATCHED-TEST', target: null, workflowId: 'WF-TEST', completeness: 'UNAVAILABLE', limitations: []
  });
  await assert.rejects(validateAdvisoryProjectionFreshness(changed, catalog), /SOURCE_SET_DIGEST_MISMATCH/);
});

test('record tampering is detected before rendering', async () => {
  const { catalog, projection } = await buildFixture();
  const changed = structuredClone(projection);
  changed.records[0].target = 'ALTERED';
  await assert.rejects(validateAdvisoryProjectionFreshness(changed, catalog), /RECORD_DIGEST_MISMATCH/);
});

test('projection summary tampering is detected', async () => {
  const { catalog, projection } = await buildFixture();
  const changed = structuredClone(projection);
  changed.summary.uncorrelatedSources = 1;
  await assert.rejects(validateAdvisoryProjectionFreshness(changed, catalog), /SUMMARY_UNCORRELATED_SOURCE_MISMATCH/);
});

test('authority escalation is rejected synchronously', async () => {
  const { projection } = await buildFixture();
  const changed = structuredClone(projection);
  changed.authority.pixInsightApplyAuthorized = true;
  assert.throws(() => validateAdvisoryProjectionContract(changed), /PixInsight apply authority drift/);
});

test('unknown contract properties are rejected', async () => {
  const { projection } = await buildFixture();
  const changed = structuredClone(projection);
  changed.automaticExecution = true;
  assert.throws(() => validateAdvisoryProjectionContract(changed), /proprietà mancanti o sconosciute/);
});

test('unknown nested F2 properties are rejected even with digest-shaped values', async () => {
  const { projection } = await buildFixture();
  const changed = structuredClone(projection);
  changed.records[0].recommendations[0].automaticApply = false;
  assert.throws(() => validateAdvisoryProjectionContract(changed), /proprietà mancanti o sconosciute/);
});

test('missing Web Crypto has no permissive fallback', async () => {
  const { catalog, projection } = await buildFixture();
  await assert.rejects(validateAdvisoryProjectionFreshness(projection, catalog, null), /WEB_CRYPTO_SHA256_UNAVAILABLE/);
});

test('F5-EVAL-014 portal preserves no-store, accessibility and non-mutative controls', () => {
  const ui = fs.readFileSync(uiPath, 'utf8');
  const page = fs.readFileSync(pagePath, 'utf8');
  const css = fs.readFileSync(cssPath, 'utf8');
  assert.equal((ui.match(/cache: 'no-store'/g) || []).length, 3);
  assert.match(ui, /ai-post-processing-advisory-f5-evaluation\.json/);
  assert.match(ui, /EVALUATION UNAVAILABLE · FAIL-CLOSED/);
  assert.match(ui, /F5 REAL-EVIDENCE EVALUATION/);
  assert.match(ui, /document\$\?\.subscribe/);
  assert.match(page, /aria-live="polite"/);
  assert.match(page, /AUTHORITY BOUNDARY/);
  assert.doesNotMatch(`${ui}\n${page}`, /<button[^>]*>\s*(Apply|Execute|Accept)/i);
  assert.match(css, /:focus-visible/);
  assert.match(css, /prefers-reduced-motion/);
  assert.match(css, /@media\(max-width:/);
});
