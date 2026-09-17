import assert from 'node:assert/strict';
import fs from 'node:fs';

const gate = fs.readFileSync('docs/architecture/scientific-assets/BKL-031-F4-C-One-Request-Generalized-Forecast-Acquisition-Gate.md', 'utf8');
const firstFailure = fs.readFileSync('docs/architecture/validation/BKL-031-F4-C-Failed-Acquisition-and-Remediation-Gate-2026-09-17.md', 'utf8');
const reconciliation = fs.readFileSync('docs/architecture/validation/BKL-031-F4-C-Acquisition-Evidence-Reconciliation-2026-09-17.md', 'utf8');
const normalized = JSON.parse(fs.readFileSync('governance/forecast-evidence/BKL031-F4C-RUN-35214129960/normalized-evidence.json', 'utf8'));

assert.equal(fs.existsSync('.github/workflows/bkl-031-f4-c-acquire-once.yml'), false, 'exhausted acquisition workflow must be removed');
assert.equal(fs.existsSync('.github/scripts/observation-planner-forecast-f4c-acquire.mjs'), false, 'exhausted acquisition script must be removed');

for (const expected of [
  '**ACCEPTED — POST-MERGE VERIFIED / REQUEST BUDGET EXHAUSTED**',
  '35201479378',
  '35214129960',
  '053fc766bfc7908a984828cc335eef07a558909c',
  '10494298154',
  'e51c6935f8e04bcce38983bc03147f4f897a833f90feb6271b2f510ee6eec102',
  '350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5',
  '71-instant normalized evidence',
  'no third-request dispatch path',
  '79fe51e71782fff6c952e9291fe8ca567da74e98',
  '15/15 applicable workflows successful',
  'all 15 applicable post-merge workflows completed successfully',
  'F4-D'
]) assert.ok(gate.includes(expected), `gate record missing ${expected}`);
for (const expected of [
  '**FIRST REQUEST FAILED / REMEDIATION EXECUTED / HISTORICAL EVIDENCE**',
  'Provider HTTP 400',
  'No automatic or manual retry was made',
  'no third request is permitted'
]) assert.ok(firstFailure.includes(expected), `first failure record missing ${expected}`);
for (const expected of [
  '**ACCEPTED — POST-MERGE VERIFIED / NO FURTHER REQUEST**',
  'HTTP 200; 4,723 bytes',
  'DROP_INCOMPLETE_INSTANT_NO_IMPUTATION',
  'accepted exactly indices 1–71',
  'imputed zero values',
  'No further provider request is authorized',
  '79fe51e71782fff6c952e9291fe8ca567da74e98',
  '15/15 applicable workflows successful'
]) assert.ok(reconciliation.includes(expected), `reconciliation record missing ${expected}`);

assert.equal(normalized.workflowRunId, 35214129960);
assert.equal(normalized.artifactId, 10494298154);
assert.equal(normalized.source.rawResponseSha256, 'e51c6935f8e04bcce38983bc03147f4f897a833f90feb6271b2f510ee6eec102');
assert.equal(normalized.normalization.rawHourlyInstantCount, 72);
assert.equal(normalized.normalization.acceptedHourlyInstantCount, 71);
assert.equal(normalized.normalization.excludedHourlyInstantCount, 1);
assert.equal(normalized.normalization.imputedValueCount, 0);
assert.equal(normalized.requestAccounting.cumulativeProviderRequestCount, 2);
assert.equal(normalized.requestAccounting.furtherRequestsAuthorized, false);
assert.equal(normalized.boundaries.publicProjection, false);
assert.equal(normalized.location.protectedSiteUsed, false);

const roadmap = JSON.parse(fs.readFileSync('.github/roadmap/roadmap-source.json', 'utf8'));
assert.equal(roadmap.nextMilestone, 'BKL-031 F8 current astronomy and explicit setup suitability integration');
assert.ok(roadmap.milestones.some((entry) => entry.id === 'M-BKL031-F4-C-FIRST-ATTEMPT-FAILED'));
assert.ok(roadmap.milestones.some((entry) => entry.id === 'M-BKL031-F4-C-EVIDENCE-RECONCILIATION'));
assert.ok(roadmap.milestones.some((entry) => entry.id === 'M-BKL031-F4-D-ACCEPTANCE'));
console.log('BKL-031 F4-C gate verified: accepted/post-merge verified, two requests consumed, HTTP 200 raw evidence reconciled to 71 complete instants with zero imputation, acquisition path removed, no protected-site use; F5 is accepted; F6 real-evidence setup-aware E2E planner integration is next.');
