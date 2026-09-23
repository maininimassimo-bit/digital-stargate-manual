import fs from 'node:fs';
import assert from 'node:assert/strict';

const schema = JSON.parse(fs.readFileSync('schemas/bkl042-f2-advisory-response.schema.json', 'utf8'));
const fixture = JSON.parse(fs.readFileSync('docs/data/bkl042-f2-advisory-response-fixture.json', 'utf8'));
assert.equal(schema.$id.endsWith('/schemas/bkl042-f2-advisory-response.schema.json'), true);
assert.equal(fixture.contractType, 'BKL042_F2_ADVISORY_RESPONSE_FIXTURE');
assert.equal(fixture.fixtureMode, 'BOUNDED_SYNTHETIC_FIXTURE');
assert.equal(fixture.cases.length, 2);
assert.equal(fixture.authority.consumerMode, 'READ_ONLY');
assert.equal(fixture.authority.advisoryOnly, true);
assert.equal(fixture.authority.citationRequired, true);
for (const key of ['actionAuthority', 'commandAuthority', 'executionAuthority', 'safetyAuthority']) assert.equal(fixture.authority[key], 'NONE');
assert.equal(fixture.authority.automaticAcceptance, false);
for (const item of fixture.cases) {
  assert.ok(item.sources.length > 0);
  assert.ok(item.response.evidenceRefs.every(ref => item.sources.some(source => source.sourceId === ref)));
  assert.ok(item.response.limitations.length > 0);
  assert.equal(item.humanDisposition.executionState, 'NOT_OBSERVED');
  assert.equal(item.humanDisposition.actionAuthority, 'NONE');
  if (item.response.state === 'INSUFFICIENT_EVIDENCE') {
    assert.ok(item.sources.some(source => ['UNAVAILABLE', 'UNKNOWN', 'STALE', 'CONFLICT'].includes(source.lifecycle)));
    assert.equal(item.response.recommendations.length, 0);
  }
}
console.log(`BKL-042-F2 advisory response PASS: cases=${fixture.cases.length}; citationRequired=true; failClosed=INSUFFICIENT_EVIDENCE; action=NONE; command=NONE; safety=NONE`);
