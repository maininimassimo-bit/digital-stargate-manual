import { access, readFile } from 'node:fs/promises';
import path from 'node:path';

const schemaPath = 'schemas/ap015-knowledge-semantic-contract.schema.json';
const fixturePath = 'docs/data/ap015-knowledge-semantic-fixture.json';
const contractPath = 'docs/architecture/knowledge/AP015-CAP40-Semantic-Contract.md';
const fail = (message) => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const json = async (file) => JSON.parse(await readFile(file, 'utf8'));
const schema = await json(schemaPath);
const fixture = await json(fixturePath);
const contract = await readFile(contractPath, 'utf8');

assert(schema.$id.includes('ap015-knowledge-semantic-contract'), 'schema id must identify AP-015');
assert(schema.properties.authority.const === 'projection', 'semantic contract must remain a projection');
assert(fixture.schemaVersion === '1.0' && fixture.authority === 'projection', 'fixture authority/version mismatch');
assert(fixture.entities.length === 3, 'fixture must remain bounded to three entities');
assert(fixture.relations.length === 2, 'fixture relation count drifted');
assert(fixture.claims.length === 1 && fixture.citations.length === 2, 'fixture claim/citation count drifted');
assert(fixture.provenance.length === 1 && fixture.conflicts.length === 1 && fixture.unknowns.length === 1, 'fixture must demonstrate all semantic classes');
const ids = new Set(fixture.entities.map((item) => item.id));
for (const relation of fixture.relations) {
  assert(ids.has(relation.from) && ids.has(relation.to), `dangling relation: ${relation.id}`);
  assert(relation.citationRefs.length > 0, `relation citation missing: ${relation.id}`);
}
const citationIds = new Set(fixture.citations.map((item) => item.id));
for (const citation of fixture.citations) {
  assert(!path.isAbsolute(citation.locator) && !citation.locator.includes('..'), `unsafe citation locator: ${citation.id}`);
  await access(citation.locator);
}
for (const item of [...fixture.entities, ...fixture.relations, ...fixture.claims, ...fixture.provenance, ...fixture.conflicts, ...fixture.unknowns]) {
  for (const citationRef of item.citationRefs ?? []) assert(citationIds.has(citationRef), `unresolved citation: ${citationRef}`);
}
for (const forbidden of ['command', 'remediation', 'Safety Authority', 'provider', 'runtime']) assert(contract.includes(forbidden), `contract boundary marker missing: ${forbidden}`);
assert(contract.includes('conflict') && contract.includes('unknown') && contract.includes('citation'), 'semantic contract classes missing');
console.log(`AP-015 semantic contract PASS: entities=${fixture.entities.length}; relations=${fixture.relations.length}; citations=${fixture.citations.length}; authority=projection; runtime=none`);
