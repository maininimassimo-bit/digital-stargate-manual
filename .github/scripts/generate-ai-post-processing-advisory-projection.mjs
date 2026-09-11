import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
import {
  buildAdvisoryProjection,
  canonicalJson,
  discoverProvenanceSources
} from './ai-post-processing-advisory-projection.mjs';

export const CATALOG_PATH = 'docs/data/scientific-session-catalog.json';
export const OUTPUT_PATH = 'docs/data/ai-post-processing-advisory-projection.json';

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const stableJson = (value) => `${JSON.stringify(value, null, 2)}\n`;

async function readJson(repositoryPath) {
  return JSON.parse(await readFile(repositoryPath, 'utf8'));
}

async function readCurrent() {
  try { return await readJson(OUTPUT_PATH); }
  catch { return null; }
}

function semanticSnapshot(value) {
  if (Array.isArray(value)) return value.map(semanticSnapshot);
  if (!value || typeof value !== 'object') return value;
  const result = {};
  for (const [key, child] of Object.entries(value)) {
    if (key === 'generatedAt' || key === 'projectionDigest' || key === 'recordDigest' || key === 'recommendationDigest') continue;
    result[key] = semanticSnapshot(child);
  }
  return result;
}

export async function generateProjection({ catalog, provenanceSources, generatedAt }) {
  return buildAdvisoryProjection({ catalog, provenanceSources, generatedAt });
}

async function main() {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);
  const [catalog, provenanceSources, current] = await Promise.all([
    readJson(CATALOG_PATH),
    discoverProvenanceSources('.'),
    readCurrent()
  ]);
  const checkTimestamp = current?.generatedAt ?? '2000-01-01T00:00:00.000Z';
  const expected = await generateProjection({ catalog, provenanceSources, generatedAt: checkTimestamp });

  if (mode === '--print') {
    process.stdout.write(stableJson(expected));
    return;
  }
  if (mode === '--check') {
    if (!current || stableJson(current) !== stableJson(expected)) {
      process.stderr.write('AI post-processing advisory projection drift detected. Run: node .github/scripts/generate-ai-post-processing-advisory-projection.mjs --write\n');
      process.exitCode = 1;
      return;
    }
    process.stdout.write(`AI advisory projection aligned: ${expected.summary.totalSessions} sessions; ${expected.summary.provenanceMatched} provenance matched; ${expected.summary.processingHistoryFailClosed} processing-history gates fail-closed.\n`);
    return;
  }

  if (current && canonicalJson(semanticSnapshot(current)) === canonicalJson(semanticSnapshot(expected))) {
    process.stdout.write('AI post-processing advisory projection already aligned; no write required.\n');
    return;
  }
  const generated = await generateProjection({ catalog, provenanceSources, generatedAt: new Date().toISOString() });
  await writeFile(OUTPUT_PATH, stableJson(generated), 'utf8');
  process.stdout.write(`Generated ${OUTPUT_PATH}: ${generated.summary.totalSessions} sessions; ${generated.summary.provenanceMatched} provenance matched; ${generated.summary.processingHistoryFailClosed} processing-history gates fail-closed.\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
