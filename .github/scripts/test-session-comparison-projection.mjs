import test from 'node:test';
import assert from 'node:assert/strict';
import { buildComparisonCandidate, buildComparisonSet } from './session-comparison-read-model.mjs';
import { buildSessionComparisonProjection } from './session-comparison-projection.mjs';

const candidate = (sessionId, value, extra = {}) => buildComparisonCandidate({
  sessionId, dimension:'SQM', value, unit:'mag/arcsec2', source:'BKL-029', provenanceRef:`sqm:${sessionId}`,
  quality:'CURRENT', completeness:'COMPLETE', ...extra
});

test('numeric comparable cohort yields descriptive summary only', () => {
  const set = buildComparisonSet({comparisonSetId:'CMP-1',dimension:'SQM',unit:'mag/arcsec2',createdAt:'2026-09-10T00:00:00Z',sourceRefs:['BKL-029'],candidates:[candidate('S1',20.1),candidate('S2',20.5),candidate('S3',20.3)]});
  const projection = buildSessionComparisonProjection({projectionId:'CPR-1',comparisonSet:set,generatedAt:'2026-09-10T00:01:00Z'});
  assert.equal(projection.comparisonState,'COMPARABLE');
  assert.deepEqual(projection.descriptiveSummary,{sampleSize:3,minimum:20.1,maximum:20.5,mean:20.3,median:20.3,range:0.3999999999999986});
  assert.equal(projection.authority.acceptanceAuthority,false);
  assert.equal(projection.authority.actionAuthority,'NONE');
  assert.ok(projection.limitations.includes('NO_RANKING_OR_QUALITY_SCORE'));
});

test('excluded candidate remains visible and cannot enter aggregation', () => {
  const unresolved = candidate('S3',20.9,{quality:'UNKNOWN'});
  const set = buildComparisonSet({comparisonSetId:'CMP-2',dimension:'SQM',unit:'mag/arcsec2',createdAt:'2026-09-10T00:00:00Z',candidates:[candidate('S1',20.1),candidate('S2',20.5),unresolved]});
  const projection = buildSessionComparisonProjection({projectionId:'CPR-2',comparisonSet:set,generatedAt:'2026-09-10T00:01:00Z'});
  assert.equal(projection.descriptiveSummary.sampleSize,2);
  assert.equal(projection.exclusions.length,1);
  assert.equal(projection.exclusions[0].sessionId,'S3');
});

test('insufficient comparable evidence produces no summary', () => {
  const set = buildComparisonSet({comparisonSetId:'CMP-3',dimension:'FWHM',unit:'arcsec',createdAt:'2026-09-10T00:00:00Z',candidates:[
    {sessionId:'S1',dimension:'FWHM',value:2.1,unit:'arcsec',source:'BKL-039',provenanceRef:'p1',quality:'CURRENT',completeness:'COMPLETE',angularCalibrationState:'NOT_PROVEN'},
    {sessionId:'S2',dimension:'FWHM',value:2.2,unit:'arcsec',source:'BKL-039',provenanceRef:'p2',quality:'CURRENT',completeness:'COMPLETE',angularCalibrationState:'NOT_PROVEN'}
  ]});
  const projection = buildSessionComparisonProjection({projectionId:'CPR-3',comparisonSet:set,generatedAt:'2026-09-10T00:01:00Z'});
  assert.equal(projection.comparisonState,'INSUFFICIENT_COMPARABLE_EVIDENCE');
  assert.equal(projection.descriptiveSummary,null);
  assert.equal(projection.exclusions.length,2);
});

test('non numeric comparable values remain descriptive without invented aggregation', () => {
  const set = buildComparisonSet({comparisonSetId:'CMP-4',dimension:'WEATHER_STATE',unit:'state',createdAt:'2026-09-10T00:00:00Z',candidates:[
    {sessionId:'S1',dimension:'WEATHER_STATE',value:'CLEAR',unit:'state',source:'weather',provenanceRef:'w1',quality:'CURRENT',completeness:'COMPLETE'},
    {sessionId:'S2',dimension:'WEATHER_STATE',value:'CLOUDY',unit:'state',source:'weather',provenanceRef:'w2',quality:'CURRENT',completeness:'COMPLETE'}
  ]});
  const projection = buildSessionComparisonProjection({projectionId:'CPR-4',comparisonSet:set,generatedAt:'2026-09-10T00:01:00Z'});
  assert.equal(projection.comparisonState,'COMPARABLE');
  assert.equal(projection.descriptiveSummary,null);
  assert.ok(projection.limitations.includes('NUMERIC_AGGREGATION_NOT_APPLICABLE'));
});

test('authority escalation is rejected', () => {
  assert.throws(()=>buildSessionComparisonProjection({projectionId:'CPR-5',generatedAt:'2026-09-10T00:01:00Z',comparisonSet:{readModelType:'SESSION_COMPARISON_SET',consumerMode:'READ_ONLY',included:[],excluded:[],authority:{acceptanceAuthority:true,actionAuthority:'NONE'}}}),/acceptance authority/);
});
