import fs from 'node:fs';
import { canonicalJson, contentDigest, validateF3BContractFixture } from './observation-planner-ephemeris-lunar-f3b-contract.mjs';

export const F3C_ADAPTER_ID = 'BKL031-F3C-BOUNDED-ADAPTER';
export const F3C_ADAPTER_VERSION = '1.0';
export const F3C_PROJECTION_TYPE = 'BKL031_F3C_BOUNDED_SANITIZED_PROJECTION';

const ROOT_KEYS = new Set(['schemaVersion', 'projectionType', 'projectionId', 'generatedAtUtc', 'environment', 'authority', 'sourceContractRef', 'contextRef', 'sitePublicEvidenceRef', 'setupAvailabilityState', 'evidenceAvailabilityState', 'method', 'validity', 'facts', 'citations', 'provenance', 'limitations', 'boundary', 'projectionDigest']);
const METHOD_KEYS = new Set(['profileRef', 'methodId', 'methodVersion', 'adapterId', 'adapterVersion', 'outputFrame', 'refractionModel']);
const VALIDITY_KEYS = new Set(['fromUtc', 'toUtc']);
const FACT_KEYS = new Set(['factType', 'instantUtc', 'numericValue', 'instantValue', 'unit']);
const PROVENANCE_KEYS = new Set(['evidenceRef', 'fixtureRef', 'profileRef', 'evidenceClass']);
const BOUNDARY_KEYS = new Set(['publicationState', 'runtimeState', 'protectedSiteUsed', 'externalReferenceCalls', 'commandAuthority', 'safetyAuthority']);
const PROTECTED_KEYS = new Set(['latitudeDeg', 'longitudeDeg', 'elevationM', 'siteRecordRef', 'siteRecordDigest', 'assignmentRef', 'assignmentDigest', 'profileSourceSha256', 'dataDigest', 'inputDigest', 'outputDigest', 'contractDigest', 'rawLocator', 'absolutePath', 'uncPath', 'credential', 'secret', 'token']);
const FORBIDDEN_CAPABILITY_KEYS = new Set(['forecast', 'weatherForecast', 'weight', 'score', 'threshold', 'rank', 'ranking', 'targetOrder', 'readiness', 'goNoGo', 'safe', 'isSafe', 'scheduler', 'deviceCommand', 'command']);
const REQUIRED_LIMITATIONS = Object.freeze([
  'SYNTHETIC_F3C_INTEGRATION_ONLY',
  'S10_RUNTIME_UNAVAILABLE',
  'NO_PROTECTED_SITE_OR_EXTERNAL_REFERENCE',
  'NO_FORECAST_RANKING_READINESS_COMMAND_OR_SAFETY_AUTHORITY'
]);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function exactKeys(value, allowed, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object.`);
  for (const key of Object.keys(value)) assert(allowed.has(key), `${label}.${key} is not allowed.`);
  for (const key of allowed) assert(Object.hasOwn(value, key), `${label}.${key} is required.`);
}

function utc(value, label) {
  assert(typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(value) && Number.isFinite(Date.parse(value)), `${label} must be a UTC instant.`);
}

function repositoryRelative(value, label) {
  assert(typeof value === 'string' && value.length > 0 && !value.includes('\\') && !value.startsWith('/') && !/^[A-Za-z]:/.test(value) && !value.split('/').includes('..'), `${label} must be repository-relative.`);
}

function visitKeys(value, visitor, path = 'projection') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) return value.forEach((child, index) => visitKeys(child, visitor, `${path}[${index}]`));
  for (const [key, child] of Object.entries(value)) {
    visitor(key, child, `${path}.${key}`);
    visitKeys(child, visitor, `${path}.${key}`);
  }
}

function digestPayload(projection) {
  const { projectionDigest: _projectionDigest, ...payload } = projection;
  return payload;
}

export function sealF3CProjection(projection) {
  projection.projectionDigest = contentDigest(digestPayload(projection));
  return projection;
}

export function buildF3CProjection(fixture) {
  validateF3BContractFixture(fixture);
  const source = fixture.publicProjection;
  const identityDigest = contentDigest({ adapterId: F3C_ADAPTER_ID, adapterVersion: F3C_ADAPTER_VERSION, source });
  const projection = {
    schemaVersion: '1.0',
    projectionType: F3C_PROJECTION_TYPE,
    projectionId: `BKL031-F3C-${identityDigest.slice(0, 24).toUpperCase()}`,
    generatedAtUtc: fixture.evidence.generatedAtUtc,
    environment: 'TEST',
    authority: 'NONE',
    sourceContractRef: fixture.fixtureId,
    contextRef: fixture.request.contextId,
    sitePublicEvidenceRef: fixture.request.siteSnapshot.publicEvidenceRef,
    setupAvailabilityState: fixture.request.setupSnapshot.availabilityState,
    evidenceAvailabilityState: fixture.evidence.availabilityState,
    method: {
      profileRef: fixture.methodProfile.profileId,
      methodId: fixture.evidence.methodId,
      methodVersion: fixture.evidence.methodVersion,
      adapterId: F3C_ADAPTER_ID,
      adapterVersion: F3C_ADAPTER_VERSION,
      outputFrame: fixture.evidence.outputFrame,
      refractionModel: fixture.evidence.refractionModel
    },
    validity: {
      fromUtc: fixture.evidence.validFromUtc,
      toUtc: fixture.evidence.validToUtc
    },
    facts: structuredClone(source.facts),
    citations: [
      'docs/architecture/ADR-010-Ephemeris-Lunar-Method-and-Validation-Profile.md',
      'docs/architecture/scientific-assets/BKL-031-F3-B-Ephemeris-Lunar-Machine-Readable-Contracts-and-Validator.md'
    ],
    provenance: {
      evidenceRef: fixture.evidence.evidenceId,
      fixtureRef: fixture.fixtureId,
      profileRef: fixture.methodProfile.profileId,
      evidenceClass: 'SYNTHETIC_VALIDATION'
    },
    limitations: [...REQUIRED_LIMITATIONS],
    boundary: {
      publicationState: 'TEST_ONLY',
      runtimeState: 'UNAVAILABLE',
      protectedSiteUsed: false,
      externalReferenceCalls: 0,
      commandAuthority: 'NONE',
      safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS'
    },
    projectionDigest: ''
  };
  sealF3CProjection(projection);
  validateF3CProjection(projection, fixture);
  return projection;
}

export function validateF3CProjection(projection, fixture) {
  validateF3BContractFixture(fixture);
  exactKeys(projection, ROOT_KEYS, 'projection');
  assert(projection.schemaVersion === '1.0' && projection.projectionType === F3C_PROJECTION_TYPE, 'projection identity mismatch.');
  assert(/^BKL031-F3C-[0-9A-F]{24}$/.test(projection.projectionId), 'projectionId is invalid.');
  utc(projection.generatedAtUtc, 'projection.generatedAtUtc');
  assert(projection.generatedAtUtc === fixture.evidence.generatedAtUtc, 'projection generation instant does not bind the evidence.');
  assert(projection.environment === 'TEST' && projection.authority === 'NONE', 'projection must remain TEST/NONE.');
  assert(projection.sourceContractRef === fixture.fixtureId && projection.contextRef === fixture.request.contextId, 'projection source/context binding mismatch.');
  assert(projection.sitePublicEvidenceRef === fixture.request.siteSnapshot.publicEvidenceRef, 'projection public site reference mismatch.');
  assert(projection.setupAvailabilityState === fixture.request.setupSnapshot.availabilityState && projection.evidenceAvailabilityState === fixture.evidence.availabilityState, 'projection availability state mismatch.');

  exactKeys(projection.method, METHOD_KEYS, 'projection.method');
  assert(projection.method.profileRef === fixture.methodProfile.profileId && projection.method.methodId === fixture.evidence.methodId && projection.method.methodVersion === fixture.evidence.methodVersion, 'projection method identity mismatch.');
  assert(projection.method.adapterId === F3C_ADAPTER_ID && projection.method.adapterVersion === F3C_ADAPTER_VERSION, 'projection adapter identity mismatch.');
  assert(projection.method.outputFrame === fixture.evidence.outputFrame && projection.method.refractionModel === fixture.evidence.refractionModel, 'projection output semantics mismatch.');

  exactKeys(projection.validity, VALIDITY_KEYS, 'projection.validity');
  utc(projection.validity.fromUtc, 'projection.validity.fromUtc');
  utc(projection.validity.toUtc, 'projection.validity.toUtc');
  assert(projection.validity.fromUtc === fixture.evidence.validFromUtc && projection.validity.toUtc === fixture.evidence.validToUtc && Date.parse(projection.validity.fromUtc) < Date.parse(projection.validity.toUtc), 'projection validity mismatch.');
  assert(Array.isArray(projection.facts) && projection.facts.length > 0 && projection.facts.length <= 72, 'projection facts are outside bounds.');
  projection.facts.forEach((fact, index) => exactKeys(fact, FACT_KEYS, `projection.facts[${index}]`));
  assert(canonicalJson(projection.facts) === canonicalJson(fixture.publicProjection.facts), 'projection facts differ from accepted sanitized evidence.');

  assert(Array.isArray(projection.citations) && projection.citations.length === 2 && new Set(projection.citations).size === projection.citations.length, 'projection citations mismatch.');
  for (const citation of projection.citations) {
    repositoryRelative(citation, 'projection citation');
    assert(fs.existsSync(citation), `projection citation does not resolve: ${citation}`);
  }
  exactKeys(projection.provenance, PROVENANCE_KEYS, 'projection.provenance');
  assert(projection.provenance.evidenceRef === fixture.evidence.evidenceId && projection.provenance.fixtureRef === fixture.fixtureId && projection.provenance.profileRef === fixture.methodProfile.profileId && projection.provenance.evidenceClass === 'SYNTHETIC_VALIDATION', 'projection provenance mismatch.');
  assert(Array.isArray(projection.limitations) && canonicalJson(projection.limitations) === canonicalJson(REQUIRED_LIMITATIONS), 'projection limitations mismatch.');

  exactKeys(projection.boundary, BOUNDARY_KEYS, 'projection.boundary');
  assert(projection.boundary.publicationState === 'TEST_ONLY' && projection.boundary.runtimeState === 'UNAVAILABLE', 'projection publication/runtime state mismatch.');
  assert(projection.boundary.protectedSiteUsed === false && projection.boundary.externalReferenceCalls === 0, 'projection crossed the protected-site or external-reference boundary.');
  assert(projection.boundary.commandAuthority === 'NONE' && projection.boundary.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'projection authority boundary mismatch.');

  visitKeys(projection, (key, _value, path) => {
    assert(!PROTECTED_KEYS.has(key), `${path} exposes protected/internal data.`);
    assert(!FORBIDDEN_CAPABILITY_KEYS.has(key), `${path} introduces a prohibited later capability.`);
  });
  const serialized = canonicalJson(projection);
  for (const protectedValue of [fixture.request.siteSnapshot.siteRecordRef, fixture.request.siteSnapshot.siteRecordDigest, fixture.request.setupSnapshot.assignmentRef, fixture.request.setupSnapshot.assignmentDigest, fixture.methodProfile.profileSourceSha256, fixture.evidence.dataDigest, fixture.request.inputDigest, fixture.evidence.outputDigest, fixture.contractDigest].filter(Boolean)) {
    assert(!serialized.includes(protectedValue), 'projection exposes a protected/internal identity or digest.');
  }
  assert(/^[0-9a-f]{64}$/.test(projection.projectionDigest) && projection.projectionDigest === contentDigest(digestPayload(projection)), 'projectionDigest does not match canonical content.');
  const expectedIdentity = contentDigest({ adapterId: F3C_ADAPTER_ID, adapterVersion: F3C_ADAPTER_VERSION, source: fixture.publicProjection });
  assert(projection.projectionId === `BKL031-F3C-${expectedIdentity.slice(0, 24).toUpperCase()}`, 'projectionId is not deterministic.');
  return true;
}
