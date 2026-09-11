import { contentDigest } from './scientific-data-quality-scoring.mjs';

export const F5_VALIDATION_TYPE = 'SCIENTIFIC_DATA_QUALITY_REAL_EVIDENCE_VALIDATION';
export const F5_VALIDATION_ID = 'BKL041-F5-REAL-EVIDENCE-V1';

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const finite = value => typeof value === 'number' && Number.isFinite(value);
const ratio = (value, total) => total ? Number((value / total).toFixed(6)) : 0;
const freeze = value => {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    Object.freeze(value);
    Object.values(value).forEach(freeze);
  }
  return value;
};

export const F5_READINESS_POLICY = Object.freeze({
  policyId: 'DSG-SCIENTIFIC-QUALITY-PRODUCTION-READINESS-1',
  policyVersion: '1.0.0',
  purpose: 'PRODUCTION_CALIBRATION_READINESS_NOT_SCIENTIFIC_QUALITY_THRESHOLD',
  requirements: Object.freeze({
    minimumImportedSessions: 30,
    minimumKnownTargets: 3,
    minimumAvailableAssessmentRatio: 0.8,
    maximumInvalidAssessmentCount: 0,
    minimumSqmEvidenceRatio: 0.8,
    requiredGuidingTemporalCoverageState: 'GOVERNED_NON_ZERO',
    requiredGroundTruthState: 'AVAILABLE',
    requiredProfileState: 'CALIBRATED_ON_REAL_EVIDENCE'
  })
});

function result(id, observed, required, pass, reason) {
  return { criterionId: id, status: pass ? 'PASS' : 'FAIL', observed, required, reason };
}

export function buildRealEvidenceValidation(catalog, projection) {
  assert(catalog?.catalogStatus === 'VERSIONED_ANALYTICS_PROJECTION', 'Catalog authority/status is not supported.');
  assert(Array.isArray(catalog.sessions), 'Catalog sessions[] is required.');
  assert(projection?.projectionType === 'SCIENTIFIC_DATA_QUALITY_PROJECTION', 'F4 projection is required.');
  assert(projection?.projectionState === 'EXPERIMENTAL_NOT_ACCEPTED', 'Only the experimental F4 projection may be validated.');
  assert(projection?.sourceCatalog?.digest === contentDigest(catalog), 'F4 projection is stale against the catalog.');
  assert(projection?.summary?.totalSessions === catalog.sessions.length, 'Projection/catalog session count mismatch.');
  assert(projection?.authority?.productionUseAuthorized === false, 'Production authority escalation is forbidden.');

  const sessions = [...catalog.sessions].sort((a, b) => a.sessionId.localeCompare(b.sessionId));
  const assessments = [...projection.assessments].sort((a, b) => a.sessionId.localeCompare(b.sessionId));
  assert(JSON.stringify(sessions.map(x => x.sessionId)) === JSON.stringify(assessments.map(x => x.sessionId)), 'Projection/catalog session identity mismatch.');
  const knownTargets = [...new Set(sessions.map(x => x.target).filter(x => x && x !== 'UNKNOWN'))].sort();
  const targetDistribution = Object.fromEntries([...new Set(sessions.map(x => x.target || 'UNKNOWN'))].sort().map(target => [target, sessions.filter(x => (x.target || 'UNKNOWN') === target).length]));
  const available = assessments.filter(x => x.projectionRecordState === 'AVAILABLE').length;
  const unavailable = assessments.filter(x => x.projectionRecordState === 'UNAVAILABLE').length;
  const invalid = assessments.filter(x => x.projectionRecordState === 'INVALID').length;
  const count = predicate => sessions.filter(predicate).length;
  const guidingWithNonZeroCoverage = assessments.filter(item => item.inputEvidence?.some(e => e.dimension === 'GUIDING_STABILITY' && finite(e.coverage) && e.coverage > 0)).length;
  const r = F5_READINESS_POLICY.requirements;

  const results = [
    result('MINIMUM_IMPORTED_SESSIONS', sessions.length, r.minimumImportedSessions, sessions.length >= r.minimumImportedSessions, 'A production calibration cohort requires broader repeated evidence.'),
    result('MINIMUM_KNOWN_TARGET_DIVERSITY', knownTargets.length, r.minimumKnownTargets, knownTargets.length >= r.minimumKnownTargets, 'Target diversity limits generalization and must exclude UNKNOWN.'),
    result('AVAILABLE_ASSESSMENT_RATIO', ratio(available, sessions.length), r.minimumAvailableAssessmentRatio, ratio(available, sessions.length) >= r.minimumAvailableAssessmentRatio, 'Unavailable or invalid records cannot silently enter calibration.'),
    result('INVALID_ASSESSMENT_COUNT', invalid, r.maximumInvalidAssessmentCount, invalid <= r.maximumInvalidAssessmentCount, 'Out-of-profile observations require a newly calibrated profile, not clamping.'),
    result('SQM_EVIDENCE_RATIO', ratio(count(x => x.sqm?.state === 'AVAILABLE'), sessions.length), r.minimumSqmEvidenceRatio, ratio(count(x => x.sqm?.state === 'AVAILABLE'), sessions.length) >= r.minimumSqmEvidenceRatio, 'Sky-quality evidence must cover most of the declared cohort.'),
    result('GUIDING_TEMPORAL_COVERAGE', guidingWithNonZeroCoverage ? 'GOVERNED_NON_ZERO' : 'UNAVAILABLE', r.requiredGuidingTemporalCoverageState, guidingWithNonZeroCoverage === sessions.length, 'Sample count without a governed temporal denominator is insufficient.'),
    result('REFERENCE_GROUND_TRUTH', 'UNAVAILABLE', r.requiredGroundTruthState, false, 'The repository contains no accepted final scientific quality ground truth.'),
    result('PROFILE_CALIBRATION_STATE', projection.profile.profileState, r.requiredProfileState, projection.profile.profileState === r.requiredProfileState, 'The F3 profile is a synthetic demonstrator and cannot be promoted implicitly.')
  ];
  const failed = results.filter(x => x.status === 'FAIL');

  const validation = {
    schemaVersion: '1.0',
    validationType: F5_VALIDATION_TYPE,
    validationId: F5_VALIDATION_ID,
    validationState: 'COMPLETE',
    generatedAt: projection.generatedAt,
    sourceCatalog: {
      path: 'docs/data/scientific-session-catalog.json',
      digest: contentDigest(catalog),
      sessionCount: sessions.length,
      sessionIds: sessions.map(x => x.sessionId)
    },
    sourceProjection: {
      path: 'docs/data/scientific-data-quality-projection.json',
      digest: projection.projectionDigest,
      projectionId: projection.projectionId,
      profileId: projection.profile.profileId,
      profileVersion: projection.profile.profileVersion
    },
    cohort: {
      cohortId: 'ALL-CANONICAL-IMPORTED-SESSIONS-F5',
      selectionRule: 'ALL_SESSIONS_IN_CANONICAL_CATALOG_NO_OUTCOME_FILTERING',
      sessionCount: sessions.length,
      observedFrom: sessions.map(x => x.start).filter(Boolean).sort()[0] ?? null,
      observedThrough: sessions.map(x => x.end ?? x.start).filter(Boolean).sort().at(-1) ?? null,
      knownTargets,
      targetDistribution,
      evidenceAvailability: {
        sourceMetrics: count(x => x.evidenceState === 'SOURCE_METRICS_AVAILABLE'),
        metadataLineage: count(x => ['REGISTERED', 'CANONICAL_EVIDENCE'].includes(x.metadataState)),
        acquisitionCompletion: count(x => finite(x.completionPct)),
        guidingRms: count(x => x.guiding?.state === 'AVAILABLE'),
        guidingTemporalCoverage: guidingWithNonZeroCoverage,
        sqm: count(x => x.sqm?.state === 'AVAILABLE')
      },
      assessmentStates: { available, unavailable, invalid }
    },
    acceptancePolicy: F5_READINESS_POLICY,
    results,
    summary: { passedCriteria: results.length - failed.length, failedCriteria: failed.length, totalCriteria: results.length },
    decision: {
      capabilityAcceptance: 'ACCEPTED_AS_READ_ONLY_EXPERIMENTAL_WITH_RETAINED_LIMITATIONS',
      productionReadiness: failed.length ? 'NOT_READY_FOR_PRODUCTION' : 'READY_FOR_PRODUCTION_REVIEW',
      productionProfileAuthorized: false,
      productionUseAuthorized: false,
      reasonCodes: failed.map(x => x.criterionId)
    },
    biasDisclosure: [
      'AVAILABLE_ASSESSMENTS_ARE_ONLY_FOR_M27_IN_THE_CURRENT_COHORT',
      'TARGET_DISTRIBUTION_IS_STRONGLY_IMBALANCED',
      'SYNTHETIC_GUIDING_BOUNDS_REJECT_REAL_LOW_RMS_VALUES',
      'NO_ACCEPTED_FINAL_SCIENTIFIC_OUTCOME_LABEL_EXISTS',
      'MISSING_EVIDENCE_IS_NOT_MISSING_AT_RANDOM'
    ],
    limitations: [
      'F5_ACCEPTS_THE_EXPERIMENTAL_READ_ONLY_CAPABILITY_NOT_A_PRODUCTION_PROFILE',
      'READINESS_CRITERIA_ARE_GOVERNANCE_GATES_NOT_IMAGE_QUALITY_THRESHOLDS',
      'NO_RANKING_RECOMMENDATION_AUTOMATIC_ACCEPTANCE_OR_SAFETY_AUTHORITY'
    ],
    authority: {
      consumerMode: 'READ_ONLY',
      productionUseAuthorized: false,
      acceptanceAuthority: false,
      actionAuthority: 'NONE',
      safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS'
    }
  };
  validation.validationDigest = contentDigest(validation);
  return freeze(validation);
}
