import assert from 'node:assert/strict';
import fs from 'node:fs';
import {
  buildDeterministicAdvisoryDemonstration,
  validateDeterministicAdvisoryOutput
} from './ai-post-processing-advisory-demonstrator.mjs';

const schema = JSON.parse(fs.readFileSync('docs/contracts/ai-post-processing-assistant-f3.schema.json', 'utf8'));
const fixture = JSON.parse(fs.readFileSync('docs/data/ai-post-processing-assistant-f2-fixture.json', 'utf8'));
const expected = JSON.parse(fs.readFileSync('docs/data/ai-post-processing-assistant-f3-output.json', 'utf8'));

assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.additionalProperties, false);
assert.equal(schema.properties.schemaVersion.const, '1.0');
assert.equal(schema.properties.contractType.const, 'AI_POST_PROCESSING_ASSISTANT_F3_DEMONSTRATOR_OUTPUT');
assert.equal(schema.properties.demonstratorMode.const, 'BOUNDED_SYNTHETIC_READ_ONLY');
assert.equal(schema.properties.subject.$ref, 'ai-post-processing-assistant-f2.schema.json#/$defs/subject');
assert.equal(schema.properties.sourceBindings.items.$ref, 'ai-post-processing-assistant-f2.schema.json#/$defs/sourceBinding');
assert.equal(schema.properties.recommendations.items.$ref, 'ai-post-processing-assistant-f2.schema.json#/$defs/recommendation');
assert.equal(schema.properties.authority.$ref, 'ai-post-processing-assistant-f2.schema.json#/$defs/authority');
assert.equal(schema.properties.decisionState.const, 'NOT_PRESENT_PRE_DECISION');

assert.equal(validateDeterministicAdvisoryOutput(expected), true);
const generated = buildDeterministicAdvisoryDemonstration(fixture);
assert.deepEqual(generated, expected, 'F3 known-answer output is stale or non-deterministic.');
assert.equal(Object.hasOwn(generated, 'humanDecisionReceipts'), false);
assert(generated.recommendations.every((item) => item.aiDerived === false));
assert(generated.recommendations.every((item) => item.confidence.value === null));

console.log(`BKL-046 F3 demonstrator verified: ${generated.recommendations.length} F2-valid recommendations, ${generated.ruleEvaluations.length} rule evaluations, digest ${generated.artifactDigest}.`);
