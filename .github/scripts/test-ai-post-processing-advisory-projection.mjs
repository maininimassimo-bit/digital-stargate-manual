import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import {
  assertAllowedProvenancePath,
  buildAdvisoryProjection,
  buildAdvisorySourceProjection,
  canonicalJson,
  contentDigest,
  validateAdvisoryProjection,
  validateAdvisorySourceProjection
} from './ai-post-processing-advisory-projection.mjs';
import { verifyWorkflowIntegration } from './verify-ai-post-processing-advisory-projection.mjs';

const pathFor = (stamp, suffix = 'OAT') => `docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-${stamp}-${suffix}.json`;
const catalog = () => ({
  schemaVersion: '1.5',
  catalogStatus: 'VERSIONED_ANALYTICS_PROJECTION',
  sessions: [
    { sessionId: 'SESSION-B', target: 'M31' },
    { sessionId: 'SESSION-A', target: 'M27' }
  ]
});
const sidecar = ({ id = 'PXP-20260911T120000000Z-OAT', sessionId = 'SESSION-A', target = 'M27', completeness = 'UNAVAILABLE' } = {}) => ({
  schemaVersion: '1.0',
  sidecarId: id,
  exportedAt: '2026-09-11T12:00:00.000Z',
  authority: 'processing_evidence',
  actionAuthority: 'NONE',
  source: {
    product: 'PixInsight',
    hostId: 'PRIVATE-HOST',
    workspaceId: 'PRIVATE-WORKSPACE'
  },
  observationContext: { sessionId, target },
  workflow: { workflowId: `WF-${sessionId}`, steps: [] },
  capture: { completeness, limitations: ['TEST_LIMITATION'] }
});
const build = (provenanceSources = []) => buildAdvisorySourceProjection({
  catalog: catalog(),
  provenanceSources,
  generatedAt: '2026-09-11T12:10:00Z'
});

test('closed BKL-045 allowlist accepts the governed path only', () => {
  assert.equal(assertAllowedProvenancePath(pathFor('20260911T120000000Z')), true);
  assert.throws(() => assertAllowedProvenancePath('docs/architecture/reviews/BKL-045-F3B-PXP-20260911T120000000Z-OAT.json'), /outside the BKL-045 allowlist/);
  assert.throws(() => assertAllowedProvenancePath('docs/architecture/scientific-assets/evidence/unrelated.json'), /outside the BKL-045 allowlist/);
});

test('absolute, backslash and traversal paths are rejected', () => {
  assert.throws(() => assertAllowedProvenancePath('/tmp/BKL-045-F3B-PXP-20260911T120000000Z-OAT.json'), /Absolute/);
  assert.throws(() => assertAllowedProvenancePath('docs\\architecture\\scientific-assets\\evidence\\BKL-045-F3B-PXP-20260911T120000000Z-OAT.json'), /Backslash/);
  assert.throws(() => assertAllowedProvenancePath('docs/architecture/scientific-assets/evidence/../BKL-045-F3B-PXP-20260911T120000000Z-OAT.json'), /traversal/);
});

test('catalog population and projection records are deterministically ordered', () => {
  const first = build([
    { path: pathFor('20260911T120001000Z', 'B'), payload: sidecar({ id: 'PXP-B', sessionId: 'UNRELATED-B' }) },
    { path: pathFor('20260911T120000000Z', 'A'), payload: sidecar({ id: 'PXP-A', sessionId: 'UNRELATED-A' }) }
  ]);
  const second = build([
    { path: pathFor('20260911T120000000Z', 'A'), payload: sidecar({ id: 'PXP-A', sessionId: 'UNRELATED-A' }) },
    { path: pathFor('20260911T120001000Z', 'B'), payload: sidecar({ id: 'PXP-B', sessionId: 'UNRELATED-B' }) }
  ]);
  assert.deepEqual(first, second);
  assert.deepEqual(first.records.map((item) => item.sessionId), ['SESSION-A', 'SESSION-B']);
  assert.deepEqual(first.sourceSet.entries.map((item) => item.sidecarId), ['PXP-A', 'PXP-B']);
});

test('duplicate paths and sidecar identities are rejected', () => {
  const repositoryPath = pathFor('20260911T120000000Z');
  assert.throws(() => build([
    { path: repositoryPath, payload: sidecar() },
    { path: repositoryPath, payload: sidecar({ id: 'PXP-OTHER' }) }
  ]), /Duplicate provenance paths/);
  assert.throws(() => build([
    { path: repositoryPath, payload: sidecar() },
    { path: pathFor('20260911T120001000Z'), payload: sidecar() }
  ]), /Duplicate provenance sidecarId/);
});

test('missing processing evidence is retained as an explicit fail-closed record', () => {
  const result = build();
  assert.equal(result.summary.totalSessions, 2);
  assert.equal(result.summary.provenanceUnavailable, 2);
  assert.equal(result.summary.failClosed, 2);
  assert(result.records.every((record) => record.correlationState === 'PROVENANCE_UNAVAILABLE'));
  assert(result.records.every((record) => record.reasonCodes.includes('PROCESSING_EVIDENCE_UNAVAILABLE')));
});

test('incomplete matched provenance remains fail-closed with preserved missingness', () => {
  const result = build([{ path: pathFor('20260911T120000000Z'), payload: sidecar() }]);
  const record = result.records.find((item) => item.sessionId === 'SESSION-A');
  assert.equal(record.correlationState, 'PROVENANCE_MATCHED');
  assert.equal(record.gateState, 'FAIL_CLOSED');
  assert.deepEqual(record.reasonCodes, ['SOURCE_COMPLETENESS_UNAVAILABLE']);
  assert.equal(record.advisoryInput.processingEvidence.quality, 'UNKNOWN');
});

test('complete exact-match provenance becomes source-ready without generating advice', () => {
  const result = build([{ path: pathFor('20260911T120000000Z'), payload: sidecar({ completeness: 'COMPLETE' }) }]);
  const record = result.records.find((item) => item.sessionId === 'SESSION-A');
  assert.equal(record.gateState, 'SOURCE_READY');
  assert.deepEqual(record.reasonCodes, []);
  assert.equal(record.recommendationState, 'NOT_GENERATED_F4A');
  assert.equal(Object.hasOwn(record, 'recommendations'), false);
});

test('target disagreement is correlation-invalid and fail-closed', () => {
  const result = build([{ path: pathFor('20260911T120000000Z'), payload: sidecar({ target: 'M42', completeness: 'COMPLETE' }) }]);
  const record = result.records.find((item) => item.sessionId === 'SESSION-A');
  assert.equal(record.correlationState, 'CORRELATION_INVALID');
  assert.deepEqual(record.reasonCodes, ['SOURCE_TARGET_MISMATCH']);
});

test('multiple candidates are correlation-ambiguous and fail-closed', () => {
  const result = build([
    { path: pathFor('20260911T120000000Z', 'A'), payload: sidecar({ id: 'PXP-A' }) },
    { path: pathFor('20260911T120001000Z', 'B'), payload: sidecar({ id: 'PXP-B' }) }
  ]);
  const record = result.records.find((item) => item.sessionId === 'SESSION-A');
  assert.equal(record.correlationState, 'CORRELATION_AMBIGUOUS');
  assert.deepEqual(record.reasonCodes, ['MULTIPLE_PROCESSING_EVIDENCE_CANDIDATES']);
});

test('raw private host and workspace identifiers never enter the public snapshot', () => {
  const result = build([{ path: pathFor('20260911T120000000Z'), payload: sidecar() }]);
  const serialized = canonicalJson(result);
  assert.equal(serialized.includes('PRIVATE-HOST'), false);
  assert.equal(serialized.includes('PRIVATE-WORKSPACE'), false);
  assert.equal(serialized.includes('hostId'), false);
  assert.equal(serialized.includes('workspaceId'), false);
});

test('unsupported source authority and action escalation are rejected', () => {
  const invalidAuthority = sidecar();
  invalidAuthority.authority = 'fixture';
  assert.throws(() => build([{ path: pathFor('20260911T120000000Z'), payload: invalidAuthority }]), /unsupported authority/);
  const escalation = sidecar();
  escalation.actionAuthority = 'PIXINSIGHT_APPLY';
  assert.throws(() => build([{ path: pathFor('20260911T120000000Z'), payload: escalation }]), /escalates action authority/);
});

test('projection and record tampering are detected', () => {
  const result = structuredClone(build());
  result.records[0].reasonCodes = [];
  assert.throws(() => validateAdvisorySourceProjection(result), /gate and reason codes disagree|Record digest mismatch/);
  const resealed = structuredClone(build());
  resealed.authority.actionAuthority = 'PIXINSIGHT_APPLY';
  delete resealed.projectionDigest;
  resealed.projectionDigest = contentDigest(resealed);
  assert.throws(() => validateAdvisorySourceProjection(resealed), /action and execution authority must be NONE/);
});

test('publication timestamp cannot change projection or record identity', () => {
  const first = build();
  const second = buildAdvisorySourceProjection({ catalog: catalog(), provenanceSources: [], generatedAt: '2026-09-11T13:10:00Z' });
  assert.equal(first.projectionId, second.projectionId);
  assert.deepEqual(first.records.map((item) => item.recordId), second.records.map((item) => item.recordId));
  assert.notEqual(first.projectionDigest, second.projectionDigest);
});

test('builder output is deeply immutable and validates against its closed invariants', () => {
  const result = build();
  assert.equal(Object.isFrozen(result), true);
  assert.equal(Object.isFrozen(result.records[0]), true);
  assert.equal(validateAdvisorySourceProjection(result), true);
});

const buildFinal = (provenanceSources = [], generatedAt = '2026-09-11T12:10:00Z') => buildAdvisoryProjection({
  catalog: catalog(),
  provenanceSources,
  generatedAt
});

function rule(record, ruleId) {
  return record.ruleEvaluations.find((item) => item.ruleId === ruleId);
}

test('F4-B generates two F2-valid F3 recommendations per catalog session', () => {
  const result = buildFinal();
  assert.equal(result.schemaVersion, '1.1');
  assert.equal(result.records.length, 2);
  assert(result.records.every((record) => record.recommendations.length === 2));
  assert(result.records.every((record) => record.decisionState === 'NOT_PRESENT_PRE_DECISION'));
  assert.equal(validateAdvisoryProjection(result), true);
});

test('resolved catalog authority passes while absent processing evidence fails closed', () => {
  const result = buildFinal();
  const record = result.records[0];
  assert.equal(rule(record, 'GOVERNANCE_READINESS').decision, 'PASS');
  assert.equal(rule(record, 'PROCESSING_HISTORY_AVAILABILITY').decision, 'FAIL_CLOSED');
  assert.deepEqual(rule(record, 'PROCESSING_HISTORY_AVAILABILITY').reasonCodes, ['REQUIRED_SOURCE_AUTHORITY_MISSING']);
  assert.equal(result.summary.governancePass, 2);
  assert.equal(result.summary.processingHistoryFailClosed, 2);
});

test('matched incomplete evidence preserves F3 missingness reason codes', () => {
  const result = buildFinal([{ path: pathFor('20260911T120000000Z'), payload: sidecar() }]);
  const record = result.records.find((item) => item.sessionId === 'SESSION-A');
  const evaluation = rule(record, 'PROCESSING_HISTORY_AVAILABILITY');
  assert.equal(evaluation.decision, 'FAIL_CLOSED');
  assert.deepEqual(evaluation.reasonCodes, ['SOURCE_COMPLETENESS_UNAVAILABLE', 'SOURCE_QUALITY_UNKNOWN']);
  const recommendation = record.recommendations.find((item) => item.recommendationId === evaluation.recommendationId);
  assert.equal(recommendation.category, 'STOP_AND_REVIEW');
  assert.equal(recommendation.parameterAdvice[0].mode, 'UNKNOWN_NOT_RECOMMENDED');
});

test('matched complete evidence passes both accepted F3 rules without parameter invention', () => {
  const result = buildFinal([{ path: pathFor('20260911T120000000Z'), payload: sidecar({ completeness: 'COMPLETE' }) }]);
  const record = result.records.find((item) => item.sessionId === 'SESSION-A');
  assert(record.ruleEvaluations.every((item) => item.decision === 'PASS'));
  assert(record.recommendations.every((item) => item.parameterAdvice.length === 0));
  assert(record.recommendations.every((item) => item.aiDerived === false));
});

test('ambiguous correlation causes both F3 rules to fail closed', () => {
  const result = buildFinal([
    { path: pathFor('20260911T120000000Z', 'A'), payload: sidecar({ id: 'PXP-A' }) },
    { path: pathFor('20260911T120001000Z', 'B'), payload: sidecar({ id: 'PXP-B' }) }
  ]);
  const record = result.records.find((item) => item.sessionId === 'SESSION-A');
  assert.equal(record.subject.correlationState, 'PARTIAL');
  assert(record.ruleEvaluations.every((item) => item.decision === 'FAIL_CLOSED'));
  assert(record.ruleEvaluations.every((item) => item.reasonCodes.includes('SUBJECT_CORRELATION_PARTIAL')));
});

test('final projection is deterministic for equivalent source ordering', () => {
  const sources = [
    { path: pathFor('20260911T120001000Z', 'B'), payload: sidecar({ id: 'PXP-B', sessionId: 'UNRELATED-B' }) },
    { path: pathFor('20260911T120000000Z', 'A'), payload: sidecar({ id: 'PXP-A', sessionId: 'UNRELATED-A' }) }
  ];
  assert.deepEqual(buildFinal(sources), buildFinal([...sources].reverse()));
});

test('a newly imported catalog session is added automatically without changing existing record identities', () => {
  const before = buildFinal();
  const expandedCatalog = catalog();
  expandedCatalog.sessions.push({ sessionId: 'SESSION-C', target: 'M42' });
  const after = buildAdvisoryProjection({
    catalog: expandedCatalog,
    provenanceSources: [],
    generatedAt: '2026-09-11T12:10:00Z'
  });
  assert.equal(after.records.length, 3);
  assert.notEqual(after.projectionId, before.projectionId);
  assert.equal(after.records.find((item) => item.sessionId === 'SESSION-A').recordId, before.records.find((item) => item.sessionId === 'SESSION-A').recordId);
  const imported = after.records.find((item) => item.sessionId === 'SESSION-C');
  assert.equal(imported.correlationState, 'PROVENANCE_UNAVAILABLE');
  assert.equal(rule(imported, 'PROCESSING_HISTORY_AVAILABILITY').decision, 'FAIL_CLOSED');
});

test('final projection sanitizes private raw fields and preserves closed authority', () => {
  const result = buildFinal([{ path: pathFor('20260911T120000000Z'), payload: sidecar() }]);
  const serialized = canonicalJson(result);
  assert.equal(serialized.includes('PRIVATE-HOST'), false);
  assert.equal(serialized.includes('PRIVATE-WORKSPACE'), false);
  assert.equal(result.authority.actionAuthority, 'NONE');
  assert.equal(result.authority.executionAuthority, 'NONE');
  assert.equal(result.authority.safetyAuthority, 'LOCAL_PHYSICAL_INTERLOCKS');
});

test('final projection rule, record and authority tampering is rejected', () => {
  const ruleTamper = structuredClone(buildFinal());
  ruleTamper.records[0].ruleEvaluations[0].decision = 'FAIL_CLOSED';
  assert.throws(() => validateAdvisoryProjection(ruleTamper), /rule evaluations drift|Record digest mismatch/);
  const authorityTamper = structuredClone(buildFinal());
  authorityTamper.authority.automaticAcceptanceAuthorized = true;
  delete authorityTamper.projectionDigest;
  authorityTamper.projectionDigest = contentDigest(authorityTamper);
  assert.throws(() => validateAdvisoryProjection(authorityTamper), /auto-accept escalation is forbidden/);
});

test('automatic import workflow contains first path, retry path and atomic governed output', () => {
  const workflow = fs.readFileSync('.github/workflows/analyze-session-automatic.yml', 'utf8');
  assert.equal(verifyWorkflowIntegration(workflow), true);
  assert.throws(() => verifyWorkflowIntegration(workflow.replace('node .github/scripts/generate-ai-post-processing-advisory-projection.mjs --write', 'node .github/scripts/generate-ai-post-processing-advisory-projection.mjs')), /--write must exist in first and retry/);
  assert.throws(() => verifyWorkflowIntegration(workflow.replaceAll('docs/data/ai-post-processing-advisory-projection.json', 'docs/data/removed.json')), /included in governed_paths/);
});
