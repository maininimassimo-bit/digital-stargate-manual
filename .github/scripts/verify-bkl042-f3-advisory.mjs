import fs from 'node:fs';
import assert from 'node:assert/strict';

const output = JSON.parse(fs.readFileSync('docs/data/bkl042-f3-deterministic-advisory-output.json', 'utf8'));
const schema = JSON.parse(fs.readFileSync('schemas/bkl042-f3-deterministic-advisory.schema.json', 'utf8'));
assert.equal(schema.$id.endsWith('/schemas/bkl042-f3-deterministic-advisory.schema.json'), true);
assert.equal(output.contractType, 'BKL042_F3_DETERMINISTIC_ADVISORY_OUTPUT');
assert.equal(output.demonstratorMode, 'BOUNDED_SYNTHETIC_READ_ONLY');
assert.equal(output.producer, 'DSG.DeterministicObservatoryAdvisory');
assert.equal(output.methodId, 'BKL042-F3-CLOSED-RULES-1');
assert.equal(output.responses.length, 2);
assert.equal(output.ruleEvaluations.length, 4);
assert.deepEqual(output.responses.map(item => item.state), ['ANSWERED', 'INSUFFICIENT_EVIDENCE']);
assert.equal(output.responses[1].recommendations.length, 0);
for (const key of ['actionAuthority', 'commandAuthority', 'executionAuthority', 'safetyAuthority']) assert.equal(output.authority[key], 'NONE');
assert.equal(output.authority.advisoryOnly, true);
assert.equal(output.authority.automaticAcceptance, false);
console.log(`BKL-042-F3 advisory PASS: cases=${output.responses.length}; method=${output.methodId}; failClosed=1; action=NONE; command=NONE; safety=NONE`);
