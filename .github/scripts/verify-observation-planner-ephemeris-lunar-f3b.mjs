import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import { validateF3BContractFixture } from './observation-planner-ephemeris-lunar-f3b-contract.mjs';

const paths = {
  method: 'schemas/observation-planner-ephemeris-lunar-method-profile-f3b.schema.json',
  request: 'schemas/observation-planner-ephemeris-lunar-request-f3b.schema.json',
  evidence: 'schemas/observation-planner-ephemeris-lunar-evidence-f3b.schema.json',
  fixture: 'docs/data/observation-planner-ephemeris-lunar-f3b-fixture.json'
};
const expectedRawDigests = {
  method: '6720d501917ba5fec17b4536d923cfffefd2f4d1ddbe2b9fd443feaa10248419',
  request: '08cac6ae2877d85c1f9d33a52418086f032c7e88737807bbc332b7eaf3ee9f18',
  evidence: '5d15a79ee19b68c02d98d9e53a0dcfdecf1fb6ebc44a7d44b5822b5d2f5134a2',
  fixture: 'e2d49122741275b086bbf2e25a5701f0403b4c36999e28847d79146ef26eaca9'
};

const documents = {};
for (const [name, path] of Object.entries(paths)) {
  const bytes = fs.readFileSync(path);
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), expectedRawDigests[name], `${name} raw digest mismatch`);
  documents[name] = JSON.parse(bytes.toString('utf8'));
}

for (const schema of [documents.method, documents.request, documents.evidence]) {
  assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
  assert.equal(schema.type, 'object');
  assert.equal(schema.additionalProperties, false);
  assert.equal(schema.properties.schemaVersion.const, '1.0');
}
assert.equal(documents.method.properties.contractType.const, 'BKL031_F3B_METHOD_PROFILE');
assert.equal(documents.method.$defs.authority.properties.runtimeAuthority.const, 'NONE');
assert.equal(documents.method.$defs.authority.properties.executionAuthority.const, 'NONE');
assert.equal(documents.method.$defs.authority.properties.safetyAuthority.const, 'LOCAL_PHYSICAL_INTERLOCKS');
assert.equal(documents.method.$defs.networkPolicy.properties.externalReference.const, 'DENY');
assert.equal(documents.method.$defs.outputSemantics.properties.refractionModel.const, 'AIRLESS');
assert.equal(documents.request.properties.contractType.const, 'BKL031_F3B_EPHEMERIS_LUNAR_REQUEST');
assert.equal(documents.request.properties.evaluationTimesUtc.maxItems, 8);
assert.equal(documents.request.$defs.site.properties.classification.const, 'SYNTHETIC_PUBLIC');
assert.equal(documents.evidence.properties.contractType.const, 'BKL031_F3B_EPHEMERIS_LUNAR_EVIDENCE');
assert.equal(documents.evidence.properties.facts.maxItems, 72);

validateF3BContractFixture(documents.fixture);
assert.equal(documents.fixture.boundaries.f3cAdapterImplemented, false);
assert.equal(documents.fixture.boundaries.runtimeActivated, false);
assert.equal(documents.fixture.boundaries.protectedSiteUsed, false);
assert.equal(documents.fixture.boundaries.externalReferenceCalls, 0);
assert.equal(documents.fixture.boundaries.forecastImplemented, false);
assert.equal(documents.fixture.boundaries.rankingImplemented, false);
assert.equal(documents.fixture.boundaries.readinessImplemented, false);
assert.equal(documents.fixture.boundaries.commandAuthority, 'NONE');
assert.equal(documents.fixture.boundaries.safetyAuthority, 'LOCAL_PHYSICAL_INTERLOCKS');

const architecture = fs.readFileSync('docs/architecture/scientific-assets/BKL-031-F3-B-Ephemeris-Lunar-Machine-Readable-Contracts-and-Validator.md', 'utf8');
const acceptance = fs.readFileSync('docs/project/BKL-031-F3-B-CONTRACTS-AND-VALIDATOR-ACCEPTANCE-2026-09-17.md', 'utf8');
const backlog = fs.readFileSync('docs/project/BACKLOG.md', 'utf8');
const roadmap = JSON.parse(fs.readFileSync('.github/roadmap/roadmap-source.json', 'utf8'));
for (const fragment of ['**IMPLEMENTED — ACCEPTANCE REVIEW PENDING**', documents.fixture.contractDigest, '34 tests', 'F3-C may be prepared only after exact-head review']) assert.ok(architecture.includes(fragment), `F3-B architecture record missing: ${fragment}`);
for (const fragment of ['**ACCEPTANCE CANDIDATE — POST-MERGE VERIFICATION PENDING**', '34/34 passing locally', 'S10 remains `UNAVAILABLE`']) assert.ok(acceptance.includes(fragment), `F3-B acceptance record missing: ${fragment}`);
assert.ok(backlog.includes('F3-B source-neutral method/request/evidence schemas') && backlog.includes('34/34 local tests'), 'BKL-031 backlog does not identify the F3-B candidate.');
assert.equal(roadmap.currentPackage, 'BKL-031');
assert.equal(roadmap.nextMilestone, 'BKL-031 F3-B exact-head acceptance and F3-C handoff');
assert.ok(roadmap.projectStatus.includes('exact-head acceptance pending') && roadmap.projectStatus.includes('S10 runtime unavailable'), 'roadmap F3-B status/boundary mismatch.');

console.log(`BKL-031 F3-B contracts verified: three source-neutral schemas, ${documents.fixture.request.evaluationTimesUtc.length} bounded instants, ${documents.fixture.evidence.facts.length} normalized facts, digest ${documents.fixture.contractDigest}.`);
