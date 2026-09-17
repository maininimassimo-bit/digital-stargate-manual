import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';

const DIR = 'governance/forecast-evidence/BKL031-F4C-RUN-35214129960';
const RAW_PATH = `${DIR}/raw-response.json`;
const PLAN_PATH = `${DIR}/request-plan.json`;
const FAILURE_PATH = `${DIR}/failure-summary.json`;
const OUTPUT_PATH = `${DIR}/normalized-evidence.json`;
const RAW_SHA256 = 'e51c6935f8e04bcce38983bc03147f4f897a833f90feb6271b2f510ee6eec102';
const VARS = [
  'temperature_2m',
  'relative_humidity_2m',
  'dew_point_2m',
  'precipitation',
  'cloud_cover',
  'cloud_cover_low',
  'cloud_cover_mid',
  'cloud_cover_high',
  'wind_speed_10m',
  'wind_gusts_10m'
];
const UNITS = {
  temperature_2m: 'degC',
  relative_humidity_2m: 'percent',
  dew_point_2m: 'degC',
  precipitation: 'mm',
  cloud_cover: 'percent',
  cloud_cover_low: 'percent',
  cloud_cover_mid: 'percent',
  cloud_cover_high: 'percent',
  wind_speed_10m: 'km/h',
  wind_gusts_10m: 'km/h'
};

function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}
function digest(value) {
  return crypto.createHash('sha256').update(canonicalJson(value)).digest('hex');
}
function isoUtc(rawTime) {
  assert.match(rawTime, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/);
  return `${rawTime}:00Z`;
}

const rawBytes = fs.readFileSync(RAW_PATH);
assert.equal(rawBytes.length, 4723);
assert.equal(crypto.createHash('sha256').update(rawBytes).digest('hex'), RAW_SHA256);
const raw = JSON.parse(rawBytes);
const plan = JSON.parse(fs.readFileSync(PLAN_PATH, 'utf8'));
const failure = JSON.parse(fs.readFileSync(FAILURE_PATH, 'utf8'));

assert.equal(plan.gateId, 'BKL031-F4C-ONE-REPLACEMENT-GENERALIZED-REQUEST-002');
assert.equal(plan.priorFailedWorkflowRunId, 35201479378);
assert.equal(plan.attemptOrdinal, 2);
assert.equal(plan.expectedHost, 'single-runs-api.open-meteo.com');
assert.equal(plan.runInitialisationUtc, '2026-09-17T00:00Z');
assert.deepEqual(plan.variables, VARS);
assert.deepEqual(plan.unavailableVariables, ['visibility']);
assert.equal(plan.protectedSiteUsed, false);
assert.equal(failure.failureClass, 'NON_FINITE_VARIABLE');
assert.equal(failure.variable, 'precipitation');
assert.equal(failure.httpStatus, 200);
assert.equal(failure.rawSha256, RAW_SHA256);
assert.equal(failure.byteLength, rawBytes.length);
assert.equal(failure.cumulativeProviderRequestCount, 2);

assert.equal(raw.timezone, 'GMT');
assert.equal(raw.utc_offset_seconds, 0);
assert.equal(raw.latitude, 42);
assert.equal(raw.longitude, 12);
assert.equal(raw.hourly.time.length, 72);
for (const variable of VARS) assert.equal(raw.hourly[variable].length, 72, `${variable} length mismatch`);

const excludedInstants = [];
const acceptedIndices = [];
for (let index = 0; index < raw.hourly.time.length; index += 1) {
  const missingVariables = VARS.filter((variable) => !Number.isFinite(raw.hourly[variable][index]));
  if (missingVariables.length) {
    excludedInstants.push({
      sourceIndex: index,
      validAtUtc: isoUtc(raw.hourly.time[index]),
      missingVariables,
      reasonCode: 'INCOMPLETE_REQUIRED_VARIABLE'
    });
  } else {
    acceptedIndices.push(index);
  }
}
assert.deepEqual(excludedInstants, [{
  sourceIndex: 0,
  validAtUtc: '2026-09-17T00:00:00Z',
  missingVariables: ['precipitation'],
  reasonCode: 'INCOMPLETE_REQUIRED_VARIABLE'
}]);
assert.deepEqual(acceptedIndices, Array.from({ length: 71 }, (_, index) => index + 1));

const series = Object.fromEntries(VARS.map((variable) => [variable, acceptedIndices.map((index) => raw.hourly[variable][index])]));
const evidence = {
  schemaVersion: '1.0',
  evidenceType: 'BKL031_F4C_RECONCILED_BOUNDED_FORECAST_EVIDENCE',
  evidenceId: 'BKL031-F4C-EVIDENCE-35214129960',
  environment: 'EVALUATION',
  authority: 'NONE',
  workflowRunId: 35214129960,
  authorizedMainSha: '053fc766bfc7908a984828cc335eef07a558909c',
  artifactId: 10494298154,
  artifactName: 'bkl-031-f4c-evidence-35214129960',
  requestAccounting: {
    priorFailedWorkflowRunId: 35201479378,
    attemptOrdinal: 2,
    requestCountThisAttempt: 1,
    cumulativeProviderRequestCount: 2,
    furtherRequestsAuthorized: false
  },
  source: {
    providerId: 'OPEN_METEO',
    upstreamAuthorityId: 'ITALIAMETEO_ARPAE',
    modelId: 'italia_meteo_arpae_icon_2i',
    deliveryInterface: 'OPEN_METEO_SINGLE_RUNS',
    runInitialisationUtc: '2026-09-17T00:00:00Z',
    rawResponseSha256: RAW_SHA256,
    rawResponseByteLength: rawBytes.length
  },
  location: {
    classification: 'SYNTHETIC_GENERALIZED',
    latitudeDeg: raw.latitude,
    longitudeDeg: raw.longitude,
    elevationM: raw.elevation,
    protectedSiteUsed: false
  },
  response: {
    httpStatus: 200,
    timezone: raw.timezone,
    utcOffsetSeconds: raw.utc_offset_seconds,
    generationTimeMs: raw.generationtime_ms
  },
  normalization: {
    policy: 'DROP_INCOMPLETE_INSTANT_NO_IMPUTATION',
    rawHourlyInstantCount: raw.hourly.time.length,
    acceptedHourlyInstantCount: acceptedIndices.length,
    excludedHourlyInstantCount: excludedInstants.length,
    excludedInstants,
    imputedValueCount: 0
  },
  validFromUtc: isoUtc(raw.hourly.time[acceptedIndices[0]]),
  validToUtcExclusive: '2026-09-20T00:00:00Z',
  forecastInstantsUtc: acceptedIndices.map((index) => isoUtc(raw.hourly.time[index])),
  series,
  units: UNITS,
  unavailableVariables: ['visibility'],
  citation: {
    provider: 'https://open-meteo.com/en/docs/single-runs-api',
    model: 'https://open-meteo.com/en/docs/italia-meteo-arpae-api',
    upstream: 'https://www.arpae.it/it/temi-ambientali/meteo/previsioni-meteo/previsioni-meteo-modellistiche'
  },
  attribution: 'Weather data by Open-Meteo; model data by ItaliaMeteo/ARPAE ICON-2I.',
  boundaries: {
    recurringTraffic: false,
    runtimeActivated: false,
    publicProjection: false,
    rankingImplemented: false,
    readinessImplemented: false,
    commandAuthority: 'NONE',
    safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS'
  }
};
evidence.evidenceDigest = digest(evidence);

for (const variable of VARS) {
  assert.equal(evidence.series[variable].length, 71);
  assert.ok(evidence.series[variable].every(Number.isFinite), `${variable} contains non-finite values`);
}
assert.ok(evidence.series.relative_humidity_2m.every((value) => value >= 0 && value <= 100));
for (const variable of ['cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high']) {
  assert.ok(evidence.series[variable].every((value) => value >= 0 && value <= 100));
}
for (const variable of ['precipitation', 'wind_speed_10m', 'wind_gusts_10m']) {
  assert.ok(evidence.series[variable].every((value) => value >= 0));
}

if (process.argv.includes('--write')) {
  fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(evidence, null, 2)}\n`);
  console.log(`Wrote ${OUTPUT_PATH}; digest ${evidence.evidenceDigest}.`);
} else {
  const committed = JSON.parse(fs.readFileSync(OUTPUT_PATH, 'utf8'));
  assert.deepEqual(committed, evidence);
  const claimed = committed.evidenceDigest;
  const unsigned = structuredClone(committed);
  delete unsigned.evidenceDigest;
  assert.equal(claimed, digest(unsigned));
  console.log(`BKL-031 F4-C evidence reconciled: raw ${RAW_SHA256}, 71 complete hourly instants, 1 excluded, 0 imputed, cumulative requests 2, evidence ${claimed}.`);
}
