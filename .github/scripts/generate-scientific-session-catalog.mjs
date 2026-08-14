import { readFile, writeFile } from 'node:fs/promises';
import process from 'node:process';

const SESSIONS_PATH = 'data/analytics/history/sessions.csv';
const TARGETS_PATH = 'data/analytics/history/targets.csv';
const METADATA_PATH = 'data/analytics/metadata/session-scientific-metadata.csv';
const OUTPUT_PATH = 'docs/data/scientific-session-catalog.json';

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const parseCsv = (text) => {
  const rows=[]; let row=[]; let field=''; let quoted=false; const source=text.replace(/^\uFEFF/,'');
  for(let i=0;i<source.length;i+=1){const ch=source[i]; if(quoted){if(ch==='"'&&source[i+1]==='"'){field+='"';i+=1;}else if(ch==='"'){quoted=false;}else field+=ch;}else if(ch==='"')quoted=true;else if(ch===','){row.push(field);field='';}else if(ch==='\n'){row.push(field.replace(/\r$/,''));if(row.some(v=>v!==''))rows.push(row);row=[];field='';}else field+=ch;}
  if(field.length||row.length){row.push(field.replace(/\r$/,''));if(row.some(v=>v!==''))rows.push(row);} assert(rows.length>0,'CSV is empty'); const headers=rows[0]; return rows.slice(1).map(values=>Object.fromEntries(headers.map((h,i)=>[h,values[i]??''])));
};
const numberOrNull=(value)=>{const text=String(value??'').trim();if(!text)return null;const parsed=Number(text);return Number.isFinite(parsed)?parsed:null;};
const valueOrNull=(value)=>{const text=String(value??'').trim();return text||null;};
const analyticsQuality=(severity)=>{const n=String(severity||'').trim().toUpperCase();if(n==='GREEN')return 'VALIDATED_ANALYTICS';if(['RED','AMBER','YELLOW'].includes(n))return 'ATTENTION_REQUIRED';return 'UNKNOWN';};
const chooseTarget=(targets)=>targets.length?[...targets].sort((a,b)=>(numberOrNull(b.integration_hours)??0)-(numberOrNull(a.integration_hours)??0))[0]:null;
const isKnown=(value)=>{const v=String(value??'').trim().toUpperCase();return Boolean(v)&&v!=='UNKNOWN'&&v!=='N/A';};
const metadataQuality=(record)=>['target','configurationId','telescope','camera'].every(k=>isKnown(record[k]))?'COMPLETE':'METADATA_INCOMPLETE';

const buildCatalog=(sessions,targets,metadata)=>{
  const targetsBySession=new Map(); for(const target of targets){const id=String(target.session_id||'').trim();if(!id)continue;if(!targetsBySession.has(id))targetsBySession.set(id,[]);targetsBySession.get(id).push(target);}
  const metadataBySession=new Map(metadata.map(row=>[String(row.session_id||'').trim(),row]));
  const outputSessions=sessions.filter(s=>String(s.session_id||'').trim()).sort((a,b)=>String(a.session_id).localeCompare(String(b.session_id))).map(session=>{
    const sessionId=String(session.session_id).trim(); const target=chooseTarget(targetsBySession.get(sessionId)||[]); const governed=metadataBySession.get(sessionId)||{}; const start=valueOrNull(session.session_start);
    const record={sessionId,observationDate:start?start.slice(0,10):sessionId.slice(0,10),start,end:valueOrNull(session.session_end),target:valueOrNull(governed.target_name)??valueOrNull(target?.target_name)??'UNKNOWN',configurationId:valueOrNull(governed.configuration_id)??valueOrNull(session.configuration_id)??'UNKNOWN',telescope:valueOrNull(governed.telescope)??valueOrNull(session.telescope)??valueOrNull(target?.telescope)??'UNKNOWN',camera:valueOrNull(governed.camera)??valueOrNull(session.camera)??'UNKNOWN',filter:valueOrNull(governed.filter_name)??valueOrNull(target?.filter_name)??'UNKNOWN',binning:valueOrNull(governed.binning)??valueOrNull(target?.binning)??'UNKNOWN',gain:numberOrNull(target?.gain),offset:numberOrNull(target?.offset),exposureSeconds:numberOrNull(target?.average_exposure_seconds),integrationHours:numberOrNull(session.integration_hours),targetIntegrationHours:numberOrNull(target?.integration_hours),lightStarted:numberOrNull(session.light_started),lightCompleted:numberOrNull(session.light_completed),completionPct:numberOrNull(session.completion_pct),rmsTotalArcsec:numberOrNull(session.rms_total_arcsec),severity:valueOrNull(session.severity)??'UNKNOWN',analyticsState:analyticsQuality(session.severity),metadataState:valueOrNull(governed.metadata_state)??'UNREGISTERED',transferState:'NOT_REPRESENTED',manifestState:'VERSIONED',evidenceState:valueOrNull(session.source_metrics_path)?'SOURCE_METRICS_AVAILABLE':'UNKNOWN',sourceMetricsPath:valueOrNull(session.source_metrics_path)};
    record.qualityState=metadataQuality(record)==='COMPLETE'?record.analyticsState:'METADATA_INCOMPLETE'; return record;
  });
  return {schemaVersion:'1.1',generatedFrom:[SESSIONS_PATH,TARGETS_PATH,METADATA_PATH],catalogStatus:'VERSIONED_ANALYTICS_PROJECTION',authoritativeNote:'Severity/analyticsState represent analytics outcome. qualityState additionally reflects scientific metadata completeness. Source session records and technical evidence remain authoritative.',sessions:outputSessions};
};
const stableJson=(value)=>`${JSON.stringify(value,null,2)}\n`;
const main=async()=>{const mode=process.argv[2]||'--check';assert(['--check','--write','--print'].includes(mode),`Unsupported mode: ${mode}`);const [sessionsText,targetsText,metadataText]=await Promise.all([readFile(SESSIONS_PATH,'utf8'),readFile(TARGETS_PATH,'utf8'),readFile(METADATA_PATH,'utf8').catch(()=> 'session_id\n')]);const generated=stableJson(buildCatalog(parseCsv(sessionsText),parseCsv(targetsText),parseCsv(metadataText)));if(mode==='--print'){process.stdout.write(generated);return;}if(mode==='--write'){await writeFile(OUTPUT_PATH,generated,'utf8');process.stdout.write(`Generated ${OUTPUT_PATH}.\n`);return;}const current=await readFile(OUTPUT_PATH,'utf8').catch(()=>'');if(current!==generated){process.stderr.write('Scientific session catalog drift detected. Run: node .github/scripts/generate-scientific-session-catalog.mjs --write\n');process.exitCode=1;return;}process.stdout.write('Scientific session catalog is aligned with analytics history and governed metadata.\n');};
main().catch(error=>{console.error(error.message);process.exitCode=1;});
