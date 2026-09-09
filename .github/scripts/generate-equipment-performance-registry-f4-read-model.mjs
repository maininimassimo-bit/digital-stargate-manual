import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
const sourcePath=path.join(root,'docs/data/equipment-performance-registry-f3.json');
const outputPath=path.join(root,'docs/data/equipment-performance-registry-f4-read-model.json');
const fail=(m)=>{throw new Error(`BKL-039 F4 generation failed: ${m}`);};
const readJson=(p)=>JSON.parse(fs.readFileSync(p,'utf8'));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);

export function buildReadModel(source){
  if(source?.component!=='DSG.EquipmentPerformanceRegistry.F3') fail('unexpected F3 component');
  if(source?.authority!=='projection'||source?.action_authority!=='NONE') fail('F3 authority boundary changed');
  const sc=source.source_contract??{};
  const expected={configuration_id:'QUATTRO200_TOUPTEK294_BIN1',session_id:'2026-07-14_2026-07-15',target_name:'LDN 1320',filter_name:'LPRO',frame_type:'LIGHT',unit:'NINA_FILENAME_FWHM_SOURCE_UNIT',unit_semantics:'SOURCE_NATIVE_UNCALIBRATED',angular_calibration_state:'NOT_PROVEN'};
  for(const [k,v] of Object.entries(expected)) if(sc[k]!==v) fail(`F3 source_contract.${k} changed`);
  const records=Array.isArray(source.records)?source.records:fail('F3 records missing');
  const measurements=records.filter(r=>r.semantic_type==='PERFORMANCE_MEASUREMENT').sort((a,b)=>String(a.sequence_number).localeCompare(String(b.sequence_number)));
  const stats=records.filter(r=>r.semantic_type==='DESCRIPTIVE_PERFORMANCE_STATISTIC');
  if(measurements.length!==19||stats.length!==4) fail('unexpected F3 population');
  const seqs=Array.from({length:19},(_,i)=>String(i).padStart(4,'0'));
  if(!same(measurements.map(r=>r.sequence_number),seqs)) fail('measurement sequence mismatch');
  const measurementMethod='BKL039-F3-FWHM-NINA-FILENAME-EXTRACT-V1';
  for(const r of measurements){
    if(r.configuration_id!==expected.configuration_id||r.session_id!==expected.session_id||r.target_name!==expected.target_name||r.filter_name!==expected.filter_name) fail(`${r.record_id} population changed`);
    if(r.metric_name!=='FWHM'||r.unit!==expected.unit||r.unit_semantics!==expected.unit_semantics||r.angular_calibration_state!==expected.angular_calibration_state) fail(`${r.record_id} semantics changed`);
    if(r.method_id!==measurementMethod||r.authority!=='projection'||r.action_authority!=='NONE'||r.quality!=='SOURCE_RESOLVED') fail(`${r.record_id} method/authority changed`);
    if(!Array.isArray(r.source_record_refs)||r.source_record_refs.length!==1) fail(`${r.record_id} source lineage changed`);
  }
  const statMethods={MEAN:'BKL039-F3-FWHM-MEAN-V1',MINIMUM:'BKL039-F3-FWHM-MIN-V1',MAXIMUM:'BKL039-F3-FWHM-MAX-V1',SAMPLE_STDDEV:'BKL039-F3-FWHM-SAMPLE-STDDEV-V1'};
  const byType=new Map();
  for(const r of stats){
    if(!statMethods[r.statistic_type]||byType.has(r.statistic_type)) fail('unexpected/duplicate statistic');
    if(r.method_id!==statMethods[r.statistic_type]||r.sample_count!==19||r.coverage!=='COMPLETE_FOR_DECLARED_POPULATION'||r.quality!=='COMPLETE_FOR_DECLARED_POPULATION') fail(`${r.statistic_type} contract changed`);
    if(r.unit!==expected.unit||r.unit_semantics!==expected.unit_semantics||r.angular_calibration_state!==expected.angular_calibration_state||r.authority!=='projection'||r.action_authority!=='NONE') fail(`${r.statistic_type} semantics changed`);
    if(!Array.isArray(r.source_record_refs)||r.source_record_refs.length!==19) fail(`${r.statistic_type} lineage changed`);
    byType.set(r.statistic_type,r);
  }
  for(const k of Object.keys(statMethods)) if(!byType.has(k)) fail(`missing statistic ${k}`);
  const citationRefs=[...new Set(records.flatMap(r=>r.citation_refs??[]))].sort();
  const provenanceRefs=[...new Set(records.flatMap(r=>r.provenance_refs??[]))].sort();
  if(!citationRefs.length||!provenanceRefs.length) fail('citation/provenance missing');
  const sourceRefs=measurements.map(r=>r.source_record_refs[0]);
  return {
    schema_version:'1.0',component:'DSG.EquipmentPerformanceRegistry.F4.ReadModel',authority:'projection',action_authority:'NONE',
    source_contract:{f3_projection:'docs/data/equipment-performance-registry-f3.json',f4_contract:'docs/architecture/telemetry/BKL-039-F4-Equipment-Performance-Read-Only-Consumer-Contract.md',accepted_f3_merge:'ce2482aa6b2da62296ebdc221f73f39c1acd3aa2'},
    view:{configuration_id:expected.configuration_id,session_id:expected.session_id,target_name:expected.target_name,filter_name:expected.filter_name,frame_type:expected.frame_type,metric_name:'FWHM',unit:expected.unit,unit_semantics:expected.unit_semantics,angular_calibration_state:expected.angular_calibration_state,measurement_count:19,coverage:'COMPLETE_FOR_DECLARED_POPULATION',measurement_method_id:measurementMethod,source_record_refs:sourceRefs,citation_refs:citationRefs,provenance_refs:provenanceRefs,
      measurements:measurements.map(r=>({record_id:r.record_id,sequence_number:r.sequence_number,timestamp:r.timestamp,value:r.value,source_record_ref:r.source_record_refs[0]})),
      statistics:['MEAN','MINIMUM','MAXIMUM','SAMPLE_STDDEV'].map(type=>{const r=byType.get(type);return{record_id:r.record_id,statistic_type:type,value:r.value,method_id:r.method_id,sample_count:r.sample_count};}),
      limitations:['SOURCE_NATIVE_FWHM_UNIT_IS_NOT_PHYSICALLY_CALIBRATED','NO_EQUIPMENT_HEALTH_RANKING_THRESHOLD_OR_RECOMMENDATION','HISTORICAL_READ_ONLY_PROJECTION_NOT_SAFETY_AUTHORITY']}
  };
}

export function generate({write=false}={}){
  const generated=buildReadModel(readJson(sourcePath));
  const text=`${JSON.stringify(generated,null,2)}\n`;
  if(write){fs.writeFileSync(outputPath,text,'utf8');return generated;}
  if(!fs.existsSync(outputPath)) fail('generated read model missing; run with --write');
  if(!same(readJson(outputPath),generated)) fail('generated read model is stale; run with --write');
  return generated;
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const write=process.argv.includes('--write');
  generate({write});
  console.log(`BKL-039 F4 read model ${write?'written':'verified'}.`);
}
