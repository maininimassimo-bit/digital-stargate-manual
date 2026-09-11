import assert from 'node:assert/strict';
import fs from 'node:fs';
import { buildRealEvidenceValidation } from './scientific-data-quality-real-evidence-validation.mjs';
import { validateRealEvidenceFreshness } from '../../docs/javascripts/scientific-data-quality-core.mjs';

const read = path => JSON.parse(fs.readFileSync(path, 'utf8'));
const schema = read('docs/contracts/scientific-data-quality-f5-validation.schema.json');
const catalog = read('docs/data/scientific-session-catalog.json');
const projection = read('docs/data/scientific-data-quality-projection.json');
const validation = read('docs/data/scientific-data-quality-f5-validation.json');
const workflow = fs.readFileSync('.github/workflows/analyze-session-automatic.yml', 'utf8');

assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.properties.validationType.const, 'SCIENTIFIC_DATA_QUALITY_REAL_EVIDENCE_VALIDATION');
assert.equal(schema.$defs.decision.properties.productionReadiness.const, 'NOT_READY_FOR_PRODUCTION');
assert.equal(schema.$defs.authority.properties.productionUseAuthorized.const, false);
assert.deepEqual(validation, buildRealEvidenceValidation(catalog, projection));
await validateRealEvidenceFreshness(validation, projection, catalog);
assert.equal(validation.summary.passedCriteria + validation.summary.failedCriteria, validation.summary.totalCriteria);
assert.equal(validation.decision.productionProfileAuthorized, false);
assert.equal(validation.decision.productionUseAuthorized, false);
assert.ok(validation.decision.reasonCodes.includes('REFERENCE_GROUND_TRUTH'));
assert.ok(validation.biasDisclosure.includes('AVAILABLE_ASSESSMENTS_ARE_ONLY_FOR_M27_IN_THE_CURRENT_COHORT'));

for (const required of [
  'node .github/scripts/generate-scientific-data-quality-f5-validation.mjs --write',
  'node .github/scripts/generate-scientific-data-quality-f5-validation.mjs --check',
  'docs/data/scientific-data-quality-f5-validation.json'
]) assert.ok(workflow.includes(required), `Automatic session workflow is missing: ${required}`);

console.log(`BKL-041 F5 validation verified: ${validation.cohort.sessionCount} real sessions; ${validation.summary.failedCriteria}/${validation.summary.totalCriteria} readiness gates failed; production use remains unauthorized.`);
