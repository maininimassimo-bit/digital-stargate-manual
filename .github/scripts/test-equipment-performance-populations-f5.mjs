import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { discoverFromTexts, discoverRepository, INPUTS, parseCsv } from './discover-equipment-performance-populations-f5.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');

function fixture(){return {metadataText:read(INPUTS.metadata),exposureText:read(INPUTS.exposures),summaryText:read(INPUTS.summary)};}

test('repository discovery is genuinely multi-session and preserves accepted LDN 1320 population',()=>{
  const r=discoverRepository();
  assert.ok(r.eligible_populations.length>1,'expected more than one eligible population');
  const ldn=r.eligible_populations.find(p=>p.session_id==='2026-07-14_2026-07-15'&&p.target_name==='LDN 1320'&&p.configuration_id==='QUATTRO200_TOUPTEK294_BIN1'&&p.filter_name==='LPRO');
  assert.ok(ldn,'accepted LDN 1320 population missing');
  assert.equal(ldn.measurement_count,19);
  assert.equal(ldn.statistics.find(s=>s.statistic_type==='MEAN')?.value,7.5995);
  assert.equal(ldn.statistics.find(s=>s.statistic_type==='MINIMUM')?.value,6.78);
  assert.equal(ldn.statistics.find(s=>s.statistic_type==='MAXIMUM')?.value,9.05);
  assert.equal(ldn.statistics.find(s=>s.statistic_type==='SAMPLE_STDDEV')?.value,0.5771);
});

test('currently source-qualified M 27 populations are discovered and unresolved registered M 27 evidence stays excluded',()=>{
  const r=discoverRepository();
  const m27=r.eligible_populations.filter(p=>p.target_name==='M 27'&&p.configuration_id==='C8_QHY695A_BIN1');
  assert.ok(m27.length>0,'no eligible M 27 population discovered');
  assert.ok(m27.some(p=>p.session_id==='2026-08-15_2026-08-16'),'eligible 2026-08-15 M 27 population not discovered');
  assert.ok(r.exclusions.some(e=>e.session_id==='2026-08-14_2026-08-15'&&e.target_name==='M 27'&&e.filter_name==='L-Pro'&&e.reason==='FWHM_SOURCE_VALUE_UNRESOLVED'),'registered M 27 population with unresolved FWHM must remain excluded');
  for(const p of m27){assert.ok(p.measurement_count>0);assert.equal(p.unit_semantics,'SOURCE_NATIVE_UNCALIBRATED');assert.equal(p.angular_calibration_state,'NOT_PROVEN');assert.equal(p.action_authority,'NONE');}
});

test('PARTIAL M 27 session is excluded fail-closed',()=>{
  const r=discoverRepository();
  assert.equal(r.eligible_populations.some(p=>p.session_id==='2026-08-10_2026-08-11'),false);
  assert.ok(r.exclusions.some(e=>e.session_id==='2026-08-10_2026-08-11'&&e.reason==='METADATA_NOT_REGISTERED'));
});

test('unresolved configuration is excluded rather than synthesized',()=>{
  const f=fixture();
  f.metadataText+='\n2099-01-01_2099-01-02,Synthetic Target,TGT-X,1,1,,Scope,Camera,L,1,REGISTERED,source.log,test\n';
  const r=discoverFromTexts(f);
  assert.equal(r.eligible_populations.some(p=>p.session_id==='2099-01-01_2099-01-02'),false);
  assert.ok(r.exclusions.some(e=>e.session_id==='2099-01-01_2099-01-02'&&e.reason==='CONFIGURATION_ID_UNRESOLVED'));
});

test('summary count mismatch excludes the affected population without suppressing valid history',()=>{
  const f=fixture();
  f.summaryText=f.summaryText.replace('2026-07-14_2026-07-15,LDN 1320,LPRO,19,','2026-07-14_2026-07-15,LDN 1320,LPRO,999,');
  const r=discoverFromTexts(f);
  assert.equal(r.eligible_populations.some(p=>p.session_id==='2026-07-14_2026-07-15'&&p.target_name==='LDN 1320'&&p.filter_name==='LPRO'),false);
  assert.ok(r.exclusions.some(e=>e.session_id==='2026-07-14_2026-07-15'&&e.reason==='EXPOSURE_SUMMARY_COUNT_MISMATCH'));
  assert.ok(r.eligible_populations.some(p=>p.target_name==='M 27'),'valid M 27 history was incorrectly suppressed');
});

test('missing FWHM source token excludes only the affected population',()=>{
  const f=fixture();
  f.exposureText=f.exposureText.replaceAll('_FWHM_8.45_','_NOFWHM_8.45_');
  const r=discoverFromTexts(f);
  assert.ok(r.exclusions.some(e=>e.session_id==='2026-07-14_2026-07-15'&&e.reason==='FWHM_SOURCE_VALUE_UNRESOLVED'));
  assert.ok(r.eligible_populations.some(p=>p.target_name==='M 27'));
});

test('discovery is deterministic for unchanged repository inputs',()=>{
  assert.deepEqual(discoverRepository(),discoverRepository());
});

// Regression: imported normalized evidence is reconciled on every discovery.
import { reconcileMetadata } from './discover-equipment-performance-populations-f5.mjs';
const newId='2099-01-01_2099-01-02';
const equipment=[{configuration_id:'SETUP',telescope:'Scope',camera:'Camera',binning:'1'}];
const metrics=()=>({session_id:newId,scientific:{target_name:'Target',source:'nina-log',configuration_id:'SETUP',telescope:'Scope',camera:'Camera',binning:1}});
test('new import becomes eligible without editing manual metadata, deterministically',()=>{
 const reconcile=()=>reconcileMetadata([], [{session_id:newId}],equipment,()=>metrics());
 const rows=reconcile();assert.deepEqual(rows,reconcile());assert.equal(rows[0].metadata_state,'REGISTERED');
 const result=discoverFromTexts({metadataRecords:rows,exposureText:`session_id,target_name,filter_name,frame_type,filename,timestamp,sequence_number,line_number\n${newId},Target,L,LIGHT,image_FWHM_2.5_.fits,2099-01-01T22:00:00Z,1,1`,summaryText:`session_id,target_name,filter_name,image_count\n${newId},Target,L,1`});
 assert.equal(result.eligible_populations.length,1);assert.equal(result.eligible_populations[0].measurements[0].value,2.5);
 assert.ok(result.eligible_populations[0].provenance_refs.some(r=>r.endsWith('normalized/session-metrics.json')));
});
test('manual PARTIAL decisions are preserved and normalized evidence cannot override them',()=>{
 const manual=[{session_id:newId,target_name:'Target',metadata_state:'PARTIAL'}];
 assert.deepEqual(reconcileMetadata(manual,[{session_id:newId}],equipment,()=>metrics()),manual);
});
test('missing, conflicting, wrong-session or untrusted normalized evidence stays unresolved',()=>{
 for(const change of [m=>{m.scientific.camera='Other';},m=>{m.session_id='other';},m=>{m.scientific.source='inferred';},m=>{m.scientific.binning=2;},m=>{delete m.scientific.configuration_id;},m=>{delete m.scientific.target_name;}]){
  const m=metrics();change(m);const rows=reconcileMetadata([],[{session_id:newId}],equipment,()=>m);
  assert.equal(rows[0].metadata_state,'PARTIAL');assert.equal(rows[0].configuration_id,'');
 }
 assert.equal(reconcileMetadata([],[{session_id:newId}],equipment,()=>{throw Error('missing');})[0].metadata_state,'PARTIAL');
});
test('current reconciliation accounts for every historical night and retains legacy decisions',()=>{
 const d=discoverRepository();
 const ids=new Set([...d.eligible_populations,...d.exclusions].map(x=>x.session_id));
 for(const row of parseCsv(read('data/analytics/history/sessions.csv'))) assert.ok(ids.has(row.session_id)); assert.ok(d.eligible_populations.length>=9);
 assert.ok(d.eligible_populations.some(x=>x.session_id==='2026-09-21_2026-09-22'));
 assert.ok(d.exclusions.some(x=>x.session_id==='2026-08-26_2026-08-27'));
});
