import assert from 'node:assert/strict';
import fs from 'node:fs';
import { buildScientificDataQualityAssessment, contentDigest, validateScoringProfile } from './scientific-data-quality-scoring.mjs';

const schema = JSON.parse(fs.readFileSync('docs/contracts/scientific-data-quality-f3.schema.json', 'utf8'));
const fixture = JSON.parse(fs.readFileSync('docs/data/scientific-data-quality-f3-fixture.json', 'utf8'));

assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.properties.schemaVersion.const, '1.0');
assert.equal(schema.properties.fixtureType.const, 'SCIENTIFIC_DATA_QUALITY_F3_KNOWN_ANSWER');
assert.equal(schema.properties.fixtureMode.const, 'BOUNDED_SYNTHETIC_FIXTURE');
assert.equal(schema.$defs.profile.properties.profileState.const, 'SYNTHETIC_DEMONSTRATOR_F3');
assert.equal(schema.$defs.authority.properties.consumerMode.const, 'READ_ONLY');
assert.equal(schema.$defs.authority.properties.acceptanceAuthority.const, false);
assert.equal(schema.$defs.authority.properties.actionAuthority.const, 'NONE');
assert.equal(schema.$defs.authority.properties.safetyAuthority.const, 'LOCAL_PHYSICAL_INTERLOCKS');

const fixturePreimage = structuredClone(fixture);
delete fixturePreimage.fixtureDigest;
assert.equal(fixture.fixtureDigest, contentDigest(fixturePreimage), 'fixtureDigest mismatch');
validateScoringProfile(fixture.profile);
const result = buildScientificDataQualityAssessment(fixture);
assert.equal(result.assessmentState, fixture.expected.assessmentState);
assert.equal(result.score?.value ?? null, fixture.expected.scoreValue);
assert.equal(result.confidence?.value ?? null, fixture.expected.confidenceValue);
assert.equal(result.evidenceCoverage, fixture.expected.evidenceCoverage);
assert.equal(result.assessmentDigest, fixture.expected.assessmentDigest);

console.log(`BKL-041 F3 scoring verified: ${result.decomposition.length} required dimensions, score ${result.score.value}, confidence ${result.confidence.value}, digest ${result.assessmentDigest}.`);
