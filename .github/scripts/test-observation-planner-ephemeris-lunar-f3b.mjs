import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { canonicalJson, contentDigest, reseal, validateF3BContractFixture } from './observation-planner-ephemeris-lunar-f3b-contract.mjs';

const source = JSON.parse(fs.readFileSync('docs/data/observation-planner-ephemeris-lunar-f3b-fixture.json', 'utf8'));
const clone = () => structuredClone(source);
const sealRoot = (fixture) => reseal(fixture, 'contractDigest');
const sealProfile = (fixture) => { reseal(fixture.methodProfile, 'profileDigest'); sealRoot(fixture); };
const sealRequest = (fixture) => { reseal(fixture.request, 'inputDigest'); sealRoot(fixture); };
const sealEvidence = (fixture) => { reseal(fixture.evidence, 'outputDigest'); sealRoot(fixture); };

test('canonical JSON and known-answer digest are deterministic', () => {
  assert.equal(canonicalJson({ b: 2, a: 1 }), '{"a":1,"b":2}');
  assert.equal(contentDigest({ b: 2, a: 1 }), '43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777');
});

test('bounded TEST/NONE fixture passes without runtime, protected-site or external-reference activity', () => {
  assert.equal(validateF3BContractFixture(clone()), true);
  assert.equal(source.boundaries.runtimeActivated, false);
  assert.equal(source.boundaries.protectedSiteUsed, false);
  assert.equal(source.boundaries.externalReferenceCalls, 0);
});

test('unknown properties are rejected fail closed', () => {
  const fixture = clone();
  fixture.request.legacyProviderPayload = {};
  sealRequest(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /legacyProviderPayload is not allowed/);
});

test('tampered contract identity is rejected by canonical digest', () => {
  const fixture = clone();
  fixture.evidence.adapterVersion = 'tampered';
  assert.throws(() => validateF3BContractFixture(fixture), /outputDigest does not match canonical content/);
});

test('method profile must resolve the exact governed source bytes', () => {
  const fixture = clone();
  fixture.methodProfile.profileSourceSha256 = '0'.repeat(64);
  sealProfile(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /source digest mismatch/);
});

test('shared-SPK cross-check cannot claim data independence', () => {
  const fixture = clone();
  fixture.methodProfile.crossCheck.dataIndependenceClaim = true;
  sealProfile(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /no data-independence claim/);
});

test('contract validation and external-reference network policies remain DENY', () => {
  for (const field of ['externalReference', 'contractValidationNetwork']) {
    const fixture = clone();
    fixture.methodProfile.networkPolicy[field] = 'ALLOW';
    sealProfile(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), /network policy must deny/);
  }
});

test('method profile cannot grant runtime or execution authority', () => {
  for (const field of ['runtimeAuthority', 'executionAuthority']) {
    const fixture = clone();
    fixture.methodProfile.authority[field] = 'GRANTED';
    sealProfile(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), /authority boundary mismatch/);
  }
});

test('coverage must remain ordered and prohibit extrapolation', () => {
  const fixture = clone();
  fixture.methodProfile.coverage.extrapolationAllowed = true;
  sealProfile(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /prohibit extrapolation/);
});

test('request instants must be unique and strictly ordered', () => {
  const fixture = clone();
  fixture.request.evaluationTimesUtc[1] = fixture.request.evaluationTimesUtc[0];
  sealRequest(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /must not contain duplicates|strictly ordered/);
});

test('request grid is bounded to eight instants and one day', () => {
  const tooMany = clone();
  tooMany.request.evaluationTimesUtc = Array.from({ length: 9 }, (_, index) => `2026-09-16T0${index}:00:00Z`);
  sealRequest(tooMany);
  assert.throws(() => validateF3BContractFixture(tooMany), /1\.\.8 items/);

  const tooWide = clone();
  tooWide.request.evaluationTimesUtc = ['2026-09-16T00:00:00Z', '2026-09-18T00:00:00Z'];
  sealRequest(tooWide);
  assert.throws(() => validateF3BContractFixture(tooWide), /approved time span/);
});

test('target coordinates require finite ICRS J2000 values in range', () => {
  for (const [field, value, expected] of [['targetRaDeg', 360, /RA is outside/], ['targetDecDeg', 91, /Dec is outside/], ['targetFrame', null, /frame\/epoch mismatch/], ['targetEpoch', null, /frame\/epoch mismatch/]]) {
    const fixture = clone();
    fixture.request.target[field] = value;
    sealRequest(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), expected);
  }
});

test('site coordinates and elevation fail closed outside semantic bounds', () => {
  for (const [field, value, expected] of [['latitudeDeg', -91, /latitude is outside/], ['longitudeDeg', 181, /longitude is outside/], ['elevationM', 10000, /elevation is outside/]]) {
    const fixture = clone();
    fixture.request.siteSnapshot[field] = value;
    sealRequest(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), expected);
  }
});

test('fixed-offset timezone and correlatable public site reference are rejected', () => {
  const fixed = clone();
  fixed.request.siteSnapshot.timezoneIana = '+01:00';
  sealRequest(fixed);
  assert.throws(() => validateF3BContractFixture(fixed), /IANA, not a fixed offset/);

  const correlatable = clone();
  correlatable.request.siteSnapshot.publicEvidenceRef = correlatable.request.siteSnapshot.siteRecordDigest;
  sealRequest(correlatable);
  assert.throws(() => validateF3BContractFixture(correlatable), /non-correlatable/);
});

test('non-available setup cannot carry an assignment identity', () => {
  const fixture = clone();
  fixture.request.setupSnapshot.assignmentRef = 'SETUP-LEAK';
  fixture.request.setupSnapshot.assignmentDigest = '1'.repeat(64);
  sealRequest(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /must not carry assignment identity/);
});

test('request profile and requested fact vocabulary must resolve exactly', () => {
  const missingProfile = clone();
  missingProfile.request.methodProfileRef = 'UNKNOWN-PROFILE';
  sealRequest(missingProfile);
  assert.throws(() => validateF3BContractFixture(missingProfile), /does not resolve/);

  const unknownFact = clone();
  unknownFact.request.requestedFacts[0] = 'forecastCloudCover';
  sealRequest(unknownFact);
  assert.throws(() => validateF3BContractFixture(unknownFact), /outside the method profile/);
});

test('request outside governed kernel coverage is rejected without extrapolation', () => {
  const fixture = clone();
  fixture.request.evaluationTimesUtc = ['2200-01-01T00:00:00Z'];
  sealRequest(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /outside method\/data coverage/);
});

test('evidence must bind the exact request and method profile', () => {
  for (const [field, value] of [['requestRef', 'OTHER-REQUEST'], ['methodProfileRef', 'OTHER-PROFILE']]) {
    const fixture = clone();
    fixture.evidence[field] = value;
    sealEvidence(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), /request\/profile reference mismatch/);
  }
});

test('method, kernel and data digests cannot silently switch', () => {
  for (const [field, value] of [['methodId', 'OTHER-METHOD'], ['providerOrKernelId', 'latest.bsp'], ['dataDigest', '2'.repeat(64)]]) {
    const fixture = clone();
    fixture.evidence[field] = value;
    sealEvidence(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), /method\/data identity mismatch/);
  }
});

test('time scales and Earth-orientation identity remain explicit', () => {
  const scales = clone();
  scales.evidence.calculationTimeScales = ['UTC'];
  sealEvidence(scales);
  assert.throws(() => validateF3BContractFixture(scales), /calculation time scales mismatch/);

  const eop = clone();
  eop.evidence.earthOrientationSource.digest = '3'.repeat(64);
  sealEvidence(eop);
  assert.throws(() => validateF3BContractFixture(eop), /Earth-orientation identity mismatch/);
});

test('output frame and refraction semantics cannot drift', () => {
  for (const [field, value] of [['outputFrame', 'GEOCENTRIC'], ['refractionModel', 'STANDARD_ATMOSPHERE']]) {
    const fixture = clone();
    fixture.evidence[field] = value;
    sealEvidence(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), /output frame\/refraction mismatch/);
  }
});

test('evidence uses a non-empty half-open validity interval', () => {
  const fixture = clone();
  fixture.evidence.validToUtc = fixture.evidence.validFromUtc;
  sealEvidence(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /non-empty half-open interval/);
});

test('fact instant must fall inside request and evidence validity', () => {
  const requestMismatch = clone();
  requestMismatch.evidence.facts[0].instantUtc = '2026-09-17T00:00:00Z';
  sealEvidence(requestMismatch);
  assert.throws(() => validateF3BContractFixture(requestMismatch), /outside the request/);

  const intervalMismatch = clone();
  intervalMismatch.evidence.validFromUtc = '2026-09-16T01:00:00Z';
  sealEvidence(intervalMismatch);
  assert.throws(() => validateF3BContractFixture(intervalMismatch), /outside the half-open validity interval/);
});

test('duplicate fact type and instant is rejected', () => {
  const fixture = clone();
  fixture.evidence.facts.push(structuredClone(fixture.evidence.facts[0]));
  sealEvidence(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /duplicate fact type\/instant pairs/);
});

test('normalized numeric fact ranges fail closed', () => {
  for (const [factType, value] of [['targetAltitudeDeg', 91], ['targetAzimuthDeg', 360], ['moonIlluminatedFraction', 1.1], ['targetMoonSeparationDeg', -1]]) {
    const fixture = clone();
    fixture.evidence.facts.find((fact) => fact.factType === factType).numericValue = value;
    sealEvidence(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), /numericValue is (above|below) range/);
  }
});

test('transit fact requires a UTC instant and no numeric value', () => {
  const fixture = clone();
  const transit = fixture.evidence.facts.find((fact) => fact.factType === 'meridianTransitUtc');
  transit.numericValue = 1;
  sealEvidence(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /numericValue must be null/);
});

test('target-Moon separation requires co-temporal target and Moon position facts', () => {
  const fixture = clone();
  fixture.evidence.facts = fixture.evidence.facts.filter((fact) => fact.factType !== 'moonAzimuthDeg');
  sealEvidence(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /same instant\/site\/method/);
});

test('AVAILABLE and non-available states enforce value/reason exclusivity', () => {
  const availableWithReason = clone();
  availableWithReason.evidence.reasonCodes = ['UNEXPECTED'];
  sealEvidence(availableWithReason);
  assert.throws(() => validateF3BContractFixture(availableWithReason), /requires facts and no reason codes/);

  const unavailableWithFacts = clone();
  unavailableWithFacts.evidence.availabilityState = 'UNAVAILABLE';
  unavailableWithFacts.evidence.reasonCodes = ['METHOD_UNAVAILABLE'];
  sealEvidence(unavailableWithFacts);
  assert.throws(() => validateF3BContractFixture(unavailableWithFacts), /must not carry fact values/);
});

test('precision profile and error budget are mandatory for AVAILABLE evidence', () => {
  const fixture = clone();
  fixture.evidence.precisionProfileId = '';
  sealEvidence(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /precisionProfileId must be non-empty/);
});

test('citations must remain repository-relative and resolvable', () => {
  const traversal = clone();
  traversal.evidence.citations[0] = '../secret.txt';
  sealEvidence(traversal);
  assert.throws(() => validateF3BContractFixture(traversal), /must not traverse/);

  const missing = clone();
  missing.evidence.citations[0] = 'docs/missing-evidence.md';
  sealEvidence(missing);
  assert.throws(() => validateF3BContractFixture(missing), /does not resolve/);
});

test('provenance must bind request and profile', () => {
  const fixture = clone();
  fixture.evidence.provenance.requestRef = 'OTHER';
  sealEvidence(fixture);
  assert.throws(() => validateF3BContractFixture(fixture), /provenance binding mismatch/);
});

test('public projection rejects exact coordinates, protected digests and altered facts', () => {
  const coordinateLeak = clone();
  coordinateLeak.publicProjection.latitudeDeg = 45;
  sealRoot(coordinateLeak);
  assert.throws(() => validateF3BContractFixture(coordinateLeak), /latitudeDeg is not allowed/);

  const digestLeak = clone();
  digestLeak.publicProjection.limitations.push(digestLeak.request.siteSnapshot.siteRecordDigest);
  sealRoot(digestLeak);
  assert.throws(() => validateF3BContractFixture(digestLeak), /exposes a protected\/internal digest/);

  const altered = clone();
  altered.publicProjection.facts[0].numericValue = 12;
  sealRoot(altered);
  assert.throws(() => validateF3BContractFixture(altered), /facts differ/);
});

test('F3-C, runtime, protected-site, external-reference, forecast, ranking and readiness remain disabled', () => {
  for (const field of ['f3cAdapterImplemented', 'runtimeActivated', 'protectedSiteUsed', 'forecastImplemented', 'rankingImplemented', 'readinessImplemented']) {
    const fixture = clone();
    fixture.boundaries[field] = true;
    sealRoot(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), new RegExp(`${field} must remain false`));
  }
  const calls = clone();
  calls.boundaries.externalReferenceCalls = 1;
  sealRoot(calls);
  assert.throws(() => validateF3BContractFixture(calls), /zero external-reference calls/);
});

test('forecast, ranking, readiness, command and secret fields are rejected anywhere', () => {
  for (const key of ['forecast', 'score', 'readiness', 'deviceCommand', 'credential']) {
    const fixture = clone();
    fixture.evidence[key] = 'FORBIDDEN';
    sealEvidence(fixture);
    assert.throws(() => validateF3BContractFixture(fixture), /forbidden in F3-B/);
  }
});
