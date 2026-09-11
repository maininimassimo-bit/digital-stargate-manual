import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
import { buildScientificDataQualityProjection } from './scientific-data-quality-projection.mjs';

export const CATALOG_PATH = 'docs/data/scientific-session-catalog.json';
export const PROFILE_FIXTURE_PATH = 'docs/data/scientific-data-quality-f3-fixture.json';
export const OUTPUT_PATH = 'docs/data/scientific-data-quality-projection.json';

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const stableJson = value => `${JSON.stringify(value, null, 2)}\n`;

async function readJson(path) {
  return JSON.parse(await readFile(path, 'utf8'));
}

async function readCurrent() {
  try { return await readJson(OUTPUT_PATH); }
  catch { return null; }
}

function withoutGenerationIdentity(value) {
  const clone = structuredClone(value);
  clone.generatedAt = '2000-01-01T00:00:00.000Z';
  delete clone.projectionDigest;
  return clone;
}

export async function generateProjection({ catalog, profile, generatedAt }) {
  return buildScientificDataQualityProjection(catalog, profile, { generatedAt });
}

async function main() {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);
  const [catalog, fixture, current] = await Promise.all([readJson(CATALOG_PATH), readJson(PROFILE_FIXTURE_PATH), readCurrent()]);
  const checkTimestamp = current?.generatedAt ?? '2000-01-01T00:00:00.000Z';
  const expected = await generateProjection({ catalog, profile: fixture.profile, generatedAt: checkTimestamp });

  if (mode === '--print') {
    process.stdout.write(stableJson(expected));
    return;
  }
  if (mode === '--check') {
    if (!current || stableJson(current) !== stableJson(expected)) {
      process.stderr.write('Scientific data quality projection drift detected. Run: node .github/scripts/generate-scientific-data-quality-projection.mjs --write\n');
      process.exitCode = 1;
      return;
    }
    process.stdout.write(`Scientific data quality projection aligned: ${expected.summary.totalSessions} sessions; ${expected.summary.availableAssessments} experimental assessments available.\n`);
    return;
  }

  if (current && stableJson(withoutGenerationIdentity(current)) === stableJson(withoutGenerationIdentity(expected))) {
    process.stdout.write('Scientific data quality projection already aligned; no write required.\n');
    return;
  }
  const generated = await generateProjection({ catalog, profile: fixture.profile, generatedAt: new Date().toISOString() });
  await writeFile(OUTPUT_PATH, stableJson(generated), 'utf8');
  process.stdout.write(`Generated ${OUTPUT_PATH}: ${generated.summary.totalSessions} sessions; ${generated.summary.availableAssessments} experimental assessments available.\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
