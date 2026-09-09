import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { discoverRepository } from './discover-equipment-performance-populations-f5.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
const outputPath=path.join(root,'docs/data/equipment-performance-registry-f5-collection.json');
const fail=m=>{throw new Error(`BKL-039 F5-B generation failed: ${m}`);};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const limitations=['SOURCE_NATIVE_FWHM_UNIT_IS_NOT_PHYSICALLY_CALIBRATED','NO_EQUIPMENT_HEALTH_RANKING_THRESHOLD_OR_RECOMMENDATION','HISTORICAL_READ_ONLY_PROJECTION_NOT_SAFETY_AUTHORITY'];

export function buildCollection(discovery){
  if(discovery?.component!=='DSG.EquipmentPerformanceRegistry.F5.Discovery'||discovery?.authority!=='projection'||discovery?.action_authority!=='NONE') fail('discovery authority/component drift');
  const populations=Array.isArray(discovery.eligible_populations)?discovery.eligible_populations:fail('eligible populations missing');
  if(populations.length<2) fail('multi-population collection requires at least two eligible populations');
  const views=populations.map(p=>{
    if(p.authority!=='projection'||p.action_authority!=='NONE'||p.unit!=='NINA_FILENAME_FWHM_SOURCE_UNIT'||p.unit_semantics!=='SOURCE_NATIVE_UNCALIBRATED'||p.angular_calibration_state!=='NOT_PROVEN') fail(`${p.population_id} semantic boundary drift`);
    if(!Array.isArray(p.measurements)||p.measurements.length!==p.measurement_count) fail(`${p.population_id} measurement count drift`);
    if(!Array.isArray(p.statistics)||!p.statistics.length) fail(`${p.population_id} statistics missing`);
    return {population_id:p.population_id,configuration_id:p.configuration_id,session_id:p.session_id,target_name:p.target_name,filter_name:p.filter_name,frame_type:p.frame_type,metric_name:p.metric_name,measurement_count:p.measurement_count,coverage:'COMPLETE_FOR_DECLARED_POPULATION',unit:p.unit,unit_semantics:p.unit_semantics,angular_calibration_state:p.angular_calibration_state,measurement_method_id:p.measurement_method_id,authority:'projection',action_authority:'NONE',source_record_refs:p.source_record_refs,citation_refs:p.citation_refs,provenance_refs:p.provenance_refs,measurements:p.measurements,statistics:p.statistics,limitations};
  });
  return {schema_version:'1.0',component:'DSG.EquipmentPerformanceRegistry.F5.CollectionReadModel',authority:'projection',action_authority:'NONE',source_contract:{discovery_contract:'docs/architecture/telemetry/BKL-039-F5-Dynamic-Multi-Session-Equipment-Performance-Registry-Contract.md',scientific_metadata:discovery.source_contract.scientific_metadata,target_exposures:discovery.source_contract.target_exposures,target_summary:discovery.source_contract.target_summary},population_count:views.length,views,exclusions:discovery.exclusions};
}

export function generate({write=false}={}){
  const generated=buildCollection(discoverRepository());
  if(write){fs.writeFileSync(outputPath,`${JSON.stringify(generated,null,2)}\n`,'utf8');return generated;}
  if(!fs.existsSync(outputPath)) fail('generated collection missing; run with --write');
  const current=JSON.parse(fs.readFileSync(outputPath,'utf8'));
  if(!same(current,generated)) fail('generated collection is stale; run with --write');
  return generated;
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const write=process.argv.includes('--write');
  const result=generate({write});
  console.log(`BKL-039 F5-B collection ${write?'written':'verified'}: ${result.population_count} population(s).`);
}
