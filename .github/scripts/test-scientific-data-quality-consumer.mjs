import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { buildScientificDataQualityProjection } from './scientific-data-quality-projection.mjs';
import { validateProjectionContract, validateProjectionFreshness } from '../../docs/javascripts/scientific-data-quality-core.mjs';

const profile = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f3-fixture.json', 'utf8')).profile;
const session = id => ({
  sessionId: id, start: `${id.slice(0, 10)}T20:00:00Z`, end: `${id.slice(11)}T04:00:00Z`, target: 'SYNTHETIC',
  metadataState: 'CANONICAL_EVIDENCE', manifestState: 'VERSIONED', evidenceState: 'SOURCE_METRICS_AVAILABLE',
  sourceMetricsPath: `data/sessions/${id.slice(0, 4)}/${id.slice(5, 7)}/${id}/normalized/session-metrics.json`,
  lightStarted: 10, lightCompleted: 8, completionPct: 80,
  guiding: { state: 'AVAILABLE', sampleCount: 1000, rmsTotalArcsec: 1.25 },
  sqm: { state: 'AVAILABLE', medianMagArcsec2: 20.5, temporalCoverage: 0.9 }
});
const catalog = { schemaVersion: '1.5', catalogStatus: 'VERSIONED_ANALYTICS_PROJECTION', sessions: [session('2026-09-01_2026-09-02')] };
const build = value => buildScientificDataQualityProjection(value, profile, { generatedAt: '2026-09-11T08:00:00.000Z' });

test('consumer accepts an aligned projection and catalog', async () => {
  const projection = build(catalog);
  assert.equal(validateProjectionContract(projection), true);
  assert.equal(await validateProjectionFreshness(projection, catalog), true);
});

test('a newly imported session without regenerated projection is rejected as stale', async () => {
  const projection = build(catalog);
  const changed = structuredClone(catalog);
  changed.sessions.push(session('2026-09-03_2026-09-04'));
  await assert.rejects(validateProjectionFreshness(projection, changed), /STALE_SOURCE_CATALOG_DIGEST_MISMATCH/);
});

test('same session set with changed evidence is rejected as stale', async () => {
  const projection = build(catalog);
  const changed = structuredClone(catalog);
  changed.sessions[0].completionPct = 70;
  await assert.rejects(validateProjectionFreshness(projection, changed), /STALE_SOURCE_CATALOG_DIGEST_MISMATCH/);
});

test('tampered projection identity is rejected', async () => {
  const projection = structuredClone(build(catalog));
  projection.summary.availableAssessments = 99;
  await assert.rejects(validateProjectionFreshness(projection, catalog), /PROJECTION_DIGEST_MISMATCH/);
});

test('authority escalation fails closed before rendering', () => {
  const projection = structuredClone(build(catalog));
  projection.authority.productionUseAuthorized = true;
  assert.throws(() => validateProjectionContract(projection), /production authority drift/);
});
