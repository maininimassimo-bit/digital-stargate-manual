import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildRegistry } from './generate-equipment-performance-registry-f3-multisession.mjs';
import { discoverRepository } from './discover-equipment-performance-populations-f5.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)); const root=path.resolve(here,'../..');
const outputPath=path.join(root,'docs/data/equipment-performance-registry-f5-collection.json');
const fail=m=>{throw new Error(`BKL-039 F5-B generation failed: ${m}`);}; const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const limitations=['SOURCE_NATIVE_FWHM_UNIT_IS_NOT_PHYSICALLY_CALIBRATED','NO_EQUIPMENT_HEALTH_RANKING_THRESHOLD_OR_RECOMMENDATION','HISTORICAL_READ_ONLY_PROJECTION_NOT_SAFETY_AUTHORITY'];
export function buildCollection(f3){
  if(f3?.component!=='DSG.EquipmentPerformanceRegistry.F3.MultiSession'||f3.authority!=='projection'||f3.action_authority!=='NONE') fail('F3 authority/component drift');
  const populations=Array.isArray(f3.populations)?f3.populations:fail('F3 populations missing'); if(populations.length<2) fail('multi-population collection requires >=2 populations');
  const views=populations.map(p=>{
    if(p.authority!=='projection'||p.action_authority!=='NONE'||p.unit!=='NINA_FILENAME_FWHM_SOURCE_UNIT'||p.unit_semantics!=='SOURCE_NATIVE_UNCALIBRATED'||p.angular_calibration_state!=='NOT_PROVEN') fail(`${p.population_id} semantic drift`);
    const measurements=p.records.filter(r=>r.semantic_type==='PERFORMANCE_MEASUREMENT').map(r=>({record_id:r.record_id,sequence_number:r.sequence_number,timestamp:r.timestamp,value:r.value,source_record_ref:r.source_record_refs[0]}));
    const statistics=p.records.filter(r=>r.semantic_type==='DESCRIPTIVE_PERFORMANCE_STATISTIC').map(r=>({record_id:r.record_id,statistic_type:r.statistic_type,value:r.value,method_id:r.method_id,sample_count:r.sample_count}));
    if(measurements.length!==p.measurement_count||!statistics.length) fail(`${p.population_id} record population drift`);
    return {population_id:p.population_id,configuration_id:p.configuration_id,session_id:p.session_id,target_name:p.target_name,filter_name:p.filter_name,frame_type:p.frame_type,metric_name:p.metric_name,measurement_count:p.measurement_count,coverage:p.coverage,unit:p.unit,unit_semantics:p.unit_semantics,angular_calibration_state:p.angular_calibration_state,measurement_method_id:p.measurement_method_id,authority:'projection',action_authority:'NONE',source_record_refs:p.source_record_refs,citation_refs:p.citation_refs,provenance_refs:p.provenance_refs,measurements,statistics,limitations};
  });
  return {schema_version:'1.0',component:'DSG.EquipmentPerformanceRegistry.F5.CollectionReadModel',authority:'projection',action_authority:'NONE',source_contract:{f3_projection:'docs/data/equipment-performance-registry-f3-multisession.json',f5_contract:'docs/architecture/telemetry/BKL-039-F5-Dynamic-Multi-Session-Equipment-Performance-Registry-Contract.md'},population_count:views.length,views,exclusions:f3.exclusions};
}
export function generate({write=false}={}){const generated=buildCollection(buildRegistry(discoverRepository())); if(write){fs.writeFileSync(outputPath,`${JSON.stringify(generated,null,2)}\n`,'utf8');return generated;} if(!fs.existsSync(outputPath))fail('generated collection missing; run with --write'); if(!same(JSON.parse(fs.readFileSync(outputPath,'utf8')),generated))fail('generated collection stale; run with --write'); return generated;}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){const write=process.argv.includes('--write');const result=generate({write});console.log(`BKL-039 F5-B collection ${write?'written':'verified'}: ${result.population_count} population(s).`);}
