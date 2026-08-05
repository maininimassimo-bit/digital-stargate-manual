import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import process from 'node:process';

const SOURCE_PATH = 'docs/data/scientific-session-catalog.json';
const OUTPUT_PATH = 'docs/data/scientific-observation-index.json';
const ALGORITHM_VERSION = '1.0.0';

const stableJson = (value) => `${JSON.stringify(value, null, 2)}\n`;
const digest = (value) => `sha256:${createHash('sha256').update(value).digest('hex')}`;
const slug = (value) => String(value || '')
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toUpperCase()
  .replace(/[^A-Z0-9]+/g, '-')
  .replace(/^-+|-+$/g, '') || 'UNKNOWN';

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const normalizeQuality = (value) => {
  const normalized = String(value || 'UNKNOWN').toUpperCase();
  if (normalized === 'VALIDATED_ANALYTICS') return 'ACCEPTED';
  if (normalized === 'ATTENTION_REQUIRED') return 'DEGRADED';
  return normalized;
};

const buildCatalogItem = (session, sourceDigest) => ({
  schemaVersion: '1.0',
  catalogItemId: `CAT-SESSION-${slug(session.sessionId)}`,
  entityType: 'OBSERVATION_SESSION',
  entityId: session.sessionId,
  sourceSystem: 'scientific-session-catalog.json',
  sourceVersion: '1.0',
  sourceDigest,
  catalogState: 'INDEXABLE',
  qualityState: normalizeQuality(session.qualityState),
  recordVersion: 1,
  indexedAtUtc: null,
  lastReconciledAtUtc: null,
  reconciliationState: 'MATCHED',
  supersedesCatalogItemId: null
});

const buildSearchDocument = (session, catalogItemId, indexBuildId, sourceDigest) => ({
  schemaVersion: '1.0',
  searchDocumentId: `SRCH-${catalogItemId}-V1`,
  catalogItemId,
  indexBuildId,
  documentType: 'SCIENTIFIC_SESSION',
  title: `${session.target} · ${session.observationDate}`,
  summary: [
    `Sessione ${session.sessionId}`,
    session.filter ? `filtro ${session.filter}` : null,
    session.telescope ? `telescopio ${session.telescope}` : null,
    session.camera ? `camera ${session.camera}` : null,
    Number.isFinite(session.integrationHours) ? `${session.integrationHours} h di integrazione` : null
  ].filter(Boolean).join(' · '),
  normalizedText: [
    session.target,
    session.sessionId,
    session.observationDate,
    session.configurationId,
    session.telescope,
    session.camera,
    session.filter,
    session.binning,
    session.qualityState,
    session.transferState,
    session.manifestState,
    session.evidenceState
  ].filter(Boolean).join(' ').toLowerCase(),
  keywords: [...new Set([
    slug(session.target).toLowerCase(),
    slug(session.telescope).toLowerCase(),
    slug(session.camera).toLowerCase(),
    slug(session.filter).toLowerCase(),
    String(session.observationDate || '').slice(0, 4),
    normalizeQuality(session.qualityState).toLowerCase()
  ].filter(Boolean))],
  facetValues: {
    target: [session.target].filter(Boolean),
    year: [String(session.observationDate || '').slice(0, 4)].filter(Boolean),
    telescope: [session.telescope].filter(Boolean),
    camera: [session.camera].filter(Boolean),
    filter: [session.filter].filter(Boolean),
    quality: [normalizeQuality(session.qualityState)]
  },
  sourceUrl: `scientific-session-detail/?sessionId=${encodeURIComponent(session.sessionId)}`,
  rankingSignals: {
    qualityWeight: normalizeQuality(session.qualityState) === 'ACCEPTED' ? 1 : 0.6,
    metadataCompleteness: [
      session.target,
      session.observationDate,
      session.configurationId,
      session.telescope,
      session.camera,
      session.filter,
      session.qualityState
    ].filter(Boolean).length / 7,
    integrationHours: Number(session.integrationHours || 0)
  },
  sourceDigest
});

const buildOutput = (sourceText, source) => {
  assert(source?.schemaVersion === '1.0', 'Unsupported scientific session catalog schema');
  assert(Array.isArray(source.sessions), 'sessions must be an array');

  const sourceDigest = digest(sourceText);
  const buildKey = sourceDigest.split(':')[1].slice(0, 14).toUpperCase();
  const indexBuildId = `IDX-${buildKey}`;

  const catalogItems = [];
  const searchDocuments = [];
  const reconciliationRecords = [];

  for (const session of [...source.sessions].sort((a, b) => String(a.sessionId).localeCompare(String(b.sessionId)))) {
    assert(session.sessionId, 'Every session requires sessionId');
    assert(session.observationDate, `Session ${session.sessionId} requires observationDate`);

    const sessionDigest = digest(stableJson(session));
    const item = buildCatalogItem(session, sessionDigest);
    const document = buildSearchDocument(session, item.catalogItemId, indexBuildId, sessionDigest);

    catalogItems.push(item);
    searchDocuments.push(document);
    reconciliationRecords.push({
      reconciliationRecordId: `REC-${indexBuildId}-${String(reconciliationRecords.length + 1).padStart(3, '0')}`,
      indexBuildId,
      catalogItemId: item.catalogItemId,
      sourceDigestExpected: sessionDigest,
      sourceDigestObserved: sessionDigest,
      reconciliationState: 'MATCHED',
      differenceType: null,
      detectedAtUtc: null,
      resolvedAtUtc: null,
      resolutionReference: null
    });
  }

  const projection = {
    schemaVersion: '1.0',
    algorithmVersion: ALGORITHM_VERSION,
    generatedFrom: SOURCE_PATH,
    sourceSnapshotDigest: sourceDigest,
    indexBuild: {
      indexBuildId,
      algorithmVersion: ALGORITHM_VERSION,
      sourceSnapshotDigest: sourceDigest,
      documentCount: searchDocuments.length,
      failureCount: 0,
      buildStatus: 'COMPLETED'
    },
    summary: {
      sessionCount: source.sessions.length,
      catalogItemCount: catalogItems.length,
      searchDocumentCount: searchDocuments.length,
      reconciliationMatched: reconciliationRecords.filter((record) => record.reconciliationState === 'MATCHED').length
    },
    catalogItems,
    searchDocuments,
    reconciliationRecords
  };

  projection.indexBuild.outputDigest = digest(stableJson({
    catalogItems,
    searchDocuments,
    reconciliationRecords
  }));

  return projection;
};

const main = async () => {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);

  const sourceText = await readFile(SOURCE_PATH, 'utf8');
  const source = JSON.parse(sourceText);
  const generated = stableJson(buildOutput(sourceText, source));

  if (mode === '--print') {
    process.stdout.write(generated);
    return;
  }

  if (mode === '--write') {
    await writeFile(OUTPUT_PATH, generated, 'utf8');
    process.stdout.write(`Generated ${OUTPUT_PATH} from ${SOURCE_PATH}.\n`);
    return;
  }

  const current = await readFile(OUTPUT_PATH, 'utf8').catch(() => '');
  if (current !== generated) {
    process.stderr.write('Scientific catalog drift detected. Run: node .github/scripts/generate-scientific-catalog.mjs --write\n');
    process.exitCode = 1;
    return;
  }

  process.stdout.write('Scientific observation index is aligned with its governed source.\n');
};

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
