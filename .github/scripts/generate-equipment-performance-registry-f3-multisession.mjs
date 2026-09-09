import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { discoverRepository } from './discover-equipment-performance-populations-f5.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
const outputPath=path.join(root,'docs/data/equipment-performance-registry-f3-multisession.json');
const fail=m=>{throw new Error(`BKL-039 F5 F3 generation failed: ${m}`);};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);

export function buildRegistry(discovery){
  if(discovery?.component!=='DSG.EquipmentPerformanceRegistry.F5.Discovery'||discovery.authority!=='projection'||discovery.action_authority!=='NONE') fail('discovery contract drift');
  const populations=(discovery.eligible_populations??[]).map(p=>({population_id:p.population_id,configuration_id:p.configuration_id,session_id:p.session_id,target_name:p.target_name,filter_name:p.filter_name,frame_type:p.frame_type,metric_name:p.metric_name,unit:p.unit,unit_semantics:p.unit_semantics,angular_calibration_state:p.angular_calibration_state,coverage:'COMPLETE_FOR_DECLARED_POPULATION',authority:'projection',action_authority:'NONE',measurement_method_id:p.measurement_method_id,measurement_count:p.measurement_count,source_metadata_ref:p.source_metadata_ref,citation_refs:p.citation_refs,provenance_refs:p.provenance_refs,source_record_refs:p.source_record_refs,records:[...p.measurements.map(m=>({record_id:`${p.population_id}-M-${m.sequence_number}`,semantic_type:'PERFORMANCE_MEASUREMENT',sequence_number:m.sequence_number,timestamp:m.timestamp,value:m.value,metric_name:p.metric_name,unit:p.unit,unit_semantics:p.unit_semantics,angular_calibration_state:p.angular_calibration_state,method_id:p.measurement_method_id,quality:'SOURCE_RESOLVED',authority:'projection',action_authority:'NONE',source_record_refs:[m.source_record_ref],citation_refs:p.citation_refs,provenance_refs:p.provenance_refs})),...p.statistics.map(s=>({record_id:`${p.population_id}-S-${s.statistic_type}`,semantic_type:'DESCRIPTIVE_PERFORMANCE_STATISTIC',statistic_type:s.statistic_type,value:s.value,sample_count:s.sample_count,metric_name:p.metric_name,unit:p.unit,unit_semantics:p.unit_semantics,angular_calibration_state:p.angular_calibration_state,method_id:s.method_id,coverage:'COMPLETE_FOR_DECLARED_POPULATION',quality:'COMPLETE_FOR_DECLARED_POPULATION',authority:'projection',action_authority:'NONE',source_record_refs:p.source_record_refs,citation_refs:p.citation_refs,provenance_refs:p.provenance_refs}))]}));
  if(populations.length<2) fail('multi-session registry requires >=2 eligible populations');
  return {schema_version:'1.0',component:'DSG.EquipmentPerformanceRegistry.F3.MultiSession',authority:'projection',action_authority:'NONE',source_contract:discovery.source_contract,population_count:populations.length,populations,exclusions:discovery.exclusions};
}
export function generate({write=false}={}){
  const generated=buildRegistry(discoverRepository());
  if(write){fs.writeFileSync(outputPath,`${JSON.stringify(generated,null,2)}\n`,'utf8');return generated;}
  if(!fs.existsSync(outputPath)) fail('generated F3 registry missing; run with --write');
  if(!same(JSON.parse(fs.readFileSync(outputPath,'utf8')),generated)) fail('generated F3 registry stale; run with --write');
  return generated;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const write=process.argv.includes('--write'); const result=generate({write});
  console.log(`BKL-039 F5 F3 multi-session registry ${write?'written':'verified'}: ${result.population_count} population(s).`);
}
