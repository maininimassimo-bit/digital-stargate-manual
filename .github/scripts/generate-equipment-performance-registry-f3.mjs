import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const exposurePath='data/analytics/history/target-exposures.csv';
const summaryPath='data/analytics/history/target-summary.csv';
const f2Path='docs/data/equipment-performance-registry-f2-fixture.json';
const outputPath='docs/data/equipment-performance-registry-f3.json';
const contractPath='docs/architecture/telemetry/BKL-039-F3-Descriptive-Performance-Measurement-and-Aggregation-Contract.md';
const SESSION='2026-07-14_2026-07-15';
const CONFIG='QUATTRO200_TOUPTEK294_BIN1';
const TARGET='LDN 1320';
const FILTER='LPRO';
const UNIT='NINA_FILENAME_FWHM_SOURCE_UNIT';
const POPULATION=`session=${SESSION};target=${TARGET};filter=${FILTER};frame_type=LIGHT`;

function fail(message){ throw new Error(`BKL-039 F3 generation failed: ${message}`); }
function read(rel){ return fs.readFileSync(path.join(root,rel),'utf8'); }
function csv(text){
  const lines=text.replace(/^\uFEFF/,'').trim().split(/\r?\n/); const headers=lines[0].split(',');
  return lines.slice(1).map(line=>{ const values=[]; let value=''; let quoted=false;
    for(let i=0;i<line.length;i++){ const c=line[i]; if(c==='"'){ if(quoted&&line[i+1]==='"'){value+='"';i++;}else quoted=!quoted; } else if(c===','&&!quoted){values.push(value);value='';}else value+=c; }
    values.push(value); return Object.fromEntries(headers.map((h,i)=>[h,values[i]??''])); });
}
function extractFwhm(filename){ const m=filename.match(/_FWHM_([0-9]+(?:\.[0-9]+)?)(?:_|\.)/); if(!m) fail(`missing FWHM token in ${filename}`); const v=Number(m[1]); if(!Number.isFinite(v)||v<=0) fail(`invalid FWHM token in ${filename}`); return v; }
function round(value){ return Number(value.toFixed(12)); }
function canonicalize(value){
  if(Array.isArray(value)) return value.map(canonicalize);
  if(value && typeof value==='object'){
    return Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonicalize(value[key])]));
  }
  return value;
}

const f2=JSON.parse(read(f2Path));
const usage=f2.records.find(r=>r.semantic_type==='EQUIPMENT_USAGE_OBSERVATION'&&r.session_id===SESSION&&r.configuration_id===CONFIG);
if(!usage) fail('accepted F2-A session/configuration binding not found');
const exposures=csv(read(exposurePath)).filter(r=>r.session_id===SESSION&&r.target_name===TARGET&&r.filter_name===FILTER&&r.frame_type.endsWith('LIGHT'));
const summary=csv(read(summaryPath)).find(r=>r.session_id===SESSION&&r.target_name===TARGET&&r.filter_name===FILTER);
if(!summary) fail('target summary population not found');
if(Number(summary.image_count)!==exposures.length) fail(`population mismatch summary=${summary.image_count} exposures=${exposures.length}`);
if(exposures.length!==19) fail(`bounded population changed: ${exposures.length}`);
const sequences=exposures.map(r=>r.sequence_number);
if(sequences.join(',')!==Array.from({length:19},(_,i)=>String(i).padStart(4,'0')).join(',')) fail('bounded sequence is not exactly 0000..0018');
const values=exposures.map(r=>extractFwhm(r.filename));
const mean=values.reduce((a,b)=>a+b,0)/values.length;
const variance=values.reduce((a,b)=>a+(b-mean)**2,0)/(values.length-1);
const sourceRefs=exposures.map(r=>`${exposurePath}#${SESSION}:line=${r.line_number}`);
const common={configuration_id:CONFIG,session_id:SESSION,target_name:TARGET,filter_name:FILTER,metric_name:'FWHM',unit:UNIT,unit_semantics:'SOURCE_NATIVE_UNCALIBRATED',angular_calibration_state:'NOT_PROVEN',citation_refs:[exposurePath,summaryPath],provenance_refs:[contractPath,f2Path],authority:'projection',action_authority:'NONE'};
const records=exposures.map((r,i)=>({record_id:`EPR-F3-FWHM-${SESSION}-${r.sequence_number}`,semantic_type:'PERFORMANCE_MEASUREMENT',...common,value:values[i],method_id:'DSG-F3-FWHM-NINA-FILENAME-EXTRACT-V1',timestamp:r.timestamp,source_log_line:Number(r.line_number),sequence_number:r.sequence_number,source_record_refs:[sourceRefs[i]],quality:'SOURCE_RESOLVED',explanation_codes:['FWHM_TOKEN_EXTRACTED_FROM_REPOSITORY_EXPOSURE_FILENAME','ANGULAR_CALIBRATION_NOT_PROVEN']}));
const stats=[
  ['MEAN',mean,'DSG-F3-FWHM-MEAN-V1'],
  ['MINIMUM',Math.min(...values),'DSG-F3-FWHM-MIN-V1'],
  ['MAXIMUM',Math.max(...values),'DSG-F3-FWHM-MAX-V1'],
  ['SAMPLE_STDDEV',Math.sqrt(variance),'DSG-F3-FWHM-SAMPLE-STDDEV-V1']
].map(([type,value,method])=>({record_id:`EPR-F3-FWHM-${SESSION}-${type}`,semantic_type:'DESCRIPTIVE_PERFORMANCE_STATISTIC',...common,statistic_type:type,value:round(value),method_id:method,sample_count:values.length,population_selector:POPULATION,coverage:'COMPLETE_FOR_DECLARED_POPULATION',source_record_refs:sourceRefs,quality:'COMPLETE_FOR_DECLARED_POPULATION',explanation_codes:['DESCRIPTIVE_STATISTIC_ONLY','NO_HEALTH_OR_RANKING_SEMANTICS','ANGULAR_CALIBRATION_NOT_PROVEN']}));
const projection={schema_version:'1.1',component:'DSG.EquipmentPerformanceRegistry.F3',authority:'projection',action_authority:'NONE',source_contract:{f2_fixture:f2Path,target_exposures:exposurePath,target_summary:summaryPath,configuration_id:CONFIG,session_id:SESSION,target_name:TARGET,filter_name:FILTER,frame_type:'LIGHT',unit:UNIT,unit_semantics:'SOURCE_NATIVE_UNCALIBRATED',angular_calibration_state:'NOT_PROVEN'},records:[...records,...stats]};
const rendered=JSON.stringify(projection,null,2)+'\n';
if(process.argv.includes('--write')){
  fs.writeFileSync(path.join(root,outputPath),rendered);
  console.log(`Wrote ${outputPath}`);
}else if(process.argv.includes('--check')){
  if(!fs.existsSync(path.join(root,outputPath))) fail('generated projection is missing; run with --write');
  let existing;
  try { existing=JSON.parse(read(outputPath)); } catch(error) { fail(`generated projection is not valid JSON: ${error.message}`); }
  if(JSON.stringify(canonicalize(existing))!==JSON.stringify(canonicalize(projection))) fail('generated projection is stale; run with --write');
  console.log('BKL-039 F3 generated projection check OK');
}else process.stdout.write(rendered);
