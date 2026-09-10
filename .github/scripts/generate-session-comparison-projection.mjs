import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
import { buildComparisonCandidate, buildComparisonSet } from './session-comparison-read-model.mjs';
import { buildSessionComparisonProjection } from './session-comparison-projection.mjs';

export const CATALOG_PATH = 'docs/data/scientific-session-catalog.json';
export const OUTPUT_PATH = 'docs/data/session-comparison-projection.json';
export const PROJECTION_ID = 'BKL037-SQM-DYNAMIC-V1';
export const COMPARISON_SET_ID = 'BKL037-SQM-CATALOG-V1';

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const nonEmpty = value => typeof value === 'string' && value.trim().length > 0;
const finiteNumber = value => typeof value === 'number' && Number.isFinite(value);
const stableJson = value => `${JSON.stringify(value, null, 2)}\n`;
const normalizeState = value => String(value ?? '').trim().toUpperCase();

function sourceRef(session) {
  return nonEmpty(session?.sourceMetricsPath) ? session.sourceMetricsPath.trim() : null;
}

function candidateFromSession(session) {
  const sessionId = String(session?.sessionId ?? '').trim();
  assert(sessionId, 'Scientific session catalog entry missing sessionId.');

  const sqm = session?.sqm && typeof session.sqm === 'object' ? session.sqm : null;
  const sqmState = normalizeState(sqm?.state);
  const median = finiteNumber(sqm?.medianMagArcsec2) ? sqm.medianMagArcsec2 : null;
  const metricsRef = sourceRef(session);
  const evidenceAvailable = session?.evidenceState === 'SOURCE_METRICS_AVAILABLE';
  const comparableEvidence = sqmState === 'AVAILABLE' && median !== null && metricsRef && evidenceAvailable;

  return buildComparisonCandidate({
    sessionId,
    dimension: 'SQM_MEDIAN',
    value: median,
    unit: 'mag/arcsec2',
    unitSemantics: 'CATALOG_PROPERTY_MEDIAN_MAG_ARCSEC2',
    source: 'SCIENTIFIC_SESSION_CATALOG',
    observedAt: session?.end ?? session?.start ?? null,
    quality: comparableEvidence ? 'AVAILABLE' : (sqmState === 'STALE' ? 'STALE' : 'UNKNOWN'),
    completeness: comparableEvidence ? 'COMPLETE' : (median === null ? 'UNAVAILABLE' : 'PARTIAL'),
    provenanceRef: metricsRef ? `${metricsRef}#sqm` : null,
    actionAuthority: 'NONE',
    acceptanceAuthority: false
  });
}

export function buildDynamicSessionComparisonProjection(catalog, { generatedAt = 'SOURCE_SNAPSHOT' } = {}) {
  assert(catalog && typeof catalog === 'object', 'Scientific session catalog is required.');
  assert(catalog.catalogStatus === 'VERSIONED_ANALYTICS_PROJECTION', 'Scientific session catalog authority/status is not supported.');
  assert(Array.isArray(catalog.sessions), 'Scientific session catalog sessions[] is required.');
  assert(catalog.sessions.length >= 2, 'At least two scientific sessions are required.');

  const sessions = [...catalog.sessions].sort((a, b) => String(a.sessionId ?? '').localeCompare(String(b.sessionId ?? '')));
  const candidates = sessions.map(candidateFromSession);
  const refs = [CATALOG_PATH, ...sessions.map(sourceRef).filter(Boolean)];
  const sourceRefs = [...new Set(refs)];

  const set = buildComparisonSet({
    comparisonSetId: COMPARISON_SET_ID,
    dimension: 'SQM_MEDIAN',
    unit: 'mag/arcsec2',
    candidates,
    inclusionRules: [
      'sqm.state == AVAILABLE',
      'sqm.medianMagArcsec2 is finite',
      'evidenceState == SOURCE_METRICS_AVAILABLE',
      'sourceMetricsPath is present'
    ],
    exclusionRules: [
      'missing SQM median -> VALUE_UNAVAILABLE',
      'missing/stale evidence -> fail closed',
      'missing provenance -> fail closed'
    ],
    sourceRefs,
    createdAt: generatedAt
  });

  const base = buildSessionComparisonProjection({
    projectionId: PROJECTION_ID,
    comparisonSet: set,
    generatedAt
  });

  return Object.freeze({
    ...base,
    catalogCoverage: Object.freeze({
      totalSessions: sessions.length,
      includedSessions: base.includedSessions.length,
      excludedSessions: base.exclusions.length,
      sourceCatalog: CATALOG_PATH
    })
  });
}

function comparableWithoutGeneratedAt(value) {
  const clone = structuredClone(value);
  clone.generatedAt = 'SOURCE_SNAPSHOT';
  return clone;
}

async function readCurrent() {
  try { return JSON.parse(await readFile(OUTPUT_PATH, 'utf8')); }
  catch { return null; }
}

async function main() {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);

  const catalog = JSON.parse(await readFile(CATALOG_PATH, 'utf8'));
  const current = await readCurrent();
  const checkTimestamp = nonEmpty(current?.generatedAt) ? current.generatedAt : 'SOURCE_SNAPSHOT';
  const expectedForCheck = buildDynamicSessionComparisonProjection(catalog, { generatedAt: checkTimestamp });

  if (mode === '--print') {
    process.stdout.write(stableJson(expectedForCheck));
    return;
  }

  if (mode === '--check') {
    if (!current || stableJson(current) !== stableJson(expectedForCheck)) {
      process.stderr.write('Session comparison projection drift detected. Run: node .github/scripts/generate-session-comparison-projection.mjs --write\n');
      process.exitCode = 1;
      return;
    }
    process.stdout.write(`Session comparison projection aligned: ${expectedForCheck.catalogCoverage.includedSessions}/${expectedForCheck.catalogCoverage.totalSessions} sessions comparable.\n`);
    return;
  }

  if (current && stableJson(comparableWithoutGeneratedAt(current)) === stableJson(comparableWithoutGeneratedAt(expectedForCheck))) {
    process.stdout.write('Session comparison projection already aligned; no write required.\n');
    return;
  }

  const generated = buildDynamicSessionComparisonProjection(catalog, { generatedAt: new Date().toISOString() });
  await writeFile(OUTPUT_PATH, stableJson(generated), 'utf8');
  process.stdout.write(`Generated ${OUTPUT_PATH}: ${generated.catalogCoverage.includedSessions}/${generated.catalogCoverage.totalSessions} sessions comparable; ${generated.catalogCoverage.excludedSessions} excluded.\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
