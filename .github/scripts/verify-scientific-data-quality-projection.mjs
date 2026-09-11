import assert from 'node:assert/strict';
import fs from 'node:fs';
import { buildScientificDataQualityProjection } from './scientific-data-quality-projection.mjs';
import { validateProjectionFreshness } from '../../docs/javascripts/scientific-data-quality-core.mjs';

const schema = JSON.parse(fs.readFileSync('docs/contracts/scientific-data-quality-f4.schema.json', 'utf8'));
const catalog = JSON.parse(fs.readFileSync('docs/data/scientific-session-catalog.json', 'utf8'));
const fixture = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f3-fixture.json', 'utf8'));
const projection = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-projection.json', 'utf8'));
const workflow = fs.readFileSync('.github/workflows/analyze-session-automatic.yml', 'utf8');

assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.properties.projectionType.const, 'SCIENTIFIC_DATA_QUALITY_PROJECTION');
assert.equal(schema.properties.projectionState.const, 'EXPERIMENTAL_NOT_ACCEPTED');
assert.equal(schema.$defs.authority.properties.productionUseAuthorized.const, false);
assert.equal(schema.$defs.authority.properties.acceptanceAuthority.const, false);
assert.equal(schema.$defs.authority.properties.actionAuthority.const, 'NONE');
assert.equal(schema.$defs.authority.properties.safetyAuthority.const, 'LOCAL_PHYSICAL_INTERLOCKS');

const expected = buildScientificDataQualityProjection(catalog, fixture.profile, { generatedAt: projection.generatedAt });
assert.deepEqual(projection, expected, 'Persisted F4 projection has drifted from catalog/profile inputs.');
await validateProjectionFreshness(projection, catalog);
assert.equal(projection.summary.totalSessions, catalog.sessions.length);
assert.equal(projection.summary.totalSessions, projection.summary.availableAssessments + projection.summary.unavailableAssessments + projection.summary.invalidAssessments);

for (const required of [
  'node .github/scripts/generate-scientific-data-quality-projection.mjs --write',
  'node .github/scripts/generate-scientific-data-quality-projection.mjs --check',
  'docs/data/scientific-data-quality-projection.json'
]) assert.ok(workflow.includes(required), `Automatic session workflow is missing: ${required}`);

console.log(`BKL-041 F4 projection verified: ${projection.summary.totalSessions} sessions; ${projection.summary.availableAssessments} experimental available, ${projection.summary.unavailableAssessments} unavailable, ${projection.summary.invalidAssessments} invalid; freshness SHA-256 matched.`);
