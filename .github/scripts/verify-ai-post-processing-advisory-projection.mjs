import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
import { validateAdvisoryProjection } from './ai-post-processing-advisory-projection.mjs';

const OUTPUT_PATH = 'docs/data/ai-post-processing-advisory-projection.json';
const WORKFLOW_PATH = '.github/workflows/analyze-session-automatic.yml';
const GENERATOR_COMMAND = 'node .github/scripts/generate-ai-post-processing-advisory-projection.mjs';

const assert = (condition, message) => { if (!condition) throw new Error(message); };

export function verifyWorkflowIntegration(workflow) {
  const writes = workflow.match(new RegExp(`${GENERATOR_COMMAND.replaceAll('.', '\\.') } --write`, 'g')) ?? [];
  const checks = workflow.match(new RegExp(`${GENERATOR_COMMAND.replaceAll('.', '\\.') } --check`, 'g')) ?? [];
  assert(writes.length >= 2, 'F4 generator --write must exist in first and retry generation paths.');
  assert(checks.length >= 2, 'F4 generator --check must exist in first and retry generation paths.');
  assert(workflow.includes(OUTPUT_PATH), 'F4 persisted projection must be included in governed_paths.');
  assert(workflow.includes('git reset --hard origin/main'), 'Retry path must regenerate after reset to origin/main.');
  return true;
}

async function main() {
  const [projectionText, workflow] = await Promise.all([
    readFile(OUTPUT_PATH, 'utf8'),
    readFile(WORKFLOW_PATH, 'utf8')
  ]);
  validateAdvisoryProjection(JSON.parse(projectionText));
  verifyWorkflowIntegration(workflow);
  process.stdout.write('BKL-046 F4-B projection and atomic workflow integration verified.\n');
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
