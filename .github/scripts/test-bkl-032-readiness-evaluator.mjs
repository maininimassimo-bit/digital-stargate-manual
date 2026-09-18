import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { evaluateReadiness } from './bkl-032-readiness-evaluator.mjs';

const readinessSchema = JSON.parse(await readFile(new URL('../../contracts/readiness/bkl-032-session-readiness-v1.schema.json', import.meta.url), 'utf8'));
const telemetrySchema = JSON.parse(await readFile(new URL('../../contracts/readiness/bkl-032-live-telemetry-v1.schema.json', import.meta.url), 'utf8'));

const evaluatedAt = '2026-09-18T12:00:00.000Z';
const envelope = (extra = {}) => ({ status: 'PASS', observed_at_utc: '2026-09-18T11:00:00.000Z', fresh_until_utc: '2026-09-18T17:00:00.000Z', source: 'synthetic-read-only-fixture', evidence_ref: 'fixture://bkl-032', ...extra });
const base = () => ({
  schema_version: '1.0',
  evaluated_at_utc: evaluatedAt,
  session: { session_id: 'session-001', target_ref: 'target://M42', setup_ref: 'setup://C8-QHY695A' },
  forecast: envelope(), astronomy: envelope(), setup_compatibility: envelope(),
  live_telemetry: {
    weather: envelope({ rain_rate_mm_h: 0, wind_speed_kmh: 15, wind_gust_kmh: 20, cloud_cover_pct: 50, humidity_pct: 90, ambient_temperature_c: 10, dew_point_c: 0 }),
    dome: envelope(), mount: envelope(), camera: envelope(), power: envelope(), network: envelope(), eagle_health: envelope()
  }
});

test('versioned contracts expose the mandatory BKL-032 evidence surface', () => {
  assert.equal(readinessSchema.properties.schema_version.const, '1.0');
  assert.deepEqual(readinessSchema.required, ['schema_version', 'session', 'evaluated_at_utc', 'forecast', 'astronomy', 'setup_compatibility', 'live_telemetry']);
  assert.deepEqual(telemetrySchema.required, ['weather', 'dome', 'mount', 'camera', 'power', 'network', 'eagle_health']);
  assert.deepEqual(telemetrySchema.$defs.weather.allOf[1].required, ['rain_rate_mm_h', 'wind_speed_kmh', 'wind_gust_kmh', 'cloud_cover_pct', 'humidity_pct', 'ambient_temperature_c', 'dew_point_c']);
});

test('complete current evidence produces GO and equality passes', () => {
  const decision = evaluateReadiness(base());
  assert.equal(decision.decision, 'GO');
  assert.equal(decision.authority.command_authority, 'NONE');
  assert.equal(decision.authority.safety_authority, 'LOCAL_PHYSICAL_INTERLOCKS');
});

test('each approved weather threshold produces NO_GO', () => {
  for (const mutation of [
    w => { w.rain_rate_mm_h = 0.1; }, w => { w.wind_speed_kmh = 15.1; }, w => { w.wind_gust_kmh = 20.1; },
    w => { w.cloud_cover_pct = 50.1; }, w => { w.humidity_pct = 90.1; }, w => { w.dew_point_c = 0.1; }
  ]) {
    const input = base(); mutation(input.live_telemetry.weather);
    assert.equal(evaluateReadiness(input).decision, 'NO_GO');
  }
});

test('missing or stale mandatory evidence produces INDETERMINATE', () => {
  const missing = base(); delete missing.live_telemetry.camera;
  assert.equal(evaluateReadiness(missing).decision, 'INDETERMINATE');
  const stale = base(); stale.forecast.fresh_until_utc = '2026-09-18T11:59:59.000Z';
  assert.equal(evaluateReadiness(stale).decision, 'INDETERMINATE');
});

test('valid current non-weather blocking evidence produces NO_GO', () => {
  const input = base(); input.live_telemetry.mount.status = 'BLOCK';
  assert.equal(evaluateReadiness(input).decision, 'NO_GO');
});

test('malformed input fails closed without authority escalation', () => {
  const decision = evaluateReadiness({ schema_version: '0.1', evaluated_at_utc: evaluatedAt });
  assert.equal(decision.decision, 'INDETERMINATE');
  assert.equal(decision.authority.consumer_mode, 'READ_ONLY');
});
