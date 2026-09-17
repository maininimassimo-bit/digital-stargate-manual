import crypto from 'node:crypto';

export const F5_METHOD_ID = 'BKL031-F5-EXPLAINABLE-RANKING';
export const F5_METHOD_VERSION = '1.0';
export const FACTORS = Object.freeze([
  Object.freeze({ id: 'ASTRONOMICAL_ALTITUDE', weight: 0.45, min: 0, max: 90, direction: 'HIGHER_IS_BETTER', unit: 'deg' }),
  Object.freeze({ id: 'LUNAR_SEPARATION', weight: 0.25, min: 0, max: 180, direction: 'HIGHER_IS_BETTER', unit: 'deg' }),
  Object.freeze({ id: 'FORECAST_EVIDENCE_COMPLETENESS', weight: 0.20, min: 0, max: 1, direction: 'HIGHER_IS_BETTER', unit: 'fraction' }),
  Object.freeze({ id: 'TARGET_IDENTITY_VALIDATION', weight: 0.10, min: 0, max: 1, direction: 'HIGHER_IS_BETTER', unit: 'fraction' })
]);

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonicalJson(value[k])}`).join(',')}}`;
  return JSON.stringify(value);
}

export function sha256(value) {
  return crypto.createHash('sha256').update(typeof value === 'string' ? value : canonicalJson(value), 'utf8').digest('hex');
}

function assertClosedObject(value, allowed, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${label} must be an object`);
  for (const key of Object.keys(value)) if (!allowed.includes(key)) throw new Error(`${label} unknown property: ${key}`);
}

function normalize(value, factor) {
  if (!Number.isFinite(value)) throw new Error(`${factor.id} value must be finite`);
  if (value < factor.min || value > factor.max) throw new Error(`${factor.id} value out of range`);
  const span = factor.max - factor.min;
  const base = (value - factor.min) / span;
  return factor.direction === 'HIGHER_IS_BETTER' ? base : 1 - base;
}

export function validateFixture(fixture) {
  assertClosedObject(fixture, ['schemaVersion','fixtureId','environment','authority','consumerMode','method','lineage','candidates','limitations'], 'fixture');
  if (fixture.schemaVersion !== '1.0') throw new Error('unsupported schemaVersion');
  if (fixture.environment !== 'EVALUATION' || fixture.authority !== 'NONE' || fixture.consumerMode !== 'READ_ONLY') throw new Error('authority boundary mismatch');
  if (fixture.method?.id !== F5_METHOD_ID || fixture.method?.version !== F5_METHOD_VERSION) throw new Error('method mismatch');
  if (fixture.method?.readinessAuthority !== false || fixture.method?.actionAuthority !== 'NONE' || fixture.method?.safetyAuthority !== 'LOCAL_PHYSICAL_INTERLOCKS') throw new Error('method authority escalation');
  if (!Array.isArray(fixture.candidates) || fixture.candidates.length < 2 || fixture.candidates.length > 5) throw new Error('candidate count must be 2..5');
  const ids = new Set();
  for (const candidate of fixture.candidates) {
    assertClosedObject(candidate, ['targetKey','targetId','canonicalName','identityState','evidence'], 'candidate');
    if (ids.has(candidate.targetKey)) throw new Error('duplicate targetKey');
    ids.add(candidate.targetKey);
    if (candidate.identityState !== 'validated') throw new Error('candidate identity must be validated');
    assertClosedObject(candidate.evidence, ['astronomicalAltitudeDeg','lunarSeparationDeg','forecastEvidenceCompleteness','targetIdentityValidation'], 'candidate.evidence');
    if (candidate.evidence.targetIdentityValidation !== 1) throw new Error('identity validation must equal 1');
    for (const factor of FACTORS) {
      const map = {
        ASTRONOMICAL_ALTITUDE: 'astronomicalAltitudeDeg',
        LUNAR_SEPARATION: 'lunarSeparationDeg',
        FORECAST_EVIDENCE_COMPLETENESS: 'forecastEvidenceCompleteness',
        TARGET_IDENTITY_VALIDATION: 'targetIdentityValidation'
      };
      normalize(candidate.evidence[map[factor.id]], factor);
    }
  }
  const weight = FACTORS.reduce((sum, f) => sum + f.weight, 0);
  if (Math.abs(weight - 1) > 1e-12) throw new Error('factor weights must sum to 1');
  return fixture;
}

export function rankFixture(fixture) {
  validateFixture(fixture);
  const fieldByFactor = {
    ASTRONOMICAL_ALTITUDE: 'astronomicalAltitudeDeg',
    LUNAR_SEPARATION: 'lunarSeparationDeg',
    FORECAST_EVIDENCE_COMPLETENESS: 'forecastEvidenceCompleteness',
    TARGET_IDENTITY_VALIDATION: 'targetIdentityValidation'
  };
  const evaluated = fixture.candidates.map(candidate => {
    const factors = FACTORS.map(def => {
      const rawValue = candidate.evidence[fieldByFactor[def.id]];
      const normalizedValue = normalize(rawValue, def);
      const contribution = normalizedValue * def.weight;
      return { id: def.id, rawValue, unit: def.unit, normalizedValue: Number(normalizedValue.toFixed(8)), weight: def.weight, contribution: Number(contribution.toFixed(8)) };
    });
    const score = Number((100 * factors.reduce((sum, f) => sum + f.contribution, 0)).toFixed(4));
    return { targetKey: candidate.targetKey, targetId: candidate.targetId, canonicalName: candidate.canonicalName, score, factors };
  });
  evaluated.sort((a, b) => b.score - a.score || a.targetKey.localeCompare(b.targetKey));
  const results = evaluated.map((item, index) => ({ rank: index + 1, ...item }));
  const projection = {
    schemaVersion: '1.0',
    projectionType: 'BKL031_F5_EXPLAINABLE_RANKING_PROJECTION',
    projectionId: `BKL031-F5-${sha256({ fixtureId: fixture.fixtureId, results }).slice(0, 24).toUpperCase()}`,
    environment: 'EVALUATION',
    authority: 'NONE',
    consumerMode: 'READ_ONLY',
    method: { id: F5_METHOD_ID, version: F5_METHOD_VERSION, factorDefinitions: FACTORS },
    lineage: fixture.lineage,
    results,
    limitations: fixture.limitations,
    boundary: { readinessAuthority: false, actionAuthority: 'NONE', safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS', automaticTargetSelection: false, schedulingAuthority: false, commandAuthority: 'NONE' }
  };
  projection.projectionDigest = sha256(projection);
  return projection;
}
