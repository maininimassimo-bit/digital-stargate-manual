import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
export const INPUTS={
  metadata:'data/analytics/metadata/session-scientific-metadata.csv',
  sessions:'data/analytics/history/sessions.csv',
  exposures:'data/analytics/history/target-exposures.csv',
  summary:'data/analytics/history/target-summary.csv',
  contract:'docs/architecture/telemetry/BKL-039-F5-Dynamic-Multi-Session-Equipment-Performance-Registry-Contract.md'
};
const UNIT='NINA_FILENAME_FWHM_SOURCE_UNIT';
const UNIT_SEMANTICS='SOURCE_NATIVE_UNCALIBRATED';
const CALIBRATION='NOT_PROVEN';
const ELIGIBLE_METADATA_STATES=new Set(['REGISTERED','CANONICAL_EVIDENCE']);
const isKnown=value=>{const s=String(value??'').trim();return Boolean(s)&&!['UNKNOWN','UNAVAILABLE','N/A','NULL'].includes(s.toUpperCase());};
const fail=(m)=>{throw new Error(`BKL-039 F5-A discovery failed: ${m}`);};

export function parseCsv(text){
  const src=String(text??'').replace(/^\uFEFF/,'').trim();
  if(!src) return [];
  const lines=[]; let row=[]; let value=''; let quoted=false;
  for(let i=0;i<src.length;i++){
    const c=src[i];
    if(c==='"'){
      if(quoted&&src[i+1]==='"'){value+='"';i++;}
      else quoted=!quoted;
    } else if(c===','&&!quoted){row.push(value);value='';}
    else if((c==='\n'||c==='\r')&&!quoted){
      if(c==='\r'&&src[i+1]==='\n') i++;
      row.push(value); value=''; lines.push(row); row=[];
    } else value+=c;
  }
  row.push(value); lines.push(row);
  const headers=lines.shift().map(x=>x.trim());
  return lines.filter(r=>r.some(x=>x!=='' )).map(r=>Object.fromEntries(headers.map((h,i)=>[h,r[i]??''])));
}

function canonicalFrameType(value){
  const s=String(value??'').trim();
  if(!s) return '';
  const leaf=s.split(/[\\/]/).filter(Boolean).at(-1)??s;
  return leaf.toUpperCase();
}
function extractFwhm(filename){
  const m=String(filename??'').match(/_FWHM_([0-9]+(?:\.[0-9]+)?)(?:_|\.)/);
  if(!m) return null;
  const v=Number(m[1]);
  return Number.isFinite(v)&&v>0?v:null;
}
function round4(v){return Number(v.toFixed(4));}
function key(...parts){return parts.map(v=>String(v??'').trim()).join('\u001f');}
function populationId(p){
  const raw=[p.configuration_id,p.session_id,p.target_name,p.filter_name,p.frame_type,'FWHM'].join('|');
  return `EPR-F5-${Buffer.from(raw,'utf8').toString('base64url')}`;
}
function sortPopulation(a,b){
  return [a.session_id,a.configuration_id,a.target_name,a.filter_name,a.frame_type].join('\u001f').localeCompare([b.session_id,b.configuration_id,b.target_name,b.filter_name,b.frame_type].join('\u001f'));
}

export function discoverFromTexts({metadataText,sessionText,exposureText,summaryText}){
  const metadata=parseCsv(metadataText);
  const sessions=parseCsv(sessionText);
  const exposures=parseCsv(exposureText);
  const summaries=parseCsv(summaryText);
  const summaryMap=new Map(summaries.map(r=>[key(r.session_id,r.target_name,r.filter_name),r]));
  const eligible=[]; const exclusions=[];
  const seenSessionTargets=new Set();
  const explicitSessionIds=new Set(metadata.map(row=>String(row.session_id??'').trim()).filter(Boolean));
  const candidates=[...metadata];
  for(const session of [...sessions].sort((a,b)=>String(a.session_id).localeCompare(String(b.session_id)))){
    const session_id=String(session.session_id??'').trim();
    if(!session_id||explicitSessionIds.has(session_id)) continue;
    const target_name=String(session.target_name??'').trim();
    const configuration_id=String(session.configuration_id??'').trim();
    const source_reference=String(session.source_metrics_path??'').trim();
    const canonical=isKnown(target_name)&&isKnown(configuration_id)&&isKnown(source_reference);
    candidates.push({session_id,target_name,configuration_id,metadata_state:canonical?'CANONICAL_EVIDENCE':'UNREGISTERED',source_reference,metadata_origin:'CANONICAL_SESSION_HISTORY'});
  }

  for(const meta of candidates.sort((a,b)=>String(a.session_id).localeCompare(String(b.session_id))||String(a.target_name).localeCompare(String(b.target_name)))){
    const session_id=String(meta.session_id??'').trim();
    const target_name=String(meta.target_name??'').trim();
    const configuration_id=String(meta.configuration_id??'').trim();
    const metadata_state=String(meta.metadata_state??'').trim().toUpperCase();
    const source_reference=String(meta.source_reference??'').trim();
    const sessionTarget=key(session_id,target_name);
    if(seenSessionTargets.has(sessionTarget)) fail(`duplicate scientific metadata identity for ${session_id}/${target_name}`);
    seenSessionTargets.add(sessionTarget);
    if(!ELIGIBLE_METADATA_STATES.has(metadata_state)){
      exclusions.push({scope:'SESSION',session_id,target_name,reason:'METADATA_NOT_REGISTERED',metadata_state:metadata_state||'UNKNOWN'}); continue;
    }
    if(!configuration_id){exclusions.push({scope:'SESSION',session_id,target_name,reason:'CONFIGURATION_ID_UNRESOLVED'});continue;}
    if(!source_reference){exclusions.push({scope:'SESSION',session_id,target_name,reason:'METADATA_PROVENANCE_UNRESOLVED'});continue;}
    const rows=exposures.filter(r=>String(r.session_id).trim()===session_id&&String(r.target_name).trim()===target_name&&canonicalFrameType(r.frame_type)==='LIGHT');
    if(!rows.length){exclusions.push({scope:'SESSION',session_id,target_name,configuration_id,reason:'NO_LIGHT_EXPOSURES'});continue;}
    const byFilter=new Map();
    for(const r of rows){
      const f=String(r.filter_name??'').trim();
      if(!f){exclusions.push({scope:'EXPOSURE',session_id,target_name,configuration_id,reason:'FILTER_UNRESOLVED',source_log_line:Number(r.line_number)||null});continue;}
      if(!byFilter.has(f))byFilter.set(f,[]); byFilter.get(f).push(r);
    }
    for(const [filter_name,group0] of [...byFilter.entries()].sort(([a],[b])=>a.localeCompare(b))){
      const group=[...group0].sort((a,b)=>String(a.timestamp).localeCompare(String(b.timestamp))||String(a.sequence_number).localeCompare(String(b.sequence_number))||Number(a.line_number)-Number(b.line_number));
      const base={session_id,target_name,configuration_id,filter_name,frame_type:'LIGHT'};
      const summary=summaryMap.get(key(session_id,target_name,filter_name));
      if(!summary){exclusions.push({scope:'POPULATION',...base,reason:'TARGET_SUMMARY_MISSING'});continue;}
      const summaryCount=Number(summary.image_count);
      if(!Number.isInteger(summaryCount)||summaryCount!==group.length){exclusions.push({scope:'POPULATION',...base,reason:'EXPOSURE_SUMMARY_COUNT_MISMATCH',exposure_count:group.length,summary_count:Number.isFinite(summaryCount)?summaryCount:null});continue;}
      const values=[]; let invalid=null;
      for(const r of group){const v=extractFwhm(r.filename);if(v===null){invalid=r;break;}values.push(v);}
      if(invalid){exclusions.push({scope:'POPULATION',...base,reason:'FWHM_SOURCE_VALUE_UNRESOLVED',source_log_line:Number(invalid.line_number)||null});continue;}
      const source_record_refs=group.map(r=>`${INPUTS.exposures}#${session_id}:line=${r.line_number}`);
      if(new Set(source_record_refs).size!==source_record_refs.length) fail(`duplicate source lineage in ${session_id}/${target_name}/${filter_name}`);
      const mean=values.reduce((a,b)=>a+b,0)/values.length;
      const variance=values.length>1?values.reduce((a,b)=>a+(b-mean)**2,0)/(values.length-1):null;
      const p={...base,metric_name:'FWHM',unit:UNIT,unit_semantics:UNIT_SEMANTICS,angular_calibration_state:CALIBRATION,authority:'projection',action_authority:'NONE',measurement_method_id:'BKL039-F3-FWHM-NINA-FILENAME-EXTRACT-V1'};
      p.population_id=populationId(p);
      p.measurement_count=group.length;
      p.population_selector=`session=${session_id};target=${target_name};filter=${filter_name};frame_type=LIGHT`;
      p.source_metadata_ref=source_reference;
      const metadataCitation=meta.metadata_origin==='CANONICAL_SESSION_HISTORY'?INPUTS.sessions:INPUTS.metadata;
      p.citation_refs=[INPUTS.exposures,INPUTS.summary,metadataCitation];
      p.provenance_refs=[INPUTS.contract,source_reference];
      p.source_record_refs=source_record_refs;
      p.measurements=group.map((r,i)=>({sequence_number:String(r.sequence_number??''),timestamp:String(r.timestamp??''),value:values[i],source_log_line:Number(r.line_number),source_record_ref:source_record_refs[i]}));
      p.statistics=[
        {statistic_type:'MEAN',value:round4(mean),method_id:'BKL039-F3-FWHM-MEAN-V1',sample_count:values.length},
        {statistic_type:'MINIMUM',value:Math.min(...values),method_id:'BKL039-F3-FWHM-MIN-V1',sample_count:values.length},
        {statistic_type:'MAXIMUM',value:Math.max(...values),method_id:'BKL039-F3-FWHM-MAX-V1',sample_count:values.length},
        ...(variance===null?[]:[{statistic_type:'SAMPLE_STDDEV',value:round4(Math.sqrt(variance)),method_id:'BKL039-F3-FWHM-SAMPLE-STDDEV-V1',sample_count:values.length}])
      ];
      eligible.push(p);
    }
  }
  eligible.sort(sortPopulation);
  exclusions.sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b)));
  const sourceSessionIds=[...new Set(sessions.map(row=>String(row.session_id??'').trim()).filter(Boolean))].sort();
  const accountedSessionIds=[...new Set([...eligible,...exclusions].map(row=>String(row.session_id??'').trim()).filter(Boolean))].sort();
  const missing=sourceSessionIds.filter(id=>!accountedSessionIds.includes(id));
  if(missing.length) fail(`unaccounted canonical session(s): ${missing.join(', ')}`);
  return {schema_version:'0.2',component:'DSG.EquipmentPerformanceRegistry.F5.Discovery',authority:'projection',action_authority:'NONE',source_contract:{scientific_metadata:INPUTS.metadata,canonical_sessions:INPUTS.sessions,target_exposures:INPUTS.exposures,target_summary:INPUTS.summary,unit:UNIT,unit_semantics:UNIT_SEMANTICS,angular_calibration_state:CALIBRATION},source_session_count:sourceSessionIds.length,accounted_session_count:accountedSessionIds.length,eligible_populations:eligible,exclusions};
}

export function discoverRepository(){
  const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
  return discoverFromTexts({metadataText:read(INPUTS.metadata),sessionText:read(INPUTS.sessions),exposureText:read(INPUTS.exposures),summaryText:read(INPUTS.summary)});
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const result=discoverRepository();
  if(process.argv.includes('--json')) process.stdout.write(`${JSON.stringify(result,null,2)}\n`);
  else {
    if(result.eligible_populations.length<2) fail(`multi-session discovery expected >=2 populations, got ${result.eligible_populations.length}`);
    console.log(`BKL-039 F5-A discovery OK: ${result.eligible_populations.length} eligible population(s), ${result.exclusions.length} exclusion(s), ${result.accounted_session_count}/${result.source_session_count} source session(s) accounted.`);
    for(const p of result.eligible_populations) console.log(`ELIGIBLE ${p.session_id} | ${p.target_name} | ${p.configuration_id} | ${p.filter_name} | n=${p.measurement_count}`);
    for(const e of result.exclusions) console.log(`EXCLUDED ${e.session_id||'-'} | ${e.target_name||'-'} | ${e.filter_name||'-'} | ${e.reason}`);
  }
}
