import test from 'node:test';
import assert from 'node:assert/strict';
import {inspectPublicSample} from './reference.mjs';
const gaia='source_id,ref_epoch,ra,dec,pmra,pmdec\n137333365999306624,2016.0,45.003085,35.314218,2.31,-0.48\n';
const ps1='objID,raMean,decMean,nDetections,gMeanPSFMag,rMeanPSFMag\r\n173222108164170026,210.81642777,54.34944415,0,-999.0,-999.0\r\n';
test('64-bit catalog IDs remain exact strings; astrometric epochs stay TCB',()=>{
  const result=inspectPublicSample(gaia,'GAIA_DR3_PUBLIC_SAMPLE');
  assert.equal(result.sources[0].catalogId,'137333365999306624');
  assert.equal(result.sources[0].astrometricEpoch.timeScale,'TCB');
  assert.equal(result.sources[0].properMotion.raConvention,'MU_ALPHA_COS_DEC');
  assert.equal(result.crossMatchPerformed,false); assert.equal(result.candidateClassification,'NOT_EVALUATED');
});
test('PS1 sentinel is unavailable magnitude, never zero or new-source evidence',()=>{
  const result=inspectPublicSample(ps1,'PS1_DR2_PUBLIC_SAMPLE');
  assert.deepEqual(result.sources[0].magnitudes,{g:null,r:null});
  assert.equal(result.sources[0].catalogDetectionCount,0);
  assert.equal(result.sources[0].measurementQuality,'UNKNOWN');
  assert.equal(result.catalogCompleteness,'NOT_ESTABLISHED');
  assert.equal(result.photometryPerformed,false);
  assert.deepEqual(inspectPublicSample(ps1.replaceAll('-999.0','-9.99e2'),'PS1_DR2_PUBLIC_SAMPLE').sources[0].magnitudes,{g:null,r:null});
});
test('missing proper motion remains unknown, not stationary',()=>{
  const result=inspectPublicSample(gaia.replace('2.31,-0.48',','),'GAIA_DR3_PUBLIC_SAMPLE');
  assert.equal(result.sources[0].properMotion.pmraMasPerYear,null);
  assert.equal(result.sources[0].epochPropagation,'NOT_PERFORMED_COVARIANCE_AND_METHOD_PENDING');
});
test('quoted values accepted, malformed/duplicate headers and rows reject',()=>{
  assert.equal(inspectPublicSample(gaia.replace('2016.0','"2016.0"'),'GAIA_DR3_PUBLIC_SAMPLE').sources.length,1);
  for(const text of [gaia.replace('pmra,pmdec','pmra,pmra'),gaia.replace('2016.0','"2016.0"garbage'),gaia.replace('2.31,-0.48','2.31'),gaia+'137333365999306624,2016.0,45,35,2,1\n']) assert.throws(()=>inspectPublicSample(text,'GAIA_DR3_PUBLIC_SAMPLE'),/INVALID_PUBLIC_REFERENCE_SAMPLE/);
});
test('HTML, wrong profiles, nonfinite coordinates and out-of-range sky reject',()=>{
  for(const text of ['<html>error</html>',gaia.replace('45.003085','NaN'),gaia.replace('45.003085','360'),gaia.replace('35.314218','91')]) assert.throws(()=>inspectPublicSample(text,'GAIA_DR3_PUBLIC_SAMPLE'),/INVALID_PUBLIC_REFERENCE_SAMPLE/);
  assert.throws(()=>inspectPublicSample(gaia,'LATEST'),/INVALID_PUBLIC_REFERENCE_SAMPLE/);
});
test('bounded sample refuses bulk results rather than claiming completeness',()=>{
  const header=gaia.split('\n')[0]+'\n';
  const rows=Array.from({length:101},(_,i)=>`${i+1},2016,45,35,2,1\n`).join('');
  assert.throws(()=>inspectPublicSample(header+rows,'GAIA_DR3_PUBLIC_SAMPLE'),/INVALID_PUBLIC_REFERENCE_SAMPLE/);
});
