import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { reseal } from './observation-planner-ephemeris-lunar-f3b-contract.mjs';
import { buildF3CProjection, sealF3CProjection, validateF3CProjection } from './observation-planner-ephemeris-lunar-f3c-adapter.mjs';
import { validateObservationPlannerProjection } from '../../docs/javascripts/observation-planner-core.mjs';

const fixture = JSON.parse(fs.readFileSync('docs/data/observation-planner-ephemeris-lunar-f3b-fixture.json', 'utf8'));
const generated = JSON.parse(fs.readFileSync('docs/data/observation-planner-ephemeris-lunar-f3c-projection.json', 'utf8'));
const fresh = () => buildF3CProjection(structuredClone(fixture));
const mutate = (change, { seal = true } = {}) => {
  const projection = fresh();
  change(projection);
  if (seal) sealF3CProjection(projection);
  return projection;
};

test('adapter output is deterministic', () => {
  assert.deepEqual(fresh(), fresh());
});

test('generated projection validates against accepted F3-B evidence', () => {
  assert.equal(validateF3CProjection(structuredClone(generated), structuredClone(fixture)), true);
});

test('adapter rejects an invalid or runtime-enabled F3-B source', () => {
  const source = structuredClone(fixture);
  source.boundaries.runtimeActivated = true;
  reseal(source, 'contractDigest');
  assert.throws(() => buildF3CProjection(source), /runtimeActivated must remain false/);
});

test('unknown root properties fail closed', () => {
  const projection = mutate(value => { value.providerPayload = {}; });
  assert.throws(() => validateF3CProjection(projection, fixture), /providerPayload is not allowed/);
});

test('projection type and version are exact', () => {
  for (const [field, value] of [['schemaVersion', '2.0'], ['projectionType', 'OTHER']]) {
    const projection = mutate(item => { item[field] = value; });
    assert.throws(() => validateF3CProjection(projection, fixture), /identity mismatch/);
  }
});

test('projection identifier is bounded and deterministic', () => {
  const malformed = mutate(value => { value.projectionId = 'F3C-LATEST'; });
  assert.throws(() => validateF3CProjection(malformed, fixture), /projectionId is invalid/);
  const switched = mutate(value => { value.projectionId = 'BKL031-F3C-' + 'A'.repeat(24); });
  assert.throws(() => validateF3CProjection(switched, fixture), /projectionId is not deterministic/);
});

test('generation instant binds exact evidence', () => {
  const projection = mutate(value => { value.generatedAtUtc = '2026-09-17T07:00:02Z'; });
  assert.throws(() => validateF3CProjection(projection, fixture), /generation instant does not bind/);
});

test('environment and authority remain TEST/NONE', () => {
  for (const [field, value] of [['environment', 'PRODUCTION'], ['authority', 'PLANNING']]) {
    const projection = mutate(item => { item[field] = value; });
    assert.throws(() => validateF3CProjection(projection, fixture), /must remain TEST\/NONE/);
  }
});

test('source and context references bind the accepted fixture', () => {
  for (const field of ['sourceContractRef', 'contextRef']) {
    const projection = mutate(value => { value[field] = 'OTHER'; });
    assert.throws(() => validateF3CProjection(projection, fixture), /source\/context binding mismatch/);
  }
});

test('public site reference cannot be switched', () => {
  const projection = mutate(value => { value.sitePublicEvidenceRef = 'OTHER-PUBLIC-SITE'; });
  assert.throws(() => validateF3CProjection(projection, fixture), /public site reference mismatch/);
});

test('setup and evidence availability states cannot drift', () => {
  for (const [field, value] of [['setupAvailabilityState', 'AVAILABLE'], ['evidenceAvailabilityState', 'STALE']]) {
    const projection = mutate(item => { item[field] = value; });
    assert.throws(() => validateF3CProjection(projection, fixture), /availability state mismatch/);
  }
});

test('method profile and implementation identity cannot drift', () => {
  for (const [field, value] of [['profileRef', 'OTHER'], ['methodId', 'OTHER'], ['methodVersion', 'latest']]) {
    const projection = mutate(item => { item.method[field] = value; });
    assert.throws(() => validateF3CProjection(projection, fixture), /method identity mismatch/);
  }
});

test('adapter identity is exact', () => {
  for (const [field, value] of [['adapterId', 'FALLBACK'], ['adapterVersion', 'latest']]) {
    const projection = mutate(item => { item.method[field] = value; });
    assert.throws(() => validateF3CProjection(projection, fixture), /adapter identity mismatch/);
  }
});

test('output frame and refraction remain accepted semantics', () => {
  for (const [field, value] of [['outputFrame', 'GEOCENTRIC'], ['refractionModel', 'STANDARD']]) {
    const projection = mutate(item => { item.method[field] = value; });
    assert.throws(() => validateF3CProjection(projection, fixture), /output semantics mismatch/);
  }
});

test('validity is half-open and bound to evidence', () => {
  const projection = mutate(value => { value.validity.toUtc = value.validity.fromUtc; });
  assert.throws(() => validateF3CProjection(projection, fixture), /validity mismatch/);
});

test('facts remain bounded', () => {
  const empty = mutate(value => { value.facts = []; });
  assert.throws(() => validateF3CProjection(empty, fixture), /outside bounds/);
  const tooMany = mutate(value => { value.facts = Array.from({ length: 73 }, () => structuredClone(value.facts[0])); });
  assert.throws(() => validateF3CProjection(tooMany, fixture), /outside bounds/);
});

test('fact shape is closed', () => {
  const projection = mutate(value => { value.facts[0].providerNote = 'hidden'; });
  assert.throws(() => validateF3CProjection(projection, fixture), /providerNote is not allowed/);
});

test('facts cannot be altered or reordered', () => {
  const altered = mutate(value => { value.facts[0].numericValue = 12; });
  assert.throws(() => validateF3CProjection(altered, fixture), /facts differ/);
  const reordered = mutate(value => { value.facts.reverse(); });
  assert.throws(() => validateF3CProjection(reordered, fixture), /facts differ/);
});

test('citations are exact, unique and repository-relative', () => {
  const traversal = mutate(value => { value.citations[0] = '../secret.txt'; });
  assert.throws(() => validateF3CProjection(traversal, fixture), /repository-relative/);
  const duplicate = mutate(value => { value.citations[1] = value.citations[0]; });
  assert.throws(() => validateF3CProjection(duplicate, fixture), /citations mismatch/);
});

test('citations must resolve', () => {
  const projection = mutate(value => { value.citations[0] = 'docs/missing-f3c-evidence.md'; });
  assert.throws(() => validateF3CProjection(projection, fixture), /does not resolve/);
});

test('provenance binds exact evidence, fixture and profile', () => {
  for (const field of ['evidenceRef', 'fixtureRef', 'profileRef', 'evidenceClass']) {
    const projection = mutate(value => { value.provenance[field] = 'OTHER'; });
    assert.throws(() => validateF3CProjection(projection, fixture), /provenance mismatch/);
  }
});

test('limitations are mandatory and ordered', () => {
  const projection = mutate(value => { value.limitations.pop(); });
  assert.throws(() => validateF3CProjection(projection, fixture), /limitations mismatch/);
});

test('publication remains TEST_ONLY with runtime unavailable', () => {
  for (const [field, value] of [['publicationState', 'PRODUCTION'], ['runtimeState', 'AVAILABLE']]) {
    const projection = mutate(item => { item.boundary[field] = value; });
    assert.throws(() => validateF3CProjection(projection, fixture), /publication\/runtime state mismatch/);
  }
});

test('protected-site use and external calls remain zero', () => {
  const protectedSite = mutate(value => { value.boundary.protectedSiteUsed = true; });
  assert.throws(() => validateF3CProjection(protectedSite, fixture), /crossed the protected-site/);
  const external = mutate(value => { value.boundary.externalReferenceCalls = 1; });
  assert.throws(() => validateF3CProjection(external, fixture), /crossed the protected-site/);
});

test('command and Safety authority cannot be claimed', () => {
  const command = mutate(value => { value.boundary.commandAuthority = 'GRANTED'; });
  assert.throws(() => validateF3CProjection(command, fixture), /authority boundary mismatch/);
  const safety = mutate(value => { value.boundary.safetyAuthority = 'SOFTWARE'; });
  assert.throws(() => validateF3CProjection(safety, fixture), /authority boundary mismatch/);
});

test('protected fields are rejected anywhere', () => {
  const projection = mutate(value => { value.provenance.rawLocator = 'C:/secret'; });
  assert.throws(() => validateF3CProjection(projection, fixture), /rawLocator is not allowed|protected/);
});

test('protected values cannot be embedded in approved string fields', () => {
  const projection = mutate(value => { value.limitations[0] = fixture.request.siteSnapshot.siteRecordDigest; });
  assert.throws(() => validateF3CProjection(projection, fixture), /limitations mismatch|protected/);
});

test('forecast, ranking, readiness and command fields are rejected', () => {
  for (const key of ['forecast', 'score', 'readiness', 'deviceCommand']) {
    const projection = mutate(value => { value.method[key] = 'FORBIDDEN'; });
    assert.throws(() => validateF3CProjection(projection, fixture), /not allowed|prohibited/);
  }
});

test('projection digest detects tampering', () => {
  const projection = mutate(value => { value.facts[0].numericValue = 12; }, { seal: false });
  assert.throws(() => validateF3CProjection(projection, fixture), /facts differ|projectionDigest/);
});

test('generated artifact equals adapter output', () => {
  assert.deepEqual(generated, fresh());
});

test('browser validator accepts the governed projection', async () => {
  assert.equal(await validateObservationPlannerProjection(structuredClone(generated)), true);
});

test('browser validator detects digest tampering', async () => {
  const projection = structuredClone(generated);
  projection.facts[0].numericValue = 12;
  await assert.rejects(() => validateObservationPlannerProjection(projection), /Digest della projection non valido/);
});

test('browser validator rejects production or runtime promotion', async () => {
  for (const change of [value => { value.environment = 'PRODUCTION'; }, value => { value.boundary.runtimeState = 'AVAILABLE'; }]) {
    const projection = structuredClone(generated);
    change(projection);
    await assert.rejects(() => validateObservationPlannerProjection(projection), /TEST\/NONE|Boundary di pubblicazione/);
  }
});

test('browser validator rejects protected or later-capability fields', async () => {
  for (const key of ['latitudeDeg', 'score']) {
    const projection = structuredClone(generated);
    projection.method[key] = key === 'latitudeDeg' ? 45 : 100;
    await assert.rejects(() => validateObservationPlannerProjection(projection), /dati protetti|capability non autorizzata|proprietà inattese o mancanti/);
  }
});

test('browser validator rejects unknown nested properties', async () => {
  const projection = structuredClone(generated);
  projection.method.providerNote = 'unexpected';
  await assert.rejects(() => validateObservationPlannerProjection(projection), /proprietà inattese o mancanti/);
});
