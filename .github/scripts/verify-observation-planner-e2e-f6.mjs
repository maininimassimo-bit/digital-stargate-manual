import assert from 'node:assert/strict';
import fs from 'node:fs';
import { buildF6Projection, loadF6Inputs, F4C_EVIDENCE_DIGEST, F6_METHOD_ID, F6_METHOD_VERSION, F6_PROJECTION_TYPE } from './observation-planner-e2e-f6.mjs';

const projectionPath = 'docs/data/observation-planner-e2e-f6-projection.json';
const schemaPath = 'schemas/observation-planner-e2e-f6.schema.json';
const architecturePath = 'docs/architecture/scientific-assets/BKL-031-F6-Real-Evidence-Setup-Aware-E2E-Planner.md';
const acceptancePath = 'docs/project/BKL-031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E-ACCEPTANCE-2026-09-17.md';
const portalPath = 'docs/observation-planner/index.md';
const consumerPath = 'docs/javascripts/observation-planner-e2e-f6.js';
const workflowPath = '.github/workflows/bkl-031-f6-governance.yml';
const developerPath = '.github/workflows/developer-foundation.yml';
const roadmapPath = '.github/roadmap/roadmap-source.json';
const f5AcceptancePath = 'docs/project/BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md';

for (const path of [projectionPath, schemaPath, architecturePath, acceptancePath, portalPath, consumerPath, workflowPath, developerPath, roadmapPath, f5AcceptancePath]) {
  assert.equal(fs.existsSync(path), true, `required F6 artifact missing: ${path}`);
}

const inputs = loadF6Inputs();
const expected = buildF6Projection(inputs);
const committed = JSON.parse(fs.readFileSync(projectionPath, 'utf8'));
assert.deepEqual(committed, expected, 'committed F6 projection must be deterministically regenerated from accepted evidence');

assert.equal(committed.schemaVersion, '1.0');
assert.equal(committed.projectionType, F6_PROJECTION_TYPE);
assert.equal(committed.environment, 'EVALUATION');
assert.equal(committed.authority, 'NONE');
assert.equal(committed.consumerMode, 'READ_ONLY');
assert.equal(committed.method.id, F6_METHOD_ID);
assert.equal(committed.method.version, F6_METHOD_VERSION);
assert.equal(committed.method.rankingAuthority, 'NONE');
assert.equal(committed.forecastEvidence.evidenceDigest, F4C_EVIDENCE_DIGEST);
assert.equal(committed.forecastEvidence.evidenceClass, 'REAL_PROVIDER_BOUNDED_GENERALIZED');
assert.equal(committed.forecastEvidence.locationClass, 'SYNTHETIC_GENERALIZED');
assert.equal(committed.forecastEvidence.protectedSiteUsed, false);
assert.equal(committed.forecastEvidence.providerRequestBudget, '2/2_EXHAUSTED');
assert.equal(committed.forecastEvidence.acceptedHourlyInstantCount, 71);
assert.equal(committed.forecastEvidence.excludedHourlyInstantCount, 1);
assert.equal(committed.forecastEvidence.imputedValueCount, 0);
assert.equal(committed.weatherSample.validAtUtc, '2026-09-17T01:00:00Z');
assert.deepEqual(
  [committed.weatherSample.temperatureC, committed.weatherSample.relativeHumidityPct, committed.weatherSample.dewPointC, committed.weatherSample.precipitationMm, committed.weatherSample.cloudCoverPct, committed.weatherSample.windSpeedKmh, committed.weatherSample.windGustKmh],
  [21.4, 90, 19.6, 0, 64, 5.8, 10.1]
);
assert.equal(committed.setupScenarios.length, 2);
assert.deepEqual(committed.setupScenarios.map(item => item.setupPublicKey), ['WIDEFIELD_OSC', 'LONG_FOCAL_MONO']);
assert.equal(committed.setupScenarios[0].eligibleTargets[0].canonicalName, 'LDN 1320');
assert.equal(committed.setupScenarios[0].eligibleTargets[0].registeredSessionEvidenceCount, 3);
assert.equal(committed.setupScenarios[1].eligibleTargets[0].canonicalName, 'M 27');
assert.equal(committed.setupScenarios[1].eligibleTargets[0].registeredSessionEvidenceCount, 2);
assert.ok(committed.setupScenarios.every(item => item.compatibilityBasis === 'REGISTERED_SCIENTIFIC_SESSION_EVIDENCE'));
assert.ok(committed.setupScenarios.flatMap(item => item.eligibleTargets).every(item => item.f5ScoreClass === 'SYNTHETIC_METHOD_VALIDATION_ONLY'));

for (const limitation of [
  'F4C_LOCATION_SYNTHETIC_GENERALIZED_NOT_PROTECTED_SITE',
  'FORECAST_SAMPLE_IS_REAL_PROVIDER_EVIDENCE_BUT_NOT_CURRENT_RUNTIME_FEED',
  'F5_METHOD_SCORE_REMAINS_SYNTHETIC_GEOMETRY_METHOD_EVIDENCE',
  'SETUP_COMPATIBILITY_IS_HISTORICAL_ACQUISITION_EVIDENCE_NOT_OPTICAL_SUITABILITY_MODEL',
  'NO_ADDITIONAL_PROVIDER_TRAFFIC',
  'NO_READINESS_GO_NO_GO_SCHEDULING_AUTOMATIC_SELECTION_COMMAND_OR_SAFETY_AUTHORITY',
  'S10_PRODUCTION_RUNTIME_UNAVAILABLE'
]) assert.ok(committed.limitations.includes(limitation), `missing F6 limitation ${limitation}`);

assert.deepEqual(committed.boundary, {
  readinessAuthority: false,
  automaticTargetSelection: false,
  schedulingAuthority: false,
  actionAuthority: 'NONE',
  commandAuthority: 'NONE',
  safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS',
  runtimeState: 'UNAVAILABLE',
  providerRequestsPerformedByF6: 0
});

const publicText = fs.readFileSync(projectionPath, 'utf8');
for (const forbidden of ['QUATTRO200_TOUPTEK294_BIN1','C8_QHY695A_BIN1','DSG-CURRENT-SETUP-ASSIGNMENT-001','DSG-SETUP-BASELINE-001','governance/setup-authority/']) {
  assert.equal(publicText.includes(forbidden), false, `protected setup detail leaked into public F6 projection: ${forbidden}`);
}

const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
assert.equal(schema.properties.projectionType.const, F6_PROJECTION_TYPE);
assert.equal(schema.properties.environment.const, 'EVALUATION');
assert.equal(schema.properties.authority.const, 'NONE');
assert.equal(schema.properties.consumerMode.const, 'READ_ONLY');
assert.equal(schema.properties.forecastEvidence.properties.evidenceDigest.const, F4C_EVIDENCE_DIGEST);
assert.equal(schema.properties.boundary.properties.readinessAuthority.const, false);
assert.equal(schema.properties.boundary.properties.providerRequestsPerformedByF6.const, 0);

const f5Acceptance = fs.readFileSync(f5AcceptancePath, 'utf8');
assert.match(f5Acceptance, /ACCEPTED — POST-MERGE VERIFIED/);
assert.match(f5Acceptance, /F6 real-evidence setup-aware E2E planner integration/);
assert.match(f5Acceptance, /BKL-031 capability closure is deferred/);

const architecture = fs.readFileSync(architecturePath, 'utf8');
for (const required of [
  'ACCEPTED — POST-MERGE VERIFIED',
  'REAL_PROVIDER_BOUNDED_GENERALIZED',
  'REGISTERED_SCIENTIFIC_SESSION_EVIDENCE',
  '2/2_EXHAUSTED',
  'S10',
  'BKL-032',
  'F7 fresh forecast supply and runtime boundary',
  'ad7cad8267eaee1e27e7b1373d34f422efd8f088',
  'f75303c9575c77f23de777d55c6067bf08bc99f1',
  '14/14 applicable post-merge push workflows',
  'local physical interlocks'
]) assert.ok(architecture.includes(required), `architecture missing F6 acceptance/boundary marker: ${required}`);

const acceptance = fs.readFileSync(acceptancePath, 'utf8');
for (const required of [
  '**ACCEPTED — POST-MERGE VERIFIED**',
  '#275',
  'ad7cad8267eaee1e27e7b1373d34f422efd8f088',
  'f75303c9575c77f23de777d55c6067bf08bc99f1',
  '13/13 successful',
  '14/14 successful',
  '2/2_EXHAUSTED',
  'F7 fresh forecast supply and runtime boundary',
  'BKL-031 remains `In Progress`'
]) assert.ok(acceptance.includes(required), `F6 acceptance record missing: ${required}`);

const portal = fs.readFileSync(portalPath, 'utf8');
assert.ok(portal.includes('observation-planner-e2e-f6.js'));
assert.ok(portal.includes('data-observation-planner-f6'));
assert.ok(portal.includes('F6'));

const consumer = fs.readFileSync(consumerPath, 'utf8');
for (const required of [F6_PROJECTION_TYPE, F6_METHOD_ID, F4C_EVIDENCE_DIGEST, '2/2_EXHAUSTED', 'providerRequestsPerformedByF6']) assert.ok(consumer.includes(required));

const workflow = fs.readFileSync(workflowPath, 'utf8');
for (const forbidden of ['curl ', 'wget ', 'Invoke-WebRequest', 'single-runs-api.open-meteo.com', 'api.open-meteo.com']) {
  assert.equal(workflow.includes(forbidden), false, `F6 workflow must perform zero provider requests: ${forbidden}`);
}
assert.ok(workflow.includes('verify-observation-planner-e2e-f6.mjs'));
assert.ok(workflow.includes('test-observation-planner-e2e-f6.mjs'));

const developer = fs.readFileSync(developerPath, 'utf8');
for (const required of [
  'Verify Observation Planner F6 real-evidence E2E',
  'Test Observation Planner F6 fail-closed evidence bindings',
  'Check Observation Planner F6 browser consumer syntax'
]) assert.ok(developer.includes(required), `Developer Foundation does not preserve F6 regression coverage: ${required}`);

const roadmap = JSON.parse(fs.readFileSync(roadmapPath, 'utf8'));
assert.equal(roadmap.currentPackage, 'BKL-036');
assert.equal(roadmap.nextMilestone, 'BKL-036 Observatory Health Score');
assert.ok(roadmap.milestones.some(entry => entry.id === 'M-BKL031-F6-ACCEPTANCE'), 'roadmap F6 acceptance milestone missing');
const f6AcceptanceMilestone = roadmap.milestones.find(entry => entry.id === 'M-BKL031-F6-ACCEPTANCE');
assert.ok(f6AcceptanceMilestone.description.includes('PR #275'), 'F6 acceptance milestone must reference PR #275');
assert.ok(f6AcceptanceMilestone.description.includes('14/14'), 'F6 acceptance milestone must retain post-merge workflow evidence');
assert.ok(f6AcceptanceMilestone.description.includes('F7 fresh forecast supply and runtime boundary'), 'F6 acceptance milestone must promote F7');
assert.ok(f6AcceptanceMilestone.description.includes('BKL-031 remains In Progress'), 'F6 acceptance milestone must preserve deferred capability closure');
assert.ok(roadmap.projectStatus.includes('BKL-031 and BKL-032 are CLOSED / ACCEPTED / POST-MERGE VERIFIED'), 'roadmap must preserve the accepted BKL-031/BKL-032 closure state');
assert.ok(roadmap.projectStatus.includes('live source/transport and public runtime GO remain separately gated'), 'roadmap must preserve the live-source/runtime boundary');
assert.ok(roadmap.target.includes('No scheduler, automatic target selection, device command or Safety Authority is authorized'), 'roadmap target must preserve the authority boundary');

console.log('BKL-031 F6 verified: Accepted/Post-Merge Verified real-evidence setup-aware E2E proof; 13/13 exact-head, 14/14 post-merge, zero provider requests; F7/F8 accepted; F9 repeatable current-night planner closure next; BKL-031 closure deferred.');
