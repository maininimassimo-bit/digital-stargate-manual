import fs from 'node:fs';
import path from 'node:path';
import { validatePixInsightWorkflowProvenance } from './pixinsight-workflow-provenance.mjs';

const file = process.argv[2];
if (!file) {
  console.error('Usage: node .github/scripts/validate-pixinsight-workflow-provenance-file.mjs <captured-sidecar.json>');
  process.exit(2);
}

const resolved = path.resolve(file);
let parsed;
try {
  parsed = JSON.parse(fs.readFileSync(resolved, 'utf8'));
} catch (error) {
  console.error(`Cannot read/parse ${resolved}: ${error.message}`);
  process.exit(1);
}

try {
  const result = validatePixInsightWorkflowProvenance(parsed);
  console.log(`VALID PixInsight workflow provenance sidecar`);
  console.log(`file=${resolved}`);
  console.log(`sidecarId=${parsed.sidecarId}`);
  console.log(`capture=${parsed.capture.completeness}`);
  console.log(`observedSteps=${parsed.capture.observedStepCount ?? 0}`);
  console.log(`declaredSteps=${parsed.capture.declaredStepCount ?? 0}`);
  console.log(`digest=${result.digest}`);
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
