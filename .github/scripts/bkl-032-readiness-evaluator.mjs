export const BKL032_CONTRACT_VERSION = '1.0';
export const MAX_FRESHNESS_HOURS = 6;
export const THRESHOLDS = Object.freeze({
  rainRateMmH: 0,
  windSpeedKmh: 15,
  windGustKmh: 20,
  cloudCoverPct: 50,
  humidityPct: 90,
  dewPointMarginC: 10
});

const TELEMETRY_DOMAINS = Object.freeze(['weather', 'dome', 'mount', 'camera', 'power', 'network', 'eagle_health']);
const REQUIRED_EVIDENCE = Object.freeze(['forecast', 'astronomy', 'setup_compatibility']);

function check(id, status, reasonCode, details = {}) {
  return { id, status, reason_code: reasonCode, details };
}

function asDate(value) {
  const date = new Date(value);
  return Number.isFinite(date.getTime()) ? date : null;
}

function validEnvelope(value, evaluatedAt) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return { ok: false, reason: 'MISSING' };
  if (!['PASS', 'BLOCK'].includes(value.status)) return { ok: false, reason: 'UNAVAILABLE' };
  if (typeof value.source !== 'string' || value.source.length === 0 || typeof value.evidence_ref !== 'string' || value.evidence_ref.length === 0) return { ok: false, reason: 'PROVENANCE_INVALID' };
  const observed = asDate(value.observed_at_utc);
  const freshUntil = asDate(value.fresh_until_utc);
  if (!observed || !freshUntil || observed > evaluatedAt || freshUntil < observed || (evaluatedAt - observed) > MAX_FRESHNESS_HOURS * 3600_000 || freshUntil < evaluatedAt) return { ok: false, reason: 'STALE_OR_INVALID_TIME' };
  return { ok: true, observed, freshUntil };
}

function finite(value) { return typeof value === 'number' && Number.isFinite(value); }

function inputInvalid(input, evaluatedAt, message) {
  return result('INDETERMINATE', evaluatedAt, [check('input', 'INDETERMINATE', 'INPUT_INVALID', { message })]);
}

function result(decision, evaluatedAt, checks) {
  return {
    schema_version: BKL032_CONTRACT_VERSION,
    decision,
    evaluated_at_utc: evaluatedAt.toISOString(),
    freshness_max_hours: MAX_FRESHNESS_HOURS,
    thresholds: THRESHOLDS,
    checks,
    authority: {
      consumer_mode: 'READ_ONLY',
      readiness_authority: 'DECISION_SUPPORT_ONLY',
      scheduling_authority: false,
      command_authority: 'NONE',
      safety_authority: 'LOCAL_PHYSICAL_INTERLOCKS'
    }
  };
}

export function evaluateReadiness(input, now = new Date()) {
  const evaluatedAt = asDate(input?.evaluated_at_utc) || now;
  if (!input || input.schema_version !== BKL032_CONTRACT_VERSION) return inputInvalid(input, evaluatedAt, 'unsupported or missing schema_version');
  if (!input.session || !input.session.session_id || !input.session.target_ref || !input.session.setup_ref) return inputInvalid(input, evaluatedAt, 'session context incomplete');

  const checks = [];
  let indeterminate = false;
  let blocked = false;

  for (const id of REQUIRED_EVIDENCE) {
    const evidence = validEnvelope(input[id], evaluatedAt);
    if (!evidence.ok) { checks.push(check(id, 'INDETERMINATE', `EVIDENCE_${evidence.reason}`)); indeterminate = true; continue; }
    if (input[id].status === 'BLOCK') { checks.push(check(id, 'NO_GO', 'EVIDENCE_BLOCKING')); blocked = true; }
    else checks.push(check(id, 'PASS', 'EVIDENCE_CURRENT_PASSING', { source: input[id].source, evidence_ref: input[id].evidence_ref }));
  }

  const telemetry = input.live_telemetry;
  if (!telemetry || typeof telemetry !== 'object') return inputInvalid(input, evaluatedAt, 'live_telemetry missing');
  for (const domain of TELEMETRY_DOMAINS) {
    const signal = validEnvelope(telemetry[domain], evaluatedAt);
    if (!signal.ok) { checks.push(check(`telemetry.${domain}`, 'INDETERMINATE', `TELEMETRY_${signal.reason}`)); indeterminate = true; continue; }
    if (telemetry[domain].status === 'BLOCK') { checks.push(check(`telemetry.${domain}`, 'NO_GO', 'TELEMETRY_BLOCKING')); blocked = true; }
    else checks.push(check(`telemetry.${domain}`, 'PASS', 'TELEMETRY_CURRENT_PASSING', { source: telemetry[domain].source, evidence_ref: telemetry[domain].evidence_ref }));
  }

  const weather = telemetry.weather;
  const weatherValues = weather && [weather.rain_rate_mm_h, weather.wind_speed_kmh, weather.wind_gust_kmh, weather.cloud_cover_pct, weather.humidity_pct, weather.ambient_temperature_c, weather.dew_point_c];
  if (!weatherValues || !weatherValues.every(finite)) {
    checks.push(check('telemetry.weather.values', 'INDETERMINATE', 'WEATHER_VALUE_MISSING_OR_INVALID'));
    indeterminate = true;
  } else {
    const margin = weather.ambient_temperature_c - weather.dew_point_c;
    const blocking = [];
    if (weather.rain_rate_mm_h > THRESHOLDS.rainRateMmH) blocking.push('RAIN_ABOVE_ZERO');
    if (weather.wind_speed_kmh > THRESHOLDS.windSpeedKmh) blocking.push('WIND_ABOVE_LIMIT');
    if (weather.wind_gust_kmh > THRESHOLDS.windGustKmh) blocking.push('GUST_ABOVE_LIMIT');
    if (weather.cloud_cover_pct > THRESHOLDS.cloudCoverPct) blocking.push('CLOUD_ABOVE_LIMIT');
    if (weather.humidity_pct > THRESHOLDS.humidityPct) blocking.push('HUMIDITY_ABOVE_LIMIT');
    if (margin < THRESHOLDS.dewPointMarginC) blocking.push('DEW_MARGIN_BELOW_LIMIT');
    if (blocking.length > 0) { checks.push(check('telemetry.weather.thresholds', 'NO_GO', 'WEATHER_THRESHOLD_BLOCKING', { blocking, dew_point_margin_c: margin })); blocked = true; }
    else checks.push(check('telemetry.weather.thresholds', 'PASS', 'WEATHER_THRESHOLDS_PASSING', { dew_point_margin_c: margin }));
  }

  const decision = blocked ? 'NO_GO' : indeterminate ? 'INDETERMINATE' : 'GO';
  return result(decision, evaluatedAt, checks);
}
