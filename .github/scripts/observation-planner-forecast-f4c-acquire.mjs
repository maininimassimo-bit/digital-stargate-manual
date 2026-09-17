import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

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
const args = Object.fromEntries(process.argv.slice(2).map((entry) => {
  const [key, ...value] = entry.replace(/^--/, '').split('=');
  return [key, value.join('=') || true];
}));
const run = String(args.run ?? '');
if (!/^\d{4}-\d{2}-\d{2}T(?:00|12):00Z$/.test(run)) {
  throw new Error('run must be an explicit 00/12 UTC initialization.');
}
const runMs = Date.parse(run);
const now = Date.now();
if (runMs > now || now - runMs > 18 * 3_600_000) {
  throw new Error('run must be available and no older than 18 hours.');
}

const url = new URL('https://single-runs-api.open-meteo.com/v1/forecast');
for (const [key, value] of Object.entries({
  latitude: '42.0',
  longitude: '12.0',
  hourly: VARS.join(','),
  models: 'italia_meteo_arpae_icon_2i',
  run: run.slice(0, -1),
  timezone: 'GMT',
  timeformat: 'iso8601',
  cell_selection: 'land',
  elevation: 'nan',
  forecast_hours: '72'
})) {
  url.searchParams.set(key, value);
}

const plan = {
  gateId: 'BKL031-F4C-ONE-REPLACEMENT-GENERALIZED-REQUEST-002',
  priorFailedWorkflowRunId: 35201479378,
  attemptOrdinal: 2,
  expectedHost: 'single-runs-api.open-meteo.com',
  method: 'GET',
  redirects: 'DENY',
  maxRequestsThisAttempt: 1,
  maxCumulativeProviderRequests: 2,
  timeoutMs: 10000,
  maxResponseBytes: 2000000,
  location: {
    classification: 'SYNTHETIC_GENERALIZED',
    latitudeDeg: 42,
    longitudeDeg: 12,
    siteAuthorityRef: 'SITE-PUBLIC-SYNTHETIC-FORECAST-IT-01'
  },
  modelId: 'italia_meteo_arpae_icon_2i',
  runInitialisationUtc: run,
  variables: VARS,
  unavailableVariables: ['visibility'],
  protectedSiteUsed: false,
  productionUse: false
};

if (url.hostname !== plan.expectedHost) throw new Error('request host mismatch.');
if (args.preflight) {
  console.log(JSON.stringify(plan, null, 2));
  process.exit(0);
}
if (!args.execute || args.confirm !== 'F4C_ONE_REPLACEMENT_REQUEST') {
  throw new Error('execution requires --execute and exact replacement confirmation.');
}

const out = path.resolve(String(args.out ?? 'work/f4c-evidence'));
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'request-plan.json'), `${JSON.stringify(plan, null, 2)}\n`);
const failure = (details) => fs.writeFileSync(
  path.join(out, 'failure-summary.json'),
  `${JSON.stringify({ gateId: plan.gateId, requestCountThisAttempt: 1, cumulativeProviderRequestCount: 2, ...details }, null, 2)}\n`
);

const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), plan.timeoutMs);
let response;
try {
  response = await fetch(url, {
    method: 'GET',
    redirect: 'manual',
    headers: { accept: 'application/json', 'user-agent': 'digital-stargate-bkl031-f4c-remediation/1.0' },
    signal: controller.signal
  });
} catch (error) {
  clearTimeout(timer);
  failure({ failureClass: 'TRANSPORT', errorName: error?.name ?? 'Error', errorMessage: error?.message ?? 'unknown' });
  throw error;
}

if (response.status >= 300 && response.status < 400) {
  clearTimeout(timer);
  failure({ failureClass: 'REDIRECT_DENIED', httpStatus: response.status });
  await response.body?.cancel().catch(() => undefined);
  throw new Error('redirect denied.');
}
const declaredLength = Number(response.headers.get('content-length'));
if (Number.isFinite(declaredLength) && declaredLength > plan.maxResponseBytes) {
  clearTimeout(timer);
  failure({ failureClass: 'RESPONSE_TOO_LARGE', httpStatus: response.status, declaredByteLength: declaredLength });
  await response.body?.cancel().catch(() => undefined);
  throw new Error('response size outside bounds.');
}
const chunks = [];
let byteLength = 0;
try {
  const reader = response.body?.getReader();
  if (!reader) throw new Error('provider response body is unavailable.');
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    byteLength += value.byteLength;
    if (byteLength > plan.maxResponseBytes) {
      failure({ failureClass: 'RESPONSE_TOO_LARGE', httpStatus: response.status, observedByteLength: byteLength });
      controller.abort();
      await reader.cancel().catch(() => undefined);
      throw new Error('response size outside bounds.');
    }
    chunks.push(value);
  }
} catch (error) {
  if (!fs.existsSync(path.join(out, 'failure-summary.json'))) {
    failure({ failureClass: 'RESPONSE_READ', httpStatus: response.status, errorName: error?.name ?? 'Error', errorMessage: error?.message ?? 'unknown' });
  }
  throw error;
} finally {
  clearTimeout(timer);
}
const bytes = new Uint8Array(byteLength);
let offset = 0;
for (const chunk of chunks) {
  bytes.set(chunk, offset);
  offset += chunk.byteLength;
}
const rawSha256 = crypto.createHash('sha256').update(bytes).digest('hex');
fs.writeFileSync(path.join(out, 'raw-response.json'), bytes);
if (response.status !== 200) {
  failure({ failureClass: 'PROVIDER_HTTP', httpStatus: response.status, rawSha256, byteLength: bytes.length });
  throw new Error(`provider HTTP ${response.status}.`);
}
if (bytes.length === 0) {
  failure({ failureClass: 'EMPTY_RESPONSE', httpStatus: response.status, rawSha256, byteLength: 0 });
  throw new Error('response size outside bounds.');
}

let raw;
try {
  raw = JSON.parse(new TextDecoder().decode(bytes));
} catch {
  failure({ failureClass: 'INVALID_JSON', httpStatus: response.status, rawSha256, byteLength: bytes.length });
  throw new Error('provider response is not JSON.');
}
if (raw.error) {
  failure({ failureClass: 'PROVIDER_ERROR', httpStatus: response.status, rawSha256, byteLength: bytes.length, providerReason: raw.reason ?? 'unknown' });
  throw new Error(`provider error: ${raw.reason ?? 'unknown'}`);
}
if (raw.timezone !== 'GMT' || raw.utc_offset_seconds !== 0) {
  failure({ failureClass: 'TIMEZONE_MISMATCH', httpStatus: response.status, rawSha256, byteLength: bytes.length });
  throw new Error('provider timezone mismatch.');
}
if (!raw.hourly || !Array.isArray(raw.hourly.time) || raw.hourly.time.length < 1 || raw.hourly.time.length > 72) {
  failure({ failureClass: 'HOURLY_TIME_BOUNDS', httpStatus: response.status, rawSha256, byteLength: bytes.length });
  throw new Error('hourly time array outside bounds.');
}
for (const variable of VARS) {
  if (!Array.isArray(raw.hourly[variable]) || raw.hourly[variable].length !== raw.hourly.time.length) {
    failure({ failureClass: 'VARIABLE_LENGTH_MISMATCH', variable, httpStatus: response.status, rawSha256, byteLength: bytes.length });
    throw new Error(`${variable} array mismatch.`);
  }
  if (raw.hourly[variable].some((value) => typeof value !== 'number' || !Number.isFinite(value))) {
    failure({ failureClass: 'NON_FINITE_VARIABLE', variable, httpStatus: response.status, rawSha256, byteLength: bytes.length });
    throw new Error(`${variable} contains non-finite value.`);
  }
}

const evidence = {
  schemaVersion: '1.1',
  evidenceType: 'BKL031_F4C_BOUNDED_ACQUISITION_EVIDENCE',
  gateId: plan.gateId,
  priorFailedWorkflowRunId: plan.priorFailedWorkflowRunId,
  attemptOrdinal: plan.attemptOrdinal,
  environment: 'EVALUATION',
  authority: 'NONE',
  requestCountThisAttempt: 1,
  cumulativeProviderRequestCount: 2,
  requestedAtUtc: new Date().toISOString(),
  providerId: 'OPEN_METEO',
  upstreamAuthorityId: 'ITALIAMETEO_ARPAE',
  modelId: plan.modelId,
  runInitialisationUtc: run,
  location: plan.location,
  response: {
    rawSha256,
    byteLength: bytes.length,
    latitudeDeg: raw.latitude,
    longitudeDeg: raw.longitude,
    elevationM: raw.elevation,
    timezone: raw.timezone,
    utcOffsetSeconds: raw.utc_offset_seconds,
    generationTimeMs: raw.generationtime_ms
  },
  hourlyUnits: raw.hourly_units,
  hourly: raw.hourly,
  unavailableVariables: ['visibility'],
  citation: {
    provider: 'https://open-meteo.com/en/docs/single-runs-api',
    model: 'https://open-meteo.com/en/docs/italia-meteo-arpae-api',
    upstream: 'https://www.arpae.it/it/temi-ambientali/meteo/previsioni-meteo/previsioni-meteo-modellistiche'
  },
  attribution: 'Weather data by Open-Meteo; model data by ItaliaMeteo/ARPAE ICON-2I.',
  boundaries: {
    protectedSiteUsed: false,
    recurringTraffic: false,
    runtimeActivated: false,
    publicProjection: false,
    rankingImplemented: false,
    readinessImplemented: false,
    commandAuthority: 'NONE',
    safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS'
  }
};
fs.writeFileSync(path.join(out, 'normalized-evidence.json'), `${JSON.stringify(evidence, null, 2)}\n`);
fs.writeFileSync(path.join(out, 'summary.json'), `${JSON.stringify({
  gateId: plan.gateId,
  requestCountThisAttempt: 1,
  cumulativeProviderRequestCount: 2,
  rawSha256,
  byteLength: bytes.length,
  runInitialisationUtc: run,
  hourlyInstants: raw.hourly.time.length,
  protectedSiteUsed: false
}, null, 2)}\n`);
console.log(JSON.stringify({ rawSha256, byteLength: bytes.length, hourlyInstants: raw.hourly.time.length, out }, null, 2));
