import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
import { buildRealEvidenceValidation } from './scientific-data-quality-real-evidence-validation.mjs';

export const OUTPUT_PATH = 'docs/data/scientific-data-quality-f5-validation.json';
const readJson = async path => JSON.parse(await readFile(path, 'utf8'));
const stable = value => `${JSON.stringify(value, null, 2)}\n`;

async function main() {
  const mode = process.argv[2] || '--check';
  if (!['--check', '--write', '--print'].includes(mode)) throw new Error(`Unsupported mode: ${mode}`);
  const [catalog, projection] = await Promise.all([
    readJson('docs/data/scientific-session-catalog.json'),
    readJson('docs/data/scientific-data-quality-projection.json')
  ]);
  const expected = buildRealEvidenceValidation(catalog, projection);
  if (mode === '--print') return process.stdout.write(stable(expected));
  if (mode === '--write') {
    await writeFile(OUTPUT_PATH, stable(expected), 'utf8');
    return process.stdout.write(`Generated ${OUTPUT_PATH}: ${expected.decision.productionReadiness}; ${expected.summary.failedCriteria}/${expected.summary.totalCriteria} readiness criteria failed.\n`);
  }
  const current = await readJson(OUTPUT_PATH).catch(() => null);
  if (!current || stable(current) !== stable(expected)) {
    process.stderr.write('F5 real-evidence validation drift detected. Run generator with --write.\n');
    process.exitCode = 1;
    return;
  }
  process.stdout.write(`F5 validation aligned: ${expected.decision.productionReadiness}; capability ${expected.decision.capabilityAcceptance}.\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main().catch(error => { console.error(error.message); process.exitCode = 1; });
