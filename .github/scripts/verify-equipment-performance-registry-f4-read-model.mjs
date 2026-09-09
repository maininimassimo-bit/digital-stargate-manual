import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
const schemaPath=path.join(root,'schemas/equipment-performance-registry-f4-read-model.schema.json');
const dataPath=path.join(root,'docs/data/equipment-performance-registry-f4-read-model.json');
const f3Path=path.join(root,'docs/data/equipment-performance-registry-f3.json');
const forbidden=/(performance_rating|health_score|health_state|threshold|ranking|percentile|recommendation|remediation|command_authority|safety_authority)/i;
const fail=(m)=>{throw new Error(`BKL-039 F4 validation failed: ${m}`);};
const read=(p)=>JSON.parse(fs.readFileSync(p,'utf8'));
const exactKeys=(o,keys,label)=>{const got=Object.keys(o).sort();const exp=[...keys].sort();if(JSON.stringify(got)!==JSON.stringify(exp))fail(`${label} fields changed: ${got.join(',')}`);};
const unique=(a)=>new Set(a).size===a.length;

export function validate(doc,{f3=read(f3Path),schema=read(schemaPath)}={}){
  exactKeys(doc,['schema_version','component','authority','action_authority','source_contract','view'],'root');
  if(doc.schema_version!=='1.0'||doc.component!=='DSG.EquipmentPerformanceRegistry.F4.ReadModel'||doc.authority!=='projection'||doc.action_authority!=='NONE')fail('root authority/schema mismatch');
  exactKeys(doc.source_contract,['f3_projection','f4_contract','accepted_f3_merge'],'source_contract');
  if(doc.source_contract.f3_projection!=='docs/data/equipment-performance-registry-f3.json'||doc.source_contract.accepted_f3_merge!=='ce2482aa6b2da62296ebdc221f73f39c1acd3aa2')fail('source contract mismatch');
  const v=doc.view;
  exactKeys(v,['configuration_id','session_id','target_name','filter_name','frame_type','metric_name','unit','unit_semantics','angular_calibration_state','measurement_count','coverage','measurement_method_id','source_record_refs','citation_refs','provenance_refs','measurements','statistics','limitations'],'view');
  const expected={configuration_id:'QUATTRO200_TOUPTEK294_BIN1',session_id:'2026-07-14_2026-07-15',target_name:'LDN 1320',filter_name:'LPRO',frame_type:'LIGHT',metric_name:'FWHM',unit:'NINA_FILENAME_FWHM_SOURCE_UNIT',unit_semantics:'SOURCE_NATIVE_UNCALIBRATED',angular_calibration_state:'NOT_PROVEN',measurement_count:19,coverage:'COMPLETE_FOR_DECLARED_POPULATION',measurement_method_id:'BKL039-F3-FWHM-NINA-FILENAME-EXTRACT-V1'};
  for(const [k,val] of Object.entries(expected))if(v[k]!==val)fail(`view.${k} mismatch`);
  if(!Array.isArray(v.measurements)||v.measurements.length!==19||!Array.isArray(v.statistics)||v.statistics.length!==4)fail('bounded population mismatch');
  if(!Array.isArray(v.source_record_refs)||v.source_record_refs.length!==19||!unique(v.source_record_refs))fail('source lineage must contain 19 unique refs');
  if(!Array.isArray(v.citation_refs)||!v.citation_refs.length||!Array.isArray(v.provenance_refs)||!v.provenance_refs.length)fail('citation/provenance missing');
  if(!Array.isArray(v.limitations)||v.limitations.length!==3||!v.limitations.includes('HISTORICAL_READ_ONLY_PROJECTION_NOT_SAFETY_AUTHORITY'))fail('limitations mismatch');
  const f3m=f3.records.filter(r=>r.semantic_type==='PERFORMANCE_MEASUREMENT').sort((a,b)=>String(a.sequence_number).localeCompare(String(b.sequence_number)));
  const f3s=f3.records.filter(r=>r.semantic_type==='DESCRIPTIVE_PERFORMANCE_STATISTIC');
  for(let i=0;i<19;i++){
    const m=v.measurements[i],src=f3m[i];
    exactKeys(m,['record_id','sequence_number','timestamp','value','source_record_ref'],`measurement[${i}]`);
    if(!src||m.record_id!==src.record_id||m.sequence_number!==src.sequence_number||m.timestamp!==src.timestamp||m.value!==src.value||m.source_record_ref!==src.source_record_refs?.[0])fail(`measurement[${i}] not exact F3 projection`);
    if(v.source_record_refs[i]!==m.source_record_ref)fail(`measurement[${i}] lineage order mismatch`);
  }
  const statMethods={MEAN:'BKL039-F3-FWHM-MEAN-V1',MINIMUM:'BKL039-F3-FWHM-MIN-V1',MAXIMUM:'BKL039-F3-FWHM-MAX-V1',SAMPLE_STDDEV:'BKL039-F3-FWHM-SAMPLE-STDDEV-V1'};
  for(const [i,s] of v.statistics.entries()){
    exactKeys(s,['record_id','statistic_type','value','method_id','sample_count'],`statistic[${i}]`);
    const src=f3s.find(x=>x.statistic_type===s.statistic_type);
    if(!src||!statMethods[s.statistic_type]||s.method_id!==statMethods[s.statistic_type]||s.record_id!==src.record_id||s.value!==src.value||s.sample_count!==src.sample_count)fail(`statistic ${s.statistic_type} not exact F3 projection`);
  }
  if(new Set(v.statistics.map(s=>s.statistic_type)).size!==4)fail('duplicate/missing statistic type');
  if(forbidden.test(JSON.stringify(doc)))fail('forbidden assessment/remediation semantics present');
  if(schema?.additionalProperties!==false||schema?.properties?.view?.additionalProperties!==false)fail('governing schema is not fail-closed');
  return true;
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  validate(read(dataPath));
  console.log('BKL-039 F4 read model validation passed.');
}
