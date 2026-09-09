import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const projectionPath=process.env.BKL039_F3_PROJECTION||'docs/data/equipment-performance-registry-f3.json';
const exposurePath='data/analytics/history/target-exposures.csv';
const summaryPath='data/analytics/history/target-summary.csv';
const f2Path='docs/data/equipment-performance-registry-f2-fixture.json';
const SESSION='2026-07-14_2026-07-15', CONFIG='QUATTRO200_TOUPTEK294_BIN1', TARGET='LDN 1320', FILTER='LPRO', UNIT='NINA_FILENAME_FWHM_SOURCE_UNIT';
function fail(m){throw new Error(`BKL-039 F3 validation failed: ${m}`);} function read(p){return fs.readFileSync(path.join(root,p),'utf8');}
function csv(text){const lines=text.replace(/^\uFEFF/,'').trim().split(/\r?\n/),h=lines[0].split(',');return lines.slice(1).map(line=>{const v=[];let x='',q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){x+='"';i++;}else q=!q;}else if(c===','&&!q){v.push(x);x='';}else x+=c;}v.push(x);return Object.fromEntries(h.map((k,i)=>[k,v[i]??'']));});}
function fwhm(name){const m=name.match(/_FWHM_([0-9]+(?:\.[0-9]+)?)(?:_|\.)/);if(!m)fail('source FWHM token missing');return Number(m[1]);}
function existsRef(ref){return fs.existsSync(path.join(root,ref.split('#')[0]));}
const p=JSON.parse(read(projectionPath));
const top=new Set(['schema_version','component','authority','action_authority','source_contract','records']);for(const k of Object.keys(p))if(!top.has(k))fail(`unexpected top-level field ${k}`);
if(p.schema_version!=='1.1'||p.component!=='DSG.EquipmentPerformanceRegistry.F3'||p.authority!=='projection'||p.action_authority!=='NONE')fail('projection authority/version boundary changed');
const sc=p.source_contract||{}; const expectedSC={f2_fixture:f2Path,target_exposures:exposurePath,target_summary:summaryPath,configuration_id:CONFIG,session_id:SESSION,target_name:TARGET,filter_name:FILTER,frame_type:'LIGHT',unit:UNIT,unit_semantics:'SOURCE_NATIVE_UNCALIBRATED',angular_calibration_state:'NOT_PROVEN'};
if(JSON.stringify(sc)!==JSON.stringify(expectedSC))fail('source contract changed');
const f2=JSON.parse(read(f2Path));if(!f2.records.some(r=>r.semantic_type==='EQUIPMENT_USAGE_OBSERVATION'&&r.configuration_id===CONFIG&&r.session_id===SESSION))fail('F2-A binding missing');
const rows=csv(read(exposurePath)).filter(r=>r.session_id===SESSION&&r.target_name===TARGET&&r.filter_name===FILTER&&r.frame_type.endsWith('LIGHT'));
const summary=csv(read(summaryPath)).find(r=>r.session_id===SESSION&&r.target_name===TARGET&&r.filter_name===FILTER);if(!summary||Number(summary.image_count)!==19||rows.length!==19)fail('declared population is not exactly 19 source rows');
const measurements=p.records.filter(r=>r.semantic_type==='PERFORMANCE_MEASUREMENT'),stats=p.records.filter(r=>r.semantic_type==='DESCRIPTIVE_PERFORMANCE_STATISTIC');if(p.records.length!==23||measurements.length!==19||stats.length!==4)fail('projection must contain 19 measurements and 4 statistics');
const forbidden=['performance_rating','health','health_state','threshold','rank','ranking','anomaly','prediction','recommendation','remediation'];
const ids=new Set();
for(const r of p.records){if(!r.record_id||ids.has(r.record_id))fail('missing/duplicate record_id');ids.add(r.record_id);for(const k of Object.keys(r))if(forbidden.includes(k))fail(`forbidden field ${k}`);if(r.configuration_id!==CONFIG||r.session_id!==SESSION||r.target_name!==TARGET||r.filter_name!==FILTER||r.metric_name!=='FWHM')fail(`${r.record_id} identity/population changed`);if(r.unit!==UNIT||r.unit_semantics!=='SOURCE_NATIVE_UNCALIBRATED'||r.angular_calibration_state!=='NOT_PROVEN')fail(`${r.record_id} unit/calibration overclaim`);if(r.authority!=='projection'||r.action_authority!=='NONE')fail(`${r.record_id} authority changed`);for(const g of ['source_record_refs','citation_refs','provenance_refs','explanation_codes'])if(!Array.isArray(r[g])||!r[g].length)fail(`${r.record_id} missing ${g}`);for(const g of ['source_record_refs','citation_refs','provenance_refs'])for(const ref of r[g])if(!existsRef(ref))fail(`${r.record_id} unresolved ${g}: ${ref}`);}
const expectedSeq=Array.from({length:19},(_,i)=>String(i).padStart(4,'0'));const values=[];
for(let i=0;i<19;i++){const r=measurements[i],s=rows[i],v=fwhm(s.filename);values.push(v);if(r.sequence_number!==expectedSeq[i]||r.source_log_line!==Number(s.line_number)||r.timestamp!==s.timestamp||r.value!==v)fail(`${r.record_id} does not match source row`);if(r.method_id!=='DSG-F3-FWHM-NINA-FILENAME-EXTRACT-V1'||r.quality!=='SOURCE_RESOLVED')fail(`${r.record_id} measurement method/quality changed`);}
const mean=values.reduce((a,b)=>a+b,0)/values.length, variance=values.reduce((a,b)=>a+(b-mean)**2,0)/(values.length-1);const expected={MEAN:[mean,'DSG-F3-FWHM-MEAN-V1'],MINIMUM:[Math.min(...values),'DSG-F3-FWHM-MIN-V1'],MAXIMUM:[Math.max(...values),'DSG-F3-FWHM-MAX-V1'],SAMPLE_STDDEV:[Math.sqrt(variance),'DSG-F3-FWHM-SAMPLE-STDDEV-V1']};
for(const r of stats){const e=expected[r.statistic_type];if(!e)fail('unsupported statistic type');if(Math.abs(r.value-e[0])>1e-12||r.method_id!==e[1])fail(`${r.record_id} statistic mismatch`);if(r.sample_count!==19||r.coverage!=='COMPLETE_FOR_DECLARED_POPULATION'||r.quality!=='COMPLETE_FOR_DECLARED_POPULATION')fail(`${r.record_id} sample/coverage mismatch`);if(r.population_selector!==`session=${SESSION};target=${TARGET};filter=${FILTER};frame_type=LIGHT`)fail(`${r.record_id} population selector changed`);}
console.log('BKL-039 F3 descriptive projection verification OK');
