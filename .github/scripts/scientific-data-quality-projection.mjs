import { buildScientificDataQualityAssessment, contentDigest, validateScoringProfile } from './scientific-data-quality-scoring.mjs';

export const F4_PROJECTION_SCHEMA_VERSION = '1.0';
export const F4_PROJECTION_TYPE = 'SCIENTIFIC_DATA_QUALITY_PROJECTION';
export const F4_PROJECTION_ID = 'BKL041-F4-CATALOG-V1';
export const F4_PROJECTION_STATE = 'EXPERIMENTAL_NOT_ACCEPTED';
export const F4_SOURCE_CATALOG_PATH = 'docs/data/scientific-session-catalog.json';

const AUTHORITY = Object.freeze({
  consumerMode: 'READ_ONLY',
  productionUseAuthorized: false,
  acceptanceAuthority: false,
  actionAuthority: 'NONE',
  safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS'
});

const nonEmpty = value => typeof value === 'string' && value.trim().length > 0;
const finite = value => typeof value === 'number' && Number.isFinite(value);
const freeze = value => {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    Object.freeze(value);
    Object.values(value).forEach(freeze);
  }
  return value;
};
const assert = (condition, message) => { if (!condition) throw new Error(message); };

function evidence(dimension, value, unit, coverage, sourceRef) {
  return {
    dimension,
    value,
    unit,
    evidenceClass: 'DECLARED',
    quality: 'VALID',
    completeness: 'COMPLETE',
    coverage,
    calibrationState: 'NOT_APPLICABLE',
    eligibility: 'ELIGIBLE_FOR_FUTURE_NORMALIZATION',
    evidenceRefs: [sourceRef]
  };
}

export function mapCatalogSessionToF3Inputs(session) {
  assert(session && typeof session === 'object' && !Array.isArray(session), 'Catalog session must be an object.');
  assert(nonEmpty(session.sessionId), 'Catalog sessionId is required.');
  const source = nonEmpty(session.sourceMetricsPath) ? session.sourceMetricsPath.trim() : null;
  const inputs = [];

  const lineageComplete = source
    && session.evidenceState === 'SOURCE_METRICS_AVAILABLE'
    && session.manifestState === 'VERSIONED'
    && ['REGISTERED', 'CANONICAL_EVIDENCE'].includes(session.metadataState);
  if (lineageComplete) inputs.push(evidence('METADATA_LINEAGE_INTEGRITY', 1, 'ratio', 1, `${source}#scientific`));

  if (source && finite(session.completionPct) && session.lightStarted > 0) {
    inputs.push(evidence('ACQUISITION_COMPLETION', session.completionPct / 100, 'ratio', 1, `${source}#nina`));
  }

  const guiding = session.guiding;
  if (source && guiding?.state === 'AVAILABLE' && finite(guiding.rmsTotalArcsec) && guiding.sampleCount > 0) {
    // The catalog does not expose a governed temporal denominator for guiding.
    // Coverage therefore remains zero; the score is experimental and confidence exposes the gap.
    inputs.push(evidence('GUIDING_STABILITY', guiding.rmsTotalArcsec, 'arcsec', 0, `${source}#phd2`));
  }

  const sqm = session.sqm;
  if (source && sqm?.state === 'AVAILABLE' && finite(sqm.medianMagArcsec2) && finite(sqm.temporalCoverage)) {
    inputs.push(evidence('SKY_QUALITY_COVERAGE', sqm.medianMagArcsec2, 'mag/arcsec2', sqm.temporalCoverage, `${source}#sqm`));
  }

  return freeze(inputs);
}

function classifyFailure(error) {
  const message = String(error?.message ?? error ?? 'UNKNOWN_PROJECTION_FAILURE');
  if (/outside \[.*\].*REJECT/.test(message)) return { code: 'PROFILE_VALUE_OUT_OF_RANGE', message };
  return { code: 'ASSESSMENT_REJECTED_FAIL_CLOSED', message };
}

function projectSession(session, profile) {
  const inputs = mapCatalogSessionToF3Inputs(session);
  const common = {
    sessionId: session.sessionId,
    target: nonEmpty(session.target) ? session.target : 'UNKNOWN',
    observedAt: session.end ?? session.start ?? null,
    sourceMetricsPath: nonEmpty(session.sourceMetricsPath) ? session.sourceMetricsPath : null,
    inputEvidence: inputs
  };
  try {
    const assessment = buildScientificDataQualityAssessment({
      profile,
      sessionId: session.sessionId,
      dimensions: inputs,
      authority: {
        consumerMode: AUTHORITY.consumerMode,
        acceptanceAuthority: AUTHORITY.acceptanceAuthority,
        actionAuthority: AUTHORITY.actionAuthority,
        safetyAuthority: AUTHORITY.safetyAuthority
      }
    });
    return {
      ...common,
      projectionRecordState: assessment.assessmentState,
      assessment,
      generationError: null
    };
  } catch (error) {
    return {
      ...common,
      projectionRecordState: 'INVALID',
      assessment: null,
      generationError: classifyFailure(error)
    };
  }
}

export function buildScientificDataQualityProjection(catalog, profile, { generatedAt } = {}) {
  assert(catalog && typeof catalog === 'object' && !Array.isArray(catalog), 'Scientific session catalog is required.');
  assert(catalog.catalogStatus === 'VERSIONED_ANALYTICS_PROJECTION', 'Scientific session catalog authority/status is not supported.');
  assert(nonEmpty(catalog.schemaVersion), 'Scientific session catalog schemaVersion is required.');
  assert(Array.isArray(catalog.sessions), 'Scientific session catalog sessions[] is required.');
  assert(nonEmpty(generatedAt) && Number.isFinite(Date.parse(generatedAt)), 'generatedAt must be an ISO date-time.');
  validateScoringProfile(profile);

  const sessions = [...catalog.sessions].sort((a, b) => String(a.sessionId ?? '').localeCompare(String(b.sessionId ?? '')));
  const ids = sessions.map(session => session.sessionId);
  assert(ids.every(nonEmpty) && new Set(ids).size === ids.length, 'Catalog session IDs must be unique and non-empty.');
  const assessments = sessions.map(session => projectSession(session, profile));
  const count = state => assessments.filter(item => item.projectionRecordState === state).length;

  const projection = {
    schemaVersion: F4_PROJECTION_SCHEMA_VERSION,
    projectionType: F4_PROJECTION_TYPE,
    projectionId: F4_PROJECTION_ID,
    projectionState: F4_PROJECTION_STATE,
    generatedAt,
    sourceCatalog: {
      path: F4_SOURCE_CATALOG_PATH,
      schemaVersion: catalog.schemaVersion,
      catalogStatus: catalog.catalogStatus,
      digest: contentDigest(catalog),
      sessionCount: sessions.length,
      sessionIds: ids
    },
    profile: {
      profileId: profile.profileId,
      profileVersion: profile.profileVersion,
      profileState: profile.profileState,
      profileDigest: profile.profileDigest,
      algorithmId: profile.algorithmId,
      algorithmVersion: profile.algorithmVersion
    },
    summary: {
      totalSessions: assessments.length,
      availableAssessments: count('AVAILABLE'),
      unavailableAssessments: count('UNAVAILABLE'),
      invalidAssessments: count('INVALID')
    },
    assessments,
    limitations: [
      'EXPERIMENTAL_F4_NOT_ACCEPTED_FOR_PRODUCTION_USE',
      'SYNTHETIC_DEMONSTRATOR_PROFILE_NOT_SCIENTIFIC_CALIBRATION',
      'GUIDING_TEMPORAL_COVERAGE_NOT_REPRESENTED_IN_SOURCE_CATALOG',
      'NO_RANKING_THRESHOLD_RECOMMENDATION_OR_AUTOMATIC_ACCEPTANCE',
      'NO_SAFETY_OR_ACTION_AUTHORITY'
    ],
    publication: {
      trigger: 'ANALYZE_SESSION_AUTOMATIC_AFTER_COMPLETE_IMPORT',
      atomicCommitPath: F4_SOURCE_CATALOG_PATH,
      freshnessMethod: 'CANONICAL_SOURCE_CATALOG_SHA256_MATCH'
    },
    authority: AUTHORITY
  };
  projection.projectionDigest = contentDigest(projection);
  return freeze(projection);
}
