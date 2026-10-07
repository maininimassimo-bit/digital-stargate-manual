import test from 'node:test';
import assert from 'node:assert/strict';
import {CONTRACT, parseIntake, inspectIntake} from './contract.mjs';
const sha = letter => letter.repeat(64);
function fixture() {
  return {kind: CONTRACT, classification: 'PRIVATE', origin: 'SYNTHETIC_TEST',
    asset: {assetId:'SYNTHETIC_MASTER',revision:1,sha256:sha('a'),byteSize:1000,format:'FITS',channels:1,linearity:'VERIFIED_LINEAR'},
    acquisition: {status:'KNOWN',intervals:[{startUtc:'2026-01-01T00:00:00Z',endUtc:'2026-01-01T00:01:00Z'}],evidenceSha256:sha('b')},
    passband:{name:'TEST_R',class:'BROADBAND',responseSha256:sha('c')},
    astrometry:{status:'VERIFIED',frame:'ICRS',solutionSha256:sha('d')},
    processing:{lineage:'VERIFIED',journalSha256:sha('e'),measurementAlterations:[]},
    independentEvidence:[{assetId:'SYNTHETIC_SPLIT',sha256:sha('f'),independence:'VERIFIED_DISJOINT'}]};
}
test('structural success never grants analysis, discovery or consent', () => {
  const result=inspectIntake(parseIntake(JSON.stringify(fixture())));
  assert.equal(result.state,'NO_ANALYSIS_EXECUTED'); assert.equal(result.scientificClassification,'NOT_EVALUATED');
  assert.equal(result.operationalGate,'OWNER_CONTRACT_DECISIONS_PENDING'); assert.equal(result.externalRequests,0);
  assert.deepEqual(result.reasons,['SYNTHETIC_NOT_REAL_EVIDENCE']);
});
test('unknown historic epoch stays unknown; no invented session or timestamp', () => {
  const data=fixture(); data.origin='EXTERNAL_RETROSPECTIVE'; data.acquisition={status:'UNKNOWN',intervals:[],evidenceSha256:null};
  const result=inspectIntake(parseIntake(JSON.stringify(data)));
  assert.ok(result.reasons.includes('ACQUISITION_EPOCH_UNKNOWN'));
  data.sessionId='invented'; assert.throws(()=>parseIntake(JSON.stringify(data)),/INVALID_S1_INTAKE/);
});
test('palette and altered final image cannot masquerade as measurement master', () => {
  const data=fixture(); data.asset.format='JPEG'; data.asset.channels=3; data.asset.linearity='NONLINEAR';
  data.passband.class='PALETTE'; data.processing.measurementAlterations=['STRETCH','DENOISE'];
  const result=inspectIntake(parseIntake(JSON.stringify(data)));
  for(const code of ['LINEARITY_NOT_VERIFIED','MEASUREMENT_INPUT_NOT_MONO_SCIENTIFIC','PASSBAND_NOT_MEASURABLE','MEASUREMENT_ALTERED_OR_UNKNOWN']) assert.ok(result.reasons.includes(code));
});
test('duplicate keys including escaped spellings reject', () => {
  assert.throws(()=>parseIntake('{"kind":1,"k\\u0069nd":2}'),/INVALID_S1_INTAKE/);
  const text=JSON.stringify(fixture()).replace('"channels":1','"channels":1,"channels":3');
  assert.throws(()=>parseIntake(text),/INVALID_S1_INTAKE/);
});
test('nonfinite, oversized, deeply nested and trailing inputs reject', () => {
  for(const text of ['1e999', ' '.repeat(65537), '['.repeat(14)+'0'+']'.repeat(14),JSON.stringify(fixture())+' null']) assert.throws(()=>parseIntake(text),/INVALID_S1_INTAKE/);
});
test('invalid calendar, reversed and overlapping acquisition intervals reject', () => {
  for(const intervals of [[{startUtc:'2026-02-30T00:00:00Z',endUtc:'2026-03-03T00:00:00Z'}],
    [{startUtc:'2026-01-02T00:00:00Z',endUtc:'2026-01-01T00:00:00Z'}],
    [{startUtc:'2026-01-01T00:00:00Z',endUtc:'2026-01-02T00:00:00Z'},{startUtc:'2026-01-02T00:00:00Z',endUtc:'2026-01-03T00:00:00Z'}]]) {
    const data=fixture(); data.acquisition.intervals=intervals; assert.throws(()=>parseIntake(JSON.stringify(data)),/INVALID_S1_INTAKE/);
  }
});
test('duplicated master is not an independent confirmation', () => {
  const data=fixture(); data.independentEvidence[0].sha256=data.asset.sha256;
  assert.throws(()=>parseIntake(JSON.stringify(data)),/INVALID_S1_INTAKE/);
});
test('unverified WCS, lineage, response and independence retain explicit limits', () => {
  const data=fixture(); data.astrometry={status:'HEADER_ONLY',frame:'ICRS',solutionSha256:null};
  data.processing={lineage:'UNKNOWN',journalSha256:null,measurementAlterations:['UNKNOWN']};
  data.passband.responseSha256=null; data.independentEvidence[0].independence='UNVERIFIED';
  const result=inspectIntake(parseIntake(JSON.stringify(data)));
  for(const code of ['ASTROMETRY_NOT_VERIFIED','MEASUREMENT_LINEAGE_NOT_VERIFIED','PASSBAND_RESPONSE_UNKNOWN','INDEPENDENT_CONFIRMATION_NOT_ESTABLISHED']) assert.ok(result.reasons.includes(code));
});
test('physical paths, coordinate additions and self-asserted consent reject', () => {
  for(const [key,value] of [['localPath','D:/owner/master.xisf'],['coordinates',{ra:1,dec:2}],['ownerApproved',true],['endpoint','https://evil.example']]) {
    const data=fixture(); data[key]=value; assert.throws(()=>parseIntake(JSON.stringify(data)),/INVALID_S1_INTAKE/);
  }
});
