import assert from 'node:assert/strict';
import fs from 'node:fs';

export const F6_PROJECTION_TYPE = 'BKL031_F6_REAL_EVIDENCE_SETUP_AWARE_E2E_PROJECTION';
export const F6_PROJECTION_ID = 'BKL031-F6-E2E-001';
export const F6_METHOD_ID = 'BKL031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E';
export const F6_METHOD_VERSION = '1.0';
export const F4C_EVIDENCE_DIGEST = '350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5';

const INTERNAL_SETUP_MAP = Object.freeze([
  Object.freeze({
    publicKey: 'WIDEFIELD_OSC',
    publicLabel: 'Wide-field OSC',
    internalConfigurationId: 'QUATTRO200_TOUPTEK294_BIN1',
    expectedSupportedTargetKey: 'dsg-target:ldn-1320',
    expectedRegisteredSessions: 3
  }),
  Object.freeze({
    publicKey: 'LONG_FOCAL_MONO',
    publicLabel: 'Long-focal mono',
    internalConfigurationId: 'C8_QHY695A_BIN1',
    expectedSupportedTargetKey: 'dsg-target:m-27',
    expectedRegisteredSessions: 2
  })
]);

const PATHS = Object.freeze({
  forecast: 'governance/forecast-evidence/BKL031-F4C-RUN-35214129960/normalized-evidence.json',
  assignment: 'governance/setup-authority/setup-assignments/DSG-CURRENT-SETUP-ASSIGNMENT-001.approved.json',
  baseline: 'governance/setup-authority/configuration-baselines/DSG-SETUP-BASELINE-001.approved.json',
  targetKnowledge: 'docs/data/target-knowledge-read-model.json',
  scientificMetadata: 'data/analytics/metadata/session-scientific-metadata.csv',
  f5Projection: 'docs/data/observation-planner-ranking-f5-projection.json',
  output: 'docs/data/observation-planner-e2e-f6-projection.json'
});

function parseCsv(text) {
  const rows = [];
  for (const line of text.trim().split(/\r?\n/)) {
    const values = [];
    let current = '';
    let quoted = false;
    for (let i = 0; i < line.length; i += 1) {
      const ch = line[i];
      if (ch === '"') {
        if (quoted && line[i + 1] === '"') {
          current += '"';
          i += 1;
        } else quoted = !quoted;
      } else if (ch === ',' && !quoted) {
        values.push(current);
        current = '';
      } else current += ch;
    }
    values.push(current);
    rows.push(values);
  }
  const [header, ...data] = rows;
  return data.map(row => Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])));
}

function assertIsoWithinHalfOpen(instant, from, to) {
  const value = Date.parse(instant);
  assert.ok(Number.isFinite(value), 'invalid evaluation instant');
  assert.ok(value >= Date.parse(from), 'evaluation instant before setup validity');
  if (to !== null) assert.ok(value < Date.parse(to), 'evaluation instant outside setup validity');
}

function targetByKey(model, targetKey) {
  const target = model.targets.find(item => item.target_key === targetKey);
  assert.ok(target, `missing target ${targetKey}`);
  assert.equal(target.identity_state, 'validated', `${targetKey} identity must be validated`);
  assert.equal(target.target_id_state, 'validated', `${targetKey} target id must be validated`);
  return target;
}

function f5ByTarget(projection, targetKey) {
  const item = projection.results.find(result => result.targetKey === targetKey);
  assert.ok(item, `missing F5 result ${targetKey}`);
  return item;
}

export function loadF6Inputs() {
  return {
    forecast: JSON.parse(fs.readFileSync(PATHS.forecast, 'utf8')),
    assignment: JSON.parse(fs.readFileSync(PATHS.assignment, 'utf8')),
    baseline: JSON.parse(fs.readFileSync(PATHS.baseline, 'utf8')),
    targetKnowledge: JSON.parse(fs.readFileSync(PATHS.targetKnowledge, 'utf8')),
    scientificMetadataCsv: fs.readFileSync(PATHS.scientificMetadata, 'utf8'),
    f5Projection: JSON.parse(fs.readFileSync(PATHS.f5Projection, 'utf8'))
  };
}

export function buildF6Projection(inputs) {
  const { forecast, assignment, baseline, targetKnowledge, scientificMetadataCsv, f5Projection } = inputs;

  assert.equal(forecast.evidenceType, 'BKL031_F4C_RECONCILED_BOUNDED_FORECAST_EVIDENCE');
  assert.equal(forecast.evidenceDigest, F4C_EVIDENCE_DIGEST);
  assert.equal(forecast.environment, 'EVALUATION');
  assert.equal(forecast.authority, 'NONE');
  assert.equal(forecast.location.classification, 'SYNTHETIC_GENERALIZED');
  assert.equal(forecast.location.protectedSiteUsed, false);
  assert.equal(forecast.requestAccounting.cumulativeProviderRequestCount, 2);
  assert.equal(forecast.requestAccounting.furtherRequestsAuthorized, false);
  assert.equal(forecast.normalization.acceptedHourlyInstantCount, 71);
  assert.equal(forecast.normalization.excludedHourlyInstantCount, 1);
  assert.equal(forecast.normalization.imputedValueCount, 0);
  assert.ok(Array.isArray(forecast.forecastInstantsUtc) && forecast.forecastInstantsUtc.length === 71);

  const sampleIndex = 0;
  const sampleInstant = forecast.forecastInstantsUtc[sampleIndex];
  const expectedSeries = [
    'temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'precipitation',
    'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high',
    'wind_speed_10m', 'wind_gusts_10m'
  ];
  for (const key of expectedSeries) {
    assert.ok(Array.isArray(forecast.series[key]) && forecast.series[key].length === 71, `${key} series invalid`);
    assert.ok(Number.isFinite(forecast.series[key][sampleIndex]), `${key} sample invalid`);
  }

  assert.equal(assignment.recordType, 'DSG_CURRENT_SETUP_ASSIGNMENT');
  assert.equal(assignment.lifecycle.state, 'APPROVED');
  assert.equal(assignment.lifecycle.eligibleForResolution, true);
  assert.equal(assignment.assignmentPayload.scope, 'OBSERVATION_PLANNER_READ_ONLY_SETUP_AUTHORITY');
  assertIsoWithinHalfOpen(sampleInstant, assignment.assignmentPayload.validity.validFromUtc, assignment.assignmentPayload.validity.validToUtc);
  assert.equal(baseline.recordType, 'DSG_CONFIGURATION_BASELINE');
  assert.equal(baseline.lifecycle.state, 'APPROVED');
  assert.equal(baseline.lifecycle.eligibleForResolution, true);
  assert.equal(assignment.assignmentPayload.setupBaselineReference.baselineId, baseline.baselinePayload.baselineId);
  assert.equal(assignment.assignmentPayload.setupBaselineReference.payloadDigest, baseline.payloadDigest.value);

  for (const setup of INTERNAL_SETUP_MAP) {
    assert.ok(baseline.baselinePayload.configurationProfiles.some(profile => profile.configurationId === setup.internalConfigurationId), `missing governed setup profile ${setup.publicKey}`);
  }

  assert.equal(f5Projection.projectionType, 'BKL031_F5_EXPLAINABLE_RANKING_PROJECTION');
  assert.equal(f5Projection.environment, 'EVALUATION');
  assert.equal(f5Projection.authority, 'NONE');
  assert.equal(f5Projection.consumerMode, 'READ_ONLY');
  assert.ok(f5Projection.limitations.includes('SYNTHETIC_FACTOR_VALUES_FOR_METHOD_VALIDATION_ONLY'));
  assert.equal(f5Projection.lineage.forecastEvidenceDigest, F4C_EVIDENCE_DIGEST);
  assert.equal(f5Projection.lineage.providerRequestBudget, '2/2_EXHAUSTED');

  const rows = parseCsv(scientificMetadataCsv);
  const targetKeys = targetKnowledge.targets.map(target => target.target_key);
  assert.deepEqual([...targetKeys].sort(), ['dsg-target:ldn-1320', 'dsg-target:m-27']);

  const setupScenarios = INTERNAL_SETUP_MAP.map(setup => {
    const supportedTarget = targetByKey(targetKnowledge, setup.expectedSupportedTargetKey);
    const historicalRows = rows.filter(row => row.metadata_state === 'REGISTERED' && row.configuration_id === setup.internalConfigurationId && row.target_id === supportedTarget.target_id);
    assert.equal(historicalRows.length, setup.expectedRegisteredSessions, `${setup.publicKey} historical evidence count changed`);
    const f5 = f5ByTarget(f5Projection, supportedTarget.target_key);
    const excludedTargets = targetKnowledge.targets
      .filter(target => target.target_key !== supportedTarget.target_key)
      .map(target => ({
        targetKey: target.target_key,
        targetId: target.target_id,
        canonicalName: target.canonical_name,
        setupCompatibilityState: 'UNVERIFIED_FOR_SELECTED_SETUP',
        reasonCode: 'NO_REGISTERED_ACQUISITION_EVIDENCE_FOR_SELECTED_SETUP'
      }));
    return {
      setupPublicKey: setup.publicKey,
      setupLabel: setup.publicLabel,
      compatibilityBasis: 'REGISTERED_SCIENTIFIC_SESSION_EVIDENCE',
      eligibleTargets: [{
        targetKey: supportedTarget.target_key,
        targetId: supportedTarget.target_id,
        canonicalName: supportedTarget.canonical_name,
        setupCompatibilityState: 'SUPPORTED_BY_HISTORY',
        registeredSessionEvidenceCount: historicalRows.length,
        f5MethodValidationRank: f5.rank,
        f5MethodValidationScore: f5.score,
        f5ScoreClass: 'SYNTHETIC_METHOD_VALIDATION_ONLY'
      }],
      excludedTargets
    };
  });

  const projection = {
    schemaVersion: '1.0',
    projectionType: F6_PROJECTION_TYPE,
    projectionId: F6_PROJECTION_ID,
    environment: 'EVALUATION',
    authority: 'NONE',
    consumerMode: 'READ_ONLY',
    method: {
      id: F6_METHOD_ID,
      version: F6_METHOD_VERSION,
      behavior: 'BIND_REAL_F4C_FORECAST_SAMPLE_TO_GOVERNED_SETUP_COMPATIBILITY_AND_F5_METHOD_EVIDENCE',
      rankingAuthority: 'NONE'
    },
    forecastEvidence: {
      evidenceClass: 'REAL_PROVIDER_BOUNDED_GENERALIZED',
      evidenceId: forecast.evidenceId,
      evidenceDigest: forecast.evidenceDigest,
      providerId: forecast.source.providerId,
      upstreamAuthorityId: forecast.source.upstreamAuthorityId,
      modelId: forecast.source.modelId,
      runInitialisationUtc: forecast.source.runInitialisationUtc,
      validFromUtc: forecast.validFromUtc,
      validToUtcExclusive: forecast.validToUtcExclusive,
      acceptedHourlyInstantCount: forecast.normalization.acceptedHourlyInstantCount,
      excludedHourlyInstantCount: forecast.normalization.excludedHourlyInstantCount,
      imputedValueCount: forecast.normalization.imputedValueCount,
      providerRequestBudget: '2/2_EXHAUSTED',
      locationClass: forecast.location.classification,
      protectedSiteUsed: false
    },
    weatherSample: {
      validAtUtc: sampleInstant,
      temperatureC: forecast.series.temperature_2m[sampleIndex],
      relativeHumidityPct: forecast.series.relative_humidity_2m[sampleIndex],
      dewPointC: forecast.series.dew_point_2m[sampleIndex],
      precipitationMm: forecast.series.precipitation[sampleIndex],
      cloudCoverPct: forecast.series.cloud_cover[sampleIndex],
      cloudCoverLowPct: forecast.series.cloud_cover_low[sampleIndex],
      cloudCoverMidPct: forecast.series.cloud_cover_mid[sampleIndex],
      cloudCoverHighPct: forecast.series.cloud_cover_high[sampleIndex],
      windSpeedKmh: forecast.series.wind_speed_10m[sampleIndex],
      windGustKmh: forecast.series.wind_gusts_10m[sampleIndex],
      semantics: 'REAL_F4C_VALUE_SAMPLE_FOR_E2E_DATA_PATH_PROOF_NOT_READINESS'
    },
    setupScenarios,
    lineage: {
      targetKnowledgeRef: PATHS.targetKnowledge,
      scientificMetadataRef: PATHS.scientificMetadata,
      astronomicalEvidenceRef: 'docs/data/observation-planner-ephemeris-lunar-f3c-projection.json',
      f5MethodProjectionRef: PATHS.f5Projection,
      f4cEvidenceRef: PATHS.forecast,
      setupAuthorityClass: 'PROTECTED_GOVERNED_INPUT_SANITIZED_BEFORE_PUBLICATION'
    },
    limitations: [
      'F4C_LOCATION_SYNTHETIC_GENERALIZED_NOT_PROTECTED_SITE',
      'FORECAST_SAMPLE_IS_REAL_PROVIDER_EVIDENCE_BUT_NOT_CURRENT_RUNTIME_FEED',
      'F5_METHOD_SCORE_REMAINS_SYNTHETIC_GEOMETRY_METHOD_EVIDENCE',
      'SETUP_COMPATIBILITY_IS_HISTORICAL_ACQUISITION_EVIDENCE_NOT_OPTICAL_SUITABILITY_MODEL',
      'NO_ADDITIONAL_PROVIDER_TRAFFIC',
      'NO_READINESS_GO_NO_GO_SCHEDULING_AUTOMATIC_SELECTION_COMMAND_OR_SAFETY_AUTHORITY',
      'S10_PRODUCTION_RUNTIME_UNAVAILABLE'
    ],
    boundary: {
      readinessAuthority: false,
      automaticTargetSelection: false,
      schedulingAuthority: false,
      actionAuthority: 'NONE',
      commandAuthority: 'NONE',
      safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS',
      runtimeState: 'UNAVAILABLE',
      providerRequestsPerformedByF6: 0
    }
  };

  const publicText = JSON.stringify(projection);
  for (const forbidden of [
    'QUATTRO200_TOUPTEK294_BIN1', 'C8_QHY695A_BIN1', 'DSG-CURRENT-SETUP-ASSIGNMENT-001',
    'DSG-SETUP-BASELINE-001', 'e7632afb4f0b2dc725b888eb858f650e2669d1ebf78e098c25b950cf36eae4ef',
    '3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8'
  ]) assert.equal(publicText.includes(forbidden), false, `protected setup detail leaked: ${forbidden}`);

  return projection;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const projection = buildF6Projection(loadF6Inputs());
  if (process.argv.includes('--write')) {
    fs.writeFileSync(PATHS.output, `${JSON.stringify(projection, null, 2)}\n`);
    console.log(`Wrote ${PATHS.output}.`);
  } else {
    const committed = JSON.parse(fs.readFileSync(PATHS.output, 'utf8'));
    assert.deepEqual(committed, projection);
    console.log('BKL-031 F6 E2E projection verified against real F4-C values, governed setup evidence and F5 method evidence.');
  }
}
