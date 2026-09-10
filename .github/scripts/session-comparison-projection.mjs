const freeze = (value) => Object.freeze(value);

function finiteNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function assertComparisonSet(set) {
  if (!set || set.readModelType !== 'SESSION_COMPARISON_SET') throw new Error('SESSION_COMPARISON_SET is required.');
  if (set.consumerMode !== 'READ_ONLY') throw new Error('Comparison set must be READ_ONLY.');
  if (set.authority?.acceptanceAuthority === true) throw new Error('Comparison projection cannot consume acceptance authority.');
  if (set.authority?.actionAuthority && set.authority.actionAuthority !== 'NONE') throw new Error('Comparison projection cannot consume action authority.');
}

function summarizeNumeric(included) {
  const values = included.map((candidate) => candidate.value);
  if (!values.every(finiteNumber)) return null;
  const sorted = [...values].sort((a,b)=>a-b);
  const sum = values.reduce((acc,value)=>acc+value,0);
  const middle = Math.floor(sorted.length / 2);
  const median = sorted.length % 2 ? sorted[middle] : (sorted[middle-1] + sorted[middle]) / 2;
  return freeze({
    sampleSize:values.length,
    minimum:sorted[0],
    maximum:sorted[sorted.length-1],
    mean:sum / values.length,
    median,
    range:sorted[sorted.length-1] - sorted[0]
  });
}

export function buildSessionComparisonProjection({ projectionId, comparisonSet, generatedAt } = {}) {
  if (typeof projectionId !== 'string' || projectionId.trim() === '') throw new Error('projectionId is required.');
  if (typeof generatedAt !== 'string' || generatedAt.trim() === '') throw new Error('generatedAt is required.');
  assertComparisonSet(comparisonSet);

  const included = Array.isArray(comparisonSet.included) ? comparisonSet.included : [];
  const excluded = Array.isArray(comparisonSet.excluded) ? comparisonSet.excluded : [];
  const comparable = comparisonSet.comparisonState === 'COMPARABLE' && included.length >= 2;
  const numericSummary = comparable ? summarizeNumeric(included) : null;

  return freeze({
    schemaVersion:'1.0',
    projectionType:'SESSION_COMPARISON_PROJECTION',
    consumerMode:'READ_ONLY',
    projectionId,
    generatedAt,
    comparisonSetId:comparisonSet.comparisonSetId,
    dimension:comparisonSet.dimension,
    unit:comparisonSet.unit,
    comparisonState:comparable ? 'COMPARABLE' : 'INSUFFICIENT_COMPARABLE_EVIDENCE',
    includedSessions:freeze(included.map((candidate)=>freeze({
      sessionId:candidate.sessionId,
      value:candidate.value,
      unit:candidate.unit,
      provenanceRef:candidate.provenanceRef,
      quality:candidate.quality,
      completeness:candidate.completeness
    }))),
    exclusions:freeze(excluded.map((item)=>freeze({...item}))),
    descriptiveSummary:numericSummary,
    limitations:freeze([
      ...(numericSummary ? [] : ['NUMERIC_AGGREGATION_NOT_APPLICABLE']),
      'DESCRIPTIVE_ONLY_NOT_ACCEPTANCE_THRESHOLD',
      'NO_RANKING_OR_QUALITY_SCORE',
      'NO_SAFETY_OR_ACTION_AUTHORITY'
    ]),
    lineage:freeze({comparisonSetId:comparisonSet.comparisonSetId,sourceRefs:freeze([...(comparisonSet.sourceRefs ?? [])])}),
    authority:freeze({acceptanceAuthority:false,actionAuthority:'NONE'})
  });
}
