import crypto from 'node:crypto';
import fs from 'node:fs';

export const SCHEMA_VERSION = '1.0';
export const CONTRACT_TYPES = Object.freeze({
  fixture: 'BKL031_F3B_BOUNDED_CONTRACT_FIXTURE',
  methodProfile: 'BKL031_F3B_METHOD_PROFILE',
  request: 'BKL031_F3B_EPHEMERIS_LUNAR_REQUEST',
  evidence: 'BKL031_F3B_EPHEMERIS_LUNAR_EVIDENCE'
});

export const FACT_RULES = Object.freeze({
  targetAltitudeDeg: { unit: 'deg', min: -90, max: 90 },
  targetAzimuthDeg: { unit: 'deg', min: 0, maxExclusive: 360 },
  meridianTransitUtc: { unit: 'utc', instant: true },
  solarAltitudeDeg: { unit: 'deg', min: -90, max: 90 },
  moonAltitudeDeg: { unit: 'deg', min: -90, max: 90 },
  moonAzimuthDeg: { unit: 'deg', min: 0, maxExclusive: 360 },
  moonPhaseAngleDeg: { unit: 'deg', min: 0, maxExclusive: 360 },
  moonIlluminatedFraction: { unit: 'fraction', min: 0, max: 1 },
  targetMoonSeparationDeg: { unit: 'deg', min: 0, max: 180 }
});

const ROOT_KEYS = new Set(['schemaVersion', 'contractType', 'fixtureId', 'environment', 'authority', 'methodProfile', 'request', 'evidence', 'publicProjection', 'boundaries', 'contractDigest']);
const PROFILE_KEYS = new Set(['schemaVersion', 'contractType', 'profileId', 'profileSourceRef', 'profileSourceSha256', 'decisionRef', 'decisionState', 'primaryMethod', 'crossCheck', 'timeSemantics', 'outputSemantics', 'coverage', 'errorBudget', 'networkPolicy', 'authority', 'profileDigest']);
const PRIMARY_KEYS = new Set(['methodId', 'library', 'libraryVersion', 'ephemerisEngine', 'kernelId', 'kernelSha256']);
const CROSS_KEYS = new Set(['methodId', 'library', 'libraryVersion', 'classification', 'dataIndependenceClaim']);
const TIME_KEYS = new Set(['inputTimeScale', 'calculationTimeScales', 'earthOrientationSourceId', 'earthOrientationSha256']);
const OUTPUT_KEYS = new Set(['frame', 'refractionModel', 'azimuthConvention', 'moonPhaseAngleConvention', 'allowedFacts']);
const COVERAGE_KEYS = new Set(['startUtc', 'endUtc', 'extrapolationAllowed']);
const BUDGET_KEYS = new Set(['profileId', 'reference', 'altitudeArcsecMax', 'azimuthArcsecMax', 'separationArcsecMax', 'illuminationAbsoluteMax', 'transitSecondsMax']);
const NETWORK_KEYS = new Set(['externalReference', 'contractValidationNetwork']);
const PROFILE_AUTHORITY_KEYS = new Set(['environment', 'authority', 'repositoryMethodAuthority', 'runtimeAuthority', 'executionAuthority', 'safetyAuthority']);
const REQUEST_KEYS = new Set(['schemaVersion', 'contractType', 'requestId', 'contextId', 'environment', 'authority', 'generatedAtUtc', 'evaluationTimesUtc', 'target', 'siteSnapshot', 'setupSnapshot', 'methodProfileRef', 'requestedFacts', 'bounds', 'inputDigest']);
const TARGET_KEYS = new Set(['targetIdentityRef', 'targetRaDeg', 'targetDecDeg', 'targetFrame', 'targetEpoch']);
const SITE_KEYS = new Set(['siteRecordRef', 'siteRecordDigest', 'publicEvidenceRef', 'classification', 'geodeticDatum', 'latitudeDeg', 'longitudeDeg', 'elevationM', 'timezoneIana']);
const SETUP_KEYS = new Set(['assignmentRef', 'assignmentDigest', 'availabilityState']);
const BOUNDS_KEYS = new Set(['maxInstants', 'maxFacts', 'maxSpanSeconds']);
const EVIDENCE_KEYS = new Set(['schemaVersion', 'contractType', 'evidenceId', 'environment', 'authority', 'requestRef', 'availabilityState', 'methodProfileRef', 'methodId', 'methodVersion', 'adapterId', 'adapterVersion', 'providerOrKernelId', 'dataDigest', 'inputTimeScale', 'calculationTimeScales', 'earthOrientationSource', 'outputFrame', 'refractionModel', 'generatedAtUtc', 'validFromUtc', 'validToUtc', 'inputDigest', 'facts', 'citations', 'provenance', 'reasonCodes', 'precisionProfileId', 'errorBudgetRef', 'outputDigest']);
const EOP_KEYS = new Set(['sourceId', 'digest']);
const FACT_KEYS = new Set(['factType', 'instantUtc', 'numericValue', 'instantValue', 'unit']);
const PROVENANCE_KEYS = new Set(['evidenceClass', 'requestRef', 'methodProfileRef', 'sourceRefs']);
const PROJECTION_KEYS = new Set(['schemaVersion', 'projectionType', 'environment', 'authority', 'sitePublicEvidenceRef', 'evidenceRef', 'availabilityState', 'methodId', 'methodVersion', 'facts', 'limitations']);
const BOUNDARY_KEYS = new Set(['f3cAdapterImplemented', 'runtimeActivated', 'protectedSiteUsed', 'externalReferenceCalls', 'forecastImplemented', 'rankingImplemented', 'readinessImplemented', 'commandAuthority', 'safetyAuthority']);
const SHA256 = /^[a-f0-9]{64}$/;
const UTC = /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z$/;
const FORBIDDEN_KEYS = new Set(['forecast', 'weatherForecast', 'weight', 'score', 'threshold', 'rank', 'ranking', 'targetOrder', 'readiness', 'goNoGo', 'safe', 'isSafe', 'scheduler', 'deviceCommand', 'command', 'credential', 'secret', 'token', 'rawLocator', 'absolutePath', 'uncPath']);
const PROJECTION_PROTECTED_KEYS = new Set(['latitudeDeg', 'longitudeDeg', 'elevationM', 'siteRecordDigest', 'siteRecordRef', 'assignmentDigest', 'assignmentRef', 'profileSourceSha256', 'dataDigest', 'inputDigest', 'outputDigest']);

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

export function contentDigest(value) {
  return crypto.createHash('sha256').update(canonicalJson(value), 'utf8').digest('hex');
}

export function reseal(record, digestField) {
  const clone = structuredClone(record);
  delete clone[digestField];
  record[digestField] = contentDigest(clone);
  return record;
}

export function resealFixture(fixture, records = []) {
  if (records.includes('methodProfile')) reseal(fixture.methodProfile, 'profileDigest');
  if (records.includes('request')) reseal(fixture.request, 'inputDigest');
  if (records.includes('evidence')) reseal(fixture.evidence, 'outputDigest');
  reseal(fixture, 'contractDigest');
  return fixture;
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function exactKeys(value, keys, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object.`);
  for (const key of Object.keys(value)) assert(keys.has(key), `${label}.${key} is not allowed.`);
  for (const key of keys) assert(Object.hasOwn(value, key), `${label}.${key} is required.`);
}

function nonEmpty(value, label) {
  assert(typeof value === 'string' && value.trim().length > 0, `${label} must be non-empty.`);
}

function sha(value, label) {
  assert(typeof value === 'string' && SHA256.test(value), `${label} must be a lowercase SHA-256 digest.`);
}

function utc(value, label) {
  assert(typeof value === 'string' && UTC.test(value) && Number.isFinite(Date.parse(value)), `${label} must be a canonical UTC instant.`);
}

function finite(value, label) {
  assert(typeof value === 'number' && Number.isFinite(value), `${label} must be finite.`);
}

function uniqueStrings(values, label, { min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
  assert(Array.isArray(values) && values.length >= min && values.length <= max, `${label} must contain ${min}..${max} items.`);
  assert(values.every((value) => typeof value === 'string' && value.length > 0), `${label} must contain non-empty strings.`);
  assert(new Set(values).size === values.length, `${label} must not contain duplicates.`);
}

function repositoryRelative(value, label) {
  nonEmpty(value, label);
  assert(!value.startsWith('/') && !value.startsWith('\\') && !/^[A-Za-z]:[\\/]/.test(value), `${label} must be repository-relative.`);
  assert(!value.replaceAll('\\', '/').split('/').includes('..'), `${label} must not traverse outside the repository.`);
}

function digestMatches(record, field, label) {
  sha(record[field], `${label}.${field}`);
  const clone = structuredClone(record);
  delete clone[field];
  assert(record[field] === contentDigest(clone), `${label}.${field} does not match canonical content.`);
}

function noForbiddenKeys(value, path = '$') {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) return value.forEach((item, index) => noForbiddenKeys(item, `${path}[${index}]`));
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_KEYS.has(key), `${path}.${key} is forbidden in F3-B.`);
    noForbiddenKeys(child, `${path}.${key}`);
  }
}

function validateMethodProfile(profile) {
  exactKeys(profile, PROFILE_KEYS, 'methodProfile');
  assert(profile.schemaVersion === SCHEMA_VERSION && profile.contractType === CONTRACT_TYPES.methodProfile, 'methodProfile identity mismatch.');
  nonEmpty(profile.profileId, 'methodProfile.profileId');
  repositoryRelative(profile.profileSourceRef, 'methodProfile.profileSourceRef');
  sha(profile.profileSourceSha256, 'methodProfile.profileSourceSha256');
  assert(fs.existsSync(profile.profileSourceRef), 'methodProfile source does not exist.');
  const actualSourceDigest = crypto.createHash('sha256').update(fs.readFileSync(profile.profileSourceRef)).digest('hex');
  assert(actualSourceDigest === profile.profileSourceSha256, 'methodProfile source digest mismatch.');
  assert(profile.decisionRef === 'ADR-010' && profile.decisionState === 'ACCEPTED_REPOSITORY_METHOD_AUTHORITY', 'methodProfile must bind accepted ADR-010 repository authority.');

  exactKeys(profile.primaryMethod, PRIMARY_KEYS, 'methodProfile.primaryMethod');
  for (const field of ['methodId', 'library', 'libraryVersion', 'ephemerisEngine', 'kernelId']) nonEmpty(profile.primaryMethod[field], `methodProfile.primaryMethod.${field}`);
  sha(profile.primaryMethod.kernelSha256, 'methodProfile.primaryMethod.kernelSha256');
  assert(profile.primaryMethod.kernelId === 'de442s.bsp', 'methodProfile kernel identity mismatch.');
  assert(profile.primaryMethod.kernelSha256 === '54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c', 'methodProfile kernel digest mismatch.');

  exactKeys(profile.crossCheck, CROSS_KEYS, 'methodProfile.crossCheck');
  assert(profile.crossCheck.classification === 'IMPLEMENTATION_CROSS_CHECK_SHARED_GOVERNED_SPK' && profile.crossCheck.dataIndependenceClaim === false, 'cross-check must disclose shared governed SPK and no data-independence claim.');

  exactKeys(profile.timeSemantics, TIME_KEYS, 'methodProfile.timeSemantics');
  assert(profile.timeSemantics.inputTimeScale === 'UTC', 'methodProfile input time scale must be UTC.');
  uniqueStrings(profile.timeSemantics.calculationTimeScales, 'methodProfile.calculationTimeScales', { min: 1, max: 5 });
  sha(profile.timeSemantics.earthOrientationSha256, 'methodProfile.earthOrientationSha256');

  exactKeys(profile.outputSemantics, OUTPUT_KEYS, 'methodProfile.outputSemantics');
  assert(profile.outputSemantics.frame === 'TOPOCENTRIC_ALTAZ' && profile.outputSemantics.refractionModel === 'AIRLESS', 'methodProfile normalized output semantics mismatch.');
  assert(profile.outputSemantics.azimuthConvention === 'EAST_OF_NORTH', 'methodProfile azimuth convention mismatch.');
  assert(profile.outputSemantics.moonPhaseAngleConvention === '0_NEW_180_FULL_DEGREES', 'methodProfile Moon phase convention mismatch.');
  uniqueStrings(profile.outputSemantics.allowedFacts, 'methodProfile.allowedFacts', { min: 9, max: 9 });
  assert(profile.outputSemantics.allowedFacts.every((fact) => Object.hasOwn(FACT_RULES, fact)), 'methodProfile contains an unknown fact type.');

  exactKeys(profile.coverage, COVERAGE_KEYS, 'methodProfile.coverage');
  utc(profile.coverage.startUtc, 'methodProfile.coverage.startUtc');
  utc(profile.coverage.endUtc, 'methodProfile.coverage.endUtc');
  assert(Date.parse(profile.coverage.startUtc) < Date.parse(profile.coverage.endUtc) && profile.coverage.extrapolationAllowed === false, 'methodProfile coverage must be ordered and prohibit extrapolation.');

  exactKeys(profile.errorBudget, BUDGET_KEYS, 'methodProfile.errorBudget');
  assert(profile.errorBudget.reference === 'ADR-010', 'methodProfile error budget must reference ADR-010.');
  for (const field of ['altitudeArcsecMax', 'azimuthArcsecMax', 'separationArcsecMax', 'illuminationAbsoluteMax', 'transitSecondsMax']) {
    finite(profile.errorBudget[field], `methodProfile.errorBudget.${field}`);
    assert(profile.errorBudget[field] > 0, `methodProfile.errorBudget.${field} must be positive.`);
  }

  exactKeys(profile.networkPolicy, NETWORK_KEYS, 'methodProfile.networkPolicy');
  assert(profile.networkPolicy.externalReference === 'DENY' && profile.networkPolicy.contractValidationNetwork === 'DENY', 'F3-B network policy must deny external and validation traffic.');
  exactKeys(profile.authority, PROFILE_AUTHORITY_KEYS, 'methodProfile.authority');
  assert(profile.authority.environment === 'TEST' && profile.authority.authority === 'NONE', 'methodProfile fixture must be TEST/NONE.');
  assert(profile.authority.repositoryMethodAuthority === 'ADR-010' && profile.authority.runtimeAuthority === 'NONE' && profile.authority.executionAuthority === 'NONE', 'methodProfile authority boundary mismatch.');
  assert(profile.authority.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'Safety Authority must remain local physical interlocks.');
  digestMatches(profile, 'profileDigest', 'methodProfile');
}

function validateRequest(request, profile) {
  exactKeys(request, REQUEST_KEYS, 'request');
  assert(request.schemaVersion === SCHEMA_VERSION && request.contractType === CONTRACT_TYPES.request, 'request identity mismatch.');
  assert(request.environment === 'TEST' && request.authority === 'NONE', 'request fixture must be TEST/NONE.');
  for (const field of ['requestId', 'contextId']) nonEmpty(request[field], `request.${field}`);
  utc(request.generatedAtUtc, 'request.generatedAtUtc');
  uniqueStrings(request.evaluationTimesUtc, 'request.evaluationTimesUtc', { min: 1, max: 8 });
  request.evaluationTimesUtc.forEach((value, index) => utc(value, `request.evaluationTimesUtc[${index}]`));
  assert(request.evaluationTimesUtc.every((value, index) => index === 0 || Date.parse(request.evaluationTimesUtc[index - 1]) < Date.parse(value)), 'request evaluation instants must be strictly ordered.');

  exactKeys(request.target, TARGET_KEYS, 'request.target');
  nonEmpty(request.target.targetIdentityRef, 'request.target.targetIdentityRef');
  finite(request.target.targetRaDeg, 'request.target.targetRaDeg');
  finite(request.target.targetDecDeg, 'request.target.targetDecDeg');
  assert(request.target.targetRaDeg >= 0 && request.target.targetRaDeg < 360, 'request target RA is outside [0,360).');
  assert(request.target.targetDecDeg >= -90 && request.target.targetDecDeg <= 90, 'request target Dec is outside [-90,90].');
  assert(request.target.targetFrame === 'ICRS' && request.target.targetEpoch === 'J2000.0', 'request target frame/epoch mismatch.');

  exactKeys(request.siteSnapshot, SITE_KEYS, 'request.siteSnapshot');
  assert(request.siteSnapshot.classification === 'SYNTHETIC_PUBLIC', 'F3-B fixture site must be unmistakably synthetic/public.');
  nonEmpty(request.siteSnapshot.siteRecordRef, 'request.siteSnapshot.siteRecordRef');
  nonEmpty(request.siteSnapshot.publicEvidenceRef, 'request.siteSnapshot.publicEvidenceRef');
  assert(request.siteSnapshot.publicEvidenceRef !== request.siteSnapshot.siteRecordRef && !SHA256.test(request.siteSnapshot.publicEvidenceRef), 'public site evidence reference must be non-correlatable to the protected record identity/digest.');
  assert(request.siteSnapshot.geodeticDatum === 'WGS84', 'request geodetic datum must be WGS84.');
  sha(request.siteSnapshot.siteRecordDigest, 'request.siteSnapshot.siteRecordDigest');
  finite(request.siteSnapshot.latitudeDeg, 'request.siteSnapshot.latitudeDeg');
  finite(request.siteSnapshot.longitudeDeg, 'request.siteSnapshot.longitudeDeg');
  finite(request.siteSnapshot.elevationM, 'request.siteSnapshot.elevationM');
  assert(request.siteSnapshot.latitudeDeg >= -90 && request.siteSnapshot.latitudeDeg <= 90, 'request site latitude is outside [-90,90].');
  assert(request.siteSnapshot.longitudeDeg >= -180 && request.siteSnapshot.longitudeDeg <= 180, 'request site longitude is outside [-180,180].');
  assert(request.siteSnapshot.elevationM >= -500 && request.siteSnapshot.elevationM <= 9000, 'request site elevation is outside the F3-B bound.');
  assert(!/^[+-][0-9]{2}:[0-9]{2}$/.test(request.siteSnapshot.timezoneIana), 'request timezone must be IANA, not a fixed offset.');
  try { new Intl.DateTimeFormat('en-US', { timeZone: request.siteSnapshot.timezoneIana }).format(new Date(0)); } catch { assert(false, 'request timezone must resolve as an IANA zone.'); }

  exactKeys(request.setupSnapshot, SETUP_KEYS, 'request.setupSnapshot');
  assert(['AVAILABLE', 'UNAVAILABLE_CURRENT', 'CONFLICTED'].includes(request.setupSnapshot.availabilityState), 'request setup availability state is invalid.');
  if (request.setupSnapshot.availabilityState === 'AVAILABLE') {
    nonEmpty(request.setupSnapshot.assignmentRef, 'request.setupSnapshot.assignmentRef');
    sha(request.setupSnapshot.assignmentDigest, 'request.setupSnapshot.assignmentDigest');
  } else {
    assert(request.setupSnapshot.assignmentRef === null && request.setupSnapshot.assignmentDigest === null, 'non-available setup must not carry assignment identity.');
  }

  assert(request.methodProfileRef === profile.profileId, 'request methodProfileRef does not resolve.');
  uniqueStrings(request.requestedFacts, 'request.requestedFacts', { min: 1, max: 9 });
  assert(request.requestedFacts.every((fact) => profile.outputSemantics.allowedFacts.includes(fact)), 'request asks for a fact outside the method profile.');
  exactKeys(request.bounds, BOUNDS_KEYS, 'request.bounds');
  assert(request.bounds.maxInstants === 8 && request.bounds.maxFacts === 9 && request.bounds.maxSpanSeconds === 86400, 'request bounds mismatch.');
  const span = (Date.parse(request.evaluationTimesUtc.at(-1)) - Date.parse(request.evaluationTimesUtc[0])) / 1000;
  assert(span <= request.bounds.maxSpanSeconds, 'request grid exceeds the approved time span.');
  for (const instant of request.evaluationTimesUtc) {
    assert(Date.parse(instant) >= Date.parse(profile.coverage.startUtc) && Date.parse(instant) < Date.parse(profile.coverage.endUtc), 'request instant is outside method/data coverage.');
  }
  digestMatches(request, 'inputDigest', 'request');
}

function validateFact(fact, index, request) {
  const label = `evidence.facts[${index}]`;
  exactKeys(fact, FACT_KEYS, label);
  const rule = FACT_RULES[fact.factType];
  assert(rule && request.requestedFacts.includes(fact.factType), `${label}.factType is not requested/allowed.`);
  utc(fact.instantUtc, `${label}.instantUtc`);
  assert(request.evaluationTimesUtc.includes(fact.instantUtc), `${label}.instantUtc is outside the request.`);
  assert(fact.unit === rule.unit, `${label}.unit mismatch.`);
  if (rule.instant) {
    assert(fact.numericValue === null, `${label}.numericValue must be null for an instant fact.`);
    utc(fact.instantValue, `${label}.instantValue`);
  } else {
    assert(fact.instantValue === null, `${label}.instantValue must be null for a numeric fact.`);
    finite(fact.numericValue, `${label}.numericValue`);
    if (Object.hasOwn(rule, 'min')) assert(fact.numericValue >= rule.min, `${label}.numericValue is below range.`);
    if (Object.hasOwn(rule, 'max')) assert(fact.numericValue <= rule.max, `${label}.numericValue is above range.`);
    if (Object.hasOwn(rule, 'maxExclusive')) assert(fact.numericValue < rule.maxExclusive, `${label}.numericValue is above range.`);
  }
}

function validateEvidence(evidence, request, profile) {
  exactKeys(evidence, EVIDENCE_KEYS, 'evidence');
  assert(evidence.schemaVersion === SCHEMA_VERSION && evidence.contractType === CONTRACT_TYPES.evidence, 'evidence identity mismatch.');
  assert(evidence.environment === 'TEST' && evidence.authority === 'NONE', 'evidence fixture must be TEST/NONE.');
  assert(evidence.requestRef === request.requestId && evidence.methodProfileRef === profile.profileId, 'evidence request/profile reference mismatch.');
  assert(['AVAILABLE', 'PARTIAL', 'UNAVAILABLE', 'CONFLICTED', 'STALE'].includes(evidence.availabilityState), 'evidence availabilityState is invalid.');
  assert(evidence.methodId === profile.primaryMethod.methodId && evidence.providerOrKernelId === profile.primaryMethod.kernelId && evidence.dataDigest === profile.primaryMethod.kernelSha256, 'evidence method/data identity mismatch.');
  for (const field of ['methodVersion', 'adapterId', 'adapterVersion']) nonEmpty(evidence[field], `evidence.${field}`);
  assert(evidence.inputTimeScale === profile.timeSemantics.inputTimeScale, 'evidence input time scale mismatch.');
  assert(canonicalJson(evidence.calculationTimeScales) === canonicalJson(profile.timeSemantics.calculationTimeScales), 'evidence calculation time scales mismatch.');
  exactKeys(evidence.earthOrientationSource, EOP_KEYS, 'evidence.earthOrientationSource');
  assert(evidence.earthOrientationSource.sourceId === profile.timeSemantics.earthOrientationSourceId && evidence.earthOrientationSource.digest === profile.timeSemantics.earthOrientationSha256, 'evidence Earth-orientation identity mismatch.');
  assert(evidence.outputFrame === profile.outputSemantics.frame && evidence.refractionModel === profile.outputSemantics.refractionModel, 'evidence output frame/refraction mismatch.');
  for (const field of ['generatedAtUtc', 'validFromUtc', 'validToUtc']) utc(evidence[field], `evidence.${field}`);
  assert(Date.parse(evidence.validFromUtc) < Date.parse(evidence.validToUtc), 'evidence validity must be a non-empty half-open interval.');
  assert(evidence.inputDigest === request.inputDigest, 'evidence inputDigest does not bind the request.');
  assert(Array.isArray(evidence.facts) && evidence.facts.length <= request.bounds.maxInstants * request.bounds.maxFacts, 'evidence facts exceed approved bounds.');
  evidence.facts.forEach((fact, index) => validateFact(fact, index, request));
  const factKeys = evidence.facts.map((fact) => `${fact.factType}|${fact.instantUtc}`);
  assert(new Set(factKeys).size === factKeys.length, 'evidence contains duplicate fact type/instant pairs.');
  for (const fact of evidence.facts) {
    assert(Date.parse(fact.instantUtc) >= Date.parse(evidence.validFromUtc) && Date.parse(fact.instantUtc) < Date.parse(evidence.validToUtc), 'evidence fact is outside the half-open validity interval.');
  }
  for (const separation of evidence.facts.filter((fact) => fact.factType === 'targetMoonSeparationDeg')) {
    for (const required of ['targetAltitudeDeg', 'targetAzimuthDeg', 'moonAltitudeDeg', 'moonAzimuthDeg']) {
      assert(evidence.facts.some((fact) => fact.factType === required && fact.instantUtc === separation.instantUtc), 'target/Moon separation requires target and Moon facts at the same instant/site/method.');
    }
  }
  if (evidence.availabilityState === 'AVAILABLE') {
    assert(evidence.facts.length > 0 && evidence.reasonCodes.length === 0, 'AVAILABLE evidence requires facts and no reason codes.');
    nonEmpty(evidence.precisionProfileId, 'evidence.precisionProfileId');
    nonEmpty(evidence.errorBudgetRef, 'evidence.errorBudgetRef');
  } else {
    assert(evidence.facts.length === 0, 'non-available evidence must not carry fact values.');
    uniqueStrings(evidence.reasonCodes, 'evidence.reasonCodes', { min: 1, max: 16 });
  }
  assert(evidence.precisionProfileId === profile.errorBudget.profileId && evidence.errorBudgetRef === profile.errorBudget.reference, 'evidence precision/error-budget reference mismatch.');
  uniqueStrings(evidence.citations, 'evidence.citations', { min: 1, max: 16 });
  for (const citation of evidence.citations) {
    repositoryRelative(citation, 'evidence citation');
    assert(fs.existsSync(citation), `evidence citation does not resolve: ${citation}`);
  }
  exactKeys(evidence.provenance, PROVENANCE_KEYS, 'evidence.provenance');
  assert(evidence.provenance.evidenceClass === 'SYNTHETIC_VALIDATION' && evidence.provenance.requestRef === request.requestId && evidence.provenance.methodProfileRef === profile.profileId, 'evidence provenance binding mismatch.');
  uniqueStrings(evidence.provenance.sourceRefs, 'evidence.provenance.sourceRefs', { min: 1, max: 16 });
  digestMatches(evidence, 'outputDigest', 'evidence');
}

function validateProjection(projection, request, evidence) {
  exactKeys(projection, PROJECTION_KEYS, 'publicProjection');
  assert(projection.schemaVersion === SCHEMA_VERSION && projection.projectionType === 'BKL031_F3B_SANITIZED_SYNTHETIC_EVIDENCE', 'public projection identity mismatch.');
  assert(projection.environment === 'TEST' && projection.authority === 'NONE', 'public projection must be TEST/NONE.');
  assert(projection.sitePublicEvidenceRef === request.siteSnapshot.publicEvidenceRef, 'public projection site reference mismatch.');
  assert(projection.evidenceRef === evidence.evidenceId && projection.availabilityState === evidence.availabilityState, 'public projection evidence binding mismatch.');
  assert(projection.methodId === evidence.methodId && projection.methodVersion === evidence.methodVersion, 'public projection method identity mismatch.');
  assert(canonicalJson(projection.facts) === canonicalJson(evidence.facts), 'public projection facts differ from normalized evidence.');
  uniqueStrings(projection.limitations, 'publicProjection.limitations', { min: 3, max: 8 });
  const visit = (value, path = 'publicProjection') => {
    if (!value || typeof value !== 'object') return;
    if (Array.isArray(value)) return value.forEach((child, index) => visit(child, `${path}[${index}]`));
    for (const [key, child] of Object.entries(value)) {
      assert(!PROJECTION_PROTECTED_KEYS.has(key), `${path}.${key} exposes protected/internal data.`);
      visit(child, `${path}.${key}`);
    }
  };
  visit(projection);
  const serialized = canonicalJson(projection);
  for (const protectedValue of [request.siteSnapshot.siteRecordDigest, evidence.dataDigest, request.inputDigest, evidence.outputDigest]) {
    assert(!serialized.includes(protectedValue), 'public projection exposes a protected/internal digest.');
  }
}

function validateBoundaries(boundaries) {
  exactKeys(boundaries, BOUNDARY_KEYS, 'boundaries');
  for (const field of ['f3cAdapterImplemented', 'runtimeActivated', 'protectedSiteUsed', 'forecastImplemented', 'rankingImplemented', 'readinessImplemented']) {
    assert(boundaries[field] === false, `boundaries.${field} must remain false in F3-B.`);
  }
  assert(boundaries.externalReferenceCalls === 0, 'F3-B must make zero external-reference calls.');
  assert(boundaries.commandAuthority === 'NONE', 'F3-B command authority must be NONE.');
  assert(boundaries.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'F3-B must preserve local physical Safety Authority.');
}

export function validateF3BContractFixture(fixture) {
  exactKeys(fixture, ROOT_KEYS, 'fixture');
  assert(fixture.schemaVersion === SCHEMA_VERSION && fixture.contractType === CONTRACT_TYPES.fixture, 'fixture identity mismatch.');
  assert(fixture.environment === 'TEST' && fixture.authority === 'NONE', 'fixture must be TEST/NONE.');
  noForbiddenKeys(fixture);
  validateMethodProfile(fixture.methodProfile);
  validateRequest(fixture.request, fixture.methodProfile);
  validateEvidence(fixture.evidence, fixture.request, fixture.methodProfile);
  validateProjection(fixture.publicProjection, fixture.request, fixture.evidence);
  validateBoundaries(fixture.boundaries);
  digestMatches(fixture, 'contractDigest', 'fixture');
  return true;
}
