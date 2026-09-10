import assert from 'node:assert/strict';
import fs from 'node:fs';
import { validateQualityContractFixture } from './scientific-data-quality-contract.mjs';

const schemaPath = 'docs/contracts/scientific-data-quality-f2.schema.json';
const fixturePath = 'docs/data/scientific-data-quality-f2-fixture.json';
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));

assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.properties.schemaVersion.const, '1.0');
assert.equal(schema.properties.contractType.const, 'SCIENTIFIC_DATA_QUALITY_F2_FIXTURE');
assert.equal(schema.properties.identityMethod.const, 'BKL041-F2-CANONICAL-JSON-SHA256-1');
assert.equal(schema.$defs.authority.properties.consumerMode.const, 'READ_ONLY');
assert.equal(schema.$defs.authority.properties.acceptanceAuthority.const, false);
assert.equal(schema.$defs.authority.properties.actionAuthority.const, 'NONE');
assert.equal(schema.$defs.authority.properties.safetyAuthority.const, 'LOCAL_PHYSICAL_INTERLOCKS');
assert.equal(schema.$defs.assessmentProfile.properties.weightSetState.const, 'NOT_ASSIGNED_F2');
assert.equal(schema.$defs.assessmentProfile.properties.scoreState.const, 'NOT_IMPLEMENTED_F2');
assert.equal(schema.$defs.dimensionAssessment.properties.normalizationState.const, 'NOT_IMPLEMENTED_F2');
assert.equal(schema.$defs.dimensionAssessment.properties.contributionState.const, 'NOT_COMPUTED_F2');

validateQualityContractFixture(fixture);
console.log(`BKL-041 F2 contract verified: ${fixture.qualityEvidence.length} evidence records, ${fixture.dimensionAssessments.length} dimension assessments, digest ${fixture.artifactDigest}.`);

