import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
import {
  buildRealEvidenceEvaluation,
  canonicalJson,
  CATALOG_PATH,
  discoverExecutionEvidenceSources,
  discoverHumanDecisionSources,
  F4_PROJECTION_PATH
} from './ai-post-processing-advisory-real-evidence-evaluation.mjs';

export const OUTPUT_PATH = 'docs/data/ai-post-processing-advisory-f5-evaluation.json';

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
    if (key === 'generatedAt' || key === 'evaluationDigest') continue;
    result[key] = semanticSnapshot(child);
  }
  return result;
}

export async function generateEvaluation({
  catalog,
  f4Projection,
  humanDecisionSources = [],
  executionEvidenceSources = [],
  generatedAt
}) {
  return buildRealEvidenceEvaluation({
    catalog,
    f4Projection,
    humanDecisionSources,
    executionEvidenceSources,
    generatedAt
  });
}

async function main() {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);
  const [catalog, f4Projection, humanDecisionSources, executionEvidenceSources, current] = await Promise.all([
    readJson(CATALOG_PATH),
    readJson(F4_PROJECTION_PATH),
    discoverHumanDecisionSources('.'),
    discoverExecutionEvidenceSources('.'),
    readCurrent()
  ]);
  const checkTimestamp = current?.generatedAt ?? '2000-01-01T00:00:00.000Z';
  const expected = await generateEvaluation({
    catalog,
    f4Projection,
    humanDecisionSources,
    executionEvidenceSources,
    generatedAt: checkTimestamp
  });

  if (mode === '--print') {
    process.stdout.write(stableJson(expected));
    return;
  }

  if (mode === '--check') {
    if (!current || stableJson(current) !== stableJson(expected)) {
      process.stderr.write('BKL-046 F5 real-evidence evaluation drift detected. Run: node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --write\n');
      process.exitCode = 1;
      return;
    }
    process.stdout.write(`BKL-046 F5-A evaluation aligned: ${expected.summary.canonicalSessions} canonical sessions; ${expected.summary.provenanceEligible} provenance eligible; scientific state ${expected.outcomes.scientific.state}.\n`);
    return;
  }

  if (current && canonicalJson(semanticSnapshot(current)) === canonicalJson(semanticSnapshot(expected))) {
    process.stdout.write('BKL-046 F5-A evaluation already aligned; no write required.\n');
    return;
  }

  const generated = await generateEvaluation({
    catalog,
    f4Projection,
    humanDecisionSources,
    executionEvidenceSources,
    generatedAt: new Date().toISOString()
  });
  await writeFile(OUTPUT_PATH, stableJson(generated), 'utf8');
  process.stdout.write(`Generated ${OUTPUT_PATH}: ${generated.summary.canonicalSessions} canonical sessions; ${generated.summary.provenanceEligible} provenance eligible; scientific state ${generated.outcomes.scientific.state}.\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}

