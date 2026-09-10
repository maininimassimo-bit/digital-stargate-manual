const freeze = (value) => Object.freeze(value);
const clone = (value) => structuredClone(value);

export const COMPARABILITY = freeze(['COMPARABLE','CONTEXT_ONLY','PARTIAL','UNAVAILABLE','INCOMPATIBLE','UNKNOWN']);

const present = (v) => v !== null && v !== undefined;
const nonEmpty = (v) => typeof v === 'string' && v.trim().length > 0;

function classify(input) {
  if (!present(input.value)) return ['UNAVAILABLE','VALUE_UNAVAILABLE'];
  if (!nonEmpty(input.dimension)) return ['UNKNOWN','DIMENSION_UNRESOLVED'];
  if (!nonEmpty(input.source) || !nonEmpty(input.provenanceRef)) return ['UNKNOWN','PROVENANCE_INSUFFICIENT'];
  if (input.completeness === 'UNAVAILABLE') return ['UNAVAILABLE','SOURCE_COMPLETENESS_UNAVAILABLE'];
  if (input.completeness === 'PARTIAL') return ['PARTIAL','SOURCE_COMPLETENESS_PARTIAL'];
  if (input.quality === 'STALE' || input.quality === 'UNKNOWN') return ['PARTIAL','SOURCE_QUALITY_INSUFFICIENT'];

  if (input.dimension === 'FWHM') {
    if (!nonEmpty(input.unit)) return ['UNKNOWN','UNIT_UNRESOLVED'];
    if (input.unitSemantics === 'SOURCE_NATIVE_UNCALIBRATED' || input.angularCalibrationState === 'NOT_PROVEN') {
      return ['CONTEXT_ONLY','FWHM_ANGULAR_UNIT_NOT_PROVEN'];
    }
    return ['COMPARABLE',null];
  }

  if (input.dimension === 'BACKGROUND') return ['CONTEXT_ONLY','BACKGROUND_NORMALIZATION_NOT_DEFINED'];
  if (input.dimension === 'FINAL_QUALITY') return ['CONTEXT_ONLY','QUALITY_SCORE_OUTSIDE_BKL037_F2'];
  if (input.dimension === 'ERRORS') return ['CONTEXT_ONLY','ERRORS_DESCRIPTIVE_ONLY'];
  if (input.dimension === 'PIXINSIGHT_WORKFLOW') {
    if (input.completeness !== 'COMPLETE') return [input.completeness === 'PARTIAL' ? 'PARTIAL' : 'UNAVAILABLE','PIXINSIGHT_HISTORY_NOT_COMPLETE'];
    return ['COMPARABLE',null];
  }

  if (!nonEmpty(input.unit)) return ['UNKNOWN','UNIT_UNRESOLVED'];
  return ['COMPARABLE',null];
}

export function buildComparisonCandidate(input = {}) {
  if (!nonEmpty(input.sessionId)) throw new Error('sessionId is required.');
  if (input.actionAuthority && input.actionAuthority !== 'NONE') throw new Error('Comparison candidate cannot carry action authority.');
  if (input.acceptanceAuthority === true) throw new Error('Comparison candidate cannot carry acceptance authority.');

  const [comparabilityClass, exclusionReason] = classify(input);
  return freeze({
    schemaVersion:'1.0',
    readModelType:'SESSION_COMPARISON_CANDIDATE',
    consumerMode:'READ_ONLY',
    sessionId:input.sessionId,
    dimension:input.dimension ?? null,
    value:present(input.value) ? clone(input.value) : null,
    unit:input.unit ?? null,
    unitSemantics:input.unitSemantics ?? null,
    angularCalibrationState:input.angularCalibrationState ?? null,
    source:input.source ?? null,
    observedAt:input.observedAt ?? null,
    interval:input.interval ? freeze(clone(input.interval)) : null,
    quality:input.quality ?? 'UNKNOWN',
    completeness:input.completeness ?? 'UNAVAILABLE',
    provenanceRef:input.provenanceRef ?? null,
    comparabilityClass,
    exclusionReason,
    authority:freeze({acceptanceAuthority:false,actionAuthority:'NONE'})
  });
}

export function buildComparisonSet({ comparisonSetId, dimension, unit = null, candidates = [], inclusionRules = [], exclusionRules = [], sourceRefs = [], createdAt } = {}) {
  if (!nonEmpty(comparisonSetId)) throw new Error('comparisonSetId is required.');
  if (!nonEmpty(dimension)) throw new Error('dimension is required.');
  if (!Array.isArray(candidates) || candidates.length < 2) throw new Error('At least two candidates are required.');
  if (!nonEmpty(createdAt)) throw new Error('createdAt is required.');

  const normalized = candidates.map((candidate) => candidate?.readModelType === 'SESSION_COMPARISON_CANDIDATE' ? candidate : buildComparisonCandidate(candidate));
  const included = [];
  const excluded = [];
  for (const candidate of normalized) {
    let reason = candidate.exclusionReason;
    if (candidate.dimension !== dimension) reason = 'DIMENSION_INCOMPATIBLE';
    else if (candidate.comparabilityClass !== 'COMPARABLE') reason = reason ?? `CLASS_${candidate.comparabilityClass}`;
    else if (unit !== null && candidate.unit !== unit) reason = 'UNIT_INCOMPATIBLE';
    if (reason) excluded.push(freeze({sessionId:candidate.sessionId,reason,comparabilityClass:candidate.comparabilityClass}));
    else included.push(candidate);
  }

  return freeze({
    schemaVersion:'1.0',readModelType:'SESSION_COMPARISON_SET',consumerMode:'READ_ONLY',comparisonSetId,dimension,unit,
    sessionIds:freeze(normalized.map((c)=>c.sessionId)),
    inclusionRules:freeze([...inclusionRules]),exclusionRules:freeze([...exclusionRules]),sourceRefs:freeze([...sourceRefs]),createdAt,
    candidates:freeze(normalized),included:freeze(included),excluded:freeze(excluded),
    comparisonState:included.length >= 2 ? 'COMPARABLE' : 'INSUFFICIENT_COMPARABLE_EVIDENCE',
    authority:freeze({acceptanceAuthority:false,actionAuthority:'NONE'})
  });
}
