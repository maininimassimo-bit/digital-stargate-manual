import assert from 'node:assert/strict';
import fs from 'node:fs';

const script = fs.readFileSync('.github/scripts/observation-planner-forecast-f4c-acquire.mjs', 'utf8');
const workflow = fs.readFileSync('.github/workflows/bkl-031-f4-c-acquire-once.yml', 'utf8');
const gate = fs.readFileSync('docs/architecture/scientific-assets/BKL-031-F4-C-One-Request-Generalized-Forecast-Acquisition-Gate.md', 'utf8');
const failure = fs.readFileSync('docs/architecture/validation/BKL-031-F4-C-Failed-Acquisition-and-Remediation-Gate-2026-09-17.md', 'utf8');

assert.equal((script.match(/fetch\(/g) ?? []).length, 1, 'gate must contain exactly one fetch site');
for (const expected of [
  "latitude: '42.0'",
  "longitude: '12.0'",
  "https://single-runs-api.open-meteo.com/v1/forecast",
  "redirect: 'manual'",
  'maxRequestsThisAttempt: 1',
  'maxCumulativeProviderRequests: 2',
  'maxResponseBytes: 2000000',
  'F4C_ONE_REPLACEMENT_REQUEST',
  'priorFailedWorkflowRunId: 35201479378',
  "unavailableVariables: ['visibility']",
  'protectedSiteUsed: false'
]) assert.ok(script.includes(expected), `script missing ${expected}`);
assert.ok(!script.match(/^\s*'visibility',?$/m), 'visibility must not be requested');

for (const expected of [
  'workflow_dispatch:',
  'expected_main_sha:',
  'run_initialisation_utc:',
  'git ls-remote origin refs/heads/main',
  'F4C_ONE_REPLACEMENT_REQUEST',
  "id: acquire",
  "if: always() && steps.acquire.outcome != 'skipped'",
  'retention-days: 7'
]) assert.ok(workflow.includes(expected), `workflow missing ${expected}`);
assert.ok(!workflow.includes('schedule:'), 'workflow must not be scheduled');

for (const expected of [
  '**REMEDIATION REVIEW CANDIDATE — REPLACEMENT NOT EXECUTED**',
  'Exactly one HTTPS GET; cumulative F4-C ceiling two requests',
  'Synthetic/generalized `42.0, 12.0`',
  'one fetch site',
  'prohibits any third request',
  'Stop after the evidence artifact'
]) assert.ok(gate.includes(expected), `gate document missing ${expected}`);
for (const expected of [
  '**FAILED / REQUEST CONSUMED / REMEDIATION PREPARED**',
  '35201479378',
  '48bd61a3337523b7790d78a37813eaf5e1228724',
  'Provider HTTP 400',
  'No automatic or manual retry was made'
]) assert.ok(failure.includes(expected), `failure evidence missing ${expected}`);

const roadmap = JSON.parse(fs.readFileSync('.github/roadmap/roadmap-source.json', 'utf8'));
assert.equal(roadmap.nextMilestone, 'BKL-031 F4-C one-replacement-request remediation gate acceptance');
assert.ok(roadmap.milestones.some((entry) => entry.id === 'M-BKL031-F4-C-FIRST-ATTEMPT-FAILED'));
assert.ok(roadmap.milestones.some((entry) => entry.id === 'M-BKL031-F4-C-ACQUISITION-GATE'));
console.log('BKL-031 F4-C remediation verified: failed request consumed, Single Runs correction, one replacement request, cumulative ceiling two, no protected-site input, no schedule; replacement NOT EXECUTED.');
