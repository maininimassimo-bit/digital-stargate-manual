import { access, readFile } from 'node:fs/promises';
import path from 'node:path';

const fixturePath = 'docs/data/bkl033-digital-twin-fixture.json';
const schemaPath = 'schemas/bkl033-digital-twin-contract.schema.json';
const contractPath = 'docs/architecture/packages/BKL-033-Observatory-Digital-Twin.md';
const fail = (message) => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const fixture = JSON.parse(await readFile(fixturePath, 'utf8'));
const schema = JSON.parse(await readFile(schemaPath, 'utf8'));
const contract = await readFile(contractPath, 'utf8');

assert(schema.$id.includes('bkl033-digital-twin-contract'), 'schema must identify BKL-033');
assert(fixture.schemaVersion === '1.0' && fixture.authority === 'projection', 'projection/version boundary mismatch');
assert(fixture.commandAuthority === 'NONE' && fixture.safetyAuthority === 'NONE', 'authority boundary drift');
assert(fixture.nodes.length === 4 && fixture.dependencies.length === 4, 'fixture must remain bounded to four nodes/dependencies');
const nodes = new Set(fixture.nodes.map((node) => node.id));
assert(fixture.nodes.some((node) => node.state === 'observed' && node.freshness === 'current'), 'current observed evidence missing');
assert(fixture.dependencies.some((dependency) => dependency.state === 'unknown'), 'unknown dependency state missing');
for (const node of fixture.nodes) {
  assert(node.sourceRefs.length > 0, `node source missing: ${node.id}`);
  for (const ref of node.sourceRefs) assert(ref.startsWith('src:'), `unsafe node source ref: ${ref}`);
}
for (const dependency of fixture.dependencies) {
  assert(nodes.has(dependency.from) && nodes.has(dependency.to), `dangling dependency: ${dependency.id}`);
  assert(dependency.evidenceRefs.length > 0, `dependency evidence missing: ${dependency.id}`);
}
for (const forbidden of ['command', 'remediation', 'readiness', 'Safety Authority', 'scheduler']) assert(contract.includes(forbidden), `boundary marker missing: ${forbidden}`);
for (const file of [fixturePath, schemaPath, contractPath]) { assert(!path.isAbsolute(file) && !file.includes('..'), `unsafe repository path: ${file}`); await access(file); }
console.log(`BKL-033 digital twin contract PASS: nodes=${fixture.nodes.length}; dependencies=${fixture.dependencies.length}; authority=projection; command=NONE; safety=NONE`);
