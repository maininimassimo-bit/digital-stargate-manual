import fs from 'node:fs';
import assert from 'node:assert/strict';
const fixture = JSON.parse(fs.readFileSync('docs/data/bkl042-f6-read-only-chat-fixture.json', 'utf8'));
const schema = JSON.parse(fs.readFileSync('schemas/bkl042-f6-read-only-chat.schema.json', 'utf8'));
assert.equal(fixture.schemaVersion, schema.properties.schemaVersion.const);
assert.equal(fixture.contractType, schema.properties.contractType.const);
assert.equal(fixture.mode, schema.properties.mode.const);
assert.ok(fixture.responses.length >= 2);
assert.ok(fixture.responses.some(item => item.state === 'ANSWERED'));
assert.ok(fixture.responses.some(item => item.state === 'INSUFFICIENT_EVIDENCE'));
assert.equal(fixture.authority.consumerMode, 'READ_ONLY');
assert.equal(fixture.authority.advisoryOnly, true);
for (const key of ['actionAuthority', 'commandAuthority', 'executionAuthority', 'safetyAuthority']) assert.equal(fixture.authority[key], 'NONE');
assert.equal(fixture.authority.automaticAcceptanceAuthorized, false);
for (const response of fixture.responses) {
  assert.ok(response.citations.length > 0);
  assert.ok(response.limitations.length > 0);
}
const page = fs.readFileSync('docs/bkl042-chat/index.md', 'utf8');
const js = fs.readFileSync('docs/javascripts/bkl042-chat.js', 'utf8');
assert.ok(page.includes('data-bkl042-chat'));
assert.ok(js.includes('BOUNDED_DETERMINISTIC_READ_ONLY'));
assert.ok(page.includes('Nessuna azione'));
assert.ok(!js.includes('fetch('));
console.log('BKL-042-F6 chat PASS: bounded deterministic read-only contract, citations and fail-closed authority verified');
