import assert from 'node:assert/strict';
import test from 'node:test';
import {
  assertAllowedProvenancePath,
  buildAdvisorySourceProjection,
  canonicalJson,
  contentDigest,
  validateAdvisorySourceProjection
} from './ai-post-processing-advisory-projection.mjs';

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
