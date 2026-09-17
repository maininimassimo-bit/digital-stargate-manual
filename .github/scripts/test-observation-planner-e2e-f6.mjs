import assert from 'node:assert/strict';
import test from 'node:test';
import { buildF6Projection, loadF6Inputs, F4C_EVIDENCE_DIGEST } from './observation-planner-e2e-f6.mjs';

function fresh() {
  const loaded = loadF6Inputs();
  return {
    forecast: structuredClone(loaded.forecast),
    assignment: structuredClone(loaded.assignment),
    baseline: structuredClone(loaded.baseline),
    targetKnowledge: structuredClone(loaded.targetKnowledge),
    scientificMetadataCsv: loaded.scientificMetadataCsv,
    f5Projection: structuredClone(loaded.f5Projection)
  };
}

test('F6 positive path binds real F4-C values, setup evidence and F5 method evidence', () => {
  const projection = buildF6Projection(fresh());
  assert.equal(projection.forecastEvidence.evidenceDigest, F4C_EVIDENCE_DIGEST);
  assert.equal(projection.weatherSample.cloudCoverPct, 64);
  assert.equal(projection.setupScenarios[0].eligibleTargets[0].canonicalName, 'LDN 1320');
  assert.equal(projection.setupScenarios[0].eligibleTargets[0].registeredSessionEvidenceCount, 3);
  assert.equal(projection.setupScenarios[1].eligibleTargets[0].canonicalName, 'M 27');
  assert.equal(projection.setupScenarios[1].eligibleTargets[0].registeredSessionEvidenceCount, 2);
  assert.equal(projection.boundary.providerRequestsPerformedByF6, 0);
});

test('F6 actually consumes the real forecast value sample', () => {
  const original = buildF6Projection(fresh());
  const mutated = fresh();
  mutated.forecast.series.cloud_cover[0] = 63;
  const changed = buildF6Projection(mutated);
  assert.equal(original.weatherSample.cloudCoverPct, 64);
  assert.equal(changed.weatherSample.cloudCoverPct, 63);
  assert.notDeepEqual(changed.weatherSample, original.weatherSample);
});

test('F6 fails closed if a third provider request is authorized', () => {
  const inputs = fresh();
  inputs.forecast.requestAccounting.furtherRequestsAuthorized = true;
  assert.throws(() => buildF6Projection(inputs));
});

test('F6 fails closed if protected-site forecast evidence is substituted', () => {
  const inputs = fresh();
  inputs.forecast.location.protectedSiteUsed = true;
  inputs.forecast.location.classification = 'PROTECTED_SITE';
  assert.throws(() => buildF6Projection(inputs));
});

test('F6 fails closed if current setup assignment is no longer approved', () => {
  const inputs = fresh();
  inputs.assignment.lifecycle.state = 'RETIRED';
  inputs.assignment.lifecycle.eligibleForResolution = false;
  assert.throws(() => buildF6Projection(inputs));
});

test('F6 fails closed if the setup assignment is outside the evidence instant', () => {
  const inputs = fresh();
  inputs.assignment.assignmentPayload.validity.validToUtc = '2026-09-17T01:00:00Z';
  assert.throws(() => buildF6Projection(inputs));
});

test('F6 fails closed when governed target identity is not validated', () => {
  const inputs = fresh();
  inputs.targetKnowledge.targets[0].identity_state = 'conflicted';
  assert.throws(() => buildF6Projection(inputs));
});

test('F6 setup compatibility changes when historical registered evidence changes', () => {
  const inputs = fresh();
  inputs.scientificMetadataCsv = inputs.scientificMetadataCsv.replace('2026-07-16_2026-07-17,LDN 1320,TGT-LDN-1320,63.8000,85.6331,QUATTRO200_TOUPTEK294_BIN1', '2026-07-16_2026-07-17,LDN 1320,TGT-LDN-1320,63.8000,85.6331,C8_QHY695A_BIN1');
  assert.throws(() => buildF6Projection(inputs), /historical evidence count changed/);
});

test('F6 public projection contains no protected setup identifiers or digests', () => {
  const text = JSON.stringify(buildF6Projection(fresh()));
  for (const forbidden of ['QUATTRO200_TOUPTEK294_BIN1','C8_QHY695A_BIN1','DSG-CURRENT-SETUP-ASSIGNMENT-001','DSG-SETUP-BASELINE-001','e7632afb4f0b2dc725b888eb858f650e2669d1ebf78e098c25b950cf36eae4ef','3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8']) {
    assert.equal(text.includes(forbidden), false);
  }
});

test('F6 preserves non-operational authority boundaries', () => {
  const projection = buildF6Projection(fresh());
  assert.deepEqual(projection.boundary, {
    readinessAuthority: false,
    automaticTargetSelection: false,
    schedulingAuthority: false,
    actionAuthority: 'NONE',
    commandAuthority: 'NONE',
    safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS',
    runtimeState: 'UNAVAILABLE',
    providerRequestsPerformedByF6: 0
  });
});
