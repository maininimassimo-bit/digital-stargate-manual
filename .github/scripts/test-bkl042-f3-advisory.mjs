import fs from 'node:fs';
import assert from 'node:assert/strict';

const output = JSON.parse(fs.readFileSync('docs/data/bkl042-f3-deterministic-advisory-output.json', 'utf8'));
const before = JSON.stringify(output);
assert.equal(output.responses[0].state, 'ANSWERED');
assert.equal(output.responses[1].state, 'INSUFFICIENT_EVIDENCE');
assert.equal(output.ruleEvaluations.filter(item => item.decision === 'FAIL_CLOSED').length, 1);
assert.equal(output.responses[1].sourceRefs.includes('SRC-BKL045-UNAVAILABLE'), true);
assert.equal(JSON.stringify(output), before);
console.log('BKL-042-F3 deterministic regression PASS: nominal and fail-closed cases stable');
