import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const fixturePath = process.env.DSG_ANOMALY_TREND_FIXTURE || path.join(root, 'docs/data/anomaly-trend-f2-fixture.json');
const schemaPath = path.join(root, 'schemas/anomaly-trend-analytical-record.schema.json');
const replayPath = path.join(root, 'docs/data/night-timeline-replay-f3.json');
const read = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const doc = read(fixturePath); const schema = read(schemaPath); const replay = read(replayPath);
const fail = m => { throw new Error(`BKL-038 F2 validation FAILED: ${m}`); };

function resolveRef(ref) { const p='#/$defs/'; if (!ref.startsWith(p)) fail(`unsupported schema ref ${ref}`); const r=schema.$defs?.[ref.slice(p.length)]; if (!r) fail(`unresolved schema ref ${ref}`); return r; }
function typeMatches(v,t){ if(t==='null')return v===null;if(t==='array')return Array.isArray(v);if(t==='object')return v!==null&&typeof v==='object'&&!Array.isArray(v);return typeof v===t; }
function validate(v,r,loc='$'){
  if(r.$ref)return validate(v,resolveRef(r.$ref),loc);
  if(Object.hasOwn(r,'const')&&v!==r.const)fail(`${loc}: const mismatch`);
  if(r.enum&&!r.enum.some(x=>x===v))fail(`${loc}: enum mismatch`);
  if(r.type){const ts=Array.isArray(r.type)?r.type:[r.type];if(!ts.some(t=>typeMatches(v,t)))fail(`${loc}: type mismatch`);}
  if(typeof v==='string'&&r.minLength!==undefined&&v.length<r.minLength)fail(`${loc}: minLength`);
  if(Array.isArray(v)){if(r.minItems!==undefined&&v.length<r.minItems)fail(`${loc}: minItems`);if(r.uniqueItems&&new Set(v.map(JSON.stringify)).size!==v.length)fail(`${loc}: uniqueItems`);if(r.items)v.forEach((x,i)=>validate(x,r.items,`${loc}[${i}]`));}
  if(v!==null&&typeof v==='object'&&!Array.isArray(v)){for(const k of r.required??[])if(!Object.hasOwn(v,k))fail(`${loc}: missing ${k}`);if(r.additionalProperties===false){const a=new Set(Object.keys(r.properties??{}));for(const k of Object.keys(v))if(!a.has(k))fail(`${loc}: unexpected ${k}`);}for(const[k,x]of Object.entries(r.properties??{}))if(Object.hasOwn(v,k))validate(v[k],x,`${loc}.${k}`);}
}
validate(doc,schema);
if(doc.baseline_commit!=='0a91e280d86cbcb7272d88c1c68f282d00272823')fail('fixture must bind accepted BKL-038 F1 merge');
const replayEvents=new Map(replay.events.map(e=>[`replay-event:${e.replay_event_id}`,e]));
const replayCorrelations=new Map(replay.correlations.map(c=>[`${c.left_event_ref}|${c.right_event_ref}`,c]));
const citations=new Set(replay.citations.map(x=>`${x.id}@${x.version}`));
const provenance=new Set(replay.provenance_records.map(x=>`${x.id}@${x.version}`));
const ids=new Set();
for(const r of doc.records){
  if(ids.has(r.derived_record_id))fail(`duplicate derived id ${r.derived_record_id}`);ids.add(r.derived_record_id);
  for(const s of r.source_record_refs)if(!replayEvents.has(s))fail(`${r.derived_record_id}: unresolved source ${s}`);
  for(const c of r.citation_refs)if(!citations.has(c))fail(`${r.derived_record_id}: unresolved citation ${c}`);
  for(const p of r.provenance_refs)if(!provenance.has(p))fail(`${r.derived_record_id}: unresolved provenance ${p}`);
  if(r.semantic_type==='TREND_MEASUREMENT'){
    if(!r.measurement?.descriptive_only)fail(`${r.derived_record_id}: F2 trend must remain descriptive_only`);
    if(r.candidate_state!==null||r.rule_id!==null)fail(`${r.derived_record_id}: descriptive trend cannot self-promote to anomaly`);
  }
  if(r.semantic_type==='ANOMALY_CANDIDATE'){
    if(r.candidate_state==='OBSERVED_RULE_MATCH'&&!r.rule_id)fail(`${r.derived_record_id}: governed rule_id required`);
    if(!['OBSERVED_RULE_MATCH','DATA_QUALITY_EXCEPTION','NOT_ASSESSED','UNSUPPORTED'].includes(r.candidate_state))fail(`${r.derived_record_id}: invalid candidate state`);
  }
  if(r.semantic_type==='CORRELATION_CANDIDATE'){
    if(r.candidate_state!=='NOT_ASSESSED')fail(`${r.derived_record_id}: bounded F2 correlation must remain NOT_ASSESSED`);
    if(!r.explanation_codes.includes('CAUSATION_NOT_INFERRED'))fail(`${r.derived_record_id}: causation guard missing`);
  }
  if(r.action_authority!=='NONE'||r.authority!=='projection')fail(`${r.derived_record_id}: authority boundary violated`);
}
const trend=doc.records.find(r=>r.derived_record_id==='AT-F2-TREND-CW-TO-NINA-DELTA');
if(!trend)fail('required exact-delta trend record missing');
const acceptedCorrelation=replayCorrelations.get(`${trend.source_record_refs[0]}|${trend.source_record_refs[1]}`);
if(!acceptedCorrelation)fail('accepted BKL-040 correlation evidence for exact delta is missing');
if(acceptedCorrelation.classification_method_id!=='BKL040-F3-EXACT-DELTA-1')fail('unexpected upstream exact-delta method');
if(acceptedCorrelation.classification_state!=='NOT_ASSESSED')fail('upstream correlation classification must remain NOT_ASSESSED');
if(trend.measurement.unit!=='ms')fail('exact-delta trend unit must be ms');
if(Math.abs(acceptedCorrelation.delta_ms-trend.measurement.value)>0.000001)fail('exact delta does not match accepted BKL-040 correlation evidence');
console.log(`BKL-038 F2 validation PASS: records=${doc.records.length}; authority=projection; action=NONE; exact_delta_ms=${acceptedCorrelation.delta_ms}`);
