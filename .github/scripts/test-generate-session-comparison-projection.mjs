import test from 'node:test';
import assert from 'node:assert/strict';
import { buildDynamicSessionComparisonProjection } from './generate-session-comparison-projection.mjs';

const session = (id, median, overrides = {}) => ({
  sessionId: id,
  start: `${id.slice(0,10)}T20:00:00`,
  end: `${id.slice(11)}T04:00:00`,
  evidenceState: 'SOURCE_METRICS_AVAILABLE',
  sourceMetricsPath: `data/sessions/${id.slice(0,4)}/${id.slice(5,7)}/${id}/normalized/session-metrics.json`,
  sqm: median === null ? { state: 'NOT_AVAILABLE', medianMagArcsec2: null } : { state: 'AVAILABLE', medianMagArcsec2: median },
  ...overrides
});

const catalog = sessions => ({ catalogStatus: 'VERSIONED_ANALYTICS_PROJECTION', sessions });

test('includes every comparable SQM session and computes descriptive summary', () => {
  const projection = buildDynamicSessionComparisonProjection(catalog([
    session('2026-09-01_2026-09-02', 18.66),
    session('2026-09-03_2026-09-04', 20.57),
    session('2026-09-05_2026-09-06', 20.89)
  ]), { generatedAt: '2026-09-10T00:00:00Z' });
  assert.equal(projection.includedSessions.length, 3);
  assert.equal(projection.exclusions.length, 0);
  assert.equal(projection.descriptiveSummary.sampleSize, 3);
  assert.deepEqual(projection.catalogCoverage, { totalSessions:3, includedSessions:3, excludedSessions:0, sourceCatalog:'docs/data/scientific-session-catalog.json' });
  assert.equal(projection.authority.actionAuthority, 'NONE');
  assert.equal(projection.authority.acceptanceAuthority, false);
});

test('keeps catalog sessions without comparable SQM as explicit exclusions', () => {
  const projection = buildDynamicSessionComparisonProjection(catalog([
    session('2026-09-01_2026-09-02', 18.66),
    session('2026-09-03_2026-09-04', 20.57),
    session('2026-09-05_2026-09-06', null)
  ]), { generatedAt: '2026-09-10T00:00:00Z' });
  assert.equal(projection.includedSessions.length, 2);
  assert.equal(projection.exclusions.length, 1);
  assert.equal(projection.exclusions[0].sessionId, '2026-09-05_2026-09-06');
  assert.equal(projection.exclusions[0].reason, 'VALUE_UNAVAILABLE');
  assert.equal(projection.catalogCoverage.excludedSessions, 1);
});

test('missing source provenance fails closed and remains excluded', () => {
  const projection = buildDynamicSessionComparisonProjection(catalog([
    session('2026-09-01_2026-09-02', 18.66),
    session('2026-09-03_2026-09-04', 20.57),
    session('2026-09-05_2026-09-06', 20.89, { sourceMetricsPath:null })
  ]), { generatedAt: '2026-09-10T00:00:00Z' });
  assert.equal(projection.includedSessions.length, 2);
  assert.equal(projection.exclusions.length, 1);
  assert.equal(projection.exclusions[0].reason, 'PROVENANCE_INSUFFICIENT');
});

test('catalog authority drift is rejected', () => {
  assert.throws(() => buildDynamicSessionComparisonProjection({ catalogStatus:'AUTHORITATIVE', sessions:[session('2026-09-01_2026-09-02',18.66),session('2026-09-03_2026-09-04',20.57)] }), /authority\/status/);
});
