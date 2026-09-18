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
for (const fragment of ['**ACCEPTED — POST-MERGE VERIFIED**', documents.fixture.contractDigest, '34 tests', 'F3-C is promoted as the next bounded gate']) assert.ok(architecture.includes(fragment), `F3-B architecture record missing: ${fragment}`);
for (const fragment of ['**ACCEPTED — POST-MERGE VERIFIED**', '34/34 passing locally and in governed CI', 'S10 remains `UNAVAILABLE`', '35192376713', '35192376685']) assert.ok(acceptance.includes(fragment), `F3-B acceptance record missing: ${fragment}`);
assert.ok(backlog.includes('F3-C Accepted/Post-Merge Verified') && backlog.includes('F4-A/ADR-011') && backlog.includes('F4-D metadata-only projection and portal Accepted/Post-Merge Verified'), 'BKL-031 backlog does not preserve the accepted successor chain after F3-B.');
assert.equal(roadmap.currentPackage, 'BKL-036');
assert.equal(roadmap.nextMilestone, 'BKL-036 Observatory Health Score');
assert.ok(roadmap.projectStatus.includes('BKL-031 and BKL-032 are CLOSED / ACCEPTED / POST-MERGE VERIFIED') && roadmap.projectStatus.includes('S10 production runtime unavailable') && roadmap.projectStatus.includes('live source/transport and public runtime GO remain separately gated'), 'roadmap successor status/boundary mismatch after F3-B.');
assert.ok(roadmap.milestones.some((item) => item.id === 'M-BKL031-F3-B-ACCEPTANCE'), 'roadmap F3-B acceptance milestone missing.');
assert.ok(roadmap.milestones.some((item) => item.id === 'M-BKL031-F4-D-ACCEPTANCE'), 'roadmap F4-D acceptance milestone missing.');

console.log(`BKL-031 F3-B contracts verified: three source-neutral schemas, ${documents.fixture.request.evaluationTimesUtc.length} bounded instants, ${documents.fixture.evidence.facts.length} normalized facts, digest ${documents.fixture.contractDigest}; F3-C/F4/F5/F6/F7 accepted; F8 current astronomy and explicit setup suitability next.`);
