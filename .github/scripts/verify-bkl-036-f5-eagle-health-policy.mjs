import fs from 'node:fs';
import assert from 'node:assert/strict';

const policy = JSON.parse(fs.readFileSync('docs/data/bkl-036-f5-eagle-health-policy-v1.json', 'utf8'));
const SIGNALS = ['cpu', 'memory', 'storage', 'uptime', 'time_sync'];
const fresh = (value, now) => value.observed_at_utc && value.fresh_until_utc && now <= value.fresh_until_utc;
const number = value => typeof value === 'number' && Number.isFinite(value);

export const evaluateEagleHealth = input => {
  const required = input.signals || {};
  for (const signal of SIGNALS) {
    if (!required[signal] || !fresh(required[signal], input.now)) return { state: 'UNAVAILABLE', score: null, reason: 'REQUIRED_SIGNAL_NOT_CURRENT' };
  }
  const cpuSamples = required.cpu.samples || [];
  const memorySamples = required.memory.samples || [];
  if (cpuSamples.length < 5 || memorySamples.length < 5 || cpuSamples.some(value => !number(value)) || memorySamples.some(value => !number(value))) {
    return { state: 'UNAVAILABLE', score: null, reason: 'WINDOW_NOT_COMPUTABLE' };
  }
  const storage = required.storage.volumes || {};
  if (!number(storage.C?.free_pct) || !number(storage.D?.free_pct)) return { state: 'UNAVAILABLE', score: null, reason: 'STORAGE_C_OR_D_NOT_COMPUTABLE' };
  const degraded = cpuSamples.some(value => value > 90) || memorySamples.some(value => value < 20) || storage.C.free_pct < 20 || storage.D.free_pct < 20;
  return degraded ? { state: 'DEGRADED', score: 50, reason: 'THRESHOLD_EXCEEDED' } : { state: 'HEALTHY', score: 100, reason: 'ALL_REQUIRED_SIGNALS_HEALTHY' };
};

assert.equal(policy.contract_id, 'DSG.BKL036.F5.EagleHealthPolicy');
assert.deepEqual(policy.required_signals, SIGNALS);
assert.equal(policy.thresholds.cpu.percent, 90);
assert.equal(policy.thresholds.memory_available.percent, 20);
assert.deepEqual(policy.thresholds.storage_volumes, ['C:', 'D:']);
assert.equal(policy.thresholds.evaluation_window.minimum_samples, 5);
assert.equal(policy.scoring.degraded, 50);
assert.deepEqual(policy.scoring.comparable_states, ['HEALTHY', 'DEGRADED']);
assert.equal(policy.boundaries.command_authority, 'NONE');
assert.equal(policy.boundaries.safety_authority, 'NONE');

const base = { now: '2026-09-22T19:00:00Z', signals: {
  cpu: { observed_at_utc: '2026-09-22T18:59:00Z', fresh_until_utc: '2026-09-22T19:01:00Z', samples: [20, 25, 30, 35, 40] },
  memory: { observed_at_utc: '2026-09-22T18:59:00Z', fresh_until_utc: '2026-09-22T19:01:00Z', samples: [60, 60, 59, 58, 58] },
  storage: { observed_at_utc: '2026-09-22T18:59:00Z', fresh_until_utc: '2026-09-22T19:01:00Z', volumes: { C: { free_pct: 30 }, D: { free_pct: 40 } } },
  uptime: { observed_at_utc: '2026-09-22T18:59:00Z', fresh_until_utc: '2026-09-22T19:01:00Z' },
  time_sync: { observed_at_utc: '2026-09-22T18:59:00Z', fresh_until_utc: '2026-09-22T19:01:00Z', last_successful_sync_utc: '2026-09-22T18:59:30Z' }
}};
assert.deepEqual(evaluateEagleHealth(base), { state: 'HEALTHY', score: 100, reason: 'ALL_REQUIRED_SIGNALS_HEALTHY' });
assert.equal(evaluateEagleHealth({ ...base, signals: { ...base.signals, storage: { ...base.signals.storage, volumes: { C: { free_pct: 19 }, D: { free_pct: 40 } } } } }).state, 'DEGRADED');
assert.equal(evaluateEagleHealth({ ...base, signals: { ...base.signals, cpu: { ...base.signals.cpu, samples: [20, 20, 20, 20, 95] } } }).score, 50);
assert.equal(evaluateEagleHealth({ ...base, signals: { ...base.signals, time_sync: { ...base.signals.time_sync, fresh_until_utc: '2026-09-22T18:59:59Z' } } }).state, 'UNAVAILABLE');
assert.equal(evaluateEagleHealth({ ...base, signals: { ...base.signals, storage: { ...base.signals.storage, volumes: { C: { free_pct: null }, D: { free_pct: 40 } } } } }).state, 'UNAVAILABLE');
console.log('BKL-036-F5 EAGLE Health policy PASS: thresholds, freshness, comparability and scoring are deterministic.');
