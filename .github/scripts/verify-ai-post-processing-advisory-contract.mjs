import assert from 'node:assert/strict';
import fs from 'node:fs';
import { validateAdvisoryContractFixture } from './ai-post-processing-advisory-contract.mjs';

const schemaPath = 'docs/contracts/ai-post-processing-assistant-f2.schema.json';
const fixturePath = 'docs/data/ai-post-processing-assistant-f2-fixture.json';
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));

assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.additionalProperties, false);
assert.equal(schema.properties.schemaVersion.const, '1.0');
assert.equal(schema.properties.contractType.const, 'AI_POST_PROCESSING_ASSISTANT_F2_FIXTURE');
assert.equal(schema.properties.identityMethod.const, 'BKL046-F2-CANONICAL-JSON-SHA256-1');
assert.equal(schema.$defs.recommendation.properties.semanticType.const, 'recommendation');
assert.equal(schema.$defs.confidence.properties.state.const, 'UNAVAILABLE_F2');
assert.equal(schema.$defs.humanDecisionReceipt.properties.executionState.const, 'NOT_OBSERVED');
assert.equal(schema.$defs.humanDecisionReceipt.properties.actionAuthority.const, 'NONE');
assert.equal(schema.$defs.authority.properties.consumerMode.const, 'READ_ONLY');
assert.equal(schema.$defs.authority.properties.advisoryOnly.const, true);
assert.equal(schema.$defs.authority.properties.acceptanceAuthority.const, 'HUMAN_ONLY');
assert.equal(schema.$defs.authority.properties.actionAuthority.const, 'NONE');
assert.equal(schema.$defs.authority.properties.executionAuthority.const, 'NONE');
assert.equal(schema.$defs.authority.properties.pixInsightApplyAuthorized.const, false);
assert.equal(schema.$defs.authority.properties.automaticAcceptanceAuthorized.const, false);
assert.equal(schema.$defs.authority.properties.safetyAuthority.const, 'LOCAL_PHYSICAL_INTERLOCKS');

validateAdvisoryContractFixture(fixture);
console.log(`BKL-046 F2 contract verified: ${fixture.sourceBindings.length} source bindings, ${fixture.recommendations.length} recommendations, ${fixture.humanDecisionReceipts.length} human decision receipts, digest ${fixture.artifactDigest}.`);
