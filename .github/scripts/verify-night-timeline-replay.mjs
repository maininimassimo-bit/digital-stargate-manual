import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const projectionPath = process.env.DSG_NIGHT_TIMELINE_REPLAY || path.join(root, 'docs/data/night-timeline-replay.json');
const schemaPath = path.join(root, 'schemas/night-timeline-replay.schema.json');
const parseJsonFile = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const doc = parseJsonFile(projectionPath);
const schema = parseJsonFile(schemaPath);
const fail = m => { throw new Error(`Night Timeline Replay validation FAILED: ${m}`); };

function resolveRef(ref) {
  const prefix = '#/$defs/';
  if (!ref.startsWith(prefix)) fail(`unsupported schema ref ${ref}`);
  const key = ref.slice(prefix.length);
  if (!schema.$defs?.[key]) fail(`unresolved schema ref ${ref}`);
  return schema.$defs[key];
}
function typeMatches(value, type) {
  if (type === 'null') return value === null;
  if (type === 'array') return Array.isArray(value);
  if (type === 'object') return value !== null && typeof value === 'object' && !Array.isArray(value);
  return typeof value === type;
}
function validateSchema(value, rule, loc='$') {
  if (rule.$ref) return validateSchema(value, resolveRef(rule.$ref), loc);
  if (Object.hasOwn(rule, 'const') && value !== rule.const) fail(`${loc}: schema const mismatch`);
  if (rule.enum && !rule.enum.some(x => x === value)) fail(`${loc}: schema enum mismatch`);
  if (rule.type) {
    const types = Array.isArray(rule.type) ? rule.type : [rule.type];
    if (!types.some(t => typeMatches(value, t))) fail(`${loc}: schema type mismatch`);
  }
  if (typeof value === 'string') {
    if (rule.minLength !== undefined && value.length < rule.minLength) fail(`${loc}: schema minLength violation`);
    if (rule.pattern && !(new RegExp(rule.pattern)).test(value)) fail(`${loc}: schema pattern violation`);
  }
  if (Array.isArray(value)) {
    if (rule.minItems !== undefined && value.length < rule.minItems) fail(`${loc}: schema minItems violation`);
    if (rule.maxItems !== undefined && value.length > rule.maxItems) fail(`${loc}: schema maxItems violation`);
    if (rule.uniqueItems) {
      const keys = value.map(x => JSON.stringify(x));
      if (new Set(keys).size !== keys.length) fail(`${loc}: schema uniqueItems violation`);
    }
    if (rule.items) value.forEach((x,i) => validateSchema(x, rule.items, `${loc}[${i}]`));
  }
  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    for (const k of rule.required ?? []) if (!Object.hasOwn(value, k)) fail(`${loc}: missing required property ${k}`);
    if (rule.additionalProperties === false) {
      const allowed = new Set(Object.keys(rule.properties ?? {}));
      for (const k of Object.keys(value)) if (!allowed.has(k)) fail(`${loc}: unexpected property ${k}`);
    }
    for (const [k,r] of Object.entries(rule.properties ?? {})) if (Object.hasOwn(value,k)) validateSchema(value[k], r, `${loc}.${k}`);
  }
}
validateSchema(doc, schema);

const order = {NINA:10,PHD2:20,CLOUDWATCHER:30,SQM:40,EAGLE_HEALTH:50,SESSION_PROJECTION:90};
if (doc.baseline_commit !== '4a4d6b89b374e87ca7f945e7399b7e69f0c9ba87') fail('baseline_commit must bind accepted BKL-040 F1 merge');
if (doc.sessions.length > doc.bounds.max_sessions) fail('session bound exceeded');
const citations = new Set(doc.citations.map(x => `${x.id}@${x.version}`));
const provenance = new Map(doc.provenance_records.map(x => [`${x.id}@${x.version}`, x]));
if (citations.size !== doc.citations.length) fail('duplicate Citation identity');
if (provenance.size !== doc.provenance_records.length) fail('duplicate Provenance identity');
const eventIds = new Set();
let count = 0;
const comparePlaced = (a,b) => new Date(a.event_time_utc).getTime() - new Date(b.event_time_utc).getTime() || a.source_order - b.source_order || a.replay_event_id.localeCompare(b.replay_event_id);
const compareUnplaced = (a,b) => a.source_order - b.source_order || a.replay_event_id.localeCompare(b.replay_event_id);
for (const s of doc.sessions) {
  if (!fs.existsSync(path.join(root, s.source_ref))) fail(`missing session source ${s.source_ref}`);
  const placed = s.events.filter(e => e.temporal_state === 'PLACED');
  const unplaced = s.events.filter(e => e.temporal_state === 'UNPLACED');
  const firstUnplaced = s.events.findIndex(e => e.temporal_state === 'UNPLACED');
  if (firstUnplaced >= 0 && s.events.slice(firstUnplaced).some(e => e.temporal_state === 'PLACED')) fail(`${s.session_id}: UNPLACED evidence interleaves synchronized sequence`);
  for (let i=1;i<placed.length;i++) if (comparePlaced(placed[i-1],placed[i]) > 0) fail(`${s.session_id}: PLACED events violate total replay order`);
  for (let i=1;i<unplaced.length;i++) if (compareUnplaced(unplaced[i-1],unplaced[i]) > 0) fail(`${s.session_id}: UNPLACED evidence violates deterministic order`);
  for (const e of s.events) {
    count++;
    if (eventIds.has(e.replay_event_id)) fail(`duplicate replay_event_id ${e.replay_event_id}`); eventIds.add(e.replay_event_id);
    if (e.source_order !== order[e.source_type]) fail(`${e.replay_event_id}: source_order mismatch`);
    if (e.temporal_state === 'PLACED') {
      if (!e.event_time_utc || !e.source_timestamp_raw) fail(`${e.replay_event_id}: placed event missing timestamp evidence`);
      if (Number.isNaN(Date.parse(e.event_time_utc)) || Number.isNaN(Date.parse(e.source_timestamp_raw))) fail(`${e.replay_event_id}: invalid timestamp`);
      if (!/Z$/.test(e.event_time_utc)) fail(`${e.replay_event_id}: event_time_utc must be canonical UTC`);
      if (new Date(e.event_time_utc).getTime() !== new Date(e.source_timestamp_raw).getTime()) fail(`${e.replay_event_id}: UTC normalization does not preserve source instant`);
    } else {
      if (e.event_time_utc !== null) fail(`${e.replay_event_id}: UNPLACED must have event_time_utc null`);
      if (e.source_timestamp_raw !== null && typeof e.source_timestamp_raw !== 'string') fail(`${e.replay_event_id}: UNPLACED raw timestamp evidence invalid`);
    }
    for (const r of e.citation_refs) if (!citations.has(r)) fail(`${e.replay_event_id}: unresolved citation ${r}`);
    for (const r of e.provenance_refs) {
      const p = provenance.get(r); if (!p) fail(`${e.replay_event_id}: unresolved provenance ${r}`);
      if (p.output_ref !== `replay-event:${e.replay_event_id}`) fail(`${e.replay_event_id}: provenance output mismatch`);
      for (const c of p.citation_refs) if (!e.citation_refs.includes(c)) fail(`${e.replay_event_id}: provenance citation not preserved`);
    }
    if (e.source_type === 'SESSION_PROJECTION') {
      const [file, fragment] = e.source_ref.split('#');
      const src = parseJsonFile(path.join(root, file));
      const field = fragment === 'start_local' ? 'start_local' : fragment === 'end_local' ? 'end_local' : null;
      if (!field) fail(`${e.replay_event_id}: unsupported session projection locator`);
      if (src[field] !== e.source_timestamp_raw) fail(`${e.replay_event_id}: timestamp not exact source evidence`);
    }
  }
}
if (count > doc.bounds.max_events) fail('event bound exceeded');
console.log(`Night Timeline Replay validation PASS: sessions=${doc.sessions.length} events=${count}; schema=2020-12-subset-enforced`);
