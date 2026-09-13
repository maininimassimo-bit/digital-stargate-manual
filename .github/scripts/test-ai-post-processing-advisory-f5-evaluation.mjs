import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { buildAdvisoryProjection } from './ai-post-processing-advisory-projection.mjs';
import {
  assertAllowedExecutionEvidencePath,
  assertAllowedHumanDecisionPath,
  buildRealEvidenceEvaluation,
  canonicalJson,
  contentDigest,
  discoverExecutionEvidenceSources,
  discoverHumanDecisionSources,
  validateRawExecutionEvidenceSource,
  validateRawHumanDecisionSource,
  validateRealEvidenceEvaluation
} from './ai-post-processing-advisory-real-evidence-evaluation.mjs';
import { verifyAtomicWorkflowIntegration } from './verify-ai-post-processing-advisory-f5-evaluation.mjs';

const GENERATED_AT = '2026-09-12T07:30:00.000Z';
const DECISION_PATH = 'docs/data/ai-post-processing-human-decisions/BKL-046-F2-HDR-20260912T070000Z-TEST.json';
const DECISION_PATH_2 = 'docs/data/ai-post-processing-human-decisions/BKL-046-F2-HDR-20260912T070100Z-TEST2.json';
const EXECUTION_PATH = 'docs/data/ai-post-processing-execution-evidence/BKL-046-F5-EXE-20260912T071000Z-TEST.json';

const [catalog, baselineProjection] = await Promise.all([
  readFile('docs/data/scientific-session-catalog.json', 'utf8').then(JSON.parse),
  readFile('docs/data/ai-post-processing-advisory-projection.json', 'utf8').then(JSON.parse)
]);

function seal(value, digestKey) {
  delete value[digestKey];
  value[digestKey] = contentDigest(value);
  return value;
}

function firstRecommendation(projection = baselineProjection) {
  const record = projection.records[0];
  return { record, recommendation: record.recommendations[0] };
}

function decisionSource(projection = baselineProjection, overrides = {}) {
  const { record, recommendation } = firstRecommendation(projection);
  const receipt = seal({
    receiptId: 'HDR-F5A-TEST-001',
    recommendationId: recommendation.recommendationId,
    presentedAt: '2026-09-12T07:00:00.000Z',
    decidedAt: '2026-09-12T07:05:00.000Z',
    actorRef: 'HUMAN-OPERATOR-TEST',
    disposition: 'DEFERRED',
    decisionEdits: [],
    decisionRationale: null,
    correlationId: recommendation.correlationId,
    executionState: 'NOT_OBSERVED',
    executionEvidenceRefs: [],
    actionAuthority: 'NONE',
    receiptDigest: ''
  }, 'receiptDigest');
  const payload = {
    schemaVersion: '1.0',
    sourceType: 'BKL046_HUMAN_DECISION_RECEIPT',
    authority: 'human_decision',
    sessionId: record.sessionId,
    recommendationId: recommendation.recommendationId,
    receipt,
    artifactDigest: ''
  };
  Object.assign(payload, overrides);
  if (overrides.receipt) payload.receipt = overrides.receipt;
  return seal(payload, 'artifactDigest');
}

function resealDecision(payload) {
  seal(payload.receipt, 'receiptDigest');
  return seal(payload, 'artifactDigest');
}

function matchedProjection() {
  const record = baselineProjection.records[0];
  const source = baselineProjection.sourceSet.entries[0];
  return buildAdvisoryProjection({
    catalog,
    provenanceSources: [{
      path: source.path,
      payload: {
        schemaVersion: '1.0',
        sidecarId: 'PXP-F5A-EXACT-CORRELATION-TEST',
        exportedAt: '2026-09-12T06:55:00.000Z',
        authority: 'processing_evidence',
        actionAuthority: 'NONE',
        source: { product: 'PixInsight', hostId: 'PRIVATE-TEST-HOST', workspaceId: 'PRIVATE-TEST-WORKSPACE' },
        observationContext: { sessionId: record.sessionId, target: record.target },
        workflow: { workflowId: 'WF-F5A-EXACT-CORRELATION-TEST', steps: [] },
        capture: { completeness: 'COMPLETE', limitations: ['Synthetic test source; not production evidence.'] }
      }
    }],
    generatedAt: baselineProjection.generatedAt
  });
}

function executionSource(projection, humanPayload, overrides = {}) {
  const source = projection.sourceSet.entries[0];
  const payload = {
    schemaVersion: '1.0',
    sourceType: 'BKL046_RECOMMENDATION_EXECUTION_EVIDENCE',
    authority: 'processing_execution_evidence',
    evidenceId: 'EXE-F5A-TEST-001',
    sessionId: humanPayload.sessionId,
    recommendationId: humanPayload.recommendationId,
    decisionReceiptId: humanPayload.receipt.receiptId,
    processingEvidenceRef: source.path,
    observedAt: '2026-09-12T07:10:00.000Z',
    executionState: 'OBSERVED_MANUAL_EXECUTION',
    actionAuthority: 'NONE',
    artifactDigest: ''
  };
  Object.assign(payload, overrides);
  return seal(payload, 'artifactDigest');
}

function build(overrides = {}) {
  return buildRealEvidenceEvaluation({
    catalog,
    f4Projection: baselineProjection,
    humanDecisionSources: [],
    executionEvidenceSources: [],
    generatedAt: GENERATED_AT,
    ...overrides
  });
}

function targetDistribution(sessions) {
  const counts = new Map();
  for (const session of sessions) {
    const target = session.target || 'UNKNOWN';
    counts.set(target, (counts.get(target) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([target, count]) => ({ target, count }));
}

test('F5C-UT-001 closure report validates with a closed schema-shaped contract', () => {
  const report = build();
  assert.equal(validateRealEvidenceEvaluation(report), true);
  assert.equal(report.schemaVersion, '2.0');
  assert.equal(report.evaluationState, 'F5C_CLOSURE_EVALUATED');
  assert.equal(report.outcomes.technical.state, 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS');
  assert.equal(report.outcomes.capabilityOutcome, 'ACCEPTED_READ_ONLY_WITH_LIMITATIONS');
  assert.equal(report.outcomes.closureRecommendation, 'CLOSE_DETERMINISTIC_CAPABILITY');
  assert.equal(report.outcomes.scientific.state, 'NOT_EVALUABLE_CURRENT_EVIDENCE');
  assert.equal(report.outcomes.production.state, 'NOT_READY_FOR_PRODUCTION');
  assert.equal(report.outcomes.aiModelImplemented, false);
  assert.equal(report.technicalGates.every(({ state }) => state === 'PASS'), true);
});

test('F5A-UT-002 full population equals the canonical catalog session set', () => {
  const report = build();
  assert.equal(report.summary.canonicalSessions, catalog.sessions.length);
  assert.deepEqual(report.cohorts[0].memberRefs, [...baselineProjection.sourceCatalog.sessionIds].sort());
  assert.equal(report.cohorts[0].eligibleCount, catalog.sessions.length);
});

test('F5A-UT-003 baseline report preserves catalog-derived observed counts', () => {
  const report = build();
  assert.deepEqual(
    {
      sessions: report.summary.canonicalSessions,
      provenance: report.summary.provenanceEligible,
      decisions: report.summary.humanDecisionReceipts,
      executions: report.summary.executionEvidence,
      uncorrelated: report.summary.uncorrelatedProcessingSources
    },
    { sessions: catalog.sessions.length, provenance: 0, decisions: 0, executions: 0, uncorrelated: 2 }
  );
  assert.deepEqual(report.summary.targetDistribution, targetDistribution(catalog.sessions));
});

test('F5A-UT-004 empty cohorts are not reported as success or percentages', () => {
  const report = build();
  assert.equal(report.cohorts[1].evidenceState, 'NOT_EVALUABLE');
  assert.equal(report.cohorts[2].evidenceState, 'NOT_AVAILABLE');
  assert.equal(report.cohorts[3].evidenceState, 'NOT_AVAILABLE');
  assert.equal(JSON.stringify(report).includes('%'), false);
  assert.equal(report.outcomes.scientific.state, 'NOT_EVALUABLE_CURRENT_EVIDENCE');
});

test('F5A-UT-005 source paths reject traversal and non-allowlisted files', () => {
  assert.throws(() => assertAllowedHumanDecisionPath('../receipt.json'), /traversal|allowlist/);
  assert.throws(() => assertAllowedExecutionEvidencePath('docs/data/execution.json'), /allowlist/);
});

test('F5A-UT-006 identity and digest are deterministic across timestamps', () => {
  const left = build({ generatedAt: '2026-09-12T07:30:00.000Z' });
  const right = build({ generatedAt: '2026-09-12T08:30:00.000Z' });
  assert.equal(left.evaluationId, right.evaluationId);
  assert.notEqual(left.evaluationDigest, right.evaluationDigest);
  const stripClock = (value) => {
    const clone = structuredClone(value);
    delete clone.generatedAt;
    delete clone.evaluationDigest;
    return clone;
  };
  assert.equal(canonicalJson(stripClock(left)), canonicalJson(stripClock(right)));
});

test('F5A-UT-007 tampered F4 projection fails closed', () => {
  const tampered = structuredClone(baselineProjection);
  tampered.summary.provenanceMatched = 99;
  assert.throws(() => build({ f4Projection: tampered }), /projection digest mismatch/i);
});

test('F5A-UT-008 catalog/F4 population drift fails closed', () => {
  const drifted = structuredClone(catalog);
  drifted.sessions.push({ sessionId: 'F5-ORPHAN', target: 'UNKNOWN' });
  assert.throws(() => build({ catalog: drifted }), /record set|source catalog digest/);
});

test('F5A-UT-009 Human Decision source rejects authority and execution claims', () => {
  const wrongAuthority = decisionSource();
  wrongAuthority.authority = 'projection';
  seal(wrongAuthority, 'artifactDigest');
  assert.throws(() => validateRawHumanDecisionSource(DECISION_PATH, wrongAuthority), /unsupported authority/);

  const executionClaim = decisionSource();
  executionClaim.receipt.executionState = 'OBSERVED';
  seal(executionClaim.receipt, 'receiptDigest');
  seal(executionClaim, 'artifactDigest');
  assert.throws(() => validateRawHumanDecisionSource(DECISION_PATH, executionClaim), /must not claim execution/);
});

test('F5A-UT-010 orphan Human Decision recommendation fails exact correlation', () => {
  const orphan = decisionSource();
  orphan.recommendationId = 'REC-UNKNOWN';
  orphan.receipt.recommendationId = 'REC-UNKNOWN';
  seal(orphan.receipt, 'receiptDigest');
  seal(orphan, 'artifactDigest');
  assert.throws(
    () => build({ humanDecisionSources: [{ path: DECISION_PATH, payload: orphan }] }),
    /unknown recommendation/
  );
});

test('F5A-UT-011 duplicate Human Decision receipt identity is rejected', () => {
  const payload = decisionSource();
  assert.throws(
    () => build({
      humanDecisionSources: [
        { path: DECISION_PATH, payload },
        { path: DECISION_PATH_2, payload }
      ]
    }),
    /Duplicate Human Decision receiptId/
  );
});

test('F5A-UT-012 execution evidence requires an exact decision link', () => {
  const projection = matchedProjection();
  const human = decisionSource(projection);
  const execution = executionSource(projection, human, { decisionReceiptId: 'HDR-UNKNOWN' });
  assert.throws(
    () => build({
      f4Projection: projection,
      humanDecisionSources: [{ path: DECISION_PATH, payload: human }],
      executionEvidenceSources: [{ path: EXECUTION_PATH, payload: execution }]
    }),
    /unknown decision receipt/
  );
});

test('F5A-UT-013 execution evidence cannot predate the Human Decision', () => {
  const projection = matchedProjection();
  const human = decisionSource(projection);
  const execution = executionSource(projection, human, { observedAt: '2026-09-12T07:04:59.000Z' });
  assert.throws(
    () => build({
      f4Projection: projection,
      humanDecisionSources: [{ path: DECISION_PATH, payload: human }],
      executionEvidenceSources: [{ path: EXECUTION_PATH, payload: execution }]
    }),
    /predates/
  );
});

test('F5A-UT-014 execution evidence must reference an accepted BKL-045 source', () => {
  const projection = matchedProjection();
  const human = decisionSource(projection);
  const execution = executionSource(projection, human, {
    processingEvidenceRef: 'docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260912T071000000Z-UNKNOWN.json'
  });
  assert.throws(
    () => build({
      f4Projection: projection,
      humanDecisionSources: [{ path: DECISION_PATH, payload: human }],
      executionEvidenceSources: [{ path: EXECUTION_PATH, payload: execution }]
    }),
    /unknown BKL-045/
  );
});

test('F5A-UT-015 exact receipt and execution sources populate separate cohorts', () => {
  const projection = matchedProjection();
  const human = decisionSource(projection);
  const execution = executionSource(projection, human);
  const report = build({
    f4Projection: projection,
    humanDecisionSources: [{ path: DECISION_PATH, payload: human }],
    executionEvidenceSources: [{ path: EXECUTION_PATH, payload: execution }]
  });
  assert.equal(report.summary.provenanceEligible, 1);
  assert.equal(report.summary.humanDecisionReceipts, 1);
  assert.equal(report.summary.executionEvidence, 1);
  assert.equal(report.outcomes.humanDecision.state, 'AVAILABLE');
  assert.equal(report.outcomes.scientific.state, 'NOT_EVALUABLE_CURRENT_EVIDENCE');
  assert.equal(report.outcomes.closureRecommendation, 'CLOSE_DETERMINISTIC_CAPABILITY');
});

test('F5A-UT-016 unknown outcome states and reason codes are rejected', () => {
  const stateDrift = structuredClone(build());
  stateDrift.outcomes.scientific.state = 'SUCCESS';
  assert.throws(() => validateRealEvidenceEvaluation(stateDrift), /Unknown scientific outcome/);

  const reasonDrift = structuredClone(build());
  reasonDrift.cohorts[1].reasonCodes = ['ZERO_DEFECTS'];
  assert.throws(() => validateRealEvidenceEvaluation(reasonDrift), /unknown reason codes/);
});

test('F5A-UT-017 report tampering and additional properties are rejected', () => {
  const tampered = structuredClone(build());
  tampered.summary.provenanceEligible = 1;
  assert.throws(() => validateRealEvidenceEvaluation(tampered), /summary\/cohort mismatch|evaluationDigest mismatch/);

  const extra = structuredClone(build());
  extra.scientificConfidence = 1;
  assert.throws(() => validateRealEvidenceEvaluation(extra), /is not allowed/);
});

test('F5C-UT-018 authority escalation and closure downgrade are rejected', () => {
  const authority = structuredClone(build());
  authority.authority.pixInsightApplyAuthorized = true;
  assert.throws(() => validateRealEvidenceEvaluation(authority), /authority drift/);

  const closure = structuredClone(build());
  closure.outcomes.closureRecommendation = 'KEEP_OPEN';
  assert.throws(() => validateRealEvidenceEvaluation(closure), /may close only/);
});

test('F5A-UT-019 missing governed source directories are valid empty sets', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'dsg-f5a-missing-'));
  try {
    assert.deepEqual(await discoverHumanDecisionSources(root), []);
    assert.deepEqual(await discoverExecutionEvidenceSources(root), []);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('F5A-UT-020 unknown files in governed source directories fail closed', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'dsg-f5a-unknown-'));
  try {
    const directory = path.join(root, 'docs/data/ai-post-processing-human-decisions');
    await mkdir(directory, { recursive: true });
    await writeFile(path.join(directory, 'unexpected.json'), '{}\n', 'utf8');
    await assert.rejects(() => discoverHumanDecisionSources(root), /Unknown file/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('F5A-UT-021 raw execution contract rejects authority escalation', () => {
  const projection = matchedProjection();
  const human = decisionSource(projection);
  const execution = executionSource(projection, human, { actionAuthority: 'APPLY' });
  assert.throws(() => validateRawExecutionEvidenceSource(EXECUTION_PATH, execution), /escalates action authority/);
});

test('F5A-UT-022 governed source directories reject nested or non-file entries', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'dsg-f5a-nested-'));
  try {
    const directory = path.join(root, 'docs/data/ai-post-processing-execution-evidence');
    await mkdir(path.join(directory, 'nested'), { recursive: true });
    await assert.rejects(() => discoverExecutionEvidenceSources(root), /Unknown non-file entry/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('F5A-UT-023 recomputed internal F4 drift is rejected by the canonical validator', () => {
  const tampered = structuredClone(baselineProjection);
  tampered.records[0].decisionState = 'PRESENT';
  seal(tampered.records[0], 'recordDigest');
  seal(tampered, 'projectionDigest');
  assert.throws(() => build({ f4Projection: tampered }), /pre-decision/);
});

test('F5A-UT-024 raw Human Decision admission enforces F2 stable IDs and bounds', () => {
  const invalidReceiptId = decisionSource();
  invalidReceiptId.receipt.receiptId = 'INVALID RECEIPT ID';
  assert.throws(() => validateRawHumanDecisionSource(DECISION_PATH, resealDecision(invalidReceiptId)), /stableId pattern/);

  const invalidActor = decisionSource();
  invalidActor.receipt.actorRef = 'X';
  assert.throws(() => validateRawHumanDecisionSource(DECISION_PATH, resealDecision(invalidActor)), /shorter than the F2 minimum/);

  const invalidEdit = decisionSource();
  invalidEdit.receipt.disposition = 'EDITED_FOR_MANUAL_APPLICATION';
  invalidEdit.receipt.decisionEdits = [{ arbitrary: 'not-an-F2-decision-edit' }];
  assert.throws(() => validateRawHumanDecisionSource(DECISION_PATH, resealDecision(invalidEdit)), /is not allowed/);

  const excessiveEdits = decisionSource();
  excessiveEdits.receipt.disposition = 'EDITED_FOR_MANUAL_APPLICATION';
  excessiveEdits.receipt.decisionEdits = Array.from({ length: 33 }, (_, index) => ({
    parameterId: `PARAM-${index}`,
    selectedValue: index,
    unit: null,
    reason: 'Test'
  }));
  assert.throws(() => validateRawHumanDecisionSource(DECISION_PATH, resealDecision(excessiveEdits)), /exceeds the F2 maximum/);

  const excessiveRationale = decisionSource();
  excessiveRationale.receipt.decisionRationale = 'X'.repeat(4097);
  assert.throws(() => validateRawHumanDecisionSource(DECISION_PATH, resealDecision(excessiveRationale)), /decisionRationale is invalid/);
});

test('F5A-UT-025 source-set metadata is pinned after digest recomputation', () => {
  const wrongDirectory = structuredClone(build());
  wrongDirectory.sourceSnapshots.humanDecisionSourceSet.directory = 'wrong-directory';
  seal(wrongDirectory, 'evaluationDigest');
  assert.throws(() => validateRealEvidenceEvaluation(wrongDirectory), /directory is outside the closed contract/);

  const wrongPattern = structuredClone(build());
  wrongPattern.sourceSnapshots.executionEvidenceSourceSet.pathPattern = '.*';
  seal(wrongPattern, 'evaluationDigest');
  assert.throws(() => validateRealEvidenceEvaluation(wrongPattern), /pathPattern is outside the closed contract/);
});

test('F5-EVAL-011 first and retry paths regenerate and verify F5 after F4', async () => {
  const workflow = await readFile('.github/workflows/analyze-session-automatic.yml', 'utf8');
  assert.equal(verifyAtomicWorkflowIntegration(workflow), true);
});

test('F5-EVAL-012 atomic path validation rejects an omitted F5 report', async () => {
  const workflow = await readFile('.github/workflows/analyze-session-automatic.yml', 'utf8');
  const changed = workflow.replace('docs/data/ai-post-processing-advisory-f5-evaluation.json ', '');
  assert.throws(() => verifyAtomicWorkflowIntegration(changed), /atomic governed path set/);
});

test('F5-EVAL-012 retry validation rejects F5 generation before F4', async () => {
  const workflow = await readFile('.github/workflows/analyze-session-automatic.yml', 'utf8');
  const f4 = 'node .github/scripts/generate-ai-post-processing-advisory-projection.mjs --write;';
  const f5 = 'node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --write;';
  const retryStart = workflow.indexOf('regenerate(){');
  const changed = `${workflow.slice(0, retryStart)}${workflow.slice(retryStart).replace(`${f4} ${f5}`, `${f5} ${f4}`)}`;
  assert.throws(() => verifyAtomicWorkflowIntegration(changed), /generated after its F4 projection/);
});
