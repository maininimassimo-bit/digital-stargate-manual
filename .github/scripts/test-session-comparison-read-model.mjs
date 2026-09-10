import test from 'node:test';
import assert from 'node:assert/strict';
import { buildComparisonCandidate, buildComparisonSet } from './session-comparison-read-model.mjs';

const base={sessionId:'S1',source:'fixture',provenanceRef:'evidence:S1',quality:'CURRENT',completeness:'COMPLETE',actionAuthority:'NONE'};

test('calibrated FWHM is comparable',()=>{
  const c=buildComparisonCandidate({...base,dimension:'FWHM',value:2.1,unit:'arcsec',unitSemantics:'ANGULAR_CALIBRATED',angularCalibrationState:'PROVEN'});
  assert.equal(c.comparabilityClass,'COMPARABLE');
  assert.equal(c.authority.actionAuthority,'NONE');
});

test('native uncalibrated FWHM remains context only',()=>{
  const c=buildComparisonCandidate({...base,dimension:'FWHM',value:2.1,unit:'NINA_FILENAME_FWHM_SOURCE_UNIT',unitSemantics:'SOURCE_NATIVE_UNCALIBRATED',angularCalibrationState:'NOT_PROVEN'});
  assert.equal(c.comparabilityClass,'CONTEXT_ONLY');
  assert.equal(c.exclusionReason,'FWHM_ANGULAR_UNIT_NOT_PROVEN');
});

test('missing unit fails closed',()=>{
  const c=buildComparisonCandidate({...base,dimension:'GUIDING_RMS',value:0.7});
  assert.equal(c.comparabilityClass,'UNKNOWN');
});

test('PixInsight unavailable history is not comparable',()=>{
  const c=buildComparisonCandidate({...base,dimension:'PIXINSIGHT_WORKFLOW',value:{observedStepCount:0},unit:'workflow',completeness:'UNAVAILABLE'});
  assert.equal(c.comparabilityClass,'UNAVAILABLE');
});

test('background and final quality stay context-only in F2',()=>{
  assert.equal(buildComparisonCandidate({...base,dimension:'BACKGROUND',value:1200,unit:'ADU'}).comparabilityClass,'CONTEXT_ONLY');
  assert.equal(buildComparisonCandidate({...base,dimension:'FINAL_QUALITY',value:0.8,unit:'score'}).comparabilityClass,'CONTEXT_ONLY');
});

test('comparison set excludes incompatible evidence and requires two comparable candidates',()=>{
  const a={...base,dimension:'SQM',value:20.4,unit:'mag/arcsec2'};
  const b={...base,sessionId:'S2',provenanceRef:'evidence:S2',dimension:'SQM',value:20.7,unit:'mag/arcsec2'};
  const c={...base,sessionId:'S3',provenanceRef:'evidence:S3',dimension:'SQM',value:20.5,unit:'unknown'};
  const set=buildComparisonSet({comparisonSetId:'CMP-1',dimension:'SQM',unit:'mag/arcsec2',candidates:[a,b,c],createdAt:'2026-09-10T12:30:00Z'});
  assert.equal(set.included.length,2);
  assert.equal(set.excluded.length,1);
  assert.equal(set.excluded[0].reason,'UNIT_INCOMPATIBLE');
  assert.equal(set.comparisonState,'COMPARABLE');
});

test('authority escalation is rejected',()=>{
  assert.throws(()=>buildComparisonCandidate({...base,dimension:'SQM',value:20,unit:'mag/arcsec2',actionAuthority:'COMMAND'}));
  assert.throws(()=>buildComparisonCandidate({...base,dimension:'SQM',value:20,unit:'mag/arcsec2',acceptanceAuthority:true}));
});
