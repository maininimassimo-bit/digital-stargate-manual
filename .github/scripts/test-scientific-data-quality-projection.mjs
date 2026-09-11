import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { buildScientificDataQualityProjection, mapCatalogSessionToF3Inputs } from './scientific-data-quality-projection.mjs';

const profile = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f3-fixture.json', 'utf8')).profile;
const catalog = sessions => ({ schemaVersion: '1.5', catalogStatus: 'VERSIONED_ANALYTICS_PROJECTION', sessions });
const session = (id, overrides = {}) => ({
  sessionId: id,
  start: `${id.slice(0, 10)}T20:00:00Z`,
  end: `${id.slice(11)}T04:00:00Z`,
  target: 'SYNTHETIC TARGET',
  metadataState: 'CANONICAL_EVIDENCE',
  manifestState: 'VERSIONED',
  evidenceState: 'SOURCE_METRICS_AVAILABLE',
  sourceMetricsPath: `data/sessions/${id.slice(0, 4)}/${id.slice(5, 7)}/${id}/normalized/session-metrics.json`,
  lightStarted: 10,
  lightCompleted: 8,
  completionPct: 80,
  guiding: { state: 'AVAILABLE', sampleCount: 1000, rmsTotalArcsec: 1.25 },
  sqm: { state: 'AVAILABLE', medianMagArcsec2: 20.5, temporalCoverage: 0.9 },
  ...overrides
});
const at = '2026-09-11T08:00:00.000Z';

test('maps catalog evidence without inventing guiding temporal coverage', () => {
  const inputs = mapCatalogSessionToF3Inputs(session('2026-09-01_2026-09-02'));
  assert.equal(inputs.length, 4);
  assert.equal(inputs.find(item => item.dimension === 'GUIDING_STABILITY').coverage, 0);
  assert.equal(inputs.find(item => item.dimension === 'SKY_QUALITY_COVERAGE').coverage, 0.9);
  assert.equal(inputs.every(item => item.evidenceClass === 'DECLARED'), true);
});

test('builds a deterministic full-catalog projection without ranking', () => {
  const source = catalog([
    session('2026-09-03_2026-09-04'),
    session('2026-09-01_2026-09-02')
  ]);
  const first = buildScientificDataQualityProjection(source, profile, { generatedAt: at });
  const second = buildScientificDataQualityProjection(source, profile, { generatedAt: at });
  assert.deepEqual(first, second);
  assert.deepEqual(first.sourceCatalog.sessionIds, ['2026-09-01_2026-09-02', '2026-09-03_2026-09-04']);
  assert.equal(first.summary.availableAssessments, 2);
  assert.equal(first.authority.productionUseAuthorized, false);
  assert.equal(JSON.stringify(first).includes('ranking'), false);
  assert.equal(Object.isFrozen(first.assessments), true);
});

test('missing required SQM stays unavailable with explicit decomposition', () => {
  const projection = buildScientificDataQualityProjection(catalog([
    session('2026-09-01_2026-09-02', { sqm: null })
  ]), profile, { generatedAt: at });
  const record = projection.assessments[0];
  assert.equal(record.projectionRecordState, 'UNAVAILABLE');
  assert.equal(record.assessment.score, null);
  assert.equal(record.assessment.decomposition.find(item => item.dimension === 'SKY_QUALITY_COVERAGE').exclusionReason, 'REQUIRED_EVIDENCE_MISSING');
});

test('profile out-of-range values become invalid records without aborting the catalog', () => {
  const projection = buildScientificDataQualityProjection(catalog([
    session('2026-09-01_2026-09-02', { guiding: { state: 'AVAILABLE', sampleCount: 1000, rmsTotalArcsec: 0.25 } }),
    session('2026-09-03_2026-09-04')
  ]), profile, { generatedAt: at });
  assert.equal(projection.summary.invalidAssessments, 1);
  assert.equal(projection.summary.availableAssessments, 1);
  assert.equal(projection.assessments[0].generationError.code, 'PROFILE_VALUE_OUT_OF_RANGE');
  assert.equal(projection.assessments[1].projectionRecordState, 'AVAILABLE');
});

test('catalog content changes source and projection identity', () => {
  const original = buildScientificDataQualityProjection(catalog([session('2026-09-01_2026-09-02')]), profile, { generatedAt: at });
  const changed = buildScientificDataQualityProjection(catalog([session('2026-09-01_2026-09-02', { completionPct: 70 })]), profile, { generatedAt: at });
  assert.notEqual(original.sourceCatalog.digest, changed.sourceCatalog.digest);
  assert.notEqual(original.projectionDigest, changed.projectionDigest);
});

test('duplicate catalog session IDs fail closed', () => {
  const duplicate = session('2026-09-01_2026-09-02');
  assert.throws(() => buildScientificDataQualityProjection(catalog([duplicate, structuredClone(duplicate)]), profile, { generatedAt: at }), /unique/);
});

test('catalog authority drift fails closed', () => {
  assert.throws(() => buildScientificDataQualityProjection({ schemaVersion: '1.5', catalogStatus: 'AUTHORITATIVE', sessions: [] }, profile, { generatedAt: at }), /authority\/status/);
});
